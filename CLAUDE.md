@AGENTS.md

## Específico de Claude Code
- **Config de Claude Code:** subagentes, hooks y permisos ya están en `.claude/` (el usuario ejecutó el `robocopy` el 2026-11-05). Las herramientas remotas de los chats no pueden escribir en `.claude/`; si hay que cambiarla, hazlo desde esta sesión de Claude Code. Si alguna vez reaparece `agent/claude-config/` con archivos, muévelos con `robocopy agent\claude-config .claude /E /MOVE` y pide reiniciar la sesión.
- **Subagentes** en `.claude/agents/`: `scribe`, `theorist`, `implementer`, `verifier`, `experimenter`, `report-writer`. El hilo principal orquesta y delega; **el registro lo hace siempre `scribe`** tras cada bloque de cambios (Regla 0).
- **Hooks** (`.claude/settings.json`): `PostToolUse` anota cada Write/Edit en `agent/log/auto_changes.log` (traza cruda); `Stop` bloquea el cierre del turno si hay archivos modificados después de la última edición de `agent/CHANGELOG.md`. Si el hook no corre en Windows, corregir el comando (p. ej. `py` en vez de `python`) y registrar el cambio.
- **Modelos y esfuerzo:** ver `agent/ROLES.md`. Recomendado: `claude --model opusplan` (Opus planifica/demuestra, Sonnet ejecuta). Subir `/effort` solo si el agente se salta pruebas o archivos.
- **Cambiar de modelo a mitad de sesión re-procesa todo el historial** (gasta cuota): mejor abrir sesión nueva y que lea `agent/CONTEXT.md`.
- Permisos: `acceptEdits` + lista de comandos permitidos para trabajar con autonomía; los destructivos están denegados.
