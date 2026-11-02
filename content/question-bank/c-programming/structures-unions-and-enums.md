---
title: "Structures, unions and enums"
weight: 5
---

6 questions asked by MathWorks, NVIDIA, Qualcomm, Texas Instruments. Try each one first, then open the toggle: it gives the answer, why it is right, and the idea behind it explained from scratch.

### 1 · Q20, struct padding

*Asked by: MathWorks (IIIT Delhi 2024)*

Consider the two structures

```cpp
struct Student {
    double height;
    int ID;
    short int Roll_num;
};
struct Teacher {
    int ID;
    double height;
    short int Roll_num;
};
```

What are the sizes of `struct Student Vineeth` and `struct Teacher Koundinya`
(in bytes)?

- **(a)** 16 and 16
- **(b)** 14 and 14
- **(c)** 16 and 24
- **(d)** None of the above

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) 16 and 24**

**Why.** Each member must start at an address that is a multiple of its size (on a typical 64-bit system).
- Student: double (8) at 0, int (4) at 8, short (2) at 12 → 14 bytes, padded to a multiple of 8 → 16.
- Teacher: int (4) at 0, 4 bytes padding so the double starts at 8, double at 8–15, short at 16–17 → 18, padded to 24.

**Concept: struct padding and alignment.** The compiler inserts gaps so each member is aligned, and pads the end so the struct's size is a multiple of its largest alignment (so arrays of it stay aligned). Ordering members from largest to smallest minimises padding.

{{< /details >}}

### 2 · Q15, struct pointer from a member address

*Asked by: NVIDIA (SSE NCG, Nov 2024)*

What would this program output? (The fourth option is [cut off in the source].)

```c
#include <stdio.h>

int main()
{
    struct site
    {
        int number;
    };

    struct site *ptr, x;
    x.number = 23;
    ptr = (struct site *)&x.number;
    printf("%d ", (ptr->number)++);

    return 0;
}
```

- **(a)** Compilation error
- **(b)** Runtime error
- **(c)** 23

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) 23**

**Why.** A struct's first member starts at offset 0, so `&x.number` is the same address as `&x`. Casting it to `struct site*` and reading `ptr->number` reads x.number. The post-increment prints the old value, 23.

**Concept: first-member address = struct address.** C guarantees no padding before the first member, which is why this cast is valid.

{{< /details >}}

### 3 · Q21, member initialiser in a C struct

*Asked by: NVIDIA (SSE NCG, Nov 2024)*

What would this program output?

```c
#include <stdio.h>

int main()
{
    struct site
    {
        int number = 23;
    };

    struct site *ptr;
    printf("%d ", ++ptr->number);

    return 0;
}
```

- **(a)** Compilation error
- **(b)** Runtime error
- **(c)** 23
- **(d)** 24

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) compilation error**

**Why.** C does not allow default values inside a struct definition (`int number = 23;`). (C++11 allows it, but `ptr` is uninitialised, so `++ptr->number` would be undefined there.)

**Concept: struct definitions only describe layout.** In C, initialise members when you create a variable: `struct site x = {23};`.

{{< /details >}}

### 4 · Q47, enum

*Asked by: Qualcomm (Nov 2024)*

What will be the output of the program given below?

```c
#include <stdio.h>
int main()
{
    char *p = "Kerala", *q = "Ooty", *r = "Mysore", *s = "Shimoga";
    enum loc {Kerala = 1, Ooty = 2, Mysore = 3, Shimoga = 4};
    enum loc dir;
    dir = Shimoga;
    if (dir == Shimoga)
        printf("The best place is %s\n", s);
    return 0;
}
```

- **(a)** The best place is Ooty
- **(b)** The best place is Mysore
- **(c)** The best place is Shimoga
- **(d)** The best place is Kerala

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) The best place is Shimoga**

**Why.** dir is set to Shimoga, the test `dir == Shimoga` is true, and s points to "Shimoga".

**Concept: enums are named integer constants.** `enum loc {Kerala = 1, ...}` just names the values 1–4. They live in a different role from the pointer variables p, q, r, s, so there is no clash.

{{< /details >}}

### 5 · an array of struct pointers

*Asked by: Texas Instruments (BITS Pilani)*

On a 64-bit system,

```cpp
struct {
    float angle, radius;
} *vector[10];
```

What is
`sizeof(vector)`?

- **(a)** 20
- **(b)** 32
- **(c)** 64
- **(d)** 80

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) 80**

**Why.** `*vector[10]` is an array of 10 pointers (to the struct). On a 64-bit system each pointer is 8 bytes: 10 × 8 = 80. The struct's own size does not matter.

**Concept: read declarations from the name outward.** `vector[10]` (array of 10), then `*` (pointers), then the struct type. `sizeof` an array = elements × element size.

{{< /details >}}

### 6 · size of a struct array

*Asked by: Texas Instruments (IIT BHU 2023)*

On a 32-bit system:

```cpp
typedef struct {
    float angle, radius;
    char *next;
} VECTOR;
VECTOR v[10];
printf("%d", sizeof(v));
```

- **(a)** 120
- **(b)** 160
- **(c)** 200
- **(d)** 320

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) 120**

**Why.** On a 32-bit system: float 4 + float 4 + pointer 4 = 12 bytes per VECTOR (no padding needed). 10 of them: 120. (The candidates' 160 and 200 are wrong.)

**Concept: struct size = members + padding.** Here all members are 4 bytes, so no padding is added.

{{< /details >}}
