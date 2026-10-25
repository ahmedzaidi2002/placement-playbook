---
title: "11 · Greedy and dynamic programming"
linkTitle: "11 Greedy and DP"
weight: 11
math: true
---
## 11.1 Greedy algorithms {#dsa-11-1}

Make the choice that looks best **right now** and never revisit it. It works only when the problem has:

- the **greedy-choice property** (some optimal solution starts with the greedy choice), and
- **optimal substructure** (the rest is a smaller instance of the same problem).

Proof technique: an **exchange argument** (swap any optimal solution's first choice for the greedy one without making it worse).

<div class="nb nb-example">

<strong>Example</strong> (Activity selection: most non-overlapping intervals)

Activities (start, finish): (1, 4), (3, 5), (0, 6), (5, 7), (3, 9), (5, 9), (6, 10), (8, 11), (8, 12), (2, 14), (12, 16). Sort by **finish time**, take each activity that starts after the last chosen one finishes: **(1, 4), (5, 7), (8, 11), (12, 16)** → 4 activities, the maximum. (Choosing by earliest start or shortest length can fail.)

</div>

<div class="nb nb-example">

<strong>Example</strong> (Fractional knapsack)

Capacity 50; items (value, weight): (60, 10), (100, 20), (120, 30). Ratios 6, 5, 4 → take item 1 whole, item 2 whole, and $20/30$ of item 3: $60 + 100 + 80 = $ **240**. Greedy by ratio is optimal **only for fractions**: in 0/1 knapsack it would give 160 while the optimum is 220 (items 2 and 3).

</div>

<div class="nb nb-example">

<strong>Example</strong> (Huffman coding)

Frequencies a 5, b 9, c 12, d 13, e 16, f 45. Repeatedly merge the two smallest: (a, b) → 14; (c, d) → 25; (14, e) → 30; (25, 30) → 55; (f, 55) → 100. Codes: **f 0**, c 100, d 101, a 1100, b 1101, e 111. Total bits $= 45\cdot1 + 12\cdot3 + 13\cdot3 + 5\cdot4 + 9\cdot4 + 16\cdot3 = $ **224**, against 300 with a fixed 3-bit code. Huffman codes are **prefix-free** (no code is a prefix of another), so decoding is unambiguous.

</div>

**Where greedy fails:** coin change with coins {1, 3, 4} and amount 6: greedy takes 4 + 1 + 1 (3 coins), the optimum is 3 + 3 (2 coins). Also 0/1 knapsack and longest path. Greedy works for Dijkstra, Prim, Kruskal, Huffman, activity selection, fractional knapsack, job sequencing with deadlines.

## 11.2 Dynamic programming {#dsa-11-2}

Use DP when a problem has **optimal substructure** and **overlapping subproblems** (the same subproblems recur, unlike divide and conquer). Solve each subproblem once and store it.

- **Top-down (memoisation):** recursion + a cache. **Bottom-up (tabulation):** fill a table in an order where dependencies come first; often allows space optimisation.
- **Recipe:** define the state (what a subproblem is) → base cases → transition (choices) → order of evaluation → answer.

## 11.3 The classic DPs {#dsa-11-3}

| Problem | State | Transition | Time |
|---|---|---|---|
| Fibonacci / climbing stairs | $f(i)$ | $f(i-1) + f(i-2)$ | $O(n)$ |
| **0/1 knapsack** | $dp[i][w]$ = best value from the first $i$ items with capacity $w$ | $\max(dp[i-1][w],\ v_i + dp[i-1][w - w_i])$ | $O(nW)$ |
| Coin change (min coins) | $dp[x]$ | $1 + \min_c dp[x - c]$ | $O(nA)$ |
| **LCS** | $dp[i][j]$ for prefixes | match: $1 + dp[i-1][j-1]$; else $\max(dp[i-1][j], dp[i][j-1])$ | $O(mn)$ |
| Edit distance | $dp[i][j]$ | match: $dp[i-1][j-1]$; else $1 + \min$(insert, delete, replace) | $O(mn)$ |
| LIS | $dp[i]$ = LIS ending at $i$ | $1 + \max dp[j]$ over $j < i$, $a_j < a_i$ | $O(n^2)$, or $O(n\log n)$ with binary search |
| Matrix chain | $dp[i][j]$ | $\min_k dp[i][k] + dp[k+1][j] + p_{i-1}p_kp_j$ | $O(n^3)$ |
| Grid paths | $dp[i][j]$ | $dp[i-1][j] + dp[i][j-1]$ | $O(mn)$ |

<div class="nb nb-example">

<strong>Example</strong> (0/1 knapsack)

Capacity 5; items (weight, value): (1, 1), (3, 4), (4, 5). Options that fit: {1, 3} weight 4, value 5; {1, 4} weight 5, value **6**; {3} 4; {4} 5. The table's last cell gives **6**. A greedy pick by ratio (4/3 for the second item) would take items 1 and 2 for value 5.

</div>

<div class="nb nb-example">

<strong>Example</strong> (LCS)

"ABCBDAB" and "BDCABA": the longest common subsequence has length **4** (for example "BCBA"). A subsequence keeps order but need not be contiguous (unlike a substring).

</div>

<div class="nb nb-example">

<strong>Example</strong> (Matrix chain)

$A$ is $10 \times 30$, $B$ is $30 \times 5$, $C$ is $5 \times 60$. $(AB)C$: $10 \cdot 30 \cdot 5 + 10 \cdot 5 \cdot 60 = 1500 + 3000 = $ **4500** multiplications. $A(BC)$: $30 \cdot 5 \cdot 60 + 10 \cdot 30 \cdot 60 = 9000 + 18000 = 27{,}000$. The order matters six-fold.

</div>

## 11.4 DP vs divide and conquer vs greedy {#dsa-11-4}

| | Subproblems | Choices |
|---|---|---|
| Divide and conquer | independent (no overlap) | solve all, combine |
| Dynamic programming | **overlapping** | try all choices, keep the best (stored) |
| Greedy | one at a time | take the locally best, never undo |

<div class="nb nb-moral">

Greedy needs the greedy-choice property (activity selection by finish time, fractional knapsack, Huffman); it fails on coin change and 0/1 knapsack. DP = overlapping subproblems + optimal substructure: define the state, the transition, and fill the table once.

</div>
