---
title: 3 · Programming basics (Q21–Q40)
weight: 3
---

Twenty questions on number systems, logic gates, C output tracing, scheduling, linked lists, searching and error spotting. Open the toggle after you have traced the code yourself.

### Q21 · Computer Architecture

What will be the conversion result of the given number in hexadecimal format? 101110101

**Options**

- **A.** `17F`
- **B.** `175`
- **C.** `77F`
- **D.** `17E`

{{< details title="Show answer and explanation" closed="true" >}}

**Answer: B.** `175`

Group in 4s from the right: 1 | 0111 | 0101 → 1, 7, 5 → 175 hex.

{{< /details >}}

### Q22 · OS Fundamentals

A buddy-system allocator manages **8 MB** of memory. Requests arrive in this order:

- P2 requests 99K
- P4 requests 119K
- P1 requests 201K
- P5 requests 91K
- P1 releases
- P3 requests 55K
- P2 releases

What is the internal fragmentation when process P1 releases its memory?

**Options**

- **A.** 136K
- **B.** 135K
- **C.** 335K
- **D.** 29K

{{< details title="Show answer and explanation" closed="true" >}}

**No reliable answer.** This question is flagged: it looks flawed or its key could not be derived, so no option is picked here.

Blocks at P1's release: P2 99→128 (29K waste), P4 119→128 (9K), P1 201→256 (55K), P5 91→128 (37K). Total = 130K; after P1 leaves = 75K. Neither matches an option, so the intended figure could not be derived. Nearest listed option is 136K.

On the 75K left after P1 leaves, nothing matches an option. If you must guess, the workbook's nearest listed option is **A. 136K**.

{{< /details >}}

### Q23 · Computer Architecture

Which one of the given logic gates has the output as 1 only if one of the input is 1?

**Options**

- **A.** NOR
- **B.** EXOR
- **C.** NOT
- **D.** EXNOR

{{< details title="Show answer and explanation" closed="true" >}}

**Answer: B.** EXOR

EXOR outputs 1 only when exactly one input is 1 (inputs differ); it outputs 0 when both are 0 or both are 1.

{{< /details >}}

### Q24 · C Programming

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

**Options**

- **A.** Garbage value
- **B.** Compile time error
- **C.** 10
- **D.** 0

{{< details title="Show answer and explanation" closed="true" >}}

**Answer: C.** 10

`m` is **static**, so every recursive call shares one copy. Each call does `++m` and calls itself again while `m < 10`. When `m` reaches 10 the check fails, the recursion stops, and every call returns `m`, which is now 10. So `printf` receives **10**.

*Confidence: medium. The answer depends on compiler behaviour or on reading an ambiguous question.*

{{< /details >}}

### Q25 · C Programming

What is the output?

```c
char a = 4; char b = 2; char c = 1;
printf("%d ", -a / b);
printf("%d ", -c % -b);
```

**Options**

- **A.** `2 1`
- **B.** `-2 -1`
- **C.** `2 -1`
- **D.** `-2 1`

{{< details title="Show answer and explanation" closed="true" >}}

**Answer: B.** `-2 -1`

`char`s are promoted to `int`. `-4 / 2 = -2`. For `%`, the result takes the **sign of the left number**: `-1 % -2 = -1`. Output: `-2 -1`.

{{< /details >}}

### Q26 · Data Structures Basics

What will be the number of swaps required to sort the elements given below in descending order using selection sort if last element of the list is sorted first? 43 23 98 61 29 30 17

**Options**

- **A.** 7
- **B.** 8
- **C.** 5
- **D.** 3

{{< details title="Show answer and explanation" closed="true" >}}

**Answer: D.** 3

Selection sort for **descending** order, filling the last slot first (the smallest of the remaining goes to the end). Count only passes where the smallest is *not* already at the end:

| Pass | Part sorted | Smallest | Swap? | Array after |
|---|---|---|---|---|
| 1 | all 7 | 17 (already last) | no | 43 23 98 61 29 30 17 |
| 2 | first 6 | 23 | yes (1) | 43 30 98 61 29 23 17 |
| 3 | first 5 | 29 (already last) | no | same |
| 4 | first 4 | 30 | yes (2) | 43 61 98 30 29 23 17 |
| 5 | first 3 | 43 | yes (3) | 98 61 43 30 29 23 17 |
| 6 | first 2 | 61 (already last) | no | same |

Total swaps = **3**.

*Confidence: medium. The answer depends on compiler behaviour or on reading an ambiguous question.*

{{< /details >}}

### Q27 · C Programming

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

**Options**

- **A.** `Compile time error`
- **B.** `69 1 1`
- **C.** `101 2 3`
- **D.** `98 1 3`

{{< details title="Show answer and explanation" closed="true" >}}

**Answer: D.** `98 1 3`

`tr` starts on the 4th letter of `"Korea"` (`e`). In the first `printf`, `*r--` gives `tr`, `++` moves it to the next letter `a`, and the last `++` makes it `b`, whose ASCII code is **98**. Only one option starts with 98: `98 1 3`.

Note: `r--` moves `r` off `&tr`, so the rest depends on how the compiler lays out the stack (undefined behaviour; it can even crash). For the exam, pick the option by the first value. The `1` and `3` are the workbook's key values.

*Confidence: medium. The answer depends on compiler behaviour or on reading an ambiguous question.*

{{< /details >}}

### Q28 · OS Fundamentals

Priority scheduling; a **lower** number means **higher** priority. All processes arrive at time 0.

| Process | Burst time | Priority |
|---|---|---|
| P0 | 7 | 3 |
| P1 | 7 | 2 |
| P2 | 4 | 5 |
| P3 | 9 | 8 |

What is the turnaround time of P2?

**Options**

- **A.** 9.75
- **B.** 18
- **C.** 14
- **D.** 7

{{< details title="Show answer and explanation" closed="true" >}}

**Answer: B.** 18

Lower number = higher priority. Order: P1 (7), P0 (7), P2 (4), P3 (9). P2 completes at 7 + 7 + 4 = 18. Arrival = 0, so turnaround = 18.

{{< /details >}}

### Q29 · Data Structures Basics

A doubly linked list is `A <-> X <-> Y <-> B -> NULL`. Three steps are applied in order:

1. Insert a new node **P** with `prev = NULL` and `next = current head`.
2. The **3rd node's** `next` is set to **B**, and **B's** `prev` is set to **X**.
3. Insert a new node **M** with `prev = B` and `next = NULL`.

What is the order of the elements?

**Options**

- **A.** A → P → X → Y → M
- **B.** P → A → X → B → M
- **C.** A → X → Y → M → P
- **D.** P → A → Y → B → M

{{< details title="Show answer and explanation" closed="true" >}}

**Answer: B.** P → A → X → B → M

Step I puts P at the head before A. Step II makes the 3rd node point to B while B's prev becomes X, effectively bypassing Y. Step III appends M after B. Result: P → A → X → B → M.

*Confidence: medium. The answer depends on compiler behaviour or on reading an ambiguous question.*

{{< /details >}}

### Q30 · Computer Architecture

Which one of the given options correctly represents the hexadecimal value of (0011 0101 1111 1010)2?

**Options**

- **A.** `30AF`
- **B.** `35FA`
- **C.** `13FC`
- **D.** `30FB`

{{< details title="Show answer and explanation" closed="true" >}}

**Answer: B.** `35FA`

0011 = 3, 0101 = 5, 1111 = F, 1010 = A → 35FA.

{{< /details >}}

### Q31 · Data Structures Basics

List: 4 17 29 30 48 51 69. If binary search technique is used to search 69 in the above list how many passes are required?

**Options**

- **A.** 7
- **B.** 3
- **C.** 4
- **D.** 5

{{< details title="Show answer and explanation" closed="true" >}}

**Answer: B.** 3

Pass 1: mid = index 3 → 30, 69 > 30, go right. Pass 2: mid of [48,51,69] → 51, go right. Pass 3: mid → 69, found. 3 passes.

{{< /details >}}

### Q32 · OS Fundamentals

Which of the program given in options helps in converting the assembly language programs to an object program?

**Options**

- **A.** Macroprocessor
- **B.** Linker
- **C.** Assembler
- **D.** Compiler

{{< details title="Show answer and explanation" closed="true" >}}

**Answer: C.** Assembler

An assembler translates assembly language source into machine-code object files. A compiler works on high-level languages; a linker combines object files.

{{< /details >}}

### Q33 · Computer Architecture

The initial content of a 4-bit register is `1011`. It is shifted **4 times to the right**, with the serial input `111010`. What is the content of the register after four shifts?

**Options**

- **A.** 101011
- **B.** 1100
- **C.** 1011
- **D.** 101110

{{< details title="Show answer and explanation" closed="true" >}}

**No reliable answer.** This question is flagged: it looks flawed or its key could not be derived, so no option is picked here.

Shifting 1011 right 4 times with serial inputs 1,1,1,0 at the MSB gives 0111; reading the input from the other end gives 1010. Neither is an option, and two options are 6 bits wide for a 4-bit register. Question appears flawed.

{{< /details >}}

### Q34 · Computer Architecture

Whenever a subroutine is called, the program counter details are stored in:

**Options**

- **A.** Queue
- **B.** Linked List
- **C.** Doubly Linked List
- **D.** Stack

{{< details title="Show answer and explanation" closed="true" >}}

**Answer: D.** Stack

The return address (PC) is pushed onto the call stack, which matches the LIFO nature of nested subroutine calls and returns.

{{< /details >}}

### Q35 · C Programming

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

**Options**

- **A.** `1 -11`
- **B.** `1 0 1 0`
- **C.** `1 -11 1 -11`
- **D.** `Compile time error`

{{< details title="Show answer and explanation" closed="true" >}}

**Answer: C.** `1 -11 1 -11`

**First call** `func(10, 10)`: `≈10 = -11` (non-zero), then `++b = 11` (non-zero), so `&&` gives **1**. The second value `≈b` is `≈10 = -11` (gcc evaluates the arguments right to left, so `b` is not yet incremented). Prints `1 -11`.

`func` returns `a`, which is 11, so the `if` condition is **true**. Short-circuit `||` only skips evaluating `c != 1`; it does **not** skip the body. So `func(b, c)` runs too, with the same values, and prints `1 -11` again.

Output: `1 -11 1 -11`.

> **Editor's note.** The source workbook lists `1 -11` (it assumed the short-circuit skips the second call). Running the code gives `1 -11 1 -11`, so the answer here is corrected.

*Confidence: medium. The answer depends on compiler behaviour or on reading an ambiguous question.*

{{< /details >}}

### Q36 · Data Structures Basics

Queue Q of size 5 containing: A P Q. What will be the queue after: Enqueue(J), Dequeue(), Enqueue(M), Enqueue(D), Enqueue(X)?

**Options**

- **A.** M D P Q J _
- **B.** _ A P Q J D
- **C.** _ M P Q J D
- **D.** Overflow

{{< details title="Show answer and explanation" closed="true" >}}

**Answer: D.** Overflow

A P Q → +J = A P Q J → Dequeue removes A → P Q J → +M → P Q J M → +D → P Q J M D (5 elements, rear at last slot). Enqueue(X) exceeds the size 5 linear queue → Overflow.

*Confidence: medium. The answer depends on compiler behaviour or on reading an ambiguous question.*

{{< /details >}}

### Q37 · Error Finding

Identify the error (if any) and how it can be fixed.

```c
int x = 5;
int y = 0;
int z = x / y;
printf("The result is: %d\n", z);
```

**Options**

- **A.** %d is wrong; Fix: Replace it with '-d'
- **B.** No Error
- **C.** Incorrect format specifier; Fix: Change '%d' to '%f' in the printf statement
- **D.** Division by zero; Fix: Change the value of y to a non-zero value

{{< details title="Show answer and explanation" closed="true" >}}

**Answer: D.** Division by zero; Fix: Change the value of y to a non-zero value

x / y with y = 0 is integer division by zero - undefined behaviour, typically a runtime crash. The fix is to ensure y is non-zero. %d is correct for an int.

{{< /details >}}

### Q38 · C Programming

What is the output?

```c
int a = 3, b = 5, c = 12;
int *pa = &a, *pb = &b, *pc = &c;
a += !(--*pa + *pb) && ++*pc;
*pc += (!++*pa) || *pb++;
printf("%d %d %d", a, b, c);
```

**Options**

- **A.** `3 5 13`
- **B.** `3 5 14`
- **C.** `2 5 19`
- **D.** `4 5 14`

{{< details title="Show answer and explanation" closed="true" >}}

**Answer: A.** `3 5 13`

**Line 3:** `--*pa` makes `a = 2`; `2 + 5 = 7`; `!7 = 0`. Since the left side of `&&` is 0, `++*pc` is **never evaluated**, so `a += 0` leaves `a = 2`.

**Line 4:** `++*pa` makes `a = 3`; `!3 = 0`, so `||` evaluates `*pb++`. That yields 5 (true) and only moves the pointer `pb`; `b` stays 5. The result is 1, so `c = 12 + 1 = 13`.

Output: `3 5 13`.

*Confidence: medium. The answer depends on compiler behaviour or on reading an ambiguous question.*

{{< /details >}}

### Q39 · C Programming

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

**Options**

- **A.** `POINTERFIRST`
- **B.** `POINTNEWENTR`
- **C.** `POINTERENSTEN`
- **D.** `POINTERERSTEW`

{{< details title="Show answer and explanation" closed="true" >}}

**Answer: D.** `POINTERERSTEW`

Trace `cpp` step by step:

1. `++cpp` points at `cp[1] = c+2`, so `**cpp = "POINTER"`. Prints **POINTER**.
2. `++cpp` points at `cp[2] = c+1`; `--` turns it into `c`, so `*c = "ENTER"`, and `+3` gives **ER**.
3. `cpp[-2] = cp[0] = c+3`, so `"FIRST" + 3` = **ST**.
4. `cpp[-1] = cp[1] = c+2`, `[-1]` gives `"NEW"`, `+1` = **EW**.

Joined: `POINTERERSTEW`.

*Confidence: medium. The answer depends on compiler behaviour or on reading an ambiguous question.*

{{< /details >}}

### Q40 · Error Finding

The code reads a number with `scanf` and prints it. Which line causes the error? (Reconstructed from the question; line numbers as in the exam.)

```c
#include <stdio.h>               // Line 1
int main() {                     // Line 2
    int num;                     // Line 3
    printf("Enter a number: ");  // Line 4
    scanf("%d", num);            // Line 5
    printf("The entered number is: %d\n", num);  // Line 6
    return 0;
}
```

**Options**

- **A.** Line 1
- **B.** Line 5
- **C.** No Error
- **D.** Line 6

{{< details title="Show answer and explanation" closed="true" >}}

**Answer: B.** Line 5

scanf requires the address of the variable. It should be scanf("%d", &num); passing num by value is the error on Line 5.

{{< /details >}}
