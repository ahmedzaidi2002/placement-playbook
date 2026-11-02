@@ go-6
**Answer: (a) an array with prefix sums**

**Why.** The output is built once and never queried or updated afterwards. One O(n) prefix-sum pass gives every power-of-two entry. An even index i only needs the original values at the powers of two in i's binary form (its set bits), O(log n) each, so O(n log n) in total. A Fenwick tree does **not** store these sums (its node 6 holds arr[5] + arr[6], not arr[2] + arr[4]); a segment tree adds overhead with no queries to serve; (d) rescans for every index, O(n²).

**Concept: pick the simplest structure that fits the access pattern.** Trees (Fenwick, segment) pay off when you mix many updates and range queries. For a one-shot transformation, a plain array and a prefix sum (`pre[i] = pre[i−1] + arr[i]`) is fastest. The set bits of i are found with `i & -i` or by scanning bits.

@@ mw-iitb-10
**Answer: (c) O(n)**

**Why.** Use the array itself as the hash table: for each value v in 1..n, swap it into index v − 1 (repeat until the slot holds the right value or v is out of range). Then scan: the first index i with a[i] ≠ i + 1 gives the answer i + 1. Each swap places one value for good, so the total is O(n), with O(1) extra space. (The candidate's O(n log n) is the sort-based approach.)

**Concept: cyclic sort / index as hash.** When values are in a known range 1..n, the value itself tells you where it belongs, so you can "sort" in linear time and use positions as presence markers.

@@ mw-nitd-8
**Answer: (c) linked-list storage**

**Why.** Inserting, deleting or moving a substring in a linked list only changes a few pointers. In arrays (fixed or variable length) you must shift all the characters after the change.

**Concept: arrays vs linked lists.** Arrays: O(1) access by index, O(n) insert/delete in the middle. Linked lists: O(n) access, O(1) insert/delete once you are at the spot. Choose by which operations dominate.

@@ or-sparse
**Answer: (d) adjacency list**

**Why.** A symmetric sparse matrix is like the adjacency matrix of a sparse undirected graph. Storing only the non-zero entries per row (and only one triangle, since it is symmetric) uses space proportional to the non-zeros, not n². A hash table keyed by (i, j) also works but is not the classic answer.

**Concept: sparse storage.** A matrix is sparse when most entries are 0. Store only the non-zeros: adjacency lists, coordinate lists (row, col, value), or compressed sparse row (CSR). Symmetry halves it again.

@@ paytm-swaps
**Answer: (b) 5**

**Why.** For each position of arr1, find where its value must go in arr2. That gives the permutation 0→8, 1→7, 2→1, 3→0, 4→4, 5→5, 6→2, 7→6, 8→3. Its cycles are (0 8 3), (1 7 6 2), (4) and (5). A cycle of length L needs L − 1 swaps: 2 + 3 + 0 + 0 = 5, i.e. n − (number of cycles) = 9 − 4.

**Concept: minimum swaps = n − cycles.** Each swap can put exactly one element into its final place while splitting a cycle; a cycle of L elements is fixed with L − 1 swaps. Find cycles by following "where does this element need to go" until you return to the start.

@@ qc60-42
**Answer: (d) insert an element into the queue**

**Why.** It checks the queue isn't full, sets `front` to 0 on the first insertion, advances `rear` circularly with `% size`, and stores the element: a circular-queue enqueue.

**Concept: circular queue.** A fixed array where `rear = (rear + 1) % size` wraps around, so slots freed at the front are reused. Enqueue moves rear; dequeue moves front.

@@ qc60-51
**Answer: (c) `for (int j = 0; j < p; j++) Sum += A[i][j] * B[j][k]; C[i][k] = Sum;`**

**Why.** C[i][k] is the dot product of row i of A with column k of B, summed over the shared dimension p: Σⱼ A[i][j] · B[j][k]. Only (c) has that loop and the right indices.

**Concept: matrix multiplication.** An (n × p) times a (p × m) matrix gives n × m. Three nested loops: rows i, columns k, and the shared index j. Time O(n·p·m).

@@ ti-minmax
**Answer: (c) O(n²)**

**Why.** Every one of the n² entries must be read once to find each row's minimum; the final maximum over n row-minima adds only O(n).

**Concept: lower bound by reading the input.** If an answer can depend on every input element, the algorithm must look at all of them, so it cannot beat the input size (here n²).

@@ ti-reverse
**Answer: both statements are true**

**Why.** The loop swaps A[i] and A[j] from the outside in, so it reverses the array (A). It runs N/2 times, linear time (B).

**Concept: two-pointer swap.** One index from each end, swap, move inward until they meet. O(n) time, O(1) extra space.

@@ ti-window
**Answer: O(n)**

**Why.** Compute the first window's sum, then slide: add the element that enters and subtract the one that leaves. Each step is O(1), and there are n − k steps.

**Concept: sliding window.** Reuse the previous window's result instead of recomputing from scratch; this turns O(nk) into O(n).

@@ wbd-17
**Answer: (a) an array of 50 numbers**

**Why.** Only scores 51–100 need counting: 50 possible values, one counter each (index = score − 51). Storing all 500 scores is unnecessary.

**Concept: counting array.** When values come from a small known range, an array of counters indexed by value gives O(1) updates and uses space proportional to the range, not the input size.

@@ wbd-19
**Answer: (c) deleting an element**

**Why.** In a sorted array the i-th smallest is a[i − 1] and the i-th largest is a[n − i], both O(1). Deleting requires shifting the later elements left, O(n).

**Concept: sorted arrays.** Great for rank queries and binary search (O(log n)); poor for inserts and deletes (O(n) shifts). Balanced BSTs give O(log n) for all of them.

@@ wbd-x
**Answer: O(n log n)** (the question is inferred from the code)

**Why.** The outer loop runs from n/2 to n: about n/2 times. The inner loop doubles j from 2 up to n: about log₂ n times. Total ≈ (n/2) · log n = O(n log n).

**Concept: loops that double.** A loop variable multiplied by 2 each time reaches n after log₂ n steps. Multiply the counts of nested independent loops.

@@ ion-q22
**Answer: (c) O(n² log n)**

**Why.** For each i, the middle loop steps by i, so it runs about n/i times; the inner loop runs n/2 times regardless. Total = Σᵢ (n/i)(n/2) = (n²/2)(1 + 1/2 + ... + 1/n) = (n²/2) Hₙ = Θ(n² log n).

**Concept: harmonic series.** 1 + 1/2 + 1/3 + ... + 1/n ≈ ln n. Loops whose step grows with the outer index (j += i) often produce this sum.

@@ mw-iiitd-4
**Answer: (a) O(n log n)** (assuming the usual split into two halves; the split is cut off in the photo)

**Why.** Two halves plus linear work to split and merge: T(n) = 2T(n/2) + O(n). The recursion has log n levels, each doing O(n) work in total: O(n log n).

**Concept: the master theorem.** For T(n) = aT(n/b) + O(nᵈ): if a = bᵈ the answer is O(nᵈ log n) (merge sort: a = 2, b = 2, d = 1); if a < bᵈ it is O(nᵈ); if a > bᵈ it is O(n^(log_b a)).

@@ mw25-asymptotic
**Answer: (c) n³/√n**

**Why.** n³/√n = n^2.5, which grows faster than n², so it is not O(n²). A huge constant (a) still gives a linear function, and n^1.98 (b) grows slower than n².

**Concept: Big-O ignores constants, not exponents.** f(n) = O(g(n)) if f eventually stays below c · g(n) for some constant c. Constants and lower-order terms never matter; a larger exponent always does.

@@ qc60-52
**Answer: (b) O(log n)**

**Why.** Each comparison with the middle element throws away half of the remaining range, so after k steps n/2ᵏ elements remain; it ends when that reaches 1, k = log₂ n.

**Concept: halving gives logarithms.** Any process that cuts the problem in half each step takes about log₂ n steps (binary search, balanced-tree height).

@@ ti-auxspace
**Answer: (a) O(1)**

**Why.** The traversal uses one extra pointer, `temp`, regardless of the list's length.

**Concept: auxiliary space.** Extra memory used besides the input itself. Iterative traversals need O(1); recursive ones need O(depth) for the call stack.

@@ ti-printcount
**Answer: (c) (n² − n)/2**

**Why.** One call for every pair i < j from {1..n}: C(n, 2) = n(n − 1)/2 = (n² − n)/2.

**Concept: counting nested loops.** For i from 1 to n − 1, the inner loop runs n − i times; adding (n − 1) + (n − 2) + ... + 1 gives n(n − 1)/2.

@@ wbd-18
**Answer: (b) O(n)**

**Why.** The outer loop runs 10 times and the innermost 6 times (n − 3 to n + 2): both constants. Only the middle loop depends on n: 10 × n × 6 = 60n = O(n).

**Concept: a loop's bounds decide its cost, not its nesting depth.** Three nested loops are not automatically O(n³); count how many times each actually runs.

@@ ti-tsp
**Answer: the cost becomes infinite** (no valid tour exists)

**Why.** In the TSP dynamic program, unreachable edges have weight ∞. Any tour must visit city k, so every candidate tour includes an ∞ edge, and the minimum stays ∞.

**Concept: Held–Karp DP.** dp[S][j] = cheapest path that starts at the origin, visits exactly the set S and ends at j. Missing edges are modelled as ∞, so they are never chosen unless there is no alternative. Time O(n² 2ⁿ).

@@ cisco1-dijkstra
**Answer: (a) 9**

**Why.** You may enter a road at time max(arrival, opening time), and arriving earlier never hurts, so Dijkstra on arrival times still works.
- A → C arrives at 2. C → E opens at 8, so leave at 8 and arrive at 9.
- Via D: A → C → D arrives at 9, then E at 11.
- Via B: A → B at 5, wait until 10 for B → D, D at 13.
The earliest arrival at E is 9.

**Concept: Dijkstra with waiting times.** Dijkstra is correct when edge costs are "first-in-first-out": leaving later never lets you arrive earlier. With opening times, the arrival time is max(t, open) + travel, which keeps that property, so the greedy choice of the earliest unvisited node still works.

@@ epam-q4
**Answer: (a) 1**

**Why.** An undirected graph's adjacency matrix is symmetric: entry (i, j) = entry (j, i). Entry (3, 4) is 1, so entry (4, 3), which is x, must be 1.

**Concept: adjacency matrix.** A[i][j] = 1 if there is an edge i–j. For undirected graphs every edge appears twice (A[i][j] and A[j][i]); directed graphs need not be symmetric.

@@ fj-kgp-ds4
**Answer: (c) O(E + V log V)**

**Why.** That is Dijkstra with a Fibonacci heap. With a binary heap it is O((E + V) log V); with a plain array O(V²), which is best for dense graphs. The question expects the heap bound.

**Concept: Dijkstra's algorithm.** Repeatedly take the unvisited vertex with the smallest tentative distance (from a priority queue), fix it, and relax its outgoing edges. Works only with non-negative weights.

@@ maq-q23
**Answer: (d) Floyd–Warshall**

**Why.** It computes shortest paths between all pairs, handles negative edges, and needs no negative cycles. O(V³). Bellman–Ford handles negative edges but from a single source; Dijkstra needs non-negative weights; Kruskal builds spanning trees.

**Concept: Floyd–Warshall.** dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j]) for each intermediate vertex k in turn. After processing k, paths may use vertices 1..k in the middle. A negative dist[i][i] at the end reveals a negative cycle.

@@ maq-q30
**Answer: (b) 9**

**Why.** A spanning tree on V vertices always has V − 1 edges (if the graph is connected), whatever the number of edges in the graph.

**Concept: trees have V − 1 edges.** A tree is connected with no cycles. Fewer edges would disconnect it; one more edge would create a cycle.

@@ mw-iitb-7
**Answer: a queue (BFS) and a stack (DFS)**

**Why.** BFS processes vertices in the order they were discovered (FIFO), level by level. DFS goes as deep as possible, returning to the most recent vertex with unexplored neighbours (LIFO); recursion supplies the stack.

**Concept: traversal order follows the container.** Swap the queue in BFS for a stack and you get a DFS-like order; use a priority queue and you get Dijkstra/Prim.

@@ mw-nitd-9
**Answer: (a)** (Prim's algorithm, growing from a root to adjacent vertices; picking the heaviest crossing edge each time gives a maximum spanning tree)

**Why.** Prim's algorithm grows one tree from a starting vertex through adjacent vertices. Taking the heaviest edge leaving the tree each time (instead of the lightest) produces a maximum spanning tree. (b) builds a minimum tree; (c) describes Kruskal's edge order but calls it Prim's. (The candidate chose (d).)

**Concept: maximum spanning tree.** Any MST algorithm finds a maximum spanning tree if you reverse the comparison (or negate all weights).

@@ paytm-critical-mst
**Answer: (a) and (d)**

**Why.** The MST weight is 1 + 2 + 2 + 5 + 5 = 15: the three light edges (0–1, 1–2, 2–3), one of the two weight-5 cycle edges (3–4 or 0–4), and 4–5.
- Remove 0–1: both weight-5 cycle edges are needed, weight 18 > 15, so critical.
- 4–5 is a bridge (the only link to vertex 5): removing it disconnects the graph, so critical.
- 3–4 and 0–4 can replace each other, so neither is critical.
(1–2 and 2–3 are critical too, but not offered.)

**Concept: critical vs pseudo-critical MST edges.** An edge is critical if every MST must contain it (removing it raises the MST weight). It is pseudo-critical if some MSTs use it and some don't (ties). Test: remove the edge and recompute the MST weight.

@@ paytm-dfs
**Answer: (b) only**

**Why.** In DFS the next vertex must be an unvisited neighbour of the deepest vertex on the current path that still has one.
- (a): after 0, 2 the search must go to 3 (2's only unvisited neighbour) before anything else.
- (b): 0 → 5 → 6, back to 5 → 7, back → 1 → 8, back to 1 → 4; back to 0 → 2 → 3. Valid.
- (c): visits 3 right after 4, but 3 is adjacent only to 2.
- (d): after 8 the search backtracks to 1, which still has 4 unvisited, so 4 must come next, not 2.

**Concept: checking a DFS order.** Keep the current path as a stack. Each next vertex must be adjacent to the top of the stack; if the top has no unvisited neighbours, pop and try again. Neighbour order is free, so many orders can be valid.

@@ ti-kruskal
**Answer: Kruskal's algorithm**

**Why.** Sorting all edges and repeatedly adding the lightest one that does not form a cycle, until V − 1 edges, is exactly Kruskal's method.

**Concept: Kruskal vs Prim.** Kruskal: global sorted edge list, union-find to detect cycles, O(E log E). Prim: grow one tree from a vertex with a priority queue, O(E log V). Both are greedy and correct by the cut property.

@@ wbd-16
**Answer: (c) queue**

**Why.** BFS visits vertices in the order they were discovered, which is first-in-first-out.

**Concept: BFS finds shortest paths in unweighted graphs.** Because it explores all vertices at distance d before any at d + 1, the first time it reaches a vertex is along a shortest path.

@@ fj-kgp-ds1
**Answer: (c) linear probing**

**Why.** "Searching for the next available slot" is linear probing: try h, h + 1, h + 2, ... (mod size). Quadratic probing tries h + 1², h + 2², ...; a linked list is used by separate chaining, the opposite of open addressing. (Strictly the underlying structure is an array; probing is the collision strategy.)

**Concept: open addressing.** All keys live in the array itself. On a collision you probe other slots in a fixed sequence. Linear probing is cache-friendly but forms clusters; quadratic probing and double hashing spread keys out more.

@@ ion-q19
**Answer: (b) both keys are stored in a list at that slot**

**Why.** With separate chaining, each slot holds a list (or another container) of all entries that hash there. Resizing is a separate policy based on the load factor, not a response to one collision.

**Concept: separate chaining.** Search = hash to a bucket, then scan its list. Average cost O(1 + α), where α = n / buckets is the load factor.

@@ sig-hash
**Answer: (b) 15⁵/20⁵**

**Why.** Each value lands in a uniformly random slot independently. Avoiding the first 5 slots has probability 15/20 for each value. With chaining, slots can be reused, so the five factors are all 15/20: (15/20)⁵.

**Concept: independent uniform hashing.** Each key's slot is like a die roll with "number of slots" faces. With chaining, keys do not exclude each other's slots, so probabilities multiply without decreasing (unlike drawing without replacement, which is option (c)).

@@ wbd-14
**Answer: (c) O(n)**

**Why.** In the worst case every key hashes to the same bucket, forming one chain of n entries, and a search may scan all of it. (Java 8's HashMap turns long chains into trees to get O(log n), but the textbook answer is O(n).)

**Concept: average vs worst case.** Hash tables are O(1) on average with a good hash function and bounded load factor, but O(n) in the worst case. Adversarial inputs can trigger it, which is why some libraries use randomised hashing.

@@ wbd-23
**Answer: (d) the size of the elements stored**

**Why.** Lookup cost depends on the load factor (elements ÷ buckets) and on how evenly the hash function spreads keys. How big each stored value is does not change the number of probes (only, slightly, the cost of hashing and comparing keys).

**Concept: load factor.** α = n / buckets. Tables resize (usually doubling) when α passes a threshold (e.g. 0.75) to keep chains short.

@@ epam-q3
**Answer: (b) 5** (reading the photo as 11 slots with 6 used)

**Why.** In a linear (non-circular) queue, new elements go only after the rear. With 6 filled slots in an array of 11, only the 5 empty slots after the rear can be used; the 6th enqueue overflows. Slots freed at the front by dequeues are not reused, which is the weakness a circular queue fixes.

**Concept: linear vs circular queue.** Linear: rear only moves forward, so space at the front is wasted after dequeues ("false overflow"). Circular: indices wrap with `% size`, so every free slot can be reused.

@@ epam-q5
**Answer: (c) it inserts a node at the end of the linked list**

**Why.** The new node's `next` is NULL. An empty list gets it as the head. Otherwise the loop walks to the last node and links the new node after it. O(n) per insertion; keeping a tail pointer makes it O(1).

**Concept: why `Node**`.** To change the caller's head pointer (when the list is empty), the function needs the address of that pointer, i.e. a pointer to a pointer.

@@ ion-q20
**Answer: (a) 7**

**Why.** [5] → [5, 8] → dequeue → [8] → [8, 3] → [8, 3, 7] → dequeue → [3, 7] → [3, 7, 10] → dequeue → [7, 10]. The front is 7.

**Concept: FIFO.** A queue removes the element that has waited longest. Track the queue's contents after each operation.

@@ mw-iisc-24
**Answer: (d) between 15 and −100** (the value is −18)

**Why.** Postfix: push 6, 3, 2, 4. `+` pops 2 and 4 → 6. `−` pops 3 and 6 → 3 − 6 = −3. `*` pops 6 and −3 → −18.

**Concept: evaluating postfix with a stack.** Push numbers; on an operator, pop the top two (the first popped is the right operand), apply, push the result. The final stack holds the answer.

@@ or-postfix
**Answer: (a) `abc*+de*+`**

**Why.** `*` binds tighter than `+`, and `+` is left-associative: ((a + (b*c)) + (d*e)). In postfix each operator follows its operands: a, then b c *, then +, then d e *, then +.

**Concept: infix to postfix.** Postfix (reverse Polish) writes operators after their operands and needs no brackets. Convert with the shunting-yard algorithm: output operands immediately, hold operators on a stack, and pop operators of higher or equal precedence before pushing a new one.

@@ paytm-infix-stack
**Answer: (c) 3**

**Why.** Only operators and parentheses go on the stack. `(` `−` → depth 2; `)` empties it. `*` pushed; `/` pops it (same precedence, left-associative) and is pushed. Then `(` and `/` → `/ ( /`: depth 3. `−` pops the inner `/` and gives `/ ( −`: still 3. `)` unwinds to `/`; the last `*` replaces it. Maximum 3.

**Concept: shunting-yard stack depth.** The stack holds pending operators. Equal-precedence left-associative operators pop each other, so the stack only grows with nesting and rising precedence.

@@ paytm-max-stack
**Answer: (c) 4**

**Why.** Stack sizes after each operation: 1, 0, 1, 2, 3, 2, 3, 4, 3. The maximum is 4, after Push(77).

**Concept: track size, not contents.** For "maximum height" questions, keep a running count (+1 push, −1 pop).

@@ paytm-postfix-stack
**Answer: (a) 1, 1**

**Why.** Push 6, 3, 2; `*` → 3 × 2 = 6, stack [6, 6]; `/` → 6 / 6 = 1, stack [1]. Push 3, 2, 1: [1, 3, 2, 1]. Just before the second `*`, the top is 1 and the bottom is 1.

**Concept: postfix evaluation with a stack** (see above): pop two, apply, push the result.
