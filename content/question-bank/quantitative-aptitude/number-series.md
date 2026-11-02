---
title: "Number series"
weight: 19
---

3 questions asked by Accenture, Texas Instruments. Try each one first, then open the toggle: it gives the answer, why it is right, and the idea behind it explained from scratch.

### 1 · Q46-50, number series

*Asked by: Accenture (Previous year)*

(46) 992, 1056, ?, 1190, 1260, 1332 [1112 / 1082 / 1134 / 1092 / none] (47) 15625, 6250, 2500,
1000, ?, 160 [600 / 400 / 500 / 650 / none] (48) 80, 370, ?, 1550, 2440, 3530 [900 / 840 / 750
/ 860 / none] (49) 15, 51, 216, 1100, ?, 46452 [6630 / 6650 / 6560 / 6530 / none]
(50) 24, 28, 36, 52, 84, ? [144 / 135 / 148 / 140 / none]

{{< details title="Answer and explanation" closed="true" >}}

**Answers: (46) none of these (the term is 1122) (47) 400 (48) 860 (49) 6630 (50) 148**

**Why.**
- (46) Differences 64, 66, 68, 70, 72: 1056 + 66 = 1122, not listed.
- (47) Each term is 0.4 times the last: 1000 × 0.4 = 400, then 160.
- (48) Differences rise by 200: 290, 490, 690, 890, 1090: 370 + 490 = 860.
- (49) ×3 + 6, ×4 + 12, ×5 + 20, ×6 + 30, ×7 + 42: 1100 × 6 + 30 = 6630.
- (50) Differences double: 4, 8, 16, 32, 64: 84 + 64 = 148.

**Concept: how to attack a number series.** Try, in order: (1) differences, and the differences of differences; (2) ratios between terms; (3) "× n + something" where n grows; (4) two interleaved series. Check the rule on every term, not just the first two.

{{< /details >}}

### 2 · series 17, 24, 33, 44

*Asked by: Texas Instruments (BITS Pilani)*

17, 24, 33, 44, $X$?

- **(a)** 55
- **(b)** 57
- **(c)** 66
- **(d)** 65

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) 57**

**Why.** Differences: 24 − 17 = 7, 33 − 24 = 9, 44 − 33 = 11. Next difference 13: 44 + 13 = 57.

**Concept: second differences.** When the gaps between terms themselves grow by a constant (here 2), the series is quadratic. Extend the gap pattern and add.

{{< /details >}}

### 3 · series 6, 13, X, 57, 131

*Asked by: Texas Instruments (IISc, second set)*

Find $X$ in 6, 13, $X$, 57, 131.

- **(a)** 31
- **(b)** 49
- **(c)** 47
- **(d)** 35

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) 31**

**Why.** Each term is (prime)² plus an even number: 2² + 2 = 6, 3² + 4 = 13, 5² + 6 = 31, 7² + 8 = 57, 11² + 10 = 131.

**Concept: series built on primes.** If differences (7, ?, ?, 74) look random, test special sequences: squares, cubes, primes. Here the base is the primes 2, 3, 5, 7, 11, squared, with 2, 4, 6, 8, 10 added. Always verify the rule on the last given term (131) before trusting it.

{{< /details >}}
