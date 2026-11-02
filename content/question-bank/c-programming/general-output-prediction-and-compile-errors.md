---
title: "General output prediction and compile errors"
weight: 2
---

14 questions asked by Qualcomm, Texas Instruments. Try each one first, then open the toggle: it gives the answer, why it is right, and the idea behind it explained from scratch.

### 1 · Q34, compile-time error

*Asked by: Qualcomm (IISc)*

Which of the line numbers in the program below will give a compile-time error?

```c
#include <stdio.h>
int a;
a = 30, 40;      // Line 3
int b = 1, 2;    // Line 4

int main(void)
{
    int c = 3, 4;    // Line 8
    int d;
    d = 10, 20;      // Line 10
    printf("%d %d %d %d", a, b, c, d);
    return 0;
}
```

- **(a)** Line 3
- **(b)** Line 4
- **(c)** Line 8
- **(d)** No error

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) Line 3** (the first error; Lines 4 and 8 also fail)

**Why.** At file scope only declarations are allowed. `a = 30, 40;` is read as a declaration of `a` (old implicit int) and the `, 40` is a syntax error. Inside a declaration the comma separates declarators, so `int b = 1, 2;` and `int c = 3, 4;` fail the same way (`2` is not a name). Line 10, `d = 10, 20;`, is an ordinary expression statement: `(d = 10), 20`, which is legal (d = 10).

**Concept: comma as separator vs operator.** In a declaration (`int x = 1, y = 2;`) the comma separates variables. In an expression it is the comma operator. Precedence also matters: `=` binds tighter than `,`, so `d = 10, 20` assigns 10.

{{< /details >}}

### 2 · Q26, which line has an error

*Asked by: Qualcomm (HirePro, Aug 2025)*

Which of the line(s) generates error(s) in the program below?

```c
#include <stdio.h>
int main()
{
    int array[] = {2, 4, 6, 8, 5, 7};
    int *ar = array + 3;
    ++*ar += 1;
    printf("%d ", --(array[1 + 3]));     //Line 1
    printf("%d", (array[!1]) + 2);       //Line 2
    return 0;                            //Line 3
}
```

- **(a)** No error in the program
- **(b)** Line 1, Line 2 and Line 3
- **(c)** Line 2 and Line 3
- **(d)** Line 1

{{< details title="Answer and explanation" closed="true" >}}

**Answer: the error is in `++*ar += 1;`**; if the labels are shifted by one line, as the options suggest, the intended answer is **(d) Line 1**.

**Why.** In C, `++*ar` produces a value, not an object you can assign to (it is not an lvalue), so `++*ar += 1` fails: "lvalue required as left operand of assignment". (In C++ pre-increment returns an lvalue and the line compiles.) The labelled lines are fine: `array[!1]` is `array[0]`.

**Concept: lvalues.** An lvalue names a storage location and may appear on the left of `=`. `x`, `*p`, `a[i]` are lvalues; `x + 1`, `++x` (in C) and function results are not.

{{< /details >}}

### 3 · C Programming

*Asked by: Qualcomm (60-question online assessment)*

What is the output?

```c
char a = 4; char b = 2; char c = 1;
printf("%d ", -a / b);
printf("%d ", -c % -b);
```

- **(a)** `2 1`
- **(b)** `-2 -1`
- **(c)** `2 -1`
- **(d)** `-2 1`

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) -2 -1**

**Why.** The chars are promoted to int. `-a / b` = −4 / 2 = −2. `-c % -b` = −1 % −2 = −1: in C the remainder takes the sign of the left operand.

**Concept: integer division and `%` in C.** Since C99, division truncates toward zero, and `a % b` has the same sign as a, so that (a / b) × b + a % b = a. Example: −7 / 2 = −3 and −7 % 2 = −1.

{{< /details >}}

### 4 · C Programming

*Asked by: Qualcomm (60-question online assessment)*

What is the output?

```c
char tri[][10] = {"Korea", "Japan", "Australia"};
char *tr = (char *)tri + 3;
char **r = &tr;
++**r;
printf("%d ", ++*++*r--);
++*tr++;
*tr = 3 - 1;
printf("%d ", ++*--*r++);
printf("%d", ++*tr--);
```

- **(a)** `Compile time error`
- **(b)** `69 1 1`
- **(c)** `101 2 3`
- **(d)** `98 1 3`

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) 98 1 3** (chosen by the first value; the rest is undefined behaviour)

**Why.** `tr` starts at the 4th character of "Korea" (`e`). `++**r` changes that `e` to `f`... then in the first printf `*r--` yields `tr`, `++` moves it to the next character `a`, and the outer `++` turns `a` into `b`, ASCII 98. Only one option starts with 98. After `r--`, `r` no longer points at `tr`, so later values depend on stack layout.

**Concept: reading `++*++*r--`.** Unary operators apply right to left: first `r--` (use r, then move it), then `*` (get tr), then `++` (advance tr), then `*` (the character), then `++` (increment the character). Characters print as their ASCII codes with `%d`.

{{< /details >}}

### 5 · C Programming

*Asked by: Qualcomm (60-question online assessment)*

What is the output?

```c
int func(char a, char b) {
    printf("%d %d ", ~a++ && ++b, ~b);
    return a;
}
int main() {
    int a = 10;
    char b = 0xa;
    float c = 10.0;
    if (func(a, b) || c != 1)
        func(b, c);
}
```

- **(a)** `1 -11`
- **(b)** `1 0 1 0`
- **(c)** `1 -11 1 -11`
- **(d)** `Compile time error`

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) 1 -11 1 -11**

**Why.**
- First call `func(10, 10)`: `~a++` = ~10 = −11 (non-zero), then `++b` = 11 (non-zero), so `&&` gives 1. The other argument `~b` is evaluated first by GCC (right to left), when b is still 10: −11. Prints `1 -11`.
- `func` returns a, now 11, so the `if` condition is true. Short-circuit `||` only skips evaluating `c != 1`; it does not skip the `if` body, so `func(b, c)` runs and prints `1 -11` again.

**Concept: bitwise NOT and short-circuit.** `~x` = −x − 1 in two's complement (~10 = −11). Short-circuiting skips the rest of a **condition**, never the statement the condition controls. (The source workbook's `1 -11` assumed the body was skipped; running the code shows the full output.)

{{< /details >}}

### 6 · Error Finding

*Asked by: Qualcomm (60-question online assessment)*

Identify the error (if any) and how it can be fixed.

```c
int x = 5;
int y = 0;
int z = x / y;
printf("The result is: %d\n", z);
```

- **(a)** %d is wrong; Fix: Replace it with '-d'
- **(b)** No Error
- **(c)** Incorrect format specifier; Fix: Change '%d' to '%f' in the printf statement
- **(d)** Division by zero; Fix: Change the value of y to a non-zero value

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) division by zero; make y non-zero**

**Why.** `x / y` with y = 0 is integer division by zero: undefined behaviour, usually a crash (SIGFPE). `%d` is the right format for an int.

**Concept: integer vs floating division by zero.** Integer division by zero is undefined (typically a hardware exception). Floating-point division by zero gives inf or NaN instead of crashing.

{{< /details >}}

### 7 · C Programming

*Asked by: Qualcomm (60-question online assessment)*

What is the output?

```c
int a = 3, b = 5, c = 12;
int *pa = &a, *pb = &b, *pc = &c;
a += !(--*pa + *pb) && ++*pc;
*pc += (!++*pa) || *pb++;
printf("%d %d %d", a, b, c);
```

- **(a)** `3 5 13`
- **(b)** `3 5 14`
- **(c)** `2 5 19`
- **(d)** `4 5 14`

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) 3 5 13**

**Why.**
- Line 3: `--*pa` makes a = 2; 2 + 5 = 7; `!7` = 0. The left side of `&&` is 0, so `++*pc` is never evaluated. `a += 0` leaves a = 2.
- Line 4: `++*pa` makes a = 3; `!3` = 0, so `||` evaluates `*pb++`: it reads b (5, true) and moves the pointer `pb`, not b. Result 1, so c = 12 + 1 = 13.

**Concept: `*p++` vs `(*p)++`.** Postfix `++` binds tighter than `*`, so `*pb++` means `*(pb++)`: read the value, then move the pointer. To increment the value write `(*pb)++`.

{{< /details >}}

### 8 · C Programming

*Asked by: Qualcomm (60-question online assessment)*

What is the output?

```c
char *c[]  = {"ENTER", "NEW", "POINTER", "FIRST"};
char **cp[] = {c+3, c+2, c+1, c};
char ***cpp = cp;
printf("%s", **++cpp);
printf("%s", *--*++cpp + 3);
printf("%s", *cpp[-2] + 3);
printf("%s", cpp[-1][-1] + 1);
```

- **(a)** `POINTERFIRST`
- **(b)** `POINTNEWENTR`
- **(c)** `POINTERENSTEN`
- **(d)** `POINTERERSTEW`

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) POINTERERSTEW**

**Why.** c = {"ENTER", "NEW", "POINTER", "FIRST"}; cp = {c+3, c+2, c+1, c}; cpp = cp.
1. `**++cpp`: cpp → cp[1] = c+2 → "POINTER".
2. `*--*++cpp + 3`: cpp → cp[2] = c+1; `--` changes cp[2] to c; `*` gives "ENTER"; +3 → "ER".
3. `*cpp[-2] + 3`: cpp[-2] = cp[0] = c+3 → "FIRST" + 3 = "ST".
4. `cpp[-1][-1] + 1`: cpp[-1] = cp[1] = c+2; [-1] → c[1] = "NEW"; +1 → "EW".

**Concept: multi-level pointers.** Draw three columns (strings, `c`, `cp`) with arrows. Apply operators one at a time and remember that `--*...` changes an element of `cp` itself, which later steps see. `p[-1]` means `*(p - 1)`.

{{< /details >}}

### 9 · C Programming

*Asked by: Qualcomm (60-question online assessment)*

Point out the error, if any.

```c
int c = 6;
int *s = &c;
while (*s);           // Line 1
{
    *s += c - 1;      // Line 2
    printf("%d ", ++*s--);
}
```

- **(a)** No error in the program
- **(b)** Line 2
- **(c)** Both Line 1 and Line 2
- **(d)** Line 1

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) Line 1**

**Why.** The semicolon after `while (*s);` makes the loop body empty. `*s` is 6 and never changes, so the program loops forever there. The braces below become a separate block that never runs.

**Concept: the stray semicolon.** `while (cond);` and `for (...);` and `if (cond);` all end at the semicolon. The block that follows is not part of them.

{{< /details >}}

### 10 · C Programming

*Asked by: Qualcomm (60-question online assessment)*

Which option is correct about this code snippet?

```c
char *ptr = "aquarious";
int i;
ptr += 1;
while (1 < *ptr) {
    printf("%c", *ptr);
}
```

- **(a)** `Compile time error`
- **(b)** `q`
- **(c)** `quarious`
- **(d)** `Infinite loop`

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) infinite loop**

**Why.** `ptr` is never advanced inside the loop, so `*ptr` stays 'q' (113), and `1 < 113` is always true. It prints 'q' forever.

**Concept: loop progress.** A loop must change something its condition depends on. Here the fix is `printf("%c", *ptr++);`.

{{< /details >}}

### 11 · C Programming

*Asked by: Qualcomm (60-question online assessment)*

What is the output?

```c
int a[10];
printf("%d", *a + 1 - *a + 3);
```

- **(a)** `Compile time error`
- **(b)** `4`
- **(c)** `2`
- **(d)** `3`

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) 4**

**Why.** The expression is `(*a) + 1 − (*a) + 3`. The two `*a` terms cancel whatever value a[0] holds, leaving 4. (`*a` is a[0]; the array is uninitialised, but it cancels out.)

**Concept: precedence of unary `*`.** Unary `*` binds tighter than `+` and `−`, so `*a + 1` is `(a[0]) + 1`, not `*(a + 1)`.

{{< /details >}}

### 12 · C Programming

*Asked by: Qualcomm (60-question online assessment)*

What is the output?

```c
const unsigned char a = 255;
const signed char b = 255;
int c;
c = fun(a, b);
printf("\n%d %d %d", a, b, c);

int fun(char a, char b) {
    printf("%d ", a << 1);
    printf("%d ", b << 1);
}
```

- **(a)** `-2 -2 / 255 -1 4`
- **(b)** `-2 -2 / 255 -1 0`
- **(c)** `-1 -1 / 255 -1 0`
- **(d)** `Compile time error`

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) -2 -2, then 255 -1 0**

**Why.** Both arguments become plain `char` parameters holding the bits 0xFF, which (signed) is −1. So `a << 1` and `b << 1` both print −2. Back in main, `a` is `unsigned char` (255) and `b` is `signed char` (−1). `fun` has no `return`, so `c` is undefined; the key takes 0.

**Concept: the same bits, different types.** 0xFF is 255 as unsigned char and −1 as signed char. Values are promoted to int before shifting, so −1 << 1 = −2. Using the value of a function that falls off its end without `return` is undefined.

{{< /details >}}

### 13 · C Programming

*Asked by: Qualcomm (60-question online assessment)*

What is the output?

```c
char ch[] = "red";
char *p[3] = {"red", "white", "pink"};
char *q[3] = {"apple", "banana", "orange"};
printf("%s %s\n", *p + 1, *q + 2);
printf("%d %d ", sizeof(*p), sizeof(q + 1));
```

- **(a)** `Compile time error`
- **(b)** `ed ple / 4 4`
- **(c)** `e p / 9 9`
- **(d)** `White banana / 9 9`

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) "ed ple" then "4 4"**

**Why.** `*p` is "red", +1 skips a letter → "ed". `*q` is "apple", +2 → "ple". `sizeof(*p)` and `sizeof(q + 1)` are both the size of a pointer: 4 on the 32-bit target the question assumes (8 on 64-bit).

**Concept: `sizeof` a pointer vs an array.** `sizeof(array)` gives the whole array's size, but `*p` here is a `char*` and `q + 1` is a `char**`, both pointers. A string literal's length does not matter to `sizeof` of a pointer.

{{< /details >}}

### 14 · find the bug

*Asked by: Texas Instruments (TI prep guide)*

```cpp
int length;
void foo(int sg) {
    int reverse_sg;
    while (sg > 0) {
        length = length + 1;
        reverse_sg = reverse_sg * 10 + (sg % 10);
        sg = sg / 10;
    }
}
```

{{< details title="Answer and explanation" closed="true" >}}

**Answer: `reverse_sg` is used without being initialised.**

**Why.** It is a local (automatic) variable, so it starts with garbage, and `reverse_sg * 10 + ...` builds on that garbage. `length` is a global, which starts at 0 automatically, so it is fine.

**Concept: initialisation rules.** Globals and statics are zero-initialised; automatic locals are not. Always initialise accumulators (`int reverse_sg = 0;`).

{{< /details >}}
