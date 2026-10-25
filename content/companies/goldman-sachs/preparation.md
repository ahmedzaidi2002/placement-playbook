---
title: Preparation style
weight: 5
---

What the account says to prepare, plus the revision material behind each item. Items from the account are marked **Reported**; the tables and formulas are an **editor's addition**.

## The overall style

- **Reported:** do well in any two of the three test sections, and score high overall. Test score sets your interview order.
- **Reported:** DSA revision goes a long way. The programming section asked direct questions on complexity and on stack-based expressions.
- **Reported:** revise **Probability and Statistics** and **Linear Algebra** if time permits.
- **Reported:** ML theory helps a lot in the data science section.
- **Reported:** in interviews, talk to the panel all the time. They help you when you are stuck.
- **Reported:** prepare good and genuine reasons for a low CPI.
- **Reported:** do not fake an interest in finance or markets. Build a real habit of following them.

## Programming

### Complexities to have memorised

| Algorithm / structure | Time |
|---|---|
| Binary search | $O(\log n)$ |
| Merge sort | $O(n \log n)$ always |
| Quick sort | $O(n \log n)$ average, $O(n^2)$ worst case |
| Heap sort | $O(n \log n)$ |
| Build a heap | $O(n)$ |
| BFS / DFS | $O(V + E)$ |
| Dijkstra with a binary heap | $O((V + E) \log V)$ |
| Kruskal | $O(E \log E)$ |
| Hash table lookup | $O(1)$ average, $O(n)$ worst case |
| Balanced BST operations | $O(\log n)$ |
| Postfix / prefix evaluation | $O(n)$ with a stack |

### Also revise

- Stack applications: expression evaluation and conversion.
- Reading constraints to choose the right complexity before writing code.
- Computational geometry basics: convex hull and the cross product.
- Searching in sorted matrices and other "exploit the ordering" problems.

## Quant

### Probability and statistics

$$\operatorname{Var}(X) = E[X^2] - (E[X])^2$$

$$\operatorname{Cov}(X, Y) = E[XY] - E[X]\,E[Y]$$

$$\rho_{X,Y} = \frac{\operatorname{Cov}(X, Y)}{\sigma_X\,\sigma_Y}$$

- Expectation is linear, even for dependent variables: $E[X + Y] = E[X] + E[Y]$.
- A fair die has $E[X] = 3.5$. For $n$ dice, the sum has expectation $3.5\,n$.
- For independent variables, covariance is zero. The reverse is not true.
- Normal distribution: know the mean, variance and the 68–95–99.7 rule.

### Linear algebra

- Determinant properties: swapping two rows flips the sign, adding a multiple of a row to another leaves it unchanged, and a zero determinant means the matrix is singular.
- Rank, and what a rank-1 matrix looks like.

### Aptitude

- Area and geometry problems such as the grazing-field question.
- Counting outcomes for dice problems.

## Data Science

For the "what to do about missing data" style of question, the standard menu is:

| Option | When it fits |
|---|---|
| Drop rows or columns | Few values are missing and they are missing at random |
| Mean / median / mode imputation | Quick baseline; median is safer with outliers |
| KNN or model-based imputation | Missingness depends on other features |
| Add a "was missing" indicator | The fact that a value is missing carries signal |

Also know the missingness types (missing completely at random, at random, not at random), the basics of the libraries in scikit-learn, and be able to explain each ML project on your resume end to end.

## Interview conduct

- Start simple and improve. The sorted-matrix question rewarded walking from brute force to the best answer, as long as you reach it.
- Ask for a hint rather than going silent.
- Be punctual, rested and honest.

{{< callout type="info" >}}
**Editor's note.** The account recommends revision areas but does not give a time plan. How long to spend on each is left to you.
{{< /callout >}}
