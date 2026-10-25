---
title: "10 · Interview rapid-fire"
linkTitle: "10 Rapid-fire"
weight: 10
math: true
---
## 10.1 Basics {#oop-10-1}

1. **Four pillars?** Encapsulation, abstraction, inheritance, polymorphism.
2. **Class vs object?** Blueprint vs instance.
3. **class vs struct in C++?** Identical except default access: private for class, public for struct.
4. **Encapsulation vs abstraction?** Hiding data behind methods vs hiding complexity behind an interface.
5. **Size of an empty class?** 1 byte, so distinct objects have distinct addresses.
6. **What is `this`?** A pointer to the object a member function was called on.

## 10.2 Constructors and lifetime {#oop-10-2}

7. **Types of constructors?** Default, parameterised, copy, move.
8. **Why is the copy constructor's parameter a reference?** Passing by value would call the copy constructor again (infinite recursion).
9. **When is the copy constructor called?** Initialising from another object, passing by value, returning by value (often elided).
10. **Can a constructor be virtual? Private?** Not virtual; private yes (singleton, factory).
11. **Order of construction and destruction?** Base, members, derived; destruction in reverse.
12. **When must you use an initialiser list?** For const members, references, members without default constructors, base-class arguments.
13. **Shallow vs deep copy?** Copying pointers vs copying what they point to.
14. **Rule of three / five / zero?** Destructor, copy constructor, copy assignment (+ two moves); or write none by using RAII members.
15. **What is RAII?** Tie a resource's lifetime to an object: acquire in the constructor, release in the destructor.
16. **What does `explicit` do?** Stops implicit conversions through a one-argument constructor.

## 10.3 Inheritance and polymorphism {#oop-10-3}

17. **Public vs protected vs private inheritance?** Keeps access / makes public members protected / makes everything private.
18. **Is-a vs has-a?** Inheritance vs composition; prefer composition.
19. **Overloading vs overriding?** Same name, different parameters, compile time vs same signature, virtual, run time.
20. **How does a virtual call work?** Through the object's vptr into its class's vtable.
21. **Why a virtual destructor?** So deleting through a base pointer runs the derived destructor.
22. **What is object slicing?** Copying a derived object into a base object by value loses the derived part.
23. **Virtual call inside a constructor?** Calls the current (base) class's version.
24. **Pure virtual function and abstract class?** `= 0` with no body; a class with one cannot be instantiated.
25. **Interface in C++?** A class with only pure virtual functions and a virtual destructor.
26. **Diamond problem?** Two copies of a shared base; fix with virtual inheritance.
27. **Name hiding?** A derived function hides all base overloads with that name; fix with `using Base::f`.
28. **dynamic_cast vs static_cast?** Run-time-checked downcast for polymorphic types vs unchecked compile-time conversion.
29. **Can you overload on return type alone?** No.

## 10.4 Members, operators, memory {#oop-10-4}

30. **Static member function?** Belongs to the class, no `this`, only static members.
31. **const member function?** Cannot modify the object; callable on const objects.
32. **mutable?** A member changeable even in const functions.
33. **Is friendship inherited?** No; nor transitive nor mutual.
34. **Operators you cannot overload?** `::`, `.`, `.*`, `?:`, `sizeof`, `typeid`.
35. **Prefix vs postfix `++` overload?** `operator++()` vs `operator++(int)`; postfix returns the old value by copy.
36. **unique_ptr vs shared_ptr vs weak_ptr?** Single owner, move-only / reference-counted shared owner / non-owning observer that breaks cycles.
37. **Templates vs virtual functions?** Compile-time polymorphism (fast, code bloat) vs run-time (flexible, indirect call).
38. **Should destructors throw?** No; throwing during stack unwinding terminates the program.

## 10.5 Design {#oop-10-5}

39. **SOLID?** Single responsibility, open/closed, Liskov substitution, interface segregation, dependency inversion.
40. **Liskov violation example?** Square inheriting Rectangle, or Penguin inheriting a `fly()`.
41. **Thread-safe singleton in C++11?** Return a function-local static.
42. **Strategy vs State?** The client chooses the algorithm vs the object switches behaviour itself as its state changes.
43. **Observer?** Subject notifies all registered observers on change.
44. **Factory?** Creates objects without the caller naming the concrete class.

<div class="nb nb-moral">

Forty-four answers under twenty seconds each cover the OOP theory round; chapter 11 has the output-prediction traps.

</div>
