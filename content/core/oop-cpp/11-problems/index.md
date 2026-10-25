---
title: "11 · Practice: output and concept questions"
linkTitle: "11 Practice"
weight: 11
math: true
---
Twelve questions in the shapes OAs use: "what does this print?" on tiny snippets, and concept multiple-choice. Assume `#include <iostream>` and `using namespace std;`.

<div class="nb nb-problem nb-block" id="problem-oop-1">

<strong>Problem 1</strong> (Construction order)

```cpp
struct M { M(){cout<<"M";} ~M(){cout<<"m";} };
struct A { A(){cout<<"A";} ~A(){cout<<"a";} };
struct B : A { M m; B(){cout<<"B";} ~B(){cout<<"b";} };
int main(){ B b; }
```

<details class="nb-sol">
<summary>Solution</summary>

**`AMBbma`**: base A, then member M, then B's body; destruction exactly reversed.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-oop-2">

<strong>Problem 2</strong> (Missing virtual destructor)

```cpp
struct Base { ~Base(){cout<<"~B";} };
struct Der : Base { ~Der(){cout<<"~D";} };
int main(){ Base* p = new Der; delete p; }
```

<details class="nb-sol">
<summary>Solution</summary>

Prints **`~B`** only: `~Base` is not virtual, so `~Der` never runs (undefined behaviour; leaks whatever Der owns). With `virtual ~Base()` it prints `~D~B`.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-oop-3">

<strong>Problem 3</strong> (Slicing)

```cpp
struct B { virtual void show(){cout<<"B";} };
struct D : B { void show() override {cout<<"D";} };
void byValue(B b){ b.show(); }
void byRef(B& b){ b.show(); }
int main(){ D d; byValue(d); byRef(d); }
```

<details class="nb-sol">
<summary>Solution</summary>

**`BD`**: passing by value slices `d` into a plain `B`; passing by reference keeps the real type.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-oop-4">

<strong>Problem 4</strong> (Default argument)

```cpp
struct B { virtual void f(int x = 1){cout<<"B"<<x;} };
struct D : B { void f(int x = 2) override {cout<<"D"<<x;} };
int main(){ B* p = new D; p->f(); }
```

<details class="nb-sol">
<summary>Solution</summary>

**`D1`**: the function is chosen at run time (D's), but the default argument is taken from the static type (B's).

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-oop-5">

<strong>Problem 5</strong> (Virtual call in a constructor)

```cpp
struct B { B(){ hello(); } virtual void hello(){cout<<"B";} };
struct D : B { void hello() override {cout<<"D";} };
int main(){ D d; }
```

<details class="nb-sol">
<summary>Solution</summary>

**`B`**: while B's constructor runs, the object is still only a B, so the base version is called.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-oop-6">

<strong>Problem 6</strong> (Name hiding)

```cpp
struct B { void f(int){cout<<"Bint";} };
struct D : B { void f(double){cout<<"Ddouble";} };
int main(){ D d; d.f(5); }
```

<details class="nb-sol">
<summary>Solution</summary>

**`Ddouble`**: `D::f` hides `B::f`, so 5 is converted to double. With `using B::f;` in D, it would print `Bint`.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-oop-7">

<strong>Problem 7</strong> (Static counter)

```cpp
struct A { static int n; A(){n++;} ~A(){n--;} };
int A::n = 0;
int main(){ A a, b; { A c; cout << A::n; } cout << A::n; }
```

<details class="nb-sol">
<summary>Solution</summary>

**`32`**: three objects inside the block, then `c` is destroyed.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-oop-8">

<strong>Problem 8</strong> (Overloading)

Which pair of declarations is **not** a valid overload? (a) `void f(int); void f(double);` (b) `void f(int); int f(int);` (c) `void f(int); void f(int, int);` (d) `void f(int&); void f(const int&);`

<details class="nb-sol">
<summary>Solution</summary>

**(b)**: they differ only in return type.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-oop-9">

<strong>Problem 9</strong> (Abstract classes)

Which are true? (a) An abstract class can have a constructor. (b) You can create an object of an abstract class. (c) You can have a pointer to an abstract class. (d) A derived class that does not override all pure virtual functions is also abstract.

<details class="nb-sol">
<summary>Solution</summary>

**(a), (c), (d)**.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-oop-10">

<strong>Problem 10</strong> (Diamond)

`B` and `C` inherit from `A` (which has `int x`), `D` inherits from `B` and `C`. Without virtual inheritance, how many `A` subobjects does a `D` contain, and what happens on `d.x`? With virtual inheritance?

<details class="nb-sol">
<summary>Solution</summary>

Without: **two** A subobjects; `d.x` is **ambiguous** (compile error; write `d.B::x`). With `virtual public A` in both B and C: **one** shared A, and `d.x` works.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-oop-11">

<strong>Problem 11</strong> (Smart pointers)

`shared_ptr<Node> a = make_shared<Node>(); shared_ptr<Node> b = make_shared<Node>(); a->next = b; b->next = a;` where `next` is a `shared_ptr`. What goes wrong when `a` and `b` go out of scope, and the fix?

<details class="nb-sol">
<summary>Solution</summary>

Each node's count stays at 1 (held by the other): **neither is freed**, a memory leak. Make one link a `weak_ptr`.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-oop-12">

<strong>Problem 12</strong> (Pick the pattern)

(a) A payment screen must support card, UPI and wallet, chosen by the user. (b) Several dashboards must update whenever a stock price changes. (c) An old payment SDK must be used through your `PaymentProcessor` interface. (d) Exactly one configuration object for the whole app.

<details class="nb-sol">
<summary>Solution</summary>

(a) **Strategy**. (b) **Observer**. (c) **Adapter**. (d) **Singleton**.

</details>

</div>
