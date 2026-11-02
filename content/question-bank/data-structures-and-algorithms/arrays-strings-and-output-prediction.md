---
title: "Arrays, strings and output prediction"
weight: 4
---

13 questions asked by Grey Orange, MathWorks, Oracle, Paytm, Qualcomm, Texas Instruments, Warner Bros. Discovery. Try each one first, then open the toggle: it gives the answer, why it is right, and the idea behind it explained from scratch.

### 1 · Q6, process an array

*Asked by: Grey Orange (OA, Oct 2024)*

Given an array of integers `arr` (1-indexed), create a new array `arr'` with
these rules, choosing the data structure that gives optimal performance for large
`arr`. (Every positive integer is a sum of distinct powers of 2.)

1. For each index $i$ that is a power of 2, `arr'[i]` is the sum of
    `arr[1..i]`. E.g. `arr = [2, 3]` gives `arr' = [2, 5]`.
2. For each index $i$ that is even but not a power of 2,
    `arr'[i] = arr[k1] + arr[k2] + ... + arr[km]`, where $k_1, \dots, k_m$ are the
    powers of 2 that sum to $i$. E.g. for $i = 6$, `arr'[6] = arr[2] + arr[4]`.
3. For each odd index $i$, `arr'[i]` is unchanged.

Examples: `[1,1,1,1,1,1,1,1]<code> &#36;&#92;to&#36; </code>[1,2,1,4,1,2,1,8]`;
`[1,2,3,4,5,6,7,8]<code> &#36;&#92;to&#36; </code>[1,3,3,10,5,6,7,36]`.

- **(a)** Create an array and do a prefix sum of all even index elements per the rules.
- **(b)** Implement a binary index tree and update all the even indexes per the rules.
- **(c)** Design a segment tree. For its even indexes, find the powers of 2 that sum to the index and sum the values at those indexes. Save the value to its node.
- **(d)** Create an array. For each even index, iterate the array to determine final values.

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) an array with prefix sums**

**Why.** The output is built once and never queried or updated afterwards. One O(n) prefix-sum pass gives every power-of-two entry. An even index i only needs the original values at the powers of two in i's binary form (its set bits), O(log n) each, so O(n log n) in total. A Fenwick tree does **not** store these sums (its node 6 holds arr[5] + arr[6], not arr[2] + arr[4]); a segment tree adds overhead with no queries to serve; (d) rescans for every index, O(n²).

**Concept: pick the simplest structure that fits the access pattern.** Trees (Fenwick, segment) pay off when you mix many updates and range queries. For a one-shot transformation, a plain array and a prefix sum (`pre[i] = pre[i−1] + arr[i]`) is fastest. The set bits of i are found with `i & -i` or by scanning bits.

{{< /details >}}

### 2 · Q10, first missing positive

*Asked by: MathWorks (IIT Bombay 2024)*

The least time to find the first missing positive integer with $O(1)$ extra space is:

- **(a)** $O(n \log n)$
- **(b)** $O(n\sqrt n)$
- **(c)** $O(n)$
- **(d)** $O(1)$

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) O(n)**

**Why.** Use the array itself as the hash table: for each value v in 1..n, swap it into index v − 1 (repeat until the slot holds the right value or v is out of range). Then scan: the first index i with a[i] ≠ i + 1 gives the answer i + 1. Each swap places one value for good, so the total is O(n), with O(1) extra space. (The candidate's O(n log n) is the sort-based approach.)

**Concept: cyclic sort / index as hash.** When values are in a known range 1..n, the value itself tells you where it belongs, so you can "sort" in linear time and use positions as presence markers.

{{< /details >}}

### 3 · Q8, string storage

*Asked by: MathWorks (NIT Durgapur 2024)*

In which storage structure for strings can one easily insert, delete, concatenate and
rearrange substrings?

- **(a)** fixed-length storage
- **(b)** variable-length storage with a fixed maximum
- **(c)** linked-list storage
- **(d)** array-type storage

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) linked-list storage**

**Why.** Inserting, deleting or moving a substring in a linked list only changes a few pointers. In arrays (fixed or variable length) you must shift all the characters after the change.

**Concept: arrays vs linked lists.** Arrays: O(1) access by index, O(n) insert/delete in the middle. Linked lists: O(n) access, O(1) insert/delete once you are at the spot. Choose by which operations dominate.

{{< /details >}}

### 4 · symmetric sparse matrix

*Asked by: Oracle (HackerRank MCQ test)*

In what way can a symmetric sparse matrix be stored efficiently?

- **(a)** Heap
- **(b)** Binary tree
- **(c)** Hash table
- **(d)** Adjacency List

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) adjacency list**

**Why.** A symmetric sparse matrix is like the adjacency matrix of a sparse undirected graph. Storing only the non-zero entries per row (and only one triangle, since it is symmetric) uses space proportional to the non-zeros, not n². A hash table keyed by (i, j) also works but is not the classic answer.

**Concept: sparse storage.** A matrix is sparse when most entries are 0. Store only the non-zeros: adjacency lists, coordinate lists (row, col, value), or compressed sparse row (CSR). Symmetry halves it again.

{{< /details >}}

### 5 · Number of Swaps II

*Asked by: Paytm (HackerRank, Sep 2025)*

Find the minimum number of swaps required to convert
`arr1 = [7, 6, 1, 3, 4, 9, 8, 2, 5]` into `arr2 = [3, 1, 8, 5, 4, 9, 2, 6, 7]`.

- **(a)** 9
- **(b)** 5
- **(c)** 7
- **(d)** 4

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) 5**

**Why.** For each position of arr1, find where its value must go in arr2. That gives the permutation 0→8, 1→7, 2→1, 3→0, 4→4, 5→5, 6→2, 7→6, 8→3. Its cycles are (0 8 3), (1 7 6 2), (4) and (5). A cycle of length L needs L − 1 swaps: 2 + 3 + 0 + 0 = 5, i.e. n − (number of cycles) = 9 − 4.

**Concept: minimum swaps = n − cycles.** Each swap can put exactly one element into its final place while splitting a cycle; a cycle of L elements is fixed with L − 1 swaps. Find cycles by following "where does this element need to go" until you return to the start.

{{< /details >}}

### 6 · Data Structures

*Asked by: Qualcomm (60-question online assessment)*

What does this code do?

```c
void Queue(int element) {
    if (!isFull()) {
        if (front == -1) front = 0;
        rear = (rear + 1) % size;
        items[rear] = element;
    }
}
```

- **(a)** `Delete an element from the queue.`
- **(b)** `Run time error`
- **(c)** `Traverse the queue.`
- **(d)** `Insert an element into the queue.`

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) insert an element into the queue**

**Why.** It checks the queue isn't full, sets `front` to 0 on the first insertion, advances `rear` circularly with `% size`, and stores the element: a circular-queue enqueue.

**Concept: circular queue.** A fixed array where `rear = (rear + 1) % size` wraps around, so slots freed at the front are reused. Enqueue moves rear; dequeue moves front.

{{< /details >}}

### 7 · Data Structures

*Asked by: Qualcomm (60-question online assessment)*

What goes in the blank so the function computes the product of two 2D matrices?

```c
int mul() {
    int A[n][p], B[p][m], C[n][m];
    for (int i = 0; i < n; i++)
        for (int k = 0; k < m; k++) {
            Sum = 0;
            ______
        }
    return C;
}
```

- **(a)** `for (int j=0;j<p;j++) Sum += A[i][k]*B[j][i]; C[i][j] = Sum`
- **(b)** `C[i][k] = Sum; Sum += A[i][k]*B[k][i];`
- **(c)** `for (int j=0;j<p;j++) Sum += A[i][j]*B[j][k]; C[i][k] = Sum;`
- **(d)** `Sum += A[i][k]*B[k][i]; C[i][k] = Sum;`

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) `for (int j = 0; j < p; j++) Sum += A[i][j] * B[j][k]; C[i][k] = Sum;`**

**Why.** C[i][k] is the dot product of row i of A with column k of B, summed over the shared dimension p: Σⱼ A[i][j] · B[j][k]. Only (c) has that loop and the right indices.

**Concept: matrix multiplication.** An (n × p) times a (p × m) matrix gives n × m. Three nested loops: rows i, columns k, and the shared index j. Time O(n·p·m).

{{< /details >}}

### 8 · max of row minima

*Asked by: Texas Instruments (IIT BHU 2023)*

For an $n \times n$ matrix, find each row's minimum and then the largest of them. Time?

- **(a)** $O(n)$
- **(b)** $O(n \log n)$
- **(c)** $O(n^2)$
- **(d)** $O(n^3)$

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) O(n²)**

**Why.** Every one of the n² entries must be read once to find each row's minimum; the final maximum over n row-minima adds only O(n).

**Concept: lower bound by reading the input.** If an answer can depend on every input element, the algorithm must look at all of them, so it cannot beat the input size (here n²).

{{< /details >}}

### 9 · reversing an array

*Asked by: Texas Instruments (IIT BHU 2023)*

```cpp
for (i = 0, j = N - 1; i < j; i++, j--) {
    temp = A[i];
    A[i] = A[j];
    A[j] = temp;
}
```

(the loop header is garbled in the screenshot). A: it reverses the array. B: it runs in linear
time.

{{< details title="Answer and explanation" closed="true" >}}

**Answer: both statements are true**

**Why.** The loop swaps A[i] and A[j] from the outside in, so it reverses the array (A). It runs N/2 times, linear time (B).

**Concept: two-pointer swap.** One index from each end, swap, move inward until they meet. O(n) time, O(1) extra space.

{{< /details >}}

### 10 · sliding window

*Asked by: Texas Instruments (IIT ISM 2024)*

Time to find the maximum sum of $k$ consecutive elements with a sliding window?

{{< details title="Answer and explanation" closed="true" >}}

**Answer: O(n)**

**Why.** Compute the first window's sum, then slide: add the element that enters and subtract the one that leaves. Each step is O(1), and there are n − k steps.

**Concept: sliding window.** Reuse the previous window's result instead of recomputing from scratch; this turns O(nk) into O(n).

{{< /details >}}

### 11 · Q17, storing score frequencies

*Asked by: Warner Bros. Discovery (HireVue, Nov 2024)*

A program $P$ reads 500 integers in the range $[0, 100]$, the scores of 500 students, and
then prints the frequency of each score above 50. What would be the best way for $P$ to
store the frequencies?

- **(a)** An array of 50 numbers
- **(b)** An array of 100 numbers
- **(c)** An array of 500 numbers
- **(d)** A dynamically allocated array of 550 numbers

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) an array of 50 numbers**

**Why.** Only scores 51–100 need counting: 50 possible values, one counter each (index = score − 51). Storing all 500 scores is unnecessary.

**Concept: counting array.** When values come from a small known range, an array of counters indexed by value gives O(1) updates and uses space proportional to the range, not the input size.

{{< /details >}}

### 12 · Q19, sorted array operations

*Asked by: Warner Bros. Discovery (HireVue, Nov 2024)*

Given a sorted array of distinct items, which operation would result in a time complexity
of more than $O(1)$?

- **(a)** Finding the ith largest element
- **(b)** Finding the ith smallest element
- **(c)** Deleting an element
- **(d)** All of the above

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) deleting an element**

**Why.** In a sorted array the i-th smallest is a[i − 1] and the i-th largest is a[n − i], both O(1). Deleting requires shifting the later elements left, O(n).

**Concept: sorted arrays.** Great for rank queries and binary search (O(log n)); poor for inserts and deletes (O(n) shifts). Balanced BSTs give O(log n) for all of them.

{{< /details >}}

### 13 · code without its question

*Asked by: Warner Bros. Discovery (HireVue, Nov 2024)*

One photo shows only this code; the question number and options were not captured. The
question on this platform was presumably "What is the time complexity of the following
code?"

```cpp
int k = 0;
for (int i = n / 2; i <= n; i++) {
    for (int j = 2; j <= n; j = j * 2) {
        k = k + n / 2;
    }
}
```

{{< details title="Answer and explanation" closed="true" >}}

**Answer: O(n log n)** (the question is inferred from the code)

**Why.** The outer loop runs from n/2 to n: about n/2 times. The inner loop doubles j from 2 up to n: about log₂ n times. Total ≈ (n/2) · log n = O(n log n).

**Concept: loops that double.** A loop variable multiplied by 2 each time reaches n after log₂ n steps. Multiply the counts of nested independent loops.

{{< /details >}}
