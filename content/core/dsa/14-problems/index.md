---
title: "14 · Practice problems"
linkTitle: "14 Practice"
weight: 14
math: true
---
Fifteen OA-style questions on new examples. Try, then open the solution.

<div class="nb nb-problem nb-block" id="problem-dsa-1">

<strong>Problem 1</strong> (Loop complexity)

`for (i = n; i > 0; i /= 2) for (j = 0; j < i; j++) work();` — complexity?

<details class="nb-sol">
<summary>Solution</summary>

Inner runs $n + n/2 + n/4 + \dots < 2n$ → **$O(n)$**, not $O(n \log n)$.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-dsa-2">

<strong>Problem 2</strong> (Master theorem)

Solve (a) $T(n) = 4T(n/2) + n$, (b) $T(n) = 3T(n/3) + n$, (c) $T(n) = T(n/2) + n$.

<details class="nb-sol">
<summary>Solution</summary>

(a) $n^{\log_2 4} = n^2$ dominates → **$\Theta(n^2)$**. (b) $n^{\log_3 3} = n$ equals $f$ → **$\Theta(n \log n)$**. (c) $n^0 = 1$, $f = n$ dominates → **$\Theta(n)$**.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-dsa-3">

<strong>Problem 3</strong> (Array address)

`char A[5][8]`, base 200, row-major. Address of `A[2][3]`?

<details class="nb-sol">
<summary>Solution</summary>

$200 + (2 \times 8 + 3) \times 1 = $ **219**.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-dsa-4">

<strong>Problem 4</strong> (Postfix)

Evaluate `6 2 / 3 - 4 2 * +`.

<details class="nb-sol">
<summary>Solution</summary>

$6/2 = 3$; $3 - 3 = 0$; $4 \times 2 = 8$; $0 + 8 = $ **8**.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-dsa-5">

<strong>Problem 5</strong> (Tree counting)

(a) A binary tree has 20 leaves: how many nodes have two children? (b) Maximum nodes in a binary tree of height 4? (c) Number of BSTs on 4 distinct keys?

<details class="nb-sol">
<summary>Solution</summary>

(a) **19**. (b) $2^5 - 1 = $ **31**. (c) $C_4 = $ **14**.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-dsa-6">

<strong>Problem 6</strong> (Rebuild from traversals)

Preorder `A B D E C F`, inorder `D B E A F C`. Postorder?

<details class="nb-sol">
<summary>Solution</summary>

Root A; left subtree {D, B, E} with root B (D left, E right); right subtree {F, C} with root C and F as its left child. Postorder: **D E B F C A**.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-dsa-7">

<strong>Problem 7</strong> (BST)

Insert 40, 20, 60, 10, 30, 50, 70, 25 into an empty BST. Height? Inorder successor of 20?

<details class="nb-sol">
<summary>Solution</summary>

25 goes left of 30, at depth 3 → height **3**. Successor of 20 = smallest in its right subtree {30, 25} = **25**.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-dsa-8">

<strong>Problem 8</strong> (AVL)

Insert 50, 40, 30 into an AVL tree. Which rotation, and the result?

<details class="nb-sol">
<summary>Solution</summary>

50 gets balance +2 with 30 in the left child's left subtree: **LL** case → one **right rotation** → **40** is the root with children 30 and 50.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-dsa-9">

<strong>Problem 9</strong> (Heap insert)

Insert 15 into the max-heap `[20, 10, 12, 5, 8]`.

<details class="nb-sol">
<summary>Solution</summary>

Append at index 5; parent index 2 holds 12 < 15 → swap; parent index 0 holds 20 > 15 → stop. **`[20, 10, 15, 5, 8, 12]`**.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-dsa-10">

<strong>Problem 10</strong> (Linear probing)

Table size 10, $h(k) = k \bmod 10$, linear probing. Insert 12, 22, 32, 15, 25. Where does 25 go, and after how many probes?

<details class="nb-sol">
<summary>Solution</summary>

12 → 2, 22 → 3, 32 → 4, 15 → 5; 25 hashes to 5 (taken) → slot **6** on the **2nd** probe. Notice the cluster 2–6 forming: primary clustering.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-dsa-11">

<strong>Problem 11</strong> (Dijkstra)

Undirected edges S–A 2, S–B 5, A–B 1, A–C 7, B–C 3. Shortest distances from S?

<details class="nb-sol">
<summary>Solution</summary>

S 0 → A 2 → B $\min(5, 2 + 1) = 3$ → C $\min(2 + 7, 3 + 3) = $ **6**. Distances: S 0, A 2, B 3, C 6.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-dsa-12">

<strong>Problem 12</strong> (MST)

Same graph. Kruskal's MST weight?

<details class="nb-sol">
<summary>Solution</summary>

Sorted: A–B 1, S–A 2, B–C 3, S–B 5, A–C 7. Take A–B, S–A, B–C (3 edges for 4 vertices) → **6**.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-dsa-13">

<strong>Problem 13</strong> (Sorting counts)

(a) Comparisons made by selection sort on 6 elements? (b) Inversions in `[3, 1, 2, 5, 4]`, and so the swaps bubble sort makes?

<details class="nb-sol">
<summary>Solution</summary>

(a) $5 + 4 + 3 + 2 + 1 = $ **15** (always). (b) (3,1), (3,2), (5,4) → **3** inversions = 3 swaps.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-dsa-14">

<strong>Problem 14</strong> (Greedy coins)

Coins {1, 5, 10, 25}, amount 63. Greedy result? Is it optimal here?

<details class="nb-sol">
<summary>Solution</summary>

25 + 25 + 10 + 1 + 1 + 1 = **6 coins**; optimal for this (canonical) coin system. Greedy fails for systems like {1, 3, 4}.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-dsa-15">

<strong>Problem 15</strong> (Matrix chain)

$A$ is $5 \times 10$, $B$ is $10 \times 3$, $C$ is $3 \times 12$. Cheapest order and its cost?

<details class="nb-sol">
<summary>Solution</summary>

$(AB)C$: $5 \cdot 10 \cdot 3 + 5 \cdot 3 \cdot 12 = 150 + 180 = $ **330**. $A(BC)$: $10 \cdot 3 \cdot 12 + 5 \cdot 10 \cdot 12 = 360 + 600 = 960$. So **$(AB)C$**.

</details>

</div>
