---
title: "Classes, access, static and friend"
weight: 3
---

6 questions asked by MathWorks, Qualcomm, Texas Instruments, Warner Bros. Discovery. Try each one first, then open the toggle: it gives the answer, why it is right, and the idea behind it explained from scratch.

### 1 · Q8, an empty class

*Asked by: MathWorks (IIT Bombay 2024); MathWorks (IIITDM Kancheepuram 2025)*

Given `class xyz {};`, can objects be created, and what is their size?

- **(a)** Size is zero
- **(b)** Size is greater than zero
- **(c)** Compilation error
- **(d)** Runtime error

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) size greater than zero** (sizeof is 1)

**Why.** Objects of an empty class can be created. Every object must have a distinct address, so C++ gives an empty class a size of at least 1 byte. (The candidate's "compilation error" is wrong.)

**Concept: object identity.** Two different objects must never share an address, so nothing can be 0 bytes. (As a base class, an empty class can take 0 bytes, the "empty base optimisation".)

{{< /details >}}

### 2 · Q54, design principle

*Asked by: Qualcomm (IISc)*

"Software entities such as classes, modules, functions, etc. should be open for extension
but closed for modification." Which principle is this?

- **(a)** Dependency Inversion Principle
- **(b)** Liskov Substitution Principle
- **(c)** Single Responsibility Principle
- **(d)** Open Closed Principle

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) Open-Closed Principle**

**Why.** "Open for extension, closed for modification" is exactly the O in SOLID: add new behaviour by adding code (a new subclass or plug-in), not by editing tested code.

**Concept: SOLID.**
- **S**ingle responsibility: one reason to change per class.
- **O**pen–closed: extend without modifying.
- **L**iskov substitution: a subclass must work wherever its base works.
- **I**nterface segregation: many small interfaces beat one large one.
- **D**ependency inversion: depend on abstractions, not concrete classes.

{{< /details >}}

### 3 · Access control

*Asked by: Qualcomm (Delhi campus 2024, Q58)*

Given a method in a protected class, what access modifier do you use to restrict access to that method to only the other members of the same class?

- **(a)** private
- **(b)** public
- **(c)** transient
- **(d)** protected

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) private**

**Why.** `private` restricts access to members of the same class. `protected` would also open it to subclasses (and, in Java, the package). `transient` is not an access modifier; it marks a field to skip during serialisation.

**Concept: access levels.** public: everyone. protected: the class and its subclasses (plus the package in Java). private: the class only. (Java's default, no keyword: the package.)

{{< /details >}}

### 4 · Static members

*Asked by: Qualcomm (NIT Durgapur, Q55)*

Which of the statements below is/are true?

I. A static method belongs to the class rather than to an object of the class.  
II. Static methods can be called without creating an object of the class.  
III. A static method can access static data members and can change their values.

- **(a)** Only (I)
- **(b)** All (I), (II) and (III)
- **(c)** Only (II)
- **(d)** Only (III)

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) all three**

**Why.** A static method belongs to the class (I), can be called as `ClassName.method()` without an object (II), and can read and change static data (III). It has no `this`, so it cannot use instance members directly.

**Concept: static members.** One copy per class, shared by all objects. Static methods are like global functions scoped inside the class.

{{< /details >}}

### 5 · sizeof a node class

*Asked by: Texas Instruments (NIT Calicut 2023)*

```cpp
class temp {
    int x;
    temp node;
    float y;
};
main() {
    temp head = new temp();
    display(sizeof(head), sizeof(temp));
}
```

- **(a)** 8 24
- **(b)** 24 24
- **(c)** 4 12
- **(d)** 8 12

{{< details title="Answer and explanation" closed="true" >}}

**Answer: as written it does not compile; with the intended `temp *node` and `temp *head`, a 64-bit build gives (a) 8 24.**

**Why.** A class cannot contain a member of its own type (it would be infinitely big), and `new` returns a pointer. Fixed version: `sizeof(head)` is a pointer, 8 bytes. `sizeof(temp)`: int 4, 4 bytes padding, pointer 8, float 4, 4 bytes padding to a multiple of 8 = 24.

**Concept: self-referential classes.** A linked-list node holds a **pointer** to its own type, never the type itself. Struct size includes alignment padding.

{{< /details >}}

### 6 · Q21, accessing private members

*Asked by: Warner Bros. Discovery (HireVue, Nov 2024)*

Given a class with only private data members, how would you access the members from an
object of the class?

- **(a)** Create public member functions to access those data members
- **(b)** Create private member functions to access those data members
- **(c)** Create protected member functions to access those data members
- **(d)** Private data members can never be accessed from outside the class

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) create public member functions** (getters/setters)

**Why.** Private members are only accessible inside the class, so outside code must go through public methods. Private or protected methods are not callable from outside either. (C++ `friend` functions are another route, not offered.)

**Concept: encapsulation.** Hide data, expose controlled operations. Setters can validate input; getters can compute values, so the internal representation can change without breaking users.

{{< /details >}}
