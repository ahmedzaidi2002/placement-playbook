---
title: "Linear algebra"
weight: 5
---

1 question asked by MathWorks. Try each one first, then open the toggle: it gives the answer, why it is right, and the idea behind it explained from scratch.

### 1 · Q16, perpendicular unit vector

*Asked by: MathWorks (IISc 2024)*

A unit vector perpendicular to both $\mathbf a = \mathbf i + 2\mathbf j + \mathbf k$ and
$\mathbf b = \mathbf j + 2\mathbf k$ is:

- **(a)** $\pm(3\mathbf i - 2\mathbf j + 2\mathbf k)/\sqrt2$
- **(b)** $\pm(3\mathbf i - 2\mathbf j + \mathbf k)/\sqrt{14}$
- **(c)** $\pm(3\mathbf i + 3\mathbf j + \mathbf k)/\sqrt{19}$
- **(d)** $\pm(3\mathbf i - 2\mathbf j + \mathbf k)/\sqrt2$

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) ±(3i − 2j + k)/√14**

**Why.** A vector perpendicular to both a and b is their cross product: a × b = (2·2 − 1·1)i − (1·2 − 1·0)j + (1·1 − 2·0)k = 3i − 2j + k. Its length is √(9 + 4 + 1) = √14; divide to get a unit vector, with ± for both directions.

**Concept: cross product.** a × b is perpendicular to both a and b. Unit vector = vector ÷ its length. Quick check: (3, −2, 1)·(1, 2, 1) = 3 − 4 + 1 = 0 ✓.

{{< /details >}}
