---
title: "10 · Searching and sorting"
linkTitle: "10 Searching and sorting"
weight: 10
math: true
---
## 10.1 Searching {#dsa-10-1}

- **Linear search:** $O(n)$, works on anything.
- **Binary search** (sorted array): compare with the middle, discard half: $O(\log n)$. Compute the middle as `lo + (hi - lo) / 2` to avoid integer overflow.
- **Lower bound** = first index with value ≥ x; **upper bound** = first index with value > x. Count of x = upper − lower.
- **Binary search on the answer:** if "can we do it with value $k$?" is monotone in $k$ (minimum capacity to ship in D days, Koko eating bananas), binary-search $k$.
- Others: **ternary search** (unimodal functions), **exponential search** (unbounded arrays), **interpolation search** ($O(\log \log n)$ on uniform data).

Searching 1,000,000 sorted items takes at most $\lceil \log_2 10^6 \rceil = 20$ comparisons.

## 10.2 Properties of a sort {#dsa-10-2}

- **Stable:** equal keys keep their original order (needed when sorting by several keys in turn).
- **In-place:** $O(1)$ (or $O(\log n)$) extra memory.
- **Adaptive:** faster on nearly sorted input.
- **Comparison-based** sorts need $\Omega(n \log n)$ comparisons in the worst case.

## 10.3 One array, every sort {#dsa-10-3}

Every example sorts **`[5, 2, 4, 6, 1, 3]`** into ascending order. (This array has **9 inversions**, pairs out of order, which is exactly the number of swaps bubble sort and shifts insertion sort make.)

<div class="nb nb-example">

<strong>Example</strong> (Bubble sort: swap adjacent pairs; the largest bubbles to the end each pass)

- Pass 1: `[2, 4, 5, 1, 3, 6]`
- Pass 2: `[2, 4, 1, 3, 5, 6]`
- Pass 3: `[2, 1, 3, 4, 5, 6]`
- Pass 4: `[1, 2, 3, 4, 5, 6]`
- Pass 5: no swaps → stop early (that is why bubble sort with a flag is $O(n)$ on sorted input).

</div>

<div class="nb nb-example">

<strong>Example</strong> (Selection sort: find the minimum of the rest, swap it into place)

- $i = 0$: min is 1 → swap with 5 → `[1, 2, 4, 6, 5, 3]`
- $i = 1$: min is 2 → stays → `[1, 2, 4, 6, 5, 3]`
- $i = 2$: min is 3 → swap with 4 → `[1, 2, 3, 6, 5, 4]`
- $i = 3$: min is 4 → swap with 6 → `[1, 2, 3, 4, 5, 6]`

At most $n - 1$ swaps (good when writes are expensive); always $n(n-1)/2$ comparisons; **not stable**.

</div>

<div class="nb nb-example">

<strong>Example</strong> (Insertion sort: insert each element into the sorted prefix)

- insert 2 → `[2, 5, 4, 6, 1, 3]`
- insert 4 → `[2, 4, 5, 6, 1, 3]`
- insert 6 → `[2, 4, 5, 6, 1, 3]` (already in place)
- insert 1 → `[1, 2, 4, 5, 6, 3]`
- insert 3 → `[1, 2, 3, 4, 5, 6]`

Best for small or nearly sorted arrays ($O(n)$ when sorted); stable.

</div>

<div class="nb nb-example">

<strong>Example</strong> (Merge sort: split, sort halves, merge)

`[5, 2, 4]` and `[6, 1, 3]` → sorted halves `[2, 4, 5]` and `[1, 3, 6]` → merge by repeatedly taking the smaller front: 1, 2, 3, 4, 5, 6. Always $O(n \log n)$, stable, $O(n)$ extra space; ideal for linked lists and external sorting.

</div>

<div class="nb nb-example">

<strong>Example</strong> (Quicksort: partition around a pivot, recurse on both sides)

Lomuto partition with the last element **3** as pivot: elements ≤ 3 (2 and 1) move to the front → **`[2, 1, 3, 6, 5, 4]`**; 3 is now in its final place. Recurse on `[2, 1]` and `[6, 5, 4]`.

Average $O(n \log n)$, in place, fastest in practice; **worst case $O(n^2)$** when the pivot is always the smallest or largest (e.g. a sorted array with a first/last pivot). Fix: random or median-of-three pivot.

</div>

<div class="nb nb-example">

<strong>Example</strong> (Heap sort: build a max-heap, repeatedly move the max to the end)

Build-heap gives `[6, 5, 4, 2, 1, 3]`. Swap 6 to the end and sift down → `[5, 3, 4, 2, 1 | 6]` → swap 5 → `[4, 3, 1, 2 | 5, 6]` → … → sorted. Always $O(n \log n)$, in place, not stable.

</div>

**Non-comparison sorts** (beat $n \log n$ by not comparing):

- **Counting sort:** count occurrences of each value in a range $0..k$, then place: $O(n + k)$, stable. Good when $k$ is small.
- **Radix sort:** sort by each digit from least significant, using a stable counting sort: $O(d(n + b))$ for $d$ digits in base $b$.
- **Bucket sort:** spread uniformly distributed values into buckets, sort each: $O(n)$ expected.

## 10.4 The master table {#dsa-10-4}

| Sort | Best | Average | Worst | Space | Stable | In-place |
|---|---|---|---|---|---|---|
| Bubble | $n$ | $n^2$ | $n^2$ | 1 | yes | yes |
| Selection | $n^2$ | $n^2$ | $n^2$ | 1 | **no** | yes |
| Insertion | $n$ | $n^2$ | $n^2$ | 1 | yes | yes |
| Merge | $n\log n$ | $n\log n$ | $n\log n$ | $n$ | yes | no |
| Quick | $n\log n$ | $n\log n$ | $n^2$ | $\log n$ | **no** | yes |
| Heap | $n\log n$ | $n\log n$ | $n\log n$ | 1 | **no** | yes |
| Counting | $n + k$ | $n + k$ | $n + k$ | $n + k$ | yes | no |
| Radix | $d(n + b)$ | $d(n + b)$ | $d(n + b)$ | $n + b$ | yes | no |

**Real libraries:** C++ `std::sort` = **introsort** (quicksort that switches to heapsort if recursion gets too deep, insertion sort for small parts); `std::stable_sort` = merge sort; Python and Java (objects) = **Timsort** (merge sort + insertion sort on natural runs; stable, $O(n)$ on sorted data).

## 10.5 Which sort when {#dsa-10-5}

| Situation | Choose |
|---|---|
| General purpose, in memory | quicksort / introsort |
| Need stability or guaranteed $n \log n$ | merge sort |
| Small or nearly sorted array | insertion sort |
| Tight memory, guaranteed $n \log n$ | heap sort |
| Integers in a small range | counting / radix sort |
| Linked list | merge sort |
| Data larger than memory | external merge sort |
| Few writes allowed | selection sort |

## 10.6 Selection: k-th smallest without sorting {#dsa-10-6}

**Quickselect:** partition like quicksort but recurse into only the side that contains $k$: $O(n)$ average, $O(n^2)$ worst. **Median of medians** guarantees $O(n)$. With a heap of size $k$: $O(n \log k)$.

<div class="nb nb-moral">

Bubble, selection, insertion are O(n²); merge, heap, quick are O(n log n) (quick's worst case is n²). Stable: bubble, insertion, merge, counting, radix. Unstable: selection, quick, heap. Binary search is O(log n) on sorted data, and also on monotone answers.

</div>
