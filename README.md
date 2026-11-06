# ADA 2026-B — Grupo 2 · Proyecto Red (reparto de presupuesto y selección de participantes)

> **Estado: en construcción (andamiaje).** Este README se completa en la tarea T07 (`agent/TASKS.md`).

- **Curso:** Análisis y Diseño de Algoritmos · Profesora Luz Enith Guerrero · Universidad de Caldas
- **Subproyecto:** 2 — Reparto de presupuesto y selección de participantes
- **Integrante:** Juan Esteban Guzmán Henao (trabajo individual)
- **Repositorio:** https://github.com/GuzGuz0208/ADA · **Versión entregada:** `[tag, p. ej. v0.1-primera-entrega]`

## Resumen
- **Parte 1 (exacta, polinomial):** reparto del presupuesto B entre los nodos participantes con el algoritmo voraz por ganancia marginal (montículo), T(N,B) = O(N + B log N).
- **Parte 2 (NP-difícil):** selección de nodos; reducción desde Cobertura Máxima; algoritmo voraz con garantía (1 − 1/e) para el caso de cupo k.

## Cómo ejecutar *(se completa en T04/T07)*
```
python -m venv .venv
pip install -r requirements.txt
python -m ada_g2 run --input project-docs/entrada_G2_red_15_nodos.json --out results/
pytest -q
```

## Contenido
`project-docs/` enunciados y caso de la profesora · `src/ada_g2/` código · `tests/` pruebas · `results/` resultados, tiempos y trazas · `informe/` informe técnico · `manual/` manual técnico · `agent/` memoria de trabajo de los agentes de IA (ver `AGENTS.md`).
