---
title: "15 · Dynamic programming"
linkTitle: "15 Dynamic programming"
weight: 15
math: true
---
## 15.1 What dynamic programming is {#sec-dsa-dpidea}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> `fib(30)`: $2.7$ million calls naively, $31$ distinct subproblems with a memo.</em>

</div>

<div class="nb nb-definition" id="definition-15-1-1">

<strong>Definition 15.1.1</strong>. <strong>Dynamic programming</strong> (DP) solves a problem by combining the answers to subproblems, and stores each subproblem’s answer so that it is computed once. It applies when the problem has

1. <strong>optimal substructure</strong>: an optimal solution is built from optimal solutions of subproblems; and
2. <strong>overlapping subproblems</strong>: the same subproblems recur many times (otherwise it is plain divide and conquer, as in merge sort).

<strong>Memoisation</strong> (top-down) is the recursion plus a cache; <strong>tabulation</strong> (bottom-up) fills a table in an order where every dependency is ready.

</div>

<div class="nb nb-definition" id="fact-15-1-2">

<strong>Fact 15.1.2</strong> (The cost of a DP). Time $=$ (number of states) $\times$ (work per state, i.e. number of choices); space $=$ number of states, often reducible to the states of the last row or two. Writing these two numbers down is the complete complexity analysis.

</div>

<div class="nb nb-remark" id="algorithm-15-1-3">

<strong>Algorithm 15.1.3</strong> (A recipe that works for almost every DP) —

1. <em>State</em>: what does `solve(...)` return, and what do its parameters mean? (“the LCS of the suffixes `a[i..]` and `b[j..]`”).
2. <em>Base cases</em>: the smallest states, answered directly.
3. <em>Choices</em>: the options at the current state (take or skip, match or not, where to split).
4. <em>Recurrence</em>: combine the choices with $\max$, $\min$ or $+$.
5. <em>Memo</em>: a table indexed by the state; return the stored value if present.

Then, if needed, convert to tabulation (loop in reverse dependency order) and drop rows that are no longer read.

</div>

| Memoisation (top-down) | Tabulation (bottom-up) |
|:--|:--|
| Natural to write from the recurrence | Needs an evaluation order |
| Computes only reachable states | Computes every state |
| Recursion overhead, stack depth | No recursion, easy to space-optimise |

<div class="nb-caption" id="table-15-1">

<strong>Table 15.1.</strong> The two styles have the same asymptotic cost.

</div>

All the programs below follow the recipe; `dp.cpp` prints:

```text {filename="Output of dp.cpp"}
LCS(ABCBDAB, BDCABA) = 4
edit distance(kitten, sitting) = 3
0/1 knapsack, weights {1,3,4,5}, values {1,4,5,7}, capacity 7 -> 9
matrix chain 30x35 35x15 15x5 5x10 10x20 20x25 -> 15125 multiplications
  optimal order ((A1(A2A3))((A4A5)A6))
  left to right ((((A1A2)A3)A4)A5)A6 costs 40500
LIS of [10 9 2 5 3 7 101 18 4 19] has length 5
ways to make 10 from {2,5,3,6} = 5
```

## 15.2 Sequences and strings {#sec-dsa-lcs}

<div class="nb nb-example nb-block" id="example-15-2-1">

<strong>Example 15.2.1</strong> (Longest common subsequence)

A. `lcs(i, j)` = LCS length of `A[i..]` and `B[j..]`. B. If either suffix is empty, $0$. C. If the first characters match, take both; otherwise skip one character of `A` or one of `B`. D. $1 + \text{lcs}(i+1, j+1)$, or $\max(\text{lcs}(i+1, j), \text{lcs}(i, j+1))$. E. Table $m \times n$. Time and space $\Theta(mn)$; space $\Theta(\min(m, n))$ if only the length is needed (two rows).

</div>

```cpp {filename="dp.cpp, lines 8–17"}
// LCS: solve(i, j) = LCS of a[i..] and b[j..]
std::string A = "ABCBDAB", B = "BDCABA";
std::vector<std::vector<int>> memoL;
int lcs(int i, int j) {
    if (i == (int)A.size() || j == (int)B.size()) return 0;            // base: an empty suffix
    int& m = memoL[i][j];
    if (m != -1) return m;
    if (A[i] == B[j]) return m = 1 + lcs(i + 1, j + 1);                 // match: take both
    return m = std::max(lcs(i + 1, j), lcs(i, j + 1));                  // skip one side
}
```

<div class="nb nb-example nb-block" id="example-15-2-2">

<strong>Example 15.2.2</strong> (Edit distance (Levenshtein))

`edit(i, j)` = edits that turn `S[i..]` into `T[j..]`. If one suffix is empty the answer is the length of the other (insert or delete everything). Equal characters cost nothing; otherwise $1 + \min(\text{delete}, \text{insert}, \text{replace})$. $\Theta(mn)$: `kitten` $\to$ `sitting` needs $3$ edits (replace `k`, replace `e`, insert `g`).

</div>

```cpp {filename="dp.cpp, lines 19–29"}
// Edit distance: solve(i, j) = edits to turn s[i..] into t[j..]
std::string S = "kitten", T = "sitting";
std::vector<std::vector<int>> memoE;
int edit(int i, int j) {
    if (i == (int)S.size()) return T.size() - j;                        // insert the rest
    if (j == (int)T.size()) return S.size() - i;                        // delete the rest
    int& m = memoE[i][j];
    if (m != -1) return m;
    if (S[i] == T[j]) return m = edit(i + 1, j + 1);
    return m = 1 + std::min({edit(i + 1, j), edit(i, j + 1), edit(i + 1, j + 1)});  // del, ins, replace
}
```

<div class="nb nb-example nb-block" id="example-15-2-3">

<strong>Example 15.2.3</strong> (Longest increasing subsequence)

The textbook DP `lis(i)` = longest increasing subsequence ending at $i$ $= 1 + \max \{\text{lis}(j) : j < i, a_j < a_i\}$ is $\Theta(n^2)$. The $\Theta(n\log n)$ method keeps `tails[L]`, the smallest possible last element of an increasing subsequence of length $L + 1$; `tails` is increasing, so each new element replaces the first tail $\ge$ it (`lower_bound`) or extends the array. Its final length is the LIS length ($5$ for `[10 9 2 5 3 7 101 18 4 19]`, e.g. $2, 3, 7, 18, 19$), but `tails` itself is not necessarily a valid subsequence.

</div>

<div class="nb nb-definition" id="fact-15-2-4">

<strong>Fact 15.2.4</strong> (Other classic sequence DPs). Longest palindromic subsequence (LCS of a string and its reverse, $\Theta(n^2)$); longest palindromic substring ($\Theta(n^2)$ by expanding around centres, $\Theta(n)$ with Manacher); word break and palindrome partitioning ($\Theta(n^2)$); maximum subarray (Kadane, $\Theta(n)$: $\text{best}(i) = \max(a_i, a_i + \text{best}(i-1))$); house robber ($\text{rob}(i) = \max(\text{rob}(i+1), a_i + \text{rob}(i+2))$, $\Theta(n)$).

</div>

## 15.3 Knapsack and coin change {#sec-dsa-knapsack}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> a bag of capacity $W$; each item has a weight and a value; take each item at most once.</em>

</div>

<div class="nb nb-example nb-block" id="example-15-3-1">

<strong>Example 15.3.1</strong> (0/1 knapsack)

`knap(i, cap)` = best value from items $i, i+1, \ldots$ with capacity `cap`. Skip item $i$, or take it if it fits. States $n \times (W + 1)$, two choices each: $\Theta(nW)$ time, and $\Theta(W)$ space with one row <em>iterated from high capacity to low</em> (iterating upwards would let an item be taken twice, which is the unbounded knapsack). With weights $\{1, 3, 4, 5\}$, values $\{1, 4, 5, 7\}$ and $W = 7$ the answer is $9$ (items of weight $3$ and $4$).

</div>

```cpp {filename="dp.cpp, lines 31–41"}
// 0/1 knapsack: solve(i, cap) = best value from items i.. with capacity cap
int W[] = {1, 3, 4, 5}, V[] = {1, 4, 5, 7};
std::vector<std::vector<int>> memoK;
int knap(int i, int cap) {
    if (i == 4) return 0;
    int& m = memoK[i][cap];
    if (m != -1) return m;
    int skip = knap(i + 1, cap);
    int take = W[i] <= cap ? V[i] + knap(i + 1, cap - W[i]) : INT_MIN;
    return m = std::max(skip, take);
}
```

<div class="nb nb-remark" id="remark-15-3-2">

<strong>Remark 15.3.2</strong> (Pseudo-polynomial) — $\Theta(nW)$ is polynomial in the <em>value</em> $W$, exponential in its bit length ([Section 1.6](../01-complexity/#sec-dsa-pseudopoly)). 0/1 knapsack is NP-hard; for small $n$ and huge $W$ use meet in the middle ($O(2^{n/2} n)$).

</div>

<div class="nb nb-definition" id="fact-15-3-3">

<strong>Fact 15.3.3</strong> (The coin-change family). With coins $c_1, \ldots, c_k$ and amount $A$, all in $\Theta(kA)$:

- fewest coins: $\text{f}(v) = 1 + \min_j f(v - c_j)$;
- number of <em>combinations</em>: loop over coins outside and amounts inside, so each multiset is counted once (`ways to make 10 from {2,5,3,6}` $= 5$ above);
- number of <em>ordered sequences</em> (compositions): amounts outside, coins inside. Swapping the two loops is the classic bug.

Unbounded knapsack and rod cutting are the same DP with values attached.

</div>

## 15.4 Interval DP: matrix chain multiplication {#sec-dsa-mcm}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> $(A_1A_2)A_3$ versus $A_1(A_2A_3)$ can differ by a factor of ten in cost.</em>

</div>

<div class="nb nb-definition" id="definition-15-4-1">

<strong>Definition 15.4.1</strong>. Multiplying a $p \times q$ matrix by a $q \times r$ matrix costs $pqr$ scalar multiplications. For a chain $A_1 \cdots A_n$ with $A_i$ of size $p_{i-1} \times p_i$, the order of multiplication (parenthesisation) changes the cost but not the result.

</div>

<div class="nb nb-example nb-block" id="example-15-4-2">

<strong>Example 15.4.2</strong> (The recurrence)

`mcm(i, j)` = cheapest cost for $A_i \cdots A_j$. Base: $i = j$ costs $0$. Choice: the last multiplication splits at $k$, $i \le k < j$: $\text{mcm}(i, j) = \min_k \text{mcm}(i, k) + \text{mcm}(k + 1, j) + p_{i-1}p_k p_j$. $\Theta(n^2)$ states, $\Theta(n)$ choices: $\Theta(n^3)$ time, $\Theta(n^2)$ space.

</div>

```cpp {filename="dp.cpp, lines 43–60"}
// Matrix chain: solve(i, j) = cheapest way to multiply A_i..A_j, A_k is p[k-1] x p[k]
std::vector<long> p = {30, 35, 15, 5, 10, 20, 25};
std::vector<std::vector<long>> memoM, split;
long mcm(int i, int j) {
    if (i == j) return 0;
    long& m = memoM[i][j];
    if (m != -1) return m;
    m = LONG_MAX;
    for (int k = i; k < j; ++k) {                                       // last multiplication splits at k
        long c = mcm(i, k) + mcm(k + 1, j) + p[i - 1] * p[k] * p[j];
        if (c < m) { m = c; split[i][j] = k; }
    }
    return m;
}
std::string paren(int i, int j) {
    if (i == j) return "A" + std::to_string(i);
    return "(" + paren(i, split[i][j]) + paren(split[i][j] + 1, j) + ")";
}
```

For the dimensions $30$, $35$, $15$, $5$, $10$, $20$, $25$ the optimum is $15125$, by the order

$$
\big(A_1(A_2A_3)\big)\big((A_4A_5)A_6\big),
$$

against $40500$ left to right. The number of parenthesisations is the Catalan number $C_{n-1}$ ($C_5 = 42$ here), so trying them all is exponential. Optimal BST construction and burst-balloons are the same interval-DP pattern.

## 15.5 Grids, subsets and digits {#s15-5}

<div class="nb nb-definition" id="fact-15-5-1">

<strong>Fact 15.5.1</strong>.

- <em>Grid paths</em>: $\text{paths}(i, j) = \text{paths}(i-1, j) + \text{paths}(i, j-1)$, $\Theta(RC)$; without obstacles it is $\binom{R + C - 2}{R - 1}$. Minimum path sum, and “unique paths with obstacles”, are the same table.
- <em>Bitmask DP</em>: the state contains a subset of up to about $20$ items as a bitmask. The travelling salesman problem by Held–Karp: $\text{tsp}(\text{mask}, v)$ = cheapest path visiting `mask` and ending at $v$: $\Theta(2^n n^2)$ time, against $n!$ by brute force.
- <em>Digit DP</em>: count numbers $\le N$ with a digit property; state (position, tight flag, property so far): $\Theta(\text{digits} \times \text{states} \times 10)$.
- <em>DP on trees</em>: compute each node’s answer from its children’s in one post-order pass (maximum independent set, tree diameter, house robber on a tree), $\Theta(n)$.

</div>

## 15.6 DP, divide and conquer, greedy {#s15-6}

|  | Divide and conquer | Dynamic programming | Greedy |
|:--|:--|:--|:--|
| Subproblems | independent | overlapping | one, after a choice |
| Choices explored | all parts solved | all choices compared | one choice, never undone |
| Correctness | by construction | optimal substructure | needs an exchange proof |
| Examples | merge sort, quicksort | LCS, knapsack, Bellman–Ford | Huffman, Kruskal, Dijkstra |

<div class="nb-caption" id="table-15-2">

<strong>Table 15.2.</strong> Three design paradigms.

</div>

| Problem | Time | Space |
|:--|:--|:--|
| Fibonacci / climbing stairs | $\Theta(n)$ | $\Theta(1)$ |
| LCS, edit distance | $\Theta(mn)$ | $\Theta(\min(m, n))$ |
| LIS | $\Theta(n \log n)$ | $\Theta(n)$ |
| 0/1 knapsack, subset sum, coin change | $\Theta(nW)$ | $\Theta(W)$ |
| Matrix chain, optimal BST, palindrome partitioning | $\Theta(n^3)$ ($\Theta(n^2)$ for some) | $\Theta(n^2)$ |
| Floyd–Warshall | $\Theta(V^3)$ | $\Theta(V^2)$ |
| Bellman–Ford | $\Theta(VE)$ | $\Theta(V)$ |
| TSP (Held–Karp) | $\Theta(2^n n^2)$ | $\Theta(2^n n)$ |

<div class="nb-caption" id="table-15-3">

<strong>Table 15.3.</strong> Standard DPs and their costs.

</div>

<div class="nb nb-moral">

Write the state in one sentence; the base cases, choices and recurrence follow from it, and (states $\times$ choices) is the running time.

</div>

## 15.7 A few harder problems to think about {#s15-7}

<div class="nb nb-problem nb-block" id="problem-15a">

<strong>Problem 15A</strong> (LCS)

Find the length of the LCS of `AGGTAB` and `GXTXAYB`, and one LCS.

<details class="nb-hint">
<summary>Hint</summary>

Look for the letters of `AGGTAB` in order inside `GXTXAYB`.

</details>

<details class="nb-sol">
<summary>Solution</summary>

$4$: `GTAB`. (Checked by `dpcheck.cpp`, as are the next answers.)

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-15b">

<strong>Problem 15B</strong> 🌶🌶 (Matrix chain)

Matrices of sizes $10 \times 20$, $20 \times 30$, $30 \times 40$, $40 \times 30$. What is the minimum number of scalar multiplications? What is it for $40 \times 20$, $20 \times 30$, $30 \times 10$, $10 \times 30$?

<details class="nb-hint">
<summary>Hint</summary>

$p = (10, 20, 30, 40, 30)$; try the three ways of choosing the last split.

</details>

<details class="nb-sol">
<summary>Solution</summary>

$30000$, by $((A_1A_2)A_3)A_4$: $6000 + 12000 + 12000$. For the second chain, $26000$, by $(A_1(A_2A_3))A_4$: $A_2A_3$ costs $20 \cdot 30 \cdot 10 = 6000$, $A_1(A_2A_3)$ costs $40 \cdot 20 \cdot 10 = 8000$, and the last product $40 \cdot 10 \cdot 30 = 12000$.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-15c">

<strong>Problem 15C</strong> (Knapsack and edit distance)

(a) 0/1 knapsack with weights $10, 20, 30$, values $60, 100, 120$, capacity $50$. (b) Edit distance between `sunday` and `saturday`.

<details class="nb-hint">
<summary>Hint</summary>

(a) Compare with the fractional answer $240$. (b) `s` and `unday` vs `aturday`.

</details>

<details class="nb-sol">
<summary>Solution</summary>

(a) $220$ (the items of weight $20$ and $30$). (b) $3$: insert `a`, insert `t`, replace `n` by `r`.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-15d">

<strong>Problem 15D</strong> (Counting paths)

How many ways are there to climb $10$ stairs taking $1$ or $2$ steps at a time? How many monotone paths (right and down moves only) go from the top-left to the bottom-right corner of a $5 \times 5$ grid of points?

<details class="nb-hint">
<summary>Hint</summary>

Fibonacci; $\binom{8}{4}$.

</details>

<details class="nb-sol">
<summary>Solution</summary>

$89$ ($= F(11)$) and $\binom{8}{4} = 70$.

</details>

</div>
