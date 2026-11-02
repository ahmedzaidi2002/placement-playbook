---
title: "Overloading, operators and exceptions"
weight: 7
---

2 questions asked by MathWorks. Try each one first, then open the toggle: it gives the answer, why it is right, and the idea behind it explained from scratch.

### 1 · Q8, overloading remarks

*Asked by: MathWorks (IIIT Delhi 2024)*

Choose the incorrect remarks.

- **(a)** C++ allows any operator to be overloaded
- **(b)** Some of the existing operators cannot be overloaded
- **(c)** Operator precedence cannot be changed

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a)** is the incorrect remark

**Why.** Not every operator can be overloaded (`::`, `.`, `.*`, `?:`, `sizeof` cannot). (b) and (c) are true: overloading never changes precedence or associativity.

**Concept: operator overloading rules.** You can give existing operators meaning for your types, but you cannot invent new operators, change their number of operands, or change their precedence.

{{< /details >}}

### 2 · Q24, operators that cannot be overloaded

*Asked by: MathWorks (NIT Durgapur 2024)*

Which operators cannot be overloaded in C++?

- **(a)** <<, !
- **(b)** (), []
- **(c)** ::, ?:
- **(d)** new, delete

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) `::` and `?:`**

**Why.** The operators that cannot be overloaded are `::` (scope resolution), `.` (member access), `.*` (pointer-to-member), `?:` (ternary) and `sizeof`. `<<`, `!`, `()`, `[]`, `new` and `delete` can all be overloaded.

**Concept: why some operators are fixed.** They work on names or types at compile time (`::`, `sizeof`) or must keep guaranteed behaviour (`.`, `?:`), so letting users redefine them would break the language.

{{< /details >}}
