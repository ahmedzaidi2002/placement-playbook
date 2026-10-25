---
title: "1.16 · A few harder problems to think about"
linkTitle: "1.16 A few harder problems to think about"
weight: 16
math: true
---
Every program in these problems was compiled and run with MinGW g++ 6.3.0, `-std=c++14`, 32-bit; the real output is in the solutions at the back of the book (the <em>Solution</em> drop-down under each problem). Predict it before looking.

<div class="nb nb-problem nb-block" id="problem-1a">

<strong>Problem 1A</strong> (Construction order)

What does this program print?

```cpp {filename="prob-order.cpp"}
#include <iostream>

struct A { A() { std::cout << "A "; }  ~A() { std::cout << "~A "; } };
struct B { B() { std::cout << "B "; }  ~B() { std::cout << "~B "; } };
struct C : A {
    B b;
    C() { std::cout << "C "; }
    ~C() { std::cout << "~C "; }
};

int main() {
    C c;
    std::cout << "| ";
    A temp = A();          // how many A's are built here?
    std::cout << "| ";
}
```

<details class="nb-hint">
<summary>Hint</summary>

Base, then members, then the body; destruction is the exact reverse, and locals die in reverse order of creation. How many `A` objects does `A temp = A();` create?

</details>

<details class="nb-sol">
<summary>Solution</summary>

It prints `A B C | A | ~A ~C ~B ~A`. `C` builds its base `A`, then its member `B`, then its body. `A temp = A();` builds a single `A`: the temporary is elided. At the end of `main`, `temp` (created last) dies first, then `c`, whose body, member and base are destroyed in reverse order.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-1b">

<strong>Problem 1B</strong> (Overload, override or hide?)

What does this program print?

```cpp {filename="prob-hide-override.cpp"}
#include <iostream>

struct Base {
    virtual void f(int)    { std::cout << "Base::f(int)\n"; }
    virtual ~Base() = default;
};
struct Derived : Base {
    void f(double)         { std::cout << "Derived::f(double)\n"; }
};

int main() {
    Derived d;
    Base& b = d;
    d.f(1);
    b.f(1);
    d.f(1.5);
}
```

<details class="nb-hint">
<summary>Hint</summary>

`Derived::f(double)` does not override anything. What does name lookup find in `Derived`?

</details>

<details class="nb-sol">
<summary>Solution</summary>

`Derived::f(double)`, `Base::f(int)`, `Derived::f(double)`. The derived `f` has a different parameter type, so it hides `Base::f` instead of overriding it. Through `d`, lookup finds only `Derived::f(double)` and converts $1$ to `double`. Through `Base&`, lookup finds `Base::f(int)`, and since nothing overrides it, that is what runs. Writing `override` would have turned the mistake into a compile error.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-1c">

<strong>Problem 1C</strong> (Polymorphism and containers)

What does this program print?

```cpp {filename="prob-vector-slice.cpp"}
#include <iostream>
#include <vector>

struct Animal {
    virtual const char* sound() const { return "..."; }
    virtual ~Animal() = default;
};
struct Dog : Animal {
    const char* sound() const override { return "Woof"; }
};

int main() {
    std::vector<Animal> zoo;
    zoo.push_back(Dog());
    Dog d;
    Animal& ref = d;
    std::vector<Animal*> pens{&d};
    std::cout << zoo[0].sound() << " " << ref.sound() << " "
              << pens[0]->sound() << "\n";
}
```

<details class="nb-hint">
<summary>Hint</summary>

What type are the elements of `zoo`?

</details>

<details class="nb-sol">
<summary>Solution</summary>

`... Woof Woof`. `zoo` stores `Animal` objects, so pushing a `Dog` slices it into an `Animal`. The reference and the pointer both reach the real `Dog`.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-1d">

<strong>Problem 1D</strong> (Counting copies)

How many times does `Photo`’s copy constructor run?

```cpp {filename="prob-copy-count.cpp"}
#include <iostream>

int copies = 0;
struct Photo {
    Photo() = default;
    Photo(const Photo&) { ++copies; }
};

void viewByValue(Photo) {}
void viewByRef(const Photo&) {}
Photo duplicate(const Photo& p) { return p; }

int main() {
    Photo p;
    viewByValue(p);
    viewByRef(p);
    Photo q = duplicate(p);
    Photo r = q;
    (void)r;
    std::cout << copies << "\n";
}
```

<details class="nb-hint">
<summary>Hint</summary>

Go line by line: pass by value, pass by reference, return from a reference, copy initialisation.

</details>

<details class="nb-sol">
<summary>Solution</summary>

$3$. One for passing `p` by value; none for the reference; one inside `duplicate`, because `return p;` must copy from a reference (RVO cannot elide a copy of an object it does not own), and the copy into `q` is elided; one for `r = q`.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-1e">

<strong>Problem 1E</strong> (Static locals)

What does this program print, and in what order?

```cpp {filename="prob-static-local.cpp"}
#include <iostream>

struct Counter {
    Counter() { std::cout << "Counter built\n"; }
    int n = 0;
};

int next() {
    static Counter c;       // when is this constructed?
    return ++c.n;
}

int main() {
    std::cout << "main starts\n";
    int a = next();
    int b = next();
    int c = next();
    std::cout << a << b << c << "\n";
}
```

<details class="nb-hint">
<summary>Hint</summary>

When is a function-local `static` initialised?

</details>

<details class="nb-sol">
<summary>Solution</summary>

`main starts`, then `Counter built`, then `123`. A local `static` is constructed the first time control passes through its declaration, not at program start, and exactly once. This is the mechanism behind the Meyers singleton ([Section 1.13](../13-patterns/)).

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-1f">

<strong>Problem 1F</strong> (Find the bug: the missing third)

This class follows “most” of the Rule of Three. What goes wrong at `b = a;`? Fix it with as little code as possible.

```cpp {filename="bug-rule-of-three.cpp"}
#include <cstring>
#include <iostream>

class Name {
public:
    explicit Name(const char* s) : s_(new char[std::strlen(s) + 1]) {
        std::strcpy(s_, s);
    }
    Name(const Name& o) : Name(o.s_) {}      // deep copy: good
    ~Name() { delete[] s_; }                 // frees: good
    const char* get() const { return s_; }
private:
    char* s_;
};

int main() {
    Name a("Asha");
    Name b("Ravi");
    b = a;                   // which function runs here?
    std::cout << b.get() << "\n";
}
```

<details class="nb-hint">
<summary>Hint</summary>

Which special member function does `b = a;` call, and who wrote it?

</details>

<details class="nb-sol">
<summary>Solution</summary>

`b = a;` is copy <em>assignment</em>, which the class does not define, so the compiler’s member-wise version copies the pointer. Ravi’s buffer leaks, and at the end of `main` both objects `delete[]` Asha’s buffer: undefined behaviour. The run printed `Asha` and exited normally, which is exactly why this bug survives testing. Fix: add copy-and-swap, `Name& operator=(Name o) { std::swap(s_, o.s_); return *this; }`, or better, store a `std::string` and delete all three special members (Rule of Zero).

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-1g">

<strong>Problem 1G</strong> (Find the bug: self-assignment)

What does this program print, and why? Give two fixes.

```cpp {filename="bug-self-assign.cpp"}
#include <algorithm>
#include <iostream>

class Scores {
public:
    explicit Scores(int n) : n_(n), data_(new int[n]) {
        std::fill(data_, data_ + n, 7);
    }
    Scores(const Scores& o) : n_(o.n_), data_(new int[o.n_]) {
        std::copy(o.data_, o.data_ + n_, data_);
    }
    ~Scores() { delete[] data_; }
    Scores& operator=(const Scores& o) {
        delete[] data_;                            // free our buffer...
        n_ = o.n_;
        data_ = new int[n_];
        std::copy(o.data_, o.data_ + n_, data_);   // ...then copy from o
        return *this;
    }
    int first() const { return data_[0]; }
private:
    int n_;
    int* data_;
};

int main() {
    Scores s(3);
    Scores& alias = s;
    s = alias;                                     // self-assignment
    std::cout << "first score after s = s: " << s.first() << "\n";
}
```

<details class="nb-hint">
<summary>Hint</summary>

In `s = s`, `o` and `*this` are the same object. What does the first line of `operator=` do to `o`?

</details>

<details class="nb-sol">
<summary>Solution</summary>

It prints garbage; the value changed between runs (this run printed the number below).

```text {filename="Output (MinGW g++ 6.3.0, -std=c++14, 32-bit)"}
first score after s = s: 13014688
```

For `s = s` the operator deletes `data_`, which is also `o.data_`, and then copies from the freed memory. Fix 1: start with `if (this == &o) return *this;`. Fix 2 (better): allocate and copy into a temporary <em>first</em>, then swap, which also gives the strong exception guarantee (copy-and-swap, [Section 1.5](../05-operators/)).

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-1h">

<strong>Problem 1H</strong> (Find the bug: a dangling reference)

This compiles with one warning. What is it, and what would happen if `main` called `s.greeting()`?

```cpp {filename="bug-dangling-warn.cpp"}
#include <iostream>
#include <string>

class Student {
public:
    explicit Student(std::string n) : name_(n) {}
    const std::string& greeting() const {
        std::string g = "Hello, " + name_;
        return g;                          // returns a reference to a local
    }
private:
    std::string name_;
};

int main() {
    Student s("Asha");
    std::cout << "compiled; calling greeting() would read a dead object\n";
    (void)s;
}
```

<details class="nb-hint">
<summary>Hint</summary>

When is `g` destroyed?

</details>

<details class="nb-sol">
<summary>Solution</summary>

The compiler says:

```text {filename="Compiler warning (MinGW g++ 6.3.0, -std=c++14, 32-bit, -Wall -Wextra)"}
bug-dangling-warn.cpp:8:21: warning: reference to local variable 'g' returned [-Wreturn-local-addr]
```

`g` is destroyed when `greeting` returns, so the caller receives a reference to a dead `std::string`; using it is undefined behaviour. Return `std::string` by value (RVO makes it cheap).

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-1i">

<strong>Problem 1I</strong> 🌶 (Virtual copy)

Given `std::vector<std::unique_ptr<Shape>>`, write a deep copy that preserves each element’s real type, without `dynamic_cast` or a type switch.

<details class="nb-hint">
<summary>Hint</summary>

A constructor cannot be virtual, but a function that calls one can.

</details>

<details class="nb-sol">
<summary>Solution</summary>

Give `Shape` a pure virtual `clone()` that each class implements by copying itself (the “virtual constructor” idiom):

```cpp {filename="prob-clone.cpp"}
#include <iostream>
#include <memory>
#include <vector>

struct Shape {
    virtual std::unique_ptr<Shape> clone() const = 0;   // "virtual copy ctor"
    virtual const char* name() const = 0;
    virtual ~Shape() = default;
};
struct Circle : Shape {
    std::unique_ptr<Shape> clone() const override {
        return std::make_unique<Circle>(*this);          // copies a CIRCLE
    }
    const char* name() const override { return "Circle"; }
};
struct Square : Shape {
    std::unique_ptr<Shape> clone() const override {
        return std::make_unique<Square>(*this);
    }
    const char* name() const override { return "Square"; }
};

int main() {
    std::vector<std::unique_ptr<Shape>> drawing;
    drawing.push_back(std::make_unique<Circle>());
    drawing.push_back(std::make_unique<Square>());

    std::vector<std::unique_ptr<Shape>> copy;            // deep copy
    for (const auto& s : drawing) copy.push_back(s->clone());
    for (const auto& s : copy) std::cout << s->name() << " ";
    std::cout << "(distinct objects: " << std::boolalpha
              << (copy[0].get() != drawing[0].get()) << ")\n";
}
```

```text {filename="Output (MinGW g++ 6.3.0, -std=c++14, 32-bit)"}
Circle Square (distinct objects: true)
```

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-1j">

<strong>Problem 1J</strong> 🌶 (Heap-only and stack-only classes)

How do you write a class whose objects can only be created with `new`? One whose objects can never be created with `new`?

<details class="nb-hint">
<summary>Hint</summary>

What does the compiler need to be able to call for a local variable, and for `new`?

</details>

<details class="nb-sol">
<summary>Solution</summary>

Heap-only: make the destructor `private` (or `protected`) and provide a member such as `void destroy() { delete this; }`. A local variable needs an accessible destructor at the end of its scope, so it will not compile; `new` does not. Stack-only: declare `static void* operator new(std::size_t) = delete;` (and the array form) in the class, so `new T` does not compile.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-1k">

<strong>Problem 1K</strong> (Movable but not copyable)

Write the declarations that make a class `Socket` movable but not copyable, and name two standard-library classes designed this way.

<details class="nb-hint">
<summary>Hint</summary>

`= delete` and `= default`.

</details>

<details class="nb-sol">
<summary>Solution</summary>

`Socket(const Socket&) = delete; Socket& operator=(const Socket&) = delete;` plus `Socket(Socket&&) noexcept; Socket& operator=(Socket&&) noexcept;` (defined to transfer the handle and leave the source empty, or `= default` if the members are themselves movable). Examples: `std::unique_ptr` and `std::fstream`.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-1l">

<strong>Problem 1L</strong> (Is it substitutable?)

`ReadOnlyFile` derives from `File` and overrides `write()` to throw. Which SOLID principle does this break, and how would you redesign it?

<details class="nb-hint">
<summary>Hint</summary>

Can every caller that writes to a `File` be given a `ReadOnlyFile`?

</details>

<details class="nb-sol">
<summary>Solution</summary>

Liskov substitution: code written against `File` may call `write()` and is broken by a subclass that refuses. Split the interface (interface segregation): a `ReadableFile` with `read()`, and a `WritableFile` that adds `write()`; `ReadOnlyFile` implements only the first.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-1m">

<strong>Problem 1M</strong> 🌶 (Design: vending machine)

Design the classes for a vending machine: insert coins, select a product, dispense it with change, or refund. The machine must reject “select” before money is inserted and must not dispense twice.

<details class="nb-hint">
<summary>Hint</summary>

The machine’s behaviour depends on its current state. Look up the State pattern: it is Strategy, where the object switches the strategy itself.

</details>

<details class="nb-sol">
<summary>Solution</summary>

Entities: `Product` (code, price), `Inventory` (stock per slot), `CoinBox`, `VendingMachine`. The behaviour lives in a `State` interface with `insertCoin`, `select`, `dispense`, `refund`, implemented by `Idle`, `HasMoney`, `Dispensing` and `SoldOut`; the machine holds the current state and each method delegates to it, and each state decides the next state. Invalid actions are handled by the state that forbids them (`Idle::select` says “insert money”), so there are no `if (state == ...)` chains, and a new state (maintenance mode) is a new class. Change-making is a separate `ChangeStrategy`.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-1n">

<strong>Problem 1N</strong> 🌶🌶 (Design: elevator system)

Design an elevator system for a building with $n$ floors and $k$ lifts: requests from floors (up/down buttons) and from inside a lift (floor buttons), a display on every floor.

<details class="nb-hint">
<summary>Hint</summary>

Separate what an elevator is from how requests are assigned to elevators.

</details>

<details class="nb-sol">
<summary>Solution</summary>

Entities: `Elevator` (current floor, `Direction`, door state, a set of stops), `Request` (floor, direction or target), `ElevatorController` (owns the elevators, receives requests), `Display`. Assignment of a hall request to a lift is a `DispatchStrategy` (nearest idle lift, or least-loaded), and the order of stops within one lift is a `SchedulingStrategy` such as SCAN/LOOK (serve all stops in the current direction, then reverse), which avoids starving far floors. Floor displays are observers of each elevator. Discuss: concurrency of button presses (a thread-safe request queue), emergency mode (a state), and testing with a simulated clock.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-1o">

<strong>Problem 1O</strong> 🌶 (Design: notification service)

Design a service that sends notifications by email, SMS and push, respects each user’s preferences and quiet hours, and retries failed sends.

<details class="nb-hint">
<summary>Hint</summary>

Which parts vary independently? Channels, policies and retry behaviour.

</details>

<details class="nb-sol">
<summary>Solution</summary>

A `Channel` interface (`EmailChannel`, `SmsChannel`, `PushChannel`) created by a factory; a `PreferenceStore` that says which channels a user allows and when; `NotificationService::send(userId, message)` asks the store and dispatches to the allowed channels (dependency inversion: the service knows only the interfaces). Retries are a decorator, `RetryingChannel`, wrapping any channel with a backoff policy, so no channel reimplements it. Quiet hours are a filter in front of dispatch (or a delayed queue).

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-1p">

<strong>Problem 1P</strong> 🌶🌶 (Design: extending the parking lot)

Extend the parking lot of [Section 1.14](../14-lld/) with electric-vehicle charging spots that charge per kWh on top of parking, and a monthly pass that makes parking free. Which classes change?

<details class="nb-hint">
<summary>Hint</summary>

Aim for adding classes, not editing `ParkingLot`.

</details>

<details class="nb-sol">
<summary>Solution</summary>

Add a spot feature (`Spot` gains a flag or a `ChargingSpot` with a meter) and let `fits` consider whether the vehicle needs charging. Pricing becomes a composition of policies: a decorator `ChargingFee` adds kWh $\times$ rate to whatever the inner `PricingPolicy` returns, and a `PassHolderPricing` returns $0$ for pass holders, selected per ticket by a small factory. `ParkingLot` only needs the ticket to carry the vehicle (for the pass) and the energy used; its algorithm does not change, which is the open/closed principle at work.

</details>

</div>
