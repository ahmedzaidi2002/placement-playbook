---
title: "Arrays and 2-D arrays"
weight: 10
---

1 question asked by Qualcomm. Try each one first, then open the toggle: it gives the answer, why it is right, and the idea behind it explained from scratch.

### 1 · C Programming

*Asked by: Qualcomm (60-question online assessment)*

a[3][3] is equivalent to which of the given pointer notation?

- **(a)** `**(a + 6)`
- **(b)** `**(a + 9)`
- **(c)** `*(a + 3) + 3`
- **(d)** `*(*(a + 3) + 3)`

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) `*(*(a + 3) + 3)`**

**Why.** For a 2-D array, `a[i][j]` is defined as `*(*(a + i) + j)`. With i = j = 3 this is `*(*(a + 3) + 3)`.

**Concept: array indexing is pointer arithmetic.** `x[k]` means `*(x + k)`. In a 2-D array, `a + i` points to row i (a whole row), `*(a + i)` is that row, which decays to a pointer to its first element, `+ j` moves j elements along, and the outer `*` reads the value. Options (a)–(c) skip one dereference or add to the wrong level.

{{< /details >}}
