---
title: 4 · Computer science (Q41–Q60)
weight: 4
---

Twenty questions on architecture, data structures, C pointers, OOP and operating systems. Several are pointer-heavy C snippets, so trace them on paper.

### Q41 · Computer Architecture

Calculate the **variance** in instruction latency of the pipeline (earlier non-pipelined) with stage times 40 ns, 50 ns, 60 ns, 30 ns, 50 ns, 50 ns and a clock skew of 4 ns.

**Options**

- **A.** 280ns
- **B.** 224ns
- **C.** 220ns
- **D.** 216ns

{{< details title="Show answer and explanation" closed="true" >}}

**No reliable answer.** This question is flagged: it looks flawed or its key could not be derived, so no option is picked here.

Non-pipelined latency = 40+50+60+30+50+50 = 280ns. Pipelined clock = max stage + skew = 60 + 4 = 64ns, so pipelined latency = 6 × 64 = 384ns; difference = 104ns (not an option). 216ns = 280 - 64 is the only derivable option, but that reading of 'variance' is non-standard. 224ns cannot be constructed from these values.

If you must guess, the workbook's only derivable option is **D. 216 ns** (280 − 64), which relies on a non-standard reading of "variance".

{{< /details >}}

### Q42 · Data Structures

What does this code do?

```c
void Queue(int element) {
    if (!isFull()) {
        if (front == -1) front = 0;
        rear = (rear + 1) % size;
        items[rear] = element;
    }
}
```

**Options**

- **A.** `Delete an element from the queue.`
- **B.** `Run time error`
- **C.** `Traverse the queue.`
- **D.** `Insert an element into the queue.`

{{< details title="Show answer and explanation" closed="true" >}}

**Answer: D.** `Insert an element into the queue.`

It checks for fullness, initialises front on the first insertion, advances rear circularly and writes the element at items[rear] - the standard circular queue enqueue operation.

{{< /details >}}

### Q43 · C Programming

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

**Options**

- **A.** No error in the program
- **B.** Line 2
- **C.** Both Line 1 and Line 2
- **D.** Line 1

{{< details title="Show answer and explanation" closed="true" >}}

**Answer: D.** Line 1

The semicolon after while(*s) makes it an empty-bodied loop with a condition that never changes (*s = 6, always true) - an infinite loop, and the braces below become a detached block. The defect is on Line 1.

*Confidence: medium. The answer depends on compiler behaviour or on reading an ambiguous question.*

{{< /details >}}

### Q44 · OOPS

When a message is sent to an object that cannot handle it:

**Options**

- **A.** The system automatically generates the method
- **B.** It is broadcast to all objects
- **C.** The message is ignored silently
- **D.** An exception or error occurs

{{< details title="Show answer and explanation" closed="true" >}}

**Answer: D.** An exception or error occurs

If no matching method exists for the message, the runtime raises an error/exception (e.g. NoSuchMethodError, AttributeError) - it is neither generated automatically nor silently ignored.

{{< /details >}}

### Q45 · C Programming

Which option is correct about this code snippet?

```c
char *ptr = "aquarious";
int i;
ptr += 1;
while (1 < *ptr) {
    printf("%c", *ptr);
}
```

**Options**

- **A.** `Compile time error`
- **B.** `q`
- **C.** `quarious`
- **D.** `Infinite loop`

{{< details title="Show answer and explanation" closed="true" >}}

**Answer: D.** `Infinite loop`

ptr is never advanced inside the loop, so *ptr stays 'q' (113) and the condition 1 < 113 is always true - the loop prints 'q' forever.

{{< /details >}}

### Q46 · Computer Architecture

Which one of the given options is the correct form after simplifying the expression given below? B'D + BC'D + C'D

**Options**

- **A.** `B'D + C'D`
- **B.** `B' + C'D`
- **C.** `B' + B + C'`
- **D.** `BD + C'D`

{{< details title="Show answer and explanation" closed="true" >}}

**Answer: A.** `B'D + C'D`

BC'D + C'D = C'D(B + 1) = C'D. So the expression reduces to B'D + C'D.

{{< /details >}}

### Q47 · C Programming

a[3][3] is equivalent to which of the given pointer notation?

**Options**

- **A.** `**(a + 6)`
- **B.** `**(a + 9)`
- **C.** `*(a + 3) + 3`
- **D.** `*(*(a + 3) + 3)`

{{< details title="Show answer and explanation" closed="true" >}}

**Answer: D.** `*(*(a + 3) + 3)`

For a 2D array, a[i][j] == *(*(a + i) + j). With i = j = 3 this gives *(*(a + 3) + 3).

{{< /details >}}

### Q48 · OOPS

class Account { private balance; updateBalance(amount) }. A subclass PromotionalAccount exposes public adjustBalance(amount) which directly modifies balance without the validation inside updateBalance(). Accounts show invalid negative balances. What encapsulation breach caused the failure?

**Options**

- **A.** Maintaining an internal cache without aligning with calling sequence
- **B.** Adding method overloading that increases constructor parameter count
- **C.** Using a new parameter type that expands acceptable data formats
- **D.** Exposing an alternate path that bypasses protected validation logic

{{< details title="Show answer and explanation" closed="true" >}}

**Answer: D.** Exposing an alternate path that bypasses protected validation logic

The subclass created a second public route to the internal state that skips the base class's invariant checks - the classic encapsulation breach of bypassing protected validation logic.

{{< /details >}}

### Q49 · C Programming

What is the output?

```c
int a[10];
printf("%d", *a + 1 - *a + 3);
```

**Options**

- **A.** `Compile time error`
- **B.** `4`
- **C.** `2`
- **D.** `3`

{{< details title="Show answer and explanation" closed="true" >}}

**Answer: B.** `4`

The expression is (*a) + 1 - (*a) + 3. The two *a terms cancel regardless of the uninitialised value, leaving 1 + 3 = 4.

{{< /details >}}

### Q50 · Computer Architecture

What is the hexadecimal equivalent of the below given binary number? 1101110

**Options**

- **A.** `6eh`
- **B.** `5dh`
- **C.** `3fh`
- **D.** `1fh`

{{< details title="Show answer and explanation" closed="true" >}}

**Answer: A.** `6eh`

Group in 4s from the right: 110 | 1110 → 0110 = 6, 1110 = E → 6Eh.

{{< /details >}}

### Q51 · Data Structures

What goes in the blank so the function computes the product of two 2D matrices?

```c
int mul() {
    int A[n][p], B[p][m], C[n][m];
    for (int i = 0; i < n; i++)
        for (int k = 0; k < m; k++) {
            Sum = 0;
            ______
        }
    return C;
}
```

**Options**

- **A.** `for (int j=0;j<p;j++) Sum += A[i][k]*B[j][i]; C[i][j] = Sum`
- **B.** `C[i][k] = Sum; Sum += A[i][k]*B[k][i];`
- **C.** `for (int j=0;j<p;j++) Sum += A[i][j]*B[j][k]; C[i][k] = Sum;`
- **D.** `Sum += A[i][k]*B[k][i]; C[i][k] = Sum;`

{{< details title="Show answer and explanation" closed="true" >}}

**Answer: C.** `for (int j=0;j<p;j++) Sum += A[i][j]*B[j][k]; C[i][k] = Sum;`

Matrix multiply needs an innermost loop over the shared dimension p, accumulating A[i][j] * B[j][k], then storing into C[i][k]. Only this option has both the loop and correct index order.

{{< /details >}}

### Q52 · Data Structures

The time taken by binary search algorithm to search a key in a sorted array of n elements is:

**Options**

- **A.** O(n)
- **B.** O(log n)
- **C.** O(n log n)
- **D.** O(n^2)

{{< details title="Show answer and explanation" closed="true" >}}

**Answer: B.** O(log n)

Each comparison halves the search space, so the number of steps is log2(n) → O(log n).

{{< /details >}}

### Q53 · C Programming

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

**Options**

- **A.** `-34 6 1134 1240`
- **B.** `-42 5 1120 1220`
- **C.** `-45 4 1239 1235`
- **D.** `-48 3 1112 1320`

{{< details title="Show answer and explanation" closed="true" >}}

**Answer: C.** `-45 4 1239 1235`

`1234 = 0x04D2`. Little-endian: byte 0 is `0xD2` (as a signed `char`, **-46**), byte 1 is `0x04`.

1. `++*ptr++` bumps byte 0 to -45 (`s` becomes 1235), prints **-45**, then `ptr` moves to byte 1.
2. `*ptr = 5` sets byte 1 to 5. `--*ptr--` makes it 4, prints **4**, then `ptr` goes back to byte 0.
3. `*ptr++;` just moves `ptr` to byte 1.
4. `*ptr++ + s` is `4 + 1235 =` **1239**.
5. `s++` prints the old value **1235**.

Output: `-45 4 1239 1235`. (The exam answer `-42 5 1120 1220` was marked by the candidate and was wrong.)

*Confidence: medium. The answer depends on compiler behaviour or on reading an ambiguous question.*

{{< /details >}}

### Q54 · C Programming

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

**Options**

- **A.** `-2 -2 / 255 -1 4`
- **B.** `-2 -2 / 255 -1 0`
- **C.** `-1 -1 / 255 -1 0`
- **D.** `Compile time error`

{{< details title="Show answer and explanation" closed="true" >}}

**Answer: B.** `-2 -2 / 255 -1 0`

Both arguments are copied into plain `char` parameters holding the bit pattern `0xFF`, which reads as **-1**. So `a << 1` and `b << 1` both print **-2**.

Back in `main`, `a` is an `unsigned char`, so it prints **255**; `b` is a `signed char`, so it prints **-1**.

`fun` has no `return`, so `c` is undefined behaviour. The two options that differ only here are `4` and `0`; the workbook's key takes **0**.

*Confidence: medium. The answer depends on compiler behaviour or on reading an ambiguous question.*

{{< /details >}}

### Q55 · Operating Systems

What is the order of the steps in a **deadlock detection algorithm**?

- (I) Initialise the temporary vector to the available vector.
- (II) Find the currently unmarked process.
- (III) If a row is not found, terminate the algorithm.
- (IV) If a row is found, add that row to the allocation matrix.
- (V) Mark the process that has a row of all zeroes.

**Options**

- **A.** (IV), (V), (III), (I) and (II)
- **B.** (V), (I), (II), (IV) and (III)
- **C.** (II), (I), (III), (IV) and (V)
- **D.** (I), (II), (IV), (III) and (V)

{{< details title="Show answer and explanation" closed="true" >}}

**Answer: D.** (I), (II), (IV), (III) and (V)

Initialise the work vector first, then look for an unmarked process, add its row if found, terminate if none is found, and mark processes whose request rows are all zeroes. Only this option starts with initialisation.

*Confidence: medium. The answer depends on compiler behaviour or on reading an ambiguous question.*

{{< /details >}}

### Q56 · C Programming

What is the output?

```c
char ch[] = "red";
char *p[3] = {"red", "white", "pink"};
char *q[3] = {"apple", "banana", "orange"};
printf("%s %s\n", *p + 1, *q + 2);
printf("%d %d ", sizeof(*p), sizeof(q + 1));
```

**Options**

- **A.** `Compile time error`
- **B.** `ed ple / 4 4`
- **C.** `e p / 9 9`
- **D.** `White banana / 9 9`

{{< details title="Show answer and explanation" closed="true" >}}

**Answer: B.** `ed ple / 4 4`

`*p` is `"red"`, and `+1` skips one letter, giving **ed**. `*q` is `"apple"`, and `+2` gives **ple**.

`sizeof(*p)` and `sizeof(q + 1)` are both the size of a pointer, which is **4** on the 32-bit target the question assumes (it would be 8 on a 64-bit build, but no option says that).

*Confidence: medium. The answer depends on compiler behaviour or on reading an ambiguous question.*

{{< /details >}}

### Q57 · Data Structures

Which of the given options is true about the singly linked list?

**Options**

- **A.** The reference part of the last node in the singly linked list must be NULL.
- **B.** No node can be inserted in the middle of the singly linked list.
- **C.** Using singly linked list, trees and graphs cannot be created.
- **D.** The address of the first node is always stored in a reference node of the previous node.

{{< details title="Show answer and explanation" closed="true" >}}

**Answer: A.** The reference part of the last node in the singly linked list must be NULL.

In a singly linked list the tail's next pointer is NULL to mark the end. Insertion in the middle is possible; trees and graphs can be built from linked nodes; the head has no previous node.

{{< /details >}}

### Q58 · Operating Systems

Which one of the given options is the responsibility of a secondary scheduler?

**Options**

- **A.** Runs threads with higher priority.
- **B.** Assigns priorities to all threads.
- **C.** Maintains states of executed, executing and non - executing threads.
- **D.** Increases the priority of non - executing threads.

{{< details title="Show answer and explanation" closed="true" >}}

**Answer: C.** Maintains states of executed, executing and non - executing threads.

The secondary (medium-term) scheduler tracks and maintains thread/process state information; running high-priority threads and assigning priorities are the primary scheduler's job.

*Confidence: medium. The answer depends on compiler behaviour or on reading an ambiguous question.*

{{< /details >}}

### Q59 · OOPS

A notification system has a method sendAlert() that behaves differently for EmailAlert, SMSAlert, and PushAlert classes. Which type of polymorphism is used here?

**Options**

- **A.** Method overloading
- **B.** Operator overloading
- **C.** Method overriding
- **D.** Compile-time binding

{{< details title="Show answer and explanation" closed="true" >}}

**Answer: C.** Method overriding

The same signature sendAlert() is redefined by each subclass and resolved at runtime - that is method overriding (runtime polymorphism). Overloading would mean different parameter lists in the same class.

{{< /details >}}

### Q60 · Operating Systems

Segment table (base, length): segment 0 = (402, 245), segment 1 = (341, 449), segment 2 = (111, 23).

What are the physical addresses for these logical addresses, and does a segmentation fault occur for any of them?

- (I) segment 0, offset 402
- (II) segment 2, offset 25

**Options**

- **A.** Segmentation Fault for both addresses
- **B.** 804, 48
- **C.** 743, 48
- **D.** 402, Segmentation fault for second address

{{< details title="Show answer and explanation" closed="true" >}}

**Answer: A.** Segmentation Fault for both addresses

(I) Segment 0, offset 402: 402 > length 245 → fault. (II) Segment 2, offset 25: 25 > length 23 → fault. Both cause a segmentation fault.

{{< /details >}}
