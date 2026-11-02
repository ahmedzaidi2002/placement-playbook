---
title: "Preprocessor and macros"
weight: 9
---

2 questions asked by MathWorks, Oracle. Try each one first, then open the toggle: it gives the answer, why it is right, and the idea behind it explained from scratch.

### 1 · Q31, macros

*Asked by: MathWorks (IISc 2024); MathWorks (NIT Durgapur 2024)*

```c
#define ADD(x) x + x
#define SUB(x) x - x
int main() {
    int y = ADD(3) / SUB(3);
    printf("%d", ADD(y));
}
```

- **(a)** 2
- **(b)** Divide by zero exception at runtime
- **(c)** 1
- **(d)** -2

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) 2**

**Why.** Macros are pasted as text. `ADD(3) / SUB(3)` becomes `3 + 3 / 3 - 3` = 3 + 1 − 3 = 1 (division first). So y = 1 and `ADD(y)` = y + y = 2. No division by zero happens.

**Concept: parenthesise macros.** `#define ADD(x) x + x` has no brackets, so surrounding operators split it. Safe form: `#define ADD(x) ((x) + (x))`.

{{< /details >}}

### 2 · MAX macro with side effects

*Asked by: Oracle (HackerRank MCQ test)*

What does this program print?

```c
#include <stdio.h>
#define MAX(a,b) ((a) > (b) ? (a) : (b))

int main() {
    int x = 5, y = 10;
    printf(" %d %d %d\n", MAX(x++, y++), x, y);
    return 0;
}
```

- **(a)** 11 6 12
- **(b)** 12 6 12
- **(c)** 11 7 12
- **(d)** 12 7 12

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) 11 6 12** (GCC; strictly undefined behaviour)

**Why.** The macro expands to `((x++) > (y++) ? (x++) : (y++))`. 5 > 10 is false (x becomes 6, y 11), so the third part runs: it yields 11 and makes y 12. x ends at 6, y at 12.

**Concept: macro arguments can be evaluated twice.** A macro copies its argument text everywhere it appears, so `x++` may run more than once. Use inline functions instead of macros for anything with side effects.

{{< /details >}}
