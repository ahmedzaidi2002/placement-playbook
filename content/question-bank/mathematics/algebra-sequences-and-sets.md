---
title: "Algebra, sequences and sets"
weight: 3
---

5 questions asked by ION Group, MathWorks, Sigmoid. Try each one first, then open the toggle: it gives the answer, why it is right, and the idea behind it explained from scratch.

### 1 · Q1, a recursive sequence

*Asked by: ION Group (SDE OA, Jul 2025)*

A sequence is defined by $a_1 = 2$ and $a_{n+1} = a_n^2 - a_n + 1$. What is the 4th term?

- **(a)** 7
- **(b)** 13
- **(c)** 49
- **(d)** 97

{{< details title="Answer and explanation" closed="true" >}}

**Answer: none of the options; the 4th term is 43.** (Option (a), 7, is the 3rd term, probably what the setter meant if they counted from a₀.)

**Why.** a₁ = 2; a₂ = 4 − 2 + 1 = 3; a₃ = 9 − 3 + 1 = 7; a₄ = 49 − 7 + 1 = 43.

**Concept: recursive sequences.** A recurrence defines each term from the previous one. Compute term by term and keep careful count of the index. (This is Sylvester's sequence 2, 3, 7, 43, 1807, ..., where each term is one more than the product of all earlier terms.)

{{< /details >}}

### 2 · Q7, log 9 from log 27

*Asked by: ION Group (SDE OA, Jul 2025)*

If $\log 27 = 1.431$, what is the value of $\log 9$?

- **(a)** 0.934
- **(b)** 0.945
- **(c)** 0.954
- **(d)** 0.958

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) 0.954**

**Why.** 27 = 3³, so log 27 = 3 log 3 → log 3 = 1.431/3 = 0.477. 9 = 3², so log 9 = 2 × 0.477 = 0.954.

**Concept: log of a power.** log(aⁿ) = n log a. Write both numbers as powers of the same base (here 3) and the logs become multiples of one value.

{{< /details >}}

### 3 · Q9, integers with |x - 2| at most 3

*Asked by: ION Group (SDE OA, Jul 2025)*

What is the cardinality of the set of integers that satisfy $|x - 2| \le 3$?

- **(a)** 7
- **(b)** 5
- **(c)** 6
- **(d)** 4

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) 7**

**Why.** |x − 2| ≤ 3 means −3 ≤ x − 2 ≤ 3, i.e. −1 ≤ x ≤ 5. The integers are −1, 0, 1, 2, 3, 4, 5: seven of them.

**Concept: absolute-value inequalities.** |x − a| ≤ r means x is within distance r of a: a − r ≤ x ≤ a + r. Count integers in [p, q] as q − p + 1.

{{< /details >}}

### 4 · Q2, geometric series

*Asked by: MathWorks (IIT Bombay 2024)*

$\displaystyle\sum_{i \ge 0} (2/7)^i = $

- **(a)** 7/2
- **(b)** 5/7
- **(c)** 2/7
- **(d)** 7/5

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) 7/5**

**Why.** 1 + 2/7 + (2/7)² + ... = 1/(1 − 2/7) = 1/(5/7) = 7/5.

**Concept: infinite geometric series.** a + ar + ar² + ... = a/(1 − r) when |r| < 1. Here a = 1 (the i = 0 term) and r = 2/7.

{{< /details >}}

### 5 · set difference

*Asked by: Sigmoid (Campus hiring 2026)*

$A = \{8, 15, 26, 78, 90, 36, 79, 29\}$ and $B = \{98, 15, 67, 75, 78, 90, 34, 29\}$ (as
far as the photo can be read). Determine $A - B$.

- **(a)** {15, 90, 74, 29}
- **(b)** {8, 26, 36, 79}
- **(c)** {98, 67, 75, 34}
- **(d)** {90, 79, 34, 15}

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) {8, 26, 36, 79}**

**Why.** A − B keeps the elements of A that are not in B. 15, 78, 90 and 29 are in both, so they go; 8, 26, 36, 79 remain.

**Concept: set difference.** A − B = {x : x ∈ A and x ∉ B}. It is not symmetric: B − A would be {98, 67, 75, 34}, option (c), a trap.

{{< /details >}}
