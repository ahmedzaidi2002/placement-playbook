---
title: "1.11 · Exceptions and classes"
linkTitle: "1.11 Exceptions and classes"
weight: 11
math: true
---
<div class="nb-proto">

<em><span>Prototypical example for this section:</span> a database connection whose constructor fails when the password is wrong.</em>

</div>

## 1.11.i Throwing from a constructor {#s1-11-i}

A constructor has no return value, so it cannot return an error code. Throwing is the way to say “this object could not be created”.

```cpp {filename="ctor-throw.cpp"}
#include <iostream>
#include <stdexcept>

struct Socket {
    Socket()  { std::cout << "  socket opened\n"; }
    ~Socket() { std::cout << "  socket closed\n"; }
};
struct Auth {
    Auth() { throw std::runtime_error("wrong password"); }
};

class DbConnection {
public:
    DbConnection() { std::cout << "  DbConnection body\n"; }
    ~DbConnection() { std::cout << "  ~DbConnection\n"; }
private:
    Socket socket_;       // constructed first...
    Auth auth_;           // ...then this one throws
};

int main() {
    try {
        DbConnection db;
    } catch (const std::exception& e) {
        std::cout << "  caught: " << e.what() << "\n";
    }
}
```

```text {filename="Output (MinGW g++ 6.3.0, -std=c++14, 32-bit)"}
  socket opened
  socket closed
  caught: wrong password
```

<div class="nb nb-theorem nb-block" id="theorem-1-11-1">

<strong>Theorem 1.11.1</strong>

If a constructor throws, the object is considered never to have existed: its destructor does <em>not</em> run. Every member and base that was already fully constructed <em>is</em> destroyed, in reverse order.

</div>

Here `socket_` was built, `auth_` threw, so the socket was closed and `~DbConnection` never ran. This is why members should own their resources (RAII): if `DbConnection` had opened the socket with a raw handle in its body, nothing would have closed it.

## 1.11.ii Never throw from a destructor {#s1-11-ii}

```cpp {filename="dtor-throw.cpp"}
#include <iostream>
#include <stdexcept>

struct Logger {
    ~Logger() noexcept(false) {              // explicitly allowed to throw
        std::cout << "  ~Logger throws\n";
        throw std::runtime_error("disk full while flushing");
    }
};

int main() {
    try {
        Logger log;
        throw std::runtime_error("request failed");   // unwinding starts...
    } catch (const std::exception& e) {               // ...and ~Logger throws
        std::cout << "  caught: " << e.what() << "\n"; // during it
    }
    std::cout << "never printed\n";
}
```

```text {filename="Output (MinGW g++ 6.3.0, -std=c++14, 32-bit)"}
  ~Logger throws
terminate called after throwing an instance of 'std::runtime_error'
  what():  disk full while flushing
[program exited with status 3]
```

<div class="nb nb-definition" id="fact-1-11-2">

<strong>Fact 1.11.2</strong>. If an exception escapes a destructor while another exception is already propagating (during stack unwinding), the program calls `std::terminate`. Since C++11, destructors are implicitly `noexcept`, so an escaping exception terminates the program even without a second one; the example had to write `noexcept(false)` to get as far as it did.

</div>

A destructor that can fail (flushing a file, closing a connection) should catch and log the error, and offer a separate function such as `close()` that callers can use when they want to handle the failure.

## 1.11.iii Exception-safety guarantees {#s1-11-iii}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> a bank transfer that fails halfway.</em>

</div>

<div class="nb nb-definition" id="definition-1-11-3">

<strong>Definition 1.11.3</strong>. A function offers:

- the <strong>basic guarantee</strong> if, when it throws, no resources leak and all invariants still hold, though the state may have changed;
- the <strong>strong guarantee</strong> if, when it throws, the state is exactly as before the call (commit or roll back);
- the <strong>nothrow guarantee</strong> if it never throws (`noexcept`).

</div>

```cpp {filename="strong-guarantee.cpp"}
#include <iostream>
#include <stdexcept>
#include <vector>

struct Ledger {
    std::vector<long> balances{1000, 500};

    // Basic guarantee only: a failure midway leaves money missing.
    void transferBasic(int from, int to, long amt) {
        balances[from] -= amt;
        if (to >= (int)balances.size()) throw std::out_of_range("no account");
        balances[to] += amt;
    }
    // Strong guarantee: do the work on a copy, then commit with a swap.
    void transferStrong(int from, int to, long amt) {
        std::vector<long> copy = balances;
        copy[from] -= amt;
        if (to >= (int)copy.size()) throw std::out_of_range("no account");
        copy[to] += amt;
        balances.swap(copy);          // noexcept: commit or nothing
    }
    long total() const { return balances[0] + balances[1]; }
};

int main() {
    Ledger a, b;
    try { a.transferBasic(0, 5, 300); }  catch (const std::exception&) {}
    try { b.transferStrong(0, 5, 300); } catch (const std::exception&) {}
    std::cout << "basic:  total " << a.total() << "\n"
              << "strong: total " << b.total() << "\n";
}
```

```text {filename="Output (MinGW g++ 6.3.0, -std=c++14, 32-bit)"}
basic:  total 1200
strong: total 1500
```

The basic transfer debited the source before failing, and Rs 300 vanished. The strong version works on a copy and commits with a `swap`, which cannot throw, so on failure the ledger is untouched. This “copy, modify, swap” shape is the same idea as copy-and-swap assignment ([Section 1.5](../05-operators/)).

## 1.11.iv `noexcept` move constructors {#s1-11-iv}

```cpp {filename="noexcept-move.cpp"}
#include <iostream>
#include <vector>

int copies = 0, moves = 0;

struct Slow {                        // move constructor NOT noexcept
    Slow() = default;
    Slow(const Slow&) { ++copies; }
    Slow(Slow&&) { ++moves; }
};
struct Fast {                        // move constructor noexcept
    Fast() = default;
    Fast(const Fast&) { ++copies; }
    Fast(Fast&&) noexcept { ++moves; }
};

template <typename T>
void grow(const char* name) {
    copies = moves = 0;
    std::vector<T> v;
    for (int i = 0; i < 1000; ++i) v.emplace_back();   // many reallocations
    std::cout << name << ": " << copies << " copies, " << moves << " moves\n";
}

int main() {
    grow<Slow>("Slow");
    grow<Fast>("Fast");
}
```

```text {filename="Output (MinGW g++ 6.3.0, -std=c++14, 32-bit)"}
Slow: 1023 copies, 0 moves
Fast: 0 copies, 1023 moves
```

<div class="nb nb-ques" id="question-1-11-4">

<strong>Question 1.11.4</strong> — The two classes differ only in the word `noexcept`. Why does `std::vector` copy one and move the other?

</div>

When a vector grows, it allocates a bigger buffer and transfers the elements. `push_back` promises the strong guarantee. If it <em>moved</em> elements and a move threw halfway, the old buffer would already be partly emptied and could not be restored. So the vector moves only if the move constructor is `noexcept` (or there is no copy constructor), and otherwise copies, which leaves the old buffer intact. (The library function is `std::move_if_noexcept`.)

<div class="nb nb-moral">

Mark move constructors and move assignments `noexcept` whenever they cannot throw, which is almost always. Forgetting it silently turns every reallocation into copies.

</div>
