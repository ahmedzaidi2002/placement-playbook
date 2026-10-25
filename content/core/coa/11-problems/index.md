---
title: "11 · Practice problems"
linkTitle: "11 Practice"
weight: 11
math: true
---
Fifteen OA-style numericals on new examples. Try, then open the solution.

<div class="nb nb-problem nb-block" id="problem-coa-1">

<strong>Problem 1</strong> (2's complement)

(a) Range of 6-bit 2's complement? (b) −20 in 8 bits? (c) Does $0110\,0100 + 0011\,0010$ overflow as signed 8-bit?

<details class="nb-sol">
<summary>Solution</summary>

(a) −32 to 31. (b) $20 = 0001\,0100$ → flip → $1110\,1011$ → +1 → **$1110\,1100$**. (c) $100 + 50 = 150 > 127$: the result $1001\,0110$ reads as −106 → **overflow**.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-coa-2">

<strong>Problem 2</strong> (IEEE-754)

Encode 0.75 in single precision (hex).

<details class="nb-sol">
<summary>Solution</summary>

$0.75 = 0.11_2 = 1.1_2 \times 2^{-1}$: $S = 0$, $E = 126 = 0111\,1110$, $F = 100\dots0$. Bits `0 01111110 10000…` = **0x3F400000**.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-coa-3">

<strong>Problem 3</strong> (Gray code)

Convert binary 1101 to Gray code.

<details class="nb-sol">
<summary>Solution</summary>

Keep the first bit, then XOR neighbours: 1, $1 \oplus 1 = 0$, $1 \oplus 0 = 1$, $0 \oplus 1 = 1$ → **1011**.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-coa-4">

<strong>Problem 4</strong> (K-map)

Minimise $F(A, B, C) = \sum m(1, 3, 5, 6, 7)$.

<details class="nb-sol">
<summary>Solution</summary>

Minterms 1, 3, 5, 7 all have $C = 1$ → $C$. Minterms 6, 7 have $A = B = 1$ → $AB$. **$F = C + AB$**.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-coa-5">

<strong>Problem 5</strong> (Counters)

(a) Flip-flops for a mod-12 counter? (b) States of a Johnson counter with 5 flip-flops? (c) Output frequency of three T flip-flops (T = 1) in a chain fed by 8 MHz?

<details class="nb-sol">
<summary>Solution</summary>

(a) $\lceil \log_2 12 \rceil = 4$. (b) $2 \times 5 = 10$. (c) $8/2^3 = 1$ MHz.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-coa-6">

<strong>Problem 6</strong> (Expanding opcode)

16-bit instructions, 6-bit address fields. 12 two-address instructions exist. Maximum one-address instructions?

<details class="nb-sol">
<summary>Solution</summary>

Two-address opcode = $16 - 12 = 4$ bits → 16 patterns; 4 unused, each followed by 6 more bits: $4 \times 2^6 = $ **256**.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-coa-7">

<strong>Problem 7</strong> (Addressing modes)

A one-word instruction at address 300 has address field 400; R1 = 200; Mem[400] = 700. Effective address in direct, indirect, PC-relative and indexed (R1) modes?

<details class="nb-sol">
<summary>Solution</summary>

Direct **400**; indirect Mem[400] = **700**; PC-relative: PC after fetch = 301, so **701**; indexed $400 + 200 = $ **600**.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-coa-8">

<strong>Problem 8</strong> (Pipeline speed-up)

Stages 40, 30, 50, 40 ns; latch 5 ns. Time for 1000 instructions pipelined and not, and the speed-up?

<details class="nb-sol">
<summary>Solution</summary>

Clock 55 ns. Pipelined $(4 + 999) \times 55 = 55{,}165$ ns. Non-pipelined $160 \times 1000 = 160{,}000$ ns. Speed-up ≈ **2.9** (limit $160/55 = 2.91$).

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-coa-9">

<strong>Problem 9</strong> (CPI with stalls)

Loads are 30% of instructions and half of them cause a 1-cycle stall; branches are 20% and half are mispredicted with a 3-cycle penalty. CPI?

<details class="nb-sol">
<summary>Solution</summary>

$1 + 0.3 \times 0.5 \times 1 + 0.2 \times 0.5 \times 3 = 1 + 0.15 + 0.3 = $ **1.45**.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-coa-10">

<strong>Problem 10</strong> (Cache address split)

16-bit addresses, 1 KB cache, 16-byte blocks, 2-way set-associative. Tag, index and offset bits?

<details class="nb-sol">
<summary>Solution</summary>

64 lines, 32 sets. Offset **4**, index **5**, tag $16 - 9 = $ **7**.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-coa-11">

<strong>Problem 11</strong> (AMAT)

Hit time 2 ns, miss rate 8%, miss penalty 60 ns. AMAT?

<details class="nb-sol">
<summary>Solution</summary>

$2 + 0.08 \times 60 = $ **6.8 ns**.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-coa-12">

<strong>Problem 12</strong> (Memory chips)

Build $32\text{K} \times 8$ from $4\text{K} \times 4$ chips. Chips, address lines, decoder?

<details class="nb-sol">
<summary>Solution</summary>

$(32/4) \times (8/4) = $ **16 chips** (8 rows of 2). 15 address lines: 12 to every chip, 3 to a **3:8 decoder**.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-coa-13">

<strong>Problem 13</strong> (Amdahl)

60% of a program is sped up 3×. Overall speed-up? The maximum possible by speeding that part up?

<details class="nb-sol">
<summary>Solution</summary>

$1/(0.4 + 0.6/3) = 1/0.6 = $ **1.67×**. Maximum $1/0.4 = $ **2.5×**.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-coa-14">

<strong>Problem 14</strong> (Iron law)

$2 \times 10^9$ instructions, CPI 1.5, clock 3 GHz. Execution time?

<details class="nb-sol">
<summary>Solution</summary>

$2 \times 10^9 \times 1.5 / 3 \times 10^9 = $ **1 s**.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-coa-15">

<strong>Problem 15</strong> (Booth)

Recode the multiplier $0110$ (6) with Booth's rule.

<details class="nb-sol">
<summary>Solution</summary>

Bit 0 with $Q_{-1} = 0$: 00 → nothing. Bits 1,0 = 10 → $-M$ at $2^1$. Bits 2,1 = 11 → nothing. Bits 3,2 = 01 → $+M$ at $2^3$. So $6M = 8M - 2M$.

</details>

</div>
