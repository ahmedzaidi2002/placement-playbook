---
title: "Inheritance, virtual functions and polymorphism"
weight: 1
---

13 questions asked by Fujitsu, MAQ Software, MathWorks, NVIDIA, Qualcomm, Warner Bros. Discovery. Try each one first, then open the toggle: it gives the answer, why it is right, and the idea behind it explained from scratch.

### 1 · PC Q2, inheritance types

*Asked by: Fujitsu (IIT Kharagpur 2023)*

In C++, which type of inheritance allows a class to inherit properties and behaviours
from multiple base classes?

- **(a)** Single Inheritance
- **(b)** Multiple Inheritance
- **(c)** Multilevel Inheritance
- **(d)** Hierarchical Inheritance

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) multiple inheritance**

**Why.** `class C : public A, public B` inherits from two bases at once. Multilevel is a chain (A → B → C); hierarchical is several classes deriving from one base. (Both screenshot ticks are wrong.)

**Concept: inheritance shapes.** Single (one parent), multiple (several parents), multilevel (grandparent chain), hierarchical (one parent, many children), hybrid (a mix). Multiple inheritance can cause the "diamond problem", solved in C++ with virtual inheritance.

{{< /details >}}

### 2 · Q27, virtual destructor output

*Asked by: MAQ Software (TalentDecrypt test, 2025)*

What is the output of the following C++ code?

```cpp
#include <iostream>
using namespace std;

class A {
public:
    A() {
        cout << "1";
    }
    virtual ~A() {
        cout << "2";
    }
};

class B : public A {
public:
    B() {
        cout << "3";
    }
    ~B() {
        cout << "4";
    }
};

int main() {
    A* obj;
    obj = new B;
    delete obj;
    obj = new A;
    delete obj;
    return 0;
}
```

- **(a)** 134212
- **(b)** 31412
- **(c)** 132412
- **(d)** 13212

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) 134212**

**Why.** `new B` runs constructors base-first: A (1) then B (3). `~A` is virtual, so `delete obj` (an `A*` to a B) runs ~B (4) then ~A (2). `new A` prints 1 and its delete prints 2.

**Concept: virtual destructors.** If a class may be deleted through a base pointer, give the base a virtual destructor. Without it only ~A would run (formally undefined behaviour) and B's cleanup would be skipped.

{{< /details >}}

### 3 · Q23, multiple inheritance

*Asked by: MathWorks (IIIT Delhi 2024)*

`Person(int)` prints "Person"; `Father : public Person` and `Mother :
public Person` print "Father" and "Mother" after calling `Person(x)`;
`class Child : public Father, public Mother` has

```cpp
Child(int x) : Mother(x), Father(x) {
    cout << "Child";
}
```

`main` creates
`Child child(30);`.

- **(a)** Person Father Person Mother Child
- **(b)** Child Father Mother Person Person
- **(c)** Person Father Mother Child Person
- **(d)** Compilation error

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) Person Father Person Mother Child**

**Why.** Base classes are constructed in the order they are **declared** (`Father, Mother`), not the order in the initialiser list. Each base first builds its own Person (no virtual inheritance, so there are two Person sub-objects). Then Child's body prints "Child".

**Concept: initialisation order is declaration order.** Compilers warn when the initialiser list order differs, because it is ignored. In a diamond without `virtual`, the shared grandparent is duplicated.

{{< /details >}}

### 4 · Q26, pure virtual functions

*Asked by: MathWorks (IIIT Delhi 2024); MathWorks (IIT Bombay 2024); MathWorks (NIT Delhi 2024)*

```c
class Base {
public:
    virtual void show() = 0;
    virtual void print() = 0;
};
class Derived : public Base {
public:
    void show() { cout << "Show Function in Derived class called"; }
};
int main() {
    Base obj;
    Base *b;
    Derived d;
    b = &d;
    b->show();
}
```

- **(a)** Prints "Show Function in Derived class called"
- **(b)** Error on line "b = &d;"
- **(c)** Error on line "Base obj;"
- **(d)** Error on line "Derived d;"

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) and (d)** (errors on `Base obj;` and `Derived d;`)

**Why.** Base has pure virtual functions, so it is abstract and cannot be instantiated. Derived overrides `show` but not `print`, so it is still abstract. A pointer to an abstract class is fine, so `b = &d` is not itself an error.

**Concept: abstract classes.** A class with at least one pure virtual function (`= 0`) is abstract: it defines an interface. A subclass becomes concrete only when it overrides **every** pure virtual function.

{{< /details >}}

### 5 · Q37, pure virtual declaration

*Asked by: MathWorks (IISc 2024)*

Which declares a pure virtual function?

- **(a)** pure virtual test();
- **(b)** virtual test() = 0;
- **(c)** pure: virtual test();
- **(d)** virtual test() {};

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) `virtual test() = 0;`** (with a return type in real code: `virtual void test() = 0;`)

**Why.** `= 0` after a virtual function declaration makes it pure virtual. There is no `pure` keyword in C++.

**Concept: pure virtual function.** It has no required body in the base and forces subclasses to provide one.

{{< /details >}}

### 6 · Q22, deleting through a base pointer

*Asked by: MathWorks (IIT Bombay 2024); MathWorks (IISc 2024)*

`Base` and `Derived` print "Constructing ..." in their constructors and
"Destroying ..." in their destructors; `Base`'s destructor is *not* virtual.

```cpp
Base *b = new Derived();
delete b;
```

What does this print? (CB = Constructing Base, etc.)

- **(a)** CB CD DD
- **(b)** CD CB DB
- **(c)** CD CB DD
- **(d)** CB CD DB

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) CB CD DB**

**Why.** Construction goes base first: CB, CD. `delete` through a `Base*` with a non-virtual destructor calls only ~Base (formally undefined behaviour), so DD is skipped.

**Concept: why base destructors should be virtual.** The call `delete b` picks the destructor from the pointer's static type unless it is virtual. Non-virtual → derived resources leak.

{{< /details >}}

### 7 · Q23, virtual destructor

*Asked by: MathWorks (IIT Bombay 2024)*

[cut off in the source] (the `Base` class is not visible). `Derived` prints "Constructing
Derived" and "Destructing Derived"; `main` does

```cpp
Derived *d = new Derived();
Base *b = d;
delete b;
```

- **(a)** CD
- **(b)** CB CD
- **(c)** CB CD DB
- **(d)** CB CD DD DB

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) CB CD DD DB** if Base has a virtual destructor (the likely point after the previous question); with a non-virtual one it would be (c).

**Why.** With a virtual destructor, `delete b` dispatches to ~Derived, which runs first (DD), then automatically ~Base (DB).

**Concept: destruction order.** Derived destructor body first, then members, then bases: the reverse of construction.

{{< /details >}}

### 8 · Q18, dynamic_cast chain

*Asked by: NVIDIA (SSE NCG, Nov 2024)*

What will be the output of the program?

```cpp
#include <cstdio>

class Base
{
public:
    virtual void Foo() { printf("Base::Foo()\n"); }
};
class Derived1 : public Base
{
public:
    void Foo() override { printf("Derived1::Foo()\n"); }
};
class Derived2 : public Base
{
public:
    void Foo() override { printf("Derived2::Foo()\n"); }
};
class Derived3 : public Derived1
{
public:
    void Foo() { printf("Derived3::Foo()\n"); }
};
void callFoo(Base* base)
{
    Derived1* derived1 = dynamic_cast<Derived1*>(base);
    Derived2* derived2 = dynamic_cast<Derived2*>(base);
    Derived3* derived3 = dynamic_cast<Derived3*>(base);
    if (base)
    {
        base->Foo();
    }
    if (derived1) {
        derived1->Foo();
    }
    if (derived2) {
        derived2->Foo();
    }
    if (derived3) {
        derived3->Foo();
    }
}
int main()
{
    Derived3 d;
    callFoo(static_cast<Base*>(&d));
    return 0;
}
```

- **(a)** Derived3::Foo() Derived3::Foo() Derived3::Foo() Derived3::Foo()
- **(b)** Base::Foo() Derived1::Foo() Derived2::Foo() Derived3::Foo()
- **(c)** Derived3::Foo() Derived3::Foo() Derived3::Foo()
- **(d)** Base::Foo() Derived3::Foo()

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) `Derived3::Foo()` three times**

**Why.** The object is a Derived3, which is also a Derived1 (and a Base). So `base`, `derived1` and `derived3` are non-null. Derived2 is a sibling branch, so `dynamic_cast<Derived2*>` returns nullptr. Every call is virtual and reaches Derived3::Foo.

**Concept: `dynamic_cast`.** It checks the object's real type at run time: a cast to a class the object actually is (or derives from) succeeds; otherwise it returns nullptr (for pointers). Virtual calls always go to the most-derived override, whatever the pointer's type.

{{< /details >}}

### 9 · Q44, benefits of inheritance

*Asked by: Qualcomm (IISc)*

Which are benefits of inheritance? (I) Reusability of code (II) Code sharing (III) Consistency
of interface.

- **(a)** All (I), (II) and (III)
- **(b)** Only (II) and (III)
- **(c)** Only (I) and (II)
- **(d)** Only (I)

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) all three**

**Why.** Inheritance lets subclasses reuse code (I), share common code in one base (II), and present a consistent interface, since every subclass has the base's methods (III).

**Concept: what inheritance buys.** "Is-a" relationships, reuse, and polymorphism through a common interface. Overuse makes rigid hierarchies; prefer composition when there is no true "is-a".

{{< /details >}}

### 10 · OOPS

*Asked by: Qualcomm (60-question online assessment)*

A notification system has a method sendAlert() that behaves differently for EmailAlert, SMSAlert, and PushAlert classes. Which type of polymorphism is used here?

- **(a)** Method overloading
- **(b)** Operator overloading
- **(c)** Method overriding
- **(d)** Compile-time binding

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) method overriding**

**Why.** The same `sendAlert()` signature is redefined in each subclass and chosen at run time from the object's type: run-time polymorphism by overriding. Overloading would mean different parameter lists.

**Concept: two kinds of polymorphism.** Compile-time: function and operator overloading, templates. Run-time: virtual functions / overriding, where a base reference calls the right subclass method.

{{< /details >}}

### 11 · Inheritance

*Asked by: Qualcomm (Delhi campus 2024, Q55)*

The figure shows two classes: **Class B → Class A** (B is derived from A, and nothing else is involved). What type of inheritance is this?

- **(a)** Multilevel inheritance
- **(b)** Single inheritance
- **(c)** Multiple inheritance
- **(d)** Hybrid inheritance

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) single inheritance**

**Why.** One base (A) and one derived class (B). Multilevel needs a chain (C → B → A); multiple needs one class with two or more bases; hybrid mixes these.

**Concept: inheritance types.** See the multiple-inheritance question above for the full list.

{{< /details >}}

### 12 · Interfaces (Java)

*Asked by: Qualcomm (NIT Durgapur, Q46)*

Which one of the statements given in the options is **false**?

- **(a)** An interface that is declared within the body of a class or interface is known as a nested interface.
- **(b)** A class declaration can be a member of an interface.
- **(c)** A constant can be a member of an interface.
- **(d)** If an interface is named in the implements clause of a class, then the class must implement all of the methods declared within the interface.

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d)** is false

**Why.** An **abstract** class can implement an interface and leave some of its methods unimplemented; only a concrete class must implement all of them (and since Java 8, `default` methods need no implementation). (a)–(c) are true: nested interfaces exist, interfaces can declare member classes, and interface fields are implicitly `public static final` constants.

**Concept: Java interfaces.** A contract of methods. Fields are constants; methods are abstract unless `default` or `static`. A class can implement many interfaces but extend only one class.

{{< /details >}}

### 13 · Q22, code reusability

*Asked by: Warner Bros. Discovery (HireVue, Nov 2024)*

Which of the following object-oriented programming features describes code reusability?

- **(a)** Encapsulation
- **(b)** Abstraction
- **(c)** Polymorphism
- **(d)** Inheritance

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) inheritance**

**Why.** A subclass reuses the fields and methods of its superclass instead of rewriting them.

**Concept: the four OOP pillars.** Encapsulation (hide data behind methods), abstraction (show only what matters), inheritance (reuse via is-a), polymorphism (one interface, many behaviours).

{{< /details >}}
