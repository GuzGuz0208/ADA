# TASKS — tablero de trabajo

Estados: ⬜ pendiente · 🔄 en curso · ✅ hecha · ⛔ bloqueada. Al cambiar un estado, anotar fecha y agente en la columna Notas y registrar en CHANGELOG (Regla 0).
Rol/modelo: ver `agent/ROLES.md`. Prioridad: **P0** primera entrega (2026-11-06) · **P1** rigor extra · **P2** variantes.

## Fase 0 — Arranque (hacer primero)
| ID | Tarea | Pri | Rol | Depende | Estado | Criterio de aceptación / Notas |
|---|---|---|---|---|---|---|
| T-SC | Andamiaje de memoria compartida, hooks, subagentes, SPEC, prompts | P0 | claude (chat) | — | ✅ | Hecho 2026-11-05 por claude-sonnet-5.5 (ver CHANGELOG C-0001) |
| T00 | Arranque en VS Code: **primero** comprobar que la config de Claude Code está en `.claude/` (si `agent/claude-config/` aún tiene archivos: `robocopy agent\claude-config .claude /E /MOVE` y reiniciar la sesión); luego `git init -b main`, `git config core.hooksPath agent/hooks`, `git update-index --chmod=+x agent/hooks/pre-commit`, primer commit (el pre-commit exige CHANGELOG: ya existe C-0001); probar los 2 hooks de Claude (editar un archivo y ver una línea en `agent/log/auto_changes.log`; terminar un turno con un cambio sin registrar y ver el bloqueo); crear `.venv` e instalar `requirements.txt`; comprobar `python --version` (≥3.10) y si hay LaTeX/pandoc; añadir el remoto `git remote add origin https://github.com/GuzGuz0208/ADA.git` (D-18; **sin push** hasta que el usuario lo pida); comprobar `.claude/` ya instalado (robocopy hecho); preguntar al usuario solo Q-03 (Word o PDF) | P0 | orquestador | T-SC | ✅ | `git log` con 1 commit; hooks probados; `pytest --version` OK; D-09 fijada; `git remote -v` muestra origin. **Nota 2026-11-05 claude-opus-5.5 (C-0005):** commit `5054456` (C-0001…C-0004); hooks probados en Windows; `.venv` con requirements; remoto origin sin push; D-20 fijada; Q-03 resuelta |

## Fase 1 — Primera entrega (P0, mañana)
| ID | Tarea | Pri | Rol | Depende | Estado | Criterio de aceptación / Notas |
|---|---|---|---|---|---|---|
| T01 | Revisión independiente de SPEC §4-5: ¿u_i, f, T1…T5 correctos y coherentes con el enunciado? Corregir errores en SPEC con entrada en CHANGELOG | P0 | theorist | T00 | ⬜ | Lista de correcciones o "sin cambios"; cualquier cita dudosa marcada `[VERIFICAR]` |
| T02 | Informe §1 **Formalización** de Parte 1 y Parte 2 por separado (contexto, entradas y tamaño, salidas, objetivo, restricciones, supuestos D-01…D-13) | P0 | theorist → report-writer | T01 | ⬜ | Cumple guía §3; tamaño con (N,B) y (N,k), no una sola variable |
| T03 | Informe §2 **NP-dureza**: Sel-Dec, pertenencia a NP, reducción desde Cobertura Máxima, polinomial O(N·\|U\|), equivalencia ⇒ y ⇐, conclusión | P0 | theorist | T01 | ⬜ | Cumple guía §4; sin saltos; verificada por el verifier con una instancia pequeña a mano y por código |
| T04 | Código base en `src/ada_g2/`: `io` (carga/validación del JSON), `model` (u_i, f, τ=O(M) con R_j), `allocate` (montículo + topes), `select` (voraz: modos `k`, `costo`, `ambos`; mejor-de-3), `exact` (fuerza bruta), `trace`, `cli` (`run`) | P0 | implementer | T00 | ⬜ | `python -m ada_g2 run --input project-docs/entrada_G2_red_15_nodos.json --out results/` corre sin editar código; desempates D-12; sin constantes del caso en el código |
| T05 | Pruebas: reparto = DP exacto (hypothesis, ≥500 casos pequeños); f monótona y submodular (propiedad); restricciones respetadas; voraz ≥ (1−1/e)·exacto en la familia 0/1; valores SPEC §6 | P0 | verifier | T04 | ⬜ | `pytest -q` verde; informe de qué se probó y qué no |
| T06 | **Ejecutar el caso de la profesora** → `results/caso_G2_15_nodos/`: `resultado.json`, `tiempo.csv`, `traza.md/csv` (selección, ganancias marginales, reparto, verificación de restricciones) por ronda | P0 | implementer + verifier | T04, T05 | ⬜ | Cumple guía "Específico G2"; identificado por caso; reproducible con semilla |
| T07 | `README.md` (identificación, Python, dependencias, ejemplo pequeño, resultados esperados) + `manual/MANUAL_TECNICO.md` (guía §6) | P0 | report-writer | T06 | ⬜ | Otra persona puede reproducir sin preguntar |
| T08 | Revisión de **consistencia** (informe = repo = manual = resultados), checklist de SPEC §8, tag `v0.1-primera-entrega`, exportar informe a PDF/DOCX | P0 | verifier + report-writer | T02, T03, T06, T07 | ⬜ | Checklist SPEC §8 todo marcado |

## Fase 2 — Rigor extra (P1)
| ID | Tarea | Pri | Rol | Depende | Estado | Notas |
|---|---|---|---|---|---|---|
| T10 | Deducción formal de T(n) (costeo línea a línea, estilo `STYLE_PROFESORA`) para reparto, voraz de selección y fuerza bruta | P1 | theorist | T04 | ⬜ | Tablas de costeo + sumatorias resueltas |
| T11 | Demostración completa de optimalidad (intercambio) con topes + discusión pseudo-polinomial y water-filling | P1 | theorist | T01 | ⬜ | SPEC T1 expandido y verificado contra DP |
| T12 | Verificación empírica de 1−1/e vs fuerza bruta (E4) con familias sintéticas | P1 | verifier + experimenter | T05 | ⬜ | Razón mínima observada ≥ 0.632 |
| T13 | Experimentos E1–E3 y E5, ≥5 tamaños, gráficas tiempo vs n con ajuste a T(n) | P1 | experimenter | T04 | ⬜ | CSV + PNG en `results/experimentos/` |
| T14 | **Guía de estudio para la sustentación** (45 %): el Claude Doc ya existe (D-16, https://claude.ai/artifact/1n9ukzYACjPEQGKqmvq8h1). Completar la **§8 (mapa del código)** con archivos/funciones reales y reemplazar toda cifra marcada PRELIMINAR por la salida del código final (R-06). Si algo del código contradice la guía, manda el código | P1 | report-writer | todo el código (T04–T06, T10, T11) | ⬜ | Guía sin PRELIMINAR; §8 con rutas reales; el usuario puede defender línea por línea |

## Fase 2b — Certificados y extras de rigor (C-0003, D-14/D-15)
| ID | Tarea | Pri | Rol | Depende | Estado | Criterio de aceptación / Notas |
|---|---|---|---|---|---|---|
| W1 | Certificado de dualidad de la Parte 1 (D-14a) + prueba de que la brecha es 0 en ≥500 instancias vs DP exacta (E5) | P1 | implementer + verifier | T04 | ⬜ | Brecha ≤ 1e-9 en todas; la ejecución falla si el certificado no se cumple |
| W2 | Cota a posteriori de la Parte 2 con LP (D-14b), modos `k`, `costo` y `ambos`; verificar que el óptimo por fuerza bruta nunca la supera | P1 | implementer + verifier | T04 | ⬜ | Óptimo ≤ cota en todas las instancias de prueba |
| W3 | Generador de la instancia ajustada (D-15) y prueba: razón del voraz = 1−(1−1/k)^k para k=2,3,5 (esperado 6/8, 57/81, 10505/15625) | P1 | implementer + verifier | T04 | ⬜ | Razones exactas (fracciones), no aproximadas |
| W4 | Informe HTML de la traza por ronda (nodos, ganancias marginales, reparto, certificados) | P2 | report-writer | T06 | ⬜ | Se abre sin servidor |
| W5 | Voraz perezoso (Minoux) con el mismo resultado y conteo de evaluaciones vs N·k | P2 | implementer | T04 | ⬜ | Mismo S que el voraz normal; menos evaluaciones |

## Fase 3 — Variantes (P2)
| ID | Tarea | Pri | Rol | Depende | Estado | Notas |
|---|---|---|---|---|---|---|
| T20 | Costos de participación + presupuesto: implementar mejor-de-3 / enumeración parcial; citar la versión correcta (R-01 `[VERIFICAR]`); T de la versión elegida | P2 | theorist + implementer | T04, T01 | ⬜ | Razón empírica vs exacto |
| T21 | T rondas con fallas (q), costo O(T·(N·k·τ+N+B log N)), políticas uniforme vs concentrada (≥100 semillas) | P2 | implementer + experimenter | T04 | ⬜ | Gráfica de utilidad total por política y q |
| T22 | Nodos relacionados: caso aditivo (demostrar separabilidad/concavidad) y caso competencia (contraejemplo + heurística con su T) | P2 | theorist + implementer | T04 | ⬜ | Contraejemplo verificado por fuerza bruta |
