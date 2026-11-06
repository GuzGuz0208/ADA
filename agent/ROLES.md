# ROLES — agentes, modelos y esfuerzo

Principio (guía oficial de Anthropic sobre modelo/esfuerzo en Claude Code): modelo más grande para lo ambiguo y difícil (demostraciones, arquitectura); modelo más pequeño para ejecución con especificación precisa; esfuerzo por defecto salvo que el agente se salte pruebas/archivos (entonces subir `/effort`). `max`/`xhigh` solo para un chequeo puntual.

| Rol | Qué hace | Modelo (Claude Code) | Esfuerzo | Entradas → Salidas |
|---|---|---|---|---|
| **orquestador** (hilo principal) | Planifica, reparte, integra, decide cuándo invocar `scribe` | `opusplan` (Opus planifica, Sonnet ejecuta) | por defecto | TASKS.md → delegaciones |
| **theorist** | Demostraciones: optimalidad del voraz (intercambio), reducción NP desde Cobertura Máxima, deducción de T(n), cota 1−1/e y variantes. Verifica citas | Opus | por defecto (medium) | SPEC §4-5 → `informe/*.md` |
| **implementer** | Código desde SPEC: modelo, reparto, selección, exacto, E/S, trazas, CLI | Sonnet | por defecto | SPEC → `src/ada_g2/` |
| **verifier** | Pruebas independientes: fuerza bruta, propiedad (hypothesis), restricciones, valores SPEC §6. Intenta romper; reporta, no arregla | Sonnet | **alto** | código → `tests/` + reporte |
| **experimenter** | Instancias sintéticas, tiempos (≥5 tamaños), gráficas, ajuste contra T(n) | Sonnet | por defecto | código → `results/experimentos/` |
| **report-writer** | Ensambla informe y manual SOLO con lo ya verificado; checklist de la guía | Sonnet | por defecto | proofs+results → `informe/`, `manual/` |
| **scribe** | CHANGELOG + CONTEXT + TASKS (Regla 0) | Haiku | bajo | git diff → memoria |

Sesiones: abrir una sesión por rol/tarea larga; no mezclar modelos dentro de una misma sesión (re-procesa el historial). El traspaso entre sesiones es SIEMPRE por `agent/CONTEXT.md`.

## Con Codex / GPT
Codex lee `AGENTS.md` solo. Mismos roles, hechos por una sola sesión: teoría con el modelo más fuerte disponible; código y experimentos con uno más barato. Mismas reglas de registro (Regla 0) con el mismo formato de CHANGELOG. Prompt de arranque: `prompts/PROMPT_CODEX.md`.

## Orden recomendado en paralelo (P0)
`theorist` (T02, T03) ‖ `implementer` (T04) → `verifier` (T05) → ejecutar caso (T06) → `report-writer` (T07) → revisión de consistencia (T08). `scribe` tras cada bloque.

## Modelos por momento y avisos de cambio de sesión (C-0003, D-17)
No cambiar de modelo a mitad de sesión: reprocesa el historial y gasta cuota.

| Momento | Dónde | Modelo / esfuerzo |
|---|---|---|
| Sesión principal en VS Code | Claude Code | `claude --model opusplan` (Opus planifica, Sonnet ejecuta) |
| Demostraciones, decisiones de modelo, depuración difícil | subagente `theorist` | Opus, esfuerzo alto |
| Implementación, pruebas, experimentos, informe | subagentes `implementer`, `experimenter`, `report-writer` | Sonnet, esfuerzo medio (alto si falla algo sutil) |
| Verificación independiente | subagente `verifier` | Sonnet, esfuerzo alto, sin haber visto el trabajo |
| Registro del CHANGELOG | subagente `scribe` | Haiku |
| Se acaba la cuota de Claude | Codex | `prompts/PROMPT_CODEX.md` |

**Cuándo imprimir el aviso** (después de hacer commit y dejar CONTEXT al día): (a) aparece cualquier aviso de límite de uso o cuota; (b) termina cada hito (T01…T08); (c) el contexto de la sesión pasa de ~70 %. Formato exacto:
```
=== CAMBIO DE SESIÓN RECOMENDADO ===
Motivo: <cuota | contexto | hito>
Siguiente: <Claude Code (opusplan) | Codex>
Hecho: commit <hash corto> · CONTEXT.md actualizado · CHANGELOG al día
Pega en el chat nuevo: prompts/PROMPT_VSCODE_CLAUDE.md  (o prompts/PROMPT_CODEX.md)
```
