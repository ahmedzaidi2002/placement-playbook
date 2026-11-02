---
title: "Strings and character arrays"
weight: 8
---

3 questions asked by NVIDIA, Qualcomm, Texas Instruments. Try each one first, then open the toggle: it gives the answer, why it is right, and the idea behind it explained from scratch.

### 1 · Q14, indexing a string by an int

*Asked by: NVIDIA (SSE NCG, Nov 2024)*

What would the output of this program be?

```c
#include <stdio.h>

int main()
{
    char *mystring = "hello world";
    int myint[] = {0, 1, 2, 3, 4, 5, 6, 7};
    char *c;
    int *x = &myint[0];
    x += 3;
    c = &mystring[0];

    printf("%c ", c[*x]);
}
```

- **(a)** Compilation error
- **(b)** Run time error
- **(c)** l
- **(d)** Cannot be predicted

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) l**

**Why.** x points to myint[3], which holds 3. `c[*x]` = c[3] = the 4th character of "hello world": 'l'.

**Concept: indexing with an expression.** `c[k]` = `*(c + k)`, where k can be any integer expression, including a value read through another pointer.

{{< /details >}}

### 2 · Q25, string copy loop

*Asked by: Qualcomm (IISc)*

What will be the output of the following program? (The photo shows the program only as far
as the line below the second `strcpy`; the rest of the program and the options are
[cut off in the source].)

```c
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
int main()
{
    char *ptr1 = "name";
    char *ptr2;
    char *ptr3;
    char *ptr4;
    int i = 0;
    ptr2 = (char *)malloc(10);
    ptr3 = (char *)malloc(12);
    ptr4 = (char *)malloc(12);
    while (ptr2[i++] = ptr1[i]);
    printf("%s\n", ptr2);
    strcpy(ptr3, "1234");
    strcpy(ptr4, "ab\0cdefghij");
    /* ... the rest of the program is cut off in the photo ... */
}
```

{{< details title="Answer and explanation" closed="true" >}}

**Answer: only the first line can be worked out: "ame" with GCC** (undefined behaviour; another compiler may print "name").

**Why.** `while (ptr2[i++] = ptr1[i]);` reads and modifies i in one expression without a sequence point. GCC evaluates the left side first, so ptr2[0] = ptr1[1], ptr2[1] = ptr1[2], ..., copying "ame". Also, `strcpy(ptr4, "ab\0cdefghij")` copies only "ab", because the literal effectively ends at the embedded `\0`.

**Concept: strings end at the first `\0`.** All `str*` functions stop at the first null byte, even if more characters follow in memory.

{{< /details >}}

### 3 · a string without a terminator

*Asked by: Texas Instruments (NIT Calicut 2023)*

```cpp
char ABC[5] = "hello";
printf("%d", *(ABC + 4));
```

- **(a)** 111
- **(b)** 0
- **(c)** Garbage value
- **(d)** Runtime error

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) 111**

**Why.** ABC[4] is the letter 'o', whose ASCII code is 111. C allows `char ABC[5] = "hello";`: the five letters fill the array exactly and the terminating null is dropped. (C++ rejects this; printing ABC with `%s` would also be unsafe.)

**Concept: string arrays need room for `\0`.** "hello" needs 6 bytes including the terminator. Declaring exactly 5 is legal in C but leaves an unterminated string.

{{< /details >}}
