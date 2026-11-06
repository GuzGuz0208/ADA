"""Modelo: utilidad u_i(x)=a_i ln(1+x) (D-01) y cobertura probabilistica f (D-02).

f(S) = sum_j a_j [1 - prod_{i in S} (1 - w_ij)],  f(vacio)=0,  w_ii=1.
Con el vector residual R_j = prod_{l in S}(1 - w_lj):
    Delta(i|S) = sum_j a_j w_ij R_j      -> tau = O(M)  (M = numero de objetivos = N en el JSON).
"""
from __future__ import annotations

import math

import numpy as np


def utilidad(a: float, x: int) -> float:
    """u(x) = a ln(1+x). Pre: a>0, x entero >=0. Post: valor creciente y concavo. T=O(1)."""
    return a * math.log1p(x)


def ganancia_marginal(a: float, t: int) -> float:
    """g(t) = u(t+1)-u(t) = a ln((t+2)/(t+1)) = a log1p(1/(t+1)). Estrictamente decreciente en t. T=O(1)."""
    return a * math.log1p(1.0 / (t + 1))


def residual_inicial(m: int) -> np.ndarray:
    """R_j = 1 para S=vacio. T=O(M)."""
    return np.ones(m)


def ganancias_todas(W: np.ndarray, a: np.ndarray, R: np.ndarray) -> np.ndarray:
    """Delta(i|S) para TODOS los candidatos i: W @ (a*R). T=O(N*M) = N evaluaciones de tau=O(M)."""
    return W @ (a * R)


def ganancia_uno(W: np.ndarray, a: np.ndarray, R: np.ndarray, i: int) -> float:
    """Delta(i|S) de un candidato: sum_j a_j W[i,j] R_j. T=tau=O(M)."""
    return float(W[i] @ (a * R))


def actualizar_residual(W: np.ndarray, R: np.ndarray, i: int) -> None:
    """Pos: R_j <- R_j (1-W[i,j]) (agregar i a S). In situ. T=O(M)."""
    R *= 1.0 - W[i]


def f_directa(W: np.ndarray, a: np.ndarray, S) -> float:
    """f(S) por la formula, sin estado incremental (para verificar). T=O(|S|*M)."""
    S = list(S)
    if not S:
        return 0.0
    return float(a @ (1.0 - np.prod(1.0 - W[S], axis=0)))
