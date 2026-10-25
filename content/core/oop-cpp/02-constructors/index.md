---
title: "2 · Constructors, destructors and copying"
linkTitle: "2 Constructors and copying"
weight: 2
math: true
---
## 2.1 Kinds of constructor {#oop-2-1}

A **constructor** has the class's name, no return type, and runs when an object is created.

| Constructor | Signature | Called when |
|---|---|---|
| **Default** | `A()` | `A a;` |
| **Parameterised** | `A(int x)` | `A a(5);` |
| **Copy** | `A(const A& other)` | `A b = a;`, pass by value, return by value |
| **Move** | `A(A&& other)` | from a temporary, or `std::move(a)` |

- If you write **no** constructor, the compiler generates a default one. If you write **any** constructor, the default one is no longer generated.
- The copy constructor's parameter **must be a reference**: taking it by value would need a copy to make the copy (infinite recursion).
- Constructors **cannot be virtual**; they can be overloaded, and can be `private` (singletons, factories).

## 2.2 Member initialiser lists {#oop-2-2}

```cpp
class Point {
    const int x; int& ref;
public:
    Point(int a, int& r) : x(a), ref(r) {}   // initialised, not assigned
};
```

The list is **required** for `const` members, **reference** members, members without a default constructor, and to pass arguments to a base-class constructor. Members are initialised in **declaration order**, not the order written in the list.

**`explicit`** on a one-argument constructor stops implicit conversions: with `explicit A(int)`, writing `A a = 5;` or passing `5` to a function taking `A` is an error.

## 2.3 Destructors and order {#oop-2-3}

A **destructor** `~A()` runs when an object goes out of scope or is `delete`d; it releases resources. One per class, no parameters, cannot be overloaded.

**Order:** construction is **base → members (in declaration order) → derived body**; destruction is the **exact reverse**. Local objects are destroyed in reverse order of creation.

<div class="nb nb-example">

<strong>Example</strong> (What does it print?)

```cpp
struct A { A(){cout<<"A";} ~A(){cout<<"a";} };
struct B : A { B(){cout<<"B";} ~B(){cout<<"b";} };
int main(){ B b; }
```

Prints **`ABba`**: base constructor first, derived destructor first.

</div>

## 2.4 Shallow vs deep copy {#oop-2-4}

The compiler's default copy copies each member **bitwise** (a **shallow copy**). If a member is a raw pointer to owned memory, both objects now point to the same buffer, and both destructors `delete` it → **double free**, or one object's changes show up in the other.

A **deep copy** allocates new memory and copies the contents. Write it in the copy constructor and the copy-assignment operator (or avoid the problem entirely with `std::vector`, `std::string`, smart pointers).

## 2.5 Rule of three, five and zero {#oop-2-5}

- **Rule of three:** if a class needs a custom **destructor**, **copy constructor** or **copy assignment**, it needs all three (it manages a resource).
- **Rule of five** (C++11): add the **move constructor** and **move assignment**, which steal the resource from a temporary instead of copying it (fast).
- **Rule of zero:** best of all, manage resources with RAII members (`vector`, `unique_ptr`) and write **none** of the five.

**Copy assignment** must handle self-assignment (`a = a`) and free the old resource; the **copy-and-swap** idiom (take the parameter by value, swap) does both and is exception-safe.

## 2.6 Copy elision and RAII {#oop-2-6}

- **Copy elision / RVO:** when a function returns a local object, the compiler builds it directly in the caller's variable: no copy, no move (guaranteed for temporaries since C++17). So copy-constructor print statements often run fewer times than you expect.
- **RAII** (Resource Acquisition Is Initialization): acquire a resource in a constructor and release it in the destructor, so it is released automatically when the object goes out of scope, even if an exception is thrown. `std::lock_guard` (mutex), `std::fstream` (file), smart pointers (memory) are RAII.

<div class="nb nb-moral">

Initialise const and reference members in the initialiser list. Build base → members → derived, destroy in reverse. Raw owning pointers need a deep copy (rule of three/five); better, use RAII members and write nothing (rule of zero).

</div>
