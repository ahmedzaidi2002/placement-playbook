---
title: "6 · Smart pointers, templates and exceptions"
linkTitle: "6 Memory, templates, exceptions"
weight: 6
math: true
---
## 6.1 Why not raw new/delete {#oop-6-1}

Manual `new`/`delete` leads to **memory leaks** (forgot `delete`, or an exception skipped it), **double deletes**, and **dangling pointers** (using memory after it was freed). Rule: use **RAII** owners instead.

## 6.2 Smart pointers {#oop-6-2}

| Smart pointer | Ownership | Notes |
|---|---|---|
| `unique_ptr<T>` | **exactly one** owner | cannot be copied, only **moved**; zero overhead; the default choice |
| `shared_ptr<T>` | **shared**; a reference count | the object is deleted when the last `shared_ptr` goes away; count lives in a control block (atomic, some overhead) |
| `weak_ptr<T>` | **non-owning** observer of a `shared_ptr` | does not keep the object alive; `lock()` to use it; **breaks reference cycles** |

- Create with `make_unique<T>(...)` / `make_shared<T>(...)` (exception-safe; `make_shared` allocates the object and control block together).
- **Cycle problem:** two objects holding `shared_ptr`s to each other (parent ↔ child) never reach count 0 → leak. Make one direction a `weak_ptr` (child → parent).

## 6.3 Templates {#oop-6-3}

**Generic programming:** write the code once for any type; the compiler generates a version per type used (**instantiation**).

- **Function template:** `template <typename T> T maxOf(T a, T b) { return a > b ? a : b; }`.
- **Class template:** `template <typename T> class Stack { … };`, as in `vector<int>`.
- **Specialisation:** a custom version for one type (`Stack<bool>` packed as bits).
- Templates are **compile-time polymorphism**: no virtual-call cost, but larger binaries (code bloat) and long error messages. They must usually be defined in headers.

## 6.4 Exceptions and classes {#oop-6-4}

- `try { … } catch (const std::exception& e) { … }`; throw by value, **catch by reference** (avoids slicing).
- **If a constructor throws,** the object never existed: its destructor does **not** run, but members and bases already constructed **are** destroyed. That is why owning resources through RAII members is safe.
- **Never throw from a destructor:** destructors are implicitly `noexcept`; throwing while another exception is unwinding the stack calls `std::terminate`.
- **Exception-safety guarantees:** **no-throw** (never fails), **strong** (if it fails, the state is unchanged, commit-or-rollback; copy-and-swap gives this), **basic** (no leaks, object still valid but possibly changed).
- Mark move constructors `noexcept`: `std::vector` only moves elements during growth if the move cannot throw (otherwise it copies).

<div class="nb nb-moral">

unique_ptr by default, shared_ptr for real shared ownership, weak_ptr to break cycles. Templates are compile-time polymorphism. A throwing constructor skips its own destructor; destructors must not throw.

</div>
