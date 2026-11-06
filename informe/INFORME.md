# Informe técnico — ADA 2026-B — Subproyecto 2 (espejo Markdown de `informe/main.tex`)

> Espejo de estudio del LaTeX (`main.tex` + `secciones/*.tex` + `referencias.tex`). Si difieren, **manda el LaTeX**.
> Universidad de Caldas · Análisis y Diseño de Algoritmos 2026-B · Profesora Luz Enith Guerrero · Subproyecto 2 — Reparto de presupuesto y selección de participantes · Integrante: Juan Esteban Guzmán Henao · Repositorio: https://github.com/GuzGuz0208/ADA · versión `v0.1-primera-entrega` · 6 de noviembre de 2026.

**Convenciones.** "Demostrado por nosotros" = prueba completa aquí; "citado" = tomado de la bibliografía. **[VERIFICAR]** = cita no confirmada con la fuente original. **[RESULTADO-T06]** = cifra que debe producir el código con semilla fija (no se escriben a mano). D-xx = decisiones de `agent/DECISIONS.md`. $\mathbb N=\{0,1,\dots\}$, $[n]=\{1,\dots,n\}$, $\ln$ natural, $\log$ en base 2 en los costos.

---

## 1. Formalización del problema

### 1.1 Contexto general
Una red de $N$ nodos entrena colaborativamente un modelo durante $T$ rondas sin compartir datos crudos; cada actualización lleva ruido calibrado (más ruido = más protección, menos utilidad). Cada nodo tiene un presupuesto total de "ruido tolerable" para todo el proyecto. En cada ronda se decide (a) **qué nodos participan** (Parte 2) y (b) **cuánto presupuesto recibe cada uno** (Parte 1). Se resuelven en cadena por ronda: primero $S_t$, luego el reparto sobre $S_t$ (Fig. 3.1 del enunciado; D-08).

### 1.2 Datos comunes y esquema
JSON con: `parametros` ($N$, $T$, $k$, $B$, $L$), `nodos` ($a_i>0$ = `coeficiente_utilidad`, $R_i$ = `presupuesto_total_nodo`, $c_i$ = `costo_participacion`), `grafo` (aristas $\{u,v\}$ con `peso_influencia` $w_{uv}\in[0,1]$). La profesora puede ejecutar **otros** JSON con este esquema: nada se fija en el código. Instancia de la profesora: $N=15$, $T=3$, $k=5$, $B=30$, $L=24$, $105=\binom{15}{2}$ aristas (cada par una vez). Resultados: **[RESULTADO-T06]**.
Lo que el enunciado **no** fija: forma de $u_i$, de $f$, y $q$ → D-01, D-02, D-07.

### 1.3 Parte 1 — Reparto óptimo del presupuesto
**Decisión:** cuántas unidades enteras de presupuesto recibe cada participante.

**Utilidad (D-01):** $u_i(x)=a_i\ln(1+x)$, $x\in\mathbb N$, $a_i>0$. Ganancia marginal
$$g_i(x)=u_i(x+1)-u_i(x)=a_i\ln\frac{x+2}{x+1}=a_i\ln\Bigl(1+\frac1{x+1}\Bigr).$$

**Lema 1 ($u_i$ creciente y cóncava; demostrado por nosotros).** Si $a_i>0$: $g_i(x)>0$ y $g_i$ estrictamente decreciente; $u_i(0)=0$.
*Demostración.* (1) $z(x)=1/(x+1)\in(0,1]$ es estrictamente decreciente. (2) $\ln(1+z)$ es estrictamente creciente y vale 0 en $z=0$, luego $\ln(1+z(x))>0$ y decrece en $x$. (3) Multiplicar por $a_i>0$ conserva signo y orden. (4) $g>0$ ⇒ creciente; $g$ decreciente = concavidad discreta del enunciado; $u_i(0)=a_i\ln1=0$. ■
*Observación.* Si $a_i=0$, $g\equiv0$ y el Teorema 3.1 sigue valiendo (Obs. 3.2); si $a_i<0$ el programa rechaza la entrada.

**Definición 1 (Reparto).**
- **Entrada:** conjunto $S$ de $N$ participantes (en la cadena $S=S_t$, $N=|S_t|\le k$); $a_i>0$; topes $r_i\in\mathbb N$ (D-06: $r_i=R_i$ en la ronda 1; $r_i=R_i-\sum_{s<t}x_{i,s}$ en la ronda $t$); $B\in\mathbb N$.
- **Salida:** $x\in\mathbb N^{N}$.
- **Restricciones:** $\sum_i x_i\le B$, $0\le x_i\le r_i$.
- **Objetivo:** maximizar $U(x)=\sum_i u_i(x_i)$.

*Relación con la Def. 3.2.1 del enunciado:* no trae topes; con $r_i\ge B$ se recupera exactamente. Se añaden porque el JSON trae `presupuesto_total_nodo`, total para las $T$ rondas; si son activos en el caso de la profesora: **[RESULTADO-T06]**.

**Tamaño de la entrada: $(N,B)$.** $N$ = nodos a repartir (números leídos, tamaño del montículo); $B$ = unidades a repartir (decisiones unitarias del voraz). No se reduce a una variable porque el costo es $O(N+B\log N)$. En bits la entrada mide $\Theta(N\beta+\log B)$; un costo lineal en $B$ es **pseudo-polinomial** (polinomial en el valor, exponencial en la longitud: $B=2^{\log B}$), como la mochila 0/1 por PD.

**Supuestos:** unidades enteras (D-13); utilidad separable (el grafo es variante P2); aritmética real de costo unitario incl. $\ln$ (`float64`, tolerancia $10^{-9}$ en pruebas, D-13); desempate por menor índice (D-12).
**Alcance:** voraz exacto (Alg. 1), optimalidad (Teo. 3.1), costo; sin fuerza bruta ni metaheurísticas (la PD exacta solo se usa en pruebas); caso continuo en Obs. 3.5.

### 1.4 Parte 2 — Selección de participantes
**Decisión:** qué subconjunto participa, con aportes que se **solapan**.

**Utilidad conjunta (D-02).** Familia general: $N$ candidatos, $M$ objetivos con $a_j\ge0$, $W\in[0,1]^{N\times M}$:
$$f(S)=\sum_{j=1}^M a_j\Bigl[1-\prod_{i\in S}(1-w_{ij})\Bigr],\qquad f(\emptyset)=0.$$
$w_{ij}$ = probabilidad (independiente) de que $i$ cubra al objetivo $j$; $f$ = peso esperado cubierto. **En el JSON:** $M=N$, $a_j$ = `coeficiente_utilidad`, $w_{ij}=w_{ji}$ = `peso_influencia` (D-10), $w_{ii}=1$, pares ausentes $w=0$.

**Ganancia marginal.** Con $R_j(S)=\prod_{l\in S}(1-w_{lj})\in[0,1]$ y $i\notin S$:
$$\Delta(i\mid S)=f(S\cup\{i\})-f(S)=\sum_j a_j\,w_{ij}\,R_j(S).\tag{1}$$
**Cuidado:** (1) solo vale para $i\notin S$ (si $i\in S$, $\Delta=0$ pero la fórmula da $\sum_j a_jw_{ij}(1-w_{ij})\prod_{l\in S\setminus\{i\}}(1-w_{lj})\neq0$ en general). El código debe excluir a los ya elegidos.

**Lema 2 (propiedades de $f$; demostrado por nosotros).** Si $a_j\ge0$ y $w_{ij}\in[0,1]$: (i) $f(\emptyset)=0$; (ii) monótona; (iii) submodular: $S\subseteq T$, $i\notin T$ ⇒ $\Delta(i\mid S)\ge\Delta(i\mid T)$.
*Demostración.* (1) Producto vacío = 1 ⇒ cada término es 0. (2) En (1) todos los factores son $\ge0$ ⇒ $\Delta\ge0$; agregando $T\setminus S$ uno a uno, $f$ no baja. (3) $R_j(T)=R_j(S)\prod_{l\in T\setminus S}(1-w_{lj})\le R_j(S)$ (producto extra en $[0,1]$, $R_j(S)\ge0$); multiplicar por $a_jw_{ij}\ge0$ y sumar, usando (1) (válida porque $i\notin T\supseteq S$). ■
*Observación.* Si $w_{ij}>1$ o $a_j<0$ se pierden (ii)/(iii): el programa valida ambas.

**Definición 2 (Selección).**
- **Entrada:** $N$, $M$ (=N en el JSON), $a\in\mathbb R_{\ge0}^M$, $W\in[0,1]^{N\times M}$, $1\le k<N$, $c_i\in\mathbb N$, $L\in\mathbb N$.
- **Salida:** $S\subseteq V$.
- **Restricciones (D-03):** modo `k`: $|S|\le k$; modo `costo`: $\sum_{i\in S}c_i\le L$; modo `ambos` (base): las dos.
- **Objetivo:** maximizar $f(S)$.

*"Tamaño $k$" vs "a lo sumo $k$":* en el modo `k` tienen el mismo óptimo (completar hasta $k$ no baja $f$ por monotonía; posible porque $k<N$). Con costos **no** son equivalentes (completar puede violar $L$); se usa "a lo sumo".

**Tamaño: $(N,k)$, además $M$ y $L$.** $N$ candidatos; $k$ = pasos del voraz y $\binom Nk$ de la fuerza bruta; $M$ = costo $\tau$ de una ganancia marginal; $L$ en modos con costo. En el JSON $M=N$. Leer $W$ ya cuesta $\Theta(NM)$.

**$\tau$.** Manteniendo $R_j$ (inicio 1; tras elegir $i$: $R_j\leftarrow R_j(1-w_{ij})$, $O(M)$), (1) da $\tau=\Theta(M)$ y el voraz cuesta $\Theta(kNM)$ = $\Theta(kN^2)$ con $M=N$. Evaluar $f$ desde cero ($O(|S|M)$) daría $O(Nk^2M)$.

**Supuestos:** grafo no dirigido (D-10, Q-04); influencias independientes (D-02); $q=0$ en el caso de la profesora (D-07); desempate por menor índice (D-12); candidatos de la ronda = nodos que no fallaron.
**Alcance:** NP-difícil (Sección 2); voraz con garantía $1-1/e$ **solo en el modo `k`** (Sección 3.3); fuerza bruta en instancias pequeñas. Modo `ambos`: mejor de tres voraces factibles (por ganancia, por razón ganancia/costo, mejor nodo individual), **sin garantía teórica afirmada** (R-01); razón contra el exacto (con $N=15$, $k=5$: a lo sumo $\sum_{r=1}^{5}\binom{15}{r}=4\,943$ subconjuntos no vacíos): **[RESULTADO-T06]**.

### 1.5 Supuestos (tabla)
| ID | Supuesto | Dónde |
|---|---|---|
| D-01 | $u_i(x)=a_i\ln(1+x)$ | Parte 1, Lema 1 |
| D-02 | $f$ de cobertura probabilística, $w_{ii}=1$, familia $N\times M$ | Parte 2, Lema 2, reducción |
| D-03 | Base con cupo **y** costo; modos `k`, `costo` por bandera | Def. 2 |
| D-04 | Alcance P0→P1→P2 | Entrega |
| D-05 | Python ≥3.10; numpy, scipy, matplotlib; pytest + hypothesis | Implementación |
| D-06 | Topes $r_i=R_i-$ gastado | Def. 1 |
| D-07 | $q=0$ en el caso de la profesora | Rondas |
| D-08 | Cadena Parte 2 → Parte 1 por ronda | Contexto |
| D-10 | Grafo no dirigido y simétrico | $W$ |
| D-11 | `perf_counter`, mediana de ≥5, semilla 20261105 | Validación |
| D-12 | Desempate por menor índice | Voraces |
| D-13 | $\ln$ natural, enteros, `float64` con tolerancia $10^{-9}$ | Ambas |

**Cubre esta entrega:** formalización, NP-dureza de la Parte 2, optimalidad del voraz de la Parte 1, cota $1-1/e$ aplicada a nuestra $f$, ejecución de la base en los casos (**[RESULTADO-T06]**). **Queda:** deducción completa de $T(n)$ y validación experimental con ≥5 tamaños (P1); variantes (Khuller et al. 1999, $T$ rondas con fallas, nodos relacionados) (P2).

---

## 2. NP-dureza de la selección de participantes

**Plan:** origen (Cobertura Máxima, NP-completo) → versión de decisión y pertenencia a NP → transformación $\varphi$ y su costo → equivalencia ⇒ y ⇐ → ejemplo → refuerzo para la subfamilia del JSON → conclusión.

### 2.1 Problema de origen
**CobMax-Dec.** Instancia: $U=[m]$, $S_1..S_n\subseteq U$, enteros $k,t$. ¿Existe $I\subseteq[n]$, $|I|\le k$, $|\bigcup_{i\in I}S_i|\ge t$?
**CobConj-Dec.** $U$, $S_1..S_n$, $k$: ¿existe $I$, $|I|\le k$, $\bigcup_{i\in I}S_i=U$?

**Lema 2.1 (CobMax-Dec es NP-completo).** (1) En NP: certificado $I$; unión con $m$ banderas en $O(m+\sum_{i\in I}|S_i|)\subseteq O(nm)$. (2) NP-difícil: CobConj-Dec es NP-completo — uno de los 21 problemas de Karp 1972 (*Set Covering*; lista comprobada con fuentes secundarias, texto original **[VERIFICAR]**) y el enunciado lo usa como conocido (Prop. 4.3.1). $(U,\{S_i\},k)\mapsto(U,\{S_i\},k,t=m)$ en tiempo lineal; como toda unión está en $U$, $|\bigcup|\ge m\iff\bigcup=U$. ■

### 2.2 Sel-Dec y pertenencia a NP
**Sel-Dec.** Instancia: $N\ge2$, $M\ge1$, $a_j\ge0$ racionales, $W\in([0,1]\cap\mathbb Q)^{N\times M}$, $1\le k<N$, $t$ racional. ¿Existe $A\subseteq[N]$, $|A|\le k$, $f(A)\ge t$? (Versión de decisión del modo `k`; datos racionales para tener longitud finita; el JSON trae decimales finitos.)

**Proposición 2.2 (Sel-Dec ∈ NP; demostrado por nosotros).** (1) Certificado $A$, $O(N\log N)$ bits. (2) Verificar $|A|\le k$ en $O(N)$ y calcular $f(A)$ con aritmética racional exacta en $O(|A|M)\subseteq O(NM)$ operaciones. (3) El producto de $|A|$ racionales de $\ell$ bits tiene $O(|A|\ell)$ bits; cada operación es polinomial en esa longitud ⇒ verificador polinomial. (4) $A$ se acepta sii es testigo. ■

### 2.3 Transformación $\varphi$ y su costo
**Caso borde $k\ge n$** (Sel-Dec exige $k<N$, como la Def. 3.3.1): la instancia de origen es positiva sii $|\bigcup_{i=1}^nS_i|\ge t$ (calculable en $O(nm)$). $\varphi$ devuelve una instancia fija: $Y_0$ ($N=2$, $M=1$, $a_1=1$, $w_{11}=w_{21}=0$, $k=1$, $t=0$: sí con $A=\emptyset$) o $N_0$ (iguales datos, $t=1$: $f\equiv0<1$, no).
**Caso general $k<n$:** candidato $i$ por conjunto $S_i$ ($N:=n$); objetivo por elemento ($M:=m$), $a_j:=1$; $w_{ij}:=1$ si $j\in S_i$, si no $0$; mismos $k$ y $t$; sin costos.

**Algoritmo $\varphi$** (E: $n$, $m$, listas $S_1..S_n$, $k$, $t$; S: $N,M,a,w,k,t$. Pre: $k<n$, $S_i\subseteq[m]$. Pos: la instancia descrita.)
```
1 para i = 1 hasta n
2   para j = 1 hasta m
3     w[i][j] <- 0
4   para cada e en S_i
5     w[i][e] <- 1
6 para j = 1 hasta m
7   a[j] <- 1
8 devolver (n, m, a, w, k, t)
```
| Línea | Instrucción | Ejecuciones | Subtotal |
|---|---|---|---|
| 1 | para i (cabeza) | $n+1$ | $c_1(n+1)$ |
| 2 | para j (cabeza) | $n(m+1)$ | $c_2n(m+1)$ |
| 3 | $w\gets0$ | $nm$ | $c_3nm$ |
| 4 | para cada $e$ (cabeza) | $\sum_i(\lvert S_i\rvert+1)\le n(m+1)$ | $\le c_4n(m+1)$ |
| 5 | $w\gets1$ | $\sum_i\lvert S_i\rvert\le nm$ | $\le c_5nm$ |
| 6 | para j (cabeza) | $m+1$ | $c_6(m+1)$ |
| 7 | $a\gets1$ | $m$ | $c_7m$ |
| 8 | devolver | 1 | $c_8$ |

De adentro hacia afuera: $T_\varphi\le\alpha nm+\beta n+\gamma m+\delta$; la línea 3 corre exactamente $nm$ veces ⇒ $T_\varphi(n,m)\in\Theta(nm)=\Theta(N\cdot|U|)$; con el caso borde sigue $O(N|U|)$. **Polinomial.**

### 2.4 Equivalencia
**Lema 2.3 ($f$ construida = cobertura; demostrado por nosotros).** En $\varphi(X)$ con $k<n$, $\forall A\subseteq[n]$: $f(A)=|\bigcup_{i\in A}S_i|$.
*Dem.* (1) $1-w_{ij}=0$ si $j\in S_i$, $=1$ si no. (2) Un producto de factores en $\{0,1\}$ es 0 sii algún factor es 0: $\prod_{i\in A}(1-w_{ij})=0\iff\exists i\in A:j\in S_i\iff j\in\bigcup_{i\in A}S_i$ ($A=\emptyset$: producto 1, unión vacía: coincide). (3) Corchete = indicador de $j\in\bigcup$. (4) Con $a_j=1$, $f(A)=|\bigcup|$. ■

**Teorema 2.4 (equivalencia; demostrado por nosotros).** $X$ positiva ⇔ $\varphi(X)$ positiva.
*Caso $k\ge n$:* $\varphi(X)=Y_0$ exactamente cuando $|\bigcup_{i=1}^nS_i|\ge t$, que es exactamente cuando $X$ es positiva (tomar todos maximiza la unión); si no, $N_0$ y $X$ negativa.
*Caso $k<n$* (candidato $i$ ↔ $S_i$):
(⇒) $\exists I$, $|I|\le k$, $|\bigcup_{i\in I}S_i|\ge t$. (1) $A:=I$, $|A|\le k$. (2) Lema 2.3: $f(A)=|\bigcup|\ge t$. (3) $\varphi(X)$ positiva.
(⇐) $\exists A$, $|A|\le k$, $f(A)\ge t$. (1) $I:=A$, $|I|\le k$. (2) Lema 2.3: $|\bigcup_{i\in I}S_i|=f(A)\ge t$. (3) $X$ positiva.
Misma correspondencia y mismo lema en ambos sentidos: el valor objetivo es idéntico para cada subconjunto. ■

**Corolario 2.5.** Sel-Dec es NP-completo (CobMax-Dec $\le_p$ Sel-Dec en $O(N|U|)$ + Prop. 2.2). ■

### 2.5 Ejemplo a mano
$U=\{1,..,5\}$, $S_1=\{1,2,3\}$, $S_2=\{3,4\}$, $S_3=\{4,5\}$, $S_4=\{1,5\}$, $k=2$, $t=5$ ($k<n=4$). $N=4$, $M=5$, $a=(1,1,1,1,1)$,
$$W=\begin{pmatrix}1&1&1&0&0\\0&0&1&1&0\\0&0&0&1&1\\1&0&0&0&1\end{pmatrix}.$$
$A=\{1,3\}$: productos por columna $(1-1)(1-0)=0$, $(0)(1)=0$, $(0)(1)=0$, $(1)(0)=0$, $(1)(0)=0$ ⇒ $f=5$. $A=\{1,2\}$: la columna 5 da $(1)(1)=1$ ⇒ $f=4$.

| $A$ | $\bigcup$ | $\lvert\bigcup\rvert$ | $f(A)$ |
|---|---|---|---|
| {1,2} | {1,2,3,4} | 4 | 4 |
| {1,3} | {1,2,3,4,5} | 5 | 5 |
| {1,4} | {1,2,3,5} | 4 | 4 |
| {2,3} | {3,4,5} | 3 | 3 |
| {2,4} | {1,3,4,5} | 4 | 4 |
| {3,4} | {1,4,5} | 3 | 3 |

(⇒) $I=\{1,3\}$ cubre $U$ y $f(\{1,3\})=5\ge5$. (⇐) el único $A$ con $|A|\le2$ y $f\ge5$ es $\{1,3\}$ (tamaño 1: $|S_i|\le3$) ↔ $I=\{1,3\}$. Ambas positivas.
**Negativa:** mismos conjuntos, $k=1$, $t=4$: $|S_i|\le3<4$ y $f(\{i\})=|S_i|\le3$. Ambas negativas.

### 2.6 Refuerzo: la subfamilia del JSON también es dura
**Proposición 2.6 (demostrado por nosotros).** Sel-Dec sigue NP-completo con $M=N$, $W$ simétrica 0/1, $w_{ii}=1$, $a_j>0$.
*Dem.* $X$ con $k<n$ (si $k\ge n$, instancias fijas que cumplen la restricción: $N=2$, $W=I_2$, $a=(1,1)$, $k=1$, $t=0$ o $t=3$).
(1) *Limpieza:* $U'=\bigcup_iS_i$; quitar $U\setminus U'$ no cambia ninguna unión ⇒ misma respuesta; $O(nm)$.
(2) *Construcción:* bipartito $s_1..s_n$, $e_1..e_{m'}$; $N=M=n+m'$; diagonal 1; $w_{s_ie_j}=w_{e_js_i}=1$ sii $j\in S_i$; $a(e_j)=1$, $a(s_i)=\varepsilon=1/(n+1)$; mismos $k,t$; $O((n+m)^2)$.
(3) Un vértice queda cubierto sii está en $A$ o tiene un vecino en $A$. $f(A)=C(A)+\varepsilon D(A)$ ($C$ = elementos cubiertos, $D$ = conjuntos cubiertos), $0\le\varepsilon D<1$.
(4) (⇒) $A=\{s_i:i\in I\}$ cubre cada $e_j$ con $j\in\bigcup_{i\in I}S_i$ ⇒ $f(A)\ge C(A)\ge t$.
(5) (⇐) $f(A)\ge t$ ⇒ $C(A)>t-1$ ⇒ $C(A)\ge t$ (enteros). $I$: cada $s_i\in A$ aporta $i$; cada $e_j\in A$ aporta un $i(j)$ con $j\in S_{i(j)}$ (existe por (1)). $|I|\le|A|\le k$ y todo $e_j$ cubierto está en $\bigcup_{i\in I}S_i$ ⇒ $|\bigcup|\ge t$.
(6) NP por la Prop. 2.2. ■
*Observación:* prueba la dureza del **esquema** (cualquier grafo, pesos en $[0,1]$), no de la instancia de 15 nodos, que es finita y se resuelve por fuerza bruta.

### 2.7 Consecuencias y conclusión
**Corolario 2.7 (demostrado por nosotros).** (a) La optimización (modo `k`) es NP-difícil: resolverla en tiempo polinomial decidiría Sel-Dec comparando $f(S^*)$ con $t$. (b) Modos `costo` ($c_i=1$, $L=k$) y `ambos` ($c_i=0$, $L=0$) contienen al modo `k` ⇒ NP-difíciles. (c) NP-difícil **en sentido fuerte**: en $\varphi(X)$ todos los números están acotados por $\max(n,m)$ ⇒ no hay algoritmo pseudo-polinomial salvo P=NP (definición según Garey–Johnson 1979, **[VERIFICAR]** página).

**Conclusión.** **Componente NP-difícil: la Parte 2** (los tres modos, incluida la subfamilia del esquema JSON) ⇒ voraz con garantía $1-1/e$ (modo `k`) y fuerza bruta solo en instancias pequeñas. **Parte 1:** exacta en $O(N+B\log N)$, polinomial en $N$ y pseudo-polinomial en $B$; no se afirma nada sobre su dureza en bits. No hay contradicción: la dificultad está en *a quién elegir*, no en *cuánto dar*.

---

## 3. Algoritmos base: optimalidad, costo y garantía

### 3.1 Parte 1: el voraz por ganancia marginal es óptimo
**Algoritmo 1 — Reparto.** E: $N$; E: $a[1..N]$ real; E: $r[1..N]$ entero; E: $B$; S: $x[1..N]$. Pre: $N\ge1$, $a_i>0$, $r_i,B\in\mathbb N$. Pos: $\sum x_i\le B$, $0\le x_i\le r_i$, $U(x)$ máxima.
```
 1 para i = 1 hasta N
 2   x[i] <- 0
 3 H <- arreglo vacío
 4 para i = 1 hasta N
 5   si r[i] > 0
 6     agregar (g_i(0), i) al final de H
 7 ConstruirMontículoMáx(H)        // mayor g; empate, menor i (D-12)
 8 b <- 0
 9 mientras b < B y H no vacío
10   (g, i) <- ExtraerMáx(H)
11   x[i] <- x[i] + 1 ; b <- b + 1
12   si x[i] < r[i]
13     Insertar(H, (g_i(x[i]), i))
14 devolver x
```
Notación: $x^{(j)}$ tras $j$ iteraciones; $U(y)=\sum_i\sum_{s<y_i}g_i(s)$ (porque $u_i(0)=0$); $e_p$ vector unitario.

**Teorema 3.1 (optimalidad con topes; demostrado por nosotros).** Si $u_i(0)=0$ y $g_i$ es positiva y no creciente, el Algoritmo 1 termina tras $J=\min(B,\sum_ir_i)$ iteraciones y devuelve un óptimo.
*Dem.* Invariante de lazo + intercambio. Existe óptimo (conjunto factible finito y no vacío).
**Invariante $\mathcal I(j)$:** (a) $x^{(j)}$ factible y $b=\sum x^{(j)}=j$; (b) $H$ = exactamente los $i$ con $x_i^{(j)}<r_i$, una vez cada uno, con clave $g_i(x_i^{(j)})$; (c) existe un óptimo $y\ge x^{(j)}$.
**Inicialización:** $x=0$, $b=0$; líneas 4–6 insertan los $i$ con $r_i>0$ y la 7 solo reordena; todo óptimo es $\ge0$.
**Mantenimiento** ($x=x^{(j-1)}$, $p$ extraído):
1. Por (b), $x_p<r_p$ y $g_p(x_p)=\max\{g_i(x_i):x_i<r_i\}$. $x^{(j)}=x+e_p$ factible; $p$ se reinserta con $g_p(x_p+1)$ si $x_p+1<r_p$ ⇒ (a), (b).
2. Caso A: $y_p>x_p$ ⇒ $y\ge x^{(j)}$.
3. Caso B: $y_p=x_p$. Si $\sum y<B$, $y+e_p$ es factible y mejora en $g_p(x_p)>0$: contradicción. Luego $\sum y=B$.
4. $\sum y=B\ge j>j-1=\sum x$ e $y\ge x$ ⇒ $\exists q$, $y_q>x_q$; $q\ne p$.
5. **$q$ era candidato:** $x_q<y_q\le r_q$ ⇒ $q\in H$ ⇒ $g_q(x_q)\le g_p(x_p)$.
6. $y'=y-e_q+e_p$ factible: misma suma; $y'_p=x_p+1\le r_p$; $y'_q=y_q-1\ge x_q\ge0$.
7. $U(y')-U(y)=g_p(x_p)-g_q(y_q-1)\ge0$ porque $g_q(y_q-1)\le g_q(x_q)\le g_p(x_p)$ (concavidad y paso 5) ⇒ $y'$ óptimo.
8. $y'\ge x^{(j)}$ ⇒ (c).
**Terminación:** cada iteración sube $b$ y baja $\sum(r_i-x_i)\ge0$; sale con $b=B$ o $H=\emptyset$ (todos $x_i=r_i$) ⇒ $J=\min(B,\sum r_i)$. Si $b=B$: $\sum y\le B=\sum x$ e $y\ge x$ ⇒ $y=x$. Si $H=\emptyset$: $r_i\ge y_i\ge x_i=r_i$ ⇒ $y=x$. ■

**Obs. 3.2 (hipótesis).** Concavidad: paso 7. $g>0$: solo paso 3 (con $g\ge0$, $y+e_p$ también es óptimo ⇒ sigue valiendo). Topes: paso 5 (que $q$ siga en el montículo lo garantiza $y_q\le r_q$). Desempates: no se usan.
**Contraejemplo 3.3 (sin concavidad).** $B=2$, $g_1=(1,10)$, $g_2=(2,1)$. Voraz: nodo 2 (2>1), luego empate 1 vs 1 → nodo 1: utilidad 3. Óptimo $(2,0)$: 11. Falla el paso 7.
**Obs. 3.4 (prueba alternativa).** Todo reparto toma prefijos de las listas decrecientes $g_i(0)\ge g_i(1)\ge\dots$, a lo sumo $B$ elementos del multiconjunto $G$; con todo positivo, $U\le$ suma de los $\min(B,|G|)$ mayores; el voraz siempre toma la cabeza mayor, que es el máximo de lo no tomado ⇒ alcanza la cota.

**Costo.** $N'=|\{i:r_i>0\}|$, $J=\min(B,\sum r_i)\le B$, $|H|\le N$ siempre (invariante (b)). Montículo binario (Notas §3.1; CLRS cap. 6): construir $O(|H|)$; extraer/insertar $O(1+\log|H|)$. Aritmética (incl. $\ln$) de costo unitario.

| Línea | Instrucción | Ejecuciones | Costo c/u |
|---|---|---|---|
| 1 | para i (cabeza) | $N+1$ | $c_1$ |
| 2 | $x\gets0$ | $N$ | $c_2$ |
| 3 | $H\gets\emptyset$ | 1 | $c_3$ |
| 4 | para i (cabeza) | $N+1$ | $c_4$ |
| 5 | si $r_i>0$ | $N$ | $c_5$ |
| 6 | agregar | $N'$ | $c_6$ |
| 7 | ConstruirMontículoMáx | 1 | $\le c_7N'$ |
| 8 | $b\gets0$ | 1 | $c_8$ |
| 9 | mientras (cabeza) | $J+1$ | $c_9$ |
| 10 | ExtraerMáx | $J$ | $\le c_{10}(1+\log N)$ |
| 11 | incrementos | $J$ | $c_{11}$ |
| 12 | si $x_i<r_i$ | $J$ | $c_{12}$ |
| 13 | Insertar | $\le J$ | $\le c_{13}(1+\log N)$ |
| 14 | devolver | 1 | $c_{14}$ |

$T(N,B)\le\alpha N+\beta B(1+\log N)+\gamma$ ⇒ $T(N,B)\in O(N+B\log N)$. Mejor caso ($B=0$ o $r\equiv0$): $\Theta(N)$. Peor caso: $J=B$ y montículo $\Theta(N)$. Espacio $\Theta(N)$. Deducción completa con constantes del código: T10.
**Pseudo-polinomial:** la entrada mide $\Theta(N\beta+\log B)$ bits pero hay hasta $B=2^{\log B}$ iteraciones; duplicar los bits de $B$ eleva $B$ al cuadrado.
**Obs. 3.5 (water-filling, esbozo; T11).** Con $x_i\in[0,r_i]$ reales: problema cóncavo con restricciones lineales, KKT suficiente. $a_i/(1+x_i)=\lambda$ ⇒ $x_i(\lambda)=\min\{r_i,\max\{0,a_i/\lambda-1\}\}$. Si $\sum r_i\le B$, $x=r$; si no, $\lambda>0$ con $\sum x_i(\lambda)=B$. $\sum x_i(\lambda)$ es continua, no creciente, lineal a trozos en $1/\lambda$ con $2N$ quiebres ($a_i$ y $a_i/(1+r_i)$): ordenar y recorrer $O(N\log N)$, **independiente de $B$**.

### 3.2 Parte 2: voraz y su costo
**Algoritmo 2 — VorazSelección (modo `k`).** E: $N,M,k$, $a[1..M]$, $w[1..N][1..M]$; S: $S$. Pre: $1\le k<N$, $a\ge0$, $w\in[0,1]$. Pos: $|S|=k$, salida del voraz (desempate menor índice).
```
 1 para j = 1 hasta M
 2   R[j] <- 1
 3 S <- {} ; enS[1..N] <- falso
 4 para t = 1 hasta k
 5   gmax <- -inf ; mejor <- 0
 6   para i = 1 hasta N
 7     si no enS[i]
 8       d <- 0
 9       para j = 1 hasta M
10         d <- d + a[j]*w[i][j]*R[j]
11       si d > gmax
12         gmax <- d ; mejor <- i
13   S <- S ∪ {mejor} ; enS[mejor] <- verdadero
14   para j = 1 hasta M
15     R[j] <- R[j]*(1 - w[mejor][j])
16 devolver S
```
**Invariante** (antes de la iteración $t$ de la línea 4): $|S|=t-1$, $R_j=\prod_{l\in S}(1-w_{lj})$. Inicialización: producto vacío. Mantenimiento: líneas 6–12 calculan $d=\Delta(i\mid S)$ por (1) para $i\notin S$ y guardan el primero máximo (">" estricto); siempre hay candidato ($N-t+1\ge2$, $d\ge0>-\infty$); 13–15 restablecen el invariante. Terminación: $|S|=k$.
**Costo de adentro hacia afuera.** $P$ = ejecuciones de la línea 8 $=\sum_{t=1}^k(N-t+1)=kN-\frac{k(k-1)}2$; con $k\le N-1$: $\frac{kN}2<P\le kN$.

| Líneas | Instrucción | Ejecuciones | Subtotal |
|---|---|---|---|
| 1–2 | inicializar $R$ | $(M+1)+M$ | $\Theta(M)$ |
| 3 | inicializar $S$, enS | 1 | $\Theta(N)$ |
| 4 | para t (cabeza) | $k+1$ | $\Theta(k)$ |
| 5 | gmax, mejor | $k$ | $\Theta(k)$ |
| 6–7 | para i (cabeza), si no enS | $k(N+1)+kN$ | $\Theta(kN)$ |
| 8 | $d\gets0$ | $P$ | $\Theta(kN)$ |
| 9–10 | para j (cabeza) y acumulación | $P(M+1)+PM$ | $\Theta(kNM)$ |
| 11–12 | comparar/actualizar | $\le2P$ | $O(kN)$ |
| 13 | agregar | $k$ | $\Theta(k)$ |
| 14–15 | actualizar $R$ | $k(M+1)+kM$ | $\Theta(kM)$ |

Dominante: línea 10, exactamente $P\cdot M$ veces ⇒ $T(N,k,M)\in\Theta(kNM)$; $\tau=\Theta(M)$ (líneas 8–10). **JSON ($M=N$): $\Theta(kN^2)$.** Espacio $\Theta(NM)$ (entrada) + $\Theta(N+M)$.
**Fuerza bruta:** $\sum_{r\le k}\binom Nr$ subconjuntos × $O(rM)$; con $k\le N/2$, $\sum_{r\le k}\binom Nr\le(k+1)\binom Nk$: exponencial si $k\propto N$. En modo `k` bastan los de tamaño exactamente $k$.

### 3.3 Cota $1-1/e$ (modo `k`)
**Teorema 3.6 (Nemhauser–Wolsey–Fisher 1978, citado; prueba estándar escrita por nosotros).** (H1) $f(\emptyset)=0$; (H2) monótona; (H3) submodular; (H4) solo $|S|\le k$, $1\le k\le N$. El voraz de $k$ pasos (cualquier desempate) cumple $f(S_k)\ge[1-(1-\frac1k)^k]\,\mathrm{OPT}\ge(1-\frac1e)\mathrm{OPT}\approx0.632\,\mathrm{OPT}$.
*Dem.* $O$ óptimo, $\delta_t=\mathrm{OPT}-f(S_t)$.
1. $\mathrm{OPT}=f(O)\le f(O\cup S_t)$ (H2).
2. $O\setminus S_t=\{o_1..o_r\}$, $r\le k$: $f(O\cup S_t)-f(S_t)=\sum_m\Delta(o_m\mid S_t\cup\{o_1..o_{m-1}\})\le\sum_m\Delta(o_m\mid S_t)$ (H3).
3. Cada $o_m\notin S_t$ era candidato: $\Delta(o_m\mid S_t)\le f(S_{t+1})-f(S_t)$, que es $\ge0$ (H2) ⇒ $r\cdot(\cdot)\le k\cdot(\cdot)$.
4. $\mathrm{OPT}\le f(S_t)+k[f(S_{t+1})-f(S_t)]$ ⇔ $\delta_{t+1}\le(1-\frac1k)\delta_t$.
5. $\delta_0=\mathrm{OPT}$ (H1) ⇒ $\delta_k\le(1-\frac1k)^k\mathrm{OPT}$.
6. $1-z\le e^{-z}$ ⇒ $(1-\frac1k)^k\le e^{-1}$. ■

**Aplicación a nuestra $f$:** (H1)–(H3) = Lema 2 ($a>0$, $w\in[0,1]$, validados); (H4) = modo `k`; el Algoritmo 2 da $k$ pasos de máxima ganancia ($k<N$) ⇒ **garantía $1-1/e$ en el modo `k`**. Verificación empírica contra fuerza bruta (familias sintéticas, porque el caso de la profesora se satura, R-02): **[RESULTADO-T12]**; razón en el caso de la profesora: **[RESULTADO-T06]**.

**Obs. 3.7 (si falla una hipótesis).** (H1): si $f(\emptyset)=c>0$ la cota vale para $f-c$. (H3): $V=\{1,2,3\}$, $f(S)=10\cdot\mathbf 1[\{1,2\}\subseteq S]+\mathbf 1[3\in S]$, $k=2$: voraz elige 3 y luego 1 → $f=1$; $\mathrm{OPT}=10$; razón $0.1$. (H4): costos, $f(\{1\})=2$, $c_1=1$; $f(\{2\})=L$, $c_2=L\ge3$; voraz por razón toma 1 y ya no cabe 2: $2$ vs $L$, razón $2/L\to0$ ⇒ por eso Khuller et al. 1999 toma el mejor con el mejor nodo individual; **para `ambos` no se afirma garantía** (R-01): **[RESULTADO-T06]**.
**Contraejemplo 3.8 (el voraz de la Parte 2 no es óptimo).** $U=\{1..6\}$, $S_1=\{1,2,3,4\}$, $S_2=\{1,2,5\}$, $S_3=\{3,4,6\}$, $k=2$: voraz $S_1$ (4), luego empate 1–1 → $S_2$: $f=5$. Óptimo $S_2\cup S_3$: 6. Razón $5/6\ge1-(1/2)^2=0.75$.
**Obs. 3.9.** Feige 1998: para Cobertura Máxima ninguna razón $1-1/e+\varepsilon$ en tiempo polinomial salvo P=NP (verificado a nivel de resumen). Como Cobertura Máxima es caso particular (Lema 2.3), la cota es la mejor posible en general.

---

## Referencias
- [enunciado] L. E. Guerrero. *Proyecto Semestral ADA 2026-B*, cap. 3 (pp. 10–12) y Prop. 4.3.1 (p. 14). U. de Caldas, 2026.
- [notas] *ADA — Notas de clase 2024-A* (§2.1, §2.3, §3.1). U. de Caldas, 2024.
- [villegas2016] E. Villegas Jaramillo, L. Guerrero Mendieta. *Análisis y Diseño de Algoritmos: un enfoque práctico*. Ed. U. Nacional, 2016.
- [clrs] Cormen, Leiserson, Rivest, Stein. *Introduction to Algorithms*, 4.ª ed., MIT Press, 2022, cap. 6.
- [karp1972] R. M. Karp. Reducibility among combinatorial problems. En *Complexity of Computer Computations*, pp. 85–103, Plenum, 1972. (Lista de 21 problemas comprobada con fuentes secundarias; original **[VERIFICAR]**.)
- [gj1979] M. R. Garey, D. S. Johnson. *Computers and Intractability*. W. H. Freeman, 1979. **[VERIFICAR]** página de dureza fuerte.
- [nwf1978] G. L. Nemhauser, L. A. Wolsey, M. L. Fisher. An analysis of approximations for maximizing submodular set functions—I. *Math. Programming* 14(1):265–294, 1978. (Resumen comprobado.)
- [fnw1978] M. L. Fisher, G. L. Nemhauser, L. A. Wolsey. … —II. *Math. Programming Study* 8:73–87, 1978. (No usada aquí.)
- [feige1998] U. Feige. A threshold of ln n for approximating set cover. *JACM* 45(4):634–652, 1998. (Resumen comprobado.)
- [kmn1999] S. Khuller, A. Moss, J. Naor. The budgeted maximum coverage problem. *IPL* 70(1):39–45, 1999.
