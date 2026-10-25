---
title: 19 · Design patterns that get asked
weight: 21
---

## Why this matters in an interview

A **design pattern** is a named, proven solution to a problem that keeps coming up in object-oriented
code. Interviewers use the names as shorthand ("use a Strategy here"), and LLD problems
quietly depend on them: pricing rules are a Strategy, notifications are an Observer, a vending machine is a State.
You need to recognise **the problem each pattern solves**, not memorise diagrams.

All code below is C++17, and every snippet was compiled and run together. The shared header is:

```cpp
#include <bits/stdc++.h>
using namespace std;
```

## The six to know

| Pattern | The problem it solves | One-line memory |
|---|---|---|
| **Strategy** | Several interchangeable ways to do one job, chosen at runtime | Swap the algorithm |
| **Observer** | When one object changes, many others must be told | Subscribe and get notified |
| **Factory** | Creating objects without the caller knowing the concrete class | Ask for it by name |
| **Singleton** | Exactly one shared instance | One and only one |
| **Builder** | Constructing an object with many optional parts step by step | Readable construction |
| **State** | Behaviour changes with the object's current state | Replace `if(state==...)` with objects |

## 1. Strategy

**Problem:** parking can be billed per hour or at a flat rate, and new rules will come. A growing `if/else` in the billing code breaks Open/Closed (chapter 18).

**Idea:** put each algorithm behind a common interface and let the user of it hold one.

```cpp
class Pricing {
public:
    virtual ~Pricing() = default;
    virtual int cost(int mins) const = 0;
};
class HourlyPricing : public Pricing {
public:
    int cost(int mins) const override { return ((mins + 59) / 60) * 20; }
};
class FlatPricing : public Pricing {
public:
    int cost(int) const override { return 50; }
};

class Parking {
    unique_ptr<Pricing> pricing;
public:
    Parking(unique_ptr<Pricing> p) : pricing(move(p)) {}
    int bill(int mins) const { return pricing->cost(mins); }
};
// Parking a(make_unique<HourlyPricing>()), b(make_unique<FlatPricing>());
// a.bill(90) == 40 (two started hours), b.bill(90) == 50
```

**Use when:** fee rules, sorting orders, payment methods, routing algorithms, rate-limiting algorithms.
**Interview note:** this is the most useful pattern. The parking lot in chapter 20 uses it.

## 2. Observer

**Problem:** when a stock price changes, an email service, an SMS service and a dashboard all need to know. The stock should not know about each of them.

**Idea:** the subject keeps a list of observers and calls each when something happens.

```cpp
class Observer {
public:
    virtual ~Observer() = default;
    virtual void update(const string& msg) = 0;
};
class EmailAlert : public Observer {
public:
    void update(const string& msg) override { cout << "email: " << msg << "\n"; }
};
class SmsAlert : public Observer {
public:
    void update(const string& msg) override { cout << "sms: " << msg << "\n"; }
};

class Stock {
    vector<Observer*> obs;
public:
    void attach(Observer* o) { obs.push_back(o); }
    void setPrice(int p) {
        for (auto* o : obs) o->update("price=" + to_string(p));
    }
};
// attach an EmailAlert and a SmsAlert, then setPrice(101) prints:
// email: price=101
// sms: price=101
```

**Use when:** event systems, notifications, UI updates, publishing a change to several listeners. It is the in-process cousin of pub-sub (chapter 08).
**Watch out for:** the subject holds raw pointers here, so observers must outlive it (or detach first). Mention a `detach` method, or `weak_ptr`, if asked.

## 3. Factory

**Problem:** the caller should say *"give me a circle"* without writing `new Circle(...)` and depending on that class everywhere.

```cpp
class Shape {
public:
    virtual ~Shape() = default;
    virtual double area() const = 0;
};
class Circle : public Shape {
    double r;
public:
    Circle(double r) : r(r) {}
    double area() const override { return 3.14159 * r * r; }
};
class Square : public Shape {
    double s;
public:
    Square(double s) : s(s) {}
    double area() const override { return s * s; }
};

unique_ptr<Shape> makeShape(const string& type, double x) {
    if (type == "circle") return make_unique<Circle>(x);
    if (type == "square") return make_unique<Square>(x);
    return nullptr;   // unknown type
}
// makeShape("square", 3)->area() == 9, makeShape("hexagon", 1) == nullptr
```

**Use when:** creating the right vehicle, notification channel, parser or payment handler from a type string or enum. Centralises the "which class?" decision in one place.
**Interview note:** the factory function still has an `if` chain, but only **in one place**. Callers stay clean.

## 4. Singleton

**Problem:** one logger, one configuration, one connection pool shared across the program.

```cpp
class Logger {
    Logger() = default;                          // private: nobody else can construct one
public:
    Logger(const Logger&) = delete;
    Logger& operator=(const Logger&) = delete;
    static Logger& get() {
        static Logger inst;                      // created once, on first use
        return inst;
    }
    void log(const string& s) { cout << "[log] " << s << "\n"; }
};
// Logger::get().log("one"); &Logger::get() == &Logger::get()  -> true
```

In C++11 and later, initialising a **function-local static** is guaranteed to be **thread safe**, so this version needs no manual locking for creation.

**Use when:** truly one instance is required (a logger, a config).
**Be honest about the cost:** a singleton is **global state**. It hides dependencies and makes testing harder. Many interviewers like hearing: *"I would usually pass the object in (dependency injection) and only use a singleton when there must be one."*

## 5. Builder

**Problem:** an object with many optional settings and a constructor with seven parameters nobody can read.

```cpp
class Request {
    string url;
    string method = "GET";
    int timeoutMs = 1000;
    Request() = default;
    friend class RequestBuilder;
public:
    void print() const { cout << method << " " << url << " timeout=" << timeoutMs << "\n"; }
};

class RequestBuilder {
    Request r;
public:
    RequestBuilder& url(string u) { r.url = move(u); return *this; }
    RequestBuilder& method(string m) { r.method = move(m); return *this; }
    RequestBuilder& timeout(int ms) { r.timeoutMs = ms; return *this; }
    Request build() { return r; }
};
// RequestBuilder().url("/home").method("POST").timeout(250).build().print();
// prints: POST /home timeout=250
```

Each setter returns `*this`, so calls chain. Defaults apply to anything you skip.

**Use when:** objects with many optional fields (HTTP requests, queries, configuration, meals in a restaurant app).

## 6. State

**Problem:** a traffic light, a vending machine or an order behaves differently depending on its state. Putting `if (state == RED) ... else if ...` in every method is messy and breaks Open/Closed.

**Idea:** make each **state a class** that knows what to do and which state comes next.

```cpp
class Light;
class LightState {
public:
    virtual ~LightState() = default;
    virtual void next(Light& l) = 0;
    virtual string name() const = 0;
};
class Light {
    unique_ptr<LightState> st;
public:
    Light();
    void setState(unique_ptr<LightState> s) { st = move(s); }
    void next() { st->next(*this); }
    string name() const { return st->name(); }
};
class Red : public LightState {
public:
    void next(Light& l) override;
    string name() const override { return "RED"; }
};
class Green : public LightState {
public:
    void next(Light& l) override;
    string name() const override { return "GREEN"; }
};
class Yellow : public LightState {
public:
    void next(Light& l) override;
    string name() const override { return "YELLOW"; }
};

Light::Light() : st(make_unique<Red>()) {}
void Red::next(Light& l) { l.setState(make_unique<Green>()); }
void Green::next(Light& l) { l.setState(make_unique<Yellow>()); }
void Yellow::next(Light& l) { l.setState(make_unique<Red>()); }
// starting at RED and calling next() four times visits: RED GREEN YELLOW RED GREEN
```

The methods of the next states are defined **after** every class is declared, because each state refers to the next one.
One subtle point: `setState` destroys the current state object, so `next` must not touch its own members afterwards. Here it does nothing after `setState`, which is safe.

**Use when:** vending machines, order lifecycle (placed, paid, shipped), document workflows, media players.
**Simple alternative:** if there are only two or three states with little logic, an `enum` and a `switch` is fine, as the vending machine in chapter 20 shows. Move to State classes when the per-state behaviour grows.

## Which pattern for which problem?

| You see in the problem... | Think |
|---|---|
| "Different pricing / sorting / payment methods" | Strategy |
| "When X happens, notify A, B and C" | Observer |
| "Create the right type from input" | Factory |
| "Only one instance" | Singleton (with care) |
| "Many optional settings" | Builder |
| "Behaves differently depending on its status" | State |

Other names worth recognising (you will not usually be asked to code them): **Decorator** (wrap an object to add behaviour), **Adapter** (make one interface look like another), **Command** (turn a request into an object, useful for undo), **Facade** (one simple front for a complicated subsystem), **Template Method** (a fixed skeleton with overridable steps).

## Trade-offs

| Decision | Choose A when... | Choose B when... |
|---|---|---|
| Pattern vs plain code | A: you can name the variation you expect | B: the code is simple. Do not force a pattern |
| Strategy vs `if/else` | A: several algorithms, more to come | B: two options that will never grow |
| State classes vs enum | A: behaviour per state is large | B: few states, little logic |
| Singleton vs injected object | A: exactly one is truly required | B: you want testability (usually) |

## Interview angle

- Name the pattern **after** describing the problem: "The fee rule can vary, so I'll make it a Strategy."
- Do not sprinkle patterns for show. One or two well-justified ones beat five forced ones.
- Be ready to explain the downside of Singleton (global state) and the lifetime issue of Observer.
- Common follow-ups: Strategy vs State (both swap objects: Strategy is chosen **from outside** and the algorithm does not change itself, State **changes itself** as events happen). Factory vs Builder (Factory picks **which** class, Builder assembles **one complex** object).

## Check yourself

1. Which pattern replaces a long `if (paymentType == ...)` chain, and how?
2. How is Observer related to pub-sub from chapter 08?
3. Why is the function-local static Singleton safe to create from several threads?
4. When would you use Builder rather than a constructor?
5. Strategy and State look alike. How do they differ?
6. Give one criticism of Singleton.

{{< details title="Answers" >}}

1. Strategy. Each payment method becomes a class behind a common interface, and the caller holds the chosen one, so adding a method means adding a class, not editing the chain.
2. Observer is the in-process version: a subject notifies registered listeners directly. Pub-sub does the same across services through a broker, with the publisher unaware of the subscribers.
3. Since C++11, initialising a function-local static is guaranteed to happen exactly once even if several threads reach it at the same time.
4. When the object has many optional fields, so a long parameter list would be hard to read and easy to get wrong.
5. Strategy is chosen from outside and stays fixed while it runs (different ways to do the same job). State transitions by itself as events happen, and the object's behaviour changes with it.
6. It is global state: it hides dependencies and makes code harder to test and reason about.

{{< /details >}}

## Remember

- Know six: **Strategy, Observer, Factory, Singleton, Builder, State**. Each one is "a problem plus a shape".
- Strategy swaps algorithms. Observer notifies many. Factory picks the class. Builder assembles step by step. State replaces status `if`s with objects.
- Function-local static gives a thread-safe Singleton in C++11 and later, but it is still global state.
- Use a pattern only when you can name the variation it protects.

{{< callout type="info" >}}
**Further reading:** any classic design-patterns reference for Strategy, Observer and State, and the object-oriented design questions in the
[System Design Primer](https://github.com/donnemartin/system-design-primer) to see patterns in use.
{{< /callout >}}
