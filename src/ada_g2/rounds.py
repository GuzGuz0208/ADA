"""Pipeline de T rondas en cadena Parte 2 -> Parte 1 (D-08) con verificacion explicita de restricciones.

Ronda t: disponibles A_t (nodos con tope restante > 0; cada uno falla con prob. q, D-07: q=0 por defecto);
S_t = seleccion (Parte 2) sobre A_t; reparto (Parte 1) de B sobre S_t con topes r_i(t) (D-06).
Politicas de gasto: 'concentrado' (tope = restante) o 'uniforme' (tope = ceil(restante/(T-t+1))).
"""
from __future__ import annotations

import math
import random
import time
from dataclasses import dataclass, field

import numpy as np

from . import certificates as cert
from .allocate import ResultadoReparto, asignar
from .exact import dp_reparto, fuerza_bruta
from .io import Instancia
from .model import f_directa
from .select import MODOS, ResultadoSeleccion, limites, seleccionar

TOL = 1e-9
POLITICAS = ("concentrado", "uniforme")


@dataclass
class Ronda:
    t: int
    disponibles: list            # indices de nodo
    S: list                      # participantes ordenados por indice
    seleccion: ResultadoSeleccion
    f: float
    costo: int
    rem_antes: list              # tope restante por nodo antes de la ronda
    topes: list                  # tope efectivo por nodo (politica)
    reparto: ResultadoReparto
    x: dict                      # indice de nodo -> unidades
    utilidad: float
    verificacion: list = field(default_factory=list)
    cert_reparto: dict = field(default_factory=dict)
    cert_seleccion: dict = field(default_factory=dict)
    exacto: dict | None = None


@dataclass
class Corrida:
    inst: Instancia
    modo: str
    q: float
    politica: str
    seed: int
    rondas: list
    gasto_total: list            # unidades gastadas por nodo en todas las rondas
    verificacion_global: list
    tiempos: dict
    ok: bool = True

    @property
    def f_total(self) -> float:
        return sum(r.f for r in self.rondas)

    @property
    def utilidad_total(self) -> float:
        return sum(r.utilidad for r in self.rondas)


def _chk(nombre: str, descripcion: str, valor, limite, aplica: bool, ok: bool) -> dict:
    return {"restriccion": nombre, "descripcion": descripcion, "valor": valor, "limite": limite,
            "aplica": aplica, "cumple": bool(ok) if aplica else True}


def verificar_ronda(inst: Instancia, modo: str, S: list, x: dict, topes: list, disp: list, rem: list) -> list:
    """Verifica explicitamente las restricciones de una ronda. T=O(N).

    Pre: x[i] definido para i en S. Pos: lista de checks {restriccion, valor, limite, aplica, cumple}.
    """
    sumx = sum(x.values())
    costo = sum(inst.c[i] for i in S)
    viol_tope = [inst.ids[i] for i in S if x[i] > topes[i]]
    viol_rem = [inst.ids[i] for i in S if x[i] > rem[i]]
    return [
        _chk("|S|<=k", "cupo de participantes", len(S), inst.k, modo in ("k", "ambos"), len(S) <= inst.k),
        _chk("sum c<=L", "costo de participacion", costo, inst.L, modo in ("costo", "ambos"), costo <= inst.L),
        _chk("sum x<=B", "presupuesto de ruido de la ronda", sumx, inst.B, True, sumx <= inst.B),
        _chk("x_i<=tope_i", "tope por nodo (politica)", max((x[i] - topes[i] for i in S), default=0), 0,
             True, not viol_tope),
        _chk("x_i<=restante_i", "presupuesto total restante del nodo", viol_rem, [], True, not viol_rem),
        _chk("x_i>=0 entero", "dominio", min(x.values(), default=0), 0, True, all(v >= 0 for v in x.values())),
        _chk("S subconjunto de disponibles", "participantes disponibles", [inst.ids[i] for i in S if i not in disp],
             [], True, set(S) <= set(disp)),
    ]


def ejecutar(inst: Instancia, modo: str = "ambos", q: float = 0.0, seed: int = 20261105,
             politica: str = "concentrado", certificar: bool = True) -> Corrida:
    """Ejecuta las T rondas. Determinista dado (inst, modo, q, seed, politica).

    Pre: modo en MODOS, 0<=q<1, politica en POLITICAS. Pos: Corrida con resultado, tiempos por fase y
    verificacion de restricciones por ronda y global (sum_t x_{i,t} <= R_i).
    T = O(T_rondas * (N*k*M [seleccion] + N + B log N [reparto])) con M=N en el esquema del JSON.
    """
    if modo not in MODOS:
        raise ValueError(f"modo '{modo}' invalido; use {MODOS}")
    if politica not in POLITICAS:
        raise ValueError(f"politica '{politica}' invalida; use {POLITICAS}")
    if not 0.0 <= q < 1.0:
        raise ValueError("q debe estar en [0,1)")
    rng = random.Random(seed)
    n = inst.N
    rem = list(inst.R)
    gasto = [0] * n
    rondas: list = []
    tiempos = {"seleccion": 0.0, "reparto": 0.0, "verificacion": 0.0, "certificados": 0.0}
    t_ini = time.perf_counter()
    for t in range(1, inst.T + 1):
        disp = [i for i in range(n) if rem[i] > 0 and (q <= 0 or rng.random() >= q)]
        mask = np.zeros(n, dtype=bool)
        mask[disp] = True
        t0 = time.perf_counter()
        sel = seleccionar(inst.W, inst.a, inst.c, mask, inst.k, inst.L, modo)
        t1 = time.perf_counter()
        S = sorted(sel.mejor.S)
        if politica == "uniforme":
            topes = [min(rem[i], math.ceil(rem[i] / (inst.T - t + 1))) for i in range(n)]
        else:
            topes = list(rem)
        rep = asignar([float(inst.a[i]) for i in S], [topes[i] for i in S], inst.B)
        t2 = time.perf_counter()
        x = {S[p]: rep.x[p] for p in range(len(S))}
        rem_antes = list(rem)
        r = Ronda(t, disp, S, sel, sel.mejor.f, sum(inst.c[i] for i in S), rem_antes, topes, rep, x, rep.utilidad)
        t3 = time.perf_counter()
        r.verificacion = verificar_ronda(inst, modo, S, x, topes, disp, rem_antes)
        t4 = time.perf_counter()
        if certificar:
            r.cert_reparto = cert.certificar_reparto([float(inst.a[i]) for i in S], [topes[i] for i in S],
                                                     inst.B, rep)
            kmax, Lmax = limites(modo, inst.k, inst.L, len(disp))
            r.cert_seleccion = cert.certificar_seleccion(inst.W, inst.a, inst.c, S, mask, kmax, Lmax, r.f)
        t5 = time.perf_counter()
        f_dir = f_directa(inst.W, inst.a, S)
        r.verificacion.append(_chk("f incremental = f directa", "coherencia numerica", abs(f_dir - r.f), TOL, True,
                                   abs(f_dir - r.f) <= TOL * max(1.0, f_dir)))
        for i in S:
            rem[i] -= x[i]
            gasto[i] += x[i]
        tiempos["seleccion"] += t1 - t0
        tiempos["reparto"] += t2 - t1
        tiempos["verificacion"] += t4 - t3
        tiempos["certificados"] += t5 - t4
        tiempos[f"seleccion_r{t}"] = t1 - t0
        tiempos[f"reparto_r{t}"] = t2 - t1
        rondas.append(r)
    glob = [_chk("sum_t x_it<=R_i", "presupuesto total del nodo en las T rondas",
                 [inst.ids[i] for i in range(n) if gasto[i] > inst.R[i]], [], True,
                 all(gasto[i] <= inst.R[i] for i in range(n)))]
    tiempos["pipeline_total"] = time.perf_counter() - t_ini
    c = Corrida(inst, modo, q, politica, seed, rondas, gasto, glob, tiempos)
    c.ok = all(ch["cumple"] for r in rondas for ch in r.verificacion) and all(ch["cumple"] for ch in glob)
    if certificar:
        c.ok = c.ok and all(r.cert_reparto.get("ok") and r.cert_seleccion.get("ok") for r in rondas)
    return c


def comparar_exacto(corrida: Corrida, max_n: int = 20) -> float:
    """Compara cada ronda con el optimo: fuerza bruta (seleccion) y DP (reparto). Devuelve el tiempo total.

    Pre: corrida ejecutada. Pos: r.exacto = dict por ronda (o None si N>max_n). T = exponencial en N (solo N<=20).
    """
    inst = corrida.inst
    t0 = time.perf_counter()
    if inst.N > max_n:
        return 0.0
    for r in corrida.rondas:
        kmax, Lmax = limites(corrida.modo, inst.k, inst.L, len(r.disponibles))
        ex = fuerza_bruta(inst.W, inst.a, inst.c, r.disponibles, kmax, Lmax)
        a_s = [float(inst.a[i]) for i in r.S]
        if len(r.S) * inst.B * inst.B <= 50_000_000:
            dp_u, _ = dp_reparto(a_s, [r.topes[i] for i in r.S], inst.B)
        else:
            dp_u = None
        r.exacto = {
            "seleccion_optima": [inst.ids[i] for i in ex.S], "f_optima": ex.f,
            "razon_voraz_sobre_optimo": (r.f / ex.f) if ex.f > 0 else 1.0,
            "subconjuntos_evaluados": ex.visitados, "subconjuntos_teoricos": ex.teorico,
            "reparto_dp_utilidad": dp_u, "reparto_voraz_utilidad": r.utilidad,
            "reparto_dif_abs": None if dp_u is None else abs(dp_u - r.utilidad),
            "reparto_optimo": None if dp_u is None else abs(dp_u - r.utilidad) <= TOL * max(1.0, abs(dp_u)),
        }
    return time.perf_counter() - t0
