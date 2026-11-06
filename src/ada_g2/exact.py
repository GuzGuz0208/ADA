"""Referencias exactas: fuerza bruta de la seleccion (Parte 2) y DP del reparto (Parte 1).

Solo para validar en instancias pequenas; son exponenciales / pseudo-polinomiales a proposito.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import comb

import numpy as np

from .model import utilidad


class ExactoDemasiadoGrande(RuntimeError):
    """La enumeracion excede el tope de nodos permitido."""


@dataclass
class ResultadoExacto:
    S: list
    f: float
    visitados: int          # subconjuntos factibles evaluados (incluye el vacio)
    teorico: int            # sum_{r<=kmax} C(n, r)


def num_subconjuntos(n: int, kmax: int) -> int:
    """sum_{r=0}^{min(kmax,n)} C(n,r). T=O(kmax)."""
    return sum(comb(n, r) for r in range(0, min(kmax, n) + 1))


def fuerza_bruta(W, a, c, cands: list, kmax: int, Lmax, max_visitas: int = 3_000_000) -> ResultadoExacto:
    """Optimo de max f(S), |S|<=kmax, costo<=Lmax, por DFS sobre subconjuntos factibles (con R incremental).

    Pre: cands lista de indices (orden creciente); Pos: S optimo (en empate, el primero hallado en DFS
    preorden, o sea el lexicograficamente menor entre los de menor tamano visitados antes).
    T = sum_{r<=kmax} C(N,r) * O(M) en el peor caso (cada subconjunto cuesta una evaluacion O(M) incremental).
    """
    cands = sorted(cands)
    aw = np.asarray(a, dtype=float)
    carr = [float(x) for x in c]
    mejor = {"S": [], "f": 0.0}
    cuenta = [0]

    def rec(inicio: int, R: np.ndarray, f: float, S: list, costo: float) -> None:
        cuenta[0] += 1
        if cuenta[0] > max_visitas:
            raise ExactoDemasiadoGrande(f"mas de {max_visitas} subconjuntos; instancia demasiado grande")
        if f > mejor["f"] + 1e-12:
            mejor["f"], mejor["S"] = f, list(S)
        if len(S) >= kmax:
            return
        aR = aw * R
        for pos in range(inicio, len(cands)):
            i = cands[pos]
            if costo + carr[i] > Lmax:
                continue
            g = float(W[i] @ aR)
            S.append(i)
            rec(pos + 1, R * (1.0 - W[i]), f + g, S, costo + carr[i])
            S.pop()

    rec(0, np.ones(W.shape[1]), 0.0, [], 0.0)
    return ResultadoExacto(mejor["S"], mejor["f"], cuenta[0], num_subconjuntos(len(cands), kmax))


def dp_reparto(a: list, topes: list, B: int):
    """Optimo del reparto por programacion dinamica. Devuelve (utilidad, x).

    dp[i][b] = mejor utilidad con los primeros i nodos y presupuesto <= b.
    T = O(N * B * min(B, r_max)) (referencia para pruebas, no para uso con B grande).
    """
    n = len(a)
    dp = [[0.0] * (B + 1) for _ in range(n + 1)]
    eleg = [[0] * (B + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        ai, ri = a[i - 1], topes[i - 1]
        for b in range(B + 1):
            best, bx = -1.0, 0
            for x in range(0, min(b, ri) + 1):
                v = dp[i - 1][b - x] + utilidad(ai, x)
                if v > best + 1e-15:
                    best, bx = v, x
            dp[i][b], eleg[i][b] = best, bx
    x = [0] * n
    b = B
    for i in range(n, 0, -1):
        x[i - 1] = eleg[i][b]
        b -= x[i - 1]
    return dp[n][B], x
