---
title: "Templates and STL"
weight: 5
---

4 questions asked by MathWorks. Try each one first, then open the toggle: it gives the answer, why it is right, and the idea behind it explained from scratch.

### 1 · Q21, typename and template

*Asked by: MathWorks (IIIT Delhi 2024)*

What is the purpose of the `typename` and `template` keywords in template
parameters?

- **(a)** typename declares the template parameter and template specifies the template type being passed as a parameter
- **(b)** typename specifies the template type being passed as a parameter and template declares the template parameter
- **(c)** Both are used interchangeably to specify the template type being passed as a parameter
- **(d)** Neither is required when using template template parameters

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a)**

**Why.** In `template <typename T, template <typename> class C>`, `typename T` declares a type parameter, and `template <typename> class C` declares a template template parameter: a template passed in as an argument (e.g. `std::vector`).

**Concept: template parameters.** Templates can take types (`typename T` or `class T`), values (`int N`), or other templates. `typename` and `class` are interchangeable for type parameters.

{{< /details >}}

### 2 · Q22, copy constructor

*Asked by: MathWorks (IIIT Delhi 2024); MathWorks (IISc 2024)*

```c
class A {
public:
    int a; int* b;
    A(int x, int* y) : a(x), b(y) {}
    A(const A& Ain) { this.a = Ain.a; }
};
int main() {
    A p(10, NULL);
    A q(p);
    if (q.b) std::cout << "true";
    else     std::cout << "false";
}
```

- **(a)** true
- **(b)** false
- **(c)** Compiler error

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) compiler error**

**Why.** `this` is a pointer, so `this.a` does not compile; it must be `this->a`. (Even fixed, the user-written copy constructor leaves `q.b` uninitialised, so the output would be unpredictable.)

**Concept: `this` and copy constructors.** `this` is a pointer to the current object: use `->`. A user-defined copy constructor must copy every member it needs; the compiler-generated one copies all of them.

{{< /details >}}

### 3 · Q28, a templated node

*Asked by: MathWorks (IIIT Delhi 2024)*

Select the templated node class that can be used in a li[nked list]:

- **(a)** template &lt;class T> class node { node* next; T value; }
- **(b)** template &lt;class T> class node { public: node* next; T value; }
- **(c)** class &lt;template T> class node { node* next; T value; }
- **(d)** class &lt;template T> class node { public: node* next; T value; }

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) `template <class T> class node { public: node* next; T value; }`**

**Why.** (c) and (d) have invalid syntax (`class <template T>`). In (a) the members are private by default in a `class`, so a linked-list class could not reach `next`. Inside the template, `node` means `node<T>`.

**Concept: class templates.** `template <class T>` before a class makes T a placeholder type. Members of a `class` are private by default; of a `struct`, public.

{{< /details >}}

### 4 · Q21, concatenating strings

*Asked by: MathWorks (IIT Bombay 2024)*

How do you concatenate two C++ strings?

- **(a)** #include &lt;string>, then s3 = s1 + s2
- **(b)** #include &lt;cstring>, then s1 + s2
- **(c)** strcat(s1, s2)
- **(d)** strcat(strcat(s1, s2), '\0')

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) `#include <string>`, then `s3 = s1 + s2`**

**Why.** `std::string` overloads `+` to concatenate. `strcat` works on C char arrays (and needs enough space in the destination).

**Concept: `std::string` vs C strings.** `std::string` manages its own memory and supports `+`, `==`, `.size()`. C strings are char arrays ending in `\0`, handled with `strcpy`, `strcat`, `strlen`.

{{< /details >}}
