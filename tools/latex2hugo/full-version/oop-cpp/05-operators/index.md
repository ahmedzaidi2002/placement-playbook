---
title: "1.5 · Operator overloading"
linkTitle: "1.5 Operator overloading"
weight: 5
math: true
---
<div class="nb-proto">

<em><span>Prototypical example for this section:</span> a `Fraction` type for which `1/2 + 1/3` prints `5/6`.</em>

</div>

<div class="nb nb-definition" id="definition-1-5-1">

<strong>Definition 1.5.1</strong>. <strong>Operator overloading</strong> lets a class define what the built-in operators mean for its objects. `a + b` is just a call: either `a.operator+(b)` (a member) or `operator+(a, b)` (a non-member). At least one operand must be of a class or enumeration type; you cannot change what `+` does for two `int`s.

</div>

The rule for a good overload: it should do what the operator does for `int`. `+` should not modify its operands, `==` should be symmetric, `<` should be a strict ordering so the type works with `std::sort` and `std::map`.

## 1.5.i Member or non-member? {#s1-5-i}

```cpp {filename="fraction-ops.cpp"}
#include <iostream>

long gcd(long a, long b) { return b == 0 ? (a < 0 ? -a : a) : gcd(b, a % b); }

class Fraction {
public:
    Fraction(long n, long d = 1) : n_(n), d_(d) { reduce(); }  // implicit
    long num() const { return n_; }
    long den() const { return d_; }
    Fraction& operator+=(const Fraction& o) {      // member: changes *this
        n_ = n_ * o.d_ + o.n_ * d_;
        d_ *= o.d_;
        reduce();
        return *this;
    }
private:
    void reduce() { long g = gcd(n_, d_); n_ /= g; d_ /= g; }
    long n_, d_;
};

// Non-members: both operands are treated alike, so 2 + f works too.
Fraction operator+(Fraction a, const Fraction& b) { return a += b; }
bool operator==(const Fraction& a, const Fraction& b) {
    return a.num() == b.num() && a.den() == b.den();
}
bool operator<(const Fraction& a, const Fraction& b) {
    return a.num() * b.den() < b.num() * a.den();
}
std::ostream& operator<<(std::ostream& os, const Fraction& f) {
    return os << f.num() << "/" << f.den();
}

int main() {
    Fraction half(1, 2), third(1, 3);
    std::cout << half + third << "  " << 2 + half << "  " << half + 2 << "\n";
    std::cout << std::boolalpha << (Fraction(2, 4) == half) << " "
              << (third < half) << "\n";
}
```

```text {filename="Output (MinGW g++ 6.3.0, -std=c++14, 32-bit)"}
5/6  5/2  5/2
true true
```

`2 + half` works because `operator+` is a non-member: the compiler converts `2` with the implicit constructor `Fraction(long, long = 1)`, exactly as it converts the right operand. Make `operator+` a member instead and the symmetry breaks:

```cpp {filename="fraction-member-err.cpp"}
class Fraction {
public:
    Fraction(long n, long d = 1) : n_(n), d_(d) {}
    Fraction operator+(const Fraction& o) const {     // member operator+
        return Fraction(n_ * o.d_ + o.n_ * d_, d_ * o.d_);
    }
private:
    long n_, d_;
};

int main() {
    Fraction half(1, 2);
    Fraction a = half + 2;    // fine: half.operator+(Fraction(2))
    Fraction b = 2 + half;    // error: int has no member operator+
    (void)a; (void)b;
}
```

```text {filename="Compiler error (MinGW g++ 6.3.0, -std=c++14, 32-bit) — this file is meant not to compile"}
fraction-member-err.cpp:14:20: error: no match for 'operator+' (operand types are 'int' and 'Fraction')
```

A member operator’s left operand must already be a `Fraction`; the compiler never converts the object a member function is called on.

<div class="nb nb-definition" id="fact-1-5-2">

<strong>Fact 1.5.2</strong> (Which to choose). The usual split:

- Members: operators that modify the left operand (`+=`, `-=`, `++`, `--`) and those the language requires to be members: `=`, `[]`, `()` and `->`.
- Non-members: symmetric binary operators (`+`, `-`, `==`, `<`) and `<<` / `>>` for streams, whose left operand is the stream. The usual trick is to write `+=` as a member and `+` as a non-member that calls it, as above.

</div>

## 1.5.ii Subscript, call and increment {#s1-5-ii}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> a matrix you can index as `m[1][2]`, a discount rule you can call like a function, and a turnstile counter.</em>

</div>

```cpp {filename="subscript-call-incr.cpp"}
#include <iostream>
#include <vector>

class Matrix {
public:
    Matrix(int r, int c) : cols_(c), data_(r * c, 0) {}
    // two versions: one for writing, one for reading const matrices
    int* operator[](int row) { return &data_[row * cols_]; }
    const int* operator[](int row) const { return &data_[row * cols_]; }
private:
    int cols_;
    std::vector<int> data_;
};

struct Discount {                       // a function object (functor)
    int percent;
    int operator()(int price) const { return price - price * percent / 100; }
};

class Turnstile {
public:
    Turnstile& operator++() { ++count_; return *this; }   // prefix: ++t
    Turnstile operator++(int) {                           // postfix: t++
        Turnstile before = *this;                         // extra copy
        ++count_;
        return before;
    }
    int count() const { return count_; }
private:
    int count_ = 0;
};

int main() {
    Matrix m(2, 3);
    m[1][2] = 7;
    const Matrix& view = m;
    std::cout << view[1][2] << "\n";

    Discount festive{20};
    std::cout << festive(1000) << "\n";

    Turnstile t;
    int a = (t++).count();              // old value
    int b = (++t).count();              // new value
    std::cout << a << " " << b << " " << t.count() << "\n";
}
```

```text {filename="Output (MinGW g++ 6.3.0, -std=c++14, 32-bit)"}
7
800
0 2 2
```

- `operator[]` comes in two versions, overloaded on `const`: the non-`const` one allows writing through it, the `const` one is what gets called on `view`.
- An object with `operator()` is a <strong>function object</strong> or <strong>functor</strong>: it can be called like a function but can also carry state (`percent` here). Comparators passed to `std::sort` and hash functions for `std::unordered_map` are functors.
- Prefix and postfix `++` are told apart by a dummy `int` parameter on the postfix one. Postfix has to return the <em>old</em> value, which costs a copy; that is why `++it` is preferred to `it++` for class types such as iterators.

## 1.5.iii Copy assignment with copy-and-swap {#s1-5-iii}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> `b = a;` for a class that owns a buffer, including `b = b;`.</em>

</div>

```cpp {filename="copy-swap.cpp"}
#include <algorithm>
#include <iostream>
#include <utility>

class Buffer {
public:
    explicit Buffer(int n) : size_(n), data_(new int[n]()) {}
    Buffer(const Buffer& o) : size_(o.size_), data_(new int[o.size_]) {
        std::copy(o.data_, o.data_ + size_, data_);
    }
    ~Buffer() { delete[] data_; }

    // Take the argument BY VALUE: the copy is made before we touch *this.
    Buffer& operator=(Buffer other) {
        swap(*this, other);            // take its contents...
        return *this;                  // ...other's dtor frees our old data
    }
    friend void swap(Buffer& a, Buffer& b) noexcept {
        std::swap(a.size_, b.size_);
        std::swap(a.data_, b.data_);
    }
    int& at(int i) { return data_[i]; }
    int size() const { return size_; }
private:
    int size_;
    int* data_;
};

int main() {
    Buffer a(3), b(5);
    a.at(0) = 42;
    b = a;                  // copy-assign
    b = b;                  // self-assignment is safe too
    a.at(0) = 7;            // b has its own copy
    std::cout << b.size() << " " << b.at(0) << " " << a.at(0) << "\n";
}
```

```text {filename="Output (MinGW g++ 6.3.0, -std=c++14, 32-bit)"}
3 42 7
```

<div class="nb nb-theorem nb-block" id="proposition-1-5-3">

<strong>Proposition 1.5.3</strong>

Copy-and-swap assignment is correct for self-assignment and gives the strong exception guarantee: if the copy throws, `*this` is unchanged.

</div>

<div class="nb nb-proof">

<em>Proof.</em> The copy is made when the argument `other` is initialised, before the body runs; if it throws, `*this` has not been touched. The body only swaps two pointers and two integers, which cannot throw. For `b = b`, `other` is a separate copy of `b`, so swapping with it is harmless. The old contents end up in `other` and are freed by its destructor.

</div>

Assignment returns `*this` by reference so that `a = b = c` works, as it does for `int`.

## 1.5.iv What you cannot overload {#s1-5-iv}

<div class="nb nb-definition" id="fact-1-5-4">

<strong>Fact 1.5.4</strong>. The operators `::`, `.`, `.*`, `?:`, `sizeof`, `alignof` and `typeid` cannot be overloaded. You also cannot invent new operators, change an operator’s precedence or associativity, or change how many operands it takes.

</div>

Trying it is rejected when the declaration is parsed:

```cpp {filename="no-overload-err.cpp"}
struct Point { int x, y; };

struct Proxy {
    Point p;
    Point& operator.(int);            // '.' cannot be overloaded
};

int main() {}
```

```text {filename="Compiler error (MinGW g++ 6.3.0, -std=c++14, 32-bit) — this file is meant not to compile"}
no-overload-err.cpp:5:20: error: expected type-specifier before '.' token
no-overload-err.cpp:5:12: error: expected ';' at end of member declaration
no-overload-err.cpp:5:20: error: expected unqualified-id before '.' token
```

<div class="nb nb-remark" id="remark-1-5-5">

<strong>Remark 1.5.5</strong> — `&&`, `||` and `,` <em>can</em> be overloaded, but should not be: the overloaded versions are ordinary function calls, so they lose short-circuit evaluation.

</div>
