---
title: "Sorting and searching"
weight: 2
---

18 questions asked by Fujitsu, Grey Orange, ION Group, MAQ Software, MathWorks, Qualcomm, Sigmoid, Texas Instruments, Warner Bros. Discovery. Try each one first, then open the toggle: it gives the answer, why it is right, and the idea behind it explained from scratch.

### 1 · DS Q5, simple quadratic sort

*Asked by: Fujitsu (IIT Kharagpur 2023)*

Which sorting algorithm has a worst-case time complexity of $O(n^2)$ but is often used
for its simplicity with small datasets?

- **(a)** Quick Sort
- **(b)** Merge Sort
- **(c)** Bubble Sort
- **(d)** Radix Sort

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) bubble sort**

**Why.** Bubble sort is O(n²) in the worst case and is used mainly because it is simple. Quicksort can also be O(n²) but is chosen for its average speed, not simplicity. (In practice insertion sort is the usual choice for small inputs.)

**Concept: bubble sort.** Repeatedly swap adjacent out-of-order pairs; after pass k, the k largest are in place. With an "any swaps?" flag it stops early on sorted input (O(n) best case).

{{< /details >}}

### 2 · Q4, predict complexity

*Asked by: Grey Orange (OA, Oct 2024)*

Which sorting algorithm does this code implement? What is its time complexity?

```cpp
void sort(int arr[]) {
    int n = arr.length;
    for (int i = 1; i < n; ++i) {
        int key = arr[i];
        int j = i - 1;
        while (j >= 0 && arr[j] > key) {
            arr[j + 1] = arr[j];
            j = j - 1;
        }
        arr[j + 1] = key;
    }
}
```

- **(a)** It is the bubble sorting algorithm. Complexity: $O(n^2)$
- **(b)** It is the insertion sort algorithm. Complexity: $O(n^2)$
- **(c)** It is the insertion sort algorithm. Complexity: $O(n \log n)$
- **(d)** It is the quick sort algorithm. Complexity: $O(n^2)$ (worst case)

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) insertion sort, O(n²)**

**Why.** Each `key` is shifted left past larger elements into the sorted prefix. Worst case (reverse order): 1 + 2 + ... + (n − 1) = n(n − 1)/2 shifts. Best case (already sorted): O(n).

**Concept: insertion sort.** Like sorting playing cards in your hand: take the next card and slide it left into place. It is stable, in-place, fast on nearly-sorted data, and online (can sort data as it arrives).

{{< /details >}}

### 3 · Q21, which sort is this

*Asked by: ION Group (SDE OA, Jul 2025)*

Which sorting algorithm does this code implement, and what is its time complexity?

```cpp
void sort(int arr[]) {
    int n = arr.length;
    for (int i = 1; i < n; ++i) {
        int key = arr[i];
        int j = i - 1;
        while (j >= 0 && arr[j] > key) {
            arr[j + 1] = arr[j];
            j = j - 1;
        }
        arr[j + 1] = key;
    }
}
```

- **(a)** Bubble sort, $O(n^2)$
- **(b)** Insertion sort, $O(n^2)$
- **(c)** Insertion sort, $O(n \log n)$
- **(d)** Quick sort, $O(n^2)$ (worst case)

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) insertion sort, O(n²)**

**Why.** Same code as the previous question: build a sorted prefix by inserting each `key` into place. O(n) on sorted input, O(n²) in the average and worst cases.

**Concept: recognising sorts from code.** Insertion: shifting with `arr[j + 1] = arr[j]` inside a while loop. Bubble: adjacent swaps in nested for loops. Selection: find the min index, then one swap per pass.

{{< /details >}}

### 4 · Q32, statements about BFS and DFS

*Asked by: MAQ Software (TalentDecrypt test, 2025)*

Which statements are correct? (1) BFS and DFS are algorithms for traversing and searching a
node in a graph. (2) BFS explores as far as possible along each branch before backtracking.
(3) DFS uses a strategy opposite to BFS: it explores the deepest node first before being
forced to backtrack and expand other nodes.

- **(a)** 1, 2 and 3 are correct
- **(b)** 1 and 2 correct, 3 incorrect
- **(c)** 1 correct, 2 and 3 incorrect
- **(d)** 2 correct, 1 and 3 incorrect
- **(e)** None

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (e) none** (statements 1 and 3 are correct, 2 is false; no option says "1 and 3")

**Why.** Statement 2 describes DFS ("as far as possible along each branch"), not BFS. BFS explores level by level.

**Concept: BFS vs DFS.** BFS: queue, level by level, shortest paths in unweighted graphs. DFS: stack/recursion, deep first, used for cycle detection, topological sort, connected components.

{{< /details >}}

### 5 · Q26, insertion sort passes

*Asked by: MathWorks (IISc 2024); MathWorks (IIITDM Kancheepuram 2025)*

Which sequence shows the passes of insertion sort on `{5, 4, 3, 2, 1}`?

- **(a)** 45321, 34521, 23451, 12345
- **(b)** (other sequences, not photographed)

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) 45321, 34521, 23451, 12345**

**Why.** Pass i inserts element i + 1 into the sorted prefix: insert 4 → 45321; insert 3 → 34521; insert 2 → 23451; insert 1 → 12345.

**Concept: insertion sort passes.** After pass i, the first i + 1 elements are sorted among themselves (but not yet in their final places).

{{< /details >}}

### 6 · Q10, is it a BST?

*Asked by: MathWorks (NIT Durgapur 2024); MathWorks (NIT Delhi 2024)*

The tree has root 10, with left child 8 (children 6 and 9; 9 has left child 7) and right
child 13 (children 11 and 15; 11 has right child 12). Which statement is true?

- **(a)** The degree of the root is 3
- **(b)** The tree is a binary search tree
- **(c)** Its postorder traversal is 6, 7, 9, 8, 12, 11, 15, 13, 10
- **(d)** The number of binary search trees present in the tree is 8

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) postorder 6, 7, 9, 8, 12, 11, 15, 13, 10**

**Why.** It is not a BST: 7 sits in 9's left subtree, which is in 8's right subtree, but 7 < 8. The root has 2 children, so its degree is 2. BST subtrees: the four leaves (6, 7, 12, 15), plus 9 (7 < 9), 11 and 13: 7 in total, not 8. Postorder (left, right, root): 6, 7, 9, 8, 12, 11, 15, 13, 10.

**Concept: BST property is global.** Every node in the left subtree (not just the left child) must be smaller than the node, and every node in the right subtree larger. Check with min/max bounds as you go down.

{{< /details >}}

### 7 · Q31, binary search third pass

*Asked by: Qualcomm (IISc)*

Which of the options is found by binary search in the 3rd pass in
$12\ 18\ 41\ 47\ 54\ 66\ 74\ 92\ 96$?

- **(a)** 18
- **(b)** 74
- **(c)** 12
- **(d)** 47

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) 12**

**Why.** Indices 0–8. Pass 1: middle index 4, value 54. Pass 2: middle of the left half (0–3) is index 1 (18), or of the right half (5–8) index 6 (74). Pass 3: below 18 only index 0 is left (12), or between 18 and 54 the middle is 41. So 12 is found in pass 3 (18 and 74 in pass 2, 47 needs 4 passes).

**Concept: binary search as a decision tree.** The first probe is the root, the next probes are its children, and so on. A value's depth in that tree is the number of passes needed to find it.

{{< /details >}}

### 8 · Data Structures Basics

*Asked by: Qualcomm (60-question online assessment)*

What will be the number of swaps required to sort the elements given below in descending order using selection sort if last element of the list is sorted first? 43 23 98 61 29 30 17

- **(a)** 7
- **(b)** 8
- **(c)** 5
- **(d)** 3

{{< details title="Answer and explanation" closed="true" >}}

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

{{< /details >}}

### 9 · Data Structures Basics

*Asked by: Qualcomm (60-question online assessment)*

List: 4 17 29 30 48 51 69. If binary search technique is used to search 69 in the above list how many passes are required?

- **(a)** 7
- **(b)** 3
- **(c)** 4
- **(d)** 5

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) 3**

**Why.** Pass 1: middle is 30 (index 3); 69 > 30, go right. Pass 2: [48, 51, 69], middle 51; go right. Pass 3: 69, found.

**Concept: binary search** compares with the middle and discards half each time: at most ⌊log₂ n⌋ + 1 passes (here 3 for n = 7).

{{< /details >}}

### 10 · inserting into a circular linked list

*Asked by: Sigmoid (Campus hiring 2026)*

Insertion of a node in a circular linked list requires modification of at least:

- **(a)** 1 pointer
- **(b)** 2 pointers
- **(c)** 3 pointers
- **(d)** No pointer

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) 2 pointers**

**Why.** Insert X after node P: X.next = P.next, then P.next = X. Two pointer changes. (Inserting before the head may also require moving the head, or fixing the last node's pointer.)

**Concept: link the new node first.** Always set the new node's `next` before changing the old node's `next`, or you lose the rest of the list.

{{< /details >}}

### 11 · partition exchange sort

*Asked by: Sigmoid (Campus hiring 2026)*

Which sorting technique is also known as partition exchange sort?

- **(a)** Quick sort
- **(b)** Merge sort
- **(c)** Bucket sort
- **(d)** Heap sort

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) quick sort**

**Why.** Quicksort partitions the array around a pivot (smaller elements left, larger right) by exchanging elements, then sorts each part. Hence "partition-exchange sort". (The question also calls it stable, which quicksort is not.)

**Concept: quicksort.** Average O(n log n), worst O(n²) (bad pivots, e.g. sorted input with first-element pivot). In-place and fast in practice; randomised or median-of-three pivots avoid the worst case.

{{< /details >}}

### 12 · worst case of selection sort

*Asked by: Sigmoid (Campus hiring 2026)*

Ten people's ages are sorted with selection sort. What is the worst-case complexity?

- **(a)** $O(n^2)$
- **(b)** $O(n \log n)$
- **(c)** $O(n)$

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) O(n²)**

**Why.** Selection sort always scans the whole unsorted part to find the minimum, in every case: (n − 1) + (n − 2) + ... + 1 comparisons.

**Concept: input-independent cost.** Selection sort does the same comparisons on any input, so its best, average and worst cases are all O(n²).

{{< /details >}}

### 13 · binary search

*Asked by: Texas Instruments (IIT ISM 2024)*

In recursive binary search, if `A[mid] > value` the call should be:

{{< details title="Answer and explanation" closed="true" >}}

**Answer: `binarySearch(A, value, low, mid - 1)`**

**Why.** If the middle element is larger than the value, the value (if present) must be to its left, so search low..mid − 1.

**Concept: shrink the range correctly.** Exclude mid itself (`mid − 1` or `mid + 1`), otherwise the range may stop shrinking and the recursion never ends.

{{< /details >}}

### 14 · what does sample() do?

*Asked by: Texas Instruments (BITS Pilani)*

A new node `ptr` is added to a circular list: if empty it points to itself; otherwise the
code walks `temp` to the last node, sets

```cpp
ptr->next = head;
temp->next = ptr;
head = ptr;
```

- **(a)** Insert at the beginning
- **(b)** Insert at the end
- **(c)** Search
- **(d)** None

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) insert at the beginning**

**Why.** The new node links to the old head, the last node links to the new node (keeping the circle), and `head = ptr` makes the new node the head. (Without the `head = ptr` line, the same steps would insert at the end; the key's "end" is wrong.)

**Concept: in a circular list, beginning and end are the same position.** The only difference is which node the `head` pointer marks.

{{< /details >}}

### 15 · merge sort variant

*Asked by: Texas Instruments (BITS Pilani)*

Merge sort with base cases for $n = 1$ and $n = 2$ and a linear merge. Complexity?

- **(a)** $O(n^2)$
- **(b)** $O(n^3)$
- **(c)** $O(n)$
- **(d)** None

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) none of these** (it is O(n log n))

**Why.** Extra base cases for n = 1 and n = 2 don't change the recurrence T(n) = 2T(n/2) + O(n), which solves to O(n log n).

**Concept: merge sort.** Split in halves, sort each recursively, merge in linear time. Always O(n log n), stable, needs O(n) extra space.

{{< /details >}}

### 16 · sorting while data arrive

*Asked by: Texas Instruments (IISc, second set)*

Elements may be added while the sort is running. Which algorithm fits?

- **(a)** Selection sort
- **(b)** Merge sort
- **(c)** Heap sort
- **(d)** Insertion sort

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) insertion sort**

**Why.** Insertion sort keeps a sorted prefix and inserts each new element into it, so it can take elements as they arrive (it is an "online" algorithm). The others need the whole input up front.

**Concept: online algorithms.** They process input piece by piece without knowing the future. Insertion sort is online; heap-based structures also suit streams.

{{< /details >}}

### 17 · Q11, merge sort on sorted input

*Asked by: Warner Bros. Discovery (HireVue, Nov 2024)*

What is the time complexity of running merge sort on an array that is already sorted?

- **(a)** $O(n \lg n)$
- **(b)** $O(\lg n)$
- **(c)** $O(n^2)$
- **(d)** $O(n)$

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) O(n log n)**

**Why.** Standard merge sort always splits down to single elements and merges every level, regardless of input order. (Natural merge sort or Timsort detect the single sorted run and take O(n), but that is not plain merge sort.)

**Concept: adaptive vs non-adaptive sorts.** Adaptive sorts (insertion, Timsort) run faster on nearly sorted input; merge sort and heap sort do not.

{{< /details >}}

### 18 · Q12, searching a sorted list

*Asked by: Warner Bros. Discovery (HireVue, Nov 2024)*

Given a sorted list of items, which search algorithm would you choose to search for an item
most efficiently?

- **(a)** Linear Search
- **(b)** Depth-first search
- **(c)** Breadth-first search
- **(d)** Binary Search

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) binary search**

**Why.** On a sorted array, binary search takes O(log n) comparisons. Linear search is O(n); DFS and BFS are graph traversals.

**Concept: sortedness enables halving.** Binary search needs both sorted order and O(1) random access (an array, not a linked list).

{{< /details >}}
