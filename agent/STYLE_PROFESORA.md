# STYLE_PROFESORA — cómo formaliza y demuestra la Dra. Luz Enith Guerrero

Fuentes leídas: `docs/ADA_24A___Notas.pdf` (notas de clase 2024, redactadas por un estudiante bajo su instrucción; caps. 1-9), libro *Análisis y Diseño de Algoritmos: un enfoque práctico* (Villegas y Guerrero, U. Nacional, 2016; cap. 5 voraces, cap. 9 aproximados) y el enunciado del proyecto. Aplicar estas convenciones en informe, manual y comentarios de código.

## Convenciones (con ubicación)
1. **Algoritmos con firma formal** (Notas §2.1): parámetros de **Forma** (E=entrada, S=salida, M=mixta), **Tipo** y **Nombre**; **precondiciones** y **poscondiciones** (§2.1.1). Pseudocódigo numerado por línea, arreglos indexados desde 1.
2. **Costeo línea a línea** (Notas §2.1, Ej. 2.1): tabla con "operaciones elementales × número de ejecuciones" por línea. En un ciclo, **cabeza = cuerpo + 1** ejecuciones. Se resuelven las sumatorias **de la más interna a la más externa**. Resultado típico: `T(n) = a·n² + b·n + c ∈ Θ(n²)`. También **S(n)** (complejidad espacial).
3. **Mejor y peor caso** (§2.1.1): T_best y T_worst cuando la entrada cambia el recorrido; el caso "invariante" cuando el ciclo siempre itera igual.
4. **Función de eficiencia por atajo** (§2.3.3): contar la operación más ejecutada (la más anidada) — válido como verificación, pero el enunciado exige la **deducción explícita paso a paso**.
5. **Correctitud por lazo invariante** (§2.3): *inicialización* (cierto antes de la primera iteración), *mantenimiento* (si es cierto antes, sigue cierto antes de la siguiente), *terminación* (al salir, la propiedad prueba la correctitud). Además distingue correctitud parcial y terminación.
6. **Voraces** (Notas §5.1; libro cap. 5): elementos = conjunto de candidatos, función de selección, función de factibilidad ("prometedor"), función objetivo z, comprobante de solución. Frase clave: *"lo importante de un voraz no es diseñarlo, es demostrar que siempre consigue el óptimo en todos los casos, o dar un contraejemplo."*
7. **Montículos** (Notas §3.1.3-3.1.5): árbol binario completo en arreglo, hijos en 2i y 2i+1; **Heapify construye en O(n)** mientras insertar uno a uno cuesta O(n lg n); colas de prioridad con max/min-heap. El enunciado usa "construir el montículo O(N), cada asignación O(log N)".
8. **Notación asintótica** (§1): O, Ω, Θ, o, ω, notación tilde, y **dos variables** (§1.1.8) — necesaria aquí porque T depende de (N,B) y (N,k).
9. **Aproximación** (libro cap. 9): error relativo respecto al costo óptimo; esquema de aproximación polinomial = familia de algoritmos con error prefijado. El enunciado pide **razón de aproximación** citada y verificada.
10. **Teoremas/ejemplos** con cierre ■ y contraejemplos explícitos cuando algo falla.

## Plantilla de costeo (copiar)
| Línea | Instrucción | Ops. elementales | Ejecuciones | Subtotal |
|---|---|---|---|---|
| 1 | … | c₁ | 1 | c₁ |
| 2 | `for i = 1 to n` | 3 | n + 1 | 3(n+1) |
| 3 | cuerpo | c₃ | n | c₃·n |
→ `T(n) = …` ⇒ `T(n) ∈ Θ(…)`; luego `T_best`, `T_worst`, `S(n)`.

## Plantilla de demostración
**Teorema.** enunciado con hipótesis explícitas. **Demostración.** (1) qué se va a probar y por qué contradicción/intercambio/inducción; (2) pasos numerados, cada uno justificado por una hipótesis o resultado citado; (3) cierre ■. **Observación.** dónde se usa cada hipótesis y qué pasa si falla (contraejemplo).

## Qué se juega en la sustentación (45 %)
Deben poder explicar **sin notas** la reducción de NP-dureza y la deducción de T(n) del exacto. El informe debe estar escrito para estudiarse: cada paso con su porqué (ver T14 en TASKS para la guía de estudio).
