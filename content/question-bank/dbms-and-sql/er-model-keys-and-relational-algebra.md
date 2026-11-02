---
title: "ER model, keys and relational algebra"
weight: 4
---

1 question asked by MathWorks. Try each one first, then open the toggle: it gives the answer, why it is right, and the idea behind it explained from scratch.

### 1 · Q25, counting super keys

*Asked by: MathWorks (IISc 2024)*

$R(A, B, C, D, E)$ has candidate keys $AB$ and $BC$. How many super keys does $R$ have?

- **(a)** 8
- **(b)** 12
- **(c)** 9
- **(d)** 15

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) 12**

**Why.** A super key is any set containing a candidate key. Supersets of AB: the other 3 attributes (C, D, E) are free, 2³ = 8. Supersets of BC: likewise 8. Supersets of both (containing ABC): D and E free, 2² = 4, counted twice. 8 + 8 − 4 = 12.

**Concept: keys.** Super key: uniquely identifies a row. Candidate key: a minimal super key. Primary key: the candidate key chosen. Count super keys with inclusion–exclusion over the candidate keys.

{{< /details >}}
