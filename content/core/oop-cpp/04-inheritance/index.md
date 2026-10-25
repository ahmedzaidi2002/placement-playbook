---
title: "4 · Inheritance"
linkTitle: "4 Inheritance"
weight: 4
math: true
---
## 4.1 Inheritance and access {#oop-4-1}

`class Dog : public Animal` — Dog gets Animal's members and can add or override behaviour. Use it for a true **"is-a"** relationship.

How base members appear in the derived class:

| Base member | `public` inheritance | `protected` inheritance | `private` inheritance |
|---|---|---|---|
| public | public | protected | private |
| protected | protected | protected | private |
| private | **not accessible** | not accessible | not accessible |

Private base members still exist inside the derived object; they are just not accessible by name. Default inheritance: `private` for `class`, `public` for `struct`.

## 4.2 Is-a vs has-a {#oop-4-2}

- **Inheritance ("is-a"):** a `Car` is a `Vehicle`.
- **Composition ("has-a"):** a `Car` has an `Engine` (a member object).
- **Prefer composition over inheritance:** it is more flexible (swap the part at run time), avoids fragile base classes, and does not expose the base's interface. Inherit only when the subclass truly can be used wherever the base is expected (see Liskov, chapter 7).

**Types of inheritance:** single, multiple (two or more bases), multilevel (A → B → C), hierarchical (one base, many derived), hybrid (a mix).

## 4.3 Constructor chaining {#oop-4-3}

The base part is built first. To pass arguments to a base constructor, use the initialiser list: `Dog(string n) : Animal(n) {}`. Constructors and destructors are **not inherited** (C++11 `using Base::Base;` can reuse them).

## 4.4 Name hiding {#oop-4-4}

A derived function with the **same name** as base functions **hides all** base overloads with that name, even ones with different parameters.

<div class="nb nb-example">

<strong>Example</strong> (Hiding)

Base has `f(int)` and `f(string)`; Derived declares only `f(double)`. Then `d.f("hi")` is a **compile error** and `d.f(5)` calls `Derived::f(double)`. Fix: `using Base::f;` inside Derived brings the base overloads back.

</div>

## 4.5 Multiple inheritance and the diamond problem {#oop-4-5}

C++ allows a class to have several bases (Java allows only one class but many interfaces). The **diamond problem**: `B` and `C` both inherit from `A`, and `D` inherits from both `B` and `C`. `D` then contains **two copies of A**, and a call like `d.aMember` is **ambiguous**.

**Fix: virtual inheritance** (`class B : virtual public A`, same for C): D holds **one shared A**. The **most-derived class** (D) constructs the virtual base A directly.

<div class="nb nb-moral">

Public inheritance keeps access levels; private members are never accessible in derived classes. Prefer composition ("has-a") unless the subclass truly is-a base. A same-named derived function hides every base overload. The diamond is solved with virtual inheritance.

</div>
