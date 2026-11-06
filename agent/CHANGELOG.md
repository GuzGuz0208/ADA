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

### C-0007 · 2026-11-05 22:13 · theorist (claude-opus-5.5), orquestado por claude-opus-5.5; registro por scribe (claude-haiku-5.5) · tarea T01, T02, T03 (y avances T10, T11)
- **Tipo:** docs
- **Archivos:**
  - A `informe/main.tex` — preámbulo estándar (babel spanish con es-nodecimaldot/es-noshorthands), portada, índice, convenciones
  - A `informe/secciones/01_formalizacion.tex` — T02: Parte 1 y Parte 2 por separado; tamaños (N,B) y (N,k)(+M,L); lemas de concavidad de u_i y monotonía/submodularidad de f; tabla D-01…D-13
  - A `informe/secciones/02_np_dureza.tex` — T03: CobMax NP-completo desde Set Cover; Sel-Dec ∈ NP; transformación φ con costeo Θ(N·|U|); equivalencia ⇒/⇐; ejemplo 4×5 con k=2; dureza de la subfamilia del JSON (W simétrica, w_ii=1); corolarios para modos costo/ambos; dureza fuerte
  - A `informe/secciones/03_optimalidad_y_cota.tex` — T1 optimalidad del reparto con topes por intercambio e invariante de lazo; costeo O(N+B log N); pseudo-polinomial; water-filling en esbozo; voraz de selección Θ(kNM); Nemhauser–Wolsey–Fisher con cota 1−(1−1/k)^k y prueba propia; contraejemplos
  - A `informe/referencias.tex` — bibliografía con marcas [VERIFICAR]
  - A `informe/INFORME.md` — espejo Markdown (manda el LaTeX)
  - M `agent/SPEC.md` — §4-5: 11 correcciones (ver abajo)
  - M `agent/DECISIONS.md` — A D-26…D-29; D-21 anotada como confirmada por theorist (misma regla, no duplicada)
  - M `agent/TASKS.md` — T01 ✅, T02 ✅, T03 ✅ (verificación del verifier pendiente), T10 🔄, T11 🔄
  - M `agent/CONTEXT.md` — estado, siguiente paso, pendientes del usuario (portada), testigo
  - M `agent/log/auto_changes.log` — traza automática de Write/Edit
- **Correcciones a SPEC (T01):** (1) el ciclo del reparto es "mientras b<B y el montículo no esté vacío", J=min(B,Σr_i), T=O(N+J log N); si Σr_i≤B, x=r; (2) hipótesis a_j≥0, w_ij∈[0,1]; (3) la fórmula de Δ vale solo para i∉S; (4) "a lo sumo k"; (5) el voraz del modo ambos salta a los candidatos que no caben; (6) Σ_{r=1..5} C(15,r)=4 943 sin ∅ (4 944 con ∅); (7) propuesta de candidatos en rondas (= D-21); (8) T1: cuatro huecos cerrados (q sigue en el montículo, j≤B, terminación por topes, g≥0); (9) T3: la cita pasa a Prop. 4.3.1 del enunciado + Karp 1972, más k≥N, NP con racionales, dureza de la subfamilia, modos con costo, dureza fuerte; (10) T4: cota exacta 1−(1−1/k)^k, solo modo k; (11) T5: Θ(kNM).
- **Qué y por qué:** primer bloque del informe de la primera entrega (P0). Las decisiones nuevas D-26…D-29 se registran aquí porque los textos del informe y de SPEC dependen de ellas. Citas: NWF 1978 y Feige 1998 (solo nivel resumen, R-04) y Khuller–Moss–Naor 1999 (solo mencionada); no se afirma garantía para cupo+costo (R-01).
- **Corrección de referencias de commit (sin editar entradas previas):** la entrada C-0005 quedó en el commit `35db17c`, no en `5054456` (que contiene C-0001…C-0004). C-0006 quedó en `5f98f59`. Se corrigió `agent/CONTEXT.md`.
- **Verificación:**
  - Ejecutado por el scribe: `git status --short --untracked-files=all` (6 archivos nuevos en `informe/`, M `agent/SPEC.md`, M `agent/log/auto_changes.log`; `tests/` con `test_smoke.py` y `__pycache__`, sin tocar y fuera de este commit); `git diff --stat`; `git log --oneline`; hora con zoneinfo.
  - Sin verificar: compilación LaTeX (no hay TeX local; D-20); `pytest -q` en este bloque (no ejecutado; `tests/` lo escribe el verifier); verificación de T03 (instancia 4×5 a mano y por código, pendiente del verifier); cifras `[RESULTADO-T06]` y cota `[RESULTADO-T12]` sin rellenar a propósito (vienen del código).
- **Commit:** pendiente (ver `git log`; el hash lo anota la siguiente entrada)
- **Siguiente paso:** `verifier`: cuando termine `tests/test_propiedades.py`, ejecutar `.venv\Scripts\python -m pytest -q` y verificar la instancia 4×5 de `informe/secciones/02_np_dureza.tex` contra `src/ada_g2/select.py`; luego `implementer` (T06) para llenar `[RESULTADO-T06]`.

### C-0008 · 2026-11-05 22:21 · scribe (claude-haiku-5.5), registrando trabajo de verifier (claude-sonnet) y fix de orquestador (claude-opus-5.5) · tarea T05, T06 (y W1, W2, W3, T12, verificación de T03)
- **Tipo:** test + fix (BUG-1)
- **Archivos:**
  - A `tests/helpers.py` — utilidades compartidas por las pruebas
  - A `tests/test_reparto.py` — reparto = DP exacto (hypothesis, 700 instancias, incl. Σr<B); dualidad con brecha ≤1e-9 (700) y dualidad débil
  - A `tests/test_funcion_f.py` — f monótona y submodular, f(∅)=0, Δ incremental = directa (600 instancias)
  - A `tests/test_seleccion.py` — 2250 instancias (3 familias × 3 modos): restricciones, voraz ≥ 1−(1−1/k)^k en modo k, óptimo ≤ cota LP; regresión de BUG-1 (`test_rectangular_sin_cuadrar`, 40 semillas)
  - A `tests/test_np_reduccion.py` — tabla 4×5 del informe, instancia negativa, CobMax-Dec ⇔ Sel-Dec en subfamilia simétrica (60 instancias); instancia ajustada D-15 (razones 3/4, 19/27, 2101/3125)
  - A `tests/test_caso_profesora.py` — reproduce los valores de SPEC §6; contraejemplos de la sección 03 (5/6, 0.1 y el de costos 2/L)
  - A `tests/test_cli_validacion.py` — CLI: 13 JSON inválidos → exit 2; 5 JSON sintéticos válidos → exit 0
  - M `src/ada_g2/select.py` — BUG-1: `voraz` y `mejor_singleton` usaban `len(a)` (M) como N; ahora `W.shape[0]`. Fallaba con N≠M (familia general y reducción); el caso de la profesora (M=N) no cambia
  - M `tests/test_seleccion.py` — la prueba xfail pasa a regresión y se añade `test_rectangular_sin_cuadrar`
  - M `results/caso_entrada_G2_red_15_nodos/tiempo.csv` — tiempos de la ejecución de T06 (resultado sin cambios)
  - M `informe/main.tex` — portada: "Facultad de Inteligencia Artificial e Ingenierías" (corrección del usuario)
  - M `agent/SPEC.md` — §4: "propuesta D-21, pendiente de registrar" → "D-21 (registrada)"
  - M `agent/CONTEXT.md`, `agent/TASKS.md` (T05, T06, W1, W2 ✅; W3, T12 🔄; nota de T03), `agent/DECISIONS.md` (A Q-06), `agent/log/auto_changes.log` (traza automática)
- **Qué y por qué:** verificación independiente de la Parte 1, f, selección, reducción NP y CLI, más allá de los 5 smoke tests. Esta verificación encontró BUG-1 (N≠M), ya corregido. T06: el caso de la profesora se ejecutó sin editar código. Dato para el informe (sección 03): el conteo literal del voraz es k·N·M multiplicaciones (calcula también los ya elegidos); P = kN−k(k−1)/2 evaluaciones útiles; la clase Θ(kNM) se mantiene.
- **Verificación:**
  - Verifier, antes del arreglo: `pytest -q` → 198 passed, 1 xfailed.
  - Orquestador, tras el arreglo: `.venv/Scripts/python -m pytest -q` → **239 passed in 17.32s**.
  - Orquestador: `python -m ada_g2 run --input project-docs/entrada_G2_red_15_nodos.json --out results/` → exit 0, TODO CUMPLE. R1=R2 S={N09,N11,N13,N14,N15} f=145.5795 costo 23 reparto 7/5/5/7/6 u=88.5640; R3 reparto N09:4 N11:8 N13:8 N14:4 N15:6 u=85.6108; Σf=436.7386, Σu=262.7387; pipeline mediana 6.685 ms; exacto de referencia 51.2 ms.
  - Razón mínima medida (3 familias × 3 modos): modo k 0.8885 (familia rala); costo 0.8864; ambos 0.8148 (familia rala, mínima global). Sin garantía en costo ni ambos (R-01).
  - No probado: exit 3 de la CLI; instancias aleatorias N>9; tiempos y T(n) (T13).
  - Sin verificar: compilación LaTeX (sin TeX local). Hook pre-commit: se ejecuta en el commit de esta entrada.
  - No bloqueante (`io.py`): un id repetido produce cascada de "arista a nodo inexistente" y el error de nodo inexistente oculta el de peso.
- **Commit:** pendiente (commit de esta misma entrada; el hash se anota en la siguiente entrada)
- **Siguiente paso:** `report-writer` (T07): `grep -rn "RESULTADO-T06" informe/` y sustituir los marcadores por las cifras de `results/caso_entrada_G2_red_15_nodos/resultado.json`; luego README y manual.

### C-0009 · 2026-11-05 22:32 · scribe (claude-haiku-5.5), registrando trabajo de report-writer (claude-sonnet) y revisión de consistencia parcial del orquestador (claude-opus-5.5) · tarea T07, T08 (parcial)
- **Tipo:** docs
- **Archivos:**
  - M `README.md` — reescrito: identificación, Python 3.12.10, instalación, ejemplo pequeño (`generar --n 6 --seed 7`: exit 0, Σf=97.6109, Σu=89.5223), resultados esperados, pruebas, códigos de salida
  - A `manual/MANUAL_TECNICO.md` — entorno, arquitectura, funcionamiento, uso, validación, límites
  - A `informe/secciones/04_caso_profesora.tex` — tabla por ronda, traza resumida de la ronda 1, verificación de restricciones, certificados, comparación con el exacto, tiempos, saturación R-02
  - M `informe/main.tex` — quita la macro `\RES`; añade el `\input` de la sección 04
  - M `informe/secciones/01_formalizacion.tex`, `informe/secciones/03_optimalidad_y_cota.tex` — marcadores [RESULTADO-T06] / [RESULTADO-T12] sustituidos por cifras reales; nota k·N·M frente a P = kN−k(k−1)/2 (en 03)
  - M `informe/INFORME.md` — espejo sincronizado con el LaTeX
  - M `agent/SPEC.md` — §8: ítems 1–4 marcados con nota; ítem 5 pendiente
  - M `agent/TASKS.md` — T07 ✅; T08 🔄; nota en T10
  - M `agent/DECISIONS.md` — D-30 (estructura de README y manual sin poder leer las guías)
  - M `agent/CONTEXT.md` — reescrito (estado, siguiente paso, pendientes, testigo)
  - M `agent/CHANGELOG.md` — solo esta entrada añadida
  - M `agent/log/auto_changes.log` — traza automática
- **Qué y por qué:** cierra la documentación de la primera entrega (T07) y deja T08 en parcial. Informe, README y manual usan las mismas cifras del código ejecutado. El agente de documentación no pudo leer las guías PDF/DOCX, así que la estructura sigue SPEC §1 y §8 (D-30); el usuario debe contrastarla antes de entregar.
- **Verificación:**
  - report-writer: `pytest -q` → 239 passed in 16.34s.
  - orquestador: chequeo estructural del LaTeX (sin caracteres de control; entornos begin/end y llaves balanceadas; $ pares; cada \ref con su \label y cada \cite con su \bibitem; \input de 01–04): OK.
  - orquestador: grep de cifras (145.5795, 88.5640, 85.6108, 436.7386, 262.7387, 145.9072, 0.9578, 151.9871, λ=1.3220/0.8952) coincide entre informe, INFORME.md, README, manual, `results/caso_entrada_G2_red_15_nodos/resultado.json` y `traza.md`. Sin marcadores sin rellenar.
  - Ejemplo del README (`generar --n 6 --seed 7`): reportado por report-writer; scribe no lo re-ejecutó.
  - Sin verificar: compilación LaTeX (sin TeX local, D-20); contraste con las guías de la profesora (D-30).
  - Tag `v0.1-primera-entrega`: NO creado, a propósito (se crea tras la compilación en letX y la confirmación de la portada).
- **Commit:** pendiente (hash en la siguiente entrada)
- **Siguiente paso:** el usuario compila `informe/` en letX y confirma la fecha de portada; después `git tag v0.1-primera-entrega` (T08).

### C-0010 · 2026-11-05 22:45 · claude-opus-5.5 (orquestador), registro por scribe (claude-haiku-5.5) · tarea W3, Q-06, T08 (parcial), T07 (manual en LaTeX en curso)
- **Tipo:** feat + docs
- **Archivos:**
  - M `src/ada_g2/generator.py` — añade `instancia_ajustada(k)`: familia general N=2k ≠ M, no expresable en el esquema JSON (D-15)
  - M `src/ada_g2/cli.py` — subcomando `ajustada [--k 2 3 5]` (`cmd_ajustada`): voraz modo k frente a fuerza bruta, razón exacta con `Fraction`; exit 0 si coincide con 1−(1−1/k)^k, 3 si no
  - M `tests/test_seleccion.py` — la prueba de la instancia ajustada usa la función del generador (sin `cuadrar()` ni constructor local); nueva prueba `test_cli_ajustada_sale_con_cero`
  - M `README.md` — §6.1 (`ajustada`); §10 "Alcance: solución base frente a variantes" (variantes (a) y (b) parciales, (c) no desarrollada, T13 no desarrollada; errores conocidos: ninguno abierto); fila `tools/` en la estructura; manual en LaTeX
  - M `informe/secciones/03_optimalidad_y_cota.tex`, M `informe/INFORME.md` — la instancia ajustada se cita como construida por `instancia_ajustada` y reproducible con `python -m ada_g2 ajustada`
  - A `tools/leer_docs.py` — extrae texto de PDF y DOCX a `.txt` (pdfplumber, pypdf, python-docx)
  - A `requirements-dev.txt` — pdfplumber 0.11.10, pypdf 6.21.4, python-docx (herramientas de lectura)
  - A `informe/informe.pdf` — compilado por el usuario en letX (21 páginas). Revisado con pdfplumber: portada (Facultad de Inteligencia Artificial e Ingenierías; Manizales, 6 de noviembre de 2026), índice de las secciones 1-4, sin "??". Anterior al cambio de 03: hay que recompilarlo antes del tag
  - M `.gitignore` — ignora `informe/*.zip` y `manual/*.zip`
  - M `agent/DECISIONS.md` (Q-06 resuelta; D-30 marcada VERIFICADA por D-31; añade D-31 y D-32), `agent/TASKS.md` (W3 ✅; T07 🔄; T08 anotada), `agent/CONTEXT.md`, `agent/CHANGELOG.md`, `agent/log/auto_changes.log`
  - Excluido a propósito: `manual/MANUAL_TECNICO.md` (M) y `manual/manual_tecnico.tex` (en curso, report-writer). Irán en una entrada posterior.
- **Qué y por qué:** Q-06 resuelta por delegación del usuario: la instancia ajustada (D-15) entra en el generador, así la cota 1−(1−1/k)^k se reproduce con un comando y no solo con un test. El usuario pidió herramientas para leer las guías; con ellas se contrastó la estructura de README y manual (D-30 → D-31). El README declara la solución base frente a las variantes (guía §5).
- **Verificación:**
  - orquestador: `.venv/Scripts/python -m pytest -q` → 240 passed in 17.18s (scribe no lo re-ejecutó)
  - orquestador: `python -m ada_g2 ajustada` con k=2,3,5 → 3/4, 19/27, 2101/3125; "cota alcanzada exactamente"; exit 0. Son las mismas fracciones que 6/8, 57/81, 10505/15625 de W3, sin reducir
  - orquestador: pdfplumber sobre `informe/informe.pdf` (portada, índice 1-4, sin "??")
  - scribe: `git status --short` y `git diff --stat` revisados; ningún archivo cambiado queda fuera de la lista salvo `manual/` (excluido a propósito)
  - Sin verificar: compilación de `informe/main.tex` tras el cambio de 03; compilación de `manual/manual_tecnico.tex` (aún no existe; el usuario compila en letX)
- **Commit:** pendiente (hash en C-0011). C-0009 quedó en `4376f41`.
- **Siguiente paso:** el usuario recompila `informe/main.tex` en letX y sustituye `informe/informe.pdf`; luego compila `manual/manual_tecnico.tex`, sube ambos PDF al repo y solo entonces crea el tag `v0.1-primera-entrega`.

### C-0011 · 2026-11-05 22:48 · claude-haiku-5.5 (scribe), con report-writer (claude-sonnet) · tarea T07, T08 (manual en LaTeX)
- **Tipo:** docs
- **Archivos:**
  - A `manual/manual_tecnico.tex` — manual técnico en LaTeX: un solo archivo con el preámbulo y la portada de `informe/main.tex` (título "Manual técnico de la solución base"); paquetes extra longtable, tabularx, listings, xcolor, tikz (sin minted ni shell-escape); secciones 1:1 con la guía §6 (Entorno · Arquitectura · Funcionamiento · Uso · Validación y límites · Identificación); figura TikZ del pipeline por ronda (sin compilar; si falla, la lista numerada la reemplaza); pseudocódigos de los 2 algoritmos; tablas de módulos, JSON de entrada, columnas de salida, códigos de salida, pruebas y alcance; salida de consola de `run`, `ajustada` y `generar`
  - M `manual/MANUAL_TECNICO.md` — remite al PDF `manual/manual_tecnico.pdf`; "sistema compatible": Windows 11 probado, Linux/macOS no probados; incluye `ajustada`; 240 pruebas; nueva sección 6b con errores conocidos y tabla de alcance base frente a variantes
  - M `agent/CONTEXT.md` (reescrito), `agent/TASKS.md` (notas en T07 y T08), `agent/DECISIONS.md` (D-33 manual en LaTeX; D-34 tag diferido), `agent/CHANGELOG.md` (solo esta entrada añadida), `agent/log/auto_changes.log` (traza automática)
- **Qué y por qué:** pedido del usuario: manual técnico en LaTeX para compilar en letX (D-20), además del Markdown. El contenido sigue la guía §6 (D-31). C-0010 quedó en el commit `730c8fa` (no se edita su entrada).
- **Verificación:**
  - report-writer: `python -m ada_g2 run --input project-docs/entrada_G2_red_15_nodos.json --out results/` → exit 0, Σf=436.7386, Σu=262.7387, TODO CUMPLE (re-ejecutado por report-writer)
  - report-writer: `python -m ada_g2 ajustada` → exit 0; 3/4, 19/27, 2101/3125 (re-ejecutado por report-writer)
  - report-writer: `generar` → salida copiada del manual en Markdown (no re-ejecutada en este turno)
  - report-writer: chequeo estructural por script de `manual_tecnico.tex` (entornos y anidamiento, llaves, $, \left/\right, \ref↔\label, sin Unicode dentro de lstlisting) → OK
  - scribe: `git status --short` = `M manual/MANUAL_TECNICO.md`, `?? manual/manual_tecnico.tex`, sin otros cambios fuera de agent/; C-0010 presente en `730c8fa`
  - scribe: no hubo cambios de código; `pytest` no re-ejecutado en esta entrada (último resultado: 240 passed, C-0010)
  - Sin verificar: compilación LaTeX de `manual/manual_tecnico.tex` (sin TeX local, D-20); figura TikZ; recompilación de `informe/informe.pdf` tras el cambio de 03 (pendiente del usuario en letX)
  - Tag `v0.1-primera-entrega`: NO creado (D-34)
- **Commit:** pendiente (hash en la respuesta del scribe; se registra en la siguiente entrada)
- **Siguiente paso:** el usuario compila en letX `manual/manual_tecnico.tex` (pdfLaTeX, 2 pasadas) → `manual/manual_tecnico.pdf`, y recompila `informe/main.tex` → `informe/informe.pdf`; después commit de ambos PDF y `git tag v0.1-primera-entrega` sobre ese commit.

### C-0012 · 2026-11-05 23:09 · claude-haiku-5.5 (scribe), por orden del orquestador · tarea T08 (cierre de la primera entrega; tag v0.1-primera-entrega)
- **Tipo:** docs + chore
- **Archivos:**
  - M `informe/informe.pdf` — recompilado por el usuario en letX: 21 págs.; incluye el cambio de la sección 3 (`instancia_ajustada`, `python -m ada_g2 ajustada`); sustituye al PDF de C-0010
  - A `manual/manual_tecnico.pdf` — compilado por el usuario en letX: 13 págs.; figura TikZ compiló; portada correcta
  - M `agent/SPEC.md` — §8 ítem 5 marcado `[x]` (consistencia)
  - M `agent/TASKS.md` — T07 ✅ y T08 ✅ con nota
  - M `agent/DECISIONS.md` — D-34 cumplida; D-35 (push y tag autorizados por el usuario); Q-02: visibilidad resuelta, pregunta de trabajo individual abierta
  - M `agent/CONTEXT.md` — reescrito: P0 completo, siguiente paso P1 (T13) en sesión nueva
  - M `agent/CHANGELOG.md` — solo esta entrada añadida
  - M `agent/log/auto_changes.log` — traza automática (si hubo cambios)
  - Tag anotado `v0.1-primera-entrega` sobre el commit de esta entrada (no es archivo)
  - Excluido a propósito: `informe/informe.zip` (ignorado por `.gitignore`)
- **Qué y por qué:** cierra la primera entrega (P0). PDF finales compilados en letX por el usuario; checklist SPEC §8 completo; tag según D-34. El usuario dejó el repo público (Q-02, visibilidad) y pidió push (D-35).
- **Verificación:**
  - orquestador: pdfplumber sobre `informe/informe.pdf` → 21 págs., 0 "??"; sobre `manual/manual_tecnico.pdf` → 13 págs., 0 "??", portada correcta, figura TikZ compiló.
  - scribe: `git status --short` antes de añadir = `M informe/informe.pdf` y `?? manual/manual_tecnico.pdf`; `git diff --stat` de informe.pdf: 565421 → 565484 bytes. `agent/log/auto_changes.log` sin cambios en ese momento.
  - Sin cambios de código: `pytest` no re-ejecutado en esta entrada (último: 240 passed, C-0010).
  - Pre-commit: resultado en la respuesta del scribe (sin `--no-verify`).
  - Sin verificar: visibilidad pública del repo (declarada por el usuario; no comprobada por el scribe); revisión visual de los PDF más allá de pdfplumber.
- **Commit:** el commit que contiene esta entrada (`git log -1`); tag `v0.1-primera-entrega` sobre él. C-0011 = `72cca80`; C-0010 = `730c8fa`; C-0009 = `4376f41`.
- **Siguiente paso:** sesión nueva; leer `agent/CONTEXT.md` y empezar P1 con T13 (experimentos E1–E3 en `results/experimentos/`, según `agent/SPEC.md`).

### C-0013 · 2026-11-06 09:07 · claude-haiku-5.5 (scribe), por orden del orquestador (Claude Code) · tarea T10 (mejor caso, peor caso y caso promedio); nueva T10b
- **Tipo:** test + docs (la parte de informe y manual aún no está escrita)
- **Archivos:**
  - A `tests/test_casos_complejidad.py` — 33 pruebas que cuentan operaciones: reparto (iteraciones = J = min(B, Σr_i) en 405 instancias); `heappop` con al menos floor(log2 n) comparaciones para n≥3 y 0 para n=2; voraz en modo k con nodo "estrella" (2 llamadas a `ganancias_todas`, |S|=1) y con todo c_i>L (1 llamada, S=∅); caso promedio del generador (exactamente kmax pasos); fuerza bruta (visitas=1 si nada cabe; sin poda, visitas = nº de subconjuntos)
  - M `agent/CONTEXT.md` (reescrito), `agent/TASKS.md` (nota en T10; T10b nueva), `agent/DECISIONS.md` (D-36: caso promedio bajo el modelo del generador), `agent/CHANGELOG.md` (solo esta entrada añadida), `agent/log/auto_changes.log` (traza automática)
- **Qué y por qué:** pedido del usuario: verificar que el informe dé la notación del mejor caso, el peor caso y el caso promedio. La revisión encontró: (1) reparto con mejor caso Θ(N) y peor caso solo O(N+B log N), sin cota ajustada; (2) el voraz de selección se presentaba como Θ(kNM), pero `select.py` se detiene antes de k pasos cuando no hay candidatos que quepan, así que su mejor caso es Θ(NM); (3) fuerza bruta solo con cota O; (4) rondas, certificados y solución completa sin analizar; (5) caso promedio ausente. Las pruebas de este bloque respaldan los conteos de (1), (2) y (3). Plan aprobado: theorist añade la subsección "Mejor caso, peor caso y caso promedio" con tabla resumen en `informe/secciones/03_optimalidad_y_cota.tex` y la replica en `informe/INFORME.md` y `manual/MANUAL_TECNICO.md`.
- **Verificación:**
  - orquestador: `.venv/Scripts/python.exe -m pytest -q` → 273 passed, 0 failed (240 previas + 33 nuevas). Con el `py` del sistema la recolección falla (ModuleNotFoundError: ada_g2); usar el venv.
  - scribe: no re-ejecutó pytest (el resultado es el reportado por el orquestador). Confirmado por `git status --short`: `?? tests/test_casos_complejidad.py` y `M agent/log/auto_changes.log`; el archivo define 11 funciones `test_` (33 casos al parametrizar).
  - scribe: `git status --short` en el momento del registro no muestra cambios en `informe/` ni en `manual/`.
  - Sin verificar: la subsección de informe y manual (aún no escrita); la deducción formal de T(n) (T10); el caso promedio frente a experimentos reales (T13).
- **Commit:** pendiente (no se hace commit en esta entrada; el commit se hará al final, con los cambios del theorist en `informe/` y `manual/`, que deben registrarse en una entrada posterior)
- **Siguiente paso:** theorist escribe la subsección "Mejor caso, peor caso y caso promedio" en `informe/secciones/03_optimalidad_y_cota.tex`, replica en `informe/INFORME.md` y `manual/MANUAL_TECNICO.md`, y el scribe registra con C-0014.

### C-0014 · 2026-11-06 09:17 · claude-haiku-5.5 (scribe), por orden del orquestador (Claude Code); análisis del theorist (claude-opus-5.5) · tarea T10b (mejor caso, peor caso y caso promedio; cierre teórico)
- **Tipo:** docs + test + chore (solo docstrings en `src/`)
- **Archivos:**
  - M `informe/secciones/03_optimalidad_y_cota.tex` — subsección "Mejor caso, peor caso y caso promedio" (`\label{sec:casos}`): lema lem:heapq, prop:casos-reparto, prop:casos-voraz, prop:casos-fb, DP, certificados, solución completa y tabla tab:casos; reparto peor caso Θ(N+B(1+log N)); espacio Θ(N+J); Θ(kNM) invariante solo en el pseudocódigo (mejor caso del código Θ(NM)); nota de fidelidad de la fuerza bruta
  - M `informe/INFORME.md` — nueva §3.3 (espejo); la cota 1−1/e pasa a §3.4
  - M `manual/MANUAL_TECNICO.md` — nueva §3.5 (espejo)
  - M `manual/manual_tecnico.tex` — `sec:casos-manual` como longtable
  - A `tests/test_casos_complejidad.py` — 33 pruebas que cuentan operaciones (su registro es C-0013; se commitea aquí)
  - M `src/ada_g2/select.py` — solo docstring de `seleccionar` (T = O(kmax·N·M); en modo `costo` kmax = |cand|)
  - M `src/ada_g2/rounds.py` — solo docstring de `ejecutar` (kmax en modo `costo`)
  - M `agent/CHANGELOG.md` (C-0013 y C-0014 añadidas), `agent/CONTEXT.md`, `agent/TASKS.md`, `agent/DECISIONS.md` (D-37), `agent/log/auto_changes.log`
- **Qué y por qué:** pedido del usuario (C-0013): el informe debe dar mejor caso, peor caso y caso promedio. Al redactar, el theorist halló que en modo `costo` `limites` fija kmax = |cand|, así que el voraz cuesta Θ(min(N,L+1)·N·M), o Θ(N²M) si hay c_i = 0, y no Θ(kNM). Por eso se corrigieron los docstrings (solo comentarios; la lógica no cambió). Quedan [VERIFICAR] (fuera de la bibliografía verificada): costo C_PL de HiGHS en el certificado de la selección, Khachiyan 1979 y el umbral de underflow. Los PDF `informe/informe.pdf` y `manual/manual_tecnico.pdf` quedan DESACTUALIZADOS hasta recompilar en letX.
- **Verificación:**
  - scribe: `.venv/Scripts/python.exe -m pytest -q` → `273 passed in 14.37s` (re-ejecutado en esta entrada).
  - orquestador (reportado, no re-ejecutado por el scribe): caso de la profesora `python -m ada_g2 run --input project-docs/entrada_G2_red_15_nodos.json --out results/` → "TODO CUMPLE".
  - orquestador (reportado): chequeo estático de LaTeX (entornos balanceados, `$` pares, 0 `\ref` sin `\label`, entornos de teorema definidos, longtable cargado) → limpio.
  - Sin verificar: compilación LaTeX de `informe/main.tex` y `manual/manual_tecnico.tex` (sin TeX local, D-20); costo C_PL de HiGHS; Khachiyan 1979; umbral de underflow.
- **Commit:** pendiente. Este commit único incluye C-0013 y C-0014; el hash se anota en la siguiente entrada.
- **Siguiente paso:** el usuario compila en letX `informe/main.tex` y `manual/manual_tecnico.tex` (pdfLaTeX, 2 pasadas) y sube los PDF; después T14 (incorporar la tabla de casos en la guía de estudio).

### C-0015 · 2026-11-06 14:40 · claude-haiku-5.5 (scribe), por orden del orquestador (Claude Code) · tarea T08 (reabierta: maquetación y citas de informe y manual; PDF pendientes de recompilar)
- **Tipo:** fix (typesetting y bibliografía; sin cambios de código)
- **Archivos:**
  - M `informe/main.tex` — paquetes graphicx, xurl y `\emergencystretch=3em`; macro `\cod` (expl3, `\str_map_function` con `\discretionary` tras `_ . / [ - :`) para identificadores que sí se pueden cortar; viñeta en Convenciones que explica el ■ (fin de demostración)
  - M `informe/referencias.tex` — nuevas entradas `cpython_heapq`, `scipy_linprog` (URL, consultadas el 2026-11-06) y `khachiyan1979` (marcada `\VER`: no cotejada con el original); comentario de `fnw1978` actualizado
  - M `informe/secciones/01_formalizacion.tex`, `02_np_dureza.tex` — `\texttt` de identificadores largos pasan a `\cod`; en 02, "$S_1,\dots,S_n\subseteq U$" pasa a "$S_1,\dots,S_n$ de subconjuntos de $U$" para que el renglón pueda cortarse
  - M `informe/secciones/03_optimalidad_y_cota.tex` — columna "Instancia testigo" de tab:casos de 3.6 a 3.0 cm; citas nuevas: `villegas2016` (cap. 5 en el contraejemplo del voraz; cap. 9 al inicio de sec:cota), `notas` (§2.3 invariante; §2.1 costeo; §2.1.1 y cap. 1 en sec:casos), `fnw1978` en el teorema NWF, `cpython_heapq` (2 veces), `scipy_linprog`, `khachiyan1979`; `\cod` en lugar de `\texttt`
  - M `informe/secciones/04_caso_profesora.tex` — tab:rondas compactada (reparto "7/5/5/7/6", leyenda en el caption) y envuelta en `\resizebox` (solo reduce si no cabe)
  - M `manual/manual_tecnico.tex` — `\cod` igual que en el informe; xurl y `\emergencystretch`; `\noindent` antes de las 3 tabularx (sangría de 17 pt que babel en español añade al primer párrafo); columnas de las longtable de módulos (6.4→6.2, 6.2→6.0) y de campos (5.2→5.0, 4.4→4.2); la ruta `.venv\Scripts\activate` pasa a `\texttt` con `\textbackslash`
  - M `agent/CHANGELOG.md` (solo esta entrada añadida), `agent/CONTEXT.md` (reescrito; corrige el commit de C-0013+C-0014 a `586beec`), `agent/TASKS.md` (T08 reabierta; nota en T10b), `agent/DECISIONS.md` (D-38), `agent/log/auto_changes.log` (traza automática)
  - **No se commitean** `informe/informe.pdf` y `manual/manual_tecnico.pdf`: siguen modificados porque son los compilados por el usuario antes de estas correcciones (muestran los defectos). Se commitean cuando el usuario recompile.
- **Qué y por qué:** el usuario compiló en letX y reportó: (1) texto encimado en la tabla de campos del JSON del manual; (2) tablas del informe que se salen del margen; (3) preguntó si las referencias se citan donde se usan; (4) preguntó qué son los cuadrados negros. Diagnóstico con pdfplumber (orquestador): unos 20 renglones del informe y 17 del manual se salen del margen derecho. Causas: `\texttt` no corta; tab:rondas medía ~626 pt frente a 453 pt del renglón; tab:casos sumaba ~16.15 cm frente a 16 cm; tres tabularx del manual sangradas 17 pt. Los ■ son `\qedsymbol` (fin de demostración), intencionales según el estilo de la profesora. Citas: villegas2016 y fnw1978 estaban en la bibliografía sin citarse; notas se citaba una vez; las fuentes nuevas de sec:casos no tenían entrada.
- **Verificación:**
  - orquestador (reportado, no re-ejecutado por el scribe): chequeo estático de LaTeX: entornos balanceados, `$` pares, llaves balanceadas, 0 `\ref` sin `\label`, 0 `\cite` sin `\bibitem`, 0 `\bibitem` sin citar, ningún `\cod` con `%`, `#`, `{` o `\`, ningún `\cite[]` sin proteger dentro de argumento opcional.
  - pytest: no aplica (sin cambios de código). Último resultado conocido: 273 passed (C-0014).
  - scribe: `git status --short` y `git diff --stat` confirman los 10 archivos modificados (sin archivos sin seguimiento).
  - Sin verificar: compilación en letX de `informe/main.tex` y `manual/manual_tecnico.tex`. Riesgo principal: la macro `\cod` (expl3) exige LaTeX ≥ 2020-10; xurl también. Si letX falla en `\cod`, alternativa: `\newcommand{\cod}[1]{\texttt{\detokenize{#1}}}`.
- **Commit:** pendiente (el hash del commit que contiene esta entrada se reporta en la respuesta del scribe y se anota en la siguiente entrada). Commit anterior de C-0013 y C-0014: `586beec`.
- **Siguiente paso:** el usuario recompila en letX `informe/main.tex` y `manual/manual_tecnico.tex` (pdfLaTeX, 2 pasadas); el orquestador mide los desbordes con pdfplumber; después commit de los dos PDF.
