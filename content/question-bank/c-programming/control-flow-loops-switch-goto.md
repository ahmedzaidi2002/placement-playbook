---
title: "Control flow (loops, switch, goto)"
weight: 7
---

3 questions asked by MathWorks, NVIDIA. Try each one first, then open the toggle: it gives the answer, why it is right, and the idea behind it explained from scratch.

### 1 · Q27, if without braces

*Asked by: MathWorks (IISc 2024); MathWorks (Recalled list)*

Predict the output:

```c
int i = 109;
if (i > 50)
    i++;
    i += 2;
else
    i--;
printf("%d\n\n\n", i);
```

{{< details title="Answer and explanation" closed="true" >}}

**Answer: compilation error** (`else` without a previous `if`)

**Why.** Without braces, `if (i > 50)` controls only `i++;`. The next statement `i += 2;` ends the if. The `else` then has no `if` to attach to.

**Concept: braces define the body.** An `if` without braces controls exactly one statement; indentation means nothing to the compiler. Always use braces for multi-statement bodies.

{{< /details >}}

### 2 · Q12, Hello World count

*Asked by: MathWorks (Recalled list)*

```c
char i = 101;
while (--i) {
    printf("\Hello World");
    i--;
}
```

Given that the ASCII value of `0' is 48, how many times is "Hello World" printed?

- **(a)** 101
- **(b)** 50
- **(c)** Infinitely many
- **(d)** 51
- **(e)** 26

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) 50**

**Why.** i starts at 101. Each loop does `--i` in the test and `i--` in the body: i drops by 2 per iteration. The body runs for i = 100, 98, ..., 2 (50 times); then `--i` makes i 0 and the loop stops. The ASCII hint is a distractor (`\H` is an unknown escape that prints H).

**Concept: trace the loop variable.** Write down its value at the test each time. Pre-decrement in the condition changes i before the comparison; the body changes it again.

{{< /details >}}

### 3 · Q10, post-decrement in a loop

*Asked by: NVIDIA (SSE NCG, Nov 2024)*

What would the output of this program be?

```c
#include <stdio.h>

int main()
{
    int x = 3;
    while (x-- >= 0)
    {
        printf("%d ", x);
    }
    return 0;
}
```

- **(a)** 3 2 1 0 -1
- **(b)** 3 2 1 0
- **(c)** 2 1 0
- **(d)** 2 1 0 -1

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) 2 1 0 -1**

**Why.** `x-- >= 0` compares the old value, then decrements. Tests: 3 ≥ 0 (x becomes 2, prints 2), 2 ≥ 0 (prints 1), 1 ≥ 0 (prints 0), 0 ≥ 0 (prints −1), −1 ≥ 0 fails.

**Concept: post-decrement in a condition.** `x--` yields the old value for the comparison; the body then sees the new value. So the body sees one less than what was tested.

{{< /details >}}
