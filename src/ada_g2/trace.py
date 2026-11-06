"""Escritura de resultado.json, tiempo.csv, traza.md y traza.csv a partir de una ``Corrida``."""
from __future__ import annotations

import csv
import json
import platform
import statistics
import sys
from pathlib import Path

from . import __version__
from .rounds import Corrida


def _sel_dict(inst, r) -> dict:
    return {
        "elegida": r.seleccion.mejor.heuristica,
        "alternativas": [{"heuristica": h.heuristica, "S": [inst.ids[i] for i in h.S], "f": h.f, "costo": h.costo}
                         for h in r.seleccion.alternativas],
    }


def a_dict(c: Corrida) -> dict:
    """Serializa la corrida a un dict JSON-able (resultado.json). T=O(T*N)."""
    inst = c.inst
    rondas = []
    for r in c.rondas:
        rondas.append({
            "ronda": r.t,
            "disponibles": [inst.ids[i] for i in r.disponibles],
            "seleccion": [inst.ids[i] for i in r.S],
            "detalle_seleccion": _sel_dict(inst, r),
            "f": r.f, "costo_participacion": r.costo,
            "topes_antes": {inst.ids[i]: r.rem_antes[i] for i in r.S},
            "topes_efectivos": {inst.ids[i]: r.topes[i] for i in r.S},
            "reparto": {inst.ids[i]: r.x[i] for i in r.S},
            "unidades_asignadas": r.reparto.unidades, "gasto_ruido": sum(r.x.values()),
            "utilidad": r.utilidad,
            "verificacion_restricciones": r.verificacion,
            "certificado_reparto": r.cert_reparto, "certificado_seleccion": r.cert_seleccion,
            "comparacion_exacto": r.exacto,
        })
    return {
        "version": __version__, "caso": inst.nombre,
        "entorno": {"python": sys.version.split()[0], "plataforma": platform.platform()},
        "parametros": {"N": inst.N, "T": inst.T, "k": inst.k, "B": inst.B, "L": inst.L, "aristas": inst.n_aristas,
                       "modo": c.modo, "q": c.q, "politica_gasto": c.politica, "semilla": c.seed},
        "avisos": list(inst.avisos),
        "rondas": rondas,
        "totales": {"suma_f": c.f_total, "suma_utilidad": c.utilidad_total,
                    "gasto_por_nodo": {inst.ids[i]: c.gasto_total[i] for i in range(inst.N)
                                       if c.gasto_total[i] > 0},
                    "presupuesto_total_nodo": {inst.ids[i]: inst.R[i] for i in range(inst.N)}},
        "verificacion_global": c.verificacion_global,
        "todo_cumple": bool(c.ok),
    }


def escribir_tiempos(path: Path, filas: dict, repeticiones: int) -> None:
    """filas: fase -> lista de muestras (s). Escribe mediana/min/max (perf_counter, D-11)."""
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["fase", "repeticiones", "mediana_s", "minimo_s", "maximo_s"])
        for fase, v in filas.items():
            w.writerow([fase, len(v), f"{statistics.median(v):.9f}", f"{min(v):.9f}", f"{max(v):.9f}"])


def _lista_eval(inst, evaluados, tope=None) -> str:
    ev = sorted(evaluados, key=lambda t: (-t[1], t[0]))
    if tope is not None and len(ev) > tope:
        return ", ".join(f"{inst.ids[i]}={g:.4f}" for i, g in ev[:tope]) + f", ... (+{len(ev) - tope})"
    return ", ".join(f"{inst.ids[i]}={g:.4f}" for i, g in ev)


def escribir_traza(c: Corrida, md: Path, csv_path: Path) -> None:
    """traza.md (legible) y traza.csv (una fila por evento). T = O(tamanio de la traza)."""
    inst = c.inst
    L = [f"# Traza - caso `{inst.nombre}`", "",
         f"Modo `{c.modo}` | N={inst.N} T={inst.T} k={inst.k} B={inst.B} L={inst.L} | politica `{c.politica}` | "
         f"q={c.q} | semilla {c.seed} | version {__version__}", ""]
    rows = []
    for r in c.rondas:
        L += [f"## Ronda {r.t}", "", f"Disponibles ({len(r.disponibles)}): "
              + ", ".join(inst.ids[i] for i in r.disponibles), ""]
        L += ["### Seleccion (Parte 2)", ""]
        for h in r.seleccion.alternativas:
            marca = " **(elegida)**" if h is r.seleccion.mejor else ""
            L += [f"**{h.heuristica}**{marca}: S = {{{', '.join(inst.ids[i] for i in h.S)}}}, "
                  f"f = {h.f:.6f}, costo = {h.costo}", ""]
            if h.pasos:
                L += ["| paso | elegido | ganancia marginal | puntaje | costo acum. | f acum. | ganancias de los candidatos factibles |",
                      "|---|---|---|---|---|---|---|"]
            for p in h.pasos:
                L.append(f"| {p.paso} | {inst.ids[p.elegido]} | {p.ganancia:.6f} | {p.puntaje:.6f} | "
                         f"{p.costo_acum} | {p.f_acum:.6f} | {_lista_eval(inst, p.evaluados, 10)} |")
                rows.append([r.t, "seleccion", h.heuristica, p.paso, inst.ids[p.elegido], f"{p.ganancia:.12g}",
                             f"costo_acum={p.costo_acum};f_acum={p.f_acum:.12g};puntaje={p.puntaje:.12g}"])
                for j, g in p.evaluados:
                    rows.append([r.t, "seleccion_candidato", h.heuristica, p.paso, inst.ids[j], f"{g:.12g}", ""])
            L.append("")
        L += ["### Reparto (Parte 1), unidad a unidad", "",
              f"Participantes: {', '.join(inst.ids[i] for i in r.S) or '(ninguno)'}; topes: "
              + ", ".join(f"{inst.ids[i]}={r.topes[i]}" for i in r.S), "",
              "| unidad | nodo | x antes | ganancia marginal | utilidad acum. |", "|---|---|---|---|---|"]
        for p in r.reparto.traza:
            nid = inst.ids[r.S[p.nodo]]
            L.append(f"| {p.paso} | {nid} | {p.x_antes} | {p.ganancia:.6f} | {p.utilidad_acum:.6f} |")
            rows.append([r.t, "reparto", "voraz_monticulo", p.paso, nid, f"{p.ganancia:.12g}",
                         f"x_antes={p.x_antes};utilidad_acum={p.utilidad_acum:.12g}"])
        L += ["", f"Reparto final: " + ", ".join(f"{inst.ids[i]}={r.x[i]}" for i in r.S)
              + f" | utilidad = {r.utilidad:.6f}", ""]
        L += ["### Verificacion de restricciones", "",
              "| restriccion | valor | limite | aplica | cumple |", "|---|---|---|---|---|"]
        for ch in r.verificacion:
            L.append(f"| {ch['restriccion']} | {ch['valor']} | {ch['limite']} | {'si' if ch['aplica'] else 'no'} | "
                     f"{'SI' if ch['cumple'] else 'NO'} |")
            rows.append([r.t, "verificacion", ch["restriccion"], "", "", ch["valor"] if not isinstance(ch["valor"], list)
                         else ";".join(ch["valor"]), f"limite={ch['limite']};aplica={ch['aplica']};cumple={ch['cumple']}"])
        cr, cs = r.cert_reparto, r.cert_seleccion
        if cr:
            L += ["", f"Certificado reparto (dualidad): lambda = {cr['lambda']:.6f}, cota = {cr['cota_superior']:.9f}, "
                  f"utilidad = {cr['utilidad']:.9f}, brecha = {cr['brecha']:.2e}, ok = {cr['ok']}"]
            rows.append([r.t, "certificado", "dualidad_reparto", "", "", f"{cr['brecha']:.3e}", f"ok={cr['ok']}"])
        if cs and cs.get("cota_superior") is not None:
            L += [f"Certificado seleccion (LP): f(S) = {cs['f_S']:.6f}, cota superior del optimo = "
                  f"{cs['cota_superior']:.6f}, razon certificada >= {cs['razon_certificada']:.6f}, ok = {cs['ok']}"]
            rows.append([r.t, "certificado", "lp_seleccion", "", "", f"{cs['razon_certificada']:.9g}", f"ok={cs['ok']}"])
        if r.exacto:
            e = r.exacto
            L += ["", f"Exacto: S* = {{{', '.join(e['seleccion_optima'])}}}, f* = {e['f_optima']:.6f}, "
                  f"razon voraz/optimo = {e['razon_voraz_sobre_optimo']:.6f} "
                  f"({e['subconjuntos_evaluados']} subconjuntos); reparto DP = {e['reparto_dp_utilidad']}"]
        L.append("")
    L += ["## Verificacion global", "", "| restriccion | cumple |", "|---|---|"]
    for ch in c.verificacion_global:
        L.append(f"| {ch['restriccion']} | {'SI' if ch['cumple'] else 'NO'} |")
        rows.append([0, "verificacion", ch["restriccion"], "", "", "", f"cumple={ch['cumple']}"])
    L += ["", f"Suma de f = {c.f_total:.6f}; suma de utilidades = {c.utilidad_total:.6f}; "
          f"todo cumple = {c.ok}", ""]
    md.write_text("\n".join(L), encoding="utf-8")
    with open(csv_path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["ronda", "fase", "heuristica_o_restriccion", "paso", "nodo", "valor", "detalle"])
        w.writerows(rows)


def escribir_json(c: Corrida, path: Path) -> None:
    path.write_text(json.dumps(a_dict(c), indent=2, ensure_ascii=False), encoding="utf-8")
