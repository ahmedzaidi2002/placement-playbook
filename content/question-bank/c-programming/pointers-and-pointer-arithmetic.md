---
title: "Pointers and pointer arithmetic"
weight: 1
---

20 questions asked by DevRev, MathWorks, Qualcomm, Texas Instruments. Try each one first, then open the toggle: it gives the answer, why it is right, and the idea behind it explained from scratch.

### 1 · Q2, passing main as a function pointer

*Asked by: DevRev (HackerEarth OA)*

What is the output of the following C code?

```c
#include <stdio.h>

void fun(int(*)());
int main()
{
    fun(main);
    printf("Earth\n");
    return 0;
}
void fun(int(*p)())
{
    printf("Hacker");}
```

- **(a)** HackerEarth
- **(b)** Earth
- **(c)** Hacker
- **(d)** Compilation error

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) HackerEarth**

**Why.** `fun` takes a pointer to a function returning int with unspecified parameters, which matches `main`. `fun(main)` prints "Hacker" (it never calls p), then `main` prints "Earth".

**Concept: function pointers.** A function's name used as a value decays to a pointer to it, like an array name. `int (*p)()` declares p as a pointer to a function returning int.

{{< /details >}}

### 2 · Q14, size of pointers

*Asked by: MathWorks (IIIT Delhi 2024); MathWorks (Recalled list)*

Given 1 char = 1 byte, 1 int = 2 bytes and 1 float = 4 bytes, what is the output?

```cpp
char *a = (char *)malloc(12);
printf("%d ", sizeof(a));
printf("%d\n", sizeof(*a));
```

- **(a)** 4 1
- **(b)** 12 1
- **(c)** 1 1
- **(d)** 2 1

{{< details title="Answer and explanation" closed="true" >}}

**Answer: pointer size, then 1:** with the 16-bit sizes stated, **(d) 2 1** (on 32-bit systems 4 1, on 64-bit 8 1)

**Why.** `sizeof(a)` is the size of the pointer variable, never the 12 bytes it points to. `sizeof(*a)` is `sizeof(char)` = 1.

**Concept: `sizeof` is compile-time.** It looks only at the type. A pointer has no idea how much memory was allocated behind it; track that size yourself.

{{< /details >}}

### 3 · Q19, correct the code snippet

*Asked by: MathWorks (IIIT Delhi 2024); MathWorks (NIT Delhi 2024); MathWorks (Recalled list)*

How can the issue in the following code be solved? Select all that apply.

```c
int* add_numbers(int, int);
void main() {
    int* p;
    p = add_numbers(1, 3);
}
int* add_numbers(int a, int b) {
    int* sum = (int*) malloc(16);
    *sum = a + b;
    return sum;
}
```

- **(a)** Defining the function add_numbers above main
- **(b)** By making the variable declaration inside the function static
- **(c)** By deallocating the allocated variable
- **(d)** By making the variable sum global

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) deallocate the memory** (`free(p)` in main)

**Why.** The function returns heap memory correctly, but nobody frees it: a memory leak. (a) is unnecessary because a prototype already exists; (b) and (d) do not free anything. (Also add `#include <stdlib.h>` and use `int main`.)

**Concept: ownership of heap memory.** Whoever receives a malloc'd pointer must eventually `free` it exactly once. Returning heap memory is fine (unlike returning a local's address).

{{< /details >}}

### 4 · Q33, levels of indirection

*Asked by: MathWorks (IISc 2024); MathWorks (IIT Bombay 2024)*

ANSI C allows how many levels of pointer indirection in a declaration?

- **(a)** at least 12
- **(b)** at most 12
- **(c)** at least 3
- **(d)** at most 3
- **(e)** exactly 3

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) at least 12**

**Why.** The ANSI C (C89) standard's translation limits require compilers to support at least 12 pointer, array and function declarators modifying one type. Compilers may allow more.

**Concept: translation limits.** The C standard sets minimum capacities that every conforming compiler must support (nesting levels, identifier lengths, etc.), not maximums.

{{< /details >}}

### 5 · Q34, pointers I

*Asked by: MathWorks (IISc 2024); MathWorks (IIT Bombay 2024); MathWorks (Recalled list)*

```c
int a[] = {1, 2, 4, 6, 8};
int *p[] = {a, a + 1, a + 2, a + 3, a + 4};
int **p1 = p;
int *p2 = *(p + 2);
printf("%u %u %u\n", *++p2, ++*p2++, *++*++p1);
```

- **(a)** 6 7 4
- **(b)** 9 7 3
- **(c)** 9 8 3
- **(d)** 8 5 4

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) 8 5 4** (GCC; strictly undefined)

**Why.** GCC evaluates the arguments right to left here:
- `*++*++p1`: p1 → p+1; `++` makes p[1] point to a+2; read 4.
- `++*p2++`: p2 points to a+2; increment a[2] to 5 (that is the value printed), then move p2 to a+3.
- `*++p2`: p2 → a+4; read 8.
Printed in order: 8 5 4. (p2 is modified twice in one call, which is undefined; left-to-right would give 6 7 4.)

**Concept: pointer arrays.** `p[]` holds pointers into `a`; incrementing `*p1` changes one of those stored pointers, and incrementing `*p2` changes an element of `a`. Draw the arrays and update them step by step.

{{< /details >}}

### 6 · Q14, a constant pointer

*Asked by: MathWorks (IIT Bombay 2024); MathWorks (Recalled list)*

Which declares a constant pointer to an `int`?

- **(a)** const int *p;
- **(b)** int* const p;
- **(c)** int const *p;
- **(d)** int const *const p;

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) `int* const p;`**

**Why.** Read the declaration right to left: "p is a const pointer to int". The pointer can't be changed; the int it points to can. (a) and (c) are "pointer to const int"; (d) is a const pointer to const int.

**Concept: where `const` sits.** `const` applies to what is on its left (or, if nothing is on its left, to what is on its right). `const int *p` / `int const *p`: data is const. `int *const p`: pointer is const.

{{< /details >}}

### 7 · Q16, pointer difference

*Asked by: MathWorks (IIT Bombay 2024); MathWorks (Recalled list)*

```cpp
int x = 4;
int *p = &x;
int *k = p++;
int r = p - k;
printf("%d", r);
```

- **(a)** 4
- **(b)** 2
- **(c)** 1
- **(d)** 5

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) 1**

**Why.** k = old p, and p moves one int forward. p − k counts elements between them: 1 (not 4 bytes).

**Concept: pointer arithmetic is in elements.** `p + 1` moves by `sizeof(*p)` bytes, and `p − q` gives the number of elements between them.

{{< /details >}}

### 8 · Q17, returning a local's address

*Asked by: MathWorks (IIT Bombay 2024); MathWorks (NIT Durgapur 2024); MathWorks (IIIT Delhi 2024)*

Will this print the incremented value of the local variable `a`?

```c
int* inc(int val) { int a = val; a++; return &a; }
int main(void) {
    int a = 10;
    int *val = inc(a);
    printf("\n Incremented value is equal to [%d] \n", *val);
    return 0;
}
```

- **(a)** YES
- **(b)** NO
- **(c)** Runtime error
- **(d)** Compiler error

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) runtime error** in practice (undefined behaviour)

**Why.** `a` is a local of `inc`; it stops existing when `inc` returns, so `val` points to dead stack memory. GCC warns and even returns a null pointer, which crashed when tested; other compilers may happen to print 11.

**Concept: never return the address of a local variable.** Locals live on the stack frame, which is reused after the function returns. Return the value itself, use a static, or allocate on the heap.

{{< /details >}}

### 9 · Q18, pointers II

*Asked by: MathWorks (IIT Bombay 2024)*

```c
char *s[] = {"black", "white", "yellow", "violet"};
char **ptr[] = {s + 3, s + 2, s + 1, s}, ***p;
p = ptr;
**++p;
printf("%s\n", *--*++p + 3);
```

{{< details title="Answer and explanation" closed="true" >}}

**Answer: `ck`**

**Why.** p = ptr. `**++p`: p moves to ptr+1. In the printf, `++p` moves to ptr+2 (which holds s+1); `--` changes ptr[2] to s; `*` gives s[0] = "black"; `+3` skips three letters → "ck".

**Concept: same as other multi-level pointer puzzles.** Apply the unary operators from the inside out and track which array element each step modifies.

{{< /details >}}

### 10 · pointer to a 2-D array

*Asked by: Qualcomm (IISc)*

What does this program print? (Options partly reconstructed: the photo shows 14, 48 and the
start of a fourth option.)

```c
#include <stdio.h>
#include <stdlib.h>
#define MAXROW 3
#define MAXCOL 4

int main(void)
{
    int (*p)[MAXROW][MAXCOL];
    p = (int (*)[MAXROW][MAXCOL]) malloc(sizeof(*p));
    printf("%d\n", (int) sizeof(*p));
    free(p);
    return 0;
}
```

- **(a)** 12
- **(b)** 14
- **(c)** 48
- **(d)** 4

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) 48**

**Why.** `p` points to a whole `int[3][4]`, so `*p` is that 2-D array: 3 × 4 × 4 bytes = 48. `sizeof` does not evaluate its operand, so the malloc plays no part.

**Concept: pointer to an array.** `int (*p)[3][4]` (parentheses!) is one pointer to an entire 3×4 array. Without the parentheses, `int *p[3][4]` would be a 3×4 array of pointers.

{{< /details >}}

### 11 · Q39, pointer walk with two loops

*Asked by: Qualcomm (IISc)*

What will be the output of the program below? (The options are [cut off in the source].)

```c
#include <stdio.h>

int main()
{
    int m[4] = {5, 2, 4, 0};
    int *p = m;
    int t = 0;
    int i = 1;
    while (t = *p++)
    {
        (i++ <= 4) ? printf("%d\n", t) : printf("error\n");
    }
    do
    {
        (i++ >= 4) ? printf("%d\n", t) : printf("%d\n", i);
    }
    while (t = *++p);
}
```

{{< details title="Answer and explanation" closed="true" >}}

**Answer: 5, 2, 4, 0, one number per line** (the final loop test reads past the array, which is undefined behaviour)

**Why.**
1. `while (t = *p++)` reads 5, 2, 4 (non-zero) with i = 1, 2, 3 ≤ 4, printing each. It then reads 0, the loop stops, and p is one past the 0 (at m[4]); i is 4.
2. The `do` body runs once with t = 0: i = 4 ≥ 4 is true, so it prints t = 0.
3. The test `t = *++p` reads m[5], beyond the array. GCC happened to read 0 and stop.

**Concept: assignment as a condition.** `while (t = *p++)` assigns, then tests the assigned value: it stops at the first 0. `*p++` reads the current element and then advances. A `do-while` always runs its body at least once.

{{< /details >}}

### 12 · Q25, four ways to read a

*Asked by: Qualcomm (Nov 2024)*

What will be the output of the program given below? (The rest of the question, "Consider the
address of ...", is [cut off in the source]; the options suggest the address of `a` is 1200.)

```c
#include <stdio.h>
int main()
{
    int *p;
    int a = 4;
    p = &a;
    printf("%d %d %d %d", a, *p, *(&a), *(*(&p)));
    return 0;
}
```

- **(a)** 4 4 4 4
- **(b)** 4 4 1200 4
- **(c)** Compile time error
- **(d)** 4 4 1200 1200

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) 4 4 4 4**

**Why.** `*p` is a (p = &a). `*(&a)` is a: "the thing at the address of a". `*(*(&p))`: `*(&p)` is p, and `*p` is a. Every expression is a, so no address is printed.

**Concept: `*` and `&` cancel.** `&x` gives the address of x; `*` follows an address. `*&x` is always x.

{{< /details >}}

### 13 · pre-increment through a pointer

*Asked by: Qualcomm (Nov 2024)*

What will be the output of the program given below?

```c
#include <stdio.h>
int main()
{
    int x = 5, *p;
    p = &x;
    printf("%d", ++*p);
    return 0;
}
```

- **(a)** compile time error
- **(b)** 6
- **(c)** Garbage value
- **(d)** 5

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) 6**

**Why.** `++*p` increments the value p points to (x goes from 5 to 6) and gives the new value.

**Concept: `++*p` vs `*p++`.** Both unary, right to left: `++*p` = `++(*p)` (increment the value); `*p++` = `*(p++)` (read, then move the pointer).

{{< /details >}}

### 14 · shifting a pointer

*Asked by: Qualcomm (Nov 2024)*

What will be the output of the program given below?

```c
#include <stdio.h>
int main(void)
{
    char arr[3] = {1, 2, 3};
    char *p = arr;
    p = p + 3;
    p = p << 1;
    *p = 4;
    printf("%d %d %d", arr[1], arr[2]);
    return 0;
}
```

- **(a)** 2 3
- **(b)** 4 3
- **(c)** 2 4
- **(d)** Compile time error

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) compile-time error**

**Why.** `p << 1` shifts a pointer, and C only allows shifts on integer types ("invalid operands to binary <<").

**Concept: allowed pointer arithmetic.** You may add or subtract an integer, subtract two pointers into the same array, and compare them. Multiplying, dividing or shifting a pointer is not allowed.

{{< /details >}}

### 15 · triple pointer to a local

*Asked by: Qualcomm (Nov 2024)*

What will be the output of the program given below? (Only the options 26 and 25 are visible;
the others are [cut off in the source].)

```c
#include <stdio.h>
int m = 25;

int main()
{
    int *q = &m;
    int ***f(int **);
    int ***p;
    p = f(&q);
    printf("%d", ***p);
    return 0;
}

int ***f(int **q)
{
    **q += **q;
    m += 1;
    return (&q);
}
```

- **(a)** 26
- **(b)** 25

{{< details title="Answer and explanation" closed="true" >}}

**Answer: undefined behaviour** (if that option is offered); by the intended logic m would be 51, not among the visible options.

**Why.** `f` returns `&q`, the address of its own parameter, which is destroyed when `f` returns. `***p` then dereferences a dangling pointer (the GCC build crashed). Intended logic: `**q += **q` doubles m to 50, `m += 1` makes it 51.

**Concept: parameters are locals too.** A function's parameters live in its stack frame; returning their address is as wrong as returning any local's address.

{{< /details >}}

### 16 · Q29, statements about pointers

*Asked by: Qualcomm (HirePro, Aug 2025)*

Choose the correct statement(s). I) The address stored in a pointer variable is always of
type integer. II) A pointer is a variable that stores the address of another variable.

- **(a)** Only (I)
- **(b)** Neither (I) nor (II)
- **(c)** Both (I) and (II)
- **(d)** Only (II)

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) only (II)**

**Why.** A pointer stores the address of another variable (II true). Its type is a pointer type (`int*`, `char*`), not an integer type; converting to an integer needs a cast or `uintptr_t` (I false).

**Concept: pointers have types.** The type tells the compiler how many bytes to read at that address and how far `p + 1` moves.

{{< /details >}}

### 17 · C Programming

*Asked by: Qualcomm (60-question online assessment)*

What is the output? (little-endian machine)

```c
static int s = 1234;
char *ptr = (char *)&s;
printf("%d ", ++*ptr++);
*ptr = 5;
printf(" %d ", --*ptr--);
*ptr++;
printf("%d ", *ptr++ + s);
printf(" %d ", s++);
```

- **(a)** `-34 6 1134 1240`
- **(b)** `-42 5 1120 1220`
- **(c)** `-45 4 1239 1235`
- **(d)** `-48 3 1112 1320`

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) -45 4 1239 1235**

**Why.** 1234 = 0x04D2. On a little-endian machine byte 0 is 0xD2 (−46 as a signed char) and byte 1 is 0x04.
1. `++*ptr++`: byte 0 becomes −45 (s becomes 1235), print −45, ptr moves to byte 1.
2. `*ptr = 5`, then `--*ptr--`: byte 1 becomes 4, print 4, ptr moves back to byte 0. (s is now 0x04D3 = 1235.)
3. `*ptr++;` just moves ptr to byte 1.
4. `*ptr++ + s` = 4 + 1235 = 1239.
5. `s++` prints the old value 1235.

**Concept: endianness.** Little-endian stores the least significant byte first, at the lowest address. A `char*` into an int lets you edit single bytes; changing the low byte changes the int by the same amount (0xD2 → 0xD3 adds 1).

{{< /details >}}

### 18 · function pointers

*Asked by: Texas Instruments (IISc 2023)*

Replace XXX so that `(*fun_ptr)(10);` calls `void fun(int)`: (1)
`void (*fun_ptr)(int) = &fun;` (2)

```cpp
void (*fun_ptr)(int);
fun_ptr = &fun;
```

{{< details title="Answer and explanation" closed="true" >}}

**Answer: both work**

**Why.** (1) declares a function pointer and initialises it with `&fun`; (2) declares it, then assigns. Either way `(*fun_ptr)(10)` calls `fun(10)`.

**Concept: function pointer syntax.** `void (*fp)(int)` = "fp is a pointer to a function taking int and returning void". `&fun` and plain `fun` both give the function's address; `fp(10)` and `(*fp)(10)` both call it.

{{< /details >}}

### 19 · a generic search

*Asked by: Texas Instruments (IISc 2023)*

A search with a `compare(void*, void*)` callback looks for 7 in `{2, 5, 7, 90, 70}`.

{{< details title="Answer and explanation" closed="true" >}}

**Answer: "The index is 2"**

**Why.** 7 is at position 2 (0-based) in {2, 5, 7, 90, 70}. The `compare(void*, void*)` callback lets the same search code work for any type: it casts the pointers to `int*` and compares the values.

**Concept: generic code with `void*`.** C has no templates, so library functions like `qsort` and `bsearch` take `void*` data plus a comparison callback that knows the real type.

{{< /details >}}

### 20 · filling an array through a pointer

*Asked by: Texas Instruments (BITS Pilani)*

```cpp
p = numbers;
*p = 10;
p++;
*p = 20;
p = &numbers[2];
*p = 30;
p = numbers + 3;
*p = 40;
p = numbers;
*(p + 4) = 50;
```

Then print each element of `numbers` followed by a comma.

{{< details title="Answer and explanation" closed="true" >}}

**Answer: 10,20,30,40,50,**

**Why.** Each step writes through p to a different element: numbers[0] = 10, [1] = 20, [2] = 30, [3] = 40, [4] = 50.

**Concept: equivalent ways to reach an element.** `p++` then `*p`, `&numbers[2]`, `numbers + 3`, and `*(p + 4)` all address array elements; `numbers + k` and `&numbers[k]` are the same address.

{{< /details >}}
