"""Linea de comandos: ``run`` (ejecuta un caso) y ``generar`` (instancia sintetica)."""
from __future__ import annotations

import argparse
import json
import statistics
import sys
import time
from pathlib import Path

from . import SEMILLA_POR_DEFECTO
from .generator import generar
from .io import EntradaInvalida, cargar
from .rounds import MODOS, POLITICAS, comparar_exacto, ejecutar
from .trace import escribir_json, escribir_tiempos, escribir_traza


def cmd_run(args) -> int:
    """Carga, ejecuta con calentamiento y N repeticiones, escribe resultado/tiempo/traza. Devuelve codigo de salida.

    0 = todo cumple; 2 = entrada invalida; 3 = alguna restriccion o certificado fallo.
    """
    try:
        t_c = []
        for _ in range(max(1, args.repeticiones)):
            t0 = time.perf_counter()
            inst = cargar(args.input)
            t_c.append(time.perf_counter() - t0)
    except EntradaInvalida as ex:
        print(f"ERROR: {ex}", file=sys.stderr)
        return 2
    kw = dict(modo=args.modo, q=args.q, seed=args.seed, politica=args.politica)
    ejecutar(inst, **kw)                                   # calentamiento (no se mide)
    muestras: dict = {"carga_json": t_c}
    corrida = None
    for _ in range(max(1, args.repeticiones)):
        corrida = ejecutar(inst, **kw)
        for fase, v in corrida.tiempos.items():
            muestras.setdefault(fase, []).append(v)
    t_ex = comparar_exacto(corrida)
    if t_ex:
        muestras["referencia_exacta (1 corrida)"] = [t_ex]
    destino = Path(args.out) / f"caso_{inst.nombre}"
    destino.mkdir(parents=True, exist_ok=True)
    escribir_json(corrida, destino / "resultado.json")
    escribir_tiempos(destino / "tiempo.csv", muestras, args.repeticiones)
    escribir_traza(corrida, destino / "traza.md", destino / "traza.csv")
    print(f"Caso {inst.nombre}: N={inst.N} T={inst.T} k={inst.k} B={inst.B} L={inst.L} modo={args.modo}")
    for r in corrida.rondas:
        print(f"  ronda {r.t}: S={[inst.ids[i] for i in r.S]} f={r.f:.4f} costo={r.costo} "
              f"reparto={ {inst.ids[i]: r.x[i] for i in r.S} } u={r.utilidad:.4f}")
    print(f"  suma f={corrida.f_total:.4f}  suma u={corrida.utilidad_total:.4f}  "
          f"pipeline (mediana)={statistics.median(muestras['pipeline_total']) * 1e3:.3f} ms")
    print(f"  restricciones y certificados: {'TODO CUMPLE' if corrida.ok else 'FALLO (ver resultado.json)'}")
    print(f"  salida: {destino}")
    return 0 if corrida.ok else 3


def cmd_generar(args) -> int:
    """Escribe una instancia sintetica (mismo esquema) en --out. Determinista por --seed."""
    d = generar(args.n, rondas=args.rondas, k=args.k, B=args.B, L=args.L, seed=args.seed, densidad=args.densidad)
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(json.dumps(d, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"escrito {args.out} (N={args.n}, aristas={len(d['grafo'])}, semilla={args.seed})")
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="ada_g2", description="ADA 2026-B Grupo 2")
    sp = ap.add_subparsers(dest="cmd", required=True)
    r = sp.add_parser("run", help="ejecutar un caso JSON")
    r.add_argument("--input", required=True)
    r.add_argument("--out", required=True)
    r.add_argument("--modo", choices=MODOS, default="ambos")
    r.add_argument("--seed", type=int, default=SEMILLA_POR_DEFECTO)
    r.add_argument("--repeticiones", type=int, default=5)
    r.add_argument("--q", type=float, default=0.0, help="prob. de falla por nodo y ronda (D-07: 0)")
    r.add_argument("--politica", choices=POLITICAS, default="concentrado")
    r.set_defaults(fn=cmd_run)
    g = sp.add_parser("generar", help="generar instancia sintetica con semilla fija")
    g.add_argument("--n", type=int, required=True)
    g.add_argument("--rondas", type=int, default=3)
    g.add_argument("--k", type=int, default=5)
    g.add_argument("--B", type=int, default=30)
    g.add_argument("--L", type=int, default=None)
    g.add_argument("--seed", type=int, default=SEMILLA_POR_DEFECTO)
    g.add_argument("--densidad", type=float, default=1.0)
    g.add_argument("--out", required=True)
    g.set_defaults(fn=cmd_generar)
    args = ap.parse_args(argv)
    return args.fn(args)
