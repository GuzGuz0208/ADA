"""Carga y validacion del JSON de entrada (esquema de la profesora).

Nada de constantes del caso: todo sale del archivo. Si el esquema no se cumple se
lanza ``EntradaInvalida`` con TODOS los errores encontrados, cada uno con su ruta
(p. ej. ``nodos[3].costo_participacion``).
"""
from __future__ import annotations

import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np


class EntradaInvalida(ValueError):
    """El JSON no cumple el esquema esperado."""


@dataclass(eq=False)
class Instancia:
    """Instancia validada. Indices de nodo 0..N-1 siguen el orden de ``nodos`` en el JSON.

    a: coeficiente_utilidad; R: presupuesto_total_nodo; c: costo_participacion;
    W: matriz simetrica de influencia con W[i,i]=1 (D-02, D-10).
    """

    nombre: str
    ids: tuple
    a: np.ndarray
    R: tuple
    c: tuple
    W: np.ndarray
    T: int
    k: int
    B: int
    L: int
    n_aristas: int
    avisos: tuple

    @property
    def N(self) -> int:
        return len(self.ids)


def _entero(v: Any, ruta: str, err: list, minimo: int):
    """Devuelve v como int si es entero (o float integral) >= minimo; si no, anota error."""
    if isinstance(v, bool) or not isinstance(v, (int, float)):
        err.append(f"{ruta}: debe ser un entero, se recibio {v!r}")
        return None
    if isinstance(v, float) and (not math.isfinite(v) or v != int(v)):
        err.append(f"{ruta}: debe ser un entero, se recibio {v!r}")
        return None
    v = int(v)
    if v < minimo:
        err.append(f"{ruta}: debe ser >= {minimo}, se recibio {v}")
        return None
    return v


def _real(v: Any, ruta: str, err: list):
    if isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v):
        err.append(f"{ruta}: debe ser un numero finito, se recibio {v!r}")
        return None
    return float(v)


def _campo(d: Any, clave: str, ruta: str, err: list) -> Any:
    if not isinstance(d, dict):
        err.append(f"{ruta}: debe ser un objeto JSON")
        return None
    if clave not in d:
        err.append(f"{ruta}: falta el campo '{clave}'")
        return None
    return d[clave]


def desde_dict(d: Any, nombre: str = "instancia") -> Instancia:
    """Valida un dict con el esquema {parametros, grafo, nodos} y construye la Instancia.

    Pre: d proviene de json.load. Post: Instancia con W simetrica, W[i,i]=1; o
    EntradaInvalida con la lista completa de problemas. T(n)=O(N + |aristas|) (+ O(N^2) para W).
    """
    err: list = []
    avisos: list = []
    if not isinstance(d, dict):
        raise EntradaInvalida("la raiz del JSON debe ser un objeto con 'parametros', 'grafo' y 'nodos'")
    p = _campo(d, "parametros", "raiz", err)
    grafo = _campo(d, "grafo", "raiz", err)
    nodos = _campo(d, "nodos", "raiz", err)
    claves = {
        "numero_nodos": 1, "numero_rondas": 1, "cupo_participantes_por_ronda_k": 1,
        "presupuesto_ruido_por_ronda_B": 0, "presupuesto_costos_participacion_por_ronda": 0,
    }
    val: dict = {}
    if p is not None:
        for cl, mn in claves.items():
            v = _campo(p, cl, "parametros", err)
            if v is not None:
                val[cl] = _entero(v, f"parametros.{cl}", err, mn)
    ids: list = []
    a_l: list = []
    r_l: list = []
    c_l: list = []
    if nodos is not None:
        if not isinstance(nodos, list) or not nodos:
            err.append("nodos: debe ser una lista no vacia")
        else:
            vistos: dict = {}
            for pos, nd in enumerate(nodos):
                ru = f"nodos[{pos}]"
                nid = _campo(nd, "id", ru, err)
                if nid is not None:
                    if not isinstance(nid, str) or not nid:
                        err.append(f"{ru}.id: debe ser un texto no vacio")
                    elif nid in vistos:
                        err.append(f"{ru}.id: id repetido '{nid}' (ya aparece en nodos[{vistos[nid]}])")
                    else:
                        vistos[nid] = pos
                ids.append(nid)
                cu = _campo(nd, "coeficiente_utilidad", ru, err)
                cu = None if cu is None else _real(cu, f"{ru}.coeficiente_utilidad", err)
                if cu is not None and cu <= 0:
                    err.append(f"{ru}.coeficiente_utilidad: debe ser > 0, se recibio {cu}")
                    cu = None
                a_l.append(cu)
                pt = _campo(nd, "presupuesto_total_nodo", ru, err)
                r_l.append(None if pt is None else _entero(pt, f"{ru}.presupuesto_total_nodo", err, 0))
                cp = _campo(nd, "costo_participacion", ru, err)
                c_l.append(None if cp is None else _entero(cp, f"{ru}.costo_participacion", err, 0))
    n = len(ids)
    nn = val.get("numero_nodos")
    if nn is not None and n and nn != n:
        err.append(f"parametros.numero_nodos={nn} no coincide con len(nodos)={n}")
    W = np.eye(n) if n else np.zeros((0, 0))
    n_ar = 0
    if grafo is not None:
        if not isinstance(grafo, list):
            err.append("grafo: debe ser una lista de aristas {u, v, peso_influencia}")
        else:
            idx = {nid: i for i, nid in enumerate(ids) if isinstance(nid, str)}
            par: dict = {}
            for pos, e in enumerate(grafo):
                ru = f"grafo[{pos}]"
                u = _campo(e, "u", ru, err)
                v = _campo(e, "v", ru, err)
                w = _campo(e, "peso_influencia", ru, err)
                w = None if w is None else _real(w, f"{ru}.peso_influencia", err)
                bad = False
                for nm, x in (("u", u), ("v", v)):
                    if x is not None and x not in idx:
                        err.append(f"{ru}.{nm}: arista a nodo inexistente '{x}'")
                        bad = True
                if u is None or v is None or w is None or bad:
                    continue
                if u == v:
                    err.append(f"{ru}: autolazo en '{u}' (w_ii=1 se fija por el modelo, D-02)")
                    continue
                if not 0.0 <= w <= 1.0:
                    err.append(f"{ru}.peso_influencia: debe estar en [0,1], se recibio {w}")
                    continue
                clave = (min(idx[u], idx[v]), max(idx[u], idx[v]))
                if clave in par and par[clave] != w:
                    err.append(f"{ru}: arista {u}-{v} repetida con peso distinto ({par[clave]} vs {w}); "
                               "el grafo se trata como no dirigido (D-10)")
                    continue
                par[clave] = w
            if not err:
                for (i, j), w in par.items():
                    W[i, j] = W[j, i] = w
                n_ar = len(par)
    if err:
        raise EntradaInvalida(f"Entrada invalida ({len(err)} problema(s)):\n  - " + "\n  - ".join(err))
    k, T = val["cupo_participantes_por_ronda_k"], val["numero_rondas"]
    if k >= n:
        avisos.append(f"k={k} >= N={n}: el enunciado supone k<N; la restriccion de cupo no es activa")
    return Instancia(
        nombre=nombre, ids=tuple(ids), a=np.array(a_l, dtype=float), R=tuple(r_l), c=tuple(c_l),
        W=W, T=T, k=k, B=val["presupuesto_ruido_por_ronda_B"],
        L=val["presupuesto_costos_participacion_por_ronda"], n_aristas=n_ar, avisos=tuple(avisos),
    )


def cargar(ruta) -> Instancia:
    """Lee y valida un archivo JSON. Pre: ruta existe. Post: Instancia (nombre = nombre del archivo sin extension)."""
    ruta = Path(ruta)
    try:
        with open(ruta, encoding="utf-8") as fh:
            d = json.load(fh)
    except FileNotFoundError:
        raise EntradaInvalida(f"no existe el archivo de entrada: {ruta}") from None
    except json.JSONDecodeError as ex:
        raise EntradaInvalida(f"{ruta}: JSON mal formado (linea {ex.lineno}, col {ex.colno}): {ex.msg}") from None
    return desde_dict(d, nombre=ruta.stem)
