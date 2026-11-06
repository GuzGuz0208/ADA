"""Parte 2: restricciones, razon voraz/exacto, certificado LP (W2), instancia ajustada (W3), contraejemplos."""
import math
import random
from fractions import Fraction

import numpy as np
import pytest
from hypothesis import HealthCheck, given, settings, strategies as st

from ada_g2 import select as sel
from ada_g2.certificates import certificar_seleccion
from ada_g2.exact import fuerza_bruta
from ada_g2.select import limites, seleccionar
from helpers import cobertura_01, cuadrar, f_naive, optimo_bruto, simetrica

CFG = settings(max_examples=400, derandomize=True, deadline=None, suppress_health_check=list(HealthCheck))
INF = float("inf")
E = 1 - 1 / math.e
FAMILIAS = ("cob01", "pesos", "rala")


def instancia_aleatoria(rng, familia):
    n = rng.randint(3, 9)
    if familia == "cob01":
        m = rng.randint(4, 14)
        W = cobertura_01(rng, n, m, rng.choice([0.15, 0.25, 0.4]))
        a = np.ones(m) if rng.random() < 0.5 else np.array([float(rng.randint(1, 5)) for _ in range(m)])
    elif familia == "pesos":
        W = simetrica(rng, n, rng.choice([0.3, 0.6, 1.0]))
        a = np.array([rng.uniform(0.5, 10) for _ in range(n)])
    else:  # grafo ralo con pesos pequenos: poca saturacion
        W = np.eye(n)
        for i in range(n):
            for j in range(i + 1, n):
                if rng.random() < 0.3:
                    W[i, j] = W[j, i] = rng.uniform(0.1, 0.5)
        a = np.array([rng.uniform(0.5, 10) for _ in range(n)])
    n = W.shape[0]
    c = [rng.randint(0, 6) for _ in range(n)]
    k = rng.randint(1, n - 1)
    L = rng.randint(1, 18)
    W, a, c, mask = cuadrar(W, a, c)         # BUG-1: el codigo solo admite M == N
    return W, a, c, k, L, mask


@pytest.mark.parametrize("familia", FAMILIAS)
@pytest.mark.parametrize("modo", ["k", "costo", "ambos"])
def test_restricciones_razon_y_certificado(familia, modo):
    rng = random.Random(20261105 + 17 * FAMILIAS.index(familia) + len(modo))
    rmin, cnt = 1.0, 0
    for _ in range(250):
        W, a, c, k, L, mask = instancia_aleatoria(rng, familia)
        n = W.shape[0]
        cands = [int(i) for i in np.flatnonzero(mask)]
        res = seleccionar(W, a, c, mask, k, L, modo)
        kmax, Lmax = limites(modo, k, L, int(mask.sum()))
        for alt in res.alternativas:                       # restricciones en TODAS las salidas
            assert len(set(alt.S)) == len(alt.S), "nodo repetido"
            assert len(alt.S) <= kmax
            assert sum(c[i] for i in alt.S) <= Lmax
            assert alt.f == pytest.approx(f_naive(W, a, alt.S), abs=1e-9)
        assert res.mejor.f >= max(r.f for r in res.alternativas) - 1e-12
        opt = optimo_bruto(W[cands], a, [c[i] for i in cands], kmax, Lmax)
        ex = fuerza_bruta(W, a, c, cands, kmax, Lmax)
        assert ex.f == pytest.approx(opt, abs=1e-9)
        assert res.mejor.f <= opt + 1e-9
        if opt > 0:
            rz = res.mejor.f / opt
            rmin = min(rmin, rz)
            if modo == "k":
                assert rz >= 1 - (1 - 1 / k) ** k - 1e-9, (W.tolist(), a.tolist(), k)
                assert rz >= E - 1e-9
        ct = certificar_seleccion(W, a, c, res.mejor.S, mask, kmax, Lmax, res.mejor.f)
        assert ct["ok"], ct
        assert opt <= ct["cota_superior"] + 1e-9, (opt, ct, W.tolist(), a.tolist(), c, k, L)
        cnt += 1
    print(f"\n[RAZON MINIMA] familia={familia} modo={modo}: {rmin:.6f} en {cnt} instancias")


@CFG
@given(st.integers(0, 10**6), st.sampled_from(["k", "costo", "ambos"]), st.sampled_from(FAMILIAS))
def test_hypothesis_restricciones_y_no_repetir(seed, modo, fam):
    rng = random.Random(seed)
    W, a, c, k, L, mask = instancia_aleatoria(rng, fam)
    n = W.shape[0]
    cand = np.array([bool(mask[i]) and rng.random() < 0.8 for i in range(n)])
    if not cand.any():
        cand[0] = True
    res = seleccionar(W, a, c, cand, k, L, modo)
    kmax, Lmax = limites(modo, k, L, int(cand.sum()))
    for alt in res.alternativas:
        assert set(alt.S) <= set(np.flatnonzero(cand).tolist())
        assert len(set(alt.S)) == len(alt.S) <= kmax
        assert sum(c[i] for i in alt.S) <= Lmax


@CFG
@given(st.integers(0, 10**6), st.sampled_from(["cob01", "pesos"]))
def test_hypothesis_cota_modo_k(seed, fam):
    rng = random.Random(seed)
    W, a, c, k, L, mask = instancia_aleatoria(rng, fam)
    res = seleccionar(W, a, c, mask, k, L, "k").mejor
    cands = [int(i) for i in np.flatnonzero(mask)]
    opt = optimo_bruto(W[cands], a, [c[i] for i in cands], k, INF)
    assert res.f >= (1 - (1 - 1 / k) ** k) * opt - 1e-9


# ---------------- Instancia ajustada (W3, D-15) ----------------
def ajustada(k):
    """k trampas (indices 0..k-1, primero) y k conjuntos optimos disjuntos de k^k elementos (D-15)."""
    m = k ** k
    trampas = [[] for _ in range(k)]
    optimos = [[] for _ in range(k)]
    elem = 0
    for i in range(k):
        for j in range(k):
            for _ in range(k ** (k - (j + 1)) * (k - 1) ** j):
                trampas[j].append(elem)
                optimos[i].append(elem)
                elem += 1
        for _ in range((k - 1) ** k):
            optimos[i].append(elem)
            elem += 1
    assert all(len(o) == m for o in optimos)
    W = np.zeros((2 * k, elem))
    for j in range(k):
        W[j, trampas[j]] = 1.0
    for i in range(k):
        W[k + i, optimos[i]] = 1.0
    return W, np.ones(elem), m


@pytest.mark.parametrize("k", [2, 3, 5])
def test_instancia_ajustada_razon_exacta(k):
    W, a, m = ajustada(k)
    n = 2 * k
    W, a, c, mask = cuadrar(W, a, [1] * n)
    res = seleccionar(W, a, c, mask, k, 10**6, "k").mejor
    assert sorted(res.S) == list(range(k)), "el voraz debe elegir las k trampas (desempate por indice)"
    ex = fuerza_bruta(W, a, c, list(range(n)), k, INF)
    assert ex.f == k * m
    razon = Fraction(int(round(res.f)), int(round(ex.f)))
    assert razon == 1 - (1 - Fraction(1, k)) ** k
    assert razon == {2: Fraction(3, 4), 3: Fraction(19, 27), 5: Fraction(2101, 3125)}[k]
    # las fracciones de SPEC/DECISIONS (6/8, 57/81, 10505/15625) son las mismas sin simplificar
    assert Fraction(6, 8) == Fraction(3, 4) and Fraction(57, 81) == Fraction(19, 27)
    assert Fraction(10505, 15625) == Fraction(2101, 3125)
    assert float(razon) >= E


# ---------------- Contraejemplos de la seccion 03 ----------------
def test_contraejemplo_parte2_razon_5_sobre_6():
    S = [{1, 2, 3, 4}, {1, 2, 5}, {3, 4, 6}]
    W = np.zeros((3, 6))
    for i, s in enumerate(S):
        for e in s:
            W[i, e - 1] = 1
    W, a, c, mask = cuadrar(W, np.ones(6), [0] * 3)
    res = seleccionar(W, a, c, mask, 2, 0, "k").mejor
    ex = fuerza_bruta(W, a, c, [0, 1, 2], 2, INF)
    assert res.f == 5 and ex.f == 6
    assert Fraction(int(res.f), int(ex.f)) == Fraction(5, 6) >= Fraction(3, 4)


def test_contraejemplo_H3_sin_submodularidad():
    """f(S)=10*[{1,2} subset S] + [3 in S]: voraz generico (misma regla) da razon 0.1. f NO es la f del proyecto."""
    def f(S):
        return 10 * ({1, 2} <= set(S)) + (3 in S)
    assert f({1, 2}) - f({1}) > f({2}) - f(set())          # no submodular
    elegido = []
    for _ in range(2):
        mejor = max((i for i in (1, 2, 3) if i not in elegido), key=lambda i: (f(elegido + [i]) - f(elegido), -i))
        elegido.append(mejor)
    assert elegido == [3, 1] and f(elegido) == 1
    opt = max(f(s) for s in ([1, 2], [1, 3], [2, 3]))
    assert opt == 10 and f(elegido) / opt == pytest.approx(0.1)


@pytest.mark.parametrize("L", [3, 5, 10, 50])
def test_contraejemplo_costos_razon_2_sobre_L(L):
    """f(1)=2,c=1; f(2)=L,c=L; presupuesto L. Voraz por razon -> 2; mejor-de-3 -> L."""
    W = np.zeros((2, 2 + L))
    W[0, :2] = 1
    W[1, 2:] = 1
    W, a, c, mask = cuadrar(W, np.ones(2 + L), [1, L])
    razon = sel.voraz(W, a, c, mask, 2, L, "razon")
    assert razon.S == [0] and razon.f == 2
    assert razon.f / L == pytest.approx(2 / L)
    mejor = seleccionar(W, a, c, mask, 2, L, "costo").mejor
    assert mejor.f == L
    assert fuerza_bruta(W, a, c, [0, 1], 2, L).f == L


def test_BUG1_voraz_rectangular_M_distinto_de_N():
    """Regresion BUG-1 (corregido): N=2 candidatos, M=3 objetivos (familia general de la reduccion)."""
    W = np.array([[1.0, 1.0, 0.0], [0.0, 0.0, 1.0]])
    res = seleccionar(W, np.ones(3), [1, 1], np.ones(2, dtype=bool), 1, 5, "k").mejor
    assert res.S == [0] and res.f == pytest.approx(2.0)


@pytest.mark.parametrize("semilla", range(40))
def test_rectangular_sin_cuadrar_voraz_cota_y_restricciones(semilla):
    """Tras BUG-1: W de N x M (M != N) directo, sin cuadrar(); voraz >= (1-(1-1/k)^k)*exacto y restricciones."""
    rng = random.Random(9000 + semilla)
    n, m = rng.randint(3, 8), rng.randint(2, 12)
    W = cobertura_01(rng, n, m, 0.3)
    a = np.ones(m)
    c = [rng.randint(1, 4) for _ in range(n)]
    mask = np.ones(n, dtype=bool)
    k = rng.randint(1, n)
    res = seleccionar(W, a, c, mask, k, 10**9, "k").mejor
    opt = fuerza_bruta(W, a, c, list(range(n)), k, INF)
    assert len(res.S) <= k and len(set(res.S)) == len(res.S)
    assert res.f == pytest.approx(f_naive(W, a, res.S))
    assert res.f >= (1 - (1 - 1 / k) ** k) * opt.f - 1e-9


# ---------------- Conteo del costo (T5) ----------------
@pytest.mark.parametrize("n,k,m", [(6, 3, 6), (10, 4, 7), (12, 5, 12)])
def test_conteo_evaluaciones_P_por_M(monkeypatch, n, k, m):
    rng = random.Random(n * 100 + k)
    m = n                                            # M = N (unico caso soportado, BUG-1)
    W = np.eye(n) + 0.05 * simetrica(rng, n, 0.5) * (1 - np.eye(n))   # ganancia > 0 siempre -> k pasos completos
    a = np.ones(m)
    mask = np.ones(n, dtype=bool)
    n_c, m_c = W.shape
    llamadas = []
    orig = sel.ganancias_todas

    def espia(W_, a_, R_):
        llamadas.append(W_.shape)
        return orig(W_, a_, R_)

    monkeypatch.setattr(sel, "ganancias_todas", espia)
    r = sel.voraz(W, a, [1] * n_c, mask, k, INF, "ganancia")
    assert len(r.S) == k
    P = k * n - k * (k - 1) // 2
    assert sum(len(p.evaluados) for p in r.pasos) == P        # candidatos factibles evaluados = P
    assert len(llamadas) == k                                  # k matvec de N x M (incluye ya elegidos)
    assert sum(s[0] * s[1] for s in llamadas) == k * n_c * m_c >= P * m_c
