# CONTEXT — estado vivo del proyecto

> Reescribir en cada checkpoint (no acumular; ≤ ~150 líneas). Historia detallada: `agent/CHANGELOG.md`.

**Última actualización:** 2026-11-05 21:50 (America/Bogota) · claude-sonnet-5.5 (chat de Claude app) · C-0003 aplicada
**Testigo:** claude-sonnet-5.5 (chat) → Claude Code en VS Code (`opusplan`) [pendiente de arrancar con `prompts/PROMPT_VSCODE_CLAUDE.md`]

## Qué es
Proyecto semestral ADA 2026-B (profesora Luz Enith Guerrero). **Grupo 2 · Subproyecto 2 "Reparto de presupuesto y selección de participantes"**: Parte 1 reparto óptimo (voraz por ganancia marginal, exacto, O(N+B log N)); Parte 2 selección de k nodos (NP-difícil por reducción desde Cobertura Máxima; voraz con garantía 1−1/e). **Proyecto individual: Juan Esteban Guzmán Henao.** Repo remoto: https://github.com/GuzGuz0208/ADA (creado; sin push aún). Guía de estudio del usuario: https://claude.ai/artifact/1n9ukzYACjPEQGKqmvq8h1 (D-16).
**Fecha crítica:** primera entrega **2026-11-06** (4 productos: informe de formalización + NP-dureza, repo con solución base, manual técnico, ejecución del caso JSON con resultado/tiempo/traza). Detalle en `agent/SPEC.md` §1.

## Estado por producto
| Producto | Estado | Dónde |
|---|---|---|
| Informe (formalización + NP-dureza) | ⬜ no iniciado (esqueletos de demostración en SPEC §5) | `informe/` (por crear) |
| Repositorio / código base | ⬜ no iniciado (solo andamiaje de agentes) | `src/ada_g2/` (por crear) |
| Manual técnico | ⬜ no iniciado | `manual/` (por crear) |
| Ejecución del caso de la profesora | ⬜ no iniciado | `results/caso_G2_15_nodos/` (por crear) |
| Memoria compartida y hooks | ✅ memoria lista; config de Claude Code **instalada en `.claude/`** (robocopy hecho por el usuario); hooks probados solo en un repo de prueba Linux → falta probarlos en Windows (T00) | `agent/`, `.claude/` |

## Hecho hasta ahora (2026-11-05, chat de Claude app)
- Leído todo `project-docs/` (PDF general solo Subproyecto 2, docx G2, guías de primera entrega, JSON) y `docs/` (notas de clase 2024, libro de la profesora; Cormen sin leer, solo consulta).
- Modelo adoptado con el usuario: D-01 u_i=a_i·ln(1+x) · D-02 f cobertura probabilística con el grafo · D-03 cupo k=5 y costo≤24 a la vez · D-04 primera entrega + extras. Resto de supuestos D-05…D-13 propuestos (DECISIONS).
- Prototipo descartable sobre el JSON → valores de referencia preliminares en SPEC §6 (a re-derivar con el código real). Hallazgo: la f se satura con ese grafo (R-02).
- Creado el andamiaje: reglas (AGENTS/CLAUDE), memoria (CONTEXT/CHANGELOG/DECISIONS/TASKS/ROLES/HANDOFF/SPEC/STYLE_PROFESORA), 6 subagentes, hooks (PostToolUse + Stop + pre-commit de git) y prompts de arranque. Hooks probados en un repo temporal: los tres comportamientos funcionan.
- C-0003 (21:50): aplicado el equipo de una persona, D-14…D-19 (certificados, instancia ajustada, guía de estudio, avisos de sesión, remoto GitHub, entorno de informe), R-01/R-04/R-06, tareas W1…W5 y T14, avisos de cambio de sesión en ROLES y en ambos prompts.
- **No se hizo `git init`** en la carpeta (OneDrive + sandbox de Linux podían dejar `.lock`/permisos raros): lo hace T00 con git nativo de Windows.

## Siguiente paso inmediato
1. Abrir VS Code en esta carpeta → terminal → `claude --model opusplan` → pegar el mensaje de arranque (leer `prompts/PROMPT_VSCODE_CLAUDE.md`).
2. Ejecutar **T00** (git init, hooksPath, chmod del pre-commit, remoto `origin` sin push, probar hooks en Windows, `.venv`) y luego T01…T08 en paralelo según `agent/TASKS.md`. Primer commit: debe incluir la entrada C-0003 del CHANGELOG (ya escrita; el hash se anota después con una entrada nueva, no editando).

## Pendiente del usuario
- Q-02 (resto): preguntar a la profesora si acepta trabajo individual/sustentación sin pareja y comprobar que el enlace del repo le sea accesible (público o invitación).
- Q-03: ¿informe en Word o PDF? (hay letX en la nube; MiKTeX/pandoc locales opcionales, D-19).
- Q-01: confirmar con la profesora qué se entrega exactamente mañana (la guía dice que los 4 productos en una fecha son una propuesta).
- R-03: decidir si mover el repo fuera de OneDrive.

## NO hacer
- No `git push` sin que el usuario lo pida; no versionar `docs/`; no `--no-verify`; no inventar citas ni números; no hardcodear el caso de la profesora; no reescribir entradas del CHANGELOG.
- No afirmar garantía teórica para cupo+costo a la vez (R-01).
