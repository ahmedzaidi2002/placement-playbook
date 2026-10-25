---
title: "7 · Heaps and priority queues"
linkTitle: "7 Heaps"
weight: 7
math: true
---
## 7.1 The binary heap {#dsa-7-1}

<div class="nb nb-definition">

<strong>Definition</strong> — A **binary heap** is a **complete** binary tree with the **heap property**: in a **max-heap** every parent ≥ its children (the maximum is at the root); in a **min-heap** every parent ≤ its children.

</div>

Stored in an array with no pointers (0-based): children of $i$ at $2i + 1$ and $2i + 2$, parent at $\lfloor (i - 1)/2 \rfloor$. Leaves are the last $\lceil n/2 \rceil$ elements.

## 7.2 Operations {#dsa-7-2}

| Operation | How | Time |
|---|---|---|
| Peek max/min | read the root | $O(1)$ |
| **Insert** | add at the end, **sift up** (swap with parent while bigger) | $O(\log n)$ |
| **Extract max/min** | move the last element to the root, **sift down** (swap with the larger child) | $O(\log n)$ |
| **Build heap** from $n$ items | sift down every internal node, from the last one back to the root | **$O(n)$** |
| Search an arbitrary key | no order to use | $O(n)$ |

<div class="nb nb-example">

<strong>Example</strong> (Build a max-heap)

Array `[3, 9, 2, 1, 4, 5]`. Internal nodes are indices 2, 1, 0.

- Index 2 (value 2): child 5 is bigger → swap → `[3, 9, 5, 1, 4, 2]`.
- Index 1 (value 9): children 1 and 4 are smaller → no change.
- Index 0 (value 3): larger child is 9 → swap → `[9, 3, 5, 1, 4, 2]`; continue at index 1: larger child is 4 → swap → **`[9, 4, 5, 1, 3, 2]`**.

Then extract-max: remove 9, move the last element 2 to the root → `[2, 4, 5, 1, 3]` → sift down: swap with 5 → **`[5, 4, 2, 1, 3]`**.

</div>

**Why build-heap is $O(n)$, not $O(n \log n)$:** most nodes are near the bottom and sift down only a little: $\sum_h \frac{n}{2^{h+1}} \cdot h = O(n)$.

## 7.3 Applications {#dsa-7-3}

- **Heap sort:** build a max-heap, then repeatedly swap the root with the last element and sift down: $O(n \log n)$, in place, **not stable**.
- **Priority queues** (C++ `priority_queue` is a max-heap; Java `PriorityQueue` and Python `heapq` are min-heaps).
- **$k$ largest elements:** keep a **min-heap of size $k$**; for each new element, if it beats the root, replace the root: $O(n \log k)$.
- **Merge $k$ sorted lists:** a min-heap of the current heads: $O(N \log k)$.
- **Median of a stream:** a max-heap for the lower half and a min-heap for the upper half.
- **Dijkstra and Prim** (chapter 9), Huffman coding (chapter 11), scheduling.

## 7.4 Other heaps {#dsa-7-4}

**$d$-ary heap** (shallower, cheaper decrease-key), **binomial heap** (merge in $O(\log n)$), **Fibonacci heap** (decrease-key $O(1)$ amortized, makes Dijkstra $O(E + V\log V)$ in theory).

<div class="nb nb-moral">

Heap = complete tree + parent ≥ children, stored in an array (children 2i+1, 2i+2). Insert and extract are O(log n); build-heap is O(n). Top-k uses a min-heap of size k.

</div>
