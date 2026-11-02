@@ mw-iitb-8
**Answer: (b) size greater than zero** (sizeof is 1)

**Why.** Objects of an empty class can be created. Every object must have a distinct address, so C++ gives an empty class a size of at least 1 byte. (The candidate's "compilation error" is wrong.)

**Concept: object identity.** Two different objects must never share an address, so nothing can be 0 bytes. (As a base class, an empty class can take 0 bytes, the "empty base optimisation".)

@@ qc-iisc-ocp
**Answer: (d) Open-Closed Principle**

**Why.** "Open for extension, closed for modification" is exactly the O in SOLID: add new behaviour by adding code (a new subclass or plug-in), not by editing tested code.

**Concept: SOLID.**
- **S**ingle responsibility: one reason to change per class.
- **O**pen–closed: extend without modifying.
- **L**iskov substitution: a subclass must work wherever its base works.
- **I**nterface segregation: many small interfaces beat one large one.
- **D**ependency inversion: depend on abstractions, not concrete classes.

@@ qcc-oop-03
**Answer: (a) private**

**Why.** `private` restricts access to members of the same class. `protected` would also open it to subclasses (and, in Java, the package). `transient` is not an access modifier; it marks a field to skip during serialisation.

**Concept: access levels.** public: everyone. protected: the class and its subclasses (plus the package in Java). private: the class only. (Java's default, no keyword: the package.)

@@ qcc-oop-04
**Answer: (b) all three**

**Why.** A static method belongs to the class (I), can be called as `ClassName.method()` without an object (II), and can read and change static data (III). It has no `this`, so it cannot use instance members directly.

**Concept: static members.** One copy per class, shared by all objects. Static methods are like global functions scoped inside the class.

@@ ti-sizeof-class
**Answer: as written it does not compile; with the intended `temp *node` and `temp *head`, a 64-bit build gives (a) 8 24.**

**Why.** A class cannot contain a member of its own type (it would be infinitely big), and `new` returns a pointer. Fixed version: `sizeof(head)` is a pointer, 8 bytes. `sizeof(temp)`: int 4, 4 bytes padding, pointer 8, float 4, 4 bytes padding to a multiple of 8 = 24.

**Concept: self-referential classes.** A linked-list node holds a **pointer** to its own type, never the type itself. Struct size includes alignment padding.

@@ wbd-21
**Answer: (a) create public member functions** (getters/setters)

**Why.** Private members are only accessible inside the class, so outside code must go through public methods. Private or protected methods are not callable from outside either. (C++ `friend` functions are another route, not offered.)

**Concept: encapsulation.** Hide data, expose controlled operations. Setters can validate input; getters can compute values, so the internal representation can change without breaking users.

@@ fj-kgp-pc3
**Answer: (c) the function does not modify the object it is called on**

**Why.** In `int get() const;`, `this` becomes a pointer to const, so the function cannot change data members (except `mutable` ones). Only const member functions can be called on a const object. (The screenshot ticks (a), which is wrong.)

**Concept: const-correctness.** Mark every member function that only reads as `const`. Then const objects and const references can use it, and the compiler stops accidental changes.

@@ mw-iisc-42
**Answer: (b)**

**Why.** A constructor that can be called with one argument of another type (and is not `explicit`) lets the compiler convert that type implicitly: `A a = 5;` calls `A(int)`.

**Concept: converting constructors and `explicit`.** Implicit conversions can hide bugs (`f(5)` silently building an `A`). Mark single-argument constructors `explicit` unless you want the conversion.

@@ nv-20
**Answer: (c) Constructor for B, B, C; Destructor for C, B, B**

**Why.** C derives from B and has a member `B a`. Building a C: base class first (B), then members (B for `a`), then C's own body (C). Class A is never used. `~B` is virtual, so `delete b` through a `B*` runs ~C, then destroys the member (B), then the base (B).

**Concept: construction and destruction order.** Construct: bases (in declaration order) → members (in declaration order) → constructor body. Destroy: exactly the reverse. Deleting through a base pointer only does this correctly if the base destructor is virtual.

@@ qc-n-ctor
**Answer: (b) constructor overloading**

**Why.** Same name, different parameter lists, chosen at compile time: overloading. Constructors are not inherited, so they cannot be overridden. Chaining is one constructor calling another (`this(...)` in Java, delegating constructors in C++).

**Concept: overloading vs overriding.** Overloading: same name, different parameters, same scope, compile-time choice. Overriding: same signature in a subclass, run-time choice through virtual dispatch.

@@ fj-kgp-pc2
**Answer: (b) multiple inheritance**

**Why.** `class C : public A, public B` inherits from two bases at once. Multilevel is a chain (A → B → C); hierarchical is several classes deriving from one base. (Both screenshot ticks are wrong.)

**Concept: inheritance shapes.** Single (one parent), multiple (several parents), multilevel (grandparent chain), hierarchical (one parent, many children), hybrid (a mix). Multiple inheritance can cause the "diamond problem", solved in C++ with virtual inheritance.

@@ maq-q27
**Answer: (a) 134212**

**Why.** `new B` runs constructors base-first: A (1) then B (3). `~A` is virtual, so `delete obj` (an `A*` to a B) runs ~B (4) then ~A (2). `new A` prints 1 and its delete prints 2.

**Concept: virtual destructors.** If a class may be deleted through a base pointer, give the base a virtual destructor. Without it only ~A would run (formally undefined behaviour) and B's cleanup would be skipped.

@@ mw-iiitd-23
**Answer: (a) Person Father Person Mother Child**

**Why.** Base classes are constructed in the order they are **declared** (`Father, Mother`), not the order in the initialiser list. Each base first builds its own Person (no virtual inheritance, so there are two Person sub-objects). Then Child's body prints "Child".

**Concept: initialisation order is declaration order.** Compilers warn when the initialiser list order differs, because it is ignored. In a diamond without `virtual`, the shared grandparent is duplicated.

@@ mw-iiitd-26
**Answer: (c) and (d)** (errors on `Base obj;` and `Derived d;`)

**Why.** Base has pure virtual functions, so it is abstract and cannot be instantiated. Derived overrides `show` but not `print`, so it is still abstract. A pointer to an abstract class is fine, so `b = &d` is not itself an error.

**Concept: abstract classes.** A class with at least one pure virtual function (`= 0`) is abstract: it defines an interface. A subclass becomes concrete only when it overrides **every** pure virtual function.

@@ mw-iisc-37
**Answer: (b) `virtual test() = 0;`** (with a return type in real code: `virtual void test() = 0;`)

**Why.** `= 0` after a virtual function declaration makes it pure virtual. There is no `pure` keyword in C++.

**Concept: pure virtual function.** It has no required body in the base and forces subclasses to provide one.

@@ mw-iitb-22
**Answer: (d) CB CD DB**

**Why.** Construction goes base first: CB, CD. `delete` through a `Base*` with a non-virtual destructor calls only ~Base (formally undefined behaviour), so DD is skipped.

**Concept: why base destructors should be virtual.** The call `delete b` picks the destructor from the pointer's static type unless it is virtual. Non-virtual → derived resources leak.

@@ mw-iitb-23
**Answer: (d) CB CD DD DB** if Base has a virtual destructor (the likely point after the previous question); with a non-virtual one it would be (c).

**Why.** With a virtual destructor, `delete b` dispatches to ~Derived, which runs first (DD), then automatically ~Base (DB).

**Concept: destruction order.** Derived destructor body first, then members, then bases: the reverse of construction.

@@ nv-18
**Answer: (c) `Derived3::Foo()` three times**

**Why.** The object is a Derived3, which is also a Derived1 (and a Base). So `base`, `derived1` and `derived3` are non-null. Derived2 is a sibling branch, so `dynamic_cast<Derived2*>` returns nullptr. Every call is virtual and reaches Derived3::Foo.

**Concept: `dynamic_cast`.** It checks the object's real type at run time: a cast to a class the object actually is (or derives from) succeeds; otherwise it returns nullptr (for pointers). Virtual calls always go to the most-derived override, whatever the pointer's type.

@@ qc-iisc-inherit
**Answer: (a) all three**

**Why.** Inheritance lets subclasses reuse code (I), share common code in one base (II), and present a consistent interface, since every subclass has the base's methods (III).

**Concept: what inheritance buys.** "Is-a" relationships, reuse, and polymorphism through a common interface. Overuse makes rigid hierarchies; prefer composition when there is no true "is-a".

@@ qc60-59
**Answer: (c) method overriding**

**Why.** The same `sendAlert()` signature is redefined in each subclass and chosen at run time from the object's type: run-time polymorphism by overriding. Overloading would mean different parameter lists.

**Concept: two kinds of polymorphism.** Compile-time: function and operator overloading, templates. Run-time: virtual functions / overriding, where a base reference calls the right subclass method.

@@ qcc-oop-02
**Answer: (b) single inheritance**

**Why.** One base (A) and one derived class (B). Multilevel needs a chain (C → B → A); multiple needs one class with two or more bases; hybrid mixes these.

**Concept: inheritance types.** See the multiple-inheritance question above for the full list.

@@ qcc-oop-05
**Answer: (d)** is false

**Why.** An **abstract** class can implement an interface and leave some of its methods unimplemented; only a concrete class must implement all of them (and since Java 8, `default` methods need no implementation). (a)–(c) are true: nested interfaces exist, interfaces can declare member classes, and interface fields are implicitly `public static final` constants.

**Concept: Java interfaces.** A contract of methods. Fields are constants; methods are abstract unless `default` or `static`. A class can implement many interfaces but extend only one class.

@@ wbd-22
**Answer: (d) inheritance**

**Why.** A subclass reuses the fields and methods of its superclass instead of rewriting them.

**Concept: the four OOP pillars.** Encapsulation (hide data behind methods), abstraction (show only what matters), inheritance (reuse via is-a), polymorphism (one interface, many behaviours).

@@ fj-kgp-pc1
**Answer: (b) 10**

**Why.** Inside the parentheses `<<` is the shift operator: 5 = 101₂, shifted left by 1 = 1010₂ = 10. Without the parentheses, `cout << x << 1` would print "51".

**Concept: left shift multiplies by 2.** `x << k` = x × 2ᵏ (for non-negative values that do not overflow). In C++, `<<` on a stream is the overloaded output operator; brackets decide which meaning applies.

@@ maq-q29
**Answer: (a) world**

**Why.** `if (i = 5)` assigns 5 to i (it does not compare). The value 5 is non-zero, so on the first iteration it prints "world" and breaks.

**Concept: `=` vs `==`.** Assignment inside a condition is legal in C/C++ and the condition takes the assigned value. Compilers warn ("suggest parentheses around assignment"). Some people write `5 == i` so a typo becomes an error.

@@ mw-iisc-36
**Answer: (d) none of these** (it prints `k`)

**Why.** `7[str]` means `*(7 + str)`, which is the same as `*(str + 7)` = `str[7]`. "MathWorks" index 7 is 'k'.

**Concept: `a[b]` is `*(a + b)`.** Addition is commutative, so `a[b]` and `b[a]` are the same thing. A curiosity, but it shows that indexing is pointer arithmetic.

@@ mw-iisc-41
**Answer: (c) `extern "C"`**

**Why.** `extern "C"` gives a function C linkage, so its symbol name is not mangled and C code can call it (and C++ can call C libraries).

**Concept: name mangling.** C++ supports overloading, so the compiler encodes parameter types into symbol names (e.g. `_Z3addii` for `add(int, int)`). C has no overloading and uses plain names; `extern "C"` switches to that scheme.

@@ nv-16
**Answer: (b) 2**

**Why.** `num` itself is not const; only the pointer gives a read-only view. Casting away that const and writing is well-defined and changes num to 2. (Writing through such a cast would be undefined if num had been declared `const int`.)

**Concept: `const_cast`.** It removes const from a pointer or reference. Safe only when the original object was not declared const; useful for calling old APIs that forgot const.

@@ qc60-44
**Answer: (d) an exception or error occurs**

**Why.** If no matching method exists, the language reports it: a compile error in statically typed languages (C++, Java), or a run-time error such as AttributeError (Python) or "does not understand" (Smalltalk). It is never generated automatically or silently ignored.

**Concept: message passing.** In OOP, calling a method is "sending a message" to an object. The object must have a method to handle it; otherwise the type system or the runtime complains.

@@ qc60-48
**Answer: (d) exposing an alternate path that bypasses protected validation logic**

**Why.** The subclass added a second public way to change `balance` that skips the checks in `updateBalance()`. The invariant (no negative balances) is no longer protected.

**Concept: encapsulation protects invariants.** All changes to internal state should go through one validated path. Subclasses should reuse that path (call the base method), not write to the field directly.

@@ wbd-10
**Answer: (b) variables**

**Why.** A variable is a named storage location whose value can change. Constants cannot change; modules are code units; tokens are the smallest pieces of source code.

**Concept: variables vs constants.** Use constants (`const`, `final`) for values that must not change; the compiler then catches accidental writes.

@@ mw-iiitd-8
**Answer: (a)** is the incorrect remark

**Why.** Not every operator can be overloaded (`::`, `.`, `.*`, `?:`, `sizeof` cannot). (b) and (c) are true: overloading never changes precedence or associativity.

**Concept: operator overloading rules.** You can give existing operators meaning for your types, but you cannot invent new operators, change their number of operands, or change their precedence.

@@ mw-nitd-24
**Answer: (c) `::` and `?:`**

**Why.** The operators that cannot be overloaded are `::` (scope resolution), `.` (member access), `.*` (pointer-to-member), `?:` (ternary) and `sizeof`. `<<`, `!`, `()`, `[]`, `new` and `delete` can all be overloaded.

**Concept: why some operators are fixed.** They work on names or types at compile time (`::`, `sizeof`) or must keep guaranteed behaviour (`.`, `?:`), so letting users redefine them would break the language.

@@ mw-iiitd-25
**Answer: (d) 2 2 3**

**Why.** `*++ptr`: move to a[1], read 2. `*(ptr++)`: read a[1] = 2, then move to a[2]. `*ptr`: read a[2] = 3.

**Concept: pre vs post increment on pointers.** `++p` moves first, then you use it. `p++` gives the old position for the expression and moves afterwards.

@@ mw-iisc-35
**Answer: 11 22 33 44 55**

**Why.** `*(arr + i)` is `arr[i]`, so the loop prints every element.

**Concept: array name decays to a pointer.** In most expressions `arr` becomes `&arr[0]`, so `arr + i` points to element i.

@@ mw-iisc-39
**Answer: (a), (b), (c) and (d)** are true; (e) is backwards.

**Why.** `new` calls the constructor (malloc does not), is an operator (malloc is a library function), can be overloaded, and returns a correctly typed pointer (malloc returns `void*`). On failure `new` throws `std::bad_alloc`, while `malloc` returns NULL.

**Concept: new/delete vs malloc/free.** In C++ use `new`/`delete` (or better, smart pointers and containers) so constructors and destructors run. Never mix them: memory from `new` must be released with `delete`, from `malloc` with `free`.

@@ mw-iiitd-21
**Answer: (a)**

**Why.** In `template <typename T, template <typename> class C>`, `typename T` declares a type parameter, and `template <typename> class C` declares a template template parameter: a template passed in as an argument (e.g. `std::vector`).

**Concept: template parameters.** Templates can take types (`typename T` or `class T`), values (`int N`), or other templates. `typename` and `class` are interchangeable for type parameters.

@@ mw-iiitd-22
**Answer: (c) compiler error**

**Why.** `this` is a pointer, so `this.a` does not compile; it must be `this->a`. (Even fixed, the user-written copy constructor leaves `q.b` uninitialised, so the output would be unpredictable.)

**Concept: `this` and copy constructors.** `this` is a pointer to the current object: use `->`. A user-defined copy constructor must copy every member it needs; the compiler-generated one copies all of them.

@@ mw-iiitd-28
**Answer: (b) `template <class T> class node { public: node* next; T value; }`**

**Why.** (c) and (d) have invalid syntax (`class <template T>`). In (a) the members are private by default in a `class`, so a linked-list class could not reach `next`. Inside the template, `node` means `node<T>`.

**Concept: class templates.** `template <class T>` before a class makes T a placeholder type. Members of a `class` are private by default; of a `struct`, public.

@@ mw-iitb-21
**Answer: (a) `#include <string>`, then `s3 = s1 + s2`**

**Why.** `std::string` overloads `+` to concatenate. `strcat` works on C char arrays (and needs enough space in the destination).

**Concept: `std::string` vs C strings.** `std::string` manages its own memory and supports `+`, `==`, `.size()`. C strings are char arrays ending in `\0`, handled with `strcpy`, `strcat`, `strlen`.
