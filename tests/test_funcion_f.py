"""f: f(vacio)=0, monotonia, submodularidad, ganancia incremental tau=O(M), caso Cobertura Maxima."""
import random

import numpy as np
from hypothesis import HealthCheck, given, settings, strategies as st

from ada_g2.model import (actualizar_residual, f_directa, ganancia_uno, ganancias_todas,
                          residual_inicial)
from helpers import f_naive, todos_subconjuntos

CFG = settings(max_examples=600, derandomize=True, deadline=None, suppress_health_check=list(HealthCheck))


@st.composite
def caso(draw):
    n = draw(st.integers(2, 7))
    simetrica = draw(st.booleans())
    m = n if simetrica else draw(st.integers(1, 8))
    val = st.one_of(st.sampled_from([0.0, 1.0]), st.floats(0.0, 1.0))
    W = np.array([[draw(val) for _ in range(m)] for _ in range(n)])
    if simetrica:
        W = np.triu(W, 1)
        W = W + W.T + np.eye(n)
    a = np.array([draw(st.floats(0.01, 20.0)) for _ in range(m)])
    perm = draw(st.permutations(range(n)))
    t = draw(st.integers(0, n - 1))
    s = draw(st.integers(0, t))
    T = list(perm[:t])
    S = T[:s]
    e = perm[n - 1]                      # e no esta en T (T usa perm[:t], t<=n-1)
    return W, a, S, T, int(e)


@CFG
@given(caso())
def test_monotona_submodular_f0(c):
    W, a, S, T, e = c
    assert f_directa(W, a, []) == 0.0
    dS = f_directa(W, a, S + [e]) - f_directa(W, a, S)
    dT = f_directa(W, a, T + [e]) - f_directa(W, a, T)
    assert dS >= -1e-9 and dT >= -1e-9, "monotonia"
    assert dS >= dT - 1e-9, "submodularidad"
    assert f_directa(W, a, T) >= f_directa(W, a, S) - 1e-9, "monotonia S<=T"
    assert abs(f_directa(W, a, T) - f_naive(W, a, T)) <= 1e-9


@CFG
@given(caso())
def test_ganancia_incremental_igual_directa(c):
    W, a, S, _, e = c
    R = residual_inicial(W.shape[1])
    for i in S:
        actualizar_residual(W, R, i)
    assert abs(ganancia_uno(W, a, R, e) - (f_directa(W, a, S + [e]) - f_directa(W, a, S))) <= 1e-9
    todas = ganancias_todas(W, a, R)
    for i in range(W.shape[0]):
        if i not in S:
            assert abs(todas[i] - (f_directa(W, a, S + [i]) - f_directa(W, a, S))) <= 1e-9


def test_formula_delta_para_i_en_S_no_es_cero():
    """Advertencia del theorist: para i en S la formula NO da 0 (el voraz debe excluirlos)."""
    W = np.array([[1.0, 0.5], [0.5, 1.0]])
    a = np.array([1.0, 1.0])
    R = residual_inicial(2)
    actualizar_residual(W, R, 0)
    assert ganancia_uno(W, a, R, 0) != 0.0          # formula con i en S


@CFG
@given(st.integers(2, 6), st.integers(1, 7), st.integers(0, 10**6))
def test_cobertura_maxima_w01_a1(n, m, seed):
    rng = random.Random(seed)
    W = np.array([[1.0 if rng.random() < 0.4 else 0.0 for _ in range(m)] for _ in range(n)])
    a = np.ones(m)
    for A in todos_subconjuntos(n):
        union = {j for i in A for j in range(m) if W[i, j] == 1.0}
        assert f_directa(W, a, A) == len(union)
