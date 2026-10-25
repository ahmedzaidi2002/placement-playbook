---
title: "3 · Static, const, friend and operator overloading"
linkTitle: "3 Members and operators"
weight: 3
math: true
---
## 3.1 static members {#oop-3-1}

- A **static data member** is shared by all objects of the class (one copy), e.g. an object counter. It must be defined once outside the class (or declared `inline static` in C++17).
- A **static member function** belongs to the class, not an object: no `this`, so it can access only static members. Call it as `A::count()`.

<div class="nb nb-example">

<strong>Example</strong> (Counting objects)

`static int n;` incremented in the constructor and decremented in the destructor: after `A a, b; { A c; }` the count is **2** (c was destroyed at the end of its block).

</div>

## 3.2 const and mutable {#oop-3-2}

- A **const member function** (`int get() const`) promises not to modify the object; it is the only kind you can call on a `const` object or through a `const&`.
- **Const-correctness:** mark everything that does not modify as `const`; pass large objects as `const T&`.
- **`mutable`** members can be changed even inside const functions (caches, counters, mutexes).

## 3.3 friend {#oop-3-3}

A **friend** function or class can access a class's private members. Used for operators that need both operands' internals (`operator<<`). Friendship is **not inherited, not transitive, and not mutual** (if A is B's friend, B is not automatically A's friend). Use it sparingly: it weakens encapsulation.

## 3.4 Operator overloading {#oop-3-4}

Give operators meaning for your types: `Complex a + b`, `cout << point`.

| Write it as | When |
|---|---|
| **Member** | the left operand is your object: `+=`, `[]`, `()`, `->`, unary operators |
| **Non-member** (often friend) | the left operand is not your type (`cout << obj`), or for symmetric binary operators (`a + b` should also allow `5 + a`) |

- **Must be members:** `=`, `[]`, `()`, `->`.
- **Cannot be overloaded:** `::`, `.`, `.*`, `?:`, `sizeof`, `typeid`.
- You cannot create new operators or change precedence or the number of operands.
- **Prefix vs postfix increment:** `A& operator++()` (prefix, returns the new value by reference) vs `A operator++(int)` (postfix: the dummy `int` marks it; returns the old value by copy, so it is slower).
- `operator<<` returns `ostream&` so calls chain: `cout << a << b`.

<div class="nb nb-moral">

static = one per class (no this); const functions are callable on const objects; mutable escapes const; friends see privates but friendship is not inherited. `=`, `[]`, `()`, `->` must be members; `::`, `.`, `?:`, `sizeof` cannot be overloaded.

</div>
