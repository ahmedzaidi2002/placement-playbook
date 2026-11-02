@@ qc-iisc-walk
**Answer: 5, 2, 4, 0, one number per line** (the final loop test reads past the array, which is undefined behaviour)

**Why.**
1. `while (t = *p++)` reads 5, 2, 4 (non-zero) with i = 1, 2, 3 ≤ 4, printing each. It then reads 0, the loop stops, and p is one past the 0 (at m[4]); i is 4.
2. The `do` body runs once with t = 0: i = 4 ≥ 4 is true, so it prints t = 0.
3. The test `t = *++p` reads m[5], beyond the array. GCC happened to read 0 and stop.

**Concept: assignment as a condition.** `while (t = *p++)` assigns, then tests the assigned value: it stops at the first 0. `*p++` reads the current element and then advances. A `do-while` always runs its body at least once.

@@ qc-n-deref
**Answer: (a) 4 4 4 4**

**Why.** `*p` is a (p = &a). `*(&a)` is a: "the thing at the address of a". `*(*(&p))`: `*(&p)` is p, and `*p` is a. Every expression is a, so no address is printed.

**Concept: `*` and `&` cancel.** `&x` gives the address of x; `*` follows an address. `*&x` is always x.

@@ qc-n-preinc
**Answer: (b) 6**

**Why.** `++*p` increments the value p points to (x goes from 5 to 6) and gives the new value.

**Concept: `++*p` vs `*p++`.** Both unary, right to left: `++*p` = `++(*p)` (increment the value); `*p++` = `*(p++)` (read, then move the pointer).

@@ qc-n-shiftptr
**Answer: (d) compile-time error**

**Why.** `p << 1` shifts a pointer, and C only allows shifts on integer types ("invalid operands to binary <<").

**Concept: allowed pointer arithmetic.** You may add or subtract an integer, subtract two pointers into the same array, and compare them. Multiplying, dividing or shifting a pointer is not allowed.

@@ qc-n-triple
**Answer: undefined behaviour** (if that option is offered); by the intended logic m would be 51, not among the visible options.

**Why.** `f` returns `&q`, the address of its own parameter, which is destroyed when `f` returns. `***p` then dereferences a dangling pointer (the GCC build crashed). Intended logic: `**q += **q` doubles m to 50, `m += 1` makes it 51.

**Concept: parameters are locals too.** A function's parameters live in its stack frame; returning their address is as wrong as returning any local's address.

@@ qc25-pointer
**Answer: (d) only (II)**

**Why.** A pointer stores the address of another variable (II true). Its type is a pointer type (`int*`, `char*`), not an integer type; converting to an integer needs a cast or `uintptr_t` (I false).

**Concept: pointers have types.** The type tells the compiler how many bytes to read at that address and how far `p + 1` moves.

@@ qc60-53
**Answer: (c) -45 4 1239 1235**

**Why.** 1234 = 0x04D2. On a little-endian machine byte 0 is 0xD2 (−46 as a signed char) and byte 1 is 0x04.
1. `++*ptr++`: byte 0 becomes −45 (s becomes 1235), print −45, ptr moves to byte 1.
2. `*ptr = 5`, then `--*ptr--`: byte 1 becomes 4, print 4, ptr moves back to byte 0. (s is now 0x04D3 = 1235.)
3. `*ptr++;` just moves ptr to byte 1.
4. `*ptr++ + s` = 4 + 1235 = 1239.
5. `s++` prints the old value 1235.

**Concept: endianness.** Little-endian stores the least significant byte first, at the lowest address. A `char*` into an int lets you edit single bytes; changing the low byte changes the int by the same amount (0xD2 → 0xD3 adds 1).

@@ ti-fnptr
**Answer: both work**

**Why.** (1) declares a function pointer and initialises it with `&fun`; (2) declares it, then assigns. Either way `(*fun_ptr)(10)` calls `fun(10)`.

**Concept: function pointer syntax.** `void (*fp)(int)` = "fp is a pointer to a function taking int and returning void". `&fun` and plain `fun` both give the function's address; `fp(10)` and `(*fp)(10)` both call it.

@@ ti-generic-search
**Answer: "The index is 2"**

**Why.** 7 is at position 2 (0-based) in {2, 5, 7, 90, 70}. The `compare(void*, void*)` callback lets the same search code work for any type: it casts the pointers to `int*` and compares the values.

**Concept: generic code with `void*`.** C has no templates, so library functions like `qsort` and `bsearch` take `void*` data plus a comparison callback that knows the real type.

@@ ti-pointers-array
**Answer: 10,20,30,40,50,**

**Why.** Each step writes through p to a different element: numbers[0] = 10, [1] = 20, [2] = 30, [3] = 40, [4] = 50.

**Concept: equivalent ways to reach an element.** `p++` then `*p`, `&numbers[2]`, `numbers + 3`, and `*(p + 4)` all address array elements; `numbers + k` and `&numbers[k]` are the same address.

@@ mw-iisc-31
**Answer: (a) 2**

**Why.** Macros are pasted as text. `ADD(3) / SUB(3)` becomes `3 + 3 / 3 - 3` = 3 + 1 − 3 = 1 (division first). So y = 1 and `ADD(y)` = y + y = 2. No division by zero happens.

**Concept: parenthesise macros.** `#define ADD(x) x + x` has no brackets, so surrounding operators split it. Safe form: `#define ADD(x) ((x) + (x))`.

@@ or-max-macro
**Answer: (a) 11 6 12** (GCC; strictly undefined behaviour)

**Why.** The macro expands to `((x++) > (y++) ? (x++) : (y++))`. 5 > 10 is false (x becomes 6, y 11), so the third part runs: it yields 11 and makes y 12. x ends at 6, y at 12.

**Concept: macro arguments can be evaluated twice.** A macro copies its argument text everywhere it appears, so `x++` may run more than once. Use inline functions instead of macros for anything with side effects.

@@ nv-14
**Answer: (c) l**

**Why.** x points to myint[3], which holds 3. `c[*x]` = c[3] = the 4th character of "hello world": 'l'.

**Concept: indexing with an expression.** `c[k]` = `*(c + k)`, where k can be any integer expression, including a value read through another pointer.

@@ qc-iisc-strings
**Answer: only the first line can be worked out: "ame" with GCC** (undefined behaviour; another compiler may print "name").

**Why.** `while (ptr2[i++] = ptr1[i]);` reads and modifies i in one expression without a sequence point. GCC evaluates the left side first, so ptr2[0] = ptr1[1], ptr2[1] = ptr1[2], ..., copying "ame". Also, `strcpy(ptr4, "ab\0cdefghij")` copies only "ab", because the literal effectively ends at the embedded `\0`.

**Concept: strings end at the first `\0`.** All `str*` functions stop at the first null byte, even if more characters follow in memory.

@@ ti-string-c
**Answer: (a) 111**

**Why.** ABC[4] is the letter 'o', whose ASCII code is 111. C allows `char ABC[5] = "hello";`: the five letters fill the array exactly and the terminating null is dropped. (C++ rejects this; printing ABC with `%s` would also be unsafe.)

**Concept: string arrays need room for `\0`.** "hello" needs 6 bytes including the terminator. Declaring exactly 5 is legal in C but leaves an unterminated string.

@@ mw-iiitd-20
**Answer: (c) 16 and 24**

**Why.** Each member must start at an address that is a multiple of its size (on a typical 64-bit system).
- Student: double (8) at 0, int (4) at 8, short (2) at 12 → 14 bytes, padded to a multiple of 8 → 16.
- Teacher: int (4) at 0, 4 bytes padding so the double starts at 8, double at 8–15, short at 16–17 → 18, padded to 24.

**Concept: struct padding and alignment.** The compiler inserts gaps so each member is aligned, and pads the end so the struct's size is a multiple of its largest alignment (so arrays of it stay aligned). Ordering members from largest to smallest minimises padding.

@@ nv-15
**Answer: (c) 23**

**Why.** A struct's first member starts at offset 0, so `&x.number` is the same address as `&x`. Casting it to `struct site*` and reading `ptr->number` reads x.number. The post-increment prints the old value, 23.

**Concept: first-member address = struct address.** C guarantees no padding before the first member, which is why this cast is valid.

@@ nv-21
**Answer: (a) compilation error**

**Why.** C does not allow default values inside a struct definition (`int number = 23;`). (C++11 allows it, but `ptr` is uninitialised, so `++ptr->number` would be undefined there.)

**Concept: struct definitions only describe layout.** In C, initialise members when you create a variable: `struct site x = {23};`.

@@ qc-n-enum
**Answer: (c) The best place is Shimoga**

**Why.** dir is set to Shimoga, the test `dir == Shimoga` is true, and s points to "Shimoga".

**Concept: enums are named integer constants.** `enum loc {Kerala = 1, ...}` just names the values 1–4. They live in a different role from the pointer variables p, q, r, s, so there is no clash.

@@ ti-ptr-array-size
**Answer: (d) 80**

**Why.** `*vector[10]` is an array of 10 pointers (to the struct). On a 64-bit system each pointer is 8 bytes: 10 × 8 = 80. The struct's own size does not matter.

**Concept: read declarations from the name outward.** `vector[10]` (array of 10), then `*` (pointers), then the struct type. `sizeof` an array = elements × element size.

@@ ti-vector
**Answer: (a) 120**

**Why.** On a 32-bit system: float 4 + float 4 + pointer 4 = 12 bytes per VECTOR (no padding needed). 10 of them: 120. (The candidates' 160 and 200 are wrong.)

**Concept: struct size = members + padding.** Here all members are 4 bytes, so no padding is added.

@@ qc60-40
**Answer: (b) Line 5**

**Why.** `scanf` needs the address of the variable to write into: `scanf("%d", &num);`. Passing `num` gives scanf a garbage value to use as an address (undefined behaviour, often a crash).

**Concept: why scanf needs `&`.** C passes arguments by value; to let a function change your variable, pass its address. (Arrays like `char s[20]` already decay to an address, so `scanf("%s", s)` has no `&`.)
