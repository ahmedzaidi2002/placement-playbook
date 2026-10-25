---
title: Questions asked
weight: 4
---

Every question the candidate reported, grouped by where it came up. **Reported** is what was asked; **Approach** is an editor's addition to help you practise it.

## Online test

### Programming

| Reported | Approach |
|---|---|
| Time complexity of well-known algorithms | Know the table in [Preparation](../preparation#complexities-to-have-memorised) cold. |
| Prefix and postfix expressions | Evaluate with a stack: scan postfix left to right, push operands, and on an operator pop two and push the result. Prefix is the same scanned right to left. Conversion between forms also uses a stack. |
| 2 coding questions where a plain solution may time out | Read the constraints first and pick the complexity they allow before coding. |

### Quant

| Reported | Approach |
|---|---|
| Cattle tied to a pole with a rope, grazing a circular field | A geometry area problem: draw the reachable region (a circle of rope-length radius around the pole) and intersect it with the field. Compute the overlap area. |
| Dice rolling probability | Count favourable outcomes over $6^n$ for $n$ dice. Use symmetry or a short DP over sums. |
| Expectation, covariance, correlation | See the formulas in [Preparation](../preparation#probability-and-statistics). |
| Matrix and determinant problems | Row operations, determinant properties, and what a determinant of zero implies. |

### Data Science

| Reported | Approach |
|---|---|
| What to do to compensate for missing data | Know the options and when each applies: see [Preparation](../preparation#data-science). |
| Four statements, pick the correct ones | Check each statement independently; one wrong word makes it false. |

## Interviews

### Convex hull

> Write code to connect points so the closed figure has the least area and encloses all the given points.

This is the **convex hull**. The standard answer is Andrew's monotone chain, which runs in $O(n \log n)$:

1. Sort the points by x, then y.
2. Build the lower hull by scanning left to right and popping the last point while the last two points and the new one do not make a counter-clockwise turn (cross product $\le 0$).
3. Build the upper hull the same way from right to left.
4. Join the two, dropping the duplicated end points.

The candidate was caught off guard at 6 AM. The takeaway: know the standard computational-geometry problems by name.

### The number game to 20

> Two players pick a number from 1 to 3 in turn. Whoever reaches 20 first wins. What is the strategy?

Work backwards, as the candidate described. Reaching **20** wins. To make that certain, you want to be on **16**: the opponent then moves to 17, 18 or 19 and you finish. The same argument puts **12**, **8** and **4** as safe positions too.

So the winning positions are the multiples of 4 below 20, and the rule is: **answer an opponent's move of k with 4 − k**. If the game starts from 0 with the other player moving first, you can always keep the running total on a multiple of 4. (Assumption: players alternate adding 1, 2 or 3 to a shared running total.)

### Variance and the Gaussian

Reported only as "calculating variance" and "Gaussian distribution". Know $\operatorname{Var}(X) = E[X^2] - (E[X])^2$ and the mean, variance and shape of the normal distribution.

### The matrix with row² and e^column

> Each element of a matrix is the sum of its row number squared and e raised to its column number. Prove something about the equality of sums of elements, then generalise to a function of row and column numbers.

The candidate does not recall the exact claim, so there is no worked solution here. What is certain is the structure: the entry in row $i$, column $j$ is $a_{ij} = i^2 + e^{j}$, a sum of a row-only term and a column-only term. Any matrix of the form $f(i) + g(j)$ has the property that the difference between two rows is the same in every column, and its rank is at most 2. That is likely the lever behind the generalisation, but treat it as a hint about the style, not as the actual problem.

### The two carts

> Two carts sit on a track with a sensor below them. You can start a cart with a chosen speed, but afterwards you only have control while a cart is over the sensor. Once it leaves, you have none. How do you make them collide?

The candidate could not articulate the problem at first, and the interviewers helped them reach what they called a simple answer. The reported advice: talk to the panel throughout. No solution was recorded.

### Project-based questions

- Yelp dataset challenge and the NLP in the candidate's AI project.
- Basic scikit-learn library questions.
- The stock-market flash crash, linked to an internship project.
- Interest in finance and global markets.

### Data structures, then sorted-matrix search

The first question was a data-structures question; the candidate gave a high-complexity answer, then a lower one that was wrong, then a **tree-based approach** that was not the intended solution, though the interviewer could not find a flaw in it.

The second was searching a **matrix sorted by rows and by columns** for an element:

| Approach | Time |
|---|---|
| Check every cell | $O(mn)$ |
| Binary search in each row | $O(m \log n)$ |
| **Staircase search**: start at the top-right (or bottom-left) corner. If the value is larger than the target, move left; if smaller, move down | $O(m + n)$ |

The candidate went through the first two on their own and needed a hint for the last, which they then solved starting from the bottom-left instead of the top-right. Both corners work because each has one direction that increases and the other that decreases.
