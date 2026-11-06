"""T3: reduccion desde Cobertura Maxima (f(A)=|union|), ejemplo 4x5 de informe/secciones/02_np_dureza.tex,
subfamilia simetrica (M=N, w_ii=1, a>0): CobMax-Dec  <=>  Sel-Dec por fuerza bruta."""
import itertools
import random

import numpy as np
import pytest

from ada_g2.exact import fuerza_bruta
from ada_g2.model import f_directa
from helpers import f_naive

CONJ = [{1, 2, 3}, {3, 4}, {4, 5}, {1, 5}]       # S_1..S_4 del ejemplo del informe, U = {1..5}


def phi(conjuntos, m):
    W = np.zeros((len(conjuntos), m))
    for i, s in enumerate(conjuntos):
        for e in s:
            W[i, e - 1] = 1.0
    return W, np.ones(m)


def union(conjuntos, A):
    u = set()
    for i in A:
        u |= conjuntos[i]
    return u


def test_ejemplo_4x5_tabla_del_informe():
    W, a = phi(CONJ, 5)
    esperado = {(0, 1): 4, (0, 2): 5, (0, 3): 4, (1, 2): 3, (1, 3): 4, (2, 3): 3}   # indices base 0
    for A, v in esperado.items():
        assert f_directa(W, a, list(A)) == v == len(union(CONJ, A))
    # unico A con |A|<=2 y f>=5 es {1,3} (base 1) = (0,2)
    positivos = [A for r in range(0, 3) for A in itertools.combinations(range(4), r)
                 if f_directa(W, a, list(A)) >= 5]
    assert positivos == [(0, 2)]


def test_ejemplo_instancia_negativa_k1_t4():
    W, a = phi(CONJ, 5)
    assert max(f_directa(W, a, [i]) for i in range(4)) == 3 < 4


@pytest.mark.parametrize("seed", range(40))
def test_f_igual_union_para_todo_A(seed):
    rng = random.Random(seed)
    n, m = rng.randint(2, 7), rng.randint(1, 9)
    conj = [{j + 1 for j in range(m) if rng.random() < 0.4} for _ in range(n)]
    W, a = phi(conj, m)
    for r in range(n + 1):
        for A in itertools.combinations(range(n), r):
            assert f_directa(W, a, list(A)) == len(union(conj, A))
            assert f_naive(W, a, A) == len(union(conj, A))


def subfamilia_simetrica(conj):
    """Construccion de la seccion 02 (refuerzo): vertices s_1..s_n y elementos e_j de la union (limpieza)."""
    n = len(conj)
    U = sorted(set().union(*conj))
    N = n + len(U)
    W = np.eye(N)
    for i, s in enumerate(conj):
        for e in s:
            j = n + U.index(e)
            W[i, j] = W[j, i] = 1.0
    a = np.array([1.0 / (n + 1)] * n + [1.0] * len(U))
    return W, a, N, len(U)


@pytest.mark.parametrize("seed", range(60))
def test_subfamilia_simetrica_equivalencia_cobmax_seldec(seed):
    rng = random.Random(1000 + seed)
    n, m = rng.randint(2, 4), rng.randint(2, 5)
    conj = [{j + 1 for j in range(m) if rng.random() < 0.45} for _ in range(n)]
    if not set().union(*conj):
        conj[0] = {1}
    W, a, N, mp = subfamilia_simetrica(conj)
    assert np.allclose(W, W.T) and np.all(np.diag(W) == 1) and np.all(a > 0)
    for k in range(1, n):                                  # k < n
        mejor_cob = max(len(union(conj, A)) for r in range(k + 1) for A in itertools.combinations(range(n), r))
        ex = fuerza_bruta(W, a, [0] * N, list(range(N)), k, float("inf"))
        for t in range(0, mp + 2):
            assert (mejor_cob >= t) == (ex.f >= t - 1e-9), (conj, k, t, mejor_cob, ex.f)
