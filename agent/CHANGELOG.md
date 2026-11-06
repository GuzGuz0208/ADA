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

### C-0005 · 2026-11-05 21:56 · claude-opus-5.5 (Claude Code en VS Code, orquestador; registro por subagente scribe) · tarea T00
- **Tipo:** chore
- **Archivos:**
  - M `.claude/hooks/log_change.py` — escribe con `newline="\n"` (en Windows metía CRLF y git avisaba) e ignora rutas fuera del repo (`../`, p. ej. planes de Claude Code)
  - M `agent/DECISIONS.md` — A D-20 (informe en PDF vía LaTeX en letX; fuente `informe/main.tex` + `informe/secciones/*.tex` + espejo Markdown; sin compilación local); Q-03 marcada RESUELTA
  - M `agent/CONTEXT.md` — estado tras T00, siguiente paso (T01 ‖ T04), Q-03 fuera de pendientes del usuario
  - M `agent/TASKS.md` — T00 → ✅ con nota
  - M `agent/log/auto_changes.log` — traza automática de Write/Edit (PostToolUse) de esta sesión
  - Además, sin archivos nuevos de contenido: `git init -b main`, `git config core.hooksPath agent/hooks`, `git update-index --chmod=+x agent/hooks/pre-commit`, `git remote add origin https://github.com/GuzGuz0208/ADA.git` (sin push)
- **Qué y por qué:** cierra T00 (arranque en Windows). El primer commit `5054456` (C-0001…C-0004) incluye esas cuatro entradas; sus campos "Commit: pendiente" no se editaron (solo-añadir). Se usa la hora de Bogotá 21:56 calculada con `zoneinfo`: en Git Bash `TZ=America/Bogota date` devolvió la hora UTC (02:56 del 2026-11-06).
- **Verificación:**
  - Ejecutado por el orquestador: `git init`/`hooksPath`/`chmod` (modo 100755 confirmado); `git remote -v` muestra origin; PostToolUse escribe en `agent/log/auto_changes.log`; `check_logged.py` probado a mano: bloquea con archivo sin registrar (`prueba_hook.txt`, borrado después), no bloquea con `stop_hook_active=true` ni con árbol limpio; pre-commit rechazó un commit sin CHANGELOG (exit 1); Python 3.12.10 (`python` y `py`), git 2.56; `.venv` con requirements.txt → pytest 9.2.0, numpy 2.5.4, scipy 1.18.1, matplotlib 3.11.2, hypothesis 6.170.14; `agent/claude-config/` no existe y `.claude/` completo.
  - Ejecutado por el scribe: `git status --short` (3 M, sin no rastreados), `git diff --stat`, `git ls-files -s agent/hooks/pre-commit`, `git config core.hooksPath`, hora con `zoneinfo`.
  - Sin verificar: `pytest -q` (aún no hay pruebas; T05); pandoc/LaTeX no instalados (comprobado en T00, no hace falta para T00).
- **Commit:** `5054456` (C-0001…C-0004). El de este cambio (T00 cerrada) se anota en la siguiente entrada.
- **Siguiente paso:** `theorist` T01 y `implementer` T04 en paralelo (ver `agent/CONTEXT.md`, "Siguiente paso inmediato").

### C-0006 · 2026-11-05 22:07 · implementer (claude-sonnet-5.5), orquestado por claude-opus-5.5; registro por scribe (claude-haiku-5.5) · tarea T04
- **Tipo:** feat
- **Archivos:**
  - A `pyproject.toml` — setuptools, src layout, paquete `ada_g2` 0.1.0, Python ≥3.10 (instalado con `pip install -e .` en `.venv`)
  - A `src/ada_g2/__init__.py`, `src/ada_g2/__main__.py` — paquete y entrada `python -m ada_g2`
  - A `src/ada_g2/io.py` — carga y validación del JSON con todos los errores y su ruta
  - A `src/ada_g2/model.py` — u_i = a_i·ln(1+x); f de cobertura probabilística con R_j incremental (τ = O(M))
  - A `src/ada_g2/allocate.py` — reparto voraz con montículo (heapify O(N)), topes y desempate por menor índice
  - A `src/ada_g2/select.py` — selección voraz, modos `k` / `costo` / `ambos`, mejor-de-3 (ganancia, razón, singleton)
  - A `src/ada_g2/exact.py` — exacto por DFS con poda; DP exacto de referencia del reparto
  - A `src/ada_g2/certificates.py` — certificados D-14: dualidad de Lagrange (W1) y cota LP con highs (W2)
  - A `src/ada_g2/rounds.py` — T rondas en cadena con q y políticas concentrado/uniforme
  - A `src/ada_g2/trace.py` — traza por ronda (md y csv)
  - A `src/ada_g2/cli.py` — subcomandos `run` y `generar`
  - A `src/ada_g2/generator.py` — generador sintético con semilla
  - A `tests/test_smoke.py` — 5 pruebas de humo
  - A `results/caso_entrada_G2_red_15_nodos/` — `resultado.json`, `tiempo.csv`, `traza.md`, `traza.csv` (salida del CLI sobre el JSON de la profesora)
  - M `agent/CONTEXT.md`, `agent/TASKS.md`, `agent/DECISIONS.md` (A D-21…D-25), `agent/log/auto_changes.log` (traza automática)
  - No incluidos: `informe/` y `agent/SPEC.md` (los escribe el theorist en paralelo; sin commit).
- **Qué y por qué:** base del código (T04) para que el verifier pruebe y el caso de la profesora se ejecute sin editar código. La carpeta de salida usa el nombre del JSON (`caso_entrada_G2_red_15_nodos`), no `caso_G2_15_nodos` como decía TASKS T06.
- **Verificación:**
  - Ejecutado por el scribe: `pytest -q` → `5 passed in 1.25s`.
  - Reportado por el implementer (no re-ejecutado por el scribe): `pip install -e .` OK; CLI `run` sobre `project-docs/entrada_G2_red_15_nodos.json`: exit 0, «restricciones y certificados: TODO CUMPLE»; ronda 1 S={N09,N11,N13,N14,N15}, f=145.5795, costo 23; Σf=436.7386, Σu=262.7387; certificado de dualidad con brecha 0 en las 3 rondas; LP cota 151.9871, razón certificada 0.95784; modo `k` exacto f=145.9072, razón 0.99775; mediana del pipeline 8.75 ms. Coincide con SPEC §6 sin ajustar código.
  - Sin verificar: pruebas de propiedades con hypothesis; W1 y W2 sobre ≥500 instancias (T05, verifier); W3 razones exactas; reproducción en otra máquina.
- **Commit:** pendiente (lo anota la siguiente entrada)
- **Siguiente paso:** `verifier` T05: crear `tests/test_propiedades.py` con hypothesis y ejecutar `.venv\Scripts\python -m pytest -q`.
