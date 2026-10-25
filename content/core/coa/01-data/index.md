---
title: "1 · Data representation"
linkTitle: "1 Data representation"
weight: 1
math: true
---
## 1.1 Number bases {#coa-1-1}

A number in base $b$: $d_{n-1}\dots d_1 d_0 = \sum d_i \, b^i$.

- **Binary → hex:** group 4 bits from the right. **Binary → octal:** group 3 bits.
- **Decimal → binary:** divide by 2 repeatedly and read the remainders bottom-up. Fractions: multiply by 2 repeatedly and read the integer parts top-down.

<div class="nb nb-example">

<strong>Example</strong> (Conversions)

$(1011\,0110)_2$ → hex groups `1011` `0110` = **0xB6**; decimal $128 + 32 + 16 + 4 + 2 = $ **182**; octal groups `10` `110` `110` = **266**. $(0.625)_{10}$: $0.625 \times 2 = 1.25$ (1), $0.25 \times 2 = 0.5$ (0), $0.5 \times 2 = 1.0$ (1) → $(0.101)_2$.

</div>

## 1.2 Signed integers {#coa-1-2}

For $n$ bits:

| Encoding | Negative of $x$ | Range | Zeros |
|---|---|---|---|
| Sign-magnitude | flip the sign bit | $-(2^{n-1}-1)$ to $2^{n-1}-1$ | two (+0, −0) |
| 1's complement | flip all bits | $-(2^{n-1}-1)$ to $2^{n-1}-1$ | two |
| **2's complement** | flip all bits, add 1 | $-2^{n-1}$ to $2^{n-1}-1$ | one |

8 bits: unsigned 0–255; 2's complement **−128 to 127**. Computers use 2's complement because addition and subtraction use the same adder and there is one zero.

<div class="nb nb-example">

<strong>Example</strong> (2's complement)

$+5 = 0000\,0101$ → flip → $1111\,1010$ → +1 → $1111\,1011 = -5$. Reading $1111\,1011$: the top bit has weight $-128$: $-128 + 64 + 32 + 16 + 8 + 2 + 1 = -5$.

</div>

**Overflow:** unsigned addition overflows when there is a **carry out** of the top bit. 2's-complement addition overflows when **two numbers of the same sign give a result of the other sign** (equivalently, the carry into the top bit ≠ the carry out). Adding numbers of opposite signs never overflows.

<div class="nb nb-example">

<strong>Example</strong> (Overflow)

$0111\,1111 + 0000\,0001 = 1000\,0000$: as unsigned, $127 + 1 = 128$ (fine, no carry out); as signed, $127 + 1$ gives $-128$: **overflow** (two positives gave a negative).

</div>

**Sign extension:** to widen a 2's-complement number, copy the sign bit into the new bits ($1011$ → $1111\,1011$, still −5).

## 1.3 IEEE-754 floating point {#coa-1-3}

$$\text{value} = (-1)^S \times 1.F \times 2^{E - \text{bias}}$$

| Format | Sign | Exponent | Fraction | Bias |
|---|---|---|---|---|
| Single (32-bit) | 1 | 8 | 23 | **127** |
| Double (64-bit) | 1 | 11 | 52 | **1023** |

<div class="nb nb-example">

<strong>Example</strong> (Encode −6.75)

$6.75 = 110.11_2 = 1.1011_2 \times 2^2$. $S = 1$, $E = 2 + 127 = 129 = 1000\,0001$, $F = 1011\,000\dots0$.
Bits: `1 10000001 10110000000000000000000` = **0xC0D80000**.

Decode 0x41200000: `0 10000010 0100…` → $E = 130 - 127 = 3$, value $= 1.01_2 \times 2^3 = 1.25 \times 8 = $ **10.0**.

</div>

**Special values:** exponent all 0s with fraction 0 = **±0**; exponent all 0s with fraction ≠ 0 = **denormal** (no hidden 1, gradual underflow); exponent all 1s with fraction 0 = **±∞**; exponent all 1s with fraction ≠ 0 = **NaN**.

<div class="nb nb-remark">

<strong>Traps</strong> — `0.1 + 0.2 != 0.3` (0.1 has no exact binary form; compare floats with a tolerance). Floating-point addition is **not associative**. A float has about 7 significant decimal digits, a double about 16.

</div>

## 1.4 Codes: BCD, excess-3, Gray {#coa-1-4}

- **BCD:** each decimal digit in 4 bits: 47 = `0100 0111`. In BCD addition, if a digit sum exceeds 9 (or carries), **add 6** (`0110`). Example: $8 + 5 = 1101$ → $+0110$ → `1 0011` = 13 ✓.
- **Excess-3:** BCD + 3 (self-complementing).
- **Gray code:** consecutive values differ in **one bit** (used in K-maps and rotary encoders). Binary → Gray: keep the top bit, then $g_i = b_{i+1} \oplus b_i$. Example: $1011$ → **1110**.

## 1.5 Endianness and alignment {#coa-1-5}

- **Big-endian:** most significant byte at the lowest address (network byte order). **Little-endian:** least significant byte first (x86, most ARM). The 32-bit value 0x12345678 at address 100: big-endian stores `12 34 56 78`, little-endian `78 56 34 12`.
- **Alignment:** a 4-byte `int` usually sits at an address that is a multiple of 4, so compilers insert **padding** in structs. `struct { char c; int i; char d; }` takes **12** bytes (1 + 3 pad + 4 + 1 + 3 pad); reordering to `int, char, char` takes **8**.

## 1.6 Bit tricks interviewers ask {#coa-1-6}

| Task | Expression |
|---|---|
| Is $x$ a power of 2? | `x > 0 && (x & (x - 1)) == 0` |
| Clear the lowest set bit | `x & (x - 1)` |
| Isolate the lowest set bit | `x & -x` |
| Set / clear / toggle / test bit $k$ | `x \| (1<<k)`, `x & ~(1<<k)`, `x ^ (1<<k)`, `(x >> k) & 1` |
| Swap without a temp | `a ^= b; b ^= a; a ^= b;` |
| Count set bits | repeat `x &= x - 1` and count |

<div class="nb nb-moral">

2's complement: flip and add 1; $n$ bits hold $-2^{n-1}$ to $2^{n-1} - 1$; overflow when same-sign inputs give the other sign. IEEE single: 1 + 8 + 23 bits, bias 127, value $(-1)^S \times 1.F \times 2^{E-127}$.

</div>
