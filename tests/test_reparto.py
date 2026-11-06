"""Parte 1: reparto voraz == DP exacta (>=500 instancias), restricciones, certificado de dualidad (W1/D-14a)."""
import itertools
import math

import pytest
from hypothesis import HealthCheck, given, settings, strategies as st

from ada_g2.allocate import asignar
from ada_g2.certificates import certificar_reparto
from ada_g2.exact import dp_reparto
from ada_g2.model import utilidad

CFG = settings(max_examples=700, derandomize=True, deadline=None,
               suppress_health_check=list(HealthCheck))


@st.composite
def instancia(draw):
    n = draw(st.integers(1, 6))
    B = draw(st.integers(0, 25))
    a = [draw(st.floats(0.05, 30.0, allow_nan=False)) for _ in range(n)]
    topes = [draw(st.integers(0, B)) for _ in range(n)]
    return a, topes, B


@CFG
@given(instancia())
def test_reparto_igual_a_dp_y_restricciones(inst):
    a, topes, B = inst
    r = asignar(a, topes, B)
    opt, _ = dp_reparto(a, topes, B)
    assert abs(r.utilidad - opt) <= 1e-9, (a, topes, B, r.x)
    assert sum(r.x) <= B
    assert all(0 <= x <= t for x, t in zip(r.x, topes))
    assert sum(r.x) == min(B, sum(topes)), "debe gastar min(B, sum r_i)"
    assert r.unidades == min(B, sum(topes))
    # utilidad reportada = suma directa
    assert abs(r.utilidad - sum(utilidad(ai, xi) for ai, xi in zip(a, r.x))) <= 1e-12
    # ganancias marginales de la traza no crecientes
    g = [p.ganancia for p in r.traza]
    assert all(g[i] >= g[i + 1] for i in range(len(g) - 1)), g
    # acumulado coherente
    if r.traza:
        assert abs(r.traza[-1].utilidad_acum - r.utilidad) <= 1e-9


@CFG
@given(instancia())
def test_certificado_dualidad_reparto(inst):
    a, topes, B = inst
    r = asignar(a, topes, B)
    c = certificar_reparto(a, topes, B, r)
    opt, _ = dp_reparto(a, topes, B)
    esc = max(1.0, abs(c["cota_superior"]))
    assert c["ok"], c
    assert abs(c["brecha"]) <= 1e-9 * esc, c
    assert c["cota_superior"] >= opt - 1e-9 * esc, "la cota nunca puede ser menor que el optimo"


def _ub_bruto(a, topes, B, lam):
    """Cota de dualidad debil para un lambda>=0 cualquiera, maximizando por enumeracion de x."""
    return lam * B + sum(max(utilidad(ai, x) - lam * x for x in range(t + 1)) for ai, t in zip(a, topes))


@CFG
@given(instancia(), st.floats(0.0, 10.0))
def test_dualidad_debil_cualquier_lambda(inst, lam):
    a, topes, B = inst
    opt, _ = dp_reparto(a, topes, B)
    assert _ub_bruto(a, topes, B, lam) >= opt - 1e-9


def test_topes_que_impiden_gastar_B():
    a, topes, B = [3.0, 5.0], [2, 1], 20
    r = asignar(a, topes, B)
    assert r.x == [2, 1] and r.unidades == 3
    c = certificar_reparto(a, topes, B, r)
    assert c["ok"] and c["lambda"] == 0.0


def test_todos_los_topes_cero_o_B_cero():
    r = asignar([1.0, 2.0], [0, 0], 7)
    assert r.x == [0, 0] and r.utilidad == 0.0 and r.unidades == 0
    assert certificar_reparto([1.0, 2.0], [0, 0], 7, r)["ok"]
    r = asignar([1.0, 2.0], [5, 5], 0)
    assert r.x == [0, 0]
    assert certificar_reparto([1.0, 2.0], [5, 5], 0, r)["ok"]
    r = asignar([], [], 5)
    assert r.x == [] and r.utilidad == 0.0


def test_desempate_menor_indice():
    r = asignar([2.0, 2.0, 2.0], [5, 5, 5], 1)
    assert r.x == [1, 0, 0]


def test_exhaustivo_pequeno_contra_enumeracion_total():
    """Independiente del DP: enumera todos los x para N=3, B=6."""
    import random
    rng = random.Random(11)
    for _ in range(60):
        a = [rng.uniform(0.1, 9) for _ in range(3)]
        topes = [rng.randint(0, 6) for _ in range(3)]
        B = rng.randint(0, 6)
        mejor = max(sum(utilidad(ai, xi) for ai, xi in zip(a, xs))
                    for xs in itertools.product(*[range(t + 1) for t in topes]) if sum(xs) <= B)
        assert abs(asignar(a, topes, B).utilidad - mejor) <= 1e-9
