# Manual técnico — ADA 2026-B · Grupo 2 · Subproyecto 2
**Reparto de presupuesto y selección de participantes** · Integrante: Juan Esteban Guzmán Henao · Profesora: Luz Enith Guerrero · Universidad de Caldas · Repositorio: https://github.com/GuzGuz0208/ADA · Versión `v0.1-primera-entrega` (paquete 0.1.0)

**Versión PDF de este manual:** `manual/manual_tecnico.pdf` (fuente LaTeX: `manual/manual_tecnico.tex`, se compila con pdfLaTeX en letX). Este archivo Markdown es el espejo del mismo contenido.

Este manual describe el código de `src/ada_g2/` tal como está. Lo que el código no hace, se dice en la Sección 6. Las demostraciones (NP-dureza, optimalidad, cota 1 − 1/e) están en `informe/`, no aquí.

---

## 1. Entorno

| Elemento | Detalle |
|---|---|
| Lenguaje | Python ≥ 3.10 (probado con 3.12.10) |
| Dependencias de ejecución | `numpy>=1.26`, `scipy>=1.11` (`pyproject.toml`) |
| Desarrollo y pruebas | `matplotlib>=3.8`, `pytest>=8.0`, `hypothesis>=6.100` (`requirements.txt`) |
| Sistema compatible | Probado en Windows 11 (Git Bash y PowerShell). No usa rutas absolutas ni nada específico del sistema, por lo que debería funcionar en Linux y macOS, pero allí **no se ha probado** |
| Instalación | `python -m venv .venv` → activar → `pip install -r requirements.txt` → `pip install -e .` |
| Punto de entrada | `python -m ada_g2 {run, generar, ajustada}` (`src/ada_g2/__main__.py` → `cli.main`) |
| Semilla por defecto | 20261105 (`ada_g2.SEMILLA_POR_DEFECTO`), D-11 |

En Linux/macOS se activa con `source .venv/bin/activate`; en Windows con `.venv\Scripts\activate`.

---

## 2. Arquitectura

### 2.1 Carpetas

| Carpeta | Responsabilidad |
|---|---|
| `src/ada_g2/` | el código (paquete instalable) |
| `tests/` | pruebas (7 archivos, 240 pruebas con parametrización) |
| `results/` | salidas por caso: `caso_<nombre>/` |
| `informe/` | informe técnico LaTeX + espejo Markdown |
| `manual/` | este manual |
| `project-docs/` | enunciado y JSON de la profesora (solo lectura) |
| `agent/` | memoria de trabajo de los agentes (decisiones D-xx, bitácora); no es parte de la solución |

### 2.2 Módulos de `src/ada_g2/`

| Módulo | Responsabilidad | Funciones y clases principales |
|---|---|---|
| `io.py` | Cargar y validar el JSON. Reúne **todos** los errores con su ruta (p. ej. `nodos[3].costo_participacion`) y lanza `EntradaInvalida`. Construye la matriz simétrica `W` con `W[i,i] = 1` | `cargar`, `desde_dict`, `Instancia`, `EntradaInvalida` |
| `model.py` | Modelo matemático: utilidad u(x) = a·ln(1+x), ganancia marginal, función de cobertura f y vector residual R_j | `utilidad`, `ganancia_marginal`, `residual_inicial`, `ganancias_todas`, `ganancia_uno`, `actualizar_residual`, `f_directa` |
| `select.py` | **Parte 2.** Voraz por ganancia marginal (`voraz`, criterios `ganancia` y `razon`), mejor nodo individual (`mejor_singleton`) y escogencia según el modo | `seleccionar`, `voraz`, `mejor_singleton`, `limites`, `MODOS` |
| `allocate.py` | **Parte 1.** Reparto voraz con montículo (`heapq`) y topes por nodo | `asignar`, `ResultadoReparto`, `PasoReparto` |
| `rounds.py` | Cadena de T rondas (Parte 2 → Parte 1), topes restantes, política de gasto, fallas con probabilidad q, verificación explícita de restricciones, comparación con el exacto | `ejecutar`, `verificar_ronda`, `comparar_exacto`, `Corrida`, `Ronda` |
| `certificates.py` | Certificados por ejecución (D-14): dualidad de Lagrange para el reparto; cota por programa lineal (HiGHS) para la selección | `certificar_reparto`, `certificar_seleccion` |
| `exact.py` | Referencias exactas para validar: fuerza bruta de la selección (DFS) y DP del reparto | `fuerza_bruta`, `dp_reparto`, `num_subconjuntos` |
| `generator.py` | Instancias sintéticas con el mismo esquema JSON, deterministas por semilla; instancia ajustada D-15 (`instancia_ajustada(k)`, familia general N≠M) | `generar`, `ajustada` |
| `trace.py` | Escribe `resultado.json`, `tiempo.csv`, `traza.md`, `traza.csv` | `escribir_json`, `escribir_tiempos`, `escribir_traza`, `a_dict` |
| `cli.py` | Línea de comandos `run`, `generar` y `ajustada`; códigos de salida | `main`, `cmd_run`, `cmd_generar`, `cmd_ajustada` |

Dependencias entre módulos: `cli → io, rounds, trace, generator`; `rounds → select, allocate, certificates, exact, model, io`; `select → model`; `allocate → model`; `certificates → model, allocate`.

---

## 3. Funcionamiento

### 3.1 Flujo general (por ronda t = 1…T)

1. **Disponibles.** A_t = nodos con presupuesto total restante > 0 (D-21) que no fallan en la ronda (cada uno falla con probabilidad q; D-07: q = 0 por defecto).
2. **Parte 2 — selección.** `seleccionar` devuelve S_t ⊆ A_t según el modo (`k`, `costo`, `ambos`).
3. **Topes.** r_i(t) = restante del nodo i (política `concentrado`) o `ceil(restante/(T−t+1))` (política `uniforme`, D-22).
4. **Parte 1 — reparto.** `asignar(a_S, topes_S, B)` reparte B unidades entre S_t.
5. **Verificación.** `verificar_ronda` comprueba las restricciones; se compara f incremental con f directa.
6. **Certificados.** dualidad (reparto) y LP (selección).
7. **Actualización.** `restante_i ← restante_i − x_i`.

Al final se verifica la restricción global Σ_t x_{i,t} ≤ R_i. La corrida es correcta (`ok`) si todo cumple.

### 3.2 Algoritmo de la Parte 2 (`select.py`)

- **Modelo.** f(S) = Σ_j a_j [1 − Π_{i∈S}(1 − w_ij)]. Con el vector residual R_j = Π_{l∈S}(1 − w_lj) (inicial R_j = 1), la ganancia de agregar i ∉ S es Δ(i|S) = Σ_j a_j·w_ij·R_j. Al elegir i se actualiza R_j ← R_j·(1 − w_ij), en O(M).
- **Implementación.** En cada paso `ganancias_todas` calcula el producto matriz-vector `W @ (a*R)` (las ganancias de **todos** los candidatos, O(N·M)); se enmascaran los ya elegidos, los que no son candidatos y los que no caben en el costo; se escoge con `np.argmax` (primer máximo = menor índice, D-12). Se detiene con |S| = kmax, cuando no hay candidato factible o cuando la mejor ganancia es ≤ 0.
- **Modos** (`limites`): `k` → |S| ≤ k; `costo` → Σ c ≤ L; `ambos` → las dos. En todos |S| ≤ k significa "a lo sumo" (D-27).
- **Heurísticas.** Modo `k`: solo `voraz_ganancia` (garantía 1 − (1 − 1/k)^k ≥ 1 − 1/e, Nemhauser–Wolsey–Fisher 1978; prueba en informe, Sección 3.3). Modos `costo` y `ambos`: el mejor entre `voraz_ganancia`, `voraz_razon` (ganancia/costo) y `singleton` (mejor nodo individual factible). En empate gana la primera en ese orden (D-23). El voraz factible salta a los candidatos que no caben en vez de detenerse (D-29). **No se afirma garantía en `costo` y `ambos`** (R-01).
- **Costo.** Θ(k·N·M) (Θ(k·N²) con M = N en el JSON). Las evaluaciones útiles son P = kN − k(k−1)/2, pero el código calcula las N ganancias en cada paso, así que hace literalmente k·N·M multiplicaciones; la clase no cambia (informe, Sección 3.2, nota de fidelidad).

### 3.3 Algoritmo de la Parte 1 (`allocate.py`)

- Ganancia marginal de dar la unidad (x+1) al nodo i: g_i(x) = a_i·ln((x+2)/(x+1)), estrictamente decreciente en x.
- **Estructura de datos:** montículo de máximos con `heapq` (que es de mínimos, por lo que se guarda `(-g, i)`). Contiene, para cada nodo con tope > 0, su próxima ganancia. Construcción con `heapify` en O(N).
- **Ciclo:** mientras se hayan asignado menos de B unidades y el montículo no esté vacío: se toma la mayor ganancia (la raíz); se incrementa `x[i]`; si `x[i] < tope[i]` se reemplaza la raíz por la nueva ganancia (`heapreplace`, O(log N)), si no se saca (`heappop`, O(log N)). Desempate por menor índice (D-12).
- **Condición de parada:** B unidades asignadas **o** montículo vacío (D-28: si Σ topes < B, sobra presupuesto y no es un error).
- **Invariante:** tras j pasos, las j unidades tomadas son las j mayores ganancias marginales del multiconjunto; por eso el resultado es óptimo (Teorema 3.1 del informe, por intercambio y concavidad).
- **Costo:** T(N, B) = O(N + B log N). La utilidad final se recalcula directamente (`sum a_i ln(1+x_i)`), no se acumula.

### 3.4 Certificados (`certificates.py`)

- **Reparto (dualidad).** Con λ = ganancia de la última unidad asignada (0 si los topes impiden gastar B), la cota UB(λ) = λ·B + Σ_i máx_{0≤x≤r_i} [a_i ln(1+x) − λx] es ≥ al óptimo. El programa exige brecha UB − utilidad ≤ 10⁻⁹. Si se cumple, el reparto es óptimo y no hace falta conocer el óptimo por otro método.
- **Selección (LP).** Para cualquier S factible y f monótona y submodular: f(S\*) ≤ f(S) + máx{Σ Δ(e|S)·z_e : Σ z_e ≤ k, Σ c_e z_e ≤ L, 0 ≤ z ≤ 1}. Se resuelve con `scipy.optimize.linprog` (HiGHS). Razón certificada = f(S)/cota. Vale con cupo y costo a la vez.
- **Exactos de referencia (`exact.py`, solo validación).** `fuerza_bruta`: DFS sobre subconjuntos factibles (hasta 3 000 000 de visitas). `dp_reparto`: programación dinámica sobre nodos y presupuesto.

---

## 4. Uso paso a paso

### 4.1 Formato del JSON de entrada

Esquema de la profesora (`project-docs/entrada_G2_red_15_nodos.json`). Todos los campos son obligatorios.

```json
{
  "parametros": {
    "numero_nodos": 15,
    "numero_rondas": 3,
    "cupo_participantes_por_ronda_k": 5,
    "presupuesto_ruido_por_ronda_B": 30,
    "presupuesto_costos_participacion_por_ronda": 24
  },
  "grafo": [
    { "u": "N01", "v": "N02", "peso_influencia": 0.25 }
  ],
  "nodos": [
    { "id": "N01", "coeficiente_utilidad": 8.5, "presupuesto_total_nodo": 18, "costo_participacion": 3 }
  ]
}
```

| Campo | Tipo y regla | Significado en el código |
|---|---|---|
| `parametros.numero_nodos` | entero ≥ 1; debe coincidir con `len(nodos)` | N |
| `parametros.numero_rondas` | entero ≥ 1 | T |
| `parametros.cupo_participantes_por_ronda_k` | entero ≥ 1 | k. Si k ≥ N se emite un aviso (el enunciado supone k < N); no es error |
| `parametros.presupuesto_ruido_por_ronda_B` | entero ≥ 0 | B: unidades a repartir por ronda |
| `parametros.presupuesto_costos_participacion_por_ronda` | entero ≥ 0 | L: costo máximo por ronda |
| `grafo[]` | lista de aristas | cada par se lista una vez; se trata como no dirigido (D-10): w_uv = w_vu |
| `grafo[].u`, `grafo[].v` | ids de `nodos`; sin autolazos | extremos |
| `grafo[].peso_influencia` | real en [0, 1]; una arista repetida debe tener el mismo peso | w_uv. Pares ausentes: w = 0. La diagonal w_ii = 1 la fija el modelo (D-02) |
| `nodos[].id` | texto no vacío, único | nombre; el orden de la lista define el índice y el desempate (D-12) |
| `nodos[].coeficiente_utilidad` | real > 0 | a_i (en f, a_j; en u, a_i) |
| `nodos[].presupuesto_total_nodo` | entero ≥ 0 | R_i: tope de ruido en las T rondas (D-06) |
| `nodos[].costo_participacion` | entero ≥ 0 | c_i |

Cualquier incumplimiento produce el código de salida 2 y un mensaje que lista todos los problemas, por ejemplo: `grafo[0].peso_influencia: debe estar en [0,1], se recibio 1.5`. La lógica no contiene constantes del caso: otro JSON con este esquema se ejecuta sin cambiar código.

### 4.2 Pasos

1. Instalar el entorno (README, Sección 4).
2. (Opcional) generar una instancia: `python -m ada_g2 generar --n 6 --rondas 2 --k 3 --B 10 --L 12 --seed 7 --out ejemplo_n6.json`. Parámetros: `--n` (obligatorio), `--rondas` (3), `--k` (5), `--B` (30), `--L` (por defecto round(0.8·k·costo medio)), `--seed` (20261105), `--densidad` (1.0 = grafo completo; con <1 cada par aparece con esa probabilidad), `--out` (obligatorio).
3. Ejecutar: `python -m ada_g2 run --input <json> --out <carpeta> [--modo ambos|k|costo] [--seed S] [--repeticiones R] [--q Q] [--politica concentrado|uniforme]`.
4. Leer la salida en consola (resumen por ronda y veredicto) y los archivos en `<carpeta>/caso_<nombre del json>/`.
5. Revisar el código de salida (`echo $?` o `echo %ERRORLEVEL%`): 0, 2 o 3.

### 4.3 Archivos de salida

**`resultado.json`** (campos principales)

| Campo | Contenido |
|---|---|
| `version`, `caso`, `entorno` | versión del paquete, nombre del caso, versión de Python y plataforma |
| `parametros` | N, T, k, B, L, aristas, modo, q, política, semilla |
| `avisos` | lista de avisos de la carga (p. ej. k ≥ N) |
| `rondas[]` | una entrada por ronda (ver abajo) |
| `totales` | `suma_f`, `suma_utilidad`, `gasto_por_nodo`, `presupuesto_total_nodo` |
| `verificacion_global` | Σ_t x_{i,t} ≤ R_i |
| `todo_cumple` | `true` si todo cumple (código 0) |

Cada elemento de `rondas[]`: `ronda`; `disponibles`; `seleccion` (ids de S_t); `detalle_seleccion` (`elegida` y `alternativas` con heurística, S en orden de elección, f y costo); `f`; `costo_participacion`; `topes_antes` (restante por participante); `topes_efectivos` (tope de la política); `reparto` (unidades por nodo); `unidades_asignadas`; `gasto_ruido`; `utilidad`; `verificacion_restricciones` (lista de `{restriccion, descripcion, valor, limite, aplica, cumple}`); `certificado_reparto` (`lambda`, `cota_superior`, `utilidad`, `brecha`, `tolerancia`, `ok`); `certificado_seleccion` (`f_S`, `extra`, `cota_superior`, `razon_certificada`, `ok`); `comparacion_exacto` (`seleccion_optima`, `f_optima`, `razon_voraz_sobre_optimo`, `subconjuntos_evaluados`, `subconjuntos_teoricos`, `reparto_dp_utilidad`, `reparto_voraz_utilidad`, `reparto_dif_abs`, `reparto_optimo`; es `null` si N > 20; `reparto_dp_utilidad` es `null` si |S|·B² > 5·10⁷).

**`tiempo.csv`** — columnas `fase, repeticiones, mediana_s, minimo_s, maximo_s` (segundos con 9 decimales). Fases: `carga_json`; `seleccion` y `reparto` (suma de las T rondas); `verificacion`; `certificados`; `seleccion_r<t>` y `reparto_r<t>` por ronda; `pipeline_total`; `referencia_exacta (1 corrida)` (fuerza bruta + DP, una sola vez; no entra en el pipeline). Se ejecuta una corrida de calentamiento sin medir y luego `--repeticiones` corridas; se reporta la mediana (D-11). Los certificados cuestan más que el algoritmo mismo (programa lineal): en el caso de la profesora, 5.2023 ms de 6.6853 ms.

**`traza.md`** — por ronda: disponibles; para cada heurística, tabla por paso (`paso, elegido, ganancia marginal, puntaje, costo acum., f acum.`, y la lista de ganancias de los candidatos factibles, truncada a 10); reparto unidad a unidad (`unidad, nodo, x antes, ganancia marginal, utilidad acum.`); tabla de verificación de restricciones; líneas de los certificados y del exacto. Cierra con la verificación global.

**`traza.csv`** — columnas `ronda, fase, heuristica_o_restriccion, paso, nodo, valor, detalle`. Valores de `fase`: `seleccion` (nodo elegido, `valor` = ganancia, `detalle` con costo y f acumulados), `seleccion_candidato` (ganancia de cada candidato evaluado en ese paso), `reparto` (`valor` = ganancia, `detalle` = x antes y utilidad acumulada), `verificacion` (una fila por restricción; ronda 0 = global) y `certificado`.

### 4.4 Ejemplo ejecutado

Con el comando de la Sección 4.2 (paso 2 y 3, `--seed 7`) se obtuvo (salida real, consola):

```
escrito ejemplo_n6.json (N=6, aristas=15, semilla=7)
Caso ejemplo_n6: N=6 T=2 k=3 B=10 L=12 modo=ambos
  ronda 1: S=['N01', 'N04', 'N06'] f=48.8055 costo=12 reparto={'N01': 3, 'N04': 5, 'N06': 2} u=44.7612
  ronda 2: S=['N01', 'N04', 'N06'] f=48.8055 costo=12 reparto={'N01': 3, 'N04': 5, 'N06': 2} u=44.7612
  suma f=97.6109  suma u=89.5223  pipeline (mediana)=3.366 ms
  restricciones y certificados: TODO CUMPLE
  salida: salida\caso_ejemplo_n6
```
En la ronda 1, `traza.md` muestra que el voraz por ganancia elige N04 (ganancia 38.223000), luego N06 (7.988310) y N01 (2.594150), con costo acumulado 2, 7 y 12 (límite L = 12). Para el caso de la profesora, ver `results/caso_entrada_G2_red_15_nodos/` y la Sección 4 del informe.

---

## 5. Validación

### 5.1 Pruebas (`pytest -q`)

Resultado verificado al escribir este manual: **240 passed** en unos 18 s (Python 3.12.10).

| Archivo | Qué prueba |
|---|---|
| `test_reparto.py` | el voraz coincide con la DP exacta en ≥ 500 instancias (700 en total); restricciones (Σx ≤ B, 0 ≤ x ≤ tope, entero); certificado de dualidad (brecha ≤ 10⁻⁹) |
| `test_funcion_f.py` | f(∅) = 0, monotonía, submodularidad (600 instancias), ganancia incremental = diferencia directa, caso Cobertura Máxima |
| `test_seleccion.py` | restricciones en los tres modos; sin nodos repetidos; razón voraz/exacto ≥ 1 − (1 − 1/k)^k en modo `k` (con hypothesis); certificado LP ≥ óptimo; instancia ajustada D-15 (razones exactas 3/4, 19/27, 2101/3125 para k = 2, 3, 5); contraejemplos (voraz no óptimo, falla de submodularidad, falla con costos); conteo de evaluaciones P y k·N·M; regresión BUG-1; subcomando `ajustada` |
| `test_np_reduccion.py` | la reducción desde Cobertura Máxima: ejemplo 4×5 del informe, instancia negativa, equivalencia CobMax-Dec ⇔ Sel-Dec en la subfamilia M = N, w_ii = 1, a > 0 (60 instancias) |
| `test_caso_profesora.py` | valores de referencia del caso (selección, f, exacto en modo `k`, reparto) re-derivados con el código |
| `test_cli_validacion.py` | 13 JSON inválidos → exit 2 con mensaje; 5 válidos → exit 0; CLI sobre JSON sintéticos |
| `test_smoke.py` | humo: reparto = DP, caso de la profesora cumple restricciones, voraz vs fuerza bruta en una instancia generada, generador determinista, mensajes de validación |

### 5.2 Certificados por ejecución
Cada corrida falla (exit 3) si algún certificado no se cumple: dualidad del reparto (brecha ≤ 10⁻⁹) o cota LP de la selección (cota ≥ f(S)). Para el caso de la profesora: brecha 0 en las tres rondas, cota 151.9871, razón certificada 0.9578.

### 5.2b Instancia ajustada (D-15)
`python -m ada_g2 ajustada [--k 2 3 5]` corre voraz y fuerza bruta sobre la instancia ajustada e imprime la razón exacta (3/4, 19/27, 2101/3125); sale con 0 si coincide con 1 − (1 − 1/k)^k y con 3 si no.

### 5.3 Códigos de salida (D-25)
0 = todo cumple · 2 = entrada inválida (archivo inexistente, JSON mal formado, esquema incumplido) · 3 = falla una restricción o un certificado. El código 3 no está cubierto por una prueba automática aún (no probado).

### 5.4 Razón con el exacto
En el caso de la profesora (modo `ambos`) la razón voraz/óptimo es 1.0000 (`resultado.json`). En el modo `k` es 0.99775 con óptimo 145.9072. Medido por el verifier (3 familias × 250 instancias, modo `k`): razón mínima 0.8885, siempre ≥ 1 − (1 − 1/k)^k; en `costo` 0.8864 y en `ambos` 0.8148, **sin garantía teórica** (R-01).

---

## 6. Límites y advertencias

1. **Saturación del caso (R-02).** El grafo de la profesora es completo con pesos ≥ 0.2: f(S) alcanza 145.5795 de un máximo Σ a = 147.8 (0.9850) y las heurísticas dan valores muy cercanos. El caso discrimina poco; la cota 1 − 1/e se verifica en familias sintéticas.
2. **Sin garantía con cupo y costo a la vez (R-01).** La garantía 1 − (1 − 1/k)^k es solo para el modo `k`. En `ambos` se usa el mejor de tres heurísticas y se certifica a posteriori (razón certificada por LP), pero no hay cota a priori demostrada.
3. **Fuerza bruta solo para N ≤ 20** (`comparar_exacto`, `max_n = 20`; además se corta a los 3 000 000 de visitas). Con N mayor, `comparacion_exacto` es `null` y el tiempo de referencia exacta no se mide.
4. **DP del reparto omitida** si |S|·B² > 5·10⁷ (D-24); entonces `reparto_dp_utilidad`, `reparto_dif_abs` y `reparto_optimo` son `null`. El certificado de dualidad sigue disponible.
5. **BUG-1 corregido.** `select.py` usaba la longitud de `a` (M) como número de candidatos N en `voraz` y `mejor_singleton`; ahora usa `W.shape[0]`. No afectaba al caso de la profesora (M = N). La suite incluye una prueba de regresión.
6. **Reparto pseudo-polinomial en B**: O(N + B log N) es lineal en el valor de B, no en sus bits. Sin topes activos ni fallas, B enorme es costoso (informe, Sección 1.3; el caso continuo con *water-filling* está esbozado, no implementado).
7. **El modelo es una decisión nuestra** (D-01, D-02): el enunciado no define u_i ni f. La profesora puede preferir otras formas.
8. **Nodos y topes:** un nodo con tope restante 0 deja de ser candidato (D-21); si Σ topes < B el ciclo termina sin gastar todo (D-28).
9. **Pendiente en esta entrega:** barrido experimental por tamaños y la estimación empírica de T(n) (T13); deducción completa de T(n) con constantes; variantes (fallas q > 0 con barrido, nodos relacionados). El informe se compila en letX (D-20).
10. **Errores de ids repetidos:** un id repetido en `nodos` genera además errores en cascada de "arista a nodo inexistente" que pueden ocultar otros mensajes (mejora pendiente en `io.py`).

---

## 6b. Errores conocidos y alcance (solución base frente a variantes)

**Errores conocidos:** ninguno abierto en la lógica. BUG-1 (la selección fallaba con N ≠ M en la familia general) se corrigió y tiene prueba de regresión. Pendientes menores: mensajes en cascada con ids repetidos (punto 10 arriba) y el código de salida 3 de `run`, sin prueba automática.

Esta versión (`v0.1-primera-entrega`) es la **solución base** y **no es la solución final**:

| Componente | Estado en esta versión |
|---|---|
| Parte 1, reparto voraz exacto con montículo y topes por nodo | implementado, probado contra DP exacta y certificado por dualidad |
| Parte 2, selección voraz (modos `k`, `costo`, `ambos`), fuerza bruta de referencia y cota LP a posteriori | implementado y probado |
| T rondas en cadena (Parte 2 → Parte 1) con topes que bajan entre rondas | implementado (q = 0 en el caso de la profesora, D-07) |
| Variante (a), costos de participación con garantía demostrada (Khuller et al.) | **parcial**: mejor-de-3, sin garantía para cupo + costo (R-01) ni enumeración parcial |
| Variante (b), fallas con probabilidad q y comparación de políticas con ≥ 100 semillas | **parcial**: `--q` y `--politica` existen; falta el experimento comparativo |
| Variante (c), nodos relacionados (aditivo y competencia) | **no desarrollada** |
| Validación experimental (≥ 5 tamaños, gráfica tiempo vs n contra T(n)) | **no desarrollada** (tarea T13) |

---

## 7. Identificación y enlace

- **Curso:** Análisis y Diseño de Algoritmos 2026-B · **Profesora:** Luz Enith Guerrero · **Universidad de Caldas**
- **Subproyecto 2 (Grupo 2):** Reparto de presupuesto y selección de participantes
- **Integrante:** Juan Esteban Guzmán Henao (trabajo individual)
- **Repositorio:** https://github.com/GuzGuz0208/ADA · rama `main` · etiqueta `v0.1-primera-entrega`
- **Informe:** `informe/main.tex` (+ `informe/INFORME.md`) · **Resultados:** `results/caso_entrada_G2_red_15_nodos/`
