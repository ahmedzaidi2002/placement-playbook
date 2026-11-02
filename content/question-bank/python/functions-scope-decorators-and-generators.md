---
title: "Functions, scope, decorators and generators"
weight: 2
---

4 questions asked by Fujitsu, MathWorks. Try each one first, then open the toggle: it gives the answer, why it is right, and the idea behind it explained from scratch.

### 1 · PC Q5, map

*Asked by: Fujitsu (IIT Kharagpur 2023)*

What is the output of the following Python code?

```python
def func(x):
    return x * 2
result = list(map(func, [1, 2, 3, 4]))
print(result)
```

- **(a)** [1, 4, 9, 16]
- **(b)** [2, 4, 6, 8]
- **(c)** [2, 2, 2, 2]
- **(d)** [1, 2, 3, 4]

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) [2, 4, 6, 8]**

**Why.** `map(func, list)` applies `func` to each element: 1×2, 2×2, 3×2, 4×2. `list(...)` turns the lazy map object into a list.

**Concept: `map`.** `map(f, xs)` = [f(x) for x in xs], computed lazily in Python 3.

{{< /details >}}

### 2 · Q42, map and filter

*Asked by: MathWorks (IIT Bombay 2024)*

```python
list(map(lambda x: x**3, filter(lambda x: x % 2 == 0, range(5, -5, -2))))
```

What is the result?

{{< details title="Answer and explanation" closed="true" >}}

**Answer: `[]`**

**Why.** `range(5, -5, -2)` gives 5, 3, 1, −1, −3, all odd. The filter keeps only even numbers, so nothing passes, and mapping over nothing gives an empty list.

**Concept: `range(start, stop, step)`.** Stops before `stop`. Starting from an odd number with step −2 gives only odd numbers.

{{< /details >}}

### 3 · Q43, a mutable default argument

*Asked by: MathWorks (IIT Bombay 2024)*

```python
def foo(i, x=[]):
    x.append(x.append(i))
    return x
for i in range(3):
    y = foo(i)
print(y)
```

- **(a)** [[[0]], [[[0]], 1], ...]
- **(b)** [[0], [[0], 1], ...]
- **(c)** [0, None, 1, None, 2, None]
- **(d)** None of these

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) [0, None, 1, None, 2, None]**

**Why.** The default `x=[]` is created once and shared by every call. In each call, `x.append(i)` adds i and returns `None`; the outer `x.append(...)` then adds that `None`. After three calls: 0, None, 1, None, 2, None.

**Concept: mutable default arguments.** Default values are evaluated once, when the function is defined. A mutable default (list, dict) keeps changes between calls. Use `x=None` and create the list inside instead. Also, `list.append` returns `None`.

{{< /details >}}

### 4 · Q44, map

*Asked by: MathWorks (IIT Bombay 2024)*

With `def incr(x): return x + 1`, what is `map(incr, [0, 1, 2])`?

{{< details title="Answer and explanation" closed="true" >}}

**Answer: the values 1, 2, 3** (a lazy `map` object in Python 3; `list(...)` gives [1, 2, 3])

**Why.** `incr` adds 1 to each element.

**Concept: lazy iterators in Python 3.** `map`, `filter` and `zip` return iterators that compute on demand; printing them shows an object, not the values.

{{< /details >}}
