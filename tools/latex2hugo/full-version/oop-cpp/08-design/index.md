---
title: "1.8 · Encapsulation and abstraction done right"
linkTitle: "1.8 Encapsulation and abstraction done right"
weight: 8
math: true
---
<div class="nb-proto">

<em><span>Prototypical example for this section:</span> a bank account whose balance can never be negative, however it is used.</em>

</div>

## 1.8.i Design around the invariant {#s1-8-i}

The four pillars are easy to recite. Using them well comes down to one habit: decide the class invariant first, then make every public function preserve it.

```cpp {filename="bank-invariant.cpp"}
#include <iostream>
#include <stdexcept>
#include <string>

// Invariant: balance_ >= 0 at all times, and every change is recorded.
class BankAccount {
public:
    explicit BankAccount(std::string owner) : owner_(owner) {}

    void deposit(long paise) {
        if (paise <= 0) throw std::invalid_argument("deposit must be > 0");
        balance_ += paise;
        ++transactions_;
    }
    bool withdraw(long paise) {             // refuses rather than breaks
        if (paise <= 0 || paise > balance_) return false;
        balance_ -= paise;
        ++transactions_;
        return true;
    }
    long balance() const { return balance_; }         // read-only view
    int transactions() const { return transactions_; }
    // deliberately NO setBalance(): it would let callers break the invariant
private:
    std::string owner_;
    long balance_ = 0;
    int transactions_ = 0;
};

int main() {
    BankAccount acc("Meera");
    acc.deposit(5000);
    bool big = acc.withdraw(8000);          // more than the balance
    bool small = acc.withdraw(3000);
    std::cout << std::boolalpha << big << " " << small << "\n";
    std::cout << acc.balance() << " after " << acc.transactions()
              << " transactions\n";
    try {
        acc.deposit(-10);
    } catch (const std::invalid_argument& e) {
        std::cout << e.what() << "\n";
    }
}
```

```text {filename="Output (MinGW g++ 6.3.0, -std=c++14, 32-bit)"}
false true
2000 after 2 transactions
deposit must be > 0
```

- The constructor establishes the invariant (balance $0$).
- Every public function either preserves it or refuses: `withdraw(8000)` returns `false` instead of going negative; `deposit(-10)` throws.
- There is no `setBalance`. The only ways to change the balance are the operations that the bank actually allows.

<div class="nb nb-definition" id="fact-1-8-1">

<strong>Fact 1.8.1</strong>. An invariant only has to hold between public calls. Inside a member function it may be broken temporarily, as long as it is restored before the function returns, or before it throws.

</div>

## 1.8.ii Getters and setters vs “tell, don’t ask” {#s1-8-ii}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> applying for leave: you tell HR how many days you want, and HR checks the rule.</em>

</div>

```cpp {filename="tell-dont-ask.cpp"}
#include <iostream>

// ASK style: the caller pulls data out and applies the rule itself.
struct LeaveRecordAsk {
    int used = 18;
    int allowed = 20;
};

// TELL style: the object applies its own rule.
class LeaveRecord {
public:
    bool apply(int days) {
        if (used_ + days > allowed_) return false;
        used_ += days;
        return true;
    }
    int remaining() const { return allowed_ - used_; }
private:
    int used_ = 18;
    int allowed_ = 20;
};

int main() {
    LeaveRecordAsk r1;
    int days = 5;
    if (r1.used + days <= r1.allowed)       // the rule, copied into
        r1.used += days;                    // every caller that needs it
    std::cout << "ask:  " << r1.allowed - r1.used << " left\n";

    LeaveRecord r2;
    bool granted = r2.apply(5);             // the rule lives in one place
    std::cout << std::boolalpha << "tell: " << granted << ", "
              << r2.remaining() << " left\n";
}
```

```text {filename="Output (MinGW g++ 6.3.0, -std=c++14, 32-bit)"}
ask:  2 left
tell: false, 2 left
```

<div class="nb nb-definition" id="definition-1-8-2">

<strong>Definition 1.8.2</strong>. <strong>Tell, don’t ask</strong>: rather than asking an object for its data and making decisions outside it, tell the object what you want and let it apply its own rules.

</div>

With the “ask” version, the leave rule is copied into every caller, and one forgotten copy overdraws someone’s leave; with the “tell” version it lives in one place. A class whose every member has a public getter and setter is a `struct` with extra typing. Getters for read-only information are fine; setters that let callers bypass the rules are not.

## 1.8.iii The PIMPL idiom {#s1-8-iii}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> a dashboard that shows engine status without exposing the engine’s wiring.</em>

</div>

```cpp {filename="pimpl.cpp"}
#include <iostream>
#include <memory>
#include <string>

// ---- widget.h: what users see. No private data members are visible. ----
class Dashboard {
public:
    Dashboard();
    ~Dashboard();                      // defined where Impl is complete
    void show() const;
private:
    struct Impl;                       // declared, not defined
    std::unique_ptr<Impl> impl_;       // the only data member
};

// ---- widget.cpp: the details, free to change without recompiling users --
struct Dashboard::Impl {
    std::string engineStatus = "OK";
    int fuelPercent = 64;
};
Dashboard::Dashboard() : impl_(new Impl) {}
Dashboard::~Dashboard() = default;
void Dashboard::show() const {
    std::cout << "Engine " << impl_->engineStatus << ", fuel "
              << impl_->fuelPercent << "%\n";
}

int main() {
    Dashboard d;
    d.show();
    std::cout << "sizeof(Dashboard) = " << sizeof(Dashboard) << "\n";
}
```

```text {filename="Output (MinGW g++ 6.3.0, -std=c++14, 32-bit)"}
Engine OK, fuel 64%
sizeof(Dashboard) = 4
```

<div class="nb nb-definition" id="definition-1-8-3">

<strong>Definition 1.8.3</strong>. <strong>PIMPL</strong> (pointer to implementation) moves a class’s private data into a separate struct that is only declared in the header and defined in the `.cpp` file. The public class holds just a pointer to it.

</div>

The benefits are compile-time and binary stability: changing the private members no longer changes the header, so files that include it do not need recompiling, and the class’s size and layout (here $4$ bytes, one pointer) do not change for code that is already compiled against it. Libraries shipped as binaries use it for that reason. The cost is one heap allocation and one extra indirection per access. The destructor must be defined in the `.cpp` file, where `Impl` is complete, because `std::unique_ptr` needs the full type to delete it.

<div class="nb nb-moral">

Good encapsulation exposes behaviour, not data. Ask of every public function: can a caller use this to put the object in a state the class says is impossible?

</div>
