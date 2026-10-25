---
title: "8 · Computer arithmetic"
linkTitle: "8 Computer arithmetic"
weight: 8
math: true
---
Addition was built in [Chapter 3](../03-combinational/). This chapter covers the algorithms behind multiplication and division, each traced by a program bit by bit in the layout used in exams, and the steps of floating-point addition and multiplication.

## 8.1 Multiplication {#sec-coa-mult}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> $13 \times (-6)$ in five bits by Booth’s algorithm: five shifts, three add/subtract steps, product $-78$.</em>

</div>

### 8.1.i Shift-and-add, and why signed numbers need more {#s8-1-i}

Unsigned multiplication is long multiplication in base $2$: for each multiplier bit that is $1$, add the shifted multiplicand. A sequential multiplier keeps the running sum in a register $A$ and the multiplier in $Q$, and in each of $n$ steps adds $M$ to $A$ if $q_0 = 1$, then shifts $A{:}Q$ right. Two’s-complement operands break this, because the top bit of the multiplier has weight $-2^{n-1}$, not $+2^{n-1}$.

### 8.1.ii Booth’s algorithm {#s8-1-ii}

<div class="nb nb-definition" id="definition-8-1-1">

<strong>Definition 8.1.1</strong>. <strong>Booth recoding</strong> replaces each multiplier bit $q_i$ by the digit $d_i = q_{i-1} - q_i \in \{-1, 0, +1\}$ (with $q_{-1} = 0$). Since $\sum_i (q_{i-1} - q_i)\,2^i = -q_{n-1}2^{n-1} + \sum_{i<n-1} q_i 2^i$, the recoded digits represent exactly the two’s-complement value of the multiplier. A run of $1$s $0111\,10$ becomes $+1$ at its left end and $-1$ at its right end.

</div>

<div class="nb nb-remark" id="algorithm-8-1-2">

<strong>Algorithm 8.1.2</strong> (Booth’s algorithm) — $A \leftarrow 0$, $Q \leftarrow$ multiplier, $Q_{-1} \leftarrow 0$, $M \leftarrow$ multiplicand. Repeat $n$ times: look at $(Q_0, Q_{-1})$: $10$: $A \leftarrow A - M$; $01$: $A \leftarrow A + M$; $00$ or $11$: nothing. Then shift $A{:}Q{:}Q_{-1}$ right <em>arithmetically</em> (the sign of $A$ is copied). The product is $A{:}Q$.

</div>

```python {filename="booth.py, lines 5–25",linenos=table,linenostart=5}
def booth(m, q, n):
    """Multiply n-bit two's-complement m (multiplicand) by q (multiplier)."""
    A, Q, q_1, M = 0, q & ((1 << n) - 1), 0, m & ((1 << n) - 1)
    print(f"M = {m} = {bits(m, n)}, Q = {q} = {bits(q, n)}, -M = {bits(-m, n)}")
    print(" step  A      Q      Q-1  action")
    print(f"   0   {bits(A, n)}  {bits(Q, n)}  {q_1}    initial")
    for step in range(1, n + 1):
        pair = (Q & 1, q_1)
        act = {(1, 0): "A = A - M", (0, 1): "A = A + M"}.get(pair, "no add")
        if pair == (1, 0): A = (A - M) & ((1 << n) - 1)
        if pair == (0, 1): A = (A + M) & ((1 << n) - 1)
        # arithmetic shift right of A, Q, Q-1 as one 2n+1-bit register
        q_1 = Q & 1
        Q = (Q >> 1) | ((A & 1) << (n - 1))
        A = (A >> 1) | (A & (1 << (n - 1)))           # keep the sign bit
        print(f"   {step}   {bits(A, n)}  {bits(Q, n)}  {q_1}    {act}, shift")
    prod = (A << n) | Q
    if prod & (1 << (2 * n - 1)): prod -= 1 << (2 * n)
    print(f"product A:Q = {bits(A, n)} {bits(Q, n)} = {prod}  (check {m * q})")
    assert prod == m * q
```

```text {filename="Output of booth.py (Python 3.11)"}
M = 13 = 01101, Q = -6 = 11010, -M = 10011
 step  A      Q      Q-1  action
   0   00000  11010  0    initial
   1   00000  01101  0    no add, shift
   2   11001  10110  1    A = A - M, shift
   3   00011  01011  0    A = A + M, shift
   4   11011  00101  1    A = A - M, shift
   5   11101  10010  1    no add, shift
product A:Q = 11101 10010 = -78  (check -78)
multiplier 111010: Booth digits 00-+-0 (+ = +1, - = -1), 3 add/subtract
   bit-pair digits [0, -1, -2]: 3 partial products instead of 6
multiplier 0101010101: Booth digits +-+-+-+-+- (+ = +1, - = -1), 10 add/subtract
   bit-pair digits [1, 1, 1, 1, 1]: 5 partial products instead of 10
multiplier 0000111100: Booth digits 000+000-00 (+ = +1, - = -1), 2 add/subtract
   bit-pair digits [0, 1, 0, -1, 0]: 5 partial products instead of 10
```

<div class="nb nb-remark" id="remark-8-1-3">

<strong>Remark 8.1.3</strong> (Facts OAs build on Booth) — The number of additions and subtractions equals the number of non-zero recoded digits: a multiplier with long runs of $1$s (`0000111100`: $2$ operations) is cheap, while alternating bits (`0101010101`: $10$ operations) are the worst case, worse than plain shift-and-add. Booth handles negative multipliers and multiplicands with no correction step. The shift must be arithmetic; a logical shift is the classic error.

</div>

<div class="nb nb-definition" id="definition-8-1-4">

<strong>Definition 8.1.4</strong> (Bit-pair recoding (radix-4 Booth)). Group the multiplier in overlapping triples $(q_{2i+1}, q_{2i}, q_{2i-1})$ and use the digit $q_{2i} + q_{2i-1} - 2q_{2i+1} \in \{-2,-1,0,1,2\}$ at weight $4^i$. Each digit selects $0, \pm M$ or $\pm 2M$ (a shift), so an $n$-bit multiplication needs only $n/2$ partial products, whatever the bit pattern; the output shows $10$ bits recoded into $5$ digits.

</div>

### 8.1.iii Fast multipliers: carry-save and Wallace trees {#s8-1-iii}

A combinational <strong>array multiplier</strong> forms all $n$ partial products with AND gates (or Booth digits) and adds them with rows of full adders. Adding rows one after another with carry propagation is slow; a <strong>carry-save adder</strong> (CSA) instead takes three numbers and returns two (a bitwise sum and a shifted carry vector) in one full-adder delay, with no carry propagation. A <strong>Wallace tree</strong> applies CSAs in parallel until two rows remain, then one fast carry-propagate adder finishes:

```text {filename="Output of csa.py (Python 3.11)"}
 4 partial products: 2 CSA levels (vs 3 sequential adds)
 8 partial products: 4 CSA levels (vs 7 sequential adds)
16 partial products: 6 CSA levels (vs 15 sequential adds)
24 partial products: 7 CSA levels (vs 23 sequential adds)
32 partial products: 8 CSA levels (vs 31 sequential adds)
64 partial products: 10 CSA levels (vs 63 sequential adds)
9 random 16-bit numbers reduced to 2 by carry-save adders; final add correct
```

The depth grows like $\log_{3/2} k$: $64$ partial products need $10$ CSA levels instead of $63$ sequential additions.

<div class="nb nb-moral">

Booth makes signed multiplication uniform; bit-pair recoding halves the number of partial products; carry-save trees add them in logarithmic depth.

</div>

## 8.2 Division {#sec-coa-div}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> $11 \div 3$ in four bits: quotient $3$, remainder $2$, by restoring and by non-restoring division.</em>

</div>

<div class="nb nb-remark" id="algorithm-8-2-1">

<strong>Algorithm 8.2.1</strong> (Restoring division, unsigned) — $A \leftarrow 0$ ($n+1$ bits), $Q \leftarrow$ dividend, $M \leftarrow$ divisor. Repeat $n$ times: shift $A{:}Q$ left; $A \leftarrow A - M$; if $A < 0$, set $q_0 = 0$ and <em>restore</em> $A \leftarrow A + M$; else set $q_0 = 1$. At the end $Q$ is the quotient and $A$ the remainder.

</div>

<div class="nb nb-remark" id="algorithm-8-2-2">

<strong>Algorithm 8.2.2</strong> (Non-restoring division) — Skip the restore: if $A$ was negative, the next step shifts and <em>adds</em> $M$ instead of subtracting ($2(A+M) - M = 2A + M$). Set $q_0 = 1$ when the new $A \ge 0$. After the last step, if $A < 0$, add $M$ once to get the remainder. One add or subtract per step instead of up to two.

</div>

```text {filename="Output of divide.py (Python 3.11)"}
restoring: 11 / 3, n = 4
  1: A = 00001  Q = 0110   A<0: restore, q0 = 0
  2: A = 00010  Q = 1100   A<0: restore, q0 = 0
  3: A = 00010  Q = 1001   A>=0: q0 = 1
  4: A = 00010  Q = 0011   A>=0: q0 = 1
  quotient 3, remainder 2
non-restoring: 11 / 3, n = 4
  1: sub M -> A = 11110  Q = 0110
  2: add M -> A = 11111  Q = 1100
  3: add M -> A = 00010  Q = 1001
  4: sub M -> A = 00010  Q = 0011
  quotient 3, remainder 2
```

<div class="nb nb-remark" id="remark-8-2-3">

<strong>Remark 8.2.3</strong> — Both give the same quotient and remainder (the script checks them against Python’s `divmod`). Restoring division may need two operations per step (subtract, then add back); non-restoring needs exactly one, plus at most one final correction. Division is inherently sequential (each quotient bit depends on the previous remainder), which is why hardware dividers take tens of cycles and compilers replace division by a constant with a multiplication by its reciprocal.

</div>

## 8.3 Floating-point addition and multiplication {#sec-coa-fpops}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> $9.75 + 0.5625$: align the smaller operand by shifting it right four places, add, normalise, round.</em>

</div>

<div class="nb nb-remark" id="algorithm-8-3-1">

<strong>Algorithm 8.3.1</strong> (Floating-point addition) — (1) Compare exponents; shift the significand of the smaller operand right by the difference (keeping three extra bits: guard, round and sticky, the sticky bit being the OR of everything shifted past it). (2) Add or subtract the significands according to the signs. (3) Normalise: shift right once if the sum overflowed to $[2,4)$, or shift left past leading zeros after a cancellation, adjusting the exponent. (4) Round to nearest even using the extra bits; renormalise if rounding overflowed. (5) Check for exponent overflow ($\pm \infty$) and underflow (subnormal or $0$).

</div>

<div class="nb nb-remark" id="algorithm-8-3-2">

<strong>Algorithm 8.3.2</strong> (Floating-point multiplication) — (1) Sign $= s_1 \oplus s_2$. (2) Add the biased exponents and subtract the bias once ($E = E_1 + E_2 - 127$). (3) Multiply the significands (a $24 \times 24$-bit integer product). (4) Normalise (the product of two numbers in $[1,2)$ lies in $[1,4)$: at most one right shift), round, and check the exponent range.

</div>

```text {filename="Output of fpops.py (Python 3.11)"}
9.75 + 0.5625: exponents 3 and -1; shift smaller right 4
  add significands: 1.00111 + 0.0001001 = 1.0100101
  normalise and round: 1.0100101 x 2^3 = 10.3125   (machine: 10.3125)
1.5 + -1.375: exponents 0 and 0; shift smaller right 0
  subtract significands: 1.1 - 1.011 = 0.001
  normalise and round: 1.0 x 2^-3 = 0.125   (machine: 0.125)
6.0 x -0.625: sign 0 xor 1 = 1; biased exponent 129 + 126 - 127 = 128 (true 1)
  significands 1.1 x 1.01 = 1.111
  normalise and round: 1.111 x 2^1 = -3.75   (machine: -3.75)
1.5 x 1.5: sign 0 xor 0 = 0; biased exponent 127 + 127 - 127 = 127 (true 0)
  significands 1.1 x 1.1 = 2.01
  normalise and round: 1.001 x 2^1 = 2.25   (machine: 2.25)
```

<div class="nb nb-example nb-block" id="example-8-3-3">

<strong>Example 8.3.3</strong> (Reading the output)

$9.75 = 1.00111_2 \times 2^3$ and $0.5625 = 1.001_2 \times 2^{-1}$: shifting the second right by $3 - (-1) = 4$ gives $0.0001001_2$, the sum $1.0100101_2 \times 2^3 = 10.3125$ needs no normalisation. $1.5 - 1.375$ cancels to $0.001_2$ and needs a left shift by $3$: <strong>cancellation</strong> loses significant bits and is the source of most floating-point accuracy problems. In $6.0 \times (-0.625)$ the biased exponents $129 + 126 - 127 = 128$ give the true exponent $1$, and $1.1_2 \times 1.01_2 = 1.111_2$. In $1.5 \times 1.5$ the significand product $10.01_2$ needs one right shift. Every result agrees with the hardware.

</div>

<div class="nb nb-moral">

Floating-point addition is the hard one (alignment, cancellation, normalisation); multiplication is an integer multiply plus an exponent add, with at most one normalisation shift.

</div>
