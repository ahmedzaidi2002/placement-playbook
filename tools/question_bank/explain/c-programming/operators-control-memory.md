@@ qc60-47
**Answer: (d) `*(*(a + 3) + 3)`**

**Why.** For a 2-D array, `a[i][j]` is defined as `*(*(a + i) + j)`. With i = j = 3 this is `*(*(a + 3) + 3)`.

**Concept: array indexing is pointer arithmetic.** `x[k]` means `*(x + k)`. In a 2-D array, `a + i` points to row i (a whole row), `*(a + i)` is that row, which decays to a pointer to its first element, `+ j` moves j elements along, and the outer `*` reads the value. Options (a)–(c) skip one dereference or add to the wrong level.

@@ mw-iiitd-17
**Answer: (b) 4** (on today's compilers)

**Why.** In C, a character constant like `'P'` has type `int`, so `sizeof('P')` is `sizeof(int)`, 4 on 32/64-bit compilers (2 on old 16-bit ones). In C++ it has type `char` and the answer is 1.

**Concept: character constants in C vs C++.** C treats `'A'` as an int with value 65. C++ changed it to `char` so overloads like `f(char)` work. Many "C trick" MCQs rely on this difference.

@@ mw-iisc-29
**Answer: 11 15 12** (with GCC; strictly undefined behaviour)

**Why.** `b = b + x++` uses x = 10, so b = 15, then x becomes 11. In `printf("%d %d %d", x++, b, x)`, `x++` and `x` are evaluated without a defined order. GCC (tested) computes `x++` first, which yields 11 and makes x 12, and reads the plain `x` afterwards as 12, printing 11 15 12.

**Concept: unsequenced side effects.** C does not fix the order in which function arguments are evaluated. Reading and modifying the same variable in two arguments of one call is undefined behaviour; the printed result depends on the compiler. In an exam, give the common GCC output but know it is not guaranteed.

@@ mw-iisc-30
**Answer: (b) 7 12** (GCC; strictly undefined behaviour)

**Why.** The usual evaluation: `i++` gives 5 (i becomes 6), `++i` makes i 7 and gives 7, so j = 5 + 7 = 12 and i = 7.

**Concept: modifying a variable twice in one expression is undefined.** Between two "sequence points" a variable may be modified at most once. `i++ + ++i` breaks that rule, so the C standard allows any result. Compilers usually give the answer above.

@@ mw-iitb-13
**Answer: (c) bitwise operators**

**Why.** `n & 1` keeps only the lowest bit: 1 for odd numbers, 0 for even.

**Concept: the lowest bit decides parity.** In binary, every place except the last is worth an even number (2, 4, 8, ...), so a number is odd exactly when its last bit is 1.

@@ mw-iitb-26
**Answer: -128 128** (where `char` is signed, as on x86)

**Why.** A signed 8-bit `char` holds −128..127. 128 does not fit and wraps to −128 (implementation-defined). Printed with `%d` it is −128. Cast to `unsigned char`, the same bits 1000 0000 read as 128. Where plain `char` is unsigned (e.g. ARM Linux), both print 128.

**Concept: two's complement and signedness.** The same 8 bits mean different numbers depending on the type: 1000 0000 is 128 unsigned and −128 signed. Whether plain `char` is signed is up to the platform.

@@ mw-iitb-28
**Answer: (d) depends on the compiler** (undefined behaviour)

**Why.** `x` is modified three times in one expression without a sequence point, so the C standard does not define the result.

**Concept: undefined behaviour.** When code breaks the sequencing rules, the compiler may produce any result (or optimise strangely). Write `x++` as a separate statement if you need a defined order.

@@ mw-nitd-17
**Answer: (c) 0 7 9 7 6** (GCC; strictly undefined)

**Why.** GCC evaluates printf's arguments right to left here: `i++` gives 6 (i = 7), `i--` gives 7 (i = 6), `i + 3` = 9, `++i` gives 7, `!i` = 0 (i is non-zero). Printed in the written order: 0 7 9 7 6.

**Concept: argument evaluation order is unspecified.** Modifying `i` in several arguments of one call is undefined. MCQs expecting a single answer assume right-to-left evaluation, the common GCC/x86 behaviour.

@@ mw-nitdl-12
**Answer: (b) n is a power of 2**

**Why.** Subtracting 1 flips the lowest set bit of n to 0 and all bits below it to 1. ANDing with n clears that lowest set bit. The result is 0 only if n had a single set bit, i.e. n is a power of 2 (or n = 0). Example: 8 = 1000, 7 = 0111, 8 & 7 = 0.

**Concept: `n & (n − 1)` removes the lowest set bit.** It is used to test powers of two and to count set bits (repeat until zero). Note: in C, `==` binds tighter than `&`, so the test must be written `(n & (n - 1)) == 0`.

@@ protium-mcq-comma
**Answer: (b) Atom Bomb**

**Why.** `i == 3, 4` is a comma expression: `i == 3` is evaluated and thrown away, and the whole condition has the value of the last part, 4, which is non-zero (true). So the `if` branch runs.

**Concept: the comma operator.** `(a, b)` evaluates a, then b, and its value is b. It has the lowest precedence of all operators. Compilers warn that the left side has no effect.

@@ protium-mcq-uchar
**Answer: (b) 1**

**Why.** The empty loop runs while `hi <= 0`. For an unsigned value that means `hi == 0`. After one increment hi is 1, the condition fails, and 1 is printed.

**Concept: unsigned comparisons.** An unsigned value is never negative, so `<= 0` is the same as `== 0`. Wrap-around (255 → 0) would only matter if the loop kept going up to 255.

@@ qc-n-logic
**Answer: (c) 1 1 2 -1**

**Why.**
- `~++a || b`: a becomes 2; ~2 = −3, non-zero, so the `||` is true (1) and `b` is not evaluated.
- `a || ~b-- && ~++b`: a is non-zero, so the whole right side, with its `b--` and `++b`, is skipped: 1.
- Then a = 2 and b is still −1.

**Concept: short-circuit evaluation.** `||` stops as soon as the left side is true; `&&` stops as soon as the left side is false. Side effects (`++`, `--`) in the skipped part never happen. Also `&&` binds tighter than `||`, so `a || (x && y)`.

@@ qc-n-xor
**Answer: (b) 4**

**Why.** `a ^ a` is 0 (any value XOR itself is 0). `0 && ...` is 0. Then `0 || a` is true because a = 4. So `printf` prints a, still 4.

**Concept: XOR identities and precedence.** x ^ x = 0, x ^ 0 = x. Precedence: `^` binds tighter than `&&`, which binds tighter than `||`, so the condition is `((a ^ a) && (a ^ a)) || a`.

@@ mw-iisc-27
**Answer: compilation error** (`else` without a previous `if`)

**Why.** Without braces, `if (i > 50)` controls only `i++;`. The next statement `i += 2;` ends the if. The `else` then has no `if` to attach to.

**Concept: braces define the body.** An `if` without braces controls exactly one statement; indentation means nothing to the compiler. Always use braces for multi-statement bodies.

@@ mw-rec-12
**Answer: (b) 50**

**Why.** i starts at 101. Each loop does `--i` in the test and `i--` in the body: i drops by 2 per iteration. The body runs for i = 100, 98, ..., 2 (50 times); then `--i` makes i 0 and the loop stops. The ASCII hint is a distractor (`\H` is an unknown escape that prints H).

**Concept: trace the loop variable.** Write down its value at the test each time. Pre-decrement in the condition changes i before the comparison; the body changes it again.

@@ nv-10
**Answer: (d) 2 1 0 -1**

**Why.** `x-- >= 0` compares the old value, then decrements. Tests: 3 ≥ 0 (x becomes 2, prints 2), 2 ≥ 0 (prints 1), 1 ≥ 0 (prints 0), 0 ≥ 0 (prints −1), −1 ≥ 0 fails.

**Concept: post-decrement in a condition.** `x--` yields the old value for the comparison; the body then sees the new value. So the body sees one less than what was tested.

@@ mw-iisc-9
**Answer: (c) only 1**

**Why.** (1) Allocators store a small header with each block's size; that is how `free(p)` knows how much to release. (2) The free list's structure depends on the allocator: the classic K&R allocator uses a singly linked circular list, so "doubly linked" is not true in general.

**Concept: how malloc works.** The heap is a pool of memory. `malloc` finds a free chunk big enough, records its size in a hidden header just before the returned pointer, and gives you the address after the header. `free` reads that header and puts the chunk back on a free list.

@@ mw-iitb-24
**Answer: (d) the memory it points to is freed**

**Why.** After `free(p)` (or after a local variable's function returns), p still holds the old address, but that memory no longer belongs to you: p is dangling. An uninitialised pointer is called a "wild" pointer.

**Concept: dangling pointers.** Using one is undefined behaviour (may crash or corrupt data). Set pointers to NULL after freeing and never return the address of a local variable.

@@ mw-nitd-19
**Answer: (a) and (c)**

**Why.** `calloc(n, size)` allocates n × size bytes and fills them with zeros; `malloc(bytes)` takes one size and leaves the contents uninitialised. Both return a single contiguous block, so (b) and (d) are false.

**Concept: malloc vs calloc.** Same kind of heap block; the differences are the argument form and zero-initialisation. Use calloc when you need zeroed memory (e.g. counters).

@@ mw25-malloc
**Answer: (b) `void*`**

**Why.** `malloc` doesn't know what you will store, so it returns a generic pointer. C converts `void*` to any object pointer automatically; C++ requires a cast.

**Concept: `void*`.** A pointer with no type information. You cannot dereference it directly; you assign it to a typed pointer first.

@@ nv-13
**Answer: (b) 2**

**Why.** `calloc(count, size)` takes the number of elements and the size of each, allocates count × size bytes and zeroes them. `malloc` takes one argument.

**Concept: same as above.** Remember the signatures: `malloc(size)`, `calloc(count, size)`, `realloc(ptr, new_size)`, `free(ptr)`.

@@ mw-iiitd-13
**Answer: (b) false** under C89 (implicit int); a strict C99 compiler requires `int main`.

**Why.** Old C (C89) assumed a missing return type was `int`, so `main()` alone compiled. C99 removed "implicit int"; modern compilers usually still accept it with a warning.

**Concept: implicit int.** In early C, any function declared without a return type returned int. Always write `int main(void)` today.

@@ mw-iiitd-16
**Answer: (d) it enters an infinite loop**

**Why.** `num` is static, so it keeps its value between calls, starting at 15 and dropping by 1 per call. Each iteration uses three calls: condition, body and increment. Init uses 15. Condition sees 14, body prints 13, increment uses 12; condition sees 11, ... The condition values are 14, 11, 8, 5, 2, −1, ... and never 0, so the loop never ends.

**Concept: static local variables.** A static local is created once and keeps its value across calls. Trace exactly which call (init, condition, body, update) gets which value.

@@ mw-iitb-15
**Answer: (b) 11**

**Why.** `value` adds the number of 1 bits of `*x` to a static `count` (which keeps accumulating) and zeroes `*x`. Set bits: 3 → 2, 5 → 2, 6 → 2, 4 → 1. After the last call count = 7. In the last iteration z = a[3] + value(&a[3]) = 4 + 7 = 11 (with a[3] read before the call zeroes it; C leaves that order unspecified, and reading it after would give 7).

**Concept: static accumulators and popcount.** `count += x & 1; x >>= 1;` counts set bits. A static local accumulates across calls instead of restarting at 0.

@@ mw25-static
**Answer: (b) static**

**Why.** Variables with static storage duration (static locals and globals) are zero-initialised before the program starts. `auto` and `register` locals contain garbage until assigned. `extern` only declares a variable defined elsewhere.

**Concept: storage classes.** auto: on the stack, uninitialised. register: a hint to keep it in a register, no address. static: one copy for the whole run, zero by default. extern: refers to a global defined in another file.

@@ qc-iisc-func
**Answer: (c) 8**

**Why.** x becomes 4 + 1 = 5. The test x ≥ 0 is true, so it returns 5 + 3 = 8.

**Concept: parameters are copies.** Changing x inside the function changes only its local copy. Trace the statements in order.

@@ qc25-register
**Answer: (a) compile-time error at Line 1**

**Why.** C forbids taking the address of a `register` variable: `&number` is an error ("address of register variable requested"), because a register has no memory address.

**Concept: the `register` keyword.** It asks the compiler to keep a variable in a CPU register. Since registers have no address, `&` is not allowed on it in C. (C++ ignored this rule and removed `register` in C++17.)

@@ qc60-24
**Answer: (c) 10**

**Why.** `m` is static, so all recursive calls share one copy. Each call does `++m` and recurses while m < 10. When m reaches 10 the recursion stops, and every pending call returns the shared m, now 10. So printf prints 10.

**Concept: static variables in recursion.** A normal local gets a fresh copy per call; a static local is shared by all calls. So every level returns the final value, not the value it saw when it started.

@@ ti-whatisit
**Answer: (c) 8, 8**

**Why.** For n ≥ 1 it returns x × WHATISIT(x, n − 1): 2 × 2 × 2 × 1 = 8. For n < 0 it multiplies by 1/x and moves n towards 0: (1/0.5)³ = 2³ = 8.

**Concept: recursive power.** xⁿ = x · xⁿ⁻¹ for n > 0, and xⁿ = (1/x) · xⁿ⁺¹ for n < 0, with x⁰ = 1. Note 0.5⁻³ = 2³.
