"""Valores de referencia SPEC s6 re-derivados con el codigo real (caso de la profesora)."""
import numpy as np
import pytest

from ada_g2.allocate import asignar
from ada_g2.exact import dp_reparto, fuerza_bruta
from ada_g2.io import cargar
from ada_g2.rounds import comparar_exacto, ejecutar
from ada_g2.select import seleccionar
from helpers import CASO

INF = float("inf")


@pytest.fixture(scope="module")
def inst():
    return cargar(CASO)


def nombres(inst, S):
    return sorted(inst.ids[i] for i in S)


def test_parametros_y_grafo(inst):
    assert (inst.N, inst.T, inst.k, inst.B, inst.L, inst.n_aristas) == (15, 3, 5, 30, 24, 105)
    assert np.allclose(inst.W, inst.W.T) and np.all(np.diag(inst.W) == 1)
    assert set(inst.R) == {18}
    assert abs(inst.a.sum() - 147.8) < 1e-9


def test_ronda1_modo_k_voraz_y_exacto(inst):
    mask = np.ones(inst.N, dtype=bool)
    r = seleccionar(inst.W, inst.a, inst.c, mask, inst.k, inst.L, "k").mejor
    assert nombres(inst, r.S) == ["N09", "N11", "N13", "N14", "N15"]
    assert [inst.ids[i] for i in r.S] == ["N11", "N14", "N09", "N15", "N13"]      # orden de eleccion
    assert r.f == pytest.approx(145.5795, abs=5e-5)
    ex = fuerza_bruta(inst.W, inst.a, inst.c, list(range(15)), 5, INF)
    assert ex.f == pytest.approx(145.9072, abs=5e-5)
    assert nombres(inst, ex.S) == ["N09", "N11", "N12", "N13", "N15"]
    assert ex.visitados == 4944 == ex.teorico                        # SPEC: 4944 contando el vacio
    assert r.f / ex.f == pytest.approx(0.9978, abs=5e-5)
    assert r.f / ex.f >= 1 - 1 / np.e


def test_ronda1_modo_ambos_y_heuristicas(inst):
    mask = np.ones(inst.N, dtype=bool)
    res = seleccionar(inst.W, inst.a, inst.c, mask, inst.k, inst.L, "ambos")
    alt = {a.heuristica: a for a in res.alternativas}
    assert alt["voraz_ganancia"].costo == 23 and alt["voraz_ganancia"].f == pytest.approx(145.5795, abs=5e-5)
    assert [inst.ids[i] for i in alt["voraz_razon"].S] == ["N05", "N09", "N14", "N11", "N15"]
    assert alt["voraz_razon"].costo == 18 and alt["voraz_razon"].f == pytest.approx(145.1056, abs=5e-5)
    ex = fuerza_bruta(inst.W, inst.a, inst.c, list(range(15)), 5, 24)
    assert nombres(inst, ex.S) == ["N09", "N11", "N13", "N14", "N15"]
    assert ex.f == pytest.approx(145.5795, abs=5e-5)
    assert res.mejor.f / ex.f == pytest.approx(1.0, abs=1e-9)


def test_reparto_ronda1(inst):
    S = [inst.ids.index(x) for x in ("N11", "N14", "N09", "N15", "N13")]
    a = [float(inst.a[i]) for i in S]
    r = asignar(a, [18] * 5, 30)
    x = {inst.ids[i]: r.x[p] for p, i in enumerate(S)}
    assert x == {"N11": 5, "N14": 7, "N09": 7, "N15": 6, "N13": 5}
    assert r.utilidad == pytest.approx(88.564, abs=5e-4)
    assert r.utilidad == pytest.approx(dp_reparto(a, [18] * 5, 30)[0], abs=1e-9)
    primeras = [(inst.ids[S[p.nodo]], round(p.ganancia, 3)) for p in r.traza[:5]]
    assert primeras == [("N14", 7.001), ("N09", 6.862), ("N15", 6.585), ("N13", 5.753), ("N11", 5.268)]


def test_tres_rondas(inst):
    c = ejecutar(inst)
    assert c.ok
    assert c.f_total == pytest.approx(436.7386, abs=5e-5)
    assert c.utilidad_total == pytest.approx(262.7387, abs=5e-5)
    assert c.rondas[0].utilidad == pytest.approx(88.5640, abs=5e-5)
    assert c.rondas[2].utilidad == pytest.approx(85.6108, abs=5e-5)
    for i in range(inst.N):
        assert c.gasto_total[i] <= 18
    for r in c.rondas:
        assert len(r.S) <= 5 and r.costo <= 24 and sum(r.x.values()) <= 30
        assert sum(r.x.values()) == min(30, sum(r.topes[i] for i in r.S))
    assert max(c.gasto_total) == 18                                  # los topes si son activos
    comparar_exacto(c)
    assert all(r.exacto["reparto_optimo"] for r in c.rondas)


def test_razon_certificada(inst):
    c = ejecutar(inst)
    rc = c.rondas[0].cert_seleccion
    assert rc["razon_certificada"] == pytest.approx(0.95784, abs=5e-6)
    assert rc["cota_superior"] == pytest.approx(151.9871, abs=5e-5)
    assert c.rondas[0].cert_reparto["brecha"] == pytest.approx(0.0, abs=1e-9)


@pytest.mark.parametrize("modo", ["k", "costo", "ambos"])
@pytest.mark.parametrize("politica", ["concentrado", "uniforme"])
def test_todas_las_banderas_cumplen(inst, modo, politica):
    c = ejecutar(inst, modo=modo, politica=politica)
    assert c.ok
    comparar_exacto(c)
    for r in c.rondas:
        assert r.exacto["razon_voraz_sobre_optimo"] <= 1 + 1e-9
        assert r.exacto["reparto_optimo"]


def test_q_positivo_determinista_y_valido(inst):
    c1, c2 = ejecutar(inst, q=0.3, seed=5), ejecutar(inst, q=0.3, seed=5)
    assert c1.ok and [r.S for r in c1.rondas] == [r.S for r in c2.rondas]
    for r in c1.rondas:
        assert set(r.S) <= set(r.disponibles)
