# CHANGELOG — registro de cambios (SOLO AÑADIR)

**Regla 0:** cada cambio de archivos deja una entrada aquí, al final. Prohibido editar o borrar entradas previas (`agent/hooks/pre-commit` lo bloquea). Hora de America/Bogota. Quien escribe: el subagente `scribe` (Claude Code) o la propia IA (Codex).

## Formato de entrada
```
### C-NNNN · AAAA-MM-DD HH:MM · <agente/modelo> · tarea <T-xx>
- **Tipo:** feat | fix | docs | test | chore | refactor | decision
- **Archivos:** A crear · M modificar · D borrar · R renombrar — ruta (qué cambió, 1 línea)
- **Qué y por qué:** 1-3 líneas
- **Verificación:** comando ejecutado y resultado real, o "sin verificar"
- **Commit:** hash corto o "pendiente"
- **Siguiente paso:** 1 línea
```

---

### C-0001 · 2026-11-05 20:04 · claude-sonnet-5.5 (chat de Claude app) · tarea T-SC
- **Tipo:** chore
- **Archivos:**
  - A `AGENTS.md` — reglas universales para todos los agentes (Regla 0 de registro, orden de lectura, reglas de trabajo, mapa del repo)
  - A `CLAUDE.md` — importa AGENTS.md + notas de Claude Code (subagentes, hooks, modelos)
  - A `README.md` — esqueleto con placeholders (integrantes, URL, comandos)
  - A `.gitignore`, `.gitattributes`, `requirements.txt` — ignorar `docs/` y basura; LF en todo; dependencias mínimas
  - A `agent/CONTEXT.md`, `agent/CHANGELOG.md`, `agent/DECISIONS.md`, `agent/TASKS.md` — memoria compartida
  - A `agent/ROLES.md`, `agent/HANDOFF.md` — roles/modelos y protocolo de traspaso Claude ⇄ Codex
  - A `agent/SPEC.md` — requisitos del Grupo 2 con trazabilidad, modelo matemático, esqueletos de demostración, valores de referencia, plan experimental, checklist
  - A `agent/STYLE_PROFESORA.md` — convenciones de formalización de la profesora (de sus notas y su libro)
  - A `agent/hooks/pre-commit` — git: exige CHANGELOG en commits que tocan el proyecto y lo mantiene solo-añadir
  - A `agent/log/.gitkeep` — carpeta de la traza cruda automática
  - A `.claude/settings.json` — permisos para autonomía + hooks PostToolUse y Stop
  - A `.claude/hooks/log_change.py`, `.claude/hooks/check_logged.py` — traza automática de Write/Edit y bloqueo de cierre con cambios sin registrar
  - A `.claude/agents/{scribe,theorist,implementer,verifier,experimenter,report-writer}.md` — 6 subagentes con modelo asignado
  - A `prompts/PROMPT_VSCODE_CLAUDE.md`, `prompts/PROMPT_CODEX.md` — prompts de arranque para cada IA
- **Qué y por qué:** el usuario pidió trabajar con varias IAs (Claude y Codex) con un contexto compartido "sagrado" y un agente que registre cada cambio. Se leyó todo `project-docs/` y `docs/`, se fijó el modelo con el usuario (D-01…D-04) y se montó el andamiaje para arrancar la ejecución en VS Code. No hay código del proyecto todavía.
- **Verificación:** hooks probados en un repo temporal de Linux — log_change.py escribe la línea esperada; check_logged.py bloquea con cambio sin registrar, no bloquea con `stop_hook_active` ni tras registrar; pre-commit bloquea commit sin CHANGELOG, bloquea CHANGELOG con líneas borradas y deja pasar commits válidos y de solo `agent/`; `settings.json` es JSON válido. **No probado:** los hooks dentro de Claude Code real en Windows (comando `python` y variable `$CLAUDE_PROJECT_DIR`) → lo prueba T00. Prototipo numérico descartable (no versionado) usado para SPEC §6.
- **Commit:** pendiente (no hay repositorio git aún; lo crea T00)
- **Siguiente paso:** T00 en VS Code: `git init -b main`, hooksPath, `update-index --chmod=+x`, primer commit, probar hooks (ver `agent/TASKS.md`).

### C-0002 · 2026-11-05 20:09 · claude-sonnet-5.5 (chat de Claude app) · tarea T-SC
- **Tipo:** fix
- **Archivos:**
  - A `agent/claude-config/settings.json`, `agent/claude-config/hooks/{log_change.py,check_logged.py}`, `agent/claude-config/agents/{scribe,theorist,implementer,verifier,experimenter,report-writer}.md` — C-0001 listó estos 9 archivos bajo `.claude/`, pero la herramienta remota rechazó escribir en `.claude/` ("Writing to .claude is not permitted via remote tools"). Se entregaron en `agent/claude-config/` con el mismo contenido para que el usuario los mueva a `.claude/` con `robocopy agent\claude-config .claude /E /MOVE` antes de abrir Claude Code (hasta entonces hooks y subagentes NO están activos).
  - M `AGENTS.md`, `CLAUDE.md`, `agent/TASKS.md` (T00), `agent/CONTEXT.md`, `prompts/PROMPT_VSCODE_CLAUDE.md` — documentan ese paso de instalación.
- **Qué y por qué:** corregir la ubicación de la config de Claude Code sin saltarse la restricción de la herramienta; la instalación la hace el usuario (una línea) o T00.
- **Verificación:** `device_commit_files` confirmó 14 archivos escritos y 0 rechazados en esta tanda (sin verificar que robocopy funcione en la máquina del usuario ni que los hooks corran en Claude Code real).
- **Commit:** pendiente (no hay repositorio git aún; lo crea T00)
- **Siguiente paso:** el usuario ejecuta el `robocopy`; luego abrir Claude Code y pegar `prompts/PROMPT_VSCODE_CLAUDE.md`.

### C-0003 · 2026-11-05 21:50 · claude-sonnet-5.5 (chat de Claude app) · tarea T00 (preparación)
- **Tipo:** decision
- **Archivos:**
  - A `agent/ACTUALIZACION_C-0003.md` — cambios acordados en el chat de Claude app (marcado como YA APLICADO; queda como historia)
  - M `README.md`, `AGENTS.md`, `agent/CONTEXT.md` — proyecto individual (Juan Esteban Guzmán Henao), URL del repo https://github.com/GuzGuz0208/ADA, `.claude/` ya instalado
  - M `agent/DECISIONS.md` — A D-14…D-19 (certificados por ejecución, instancia ajustada 1−(1−1/k)^k, guía de estudio, avisos de sesión, remoto GitHub, entorno de informe/letX); M Q-02 (resuelta salvo aceptación de la profesora), Q-03, R-01, R-04; A R-06
  - M `agent/TASKS.md` — T00 (remoto origin, sin push), T14 (completar §8 de la guía), A Fase 2b con W1…W5
  - M `agent/ROLES.md` — tabla de modelos por momento y formato del aviso «CAMBIO DE SESIÓN RECOMENDADO»
  - M `prompts/PROMPT_VSCODE_CLAUDE.md`, `prompts/PROMPT_CODEX.md` — trabajo individual, remoto sin push, avisos de sesión, robocopy ya hecho
- **Qué y por qué:** el proyecto lo hace una sola persona; el usuario creó el repo en GitHub y quiere arrancar Claude Code. Se añaden los certificados por ejecución (el "wow" matemático), la instancia ajustada para 1−1/e, el enlace a la guía de estudio y los avisos de cambio de sesión. Las referencias de R-01 se comprobaron en resúmenes/registros bibliográficos, no en texto completo.
- **Verificación:** sin código nuevo; solo documentos. Se comprobó con `grep` que las filas D-14…D-19, Q-02/Q-03 y R-01/R-04/R-06 quedaron en `agent/DECISIONS.md` y que `agent/claude-config/` ya no existe (`.claude/` tiene settings.json, 6 agentes y 2 hooks). Las cifras de la guía (UB(λ*), 0.9578, 0.7037, 0.67232) siguen siendo de un prototipo descartable → R-06.
- **Commit:** pendiente (no hay repositorio git aún; lo crea T00 y el hash se anotará en una entrada nueva)
- **Siguiente paso:** T00 en VS Code: `git init -b main`, `git config core.hooksPath agent/hooks`, `git update-index --chmod=+x agent/hooks/pre-commit`, `git remote add origin https://github.com/GuzGuz0208/ADA.git`, primer commit (sin push), probar hooks en Windows, `.venv`.

### C-0004 · 2026-11-05 21:55 · claude-sonnet-5.5 (chat de Claude app) · tarea T00 (preparación)
- **Tipo:** docs
- **Archivos:**
  - M `AGENTS.md`, `CLAUDE.md` — quitar las instrucciones obsoletas sobre `agent/claude-config/` y `robocopy` (la config ya está en `.claude/`); `CLAUDE.md` no figuraba en C-0003
- **Qué y por qué:** una revisión con `grep` encontró dos textos que seguían diciendo que la config no estaba instalada.
- **Verificación:** `grep claude-config AGENTS.md CLAUDE.md` solo deja la mención condicional de CLAUDE.md.
- **Commit:** pendiente (lo crea T00)
- **Siguiente paso:** T00 en VS Code.
