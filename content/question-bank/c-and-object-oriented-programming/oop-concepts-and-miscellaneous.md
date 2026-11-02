---
title: "OOP concepts and miscellaneous"
weight: 2
---

8 questions asked by Fujitsu, MAQ Software, MathWorks, NVIDIA, Qualcomm, Warner Bros. Discovery. Try each one first, then open the toggle: it gives the answer, why it is right, and the idea behind it explained from scratch.

### 1 · PC Q1, left shift

*Asked by: Fujitsu (IIT Kharagpur 2023)*

What is the output of the following C++ code?

```cpp
#include <iostream>
int main() {
    int x = 5;
    std::cout << (x << 1) << std::endl;
    return 0;
}
```

- **(a)** 5
- **(b)** 10
- **(c)** 1
- **(d)** 0
- **(e)** return 0;

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) 10**

**Why.** Inside the parentheses `<<` is the shift operator: 5 = 101₂, shifted left by 1 = 1010₂ = 10. Without the parentheses, `cout << x << 1` would print "51".

**Concept: left shift multiplies by 2.** `x << k` = x × 2ᵏ (for non-negative values that do not overflow). In C++, `<<` on a stream is the overloaded output operator; brackets decide which meaning applies.

{{< /details >}}

### 2 · Q29, assignment inside if

*Asked by: MAQ Software (TalentDecrypt test, 2025)*

What is the output of the following C++ code?

```cpp
#include <iostream>
using namespace std;

int main()
{
    int i = 16;
    for (; i; i >>= 1) {
        if (i = 5) {
            cout << "world ";
            break;
        }
        cout << i << " ";
    }
}
```

- **(a)** world
- **(b)** 16 8 world
- **(c)** 16 8 world 4 2 1
- **(d)** 16 8 world 5 4 2 1

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) world**

**Why.** `if (i = 5)` assigns 5 to i (it does not compare). The value 5 is non-zero, so on the first iteration it prints "world" and breaks.

**Concept: `=` vs `==`.** Assignment inside a condition is legal in C/C++ and the condition takes the assigned value. Compilers warn ("suggest parentheses around assignment"). Some people write `5 == i` so a typo becomes an error.

{{< /details >}}

### 3 · Q36, 7[str]

*Asked by: MathWorks (IISc 2024)*

```cpp
char str[] = "MathWorks";
cout << 7[str];
```

The output is:

- **(a)** syntax error
- **(b)** runtime error
- **(c)** Mathwork
- **(d)** none of these

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) none of these** (it prints `k`)

**Why.** `7[str]` means `*(7 + str)`, which is the same as `*(str + 7)` = `str[7]`. "MathWorks" index 7 is 'k'.

**Concept: `a[b]` is `*(a + b)`.** Addition is commutative, so `a[b]` and `b[a]` are the same thing. A curiosity, but it shows that indexing is pointer arithmetic.

{{< /details >}}

### 4 · Q41, name mangling

*Asked by: MathWorks (IISc 2024)*

How can C++ name mangling be stopped? (more than one answer)

- **(a)** It is not possible
- **(b)** By converting to pure OOP or C code
- **(c)** extern "C"
- **(d)** static "C"

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) `extern "C"`**

**Why.** `extern "C"` gives a function C linkage, so its symbol name is not mangled and C code can call it (and C++ can call C libraries).

**Concept: name mangling.** C++ supports overloading, so the compiler encodes parameter types into symbol names (e.g. `_Z3addii` for `add(int, int)`). C has no overloading and uses plain names; `extern "C"` switches to that scheme.

{{< /details >}}

### 5 · Q16, const_cast

*Asked by: NVIDIA (SSE NCG, Nov 2024)*

What is the output printed by the following program?

```cpp
#include <iostream>
using namespace std;
int main() {
    int num = 0;
    const int* cptr = &num;

    *(const_cast<int*>(cptr)) = 2;

    cout << num << endl;
}
```

- **(a)** 0
- **(b)** 2
- **(c)** Cannot say - Undefined behavior
- **(d)** Compilation Error

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) 2**

**Why.** `num` itself is not const; only the pointer gives a read-only view. Casting away that const and writing is well-defined and changes num to 2. (Writing through such a cast would be undefined if num had been declared `const int`.)

**Concept: `const_cast`.** It removes const from a pointer or reference. Safe only when the original object was not declared const; useful for calling old APIs that forgot const.

{{< /details >}}

### 6 · OOPS

*Asked by: Qualcomm (60-question online assessment)*

When a message is sent to an object that cannot handle it:

- **(a)** The system automatically generates the method
- **(b)** It is broadcast to all objects
- **(c)** The message is ignored silently
- **(d)** An exception or error occurs

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) an exception or error occurs**

**Why.** If no matching method exists, the language reports it: a compile error in statically typed languages (C++, Java), or a run-time error such as AttributeError (Python) or "does not understand" (Smalltalk). It is never generated automatically or silently ignored.

**Concept: message passing.** In OOP, calling a method is "sending a message" to an object. The object must have a method to handle it; otherwise the type system or the runtime complains.

{{< /details >}}

### 7 · OOPS

*Asked by: Qualcomm (60-question online assessment)*

class Account { private balance; updateBalance(amount) }. A subclass PromotionalAccount exposes public adjustBalance(amount) which directly modifies balance without the validation inside updateBalance(). Accounts show invalid negative balances. What encapsulation breach caused the failure?

- **(a)** Maintaining an internal cache without aligning with calling sequence
- **(b)** Adding method overloading that increases constructor parameter count
- **(c)** Using a new parameter type that expands acceptable data formats
- **(d)** Exposing an alternate path that bypasses protected validation logic

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) exposing an alternate path that bypasses protected validation logic**

**Why.** The subclass added a second public way to change `balance` that skips the checks in `updateBalance()`. The invariant (no negative balances) is no longer protected.

**Concept: encapsulation protects invariants.** All changes to internal state should go through one validated path. Subclasses should reuse that path (call the base method), not write to the field directly.

{{< /details >}}

### 8 · Q10, variables

*Asked by: Warner Bros. Discovery (HireVue, Nov 2024)*

What are the entities whose values can be changed called?

- **(a)** Constants
- **(b)** Variables
- **(c)** Modules
- **(d)** Tokens

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) variables**

**Why.** A variable is a named storage location whose value can change. Constants cannot change; modules are code units; tokens are the smallest pieces of source code.

**Concept: variables vs constants.** Use constants (`const`, `final`) for values that must not change; the compiler then catches accidental writes.

{{< /details >}}
