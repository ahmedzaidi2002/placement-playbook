---
title: "Constructors, destructors and copy semantics"
weight: 4
---

4 questions asked by Fujitsu, MathWorks, NVIDIA, Qualcomm. Try each one first, then open the toggle: it gives the answer, why it is right, and the idea behind it explained from scratch.

### 1 · PC Q3, const member function

*Asked by: Fujitsu (IIT Kharagpur 2023)*

What does the `const` keyword indicate when used in a C++ (member) function
declaration, as in `int get() const;`?

- **(a)** The function cannot be called
- **(b)** The function is a constructor.
- **(c)** The function does not modify the object it is called on.
- **(d)** The function is a destructor.

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) the function does not modify the object it is called on**

**Why.** In `int get() const;`, `this` becomes a pointer to const, so the function cannot change data members (except `mutable` ones). Only const member functions can be called on a const object. (The screenshot ticks (a), which is wrong.)

**Concept: const-correctness.** Mark every member function that only reads as `const`. Then const objects and const references can use it, and the compiler stops accidental changes.

{{< /details >}}

### 2 · Q42, conversion constructors

*Asked by: MathWorks (IISc 2024); MathWorks (IIIT Delhi 2024)*

Which are true about conversion constructors in C++? (more than one answer)

- **(a)** They can convert the data types of public variables
- **(b)** A conversion constructor accepts one argument of a different type
- **(c)** Conversion constructors do not exist in C++
- **(d)** A conversion constructor can do the job of the destructor

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b)**

**Why.** A constructor that can be called with one argument of another type (and is not `explicit`) lets the compiler convert that type implicitly: `A a = 5;` calls `A(int)`.

**Concept: converting constructors and `explicit`.** Implicit conversions can hide bugs (`f(5)` silently building an `A`). Mark single-argument constructors `explicit` unless you want the conversion.

{{< /details >}}

### 3 · Q20, construction and destruction order

*Asked by: NVIDIA (SSE NCG, Nov 2024)*

What is the output printed by the following program? (Each option is six or four lines;
they are abbreviated here.)

```cpp
#include <iostream>
using namespace std;

class A {
public:
    A() { cout << "Constructor for A Called" << endl; }
    ~A() { cout << "Destructor for A Called" << endl; }
};

class B {
public:
    B() { cout << "Constructor for B Called" << endl; }
    virtual ~B() { cout << "Destructor for B Called" << endl; }
};

class C : public B {
    B a;
public:
    C() { cout << "Constructor for C Called" << endl; }
    ~C() {
        cout << "Destructor for C Called" << endl;
    }
};

int main() {
    B* b = new C();
    delete b;
}
```

- **(a)** Constructor for A, A, C; Destructor for C, A, A
- **(b)** Constructor for C, B; Destructor for C, B
- **(c)** Constructor for B, B, C; Destructor for C, B, B
- **(d)** Constructor for B, C; Destructor for C, B

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) Constructor for B, B, C; Destructor for C, B, B**

**Why.** C derives from B and has a member `B a`. Building a C: base class first (B), then members (B for `a`), then C's own body (C). Class A is never used. `~B` is virtual, so `delete b` through a `B*` runs ~C, then destroys the member (B), then the base (B).

**Concept: construction and destruction order.** Construct: bases (in declaration order) → members (in declaration order) → constructor body. Destroy: exactly the reverse. Deleting through a base pointer only does this correctly if the base destructor is virtual.

{{< /details >}}

### 4 · Q57, several constructors

*Asked by: Qualcomm (Nov 2024); Qualcomm (Delhi campus 2024, Q54)*

Defining more than one constructor with differing parameter lists in the same class is known
as:

- **(a)** Constructor chaining
- **(b)** Constructor overloading
- **(c)** Constructor overriding
- **(d)** Constructor hiding

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) constructor overloading**

**Why.** Same name, different parameter lists, chosen at compile time: overloading. Constructors are not inherited, so they cannot be overridden. Chaining is one constructor calling another (`this(...)` in Java, delegating constructors in C++).

**Concept: overloading vs overriding.** Overloading: same name, different parameters, same scope, compile-time choice. Overriding: same signature in a subclass, run-time choice through virtual dispatch.

{{< /details >}}
