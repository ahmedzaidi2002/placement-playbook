---
title: "1 · The four pillars, classes and objects"
linkTitle: "1 Pillars and classes"
weight: 1
math: true
---
## 1.1 Why OOP {#oop-1-1}

Object-oriented programming bundles **data** and the **functions that work on it** into objects, so each part of a program guards its own data and exposes only a small interface. It makes large programs easier to change and reason about, and models real-world entities naturally (an `Account` with `deposit` and `withdraw`).

<div class="nb nb-definition">

<strong>Definition</strong> — A **class** is a blueprint (a user-defined type); an **object** is an instance of it with its own data in memory. A class uses no memory for data until objects are created.

</div>

## 1.2 The four pillars {#oop-1-2}

| Pillar | Meaning | C++ tool | Example |
|---|---|---|---|
| **Encapsulation** | bundle data with methods and **hide** the data | `private` members + public methods | `balance` is private; only `deposit()` changes it, and it rejects negative amounts |
| **Abstraction** | expose **what** an object does, hide **how** | abstract classes, interfaces, headers | a `Shape` with `area()`; callers do not care how a circle computes it |
| **Inheritance** | a new class **reuses** and extends an existing one ("is-a") | `class Dog : public Animal` | `SavingsAccount` is an `Account` with interest |
| **Polymorphism** | one interface, **many behaviours** | overloading, templates (compile time); `virtual` (run time) | `shape->area()` calls the right version for each shape |

<div class="nb nb-remark">

<strong>Encapsulation vs abstraction</strong> — Encapsulation is about **protecting** data (access control, keeping an invariant like "balance ≥ 0" true). Abstraction is about **simplifying** the interface (hiding complexity). Encapsulation is one way to achieve abstraction.

</div>

## 1.3 class vs struct, access specifiers {#oop-1-3}

- `public`: accessible everywhere. `private`: only inside the class (and friends). `protected`: inside the class and derived classes.
- In C++, `class` and `struct` are the **same** except for defaults: `class` members and inheritance are **private** by default; `struct` ones are **public**. Convention: `struct` for plain data, `class` for types with invariants.

## 1.4 The this pointer {#oop-1-4}

Inside a non-static member function, `this` points to the object the function was called on. Uses: disambiguate a parameter with the same name as a member (`this->x = x;`), return `*this` for chaining (`a.setX(1).setY(2)`), and pass the object to another function. Static member functions have no `this`.

## 1.5 Object size {#oop-1-5}

- An **empty class has size 1**, so that two distinct objects have different addresses.
- Size = members + **padding** for alignment: `class { char c; int i; }` is 8 bytes, not 5.
- A class with at least one virtual function also holds a hidden **vptr** (8 bytes on a 64-bit system).
- Member functions do **not** take space in objects; static data members are not part of the object either.

<div class="nb nb-moral">

Encapsulation hides data behind methods, abstraction hides complexity behind an interface, inheritance reuses ("is-a"), polymorphism lets one call do the right thing per type. class = struct with private defaults.

</div>
