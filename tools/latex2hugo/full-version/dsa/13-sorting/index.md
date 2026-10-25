---
title: "13 · Sorting"
linkTitle: "13 Sorting"
weight: 13
math: true
---
Every algorithm in this chapter is run on the same array, `[29 10 14 37 13 5 41 8]`, so the traces can be compared line by line. OA questions on sorting are almost always one of three kinds: “what does the array look like after $k$ passes”, “how many swaps or comparisons”, and “which of these sorts is stable / in place / adaptive”. The traces answer the first two; the master table ([Section 13.10](#sec-dsa-sorttable)) answers the third.

## 13.1 Properties of a sort {#sec-dsa-sortprops}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> sorting a spreadsheet by city after sorting it by name: a stable sort keeps the names in order within each city.</em>

</div>

<div class="nb nb-definition" id="definition-13-1-1">

<strong>Definition 13.1.1</strong>.

- <strong>Stable</strong>: equal keys keep their relative input order.
- <strong>In place</strong>: $O(1)$ extra memory (often relaxed to $O(\log n)$ for the recursion stack).
- <strong>Adaptive</strong>: faster on inputs that are already partly sorted (few inversions or few runs).
- <strong>Online</strong>: can sort a stream, inserting each element as it arrives.
- <strong>Comparison-based</strong>: only compares pairs of keys, so it obeys the $\Omega(n \log n)$ lower bound ([Theorem 1.6.3](../01-complexity/#theorem-1-6-3)).
- <strong>Internal</strong> sorts work in RAM; <strong>external</strong> sorts handle data larger than memory.

</div>

Stability matters only for records with equal keys and other data attached:

```cpp {filename="stability.cpp, lines 18–28"}
    std::vector<Rec> s = in;                       // selection sort: long-distance swaps
    for (std::size_t i = 0; i + 1 < s.size(); ++i) {
        std::size_t m = i;
        for (std::size_t j = i + 1; j < s.size(); ++j) if (s[j].key < s[m].key) m = j;
        std::swap(s[i], s[m]);
    }
    print("selection sort", s);

    std::vector<Rec> t = in;
    std::stable_sort(t.begin(), t.end(), [](const Rec& x, const Rec& y) { return x.key < y.key; });
    print("stable_sort", t);
```

```text {filename="Output of stability.cpp"}
input           4a 4b 2c 1d
selection sort  1d 2c 4b 4a
stable_sort     1d 2c 4a 4b
```

Selection sort’s long-distance swap moved `4a` behind `4b`. Any sort can be made stable by sorting the pairs (key, original index), at the cost of the extra index.

## 13.2 The quadratic sorts {#s13-2}

### 13.2.i Bubble sort {#sec-dsa-bubble}

<div class="nb nb-remark" id="algorithm-13-2-1">

<strong>Algorithm 13.2.1</strong> (Bubble sort) — Sweep left to right swapping adjacent elements that are out of order. After pass $p$ the $p$ largest elements are in their final places at the end. Stop early if a pass makes no swap.

</div>

```cpp {filename="bubble.cpp, lines 3–12"}
void bubbleSort(std::vector<int>& a) {
    int n = a.size();
    for (int pass = 1; pass < n; ++pass) {
        bool swapped = false;
        for (int j = 0; j + pass < n; ++j)          // the last pass-1 cells are final
            if (a[j] > a[j + 1]) { std::swap(a[j], a[j + 1]); swapped = true; }
        show("pass " + std::to_string(pass), a);
        if (!swapped) break;                         // early exit: already sorted
    }
}
```

```text {filename="Output of bubble.cpp"}
input          [29 10 14 37 13 5 41 8]
pass 1         [10 14 29 13 5 37 8 41]
pass 2         [10 14 13 5 29 8 37 41]
pass 3         [10 13 5 14 8 29 37 41]
pass 4         [10 5 13 8 14 29 37 41]
pass 5         [5 10 8 13 14 29 37 41]
pass 6         [5 8 10 13 14 29 37 41]
pass 7         [5 8 10 13 14 29 37 41]
```

<div class="nb nb-definition" id="fact-13-2-2">

<strong>Fact 13.2.2</strong>. Comparisons: $n(n-1)/2$ worst case, $n - 1$ best case (sorted input, one pass with the flag). Swaps $=$ number of inversions ($16$ here). Stable (only strictly greater neighbours are swapped), in place, adaptive only to “sortedness” in the weak sense: a single small element at the end (a <strong>turtle</strong>) still needs $n - 1$ passes, because it moves only one step left per pass. Pass $7$ above made no swap; that is how the algorithm learns it is done.

</div>

### 13.2.ii Selection sort {#s13-2-ii}

<div class="nb nb-remark" id="algorithm-13-2-3">

<strong>Algorithm 13.2.3</strong> (Selection sort) — For $i = 0, 1, \ldots$: find the minimum of `a[i..n-1]` and swap it into position $i$.

</div>

```cpp {filename="selection.cpp, lines 3–13"}
void selectionSort(std::vector<int>& a) {
    int n = a.size(), swaps = 0;
    for (int i = 0; i + 1 < n; ++i) {
        int m = i;
        for (int j = i + 1; j < n; ++j)
            if (a[j] < a[m]) m = j;                  // index of the minimum of a[i..]
        if (m != i) { std::swap(a[i], a[m]); ++swaps; }
        show("pass " + std::to_string(i + 1), a);
    }
    std::printf("swaps = %d, comparisons = %d\n", swaps, n * (n - 1) / 2);
}
```

```text {filename="Output of selection.cpp"}
input          [29 10 14 37 13 5 41 8]
pass 1         [5 10 14 37 13 29 41 8]
pass 2         [5 8 14 37 13 29 41 10]
pass 3         [5 8 10 37 13 29 41 14]
pass 4         [5 8 10 13 37 29 41 14]
pass 5         [5 8 10 13 14 29 41 37]
pass 6         [5 8 10 13 14 29 41 37]
pass 7         [5 8 10 13 14 29 37 41]
swaps = 6, comparisons = 28
```

<div class="nb nb-definition" id="fact-13-2-4">

<strong>Fact 13.2.4</strong>. Always exactly $n(n-1)/2$ comparisons, best case included: it is not adaptive. At most $n - 1$ swaps, the fewest of the simple sorts, which matters when writes are expensive (flash memory). Not stable (the long swap, above). In place. Passes $5$ and $6$ above find the minimum already in place and swap nothing, which is why there are only $6$ swaps.

</div>

### 13.2.iii Insertion sort {#sec-dsa-insertion}

<div class="nb nb-remark" id="algorithm-13-2-5">

<strong>Algorithm 13.2.5</strong> (Insertion sort) — Keep `a[0..i-1]` sorted; take `a[i]` and shift larger elements one place right until its slot is found.

</div>

```cpp {filename="insertion.cpp, lines 10–19"}
void insertionSort(std::vector<int>& a) {
    int shifts = 0;
    for (int i = 1; i < (int)a.size(); ++i) {
        int key = a[i], j = i - 1;
        while (j >= 0 && a[j] > key) { a[j + 1] = a[j]; --j; ++shifts; }
        a[j + 1] = key;
        show("insert " + std::to_string(key), a);
    }
    std::printf("shifts = %d\n", shifts);
}
```

```text {filename="Output of insertion.cpp"}
input          [29 10 14 37 13 5 41 8]
inversions = 16
insert 10      [10 29 14 37 13 5 41 8]
insert 14      [10 14 29 37 13 5 41 8]
insert 37      [10 14 29 37 13 5 41 8]
insert 13      [10 13 14 29 37 5 41 8]
insert 5       [5 10 13 14 29 37 41 8]
insert 41      [5 10 13 14 29 37 41 8]
insert 8       [5 8 10 13 14 29 37 41]
shifts = 16
```

<div class="nb nb-theorem nb-block" id="theorem-13-2-6">

<strong>Theorem 13.2.6</strong> (Insertion sort and inversions)

Insertion sort performs exactly one shift per inversion, so its running time is $\Theta(n + I)$ where $I$ is the number of inversions. Hence $\Theta(n)$ on sorted input, $\Theta(n^2)$ on reversed input, and $\Theta(n^2)$ on average ($I = n(n-1)/4$ for a random permutation).

</div>

<div class="nb nb-proof">

<em>Proof.</em> Shifting `a[j]` past the key removes exactly one inversion (the pair $(a_j, \text{key})$) and creates none; sorting ends with $0$ inversions. The output confirms $16$ shifts for $16$ inversions.

</div>

<div class="nb nb-definition" id="fact-13-2-7">

<strong>Fact 13.2.7</strong>. Stable, in place, adaptive, online (it can insert elements as they arrive). With $n \le$ about $16$–$32$ it is the fastest sort in practice (tight loop, sequential access, no overhead), which is why every hybrid sort switches to it on small ranges. Binary search for the insertion point reduces comparisons to $O(n\log n)$ but not the $\Theta(n^2)$ shifts. Any algorithm that swaps only adjacent elements removes one inversion per swap and therefore needs $\Omega(n^2)$ swaps on average.

</div>

### 13.2.iv Shell sort {#s13-2-iv}

<div class="nb nb-remark" id="algorithm-13-2-8">

<strong>Algorithm 13.2.8</strong> (Shell sort) — Insertion sort on elements $g$ apart, for a decreasing sequence of gaps ending with $1$. Large gaps move elements far in few steps, killing the turtles; the final gap-$1$ pass is ordinary insertion sort on an almost sorted array.

</div>

```cpp {filename="shell.cpp, lines 4–14"}
void shellSort(std::vector<int>& a) {
    int n = a.size();
    for (int gap = n / 2; gap > 0; gap /= 2) {
        for (int i = gap; i < n; ++i) {
            int key = a[i], j = i;
            while (j >= gap && a[j - gap] > key) { a[j] = a[j - gap]; j -= gap; }
            a[j] = key;
        }
        show("gap " + std::to_string(gap), a);
    }
}
```

```text {filename="Output of shell.cpp"}
input          [29 10 14 37 13 5 41 8]
gap 4          [13 5 14 8 29 10 41 37]
gap 2          [13 5 14 8 29 10 41 37]
gap 1          [5 8 10 13 14 29 37 41]
```

<div class="nb nb-definition" id="fact-13-2-9">

<strong>Fact 13.2.9</strong>. The complexity depends on the gap sequence: $\Theta(n^2)$ worst case for Shell’s $n/2, n/4, \ldots$ (the gap-$2$ pass above changed nothing), $O(n^{3/2})$ for Knuth’s $1, 4, 13, 40, \ldots$ ($h = 3h + 1$), $O(n^{4/3})$ for Sedgewick’s sequences. Not stable (elements jump over equal keys), in place, adaptive. Useful in embedded code: no recursion, no extra memory, decent speed.

</div>

## 13.3 Merge sort {#sec-dsa-merge}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> merging two sorted piles of exam papers by repeatedly taking the smaller top sheet.</em>

</div>

<div class="nb nb-remark" id="algorithm-13-3-1">

<strong>Algorithm 13.3.1</strong> (Merge sort) — Split the array in halves, sort each half recursively, merge the two sorted halves in linear time with a buffer. The bottom-up version merges runs of width $1, 2, 4, \ldots$ without recursion.

</div>

```cpp {filename="merge.cpp, lines 5–24"}
// Merge the sorted runs a[lo..mid) and a[mid..hi). Taking from the left on ties keeps it stable.
void mergeRuns(std::vector<int>& a, int lo, int mid, int hi) {
    std::vector<int> out;
    int i = lo, j = mid;
    while (i < mid && j < hi) { ++comparisons; out.push_back(a[i] <= a[j] ? a[i++] : a[j++]); }
    while (i < mid) out.push_back(a[i++]);
    while (j < hi) out.push_back(a[j++]);
    for (int k = lo; k < hi; ++k) a[k] = out[k - lo];
}

// Bottom-up merge sort: merge runs of width 1, 2, 4, ...
void mergeSort(std::vector<int>& a) {
    int n = a.size();
    for (int w = 1; w < n; w *= 2) {
        for (int lo = 0; lo + w < n; lo += 2 * w)
            mergeRuns(a, lo, lo + w, std::min(lo + 2 * w, n));
        show("width " + std::to_string(w), a);
    }
    std::printf("comparisons = %ld\n", comparisons);
}
```

```text {filename="Output of merge.cpp"}
input          [29 10 14 37 13 5 41 8]
width 1        [10 29 14 37 5 13 8 41]
width 2        [10 14 29 37 5 8 13 41]
width 4        [5 8 10 13 14 29 37 41]
comparisons = 17
```

<div class="nb nb-definition" id="fact-13-3-2">

<strong>Fact 13.3.2</strong>.

- $T(n) = 2T(n/2) + \Theta(n) = \Theta(n\log n)$ in <em>every</em> case: it is not adaptive in this basic form.
- Merging runs of lengths $a$ and $b$ takes between $\min(a, b)$ and $a + b - 1$ comparisons; the whole sort makes at most $n\lceil \log_2 n\rceil - 2^{\lceil \log_2 n \rceil} + 1$ comparisons ($17$ for $n = 8$: exactly what the output shows).
- Stable, <em>if</em> the merge takes from the left run on ties (`<=` above; `<` would break stability).
- $\Theta(n)$ extra memory for arrays (in-place merging exists but is slow and complicated); only $O(1)$ extra for linked lists, where merging relinks nodes. That, plus needing no random access, makes merge sort the sort for linked lists.
- Parallelises naturally, and is the basis of <strong>external sorting</strong>: sort memory-sized chunks into runs on disk, then $k$-way merge them with a heap, reading every run sequentially.

</div>

## 13.4 Quicksort {#sec-dsa-quick}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> pick a pivot, put smaller elements to its left and larger to its right; the pivot is now in its final place.</em>

</div>

<div class="nb nb-remark" id="algorithm-13-4-1">

<strong>Algorithm 13.4.1</strong> (Quicksort) — Choose a <strong>pivot</strong>, <strong>partition</strong> the array so that smaller elements precede it and larger ones follow, then sort both sides recursively. No combine step is needed.

</div>

### 13.4.i Partition schemes {#s13-4-i}

<div class="nb nb-definition" id="definition-13-4-2">

<strong>Definition 13.4.2</strong>. <strong>Lomuto partition</strong> takes the last element as pivot and scans once, keeping `a[lo..i)` $<$ pivot; it ends by swapping the pivot into index $i$, its final position. <strong>Hoare partition</strong> takes (traditionally) the first element, moves two indices towards each other and swaps out-of-place pairs; it makes about three times fewer swaps but returns only a split point, not the pivot’s final index.

</div>

```cpp {filename="quick.cpp, lines 5–33"}
// Lomuto: pivot = last element; a[lo..i) < pivot <= a[i..j)
int lomuto(std::vector<int>& a, int lo, int hi) {
    int pivot = a[hi], i = lo;
    for (int j = lo; j < hi; ++j)
        if (a[j] < pivot) std::swap(a[i++], a[j]);
    std::swap(a[i], a[hi]);                   // pivot lands at its final index i
    return i;
}

void quickSort(std::vector<int>& a, int lo, int hi) {
    if (lo >= hi) return;
    int pv = a[hi];
    int p = lomuto(a, lo, hi);
    std::printf("pivot %2d -> index %d  ", pv, p);
    show("", *whole);
    quickSort(a, lo, p - 1);
    quickSort(a, p + 1, hi);
}

// Hoare: pivot = first element; returns j with a[lo..j] <= pivot <= a[j+1..hi]
int hoare(std::vector<int>& a, int lo, int hi) {
    int pivot = a[lo], i = lo - 1, j = hi + 1;
    while (true) {
        do ++i; while (a[i] < pivot);
        do --j; while (a[j] > pivot);
        if (i >= j) return j;
        std::swap(a[i], a[j]);
    }
}
```

```text {filename="Output of quick.cpp"}
input          [29 10 14 37 13 5 41 8]
pivot  8 -> index 1                 [5 8 14 37 13 29 41 10]
pivot 10 -> index 2                 [5 8 10 37 13 29 41 14]
pivot 14 -> index 4                 [5 8 10 13 14 29 41 37]
pivot 37 -> index 6                 [5 8 10 13 14 29 37 41]
Hoare partition of the input around 29 -> split after index 4
               [8 10 14 5 13 37 41 29]
```

<div class="nb nb-example nb-block" id="example-13-4-3">

<strong>Example 13.4.3</strong> (Reading the trace)

The first pivot is $8$, the second smallest element, so the partition is badly unbalanced ($1$ element left, $6$ right). After each partition the pivot never moves again: $8$ at index $1$, $10$ at $2$, $14$ at $4$, $37$ at $6$. The Hoare partition of the same input around $29$ splits it into `[8 10 14 5 13]` and `[37 41 29]`; $29$ itself is not yet in its final place.

</div>

### 13.4.ii Complexity {#s13-4-ii}

<div class="nb nb-theorem nb-block" id="theorem-13-4-4">

<strong>Theorem 13.4.4</strong> (Quicksort’s running time)

- <em>Best case</em> (pivot always the median): $T(n) = 2T(n/2) + \Theta(n) = \Theta(n \log n)$.
- <em>Worst case</em> (pivot always the minimum or maximum): $T(n) = T(n-1) + \Theta(n) = \Theta(n^2)$, exactly $n(n-1)/2$ comparisons. With the first or last element as pivot this happens on sorted, reverse-sorted and all-equal input (with a two-way partition).
- <em>Average case</em> over random permutations, and <em>expected</em> case of randomized quicksort on any input: about $2n\ln n \approx 1.39\,n\log_2 n$ comparisons, $\Theta(n\log n)$.
- Even a constant-fraction split (say $1 : 9$ every time) gives $\Theta(n\log n)$: depth $\log_{10/9} n$, linear work per level.

</div>

<div class="nb nb-proof">

<em>Why $2n\ln n$.</em> Let $z_1 < \cdots < z_n$ be the sorted keys. $z_i$ and $z_j$ are compared iff one of them is the first pivot chosen among $z_i, \ldots, z_j$ (any other pivot from that range separates them), which has probability $2/(j - i + 1)$. Summing over pairs, $\mathbb E[\text{comparisons}] = \sum_{i<j} \frac{2}{j-i+1} \le 2n H_n \approx 2n\ln n$.

</div>

<div class="nb nb-remark" id="remark-13-4-5">

<strong>Remark 13.4.5</strong> (Making the worst case unlikely) —

- <strong>Randomized pivot</strong>: the expected time is $O(n\log n)$ for every input; the worst case is still $\Theta(n^2)$ but with vanishing probability.
- <strong>Median of three</strong> (first, middle, last) fixes sorted input and gives better splits; it can still be defeated by crafted “median-of-three killer” inputs.
- <strong>Three-way partition</strong> (Dijkstra’s Dutch national flag: $< p$, $= p$, $> p$) makes inputs with many duplicates $\Theta(n)$ instead of $\Theta(n^2)$ (an all-equal array is one partition).
- <strong>Introsort</strong> switches to heap sort when the recursion gets too deep, guaranteeing $O(n\log n)$ ([Section 13.6](#sec-dsa-introsort)).
- Recursing on the smaller side and looping on the larger bounds the stack by $O(\log n)$ even in the worst case.

</div>

<div class="nb nb-definition" id="fact-13-4-6">

<strong>Fact 13.4.6</strong> (Why quicksort is the fastest in practice). Its inner loop compares against a pivot held in a register and walks memory sequentially (cache friendly), it sorts in place, and it makes fewer data moves than merge sort. It is not stable, and its worst case must be guarded against. Java sorts primitive arrays with a dual-pivot variant (two pivots, three parts).

</div>

## 13.5 Heap sort {#sec-dsa-heapsort}

<div class="nb nb-remark" id="algorithm-13-5-1">

<strong>Algorithm 13.5.1</strong> (Heap sort) — Build a max-heap in $O(n)$ ([Section 8.3](../08-heaps/#sec-dsa-buildheap)), then $n - 1$ times swap the root (the maximum) with the last element of the heap, shrink the heap by one, and sift the new root down.

</div>

```cpp {filename="heapsort.cpp, lines 3–24"}
// Sift a[i] down in the max-heap a[0..n): children of i are 2i+1 and 2i+2.
void siftDown(std::vector<int>& a, int i, int n) {
    while (true) {
        int big = i, l = 2 * i + 1, r = 2 * i + 2;
        if (l < n && a[l] > a[big]) big = l;
        if (r < n && a[r] > a[big]) big = r;
        if (big == i) return;
        std::swap(a[i], a[big]);
        i = big;
    }
}

void heapSort(std::vector<int>& a) {
    int n = a.size();
    for (int i = n / 2 - 1; i >= 0; --i) siftDown(a, i, n);   // build-heap, O(n)
    show("max-heap", a);
    for (int end = n - 1; end > 0; --end) {
        std::swap(a[0], a[end]);                              // max goes to its final place
        siftDown(a, 0, end);
        show("extract " + std::to_string(a[end]), a);
    }
}
```

```text {filename="Output of heapsort.cpp"}
input          [29 10 14 37 13 5 41 8]
max-heap       [41 37 29 10 13 5 14 8]
extract 41     [37 13 29 10 8 5 14 41]
extract 37     [29 13 14 10 8 5 37 41]
extract 29     [14 13 5 10 8 29 37 41]
extract 14     [13 10 5 8 14 29 37 41]
extract 13     [10 8 5 13 14 29 37 41]
extract 10     [8 5 10 13 14 29 37 41]
extract 8      [5 8 10 13 14 29 37 41]
```

<div class="nb nb-definition" id="fact-13-5-2">

<strong>Fact 13.5.2</strong>. $O(n \log n)$ in the worst case and $O(1)$ extra memory: the only standard comparison sort with both. Not stable (the swaps jump over equal keys), not adaptive. In practice two to three times slower than quicksort, because sift-down jumps from $i$ to $2i+1$ across memory (cache misses) and the element moved to the root is small and almost always sinks to the bottom again. Its real use is as the safety net inside introsort, and its partial form (stop after $k$ extractions) gives the top $k$ in $O(n + k\log n)$.

</div>

## 13.6 Hybrid sorts used by real libraries {#sec-dsa-introsort}

<div class="nb nb-definition" id="definition-13-6-1">

<strong>Definition 13.6.1</strong>. <strong>Introsort</strong> (C++ `std::sort` in libstdc++ and others) runs quicksort with median-of-three pivots, switches to <em>heap sort</em> when the recursion depth exceeds $2\lfloor \log_2 n\rfloor$, and finishes small partitions ($16$ elements in libstdc++) with <em>insertion sort</em>. Worst case $O(n\log n)$, not stable.

</div>

<div class="nb nb-definition" id="definition-13-6-2">

<strong>Definition 13.6.2</strong>. <strong>Timsort</strong> (Python before 3.11’s refinement, Java for objects, Android, V8) finds the <strong>runs</strong> that already exist in the data (reversing descending ones), extends short runs to a minimum length of $32$ to $64$ with binary insertion sort, and merges runs with a stack whose invariants keep the merges balanced, using “galloping” when one run keeps winning. It is stable, $O(n\log n)$ worst case, and $O(n)$ on sorted or reverse-sorted input or input made of a few sorted runs: <em>adaptive merge sort</em>. It needs up to $n/2$ extra memory.

</div>

## 13.7 Sorting without comparisons {#sec-dsa-noncomp}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> sorting $10^7$ exam marks between $0$ and $100$: count them.</em>

</div>

### 13.7.i Counting sort {#s13-7-i}

<div class="nb nb-remark" id="algorithm-13-7-1">

<strong>Algorithm 13.7.1</strong> (Counting sort, keys in $\{0, \ldots, k\}$) — Count the occurrences of each key, turn the counts into prefix sums (so `cnt[v]` is the number of keys $\le v$, i.e. one past the last slot for $v$), then place the elements scanning the input from right to left, decrementing the slot counter. $\Theta(n + k)$ time and space.

</div>

```cpp {filename="counting.cpp, lines 3–13"}
// Stable counting sort for keys in [0, k].
std::vector<int> countingSort(const std::vector<int>& a, int k) {
    std::vector<int> cnt(k + 1, 0), out(a.size());
    for (int x : a) cnt[x]++;
    show("counts", cnt);
    for (int v = 1; v <= k; ++v) cnt[v] += cnt[v - 1];      // cnt[v] = #keys <= v
    show("prefix sums", cnt);
    for (int i = (int)a.size() - 1; i >= 0; --i)              // right to left: stable
        out[--cnt[a[i]]] = a[i];
    return out;
}
```

```text {filename="Output of counting.cpp"}
input          [4 2 2 8 3 3 1]
counts         [0 1 2 2 1 0 0 0 1]
prefix sums    [0 1 3 5 6 6 6 6 7]
output         [1 2 2 3 3 4 8]
```

<div class="nb nb-definition" id="fact-13-7-2">

<strong>Fact 13.7.2</strong>. Stable thanks to the right-to-left pass (that is the only reason for it), which is exactly what radix sort needs. Not in place. Good only when $k = O(n)$: sorting $10$ numbers up to $10^9$ this way is absurd. It does not violate the $\Omega(n\log n)$ bound because it never compares keys; it uses them as indices.

</div>

### 13.7.ii Radix sort {#s13-7-ii}

<div class="nb nb-remark" id="algorithm-13-7-3">

<strong>Algorithm 13.7.3</strong> (LSD radix sort) — Sort by the least significant digit, then by the next, …, up to the most significant, each pass with a <em>stable</em> sort (counting sort on $b$ possible digit values). Correctness rests on stability: after pass $i$ the keys are sorted by their last $i$ digits.

</div>

```cpp {filename="radix.cpp, lines 3–14"}
// LSD radix sort, base 10: one stable counting sort per digit, least significant first.
void radixSort(std::vector<int>& a) {
    int mx = *std::max_element(a.begin(), a.end());
    for (int exp = 1; mx / exp > 0; exp *= 10) {
        std::vector<int> cnt(10, 0), out(a.size());
        for (int x : a) cnt[x / exp % 10]++;
        for (int d = 1; d < 10; ++d) cnt[d] += cnt[d - 1];
        for (int i = (int)a.size() - 1; i >= 0; --i) out[--cnt[a[i] / exp % 10]] = a[i];
        a = out;
        show("by digit " + std::to_string(exp), a);
    }
}
```

```text {filename="Output of radix.cpp"}
input          [170 45 75 90 802 24 2 66]
by digit 1     [170 90 802 2 24 45 75 66]
by digit 10    [802 2 24 45 66 170 75 90]
by digit 100   [2 24 45 66 75 90 170 802]
```

<div class="nb nb-definition" id="fact-13-7-4">

<strong>Fact 13.7.4</strong>. $d$ passes of $\Theta(n + b)$: $\Theta(d(n + b))$. For $n$ integers below $n^c$, choosing $b = n$ gives $d = c$ passes: linear time for polynomially bounded integers. <strong>MSD radix sort</strong> goes from the most significant digit and recurses into each bucket; it can stop early on distinct prefixes and is the natural way to sort strings (lexicographic order).

</div>

### 13.7.iii Bucket sort {#s13-7-iii}

<div class="nb nb-remark" id="algorithm-13-7-5">

<strong>Algorithm 13.7.5</strong> (Bucket sort) — For keys spread uniformly over $[0, 1)$: create $n$ buckets, put key $x$ into bucket $\lfloor nx \rfloor$, sort each bucket (insertion sort), concatenate. Expected $\Theta(n)$ because each bucket holds $O(1)$ keys on average ($\mathbb E[\sum n_i^2] = 2n - 1$); worst case $\Theta(n^2)$ when all keys land in one bucket. Stable if the per-bucket sort is.

</div>

## 13.8 Curiosities that interviews mention {#s13-8}

<div class="nb nb-definition" id="fact-13-8-1">

<strong>Fact 13.8.1</strong>.

- <strong>Cycle sort</strong>: places each element directly in its final position by counting smaller elements, following the cycles of the permutation; $\Theta(n^2)$ comparisons but the minimum possible number of <em>writes</em>, $n - (\text{number of cycles})$.
- <strong>Pancake sorting</strong>: only prefix reversals are allowed; $O(n)$ flips (at most $2n - 3$).
- <strong>Odd–even transposition sort</strong> and <strong>bitonic sort</strong>: fixed comparison networks that run in parallel ($O(\log^2 n)$ depth for bitonic), used on GPUs and in hardware.
- <strong>Comb sort</strong> (bubble sort with shrinking gaps) and <strong>cocktail shaker sort</strong> (bidirectional bubble sort, which handles turtles) are bubble-sort improvements.
- <strong>Bogosort</strong> (shuffle until sorted, $\Theta(n \cdot n!)$ expected) and <strong>sleep sort</strong> are jokes; know them only to recognise them.

</div>

## 13.9 Measured comparison counts {#sec-dsa-sortmeasured}

The program `sortcounts.cpp` counts the key comparisons of seven sorts on $1000$ random, sorted and reversed keys:

```text {filename="Output of sortcounts.cpp"}
n = 1000                random    sorted  reversed
bubble (early exit)     497222       999    499500
selection               499500    499500    499500
insertion               252163       999    499500
merge (top-down)          8693      4932      5044
quick, last pivot        10563    499500    499500
quick, random pivot      10871     10330     10469
heap                     16839     17583     15965
n(n-1)/2 = 499500,  n log2 n = 9966
```

<div class="nb nb-remark" id="remark-13-9-1">

<strong>Remark 13.9.1</strong> (What the table shows) —

- Selection sort is blind: $499500$ comparisons whatever the input.
- Insertion sort and bubble sort with the flag drop to $n - 1 = 999$ on sorted input; on random input insertion sort makes about $n^2/4$, half of bubble sort’s.
- Last-element-pivot quicksort hits its $\Theta(n^2)$ worst case on sorted and reversed input; the random pivot is immune.
- Merge sort and heap sort stay near $n\log_2 n \approx 9966$ (heap sort somewhat above it, merge sort below), and merge sort needs only about half as many on sorted input because every merge stops as soon as one run is exhausted.

</div>

## 13.10 The master table {#sec-dsa-sorttable}

| Algorithm | Best | Average | Worst | Extra space | Stable | In place | Adaptive |
|:--|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| Bubble (with flag) | $n$ | $n^2$ | $n^2$ | $1$ | yes | yes | yes |
| Selection | $n^2$ | $n^2$ | $n^2$ | $1$ | no | yes | no |
| Insertion | $n$ | $n^2$ | $n^2$ | $1$ | yes | yes | yes |
| Shell (Knuth gaps) | $n\log n$ | $\approx n^{1.25}$ | $n^{1.5}$ | $1$ | no | yes | yes |
| Merge | $n\log n$ | $n\log n$ | $n\log n$ | $n$ | yes | no | no |
| Quick (random pivot) | $n\log n$ | $n\log n$ | $n^2$ | $\log n$ | no | yes | no |
| Heap | $n\log n$ | $n\log n$ | $n\log n$ | $1$ | no | yes | no |
| Introsort (`std::sort`) | $n\log n$ | $n\log n$ | $n\log n$ | $\log n$ | no | yes | no |
| Timsort | $n$ | $n\log n$ | $n\log n$ | $n$ | yes | no | yes |
| Tree sort (balanced BST) | $n\log n$ | $n\log n$ | $n\log n$ | $n$ | yes$^*$ | no | no |
| Cycle | $n^2$ | $n^2$ | $n^2$ | $1$ | no | yes | no |
| Counting | $n + k$ | $n + k$ | $n + k$ | $n + k$ | yes | no | – |
| Radix (LSD) | $d(n + b)$ | $d(n + b)$ | $d(n + b)$ | $n + b$ | yes | no | – |
| Bucket | $n$ | $n$ | $n^2$ | $n$ | yes | no | – |

<div class="nb-caption" id="table-13-1">

<strong>Table 13.1.</strong> All bounds are $\Theta(\cdot)$ time. $k$ = key range, $d$ = number of digits, $b$ = base. ${}^*$If equal keys are inserted after existing ones. Online: insertion sort (and tree sort). Heap sort’s best case is $\Theta(n)$ only when all keys are equal.

</div>

## 13.11 Which sort when? {#s13-11}

<div class="nb nb-definition" id="fact-13-11-1">

<strong>Fact 13.11.1</strong>.

- <em>General purpose, in memory</em>: the library sort (introsort, or Timsort for objects).
- <em>Need stability</em>: merge sort, Timsort, insertion sort for small $n$, counting/radix.
- <em>Worst-case $O(n\log n)$ with $O(1)$ memory</em>: heap sort.
- <em>Nearly sorted data</em> or a few elements out of place: insertion sort ($O(n + I)$) or Timsort. A <strong>$k$-sorted</strong> array (each element within $k$ of its final position): a min-heap of size $k + 1$, $O(n\log k)$.
- <em>Linked list</em>: merge sort ($O(1)$ extra space, no random access needed).
- <em>Small integer keys</em>: counting sort; <em>fixed-width integers or strings</em>: radix sort.
- <em>Data larger than memory</em>: external merge sort.
- <em>Expensive writes</em>: selection sort or cycle sort.
- <em>Only the $k$ smallest, or the median</em>: do not sort; use a heap or quickselect.

</div>

## 13.12 Selection: the $k$-th smallest without sorting {#sec-dsa-selection}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> the median of $10^7$ numbers in linear time.</em>

</div>

<div class="nb nb-remark" id="algorithm-13-12-1">

<strong>Algorithm 13.12.1</strong> (Quickselect (Hoare)) — Partition as in quicksort; the pivot lands at its final index $p$. If $p = k$ we are done; otherwise continue in the <em>one</em> side that contains index $k$.

</div>

```cpp {filename="quickselect.cpp, lines 4–15"}
int quickselect(std::vector<int>& a, int k) {          // k is 0-based
    int lo = 0, hi = (int)a.size() - 1;
    while (true) {
        int pivot = a[hi], i = lo;                     // Lomuto, last element as pivot
        for (int j = lo; j < hi; ++j) if (a[j] < pivot) std::swap(a[i++], a[j]);
        std::swap(a[i], a[hi]);
        std::printf("pivot %2d lands at %d  ", pivot, i);
        show("", a);
        if (i == k) return a[i];
        if (k < i) hi = i - 1; else lo = i + 1;        // recurse into one side only
    }
}
```

```text {filename="Output of quickselect.cpp"}
median (k = 3, 0-based) of [29 10 14 37 13 5 41 8]
pivot  8 lands at 1                 [5 8 14 37 13 29 41 10]
pivot 10 lands at 2                 [5 8 10 37 13 29 41 14]
pivot 14 lands at 4                 [5 8 10 13 14 29 41 37]
pivot 13 lands at 3                 [5 8 10 13 14 29 41 37]
answer 13
```

<div class="nb nb-definition" id="fact-13-12-2">

<strong>Fact 13.12.2</strong>. Expected time $T(n) = T(\approx n/2) + \Theta(n) = \Theta(n)$ with a random pivot (at most about $3.4n$ comparisons on average); worst case $\Theta(n^2)$. <strong>Median of medians</strong> (Blum, Floyd, Pratt, Rivest, Tarjan) chooses the pivot as the median of the medians of groups of $5$, which guarantees that at least $3n/10$ elements fall on each side, giving $T(n) \le T(n/5) + T(7n/10) + \Theta(n) = \Theta(n)$ worst case. It is mostly of theoretical interest; `std::nth_element` uses introselect (quickselect with a fallback).

</div>

<div class="nb nb-moral">

Know each sort by four properties (time, space, stability, adaptivity) and by the one reason it exists: insertion sort for small or nearly sorted input, merge sort for stability and lists, quicksort for speed, heap sort for guarantees, counting and radix sort for integer keys.

</div>

## 13.13 A few harder problems to think about {#s13-13}

<div class="nb nb-problem nb-block" id="problem-13a">

<strong>Problem 13A</strong> (After three passes)

Give the array after three passes of (a) bubble sort, (b) selection sort, (c) insertion sort (three insertions) on `[64 25 12 22 11 90 3]`.

<details class="nb-hint">
<summary>Hint</summary>

Bubble moves the largest to the end each pass; selection moves the smallest to the front; insertion sorts a growing prefix.

</details>

<details class="nb-sol">
<summary>Solution</summary>

(a) `[12 11 22 3 25 64 90]` (after pass 1: `[25 12 22 11 64 3 90]`, after pass 2: `[12 22 11 25 3 64 90]`); (b) `[3 11 12 22 25 90 64]`; (c) `[12 22 25 64 11 90 3]`. All three are printed by `sortcheck.cpp`.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-13b">

<strong>Problem 13B</strong> (Count)

How many inversions does `[5 1 4 2 3]` have? How many swaps does bubble sort make on it, how many shifts does insertion sort make, and how many swaps does selection sort make?

<details class="nb-hint">
<summary>Hint</summary>

Bubble swaps and insertion shifts both equal the number of inversions.

</details>

<details class="nb-sol">
<summary>Solution</summary>

Inversions: $(5,1), (5,4), (5,2), (5,3), (4,2), (4,3)$: $6$. Bubble swaps $6$, insertion shifts $6$. Selection sort: pass 1 swaps $5$ and $1$ (`[1 5 4 2 3]`), pass 2 swaps $5$ and $2$ (`[1 2 4 5 3]`), pass 3 swaps $4$ and $3$ (`[1 2 3 5 4]`), pass 4 swaps $5$ and $4$: $4$ swaps.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-13c">

<strong>Problem 13C</strong> (Partition)

Apply one Lomuto partition (pivot = last element) to `[7 2 9 4 3 8 6]`. Where does the pivot end up and what is the array?

<details class="nb-hint">
<summary>Hint</summary>

Elements smaller than $6$ are swapped to the front in order of appearance.

</details>

<details class="nb-sol">
<summary>Solution</summary>

Smaller than $6$: $2, 4, 3$, swapped into positions $0, 1, 2$ in turn: `[2 4 3 7 9 8 6]` after the scan, then the pivot is swapped into index $3$: `[2 4 3 6 9 8 7]`.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-13d">

<strong>Problem 13D</strong> (Stability puzzle)

Which of these are stable as usually implemented: selection, insertion, shell, merge, quick, heap, counting, radix (LSD)? What breaks if LSD radix sort uses an unstable sort per digit?

<details class="nb-hint">
<summary>Hint</summary>

Long-distance swaps break stability.

</details>

<details class="nb-sol">
<summary>Solution</summary>

Stable: insertion, merge, counting, radix. Not stable: selection, shell, quick, heap. With an unstable per-digit sort, the order established by the earlier (less significant) digits can be destroyed among keys that share the current digit. Example: `[13 12]` after the units pass is `[12 13]`; both have tens digit $1$, so an unstable tens pass is free to output `[13 12]`, which is not sorted.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-13e">

<strong>Problem 13E</strong> 🌶🌶 (Worst cases)

For each, give an input of size $n$ that triggers the worst case: (a) insertion sort; (b) quicksort with the first element as pivot; (c) bubble sort with the flag needing all $n - 1$ passes but only $n - 1$ swaps.

<details class="nb-hint">
<summary>Hint</summary>

For (c), think of a turtle.

</details>

<details class="nb-sol">
<summary>Solution</summary>

(a) reverse-sorted input, $n(n-1)/2$ shifts. (b) sorted (or reverse-sorted) input. (c) `[2 3 4 ... n 1]`: the $1$ moves one step left per pass, so $n - 1$ passes are needed, each with exactly one swap.

</details>

</div>
