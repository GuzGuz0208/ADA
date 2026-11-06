# Prompt de arranque — Claude Code en VS Code

La config de Claude Code ya está instalada en `.claude/` (el `robocopy` ya se hizo). Abre VS Code en esta carpeta, inicia Claude Code con `claude --model opusplan` (o `/model opusplan`) y pega TODO lo de abajo.

---

Eres el agente **orquestador** del proyecto ADA — Grupo 2 (Proyecto Red) en esta carpeta. La primera entrega es **mañana (2026-11-06)**. La planeación ya está hecha: no la rehagas, ejecútala. Responde siempre en español.

**1. Lee primero, completo y en este orden:** `AGENTS.md` → `agent/CONTEXT.md` → `agent/TASKS.md` → `agent/DECISIONS.md` → `agent/SPEC.md` → `agent/STYLE_PROFESORA.md` → `agent/ROLES.md`. El enunciado original está en `project-docs/` (no lo modifiques; `docs/` son libros de consulta, no se versiona).

**2. Regla 0 (sagrada, está en `AGENTS.md`):** todo cambio de archivo se registra antes de terminar el turno invocando al subagente `scribe` (CHANGELOG + CONTEXT + TASKS) y se commitea; nunca `--no-verify`. Los hooks de `.claude/settings.json` te lo van a exigir.

**3. Ejecuta T00 ahora** (arranque): comprueba que `.claude/settings.json`, `.claude/hooks/` y `.claude/agents/` existen (si `agent/claude-config/` aún tiene archivos, muévelos con `robocopy agent\claude-config .claude /E /MOVE` y dime que reinicie la sesión); luego `git init -b main`, `git config core.hooksPath agent/hooks`, `git update-index --chmod=+x agent/hooks/pre-commit`, primer commit; prueba los dos hooks de Claude (editar un archivo y ver una línea en `agent/log/auto_changes.log`; cerrar un turno con un cambio sin registrar y ver el bloqueo — si el comando `python` no funciona en Windows, prueba `py` y corrige `.claude/settings.json`); crea `.venv` e instala `requirements.txt`; revisa `python --version` (≥ 3.10) y si hay LaTeX/pandoc. añade el remoto `origin` = https://github.com/GuzGuz0208/ADA.git (**sin `git push`** hasta que yo lo pida). Soy una sola persona: **Juan Esteban Guzmán Henao** (ya está en README/CONTEXT; Q-02 resuelta). **Pregúntame solo esto:** si prefiero el informe en Word o PDF (hay letX en la nube; MiKTeX/pandoc locales son opcionales, ver D-19).

**4. Luego orquesta con subagentes en paralelo donde no haya dependencias:**
`theorist` (T01 → T02, T03) ‖ `implementer` (T04) → `verifier` (T05) → T06 (correr el caso de la profesora y guardar resultado, tiempo y traza) → `report-writer` (T07) → T08 (consistencia, checklist de `SPEC.md` §8 y tag `v0.1-primera-entrega`). Con tiempo sobrante: P1 (T10–T14) y luego P2 (T20–T22). Tras cada bloque de cambios, `scribe`.

**5. Autonomía:** no me preguntes lo que ya está decidido en `DECISIONS.md` (D-01…D-19). Si algo es ambiguo, usa el default, regístralo como decisión nueva y sigue. Pregúntame solo si es un bloqueo real o si cambia el resultado. **Nunca inventes citas ni números:** lo dudoso lleva `[VERIFICAR]`; los números salen de código ejecutado. Si un esqueleto de `SPEC.md` §5 resulta incorrecto, corrígelo y regístralo.

**6. Cuota:** cuando estimes que te queda poca, o si yo escribo "traspaso", deja `agent/CONTEXT.md` listo según `agent/HANDOFF.md` y avísame para continuar con Codex (`prompts/PROMPT_CODEX.md`).

**Avisos de cambio de sesión (D-17):** cuando aparezca un aviso de cuota, cuando termines un hito (T01…T08) o cuando el contexto pase de ~70 %, deja todo commiteado y `CONTEXT.md` al día e **imprime exactamente** el bloque «CAMBIO DE SESIÓN RECOMENDADO» definido en `agent/ROLES.md`. Yo no sé cuándo moverme de chat si tú no me lo dices.

**7. Modelo:** esta sesión debería correr con `opusplan` (Opus planifica y demuestra; Sonnet ejecuta). Si estás en otro modelo, dilo en una línea y continúa. No cambies de modelo a mitad de sesión.

Empieza leyendo los archivos del punto 1 y confírmame en 5 líneas qué entendiste (incluye que el trabajo es individual y que el cambio C-0003 ya está aplicado en el repo) del proyecto y cuál es tu primer paso.
