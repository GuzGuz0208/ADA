# CONTEXT — estado vivo del proyecto

> Reescribir en cada checkpoint (no acumular; ≤ ~150 líneas). Historia detallada: `agent/CHANGELOG.md`.

**Última actualización:** 2026-11-06 09:17 (America/Bogota) · scribe (claude-haiku-5.5) registrando C-0013 y C-0014 (T10b: mejor caso, peor caso y caso promedio)
**Testigo:** Claude Code (orquestador). El commit único de C-0013 + C-0014 lo hace el orquestador por pedido del usuario; su hash va en C-0015.

## Qué es
Proyecto semestral ADA 2026-B (profesora Luz Enith Guerrero). **Grupo 2 · Subproyecto 2 "Reparto de presupuesto y selección de participantes"**: Parte 1 reparto óptimo (voraz por ganancia marginal, exacto, O(N+B log N)); Parte 2 selección de k nodos (NP-difícil por reducción desde Cobertura Máxima; voraz con garantía 1−(1−1/k)^k, ≥ 1−1/e). **Proyecto individual: Juan Esteban Guzmán Henao.** Repo: `C:\Users\danna\OneDrive\Documentos\ADA`, rama `main`, remoto `origin` = https://github.com/GuzGuz0208/ADA.git (público, según el usuario). Guía de estudio del usuario: https://claude.ai/artifact/1n9ukzYACjPEQGKqmvq8h1 (D-16).
**Primera entrega (2026-11-06): P0 COMPLETO** (tag `v0.1-primera-entrega` sobre `6a25d0f`, C-0012). Detalle en `agent/SPEC.md` §1 y §8.

## Estado por producto
| Producto | Estado | Dónde |
|---|---|---|
| Informe (formalización, NP-dureza, optimalidad, caso) | ✅ entregado en C-0012. C-0014 añade la subsección de casos en 03; **PDF DESACTUALIZADO** (recompilar) | `informe/main.tex`, `informe/secciones/01…04`, `informe/INFORME.md`, `informe/informe.pdf` |
| Análisis por casos (mejor, peor, promedio) | ✅ teórico (T10b, C-0014). Pendiente: PDF en letX | `informe/secciones/03_optimalidad_y_cota.tex` (`sec:casos`), `tests/test_casos_complejidad.py` |
| Código base y pruebas | ✅ `pytest` 273 passed (scribe re-ejecutó en C-0014) | `src/ada_g2/`, `tests/`, `README.md` |
| Caso de la profesora | ✅ T06: exit 0, TODO CUMPLE (reportado en C-0014) | `results/caso_entrada_G2_red_15_nodos/` |
| Manual técnico | ✅ entregado en C-0012. C-0014 añade §3.5; **PDF DESACTUALIZADO** | `manual/MANUAL_TECNICO.md`, `manual/manual_tecnico.tex`, `manual/manual_tecnico.pdf` |
| Experimentos | 🔄 T12 razón mínima medida; ⬜ T13 (no existe `results/experimentos/`) | `results/` |
| Memoria compartida y hooks | ✅ T00; hooks probados en Windows; config en `.claude/` | `agent/`, `.claude/`, `agent/hooks/` |

## Entorno (comprobado en T00 y C-0006 a C-0014)
- Python 3.12.10; git 2.56. `.venv` con `requirements.txt` y `requirements-dev.txt`; `pip install -e .` (ada_g2 0.1.0).
- Pruebas: `.venv/Scripts/python.exe -m pytest -q` → 273 passed. **Con `py` del sistema la recolección falla** (ModuleNotFoundError: ada_g2): usar el venv.
- Lectura de documentos: `python tools/leer_docs.py <archivo.pdf|.docx> --out <carpeta>` (D-31).
- `core.hooksPath = agent/hooks`; `agent/hooks/pre-commit` exige CHANGELOG si el commit toca fuera de `agent/` y `.claude/`; CHANGELOG solo-añadir.
- Hooks de Claude Code: PostToolUse escribe en `agent/log/auto_changes.log`; Stop (`check_logged.py`) bloquea cambios sin registrar.
- Hora: `TZ=America/Bogota date` en Git Bash devuelve **UTC** (14:16 cuando en Bogotá eran 09:16). Usar `python` con `zoneinfo`: `datetime.now(ZoneInfo('America/Bogota'))`.
- pandoc y LaTeX **no** instalados localmente: los PDF se compilan en letX por el usuario (D-20).

## Hecho hasta ahora (resumen; detalle en CHANGELOG)
- Modelo y supuestos: D-01 u_i = a_i·ln(1+x); D-02 f cobertura probabilística; D-03 cupo k=5 y costo ≤ 24 a la vez; D-14 certificados; D-15/D-32 instancia ajustada; D-20 PDF en letX; D-33 manual en LaTeX; D-34/D-35 tag y push de la primera entrega (cumplidos en C-0012); **D-36 caso promedio bajo el modelo del generador; D-37 voraz de selección en modo `costo` cuesta Θ(min(N,L+1)·N·M), no Θ(kNM).**
- Caso de la profesora: R1=R2 S={N09,N11,N13,N14,N15} f=145.5795, costo 23; Σf=436.7386, Σu=262.7387; razón certificada 0.9578.
- Instancia ajustada (`python -m ada_g2 ajustada`): k=2,3,5 → 3/4, 19/27, 2101/3125 (cota alcanzada exactamente).
- Razón mínima medida (C-0008, sin garantía en costo/ambos, R-01): modo k 0.8885; costo 0.8864; ambos 0.8148.
- **Análisis por casos (C-0013/C-0014):** reparto: mejor Θ(N), peor Θ(N+B(1+log N)), espacio Θ(N+J). Voraz de selección: modo k/ambos Θ(kNM) en el peor caso; modo costo Θ(min(N,L+1)·N·M) (D-37); mejor caso del código Θ(NM), porque se detiene antes si nada cabe. Fuerza bruta sin poda: visitas = nº de subconjuntos. Caso promedio bajo el modelo del generador (D-36). Pruebas de conteo: 33 casos en `tests/test_casos_complejidad.py`.
- Commits: C-0001…C-0004 `5054456`; C-0005 `35db17c`; C-0006 `5f98f59`; C-0007 `db0c194`; C-0008 `27b71f4`; C-0009 `4376f41`; C-0010 `730c8fa`; C-0011 `72cca80`; C-0012 `6a25d0f` (tag `v0.1-primera-entrega`). **C-0013 + C-0014: commit pendiente (hash en C-0015).**

## Siguiente paso inmediato
**Usuario, en letX:** compilar `informe/main.tex` → `informe/informe.pdf` y `manual/manual_tecnico.tex` → `manual/manual_tecnico.pdf` (pdfLaTeX, 2 pasadas). Subir los PDF al repo; el commit va en la siguiente entrada. Verificar sin "??" con pdfplumber (`requirements-dev.txt`).

Orden P1 después de eso:
1. T14 (report-writer): la guía de estudio debe incorporar la tabla de casos (`tab:casos`); reemplazar cifras PRELIMINAR; completar §8 con rutas reales.
2. T13 (experimenter): E1–E3 y E5 con ≥5 tamaños de n; CSV + PNG en `results/experimentos/`; semillas fijas; `.venv/Scripts/python.exe`.
3. Opcional (verifier): pruebas de conteo pendientes sugeridas por el theorist: heapreplace = B con r_i > B; modo costo con c ≡ 1: min(N,L+1) llamadas; p ≤ I ≤ min(kmax, p+1); conteos del DP.
4. T10 (theorist): deducción formal de T(n) con costeo línea a línea y sumatorias contra conteo real.
5. T11 (theorist): water-filling, de esbozo a demostración.

Cada bloque de cambios: `scribe` registra antes de cerrar el turno (Regla 0).

## Pendiente del usuario
- **(a)** Q-02: ¿la profesora acepta trabajo individual y sustentación sin pareja?
- **(b)** Q-01: confirmar con la profesora qué se entrega exactamente.
- **(c)** R-03: decidir si mover el repo fuera de OneDrive (advertencias CRLF; `.git` en OneDrive).
- **(d)** Recompilar los PDF de informe y manual en letX (ver Siguiente paso).

## Bloqueos
- Ninguno duro para P0 (entregado).
- **PDF desactualizados:** `informe/informe.pdf` y `manual/manual_tecnico.pdf` no reflejan la subsección de casos ni la §3.5. Hasta recompilar, el PDF de la entrega está atrás del fuente.
- Sin verificar: compilación LaTeX de C-0014 (sin TeX local, D-20).
- No probado todavía: exit 3 de `ajustada` y de la CLI `run`; instancias aleatorias N>9; tiempos y T(n) (T13); caso promedio frente a experimentos (T13).
- No bloqueante: `io.py` — un id de nodo repetido genera cascada de "arista a nodo inexistente", y ese error enmascara el de peso. Sin asignar.

## Riesgos y citas
- **R-01 — Garantía con cupo + costo a la vez:** sin garantía demostrada por nosotros para la combinación. La cota ½(1−1/e) de Khuller et al. (1999) es para cobertura máxima con presupuesto. Vecinos (comprobados solo en resumen): Leskovec et al. KDD'07; Khuller–Moss–Naor 1999, IPL 70(1):39-45; Sviridenko 2004, ORL 32(1):41-43; Kulik–Shachnai–Tamir, SODA 2009, pp. 545-554; Sarpatwar–Schieber–Shachnai (falta confirmar la revista). Mitigación: certificado a posteriori D-14(b) + razón contra fuerza bruta + familia 0/1. **No afirmar garantía teórica para la combinación.**
- **R-02 — Saturación:** con K15 y pesos ≥ 0.2, f se satura; la instancia de la profesora no discrimina. Añadir familias sintéticas para 1−1/e (SPEC §6-7).
- **R-03 — OneDrive + git:** `.git` con muchos archivos pequeños y `.lock` puede sincronizar mal. Recomendado mover el repo fuera de OneDrive.
- **R-04 — Citas [VERIFICAR]:** Karp 1972; Garey–Johnson 1979 (número del problema Conjunto Dominante); Minoux 1978 (original); revista de Sarpatwar et al.; nuevos (C-0014): costo C_PL de HiGHS en el certificado de la selección; Khachiyan 1979; umbral de underflow. Comprobadas a nivel de resumen: Nemhauser–Wolsey–Fisher 1978 (MP 14(1):265-294), Feige 1998 (JACM 45(4):634-652), Fox 1966 (MS 13(3):210-216), Federgruen–Groenevelt 1986 (OR 34(6):909-918).
- **R-05 — Docx vs PDF:** difieren en detalles (semanas, T(N,B)); se usa el PDF.
- **R-06 — Cifras PRELIMINARES de la guía de estudio:** la guía §5 (UB(λ*), razón 0.9578, 0.7037/0.67232) sale de un prototipo; T14 las reemplaza con el código final.

## NO hacer
- No `git push` sin pedido explícito del usuario (D-18; D-35 cubre solo la primera entrega).
- No mover ni recrear `v0.1-primera-entrega`.
- No versionar `docs/`; no `--no-verify`; no `reset --hard`, `clean` ni force-push.
- No inventar citas ni números; no hardcodear el caso de la profesora; no reescribir entradas del CHANGELOG.
- No afirmar garantía teórica para cupo + costo a la vez (R-01).
- No presentar cifras de caso promedio fuera del modelo de D-36.
