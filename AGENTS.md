# AGENTS.md — ADA Grupo 2 (Proyecto Red)

> Fuente única de reglas para TODOS los agentes (Claude Code, Codex/GPT, cualquier otro).
> `CLAUDE.md` solo importa este archivo. Idioma de todo el proyecto: español.

## Qué es esto
Proyecto semestral de **Análisis y Diseño de Algoritmos** (profesora Luz Enith Guerrero, U. de Caldas), 2026-B.
**Grupo 2 = Subproyecto 2: "Reparto de presupuesto y selección de participantes"** (proyecto individual: Juan Esteban Guzmán Henao; repo remoto https://github.com/GuzGuz0208/ADA, sin `git push` hasta que el usuario lo pida).
Fecha crítica: **entrega de la primera entrega el 2026-11-06** (detalle en `agent/SPEC.md` §1).
Lo que se califica no es "que el código corra" sino demostrar con rigor *por qué* es eficiente y *qué tan eficiente es* (T(n), NP-dureza por reducción, cota de aproximación, validación experimental). La sustentación pesa 45 %.

## REGLA 0 (sagrada): todo cambio queda registrado
Cualquier modificación (crear, editar, borrar, renombrar un archivo) se registra **antes de terminar el turno**:
1. Añadir UNA entrada al final de `agent/CHANGELOG.md` (formato en su encabezado). Es solo-añadir: jamás se edita ni se borra lo anterior.
2. Actualizar `agent/CONTEXT.md` (Estado actual, Siguiente paso, Testigo) y `agent/TASKS.md`.
3. Decisiones nuevas → `agent/DECISIONS.md`.
4. Commit local (Conventional Commits, en español) que incluya el CHANGELOG. **Prohibido `--no-verify`.**

Cómo se hace cumplir: `agent/hooks/pre-commit` (git, vale para cualquier IA) bloquea commits sin CHANGELOG; en Claude Code además un hook anota cada Write/Edit en `agent/log/auto_changes.log` y otro impide cerrar el turno con cambios sin registrar.
Quién lo hace: en Claude Code, el subagente **`scribe`** (modelo barato) — el hilo principal lo invoca tras cada bloque de cambios. En Codex u otra IA: hacerlo uno mismo con el mismo formato.

## Al empezar cualquier sesión (orden de lectura)
1. `agent/CONTEXT.md` → 2. `agent/TASKS.md` → 3. últimas ~5 entradas de `agent/CHANGELOG.md` → 4. `agent/DECISIONS.md`.
Solo si hace falta: `agent/SPEC.md` (requisitos y modelo), `agent/STYLE_PROFESORA.md` (cómo formaliza la profesora), `agent/ROLES.md`, `agent/HANDOFF.md`.
Al terminar, o si queda poca cuota: dejar `CONTEXT.md` tal que **otra IA continúe sin preguntarle nada al usuario** (`agent/HANDOFF.md`).

## Reglas de trabajo
- **No inventes enunciado.** Lo que no esté en `project-docs/` ni en `agent/DECISIONS.md` es una decisión abierta: regístrala (sección "Abiertas"), sigue con el default marcado y solo pregunta al usuario si la respuesta cambia el resultado.
- **Citas:** solo las verificadas (Nemhauser–Wolsey–Fisher 1978, Khuller–Moss–Naor 1999, Karp 1972… bibliografía del enunciado). Si dudas, márcala `[VERIFICAR]` y no la presentes como hecho.
- **Todo número del informe sale de código ejecutado** (semillas fijas). Nada de cifras a mano.
- **Código reproducible:** Python ≥ 3.10, semillas fijas, sin rutas absolutas. La lógica NO se edita para correr otro caso: la profesora ejecutará OTROS JSON con el mismo esquema (`agent/SPEC.md` §3).
- **Estilo formal de la profesora:** `agent/STYLE_PROFESORA.md` (costeo línea a línea, pre/poscondiciones, invariantes, O/Θ, "voraz = demostrar óptimo o dar contraejemplo").
- Nada destructivo (`reset --hard`, `clean`, `rm -rf`, force-push). No `git push` sin que el usuario lo pida. No versionar `docs/` (libros).
- Si dos IAs alternan, el último en actuar deja el testigo en `CONTEXT.md` (`Testigo: <agente>`). No editar a la vez el mismo archivo.
- Prioridades: **P0** = primera entrega (mañana) · **P1** = rigor extra (T(n) formal, cota 1−1/e, experimentos) · **P2** = variantes.
- Tras cambiar código: correr `pytest` y anotar el resultado real (o "sin verificar") en el CHANGELOG. No afirmar lo que no se ejecutó.

## Mapa del repo
| Ruta | Contenido |
|---|---|
| `project-docs/` | Enunciados y JSON de la profesora (solo lectura) |
| `docs/` | Libros y notas de clase (local, no versionado) |
| `agent/` | Memoria compartida: CONTEXT, CHANGELOG, DECISIONS, TASKS, ROLES, HANDOFF, SPEC, STYLE_PROFESORA, hooks, log |
| `.claude/` | Subagentes, hooks y permisos de Claude Code (ya instalada por el usuario con `robocopy`; las herramientas remotas no pueden escribir aquí, así que los cambios a esta carpeta los hace Claude Code o el usuario) |
| `prompts/` | Prompts de arranque para Claude Code y para Codex |
| `src/ada_g2/` | Código (se crea en T04) |
| `tests/` | Pruebas (T05) |
| `results/` | Salidas por caso: resultado, tiempo, traza (T06) y experimentos (T13) |
| `informe/` | Informe técnico: formalización, NP-dureza, T(n), cota, validación |
| `manual/` | Manual técnico (T07) |

## Comandos (completar en T00/T04)
- Entorno: `python -m venv .venv` → `pip install -r requirements.txt`
- Pruebas: `pytest -q`
- Ejecutar un caso: `python -m ada_g2 run --input project-docs/entrada_G2_red_15_nodos.json --out results/` *(CLI aún por crear)*
