---
title: "Probability and statistics for ML"
weight: 7
---

1 question asked by Qualcomm. Try each one first, then open the toggle: it gives the answer, why it is right, and the idea behind it explained from scratch.

### 1 · Q52, correlation

*Asked by: Qualcomm (IISc)*

A researcher reports a correlation of $r = -0.5$. Which statement is correct?

- **(a)** The x-variable explains 75% of the variability in y.
- **(b)** The x-variable explains 25% of the variability in y.
- **(c)** The x-variable explains -25% of the variability in y.
- **(d)** The x-variable explains -75% of the variability in y.

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) 25%**

**Why.** The fraction of variance in y explained by a linear fit on x is r² = (−0.5)² = 0.25. It is never negative; the sign of r only tells the direction of the relationship.

**Concept: correlation and R².** r ranges from −1 to 1 (strength and direction of a linear relationship). R² = r² for simple linear regression: the share of variance explained.

{{< /details >}}
