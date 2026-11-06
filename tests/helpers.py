"""Utilidades compartidas por las pruebas del verificador (no es codigo de produccion)."""
from __future__ import annotations

import itertools
import random
from pathlib import Path

import numpy as np

RAIZ = Path(__file__).resolve().parent.parent
CASO = RAIZ / "project-docs" / "entrada_G2_red_15_nodos.json"
TOL = 1e-9


def f_naive(W, a, S):
    """f(S) calculada con bucles puros, independiente de numpy (referencia)."""
    tot = 0.0
    for j in range(len(a)):
        p = 1.0
        for i in S:
            p *= 1.0 - W[i][j]
        tot += a[j] * (1.0 - p)
    return tot


def todos_subconjuntos(n, kmax=None):
    kmax = n if kmax is None else kmax
    for r in range(0, min(kmax, n) + 1):
        yield from itertools.combinations(range(n), r)


def optimo_bruto(W, a, c, kmax, Lmax):
    """Optimo por enumeracion total independiente de ``exact.fuerza_bruta``."""
    n = len(W)
    mejor = 0.0
    for S in todos_subconjuntos(n, kmax):
        if sum(c[i] for i in S) <= Lmax:
            mejor = max(mejor, f_naive(W, a, S))
    return mejor


def cobertura_01(rng: random.Random, n, m, dens=0.3):
    W = np.zeros((n, m))
    for i in range(n):
        for j in range(m):
            if rng.random() < dens:
                W[i, j] = 1.0
    return W


def simetrica(rng: random.Random, n, dens=1.0):
    W = np.eye(n)
    for i in range(n):
        for j in range(i + 1, n):
            if rng.random() < dens:
                W[i, j] = W[j, i] = round(rng.uniform(0.05, 0.95), 3)
    return W


def cuadrar(W, a, c=None):
    """Rellena W (N x M) a cuadrada (max(N,M)) con filas/columnas nulas y a con ceros.

    Necesario porque ``select.voraz`` usa n=len(a) (=M) como numero de candidatos (BUG-1: no soporta M!=N).
    Devuelve (W2, a2, c2, mascara_candidatos_reales).
    """
    N, M = W.shape
    s = max(N, M)
    W2 = np.zeros((s, s))
    W2[:N, :M] = W
    a2 = np.zeros(s)
    a2[:len(a)] = a
    c2 = list(c if c is not None else [1] * N) + [0] * (s - N)
    mask = np.zeros(s, dtype=bool)
    mask[:N] = True
    return W2, a2, c2, mask
