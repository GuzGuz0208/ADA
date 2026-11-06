# CONTEXT — estado vivo del proyecto

> Reescribir en cada checkpoint (no acumular; ≤ ~150 líneas). Historia detallada: `agent/CHANGELOG.md`.

**Última actualización:** 2026-11-06 09:59 (America/Bogota) · scribe (claude-haiku-5.5) registrando C-0017 (etiqueta `v0.1-primera-entrega` movida a `5beb850`, D-41)
**Testigo:** Claude Code. C-0017 se commitea por el scribe; su hash lo reporta el scribe al orquestador y se anota en la siguiente entrada.
Nota de hora: C-0015 y versiones anteriores de este archivo dicen 14:40; esa hora era UTC (= 09:40 Bogotá). Comprobar la hora con el comando de abajo, no con `TZ=... date`.

## Qué es
Proyecto semestral ADA 2026-B (profesora Luz Enith Guerrero). **Grupo 2 · Subproyecto 2 "Reparto de presupuesto y selección de participantes"**: Parte 1 reparto óptimo (voraz por ganancia marginal, exacto, O(N+B log N)); Parte 2 selección de k nodos (NP-difícil por reducción desde Cobertura Máxima; voraz con garantía 1−(1−1/k)^k, ≥ 1−1/e). **Proyecto individual: Juan Esteban Guzmán Henao.** Repo: `C:\Users\danna\OneDrive\Documentos\ADA`, rama `main`, remoto `origin` = https://github.com/GuzGuz0208/ADA.git (público, según el usuario). Guía de estudio del usuario: https://claude.ai/artifact/1n9ukzYACjPEQGKqmvq8h1 (D-16).
**Primera entrega (2026-11-06): COMPLETA.** Etiqueta anotada `v0.1-primera-entrega` → commit `5beb850` (C-0016: PDF recompilados en letX, maquetación y casos corregidos). Movida desde `6a25d0f` por petición del usuario (D-41); el force-push de la etiqueta lo ejecutó el usuario. Remoto verificado en C-0017: `refs/tags/v0.1-primera-entrega` (objeto `223f484`, `^{}` = `5beb850`); `origin/main` = `5beb850`. Detalle en `agent/SPEC.md` §1 y §8.

## Estado por producto
| Producto | Estado | Dónde |
|---|---|---|
| Informe (formalización, NP-dureza, optimalidad, caso) | ✅ PDF recompilado en letX (27 págs.) y verificado (C-0016): sin desbordes ni "??" | `informe/main.tex`, `informe/informe.pdf`, `informe/secciones/01…04`, `informe/INFORME.md` |
| Análisis por casos (mejor, peor, promedio) | ✅ teórico (C-0014) y PDF (C-0016) | `informe/secciones/03_optimalidad_y_cota.tex` (`sec:casos`), `tests/test_casos_complejidad.py` |
| Código base y pruebas | ✅ `pytest` 273 passed (C-0014). Sin cambios de código desde C-0014 | `src/ada_g2/`, `tests/`, `README.md` |
| Caso de la profesora | ✅ T06: exit 0, TODO CUMPLE. Cifras de la guía §5 aún PRELIMINARES (R-06) | `results/caso_entrada_G2_red_15_nodos/` |
| Manual técnico | ✅ PDF recompilado en letX (15 págs.) y verificado (C-0016) | `manual/manual_tecnico.tex`, `manual/manual_tecnico.pdf`, `manual/MANUAL_TECNICO.md` |
| Experimentos | 🔄 T12 razón mínima medida; ⬜ T13 (no existe `results/experimentos/`) | `results/` |
| Guía de estudio (sustentación 45 %) | ⬜ T14: falta la tabla de casos y reemplazar cifras PRELIMINAR | Claude Doc (D-16) |
| Memoria compartida y hooks | ✅ T00; hooks probados en Windows; config en `.claude/` | `agent/`, `.claude/`, `agent/hooks/` |

## Entorno (comprobado en T00 y C-0006 a C-0017)
- Python 3.12.10; git 2.56. `.venv` con `requirements.txt` y `requirements-dev.txt`; `pip install -e .` (ada_g2 0.1.0).
- Pruebas: `.venv/Scripts/python.exe -m pytest -q` → 273 passed. **Con `py` del sistema la recolección falla** (ModuleNotFoundError: ada_g2): usar el venv.
- Lectura de documentos: `python tools/leer_docs.py <archivo.pdf|.docx> --out <carpeta>` (D-31).
- `core.hooksPath = agent/hooks`; `agent/hooks/pre-commit` exige CHANGELOG si el commit toca fuera de `agent/` y `.claude/`; CHANGELOG solo-añadir.
- Hooks de Claude Code: PostToolUse escribe en `agent/log/auto_changes.log`; Stop (`check_logged.py`) bloquea cambios sin registrar.
- Hora de Bogotá: `python -c "from datetime import datetime; from zoneinfo import ZoneInfo; print(datetime.now(ZoneInfo('America/Bogota')).strftime('%Y-%m-%d %H:%M'))"` (en Git Bash, `TZ=America/Bogota date` devuelve UTC).
- Permisos: `git tag -f` y `git push --force` están bloqueados para el agente (D-41); los ejecuta el usuario.
- pandoc y LaTeX **no** instalados localmente: los PDF se compilan en letX por el usuario (D-20).

## Hecho hasta ahora (resumen; detalle en CHANGELOG)
- Modelo y supuestos: D-01 u_i = a_i·ln(1+x); D-02 f cobertura probabilística; D-03 cupo k=5 y costo ≤ 24 a la vez; D-14 certificados; D-15/D-32 instancia ajustada; D-20 PDF en letX; D-33 manual en LaTeX; D-36 caso promedio bajo el modelo del generador; D-37 voraz de selección en modo `costo` cuesta Θ(min(N,L+1)·N·M); D-38/D-39 macro `\cod` (expl3) verificada en letX.
- Push y etiqueta: D-34/D-35 (primera entrega, C-0012); D-40 push a `main` (C-0016); D-41 etiqueta movida a `5beb850` (C-0017).
- Caso de la profesora: R1=R2 S={N09,N11,N13,N14,N15} f=145.5795, costo 23; Σf=436.7386, Σu=262.7387; razón certificada 0.9578.
- Instancia ajustada (`python -m ada_g2 ajustada`): k=2,3,5 → 3/4, 19/27, 2101/3125 (cota alcanzada exactamente).
- Razón mínima medida (C-0008, sin garantía en costo/ambos, R-01): modo k 0.8885; costo 0.8864; ambos 0.8148.
- **Análisis por casos (C-0013/C-0014):** reparto: mejor Θ(N), peor Θ(N+B(1+log N)), espacio Θ(N+J). Voraz de selección: modo k/ambos Θ(kNM) en el peor caso; modo costo Θ(min(N,L+1)·N·M) (D-37); mejor caso del código Θ(NM). Fuerza bruta sin poda: visitas = nº de subconjuntos. Caso promedio bajo el modelo del generador (D-36). Pruebas de conteo: 33 casos.
- Commits: C-0001…C-0004 `5054456`; C-0005 `35db17c`; C-0006 `5f98f59`; C-0007 `db0c194`; C-0008 `27b71f4`; C-0009 `4376f41`; C-0010 `730c8fa`; C-0011 `72cca80`; C-0012 `6a25d0f` (tag original, movido por D-41); C-0013 + C-0014 `586beec`; C-0015 `fec0826`; C-0016 `5beb850` (etiqueta y `origin/main`); C-0017: commit pendiente (hash en la respuesta del scribe). No quedan PDF sin commitear.

## Siguiente paso inmediato
**T14 (report-writer), una acción:** ejecutar `.venv/Scripts/python.exe -m ada_g2 run --input project-docs/entrada_G2_red_15_nodos.json --out results/` y contrastar con `results/caso_entrada_G2_red_15_nodos/resultado.json` las cifras PRELIMINARES de la guía §5 (R-06: UB(λ*), razón 0.9578, 0.7037/0.67232). Anotar cuáles cambian para reemplazarlas en la guía (Claude Doc, D-16).

Orden P1 después de eso:
1. T13 (experimenter): E1–E3 y E5 con ≥5 tamaños de n; CSV + PNG en `results/experimentos/`; semillas fijas; `.venv/Scripts/python.exe`.
2. Opcional (verifier): pruebas de conteo pendientes sugeridas por el theorist: heapreplace = B con r_i > B; modo costo con c ≡ 1: min(N,L+1) llamadas; p ≤ I ≤ min(kmax, p+1); conteos del DP.
3. T10 (theorist): deducción formal de T(n) con costeo línea a línea y sumatorias contra conteo real.
4. T11 (theorist): water-filling, de esbozo a demostración.

Cada bloque de cambios: `scribe` registra antes de cerrar el turno (Regla 0).

## Pendiente del usuario
- **(a)** Q-02: ¿la profesora acepta trabajo individual y sustentación sin pareja?
- **(b)** Q-01: confirmar con la profesora qué se entrega exactamente.
- **(c)** R-03: decidir si mover el repo fuera de OneDrive (advertencias CRLF; `.git` en OneDrive).

## Bloqueos
- Ninguno duro. P0 entregado; PDF de maquetación verificados (C-0016); etiqueta en `5beb850` (C-0017).
- **Sin verificar / no probado:** exit 3 de `ajustada` y de la CLI `run`; instancias aleatorias N>9; tiempos y T(n) (T13); caso promedio frente a experimentos (T13).
- No bloqueante: `io.py` — un id de nodo repetido genera cascada de "arista a nodo inexistente", y ese error enmascara el de peso. Sin asignar.

## Riesgos y citas
- **R-01 — Garantía con cupo + costo a la vez:** sin garantía demostrada por nosotros para la combinación. La cota ½(1−1/e) de Khuller et al. (1999) es para cobertura máxima con presupuesto. Vecinos (comprobados solo en resumen): Leskovec et al. KDD'07; Khuller–Moss–Naor 1999, IPL 70(1):39-45; Sviridenko 2004, ORL 32(1):41-43; Kulik–Shachnai–Tamir, SODA 2009, pp. 545-554; Sarpatwar–Schieber–Shachnai (falta confirmar la revista). Mitigación: certificado a posteriori D-14(b) + razón contra fuerza bruta + familia 0/1. **No afirmar garantía teórica para la combinación.**
- **R-02 — Saturación:** con K15 y pesos ≥ 0.2, f se satura; la instancia de la profesora no discrimina. Añadir familias sintéticas para 1−1/e (SPEC §6-7).
- **R-03 — OneDrive + git:** `.git` con muchos archivos pequeños y `.lock` puede sincronizar mal. Recomendado mover el repo fuera de OneDrive.
- **R-04 — Citas [VERIFICAR]:** Karp 1972; Garey–Johnson 1979 (número del problema Conjunto Dominante); Minoux 1978 (original); revista de Sarpatwar et al.; costo C_PL de HiGHS en el certificado de la selección; Khachiyan 1979 (`\VER` en `referencias.tex`, C-0015); umbral de underflow. Comprobadas a nivel de resumen: Nemhauser–Wolsey–Fisher 1978 (MP 14(1):265-294), Feige 1998 (JACM 45(4):634-652), Fox 1966 (MS 13(3):210-216), Federgruen–Groenevelt 1986 (OR 34(6):909-918).
- **R-05 — Docx vs PDF:** difieren en detalles (semanas, T(N,B)); se usa el PDF.
- **R-06 — Cifras PRELIMINARES de la guía de estudio:** la guía §5 (UB(λ*), razón 0.9578, 0.7037/0.67232) sale de un prototipo; T14 las reemplaza con el código final.

## NO hacer
- No `git push` sin pedido explícito del usuario (D-18). D-35 (primera entrega), D-40 (`main`) y D-41 (etiqueta) son pedidos puntuales.
- No volver a mover `v0.1-primera-entrega` sin pedido del usuario (D-41). Ahora apunta a `5beb850`.
- No versionar `docs/`; no `--no-verify`; no `reset --hard`, `clean` ni force-push.
- No inventar citas ni números; no hardcodear el caso de la profesora; no reescribir entradas del CHANGELOG.
- No afirmar garantía teórica para cupo + costo a la vez (R-01).
- No presentar cifras de caso promedio fuera del modelo de D-36.
