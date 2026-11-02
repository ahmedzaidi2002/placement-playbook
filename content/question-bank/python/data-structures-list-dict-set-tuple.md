---
title: "Data structures (list, dict, set, tuple)"
weight: 5
---

2 questions asked by Info Edge, MathWorks. Try each one first, then open the toggle: it gives the answer, why it is right, and the idea behind it explained from scratch.

### 1 · Q40, dictionaries

*Asked by: Info Edge (Data Science II)*

Which of the following is FALSE about the dictionary data type in Python?

- **(a)** Values of a dictionary can be accessed via keys
- **(b)** Keys of a dictionary can be accessed via values
- **(c)** Dictionaries are not generally ordered
- **(d)** Dictionaries are mutable

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) keys can be accessed via values** (false)

**Why.** A dictionary maps keys to values; lookup goes key → value only. To find a key from a value you must search all entries.

**Concept: Python dict.** A hash table: average O(1) lookup by key. Keys must be hashable (immutable); values can be anything. Since Python 3.7, dicts keep insertion order, though not sorted order.

{{< /details >}}

### 2 · Q40, slicing

*Asked by: MathWorks (IIT Bombay 2024)*

`str1 = "helloworld"; str1[::-1]` gives?

{{< details title="Answer and explanation" closed="true" >}}

**Answer: `dlrowolleh`**

**Why.** `s[::-1]` takes the whole string with step −1, i.e. backwards.

**Concept: slicing `s[start:stop:step]`.** Omitted start/stop mean "from the beginning/end in the step's direction". A negative step walks backwards, so `[::-1]` reverses any sequence.

{{< /details >}}
