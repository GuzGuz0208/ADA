"""Parte 2: seleccion voraz por ganancia marginal (modos k, costo, ambos; D-03, D-12).

Cada paso evalua Delta(i|S) de todos los candidatos con el vector residual R_j (tau = O(M)).
Modo 'k': |S|<=k. Modo 'costo': sum c<=L. Modo 'ambos': las dos. Con costo se toma el mejor de
{voraz por ganancia, voraz por ganancia/costo, mejor singleton factible}. No se afirma garantia teorica
para la combinacion (R-01).
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from .model import (actualizar_residual, f_directa, ganancias_todas,
                    residual_inicial)

MODOS = ("ambos", "k", "costo")
TOL = 1e-12


@dataclass
class PasoSeleccion:
    """Un paso: nodo elegido, su ganancia marginal y puntaje, ganancia de cada candidato factible evaluado."""

    paso: int
    elegido: int
    ganancia: float
    puntaje: float
    evaluados: list          # [(indice_nodo, ganancia_marginal)] de los candidatos factibles
    costo_acum: int
    f_acum: float


@dataclass
class ResultadoVoraz:
    heuristica: str
    S: list                  # en orden de eleccion
    f: float
    costo: int
    pasos: list = field(default_factory=list)


@dataclass
class ResultadoSeleccion:
    mejor: ResultadoVoraz
    alternativas: list       # todas las heuristicas ejecutadas (incluye la mejor)


def limites(modo: str, k: int, L: int, n_cand: int):
    """(kmax, Lmax) efectivos segun el modo. Pre: modo en MODOS. T=O(1)."""
    if modo not in MODOS:
        raise ValueError(f"modo desconocido '{modo}'; use uno de {MODOS}")
    kmax = k if modo in ("k", "ambos") else n_cand
    Lmax = L if modo in ("costo", "ambos") else float("inf")
    return kmax, Lmax


def voraz(W, a, c, cand: np.ndarray, kmax: int, Lmax, criterio: str) -> ResultadoVoraz:
    """Voraz por 'ganancia' o por 'razon' (ganancia/costo), respetando |S|<=kmax y costo<=Lmax en cada paso.

    Pre: cand es mascara booleana de candidatos; W simetrica con diagonal 1; c enteros>=0.
    Pos: S factible; f = sum de ganancias marginales = f(S). Para en k elementos o cuando ningun candidato
    factible tiene ganancia > 0. Desempate: menor indice (np.argmax devuelve la primera aparicion).
    T = O(kmax * N * M): kmax pasos, cada uno N evaluaciones de tau=O(M) (matvec W @ (a*R)) + O(N) elegir.
    """
    n = len(a)
    carr = np.asarray(c, dtype=float)
    R = residual_inicial(W.shape[1])
    en_S = np.zeros(n, dtype=bool)
    S: list = []
    pasos: list = []
    costo = 0
    f = 0.0
    while len(S) < kmax:
        gan = ganancias_todas(W, a, R)
        fact = cand & ~en_S & (costo + carr <= Lmax)
        if not fact.any():
            break
        if criterio == "ganancia":
            punt = gan
        else:
            with np.errstate(divide="ignore", invalid="ignore"):
                punt = np.where(carr > 0, gan / np.where(carr > 0, carr, 1.0), np.inf)
        masc = np.where(fact, punt, -np.inf)
        i = int(np.argmax(masc))
        if gan[i] <= 0:
            break
        f += float(gan[i])
        costo += int(carr[i])
        pasos.append(PasoSeleccion(len(S) + 1, i, float(gan[i]), float(punt[i]),
                                   [(int(j), float(gan[j])) for j in np.flatnonzero(fact)], costo, f))
        S.append(i)
        en_S[i] = True
        actualizar_residual(W, R, i)
    return ResultadoVoraz(f"voraz_{criterio}", S, f, costo, pasos)


def mejor_singleton(W, a, c, cand: np.ndarray, kmax: int, Lmax) -> ResultadoVoraz:
    """Mejor conjunto unitario factible (c_i<=Lmax). Pre/Pos como voraz. T = O(N*M)."""
    carr = np.asarray(c, dtype=float)
    gan = ganancias_todas(W, a, residual_inicial(W.shape[1]))
    fact = cand & (carr <= Lmax) if kmax >= 1 else np.zeros(len(a), dtype=bool)
    if not fact.any():
        return ResultadoVoraz("singleton", [], 0.0, 0, [])
    i = int(np.argmax(np.where(fact, gan, -np.inf)))
    paso = PasoSeleccion(1, i, float(gan[i]), float(gan[i]),
                         [(int(j), float(gan[j])) for j in np.flatnonzero(fact)], int(carr[i]), float(gan[i]))
    return ResultadoVoraz("singleton", [i], float(gan[i]), int(carr[i]), [paso])


def seleccionar(W, a, c, cand: np.ndarray, k: int, L: int, modo: str) -> ResultadoSeleccion:
    """Seleccion segun el modo. Pre: modo en MODOS; cand mascara booleana.

    Modo 'k': voraz por ganancia (garantia 1-1/e de Nemhauser-Wolsey-Fisher 1978 para f monotona submodular).
    Modos 'costo'/'ambos': mejor de {ganancia, razon, singleton}; en empate gana el primero en ese orden.
    T = O(k * N * M) (las tres heuristicas suman a lo sumo 2 voraces + 1 singleton).
    """
    kmax, Lmax = limites(modo, k, L, int(cand.sum()))
    alts = [voraz(W, a, c, cand, kmax, Lmax, "ganancia")]
    if modo != "k":
        alts.append(voraz(W, a, c, cand, kmax, Lmax, "razon"))
        alts.append(mejor_singleton(W, a, c, cand, kmax, Lmax))
    mejor = alts[0]
    for r in alts[1:]:
        if r.f > mejor.f + TOL:
            mejor = r
    return ResultadoSeleccion(mejor, alts)


def f_de(W, a, S) -> float:
    """f(S) directa (verificacion). T=O(|S| M)."""
    return f_directa(W, a, S)
