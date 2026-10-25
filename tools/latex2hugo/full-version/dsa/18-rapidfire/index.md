---
title: "18 · Interview rapid-fire"
linkTitle: "18 Interview rapid-fire"
weight: 18
math: true
---
Short answers to the theory questions that come up again and again, in the form you would say them out loud. Each answer points back to the section that explains it.

## 18.1 Complexity {#s18-1}

1. <strong>What does $O(n)$ mean precisely?</strong><br>An upper bound up to a constant factor for large $n$: $f(n) \le c\,n$ for all $n \ge n_0$. It says nothing by itself about best or worst case ([Section 1.1](../01-complexity/#sec-dsa-asym)).
2. <strong>Big-O versus big-Theta?</strong><br>$O$ is an upper bound, $\Theta$ a tight bound. Insertion sort is $O(n^2)$ and also $O(n^3)$, but $\Theta(n^2)$ only in the worst case.
3. <strong>Amortized versus average?</strong><br>Amortized: a guarantee on the total cost of any sequence of operations (dynamic-array push). Average/expected: an expectation over random inputs or random coin flips ([Section 1.4](../01-complexity/#sec-dsa-amortized)).
4. <strong>Why is `push_back` $O(1)$?</strong><br>The capacity doubles when full, so the copies total less than $2n$ over $n$ pushes: $O(1)$ amortized, $O(n)$ for the one push that triggers growth.
5. <strong>Why must a dynamic array grow by a factor, not by a constant?</strong><br>Growing by $+k$ makes the copies sum to $\Theta(n^2/k)$, i.e. $\Theta(n)$ per push.
6. <strong>Complexity of `for (i = n; i > 0; i /= 2) for (j = 0; j < i; j++)`?</strong><br>$n + n/2 + \cdots < 2n$: $\Theta(n)$, not $n\log n$ ([Section 1.2](../01-complexity/#sec-dsa-loops)).
7. <strong>State the Master theorem in one line.</strong><br>Compare $f(n)$ with $n^{\log_b a}$: the polynomially larger one wins; if equal, multiply by $\log n$.
8. <strong>Why can no comparison sort beat $n\log n$?</strong><br>A decision tree with $n!$ leaves has height at least $\log_2 n! = \Theta(n\log n)$ ([Theorem 1.6.3](../01-complexity/#theorem-1-6-3)).
9. <strong>Is an $O(nW)$ knapsack polynomial?</strong><br>No, pseudo-polynomial: $W$ is exponential in its number of bits ([Section 1.6](../01-complexity/#sec-dsa-pseudopoly)).
10. <strong>Space complexity of a recursive function?</strong><br>At least its maximum recursion depth times the frame size, plus anything it allocates.

## 18.2 Arrays, lists, stacks, queues {#s18-2}

11. <strong>Array versus linked list?</strong><br>Array: $O(1)$ indexing, contiguous and cache friendly, $O(n)$ middle insertion. List: $O(1)$ insertion at a known node, $O(n)$ access, poor locality, pointer overhead ([Section 4.2](../04-lists/#sec-dsa-list-vs-array)).
12. <strong>Why is `vector` usually faster than `list` even for insertions?</strong><br>Finding the position in a list is $O(n)$ pointer chasing with cache misses; shifting a vector tail is a fast sequential copy.
13. <strong>Detect a cycle in a linked list in $O(1)$ space?</strong><br>Floyd’s slow and fast pointers; reset one to the head to find the cycle’s start ([Section 4.3.i](../04-lists/#sec-dsa-floyd)).
14. <strong>Reverse a singly linked list.</strong><br>Three pointers, `prev`, `cur`, `next`; $O(n)$ time, $O(1)$ space.
15. <strong>Delete a node given only a pointer to it?</strong><br>Copy the next node into it and delete the next node; impossible for the last node.
16. <strong>How do you implement a queue with two stacks? Cost?</strong><br>Push to `in`; pop from `out`, refilling it from `in` when empty. $O(1)$ amortized ([Section 5.3](../05-stacks/#sec-dsa-twostacks)).
17. <strong>Full versus empty in a circular queue?</strong><br>Leave one slot unused: empty iff `front == rear`, full iff `(rear + 1) % n == front`; or keep a count ([Section 5.2](../05-stacks/#sec-dsa-circular)).
18. <strong>Applications of a stack?</strong><br>Function calls, expression evaluation, bracket matching, undo, DFS, monotonic-stack problems.
19. <strong>Why is `a^b^c` converted to `abc^^`?</strong><br>Exponentiation is right-associative, so an incoming `^` does not pop an equal-precedence `^` ([Section 5.4](../05-stacks/#sec-dsa-expressions)).
20. <strong>How many sequences can a stack produce from $1..n$?</strong><br>The Catalan number $C_n$; the forbidden pattern is $312$ ([Section 5.6](../05-stacks/#sec-dsa-stackperm)).
21. <strong>Deque versus queue?</strong><br>A deque supports insertion and removal at both ends in $O(1)$; it powers the sliding-window maximum.

## 18.3 Trees and heaps {#s18-3}

22. <strong>Full, complete, perfect binary tree?</strong><br>Full: $0$ or $2$ children. Complete: all levels full except the last, filled from the left. Perfect: full with all leaves at one depth ([Section 6.1](../06-trees/#sec-dsa-treevocab)).
23. <strong>Which traversal of a BST gives sorted order?</strong><br>Inorder.
24. <strong>Which traversals determine a binary tree?</strong><br>Inorder plus one of preorder, postorder or level order. Preorder plus postorder does not, unless the tree is full ([Section 6.4](../06-trees/#sec-dsa-reconstruct)).
25. <strong>Traverse a tree in $O(1)$ extra space?</strong><br>Morris traversal, using temporary threads.
26. <strong>Number of binary trees with $n$ nodes?</strong><br>$C_n$: $1, 2, 5, 14, 42, \ldots$
27. <strong>BST operations cost?</strong><br>$O(h)$: $O(\log n)$ if balanced, $O(n)$ for sorted insertions ([Section 7.1](../07-bst/#sec-dsa-bst)).
28. <strong>How do you delete a node with two children from a BST?</strong><br>Replace its key with the inorder successor’s (minimum of the right subtree) and delete the successor, which has at most one child.
29. <strong>How do you validate a BST?</strong><br>Pass a valid range down the recursion, or check that the inorder sequence is strictly increasing; comparing only with direct children is wrong.
30. <strong>AVL versus red–black?</strong><br>AVL is more strictly balanced (faster lookups, height $< 1.44\log n$); red–black needs fewer rotations per update (height $\le 2\log n$); `std::map` uses red–black ([Section 7.3](../07-bst/#sec-dsa-rb)).
31. <strong>How many rotations can an AVL insertion need?</strong><br>At most one single or double rotation; a deletion may need $O(\log n)$.
32. <strong>Why do databases use B+-trees, not binary trees?</strong><br>A node fills a disk block, so the height is $\log_t n$ with $t$ in the hundreds (a handful of disk reads), and linked leaves make range scans sequential.
33. <strong>Heap versus BST?</strong><br>Heap: $O(1)$ max, $O(\log n)$ insert/extract, $O(n)$ build, no ordered traversal or search. BST: $O(\log n)$ everything, full order.
34. <strong>Why is build-heap $O(n)$?</strong><br>Most nodes are near the leaves and sift down only a little: $\sum_h h\,n/2^{h+1} = O(n)$ ([Section 8.3](../08-heaps/#sec-dsa-buildheap)).
35. <strong>Where can the minimum of a max-heap be?</strong><br>In any leaf, indices $\lfloor n/2 \rfloor..n - 1$: finding it is $O(n)$.
36. <strong>Top $k$ elements of a stream of $n$?</strong><br>A min-heap of size $k$: $O(n\log k)$ time, $O(k)$ memory.
37. <strong>Why do textbooks mention Fibonacci heaps?</strong><br>$O(1)$ amortized decrease-key makes Dijkstra $O(E + V\log V)$; in practice binary heaps are faster.

## 18.4 Hashing {#s18-4}

38. <strong>Why is a hash-table lookup $O(1)$?</strong><br>The hash sends the key to one bucket; with a uniform (or universal) hash and a load factor kept constant by resizing, the expected bucket size is $O(1)$. It is expected and amortized, not worst case ([Section 9.6](../09-hashing/#sec-dsa-whyo1)).
39. <strong>Worst case of a hash table?</strong><br>$O(n)$ per operation when all keys collide: a bad hash, adversarial keys (hash flooding), or a degenerate table size.
40. <strong>What is the load factor and why does it matter?</strong><br>$\alpha = n/m$; expected chain length or probe count grows with it ($1 + \alpha$ for chaining, about $1/(1-\alpha)$ for open addressing).
41. <strong>Chaining versus open addressing?</strong><br>Chaining: lists per bucket, tolerates $\alpha > 1$, easy deletes. Open addressing: everything in the array, better cache use, needs $\alpha$ well below $1$ and tombstones ([Section 9.4](../09-hashing/#sec-dsa-openaddr)).
42. <strong>Primary versus secondary clustering?</strong><br>Primary: linear probing’s runs merge and grow. Secondary: keys with the same home follow the same quadratic sequence. Double hashing avoids both.
43. <strong>Why should the table size be prime?</strong><br>With $k \bmod m$, a prime $m$ uses all bits of the key and avoids patterns in the keys; quadratic probing and double hashing need it to reach enough slots.
44. <strong>What happens on rehashing?</strong><br>A bigger table is allocated and every key re-inserted ($O(n)$), amortized $O(1)$ per insert; all iterators are invalidated.
45. <strong>Why can’t you delete by emptying a slot in open addressing?</strong><br>Searches stop at empty slots and would miss keys inserted after the deleted one; use tombstones.
46. <strong>What does Java 8 do against long chains?</strong><br>A bucket that grows past $8$ entries (in a table of at least $64$) becomes a red–black tree: $O(\log n)$ worst case.
47. <strong>`unordered_map` versus `map`?</strong><br>Hash table, $O(1)$ average, no order, versus red–black tree, $O(\log n)$, sorted, range queries ([Section 9.8](../09-hashing/#sec-dsa-unordered)).
48. <strong>What is universal hashing?</strong><br>Choosing the hash function at random from a family with collision probability $\le 1/m$, so no fixed input is bad for the algorithm.
49. <strong>How does an LRU cache get $O(1)$?</strong><br>Hash map from key to node of a doubly linked list kept in recency order ([Section 9.10](../09-hashing/#sec-dsa-lru)).
50. <strong>What is a Bloom filter?</strong><br>A bit array with $k$ hashes answering “definitely not present” or “maybe present”; no false negatives, tunable false positives ([Section 9.9](../09-hashing/#sec-dsa-bloom)).
51. <strong>Why must equal objects have equal hash codes?</strong><br>Otherwise they land in different buckets and `find` misses the stored one; overriding `equals` without `hashCode` breaks `HashMap`.

## 18.5 Sorting and searching {#s18-5}

52. <strong>What does stable mean, and which sorts are stable?</strong><br>Equal keys keep their input order. Stable: insertion, bubble, merge, counting, radix, Timsort. Unstable: selection, quick, heap, shell ([Section 13.1](../13-sorting/#sec-dsa-sortprops)).
53. <strong>Fastest sort for nearly sorted data?</strong><br>Insertion sort, $O(n + \text{inversions})$, or Timsort.
54. <strong>Why is quicksort preferred to merge sort for arrays?</strong><br>In place, sequential memory access, fewer data moves; average $1.39\,n\log_2 n$ comparisons with small constants.
55. <strong>Why is merge sort preferred for linked lists?</strong><br>It needs only sequential access and $O(1)$ extra space on lists; quicksort’s random access and heap sort’s indexing do not fit lists.
56. <strong>Quicksort worst case and how to avoid it?</strong><br>$O(n^2)$ when the pivot is always extreme (sorted input with first/last pivot); randomize the pivot, median of three, three-way partitioning, or introsort ([Section 13.4](../13-sorting/#sec-dsa-quick)).
57. <strong>Why is heap sort rarely used despite $O(n\log n)$ worst case?</strong><br>Poor cache behaviour and more comparisons than quicksort; it lives on as introsort’s fallback.
58. <strong>Which sort makes the fewest swaps?</strong><br>Selection sort ($\le n - 1$); cycle sort makes the fewest writes.
59. <strong>How does counting sort beat $n\log n$?</strong><br>It does not compare keys; it uses them as indices. $O(n + k)$, useful when $k = O(n)$ ([Section 13.7](../13-sorting/#sec-dsa-noncomp)).
60. <strong>Why must radix sort’s per-digit sort be stable?</strong><br>Each pass must preserve the order established by the less significant digits.
61. <strong>What does `std::sort` use?</strong><br>Introsort: quicksort, switching to heap sort at depth $2\log n$ and insertion sort for small ranges ([Section 13.6](../13-sorting/#sec-dsa-introsort)).
62. <strong>What does Python’s sort use?</strong><br>Timsort (with the Powersort merge policy since 3.11): stable, adaptive, $O(n)$ on sorted input.
63. <strong>$k$-th smallest without sorting?</strong><br>Quickselect, $O(n)$ expected; median of medians, $O(n)$ worst case ([Section 13.12](../13-sorting/#sec-dsa-selection)).
64. <strong>Binary search overflow bug?</strong><br>`(lo + hi) / 2` overflows; use `lo + (hi - lo) / 2`.
65. <strong>When does binary search apply beyond arrays?</strong><br>Whenever a predicate is monotone over an ordered range: “search on the answer” ([Section 12.2](../12-searching/#sec-dsa-binsearch)).
66. <strong>Interpolation search complexity?</strong><br>$O(\log \log n)$ on uniform keys, $O(n)$ worst case.

## 18.6 Greedy and dynamic programming {#s18-6}

67. <strong>When does greedy work?</strong><br>When the greedy-choice property and optimal substructure hold; prove it with an exchange argument ([Section 14.1](../14-greedy/#sec-dsa-greedyproof)).
68. <strong>Give a problem where greedy fails.</strong><br>Coin change with $\{1, 3, 4\}$ for $6$; 0/1 knapsack; weighted interval scheduling.
69. <strong>Why sort activities by finishing time?</strong><br>Finishing earliest leaves the most room; the exchange argument replaces any first choice by the earliest-finishing one.
70. <strong>Why is Huffman coding optimal?</strong><br>The two rarest symbols can be deepest siblings in some optimal tree; merge them and recurse ([Section 14.4](../14-greedy/#sec-dsa-huffman)).
71. <strong>DP versus divide and conquer?</strong><br>DP has overlapping subproblems and caches them; divide and conquer splits into independent subproblems.
72. <strong>Memoisation versus tabulation?</strong><br>Top-down recursion with a cache versus bottom-up table filling; same complexity, tabulation avoids recursion and is easier to space-optimise.
73. <strong>How do you get the complexity of a DP?</strong><br>Number of states times work per state.
74. <strong>Why does 0/1 knapsack iterate capacity downwards in the 1-D version?</strong><br>So each item is used at most once; upwards gives the unbounded knapsack.
75. <strong>Counting coin-change combinations versus permutations?</strong><br>Coins in the outer loop count combinations; amounts in the outer loop count ordered sequences.
76. <strong>LIS in $O(n\log n)$?</strong><br>Keep the smallest tail of each length and binary-search each new element into it.

## 18.7 Graphs {#s18-7}

77. <strong>Adjacency matrix versus list?</strong><br>Matrix: $O(V^2)$ space, $O(1)$ edge test, good for dense graphs. List: $O(V + E)$ space and traversal, good for sparse graphs ([Section 10.3](../10-graphrep/#sec-dsa-graphrepr)).
78. <strong>BFS versus DFS?</strong><br>BFS: queue, level by level, shortest paths in unweighted graphs, memory $O$(width). DFS: stack/recursion, goes deep, cycle detection, topological sort, SCCs, memory $O$(depth).
79. <strong>Detect a cycle in a directed graph?</strong><br>DFS finds a back edge (to a grey vertex), or Kahn’s algorithm cannot remove every vertex.
80. <strong>Detect a cycle in an undirected graph?</strong><br>DFS finds an edge to a visited vertex that is not the parent, or union–find sees an edge whose endpoints are already connected.
81. <strong>Why does Dijkstra fail with negative edges?</strong><br>It finalises a vertex when extracted, assuming no later path can be cheaper; a negative edge breaks that assumption ([Section 16.5.i](../16-graphs/#sec-dsa-dijkstra)).
82. <strong>Dijkstra’s complexity?</strong><br>$O((V + E)\log V)$ with a binary heap, $O(V^2)$ with an array, $O(E + V\log V)$ with a Fibonacci heap.
83. <strong>How does Bellman–Ford detect negative cycles?</strong><br>If the $V$-th round of relaxations still improves some distance.
84. <strong>Floyd–Warshall loop order?</strong><br>The intermediate vertex $k$ must be the outermost loop.
85. <strong>Kruskal versus Prim?</strong><br>Kruskal sorts edges and uses union–find, $O(E\log E)$, good for sparse graphs; Prim grows a tree with a heap, $O(E\log V)$, or $O(V^2)$ with an array for dense graphs ([Section 16.6](../16-graphs/#sec-dsa-mst)).
86. <strong>Is the MST unique?</strong><br>Yes if all edge weights are distinct; otherwise possibly not, but its total weight is unique.
87. <strong>Is the shortest-path tree an MST?</strong><br>No; they optimise different things.
88. <strong>Euler versus Hamiltonian path?</strong><br>Euler (every edge once) is easy: $0$ or $2$ odd vertices. Hamiltonian (every vertex once) is NP-complete.
89. <strong>What is a topological sort and when does it exist?</strong><br>An order with every edge going forward; it exists iff the graph is a DAG ([Section 16.3](../16-graphs/#sec-dsa-topo)).
90. <strong>What are SCCs and how are they found?</strong><br>Maximal sets of mutually reachable vertices; Kosaraju (two DFS) or Tarjan (one DFS), $O(V + E)$.
91. <strong>Shortest path in a grid with walls?</strong><br>BFS from the start, $O(RC)$; with weights $0/1$ use 0-1 BFS.
