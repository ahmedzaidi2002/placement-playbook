---
title: "17 · Complexity cheat sheet"
linkTitle: "17 Complexity cheat sheet"
weight: 17
math: true
---
The standard complexities of this book on four pages, for the last hour before an interview or an OA. “avg” is average or expected, “am.” amortized; all bounds are $O(\cdot)$ unless stated. Each row points to the section that explains it.

## 17.1 Data structures {#s17-1}

| Structure | Access | Search | Insert | Delete | Notes |
|:--|:-:|:-:|:-:|:-:|:--|
| Static array | $1$ | $n$ | $n$ | $n$ | sorted: search $\log n$ |
| Dynamic array | $1$ | $n$ | $1$ am. at end, $n$ middle | $1$ at end | [Section 3.2](../03-arrays/#sec-dsa-dynarray) |
| Singly linked list | $n$ | $n$ | $1$ at head / after node | $1$ at head | [Section 4.1](../04-lists/#sec-dsa-lists) |
| Doubly linked list | $n$ | $n$ | $1$ at a node | $1$ at a node |  |
| Stack, queue, deque | – | $n$ | $1$ | $1$ | [Chapter 5](../05-stacks/) |
| Hash table | – | $1$ avg, $n$ worst | $1$ avg am. | $1$ avg | no order; [Section 9.6](../09-hashing/#sec-dsa-whyo1) |
| BST (unbalanced) | – | $h$: $\log n$ avg, $n$ worst | $h$ | $h$ | [Section 7.1](../07-bst/#sec-dsa-bst) |
| AVL / red–black tree | – | $\log n$ | $\log n$ | $\log n$ | ordered, range queries |
| Splay tree | – | $\log n$ am. | $\log n$ am. | $\log n$ am. |  |
| Skip list | – | $\log n$ avg | $\log n$ avg | $\log n$ avg | [Section 4.4](../04-lists/#sec-dsa-skiplist) |
| Binary heap | top $1$ | $n$ | $\log n$ | extract $\log n$ | build $n$; [Chapter 8](../08-heaps/) |
| B-tree (degree $t$) | – | $\log n$ | $\log n$ | $\log n$ | height $\log_t n$ |
| Bloom filter | – | $k$ | $k$ | no | false positives only |

<div class="nb-caption" id="table-17-1">

<strong>Table 17.1.</strong> Operations on the standard data structures.

</div>

| Fact | Value |
|:--|:--|
| Height of a complete binary tree / binary heap | $\lfloor \log_2 n \rfloor$ |
| Nodes of a binary tree of height $h$ | between $h + 1$ and $2^{h+1} - 1$ |
| Leaves of a full binary tree | internal nodes $+ 1$; generally $n_0 = n_2 + 1$ |
| Binary trees with $n$ nodes; BSTs on $n$ keys; stack permutations | $C_n = \binom{2n}{n}/(n+1)$ |
| Minimum nodes of an AVL tree of height $h$ | $N(h) = N(h-1) + N(h-2) + 1$: $1, 2, 4, 7, 12, 20, 33$ |
| AVL / red–black height | $< 1.44\log_2 n$ / $\le 2\log_2(n + 1)$ |
| Heap: parent, children (0-based) | $\lfloor (i-1)/2 \rfloor$, $2i + 1$, $2i + 2$ |
| Row-major address of $A[i][j]$ with $C$ columns | $B + (iC + j)s$ |
| Edges of a simple graph / tree | $\le n(n-1)/2$ / exactly $n - 1$ |
| Expected chain length, chaining | $\alpha = n/m$ |
| Expected probes, open addressing (miss) | $1/(1 - \alpha)$; linear probing $\frac12(1 + 1/(1-\alpha)^2)$ |

<div class="nb-caption" id="table-17-2">

<strong>Table 17.2.</strong> Numbers that OA questions are built on.

</div>

## 17.2 Sorting and searching {#s17-2}

| Algorithm | Best | Average | Worst | Space | Stable |
|:--|:-:|:-:|:-:|:-:|:-:|
| Bubble (flag), insertion | $n$ | $n^2$ | $n^2$ | $1$ | yes |
| Selection | $n^2$ | $n^2$ | $n^2$ | $1$ | no |
| Shell | $n\log n$ | gap dependent | $n^{1.5}$ (Knuth) | $1$ | no |
| Merge | $n\log n$ | $n\log n$ | $n\log n$ | $n$ | yes |
| Quick | $n\log n$ | $n\log n$ | $n^2$ | $\log n$ | no |
| Heap | $n\log n$ | $n\log n$ | $n\log n$ | $1$ | no |
| Timsort / introsort | $n$ / $n\log n$ | $n\log n$ | $n\log n$ | $n$ / $\log n$ | yes / no |
| Counting | $n + k$ | $n + k$ | $n + k$ | $n + k$ | yes |
| Radix (LSD) | $d(n + b)$ | $d(n + b)$ | $d(n + b)$ | $n + b$ | yes |
| Bucket | $n$ | $n$ | $n^2$ | $n$ | yes |
| Quickselect / median of medians | $n$ | $n$ | $n^2$ / $n$ | $1$ | – |
| Linear / binary search | $1$ | $n$ / $\log n$ | $n$ / $\log n$ | $1$ | – |
| Interpolation search | $1$ | $\log \log n$ (uniform) | $n$ | $1$ | – |

<div class="nb-caption" id="table-17-3">

<strong>Table 17.3.</strong> Sorting and searching ([Section 13.10](../13-sorting/#sec-dsa-sorttable)).

</div>

## 17.3 Algorithms {#s17-3}

| Algorithm | Time | Space |
|:--|:--|:--|
| BFS, DFS, topological sort, SCC, bridges | $V + E$ | $V$ |
| Dijkstra (binary heap / array / Fibonacci) | $(V + E)\log V$ / $V^2$ / $E + V\log V$ | $V$ |
| Bellman–Ford | $VE$ | $V$ |
| Floyd–Warshall | $V^3$ | $V^2$ |
| Kruskal / Prim (heap) | $E\log E$ / $E\log V$ | $V + E$ |
| Edmonds–Karp max flow | $VE^2$ | $V + E$ |
| Huffman coding, activity selection | $n\log n$ | $n$ |
| LCS, edit distance | $mn$ | $\min(m, n)$ |
| LIS | $n\log n$ | $n$ |
| 0/1 knapsack, coin change | $nW$ (pseudo-polynomial) | $W$ |
| Matrix-chain multiplication | $n^3$ | $n^2$ |
| TSP: brute force / Held–Karp | $n!$ / $2^n n^2$ | $n$ / $2^n n$ |
| Naive Fibonacci / memoised | $\varphi^n$ / $n$ | $n$ / $n$ |
| Subsets / permutations / $N$-queens | $2^n$ / $n!$ / $\le n!$ | $n$ |
| Binary exponentiation | $\log n$ | $1$ |
| Karatsuba / Strassen | $n^{1.585}$ / $n^{2.81}$ |  |

<div class="nb-caption" id="table-17-4">

<strong>Table 17.4.</strong> Standard algorithms.

</div>

| Recurrence | Solution |
|:--|:--|
| $T(n) = T(n/2) + 1$ | $\log n$ (binary search) |
| $T(n) = T(n/2) + n$ | $n$ (quickselect, average) |
| $T(n) = 2T(n/2) + 1$ | $n$ (tree traversal) |
| $T(n) = 2T(n/2) + n$ | $n\log n$ (merge sort) |
| $T(n) = 2T(n/2) + n\log n$ | $n\log^2 n$ |
| $T(n) = 3T(n/2) + n$ / $7T(n/2) + n^2$ | $n^{1.585}$ / $n^{2.81}$ |
| $T(n) = T(n-1) + 1$ / $T(n-1) + n$ | $n$ / $n^2$ |
| $T(n) = 2T(n-1) + 1$ | $2^n$ (Tower of Hanoi) |
| $T(n) = T(n/3) + T(2n/3) + n$ | $n\log n$ |
| $T(n) = T(n/5) + T(7n/10) + n$ | $n$ (median of medians) |
| $T(n) = 2T(\sqrt n) + \log n$ | $\log n \log \log n$ |

<div class="nb-caption" id="table-17-5">

<strong>Table 17.5.</strong> Recurrences ([Section 1.5](../01-complexity/#sec-dsa-recurrences)).

</div>
