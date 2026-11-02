---
title: "Trees (BST, AVL, heap, traversals)"
weight: 3
---

18 questions asked by EPAM, Fujitsu, Grey Orange, ION Group, MathWorks, NVIDIA, Oracle, Paytm, Qualcomm, Sigmoid, Warner Bros. Discovery. Try each one first, then open the toggle: it gives the answer, why it is right, and the idea behind it explained from scratch.

### 1 · Q6, which binary trees can be folded

*Asked by: EPAM (EPAM freshers test)*

A binary tree can be *folded* if its left and right subtrees are structural mirror
images (values do not matter). Which of these trees can be folded?

1. Root 1, children 6 and 14; 6 has a right child 8; 14 has a left child 11.
2. Root 1, children 6 and 14; 6 has a left child 8; 14 has a right child 11.
3. Root 1, children 7 and 12; 7 has a left child 5; 12 has a left child 11.
4. Root 1, children 7 and 12; 7 has children 5 and 11; 12 has a left child 11.

- **(a)** 1 and 2 only
- **(b)** 2 and 3 only
- **(c)** 3 and 4 only
- **(d)** 1 and 4 only

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) 1 and 2 only**

**Why.** Compare the left subtree with the mirror of the right one (shapes only). Tree 1: 6 has a right child, 14 a left child — mirrors. Tree 2: 6 left, 14 right — mirrors. Tree 3: both grandchildren are left children — not mirrors. Tree 4: three grandchildren, so the sides cannot match.

**Concept: mirror check recursively.** Two subtrees L and R are mirrors if both are empty, or both exist and L.left mirrors R.right and L.right mirrors R.left.

{{< /details >}}

### 2 · DS Q2, AVL balance factor

*Asked by: Fujitsu (IIT Kharagpur 2023)*

In the context of data structures, what is the "balancing factor" of an AVL tree?

- **(a)** The number of nodes in the left subtree minus the number of nodes in the right subtree
- **(b)** The height of the left subtree minus the height of the right subtree
- **(c)** The height of the tree
- **(d)** The number of leaf nodes in the tree

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) height of the left subtree minus height of the right subtree**

**Why.** An AVL tree keeps this balance factor in {−1, 0, +1} at every node, and rotates when an insertion or deletion pushes it to ±2.

**Concept: AVL trees.** Self-balancing BSTs: the height stays O(log n), so search, insert and delete are O(log n). Rotations (LL, RR, LR, RL) restore balance locally.

{{< /details >}}

### 3 · DS Q3, priority queue

*Asked by: Fujitsu (IIT Kharagpur 2023)*

Which data structure is best suited for implementing a priority queue efficiently,
especially with dynamic updates?

- **(a)** Array
- **(b)** Linked List
- **(c)** Binary Heap
- **(d)** AVL Tree

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) binary heap**

**Why.** A binary heap gives O(log n) insert and extract-min/max, O(1) peek, and is stored compactly in an array. A balanced BST also gives O(log n) but with more overhead.

**Concept: binary heap.** A complete binary tree where each parent is ≤ its children (min-heap). Stored in an array: children of i at 2i + 1 and 2i + 2. Insert = add at end and bubble up; extract = move last to root and sift down.

{{< /details >}}

### 4 · Q1, DFS traversal

*Asked by: Grey Orange (OA, Oct 2024)*

Which of the following is/are a valid DFS traversal starting from node 9 of the given
graph? There may be more than one. (Pick one or more.)
[figure: see the original PDF]
(Graph redrawn from the screenshot: edges 1-2, 1-3, 2-3, 3-4, 4-8, 4-6, 8-7,
7-5, 7-6, 8-9, 9-10, 9-11, 11-12, 11-14, 11-13, 12-14, 12-13.)

- **(a)** 9, 10, 11, 13, 12, 14, 8, 7, 5, 6, 4, 3, 2, 1
- **(b)** 9, 10, 11, 13, 14, 12, 8, 7, 5, 6, 4, 3, 2, 1
- **(c)** 9, 8, 4, 3, 1, 2, 6, 7, 5, 10, 11, 14, 13, 12
- **(d)** 9, 8, 4, 3, 1, 2, 7, 6, 5, 10, 11, 14, 13, 12

{{< details title="Answer and explanation" closed="true" >}}

**Answer: only (a)**

**Why.** In a DFS order each new node must be adjacent to the deepest node on the current path that still has unvisited neighbours.
- (b) goes 13 → 14, but they are not adjacent, and 13 still has the unvisited neighbour 12.
- (c) goes 14 → 13 while 14's neighbour 12 is unvisited (and 13 is not adjacent to 14).
- (d) jumps from the 1-2-3 triangle back to 4 and then visits 7, which is not adjacent to 4.

**Concept: validate DFS orders with a stack.** Keep the current path; the next vertex must be a neighbour of the top; if the top has no unvisited neighbours, pop.

{{< /details >}}

### 5 · Q18, modelling an expression dependency tree

*Asked by: ION Group (SDE OA, Jul 2025)*

What is the best data structure to model the dependency tree used in compilers for parsing
expressions?

- **(a)** Stack
- **(b)** Heap
- **(c)** Directed Acyclic Graph (DAG)
- **(d)** Queue

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) directed acyclic graph (DAG)**

**Why.** An expression DAG is a syntax tree in which common subexpressions are shared (a*b used twice is stored once). Dependencies only point one way, so there are no cycles. A stack is used **while** parsing, but does not model the dependencies.

**Concept: expression trees and DAGs.** Leaves are operands, internal nodes are operators. Merging identical subtrees gives a DAG, which compilers use for common-subexpression elimination.

{{< /details >}}

### 6 · Q12, the heaviest edge in an MST

*Asked by: MathWorks (IIIT Delhi 2024)*

Let $G$ be a weighted undirected graph and $e$ an edge of maximum weight. Suppose there
[is a minimum spanning tree containing $e$] [cut off in the source]. Which statements are FALSE?

- **(a)** There does not exist any cutset in G having all edges of maximum weight
- **(b)** There does not exist a cycle in G having all edges of maximum weight
- **(c)** Edge e can be contained in at least one cycle
- **(d)** All edges in G do not have the same weight

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a)** is false

**Why.** If an MST contains the heaviest edge e, removing e from the tree splits the vertices into two sides. Every other edge across that cut must be at least as heavy as e (otherwise swapping it in would give a lighter tree), so all crossing edges have the maximum weight: such a cutset exists, making (a) false. (b), (c), (d) can be true or false depending on G.

**Concept: the cut property.** For any cut, the lightest edge crossing it belongs to some MST. Equivalently, an MST edge is a lightest edge across the cut it defines.

{{< /details >}}

### 7 · Q12, unique binary trees

*Asked by: MathWorks (IIT Bombay 2024)*

From which traversal pairs can a binary tree NOT be constructed uniquely? (select all)

- **(a)** postorder and preorder
- **(b)** inorder and level order
- **(c)** postorder and level order

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) and (c)**

**Why.** Without the inorder sequence you cannot tell a left child from a right child: a root with one child gives the same preorder, postorder and level order whether the child is left or right. Inorder plus level order (or plus preorder/postorder) is unique. (The candidate ticked all three.)

**Concept: inorder separates left and right.** The root's position in the inorder sequence splits it into the left and right subtrees; the other traversal tells you which node is the root.

{{< /details >}}

### 8 · Q19, implementing a binary tree

*Asked by: NVIDIA (SSE NCG, Nov 2024)*

Which one of the following data structures would you consider using to implement a
binary tree?

- **(a)** Singly linked list
- **(b)** Doubly linked list
- **(c)** AVL tree
- **(d)** None of the above

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) doubly linked list** (the usual key)

**Why.** A tree node with two pointers (left, right) has the same shape as a doubly-linked-list node (two pointers). An AVL tree already **is** a binary tree, so it cannot be its implementation. Arrays (heap-style indexing) are the other standard answer but are not offered.

**Concept: two ways to store a binary tree.** Linked nodes with left/right pointers (any shape), or an array where node i has children at 2i + 1 and 2i + 2 (compact for complete trees, wasteful for sparse ones).

{{< /details >}}

### 9 · 2-3 tree versus BST

*Asked by: Oracle (HackerRank MCQ test)*

Which of the following is false?

- **(a)** 2-3 tree requires less storage than the BST
- **(b)** lookup in 2-3 tree is more efficient than in BST
- **(c)** 2-3 tree is shallower than BST
- **(d)** 2-3 tree is a balanced tree

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a)** is false

**Why.** A 3-node holds two keys and three child pointers, so a 2-3 tree generally needs **more** storage for the same keys. Being balanced (all leaves at the same depth), it is shallower than an arbitrary BST and guarantees O(log n) lookup.

**Concept: 2-3 trees.** Each node has 2 or 3 children; insertion splits overfull nodes upward, keeping perfect balance. Red-black trees are a binary encoding of the same idea.

{{< /details >}}

### 10 · postorder from inorder and preorder

*Asked by: Paytm (HackerRank, Sep 2025)*

Given the inorder and preorder traversals of a tree, find its postorder traversal.
Inorder: $[9, 2, 4, 6, 8, 7, 3, 1, 5, 10]$. Preorder: $[8, 2, 9, 6, 4, 1, 3, 7, 5, 10]$.

- **(a)** $[9, 6, 4, 2, 3, 7, 10, 5, 1, 8]$
- **(b)** $[9, 4, 6, 2, 7, 3, 10, 5, 1, 8]$
- **(c)** $[9, 4, 6, 2, 3, 7, 10, 5, 1, 8]$
- **(d)** None of the above

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) [9, 4, 6, 2, 7, 3, 10, 5, 1, 8]**

**Why.** Root = 8 (first in preorder). Inorder splits into left [9, 2, 4, 6] and right [7, 3, 1, 5, 10].
- Left, preorder [2, 9, 6, 4]: root 2, left 9, right 6 whose left child is 4. Postorder: 9, 4, 6, 2.
- Right, preorder [1, 3, 7, 5, 10]: root 1, left 3 (left child 7), right 5 (right child 10). Postorder: 7, 3, 10, 5, 1.
- Whole: left, right, root. (One photo ticks (c), which puts 3 before its child 7.)

**Concept: rebuild from preorder + inorder.** The first preorder element is the root; find it in inorder to split left and right sizes; recurse on each part with the matching slice of preorder.

{{< /details >}}

### 11 · inorder traversal

*Asked by: Paytm (HackerRank, Sep 2025)*

What is the inorder traversal of this tree? Root F; F's children are B and G; B's are A
and D; D's are C and E; G has only a right child I, whose only child is its left child H.

- **(a)** FBADCEGIH
- **(b)** ABCDEFGHI
- **(c)** ACEDBHIGF
- **(d)** ABCDEFGIH

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) ABCDEFGHI**

**Why.** Inorder = left, root, right. Left subtree of F: A, B, C, D, E. Then F. Right subtree: G (no left child), then I's subtree: its left child H, then I. Option (a) is the preorder and (c) the postorder. (The tree is a BST on letters, so inorder gives sorted order, a quick check.)

**Concept: three depth-first traversals.** Preorder: root, left, right. Inorder: left, root, right. Postorder: left, right, root. Inorder of a BST is sorted.

{{< /details >}}

### 12 · Q36, internal nodes

*Asked by: Qualcomm (IISc)*

A binary tree has root 45 with children 30 and 50; 30 has left child 22; 50 has left child 48;
48 has right child 49. How many internal nodes are there?

- **(a)** 2
- **(b)** 3
- **(c)** 6
- **(d)** 4

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) 4**

**Why.** Internal nodes have at least one child: 45, 30, 50 and 48. The leaves are 22 and 49.

**Concept: internal vs leaf nodes.** A leaf has no children. In any tree, nodes = internal + leaves.

{{< /details >}}

### 13 · Q58, balancing a BST

*Asked by: Qualcomm (Nov 2024)*

Construct a BST from $40, 30, 25, 45, 50, 19, 27$. Which node(s) should be deleted to make the
resulting BST balanced?

- **(a)** 30 and 27
- **(b)** 50
- **(c)** 50 and 19
- **(d)** 30

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) 30**

**Why.** Inserting 40, 30, 25, 45, 50, 19, 27 gives: 40 with left 30 (left child 25, which has children 19 and 27) and right 45 (right child 50). Node 30 has left height 2 and right height 0: unbalanced. Deleting 30 lets 25 take its place with children 19 and 27, and every node becomes balanced. (Deleting 50 instead leaves the root unbalanced.)

**Concept: balance = subtree heights differ by at most 1 at every node.** Find the lowest unbalanced node; fixing it (here by deletion) often fixes its ancestors too.

{{< /details >}}

### 14 · Q41, one child per parent

*Asked by: Qualcomm (Nov 2024)*

Identify the type of binary tree in which each parent node has only one associated child node.

- **(a)** Complete Binary Tree
- **(b)** Full Binary Tree
- **(c)** Degenerate Tree
- **(d)** None of the options given

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) degenerate tree**

**Why.** If every parent has exactly one child, the tree is a single chain, effectively a linked list, with height n − 1 and O(n) operations.

**Concept: tree shapes.** Full: every node has 0 or 2 children. Complete: all levels full except possibly the last, filled left to right. Perfect: all levels full. Degenerate: one child each, the worst case for a BST.

{{< /details >}}

### 15 · nodes of a full binary tree

*Asked by: Sigmoid (Campus hiring 2026)*

If a full binary tree has 10 leaf nodes, what is the total number of nodes?

- **(a)** 19
- **(b)** 9
- **(c)** 11
- **(d)** 20

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) 19**

**Why.** In a full binary tree (every internal node has exactly 2 children), internal nodes = leaves − 1 = 9. Total = 10 + 9 = 19.

**Concept: L = I + 1 for full binary trees.** Each internal node adds 2 child slots but uses up 1 (its own), so leaves exceed internal nodes by exactly one.

{{< /details >}}

### 16 · height of a binary tree

*Asked by: Sigmoid (Campus hiring 2026)*

What does the program print? `height(root)` returns 0 for `null` and otherwise
$1 + \max$ of the children's heights; the tree has root 15, children 10 and 20, and
grandchildren 8, 12, 16, 25 (one candidate's version uses slightly different values).

- **(a)** 2
- **(b)** 3
- **(c)** 4
- **(d)** 5

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) 3**

**Why.** height(null) = 0 and height(node) = 1 + max(children). Leaves have height 1, their parents 2, the root 3: three levels of nodes.

**Concept: height conventions.** Some count nodes on the longest root-to-leaf path (here 3), others count edges (2). Read the code's base case to know which.

{{< /details >}}

### 17 · Q13, postorder from inorder and preorder

*Asked by: Warner Bros. Discovery (HireVue, Nov 2024)*

The inorder and preorder traversals of a binary tree are `d b e a f c g` and
`a b d e c f g`. What is the postorder traversal?

- **(a)** e d b g f c a
- **(b)** d e b f g c a
- **(c)** e d b f g c a
- **(d)** d e f g b c a

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) d e b f g c a**

**Why.** Preorder starts with the root a. Inorder splits around a: left {d, b, e}, right {f, c, g}. Preorder of the left is b d e: root b, children d and e. Right: root c, children f and g. Postorder (left, right, root): d e b, f g c, a.

**Concept: rebuild from preorder + inorder** (same method as above).

{{< /details >}}

### 18 · Q6 and Q24, nodes on a level

*Asked by: Warner Bros. Discovery (HireVue, Nov 2024)*

The level of a node is its distance from the root, where the root is at level 1 and its
children at level 2. What is the maximum number of nodes on level $i$ of a binary tree?
(Asked twice in the same test, as questions 6 and 24.)

- **(a)** $2^{i-1}$
- **(b)** $2^{i}$
- **(c)** $2^{i+1}$
- **(d)** $2^{(i+1)/2}$

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) 2^(i−1)**

**Why.** Level 1 has at most 1 node; each level can at most double the previous: 1, 2, 4, ..., so level i has at most 2^(i−1).

**Concept: binary tree capacity.** With levels numbered from 1, a tree of height h has at most 2ʰ − 1 nodes. If levels start at 0, level i holds at most 2ⁱ.

{{< /details >}}
