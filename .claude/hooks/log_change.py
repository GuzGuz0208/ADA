#!/usr/bin/env python3
"""PostToolUse (Write|Edit|MultiEdit|NotebookEdit): anota en agent/log/auto_changes.log
cada archivo que Claude Code escribe o edita.

Es la traza CRUDA y automatica (determinista: corre siempre, a diferencia de una instruccion).
NO sustituye la entrada semantica de agent/CHANGELOG.md, que escribe el subagente `scribe`.
Nunca debe fallar ni bloquear la herramienta: cualquier error se ignora.
Solo libreria estandar.
"""
import datetime
import json
import os
import sys


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        return
    ti = data.get("tool_input") or {}
    path = ti.get("file_path") or ti.get("notebook_path") or ""
    if not path:
        return
    root = os.environ.get("CLAUDE_PROJECT_DIR") or data.get("cwd") or os.getcwd()
    try:
        rel = os.path.relpath(path, root) if os.path.isabs(path) else path
    except ValueError:  # otra unidad en Windows
        rel = path
    rel = rel.replace("\\", "/")
    if rel.startswith("agent/log/") or rel.startswith("../"):
        return  # la propia traza, o archivos fuera del repo (p. ej. planes de Claude Code)
    bogota = datetime.timezone(datetime.timedelta(hours=-5))  # America/Bogota, sin horario de verano
    ts = datetime.datetime.now(bogota).strftime("%Y-%m-%d %H:%M:%S")
    line = "{}\t{}\t{}\tsesion={}\n".format(
        ts, data.get("tool_name", "?"), rel, str(data.get("session_id", ""))[:8]
    )
    logdir = os.path.join(root, "agent", "log")
    os.makedirs(logdir, exist_ok=True)
    with open(os.path.join(logdir, "auto_changes.log"), "a", encoding="utf-8", newline="\n") as fh:
        fh.write(line)


try:
    main()
except Exception:
    pass
sys.exit(0)
