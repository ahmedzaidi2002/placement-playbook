---
title: "12 · Searching"
linkTitle: "12 Searching"
weight: 12
math: true
---
## 12.1 Linear search {#s12-1}

<div class="nb nb-definition" id="fact-12-1-1">

<strong>Fact 12.1.1</strong>. Scanning an unsorted array is $\Theta(n)$ worst case; a successful search for a uniformly random present key looks at $(n + 1)/2$ elements on average, an unsuccessful one at all $n$. A <strong>sentinel</strong> (placing the key after the last element) removes the bounds check from the loop. Linear search is optimal for unsorted data and for tiny arrays, and it is the only option for a singly linked list.

</div>

## 12.2 Binary search {#sec-dsa-binsearch}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> guessing a number between $1$ and $1000$ in at most $10$ questions.</em>

</div>

<div class="nb nb-remark" id="algorithm-12-2-1">

<strong>Algorithm 12.2.1</strong> (Binary search on a sorted array) — Keep an interval $[lo, hi]$ that contains the key if it is present. Compare with the middle element and discard the half that cannot contain it. Each step halves the interval, so it takes at most $\lfloor \log_2 n \rfloor + 1$ comparisons with the middle element: $\Theta(\log n)$ worst case, $\Theta(1)$ space iteratively.

</div>

```cpp {filename="search.cpp, lines 9–21"}
    std::vector<int> a = {3, 8, 12, 17, 21, 21, 21, 30, 42, 56, 61, 77, 85, 90, 99};
    int x = 61, lo = 0, hi = (int)a.size() - 1;
    std::printf("search %d in 15 sorted keys\n", x);
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;                     // not (lo+hi)/2: that can overflow
        std::printf("  lo=%2d hi=%2d mid=%2d a[mid]=%2d\n", lo, hi, mid, a[mid]);
        if (a[mid] == x) { std::printf("  found at %d\n", mid); break; }
        if (a[mid] < x) lo = mid + 1; else hi = mid - 1;
    }
    auto lb = std::lower_bound(a.begin(), a.end(), 21) - a.begin();
    auto ub = std::upper_bound(a.begin(), a.end(), 21) - a.begin();
    std::printf("21: lower_bound %ld, upper_bound %ld, count %ld\n", (long)lb, (long)ub, (long)(ub - lb));
    std::printf("25: lower_bound %ld (insertion point)\n", (long)(std::lower_bound(a.begin(), a.end(), 25) - a.begin()));
```

```text {filename="Output of search.cpp"}
search 61 in 15 sorted keys
  lo= 0 hi=14 mid= 7 a[mid]=30
  lo= 8 hi=14 mid=11 a[mid]=77
  lo= 8 hi=10 mid= 9 a[mid]=56
  lo=10 hi=10 mid=10 a[mid]=61
  found at 10
21: lower_bound 4, upper_bound 7, count 3
25: lower_bound 7 (insertion point)
uniform     keys: binary 18.9 probes, interpolation 6.1 probes
exponential keys: binary 14.4 probes, interpolation 70154.5 probes
```

<div class="nb nb-remark" id="remark-12-2-2">

<strong>Remark 12.2.2</strong> (The bugs everyone writes once) —

- `mid = (lo + hi) / 2` overflows when `lo + hi` exceeds the integer range (a bug that sat in Java’s `Arrays.binarySearch` for nine years); write `lo + (hi - lo) / 2`.
- Off-by-one: with a closed interval `[lo, hi]` the loop is `while (lo <= hi)` and the updates are `mid + 1` and `mid - 1`; with a half-open `[lo, hi)` it is `while (lo < hi)` and `hi = mid`. Mixing them loops forever or skips the answer.
- State the <strong>invariant</strong> (“the answer is in $[lo, hi]$”) and check that every update keeps it and that the interval strictly shrinks.

</div>

### 12.2.i Lower bound, upper bound, and searching on the answer {#s12-2-i}

<div class="nb nb-definition" id="definition-12-2-3">

<strong>Definition 12.2.3</strong>. `lower_bound(x)` is the first position whose element is $\ge x$; `upper_bound(x)` is the first position whose element is $> x$. Their difference is the number of copies of $x$, and `lower_bound` is the insertion point that keeps the array sorted (the output shows both for $21$, and $7$ as the insertion point of $25$).

</div>

<div class="nb nb-definition" id="fact-12-2-4">

<strong>Fact 12.2.4</strong> (The general form). Binary search works on any <em>monotone predicate</em> $P$ over an ordered range: if $P(x)$ is false, false, …, false, true, …, true, then binary search finds the first true in $O(\log(\text{range}))$ evaluations. “Search on the answer” problems (minimum capacity to ship within $D$ days, minimum eating speed, the largest minimum distance between placed items) all have this shape: $P(c)$ = “capacity $c$ suffices” is monotone in $c$, and each evaluation is a greedy $O(n)$ check, for $O(n \log(\text{range}))$ total. On real numbers, iterate a fixed number of times ($60$ to $100$ halvings) instead of comparing with an $\varepsilon$.

</div>

<div class="nb nb-remark" id="remark-12-2-5">

<strong>Remark 12.2.5</strong> (Rotated arrays and other variants) — In a sorted array rotated by an unknown amount, at least one half around `mid` is sorted; check whether the key lies in that half’s range and discard the other: still $O(\log n)$ with distinct keys, $O(n)$ worst case with duplicates. A peak in a bitonic array, the first true in an infinite sorted stream, and the square root of an integer are all binary searches.

</div>

## 12.3 Ternary, exponential and interpolation search {#sec-dsa-othersearch}

<div class="nb nb-definition" id="fact-12-3-1">

<strong>Fact 12.3.1</strong> (Ternary search). Ternary search finds the maximum of a <em>unimodal</em> function (increasing, then decreasing) by comparing $f$ at two interior points and discarding a third of the range: $O(\log n)$. For a sorted array it is <em>worse</em> than binary search: it shrinks the range by $3$ per step with $2$ comparisons, i.e. $2\log_3 n \approx 1.26\log_2 n$ comparisons.

</div>

<div class="nb nb-definition" id="fact-12-3-2">

<strong>Fact 12.3.2</strong> (Exponential search). Check positions $1, 2, 4, 8, \ldots$ until the element there is $\ge x$, then binary search inside the last gap: $O(\log i)$ where $i$ is the position of $x$. It works on unbounded lists and is fast when the key is near the front.

</div>

<div class="nb nb-definition" id="fact-12-3-3">

<strong>Fact 12.3.3</strong> (Interpolation search). Guess the position by linear interpolation, $\text{pos} = lo + \frac{(x - a[lo])(hi - lo)}{a[hi] - a[lo]}$, the way you open a dictionary near “S” for “Smith”. On keys drawn <em>uniformly</em> it takes $O(\log \log n)$ probes on average; on skewed keys it can degrade to $\Theta(n)$.

</div>

The second half of `search.cpp` measures exactly this on $10^6$ sorted keys (the last two lines of the output): $6.1$ probes against $18.9$ for binary search on uniform keys, but tens of thousands of probes on exponentially distributed keys, where the linear guess is badly wrong.

| Method | Requirement | Time | Note |
|:--|:--|:--|:--|
| Linear | none | $\Theta(n)$ | works on lists |
| Binary | sorted, random access | $\Theta(\log n)$ | the default |
| Ternary | unimodal function | $\Theta(\log n)$ | optimisation, not lookup |
| Exponential | sorted, possibly unbounded | $O(\log i)$ | position-sensitive |
| Interpolation | sorted, roughly uniform | $O(\log \log n)$ avg, $O(n)$ worst | data-sensitive |
| Hash table | a hash function | $O(1)$ expected | no order ([Chapter 9](../09-hashing/)) |
| Balanced BST | ordering | $O(\log n)$ | supports updates and ranges |

<div class="nb-caption" id="table-12-1">

<strong>Table 12.1.</strong> Searching methods.

</div>

<div class="nb nb-moral">

Binary search is not about arrays; it is about a monotone predicate. Find the predicate and the invariant, and the code writes itself.

</div>

## 12.4 A few harder problems to think about {#s12-4}

<div class="nb nb-problem nb-block" id="problem-12a">

<strong>Problem 12A</strong> (Count the comparisons)

How many three-way comparisons does binary search make, at most, on $1000$ sorted elements? On $1024$? How many for an unsuccessful search in $15$ elements?

<details class="nb-hint">
<summary>Hint</summary>

$\lfloor \log_2 n \rfloor + 1$.

</details>

<details class="nb-sol">
<summary>Solution</summary>

$\lfloor \log_2 1000 \rfloor + 1 = 10$; $\lfloor \log_2 1024 \rfloor + 1 = 11$. With $15 = 2^4 - 1$ elements the search tree is perfect, so every unsuccessful search makes exactly $4$ comparisons.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-12b">

<strong>Problem 12B</strong> (Trace)

Binary search for $17$ in `3 8 12 17 21 21 21 30 42 56 61 77 85 90 99` (indices $0..14$, closed interval, `mid = lo + (hi - lo) / 2`). List the `mid` values.

<details class="nb-hint">
<summary>Hint</summary>

The first `mid` is $7$.

</details>

<details class="nb-sol">
<summary>Solution</summary>

$7$ ($30 > 17$, so `hi = 6`), then $3$ ($17$, found). Two probes.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-12c">

<strong>Problem 12C</strong> 🌶🌶 (Search on the answer)

Packages with weights $w_1, \ldots, w_n$ must be shipped in order within $D$ days. What is the search range for the minimum ship capacity, and the total time?

<details class="nb-hint">
<summary>Hint</summary>

The capacity must be at least the heaviest package and need not exceed the total.

</details>

<details class="nb-sol">
<summary>Solution</summary>

Binary search $c$ in $[\max w, \sum w]$; the predicate “capacity $c$ ships everything in at most $D$ days” is checked greedily in $O(n)$ and is monotone in $c$. Total $O(n\log(\sum w))$.

</details>

</div>
