---
title: "Object-Oriented Programming in C++"
weight: 2
sidebar:
  open: false
---

This book is everything about object-oriented programming in C++ that a placement interview or an online assessment can ask: what each feature does, why it exists, what a tricky snippet prints, the SOLID principles, design patterns and low-level design case studies. Every listing is a complete program that was compiled and run, and the box under it is its real output.

<div class="nb nb-remark">

<strong>Remark</strong> (How to read the code) — Every listing is a complete program. It was compiled with `g++ -std=c++14 -Wall -Wextra -pedantic` and run, and the box under it is what it actually printed. The compiler is MinGW g++ 6.3.0, `-std=c++14`, 32-bit on Windows. Two consequences:

- Sizes of objects are for a 32-bit build, where a pointer is $4$ bytes. On a 64-bit build pointers are $8$ bytes and every size that contains one changes. The C++ standard fixes very few sizes; where it does, the text says so.
- This toolchain has no `std::thread` or `std::mutex`, so the few examples about locks use a small stand-in class that prints what it does. The real standard-library code is shown next to it, marked as not compiled here.

</div>

## Contents

- [1.1 · Why object-oriented programming](01-why/)
- [1.2 · Classes and objects](02-classes/)
- [1.3 · Object lifecycle](03-lifecycle/)
- [1.4 · Static, const, mutable and friend members](04-members/)
- [1.5 · Operator overloading](05-operators/)
- [1.6 · Inheritance](06-inheritance/)
- [1.7 · Polymorphism](07-polymorphism/)
- [1.8 · Encapsulation and abstraction done right](08-design/)
- [1.9 · Memory and ownership](09-memory/)
- [1.10 · Templates and generic programming](10-templates/)
- [1.11 · Exceptions and classes](11-exceptions/)
- [1.12 · The SOLID principles](12-solid/)
- [1.13 · Design patterns](13-patterns/)
- [1.14 · Low-level design case studies](14-lld/)
- [1.15 · Interview rapid-fire](15-rapidfire/)
- [1.16 · A few harder problems to think about](16-problems/)
