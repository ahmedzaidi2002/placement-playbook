---
title: "1.10 · Templates and generic programming"
linkTitle: "1.10 Templates and generic programming"
weight: 10
math: true
---
<div class="nb-proto">

<em><span>Prototypical example for this section:</span> `Stack<T>`: one piece of code for an undo stack of `int`s and a browser history of `std::string`s.</em>

</div>

## 1.10.i Class templates {#s1-10-i}

```cpp {filename="stack-template.cpp"}
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>

template <typename T>
class Stack {
public:
    void push(const T& x) { items_.push_back(x); }
    T pop() {
        if (items_.empty()) throw std::out_of_range("pop on empty stack");
        T top = items_.back();
        items_.pop_back();
        return top;
    }
    bool empty() const { return items_.empty(); }
    std::size_t size() const { return items_.size(); }
private:
    std::vector<T> items_;
};

int main() {
    Stack<int> undo;                       // Stack<int> and Stack<std::string>
    undo.push(1);                          // are two unrelated classes
    undo.push(2);
    Stack<std::string> history;
    history.push("home");
    history.push("cart");
    int lastEdit = undo.pop();
    std::string lastPage = history.pop();
    std::cout << lastEdit << " " << lastPage << " left: " << undo.size()
              << " and " << history.size() << "\n";
    try {
        undo.pop();
        undo.pop();                        // one too many
    } catch (const std::out_of_range& e) {
        std::cout << e.what() << "\n";
    }
}
```

```text {filename="Output (MinGW g++ 6.3.0, -std=c++14, 32-bit)"}
2 cart left: 1 and 1
pop on empty stack
```

<div class="nb nb-definition" id="definition-1-10-1">

<strong>Definition 1.10.1</strong>. A <strong>class template</strong> is a pattern for classes, parameterised by types (or values). Writing `Stack<int>` makes the compiler <strong>instantiate</strong> the template: generate a real class with `T` replaced by `int`. Different arguments give unrelated classes: `Stack<int>` and `Stack<std::string>` share no code and cannot be assigned to each other.

</div>

<div class="nb nb-definition" id="fact-1-10-2">

<strong>Fact 1.10.2</strong>. Template definitions are normally placed entirely in headers, because the compiler needs the full definition at the point of instantiation. Member functions of a class template are only instantiated if they are used, so `Stack<T>` works even for a `T` that does not support some operation, as long as the functions needing it are never called.

</div>

## 1.10.ii Specialisation {#s1-10-ii}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> describing a type: something generic, but special wording for `bool` and for pointers.</em>

</div>

```cpp {filename="specialisation.cpp"}
#include <iostream>
#include <string>

template <typename T>                       // primary template
struct Describe { static std::string get() { return "some type"; } };

template <>                                 // full specialisation
struct Describe<bool> { static std::string get() { return "a yes/no flag"; } };

template <typename T>                       // partial specialisation:
struct Describe<T*> {                       // any pointer type
    static std::string get() { return "a pointer to " + Describe<T>::get(); }
};

int main() {
    std::cout << Describe<int>::get() << "\n"
              << Describe<bool>::get() << "\n"
              << Describe<bool*>::get() << "\n"
              << Describe<double**>::get() << "\n";
}
```

```text {filename="Output (MinGW g++ 6.3.0, -std=c++14, 32-bit)"}
some type
a yes/no flag
a pointer to a yes/no flag
a pointer to a pointer to some type
```

<div class="nb nb-definition" id="definition-1-10-3">

<strong>Definition 1.10.3</strong>. A <strong>full specialisation</strong> (`template <>`) replaces the template for one exact argument list. A <strong>partial specialisation</strong> replaces it for a family of arguments, such as all pointer types `T*`; only class templates can be partially specialised. The compiler picks the most specialised match.

</div>

`Describe<double**>` matched `T*` with `T = double*`, which matched again with `T = double`, which fell back to the primary template. `std::vector<bool>` is the standard library’s own (much criticised) full specialisation.

## 1.10.iii Static vs dynamic polymorphism {#s1-10-iii}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> the same `describe()` for shapes, resolved at compile time.</em>

</div>

The <strong>curiously recurring template pattern</strong> (CRTP) is a class deriving from a base template instantiated with itself, `struct Square : Shape<Square>`. The base can then cast `this` to the derived type and call its functions directly, with no virtual call:

```cpp {filename="crtp.cpp"}
#include <iostream>

// CRTP: the base knows the derived type at compile time, so no virtual.
template <typename Derived>
struct Shape {
    double area() const {
        return static_cast<const Derived*>(this)->areaImpl();
    }
    void describe() const { std::cout << "area " << area() << "\n"; }
};

struct Square : Shape<Square> {
    double s = 2;
    double areaImpl() const { return s * s; }
};
struct Rect : Shape<Rect> {
    double w = 2, h = 3;
    double areaImpl() const { return w * h; }
};

template <typename D>
void report(const Shape<D>& shape) { shape.describe(); }   // static dispatch

int main() {
    report(Square{});
    report(Rect{});
    std::cout << "sizeof(Square) = " << sizeof(Square) << " (no vptr)\n";
}
```

```text {filename="Output (MinGW g++ 6.3.0, -std=c++14, 32-bit)"}
area 4
area 6
sizeof(Square) = 8 (no vptr)
```

|  | <strong>Virtual functions</strong> | <strong>Templates / CRTP</strong> |
|:--|:--|:--|
| Decided | at run time | at compile time |
| Cost | vptr per object, indirect call, rarely inlined | none; calls can be inlined |
| Mixed collections | yes: `vector<unique_ptr<Shape>>` | no: each `Shape<D>` is a different type |
| New types | added without recompiling users | users must be recompiled |
| Errors | at the call site | sometimes long template error messages |

<div class="nb nb-moral">

Use virtual functions when the set of types is open or decided at run time (plugins, user choices, heterogeneous containers). Use templates when the type is known at compile time and speed matters (containers, algorithms, numeric code).

</div>
