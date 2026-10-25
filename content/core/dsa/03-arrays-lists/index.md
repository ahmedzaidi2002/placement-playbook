---
title: "3 · Arrays, strings and linked lists"
linkTitle: "3 Arrays and lists"
weight: 3
math: true
---
## 3.1 Arrays {#dsa-3-1}

Elements stored **contiguously**, so element $i$ is at $\text{base} + i \times \text{size}$: **$O(1)$ random access**, cache-friendly. Inserting or deleting in the middle shifts elements: $O(n)$.

**2-D address calculation** for an $m \times n$ array, element size $w$:

- **Row-major** (C, C++, Java): $\text{addr}(A[i][j]) = \text{base} + (i \cdot n + j)\,w$.
- **Column-major** (Fortran, MATLAB): $\text{addr}(A[i][j]) = \text{base} + (j \cdot m + i)\,w$.

<div class="nb nb-example">

<strong>Example</strong> (Address)

`int A[10][20]` (4 bytes each), base 1000. Row-major: $A[3][5]$ at $1000 + (3 \times 20 + 5) \times 4 = $ **1260**. Column-major: $1000 + (5 \times 10 + 3) \times 4 = $ **1212**.

</div>

**Dynamic arrays** (`vector`, `ArrayList`, Python `list`): grow by doubling when full, so append is **$O(1)$ amortized** (chapter 1). Insert/delete at the front is $O(n)$.

## 3.2 Strings {#dsa-3-2}

An array of characters. Common techniques: **two pointers** (palindromes, reversing), **sliding window** (longest substring without repeats), **frequency counting** with a 26-length array or hash map (anagrams), **prefix sums**. Pattern matching: naive $O(nm)$; **KMP** $O(n + m)$ (prefix function avoids re-checking); **Rabin–Karp** (rolling hash, expected $O(n + m)$); **Z-algorithm**.

In C++ and Java, building a string by repeated `+` in a loop can be $O(n^2)$ (Java strings are immutable): use `StringBuilder` / `+=` on `std::string`.

## 3.3 Linked lists {#dsa-3-3}

Nodes connected by pointers; no contiguous memory.

| Type | Each node has | Notes |
|---|---|---|
| Singly linked | data, next | one direction |
| Doubly linked | data, prev, next | delete a given node in $O(1)$; more memory |
| Circular | last node points to the first | round-robin structures |

| Operation | Array | Linked list |
|---|---|---|
| Access $i$-th element | **$O(1)$** | $O(n)$ |
| Insert/delete at front | $O(n)$ | **$O(1)$** |
| Insert/delete after a known node | $O(n)$ | **$O(1)$** |
| Search | $O(n)$ ($O(\log n)$ if sorted) | $O(n)$ (no binary search) |
| Memory | compact, cache-friendly | extra pointers, scattered |

## 3.4 Classic list techniques {#dsa-3-4}

- **Reverse a list:** walk with three pointers (prev, current, next), flipping each link. $O(n)$ time, $O(1)$ space.
- **Middle node:** slow pointer moves 1 step, fast moves 2; when fast reaches the end, slow is in the middle.
- **Floyd's cycle detection:** slow (1 step) and fast (2 steps); they meet inside the cycle iff there is one. To find the cycle start, move one pointer back to the head and advance both 1 step at a time; they meet at the start.
- **Merge two sorted lists:** compare heads, attach the smaller, advance.
- **$k$-th node from the end:** move one pointer $k$ steps ahead, then move both until the first reaches the end.
- A **dummy (sentinel) head node** removes special cases at the front.

**Skip list:** a sorted linked list with extra "express" levels chosen randomly, giving $O(\log n)$ expected search/insert/delete (a simpler alternative to balanced trees; used in Redis sorted sets).

<div class="nb nb-moral">

Arrays: O(1) access, O(n) middle insert, contiguous and cache-friendly. Linked lists: O(1) insert/delete at a known node, O(n) access. Slow/fast pointers find middles and cycles.

</div>
