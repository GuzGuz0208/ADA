# Prompt de arranque — Codex / GPT (segundo agente)

Abre Codex en esta carpeta (raíz del repo; Codex lee `AGENTS.md` solo) y pega TODO lo de abajo.

---

Eres el segundo agente del proyecto ADA — Grupo 2 (Proyecto Red). Otra IA (Claude) trabajó antes y dejó todo el estado en archivos; **no hay nada importante en el chat**. Responde en español.

1. Lee en este orden, completo: `AGENTS.md` → `agent/CONTEXT.md` → `agent/TASKS.md` → últimas ~5 entradas de `agent/CHANGELOG.md` → `agent/DECISIONS.md`. Si necesitas detalle: `agent/SPEC.md`, `agent/STYLE_PROFESORA.md`, `agent/HANDOFF.md`.
2. Verifica con `git log --oneline -10` y `git status` que `CONTEXT.md` coincide con la realidad. Si no coincide, **manda el repo**; regístralo.
3. Toma el "Siguiente paso inmediato" de `CONTEXT.md`. No rehagas lo hecho ni reescribas archivos ajenos sin motivo registrado.
4. **Regla 0 (sagrada):** todo cambio de archivo se registra antes de terminar el turno: una entrada al final de `agent/CHANGELOG.md` (solo-añadir, con el formato de su encabezado), actualizar `agent/CONTEXT.md` y `agent/TASKS.md`, y commit local en Conventional Commits en español. Nunca `--no-verify`: `agent/hooks/pre-commit` bloquea commits sin CHANGELOG (actívalo con `git config core.hooksPath agent/hooks` si no está activo). Como no tienes el subagente `scribe`, haz tú el registro con el mismo formato.
5. Haz tú los roles de `agent/ROLES.md`: teoría con tu modelo más fuerte (demostraciones, reducción NP, T(n), citas verificadas); código y experimentos con uno más económico si puedes elegir. Nada de citas ni números inventados: lo dudoso lleva `[VERIFICAR]`; los números salen de código ejecutado.
6. Al terminar tu cuota o cuando te lo pida el usuario, deja `CONTEXT.md` listo (`agent/HANDOFF.md`) con `Testigo: codex → claude` y avísame.
7. **Avisos de cambio de sesión (D-17):** cuando aparezca un aviso de cuota, cuando termines un hito (T01…T08) o cuando el contexto pase de ~70 %, deja todo commiteado e **imprime exactamente** el bloque «CAMBIO DE SESIÓN RECOMENDADO» definido en `agent/ROLES.md`.
8. El trabajo es individual (Juan Esteban Guzmán Henao); remoto = https://github.com/GuzGuz0208/ADA — **no hagas `git push`** hasta que el usuario lo pida.

Empieza leyendo los archivos y confírmame en 5 líneas el estado real y cuál es tu primer paso.
