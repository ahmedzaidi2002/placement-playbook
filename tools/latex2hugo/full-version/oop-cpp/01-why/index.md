---
title: "1.1 · Why object-oriented programming"
linkTitle: "1.1 Why object-oriented programming"
weight: 1
math: true
---
<div class="nb-proto">

<em><span>Prototypical example for this section:</span> a college library: books, members, and the rule that you cannot issue a book with no copies left.</em>

</div>

## 1.1.i The same problem, written two ways {#s1-1-i}

Start with the library. The procedural way is to keep the data in plain structures and write the rules as free functions that operate on them.

```cpp {filename="library-procedural.cpp"}
#include <iostream>
#include <string>

// Procedural style: data in a plain struct, logic in free functions.
struct Book {
    std::string title;
    int copies;                    // anyone can write to this
};

Book shelf[2] = {{"CLRS", 2}, {"SICP", 1}};

void issue(Book& b) {
    if (b.copies > 0) b.copies--;  // the rule lives here...
}

int main() {
    issue(shelf[0]);
    shelf[1].copies -= 5;          // ...but nobody is forced to use it
    for (const Book& b : shelf)
        std::cout << b.title << ": " << b.copies << " copies\n";
}
```

```text {filename="Output (MinGW g++ 6.3.0, -std=c++14, 32-bit)"}
CLRS: 1 copies
SICP: -4 copies
```

The rule “never go below zero copies” is written inside `issue()`, but nothing makes anyone call `issue()`. Any line anywhere in the program can write `copies` directly, and one did. In a program of fifty lines this is easy to spot; in a program of fifty thousand lines, written by twenty people, it is the most common kind of bug: data put into a state that the rules say is impossible.

The object-oriented way puts the data and the rules that guard it in one unit, and makes the data unreachable except through those rules.

```cpp {filename="library-oop.cpp"}
#include <iostream>
#include <string>

// Object-oriented style: data and the rules guarding it live together.
class Book {
public:
    Book(std::string title, int copies)
        : title_(title), copies_(copies) {}

    bool issue() {                 // the only way to change copies_
        if (copies_ == 0) return false;
        --copies_;
        return true;
    }
    void giveBack() { ++copies_; }
    int copies() const { return copies_; }
    const std::string& title() const { return title_; }

private:
    std::string title_;
    int copies_;                   // unreachable from outside
};

int main() {
    Book sicp("SICP", 1);
    bool first = sicp.issue();
    bool second = sicp.issue();    // no copies left
    std::cout << std::boolalpha << first << " " << second << "\n";
    std::cout << sicp.title() << ": " << sicp.copies() << " copies\n";
}
```

```text {filename="Output (MinGW g++ 6.3.0, -std=c++14, 32-bit)"}
true false
SICP: 0 copies
```

Now there is exactly one way to change `copies_`, and it checks the rule. The book can never have $-4$ copies, no matter who writes the calling code.

<div class="nb nb-definition" id="definition-1-1-1">

<strong>Definition 1.1.1</strong>. A <strong>class</strong> is a user-defined type that bundles data (<strong>data members</strong>) with the functions that operate on it (<strong>member functions</strong> or <strong>methods</strong>). An <strong>object</strong> is one value of that type, with its own copy of the data members. The condition that must always hold for a valid object, here $\texttt{copies\_} \ge 0$, is called its <strong>class invariant</strong>.

</div>

<div class="nb nb-moral">

Object-oriented programming is about protecting invariants: the data and the only code allowed to change it live together, behind a wall.

</div>

Four ideas make this work. Interviewers call them the <strong>four pillars</strong>, and nearly every OOP interview starts with “explain the four pillars with an example”.

## 1.1.ii Encapsulation {#s1-1-ii}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> a bank account whose balance you can read but never set.</em>

</div>

<div class="nb nb-example nb-block" id="example-1-1-2">

<strong>Example 1.1.2</strong> (The bank counter)

You cannot walk into the vault and change the number in your account. You go to the counter, and the teller deposits or withdraws for you, applying the bank’s rules (no negative deposits, no overdraft). The counter is the <em>public interface</em>; the vault is <em>private</em>.

</div>

<div class="nb nb-definition" id="definition-1-1-3">

<strong>Definition 1.1.3</strong>. <strong>Encapsulation</strong> is bundling data with the methods that operate on it and restricting direct access to the data. In C++ the restriction is enforced by the compiler through the access specifiers `public`, `private` and `protected`.

</div>

Trying to break the wall is a compile-time error, not a run-time one:

```cpp {filename="bank-private-err.cpp"}
class BankAccount {
public:
    void deposit(long amount) { if (amount > 0) balance_ += amount; }
    long balance() const { return balance_; }
private:
    long balance_ = 0;
};

int main() {
    BankAccount acc;
    acc.deposit(500);
    acc.balance_ = 1000000;    // try to set the balance directly
}
```

```text {filename="Compiler error (MinGW g++ 6.3.0, -std=c++14, 32-bit) — this file is meant not to compile"}
bank-private-err.cpp:12:9: error: 'long int BankAccount::balance_' is private within this context
```

<div class="nb nb-remark" id="remark-1-1-4">

<strong>Remark 1.1.4</strong> (Encapsulation is not “make everything private and add getters and setters”) — A public `setBalance(long)` is just a public data member with extra typing. Encapsulation means exposing <em>operations that keep the invariant</em> (`deposit`, `withdraw`), not the raw data. [Section 1.8](../08-design/) returns to this.

</div>

## 1.1.iii Abstraction {#s1-1-iii}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> driving a car with a key, a steering wheel and pedals.</em>

</div>

<div class="nb nb-example nb-block" id="example-1-1-5">

<strong>Example 1.1.5</strong> (The driver’s view)

To start a car you turn a key. You do not check the fuel pump, time the injection or fire the spark plugs yourself; the car does all of that when you turn the key. You work with a simple model (key, wheel, pedals) that hides a complicated mechanism.

</div>

<div class="nb nb-definition" id="definition-1-1-6">

<strong>Definition 1.1.6</strong>. <strong>Abstraction</strong> is exposing <em>what</em> an object does while hiding <em>how</em> it does it. The user of a class programs against its interface, not its implementation.

</div>

```cpp {filename="car-abstraction.cpp"}
#include <iostream>

// The driver sees start() and drive(); the engine stays hidden.
class Car {
public:
    void start() {
        checkFuel();
        injectFuel();
        ignite();
        std::cout << "Car started\n";
    }
    void drive(int km) { std::cout << "Driving " << km << " km\n"; }

private:
    void checkFuel()  { std::cout << "  fuel ok\n"; }
    void injectFuel() { std::cout << "  fuel injected\n"; }
    void ignite()     { std::cout << "  spark plug fired\n"; }
};

int main() {
    Car c;
    c.start();          // one call; three private steps happen inside
    c.drive(12);
}
```

```text {filename="Output (MinGW g++ 6.3.0, -std=c++14, 32-bit)"}
  fuel ok
  fuel injected
  spark plug fired
Car started
Driving 12 km
```

<div class="nb nb-remark" id="remark-1-1-7">

<strong>Remark 1.1.7</strong> (Encapsulation vs abstraction) — The two are asked about together, and are easy to blur. <em>Abstraction</em> is a design idea: decide what the outside world needs to know (“a car can start”). <em>Encapsulation</em> is the mechanism that enforces the decision: make everything else inaccessible (`ignite()` is `private`). Abstraction chooses the interface; encapsulation hides the rest.

</div>

## 1.1.iv Inheritance {#s1-1-iv}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> a car and a bike are both vehicles with a registration number.</em>

</div>

<div class="nb nb-example nb-block" id="example-1-1-8">

<strong>Example 1.1.8</strong> (The RTO’s view)

Every vehicle the transport office registers has a registration number, whatever kind of vehicle it is. A car additionally has a boot; a bike can be kick-started. The shared part is described once; each kind adds only what is special about it.

</div>

<div class="nb nb-definition" id="definition-1-1-9">

<strong>Definition 1.1.9</strong>. <strong>Inheritance</strong> lets a new class (the <strong>derived</strong> class or subclass) be defined as an extension of an existing one (the <strong>base</strong> class or superclass): the derived class gets the base’s members and adds or changes some. Public inheritance models an <strong>is-a</strong> relationship: every `Car` is a `Vehicle`.

</div>

```cpp {filename="vehicle-inheritance.cpp"}
#include <iostream>
#include <string>

// Inheritance: what every vehicle has is written once, in the base class.
class Vehicle {
public:
    explicit Vehicle(std::string reg) : reg_(reg) {}
    void showRegistration() const { std::cout << "Reg no. " << reg_ << "\n"; }
private:
    std::string reg_;
};

class Car : public Vehicle {            // a Car is a Vehicle...
public:
    using Vehicle::Vehicle;             // reuse Vehicle's constructor
    void openBoot() const { std::cout << "Boot opened\n"; }  // ...plus more
};

class Bike : public Vehicle {
public:
    using Vehicle::Vehicle;
    void kickStart() const { std::cout << "Kick!\n"; }
};

int main() {
    Car c("TN-01-AB-1234");
    Bike b("TN-02-CD-5678");
    c.showRegistration(); c.openBoot();
    b.showRegistration(); b.kickStart();
}
```

```text {filename="Output (MinGW g++ 6.3.0, -std=c++14, 32-bit)"}
Reg no. TN-01-AB-1234
Boot opened
Reg no. TN-02-CD-5678
Kick!
```

The line `using Vehicle::Vehicle;` inherits the base class constructors (C++11); without it `Car` would need its own constructor that forwards the registration number. [Section 1.6](../06-inheritance/) covers inheritance properly, including when <em>not</em> to use it.

## 1.1.v Polymorphism {#s1-1-v}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> a checkout page that calls `pay()` without knowing whether it is UPI, card or cash.</em>

</div>

<div class="nb nb-example nb-block" id="example-1-1-10">

<strong>Example 1.1.10</strong> (One button, many behaviours)

At an online checkout you press “Pay”. What happens next depends on the method you chose: UPI sends a collect request, a card asks for an OTP, cash on delivery just records the order. The checkout page issues the same command every time; each payment method responds in its own way.

</div>

<div class="nb nb-definition" id="definition-1-1-11">

<strong>Definition 1.1.11</strong>. <strong>Polymorphism</strong> (“many forms”) is the ability of one interface to be used with objects of different types, each responding in its own way. C++ has two kinds: <strong>compile-time</strong> (static) polymorphism, through function overloading and templates, and <strong>run-time</strong> (dynamic) polymorphism, through `virtual` functions called via a pointer or reference to a base class.

</div>

```cpp {filename="payment-polymorphism.cpp"}
#include <iostream>
#include <memory>
#include <vector>

// One call, pay(), behaves differently for each payment method.
class Payment {
public:
    virtual void pay(int rupees) const = 0;  // each method says how
    virtual ~Payment() = default;
};

class Upi : public Payment {
public:
    void pay(int r) const override {
        std::cout << "UPI: Rs " << r << " sent to VPA\n";
    }
};
class Card : public Payment {
public:
    void pay(int r) const override {
        std::cout << "Card: Rs " << r << " charged after OTP\n";
    }
};
class Cash : public Payment {
public:
    void pay(int r) const override {
        std::cout << "Cash: collect Rs " << r << " on delivery\n";
    }
};

int main() {
    std::vector<std::unique_ptr<Payment>> methods;
    methods.push_back(std::make_unique<Upi>());
    methods.push_back(std::make_unique<Card>());
    methods.push_back(std::make_unique<Cash>());
    for (const auto& m : methods)
        m->pay(250);                 // checkout code never changes
}
```

```text {filename="Output (MinGW g++ 6.3.0, -std=c++14, 32-bit)"}
UPI: Rs 250 sent to VPA
Card: Rs 250 charged after OTP
Cash: collect Rs 250 on delivery
```

The loop is written once against `Payment`. Adding a new method, say a wallet, means adding one class; the checkout loop does not change at all. The `virtual`, `= 0`, `override` and the virtual destructor in this listing are each explained in [Section 1.7](../07-polymorphism/).

<div class="nb nb-moral">

Encapsulation protects the data, abstraction simplifies the interface, inheritance reuses the common part, and polymorphism lets one piece of code work with many types.

</div>
