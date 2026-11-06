"""Certificados por ejecucion (D-14).

(a) Parte 1: cota de dualidad de Lagrange UB(lam) = lam*B + sum_i max_{0<=x<=r_i} [a_i ln(1+x) - lam*x];
    por dualidad debil UB(lam) >= optimo para todo lam >= 0; con lam = ganancia de la ultima unidad la brecha es 0.
(b) Parte 2: cota a posteriori f(S*) <= f(S) + max{ sum_e Delta(e|S) z_e : sum z <= k, sum c z <= L, 0<=z<=1 }
    (LP, scipy/HiGHS). Vale para f monotona submodular y cualquier S factible.
"""
from __future__ import annotations

import math

import numpy as np
from scipy.optimize import linprog

from .allocate import ResultadoReparto
from .model import ganancia_marginal, ganancias_todas, residual_inicial, actualizar_residual, utilidad

TOL = 1e-9


def _max_entero(a: float, lam: float, r: int) -> float:
    """max_{x entero en [0,r]} a ln(1+x) - lam x (funcion concava: basta probar vecinos del optimo continuo). T=O(1)."""
    if r <= 0:
        return 0.0
    if lam <= 0:
        return utilidad(a, r)
    xc = a / lam - 1.0
    cand = {0, r}
    if math.isfinite(xc):
        for x in (math.floor(xc), math.ceil(xc)):
            cand.add(min(max(int(x), 0), r))
    return max(utilidad(a, x) - lam * x for x in cand)


def certificar_reparto(a: list, topes: list, B: int, res: ResultadoReparto) -> dict:
    """Cota de dualidad del reparto. Pre: res es la salida de ``asignar`` para (a, topes, B).

    Pos: dict con lam, cota_superior, utilidad, brecha, ok (brecha<=1e-9 y cota>=utilidad-1e-9). T=O(N).
    """
    n = len(a)
    if res.unidades == B and B > 0:
        lam = res.traza[-1].ganancia            # menor ganancia asignada
    elif res.unidades < B:                      # topes agotados: sobra presupuesto
        lam = 0.0
    else:                                       # B == 0
        lam = max((ganancia_marginal(a[i], 0) for i in range(n) if topes[i] > 0), default=0.0)
    ub = lam * B + sum(_max_entero(a[i], lam, topes[i]) for i in range(n))
    brecha = ub - res.utilidad
    ok = brecha >= -TOL * max(1.0, abs(ub)) and brecha <= TOL * max(1.0, abs(ub))
    return {"lambda": lam, "cota_superior": ub, "utilidad": res.utilidad, "brecha": brecha,
            "tolerancia": TOL, "ok": bool(ok)}


def certificar_seleccion(W, a, c, S: list, cand: np.ndarray, kmax, Lmax, f_S: float) -> dict:
    """Cota a posteriori por LP para la seleccion S (Parte 2).

    Pos: dict con f_S, extra (valor del LP), cota_superior = f_S + extra, razon_certificada = f_S/cota, ok.
    Se omite la restriccion de cardinalidad si kmax>=#candidatos y la de costo si Lmax es infinito.
    T = O(|S| M + N M) para las ganancias + resolver un LP de N variables y <=2 restricciones.
    """
    R = residual_inicial(W.shape[1])
    for i in S:
        actualizar_residual(W, R, i)
    delta = ganancias_todas(W, a, R)
    en_S = set(S)
    idx = [int(i) for i in np.flatnonzero(cand) if int(i) not in en_S and delta[i] > 0]
    if not idx:
        return {"f_S": f_S, "extra": 0.0, "cota_superior": f_S, "razon_certificada": 1.0, "ok": True}
    d = np.array([delta[i] for i in idx])
    A, b = [], []
    if kmax < len(idx):
        A.append(np.ones(len(idx)))
        b.append(float(kmax))                        # |S* \ S| <= |S*| <= kmax
    if math.isfinite(Lmax):
        A.append(np.array([float(c[i]) for i in idx]))
        b.append(float(Lmax))
    kwargs = {"A_ub": np.array(A), "b_ub": np.array(b)} if A else {}
    res = linprog(-d, bounds=(0, 1), method="highs", **kwargs)
    if res.status != 0:
        return {"f_S": f_S, "extra": None, "cota_superior": None, "razon_certificada": None, "ok": False,
                "error": f"linprog status {res.status}: {res.message}"}
    extra = float(-res.fun)
    cota = f_S + extra
    return {"f_S": f_S, "extra": extra, "cota_superior": cota,
            "razon_certificada": f_S / cota if cota > 0 else 1.0, "ok": bool(cota >= f_S - TOL)}
