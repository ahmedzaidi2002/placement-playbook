---
title: "2 · Boolean algebra, gates and K-maps"
linkTitle: "2 Boolean algebra"
weight: 2
math: true
---
## 2.1 Gates {#coa-2-1}

| Gate | Output 1 when | Expression |
|---|---|---|
| AND | all inputs 1 | $AB$ |
| OR | any input 1 | $A + B$ |
| NOT | input 0 | $\overline{A}$ |
| NAND | not all 1 | $\overline{AB}$ |
| NOR | all 0 | $\overline{A + B}$ |
| XOR | inputs differ (odd number of 1s) | $A \oplus B = A\overline{B} + \overline{A}B$ |
| XNOR | inputs equal | $\overline{A \oplus B}$ |

**Universal gates:** NAND alone (or NOR alone) can build any circuit. NOT = NAND with both inputs tied; AND = NAND + NOT (2 gates); OR = 3 NANDs; **XOR = 4 NANDs** (or 5 NORs).

## 2.2 Laws of Boolean algebra {#coa-2-2}

| Law | AND form | OR form |
|---|---|---|
| Identity | $A \cdot 1 = A$ | $A + 0 = A$ |
| Null | $A \cdot 0 = 0$ | $A + 1 = 1$ |
| Idempotent | $AA = A$ | $A + A = A$ |
| Complement | $A\overline{A} = 0$ | $A + \overline{A} = 1$ |
| Absorption | $A(A + B) = A$ | $A + AB = A$ |
| Distributive | $A(B + C) = AB + AC$ | $A + BC = (A + B)(A + C)$ |
| **De Morgan** | $\overline{AB} = \overline{A} + \overline{B}$ | $\overline{A + B} = \overline{A}\,\overline{B}$ |

Also: $A + \overline{A}B = A + B$, and the **consensus theorem** $AB + \overline{A}C + BC = AB + \overline{A}C$.

**Duality:** swap AND ↔ OR and 0 ↔ 1 and an identity stays true.

<div class="nb nb-example">

<strong>Example</strong> (Simplify)

$AB + A\overline{B} + \overline{A}B = A(B + \overline{B}) + \overline{A}B = A + \overline{A}B = $ **$A + B$**.

</div>

## 2.3 Canonical forms {#coa-2-3}

- **Minterm** $m_i$: an AND of all variables, true for exactly one input combination. **SOP** (sum of products): $F = \sum m(\dots)$, listing where $F = 1$.
- **Maxterm** $M_i$: an OR term, false for exactly one combination. **POS**: $F = \prod M(\dots)$, listing where $F = 0$.
- The two lists are complements: $\sum m(1, 3, 5, 7) = \prod M(0, 2, 4, 6)$ for three variables.

## 2.4 Karnaugh maps {#coa-2-4}

Arrange the truth table so neighbouring cells differ in one variable (Gray-code order 00, 01, 11, 10, with wrap-around at the edges). Group 1s in rectangles of size 1, 2, 4, 8 (as large as possible, overlaps allowed, fewest groups). Each group gives one product term; the variables that change inside the group disappear.

<div class="nb nb-example">

<strong>Example</strong> (4-variable K-map)

$F(A, B, C, D) = \sum m(0, 1, 2, 5, 8, 9, 10)$.

| $AB \backslash CD$ | 00 | 01 | 11 | 10 |
|---|---|---|---|---|
| **00** | 1 (m0) | 1 (m1) | 0 | 1 (m2) |
| **01** | 0 | 1 (m5) | 0 | 0 |
| **11** | 0 | 0 | 0 | 0 |
| **10** | 1 (m8) | 1 (m9) | 0 | 1 (m10) |

Groups: the four **corners** (0, 2, 8, 10) → $\overline{B}\,\overline{D}$; the block 0, 1, 8, 9 → $\overline{B}\,\overline{C}$; the pair 1, 5 → $\overline{A}\,\overline{C}D$.

$$F = \overline{B}\,\overline{D} + \overline{B}\,\overline{C} + \overline{A}\,\overline{C}D.$$

</div>

**Don't-cares** (X) may be grouped as 1s if that makes groups bigger, and ignored otherwise. For more than 5–6 variables use the **Quine–McCluskey** tabular method.

## 2.5 Hazards {#coa-2-5}

A **static-1 hazard** is a momentary 0 glitch when the output should stay 1, because two adjacent 1-groups are not covered by a common term and gate delays differ. Fix: add the **redundant consensus term** covering the transition.

<div class="nb nb-moral">

NAND and NOR are universal. De Morgan: break the bar, change the sign. K-maps: group 1s in powers of two, wrap around edges, largest groups first.

</div>
