---
title: "19 · Mixed practice in OA style"
linkTitle: "19 Mixed practice in OA style"
weight: 19
math: true
---
These problems mix the whole book in the formats that online assessments use: a trace, a count, a “which of these is true” with possibly several correct options, or a complexity. Every numeric answer was computed by `mixcheck.cpp` or by the checking programs of the earlier chapters. Time yourself: about two minutes each.

## 19.1 A few harder problems to think about {#s19-1}

<div class="nb nb-problem nb-block" id="problem-19a">

<strong>Problem 19A</strong> (Recurrence)

Solve $T(n) = 4T(n/2) + n^2\log n$.

<details class="nb-hint">
<summary>Hint</summary>

$\log_2 4 = 2$.

</details>

<details class="nb-sol">
<summary>Solution</summary>

$f(n) = n^2 \log n = \Theta(n^{\log_2 4}\log^1 n)$: Master theorem case 2 with $k = 1$, so $T(n) = \Theta(n^2\log^2 n)$.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-19b">

<strong>Problem 19B</strong> (Loop count)

What is `c` after `for (i = 1; i <= 16; i *= 2) for (j = 1; j <= i; j++) c++;` starting from $0$? What is the complexity for general $n$?

<details class="nb-hint">
<summary>Hint</summary>

$i$ takes the values $1, 2, 4, 8, 16$.

</details>

<details class="nb-sol">
<summary>Solution</summary>

$1 + 2 + 4 + 8 + 16 = 31$; in general about $2n$, so $\Theta(n)$.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-19c">

<strong>Problem 19C</strong> (Build-heap)

Apply bottom-up build-max-heap to `[5 3 17 10 84 19 6 22 9]`. Give the array.

<details class="nb-hint">
<summary>Hint</summary>

Start sifting down at index $3$ (value $10$), then $2$, $1$, $0$.

</details>

<details class="nb-sol">
<summary>Solution</summary>

`[84 22 19 10 3 17 6 5 9]`.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-19d">

<strong>Problem 19D</strong> (Hash table)

Keys `43 135 72 23 99 19 82` are inserted into a table of size $10$ with $h(k) = k \bmod 10$ and linear probing. Which slots stay empty, and where does $82$ go?

<details class="nb-hint">
<summary>Hint</summary>

$23$ collides with $43$; $19$ wraps around past slot $9$.

</details>

<details class="nb-sol">
<summary>Solution</summary>

Table `[19 - 72 43 23 135 82 - - 99]`: slots $1$, $7$ and $8$ are empty; $82$ probes $2, 3, 4, 5$ and lands in $6$.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-19e">

<strong>Problem 19E</strong> (BST from preorder)

A BST has preorder `30 20 10 15 25 40 50 45`. Give its postorder.

<details class="nb-hint">
<summary>Hint</summary>

A preorder alone determines a BST; insert the keys in that order.

</details>

<details class="nb-sol">
<summary>Solution</summary>

`15 10 25 20 45 50 40 30`.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-19f">

<strong>Problem 19F</strong> 🌶🌶 (AVL tree)

Insert `21 26 30 9 4 14 28 18 15` into an empty AVL tree. Give the final preorder and height.

<details class="nb-hint">
<summary>Hint</summary>

Five of the nine insertions cause a rotation. After each insertion find the lowest unbalanced node and classify the case (LL, RR, LR, RL) by the path to the new key.

</details>

<details class="nb-sol">
<summary>Solution</summary>

The trace (`avltrace.cpp`): $30$: RR at $21$, root $26$. $4$: LL at $21$, giving `26 9 4 21 30`. $14$: LR at $26$ (left rotation at $9$, right rotation at $26$), root $21$: `21 9 4 14 26 30`. $28$: RL at $26$, giving `21 9 4 14 28 26 30`. $18$: no rotation. $15$: RL at $14$ (right rotation at $18$, left rotation at $14$). Final preorder `21 9 4 15 14 18 28 26 30`, height $3$.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-19g">

<strong>Problem 19G</strong> (Quicksort comparisons)

How many comparisons does quicksort with the first element as pivot make on the sorted array $1, 2, \ldots, 10$?

<details class="nb-hint">
<summary>Hint</summary>

Each partition compares the pivot with every other element of its range, and one side is empty.

</details>

<details class="nb-sol">
<summary>Solution</summary>

$9 + 8 + \cdots + 1 = 45 = n(n-1)/2$.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-19h">

<strong>Problem 19H</strong> (Optimal merge pattern)

Four sorted files have $20$, $30$, $10$ and $40$ records. Merging two files costs the sum of their sizes. What is the minimum total cost to merge them into one?

<details class="nb-hint">
<summary>Hint</summary>

It is Huffman’s algorithm.

</details>

<details class="nb-sol">
<summary>Solution</summary>

Merge $10 + 20 = 30$, then $30 + 30 = 60$, then $40 + 60 = 100$: total $30 + 60 + 100 = 190$.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-19i">

<strong>Problem 19I</strong> (Counting topological orders)

How many topological orders does the DAG with edges $1 \to 3$, $2 \to 3$, $3 \to 4$, $3 \to 5$, $4 \to 6$, $5 \to 6$ have?

<details class="nb-hint">
<summary>Hint</summary>

$3$ separates the graph into “before” and “after”.

</details>

<details class="nb-sol">
<summary>Solution</summary>

$\{1, 2\}$ in either order, then $3$, then $\{4, 5\}$ in either order, then $6$: $2 \cdot 2 = 4$.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-19j">

<strong>Problem 19J</strong> (Counting BSTs)

How many BSTs store the keys $1..6$? How many of them have $3$ at the root?

<details class="nb-hint">
<summary>Hint</summary>

With root $r$, the left subtree holds $r - 1$ keys and the right $6 - r$.

</details>

<details class="nb-sol">
<summary>Solution</summary>

$C_6 = 132$. With root $3$: $C_2 \cdot C_3 = 2 \cdot 5 = 10$.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-19k">

<strong>Problem 19K</strong> (Inversions)

How many inversions does `[4 3 2 1 5]` have, and how many comparisons does insertion sort make on it?

<details class="nb-hint">
<summary>Hint</summary>

The first four are reversed.

</details>

<details class="nb-sol">
<summary>Solution</summary>

$\binom42 = 6$ inversions. Insertion sort makes one comparison per shift plus one failed comparison for each insertion that stops before the front: inserting $3$, $2$, $1$ shifts $1 + 2 + 3$ times and runs off the front each time ($6$ comparisons), inserting $5$ costs $1$: $7$ comparisons and $6$ shifts.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-19l">

<strong>Problem 19L</strong> (Radix sort)

Give the array after the first two passes of LSD radix sort on `[329 457 657 839 436 720 355]`.

<details class="nb-hint">
<summary>Hint</summary>

Each pass is a stable sort on one digit.

</details>

<details class="nb-sol">
<summary>Solution</summary>

After the units digit: `[720 355 436 457 657 329 839]`. After the tens digit: `[720 329 436 839 355 457 657]`.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-19m">

<strong>Problem 19M</strong> (Tree heights)

A complete binary tree has $100$ nodes. How many leaves, and what is its height? A binary heap with $100$ elements: at which indices (0-based) are the children of index $40$?

<details class="nb-hint">
<summary>Hint</summary>

Leaves are the last $\lceil n/2 \rceil$ positions.

</details>

<details class="nb-sol">
<summary>Solution</summary>

$50$ leaves, height $\lfloor \log_2 100 \rfloor = 6$. The children of $40$ would be $81$ and $82$; both exist (indices $\le 99$).

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-19n">

<strong>Problem 19N</strong> (Which statements are true? (select all))

(a) Every comparison sort needs $\Omega(n\log n)$ comparisons in the worst case. (b) Heap sort is stable. (c) Insertion sort is $O(n)$ on sorted input. (d) Merge sort on a linked list needs $O(n)$ extra memory. (e) Counting sort is stable when the output is filled from right to left.

<details class="nb-hint">
<summary>Hint</summary>

Two of the five are false.

</details>

<details class="nb-sol">
<summary>Solution</summary>

True: (a), (c), (e). False: (b) (heap sort is not stable); (d) (merging lists relinks nodes, $O(1)$ extra apart from the recursion stack).

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-19o">

<strong>Problem 19O</strong> (Which statements are true? (select all))

(a) A hash table with chaining can have a load factor above $1$. (b) Linear probing suffers from secondary clustering but not primary clustering. (c) The worst-case search time in a hash table is $O(n)$. (d) Rehashing makes a single insertion $O(1)$ in the worst case. (e) Double hashing needs $h_2(k) \ne 0$.

<details class="nb-hint">
<summary>Hint</summary>

Primary clustering is linear probing’s problem.

</details>

<details class="nb-sol">
<summary>Solution</summary>

True: (a), (c), (e). (b) is backwards: linear probing has primary clustering. (d) is false: the insertion that triggers a rehash costs $O(n)$; only the amortized cost is $O(1)$.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-19p">

<strong>Problem 19P</strong> (Euler and Hamilton)

A connected graph has vertex degrees $2, 2, 3, 3, 4, 4$. Does it have an Euler circuit? An Euler path?

<details class="nb-hint">
<summary>Hint</summary>

Count odd degrees.

</details>

<details class="nb-sol">
<summary>Solution</summary>

Two odd-degree vertices: no Euler circuit, but an Euler path between the two vertices of degree $3$. Nothing follows about Hamiltonian paths.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-19q">

<strong>Problem 19Q</strong> (Spanning trees)

How many spanning trees does $K_4$ have? How many edges does a spanning tree of a connected graph with $12$ vertices have?

<details class="nb-hint">
<summary>Hint</summary>

Cayley’s formula $n^{n-2}$.

</details>

<details class="nb-sol">
<summary>Solution</summary>

$4^2 = 16$; $11$ edges.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-19r">

<strong>Problem 19R</strong> (Postfix)

Evaluate `5 1 2 + 4 * + 3 -`.

<details class="nb-hint">
<summary>Hint</summary>

$1\,2\,+$ is $3$.

</details>

<details class="nb-sol">
<summary>Solution</summary>

$1 + 2 = 3$, $3 \cdot 4 = 12$, $5 + 12 = 17$, $17 - 3 = 14$.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-19s">

<strong>Problem 19S</strong> (Choose the structure (select all that achieve the bound))

Which structures support “insert” and “find the minimum” both in $O(\log n)$ worst case or better? (a) sorted array; (b) binary min-heap; (c) AVL tree; (d) unsorted linked list; (e) hash table.

<details class="nb-hint">
<summary>Hint</summary>

Check both operations, worst case.

</details>

<details class="nb-sol">
<summary>Solution</summary>

(b) (insert $O(\log n)$, min $O(1)$) and (c) (both $O(\log n)$). A sorted array inserts in $O(n)$, an unsorted list finds the minimum in $O(n)$, a hash table has no order.

</details>

</div>
