---
title: "1.15 · Interview rapid-fire"
linkTitle: "1.15 Interview rapid-fire"
weight: 15
math: true
---
<div class="nb-proto">

<em><span>Prototypical example for this section:</span> “What is the difference between overloading and overriding?”, answered in two lines.</em>

</div>

Short answers to the questions that come up again and again, grouped by topic. Each answer points back to the section that explains it.

## 1.15.i Basics {#s1-15-i}

1. <strong>What are the four pillars of OOP?</strong><br>Encapsulation, abstraction, inheritance and polymorphism ([Section 1.1](../01-why/)).
2. <strong>Class vs object?</strong><br>A class is a type (a blueprint); an object is a value of that type occupying memory.
3. <strong>`struct` vs `class` in C++?</strong><br>Only the default access: `public` for `struct`, `private` for `class`, for both members and base classes.
4. <strong>Encapsulation vs abstraction?</strong><br>Abstraction decides what to expose; encapsulation enforces that nothing else is reachable.
5. <strong>What is `sizeof` an empty class?</strong><br>Nonzero ($1$ with g++), so that distinct objects have distinct addresses; an empty <em>base</em> may take zero bytes (EBO).
6. <strong>Can a member function of a class read private members of another object of the same class?</strong><br>Yes. Access control is per class, not per object.
7. <strong>What is `this`? Can you `delete this`?</strong><br>A pointer to the object a member function was called on. `delete this` is legal only if the object was allocated with `new` and is not used afterwards; it is rarely a good idea.

## 1.15.ii Constructors and lifetime {#s1-15-ii}

8. <strong>Can a constructor be virtual?</strong><br>No. The object’s dynamic type is being decided by the constructor; there is no vtable to dispatch through yet. Use a virtual `clone()` or a factory for “virtual construction”.
9. <strong>Can a constructor be private? Why?</strong><br>Yes: to force creation through a factory or a singleton’s `instance()`, or to forbid creation entirely.
10. <strong>Why does the copy constructor take a reference?</strong><br>By value, passing the argument would itself need a copy: infinite recursion ([Section 1.3](../03-lifecycle/)).
11. <strong>Copy constructor vs copy assignment?</strong><br>The constructor makes a new object; assignment overwrites an existing one and must free what it already holds. `T b = a;` is construction, `b = a;` is assignment.
12. <strong>In what order are members initialised?</strong><br>Bases in declaration order, then members in declaration order, then the constructor body; the initialiser list’s order is ignored.
13. <strong>When must you use the initialiser list?</strong><br>For `const` and reference members, members without a default constructor, and base classes needing arguments.
14. <strong>What is the Rule of Three / Five / Zero?</strong><br>Need one of destructor, copy constructor, copy assignment and you need all three (five with the moves); better, need none by letting members manage resources.
15. <strong>What does `std::move` do?</strong><br>Nothing at run time: it casts to an rvalue reference so that the move overload is chosen.
16. <strong>What is RAII?</strong><br>Acquire a resource in a constructor and release it in the destructor, so scope exit, including by exception, always releases it.
17. <strong>What is copy elision / RVO?</strong><br>The compiler constructs a returned object directly in the caller, skipping the copy or move; mandatory for returned temporaries since C++17.
18. <strong>What does `explicit` do?</strong><br>Stops a single-argument constructor from being used as a silent conversion.
19. <strong>`= default` vs `= delete`?</strong><br>`= default` asks for the compiler-generated version; `= delete` forbids the function (for example, copying).

## 1.15.iii Inheritance and polymorphism {#s1-15-iii}

20. <strong>Overloading vs overriding?</strong><br>Overloading: same name, different parameters, same scope, resolved at compile time. Overriding: a derived class redefines a `virtual` function with the same signature, resolved at run time.
21. <strong>Overriding vs hiding?</strong><br>Hiding happens when a derived class declares <em>any</em> function with the same name as a base one that is not an override: the base versions disappear from lookup ([Section 1.6](../06-inheritance/)).
22. <strong>Early vs late binding?</strong><br>Early: the call is fixed at compile time from the static type. Late: chosen at run time from the dynamic type, for virtual calls through pointers or references.
23. <strong>How are virtual functions implemented?</strong><br>Usually a vtable per class and a vptr per object; a virtual call loads the vptr, then the slot, then calls indirectly. The standard does not require this.
24. <strong>Why a virtual destructor?</strong><br>Deleting a derived object through a base pointer is undefined behaviour otherwise; in practice the derived destructor is skipped.
25. <strong>What is object slicing?</strong><br>Copying a derived object into a base object keeps only the base part, including the base’s vptr.
26. <strong>What does a virtual call in a constructor do?</strong><br>Calls the version of the class being constructed, never a more derived one.
27. <strong>What is an abstract class? An interface?</strong><br>A class with at least one pure virtual function; it cannot be instantiated. An interface is an abstract class with only pure virtual functions and no data.
28. <strong>Can a pure virtual function have a body?</strong><br>Yes; derived classes can call it explicitly. A pure virtual destructor must have one.
29. <strong>Can static functions be virtual?</strong><br>No: they have no object to dispatch on.
30. <strong>What is the diamond problem?</strong><br>Two paths to the same base give two copies of it; `virtual` inheritance shares one, constructed by the most derived class.
31. <strong>Public vs protected vs private inheritance?</strong><br>Public models is-a; the other two cap the access of inherited members and hide the base from outside code ([Section 1.6](../06-inheritance/)).
32. <strong>Composition vs inheritance?</strong><br>Has-a vs is-a. Prefer composition unless you need substitutability.
33. <strong>`dynamic_cast` vs `static_cast`?</strong><br>`dynamic_cast` checks at run time (polymorphic types only) and returns `nullptr` or throws; `static_cast` trusts you.
34. <strong>What are `override` and `final`?</strong><br>`override` makes the compiler check that the function really overrides; `final` forbids further overriding or derivation.
35. <strong>Are default arguments of virtual functions dynamic?</strong><br>No, they come from the static type ([Section 1.7](../07-polymorphism/)).

## 1.15.iv Members, operators and memory {#s1-15-iv}

36. <strong>Static member vs normal member?</strong><br>One copy per class vs one per object; static functions have no `this`.
37. <strong>What is a `const` member function? `mutable`?</strong><br>It promises not to change the object and is the only kind callable on `const` objects; `mutable` members may change anyway (caches).
38. <strong>Does `friend` break encapsulation?</strong><br>No more than a member does: the class chooses its friends. Friendship is not inherited, transitive or mutual.
39. <strong>Which operators cannot be overloaded?</strong><br>`::`, `.`, `.*`, `?:`, `sizeof`, `alignof`, `typeid`.
40. <strong>Prefix vs postfix `++` for classes?</strong><br>Postfix takes a dummy `int` and returns a copy of the old value, so prefix is cheaper.
41. <strong>`unique_ptr` vs `shared_ptr` vs `weak_ptr`?</strong><br>One owner (move-only, no overhead); shared owners (reference count); a non-owning observer of a `shared_ptr` that breaks cycles.
42. <strong>Why `make_shared`?</strong><br>One allocation for object and control block, and no leak window between `new` and the smart pointer.
43. <strong>Shallow vs deep copy?</strong><br>Copying pointers vs copying what they point to.
44. <strong>Can a destructor throw?</strong><br>It should not; destructors are `noexcept` by default, and a throw during unwinding calls `std::terminate`.
45. <strong>Why mark move constructors `noexcept`?</strong><br>Otherwise `std::vector` copies instead of moving when it reallocates ([Section 1.11](../11-exceptions/)).

## 1.15.v Design {#s1-15-v}

46. <strong>What is SOLID?</strong><br>Single responsibility, open/closed, Liskov substitution, interface segregation, dependency inversion ([Section 1.12](../12-solid/)).
47. <strong>Why is a square not a rectangle in code?</strong><br>A `Rectangle`’s `setWidth` promises not to change the height; a `Square` cannot keep that promise, so it is not substitutable.
48. <strong>Singleton: how and why not?</strong><br>A function-local static (thread-safe since C++11); it hides dependencies and hinders testing, so pass objects in instead where possible.
49. <strong>Strategy vs inheritance of the whole class?</strong><br>Strategy varies one behaviour by composition and can change at run time; subclassing fixes it at creation and multiplies classes.
50. <strong>Templates vs virtual functions?</strong><br>Compile time, zero overhead, one type at a time vs run time, a small overhead, mixed types in one container.

## 1.15.vi Output traps {#s1-15-vi}

51. <strong>Does `std::cout << f() << g();` call `f` first?</strong><br>Not necessarily before C++17: the order of evaluating the operands was unspecified. This chapter’s compiler, in C++14 mode, evaluated them right to left, which is how the listing below printed “computed 0 time(s)” although the three calls to `length()` are written first.

```cpp {filename="eval-order-trap.cpp"}
#include <cmath>
#include <iostream>

// A route whose length is expensive to compute, so it is cached.
class Route {
public:
    Route(double dx, double dy) : dx_(dx), dy_(dy) {}
    double length() const {                 // logically read-only
        if (!cached_) {
            ++computations_;
            length_ = std::sqrt(dx_ * dx_ + dy_ * dy_);
            cached_ = true;                 // allowed: member is mutable
        }
        return length_;
    }
    int computations() const { return computations_; }
private:
    double dx_, dy_;
    mutable double length_ = 0;             // cache: not part of the
    mutable bool cached_ = false;           // object's observable state
    mutable int computations_ = 0;
};

int main() {
    const Route r(3, 4);
    std::cout << r.length() << " " << r.length() << " " << r.length()
              << ", computed " << r.computations() << " time(s)\n";
}
```

```text {filename="Output (MinGW g++ 6.3.0, -std=c++14, 32-bit)"}
5 5 5, computed 0 time(s)
```

C++17 fixed the order for `<<`: left to right. The safe habit in any standard is to call functions with side effects in separate statements, as `mutable-cache.cpp` in [Section 1.4](../04-members/) does.
