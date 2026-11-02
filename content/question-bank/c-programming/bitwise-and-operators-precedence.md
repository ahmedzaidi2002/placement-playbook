---
title: "Bitwise and operators, precedence"
weight: 3
---

12 questions asked by MathWorks, Protium Finance, Qualcomm. Try each one first, then open the toggle: it gives the answer, why it is right, and the idea behind it explained from scratch.

### 1 · Q17, sizeof a character constant

*Asked by: MathWorks (IIIT Delhi 2024)*

`printf("%d\ n", sizeof('P'));` in C prints:

- **(a)** 1
- **(b)** 4
- **(c)** 2
- **(d)** Varies with compiler

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) 4** (on today's compilers)

**Why.** In C, a character constant like `'P'` has type `int`, so `sizeof('P')` is `sizeof(int)`, 4 on 32/64-bit compilers (2 on old 16-bit ones). In C++ it has type `char` and the answer is 1.

**Concept: character constants in C vs C++.** C treats `'A'` as an int with value 65. C++ changed it to `char` so overloads like `f(char)` work. Many "C trick" MCQs rely on this difference.

{{< /details >}}

### 2 · Q29, post-increment

*Asked by: MathWorks (IISc 2024)*

```cpp
int x = 10, b = 5;
b = b + x++;
printf("%d %d %d", x++, b, x);
```

What does the program print?

{{< details title="Answer and explanation" closed="true" >}}

**Answer: 11 15 12** (with GCC; strictly undefined behaviour)

**Why.** `b = b + x++` uses x = 10, so b = 15, then x becomes 11. In `printf("%d %d %d", x++, b, x)`, `x++` and `x` are evaluated without a defined order. GCC (tested) computes `x++` first, which yields 11 and makes x 12, and reads the plain `x` afterwards as 12, printing 11 15 12.

**Concept: unsequenced side effects.** C does not fix the order in which function arguments are evaluated. Reading and modifying the same variable in two arguments of one call is undefined behaviour; the printed result depends on the compiler. In an exam, give the common GCC output but know it is not guaranteed.

{{< /details >}}

### 3 · Q30, i++ + ++i

*Asked by: MathWorks (IISc 2024); MathWorks (NIT Durgapur 2024)*

```cpp
int i = 5, j = 12;
j = i++ + ++i;
printf("%d %d", i, j);
```

- **(a)** 12 12
- **(b)** 7 12
- **(c)** 12 14
- **(d)** 7 14

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) 7 12** (GCC; strictly undefined behaviour)

**Why.** The usual evaluation: `i++` gives 5 (i becomes 6), `++i` makes i 7 and gives 7, so j = 5 + 7 = 12 and i = 7.

**Concept: modifying a variable twice in one expression is undefined.** Between two "sequence points" a variable may be modified at most once. `i++ + ++i` breaks that rule, so the C standard allows any result. Compilers usually give the answer above.

{{< /details >}}

### 4 · Q13, parity without the modulo operator

*Asked by: MathWorks (IIT Bombay 2024)*

To test even or odd without `%`, use:

- **(a)** addition and subtraction
- **(b)** multiplication and division
- **(c)** bitwise operators
- **(d)** bit fields

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) bitwise operators**

**Why.** `n & 1` keeps only the lowest bit: 1 for odd numbers, 0 for even.

**Concept: the lowest bit decides parity.** In binary, every place except the last is worth an even number (2, 4, 8, ...), so a number is odd exactly when its last bit is 1.

{{< /details >}}

### 5 · Q26, char overflow

*Asked by: MathWorks (IIT Bombay 2024)*

```cpp
char c = 128;
printf("%d %d\n", c, (unsigned char)c);
```

(options not photographed)

{{< details title="Answer and explanation" closed="true" >}}

**Answer: -128 128** (where `char` is signed, as on x86)

**Why.** A signed 8-bit `char` holds −128..127. 128 does not fit and wraps to −128 (implementation-defined). Printed with `%d` it is −128. Cast to `unsigned char`, the same bits 1000 0000 read as 128. Where plain `char` is unsigned (e.g. ARM Linux), both print 128.

**Concept: two's complement and signedness.** The same 8 bits mean different numbers depending on the type: 1000 0000 is 128 unsigned and −128 signed. Whether plain `char` is signed is up to the platform.

{{< /details >}}

### 6 · Q28, x++ + ++x + x++

*Asked by: MathWorks (IIT Bombay 2024)*

```cpp
int x = 5;
int y = (x++) + (++x) + (x++);
```

The value of `y` is:

- **(a)** 17
- **(b)** 16
- **(c)** 15
- **(d)** Depends on the compiler

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) depends on the compiler** (undefined behaviour)

**Why.** `x` is modified three times in one expression without a sequence point, so the C standard does not define the result.

**Concept: undefined behaviour.** When code breaks the sequencing rules, the compiler may produce any result (or optimise strangely). Write `x++` as a separate statement if you need a defined order.

{{< /details >}}

### 7 · Q17, operator sequence II

*Asked by: MathWorks (NIT Durgapur 2024)*

```cpp
int i = 6;
printf("%d %d %d %d %d\n", !i, ++i, i + 3, i--, i++);
```

- **(a)** 0 7 10 7 6
- **(b)** 1 7 10 7 6
- **(c)** 0 7 9 7 6
- **(d)** None of these

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) 0 7 9 7 6** (GCC; strictly undefined)

**Why.** GCC evaluates printf's arguments right to left here: `i++` gives 6 (i = 7), `i--` gives 7 (i = 6), `i + 3` = 9, `++i` gives 7, `!i` = 0 (i is non-zero). Printed in the written order: 0 7 9 7 6.

**Concept: argument evaluation order is unspecified.** Modifying `i` in several arguments of one call is undefined. MCQs expecting a single answer assume right-to-left evaluation, the common GCC/x86 behaviour.

{{< /details >}}

### 8 · Q12, n AND (n - 1)

*Asked by: MathWorks (NIT Delhi 2024)*

If `n & (n - 1) == 0`, what can you say about the integer $n$?

- **(a)** n is even
- **(b)** n is a power of 2
- **(c)** n is odd
- **(d)** n is not a power of 2

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) n is a power of 2**

**Why.** Subtracting 1 flips the lowest set bit of n to 0 and all bits below it to 1. ANDing with n clears that lowest set bit. The result is 0 only if n had a single set bit, i.e. n is a power of 2 (or n = 0). Example: 8 = 1000, 7 = 0111, 8 & 7 = 0.

**Concept: `n & (n − 1)` removes the lowest set bit.** It is used to test powers of two and to count set bits (repeat until zero). Note: in C, `==` binds tighter than `&`, so the test must be written `(n & (n - 1)) == 0`.

{{< /details >}}

### 9 · comma operator in an if

*Asked by: Protium Finance (OA 2025)*

Predict the output of the C program.

```c
#include<stdio.h>
int main(){
    int i = 5;
    if(i == 3, 4)
        printf("Atom Bomb");
    else
        printf("Hydrogen Bomb");
    return 0;
}
```

- **(a)** Hydrogen Bomb
- **(b)** Atom Bomb
- **(c)** Compilation error
- **(d)** Runtime error

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) Atom Bomb**

**Why.** `i == 3, 4` is a comma expression: `i == 3` is evaluated and thrown away, and the whole condition has the value of the last part, 4, which is non-zero (true). So the `if` branch runs.

**Concept: the comma operator.** `(a, b)` evaluates a, then b, and its value is b. It has the lowest precedence of all operators. Compilers warn that the left side has no effect.

{{< /details >}}

### 10 · unsigned char loop

*Asked by: Protium Finance (OA 2025)*

Predict the output of the C program.

```c
#include<stdio.h>
int main()
{
    unsigned char hi = 0;
    for(;hi<=0;hi++) ;
    printf("%d\n",hi);
    return 0;
}
```

- **(a)** 0
- **(b)** 1
- **(c)** 2
- **(d)** Compilation error

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) 1**

**Why.** The empty loop runs while `hi <= 0`. For an unsigned value that means `hi == 0`. After one increment hi is 1, the condition fails, and 1 is printed.

**Concept: unsigned comparisons.** An unsigned value is never negative, so `<= 0` is the same as `== 0`. Wrap-around (255 → 0) would only matter if the loop kept going up to 255.

{{< /details >}}

### 11 · short-circuit with

*Asked by: Qualcomm (Nov 2024)*

What will be the output of the program given below?

```c
#include <stdio.h>
int main(void)
{
    char a = 1;
    char b = -1;
    printf("%d %d ", ~++a || b, a || ~b-- && ~++b);
    printf("%d %d", a, b);
    return 0;
}
```

- **(a)** Compile time error
- **(b)** 1 0 3 1
- **(c)** 1 1 2 -1
- **(d)** 1 0 2 -1

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) 1 1 2 -1**

**Why.**
- `~++a || b`: a becomes 2; ~2 = −3, non-zero, so the `||` is true (1) and `b` is not evaluated.
- `a || ~b-- && ~++b`: a is non-zero, so the whole right side, with its `b--` and `++b`, is skipped: 1.
- Then a = 2 and b is still −1.

**Concept: short-circuit evaluation.** `||` stops as soon as the left side is true; `&&` stops as soon as the left side is false. Side effects (`++`, `--`) in the skipped part never happen. Also `&&` binds tighter than `||`, so `a || (x && y)`.

{{< /details >}}

### 12 · XOR in a condition

*Asked by: Qualcomm (Nov 2024)*

What will be the output of the program given below?

```c
#include <stdio.h>
int main()
{
    int a = 4;
    if (a ^ a && (a ^ a) || a)
        printf("%d", a);
    return 0;
}
```

- **(a)** 5
- **(b)** 4
- **(c)** 7
- **(d)** 6

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) 4**

**Why.** `a ^ a` is 0 (any value XOR itself is 0). `0 && ...` is 0. Then `0 || a` is true because a = 4. So `printf` prints a, still 4.

**Concept: XOR identities and precedence.** x ^ x = 0, x ^ 0 = x. Precedence: `^` binds tighter than `&&`, which binds tighter than `||`, so the condition is `((a ^ a) && (a ^ a)) || a`.

{{< /details >}}
