---
title: "References, pointers and memory in C++"
weight: 6
---

3 questions asked by MathWorks. Try each one first, then open the toggle: it gives the answer, why it is right, and the idea behind it explained from scratch.

### 1 · Q25, pointer increments

*Asked by: MathWorks (IIIT Delhi 2024)*

```cpp
int a[5] = {1,2,3,4,5};
int *ptr = a;
cout << *++ptr << endl;
cout << *(ptr++) << endl;
cout << *ptr << endl;
```

- **(a)** 1 2 3
- **(b)** 1 2 2
- **(c)** 2 2 2
- **(d)** 2 2 3

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) 2 2 3**

**Why.** `*++ptr`: move to a[1], read 2. `*(ptr++)`: read a[1] = 2, then move to a[2]. `*ptr`: read a[2] = 3.

**Concept: pre vs post increment on pointers.** `++p` moves first, then you use it. `p++` gives the old position for the expression and moves afterwards.

{{< /details >}}

### 2 · Q35, pointer arithmetic

*Asked by: MathWorks (IISc 2024)*

```cpp
int arr[] = {11, 22, 33, 44, 55};
for (int i = 0; i < 5; i++)
    cout << *(arr + i) << " ";
```

{{< details title="Answer and explanation" closed="true" >}}

**Answer: 11 22 33 44 55**

**Why.** `*(arr + i)` is `arr[i]`, so the loop prints every element.

**Concept: array name decays to a pointer.** In most expressions `arr` becomes `&arr[0]`, so `arr + i` points to element i.

{{< /details >}}

### 3 · Q39, new versus malloc

*Asked by: MathWorks (IISc 2024); MathWorks (IIT Bombay 2024); MathWorks (IIIT Delhi 2024)*

Select all true statements.

- **(a)** new calls the constructor while malloc does not
- **(b)** new is an operator while malloc is a function
- **(c)** new can be overloaded while malloc cannot
- **(d)** new returns the exact data type while malloc returns void*
- **(e)** new returns NULL if memory is unavailable while malloc throws an exception

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a), (b), (c) and (d)** are true; (e) is backwards.

**Why.** `new` calls the constructor (malloc does not), is an operator (malloc is a library function), can be overloaded, and returns a correctly typed pointer (malloc returns `void*`). On failure `new` throws `std::bad_alloc`, while `malloc` returns NULL.

**Concept: new/delete vs malloc/free.** In C++ use `new`/`delete` (or better, smart pointers and containers) so constructors and destructors run. Never mix them: memory from `new` must be released with `delete`, from `malloc` with `free`.

{{< /details >}}
