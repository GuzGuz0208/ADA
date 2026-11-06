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
