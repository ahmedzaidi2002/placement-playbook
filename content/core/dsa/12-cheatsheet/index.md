---
title: "12 · Complexity cheat sheet and library containers"
linkTitle: "12 Cheat sheet"
weight: 12
math: true
---
## 12.1 Data structures {#dsa-12-1}

| Structure | Access | Search | Insert | Delete | Notes |
|---|---|---|---|---|---|
| Array | $O(1)$ | $O(n)$ | $O(n)$ | $O(n)$ | sorted: search $O(\log n)$ |
| Dynamic array | $O(1)$ | $O(n)$ | $O(1)$* at end | $O(1)$ at end | *amortized |
| Linked list | $O(n)$ | $O(n)$ | $O(1)$ at a known node | $O(1)$ at a known node (doubly) | |
| Stack / queue | — | $O(n)$ | $O(1)$ | $O(1)$ | |
| Hash table | — | $O(1)$ avg, $O(n)$ worst | $O(1)$ avg | $O(1)$ avg | no order |
| BST (unbalanced) | — | $O(h)$, worst $O(n)$ | $O(h)$ | $O(h)$ | |
| AVL / red–black | — | $O(\log n)$ | $O(\log n)$ | $O(\log n)$ | ordered |
| Binary heap | min/max $O(1)$ | $O(n)$ | $O(\log n)$ | extract $O(\log n)$ | build $O(n)$ |
| Trie | — | $O(L)$ | $O(L)$ | $O(L)$ | $L$ = key length |
| Union–find | — | find ≈ $O(1)$ | union ≈ $O(1)$ | — | amortized $\alpha(n)$ |

## 12.2 Algorithms {#dsa-12-2}

| Algorithm | Time | Space |
|---|---|---|
| Binary search | $O(\log n)$ | $O(1)$ |
| Merge sort | $O(n \log n)$ | $O(n)$ |
| Quicksort | $O(n \log n)$ avg, $O(n^2)$ worst | $O(\log n)$ |
| Heap sort | $O(n \log n)$ | $O(1)$ |
| Counting sort | $O(n + k)$ | $O(n + k)$ |
| BFS / DFS | $O(V + E)$ | $O(V)$ |
| Topological sort | $O(V + E)$ | $O(V)$ |
| Dijkstra (binary heap) | $O((V + E)\log V)$ | $O(V)$ |
| Bellman–Ford | $O(VE)$ | $O(V)$ |
| Floyd–Warshall | $O(V^3)$ | $O(V^2)$ |
| Kruskal | $O(E \log E)$ | $O(V)$ |
| Prim (binary heap) | $O(E \log V)$ | $O(V)$ |
| KMP string match | $O(n + m)$ | $O(m)$ |
| 0/1 knapsack DP | $O(nW)$ | $O(W)$ optimised |
| LCS / edit distance | $O(mn)$ | $O(\min(m, n))$ optimised |

## 12.3 What input size allows what {#dsa-12-3}

Roughly $10^8$ simple operations per second:

| $n$ up to | Acceptable complexity |
|---|---|
| 10–12 | $O(n!)$ |
| 20–25 | $O(2^n)$ |
| 500 | $O(n^3)$ |
| 5,000 | $O(n^2)$ |
| $10^6$ | $O(n \log n)$ |
| $10^8$ | $O(n)$ |
| $10^{18}$ | $O(\log n)$ or $O(1)$ |

## 12.4 Library containers {#dsa-12-4}

| Need | C++ | Java | Python |
|---|---|---|---|
| Dynamic array | `vector` | `ArrayList` | `list` |
| Stack | `stack` (or `vector`) | `ArrayDeque` | `list` |
| Queue / deque | `queue`, `deque` | `ArrayDeque` | `collections.deque` |
| Priority queue | `priority_queue` (**max**-heap) | `PriorityQueue` (**min**-heap) | `heapq` (**min**-heap) |
| Hash map / set | `unordered_map` / `unordered_set` | `HashMap` / `HashSet` | `dict` / `set` |
| Ordered map / set | `map` / `set` (red–black) | `TreeMap` / `TreeSet` | (no built-in) |
| Linked list | `list` | `LinkedList` | — |

**Iterator invalidation (C++):** inserting into a `vector` can reallocate and invalidate **all** iterators; erasing invalidates those at and after the point. `list`/`map`/`set` iterators stay valid except for the erased element. `unordered_map` rehashing invalidates iterators (but not references to elements).

<div class="nb nb-moral">

Hash table O(1) average, balanced tree O(log n) with order, heap O(log n) insert/extract and O(n) build. About 10⁸ operations per second decides which complexity fits the constraints.

</div>
