# ADA 2026-B — Grupo 2 · Proyecto Red
## Subproyecto 2: Reparto de presupuesto y selección de participantes

## 1. Identificación

| Campo | Valor |
|---|---|
| Curso | Análisis y Diseño de Algoritmos, 2026-B |
| Profesora | Luz Enith Guerrero |
| Universidad | Universidad de Caldas (Facultad de Inteligencia Artificial e Ingenierías) |
| Subproyecto | 2 — Reparto de presupuesto y selección de participantes (Grupo 2) |
| Integrante | Juan Esteban Guzmán Henao (trabajo individual) |
| Repositorio | https://github.com/GuzGuz0208/ADA |
| Rama | `main` |
| Versión entregada | `v0.1-primera-entrega` (versión del paquete: 0.1.0) |
| Entrega | Primera entrega, 2026-11-06 |

> Pendiente de confirmar por el integrante: que el repositorio sea accesible para la profesora (público o por invitación) y que la etiqueta `v0.1-primera-entrega` esté creada al entregar.

## 2. Qué resuelve

Una red de N nodos entrena un modelo durante T rondas. En cada ronda se resuelven dos problemas encadenados (Parte 2 y luego Parte 1):

- **Parte 2 — selección de participantes (NP-difícil).** Elegir un subconjunto S de nodos con |S| ≤ k y Σ costo ≤ L que maximice la utilidad conjunta f(S) = Σ_j a_j·[1 − Π_{i∈S}(1 − w_ij)]. Se demuestra NP-dureza por reducción desde Cobertura Máxima (informe, Sección 2). Algoritmo: voraz por ganancia marginal; con garantía 1 − (1 − 1/k)^k ≥ 1 − 1/e **solo en el modo `k`** (cupo sin costo). Con cupo y costo a la vez no se afirma garantía teórica (R-01); se certifica a posteriori.
- **Parte 1 — reparto del presupuesto de ruido (exacto, polinomial en N y pseudo-polinomial en B).** Repartir B unidades enteras entre los participantes para maximizar Σ a_i·ln(1 + x_i), con tope por nodo. Algoritmo voraz con montículo, T(N, B) = O(N + B log N), óptimo (Teorema de optimalidad, informe Sección 3.1).

Supuestos de modelado (D-01…D-13) en `agent/DECISIONS.md` y en la Sección 1.5 del informe. Los principales: u_i(x) = a_i·ln(1+x) (D-01); f de cobertura probabilística con w_ii = 1 (D-02); selección con cupo y costo a la vez (D-03); grafo no dirigido (D-10); q = 0 en el caso de la profesora (D-07); desempate por menor índice (D-12).

## 3. Entorno y dependencias

- **Python ≥ 3.10** (probado con Python 3.12.10 en Windows 11).
- Dependencias de ejecución (`pyproject.toml`): `numpy>=1.26`, `scipy>=1.11`.
- Dependencias de desarrollo y pruebas (`requirements.txt`): `numpy>=1.26`, `scipy>=1.11`, `matplotlib>=3.8`, `pytest>=8.0`, `hypothesis>=6.100`.
- Versiones con las que se probó el código (entorno `.venv`): pytest 9.2.0, numpy 2.5.4, scipy 1.18.1, matplotlib 3.11.2, hypothesis 6.170.14.

## 4. Instalación

Desde la raíz del repositorio.

**Windows (PowerShell o Git Bash):**
```
python -m venv .venv
.venv\Scripts\activate          # en Git Bash: source .venv/Scripts/activate
pip install -r requirements.txt
pip install -e .
```

**Linux / macOS:**
```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

`pip install -e .` registra el paquete `ada_g2` (carpeta `src/`) para poder usar `python -m ada_g2` desde cualquier directorio.

## 5. Ejecución del caso de la profesora

```
python -m ada_g2 run --input project-docs/entrada_G2_red_15_nodos.json --out results/
```

Opciones (`python -m ada_g2 run --help`):

| Opción | Valores | Por defecto | Significado |
|---|---|---|---|
| `--input` | ruta | (obligatoria) | JSON de entrada con el esquema de la profesora |
| `--out` | carpeta | (obligatoria) | se crea `<out>/caso_<nombre del JSON>/` |
| `--modo` | `ambos`, `k`, `costo` | `ambos` | restricciones de la selección: cupo y costo, solo cupo, solo costo (D-03) |
| `--seed` | entero | 20261105 | semilla (solo afecta si `--q > 0`) |
| `--repeticiones` | entero | 5 | repeticiones para la mediana de tiempos (más 1 de calentamiento) |
| `--q` | [0, 1) | 0.0 | probabilidad de falla por nodo y ronda (D-07: 0 en el caso base) |
| `--politica` | `concentrado`, `uniforme` | `concentrado` | tope de gasto por ronda: todo el restante, o `ceil(restante/(T−t+1))` (D-22) |

Cada ejecución escribe en `<out>/caso_<nombre>/`:

| Archivo | Contenido |
|---|---|
| `resultado.json` | selección, f, costo, reparto, utilidad, verificación, certificados y comparación con el exacto, por ronda; totales |
| `tiempo.csv` | mediana, mínimo y máximo (s) por fase, con `time.perf_counter` |
| `traza.md` | traza legible: elecciones del voraz con su ganancia marginal, reparto unidad a unidad, verificación de restricciones |
| `traza.csv` | la misma traza, una fila por evento |

### Códigos de salida (D-25)

| Código | Significado |
|---|---|
| 0 | todo cumple (restricciones y certificados) |
| 2 | entrada inválida (archivo inexistente, JSON mal formado o esquema incumplido; el mensaje lista todos los problemas con su ruta) |
| 3 | falla alguna restricción o algún certificado (ver `resultado.json`) |

### Resultados esperados del caso de la profesora

Salida real de la ejecución entregada (`results/caso_entrada_G2_red_15_nodos/`; semilla 20261105, modo `ambos`):

| Ronda | Selección | f | Costo | Reparto N09/N11/N13/N14/N15 | Utilidad |
|---|---|---|---|---|---|
| 1 | N09, N11, N13, N14, N15 | 145.5795 | 23 | 7 / 5 / 5 / 7 / 6 | 88.5640 |
| 2 | N09, N11, N13, N14, N15 | 145.5795 | 23 | 7 / 5 / 5 / 7 / 6 | 88.5640 |
| 3 | N09, N11, N13, N14, N15 | 145.5795 | 23 | 4 / 8 / 8 / 4 / 6 | 85.6108 |

- Σ f = 436.7386 · Σ utilidad = 262.7387 · `todo_cumple = true` · código de salida 0.
- Certificado del reparto: brecha de dualidad 0 en las tres rondas.
- Certificado de la selección: cota superior del óptimo 151.9871, razón certificada 0.9578.
- Exacto por fuerza bruta (modo `ambos`): razón voraz/óptimo 1.0000 (3 893 subconjuntos evaluados). En modo `k`: óptimo 145.9072, razón 0.99775 (`tests/test_caso_profesora.py`).
- Tiempo del pipeline completo (mediana de 5): 6.6853 ms; referencia exacta (1 corrida): 51.2363 ms (`tiempo.csv`).
- **Advertencia de saturación (R-02):** el grafo es completo con pesos ≥ 0.2, f se satura (145.5795 de Σ a = 147.8, es decir 0.9850) y el caso discrimina poco entre selecciones. Detalle en el informe, Sección 4.

## 6. Ejemplo pequeño (generar y ejecutar)

El generador crea instancias con el mismo esquema JSON, deterministas por semilla (`python -m ada_g2 generar --help`: `--n`, `--rondas`, `--k`, `--B`, `--L`, `--seed`, `--densidad`, `--out`).

```
python -m ada_g2 generar --n 6 --rondas 2 --k 3 --B 10 --L 12 --seed 7 --out ejemplo_n6.json
python -m ada_g2 run --input ejemplo_n6.json --out salida/ --repeticiones 3
```

Salida real de esas dos órdenes (los tiempos cambian de una máquina a otra; lo demás es determinista):

```
escrito ejemplo_n6.json (N=6, aristas=15, semilla=7)
Caso ejemplo_n6: N=6 T=2 k=3 B=10 L=12 modo=ambos
  ronda 1: S=['N01', 'N04', 'N06'] f=48.8055 costo=12 reparto={'N01': 3, 'N04': 5, 'N06': 2} u=44.7612
  ronda 2: S=['N01', 'N04', 'N06'] f=48.8055 costo=12 reparto={'N01': 3, 'N04': 5, 'N06': 2} u=44.7612
  suma f=97.6109  suma u=89.5223  pipeline (mediana)=3.366 ms
  restricciones y certificados: TODO CUMPLE
  salida: salida\caso_ejemplo_n6
```
Código de salida: 0. Con un archivo inexistente (`--input noexiste.json`) la salida es `ERROR: no existe el archivo de entrada: noexiste.json` y el código es 2.

## 7. Pruebas

```
pytest -q
```
Resultado en la verificación de esta entrega (Windows 11, Python 3.12.10): `239 passed` (tiempo de unos 16 s). Qué cubren: reparto del voraz = programación dinámica exacta; certificado de dualidad; monotonía y submodularidad de f; selección factible en los tres modos; razón voraz/exacto ≥ 1 − (1 − 1/k)^k en modo `k`; instancia ajustada de la cota; reducción de NP-dureza (ejemplo del informe, equivalencia en una subfamilia); caso de la profesora; validación de entradas inválidas (exit 2) y CLI. Detalle en `manual/MANUAL_TECNICO.md`, Sección 6.

## 8. Estructura de carpetas

| Ruta | Contenido |
|---|---|
| `src/ada_g2/` | código: `io.py`, `model.py`, `select.py`, `allocate.py`, `rounds.py`, `certificates.py`, `exact.py`, `generator.py`, `trace.py`, `cli.py` |
| `tests/` | pruebas con pytest y hypothesis |
| `results/` | salidas por caso (`caso_<nombre>/`: resultado, tiempo, traza) |
| `informe/` | informe técnico en LaTeX (`main.tex`, `secciones/`, `referencias.tex`) y espejo `INFORME.md` |
| `manual/` | `MANUAL_TECNICO.md` |
| `project-docs/` | enunciados y JSON de la profesora (solo lectura) |
| `agent/`, `prompts/` | memoria de trabajo de los agentes de IA y sus prompts (ver `AGENTS.md`) |
| `docs/` | material de consulta local (no versionado) |

## 9. Limitaciones conocidas

- La Parte 2 es NP-difícil: el código es un algoritmo de aproximación; no hay garantía teórica con cupo y costo a la vez (R-01).
- La fuerza bruta de referencia solo se ejecuta con N ≤ 20; la DP de referencia del reparto se omite si |S|·B² > 5·10⁷ (D-24).
- El caso de la profesora satura f (R-02); la validación de la cota 1 − 1/e usa familias sintéticas.
- Validación experimental por tamaños (T13) y la deducción completa de T(n) aún no entregadas. El informe se compila en letX (D-20); el PDF no se genera en este repositorio.
