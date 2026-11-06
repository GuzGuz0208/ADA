# HANDOFF — traspaso entre IAs (Claude ⇄ Codex/GPT)

Objetivo: poder cambiar de IA en cualquier momento sin perder nada y sin preguntarle al usuario qué se hizo.

## Quien SALE (o se queda sin cuota)
1. Terminar o dejar en estado coherente el archivo que se está editando (nada a medias sin avisar).
2. Ejecutar `pytest -q` y anotar el resultado real en el CHANGELOG.
3. Entrada en `agent/CHANGELOG.md` (Regla 0) y commit.
4. Reescribir `agent/CONTEXT.md`: estado por producto, **Siguiente paso inmediato** (1 acción concreta con archivo y comando), bloqueos, y `Testigo: <agente que entrega> → <agente que recibe>`.
5. Marcar en `agent/TASKS.md` el estado exacto (en curso / bloqueada / lista) y qué falta.
6. Si hay una decisión abierta que frena algo, ponerla arriba en `agent/DECISIONS.md`.
7. Avisar al usuario con una línea: "Listo para traspaso; abre <Codex/Claude> y pega prompts/PROMPT_*.md".

## Quien ENTRA
1. Pegar el prompt de `prompts/` (Claude: `PROMPT_VSCODE_CLAUDE.md`; Codex: `PROMPT_CODEX.md`).
2. Leer en el orden de `AGENTS.md`. Verificar con `git log --oneline -10` y `git status` que CONTEXT coincide con la realidad; si no coincide, **manda el repo**, y registrar la discrepancia.
3. Tomar el "Siguiente paso inmediato". No rehacer lo ya hecho; no reescribir archivos ajenos sin motivo registrado.
4. Primera acción de la sesión: entrada en CHANGELOG "sesión iniciada por <agente>" solo si ya hay cambios; si no, nada que registrar.

## Qué NO se traspasa por chat
Todo lo importante debe estar en archivos del repo. Si algo vive solo en la conversación (una decisión, un número, una cita), el que sale lo escribe en DECISIONS/CONTEXT antes de irse.

## Formato de `Testigo` en CONTEXT.md
`Testigo: claude-sonnet-5.5 (VS Code) → codex-gpt (2026-11-06 03:10)`
