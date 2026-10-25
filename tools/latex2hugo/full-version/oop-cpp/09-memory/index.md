---
title: "1.9 · Memory and ownership"
linkTitle: "1.9 Memory and ownership"
weight: 9
math: true
---
<div class="nb-proto">

<em><span>Prototypical example for this section:</span> `std::vector<std::unique_ptr<Shape>>`: a container that owns a mix of circles and squares and frees them all automatically.</em>

</div>

## 1.9.i The problem with raw `new` and `delete` {#s1-9-i}

```cpp {filename="raw-new-leak.cpp"}
#include <iostream>
#include <stdexcept>

struct Report {
    Report()  { std::cout << "  Report allocated\n"; }
    ~Report() { std::cout << "  Report freed\n"; }
};

void generate(bool fail) {
    Report* r = new Report;          // raw owning pointer
    if (fail) throw std::runtime_error("printer jammed");
    delete r;                        // skipped when we throw: LEAK
}

int main() {
    try {
        generate(true);
    } catch (const std::exception& e) {
        std::cout << "  caught: " << e.what() << "\n";
    }
    std::cout << "end of main\n";
}
```

```text {filename="Output (MinGW g++ 6.3.0, -std=c++14, 32-bit)"}
  Report allocated
  caught: printer jammed
end of main
```

“Report freed” never appears: the exception jumped over `delete`. Every raw `new` needs a matching `delete` on <em>every</em> path out of the function, including every exception, which is impossible to maintain by hand. The answer is RAII again ([Section 1.3](../03-lifecycle/)): let an object own the memory.

<div class="nb nb-definition" id="definition-1-9-1">

<strong>Definition 1.9.1</strong>. An <strong>owning</strong> pointer is responsible for deleting what it points to; a <strong>non-owning</strong> pointer only uses it. In modern C++, owning pointers are smart pointers and raw pointers (`T*`) or references are non-owning by convention.

</div>

## 1.9.ii `std::unique_ptr`: one owner {#s1-9-ii}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> car keys: exactly one person holds them, and handing them over leaves you with none.</em>

</div>

```cpp {filename="unique-ptr.cpp"}
#include <iostream>
#include <memory>
#include <utility>

struct CarKeys {
    explicit CarKeys(int id) : id(id) {
        std::cout << "  keys #" << id << " cut\n";
    }
    ~CarKeys() { std::cout << "  keys #" << id << " destroyed\n"; }
    int id;
};

std::unique_ptr<CarKeys> makeKeys(int id) {
    return std::make_unique<CarKeys>(id);      // ownership leaves the factory
}

int main() {
    std::unique_ptr<CarKeys> mine = makeKeys(7);
    std::unique_ptr<CarKeys> yours = std::move(mine);  // hand over the keys
    std::cout << "mine is " << (mine ? "set" : "empty")
              << ", yours holds #" << yours->id << "\n";
    yours.reset();                               // destroy now
    std::cout << "end of main\n";
}
```

```text {filename="Output (MinGW g++ 6.3.0, -std=c++14, 32-bit)"}
  keys #7 cut
mine is empty, yours holds #7
  keys #7 destroyed
end of main
```

- `unique_ptr` deletes its object in its destructor, or on `reset()`.
- It is move-only: ownership can be transferred with `std::move`, which leaves the source empty, but never copied, because two owners would delete twice.
- On this build it is $4$ bytes, the same as a raw pointer: no run-time cost.

```cpp {filename="unique-copy-err.cpp"}
#include <memory>

int main() {
    std::unique_ptr<int> a = std::make_unique<int>(5);
    std::unique_ptr<int> b = a;        // error: unique ownership cannot copy
}
```

```text {filename="Compiler error (MinGW g++ 6.3.0, -std=c++14, 32-bit) — this file is meant not to compile"}
unique-copy-err.cpp:5:30: error: use of deleted function 'std::unique_ptr<_Tp, _Dp>::unique_ptr(const std::unique_ptr<_Tp, _Dp>&) [with _Tp = int; _Dp = std::default_delete<int>]'
```

## 1.9.iii `std::shared_ptr`: shared ownership {#s1-9-iii}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> a family streaming plan: the account closes when the last member leaves.</em>

</div>

```cpp {filename="shared-ptr.cpp"}
#include <iostream>
#include <memory>

struct Playlist {
    ~Playlist() { std::cout << "  playlist deleted\n"; }
};

int main() {
    std::shared_ptr<Playlist> a = std::make_shared<Playlist>();
    std::cout << "owners: " << a.use_count() << "\n";
    {
        std::shared_ptr<Playlist> b = a;          // a second owner
        std::cout << "owners: " << a.use_count() << "\n";
    }                                              // b gone
    std::cout << "owners: " << a.use_count() << "\n";
    a.reset();                                     // last owner gone
    std::cout << "end of main\n";
}
```

```text {filename="Output (MinGW g++ 6.3.0, -std=c++14, 32-bit)"}
owners: 1
owners: 2
owners: 1
  playlist deleted
end of main
```

<div class="nb nb-definition" id="definition-1-9-2">

<strong>Definition 1.9.2</strong>. `std::shared_ptr` keeps a <strong>reference count</strong> of how many `shared_ptr`s own the object, stored in a separately allocated <strong>control block</strong>. Copying increments it, destroying decrements it, and the object is deleted when it reaches $0$.

</div>

The costs: two pointers per `shared_ptr` ($8$ bytes here, see the output of `custom-deleter.cpp` below), the control block, and atomic increments and decrements so that it is safe to copy across threads. Use it only when ownership is genuinely shared; `unique_ptr` should be the default.

<div class="nb nb-remark" id="remark-1-9-3">

<strong>Remark 1.9.3</strong> (`make_unique` and `make_shared`) — Prefer them to `new`: the code never contains a naked `new`, and before C++17 `f(std::shared_ptr<A>(new A), g())` could leak if `g()` threw between the `new` and the `shared_ptr` constructor. `make_shared` also puts the object and the control block in one allocation.

</div>

## 1.9.iv Cycles and `std::weak_ptr` {#s1-9-iv}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> a parent and a child that point to each other.</em>

</div>

```cpp {filename="shared-cycle.cpp"}
#include <iostream>
#include <memory>

struct Child;
struct Parent {
    std::shared_ptr<Child> child;
    ~Parent() { std::cout << "  ~Parent\n"; }
};
struct Child {
    std::shared_ptr<Parent> parent;           // owning back-pointer: a cycle
    ~Child() { std::cout << "  ~Child\n"; }
};

int main() {
    {
        auto p = std::make_shared<Parent>();
        auto c = std::make_shared<Child>();
        p->child = c;
        c->parent = p;
        std::cout << "counts: parent " << p.use_count()
                  << ", child " << c.use_count() << "\n";
    }
    std::cout << "scope ended: no destructor ran, both leaked\n";
}
```

```text {filename="Output (MinGW g++ 6.3.0, -std=c++14, 32-bit)"}
counts: parent 2, child 2
scope ended: no destructor ran, both leaked
```

<div class="nb nb-ques" id="question-1-9-4">

<strong>Question 1.9.4</strong> — Why did neither destructor run?

</div>

When `p` and `c` go out of scope, each count drops from $2$ to $1$: the parent is still owned by the child’s `parent` member, and the child by the parent’s `child` member. Neither count reaches $0$, so both objects leak. Reference counting cannot collect cycles.

<div class="nb nb-definition" id="definition-1-9-5">

<strong>Definition 1.9.5</strong>. A `std::weak_ptr` refers to an object managed by `shared_ptr`s without owning it: it does not change the count. `lock()` returns a `shared_ptr` to the object if it is still alive, or an empty one if it has been destroyed.

</div>

```cpp {filename="weak-ptr.cpp"}
#include <iostream>
#include <memory>

struct Child;
struct Parent {
    std::shared_ptr<Child> child;
    ~Parent() { std::cout << "  ~Parent\n"; }
};
struct Child {
    std::weak_ptr<Parent> parent;             // observes, does not own
    ~Child() { std::cout << "  ~Child\n"; }
    void greet() const {
        if (auto p = parent.lock())           // shared_ptr, or empty if gone
            std::cout << "  parent is alive\n";
        else
            std::cout << "  parent is gone\n";
    }
};

int main() {
    std::shared_ptr<Child> keep;
    {
        auto p = std::make_shared<Parent>();
        auto c = std::make_shared<Child>();
        p->child = c;
        c->parent = p;
        c->greet();
        keep = c;
    }
    keep->greet();
    std::cout << "end of main\n";
}
```

```text {filename="Output (MinGW g++ 6.3.0, -std=c++14, 32-bit)"}
  parent is alive
  ~Parent
  parent is gone
end of main
  ~Child
```

The back-pointer is now weak, so the parent is destroyed at the end of the scope, and the child can detect that safely. The rule for any graph of `shared_ptr`s: ownership must form a tree (or a DAG); every edge that points “back up” is a `weak_ptr`. Observers ([Section 1.13](../13-patterns/)) and caches are the other classic uses.

## 1.9.v Custom deleters {#s1-9-v}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> a `FILE*` that must be closed with `fclose`, not `delete`.</em>

</div>

```cpp {filename="custom-deleter.cpp"}
#include <cstdio>
#include <iostream>
#include <memory>

struct FileCloser {
    void operator()(std::FILE* f) const {
        std::fclose(f);
        std::cout << "  fclose called\n";
    }
};

int main() {
    {
        std::unique_ptr<std::FILE, FileCloser> f(std::tmpfile());
        std::fputs("attendance", f.get());
        std::cout << "  writing done\n";
    }                                     // FileCloser runs here
    std::cout << "sizeof(unique_ptr<int>) = "
              << sizeof(std::unique_ptr<int>) << ", sizeof(shared_ptr<int>) = "
              << sizeof(std::shared_ptr<int>) << "\n";
}
```

```text {filename="Output (MinGW g++ 6.3.0, -std=c++14, 32-bit)"}
  writing done
  fclose called
sizeof(unique_ptr<int>) = 4, sizeof(shared_ptr<int>) = 8
```

Smart pointers manage any resource with a “release” function, not just memory from `new`. With a stateless deleter type, the `unique_ptr` is still the size of one pointer.

## 1.9.vi Polymorphic containers {#s1-9-vi}

```cpp {filename="polymorphic-container.cpp"}
#include <iostream>
#include <memory>
#include <vector>

struct Shape {
    virtual double area() const = 0;
    virtual ~Shape() = default;
};
struct Square : Shape {
    explicit Square(double s) : s(s) {}
    double area() const override { return s * s; }
    double s;
};
struct Circle : Shape {
    explicit Circle(double r) : r(r) {}
    double area() const override { return 3.14159 * r * r; }
    double r;
};

int main() {
    std::vector<std::unique_ptr<Shape>> plot;      // owns every shape
    plot.push_back(std::make_unique<Square>(2));
    plot.push_back(std::make_unique<Circle>(1));
    plot.push_back(std::make_unique<Square>(3));
    double total = 0;
    for (const auto& s : plot) total += s->area();
    std::cout << "total area " << total << "\n";
}                                                  // all freed here
```

```text {filename="Output (MinGW g++ 6.3.0, -std=c++14, 32-bit)"}
total area 16.1416
```

Storing `Shape` objects by value would slice every element ([Section 1.7](../07-polymorphism/)), and storing raw `Shape*` would need a manual `delete` for each. A vector of `unique_ptr` gives polymorphism <em>and</em> automatic cleanup; the virtual destructor in `Shape` makes sure each object is destroyed as what it really is.

<div class="nb nb-moral">

Default to `unique_ptr`; use `shared_ptr` only for real shared ownership and break every cycle with `weak_ptr`; never write `delete` in application code.

</div>
