---
title: "Recursion, backtracking and divide and conquer"
weight: 8
---

2 questions asked by Sigmoid, Texas Instruments. Try each one first, then open the toggle: it gives the answer, why it is right, and the idea behind it explained from scratch.

### 1 · call stack with tail-call optimisation

*Asked by: Sigmoid (Campus hiring 2026)*

$f(n)$ returns the factorial of $n$ and is tail-recursive. If the compiler optimises tail
recursion, what is the maximum depth of the call stack at any time for $f(10)$?

- **(a)** 10
- **(b)** 11
- **(c)** 1
- **(d)** 2

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) 1**

**Why.** In a tail-recursive function the recursive call is the last thing done, so nothing in the current frame is needed afterwards. With tail-call optimisation the compiler reuses the same frame for each call, turning the recursion into a loop: one frame at any time.

**Concept: tail calls.** `return f(n − 1, acc * n);` is a tail call; `return n * f(n − 1);` is not (the multiplication happens after the call returns). C/C++ compilers often optimise tail calls at -O2; Python never does.

{{< /details >}}

### 2 · selling or splitting

*Asked by: Texas Instruments (BITS Pilani)*

A fruit worth $n$ can be sold for $n$ or split into $n/2$, $n/3$, $n/4$ (integer division),
recursively. Complete

```cpp
Solve(n) {
    if (n == 0)
        return 0;
    return X;
}
```

{{< details title="Answer and explanation" closed="true" >}}

**Answer: `max(n, Solve(n/2) + Solve(n/3) + Solve(n/4))`** (e.g. 12 gives 13); memoise it for large n

**Why.** At each value you choose the better of selling it now (n) or splitting and doing the best with each part. For 12: 12 vs 6 + 4 + 3 = 13, so 13.

**Concept: recursion with memoisation.** The same sub-values repeat (n/2/3 = n/3/2), so store results in a map to avoid recomputing. This is the "Bytelandian gold coins" problem.

{{< /details >}}
