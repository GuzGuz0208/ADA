# CONTEXT — estado vivo del proyecto

> Reescribir en cada checkpoint (no acumular; ≤ ~150 líneas). Historia detallada: `agent/CHANGELOG.md`.

**Última actualización:** 2026-11-05 21:56 (America/Bogota) · claude-opus-5.5 (Claude Code en VS Code, orquestador; registro por `scribe`) · C-0005 (T00 cerrada)
**Testigo:** claude-opus-5.5 (Claude Code en VS Code, orquestador)

## Qué es
Proyecto semestral ADA 2026-B (profesora Luz Enith Guerrero). **Grupo 2 · Subproyecto 2 "Reparto de presupuesto y selección de participantes"**: Parte 1 reparto óptimo (voraz por ganancia marginal, exacto, O(N+B log N)); Parte 2 selección de k nodos (NP-difícil por reducción desde Cobertura Máxima; voraz con garantía 1−1/e). **Proyecto individual: Juan Esteban Guzmán Henao.** Repo: `C:\Users\danna\OneDrive\Documentos\ADA`, rama `main`, remoto `origin` = https://github.com/GuzGuz0208/ADA.git (**sin push**). Guía de estudio del usuario: https://claude.ai/artifact/1n9ukzYACjPEQGKqmvq8h1 (D-16).
**Fecha crítica:** primera entrega **2026-11-06** (4 productos: informe de formalización + NP-dureza, repo con solución base, manual técnico, ejecución del caso JSON con resultado/tiempo/traza). Detalle en `agent/SPEC.md` §1.

## Estado por producto
| Producto | Estado | Dónde |
|---|---|---|
| Informe (formalización + NP-dureza) | ⬜ no iniciado (esqueletos en SPEC §5). Formato PDF vía LaTeX en letX (D-20) | `informe/` (por crear: `main.tex` + `secciones/*.tex` + espejo Markdown) |
| Repositorio / código base | ⬜ no iniciado (solo andamiaje y `.venv`) | `src/ada_g2/` (por crear) |
| Manual técnico | ⬜ no iniciado | `manual/` (por crear) |
| Ejecución del caso de la profesora | ⬜ no iniciado | `results/caso_G2_15_nodos/` (por crear) |
| Memoria compartida y hooks | ✅ T00 cerrada: git inicializado (commit `5054456`), hooks probados en Windows, config en `.claude/` | `agent/`, `.claude/`, `agent/hooks/` |

## Entorno (comprobado en T00)
- Python 3.12.10 (`python` y `py`); git 2.56. `.venv` creado con `requirements.txt`: pytest 9.2.0, numpy 2.5.4, scipy 1.18.1, matplotlib 3.11.2, hypothesis 6.170.14.
- `core.hooksPath = agent/hooks`; `agent/hooks/pre-commit` con modo 100755 en el índice.
- Hooks de Claude Code: PostToolUse (comando `python`, `$CLAUDE_PROJECT_DIR`) escribe en `agent/log/auto_changes.log`; Stop (`check_logged.py`) bloquea con cambios sin registrar. No hizo falta cambiar a `py`.
- pandoc y LaTeX **no** instalados: los agentes no compilan el informe; el usuario lo compila en letX (D-20).
- `agent/claude-config/` ya no existe; `.claude/` completo.

## Hecho hasta ahora
- Lectura completa de `project-docs/` y `docs/` (Cormen solo consulta). Modelo: D-01 u_i=a_i·ln(1+x) · D-02 f cobertura probabilística con el grafo · D-03 cupo k=5 y costo≤24 a la vez · D-04 primera entrega + extras. Supuestos D-05…D-13 (propuestos).
- Prototipo descartable → valores preliminares en SPEC §6 (a re-derivar con el código real). La f se satura con ese grafo (R-02).
- Memoria, 6 subagentes, hooks y prompts de arranque listos; D-14…D-19 (certificados por ejecución, instancia ajustada 1−(1−1/k)^k, guía de estudio, avisos de sesión, remoto GitHub, entorno de informe).
- T00 (C-0005): git init, remoto, `.venv`, hooks probados (PostToolUse, Stop, pre-commit que rechazó un commit sin CHANGELOG), D-20 (informe en PDF vía LaTeX en letX). Q-03 resuelta.

## Siguiente paso inmediato
1. Lanzar **en paralelo**: `theorist` con **T01** (revisar `agent/SPEC.md` §4-5 contra `project-docs/`) e `implementer` con **T04** (empezar por `src/ada_g2/io.py`; comprobar con `.venv\Scripts\python -m py_compile src\ada_g2\io.py`).
2. Después: `theorist` T02/T03 (informe en `informe/main.tex` + `informe/secciones/*.tex`) ‖ `implementer` T04 → `verifier` T05 (`.venv\Scripts\python -m pytest -q`) → T06 (caso de la profesora) → T07 → T08.

Cada bloque de cambios: `scribe` registra antes de cerrar el turno (Regla 0).

## Pendiente del usuario
- Q-02 (resto): preguntar a la profesora si acepta trabajo individual/sustentación sin pareja y comprobar que el enlace del repo le sea accesible (público o invitación).
- Q-01: confirmar con la profesora qué se entrega exactamente mañana (la guía dice que los 4 productos en una fecha son una propuesta).
- R-03: decidir si mover el repo fuera de OneDrive.

## Bloqueos
- Ninguno duro. Informe: compilación solo en letX (sin TeX local).

## NO hacer
- No `git push` sin que el usuario lo pida; no versionar `docs/`; no `--no-verify`; no inventar citas ni números; no hardcodear el caso de la profesora; no reescribir entradas del CHANGELOG.
- No afirmar garantía teórica para cupo+costo a la vez (R-01).
