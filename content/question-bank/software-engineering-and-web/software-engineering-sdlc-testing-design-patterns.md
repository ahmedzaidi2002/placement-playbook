---
title: "Software engineering (SDLC, testing, design patterns)"
weight: 2
---

7 questions asked by EPAM, Fujitsu, MathWorks. Try each one first, then open the toggle: it gives the answer, why it is right, and the idea behind it explained from scratch.

### 1 · Q7, edges from cyclomatic complexity

*Asked by: EPAM (EPAM freshers test)*

Given a graph with $V$ vertices, $DV$ decision vertices and $C$ connected components,
calculate the number of edges $E$ using the standard cyclomatic-complexity formula
$M = E - V + 2C$. The values are $V = 13$, $DV = 4$, $C = 1$. (The options visible are 14,
9 and 10; the fourth is cut off.)

{{< details title="Answer and explanation" closed="true" >}}

**Answer: E = 16** (presumably the cut-off fourth option)

**Why.** For a control-flow graph, cyclomatic complexity also equals (decision points + 1): M = 4 + 1 = 5. Then from M = E − V + 2C: E = M + V − 2C = 5 + 13 − 2 = 16. None of the visible 14, 9, 10 satisfies both formulas.

**Concept: cyclomatic complexity.** McCabe's measure of how many independent paths a program has. M = E − N + 2P (edges, nodes, connected components) = decisions + 1. It equals the minimum number of test cases for full branch coverage; above about 10, functions are considered hard to test.

{{< /details >}}

### 2 · SE Q1, design patterns

*Asked by: Fujitsu (IIT Kharagpur 2023)*

Which design pattern is used to represent an object that encapsulates how a set of
objects interact?

- **(a)** Singleton Pattern
- **(b)** Observer Pattern
- **(c)** Mediator Pattern
- **(d)** Prototype Pattern

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) Mediator**

**Why.** The Gang of Four defines Mediator as "an object that encapsulates how a set of objects interact": objects talk to the mediator instead of to each other (like an air-traffic control tower). Observer (ticked in the screenshot) is one-to-many notification, not an object that owns the interaction logic.

**Concept: Mediator vs Observer.** Mediator centralises complex many-to-many communication. Observer lets many listeners subscribe to one subject's changes. Both reduce coupling, in different shapes.

{{< /details >}}

### 3 · SE Q2, one instance

*Asked by: Fujitsu (IIT Kharagpur 2023)*

Which software design pattern ensures that a class has only one instance and provides
a global point of access to it?

- **(a)** Factory Method
- **(b)** Singleton
- **(c)** Observer
- **(d)** Prototype

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) Singleton**

**Why.** A private constructor plus a static accessor that creates the single instance on first use guarantees exactly one instance with global access.

**Concept: Singleton caveats.** Useful for shared resources (config, logger), but it is global state: hard to test and must be made thread-safe (e.g. a function-local static in C++11, which is initialised safely).

{{< /details >}}

### 4 · SE Q3, branch merging

*Asked by: Fujitsu (IIT Kharagpur 2023)*

In the context of version control systems (VCS), what does "branch merging" refer to?

- **(a)** Creating a new branch from the master branch
- **(b)** Combining changes from one branch into another branch
- **(c)** Deleting a branch after it's no longer needed
- **(d)** Renaming a branch to match a new feature's name

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) combining changes from one branch into another**

**Why.** For example, `git merge feature` while on `main` brings the feature branch's commits into main. If both changed the same lines, you get a merge conflict to resolve.

**Concept: branching workflow.** Create a branch per feature, commit there, then merge (or rebase) back. Merge keeps history as it happened (with a merge commit); rebase rewrites it into a straight line.

{{< /details >}}

### 5 · SE Q4, SOLID

*Asked by: Fujitsu (IIT Kharagpur 2023)*

Which of the following is NOT one of the SOLID principles of object-oriented design?

- **(a)** Single Responsibility Principle (SRP)
- **(b)** Open/Closed Principle (OCP)
- **(c)** Dependency Injection Principle (DIP)
- **(d)** Mutable State Principle (MSP)

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) Mutable State Principle** (it does not exist)

**Why.** SOLID = Single responsibility, Open–closed, Liskov substitution, Interface segregation, Dependency inversion. (Option (c) is also misnamed: the D is Dependency **Inversion**; dependency injection is a technique for applying it.)

**Concept: dependency inversion.** High-level modules should depend on abstractions (interfaces), not on concrete low-level classes. Dependency injection (passing dependencies in from outside) is how you achieve that.

{{< /details >}}

### 6 · SE Q5, cyclomatic complexity

*Asked by: Fujitsu (IIT Kharagpur 2023)*

What does the term "cyclomatic complexity" measure in software development?

- **(a)** The number of code lines in a program
- **(b)** The number of variables used in a function
- **(c)** The number of linearly independent paths through a program's control flow
- **(d)** The number of classes in an object-oriented system

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) the number of linearly independent paths through the control flow**

**Why.** McCabe's metric M = E − N + 2P on the control-flow graph; for one function it equals decision points + 1.

**Concept: why it matters.** Higher M = more paths = more tests needed and higher bug risk. Refactor functions with high M into smaller ones.

{{< /details >}}

### 7 · Q22, debuggers

*Asked by: MathWorks (NIT Durgapur 2024)*

What is the purpose of a debugger in C++?

- **(a)** To fix syntax errors in the code
- **(b)** To optimise the performance of the program
- **(c)** To analyse and detect logical errors in the program
- **(d)** To generate executables from the source code

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) to analyse and detect logical errors**

**Why.** A debugger (gdb, Visual Studio) lets you pause the running program, step through it and inspect variables to find where the logic goes wrong. Syntax errors are reported by the compiler, which also builds the executable. (The candidate's (a) is wrong.)

**Concept: debugging tools.** Breakpoints (stop at a line), stepping (over/into/out), watches (track variables), call stack (how you got here). Compile with `-g` to keep debug information.

{{< /details >}}
