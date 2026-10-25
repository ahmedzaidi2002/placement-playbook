---
title: "6 · BSTs and balanced trees"
linkTitle: "6 BSTs and balanced trees"
weight: 6
math: true
---
## 6.1 Binary search trees {#dsa-6-1}

<div class="nb nb-definition">

<strong>Definition</strong> — In a **BST**, every key in a node's left subtree is smaller than the node's key, and every key in its right subtree is larger. So an **inorder traversal gives the keys in sorted order**.

</div>

- **Search / insert:** go left or right by comparison: $O(h)$.
- **Delete:** a leaf → remove it; one child → replace the node by its child; **two children** → replace its key with its **inorder successor** (smallest key in the right subtree) or predecessor, then delete that node.
- $h$ is $O(\log n)$ for a balanced tree but **$O(n)$ in the worst case** (inserting sorted keys gives a linked list).

<div class="nb nb-example">

<strong>Example</strong> (Insert and delete)

Insert 50, 30, 70, 20, 40, 60, 80: root 50; 30 and 70 its children; 20, 40 under 30; 60, 80 under 70 (a perfect tree, height 2). Delete 50 (two children): its inorder successor is **60** (leftmost in the right subtree); 60 replaces 50 and the old 60 node is removed. Inserting 10, 20, 30, 40, 50 in order instead gives a chain of height 4.

</div>

## 6.2 AVL trees {#dsa-6-2}

**Balance factor** = height(left) − height(right). An **AVL tree** keeps it in $\{-1, 0, +1\}$ at every node, so height $\le 1.44 \log_2 n$ and all operations are $O(\log n)$. After an insert, walk up; at the first unbalanced node, **rotate**:

| Case | Inserted into | Fix |
|---|---|---|
| **LL** | left child's left subtree | one **right** rotation |
| **RR** | right child's right subtree | one **left** rotation |
| **LR** | left child's right subtree | left rotation at the child, then right rotation at the node |
| **RL** | right child's left subtree | right rotation at the child, then left rotation at the node |

<div class="nb nb-example">

<strong>Example</strong> (Rotations)

- Insert **10, 20, 30**: node 10 has balance −2 (RR case) → left rotation → **20** becomes the root with children 10 and 30.
- Insert **30, 10, 20**: node 30 has balance +2 and 20 sits in the left child's right subtree (LR) → rotate left at 10, then right at 30 → **20** is the root with children 10 and 30.

</div>

**Minimum nodes in an AVL tree of height $h$:** $N(h) = N(h-1) + N(h-2) + 1$ with $N(0) = 1$, $N(1) = 2$ → 4, 7, 12, 20 for $h = 2..5$. So with 12 nodes the height can be 4, but not 5.

## 6.3 Red–black trees {#dsa-6-3}

Rules: every node is red or black; the **root is black**; a **red node has no red child**; every path from a node down to a null leaf has the **same number of black nodes**. Consequence: height $\le 2\log_2(n + 1)$. Fixes after insert/delete use recolouring and at most 2 (insert) or 3 (delete) rotations.

**AVL vs red–black:** AVL is more strictly balanced (faster lookups); red–black does fewer rotations on updates (faster inserts/deletes). C++ `std::map`/`set` and Java `TreeMap` are red–black trees.

## 6.4 Other balanced search trees {#dsa-6-4}

- **B-tree / B+ tree:** many keys per node and a high fan-out, so the tree is very shallow; designed for disks and database indexes (see the DBMS book).
- **2-3 trees**, **splay trees** (move each accessed node to the root; $O(\log n)$ amortized), **treaps** (BST by key + heap by random priority).

<div class="nb nb-moral">

BST operations cost O(height): O(log n) when balanced, O(n) when skewed. Delete with two children uses the inorder successor. AVL fixes imbalance with LL, RR, LR, RL rotations; red–black trees trade looser balance for fewer rotations.

</div>
