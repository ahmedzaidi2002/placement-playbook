---
title: "1.4 · Static, const, mutable and friend members"
linkTitle: "1.4 Static, const, mutable and friend members"
weight: 4
math: true
---
<div class="nb-proto">

<em><span>Prototypical example for this section:</span> a railway ticket counter: every ticket has its own number, but the count of tickets issued belongs to the counter, not to any one ticket.</em>

</div>

## 1.4.i `static` members {#s1-4-i}

<div class="nb nb-example nb-block" id="example-1-4-1">

<strong>Example 1.4.1</strong> (The counter vs the ticket)

The seat number printed on your ticket is yours; the “tickets issued today” number on the booking office board is shared by everyone. In a class, the first is an ordinary data member (one per object) and the second is a `static` data member (one per class).

</div>

```cpp {filename="static-counter.cpp"}
#include <iostream>

class Ticket {
public:
    Ticket() : id_(++issued_) {}        // every ticket gets the next id
    int id() const { return id_; }
    static int issued() { return issued_; }   // no 'this' inside
private:
    int id_;                            // one per object
    static int issued_;                 // ONE shared by all tickets
};
int Ticket::issued_ = 0;                // defined once, outside the class

int main() {
    Ticket a, b;
    {
        Ticket c;
        std::cout << "ids " << a.id() << b.id() << c.id() << "\n";
    }
    Ticket d;
    std::cout << "issued " << Ticket::issued() << ", d is #" << d.id()
              << "\n";
}
```

```text {filename="Output (MinGW g++ 6.3.0, -std=c++14, 32-bit)"}
ids 123
issued 4, d is #4
```

<div class="nb nb-definition" id="definition-1-4-2">

<strong>Definition 1.4.2</strong>. A <strong>static data member</strong> belongs to the class, not to any object: there is exactly one copy, shared by all objects, and it exists even when no object does. A <strong>static member function</strong> has no `this` pointer, so it can use only static members, and is called as `Ticket::issued()` without an object.

</div>

- A non-`const`, non-`inline` static data member is only <em>declared</em> in the class and must be <em>defined</em> once in a `.cpp` file (`int Ticket::issued_ = 0;`); forgetting that gives a linker error. C++17 allows `inline static int issued_ = 0;` inside the class instead.
- Static members count for nothing in `sizeof`: they are not stored in objects.
- A static member function cannot be `virtual` or `const`, since both are about the object it is called on, and there is none.

## 1.4.ii `const` member functions and const-correctness {#s1-4-ii}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> printing a marksheet should never be able to change the marks.</em>

</div>

<div class="nb nb-definition" id="definition-1-4-3">

<strong>Definition 1.4.3</strong>. A <strong>`const` member function</strong>, declared with `const` after the parameter list, promises not to modify the object: inside it, `this` is a pointer to `const`. Only `const` member functions can be called on a `const` object or through a `const` reference or pointer.

</div>

```cpp {filename="const-member-fn-err.cpp"}
class Marksheet {
public:
    int total() { return total_; }          // forgot const
    void addMarks(int m) { total_ += m; }
private:
    int total_ = 0;
};

void printReport(const Marksheet& m) {      // read-only access
    int t = m.total();                      // error: total() is not const
    (void)t;
}

int main() { Marksheet m; printReport(m); }
```

```text {filename="Compiler error (MinGW g++ 6.3.0, -std=c++14, 32-bit) — this file is meant not to compile"}
const-member-fn-err.cpp:10:21: error: passing 'const Marksheet' as 'this' argument discards qualifiers [-fpermissive]
```

“Discards qualifiers” means: calling `total()` would pass a `const Marksheet*` as `this`, but a non-`const` member function needs a non-`const` one.

<div class="nb nb-moral">

Mark every member function that does not change the object `const`, from the start. Adding it later forces changes all over the code, because a single missing `const` stops every caller that holds a `const` reference.

</div>

## 1.4.iii `mutable` {#s1-4-iii}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> a route that caches its length the first time you ask.</em>

</div>

Sometimes a `const` function needs to change a member that is not part of the object’s observable value: a cache, a counter of calls, a mutex.

```cpp {filename="mutable-cache.cpp"}
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
    double a = r.length(), b = r.length(), c = r.length();
    std::cout << a << " " << b << " " << c << ", computed "
              << r.computations() << " time(s)\n";
}
```

```text {filename="Output (MinGW g++ 6.3.0, -std=c++14, 32-bit)"}
5 5 5, computed 1 time(s)
```

<div class="nb nb-definition" id="definition-1-4-4">

<strong>Definition 1.4.4</strong>. A data member declared `mutable` may be modified even through a `const` object. Use it only for state that does not affect what the object <em>means</em> (so-called logical constness).

</div>

## 1.4.iv `friend` {#s1-4-iv}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> an auditor who is allowed to look at your private account, and nobody else.</em>

</div>

```cpp {filename="friend-demo.cpp"}
#include <iostream>

class BankAccount {
public:
    explicit BankAccount(long b) : balance_(b) {}
    friend class Auditor;                             // a trusted class
    friend std::ostream& operator<<(std::ostream& os, const BankAccount& a);
private:
    long balance_;
};

class Auditor {
public:
    bool flag(const BankAccount& a) const { return a.balance_ > 1000000; }
};

std::ostream& operator<<(std::ostream& os, const BankAccount& a) {
    return os << "Account(balance=" << a.balance_ << ")";   // reads private
}

int main() {
    BankAccount acc(2500000);
    std::cout << acc << ", flagged: " << std::boolalpha
              << Auditor().flag(acc) << "\n";
}
```

```text {filename="Output (MinGW g++ 6.3.0, -std=c++14, 32-bit)"}
Account(balance=2500000), flagged: true
```

<div class="nb nb-definition" id="definition-1-4-5">

<strong>Definition 1.4.5</strong>. A <strong>friend</strong> function or class, declared inside a class with `friend`, may access that class’s private and protected members. Friendship is granted by the class, not claimed by the friend; it is not inherited and not transitive, and it is not mutual.

</div>

<div class="nb nb-remark" id="remark-1-4-6">

<strong>Remark 1.4.6</strong> (When is `friend` justified?) — It is justified when two pieces of code are really one abstraction split for syntactic reasons. The standard example is `operator<<`: it must be a non-member (its left operand is a `std::ostream`) but it is part of the class’s interface. It is not justified as a way around `private` for convenience; then the design is wrong. “Does `friend` break encapsulation?” No more than a member function does: the class itself decides who is trusted.

</div>
