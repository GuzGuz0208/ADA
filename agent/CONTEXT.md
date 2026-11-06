# CONTEXT — estado vivo del proyecto

> Reescribir en cada checkpoint (no acumular; ≤ ~150 líneas). Historia detallada: `agent/CHANGELOG.md`.

**Última actualización:** 2026-11-05 22:13 (America/Bogota) · scribe (claude-haiku-5.5) registrando C-0007 de theorist (claude-opus-5.5), orquestado por claude-opus-5.5
**Testigo:** scribe (claude-haiku-5.5), registro de C-0007 por encargo de claude-opus-5.5

## Qué es
Proyecto semestral ADA 2026-B (profesora Luz Enith Guerrero). **Grupo 2 · Subproyecto 2 "Reparto de presupuesto y selección de participantes"**: Parte 1 reparto óptimo (voraz por ganancia marginal, exacto, O(N+B log N)); Parte 2 selección de k nodos (NP-difícil por reducción desde Cobertura Máxima; voraz con garantía 1−1/e). **Proyecto individual: Juan Esteban Guzmán Henao.** Repo: `C:\Users\danna\OneDrive\Documentos\ADA`, rama `main`, remoto `origin` = https://github.com/GuzGuz0208/ADA.git (**sin push**). Guía de estudio del usuario: https://claude.ai/artifact/1n9ukzYACjPEQGKqmvq8h1 (D-16).
**Fecha crítica:** primera entrega **2026-11-06** (4 productos: informe de formalización + NP-dureza, repo con solución base, manual técnico, ejecución del caso JSON con resultado/tiempo/traza). Detalle en `agent/SPEC.md` §1.

## Estado por producto
| Producto | Estado | Dónde |
|---|---|---|
| Informe (formalización + NP-dureza + optimalidad) | 🔄 secciones 01–03 redactadas (C-0007, sin commit hasta el de C-0007). Sin compilar (sin TeX local, D-20). Faltan cifras `[RESULTADO-T06]` y cota `[RESULTADO-T12]` | `informe/main.tex`, `informe/secciones/`, `informe/referencias.tex`, `informe/INFORME.md` (espejo) |
| Repositorio / código base | ✅ T04 base (commit `5f98f59`, C-0006): `pyproject.toml`, 12 módulos en `src/ada_g2/`, `tests/test_smoke.py`. 🔄 `tests/test_propiedades.py` en curso (verifier, T05), sin registrar | `src/ada_g2/`, `tests/` |
| Manual técnico | ⬜ no iniciado (T07) | `manual/` |
| Ejecución del caso de la profesora | 🔄 salida preliminar generada por implementer; falta confirmar tras T05 (T06) | `results/caso_entrada_G2_red_15_nodos/` (nombre según el JSON) |
| Memoria compartida y hooks | ✅ T00 (cierre en commit `35db17c`, C-0005; `5054456` contiene C-0001…C-0004), hooks probados en Windows, config en `.claude/` | `agent/`, `.claude/`, `agent/hooks/` |

## Entorno (comprobado en T00 y C-0006)
- Python 3.12.10 (`python` y `py`); git 2.56. `.venv` con `requirements.txt` (pytest 9.2.0, numpy 2.5.4, scipy 1.18.1, matplotlib 3.11.2, hypothesis 6.170.14) y `pip install -e .` (ada_g2 0.1.0).
- `core.hooksPath = agent/hooks`; `agent/hooks/pre-commit` con modo 100755 en el índice.
- Hooks de Claude Code: PostToolUse (comando `python`, `$CLAUDE_PROJECT_DIR`) escribe en `agent/log/auto_changes.log`; Stop (`check_logged.py`) bloquea con cambios sin registrar.
- Git Bash: `TZ=America/Bogota date` devuelve **UTC**; para la hora usar `python -c` con zoneinfo.
- pandoc y LaTeX **no** instalados: los agentes no compilan el informe; el usuario lo compila en letX (D-20).
- `pytest -q` → 5 passed (verificado por el scribe en C-0006). No re-ejecutado en C-0007.

## Hecho hasta ahora
- Lectura de `project-docs/` y `docs/`. Modelo: D-01 u_i=a_i·ln(1+x) · D-02 f cobertura probabilística · D-03 cupo k=5 y costo≤24 a la vez · D-04 primera entrega + extras. Supuestos D-05…D-13.
- Memoria, 6 subagentes, hooks y prompts listos; D-14…D-20 (certificados, instancia ajustada, guía, avisos de sesión, remoto, entorno de informe, formato PDF).
- T00 (C-0005): git, remoto, `.venv`, hooks probados. Q-03 resuelta.
- T04 base (C-0006): reparto con montículo y topes; selección voraz (k/costo/ambos, mejor-de-3); exacto; certificados D-14 (dualidad y cota LP); rondas con q y políticas; CLI `run`/`generar`. Según implementer, el caso de la profesora cumple todo: ronda 1 S={N09,N11,N13,N14,N15}, Σf=436.7386, Σu=262.7387, LP cota 151.9871, razón certificada 0.95784 (reproduce R-06 preliminar). D-21…D-25 fijadas.
- T01 (C-0007, theorist): 11 correcciones en `agent/SPEC.md` §4-5. D-26…D-29 fijadas. D-21 (theorist) = D-21 existente.
- T02 y T03 redactadas (C-0007); T11 con T1 completo; T10 con costeos del reparto y voraz. Verificación de T03 pendiente del verifier.

## Siguiente paso inmediato
1. `verifier` (**T05 y T03**): cuando termine `tests/test_propiedades.py`, ejecutar `.venv\Scripts\python -m pytest -q` y comprobar a mano la instancia 4×5 de `informe/secciones/02_np_dureza.tex` contra `src/ada_g2/select.py`. Registrar el resultado real en un CHANGELOG nuevo.
2. Después: `implementer` (**T06**) confirma `results/caso_entrada_G2_red_15_nodos/` y entrega las cifras para los marcadores `[RESULTADO-T06]` de `informe/`. Luego T07 → T08.

Cada bloque de cambios: `scribe` registra antes de cerrar el turno (Regla 0).

## Pendiente del usuario
- **Portada del informe (`informe/main.tex`):** revisar "Facultad de Ingenierías" y "Manizales". Los puso theorist como supuesto; no están verificados contra el enunciado.
- Q-02 (resto): preguntar a la profesora si acepta trabajo individual/sustentación sin pareja y comprobar que el enlace del repo le sea accesible (público o invitación).
- Q-01: confirmar con la profesora qué se entrega exactamente mañana (la guía dice que los 4 productos en una fecha son una propuesta).
- R-03: decidir si mover el repo fuera de OneDrive (el commit de C-0006 tuvo advertencias CRLF y `.git` en OneDrive).

## Bloqueos
- Ninguno duro. Informe: compilación solo en letX (sin TeX local).
- `tests/` tiene trabajo del verifier sin registrar: no añadirlo a commits ajenos.
- `agent/SPEC.md` §4 todavía dice "propuesta D-21, pendiente de registrar": D-21 ya está registrada (ver DECISIONS). Corregirlo en la próxima edición de SPEC.

## NO hacer
- No `git push` sin que el usuario lo pida; no versionar `docs/`; no `--no-verify`; no `git add -A` mientras haya trabajo ajeno sin commit (`tests/`); no inventar citas ni números; no hardcodear el caso de la profesora; no reescribir entradas del CHANGELOG.
- No afirmar garantía teórica para cupo+costo a la vez (R-01).
