---
title: "8 · Design patterns"
linkTitle: "8 Design patterns"
weight: 8
math: true
---
A design pattern is a reusable solution to a recurring design problem. Three families: **creational** (how objects are created), **structural** (how classes are composed), **behavioural** (how objects interact). For each: the problem, the idea, and when to use it.

## 8.1 Creational {#oop-8-1}

**Singleton:** exactly one instance with a global access point (a logger, configuration, connection pool).
- *How:* private constructor, deleted copy, and a static `getInstance()`. In C++11 the simplest thread-safe version is a **function-local static** (`static Logger instance; return instance;`), which the language initialises exactly once.
- *Criticism:* it is hidden global state, makes testing harder, and couples code. Prefer passing the object in.

**Factory (factory method):** create objects without the caller naming the concrete class: `ShapeFactory::create("circle")` returns a `Shape*`. Adding a type changes only the factory. **Abstract factory:** a factory of related families (a `WindowsUIFactory` makes Windows buttons and checkboxes).

**Builder:** build a complex object step by step (`Pizza::Builder().size(L).cheese().olives().build()`), avoiding constructors with many parameters.

## 8.2 Structural {#oop-8-2}

**Adapter:** make an existing class fit an interface it was not written for (a wrapper that converts calls), like a power-plug adapter. Example: wrap an old `XmlPaymentGateway` so it implements your `PaymentProcessor` interface.

**Decorator:** add responsibilities to an object at run time by wrapping it in an object with the same interface: `Milk(Sugar(Coffee))`, each adding cost; Java's `BufferedInputStream(FileInputStream)`. An alternative to a subclass for every combination.

**Facade:** one simple interface in front of a complex subsystem (`HomeTheater.watchMovie()` drives the TV, amplifier and player).

**Proxy:** a stand-in that controls access to the real object (lazy loading, caching, access control, remote objects).

## 8.3 Behavioural {#oop-8-3}

**Strategy:** a family of interchangeable algorithms behind one interface, chosen at run time: a `PaymentStrategy` (card, UPI, wallet), or a sort comparator. Replaces long `if/else` chains; follows open/closed.

**Observer (publish–subscribe):** when one object (subject) changes, all registered observers are notified automatically: event listeners, a stock price feeding several displays, notifications. The subject keeps a list of observers and calls `update()` on each.

**State:** an object changes its behaviour when its internal state changes, by delegating to a state object (`VendingMachine` in `Idle`, `HasMoney`, `Dispensing`). Replaces large `switch (state)` blocks.

**Command:** wrap a request as an object, so you can queue it, log it or **undo** it (editor actions, remote-control buttons).

**Template method:** the base class fixes the steps of an algorithm and lets subclasses fill in some steps.

**Iterator:** walk a collection without exposing its internals (every STL container).

## 8.4 Which pattern when {#oop-8-4}

| Problem | Pattern |
|---|---|
| Only one instance should exist | Singleton |
| Create objects without naming concrete classes | Factory |
| Many optional constructor parameters | Builder |
| Make an incompatible class fit an interface | Adapter |
| Add features to objects dynamically | Decorator |
| Simplify a complex subsystem | Facade |
| Swap algorithms at run time | Strategy |
| Notify many objects of a change | Observer |
| Behaviour depends on the current state | State |
| Undo / queue operations | Command |

<div class="nb nb-moral">

Creational: Singleton, Factory, Builder. Structural: Adapter, Decorator, Facade, Proxy. Behavioural: Strategy, Observer, State, Command. Name the problem first, then the pattern.

</div>
