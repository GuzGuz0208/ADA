# CONTEXT — estado vivo del proyecto

> Reescribir en cada checkpoint (no acumular; ≤ ~150 líneas). Historia detallada: `agent/CHANGELOG.md`.

**Última actualización:** 2026-11-05 23:09 (America/Bogota) · scribe (claude-haiku-5.5) registrando C-0012 (cierre de la primera entrega: PDF finales y tag `v0.1-primera-entrega`)
**Testigo:** scribe (claude-haiku-5.5), registro de C-0012

## Qué es
Proyecto semestral ADA 2026-B (profesora Luz Enith Guerrero). **Grupo 2 · Subproyecto 2 "Reparto de presupuesto y selección de participantes"**: Parte 1 reparto óptimo (voraz por ganancia marginal, exacto, O(N+B log N)); Parte 2 selección de k nodos (NP-difícil por reducción desde Cobertura Máxima; voraz con garantía 1−(1−1/k)^k, ≥ 1−1/e). **Proyecto individual: Juan Esteban Guzmán Henao.** Repo: `C:\Users\danna\OneDrive\Documentos\ADA`, rama `main`, remoto `origin` = https://github.com/GuzGuz0208/ADA.git (**público** según el usuario, 2026-11-05; push autorizado para C-0012, D-35). Guía de estudio del usuario: https://claude.ai/artifact/1n9ukzYACjPEQGKqmvq8h1 (D-16).
**Primera entrega (2026-11-06): P0 COMPLETO.** Cuatro productos: informe de formalización + NP-dureza, repo con solución base, manual técnico, ejecución del caso JSON con resultado/tiempo/traza. Detalle en `agent/SPEC.md` §1 y §8.

## Estado por producto
| Producto | Estado | Dónde |
|---|---|---|
| Informe (formalización + NP-dureza + optimalidad + caso) | ✅ **compilado en letX** por el usuario: `informe.pdf` 21 págs., incluye el cambio de la sección 3 (`instancia_ajustada`); sin "??" (C-0012) | `informe/main.tex`, `informe/secciones/01…04`, `informe/referencias.tex`, `informe/INFORME.md` (espejo), `informe/informe.pdf` |
| Repositorio / código base | ✅ **240 passed** (C-0010). Generador `instancia_ajustada` y subcomando `ajustada`; lectores PDF/DOCX; README con §10 (alcance) | `src/ada_g2/`, `tests/`, `README.md`, `tools/leer_docs.py` |
| Ejecución del caso de la profesora | ✅ T06 (C-0008): exit 0, TODO CUMPLE | `results/caso_entrada_G2_red_15_nodos/` |
| Manual técnico | ✅ **compilado en letX** por el usuario: `manual_tecnico.pdf` 13 págs., figura TikZ compiló, portada correcta, sin "??" (C-0012). Espejo Markdown: `MANUAL_TECNICO.md` | `manual/` |
| Experimentos | 🔄 T12 razón mínima medida; ⬜ T13 (no existe `results/experimentos/`) | `results/` |
| Memoria compartida y hooks | ✅ T00, hooks probados en Windows, config en `.claude/` | `agent/`, `.claude/`, `agent/hooks/` |

## Entorno (comprobado en T00, C-0006, C-0008 a C-0012)
- Python 3.12.10 (`python` y `py`); git 2.56. `.venv` con `requirements.txt` (pytest 9.2.0, numpy 2.5.4, scipy 1.18.1, matplotlib 3.11.2, hypothesis 6.170.14) y `requirements-dev.txt` (pdfplumber 0.11.10, pypdf 6.21.4, python-docx); `pip install -e .` (ada_g2 0.1.0).
- Pruebas: `.venv/Scripts/python -m pytest -q` → **240 passed** (17.18 s, C-0010; ejecutado por el orquestador).
- Lectura de documentos: `python tools/leer_docs.py <archivo.pdf|.docx> --out <carpeta>` extrae texto a `.txt` (D-31; requiere `requirements-dev.txt`).
- `core.hooksPath = agent/hooks`; `agent/hooks/pre-commit` (exige CHANGELOG si el commit toca fuera de `agent/` y `.claude/`; CHANGELOG solo-añadir).
- Hooks de Claude Code: PostToolUse (comando `python`, `$CLAUDE_PROJECT_DIR`) escribe en `agent/log/auto_changes.log`; Stop (`check_logged.py`) bloquea con cambios sin registrar.
- Hora: en Git Bash `TZ=America/Bogota date` devuelve **UTC**; usar `py` con zoneinfo (`America/Bogota`).
- pandoc y LaTeX **no** instalados localmente: los PDF se compilan en letX por el usuario (D-20).

## Hecho hasta ahora
- Modelo y supuestos: D-01 u_i=a_i·ln(1+x) · D-02 f cobertura probabilística · D-03 cupo k=5 y costo≤24 a la vez · D-04 primera entrega + extras · D-05…D-13 supuestos · D-14…D-20 certificados, instancia ajustada, guía, avisos, remoto, entorno de informe, formato PDF · D-21…D-29 código y correcciones de SPEC · D-30/D-31 estructura de README y manual, lectura de guías · D-32 instancia ajustada en el código (resuelve Q-06) · D-33 manual en LaTeX además del Markdown · D-34 tag tras compilar PDF (cumplida, C-0012) · D-35 push y tag autorizados por el usuario (C-0012).
- T00 (C-0005) y T04 base (C-0006): reparto con montículo y topes; selección voraz (k/costo/ambos, mejor-de-3); exacto; certificados D-14; rondas con q y políticas; CLI `run`/`generar`.
- T01, T02, T03 (C-0007): 11 correcciones a SPEC §4-5; secciones 01–03 del informe.
- T05 ✅, T06 ✅, W1 ✅, W2 ✅ (C-0008). Verifier: reparto = DP (700 instancias), brecha de dualidad ≤1e-9 (700), f monótona y submodular (600), selección con restricciones y voraz ≥ 1−(1−1/k)^k en modo k (2250), óptimo ≤ cota LP (2250), reducción NP (tabla 4×5, instancia negativa, equivalencia en subfamilia simétrica, 60 instancias), caso de la profesora (SPEC §6), CLI (13 JSON inválidos → exit 2; 5 válidos → exit 0).
- **BUG-1 (C-0008):** `select.py` usaba `len(a)` (M) como N; corregido con `W.shape[0]`. No afectaba al caso (M=N); sí a la familia general y a la reducción.
- **Caso de la profesora (T06):** R1=R2 S={N09,N11,N13,N14,N15} f=145.5795 costo 23 reparto 7/5/5/7/6 u=88.5640; R3 reparto N09:4 N11:8 N13:8 N14:4 N15:6 u=85.6108; Σf=436.7386, Σu=262.7387; razón certificada 0.9578. Pipeline mediana 6.685 ms; exacto de referencia 51.2 ms.
- **Instancia ajustada (W3, C-0010):** `python -m ada_g2 ajustada` → k=2,3,5: 3/4, 19/27, 2101/3125 (exit 0; cota alcanzada exactamente).
- **T07 ✅ y T08 ✅ (C-0009 a C-0012):** README, `manual/MANUAL_TECNICO.md` y `manual/manual_tecnico.tex`; informe 01–04; PDF finales compilados en letX (C-0012); checklist SPEC §8 completo.
- Razón mínima medida (C-0008, sin garantía en costo/ambos, R-01): modo k 0.8885 (familia rala); costo 0.8864; ambos 0.8148 (familia rala, mínima global).
- Commits: C-0001…C-0004 en `5054456`; C-0005 en `35db17c`; C-0006 en `5f98f59`; C-0007 en `db0c194`; C-0008 en `27b71f4`; C-0009 en `4376f41`; C-0010 en `730c8fa`; C-0011 en `72cca80`; C-0012 = commit que contiene esta entrada (`git log -1`), con tag `v0.1-primera-entrega`.

## Siguiente paso inmediato
**Sesión nueva (P1, rigor extra).** Primera acción: T13 (experimenter). Leer en `agent/SPEC.md` los parámetros de E1–E3 y E5 (≥5 tamaños de n), escribir el script de experimentos (ubicación a decidir y registrar en `agent/DECISIONS.md`), ejecutarlo con `.venv/Scripts/python` con semillas fijas y guardar CSV + PNG en `results/experimentos/`. Antes y después: `.venv/Scripts/python -m pytest -q`.

Orden P1 después de T13:
1. T10 (theorist): deducción formal completa de T(n) con costeo de la fuerza bruta y sumatorias verificadas contra conteo real (`informe/secciones/03_optimalidad_y_cota.tex`).
2. T11 (theorist): water-filling, de esbozo a demostración.
3. T14 (report-writer): guía de estudio (D-16): reemplazar toda cifra PRELIMINAR; ya reproducidos 0.9578, 19/27 y 2101/3125; completar §8 con rutas reales.

Cada bloque de cambios: `scribe` registra antes de cerrar el turno (Regla 0).

## Pendiente del usuario
- **(a)** Q-02: ¿la profesora acepta trabajo individual y sustentación sin pareja? (la visibilidad del repo ya está resuelta: repo público).
- **(b)** Q-01: confirmar con la profesora qué se entrega exactamente.
- **(c)** R-03: decidir si mover el repo fuera de OneDrive (advertencias CRLF; `.git` en OneDrive).

## Bloqueos
- Ninguno duro para P0.
- No probado todavía: exit 3 de `ajustada` y de la CLI `run`; instancias aleatorias N>9; tiempos y T(n) (T13).
- Visibilidad pública del repo: declarada por el usuario; la IA no la comprobó desde fuera.
- No bloqueante: `io.py` — un id de nodo repetido genera cascada de "arista a nodo inexistente", y ese error enmascara el de peso. Sin asignar.

## NO hacer
- No `git push` sin pedido explícito del usuario (D-18; D-35 cubre solo el push de la primera entrega).
- No mover ni recrear `v0.1-primera-entrega` (ya apunta al commit de C-0012).
- No versionar `docs/`; no `--no-verify`; no `reset --hard`, `clean` ni force-push.
- No inventar citas ni números; no hardcodear el caso de la profesora; no reescribir entradas del CHANGELOG.
- No afirmar garantía teórica para cupo+costo a la vez (R-01).
