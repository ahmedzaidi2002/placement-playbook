---
title: "Complexity and recurrences"
weight: 6
---

7 questions asked by ION Group, MathWorks, Qualcomm, Texas Instruments, Warner Bros. Discovery. Try each one first, then open the toggle: it gives the answer, why it is right, and the idea behind it explained from scratch.

### 1 · Q22, triple loop complexity

*Asked by: ION Group (SDE OA, Jul 2025)*

What is the time complexity of this code?

```cpp
int temp = 0;
for (int i = 1; i <= n; i++)
    for (int j = 1; j <= n; j += i)
        for (int k = 1; k <= n; k += 2)
            temp++;
```

- **(a)** $O(n \log n)$
- **(b)** $O(n \log^2 n)$
- **(c)** $O(n^2 \log n)$
- **(d)** $O(n^2 \log^2 n)$

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) O(n² log n)**

**Why.** For each i, the middle loop steps by i, so it runs about n/i times; the inner loop runs n/2 times regardless. Total = Σᵢ (n/i)(n/2) = (n²/2)(1 + 1/2 + ... + 1/n) = (n²/2) Hₙ = Θ(n² log n).

**Concept: harmonic series.** 1 + 1/2 + 1/3 + ... + 1/n ≈ ln n. Loops whose step grows with the outer index (j += i) often produce this sum.

{{< /details >}}

### 2 · Q4, a recursive algorithm

*Asked by: MathWorks (IIIT Delhi 2024)*

Suppose that I have a recursive algorithm that breaks a pro[blem ...] (Assume that it
takes linear time to process/re-assemble th[e ...]) [cut off in the source] What is its asymptotic
running time?

- **(a)** $O(n \log n)$
- **(b)** $O(n^2 \log n)$
- **(c)** $O(n)$
- **(d)** $O(n^2)$

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) O(n log n)** (assuming the usual split into two halves; the split is cut off in the photo)

**Why.** Two halves plus linear work to split and merge: T(n) = 2T(n/2) + O(n). The recursion has log n levels, each doing O(n) work in total: O(n log n).

**Concept: the master theorem.** For T(n) = aT(n/b) + O(nᵈ): if a = bᵈ the answer is O(nᵈ log n) (merge sort: a = 2, b = 2, d = 1); if a < bᵈ it is O(nᵈ); if a > bᵈ it is O(n^(log_b a)).

{{< /details >}}

### 3 · Q1, which is not $O(n^2)$

*Asked by: MathWorks (IIITDM Kancheepuram 2025)*

Which of the following is not $O(n^2)$? (The fourth option is cut off.)

- **(a)** $(15^{10}) \cdot n + 12099$
- **(b)** $n^{1.98}$
- **(c)** $n^3 / \sqrt{n}$
- **(d)** (not visible)

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) n³/√n**

**Why.** n³/√n = n^2.5, which grows faster than n², so it is not O(n²). A huge constant (a) still gives a linear function, and n^1.98 (b) grows slower than n².

**Concept: Big-O ignores constants, not exponents.** f(n) = O(g(n)) if f eventually stays below c · g(n) for some constant c. Constants and lower-order terms never matter; a larger exponent always does.

{{< /details >}}

### 4 · Data Structures

*Asked by: Qualcomm (60-question online assessment)*

The time taken by binary search algorithm to search a key in a sorted array of n elements is:

- **(a)** O(n)
- **(b)** O(log n)
- **(c)** O(n log n)
- **(d)** O(n^2)

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) O(log n)**

**Why.** Each comparison with the middle element throws away half of the remaining range, so after k steps n/2ᵏ elements remain; it ends when that reaches 1, k = log₂ n.

**Concept: halving gives logarithms.** Any process that cuts the problem in half each step takes about log₂ n steps (binary search, balanced-tree height).

{{< /details >}}

### 5 · printing a circular list

*Asked by: Texas Instruments (IIT BHU 2023)*

What is the auxiliary space of this circular-list traversal?

```cpp
do {
    print;
    temp = temp->next;
} while (temp != first);
```

- **(a)** $O(1)$
- **(b)** $O(n)$
- **(c)** $O(2n)$
- **(d)** None

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) O(1)**

**Why.** The traversal uses one extra pointer, `temp`, regardless of the list's length.

**Concept: auxiliary space.** Extra memory used besides the input itself. Iterative traversals need O(1); recursive ones need O(depth) for the call stack.

{{< /details >}}

### 6 · counting print calls

*Asked by: Texas Instruments (IIT BHU 2023)*

```cpp
for (i = 1; i <= n - 1; i++)
    for (j = i + 1; j <= n; j++)
        print(i, j);
```

How many calls?

- **(a)** $n^2$
- **(b)** $n^2 - n$
- **(c)** $(n^2 - n)/2$
- **(d)** $n^2/2$

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) (n² − n)/2**

**Why.** One call for every pair i < j from {1..n}: C(n, 2) = n(n − 1)/2 = (n² − n)/2.

**Concept: counting nested loops.** For i from 1 to n − 1, the inner loop runs n − i times; adding (n − 1) + (n − 2) + ... + 1 gives n(n − 1)/2.

{{< /details >}}

### 7 · Q18, triple loop complexity

*Asked by: Warner Bros. Discovery (HireVue, Nov 2024)*

What is the time complexity of the following code?

```cpp
for (int i = 0; i < 10; i++) {
    for (int j = 1; j <= n; j++) {
        for (int k = n - 3; k < n + 3; k++) {
            print k
        }
    }
}
```

- **(a)** $O(1)$
- **(b)** $O(n)$
- **(c)** $O(n^2)$
- **(d)** $O(n^3)$

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) O(n)**

**Why.** The outer loop runs 10 times and the innermost 6 times (n − 3 to n + 2): both constants. Only the middle loop depends on n: 10 × n × 6 = 60n = O(n).

**Concept: a loop's bounds decide its cost, not its nesting depth.** Three nested loops are not automatically O(n³); count how many times each actually runs.

{{< /details >}}
