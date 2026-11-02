---
title: "OOP rules (overriding, constructors, initialisation)"
weight: 1
---

4 questions asked by Qualcomm, Warner Bros. Discovery. Try each one first, then open the toggle: it gives the answer, why it is right, and the idea behind it explained from scratch.

### 1 · Q58, initialisation blocks

*Asked by: Qualcomm (Nov 2024)*

Which statement(s) is/are true? (I) Static initialisation blocks run once, when the class is
first loaded. (II) Instance initialisation blocks run every time a new instance is created.

- **(a)** Only (I)
- **(b)** Only (II)
- **(c)** Both (I) and (II)
- **(d)** Neither (I) nor (II)

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) both** (Java)

**Why.** A static initialisation block runs once, when the class is loaded. An instance initialisation block runs every time an object is created, before the constructor body.

**Concept: Java initialisation order.** On class load: static fields and static blocks, in order. On each `new`: superclass constructor, then instance fields and instance blocks, then the rest of the constructor.

{{< /details >}}

### 2 · Q45, overriding rules

*Asked by: Qualcomm (Nov 2024)*

Which statement(s) is/are rule(s) for overriding a method? (I) If a method cannot be
inherited, it cannot be overridden. (II) A method declared as static cannot be overridden and
cannot be re-declared [cut off in the source]. (III) Instance methods cannot be overridden.

- **(a)** Only (III)
- **(b)** Only (I) and (III)
- **(c)** Only (I)
- **(d)** Only (II) and (III)

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) only (I)**

**Why.** (I) True: a method a subclass cannot inherit (e.g. private) cannot be overridden. (II) False: a static method cannot be overridden, but a subclass **can** re-declare it (method hiding). (III) False: instance methods are exactly the ones that get overridden.

**Concept: overriding vs hiding.** Overriding replaces an inherited instance method and is chosen at run time by the object's type. A static method with the same signature in a subclass hides the parent's, and the call is chosen at compile time by the reference type.

{{< /details >}}

### 3 · Q20, constructor chain

*Asked by: Warner Bros. Discovery (HireVue, Nov 2024)*

What is the output of the following code?

```java
class Person {
    public Person() {
        System.out.println("Person created");
    }
}

class Superhero extends Person {
    public Superhero() {
        System.out.println("Superhero created");
    }
}

class Batman extends Superhero {
    public Batman() {
        System.out.println("Batman created");
    }
}

class Main {
    public static void main(String[] args) {
        Batman myHero = new Batman();
    }
}
```

- **(a)** Person created Superhero created Batman created
- **(b)** Batman created Superhero created Person created
- **(c)** Batman created
- **(d)** Runtime Error

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) Person created, Superhero created, Batman created**

**Why.** Every constructor first calls its superclass constructor (an implicit `super()`), so construction runs from the top of the hierarchy down: Person, then Superhero, then Batman.

**Concept: constructor chaining.** A subclass object contains its superclass part, which must be built first. If you don't write `super(...)`, Java inserts `super()` as the first statement.

{{< /details >}}

### 4 · Q26, final method and a missing method

*Asked by: Warner Bros. Discovery (HireVue, Nov 2024)*

What is the output of the following code?

```java
class Superhero {
    final public void greet() {
        System.out.println("Greetings from a Superhero");
    }
}

class Batman extends Superhero {
    public void greet() {
        System.out.println("Greetings from Batman");
    }
}

class Main {
    public static void main(String[] args) {
        Superhero myHero = new Batman();
        myHero.show();
    }
}
```

- **(a)** Greetings from a Superhero
- **(b)** Greetings from Batman
- **(c)** Compiler Error
- **(d)** Runtime Error

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) compiler error**

**Why.** Two separate errors: `Batman.greet()` tries to override a `final` method, which is not allowed; and `Superhero` has no `show()` method, so `myHero.show()` cannot compile.

**Concept: `final` and static typing.** A `final` method cannot be overridden. The compiler checks method calls against the reference's declared type (Superhero), not the object's run-time type.

{{< /details >}}
