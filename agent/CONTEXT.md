# CONTEXT — estado vivo del proyecto

> Reescribir en cada checkpoint (no acumular; ≤ ~150 líneas). Historia detallada: `agent/CHANGELOG.md`.

**Última actualización:** 2026-11-05 22:32 (America/Bogota) · scribe (claude-haiku-5.5) registrando C-0009 (report-writer en T07; orquestador en T08, parcial)
**Testigo:** scribe (claude-haiku-5.5), registro de C-0009

## Qué es
Proyecto semestral ADA 2026-B (profesora Luz Enith Guerrero). **Grupo 2 · Subproyecto 2 "Reparto de presupuesto y selección de participantes"**: Parte 1 reparto óptimo (voraz por ganancia marginal, exacto, O(N+B log N)); Parte 2 selección de k nodos (NP-difícil por reducción desde Cobertura Máxima; voraz con garantía 1−(1−1/k)^k, ≥ 1−1/e). **Proyecto individual: Juan Esteban Guzmán Henao.** Repo: `C:\Users\danna\OneDrive\Documentos\ADA`, rama `main`, remoto `origin` = https://github.com/GuzGuz0208/ADA.git (**sin push**). Guía de estudio del usuario: https://claude.ai/artifact/1n9ukzYACjPEQGKqmvq8h1 (D-16).
**Fecha crítica:** primera entrega **2026-11-06** (4 productos: informe de formalización + NP-dureza, repo con solución base, manual técnico, ejecución del caso JSON con resultado/tiempo/traza). Detalle en `agent/SPEC.md` §1.

## Estado por producto
| Producto | Estado | Dónde |
|---|---|---|
| Informe (formalización + NP-dureza + optimalidad + caso) | 🔄 contenido listo (secciones 01–04, cifras reales, C-0009); **sin compilar**. Falta compilar en letX (D-20) y confirmar la portada | `informe/main.tex`, `informe/secciones/01…04`, `informe/referencias.tex`, `informe/INFORME.md` (espejo) |
| Repositorio / código base | ✅ código + pruebas: **239 passed**. BUG-1 corregido (C-0008). README reescrito (C-0009) | `src/ada_g2/`, `tests/`, `README.md` |
| Ejecución del caso de la profesora | ✅ T06 (C-0008): exit 0, TODO CUMPLE | `results/caso_entrada_G2_red_15_nodos/` |
| Manual técnico | ✅ redactado (T07, C-0009); contrastar con guías de la profesora (D-30) | `manual/MANUAL_TECNICO.md` |
| Experimentos | 🔄 T12 razón mínima medida; ⬜ T13 (no creado `results/experimentos/`) | `results/` |
| Memoria compartida y hooks | ✅ T00, hooks probados en Windows, config en `.claude/` | `agent/`, `.claude/`, `agent/hooks/` |

## Entorno (comprobado en T00, C-0006, C-0008 y C-0009)
- Python 3.12.10 (`python` y `py`); git 2.56. `.venv` con `requirements.txt` (pytest 9.2.0, numpy 2.5.4, scipy 1.18.1, matplotlib 3.11.2, hypothesis 6.170.14) y `pip install -e .` (ada_g2 0.1.0).
- Pruebas: `.venv/Scripts/python -m pytest -q` → **239 passed** (17.32 s en C-0008; 16.34 s en el informe de report-writer, C-0009). Antes del arreglo BUG-1: 198 passed, 1 xfailed.
- `core.hooksPath = agent/hooks`; `agent/hooks/pre-commit` (exige CHANGELOG si el commit toca fuera de `agent/` y `.claude/`; CHANGELOG solo-añadir).
- Hooks de Claude Code: PostToolUse (comando `python`, `$CLAUDE_PROJECT_DIR`) escribe en `agent/log/auto_changes.log`; Stop (`check_logged.py`) bloquea con cambios sin registrar.
- Hora: en Git Bash `TZ=America/Bogota date` devuelve **UTC**; usar `python -c` con zoneinfo.
- pandoc y LaTeX **no** instalados: los agentes no compilan el informe; el usuario lo compila en letX (D-20).

## Hecho hasta ahora
- Modelo y supuestos: D-01 u_i=a_i·ln(1+x) · D-02 f cobertura probabilística · D-03 cupo k=5 y costo≤24 a la vez · D-04 primera entrega + extras · D-05…D-13 supuestos · D-14…D-20 certificados, instancia ajustada, guía, avisos, remoto, entorno de informe, formato PDF · D-21…D-25 código · D-26…D-29 correcciones de SPEC (C-0007) · D-30 estructura de README y manual (C-0009).
- T00 (C-0005) y T04 base (C-0006): reparto con montículo y topes; selección voraz (k/costo/ambos, mejor-de-3); exacto; certificados D-14; rondas con q y políticas; CLI `run`/`generar`.
- T01, T02, T03 (C-0007): 11 correcciones a SPEC §4-5; secciones 01–03 del informe.
- T05 ✅, T06 ✅, W1 ✅, W2 ✅ (C-0008). Verifier: reparto = DP (700 instancias), brecha de dualidad ≤1e-9 (700), f monótona y submodular (600), selección con restricciones y voraz ≥ 1−(1−1/k)^k en modo k (2250), óptimo ≤ cota LP (2250), reducción NP (tabla 4×5, instancia negativa, equivalencia en subfamilia simétrica, 60 instancias), caso de la profesora (SPEC §6), CLI (13 JSON inválidos → exit 2; 5 válidos → exit 0).
- **Caso de la profesora (T06):** R1=R2 S={N09,N11,N13,N14,N15} f=145.5795 costo 23 reparto 7/5/5/7/6 u=88.5640; R3 reparto N09:4 N11:8 N13:8 N14:4 N15:6 u=85.6108; Σf=436.7386, Σu=262.7387. Pipeline mediana 6.685 ms; exacto de referencia 51.2 ms.
- **T07 ✅ (C-0009):** README (ejemplo `generar --n 6 --seed 7`: Σf=97.6109, Σu=89.5223), `manual/MANUAL_TECNICO.md`, sección 04 del informe; marcadores `[RESULTADO-T06]`/`[RESULTADO-T12]` sustituidos.
- **T08 parcial (C-0009):** chequeo estructural del LaTeX OK (entornos, llaves, $, \ref/\label, \cite/\bibitem, \input 01–04); grep de cifras coincide entre informe, INFORME.md, README, manual, `resultado.json` y `traza.md`. **No compilado.**
- **BUG-1 (C-0008):** `select.py` usaba `len(a)` (M) como N en `voraz` y `mejor_singleton`; corregido con `W.shape[0]`. No afectaba al caso (M=N); sí a la familia general y a la reducción.
- Razón mínima medida (C-0008, sin garantía en costo/ambos, R-01): modo k 0.8885 (familia rala); costo 0.8864; ambos 0.8148 (familia rala, mínima global).
- Commits: C-0001…C-0004 en `5054456`; C-0005 en `35db17c`; C-0006 en `5f98f59`; C-0007 en `db0c194`; C-0008 en `27b71f4`; C-0009 en el commit siguiente (hash en C-0010).

## Siguiente paso inmediato
1. **Usuario (T08):** compilar `informe/` en letX (pdfLaTeX; subir `main.tex`, `secciones/` y `referencias.tex`) y confirmar que la portada dice "Manizales, 6 de noviembre de 2026".
2. Solo después de (1): `git tag v0.1-primera-entrega` sobre HEAD (si no hubo cambios en `informe/` posteriores) y marcar el ítem 5 de SPEC §8. No crear el tag antes.
3. Después, P1 (en este orden): T13 experimentos E1–E3 (`results/experimentos/`); T10 deducción formal completa de T(n); T14 guía de estudio (D-16: reemplazar PRELIMINAR; 0.9578 ya reproducido; 0.7037 = 19/27 y 0.67232 = 2101/3125).

Cada bloque de cambios: `scribe` registra antes de cerrar el turno (Regla 0).

## Pendiente del informe (theorist, T10/T11)
- Conteo del voraz (k·N·M, P = kN−k(k−1)/2): incorporado en `informe/secciones/03_optimalidad_y_cota.tex` (C-0009).
- T10: costeo completo de la fuerza bruta y sumatorias contra conteo real.
- T11: water-filling sigue en esbozo.

## Pendiente del usuario
- **(a) Compilar** `informe/` en letX (pdfLaTeX). Sin TeX local no se puede verificar que compile.
- **(b) Confirmar** "Manizales, 6 de noviembre de 2026" en la portada.
- **(c) Q-02:** visibilidad del repo (público o invitación a la profesora) y si acepta trabajo individual.
- **(d) Q-06 (`agent/DECISIONS.md`):** ¿la instancia ajustada D-15 entra en el generador? Default: no, queda en el test.
- **(e) D-30:** contrastar README y manual con las guías de la profesora (PDF/DOCX), que los agentes no pudieron leer.
- **(f) git push:** solo cuando el usuario lo pida (D-18).
- Q-01: confirmar con la profesora qué se entrega exactamente mañana.
- R-03: decidir si mover el repo fuera de OneDrive (advertencias CRLF; `.git` en OneDrive).

## Bloqueos
- Ninguno duro. Informe: compilación solo en letX (sin TeX local); README y manual sin contrastar con las guías (D-30).
- No bloqueante: `io.py` — un id de nodo repetido genera cascada de "arista a nodo inexistente", y ese error enmascara el de peso. Mejorar mensajes cuando se toque el módulo (sin asignar).
- No probado todavía: exit 3 de la CLI; instancias aleatorias N>9; tiempos y T(n) (T13).

## NO hacer
- No `git push` sin que el usuario lo pida; no versionar `docs/`; no `--no-verify`; no `reset --hard`, `clean` ni force-push; no inventar citas ni números; no hardcodear el caso de la profesora; no reescribir entradas del CHANGELOG; no crear el tag antes de la compilación en letX; no afirmar garantía teórica para cupo+costo a la vez (R-01).
