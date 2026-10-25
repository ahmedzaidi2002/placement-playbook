---
title: "5 · Trees"
linkTitle: "5 Trees"
weight: 5
math: true
---
## 5.1 Vocabulary {#dsa-5-1}

**Root**, **parent**, **child**, **leaf** (no children), **internal node**, **depth** of a node (edges from the root), **height** of a tree (edges on the longest root-to-leaf path; a single node has height 0), **subtree**, **degree** (number of children).

| Binary tree type | Meaning |
|---|---|
| **Full** (strict) | every node has 0 or 2 children |
| **Complete** | every level full except possibly the last, which is filled left to right (heaps) |
| **Perfect** | all internal nodes have 2 children and all leaves are at the same level |
| **Balanced** | heights of left and right subtrees differ by a small bound everywhere (AVL: ≤ 1) |
| **Degenerate (skewed)** | every node has one child: a linked list |

## 5.2 Counting facts {#dsa-5-2}

For a binary tree with $n$ nodes:

- $n - 1$ edges, and $n + 1$ null child pointers.
- In any binary tree, **leaves = (nodes with 2 children) + 1**.
- At most $2^d$ nodes at depth $d$; at most $2^{h+1} - 1$ nodes with height $h$.
- Minimum height with $n$ nodes: $\lceil \log_2(n + 1) \rceil - 1$; maximum height: $n - 1$.
- A full binary tree with $I$ internal nodes has $I + 1$ leaves and $2I + 1$ nodes.
- Number of distinct binary tree **shapes** with $n$ nodes = number of BSTs on keys $1..n$ = **Catalan** $C_n$: 1, 1, 2, **5**, 14, 42 for $n = 0..5$. With labelled nodes: $n! \cdot C_n$.

## 5.3 Traversals {#dsa-5-3}

| Traversal | Order | Use |
|---|---|---|
| **Preorder** | root, left, right | copy a tree, prefix expression |
| **Inorder** | left, root, right | **sorted order in a BST** |
| **Postorder** | left, right, root | delete a tree, postfix expression |
| **Level order** | level by level (BFS with a queue) | shortest depth, printing by level |

All are $O(n)$ time; recursive ones use $O(h)$ stack. **Morris traversal** does inorder in $O(1)$ extra space using temporary links.

<div class="nb nb-example">

<strong>Example</strong> (Four traversals)

Tree: root **1**; left child **2** with children **4** and **5**; right child **3** with right child **6**.

- Preorder: **1 2 4 5 3 6**
- Inorder: **4 2 5 1 3 6**
- Postorder: **4 5 2 6 3 1**
- Level order: **1 2 3 4 5 6**

</div>

## 5.4 Which traversals determine the tree? {#dsa-5-4}

**Inorder + preorder** or **inorder + postorder** determine a binary tree uniquely (the pre/postorder gives the root; inorder splits left and right). **Preorder + postorder** do not (unless the tree is full). For a **BST**, preorder alone is enough (inorder is the sorted keys).

<div class="nb nb-example">

<strong>Example</strong> (Rebuild)

Preorder `1 2 4 5 3 6`, inorder `4 2 5 1 3 6`: the root is 1 (first in preorder); in inorder, `4 2 5` is the left subtree and `3 6` the right. Recurse: the left root is 2 (next in preorder), with 4 left and 5 right; the right root is 3, with 6 on its right. That is the tree above.

</div>

## 5.5 Expression trees and other trees {#dsa-5-5}

- **Expression tree:** leaves are operands, internal nodes operators. Inorder (with parentheses) = infix, preorder = prefix, postorder = postfix.
- **N-ary trees, tries** (prefix trees for strings: insert/search $O(\text{word length})$; autocomplete), **segment trees** and **Fenwick trees** (range queries with updates in $O(\log n)$).

<div class="nb nb-moral">

Leaves = degree-2 nodes + 1; n nodes have n − 1 edges. Inorder of a BST is sorted. Inorder plus pre- or postorder rebuilds a tree; pre + post alone does not.

</div>
