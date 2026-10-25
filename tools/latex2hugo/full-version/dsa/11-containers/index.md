---
title: "11 · Library containers"
linkTitle: "11 Library containers"
weight: 11
math: true
---
Interviews in C++ or Java assume you know what the standard containers are underneath, what each operation costs, and when an iterator or reference stops being valid. This chapter is a reference; the structures themselves are explained in the earlier chapters.

## 11.1 C++ standard library {#sec-dsa-stl}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> “What does `std::map` use internally? What does `std::priority_queue`?”</em>

</div>

| Container | Underlying structure | Costs |
|:--|:--|:--|
| `vector` | dynamic array | index $O(1)$; `push_back` $O(1)$ amortized; insert/erase in the middle $O(n)$ |
| `deque` | array of fixed-size blocks + index map | index $O(1)$; push/pop at both ends $O(1)$; middle $O(n)$ |
| `list` / `forward_list` | doubly / singly linked list | insert/erase at an iterator $O(1)$; no indexing; `splice` $O(1)$ |
| `stack`, `queue` | adaptors over `deque` by default | push/pop $O(1)$ |
| `priority_queue` | binary max-heap over a `vector` | push/pop $O(\log n)$, top $O(1)$; `std::greater` for a min-heap |
| `set`, `map`, `multiset`, `multimap` | red–black tree | find/insert/erase $O(\log n)$; ordered iteration; `lower_bound` $O(\log n)$ |
| `unordered_set`, `unordered_map` | hash table with chaining | $O(1)$ average, $O(n)$ worst; no order |
| `array` | fixed-size array on the stack | like a C array |
| `string` | dynamic array of `char` with small-string optimisation | like `vector` |

<div class="nb-caption" id="table-11-1">

<strong>Table 11.1.</strong> C++ containers.

</div>

<div class="nb nb-definition" id="fact-11-1-1">

<strong>Fact 11.1.1</strong> (Algorithms). `std::sort`: introsort, $O(n\log n)$ worst case (guaranteed since C++11), not stable. `std::stable_sort`: merge sort, $O(n\log n)$ with a buffer, $O(n \log^2 n)$ without one. `std::partial_sort`: heap-based, $O(n \log k)$. `std::nth_element`: introselect, $O(n)$ average. `std::binary_search`, `lower_bound`, `upper_bound`, `equal_range`: $O(\log n)$ on random-access iterators (linear steps on a `list`). `std::make_heap`: $O(n)$. Note that `std::lower_bound` on a `std::set` walks iterators in $O(n)$; call the member `s.lower_bound(x)`, which is $O(\log n)$.

</div>

## 11.2 Iterator invalidation {#sec-dsa-invalidation}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> `for (auto it = v.begin(); it != v.end(); ++it) if (*it == x) v.erase(it);` is undefined behaviour.</em>

</div>

<div class="nb nb-definition" id="fact-11-2-1">

<strong>Fact 11.2.1</strong>.

- `vector`: a reallocation (growth beyond capacity) invalidates <em>every</em> iterator, pointer and reference; insert/erase without reallocation invalidates those at or after the position.
- `deque`: insertion at either end invalidates all iterators but <em>not</em> references to elements; insertion in the middle invalidates everything.
- `list`, `set`, `map`: only iterators to the erased element are invalidated; insertion invalidates nothing.
- `unordered_map`/`set`: a rehash invalidates all iterators but not references to elements; erase invalidates only the erased element.

The safe erase loop uses the iterator that `erase` returns: `it = v.erase(it)` instead of `++it`, or the erase–remove idiom `v.erase(std::remove(v.begin(), v.end(), x), v.end())`, which is $O(n)$ in total instead of $O(n^2)$.

</div>

## 11.3 Java and Python equivalents {#s11-3}

| C++ | Java | Python |
|:--|:--|:--|
| `vector` | `ArrayList` | `list` |
| `deque` | `ArrayDeque` | `collections.deque` |
| `list` | `LinkedList` | (none; `deque` or hand-written) |
| `priority_queue` | `PriorityQueue` (min-heap) | `heapq` (min-heap functions on a list) |
| `map`/`set` | `TreeMap`/`TreeSet` (red–black) | (none built in; `bisect` on a sorted list, or `sortedcontainers`) |
| `unordered_map`/`set` | `HashMap`/`HashSet` | `dict`/`set` |
| `std::sort` | `Arrays.sort` (dual-pivot quicksort for primitives, Timsort for objects) | `sorted`/`list.sort` (Timsort; Powersort since 3.11) |

<div class="nb-caption" id="table-11-2">

<strong>Table 11.2.</strong> Containers across languages.

</div>

<div class="nb nb-remark" id="remark-11-3-1">

<strong>Remark 11.3.1</strong> (Traps) —

- Java’s `PriorityQueue` and Python’s `heapq` are <em>min</em>-heaps; C++’s `priority_queue` is a <em>max</em>-heap.
- Python’s `list.pop(0)` and `list.insert(0, x)` are $O(n)$; use a `deque`. `x in list` is $O(n)$, `x in set` is $O(1)$ average.
- Java’s `LinkedList.get(i)` is $O(n)$, so a `for (int i...)` loop over it is $O(n^2)$.
- Java sorts primitive arrays with an unstable quicksort and object arrays with stable Timsort, because stability is meaningless for primitives.
- `std::map::operator[]` inserts a default value when the key is missing; use `find` or `count` to test membership.

</div>

<div class="nb nb-moral">

Know the structure under each container; its costs and its invalidation rules both follow from it.

</div>

## 11.4 A few harder problems to think about {#s11-4}

<div class="nb nb-problem nb-block" id="problem-11a">

<strong>Problem 11A</strong> (Pick the container)

For each task choose a C++ container and give the cost: (a) the $k$ largest numbers of a stream; (b) the number of distinct words in a book; (c) for each query $x$, the smallest stored key $\ge x$, with inserts in between; (d) a queue with access to both ends.

<details class="nb-hint">
<summary>Hint</summary>

Heap, hash set, ordered set, deque.

</details>

<details class="nb-sol">
<summary>Solution</summary>

(a) A min-heap of size $k$ (a `priority_queue` with `std::greater`), $O(n \log k)$. (b) An `unordered_set<string>`, $O(\text{total length})$ expected. (c) A `set` queried with its member `lower_bound`, $O(\log n)$ per operation. (d) A `deque`, $O(1)$ at both ends.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-11b">

<strong>Problem 11B</strong> (Erase while iterating)

Why is erasing from a `std::vector` inside a range-based `for` loop wrong, and what is the cost of erasing all occurrences of $x$ one at a time from the front?

<details class="nb-hint">
<summary>Hint</summary>

Erase shifts the tail and invalidates the iterators after the erased position.

</details>

<details class="nb-sol">
<summary>Solution</summary>

The loop keeps using iterators that `erase` invalidated (undefined behaviour), and it would skip the element shifted into the erased slot. Erasing $k$ occurrences one by one shifts the tail $k$ times: $O(kn)$, up to $O(n^2)$. The erase–remove idiom compacts in one pass: $O(n)$.

</details>

</div>
