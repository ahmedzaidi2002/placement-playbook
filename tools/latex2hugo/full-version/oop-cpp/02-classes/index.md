---
title: "1.2 · Classes and objects"
linkTitle: "1.2 Classes and objects"
weight: 2
math: true
---
<div class="nb-proto">

<em><span>Prototypical example for this section:</span> a `Student` record in the placement portal: a name and a CGPA, and the question “is this student eligible for a company’s cutoff?”.</em>

</div>

## 1.2.i `class` vs `struct` {#s1-2-i}

<div class="nb nb-definition" id="fact-1-2-1">

<strong>Fact 1.2.1</strong>. In C++, `class` and `struct` are the same thing with one difference: members and base classes are `private` by default in a `class` and `public` by default in a `struct`.

</div>

```cpp {filename="struct-vs-class-err.cpp"}
struct PointS { int x; };    // struct: members are public by default
class  PointC { int x; };    // class:  members are private by default

int main() {
    PointS s;
    s.x = 1;                 // fine
    PointC c;
    c.x = 1;                 // error
}
```

```text {filename="Compiler error (MinGW g++ 6.3.0, -std=c++14, 32-bit) — this file is meant not to compile"}
struct-vs-class-err.cpp:8:7: error: 'int PointC::x' is private within this context
```

Everything else (member functions, constructors, inheritance, `virtual`) works identically in both. The convention is to use `struct` for plain bundles of data with no invariant (a 2D point, a config record) and `class` for types that protect an invariant.

<div class="nb nb-remark" id="remark-1-2-2">

<strong>Remark 1.2.2</strong> (The C-style answer is wrong) — “A struct cannot have member functions” is true in C, not in C++. Interviewers ask this question precisely to see if you know the difference.

</div>

## 1.2.ii Access specifiers {#s1-2-ii}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> a hostel: the corridor is public, your room is private, and the family visiting room is protected.</em>

</div>

<div class="nb nb-definition" id="definition-1-2-3">

<strong>Definition 1.2.3</strong>. The three <strong>access specifiers</strong> control who may name a member:

- `public`: anyone;
- `private`: only the class’s own member functions and its friends;
- `protected`: the class, its friends, and classes derived from it.

Access is checked at compile time, per class and not per object: a member function of `Student` may read the private members of <em>another</em> `Student`.

</div>

<div class="nb nb-remark" id="remark-1-2-4">

<strong>Remark 1.2.4</strong> — Access control is not security. It stops honest mistakes at compile time; it does not stop someone who casts pointers deliberately. Everything is still in the same memory.

</div>

## 1.2.iii The `this` pointer {#s1-2-iii}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> a pizza order built with chained calls.</em>

</div>

<div class="nb nb-definition" id="definition-1-2-5">

<strong>Definition 1.2.5</strong>. Inside a non-static member function, <strong>`this`</strong> is a pointer to the object the function was called on. In `order.size('L')`, `this` is `&order`. In a `const` member function it is a pointer to `const`.

</div>

Returning `*this` by reference lets calls be chained, which is how builders and `std::cout << a << b` work:

```cpp {filename="this-chaining.cpp"}
#include <iostream>
#include <string>

// A builder: every setter returns *this, so calls can be chained.
class PizzaOrder {
public:
    PizzaOrder& size(char s)       { size_ = s;            return *this; }
    PizzaOrder& topping(std::string t)
                                   { toppings_ += t + " "; return *this; }
    PizzaOrder& extraCheese()      { cheese_ = true;       return *this; }

    void print() const {
        std::cout << "Size " << size_ << ", toppings: " << toppings_
                  << (cheese_ ? "(extra cheese)" : "") << "\n";
    }
    bool isSame(const PizzaOrder* other) const { return this == other; }

private:
    char size_ = 'M';
    std::string toppings_;
    bool cheese_ = false;
};

int main() {
    PizzaOrder order;
    order.size('L').topping("paneer").topping("onion").extraCheese().print();
    PizzaOrder other;
    std::cout << std::boolalpha << order.isSame(&order) << " "
              << order.isSame(&other) << "\n";
}
```

```text {filename="Output (MinGW g++ 6.3.0, -std=c++14, 32-bit)"}
Size L, toppings: paneer onion (extra cheese)
true false
```

The other everyday use of `this` is to tell a member apart from a parameter with the same name. Look at what happens without it:

```cpp {filename="this-shadow.cpp"}
#include <iostream>

class Account {
public:
    explicit Account(int balance) {
        balance = balance;          // assigns the parameter to itself!
    }
    int get() const { return balance; }
private:
    int balance = 0;
};

class FixedAccount {
public:
    explicit FixedAccount(int balance) {
        this->balance = balance;    // this-> names the member
    }
    int get() const { return balance; }
private:
    int balance = 0;
};

int main() {
    std::cout << Account(500).get() << " " << FixedAccount(500).get() << "\n";
}
```

```text {filename="Output (MinGW g++ 6.3.0, -std=c++14, 32-bit)"}
0 500
```

<div class="nb nb-ques" id="question-1-2-6">

<strong>Question 1.2.6</strong> — Why does the first account print $0$?

</div>

Inside the constructor, the name `balance` refers to the <em>parameter</em>, which hides the member. So `balance = balance` assigns the parameter to itself and the member keeps its default of $0$. Note that `-Wall -Wextra` gave <em>no warning</em> here. The cleanest fix is not `this->` but a member initialiser list, `Account(int balance) : balance(balance) `, where the name outside the parentheses can only mean the member ([Section 1.3](../03-lifecycle/)). Many codebases also avoid the clash by naming members with a trailing underscore, as the rest of this chapter does.

## 1.2.iv Defining members inside and outside the class {#s1-2-iv}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> `student.h` declares, `student.cpp` defines.</em>

</div>

In real projects the class definition goes in a header, which other files include, and most member functions are defined in a `.cpp` file using the scope-resolution operator `Class::member`.

```cpp {filename="outside-definition.cpp"}
#include <iostream>
#include <string>

// Usually in student.h: the class definition, i.e. the interface.
class Student {
public:
    Student(std::string name, double cgpa);
    bool eligibleFor(double cutoff) const;       // declared only
    std::string name() const { return name_; }   // defined inside: inline
private:
    std::string name_;
    double cgpa_;
};

// Usually in student.cpp: member functions defined outside, with Student::
Student::Student(std::string name, double cgpa) : name_(name), cgpa_(cgpa) {}

bool Student::eligibleFor(double cutoff) const {
    return cgpa_ >= cutoff;
}

int main() {
    Student s("Asha", 8.4);
    std::cout << s.name() << " eligible for 8.0 cutoff: " << std::boolalpha
              << s.eligibleFor(8.0) << "\n";
}
```

```text {filename="Output (MinGW g++ 6.3.0, -std=c++14, 32-bit)"}
Asha eligible for 8.0 cutoff: true
```

<div class="nb nb-definition" id="fact-1-2-7">

<strong>Fact 1.2.7</strong>. A member function <em>defined</em> inside the class body is implicitly `inline`, so the definition may appear in every file that includes the header without violating the one-definition rule. Whether the compiler actually inlines the call is its own decision, as with any `inline` function.

</div>

## 1.2.v Why an empty class has size 1 {#s1-2-v}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> `class Empty ;`</em>

</div>

```cpp {filename="empty-class.cpp"}
#include <iostream>

class Empty {};
class HasInt { int x; };
class IntAndEmptyMember { int x; Empty e; };
class DerivesFromEmpty : public Empty { int x; };

int main() {
    Empty a, b;
    Empty arr[3];
    std::cout << "sizeof(Empty)             = " << sizeof(Empty) << "\n"
              << "distinct addresses        = " << std::boolalpha
              << (&a != &b) << "\n"
              << "sizeof(Empty[3])          = " << sizeof(arr) << "\n"
              << "sizeof(HasInt)            = " << sizeof(HasInt) << "\n"
              << "sizeof(IntAndEmptyMember) = " << sizeof(IntAndEmptyMember)
              << "\n"
              << "sizeof(DerivesFromEmpty)  = " << sizeof(DerivesFromEmpty)
              << "\n";
}
```

```text {filename="Output (MinGW g++ 6.3.0, -std=c++14, 32-bit)"}
sizeof(Empty)             = 1
distinct addresses        = true
sizeof(Empty[3])          = 3
sizeof(HasInt)            = 4
sizeof(IntAndEmptyMember) = 8
sizeof(DerivesFromEmpty)  = 4
```

<div class="nb nb-theorem nb-block" id="proposition-1-2-8">

<strong>Proposition 1.2.8</strong>

The size of an object of an empty class is never $0$.

</div>

<div class="nb nb-proof">

<em>Argument.</em> The standard requires distinct objects of the same type to have distinct addresses. If `sizeof(Empty)` were $0$, the three elements of `Empty arr[3]` would all sit at the same address, and pointer arithmetic (`arr + 1`) would not move. So the compiler gives the object at least one byte; the standard only says “nonzero”, and g++ uses $1$.

</div>

Two more lines of that output are classic follow-ups.

- `IntAndEmptyMember` is $8$, not $5$: the empty member takes one byte and then padding rounds the size up to a multiple of `alignof(int)` $= 4$.
- `DerivesFromEmpty` is only $4$: an empty <em>base class</em> is allowed to take no space. This is the <strong>empty base optimisation</strong> (EBO), which the standard library uses to store empty allocators and comparators for free.

## 1.2.vi Data layout and padding {#s1-2-vi}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> packing a suitcase: the same items take less space in a better order.</em>

</div>

Each type has an <strong>alignment</strong>: its address must be a multiple of `alignof(T)`. To keep every member aligned, the compiler inserts unused <strong>padding</strong> bytes between members and at the end.

```cpp {filename="padding.cpp"}
#include <cstddef>
#include <iostream>

struct Wasteful { char a; int b; char c; };   // declared in a bad order
struct Packed   { int b; char a; char c; };   // same members, reordered
struct WithDbl  { char c; double d; };

int main() {
    std::cout << "alignof(int) = " << alignof(int)
              << ", alignof(double) = " << alignof(double)
              << ", sizeof(void*) = " << sizeof(void*) << "\n";
    std::cout << "Wasteful: size " << sizeof(Wasteful)
              << "  offsets a=" << offsetof(Wasteful, a)
              << " b=" << offsetof(Wasteful, b)
              << " c=" << offsetof(Wasteful, c) << "\n";
    std::cout << "Packed:   size " << sizeof(Packed)
              << "  offsets b=" << offsetof(Packed, b)
              << " a=" << offsetof(Packed, a)
              << " c=" << offsetof(Packed, c) << "\n";
    std::cout << "WithDbl:  size " << sizeof(WithDbl)
              << "  offset d=" << offsetof(WithDbl, d) << "\n";
}
```

```text {filename="Output (MinGW g++ 6.3.0, -std=c++14, 32-bit)"}
alignof(int) = 4, alignof(double) = 8, sizeof(void*) = 4
Wasteful: size 12  offsets a=0 b=4 c=8
Packed:   size 8  offsets b=0 a=4 c=5
WithDbl:  size 16  offset d=8
```

<figure class="nb-fig"><img src="fig-1.svg" alt="Figure 1" loading="lazy"></figure>

<div class="nb nb-definition" id="fact-1-2-9">

<strong>Fact 1.2.9</strong>. Members are laid out in declaration order (within one access level), each at an offset that is a multiple of its alignment, and the total size is a multiple of the largest alignment, so that arrays of the struct stay aligned. Ordering members from largest to smallest alignment usually minimises padding.

</div>

<div class="nb nb-remark" id="remark-1-2-10">

<strong>Remark 1.2.10</strong> (These numbers are not universal) — Alignments and sizes are set by the platform’s ABI, not by the C++ standard. On this 32-bit MinGW build `alignof(double)` is $8$, so `WithDbl` is $16$; other 32-bit ABIs align `double` to $4$ inside structs. What the standard does guarantee is `sizeof(char)` $= 1$ and the ordering rules above. Always say “on my compiler” when quoting a `sizeof` in an interview.

</div>

<div class="nb nb-moral">

A class is a type; an object is a value of it with its own data. The compiler lays that data out in declaration order with padding, and never gives an object zero size.

</div>
