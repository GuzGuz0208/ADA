"""Generador de instancias sinteticas con el MISMO esquema JSON de la profesora, con semilla fija.

Uso: python -m ada_g2 generar --n 30 --seed 7 --out instancia.json
"""
from __future__ import annotations

import random


def generar(n: int, rondas: int = 3, k: int = 5, B: int = 30, L: int | None = None, seed: int = 20261105,
            densidad: float = 1.0, r_nodo: tuple = (10, 24), costo: tuple = (2, 7),
            coef: tuple = (5.0, 15.0), peso: tuple = (0.1, 0.9)) -> dict:
    """Genera un dict {parametros, grafo, nodos} valido para ``io.desde_dict``.

    Pre: n>=2, 0<densidad<=1, rangos con min<=max. Pos: determinista dada la semilla; grafo no dirigido con cada
    par (u<v) presente con probabilidad ``densidad``; L por defecto = round(0.8*k*costo medio).
    T = O(n^2).
    """
    if n < 2:
        raise ValueError("n debe ser >= 2")
    if not 0 < densidad <= 1:
        raise ValueError("densidad debe estar en (0,1]")
    rng = random.Random(seed)
    w = max(2, len(str(n)))
    ids = [f"N{i + 1:0{w}d}" for i in range(n)]
    nodos = [{"id": ids[i], "coeficiente_utilidad": round(rng.uniform(*coef), 1),
              "presupuesto_total_nodo": rng.randint(*r_nodo), "costo_participacion": rng.randint(*costo)}
             for i in range(n)]
    grafo = []
    for i in range(n):
        for j in range(i + 1, n):
            if densidad >= 1 or rng.random() < densidad:
                grafo.append({"u": ids[i], "v": ids[j], "peso_influencia": round(rng.uniform(*peso), 2)})
    if L is None:
        L = max(1, round(0.8 * k * (costo[0] + costo[1]) / 2))
    return {
        "parametros": {"numero_nodos": n, "numero_rondas": rondas, "cupo_participantes_por_ronda_k": k,
                       "presupuesto_ruido_por_ronda_B": B, "presupuesto_costos_participacion_por_ronda": L},
        "grafo": grafo, "nodos": nodos,
    }
