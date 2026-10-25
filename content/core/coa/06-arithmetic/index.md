---
title: "6 · Computer arithmetic"
linkTitle: "6 Arithmetic"
weight: 6
math: true
---
## 6.1 Multiplication {#coa-6-1}

**Shift-and-add** (unsigned): for each multiplier bit that is 1, add the shifted multiplicand. $n$-bit × $n$-bit gives a $2n$-bit product.

**Booth's algorithm** (signed, 2's complement): look at each multiplier bit together with the bit to its right ($Q_0$, $Q_{-1}$, starting with $Q_{-1} = 0$):

| $Q_0 Q_{-1}$ | Action at this bit position |
|---|---|
| 0 0 or 1 1 | nothing (inside a run) |
| 1 0 | **subtract** the multiplicand (start of a run of 1s) |
| 0 1 | **add** the multiplicand (end of a run of 1s) |

then arithmetic-shift right. A run of 1s from bit $i$ to bit $j$ equals $2^{j+1} - 2^i$, so one subtract and one add replace many adds.

<div class="nb nb-example">

<strong>Example</strong> (Booth recoding)

Multiplier $7 = 0111$. Pairs from the right: bit 0 with $Q_{-1} = 0$: **10** → $-M$ at $2^0$; bits 1 and 2: **11** → nothing; bit 3 with bit 2: **01** → $+M$ at $2^3$. So $7M = 8M - M$: one subtraction and one addition instead of three additions.

</div>

**Fast multipliers:** carry-save adders add three numbers to two without carry propagation; a **Wallace tree** reduces all partial products in $O(\log n)$ levels.

## 6.2 Division {#coa-6-2}

**Restoring division:** shift the remainder left, subtract the divisor; if the result is negative, restore (add the divisor back) and set the quotient bit to 0, else set it to 1. **Non-restoring division** skips the restore step: if negative, add instead of subtract in the next step. Division is slower than multiplication (one bit per step, cannot be parallelised as easily).

## 6.3 Floating-point arithmetic {#coa-6-3}

**Addition:**

1. **Align** exponents: shift the smaller number's mantissa right by the exponent difference.
2. **Add** the mantissas.
3. **Normalise** (shift so the result is $1.xxx$) and adjust the exponent.
4. **Round** to the available bits (guard, round and sticky bits help round correctly).

<div class="nb nb-example">

<strong>Example</strong> (FP add)

$9.75 + 0.5625$: $9.75 = 1.00111_2 \times 2^3$, $0.5625 = 1.001_2 \times 2^{-1}$. Shift the second right by $3 - (-1) = 4$: $0.0001001_2 \times 2^3$. Sum $= 1.0100101_2 \times 2^3 = 10.3125$ ✓.

</div>

**Multiplication:** add the exponents (subtract one bias), multiply the mantissas, XOR the signs, normalise, round.

<div class="nb nb-moral">

Booth: 10 → subtract, 01 → add, 00/11 → shift only. Float add = align, add, normalise, round; float multiply = add exponents (minus bias), multiply mantissas.

</div>
