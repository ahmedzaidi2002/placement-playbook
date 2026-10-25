---
title: "13 · Interview rapid-fire"
linkTitle: "13 Rapid-fire"
weight: 13
math: true
---
## 13.1 Complexity and basics {#dsa-13-1}

1. **Big-O vs Big-Θ?** Upper bound vs tight bound.
2. **What is amortized analysis?** Average cost per operation over a worst-case sequence (vector push is O(1) amortized).
3. **Master theorem for merge sort?** $T(n) = 2T(n/2) + n = \Theta(n \log n)$.
4. **Array vs linked list?** O(1) access and cache-friendly vs O(1) insert/delete at a known node.
5. **How do you detect a cycle in a linked list?** Floyd's slow and fast pointers.
6. **Find the middle of a list in one pass?** Slow moves 1, fast moves 2.
7. **Stack vs queue?** LIFO vs FIFO.
8. **Queue using two stacks?** Push to one; pop from the other, refilling it when empty; O(1) amortized.
9. **Why postfix notation?** No parentheses or precedence needed; evaluated with one stack.

## 13.2 Trees and heaps {#dsa-13-2}

10. **Leaves in a binary tree with $k$ two-child nodes?** $k + 1$.
11. **Which traversal of a BST is sorted?** Inorder.
12. **Which traversal pairs rebuild a binary tree?** Inorder with preorder or postorder.
13. **BST worst case?** O(n), when keys arrive sorted (a skewed tree).
14. **Delete a BST node with two children?** Replace it with its inorder successor (or predecessor).
15. **AVL vs red–black?** AVL is more strictly balanced (faster search); red–black rotates less (faster updates).
16. **Heap insert and extract?** O(log n) by sifting up / down.
17. **Why is building a heap O(n)?** Most nodes are near the bottom and move only a few levels.
18. **k largest elements?** Min-heap of size k: O(n log k).
19. **Number of BSTs with $n$ keys?** Catalan number $C_n$ (5 for 3 keys, 14 for 4).
20. **What is a trie for?** Prefix search and autocomplete in O(word length).

## 13.3 Hashing {#dsa-13-3}

21. **Why is hashing O(1)?** A good hash spreads keys so buckets stay short, and rehashing keeps the load factor bounded.
22. **When is it O(n)?** When many keys collide (bad hash or adversarial keys).
23. **Chaining vs open addressing?** Lists per bucket vs probing other slots in the array.
24. **Load factor?** Items / buckets; rehash around 0.75.
25. **Hash map vs tree map?** O(1) average without order vs O(log n) with sorted order.
26. **How to build an LRU cache?** Hash map + doubly linked list; O(1) get and put.
27. **Bloom filter?** Probabilistic set: no false negatives, some false positives.

## 13.4 Sorting and searching {#dsa-13-4}

28. **Stable sorts?** Bubble, insertion, merge, counting, radix (not selection, quick, heap).
29. **Quicksort worst case and fix?** O(n²) with bad pivots; random or median-of-three pivot.
30. **Merge sort vs quicksort?** Guaranteed n log n and stable but O(n) extra space vs faster in practice, in place, n² worst.
31. **Best sort for nearly sorted data?** Insertion sort (O(n)).
32. **Lower bound for comparison sorting?** Ω(n log n).
33. **How can you sort in O(n)?** Counting or radix sort, when keys are small integers.
34. **What does `std::sort` use?** Introsort (quick + heap + insertion).
35. **Binary search requirement?** Sorted data or a monotone predicate.
36. **k-th smallest without sorting?** Quickselect, O(n) average.

## 13.5 Graphs, greedy, DP {#dsa-13-5}

37. **BFS vs DFS?** Queue, level by level, shortest unweighted paths vs stack, deep first, cycles and topological order.
38. **Adjacency matrix vs list?** O(V²) space, O(1) edge check vs O(V + E) space, good for sparse graphs.
39. **Why does Dijkstra fail with negative edges?** It finalises a vertex assuming later paths cannot be shorter.
40. **Detect a negative cycle?** Bellman–Ford: a V-th relaxation still improves something.
41. **Topological sort exists when?** Only for a DAG.
42. **Kruskal vs Prim?** Sort edges + union–find (sparse) vs grow a tree with a heap (dense).
43. **Greedy vs DP?** Greedy commits to the local best; DP tries all choices on overlapping subproblems and stores results.
44. **When does greedy coin change fail?** Coins {1, 3, 4}, amount 6: greedy gives 3 coins, optimal is 2.
45. **Memoisation vs tabulation?** Top-down recursion with a cache vs bottom-up table filling.
46. **Why is 0/1 knapsack's O(nW) not polynomial?** W is a number; its input size is log W bits.

<div class="nb nb-moral">

Forty-six answers, each under twenty seconds, cover the DSA theory round; chapter 14 has the numericals.

</div>
