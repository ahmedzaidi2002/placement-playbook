---
title: "Functions, recursion, scope and storage classes"
weight: 4
---

8 questions asked by MathWorks, Qualcomm, Texas Instruments. Try each one first, then open the toggle: it gives the answer, why it is right, and the idea behind it explained from scratch.

### 1 · Q13, the return type of main

*Asked by: MathWorks (IIIT Delhi 2024)*

In a C program, does `main()` need an explicit return type definition?

- **(a)** True
- **(b)** False

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) false** under C89 (implicit int); a strict C99 compiler requires `int main`.

**Why.** Old C (C89) assumed a missing return type was `int`, so `main()` alone compiled. C99 removed "implicit int"; modern compilers usually still accept it with a warning.

**Concept: implicit int.** In early C, any function declared without a return type returned int. Always write `int main(void)` today.

{{< /details >}}

### 2 · Q16, a static counter in a for loop

*Asked by: MathWorks (IIIT Delhi 2024)*

What is the sum of the values printed?

```c
int fun() { static int num = 15; return num--; }
int main() {
    for (fun(); fun(); fun())
        printf("%d", fun());
    return 0;
}
```

- **(a)** 99
- **(b)** 100
- **(c)** 101
- **(d)** It enters an infinite loop

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) it enters an infinite loop**

**Why.** `num` is static, so it keeps its value between calls, starting at 15 and dropping by 1 per call. Each iteration uses three calls: condition, body and increment. Init uses 15. Condition sees 14, body prints 13, increment uses 12; condition sees 11, ... The condition values are 14, 11, 8, 5, 2, −1, ... and never 0, so the loop never ends.

**Concept: static local variables.** A static local is created once and keeps its value across calls. Trace exactly which call (init, condition, body, update) gets which value.

{{< /details >}}

### 3 · Q15, a static counter

*Asked by: MathWorks (IIT Bombay 2024)*

```c
int value(int *x) {
    static int count;
    while (*x) { count = count + (*x & 1); *x >>= 1; }
    return count;
}
int main() {
    int a[] = {3, 5, 6, 4}; int y = 0, z = 0;
    for (; y < sizeof(a)/sizeof(int); y++) z = a[y] + value(&a[y]);
    printf("%d\n", z);
}
```

- **(a)** 10
- **(b)** 11
- **(c)** 12
- **(d)** 13

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) 11**

**Why.** `value` adds the number of 1 bits of `*x` to a static `count` (which keeps accumulating) and zeroes `*x`. Set bits: 3 → 2, 5 → 2, 6 → 2, 4 → 1. After the last call count = 7. In the last iteration z = a[3] + value(&a[3]) = 4 + 7 = 11 (with a[3] read before the call zeroes it; C leaves that order unspecified, and reading it after would give 7).

**Concept: static accumulators and popcount.** `count += x & 1; x >>= 1;` counts set bits. A static local accumulates across calls instead of restarting at 0.

{{< /details >}}

### 4 · Q2, automatically initialised to zero

*Asked by: MathWorks (IIITDM Kancheepuram 2025)*

If we declare a variable with which of the following keywords, its value will be
automatically initialised to 0?

- **(a)** auto
- **(b)** static
- **(c)** extern
- **(d)** register

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) static**

**Why.** Variables with static storage duration (static locals and globals) are zero-initialised before the program starts. `auto` and `register` locals contain garbage until assigned. `extern` only declares a variable defined elsewhere.

**Concept: storage classes.** auto: on the stack, uninitialised. register: a hint to keep it in a register, no address. static: one copy for the whole run, zero by default. extern: refers to a global defined in another file.

{{< /details >}}

### 5 · return value

*Asked by: Qualcomm (IISc)*

What will be the return value on calling `func(4, 3)`? (Options partly reconstructed.)

```c
#include <stdio.h>

int func(int x, int y)
{
    int count = 0;
    x = x + 1;
    if (x >= 0)
        return x + y;
    else
        return count;
}

int main(void)
{
    printf("%d\n", func(4, 3));
    return 0;
}
```

- **(a)** 0
- **(b)** 7
- **(c)** 8
- **(d)** 4

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) 8**

**Why.** x becomes 4 + 1 = 5. The test x ≥ 0 is true, so it returns 5 + 3 = 8.

**Concept: parameters are copies.** Changing x inside the function changes only its local copy. Trace the statements in order.

{{< /details >}}

### 6 · Q24, address of a register variable

*Asked by: Qualcomm (HirePro, Aug 2025)*

Which option is correct regarding the code snippet below?

```c
#include <stdio.h>
int main()
{
    register int number = 130;
    char *nu = (char*)&number;           //Line 1
    printf("%d ", ++*nu++);
    nu -= 1;
    nu--;
    printf("%d ", --*nu--);
    return 0;
}
```

- **(a)** Compile time error at //Line 1
- **(b)** 131 129
- **(c)** 132 130
- **(d)** 131 130

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) compile-time error at Line 1**

**Why.** C forbids taking the address of a `register` variable: `&number` is an error ("address of register variable requested"), because a register has no memory address.

**Concept: the `register` keyword.** It asks the compiler to keep a variable in a CPU register. Since registers have no address, `&` is not allowed on it in C. (C++ ignored this rule and removed `register` in C++17.)

{{< /details >}}

### 7 · C Programming

*Asked by: Qualcomm (60-question online assessment)*

A program defines a recursive function through a pointer-to-function. Only these pieces of the code were legible in the exam screenshot:

```c
int change(int (**)(int (**)(void)));    /* declaration, as transcribed */
ptr = change;                            /* function pointer */
printf("%d", (*ptr)(&ptr));

/* inside change(temp): */
static int m;
if (++m < 10) (**temp)(temp);
return m;
```

- **(a)** Garbage value
- **(b)** Compile time error
- **(c)** 10
- **(d)** 0

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) 10**

**Why.** `m` is static, so all recursive calls share one copy. Each call does `++m` and recurses while m < 10. When m reaches 10 the recursion stops, and every pending call returns the shared m, now 10. So printf prints 10.

**Concept: static variables in recursion.** A normal local gets a fresh copy per call; a static local is shared by all calls. So every level returns the final value, not the value it saw when it started.

{{< /details >}}

### 8 · a recursive power

*Asked by: Texas Instruments (IIT BHU 2023)*

```cpp
float WHATISIT(float x, int n) {
    if (n >= 1)
        return (n == 0) ? 1 : x * WHATISIT(x, n-1);
    else
        return (n == 0) ? 1 : (1/x) * WHATISIT(x, n+1);
}
```

Print `WHATISIT(2, 3)` and
`WHATISIT(0.5, -3)`.

- **(a)** 6, 1.5
- **(b)** 4, .25
- **(c)** 8, 8
- **(d)** Endless loop

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) 8, 8**

**Why.** For n ≥ 1 it returns x × WHATISIT(x, n − 1): 2 × 2 × 2 × 1 = 8. For n < 0 it multiplies by 1/x and moves n towards 0: (1/0.5)³ = 2³ = 8.

**Concept: recursive power.** xⁿ = x · xⁿ⁻¹ for n > 0, and xⁿ = (1/x) · xⁿ⁺¹ for n < 0, with x⁰ = 1. Note 0.5⁻³ = 2³.

{{< /details >}}
