---
title: "printf/scanf and I/O"
weight: 11
---

1 question asked by Qualcomm. Try each one first, then open the toggle: it gives the answer, why it is right, and the idea behind it explained from scratch.

### 1 · Error Finding

*Asked by: Qualcomm (60-question online assessment)*

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

- **(a)** Line 1
- **(b)** Line 5
- **(c)** No Error
- **(d)** Line 6

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) Line 5**

**Why.** `scanf` needs the address of the variable to write into: `scanf("%d", &num);`. Passing `num` gives scanf a garbage value to use as an address (undefined behaviour, often a crash).

**Concept: why scanf needs `&`.** C passes arguments by value; to let a function change your variable, pass its address. (Arrays like `char s[20]` already decay to an address, so `scanf("%s", s)` has no `&`.)

{{< /details >}}
