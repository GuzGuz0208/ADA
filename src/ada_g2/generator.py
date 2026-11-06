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


def instancia_ajustada(k: int):
    """Instancia ajustada de la cota del voraz (D-15, W3): familia general de cobertura 0/1 (M != N).

    Pre: k >= 2 entero. Construye 2k candidatos sobre M = k * k^k objetivos con a_j = 1:
      - candidatos 0..k-1 = "trampas": la trampa j cubre, en cada conjunto optimo, una capa de
        k^(k-(j+1)) * (k-1)^j elementos;
      - candidatos k..2k-1 = conjuntos optimos disjuntos de m = k^k elementos cada uno.
    Con desempate por menor indice (D-12) y las trampas indexadas primero, el voraz con cupo k elige
    las k trampas y obtiene k*m*(1-(1-1/k)^k), mientras el optimo (los k conjuntos optimos) vale k*m.
    Pos: devuelve (W, a, m) con W in {0,1}^{2k x M}, a = unos(M); razon voraz/optimo = 1-(1-1/k)^k.
    T = O(k * M) = O(k^(k+2)) para llenar W.
    """
    import numpy as np

    if k < 2:
        raise ValueError("k debe ser >= 2")
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
    W = np.zeros((2 * k, elem))
    for j in range(k):
        W[j, trampas[j]] = 1.0
    for i in range(k):
        W[k + i, optimos[i]] = 1.0
    return W, np.ones(elem), m
