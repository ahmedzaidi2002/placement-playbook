---
title: "7 · SOLID principles"
linkTitle: "7 SOLID"
weight: 7
math: true
---
Five principles that keep object-oriented code easy to change. Interviewers want the one-line meaning, a violation, and the fix.

## 7.1 S: Single responsibility {#oop-7-1}

**A class should have one reason to change.**

- *Violation:* `Invoice` calculates totals, prints itself, and saves itself to the database. A change to the database schema or the print format both touch this class.
- *Fix:* `Invoice` (data and totals), `InvoicePrinter`, `InvoiceRepository`.

## 7.2 O: Open/closed {#oop-7-2}

**Open for extension, closed for modification:** add new behaviour by adding code, not by editing working code.

- *Violation:* `area(Shape s)` with `if (s.type == CIRCLE) … else if (s.type == SQUARE) …`; every new shape edits this function.
- *Fix:* an abstract `Shape` with a virtual `area()`; a new shape is a new class.

## 7.3 L: Liskov substitution {#oop-7-3}

**A subclass must be usable wherever its base class is expected, without surprises** (it must keep the base's promises).

- *Violation:* `Square` inherits `Rectangle` and overrides `setWidth` to also set the height. Code that sets width 5 and height 4 and expects area 20 gets 16. Or `Penguin` inherits `Bird::fly()` and throws.
- *Fix:* do not model it as inheritance; use a common `Shape` interface, or split `Bird` into `FlyingBird` and others.

## 7.4 I: Interface segregation {#oop-7-4}

**Clients should not be forced to depend on methods they do not use.** Prefer several small interfaces to one fat one.

- *Violation:* a `Machine` interface with `print()`, `scan()`, `fax()`; a simple printer must implement `scan` and `fax` with empty or throwing bodies.
- *Fix:* `Printer`, `Scanner`, `Fax` interfaces; a multifunction device implements all three.

## 7.5 D: Dependency inversion {#oop-7-5}

**High-level modules should depend on abstractions, not on concrete low-level classes.**

- *Violation:* `OrderService` creates a `MySQLDatabase` inside itself; switching databases or testing with a fake means editing `OrderService`.
- *Fix:* `OrderService` depends on a `Database` interface passed in through its constructor (**dependency injection**); `MySQLDatabase` and `FakeDatabase` implement it.

<div class="nb nb-moral">

S: one reason to change. O: extend by adding classes, not editing them. L: subclasses keep the base's promises. I: small focused interfaces. D: depend on interfaces and inject the implementation.

</div>
