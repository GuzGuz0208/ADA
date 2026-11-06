# ACTUALIZACIÓN PENDIENTE C-0003 — aplicar al empezar T00 y registrar en el CHANGELOG

Origen: chat de Claude app, 2026-11-05 ~21:00 (America/Bogota), modelo claude-sonnet-5.5. El equipo del usuario se desconectó antes de que ese chat pudiera escribir en el repo, así que estos cambios **no están aplicados**. Quien abra este archivo (Claude Code o Codex): aplícalos tal cual, luego registra la entrada C-0003 (texto al final) **añadiéndola** al final de `agent/CHANGELOG.md` (nunca editar entradas previas), actualiza `agent/CONTEXT.md` y haz commit. Después puedes dejar este archivo en el repo (es parte de la historia).

## 1. Datos del equipo (resuelve Q-02 en parte)
- El proyecto lo hace **una sola persona: Juan Esteban Guzmán Henao** (no son 2 integrantes). Sustituye en `README.md`, `agent/CONTEXT.md` ("Equipo de 2"), `agent/DECISIONS.md` (Q-02) y `AGENTS.md` donde diga "2 integrantes" / `[INTEGRANTE 1]` / `[INTEGRANTE 2]`.
- Sigue abierta: la **URL del repositorio** (el usuario aún no ha creado el repo en GitHub; la dará en T00) y si la sustentación grupal aplica a un equipo de una persona (preguntar a la profesora).

## 2. Decisiones nuevas (añadir a `agent/DECISIONS.md`, tabla "Propuestas de Claude")
| ID | Decisión | Por qué |
|---|---|---|
| D-14 | **Certificados por ejecución** (el "wow"): el programa calcula y verifica en cada caso (a) Parte 1: cota de dualidad de Lagrange UB(λ*) = λ*·B + Σ máx_x[a_i·ln(1+x) − λ*·x] (máximo entero = piso/techo de a_i/λ − 1 recortado a [0, r_i]); debe coincidir con la utilidad del reparto (brecha 0, tolerancia 1e-9); si los topes impiden gastar todo B, usar λ=0; (b) Parte 2: cota a posteriori f(S*) ≤ f(S) + máx{Σ Δ_e·z_e : Σ z_e ≤ k, Σ c_e·z_e ≤ L, 0≤z≤1} (programa lineal con scipy/highs); razón certificada = f(S)/(f(S)+máx). La ejecución **falla** si un certificado no se cumple | Prueba cada resultado sin conocer el óptimo; vale también con cupo+costo, donde no hay garantía a priori (R-01) |
| D-15 | Familia sintética "instancia ajustada" para k∈{2,3,5,…}: k conjuntos óptimos disjuntos de m=k^k elementos y k trampas con capas de tamaño k^(k−j)·(k−1)^(j−1) por conjunto óptimo; con desempate por menor índice (D-12) y trampas indexadas primero, el voraz logra exactamente 1−(1−1/k)^k | Muestra que la cota 1−1/e es ajustada para el voraz; sirve para E4 |
| D-16 | **Guía de estudio** del usuario: Claude Doc "Guía de estudio — ADA 2026-B · Grupo 2 · Proyecto Red" en https://claude.ai/artifact/1n9ukzYACjPEQGKqmvq8h1 (secciones 0-8). T14 debe **completar la sección 8 (mapa del código)** y reemplazar toda cifra marcada PRELIMINAR por la salida del código final. Si algo del código contradice la guía, manda el código y se corrige la guía | El usuario sustenta solo y sin notas (45 % de la nota) |
| D-17 | **Avisos de cambio de sesión**: ver §5. Quien trabaje debe imprimirlos él mismo, porque ningún chat puede avisar sin que el usuario escriba | El usuario quiere saber cuándo mover el trabajo entre chats/IAs |

## 3. Riesgos (añadir/actualizar en `agent/DECISIONS.md`)
- **R-01 (actualizar):** sigue sin haber garantía *demostrada por nosotros* para cupo+costo. Pero existen resultados para problemas vecinos, ya comprobados en resumen/registro (no en texto completo): Leskovec et al. KDD'07 (mejor de dos voraces, ½(1−1/e), cotas en línea); Khuller–Moss–Naor 1999 IPL 70(1):39-45; Sviridenko 2004 Oper. Res. Lett. 32(1):41-43; Kulik–Shachnai–Tamir SODA 2009 pp. 545-554 ((1−ε)(1−1/e) con un número constante de restricciones lineales: cupo+costo lo es); Sarpatwar–Schieber–Shachnai (½(1−1/e²), mochila + matroide) — **falta confirmar la revista**. Mitigación: certificado a posteriori D-14(b) + razón real contra fuerza bruta.
- **R-04 (actualizar):** pendientes de verificar con la fuente: Karp 1972, Garey–Johnson 1979 (número de problema de Conjunto Dominante), Minoux 1978 (original), revista de Sarpatwar et al.
- **R-06 (nuevo):** las cifras de la guía de estudio §5 (UB(λ*), razón certificada 0.9578, razones 0.7037/0.67232, etc.) salen de un prototipo desechable; el verifier debe reproducirlas con el código final.

## 4. Tareas nuevas (añadir a `agent/TASKS.md`)
| ID | P | Tarea | Depende de |
|---|---|---|---|
| W1 | P1 | Certificado de dualidad de la Parte 1 (D-14a) + prueba de que la brecha es 0 en ≥500 instancias vs DP exacta (E5) | T-reparto |
| W2 | P1 | Cota a posteriori de la Parte 2 con LP (D-14b), con modo `k`, `costo` y ambos; verificar que el óptimo por fuerza bruta nunca la supera | T-selección |
| W3 | P1 | Generador de la instancia ajustada (D-15) y prueba: razón del voraz = 1−(1−1/k)^k para k=2,3,5 (valores esperados 6/8, 57/81, 10505/15625) | T-selección |
| W4 | P2 | Informe HTML de la traza por ronda (nodos, ganancias marginales, reparto, certificados) | T06 |
| W5 | P2 | Voraz perezoso (Minoux) con el mismo resultado y conteo de evaluaciones vs N·k | T-selección |
| T14 | P1 | (actualizar) completar §8 de la guía de estudio (ver D-16) | todo el código |

## 5. Avisos de cambio de sesión (añadir a `agent/ROLES.md` y a ambos prompts de `prompts/`)
Modelos por momento (no cambiar de modelo a mitad de sesión: reprocesa el historial y gasta cuota):
| Momento | Dónde | Modelo / esfuerzo |
|---|---|---|
| Sesión principal en VS Code | Claude Code | `opusplan` (Opus planifica, Sonnet ejecuta) |
| Demostraciones, decisiones de modelo, depuración difícil | subagente `theorist` | Opus, esfuerzo alto |
| Implementación, pruebas, experimentos, informe | subagentes `implementer`, `experimenter`, `report-writer` | Sonnet, esfuerzo medio (alto si falla algo sutil) |
| Verificación independiente | subagente `verifier` | Sonnet, esfuerzo alto, sin haber visto el trabajo |
| Registro del CHANGELOG | subagente `scribe` | Haiku |
| Se acaba la cuota de Claude | Codex | `prompts/PROMPT_CODEX.md` |

Cuándo el agente debe imprimir el aviso (después de hacer commit y dejar CONTEXT al día): (a) aparece cualquier aviso de límite de uso o cuota; (b) termina cada hito (T01…T08); (c) el contexto de la sesión pasa de ~70 %. Formato exacto:
```
=== CAMBIO DE SESIÓN RECOMENDADO ===
Motivo: <cuota | contexto | hito>
Siguiente: <Claude Code (opusplan) | Codex>
Hecho: commit <hash corto> · CONTEXT.md actualizado · CHANGELOG al día
Pega en el chat nuevo: prompts/PROMPT_VSCODE_CLAUDE.md  (o prompts/PROMPT_CODEX.md)
```

## 6. Texto de la entrada para añadir al final de `agent/CHANGELOG.md` (rellenar hash y hora al aplicarla)
```
### C-0003 · <AAAA-MM-DD HH:MM> · <agente/modelo> · tarea T00
- **Tipo:** decision
- **Archivos:**
  - A `agent/ACTUALIZACION_C-0003.md` — cambios pendientes del chat de Claude app (equipo de una persona, certificados, guía de estudio, avisos de sesión)
  - M `README.md`, `AGENTS.md`, `agent/CONTEXT.md`, `agent/DECISIONS.md` (Q-02, D-14…D-17, R-01/R-04/R-06), `agent/TASKS.md` (W1…W5, T14), `agent/ROLES.md`, `prompts/PROMPT_VSCODE_CLAUDE.md`, `prompts/PROMPT_CODEX.md` — aplicar §1-§5 de ACTUALIZACION_C-0003.md
- **Qué y por qué:** el proyecto lo hace Juan Esteban Guzmán Henao solo; se añaden certificados por ejecución (wow), la instancia ajustada para 1−1/e, la guía de estudio como Claude Doc y los avisos de cambio de sesión. Las referencias de R-01 se comprobaron en resúmenes/registros bibliográficos, no en el texto completo.
- **Verificación:** sin código nuevo; cifras de la guía (UB(λ*), 0.9578, 0.7037, 0.67232) son de un prototipo descartable → R-06
- **Commit:** <hash>
- **Siguiente paso:** T00 (git init, hooksPath, chmod +x del pre-commit, probar hooks, entorno) y luego T01…T08
```
