---
title: "2 · Recursion, divide and conquer, backtracking"
linkTitle: "2 Recursion, divide and conquer, backtracking"
weight: 2
math: true
---
## 2.1 Recursion and the call stack {#sec-dsa-callstack}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> naive `fib(30)` makes $2.7$ million calls to compute $832040$.</em>

</div>

<div class="nb nb-definition" id="definition-2-1-1">

<strong>Definition 2.1.1</strong>. A function is <strong>recursive</strong> if it calls itself on a smaller instance. It needs a <strong>base case</strong> that stops the recursion and a <strong>recursive case</strong> that makes progress towards it. Each active call owns a <strong>stack frame</strong> (arguments, locals, return address), so the space used is proportional to the maximum <em>depth</em> of the recursion.

</div>

The program `recursion.cpp` counts the calls of the textbook Fibonacci function, uses merge sort to count inversions, and uses backtracking to count $N$-queens solutions; the three parts are shown in this chapter where they are explained.

```cpp {filename="recursion.cpp, lines 5–6"}
long calls = 0;
long fib(int n) { ++calls; return n < 2 ? n : fib(n - 1) + fib(n - 2); }
```

```text {filename="Output of recursion.cpp"}
fib(10) = 55 needs 177 calls
fib(20) = 6765 needs 21891 calls
fib(30) = 832040 needs 2692537 calls
inversions in [29 10 14 37 13 5 41 8] = 16
 4-queens:    2 solutions,      17 search-tree nodes
 5-queens:   10 solutions,      54 search-tree nodes
 6-queens:    4 solutions,     153 search-tree nodes
 7-queens:   40 solutions,     552 search-tree nodes
 8-queens:   92 solutions,    2057 search-tree nodes
 9-queens:  352 solutions,    8394 search-tree nodes
10-queens:  724 solutions,   35539 search-tree nodes
```

<div class="nb nb-example nb-block" id="example-2-1-2">

<strong>Example 2.1.2</strong> (Why naive Fibonacci is exponential)

The number of calls $C(n)$ satisfies $C(n) = C(n-1) + C(n-2) + 1$ with $C(0) = C(1) = 1$, whose solution is $C(n) = 2F(n+1) - 1$: $2 \cdot 89 - 1 = 177$ for $n = 10$, matching the output. Since $F(n) \approx \varphi^n/\sqrt5$ with $\varphi \approx 1.618$, the time is $\Theta(\varphi^n)$. The same values are recomputed again and again: `fib(30)` calls `fib(2)` $F(29) = 514229$ times. Remembering them (memoisation) makes it $\Theta(n)$; this is the entire idea of dynamic programming ([Chapter 15](../15-dp/)). The <em>depth</em> is only $n$, so the space is $\Theta(n)$ even for the exponential version.

</div>

<div class="nb nb-remark" id="remark-2-1-3">

<strong>Remark 2.1.3</strong> (Stack overflow) — Each frame costs tens of bytes or more, and a default thread stack is about $1$ MB (Windows) or $8$ MB (Linux main thread). A recursive DFS on a path of $10^6$ vertices therefore overflows. The fixes are an explicit stack, or <strong>tail recursion</strong>: if the recursive call is the last action of the function, the compiler <em>may</em> reuse the frame (<strong>tail-call optimisation</strong>). C and C++ compilers often do this with optimisation on; Java and CPython never do, so do not rely on it in an interview answer.

</div>

<div class="nb nb-definition" id="fact-2-1-4">

<strong>Fact 2.1.4</strong> (Recursion versus iteration). Every recursion can be turned into a loop with an explicit stack, and every loop into a tail recursion. Recursion is natural for trees, divide and conquer and backtracking; iteration avoids call overhead and stack limits.

</div>

## 2.2 Divide and conquer {#sec-dsa-dc}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> merge sort: split in half, sort each half, merge in linear time.</em>

</div>

<div class="nb nb-remark" id="algorithm-2-2-1">

<strong>Algorithm 2.2.1</strong> (Divide and conquer) — <em>Divide</em> the problem into $a$ subproblems of size $n/b$, <em>conquer</em> them recursively, <em>combine</em> the answers. The running time obeys $T(n) = a\,T(n/b) + (\text{divide} + \text{combine cost})$, solved by the Master theorem ([Section 1.5](../01-complexity/#sec-dsa-recurrences)).

</div>

| Algorithm | Recurrence | Time | Idea |
|:--|:--|:--|:--|
| Binary search | $T(n/2) + 1$ | $\Theta(\log n)$ | discard half |
| Merge sort | $2T(n/2) + n$ | $\Theta(n \log n)$ | linear merge |
| Quicksort (balanced) | $2T(n/2) + n$ | $\Theta(n \log n)$ | linear partition |
| Counting inversions | $2T(n/2) + n$ | $\Theta(n \log n)$ | count while merging |
| Maximum subarray | $2T(n/2) + n$ | $\Theta(n \log n)$ | best sum crossing the middle (Kadane’s scan does it in $\Theta(n)$) |
| Closest pair of points | $2T(n/2) + n$ | $\Theta(n \log n)$ | strip of width $2\delta$ |
| Karatsuba multiplication | $3T(n/2) + n$ | $\Theta(n^{1.585})$ | 3 products instead of 4 |
| Strassen matrix product | $7T(n/2) + n^2$ | $\Theta(n^{2.81})$ | 7 products instead of 8 |
| Fast exponentiation | $T(n/2) + 1$ | $\Theta(\log n)$ | $x^n = (x^{n/2})^2$ |

<div class="nb-caption" id="table-2-1">

<strong>Table 2.1.</strong> Standard divide-and-conquer algorithms.

</div>

### 2.2.i Counting inversions {#s2-2-i}

<div class="nb nb-definition" id="definition-2-2-2">

<strong>Definition 2.2.2</strong>. An <strong>inversion</strong> of an array is a pair $i < j$ with $a_i > a_j$. A sorted array has none; a reversed one has $n(n-1)/2$, the maximum.

</div>

Merge sort counts them for free: when the merge takes an element from the right half, that element jumps over every element still waiting in the left half, so add their number.

```cpp {filename="recursion.cpp, lines 8–22"}
long inv = 0;
void sortCount(std::vector<int>& a, int lo, int hi) {         // a[lo..hi)
    if (hi - lo < 2) return;
    int mid = (lo + hi) / 2;
    sortCount(a, lo, mid); sortCount(a, mid, hi);
    std::vector<int> t;
    int i = lo, j = mid;
    while (i < mid && j < hi) {
        if (a[j] < a[i]) { inv += mid - i; t.push_back(a[j++]); }   // a[j] jumps over mid-i elements
        else t.push_back(a[i++]);
    }
    while (i < mid) t.push_back(a[i++]);
    while (j < hi) t.push_back(a[j++]);
    for (int k = lo; k < hi; ++k) a[k] = t[k - lo];
}
```

The output above reports $16$ inversions for `[29 10 14 37 13 5 41 8]`, which is also exactly the number of shifts insertion sort makes on that array ([Section 13.2.iii](../13-sorting/#sec-dsa-insertion)).

### 2.2.ii Karatsuba, Strassen, closest pair {#s2-2-ii}

<div class="nb nb-example nb-block" id="example-2-2-3">

<strong>Example 2.2.3</strong> (Karatsuba: three multiplications instead of four)

Split two $n$-digit numbers as $x = x_1 B + x_0$, $y = y_1 B + y_0$. Then $xy = x_1y_1 B^2 + (x_1y_0 + x_0y_1) B + x_0y_0$, and the middle term equals $(x_1 + x_0)(y_1 + y_0) - x_1y_1 - x_0y_0$. Three half-size products plus linear work give $T(n) = 3T(n/2) + \Theta(n) = \Theta(n^{\log_2 3}) \approx \Theta(n^{1.585})$ instead of the schoolbook $\Theta(n^2)$. Strassen plays the same trick on $2 \times 2$ block matrices with $7$ products instead of $8$: $\Theta(n^{\log_2 7})$.

</div>

<div class="nb nb-remark" id="algorithm-2-2-4">

<strong>Algorithm 2.2.4</strong> (Closest pair in $O(n \log n)$) — Sort the points by $x$, split at the median line, solve both halves recursively and let $\delta$ be the smaller answer. A closer pair must straddle the line within distance $\delta$ of it. In that strip, sorted by $y$, each point needs to be compared only with a constant number (at most $7$) of the following points, because a $\delta \times 2\delta$ rectangle holds at most $8$ points that are pairwise at least $\delta$ apart. Combining is linear if the $y$-order is maintained by merging, so $T(n) = 2T(n/2) + \Theta(n)$.

</div>

<div class="nb nb-moral">

Divide and conquer wins when the combine step is cheaper than solving the whole problem directly; the recurrence tells you by how much.

</div>

## 2.3 Backtracking {#sec-dsa-backtracking}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> placing $8$ queens so that none attacks another: $92$ solutions among $2057$ partial placements tried.</em>

</div>

<div class="nb nb-definition" id="definition-2-3-1">

<strong>Definition 2.3.1</strong>. <strong>Backtracking</strong> builds a solution one choice at a time, depth first, and abandons a partial solution (<strong>prunes</strong>) as soon as it cannot be completed. The partial solutions form the <strong>state-space tree</strong>.

</div>

```cpp {filename="recursion.cpp, lines 24–36"}
int n, solutions;
long nodes;
std::vector<bool> col, d1, d2;
void place(int r) {
    ++nodes;
    if (r == n) { ++solutions; return; }
    for (int c = 0; c < n; ++c)
        if (!col[c] && !d1[r + c] && !d2[r - c + n]) {
            col[c] = d1[r + c] = d2[r - c + n] = true;
            place(r + 1);
            col[c] = d1[r + c] = d2[r - c + n] = false;
        }
}
```

The output above shows how much pruning buys: the $8$-queens search visits $2057$ nodes, while the unpruned tree with one queen per row in any column has $\sum_{k=0}^{8} 8^k \approx 1.9 \times 10^7$ nodes.

<div class="nb nb-definition" id="fact-2-3-2">

<strong>Fact 2.3.2</strong> (Sizes of state spaces).

- All subsets of $n$ items: $2^n$ leaves; enumerating them costs $\Theta(n 2^n)$ if each subset is printed.
- All permutations: $n!$ leaves, $\Theta(n \cdot n!)$ to print.
- All $k$-subsets: $\binom nk$; all balanced parenthesis strings of length $2n$: the Catalan number $C_n$ ([Section 6.5](../06-trees/#sec-dsa-catalan)).
- $N$-queens with one queen per row: at most $n!$ leaves; the solution counts $2, 10, 4, 40, 92, 352, 724$ for $n = 4, \ldots, 10$ are in the output above.

The time of a backtracking algorithm is (number of nodes visited) $\times$ (work per node), and good pruning changes only the first factor.

</div>

<div class="nb nb-remark" id="remark-2-3-3">

<strong>Remark 2.3.3</strong> (Backtracking versus branch and bound versus DP) — Backtracking prunes <em>infeasible</em> partial solutions; <strong>branch and bound</strong> also prunes <em>feasible but provably worse</em> ones using a bound on the best completion (used for TSP and integer programming). If different branches keep reaching the <em>same</em> subproblem, memoise it: that is dynamic programming.

</div>

## 2.4 A few harder problems to think about {#s2-4}

<div class="nb nb-problem nb-block" id="problem-2a">

<strong>Problem 2A</strong> 🌶🌶 (Calls of a recursive function)

How many times is `f` called by `f(5)`, where `int f(int n){ if (n <= 1) return 1; return f(n-1) + f(n-2) + f(n-3); }`? (Calls with $n \le 1$, including `f(-1)`, count.)

<details class="nb-hint">
<summary>Hint</summary>

Let $C(n)$ be the number of calls; $C(n) = 1 + C(n-1) + C(n-2) + C(n-3)$ for $n \ge 2$ and $C(n) = 1$ for $n \le 1$.

</details>

<details class="nb-sol">
<summary>Solution</summary>

$C(-1) = C(0) = C(1) = 1$, $C(2) = 4$, $C(3) = 7$, $C(4) = 13$, $C(5) = 25$.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-2b">

<strong>Problem 2B</strong> (Unequal split)

A divide-and-conquer algorithm recurses on parts of size $n/5$ and $7n/10$ and does linear extra work. What is its running time? Which famous algorithm is it?

<details class="nb-hint">
<summary>Hint</summary>

$1/5 + 7/10 < 1$: the level totals shrink geometrically.

</details>

<details class="nb-sol">
<summary>Solution</summary>

The level sums are $n, 0.9n, 0.81n, \ldots$, a geometric series, so $T(n) = \Theta(n)$. It is median of medians, deterministic linear-time selection ([Section 13.12](../13-sorting/#sec-dsa-selection)).

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-2c">

<strong>Problem 2C</strong> (Stack depth)

What is the maximum recursion depth of merge sort on $n = 10^6$ elements? Of quicksort with the last element as pivot on an already sorted array of the same size?

<details class="nb-hint">
<summary>Hint</summary>

One halves; the other peels off one element per call.

</details>

<details class="nb-sol">
<summary>Solution</summary>

Merge sort: $\lceil \log_2 10^6 \rceil = 20$ levels. Quicksort on sorted input recurses on a part of size $n - 1$ each time: depth about $10^6$, which overflows a default stack unless it recurses on the smaller part and loops on the larger.

</details>

</div>
