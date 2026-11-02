@@ qc-iisc-stack
**Answer: (b) underflow**

**Why.** Push 2 → [2]; Push 1 → [2, 1]; Pop → [2]; Push 3 → [2, 3]; Pop → [2]; Pop → []; Pop on an empty stack → underflow.

**Concept: overflow and underflow.** Overflow = pushing onto a full stack (capacity reached). Underflow = popping from an empty one. Implementations check `top == -1` before popping.

@@ qc25-stacks
**Answer: (c)** is incorrect

**Why.** Stacks are implemented with arrays or linked lists, not trees. (a) Bracket balancing is a classic stack application. (b) An empty stack cannot be popped (underflow). (d) With the usual convention top = −1 for empty, top = 0 means exactly one element.

**Concept: stack applications.** Matching brackets, undo, function calls (the call stack), expression evaluation and conversion, DFS, backtracking.

@@ qc60-29
**Answer: (b) P → A → X → B → M**

**Why.** Step 1 puts P before A as the new head. Step 2 makes the 3rd node (X, counting P, A, X) point to B and B's prev point to X, bypassing Y. Step 3 appends M after B.

**Concept: doubly linked list updates.** Each node has `prev` and `next`. Removing or bypassing a node means fixing both directions: the previous node's `next` and the following node's `prev`.

@@ qc60-36
**Answer: (d) overflow**

**Why.** In a linear queue of size 5: A P Q → enqueue J → A P Q J (rear at slot 4) → dequeue removes A (front moves on, but the slot is not reused) → enqueue M fills slot 5 → enqueue D: rear is already at the last slot, so overflow. (Even counting only live elements, P Q J M D is 5, and X would overflow.)

**Concept: linear queue limits.** Rear only moves forward. Once it reaches the end, further enqueues overflow even if dequeued slots at the front are free. A circular queue avoids this.

@@ qc60-57
**Answer: (a) the last node's reference must be NULL**

**Why.** The tail's `next` is NULL to mark the end. Inserting in the middle is possible (b false); trees and graphs are built from linked nodes (c false); the head has no previous node (d false).

**Concept: singly linked lists.** Each node stores data and a pointer to the next. You reach any node by walking from the head; NULL marks the end.

@@ ti-circ-delete
**Answer: `prev->next = cur->next;` (and if `cur == head`, move `head` to `cur->next`), then free `cur`.**

**Why.** Linking the predecessor directly to the successor removes `cur` from the cycle. If `cur` was the head, the head pointer must move too, or it would point at freed memory. (If it was the only node, the list becomes empty.)

**Concept: deleting from a circular list.** Same as a normal list, but there is no NULL end, so be careful with the head and with the one-node case (`cur->next == cur`).

@@ ti-cycle
**Answer: Floyd's cycle-finding algorithm** (slow and fast pointers)

**Why.** Move one pointer one step and another two steps at a time. If there is a loop, the fast pointer eventually catches the slow one inside it; if fast reaches NULL, there is no loop. O(n) time, O(1) space. (A hash set of visited nodes also works, with O(n) space.)

**Concept: why the pointers must meet.** Inside the loop the fast pointer gains one step per move on the slow one, so the gap shrinks by 1 each move until it is 0. To find the loop's start, reset one pointer to the head and move both one step at a time; they meet at the start.

@@ ti-queue-stack
**Answer: `q.front()` is 2 and `s.top()` is 3**

**Why.** Queue after enqueues: [3, 5, 2]. Dequeue 3 → push → s = [3]. Dequeue 5 → push → s = [3, 5]. Pop → s = [3]. The queue now holds [2].

**Concept: FIFO vs LIFO.** The queue gives back the oldest element; the stack gives back the newest. Track both containers step by step.

@@ wbd-15
**Answer: (d) No, it is feasible**

**Why.** With two queues (or one queue rotated), one of push or pop costs O(n) and the other O(1). That is slower than a native stack but workable, and it uses O(n) memory, the same as the data itself.

**Concept: stack from queues.** To pop the newest item from a FIFO structure, move the other n − 1 items around it. Interviews ask this to test understanding of both structures, not as a practical design.

@@ wbd-25
**Answer: (d) all of the above**

**Why.** Inserting or deleting at a known node needs no shifting (a). Getting the k-th element needs a walk from the head (b). Nodes are allocated one at a time, so the list grows and shrinks freely (c).

**Concept: arrays vs linked lists.** Arrays: contiguous, O(1) index access, cache-friendly, costly inserts. Linked lists: scattered nodes, O(n) access, cheap inserts/deletes, extra memory for pointers.

@@ wbd-7
**Answer: (d) none of the above**

**Why.** A stack is LIFO, so pop must remove from the **same** end that push inserts at, normally the head (O(1) both ways). (a) and (b) push and pop at opposite ends, which is a queue.

**Concept: linked-list stack.** Push = insert at head; pop = remove head. Both O(1), no capacity limit.

@@ sig-tail
**Answer: (c) 1**

**Why.** In a tail-recursive function the recursive call is the last thing done, so nothing in the current frame is needed afterwards. With tail-call optimisation the compiler reuses the same frame for each call, turning the recursion into a loop: one frame at any time.

**Concept: tail calls.** `return f(n − 1, acc * n);` is a tail call; `return n * f(n − 1);` is not (the multiplication happens after the call returns). C/C++ compilers often optimise tail calls at -O2; Python never does.

@@ ti-fruit
**Answer: `max(n, Solve(n/2) + Solve(n/3) + Solve(n/4))`** (e.g. 12 gives 13); memoise it for large n

**Why.** At each value you choose the better of selling it now (n) or splitting and doing the best with each part. For 12: 12 vs 6 + 4 + 3 = 13, so 13.

**Concept: recursion with memoisation.** The same sub-values repeat (n/2/3 = n/3/2), so store results in a map to avoid recomputing. This is the "Bytelandian gold coins" problem.

@@ fj-kgp-ds5
**Answer: (c) bubble sort**

**Why.** Bubble sort is O(n²) in the worst case and is used mainly because it is simple. Quicksort can also be O(n²) but is chosen for its average speed, not simplicity. (In practice insertion sort is the usual choice for small inputs.)

**Concept: bubble sort.** Repeatedly swap adjacent out-of-order pairs; after pass k, the k largest are in place. With an "any swaps?" flag it stops early on sorted input (O(n) best case).

@@ go-4
**Answer: (b) insertion sort, O(n²)**

**Why.** Each `key` is shifted left past larger elements into the sorted prefix. Worst case (reverse order): 1 + 2 + ... + (n − 1) = n(n − 1)/2 shifts. Best case (already sorted): O(n).

**Concept: insertion sort.** Like sorting playing cards in your hand: take the next card and slide it left into place. It is stable, in-place, fast on nearly-sorted data, and online (can sort data as it arrives).

@@ ion-q21
**Answer: (b) insertion sort, O(n²)**

**Why.** Same code as the previous question: build a sorted prefix by inserting each `key` into place. O(n) on sorted input, O(n²) in the average and worst cases.

**Concept: recognising sorts from code.** Insertion: shifting with `arr[j + 1] = arr[j]` inside a while loop. Bubble: adjacent swaps in nested for loops. Selection: find the min index, then one swap per pass.

@@ maq-q32
**Answer: (e) none** (statements 1 and 3 are correct, 2 is false; no option says "1 and 3")

**Why.** Statement 2 describes DFS ("as far as possible along each branch"), not BFS. BFS explores level by level.

**Concept: BFS vs DFS.** BFS: queue, level by level, shortest paths in unweighted graphs. DFS: stack/recursion, deep first, used for cycle detection, topological sort, connected components.

@@ mw-iisc-26
**Answer: (a) 45321, 34521, 23451, 12345**

**Why.** Pass i inserts element i + 1 into the sorted prefix: insert 4 → 45321; insert 3 → 34521; insert 2 → 23451; insert 1 → 12345.

**Concept: insertion sort passes.** After pass i, the first i + 1 elements are sorted among themselves (but not yet in their final places).

@@ mw-nitd-10
**Answer: (c) postorder 6, 7, 9, 8, 12, 11, 15, 13, 10**

**Why.** It is not a BST: 7 sits in 9's left subtree, which is in 8's right subtree, but 7 < 8. The root has 2 children, so its degree is 2. BST subtrees: the four leaves (6, 7, 12, 15), plus 9 (7 < 9), 11 and 13: 7 in total, not 8. Postorder (left, right, root): 6, 7, 9, 8, 12, 11, 15, 13, 10.

**Concept: BST property is global.** Every node in the left subtree (not just the left child) must be smaller than the node, and every node in the right subtree larger. Check with min/max bounds as you go down.

@@ qc-iisc-bsearch
**Answer: (c) 12**

**Why.** Indices 0–8. Pass 1: middle index 4, value 54. Pass 2: middle of the left half (0–3) is index 1 (18), or of the right half (5–8) index 6 (74). Pass 3: below 18 only index 0 is left (12), or between 18 and 54 the middle is 41. So 12 is found in pass 3 (18 and 74 in pass 2, 47 needs 4 passes).

**Concept: binary search as a decision tree.** The first probe is the root, the next probes are its children, and so on. A value's depth in that tree is the number of passes needed to find it.

@@ qc60-26
**Answer: (d) 3**

**Why.** Sort descending by placing the smallest remaining element at the end each pass; count only passes that need a swap.

| Pass | Range | Smallest | Swap? | Array after |
|---|---|---|---|---|
| 1 | all 7 | 17 (already last) | no | 43 23 98 61 29 30 17 |
| 2 | first 6 | 23 | yes | 43 30 98 61 29 23 17 |
| 3 | first 5 | 29 (already last) | no | same |
| 4 | first 4 | 30 | yes | 43 61 98 30 29 23 17 |
| 5 | first 3 | 43 | yes | 98 61 43 30 29 23 17 |
| 6 | first 2 | 61 (already last) | no | same |

**Concept: selection sort.** Each pass selects the extreme element of the unsorted part and swaps it into place: at most n − 1 swaps, but always n(n − 1)/2 comparisons. That few swaps is its one advantage (good when writes are expensive).

@@ qc60-31
**Answer: (b) 3**

**Why.** Pass 1: middle is 30 (index 3); 69 > 30, go right. Pass 2: [48, 51, 69], middle 51; go right. Pass 3: 69, found.

**Concept: binary search** compares with the middle and discards half each time: at most ⌊log₂ n⌋ + 1 passes (here 3 for n = 7).

@@ sig-circular
**Answer: (b) 2 pointers**

**Why.** Insert X after node P: X.next = P.next, then P.next = X. Two pointer changes. (Inserting before the head may also require moving the head, or fixing the last node's pointer.)

**Concept: link the new node first.** Always set the new node's `next` before changing the old node's `next`, or you lose the rest of the list.

@@ sig-quicksort
**Answer: (a) quick sort**

**Why.** Quicksort partitions the array around a pivot (smaller elements left, larger right) by exchanging elements, then sorts each part. Hence "partition-exchange sort". (The question also calls it stable, which quicksort is not.)

**Concept: quicksort.** Average O(n log n), worst O(n²) (bad pivots, e.g. sorted input with first-element pivot). In-place and fast in practice; randomised or median-of-three pivots avoid the worst case.

@@ sig-selection
**Answer: (a) O(n²)**

**Why.** Selection sort always scans the whole unsorted part to find the minimum, in every case: (n − 1) + (n − 2) + ... + 1 comparisons.

**Concept: input-independent cost.** Selection sort does the same comparisons on any input, so its best, average and worst cases are all O(n²).

@@ ti-binsearch
**Answer: `binarySearch(A, value, low, mid - 1)`**

**Why.** If the middle element is larger than the value, the value (if present) must be to its left, so search low..mid − 1.

**Concept: shrink the range correctly.** Exclude mid itself (`mid − 1` or `mid + 1`), otherwise the range may stop shrinking and the recursion never ends.

@@ ti-circular-insert
**Answer: (a) insert at the beginning**

**Why.** The new node links to the old head, the last node links to the new node (keeping the circle), and `head = ptr` makes the new node the head. (Without the `head = ptr` line, the same steps would insert at the end; the key's "end" is wrong.)

**Concept: in a circular list, beginning and end are the same position.** The only difference is which node the `head` pointer marks.

@@ ti-mergesort
**Answer: (d) none of these** (it is O(n log n))

**Why.** Extra base cases for n = 1 and n = 2 don't change the recurrence T(n) = 2T(n/2) + O(n), which solves to O(n log n).

**Concept: merge sort.** Split in halves, sort each recursively, merge in linear time. Always O(n log n), stable, needs O(n) extra space.

@@ ti-online-sort
**Answer: (d) insertion sort**

**Why.** Insertion sort keeps a sorted prefix and inserts each new element into it, so it can take elements as they arrive (it is an "online" algorithm). The others need the whole input up front.

**Concept: online algorithms.** They process input piece by piece without knowing the future. Insertion sort is online; heap-based structures also suit streams.

@@ wbd-11
**Answer: (a) O(n log n)**

**Why.** Standard merge sort always splits down to single elements and merges every level, regardless of input order. (Natural merge sort or Timsort detect the single sorted run and take O(n), but that is not plain merge sort.)

**Concept: adaptive vs non-adaptive sorts.** Adaptive sorts (insertion, Timsort) run faster on nearly sorted input; merge sort and heap sort do not.

@@ wbd-12
**Answer: (d) binary search**

**Why.** On a sorted array, binary search takes O(log n) comparisons. Linear search is O(n); DFS and BFS are graph traversals.

**Concept: sortedness enables halving.** Binary search needs both sorted order and O(1) random access (an array, not a linked list).

@@ epam-q6
**Answer: (a) 1 and 2 only**

**Why.** Compare the left subtree with the mirror of the right one (shapes only). Tree 1: 6 has a right child, 14 a left child — mirrors. Tree 2: 6 left, 14 right — mirrors. Tree 3: both grandchildren are left children — not mirrors. Tree 4: three grandchildren, so the sides cannot match.

**Concept: mirror check recursively.** Two subtrees L and R are mirrors if both are empty, or both exist and L.left mirrors R.right and L.right mirrors R.left.

@@ fj-kgp-ds2
**Answer: (b) height of the left subtree minus height of the right subtree**

**Why.** An AVL tree keeps this balance factor in {−1, 0, +1} at every node, and rotates when an insertion or deletion pushes it to ±2.

**Concept: AVL trees.** Self-balancing BSTs: the height stays O(log n), so search, insert and delete are O(log n). Rotations (LL, RR, LR, RL) restore balance locally.

@@ fj-kgp-ds3
**Answer: (c) binary heap**

**Why.** A binary heap gives O(log n) insert and extract-min/max, O(1) peek, and is stored compactly in an array. A balanced BST also gives O(log n) but with more overhead.

**Concept: binary heap.** A complete binary tree where each parent is ≤ its children (min-heap). Stored in an array: children of i at 2i + 1 and 2i + 2. Insert = add at end and bubble up; extract = move last to root and sift down.

@@ go-1
**Answer: only (a)**

**Why.** In a DFS order each new node must be adjacent to the deepest node on the current path that still has unvisited neighbours.
- (b) goes 13 → 14, but they are not adjacent, and 13 still has the unvisited neighbour 12.
- (c) goes 14 → 13 while 14's neighbour 12 is unvisited (and 13 is not adjacent to 14).
- (d) jumps from the 1-2-3 triangle back to 4 and then visits 7, which is not adjacent to 4.

**Concept: validate DFS orders with a stack.** Keep the current path; the next vertex must be a neighbour of the top; if the top has no unvisited neighbours, pop.

@@ ion-q18
**Answer: (c) directed acyclic graph (DAG)**

**Why.** An expression DAG is a syntax tree in which common subexpressions are shared (a*b used twice is stored once). Dependencies only point one way, so there are no cycles. A stack is used **while** parsing, but does not model the dependencies.

**Concept: expression trees and DAGs.** Leaves are operands, internal nodes are operators. Merging identical subtrees gives a DAG, which compilers use for common-subexpression elimination.

@@ mw-iiitd-12
**Answer: (a)** is false

**Why.** If an MST contains the heaviest edge e, removing e from the tree splits the vertices into two sides. Every other edge across that cut must be at least as heavy as e (otherwise swapping it in would give a lighter tree), so all crossing edges have the maximum weight: such a cutset exists, making (a) false. (b), (c), (d) can be true or false depending on G.

**Concept: the cut property.** For any cut, the lightest edge crossing it belongs to some MST. Equivalently, an MST edge is a lightest edge across the cut it defines.

@@ mw-iitb-12
**Answer: (a) and (c)**

**Why.** Without the inorder sequence you cannot tell a left child from a right child: a root with one child gives the same preorder, postorder and level order whether the child is left or right. Inorder plus level order (or plus preorder/postorder) is unique. (The candidate ticked all three.)

**Concept: inorder separates left and right.** The root's position in the inorder sequence splits it into the left and right subtrees; the other traversal tells you which node is the root.

@@ nv-19
**Answer: (b) doubly linked list** (the usual key)

**Why.** A tree node with two pointers (left, right) has the same shape as a doubly-linked-list node (two pointers). An AVL tree already **is** a binary tree, so it cannot be its implementation. Arrays (heap-style indexing) are the other standard answer but are not offered.

**Concept: two ways to store a binary tree.** Linked nodes with left/right pointers (any shape), or an array where node i has children at 2i + 1 and 2i + 2 (compact for complete trees, wasteful for sparse ones).

@@ or-23tree
**Answer: (a)** is false

**Why.** A 3-node holds two keys and three child pointers, so a 2-3 tree generally needs **more** storage for the same keys. Being balanced (all leaves at the same depth), it is shallower than an arbitrary BST and guarantees O(log n) lookup.

**Concept: 2-3 trees.** Each node has 2 or 3 children; insertion splits overfull nodes upward, keeping perfect balance. Red-black trees are a binary encoding of the same idea.

@@ paytm-in-pre-post
**Answer: (b) [9, 4, 6, 2, 7, 3, 10, 5, 1, 8]**

**Why.** Root = 8 (first in preorder). Inorder splits into left [9, 2, 4, 6] and right [7, 3, 1, 5, 10].
- Left, preorder [2, 9, 6, 4]: root 2, left 9, right 6 whose left child is 4. Postorder: 9, 4, 6, 2.
- Right, preorder [1, 3, 7, 5, 10]: root 1, left 3 (left child 7), right 5 (right child 10). Postorder: 7, 3, 10, 5, 1.
- Whole: left, right, root. (One photo ticks (c), which puts 3 before its child 7.)

**Concept: rebuild from preorder + inorder.** The first preorder element is the root; find it in inorder to split left and right sizes; recurse on each part with the matching slice of preorder.

@@ paytm-inorder
**Answer: (b) ABCDEFGHI**

**Why.** Inorder = left, root, right. Left subtree of F: A, B, C, D, E. Then F. Right subtree: G (no left child), then I's subtree: its left child H, then I. Option (a) is the preorder and (c) the postorder. (The tree is a BST on letters, so inorder gives sorted order, a quick check.)

**Concept: three depth-first traversals.** Preorder: root, left, right. Inorder: left, root, right. Postorder: left, right, root. Inorder of a BST is sorted.

@@ qc-iisc-internal
**Answer: (d) 4**

**Why.** Internal nodes have at least one child: 45, 30, 50 and 48. The leaves are 22 and 49.

**Concept: internal vs leaf nodes.** A leaf has no children. In any tree, nodes = internal + leaves.

@@ qc-n-bst
**Answer: (d) 30**

**Why.** Inserting 40, 30, 25, 45, 50, 19, 27 gives: 40 with left 30 (left child 25, which has children 19 and 27) and right 45 (right child 50). Node 30 has left height 2 and right height 0: unbalanced. Deleting 30 lets 25 take its place with children 19 and 27, and every node becomes balanced. (Deleting 50 instead leaves the root unbalanced.)

**Concept: balance = subtree heights differ by at most 1 at every node.** Find the lowest unbalanced node; fixing it (here by deletion) often fixes its ancestors too.

@@ qc-n-degenerate
**Answer: (c) degenerate tree**

**Why.** If every parent has exactly one child, the tree is a single chain, effectively a linked list, with height n − 1 and O(n) operations.

**Concept: tree shapes.** Full: every node has 0 or 2 children. Complete: all levels full except possibly the last, filled left to right. Perfect: all levels full. Degenerate: one child each, the worst case for a BST.

@@ sig-full-tree
**Answer: (a) 19**

**Why.** In a full binary tree (every internal node has exactly 2 children), internal nodes = leaves − 1 = 9. Total = 10 + 9 = 19.

**Concept: L = I + 1 for full binary trees.** Each internal node adds 2 child slots but uses up 1 (its own), so leaves exceed internal nodes by exactly one.

@@ sig-height
**Answer: (b) 3**

**Why.** height(null) = 0 and height(node) = 1 + max(children). Leaves have height 1, their parents 2, the root 3: three levels of nodes.

**Concept: height conventions.** Some count nodes on the longest root-to-leaf path (here 3), others count edges (2). Read the code's base case to know which.

@@ wbd-13
**Answer: (b) d e b f g c a**

**Why.** Preorder starts with the root a. Inorder splits around a: left {d, b, e}, right {f, c, g}. Preorder of the left is b d e: root b, children d and e. Right: root c, children f and g. Postorder (left, right, root): d e b, f g c, a.

**Concept: rebuild from preorder + inorder** (same method as above).

@@ wbd-6
**Answer: (a) 2^(i−1)**

**Why.** Level 1 has at most 1 node; each level can at most double the previous: 1, 2, 4, ..., so level i has at most 2^(i−1).

**Concept: binary tree capacity.** With levels numbered from 1, a tree of height h has at most 2ʰ − 1 nodes. If levels start at 0, level i holds at most 2ⁱ.
