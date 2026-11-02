@@ qc-iisc-lines
**Answer: (a) Line 3** (the first error; Lines 4 and 8 also fail)

**Why.** At file scope only declarations are allowed. `a = 30, 40;` is read as a declaration of `a` (old implicit int) and the `, 40` is a syntax error. Inside a declaration the comma separates declarators, so `int b = 1, 2;` and `int c = 3, 4;` fail the same way (`2` is not a name). Line 10, `d = 10, 20;`, is an ordinary expression statement: `(d = 10), 20`, which is legal (d = 10).

**Concept: comma as separator vs operator.** In a declaration (`int x = 1, y = 2;`) the comma separates variables. In an expression it is the comma operator. Precedence also matters: `=` binds tighter than `,`, so `d = 10, 20` assigns 10.

@@ qc25-array-lines
**Answer: the error is in `++*ar += 1;`**; if the labels are shifted by one line, as the options suggest, the intended answer is **(d) Line 1**.

**Why.** In C, `++*ar` produces a value, not an object you can assign to (it is not an lvalue), so `++*ar += 1` fails: "lvalue required as left operand of assignment". (In C++ pre-increment returns an lvalue and the line compiles.) The labelled lines are fine: `array[!1]` is `array[0]`.

**Concept: lvalues.** An lvalue names a storage location and may appear on the left of `=`. `x`, `*p`, `a[i]` are lvalues; `x + 1`, `++x` (in C) and function results are not.

@@ qc60-25
**Answer: (b) -2 -1**

**Why.** The chars are promoted to int. `-a / b` = −4 / 2 = −2. `-c % -b` = −1 % −2 = −1: in C the remainder takes the sign of the left operand.

**Concept: integer division and `%` in C.** Since C99, division truncates toward zero, and `a % b` has the same sign as a, so that (a / b) × b + a % b = a. Example: −7 / 2 = −3 and −7 % 2 = −1.

@@ qc60-27
**Answer: (d) 98 1 3** (chosen by the first value; the rest is undefined behaviour)

**Why.** `tr` starts at the 4th character of "Korea" (`e`). `++**r` changes that `e` to `f`... then in the first printf `*r--` yields `tr`, `++` moves it to the next character `a`, and the outer `++` turns `a` into `b`, ASCII 98. Only one option starts with 98. After `r--`, `r` no longer points at `tr`, so later values depend on stack layout.

**Concept: reading `++*++*r--`.** Unary operators apply right to left: first `r--` (use r, then move it), then `*` (get tr), then `++` (advance tr), then `*` (the character), then `++` (increment the character). Characters print as their ASCII codes with `%d`.

@@ qc60-35
**Answer: (c) 1 -11 1 -11**

**Why.**
- First call `func(10, 10)`: `~a++` = ~10 = −11 (non-zero), then `++b` = 11 (non-zero), so `&&` gives 1. The other argument `~b` is evaluated first by GCC (right to left), when b is still 10: −11. Prints `1 -11`.
- `func` returns a, now 11, so the `if` condition is true. Short-circuit `||` only skips evaluating `c != 1`; it does not skip the `if` body, so `func(b, c)` runs and prints `1 -11` again.

**Concept: bitwise NOT and short-circuit.** `~x` = −x − 1 in two's complement (~10 = −11). Short-circuiting skips the rest of a **condition**, never the statement the condition controls. (The source workbook's `1 -11` assumed the body was skipped; running the code shows the full output.)

@@ qc60-37
**Answer: (d) division by zero; make y non-zero**

**Why.** `x / y` with y = 0 is integer division by zero: undefined behaviour, usually a crash (SIGFPE). `%d` is the right format for an int.

**Concept: integer vs floating division by zero.** Integer division by zero is undefined (typically a hardware exception). Floating-point division by zero gives inf or NaN instead of crashing.

@@ qc60-38
**Answer: (a) 3 5 13**

**Why.**
- Line 3: `--*pa` makes a = 2; 2 + 5 = 7; `!7` = 0. The left side of `&&` is 0, so `++*pc` is never evaluated. `a += 0` leaves a = 2.
- Line 4: `++*pa` makes a = 3; `!3` = 0, so `||` evaluates `*pb++`: it reads b (5, true) and moves the pointer `pb`, not b. Result 1, so c = 12 + 1 = 13.

**Concept: `*p++` vs `(*p)++`.** Postfix `++` binds tighter than `*`, so `*pb++` means `*(pb++)`: read the value, then move the pointer. To increment the value write `(*pb)++`.

@@ qc60-39
**Answer: (d) POINTERERSTEW**

**Why.** c = {"ENTER", "NEW", "POINTER", "FIRST"}; cp = {c+3, c+2, c+1, c}; cpp = cp.
1. `**++cpp`: cpp → cp[1] = c+2 → "POINTER".
2. `*--*++cpp + 3`: cpp → cp[2] = c+1; `--` changes cp[2] to c; `*` gives "ENTER"; +3 → "ER".
3. `*cpp[-2] + 3`: cpp[-2] = cp[0] = c+3 → "FIRST" + 3 = "ST".
4. `cpp[-1][-1] + 1`: cpp[-1] = cp[1] = c+2; [-1] → c[1] = "NEW"; +1 → "EW".

**Concept: multi-level pointers.** Draw three columns (strings, `c`, `cp`) with arrows. Apply operators one at a time and remember that `--*...` changes an element of `cp` itself, which later steps see. `p[-1]` means `*(p - 1)`.

@@ qc60-43
**Answer: (d) Line 1**

**Why.** The semicolon after `while (*s);` makes the loop body empty. `*s` is 6 and never changes, so the program loops forever there. The braces below become a separate block that never runs.

**Concept: the stray semicolon.** `while (cond);` and `for (...);` and `if (cond);` all end at the semicolon. The block that follows is not part of them.

@@ qc60-45
**Answer: (d) infinite loop**

**Why.** `ptr` is never advanced inside the loop, so `*ptr` stays 'q' (113), and `1 < 113` is always true. It prints 'q' forever.

**Concept: loop progress.** A loop must change something its condition depends on. Here the fix is `printf("%c", *ptr++);`.

@@ qc60-49
**Answer: (b) 4**

**Why.** The expression is `(*a) + 1 − (*a) + 3`. The two `*a` terms cancel whatever value a[0] holds, leaving 4. (`*a` is a[0]; the array is uninitialised, but it cancels out.)

**Concept: precedence of unary `*`.** Unary `*` binds tighter than `+` and `−`, so `*a + 1` is `(a[0]) + 1`, not `*(a + 1)`.

@@ qc60-54
**Answer: (b) -2 -2, then 255 -1 0**

**Why.** Both arguments become plain `char` parameters holding the bits 0xFF, which (signed) is −1. So `a << 1` and `b << 1` both print −2. Back in main, `a` is `unsigned char` (255) and `b` is `signed char` (−1). `fun` has no `return`, so `c` is undefined; the key takes 0.

**Concept: the same bits, different types.** 0xFF is 255 as unsigned char and −1 as signed char. Values are promoted to int before shifting, so −1 << 1 = −2. Using the value of a function that falls off its end without `return` is undefined.

@@ qc60-56
**Answer: (b) "ed ple" then "4 4"**

**Why.** `*p` is "red", +1 skips a letter → "ed". `*q` is "apple", +2 → "ple". `sizeof(*p)` and `sizeof(q + 1)` are both the size of a pointer: 4 on the 32-bit target the question assumes (8 on 64-bit).

**Concept: `sizeof` a pointer vs an array.** `sizeof(array)` gives the whole array's size, but `*p` here is a `char*` and `q + 1` is a `char**`, both pointers. A string literal's length does not matter to `sizeof` of a pointer.

@@ ti-prep-2
**Answer: `reverse_sg` is used without being initialised.**

**Why.** It is a local (automatic) variable, so it starts with garbage, and `reverse_sg * 10 + ...` builds on that garbage. `length` is a global, which starts at 0 automatically, so it is fine.

**Concept: initialisation rules.** Globals and statics are zero-initialised; automatic locals are not. Always initialise accumulators (`int reverse_sg = 0;`).

@@ devrev-q2
**Answer: (a) HackerEarth**

**Why.** `fun` takes a pointer to a function returning int with unspecified parameters, which matches `main`. `fun(main)` prints "Hacker" (it never calls p), then `main` prints "Earth".

**Concept: function pointers.** A function's name used as a value decays to a pointer to it, like an array name. `int (*p)()` declares p as a pointer to a function returning int.

@@ mw-iiitd-14
**Answer: pointer size, then 1:** with the 16-bit sizes stated, **(d) 2 1** (on 32-bit systems 4 1, on 64-bit 8 1)

**Why.** `sizeof(a)` is the size of the pointer variable, never the 12 bytes it points to. `sizeof(*a)` is `sizeof(char)` = 1.

**Concept: `sizeof` is compile-time.** It looks only at the type. A pointer has no idea how much memory was allocated behind it; track that size yourself.

@@ mw-iiitd-19
**Answer: (c) deallocate the memory** (`free(p)` in main)

**Why.** The function returns heap memory correctly, but nobody frees it: a memory leak. (a) is unnecessary because a prototype already exists; (b) and (d) do not free anything. (Also add `#include <stdlib.h>` and use `int main`.)

**Concept: ownership of heap memory.** Whoever receives a malloc'd pointer must eventually `free` it exactly once. Returning heap memory is fine (unlike returning a local's address).

@@ mw-iisc-33
**Answer: (a) at least 12**

**Why.** The ANSI C (C89) standard's translation limits require compilers to support at least 12 pointer, array and function declarators modifying one type. Compilers may allow more.

**Concept: translation limits.** The C standard sets minimum capacities that every conforming compiler must support (nesting levels, identifier lengths, etc.), not maximums.

@@ mw-iisc-34
**Answer: (d) 8 5 4** (GCC; strictly undefined)

**Why.** GCC evaluates the arguments right to left here:
- `*++*++p1`: p1 → p+1; `++` makes p[1] point to a+2; read 4.
- `++*p2++`: p2 points to a+2; increment a[2] to 5 (that is the value printed), then move p2 to a+3.
- `*++p2`: p2 → a+4; read 8.
Printed in order: 8 5 4. (p2 is modified twice in one call, which is undefined; left-to-right would give 6 7 4.)

**Concept: pointer arrays.** `p[]` holds pointers into `a`; incrementing `*p1` changes one of those stored pointers, and incrementing `*p2` changes an element of `a`. Draw the arrays and update them step by step.

@@ mw-iitb-14
**Answer: (b) `int* const p;`**

**Why.** Read the declaration right to left: "p is a const pointer to int". The pointer can't be changed; the int it points to can. (a) and (c) are "pointer to const int"; (d) is a const pointer to const int.

**Concept: where `const` sits.** `const` applies to what is on its left (or, if nothing is on its left, to what is on its right). `const int *p` / `int const *p`: data is const. `int *const p`: pointer is const.

@@ mw-iitb-16
**Answer: (c) 1**

**Why.** k = old p, and p moves one int forward. p − k counts elements between them: 1 (not 4 bytes).

**Concept: pointer arithmetic is in elements.** `p + 1` moves by `sizeof(*p)` bytes, and `p − q` gives the number of elements between them.

@@ mw-iitb-17
**Answer: (c) runtime error** in practice (undefined behaviour)

**Why.** `a` is a local of `inc`; it stops existing when `inc` returns, so `val` points to dead stack memory. GCC warns and even returns a null pointer, which crashed when tested; other compilers may happen to print 11.

**Concept: never return the address of a local variable.** Locals live on the stack frame, which is reused after the function returns. Return the value itself, use a static, or allocate on the heap.

@@ mw-iitb-18
**Answer: `ck`**

**Why.** p = ptr. `**++p`: p moves to ptr+1. In the printf, `++p` moves to ptr+2 (which holds s+1); `--` changes ptr[2] to s; `*` gives s[0] = "black"; `+3` skips three letters → "ck".

**Concept: same as other multi-level pointer puzzles.** Apply the unary operators from the inside out and track which array element each step modifies.

@@ qc-iisc-sizeof
**Answer: (c) 48**

**Why.** `p` points to a whole `int[3][4]`, so `*p` is that 2-D array: 3 × 4 × 4 bytes = 48. `sizeof` does not evaluate its operand, so the malloc plays no part.

**Concept: pointer to an array.** `int (*p)[3][4]` (parentheses!) is one pointer to an entire 3×4 array. Without the parentheses, `int *p[3][4]` would be a 3×4 array of pointers.
