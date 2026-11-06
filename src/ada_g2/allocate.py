"""Parte 1: reparto voraz del presupuesto de ruido con monticulo (Algoritmo 3.2.1, D-06, D-12).

Maximiza sum_i a_i ln(1+x_i) sujeto a sum x_i <= B, 0 <= x_i <= r_i, x_i entero.
Optimo por argumento de intercambio (SPEC T1): se toman las B mayores ganancias marginales.
"""
from __future__ import annotations

import heapq
from dataclasses import dataclass, field

from .model import ganancia_marginal, utilidad


@dataclass
class PasoReparto:
    """Una unidad asignada: paso (1..), posicion local del nodo, x antes, ganancia marginal, utilidad acumulada."""

    paso: int
    nodo: int
    x_antes: int
    ganancia: float
    utilidad_acum: float


@dataclass
class ResultadoReparto:
    x: list
    utilidad: float
    unidades: int
    traza: list = field(default_factory=list)
    pasos_monticulo: int = 0


def asignar(a: list, topes: list, B: int) -> ResultadoReparto:
    """Reparto voraz exacto.

    Pre: a[i]>0, topes[i]>=0 enteros, B>=0 entero; la posicion i es el orden de desempate (menor i gana, D-12).
    Pos: x[i] en [0, topes[i]], sum x <= B, y sum u_i(x_i) es maximo (Teorema 3.2.1). Si sum topes < B se agota
    el tope de todos y sobra presupuesto. Invariante: tras j pasos el montículo contiene, para cada nodo con
    x_i<r_i, su proxima ganancia g_i(x_i), y las j unidades tomadas son las j mayores ganancias del multiconjunto.
    T(N,B) = O(N) [heapify] + B * O(log N) [heapreplace/heappop] = O(N + B log N)  (pseudo-polinomial en B).
    """
    n = len(a)
    x = [0] * n
    heap = [(-ganancia_marginal(a[i], 0), i) for i in range(n) if topes[i] > 0]
    heapq.heapify(heap)                                   # O(N)
    traza: list = []
    util = 0.0
    paso = 0
    ops = len(heap)
    while paso < B and heap:                              # <= B iteraciones
        negg, i = heap[0]
        g = -negg
        paso += 1
        util += g
        traza.append(PasoReparto(paso, i, x[i], g, util))
        x[i] += 1
        if x[i] < topes[i]:
            heapq.heapreplace(heap, (-ganancia_marginal(a[i], x[i]), i))   # O(log N)
        else:
            heapq.heappop(heap)                                            # O(log N)
        ops += 1
    # utilidad recomputada directamente (evita acumular error de la suma de ganancias)
    util_dir = sum(utilidad(a[i], x[i]) for i in range(n))
    return ResultadoReparto(x=x, utilidad=util_dir, unidades=paso, traza=traza, pasos_monticulo=ops)
