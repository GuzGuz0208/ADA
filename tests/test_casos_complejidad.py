"""Casos de complejidad (mejor, peor, promedio) respaldados CONTANDO operaciones, sin medir tiempos.

Cubre: (1) iteraciones y llamadas al monticulo del reparto = J = min(B, sum topes); (2) comparaciones de
heappop en CPython; (3) llamadas a ganancias_todas en select.voraz; (4) visitas de exact.fuerza_bruta.
"""
from __future__ import annotations

import heapq
import math
import random
from types import SimpleNamespace

import numpy as np
import pytest

from ada_g2 import allocate, exact
from ada_g2 import select as sel
from ada_g2.generator import generar
from ada_g2.io import desde_dict


# ---------------------------------------------------------------- (1) reparto: J = min(B, sum topes)
def _contador_heap(monkeypatch):
    """Sustituye el nombre ``heapq`` dentro de allocate por un proxy que cuenta pop, replace y heapify."""
    llamadas = {"pop": 0, "replace": 0, "heapify": 0}

    def pop(h):
        llamadas["pop"] += 1
        return heapq.heappop(h)

    def rep(h, it):
        llamadas["replace"] += 1
        return heapq.heapreplace(h, it)

    def hfy(h):
        llamadas["heapify"] += 1
        return heapq.heapify(h)

    monkeypatch.setattr(allocate, "heapq", SimpleNamespace(heappop=pop, heapreplace=rep, heapify=hfy))
    return llamadas


def _instancias_reparto():
    rng = random.Random(20261106)
    casos = [([5.0, 7.0], [3, 4], 0),          # B = 0
             ([5.0, 7.0], [0, 0], 10),         # todos los topes 0
             ([5.0, 7.0, 6.0], [0, 3, 0], 2),  # topes mixtos con ceros
             ([5.0], [4], 4),                  # B = suma de topes exacta
             ([5.0, 9.0], [3, 3], 10**6)]      # B muy holgado
    for _ in range(400):
        n = rng.randint(1, 12)
        a = [round(rng.uniform(0.5, 15), 1) for _ in range(n)]
        topes = [rng.choice([0, 0, 1, 2, 5, 10, 30]) for _ in range(n)]
        B = rng.choice([0, 1, rng.randint(0, 40), sum(topes), sum(topes) + 1, 10**4])
        casos.append((a, topes, B))
    return casos


def test_reparto_iteraciones_igual_J(monkeypatch):
    llamadas = _contador_heap(monkeypatch)
    for a, topes, B in _instancias_reparto():
        for k in llamadas:
            llamadas[k] = 0
        J = min(B, sum(topes))
        r = allocate.asignar(a, topes, B)
        assert r.unidades == J, (a, topes, B)
        assert len(r.traza) == J and sum(r.x) == J
        # cada iteracion hace exactamente un heapreplace o un heappop: la suma es J
        assert llamadas["pop"] + llamadas["replace"] == J, (a, topes, B, llamadas)
        # heappop ocurre una vez por cada nodo cuyo tope se agota (tope>0 y x=tope)
        agotados = sum(1 for i in range(len(a)) if topes[i] > 0 and r.x[i] == topes[i])
        assert llamadas["pop"] == agotados
        assert llamadas["heapify"] == 1
        # pasos_monticulo = heapify (nodos con tope>0) + J
        assert r.pasos_monticulo == sum(1 for t in topes if t > 0) + J


# ---------------------------------------------------------------- (2) heappop: >= floor(log2 n) comparaciones
class _Cuenta:
    n = 0

    def __init__(self, v):
        self.v = v

    def __lt__(self, o):
        _Cuenta.n += 1
        return self.v < o.v


def _comparaciones_pop(valores):
    h = [_Cuenta(v) for v in valores]
    heapq.heapify(h)
    _Cuenta.n = 0
    heapq.heappop(h)
    return _Cuenta.n


@pytest.mark.parametrize("n", [8, 64, 1000])
@pytest.mark.parametrize("tipo", ["aleatorio", "ordenado", "inverso"])
def test_heappop_al_menos_floor_log2(n, tipo):
    rng = random.Random(n)
    piso = math.floor(math.log2(n))
    for _ in range(40 if tipo == "aleatorio" else 1):
        v = list(range(n))
        if tipo == "aleatorio":
            rng.shuffle(v)
        elif tipo == "inverso":
            v.reverse()
        assert _comparaciones_pop(v) >= piso


def test_heappop_barrido_n_3_a_300():
    """La afirmacion se sostiene para todo 3 <= n <= 300 con valores aleatorios y ordenados."""
    rng = random.Random(1)
    for n in range(3, 301):
        piso = math.floor(math.log2(n))
        for _ in range(5):
            v = list(range(n))
            rng.shuffle(v)
            assert _comparaciones_pop(v) >= piso, n
        assert _comparaciones_pop(list(range(n))) >= piso, n


def test_heappop_n2_es_excepcion():
    """FALSO para n=2: tras extraer queda 1 elemento y _siftup no compara nada (floor(log2 2)=1 > 0)."""
    assert _comparaciones_pop([0, 1]) == 0
    assert _comparaciones_pop([1, 0]) == 0
    # cota valida tambien en n=2: floor(log2(n-1)) (tamano tras la extraccion)
    for n in range(2, 300):
        assert _comparaciones_pop(list(range(n))) >= math.floor(math.log2(n - 1))


# ---------------------------------------------------------------- (3) voraz: llamadas a ganancias_todas
def _contar_ganancias(monkeypatch):
    c = {"n": 0}
    orig = sel.ganancias_todas

    def espia(W, a, R):
        c["n"] += 1
        return orig(W, a, R)

    monkeypatch.setattr(sel, "ganancias_todas", espia)
    return c


def _estrella(n=6, m=5):
    """Nodo 0 con w=1 hacia todos los objetivos y la mayor ganancia; los demas con pesos < 1."""
    rng = random.Random(3)
    W = np.array([[round(rng.uniform(0.1, 0.8), 2) for _ in range(m)] for _ in range(n)])
    W[0, :] = 1.0
    return W, np.array([float(rng.randint(1, 9)) for _ in range(m)]), [2] * n


@pytest.mark.parametrize("kmax", [2, 3, 5])
@pytest.mark.parametrize("criterio", ["ganancia", "razon"])
def test_voraz_mejor_caso_k(monkeypatch, kmax, criterio):
    W, a, c = _estrella()
    cand = np.ones(W.shape[0], dtype=bool)
    cuenta = _contar_ganancias(monkeypatch)
    r = sel.voraz(W, a, c, cand, kmax, float("inf"), criterio)
    assert r.S == [0] and len(r.pasos) == 1
    assert cuenta["n"] == 2          # la 2.a ve ganancia 0 y corta


def test_voraz_mejor_caso_k_via_seleccionar(monkeypatch):
    W, a, c = _estrella()
    cand = np.ones(W.shape[0], dtype=bool)
    cuenta = _contar_ganancias(monkeypatch)
    res = sel.seleccionar(W, a, c, cand, 3, 10**6, "k")
    assert res.mejor.S == [0] and cuenta["n"] == 2


@pytest.mark.parametrize("criterio", ["ganancia", "razon"])
def test_voraz_mejor_caso_costo_todos_mayores_que_L(monkeypatch, criterio):
    W, a, _ = _estrella()
    n = W.shape[0]
    cand = np.ones(n, dtype=bool)
    cuenta = _contar_ganancias(monkeypatch)
    r = sel.voraz(W, a, [5] * n, cand, n, 4, criterio)
    assert r.S == [] and cuenta["n"] == 1


def test_voraz_caso_promedio_generador_kmax_pasos(monkeypatch):
    """En instancias del generador se hacen exactamente kmax pasos; ganancias_todas se llama kmax veces."""
    cuenta = _contar_ganancias(monkeypatch)
    for seed in range(60):
        n = 8 + seed % 13
        k = 1 + seed % 6
        dens = (1.0, 0.5, 0.2)[seed % 3]
        inst = desde_dict(generar(n, k=k, seed=seed, densidad=dens))
        cand = np.ones(inst.N, dtype=bool)
        cuenta["n"] = 0
        r = sel.voraz(inst.W, inst.a, inst.c, cand, k, float("inf"), "ganancia")
        assert len(r.S) == k and len(r.pasos) == k, (seed, n, k, dens)
        assert cuenta["n"] == k      # la rama de corte por ganancia 0 no se activa
        assert all(p.ganancia > 0 for p in r.pasos)


def test_generador_pesos_nunca_0_ni_1():
    """El redondeo (2 decimales, rango [0.1,0.9]) no produce pesos 0 ni 1 ni coeficientes <= 0."""
    for seed in range(200):
        d = generar(25, seed=seed)
        pesos = [e["peso_influencia"] for e in d["grafo"]]
        assert min(pesos) >= 0.1 and max(pesos) <= 0.9
        assert all(0 < p < 1 for p in pesos)
        assert all(nd["coeficiente_utilidad"] >= 5.0 for nd in d["nodos"])


# ---------------------------------------------------------------- (4) fuerza bruta: visitas
def _inst_pequena(seed=11, n=9):
    inst = desde_dict(generar(n, k=3, seed=seed))
    return inst.W, inst.a, list(inst.c)


@pytest.mark.parametrize("kmax", [1, 2, 3, 5])
def test_fuerza_bruta_todos_costos_mayores_que_L(kmax):
    W, a, c = _inst_pequena()
    L = min(c) - 1
    r = exact.fuerza_bruta(W, a, c, list(range(len(c))), kmax, L)
    assert r.visitados == 1 and r.S == [] and r.f == 0.0


@pytest.mark.parametrize("n,kmax", [(6, 0), (6, 1), (6, 3), (8, 4), (9, 9), (7, 12)])
def test_fuerza_bruta_sin_poda_visita_num_subconjuntos(n, kmax):
    W, a, c = _inst_pequena(seed=n, n=n)
    r = exact.fuerza_bruta(W, a, c, list(range(n)), kmax, 10**9)
    assert r.visitados == exact.num_subconjuntos(n, kmax) == r.teorico
