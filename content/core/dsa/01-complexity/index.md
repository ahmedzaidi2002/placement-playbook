---
title: "1 · Complexity analysis"
linkTitle: "1 Complexity"
weight: 1
math: true
---
## 1.1 Asymptotic notation {#dsa-1-1}

| Notation | Meaning | Think |
|---|---|---|
| $O(g)$ | grows **at most** like $g$ (upper bound) | ≤ |
| $\Omega(g)$ | grows **at least** like $g$ (lower bound) | ≥ |
| $\Theta(g)$ | grows **exactly** like $g$ (both) | = |

Constants and lower-order terms are dropped: $3n^2 + 10n + 5 = \Theta(n^2)$.

**Growth order:** $1 < \log n < \sqrt{n} < n < n\log n < n^2 < n^3 < 2^n < n! < n^n$.

**Best, worst, average case** are separate questions: quicksort is $O(n \log n)$ on average but $O(n^2)$ in the worst case. "Big-O" usually means the worst case unless stated.

<div class="nb nb-remark">

<strong>Trap</strong> — $O$ is not "worst case" and $\Omega$ is not "best case". They are bounds on a function; you can state an upper bound on the best case. Also, $\log_2 n$ and $\log_{10} n$ differ only by a constant, so the base does not matter inside $O$.

</div>

## 1.2 Counting loops {#dsa-1-2}

| Loop | Iterations | Complexity |
|---|---|---|
| `for i in 1..n` | $n$ | $O(n)$ |
| `for i in 1..n: for j in 1..n` | $n^2$ | $O(n^2)$ |
| `for i in 1..n: for j in 1..i` | $n(n+1)/2$ | $O(n^2)$ |
| `i = 1; while i < n: i *= 2` | $\log_2 n$ | $O(\log n)$ |
| `for i in 1..n: (j = 1; j < n; j *= 2)` | $n \log n$ | $O(n \log n)$ |
| `for i in 1..n: for j = i; j <= n; j += i` | $n/1 + n/2 + \dots + n/n$ | $O(n \log n)$ (harmonic) |
| `while n > 1: n = sqrt(n)` | $\log \log n$ | $O(\log \log n)$ |

Sequential blocks **add** (keep the biggest); nested loops **multiply**.

## 1.3 Recurrences and the Master theorem {#dsa-1-3}

<div class="nb nb-theorem nb-block">

<strong>Master theorem</strong> for $T(n) = a\,T(n/b) + f(n)$

Compare $f(n)$ with $n^{\log_b a}$:

1. $f(n)$ smaller (polynomially) → $T(n) = \Theta(n^{\log_b a})$.
2. Equal ($f(n) = \Theta(n^{\log_b a})$) → $T(n) = \Theta(n^{\log_b a} \log n)$.
3. $f(n)$ bigger (and regular) → $T(n) = \Theta(f(n))$.

</div>

<div class="nb nb-example">

<strong>Example</strong> (Recurrences you must know)

| Recurrence | Algorithm | Solution |
|---|---|---|
| $T(n) = 2T(n/2) + n$ | merge sort | $\Theta(n \log n)$ (case 2) |
| $T(n) = T(n/2) + 1$ | binary search | $\Theta(\log n)$ (case 2) |
| $T(n) = 2T(n/2) + 1$ | tree traversal | $\Theta(n)$ (case 1) |
| $T(n) = 8T(n/2) + n^2$ | naive matrix multiply | $\Theta(n^3)$ (case 1) |
| $T(n) = 7T(n/2) + n^2$ | Strassen | $\Theta(n^{\log_2 7}) \approx n^{2.81}$ |
| $T(n) = 2T(n/2) + n^2$ | | $\Theta(n^2)$ (case 3) |
| $T(n) = T(n-1) + n$ | selection/insertion sort | $\Theta(n^2)$ (not master: sum) |
| $T(n) = T(n-1) + 1$ | linear recursion | $\Theta(n)$ |
| $T(n) = 2T(n-1) + 1$ | Tower of Hanoi | $\Theta(2^n)$ |

</div>

Other methods: the **recursion tree** (add the cost of each level) and **substitution** (guess and prove by induction).

## 1.4 Space complexity {#dsa-1-4}

Extra memory used, not counting the input. Recursion uses **stack space** equal to the recursion depth: recursive binary search uses $O(\log n)$, the iterative version $O(1)$; merge sort uses $O(n)$ extra; quicksort $O(\log n)$ stack on average.

## 1.5 Amortized analysis {#dsa-1-5}

The **average cost per operation over a worst-case sequence** (not an average over random inputs).

<div class="nb nb-example">

<strong>Example</strong> (Dynamic array)

A vector doubles its capacity when full. Pushing $n$ items copies $1 + 2 + 4 + \dots + n/2 < n$ elements in total, so $n$ pushes cost $O(n)$: **$O(1)$ amortized** per push, even though one push occasionally costs $O(n)$.

</div>

Other examples: stack with multipop, union-find with path compression, hash-table rehashing.

## 1.6 Pseudo-polynomial time {#dsa-1-6}

An algorithm running in $O(nW)$, like 0/1 knapsack's DP, looks polynomial but is **pseudo-polynomial**: $W$ is a number in the input, and its size in bits is only $\log W$. Doubling the number of bits of $W$ squares the running time.

**Lower bound:** any comparison-based sort needs $\Omega(n \log n)$ comparisons (a decision tree with $n!$ leaves has height $\ge \log_2 n!$).

<div class="nb nb-moral">

Nested loops multiply, sequential ones add, halving gives log. Master theorem: compare f(n) with n^(log_b a). Amortized = total cost of a worst-case sequence divided by its length.

</div>
