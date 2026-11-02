---
title: "Exceptions, files and miscellaneous"
weight: 4
---

3 questions asked by Fujitsu, Info Edge, MathWorks. Try each one first, then open the toggle: it gives the answer, why it is right, and the idea behind it explained from scratch.

### 1 · PC Q4, the GIL

*Asked by: Fujitsu (IIT Kharagpur 2023)*

In Python, which of the following is true about the Global Interpreter Lock (GIL)?

- **(a)** GIL allows multiple threads to execute Python code concurrently.
- **(b)** GIL is used to manage memory in Python.
- **(c)** GIL ensures that only one thread executes Python bytecode at a time.
- **(d)** GIL is a tool for handling exceptions in Python.

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) the GIL ensures only one thread executes Python bytecode at a time**

**Why.** In CPython, the Global Interpreter Lock lets only one thread run Python code at once. CPU-bound threads therefore do not run in parallel (use processes); I/O-bound threads still help, because the GIL is released while waiting.

**Concept: the GIL.** It exists to keep CPython's reference counting thread-safe. It is a lock, not a memory manager or an exception tool. For parallel computation use `multiprocessing` or libraries (NumPy) that release the GIL.

{{< /details >}}

### 2 · Q37, paradigms

*Asked by: Info Edge (Data Science II)*

Python supports:

- **(a)** Object Oriented programming
- **(b)** Structured programming
- **(c)** Functional Programming
- **(d)** All of the above

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) all of the above**

**Why.** Python supports classes and objects (OOP), plain functions and control structures (structured), and first-class functions, lambdas, map/filter (functional).

**Concept: multi-paradigm languages.** A paradigm is a style of organising code; many modern languages let you mix them.

{{< /details >}}

### 3 · Q41, sys.argv

*Asked by: MathWorks (IIT Bombay 2024)*

What is `sys.argv[0]`?

{{< details title="Answer and explanation" closed="true" >}}

**Answer: the script's name**

**Why.** `sys.argv` holds the command-line words: `argv[0]` is the program (script) name, and the user's arguments start at `argv[1]`.

**Concept: command-line arguments.** Same convention as C's `argv`. `len(sys.argv) − 1` is the number of user arguments.

{{< /details >}}
