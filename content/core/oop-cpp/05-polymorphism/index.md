---
title: "5 · Polymorphism and virtual functions"
linkTitle: "5 Polymorphism"
weight: 5
math: true
---
## 5.1 Compile-time vs run-time polymorphism {#oop-5-1}

| | Compile-time (static) | Run-time (dynamic) |
|---|---|---|
| How | **function overloading**, operator overloading, **templates** | **virtual functions** + base pointers/references |
| Decided by | the compiler, from argument types | the actual object type, at run time (vtable) |
| Cost | none | an indirect call |

## 5.2 Overloading vs overriding {#oop-5-2}

| | Overloading | Overriding |
|---|---|---|
| Where | same scope (same class) | base and derived class |
| Signature | **different** parameters | **same** signature |
| Needs `virtual`? | no | yes (in the base) |
| Resolved | compile time | run time |

Overloads cannot differ **only** by return type. Mark overrides with **`override`** so the compiler catches a signature mismatch; **`final`** stops further overriding (or inheritance).

## 5.3 How virtual calls work {#oop-5-3}

Each class with virtual functions has a **vtable** (one per class): an array of pointers to its versions of the virtual functions. Each object of such a class holds a hidden **vptr** pointing to its class's vtable. A call `p->speak()` loads the vptr, indexes the vtable and calls whatever function is there: the **derived** version if `p` points to a derived object.

<div class="nb nb-example">

<strong>Example</strong> (Dynamic dispatch)

```cpp
struct Animal { virtual void speak(){ cout << "..."; } };
struct Dog : Animal { void speak() override { cout << "Woof"; } };
Animal* p = new Dog; p->speak();
```

Prints **Woof**. Without `virtual`, it would print `...` (the call is chosen by the pointer type).

</div>

## 5.4 Virtual destructors {#oop-5-4}

If a class will be deleted through a base pointer, its base **destructor must be virtual**. Otherwise `Base* p = new Derived; delete p;` runs only `~Base()`: the derived part is never cleaned up (**undefined behaviour**, typically a leak). Rule: a class with any virtual function should have a virtual destructor.

## 5.5 The classic traps {#oop-5-5}

- **Object slicing:** copying a `Derived` into a `Base` **by value** (assignment, or passing to a function taking `Base`) keeps only the base part, and virtual calls on the copy use the base version. Pass by reference or pointer.
- **Virtual call inside a constructor or destructor** calls the **current class's** version, not the derived one (the derived part does not exist yet / any more).
- **Default arguments are bound statically:** with `virtual void f(int x = 1)` in the base and `void f(int x = 2) override` in the derived, `Base* p = new Derived; p->f();` runs the **derived** function with the **base's** default: prints with **1**.
- **Constructors cannot be virtual** (there is no object, so no vptr, yet).

## 5.6 Abstract classes and interfaces {#oop-5-6}

- A **pure virtual function** `virtual double area() = 0;` has no implementation in the base and must be overridden.
- A class with at least one pure virtual function is **abstract**: it cannot be instantiated, but you can have pointers and references to it, and it can have constructors, data and normal methods.
- An **interface** in C++ = a class with only pure virtual functions (and a virtual destructor). A derived class that does not override every pure virtual function is still abstract.

## 5.7 Casts and RTTI {#oop-5-7}

| Cast | Use |
|---|---|
| `static_cast` | ordinary conversions known at compile time (int ↔ double, upcasts, unchecked downcasts) |
| `dynamic_cast` | **safe downcast** of polymorphic types, checked at run time: `nullptr` for a bad pointer cast, `std::bad_cast` for a bad reference |
| `const_cast` | add or remove `const` |
| `reinterpret_cast` | reinterpret bits (pointer ↔ integer); low-level and dangerous |

`dynamic_cast` and `typeid` use **RTTI** (run-time type information), available only for classes with virtual functions.

<div class="nb nb-moral">

Overloading = same name, different parameters, compile time; overriding = same signature, virtual, run time through the vtable. Make base destructors virtual. Watch slicing, virtual calls in constructors, and statically bound default arguments.

</div>
