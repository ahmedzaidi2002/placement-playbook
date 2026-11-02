---
title: "Discrete mathematics, graphs and number theory"
weight: 1
---

9 questions asked by MathWorks, Qualcomm, Texas Instruments. Try each one first, then open the toggle: it gives the answer, why it is right, and the idea behind it explained from scratch.

### 1 · Q1, k-regular graphs

*Asked by: MathWorks (IIIT Delhi 2024)*

How many edges does a $k$-regular graph on $n$ vertices have?

- **(a)** $n \times k$
- **(b)** $(n \times k)/2$
- **(c)** $n + k$
- **(d)** $n^2 - k^2$

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) nk/2**

**Why.** Each of the n vertices has degree k, so the degrees add to nk. Every edge has two ends and is counted twice in that sum, so edges = nk/2.

**Concept: handshake lemma.** Sum of all degrees = 2 × number of edges. (So in any graph, the number of odd-degree vertices is even.)

{{< /details >}}

### 2 · Q6, remainder modulo 17

*Asked by: MathWorks (IIIT Delhi 2024)*

What is the remainder when $2^{2021}$ is divided by 17?

- **(a)** 1
- **(b)** 2
- **(c)** 7
- **(d)** 15

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) 15**

**Why.** 2⁴ = 16 ≡ −1 (mod 17), so 2⁸ ≡ 1. 2021 = 8 × 252 + 5, so 2²⁰²¹ ≡ 2⁵ = 32 ≡ 15 (mod 17).

**Concept: modular exponent cycles.** Find a small power that is ≡ 1 (or −1); then powers repeat with that period, and you only need the exponent's remainder.

{{< /details >}}

### 3 · Q20, a remainder

*Asked by: MathWorks (IISc 2024)*

What is the remainder when $2^{100}$ is divided by 101?

- **(a)** 1
- **(b)** 2
- **(c)** 50
- **(d)** 100

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) 1**

**Why.** 101 is prime and does not divide 2, so by Fermat's little theorem 2¹⁰⁰ ≡ 1 (mod 101).

**Concept: Fermat's little theorem.** If p is prime and p does not divide a, then a^(p−1) ≡ 1 (mod p). It turns huge powers into easy remainders.

{{< /details >}}

### 4 · Q11, linear Diophantine equations

*Asked by: MathWorks (IIT Bombay 2024)*

For $ax + by = c$ with $g = \gcd(a, b)$ dividing $c$, the solutions for $x$ are:

- **(a)** $x \equiv (c/g)(b/g) \pmod{a/g}$
- **(b)** $x \equiv (c/g)(a/g)^{-1} \pmod{b/g}$
- **(c)** $x \equiv (c/g)(a/g) \pmod{b/g}$
- **(d)** $x \equiv (c/g)(b/g)^{-1} \pmod{a/g}$

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) x ≡ (c/g)(a/g)⁻¹ (mod b/g)**

**Why.** Divide ax + by = c by g: (a/g)x + (b/g)y = c/g. Taken modulo b/g, the y term disappears: (a/g)x ≡ c/g. Since a/g and b/g share no factors, a/g has an inverse modulo b/g, so x ≡ (c/g)(a/g)⁻¹.

**Concept: linear Diophantine equations.** ax + by = c has integer solutions exactly when gcd(a, b) divides c. The x-values repeat every b/g. The modular inverse a⁻¹ (mod m) exists when gcd(a, m) = 1, and is found by the extended Euclidean algorithm.

{{< /details >}}

### 5 · Q6, digit sum of a power of two

*Asked by: MathWorks (IIT Bombay 2024)*

The sum of the digits of $2^{100}$ is:

- **(a)** 5
- **(b)** 7
- **(c)** 9
- **(d)** 11

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) 7** (as the repeated digit sum; the plain digit sum is 115, not an option)

**Why.** The digit sum is congruent to the number mod 9. 2⁶ = 64 ≡ 1 (mod 9), and 100 = 6 × 16 + 4, so 2¹⁰⁰ ≡ 2⁴ = 16 ≡ 7 (mod 9). The repeated digit sum (digital root) is 7. Check: the actual digit sum is 115, and 1 + 1 + 5 = 7.

**Concept: digital root = value mod 9.** Adding a number's digits repeatedly until one digit remains gives n mod 9 (with 9 instead of 0). Useful for checking big arithmetic.

{{< /details >}}

### 6 · Q1, posets

*Asked by: MathWorks (NIT Delhi 2024)*

Which property is NOT obeyed by a POSET?

- **(a)** Reflexivity
- **(b)** Transitivity
- **(c)** Anti-symmetry
- **(d)** Symmetry

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) symmetry**

**Why.** A partial order (like ≤ or "divides") is reflexive (a ≤ a), antisymmetric (a ≤ b and b ≤ a means a = b) and transitive. Symmetry (a ≤ b implies b ≤ a) would make it an equivalence relation instead. The candidate's "anti-symmetry" is wrong.

**Concept: relation properties.**
- Equivalence relation: reflexive, symmetric, transitive (e.g. "same remainder mod 5").
- Partial order: reflexive, antisymmetric, transitive (e.g. ⊆, ≤, divides).

{{< /details >}}

### 7 · Q6, $T(n) = 2T(n-1) + n$

*Asked by: MathWorks (IIITDM Kancheepuram 2025)*

Solve $T(1) = 1$, $T(n) = 2T(n-1) + n$ for $n \ge 2$.

- **(a)** $2^{n+1} - n - 2$
- **(b)** $2^n - n$
- **(c)** $2^{n+1} - 2n - 2$
- **(d)** (not visible)

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) 2ⁿ⁺¹ − n − 2**

**Why.** Check T(1) = 4 − 1 − 2 = 1 ✓. Check the recurrence: 2T(n − 1) + n = 2(2ⁿ − (n − 1) − 2) + n = 2ⁿ⁺¹ − 2n − 2 + n = 2ⁿ⁺¹ − n − 2 ✓. Neat derivation: set U(n) = T(n) + n + 2; then U(n) = 2U(n − 1), so U doubles each step from U(1) = 4, giving U(n) = 2ⁿ⁺¹.

**Concept: verify by substitution.** For MCQs on recurrences, plug each option into the base case and the recurrence; the one that satisfies both is the answer. To solve T(n) = 2T(n − 1) + n, absorb the extra term with a shift (T + n + 2) that turns it into pure doubling.

{{< /details >}}

### 8 · Q53, bond of a graph

*Asked by: Qualcomm (IISc)*

If $F$ is a bond (a minimal non-empty edge cut) of a connected graph $G$, find $c(G - F)$, the
number of components of $G - F$.

- **(a)** 2
- **(b)** 3
- **(c)** 6
- **(d)** 4

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) 2**

**Why.** Removing a cut disconnects G. If removing a bond F left three or more components, the edges of F between just two of those components would already disconnect G, a smaller cut, contradicting that F is minimal. So exactly 2 components.

**Concept: cuts and bonds.** An edge cut is a set of edges whose removal disconnects the graph. A bond is a minimal one: removing any edge from it makes it no longer a cut. Bonds always split a connected graph into exactly two pieces.

{{< /details >}}

### 9 · branches of a network graph

*Asked by: Texas Instruments (NIT Calicut 2023)*

A network graph has 10 nodes and 4 independent loops. Branches?

- **(a)** 11
- **(b)** 13
- **(c)** 14
- **(d)** 12

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) 13**

**Why.** For a connected network, independent loops = branches − nodes + 1. So branches = loops + nodes − 1 = 4 + 10 − 1 = 13.

**Concept: graph theory for circuits.** A spanning tree of n nodes has n − 1 branches. Each extra branch closes one independent loop. So loops = b − (n − 1). This counts the independent mesh equations in circuit analysis.

{{< /details >}}
