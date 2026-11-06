"""Pruebas minimas de humo (el verifier hara las independientes)."""
import random
from pathlib import Path

import numpy as np
import pytest

from ada_g2.allocate import asignar
from ada_g2.exact import dp_reparto, fuerza_bruta
from ada_g2.generator import generar
from ada_g2.io import EntradaInvalida, cargar, desde_dict
from ada_g2.rounds import comparar_exacto, ejecutar
from ada_g2.select import limites, seleccionar

RAIZ = Path(__file__).resolve().parent.parent
CASO = RAIZ / "project-docs" / "entrada_G2_red_15_nodos.json"


def test_reparto_igual_a_dp():
    rng = random.Random(1)
    for _ in range(60):
        n = rng.randint(1, 5)
        a = [rng.uniform(0.5, 10) for _ in range(n)]
        topes = [rng.randint(0, 6) for _ in range(n)]
        B = rng.randint(0, 15)
        r = asignar(a, topes, B)
        assert sum(r.x) <= B and all(x <= t for x, t in zip(r.x, topes))
        assert r.utilidad == pytest.approx(dp_reparto(a, topes, B)[0], abs=1e-9)


def test_caso_profesora_cumple_restricciones():
    inst = cargar(CASO)
    c = ejecutar(inst)
    assert c.ok
    for r in c.rondas:
        assert len(r.S) <= inst.k and r.costo <= inst.L and sum(r.x.values()) <= inst.B
        assert all(v <= inst.R[i] for i, v in r.x.items())
    comparar_exacto(c)
    assert all(r.exacto["reparto_optimo"] for r in c.rondas)
    assert all(r.exacto["razon_voraz_sobre_optimo"] >= 1 - 1 / np.e for r in c.rondas)


def test_voraz_vs_fuerza_bruta_generado():
    inst = desde_dict(generar(10, k=3, B=12, seed=3))
    mask = np.ones(inst.N, dtype=bool)
    kmax, Lmax = limites("ambos", inst.k, inst.L, inst.N)
    s = seleccionar(inst.W, inst.a, inst.c, mask, inst.k, inst.L, "ambos").mejor
    ex = fuerza_bruta(inst.W, inst.a, inst.c, list(range(inst.N)), kmax, Lmax)
    assert s.f <= ex.f + 1e-9 and len(s.S) <= inst.k and s.costo <= inst.L


def test_generador_determinista():
    assert generar(8, seed=5) == generar(8, seed=5)
    assert generar(8, seed=5) != generar(8, seed=6)


def test_validacion_mensajes():
    d = generar(4, k=2, seed=1)
    d["nodos"][1]["id"] = d["nodos"][0]["id"]
    d["grafo"][0]["v"] = "NXX"
    del d["nodos"][2]["costo_participacion"]
    d["parametros"]["cupo_participantes_por_ronda_k"] = 0
    with pytest.raises(EntradaInvalida) as ex:
        desde_dict(d)
    msg = str(ex.value)
    for frag in ("id repetido", "inexistente", "costo_participacion", "cupo_participantes_por_ronda_k"):
        assert frag in msg
