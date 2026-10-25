---
title: "1.12 · The SOLID principles"
linkTitle: "1.12 The SOLID principles"
weight: 12
math: true
---
<div class="nb-proto">

<em><span>Prototypical example for this section:</span> an invoicing system for an online store that keeps getting new requirements: new offers, new output formats, new ways to notify customers.</em>

</div>

SOLID is five design rules, collected by Robert C. Martin, for classes that are easy to change. Interviewers ask for each one with an example; the best answers show a design that breaks the rule, what goes wrong, and the fix.

## 1.12.i S: Single responsibility {#s1-12-i}

<div class="nb nb-definition" id="definition-1-12-1">

<strong>Definition 1.12.1</strong>. A class should have one reason to change: one responsibility, owned by one kind of stakeholder.

</div>

<div class="nb nb-example nb-block" id="example-1-12-2">

<strong>Example 1.12.2</strong> (A restaurant)

The chef cooks, the cashier bills, the waiter serves. If the chef also did the billing, a change in GST rules would mean retraining the chef.

</div>

```cpp {filename="solid-srp.cpp"}
#include <iomanip>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>

// BAD: one class computes, formats AND stores -> three reasons to change.
//   class Invoice { double total(); std::string toPdf(); void saveToDb(); };

// GOOD: one responsibility each.
struct Invoice {                                   // business rules
    std::vector<double> items;
    double total() const {
        double t = 0;
        for (double x : items) t += x;
        return t * 1.18;                           // with 18% GST
    }
};
struct InvoicePrinter {                            // presentation
    std::string format(const Invoice& inv) const {
        std::ostringstream out;
        out << "TOTAL Rs " << std::fixed << std::setprecision(2) << inv.total();
        return out.str();
    }
};
struct InvoiceStore {                              // persistence
    void save(const Invoice& inv) const {
        std::cout << "saved invoice of " << inv.items.size() << " items\n";
    }
};

int main() {
    Invoice inv{{100, 250}};
    std::cout << InvoicePrinter().format(inv) << "\n";
    InvoiceStore().save(inv);
}
```

```text {filename="Output (MinGW g++ 6.3.0, -std=c++14, 32-bit)"}
TOTAL Rs 413.00
saved invoice of 2 items
```

The commented-out `Invoice` would change when tax rules change, when the PDF layout changes and when the database changes. Split, each class changes for one reason, and each can be tested alone.

## 1.12.ii O: Open/closed {#s1-12-ii}

<div class="nb nb-definition" id="definition-1-12-3">

<strong>Definition 1.12.3</strong>. Software entities should be open for extension but closed for modification: new behaviour is added by adding code, not by editing code that already works.

</div>

<div class="nb nb-example nb-block" id="example-1-12-4">

<strong>Example 1.12.4</strong> (A power strip)

You add a device by plugging it in, not by rewiring the strip.

</div>

```cpp {filename="solid-ocp.cpp"}
#include <iostream>
#include <memory>
#include <string>
#include <vector>

// BAD: every new offer means editing this function.
double priceBad(double base, const std::string& offer) {
    if (offer == "festive") return base * 0.8;
    if (offer == "student") return base * 0.9;
    return base;
}

// GOOD: open for extension (new classes), closed for modification.
struct Offer {
    virtual double apply(double base) const = 0;
    virtual ~Offer() = default;
};
struct Festive : Offer {
    double apply(double b) const override { return b * 0.8; }
};
struct Student : Offer {
    double apply(double b) const override { return b * 0.9; }
};
struct Flat50 : Offer {                  // added later: nothing else edited
    double apply(double b) const override { return b - 50; }
};

double price(double base, const Offer& offer) { return offer.apply(base); }

int main() {
    std::cout << priceBad(1000, "festive") << "\n";
    std::vector<std::unique_ptr<Offer>> offers;
    offers.push_back(std::make_unique<Festive>());
    offers.push_back(std::make_unique<Student>());
    offers.push_back(std::make_unique<Flat50>());
    for (const auto& o : offers) std::cout << price(1000, *o) << " ";
    std::cout << "\n";
}
```

```text {filename="Output (MinGW g++ 6.3.0, -std=c++14, 32-bit)"}
800
800 900 950 
```

`priceBad` must be edited, retested and redeployed for every new offer, and every edit risks the old offers. With the `Offer` interface, `Flat50` was added without touching `price`. This is the Strategy pattern ([Section 1.13](../13-patterns/)).

## 1.12.iii L: Liskov substitution {#s1-12-iii}

<div class="nb nb-definition" id="definition-1-12-5">

<strong>Definition 1.12.5</strong>. Objects of a derived class must be usable wherever the base class is expected, without the caller noticing: a subclass may not strengthen the preconditions or weaken the postconditions and invariants of the base.

</div>

<div class="nb nb-example nb-block" id="example-1-12-6">

<strong>Example 1.12.6</strong> (The classic counterexample)

Mathematically every square is a rectangle. In code, a `Rectangle` promises that `setWidth` leaves the height alone, and a `Square` cannot keep that promise.

</div>

```cpp {filename="solid-lsp.cpp"}
#include <iostream>

class Rectangle {
public:
    virtual void setWidth(int w)  { w_ = w; }
    virtual void setHeight(int h) { h_ = h; }
    int area() const { return w_ * h_; }
    virtual ~Rectangle() = default;
protected:
    int w_ = 0, h_ = 0;
};

class Square : public Rectangle {      // "a square IS a rectangle"...
public:
    void setWidth(int w) override  { w_ = h_ = w; }   // keep sides equal
    void setHeight(int h) override { w_ = h_ = h; }
};

// Written against Rectangle's contract: width and height are independent.
void resizeBanner(Rectangle& r) {
    r.setWidth(5);
    r.setHeight(4);
    std::cout << "expected area 20, got " << r.area() << "\n";
}

int main() {
    Rectangle r;
    Square s;
    resizeBanner(r);
    resizeBanner(s);                   // ...but it cannot be used as one
}
```

```text {filename="Output (MinGW g++ 6.3.0, -std=c++14, 32-bit)"}
expected area 20, got 20
expected area 20, got 16
```

`resizeBanner` is correct for every `Rectangle`, yet it breaks for a `Square`. The fault is the hierarchy, not the function. Fixes: make shapes immutable (then a square really is substitutable), or do not relate the two classes by inheritance at all. Another common example: `Penguin` derived from a `Bird` that has `fly()`.

<div class="nb nb-moral">

“Is-a” in code means “behaves as a”, not “is a kind of” in the dictionary sense.

</div>

## 1.12.iv I: Interface segregation {#s1-12-iv}

<div class="nb nb-definition" id="definition-1-12-7">

<strong>Definition 1.12.7</strong>. Clients should not be forced to depend on methods they do not use: prefer several small, focused interfaces to one large one.

</div>

<div class="nb nb-example nb-block" id="example-1-12-8">

<strong>Example 1.12.8</strong> (A TV remote)

A TV remote with the buttons of every appliance in the house is useless; each device gets a remote with the buttons it actually has.

</div>

```cpp {filename="solid-isp.cpp"}
#include <iostream>
#include <stdexcept>

// BAD: one fat interface forces every device to implement everything.
struct OfficeMachine {
    virtual void print() = 0;
    virtual void scan() = 0;
    virtual void fax() = 0;
    virtual ~OfficeMachine() = default;
};
struct CheapPrinter : OfficeMachine {
    void print() override { std::cout << "printing\n"; }
    void scan() override  { throw std::logic_error("cannot scan"); }
    void fax() override   { throw std::logic_error("cannot fax"); }
};

// GOOD: small interfaces; a device implements only what it can do.
struct Printer { virtual void print() = 0; virtual ~Printer() = default; };
struct Scanner { virtual void scan() = 0;  virtual ~Scanner() = default; };
struct BasicPrinter : Printer {
    void print() override { std::cout << "printing\n"; }
};
struct AllInOne : Printer, Scanner {
    void print() override { std::cout << "printing\n"; }
    void scan() override  { std::cout << "scanning\n"; }
};

int main() {
    CheapPrinter bad;
    try {
        bad.scan();
    } catch (const std::logic_error& e) {
        std::cout << "bad design: " << e.what() << "\n";
    }
    BasicPrinter p;
    AllInOne a;
    p.print();
    Scanner& s = a;            // code that needs scanning asks for a Scanner
    s.scan();
}
```

```text {filename="Output (MinGW g++ 6.3.0, -std=c++14, 32-bit)"}
bad design: cannot scan
printing
scanning
```

`CheapPrinter` had to “implement” `scan` and `fax` by throwing, so the type system no longer tells callers what really works. With `Printer` and `Scanner` separate, a function that needs scanning asks for a `Scanner` and can only be given devices that scan.

## 1.12.v D: Dependency inversion {#s1-12-v}

<div class="nb nb-definition" id="definition-1-12-9">

<strong>Definition 1.12.9</strong>. High-level modules should not depend on low-level modules; both should depend on abstractions. The concrete dependency is supplied from outside (<strong>dependency injection</strong>).

</div>

<div class="nb nb-example nb-block" id="example-1-12-10">

<strong>Example 1.12.10</strong> (A wall socket)

Your laptop depends on the socket standard, not on the power station. The power company can switch from coal to solar without you changing your laptop.

</div>

```cpp {filename="solid-dip.cpp"}
#include <iostream>
#include <string>

// BAD: high-level policy hard-wired to a low-level detail.
//   class OrderService { SmsSender sms; ... };  // cannot switch to email

// GOOD: both depend on an abstraction; the detail is injected.
struct Notifier {
    virtual void send(const std::string& msg) = 0;
    virtual ~Notifier() = default;
};
struct SmsNotifier : Notifier {
    void send(const std::string& m) override {
        std::cout << "SMS: " << m << "\n";
    }
};
struct EmailNotifier : Notifier {
    void send(const std::string& m) override {
        std::cout << "Email: " << m << "\n";
    }
};

class OrderService {
public:
    explicit OrderService(Notifier& n) : notifier_(n) {}   // injected
    void place(int orderId) {
        notifier_.send("order #" + std::to_string(orderId) + " placed");
    }
private:
    Notifier& notifier_;
};

int main() {
    SmsNotifier sms;
    EmailNotifier email;
    OrderService(sms).place(101);
    OrderService(email).place(102);    // no change to OrderService
}
```

```text {filename="Output (MinGW g++ 6.3.0, -std=c++14, 32-bit)"}
SMS: order #101 placed
Email: order #102 placed
```

`OrderService` depends only on `Notifier`; the choice of SMS or email is made in `main`. The same design lets tests inject a fake notifier, as the payment gateway did in [Section 1.7](../07-polymorphism/).

<div class="nb nb-moral">

SOLID in one sentence: small classes with one job, extended by adding new types behind interfaces that are small, honestly substitutable, and injected rather than hard-coded.

</div>
