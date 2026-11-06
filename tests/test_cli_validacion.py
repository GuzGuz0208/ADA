"""Validacion de entrada (exit 2 + mensaje claro) y CLI sobre JSON sinteticos (sin constantes del caso)."""
import copy
import json
import random

import pytest

from ada_g2.cli import main
from ada_g2.generator import generar
from ada_g2.io import cargar
from ada_g2.rounds import ejecutar
from helpers import CASO


def base():
    return json.loads(CASO.read_text(encoding="utf-8"))


def correr(tmp_path, d, *extra, nombre="x.json"):
    p = tmp_path / nombre
    p.write_text(d if isinstance(d, str) else json.dumps(d), encoding="utf-8")
    rc = main(["run", "--input", str(p), "--out", str(tmp_path / "out"), "--repeticiones", "1", *extra])
    return rc, tmp_path / "out" / f"caso_{p.stem}"


def m_quitar_nodos(d):
    del d["nodos"][3]["costo_participacion"]


def m_B_negativo(d):
    d["parametros"]["presupuesto_ruido_por_ronda_B"] = -1


def m_peso_fuera(d):
    d["grafo"][0]["peso_influencia"] = 1.5


def m_arista_inexistente(d):
    d["grafo"][2]["u"] = "ZZZ"


def m_id_repetido(d):
    d["nodos"][1]["id"] = d["nodos"][0]["id"]


def m_numero_nodos(d):
    d["parametros"]["numero_nodos"] = 14


def m_coef_cero(d):
    d["nodos"][0]["coeficiente_utilidad"] = 0


def m_k_float(d):
    d["parametros"]["cupo_participantes_por_ronda_k"] = 2.5


def m_sin_grafo(d):
    del d["grafo"]


def m_texto(d):
    d["nodos"][0]["presupuesto_total_nodo"] = "18"


def m_autolazo(d):
    d["grafo"][0]["v"] = d["grafo"][0]["u"]


def m_bool(d):
    d["parametros"]["numero_rondas"] = True


def m_peso_contradictorio(d):
    e = copy.deepcopy(d["grafo"][0])
    e["u"], e["v"], e["peso_influencia"] = e["v"], e["u"], 0.123
    d["grafo"].append(e)


CASOS_MAL = [(m_quitar_nodos, "costo_participacion"), (m_B_negativo, "presupuesto_ruido_por_ronda_B"),
             (m_peso_fuera, "peso_influencia"), (m_arista_inexistente, "inexistente"),
             (m_id_repetido, "repetido"), (m_numero_nodos, "numero_nodos"), (m_coef_cero, "coeficiente_utilidad"),
             (m_k_float, "cupo_participantes_por_ronda_k"), (m_sin_grafo, "grafo"),
             (m_texto, "presupuesto_total_nodo"), (m_autolazo, "autolazo"), (m_bool, "numero_rondas"),
             (m_peso_contradictorio, "repetida")]


@pytest.mark.parametrize("mut,frag", CASOS_MAL, ids=[m.__name__ for m, _ in CASOS_MAL])
def test_entrada_invalida_exit_2(tmp_path, capsys, mut, frag):
    d = base()
    mut(d)
    rc, _ = correr(tmp_path, d)
    err = capsys.readouterr().err
    assert rc == 2, err
    assert "ERROR" in err and frag in err


def test_json_mal_formado_y_archivo_inexistente(tmp_path, capsys):
    rc, _ = correr(tmp_path, '{"parametros": ')
    assert rc == 2 and "mal formado" in capsys.readouterr().err
    rc = main(["run", "--input", str(tmp_path / "nada.json"), "--out", str(tmp_path / "o")])
    assert rc == 2 and "no existe" in capsys.readouterr().err
    rc, _ = correr(tmp_path, "[1,2]")
    assert rc == 2
    rc, _ = correr(tmp_path, {})
    assert rc == 2


def test_se_reportan_todos_los_errores_juntos(tmp_path, capsys):
    d = base()
    m_B_negativo(d)
    d["grafo"][60]["peso_influencia"] = 1.5      # arista lejos de las que toca el id repetido
    m_id_repetido(d)
    rc, _ = correr(tmp_path, d)
    err = capsys.readouterr().err
    assert rc == 2 and "problema(s)" in err and all(f in err for f in ("presupuesto_ruido_por_ronda_B", "peso_influencia", "repetido"))


def test_cli_caso_profesora_numeros(tmp_path, capsys):
    rc, destino = correr(tmp_path, CASO.read_text(encoding="utf-8"), nombre="prof.json")
    assert rc == 0
    out = capsys.readouterr().out
    assert "suma f=436.7386" in out and "suma u=262.7387" in out and "TODO CUMPLE" in out
    res = json.loads((destino / "resultado.json").read_text(encoding="utf-8"))
    assert res["todo_cumple"] is True
    assert (destino / "tiempo.csv").exists() and (destino / "traza.md").exists() and (destino / "traza.csv").exists()


@pytest.mark.parametrize("n,k,B,T,dens,seed", [(12, 4, 20, 2, 0.5, 7), (8, 3, 15, 4, 1.0, 1), (20, 6, 40, 3, 0.2, 99),
                                               (3, 1, 5, 1, 1.0, 3), (30, 10, 10, 3, 0.1, 5)])
def test_cli_json_sintetico(tmp_path, capsys, n, k, B, T, dens, seed):
    d = generar(n, rondas=T, k=k, B=B, seed=seed, densidad=dens)
    rc, destino = correr(tmp_path, d)
    out = capsys.readouterr().out
    assert rc == 0, out
    res = json.loads((destino / "resultado.json").read_text(encoding="utf-8"))
    assert res["todo_cumple"] is True and len(res["rondas"]) == T
    assert res["parametros"]["N"] == n and res["parametros"]["B"] == B and res["parametros"]["k"] == k
    inst = cargar(tmp_path / "x.json")
    c = ejecutar(inst)
    assert res["totales"] is not None
    for r, rr in zip(res["rondas"], c.rondas):
        assert sum(r["reparto"].values()) <= B and len(r["seleccion"]) <= k
        assert r["f"] == pytest.approx(rr.f)


def test_generador_cli_y_reproducibilidad(tmp_path):
    p1, p2 = tmp_path / "a.json", tmp_path / "b.json"
    assert main(["generar", "--n", "9", "--seed", "4", "--out", str(p1)]) == 0
    assert main(["generar", "--n", "9", "--seed", "4", "--out", str(p2)]) == 0
    assert p1.read_text() == p2.read_text()


def test_invariancia_por_permutacion_de_nodos(tmp_path):
    """Reordenar la lista de nodos no debe cambiar los totales (sin empates exactos)."""
    d = base()
    c0 = ejecutar(cargar_dict(d))
    d2 = copy.deepcopy(d)
    random.Random(3).shuffle(d2["nodos"])
    c1 = ejecutar(cargar_dict(d2))
    assert c1.f_total == pytest.approx(c0.f_total, abs=1e-9)
    assert c1.utilidad_total == pytest.approx(c0.utilidad_total, abs=1e-9)


def cargar_dict(d):
    from ada_g2.io import desde_dict
    return desde_dict(d)


@pytest.mark.parametrize("mut", [
    lambda d: d["parametros"].update(presupuesto_ruido_por_ronda_B=0),
    lambda d: d["parametros"].update(cupo_participantes_por_ronda_k=20),
    lambda d: d["parametros"].update(presupuesto_costos_participacion_por_ronda=0),
    lambda d: d["parametros"].update(numero_rondas=1),
    lambda d: [n.update(presupuesto_total_nodo=0) for n in d["nodos"][:10]],
    lambda d: [n.update(costo_participacion=0) for n in d["nodos"]],
    lambda d: d["grafo"].clear(),
], ids=["B0", "k>N", "L0", "T1", "diez_nodos_sin_tope", "costos0", "sin_aristas"])
@pytest.mark.parametrize("modo", ["k", "costo", "ambos"])
def test_casos_borde_no_revientan(mut, modo):
    d = base()
    mut(d)
    c = ejecutar(cargar_dict(d), modo=modo)
    assert c.ok
