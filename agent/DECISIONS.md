# DECISIONS — decisiones de modelado, supuestos y preguntas abiertas

Reglas: cada decisión tiene ID estable; no se renumera. Si una decisión cambia, se añade una nueva que la reemplaza y la antigua se marca `REEMPLAZADA POR D-xx` (no se borra). Origen: `usuario`, `profesora`, `claude`, `codex`.

## Aceptadas por el usuario (2026-11-05)
Contexto: se verificó que **ningún documento del Grupo 2** (PDF general, docx, guías, JSON) define u_i, f ni q; el enunciado dice que el equipo "precisa τ para la función de utilidad que implemente". El usuario pidió elegir las opciones recomendadas.

| ID | Decisión | Origen |
|---|---|---|
| D-01 | **u_i(x) = a_i·ln(1+x)**, x∈ℕ, a_i = `coeficiente_utilidad`. Ganancia marginal a_i·ln((x+2)/(x+1)), estrictamente decreciente | usuario |
| D-02 | **f(S) = Σ_j a_j·[1 − Π_{i∈S}(1 − w_ij)]** (cobertura probabilística con el grafo), w_ii=1. Monótona y submodular; con w∈{0,1}, a=1 es Cobertura Máxima (sirve para la reducción). Familia general: candidatos N, objetivos M | usuario |
| D-03 | Selección de la base con **ambas restricciones a la vez**: |S|≤k=5 **y** Σc_i≤24 por ronda. El código debe permitir además los modos `k` y `costo` por bandera, para poder reportar las otras lecturas | usuario |
| D-04 | Alcance: **primera entrega + extras si alcanza** (P0 → P1 → P2) | usuario |

## Propuestas de Claude (vigentes como default; cambiarlas solo con un D-xx nuevo)
| ID | Decisión | Por qué |
|---|---|---|
| D-05 | Python ≥ 3.10; librerías: numpy, scipy, matplotlib; pruebas: pytest + hypothesis | Estándar, reproducible; hypothesis valida propiedades (optimalidad, submodularidad) |
| D-06 | Topes por nodo r_i = `presupuesto_total_nodo` − gastado en rondas previas; en el reparto el nodo sale del montículo al llegar a su tope | El JSON los trae y sí son activos en la ronda 3 (SPEC §3). El voraz sigue óptimo con topes (SPEC T1) |
| D-07 | q no está en el JSON ⇒ **q=0** para el caso de la profesora; barrido q∈{0.1,0.2,0.3} con ≥100 semillas como extra (variante) | Mantener el caso base determinista |
| D-08 | Se resuelven por separado y en cadena (Parte 2 → Parte 1) como en la Fig. 3.1 del PDF; se reportan Σ_t f(S_t) y Σ_t Σ_i u_i(x_{i,t}) | Fiel al enunciado |
| D-09 | Informe: fuente en Markdown con LaTeX (`informe/`), exportable a PDF (LaTeX/pandoc) o DOCX según lo que haya instalado; se fija en T00 | Las demostraciones llevan mucha matemática |
| D-10 | Grafo **no dirigido y simétrico**: w_uv = w_vu = `peso_influencia` listado | El JSON lista cada par una sola vez; la dirección no está especificada (Q-04) |
| D-11 | Tiempos: `time.perf_counter`, mediana de ≥5 repeticiones, calentamiento previo, semilla fija `20261105`, sin otros procesos pesados | Reproducibilidad de la validación experimental |
| D-12 | Desempates por **menor índice de nodo** | Determinismo: mismas trazas en cualquier máquina |
| D-13 | Logaritmo natural; B y costos enteros; utilidades en float64 con comparaciones con tolerancia 1e-9 en pruebas | Evitar falsos fallos numéricos |
| D-14 | **Certificados por ejecución** (el "wow"): el programa calcula y verifica en cada caso (a) Parte 1: cota de dualidad de Lagrange UB(λ*) = λ*·B + Σ máx_x[a_i·ln(1+x) − λ*·x] (máximo entero = piso/techo de a_i/λ − 1 recortado a [0, r_i]); debe coincidir con la utilidad del reparto (brecha 0, tolerancia 1e-9); si los topes impiden gastar todo B, usar λ=0; (b) Parte 2: cota a posteriori f(S*) ≤ f(S) + máx{Σ Δ_e·z_e : Σ z_e ≤ k, Σ c_e·z_e ≤ L, 0≤z≤1} (programa lineal con scipy/highs); razón certificada = f(S)/(f(S)+máx). La ejecución **falla** si un certificado no se cumple | Prueba cada resultado sin conocer el óptimo; vale también con cupo+costo, donde no hay garantía a priori (R-01) |
| D-15 | Familia sintética "instancia ajustada" para k∈{2,3,5,…}: k conjuntos óptimos disjuntos de m=k^k elementos y k trampas con capas de tamaño k^(k−j)·(k−1)^(j−1) por conjunto óptimo; con desempate por menor índice (D-12) y trampas indexadas primero, el voraz logra exactamente 1−(1−1/k)^k | Muestra que la cota 1−1/e es ajustada para el voraz; sirve para E4 |
| D-16 | **Guía de estudio** del usuario: Claude Doc "Guía de estudio — ADA 2026-B · Grupo 2 · Proyecto Red" en https://claude.ai/artifact/1n9ukzYACjPEQGKqmvq8h1 (secciones 0-8). T14 debe **completar la sección 8 (mapa del código)** y reemplazar toda cifra marcada PRELIMINAR por la salida del código final. Si algo del código contradice la guía, manda el código y se corrige la guía | El usuario sustenta solo y sin notas (45 % de la nota) |
| D-17 | **Avisos de cambio de sesión** (formato en `agent/ROLES.md`): quien trabaje debe imprimirlos él mismo, porque ningún chat puede avisar sin que el usuario escriba | El usuario quiere saber cuándo mover el trabajo entre chats/IAs |
| D-18 | **Repositorio remoto:** https://github.com/GuzGuz0208/ADA (creado por el usuario el 2026-11-05). Se añade como `origin` en T00; **no hacer `git push` hasta que el usuario lo pida**; etiqueta `v0.1-primera-entrega` al entregar | Resuelve la parte de URL de Q-02; el enlace debe ser accesible para la profesora (verificar visibilidad/invitación) |
| D-19 | **Entorno de informe:** el usuario tiene sesión iniciada en letX (plan gratuito) para compilar el LaTeX en la nube; MiKTeX + pandoc locales son opcionales (permiten a los agentes generar el PDF sin conexión). Si no hay TeX local, el informe se entrega compilando en letX o exportando desde pandoc a DOCX | Resuelve Q-03 en parte; no bloquea nada |

## Abiertas (preguntar solo si cambian el resultado)
| ID | Pregunta | Bloquea | Default mientras tanto |
|---|---|---|---|
| Q-01 | ¿Qué se entrega exactamente mañana? La guía dice que pedir los 4 productos juntos es "propuesta pendiente de confirmar con el docente" | Prioridades | P0 = los 4 productos de la guía |
| Q-02 | ~~Nombres de los 2 integrantes y URL del repositorio~~ **RESUELTA 2026-11-05:** integrante único = Juan Esteban Guzmán Henao; repo = https://github.com/GuzGuz0208/ADA (D-18). **Sigue abierto:** ¿la profesora acepta trabajo individual y sustentación sin pareja? y ¿el enlace es accesible para ella (público o invitación)? | Informe | Preguntar a la profesora |
| Q-03 | ¿Hay LaTeX (MiKTeX/TeX Live) o pandoc instalado en el PC? ¿Informe en Word o PDF? (D-19: hay letX en la nube; falta saber lo local) | Exportación | Markdown + exportar con lo que haya; PDF vía letX |
| Q-04 | ¿El grafo de influencia es dirigido? | Cálculo de f | Simétrico (D-10) |
| Q-05 | ¿La profesora espera una forma concreta de u_i, f o q? | Modelo | D-01, D-02, D-07 |

## Riesgos y advertencias
- **R-01 — Garantía con cupo+costo a la vez (actualizado C-0003):** sigue sin haber garantía *demostrada por nosotros* para la combinación. La cota ½(1−1/e) de Khuller et al. (1999) se probó para *cobertura máxima con presupuesto*; nuestra f es una cobertura *probabilística* con cupo k además del costo. **No afirmar garantía teórica para la combinación.** Existen resultados para problemas vecinos, comprobados solo en resumen/registro (no en texto completo): Leskovec et al. KDD'07 (mejor de dos voraces, ½(1−1/e), cotas en línea); Khuller–Moss–Naor 1999, IPL 70(1):39-45; Sviridenko 2004, Oper. Res. Lett. 32(1):41-43; Kulik–Shachnai–Tamir, SODA 2009, pp. 545-554 ((1−ε)(1−1/e) con un número constante de restricciones lineales: cupo+costo lo es); Sarpatwar–Schieber–Shachnai (½(1−1/e²), mochila + matroide) — **falta confirmar la revista**. Mitigación: certificado a posteriori D-14(b) + razón real contra fuerza bruta (N=15 ⇒ ≤4 943 subconjuntos) + familia 0/1 para la cota clásica.
- **R-02 — Saturación:** con K15 y pesos ≥0.2, f se satura (≈98 % de Σa con 5 nodos); la instancia de la profesora no discrimina. Añadir familias sintéticas para la verificación de 1−1/e (SPEC §6-7).
- **R-03 — OneDrive + git:** la carpeta está en OneDrive; `.git` con muchos archivos pequeños y archivos `.lock` puede sincronizar mal o corromperse. Recomendado: mover el repo fuera de OneDrive (p. ej. `C:\dev\ADA`) o excluir `.git` de la sincronización. Hasta decidirlo, seguir en esta carpeta.
- **R-04 — Citas (actualizado C-0003):** todo lo marcado `[VERIFICAR]` debe confirmarse con la fuente antes de entrar al informe. Pendientes: Karp 1972, Garey–Johnson 1979 (número del problema Conjunto Dominante), Minoux 1978 (original), revista de Sarpatwar et al. Comprobadas a nivel de resumen/registro: Nemhauser–Wolsey–Fisher 1978 (Math. Prog. 14(1):265-294), Feige 1998 (JACM 45(4):634-652), Fox 1966 (Mgmt Sci 13(3):210-216), Federgruen–Groenevelt 1986 (Oper. Res. 34(6):909-918).
- **R-05 — Docx vs PDF:** difieren en detalles (semanas, T(N,B)); se usa el PDF; registrar si la profesora aclara otra cosa.
- **R-06 — Cifras PRELIMINARES de la guía de estudio:** las cifras de la guía §5 (UB(λ*), razón certificada 0.9578, razones 0.7037/0.67232, etc.) salen de un prototipo desechable; el `verifier` debe reproducirlas con el código final y T14 reemplazarlas.
