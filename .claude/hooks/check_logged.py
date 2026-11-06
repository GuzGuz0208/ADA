#!/usr/bin/env python3
"""Stop hook: impide cerrar el turno si hay archivos del proyecto modificados DESPUES de la
ultima edicion de agent/CHANGELOG.md (es decir, cambios sin registrar).

Hace deterministica la Regla 0 de AGENTS.md para Claude Code. Se activa como maximo una vez por
turno (si Claude ya estaba continuando por este hook, `stop_hook_active` evita el bucle).
Ignora lo que vive en agent/ y .claude/. Si no hay git o hay cualquier error, no bloquea.
Solo libreria estandar.
"""
import json
import os
import subprocess
import sys


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        data = {}
    if data.get("stop_hook_active"):
        return
    root = os.environ.get("CLAUDE_PROJECT_DIR") or data.get("cwd") or os.getcwd()
    changelog = os.path.join(root, "agent", "CHANGELOG.md")
    if not os.path.exists(changelog):
        return
    try:
        out = subprocess.run(
            ["git", "status", "--porcelain", "-uall"],
            cwd=root, capture_output=True, text=True, timeout=20,
        )
    except Exception:
        return
    if out.returncode != 0:
        return
    changelog_mtime = os.path.getmtime(changelog)
    pending = []
    for line in out.stdout.splitlines():
        if len(line) < 4:
            continue
        p = line[3:].strip().strip('"')
        if " -> " in p:
            p = p.split(" -> ")[-1]
        p = p.replace("\\", "/")
        if p.startswith(("agent/", ".claude/")):
            continue
        full = os.path.join(root, p)
        if os.path.exists(full) and os.path.getmtime(full) > changelog_mtime + 1:
            pending.append(p)
    if pending:
        shown = ", ".join(pending[:8]) + (" ..." if len(pending) > 8 else "")
        reason = (
            "REGLA 0 (registro sagrado): hay cambios sin registrar: " + shown + ". "
            "Invoca al subagente `scribe` para anadir la entrada en agent/CHANGELOG.md "
            "y actualizar agent/CONTEXT.md y agent/TASKS.md antes de terminar el turno."
        )
        print(json.dumps({"decision": "block", "reason": reason}))


try:
    main()
except Exception:
    pass
sys.exit(0)
