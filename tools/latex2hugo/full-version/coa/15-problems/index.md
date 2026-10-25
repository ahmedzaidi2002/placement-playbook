---
title: "15 · A few harder problems to think about"
linkTitle: "15 A few harder problems to think about"
weight: 15
math: true
---
These problems follow the patterns of real online assessments (Texas Instruments, Qualcomm, NVIDIA and others) without copying them: conversions, “which statements are true” (more than one may be), circuit behaviour, HDL reading and numericals. Hints are in the <em>Hint</em> drop-down under each problem, solutions in the <em>Solution</em> drop-down under each problem. Every number in the solutions was computed by `problems.py` or by the small programs named in the solutions; the script’s full output is printed at the end of this chapter, with each line tagged by its problem number. Chilis mark the harder ones.

## 15.1 Number representation {#s15-1}

<div class="nb nb-problem nb-block" id="problem-15-1">

<strong>Problem 15.1</strong> (Conversions against the clock)

Convert: (a) $(1101\,0110\,1011)_2$ to hexadecimal; (b) $(7\mathrm{A3C})_{16}$ to decimal; (c) $(9876)_{10}$ to hexadecimal; (d) $(645)_8$ to decimal; (e) $(5\mathrm{B9})_{16}$ to binary.

<details class="nb-hint">
<summary>Hint</summary>

Group bits by four for hex; use Horner’s rule for base-to-decimal and repeated division by $16$ for decimal-to-hex.

</details>

<details class="nb-sol">
<summary>Solution</summary>

(a) `1101 0110 1011` $=$ `D6B`. (b) $((7 \cdot 16 + 10)\cdot 16 + 3)\cdot 16 + 12 = 31292$. (c) $9876 = 38 \cdot 256 + 148$; $38 = \mathrm{26}_{16}$, $148 = \mathrm{94}_{16}$, so `2694`. (d) $6 \cdot 64 + 4 \cdot 8 + 5 = 421$. (e) `0101 1011 1001`, that is `10110111001`.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-15-2">

<strong>Problem 15.2</strong> (Bitwise operators on decimals)

What are $45 \mathbin{\&} 45$, $45 \oplus 45$, $45 \mathbin{\&} 54$ and $45 \mid 54$ (decimal results)?

<details class="nb-hint">
<summary>Hint</summary>

The first two need no conversion at all.

</details>

<details class="nb-sol">
<summary>Solution</summary>

$45 \mathbin{\&} 45 = 45$ (idempotence) and $45 \oplus 45 = 0$. With $45 = \texttt{101101}$ and $54 = \texttt{110110}$: AND $= \texttt{100100} = 36$, OR $= \texttt{111111} = 63$.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-15-3">

<strong>Problem 15.3</strong> (Three encodings of $-23$)

Write $-23$ in 8 bits in sign-magnitude, 1’s complement and 2’s complement. Which of the three has two representations of zero, and what is the range of the 8-bit 2’s-complement format?

<details class="nb-hint">
<summary>Hint</summary>

$23 = \texttt{00010111}$.

</details>

<details class="nb-sol">
<summary>Solution</summary>

Sign-magnitude `10010111`; 1’s complement `11101000`; 2’s complement `11101001`. Sign-magnitude and 1’s complement both have $+0$ and $-0$; 2’s complement has one zero and the range $-128 \dots 127$.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-15-4">

<strong>Problem 15.4</strong> (Which additions overflow?)

In 8-bit 2’s complement, which of these overflow? (i) $90 + 40$; (ii) $(-90) + (-40)$; (iii) $(-90) + 40$; (iv) $127 + 1$; (v) $(-128) + (-1)$; (vi) $64 + 63$.

<details class="nb-hint">
<summary>Hint</summary>

Overflow needs operands of the same sign and a result of the other sign.

</details>

<details class="nb-sol">
<summary>Solution</summary>

(i), (ii), (iv) and (v) overflow (results $-126$, $126$, $-128$, $127$); (iii) has operands of opposite signs and cannot overflow ($-50$); (vi) gives $127$, the largest value, without overflow.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-15-5">

<strong>Problem 15.5</strong> 🌶 (IEEE-754 both ways)

(a) Encode $-13.625$ as a single-precision float in hexadecimal. (b) Decode `0x41C80000`. (c) What is `0x80000000`?

<details class="nb-hint">
<summary>Hint</summary>

$13.625 = 1101.101_2$. For (b), the exponent field is the 8 bits after the sign.

</details>

<details class="nb-sol">
<summary>Solution</summary>

(a) $13.625 = 1.101101_2 \times 2^3$: sign $1$, exponent $3 + 127 = 130 = \texttt{10000010}$, fraction `101101` then zeros: `0xC15A0000`. (b) Sign $0$, exponent `10000011` $= 131$, so $2^4$; fraction `1001`: $1.1001_2 \times 2^4 = 11001_2 = 25.0$. (c) $-0.0$: sign set, everything else zero; it compares equal to $+0.0$.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-15-6">

<strong>Problem 15.6</strong> (Floating-point statements)

Which are true for IEEE double precision in C? (i) `0.1 + 0.2 == 0.3`; (ii) `(float)16777217 == 16777216.0f`; (iii) for a NaN `x`, `x != x` is true; (iv) `-0.0 == 0.0` is true; (v) floating-point addition is associative.

<details class="nb-hint">
<summary>Hint</summary>

Each statement is one line of the float-traps program in [Section 1.3](../01-data/#sec-coa-ieee).

</details>

<details class="nb-sol">
<summary>Solution</summary>

(ii), (iii) and (iv). (i) is false (the sum is $0.30000000000000004$); a float has 24 significand bits so $2^{24}+1$ rounds to $2^{24}$; NaN is unequal to itself; the two zeros compare equal; addition is not associative because each step rounds.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-15-7">

<strong>Problem 15.7</strong> (Structure sizes)

On x86-64 Linux, what are `sizeof` of `struct S1 {char a; double b; int c; char d;}`, `struct S2 {double b; int c; char a; char d;}` and `struct S3 {char a; short b; char c; int d;}`?

<details class="nb-hint">
<summary>Hint</summary>

Each member starts at a multiple of its own size; the total is a multiple of the largest alignment.

</details>

<details class="nb-sol">
<summary>Solution</summary>

$24$, $16$ and $12$ (program `prob-padding.c` printed them). S1: $a$ at $0$, $b$ at $8$, $c$ at $16$, $d$ at $20$, padded to $24$. S2 sorts the members by size: $8 + 4 + 1 + 1 = 14$, padded to $16$. S3: $a$ $0$, $b$ $2$, $c$ $4$, $d$ $8$, size $12$.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-15-8">

<strong>Problem 15.8</strong> (Bytes in memory, and a 32-bit type)

The 32-bit value `0xA1B2C3D4` is stored at address `0x200`. Which byte is at `0x202` on a little-endian machine, and on a big-endian one? Which C type is guaranteed to be a 32-bit signed integer: `int`, `long`, `int32_t`, `int_least32_t`?

<details class="nb-hint">
<summary>Hint</summary>

Little-endian: least significant byte first.

</details>

<details class="nb-sol">
<summary>Solution</summary>

Little-endian stores `D4 C3 B2 A1`, so `0x202` holds `B2`; big-endian stores `A1 B2 C3 D4`, so `C3`. Only `int32_t` is guaranteed to be exactly 32 bits, two’s complement; `int` is 32 bits on common platforms but only guaranteed $\ge 16$, `long` is 64 bits on Linux x86-64, and `int_least32_t` may be wider.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-15-9">

<strong>Problem 15.9</strong> (Encodings and switching power)

A sensor’s 12-bit samples hover around $0$, alternating in sign. A designer wants the least dynamic power on the data bus. Which statements are true? (i) 2’s complement is best because the adder is simplest; (ii) sign-magnitude toggles fewer bits for small values changing sign; (iii) Gray code helps most for values that change by $\pm 1$ in sequence, such as counters and addresses; (iv) dynamic power is independent of the data.

<details class="nb-hint">
<summary>Hint</summary>

Count the bits that change between $+1$ and $-1$ in each encoding.

</details>

<details class="nb-sol">
<summary>Solution</summary>

(ii) and (iii). Dynamic power $\propto \alpha C V^2 f$ depends on the toggle rate $\alpha$, hence on the data; from $+1$ to $-1$ two’s complement flips every bit, while sign-magnitude flips two. The simulation in [Section 1.7](../01-data/#sec-coa-lowpower) measured about five times fewer toggles. (i) mixes up arithmetic convenience with bus power.

</details>

</div>

## 15.2 Boolean algebra and combinational logic {#s15-2}

<div class="nb nb-problem nb-block" id="problem-15-10">

<strong>Problem 15.10</strong> (Reduce)

Simplify $(AB + C)(AB + \bar C)$.

<details class="nb-hint">
<summary>Hint</summary>

Distribute OR over AND: $(X + Y)(X + Z) = X + YZ$.

</details>

<details class="nb-sol">
<summary>Solution</summary>

$AB + C\bar C = AB + 0 = AB$; the script confirms equality on all eight inputs.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-15-11">

<strong>Problem 15.11</strong> (Names of the laws)

Which are correct? (i) Intersection (AND with constants): $P \cdot 1 = P$ and $P \cdot 0 = 0$; (ii) union: $P + 1 = P$; (iii) absorption: $P + PQ = P$; (iv) complement: $P \cdot \bar P = 1$; (v) De Morgan: $\overline{P + Q} = \bar P\,\bar Q$.

<details class="nb-hint">
<summary>Hint</summary>

Check each with $P = 0$ and $P = 1$.

</details>

<details class="nb-sol">
<summary>Solution</summary>

(i), (iii) and (v). (ii) is wrong: $P + 1 = 1$ (and $P + 0 = P$). (iv) is wrong: $P \bar P = 0$, while $P + \bar P = 1$.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-15-12">

<strong>Problem 15.12</strong> (Which function, which gate?)

(a) Which single gate equals $f = \overline{(xy) + (\bar x \bar y)}$? (b) A NAND gate is fed $\bar A$ and $\bar B$. What gate is the combination?

<details class="nb-hint">
<summary>Hint</summary>

$xy + \bar x\bar y$ is the equality test.

</details>

<details class="nb-sol">
<summary>Solution</summary>

(a) $xy + \bar x\bar y$ is XNOR, so $f = x \oplus y$, an XOR. (b) $\overline{\bar A \bar B} = A + B$ by De Morgan: an OR gate. Both were checked on all inputs.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-15-13">

<strong>Problem 15.13</strong> 🌶 (A product of maxterms)

$F(A,B,C,D) = \prod M(1,2,3,5,6,7,10,14,15)$. Give a minimal SOP and a minimal POS.

<details class="nb-hint">
<summary>Hint</summary>

The ones of $F$ are the minterms that are <em>not</em> listed.

</details>

<details class="nb-sol">
<summary>Solution</summary>

$F = \sum m(0,4,8,9,11,12,13)$. Quine–McCluskey gives the minimal SOP $F = \bar C\bar D + A\bar C + A\bar BD$ and the minimal POS $F = (\bar C + D)(\bar B + \bar C)(A + \bar D)$. Check: minterm $1$ ($ABCD = 0001$) makes $A + \bar D = 0$, as a maxterm must.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-15-14">

<strong>Problem 15.14</strong> (Spot the redundant term)

Simplify $XY + \bar XZ + YZ$.

<details class="nb-hint">
<summary>Hint</summary>

One term is the consensus of the other two.

</details>

<details class="nb-sol">
<summary>Solution</summary>

$XY + \bar XZ$: $YZ$ is the consensus of $XY$ and $\bar XZ$ on $X$ (the ON-set is $\{1,3,6,7\}$ either way). Keep $YZ$ only if the circuit must be hazard-free.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-15-15">

<strong>Problem 15.15</strong> (K-map with don’t-cares)

Minimise $F = \sum m(0,1,2,5,8,9,10) + d(13,15)$.

<details class="nb-hint">
<summary>Hint</summary>

The four corners form one group.

</details>

<details class="nb-sol">
<summary>Solution</summary>

$F = \bar C D + \bar B \bar D$. The corners $0, 2, 8, 10$ give $\bar B\bar D$; the cells $1, 5, 9, 13$ (using don’t-care $13$) give $\bar C D$; don’t-care $15$ is not needed.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-15-16">

<strong>Problem 15.16</strong> (Hazard or not?)

(a) Does $F = A\bar B + BC$ have a static hazard? If so, when, and how is it removed? (b) Does $Z = \bar A + B + \bar C$?

<details class="nb-hint">
<summary>Hint</summary>

Look for a variable appearing both complemented and uncomplemented in different terms.

</details>

<details class="nb-sol">
<summary>Solution</summary>

(a) Yes, a static-1 hazard when $A = C = 1$ and $B$ changes: $F(1,0,1) = F(1,1,1) = 1$ but no single term covers both cells, so the output can glitch to $0$. Adding the consensus term $AC$ removes it. (b) No: each variable appears once, so no input reaches the output along paths of opposite polarity; and as a combinational function it has no race either.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-15-17">

<strong>Problem 15.17</strong> (Gates, families and scales)

Which are true? (i) An XNOR needs at least four 2-input NOR gates; (ii) an OR needs at least three 2-input NAND gates; (iii) an unconnected TTL input behaves as logic $1$; (iv) RTL’s main advantage is its simplicity (few components); (v) CMOS dissipates significant power even when its inputs do not change; (vi) an LSI package holds a few gates.

<details class="nb-hint">
<summary>Hint</summary>

The gate counts are in [Section 2.2](../02-boolean/#sec-coa-universal), the families in [Section 2.6](../02-boolean/#sec-coa-families).

</details>

<details class="nb-sol">
<summary>Solution</summary>

(i), (ii), (iii) and (iv). CMOS’s static power is very small (dynamic power dominates, though leakage grows in modern processes); an LSI package holds hundreds to thousands of gates (a few gates is SSI).

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-15-18">

<strong>Problem 15.18</strong> 🌶 (Testing a stuck-at fault)

For $F = (A + B)\,C$, which input vector(s) detect the fault “$A$ stuck-at-$0$”? Does higher observability of internal nodes increase or decrease the number of test cycles?

<details class="nb-hint">
<summary>Hint</summary>

Set $A$ to the opposite of the stuck value, and make the fault visible at $F$.

</details>

<details class="nb-sol">
<summary>Solution</summary>

Only $ABC = 101$: $A = 1$ excites the fault, $B = 0$ keeps the OR from masking it, $C = 1$ lets it through the AND. Higher observability (and controllability) means <em>fewer</em> test vectors and cycles for the same coverage.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-15-19">

<strong>Problem 15.19</strong> (Demultiplexer routing)

A 1-to-8 demultiplexer has data input $D$ and selects $S_2S_1S_0$ ($S_2$ the most significant). Which output receives $D$ for $S_2S_1S_0 = 110$? Write the expression for $O_5$.

<details class="nb-hint">
<summary>Hint</summary>

The select value is the output index.

</details>

<details class="nb-sol">
<summary>Solution</summary>

$O_6$. $O_5 = D\,S_2\,\bar S_1\,S_0$ ($5 = \texttt{101}$); every other output is $0$.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-15-20">

<strong>Problem 15.20</strong> (A function on a 4:1 mux)

Implement $F(A,B,C) = \sum m(0,3,5,6)$ on a 4:1 multiplexer with selects $A, B$.

<details class="nb-hint">
<summary>Hint</summary>

For each $AB$, look at the two rows with $C = 0$ and $C = 1$.

</details>

<details class="nb-sol">
<summary>Solution</summary>

$I_0 = \bar C$, $I_1 = C$, $I_2 = C$, $I_3 = \bar C$ (this $F$ is $A \oplus B \oplus \bar C$, a parity function).

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-15-21">

<strong>Problem 15.21</strong> 🌶 (Adder delays)

With one delay per AND, OR or XOR gate: when is the carry out of a 32-bit ripple-carry adder ready, and when if it is built from 4-bit carry-lookahead blocks with the block carries rippling?

<details class="nb-hint">
<summary>Hint</summary>

Ripple: two levels per bit. A block produces its carry-out $2$ delays after its carry-in, except the first, which needs $3$.

</details>

<details class="nb-sol">
<summary>Solution</summary>

Ripple: $2 \times 32 = 64$ (last sum bit $63$). CLA blocks: $3 + 2 \times 7 = 17$, last sum at $18$, matching the gate-level model of [Section 3.2](../03-combinational/#sec-coa-cla).

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-15-22">

<strong>Problem 15.22</strong> (Building big multiplexers and decoders)

How many 4:1 muxes make a 64:1 mux? How many 2:1 muxes make a 128:1 mux? How many 3-to-8 decoders (with enable) make a 6-to-64 decoder?

<details class="nb-hint">
<summary>Hint</summary>

Count by levels of the tree.

</details>

<details class="nb-sol">
<summary>Solution</summary>

$16 + 4 + 1 = 21$; $127$ ($n - 1$ for any $n$:1 tree of 2:1 muxes); $8 + 1 = 9$ (one decodes the high three bits and enables one of eight).

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-15-23">

<strong>Problem 15.23</strong> (A wide select)

For `wire [255:0] a, b, c; assign c = sel ? a : b;` which are true? (i) it synthesises to 256 two-input muxes; (ii) the path from `a` to `c` has 256 mux delays; (iii) `sel` drives 256 loads and needs buffering; (iv) it creates latches.

<details class="nb-hint">
<summary>Hint</summary>

The muxes work in parallel, one per bit.

</details>

<details class="nb-sol">
<summary>Solution</summary>

(i) and (iii). The data path is one mux deep; the high fan-out of `sel` is the real cost. A continuous assignment with both branches defined is purely combinational, so there are no latches.

</details>

</div>

## 15.3 Sequential circuits and HDLs {#s15-3}

<div class="nb nb-problem nb-block" id="problem-15-24">

<strong>Problem 15.24</strong> (Dividing a clock)

A D flip-flop with $D = \bar Q$ is clocked at $25$ MHz. What is the frequency of $Q$? What if three such stages are chained, each clocked by the previous stage?

<details class="nb-hint">
<summary>Hint</summary>

Each stage toggles once per active edge.

</details>

<details class="nb-sol">
<summary>Solution</summary>

$12.5$ MHz with a $50\%$ duty cycle; three stages divide by $8$: $3.125$ MHz.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-15-25">

<strong>Problem 15.25</strong> (XOR feedback, inverted)

A D flip-flop has $D = \bar X \oplus Q$. What does it behave like? Is $D = X \oplus \bar Q$ any different?

<details class="nb-hint">
<summary>Hint</summary>

Write $Q^+$ for $X = 0$ and $X = 1$.

</details>

<details class="nb-sol">
<summary>Solution</summary>

For $X = 0$, $Q^+ = \bar Q$ (toggle); for $X = 1$, $Q^+ = Q$ (hold): a T flip-flop with $T = \bar X$. $X \oplus \bar Q$ is the same function ($= \overline{X \oplus Q}$), so the second circuit behaves identically.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-15-26">

<strong>Problem 15.26</strong> 🌶🌶 (A counter from J/K equations)

Two JK flip-flops share a clock: $J_A = \bar Q_B$, $K_A = Q_B$, $J_B = Q_A$, $K_B = \bar Q_A$. Starting from $Q_AQ_B = 00$, list the states for four clocks. What kind of counter is it?

<details class="nb-hint">
<summary>Hint</summary>

With $K = \bar J$ a JK flip-flop is a D flip-flop with $D = J$.

</details>

<details class="nb-sol">
<summary>Solution</summary>

$00 \to 10 \to 11 \to 01 \to 00$ (and from $11$: $11 \to 01 \to 00 \to 10 \to 11$). Since $K_A = \bar J_A$ and $K_B = \bar J_B$, $Q_A^+ = \bar Q_B$ and $Q_B^+ = Q_A$: a 2-bit Johnson (twisted-ring) counter with four states, each differing from the next in one bit.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-15-27">

<strong>Problem 15.27</strong> 🌶 (A feedback shift register)

A 4-bit register $Q_3Q_2Q_1Q_0$ shifts right on each clock; the new $Q_3$ is $(Q_1 \cdot Q_0) \oplus Q_3$. Starting from `0110`, give the state after each of six clocks.

<details class="nb-hint">
<summary>Hint</summary>

Compute the feedback bit from the current state before shifting.

</details>

<details class="nb-sol">
<summary>Solution</summary>

`0110` $\to$ `0011` $\to$ `1001` $\to$ `1100` $\to$ `1110` $\to$ `1111` $\to$ `0111`.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-15-28">

<strong>Problem 15.28</strong> (Latches and master–slave flip-flops)

Which are true? (i) A NOR latch holds its state with $S = R = 0$; (ii) a NAND latch holds its state with $\bar S = \bar R = 0$; (iii) a master–slave flip-flop with the master enabled while the clock is high changes its output when the clock falls; (iv) a gated D latch is transparent while enabled; (v) a master–slave JK flip-flop suffers from race-around.

<details class="nb-hint">
<summary>Hint</summary>

Hold means: every input at its gate’s non-controlling value.

</details>

<details class="nb-sol">
<summary>Solution</summary>

(i), (iii) and (iv). A NAND latch holds with both active-low inputs at $1$; $0, 0$ is its forbidden input. Master–slave construction exists precisely to cure race-around (it keeps the weaker ones-catching problem).

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-15-29">

<strong>Problem 15.29</strong> 🌶🌶 (Setup, hold and skew)

A path between two flip-flops has $t_{cq} = 0.8$ ns, logic delay between $0.4$ and $4.5$ ns, $t_{su} = 0.6$ ns, $t_h = 0.9$ ns. The capturing flip-flop’s clock arrives $0.7$ ns after the launching one’s. Find the minimum clock period and check hold. What would they be without skew?

<details class="nb-hint">
<summary>Hint</summary>

$T \ge t_{cq} + t_{\max} + t_{su} - \delta$ and $t_{cq} + t_{\min} \ge t_h + \delta$.

</details>

<details class="nb-sol">
<summary>Solution</summary>

$T \ge 0.8 + 4.5 + 0.6 - 0.7 = 5.2$ ns ($192$ MHz). Hold slack $= 0.8 + 0.4 - 0.9 - 0.7 = -0.4$ ns: a hold violation, whatever the clock period. Without skew: $T \ge 5.9$ ns and hold slack $+0.3$ ns. The skew bought speed and broke hold.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-15-30">

<strong>Problem 15.30</strong> 🌶 (A flip-flop feeding itself)

A flip-flop’s $Q$ returns to its own $D$ through $0.1$ ns of logic; $t_{cq} = 1.0$ ns, $t_{su} = 0.5$ ns, $t_h = 1.4$ ns, and the clock reaches it through a buffer with $0.6$ ns delay. Setup or hold problem? Does the buffer matter?

<details class="nb-hint">
<summary>Hint</summary>

Launch and capture are the same flip-flop.

</details>

<details class="nb-sol">
<summary>Solution</summary>

Hold: new data arrive $1.0 + 0.1 = 1.1$ ns after the edge but must stay stable for $1.4$ ns, a violation of $0.3$ ns at any frequency. The buffer delays launch and capture equally, so it does not matter. Fix: at least $0.3$ ns more delay in the feedback path.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-15-31">

<strong>Problem 15.31</strong> (Two always blocks)

What are `c1` and `c2` after one rising edge, and after two? How many stages of delay does each version describe?

```verilog {filename="prob-blocking.v, lines 4–6",linenos=table,linenostart=4}
  reg b1 = 0, c1 = 0, b2 = 0, c2 = 0;
  always @(posedge clk) begin b1 = a;  c1 = b1;  end   // version 1
  always @(posedge clk) begin b2 <= a; c2 <= b2; end   // version 2
```

<details class="nb-hint">
<summary>Hint</summary>

Blocking assignments in order; nonblocking ones all at the end of the step.

</details>

<details class="nb-sol">
<summary>Solution</summary>

After one edge `c1 = 1`, `c2 = 0`; after two both are $1$ (simulated with Icarus Verilog, `prob-blocking.v`). Version 1 reads the new `b1`, so `c1` is loaded with `a` at the same edge: both registers hold the same value, a single stage of delay (synthesis may merge them into one flip-flop). Version 2 is a two-stage shift register.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-15-32">

<strong>Problem 15.32</strong> (What does this VHDL describe?)

Describe the hardware this process infers.

```vhdl
process (clk, rst) begin
  if rst = '1' then q <= '0';
  elsif rising_edge(clk) then
    if en = '1' then q <= d; end if;
  end if;
end process;
```

<details class="nb-hint">
<summary>Hint</summary>

Where is `rst` tested relative to the clock edge?

</details>

<details class="nb-sol">
<summary>Solution</summary>

A rising-edge D flip-flop with an <em>asynchronous</em> active-high reset (it is in the sensitivity list and tested before the edge) and a clock enable. Compare [Section 4.7](../04-sequential/#sec-coa-hdl), where reset is tested inside `rising_edge`: synchronous.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-15-33">

<strong>Problem 15.33</strong> 🌶 (Fork and join)

A process forks three threads: one waits $15$, one waits $40$, one loops for ever (`forever #5;`). At what time does the parent continue with `join_any`? With `join_none`? And if only the first two threads are forked with `join`?

<details class="nb-hint">
<summary>Hint</summary>

All, first, none.

</details>

<details class="nb-sol">
<summary>Solution</summary>

`join_any`: $t = 15$; `join_none`: $t = 0$; `join` of the two finite threads: $t = 40$ (with the infinite thread in a `join` it would never continue). Simulated in `prob-fork.v`.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-15-34">

<strong>Problem 15.34</strong> (Storage from multiplexers)

How many 2:1 multiplexers (and nothing else) make a latch, an edge-triggered flip-flop, and an element that stores data on both clock edges?

<details class="nb-hint">
<summary>Hint</summary>

A mux with its output fed back to one input is a latch.

</details>

<details class="nb-sol">
<summary>Solution</summary>

One, two (master–slave), three (two latches with opposite enables plus an output mux selected by the clock), as simulated in [Section 4.7](../04-sequential/#sec-coa-hdl).

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-15-35">

<strong>Problem 15.35</strong> (States of a detector)

How many states do a Mealy and a Moore machine need to detect the overlapping pattern `1101`?

<details class="nb-hint">
<summary>Hint</summary>

States remember the longest matched prefix.

</details>

<details class="nb-sol">
<summary>Solution</summary>

Mealy: $4$ (prefixes of length $0$ to $3$; the output is on the transition). Moore: $5$ (one more state meaning “`1101` just seen”). Both need $\lceil \log_2 k \rceil = 2$ or $3$ flip-flops in binary encoding.

</details>

</div>

## 15.4 Instruction sets and control {#s15-4}

<div class="nb nb-problem nb-block" id="problem-15-36">

<strong>Problem 15.36</strong> 🌶 (Expanding opcodes)

A machine has 16-bit instructions and 6-bit address fields. It has 10 two-address instructions. How many one-address instructions can it have at most? If it has 300 one-address instructions, how many zero-address ones at most?

<details class="nb-hint">
<summary>Hint</summary>

Free patterns of one format become prefixes for the next, each gaining $6$ bits.

</details>

<details class="nb-sol">
<summary>Solution</summary>

Two-address format: $16 - 12 = 4$ opcode bits, $16$ patterns; $6$ unused, each with $2^6$ extensions: $384$ one-address. With $300$ used: $84 \times 64 = 5376$ zero-address.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-15-37">

<strong>Problem 15.37</strong> (Effective addresses)

$R1 = \texttt{0x300}$, $R2 = 8$; memory: $M[\texttt{0x300}] = \texttt{0x500}$, $M[\texttt{0x308}] = \texttt{0x44}$, $M[\texttt{0x380}] = \texttt{0x99}$, $M[\texttt{0x500}] = \texttt{0x77}$, $M[\texttt{0x200}] = \texttt{0x300}$. Give the operand for: `(R1)`, `0x80(R1)`, `(R1+R2)`, memory indirect `@0x200`, and `@(R1)` (the operand’s address is $M[R1]$).

<details class="nb-hint">
<summary>Hint</summary>

Each pair of brackets is one memory read.

</details>

<details class="nb-sol">
<summary>Solution</summary>

`0x500`, `0x99`, `0x44`, `0x500` ($M[M[\texttt{0x200}]] = M[\texttt{0x300}]$), and `0x77` ($M[M[\texttt{0x300}]]$).

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-15-38">

<strong>Problem 15.38</strong> (PC-relative target)

A 4-byte branch at `0x3FFC` has displacement $-\texttt{0x40}$. Where does it go?

<details class="nb-hint">
<summary>Hint</summary>

The displacement is added to the address of the next instruction.

</details>

<details class="nb-sol">
<summary>Solution</summary>

$\texttt{0x3FFC} + 4 - \texttt{0x40} = \texttt{0x3FC0}$.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-15-39">

<strong>Problem 15.39</strong> (Legal MOVs)

Which assemble on 32-bit x86? (i) `mov cl, dh`; (ii) `mov ax, si`; (iii) `mov [esi], [edi]`; (iv) `mov es, 0x20`; (v) `mov bp, sp`; (vi) `mov eax, dl`; (vii) `mov dword ptr [ebx], 7`.

<details class="nb-hint">
<summary>Hint</summary>

Same size, at most one memory operand, no immediate into a segment register.

</details>

<details class="nb-sol">
<summary>Solution</summary>

(i), (ii), (v) and (vii); GNU `as` rejected (iii) (two memory operands), (iv) (immediate to a segment register) and (vi) (size mismatch; `movzx` exists for that). Checked by `prob-mov.sh`.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-15-40">

<strong>Problem 15.40</strong> (Registers)

Which are true? (i) The accumulator holds an implicit operand and the ALU result; (ii) on the 8086, the data registers and the pointer/index registers are both general registers; (iii) IP is a general register; (iv) the flags register is updated by `MOV`; (v) `INC` leaves the carry flag unchanged on x86.

<details class="nb-hint">
<summary>Hint</summary>

Sections [5.1](../05-isa/#sec-coa-formats) and [5.4](../05-isa/#sec-coa-x86).

</details>

<details class="nb-sol">
<summary>Solution</summary>

(i), (ii) and (v). IP is the program counter, not a general register; `MOV` sets no flags.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-15-41">

<strong>Problem 15.41</strong> (Where do the arguments go?)

`long f(long a1, ..., long a9)` is called on x86-64 Linux. Where are `a3` and `a7` on entry to `f`? And on 32-bit x86 with cdecl?

<details class="nb-hint">
<summary>Hint</summary>

Six integer argument registers.

</details>

<details class="nb-sol">
<summary>Solution</summary>

x86-64 System V: `a3` in `rdx`; `a7` on the stack at `[rsp+8]` (just above the return address), `a8` and `a9` above it. 32-bit cdecl: all on the stack, `a1` at `[esp+4]`, so `a3` at `[esp+12]` and `a7` at `[esp+28]` (compare the `-m32` assembly in [Section 5.6](../05-isa/#sec-coa-calling)).

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-15-42">

<strong>Problem 15.42</strong> 🌶 (MIPS by hand)

Encode <code>sub &#36;t1, &#36;s2, &#36;s3</code> (<code>&#36;t1</code> $= 9$, <code>&#36;s2</code> $= 18$, <code>&#36;s3</code> $= 19$, funct of `sub` $= \texttt{0x22}$). Decode `0x8FA80010`.

<details class="nb-hint">
<summary>Hint</summary>

R-format: op(6) rs(5) rt(5) rd(5) shamt(5) funct(6).

</details>

<details class="nb-sol">
<summary>Solution</summary>

`000000 10010 10011 01001 00000 100010` $=$ `0x02534822`. The second word: op $= \texttt{0x23}$ (`lw`), rs $= 29$ (<code>&#36;sp</code>), rt $= 8$ (<code>&#36;t0</code>), immediate $16$: <code>lw &#36;t0, 16(&#36;sp)</code>.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-15-43">

<strong>Problem 15.43</strong> 🌶 (Microinstruction width)

A control unit has 36 control signals in five mutually exclusive groups of sizes $7, 5, 12, 6, 6$; branches can test 9 conditions; the control memory has 1024 words. Find the width of a horizontal and of a vertical (field-encoded) microinstruction.

<details class="nb-hint">
<summary>Hint</summary>

Add “always” to the conditions and “none” to each group.

</details>

<details class="nb-sol">
<summary>Solution</summary>

Next address $10$ bits; condition select $\lceil \log_2 10 \rceil = 4$. Horizontal: $36 + 4 + 10 = 50$ bits. Vertical: fields $3, 3, 4, 3, 3 = 16$ bits, word $16 + 4 + 10 = 30$ bits.

</details>

</div>

## 15.5 Pipelining and performance {#s15-5}

<div class="nb nb-problem nb-block" id="problem-15-44">

<strong>Problem 15.44</strong> (Unpipelined latency)

A 5-stage datapath has stage delays $60, 45, 110, 75, 30$ ns. What is the instruction latency without pipelining? Pipelined with $5$ ns latches: the clock, the latency, the time for $1000$ instructions and the speed-up.

<details class="nb-hint">
<summary>Hint</summary>

Unpipelined latency is the sum; the pipelined clock is the maximum plus the latch.

</details>

<details class="nb-sol">
<summary>Solution</summary>

Unpipelined: $320$ ns. Pipelined: clock $115$ ns, latency $575$ ns, $1000$ instructions in $(5 + 999) \times 115 = 115460$ ns against $320000$ ns, speed-up $2.77$.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-15-45">

<strong>Problem 15.45</strong> 🌶 (Stages that take several cycles)

Five stages take $1, 2, 1, 3, 1$ cycles. How many cycles do $8$ instructions take if every unit accepts a new instruction each cycle? If a unit is busy until it finishes?

<details class="nb-hint">
<summary>Hint</summary>

In the second case the slowest stage sets the rate.

</details>

<details class="nb-sol">
<summary>Solution</summary>

Pipelined units: $8 + 7 = 15$ cycles. Non-pipelined units: the 3-cycle stage releases one instruction every $3$ cycles: $8 + 7 \times 3 = 29$.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-15-46">

<strong>Problem 15.46</strong> (Name the dependence)

`I1: r1 = r2 + r3`; `I2: r4 = r1 * r5`; `I3: r5 = r6 - 1`; `I4: r1 = r7 + r8`. Name every dependence. Which can cause hazards in a 5-stage in-order pipeline?

<details class="nb-hint">
<summary>Hint</summary>

Later instruction reads what an earlier writes: RAW; writes what it reads: WAR.

</details>

<details class="nb-sol">
<summary>Solution</summary>

I2–I1 RAW on `r1`; I3–I2 WAR on `r5` (I3 writes a register the earlier I2 reads); I4–I1 WAW on `r1`; I4–I2 WAR on `r1`. In the in-order 5-stage pipeline only the RAW can stall; register renaming removes the WAR and WAW.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-15-47">

<strong>Problem 15.47</strong> 🌶🌶 (Count the stalls)

<code>lw &#36;2,0(&#36;1)</code>; <code>add &#36;3,&#36;2,&#36;2</code>; <code>lw &#36;4,4(&#36;1)</code>; <code>sub &#36;5,&#36;4,&#36;3</code>; <code>sw &#36;5,8(&#36;1)</code>. How many cycles on the 5-stage pipeline with a split-phase register file and no forwarding, and with full forwarding?

<details class="nb-hint">
<summary>Hint</summary>

Without forwarding a dependent instruction reads in the producer’s WB cycle; with forwarding only load-use costs a cycle.

</details>

<details class="nb-sol">
<summary>Solution</summary>

The simulator of [Section 7.3](../07-pipeline/#sec-coa-forwarding) gives $15$ cycles ($6$ stalls) without forwarding and $11$ cycles ($2$ stalls, one per load-use pair) with it.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-15-48">

<strong>Problem 15.48</strong> (Average CPI)

An 800 MHz processor runs a mix of $40\%$ ALU (CPI 1), $25\%$ loads (CPI 4), $10\%$ stores (CPI 3), $25\%$ branches (CPI 2). Find the CPI, the MIPS rating and the time for $2 \times 10^9$ instructions.

<details class="nb-hint">
<summary>Hint</summary>

Weighted average.

</details>

<details class="nb-sol">
<summary>Solution</summary>

$\text{CPI} = 0.4 + 1.0 + 0.3 + 0.5 = 2.2$; $800/2.2 = 363.6$ MIPS; $2\times10^9 \times 2.2 / 800\times10^6 = 5.5$ s.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-15-49">

<strong>Problem 15.49</strong> 🌶 (Branches)

(a) $20\%$ of instructions are branches, $35\%$ of them mispredicted, $3$ cycles lost per misprediction: CPI with a base of $1$? (b) A loop branch is taken 5 times then not taken, and the loop runs 10 times. How many mispredictions do a 1-bit and a 2-bit predictor (starting strongly taken) make?

<details class="nb-hint">
<summary>Hint</summary>

(b) A 1-bit predictor also misses on re-entry.

</details>

<details class="nb-sol">
<summary>Solution</summary>

(a) $1 + 0.2 \times 0.35 \times 3 = 1.21$. (b) 1-bit: $19$ (one in the first execution, two in each of the other nine); 2-bit: $10$ (only the exits).

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-15-50">

<strong>Problem 15.50</strong> (What makes a pipelined RISC faster?)

All arithmetic instructions have the same CPI. Which improve execution time of a typical program? (i) A higher clock frequency with the same CPI; (ii) disabling forwarding; (iii) doubling the instruction and data caches without changing the cycle time; (iv) adding a pipeline stage that does no useful work; (v) better branch prediction.

<details class="nb-hint">
<summary>Hint</summary>

Iron law: IC $\times$ CPI $/ f$.

</details>

<details class="nb-sol">
<summary>Solution</summary>

(i), (iii) and (v). Disabling forwarding adds stalls; an extra empty stage adds latency and branch penalty without shortening the clock ([Section 7.7](../07-pipeline/#sec-coa-speedup-what)).

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-15-51">

<strong>Problem 15.51</strong> (Amdahl)

$60\%$ of a program’s time is sped up $10\times$. Overall speed-up? The limit? And a program $70\%$ parallel on $16$ cores?

<details class="nb-hint">
<summary>Hint</summary>

$1/((1-p) + p/s)$.

</details>

<details class="nb-sol">
<summary>Solution</summary>

$1/(0.4 + 0.06) = 2.17$; limit $1/0.4 = 2.5$; $1/(0.3 + 0.7/16) = 2.91$.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-15-52">

<strong>Problem 15.52</strong> (Voltage and frequency)

Supply voltage drops $10\%$ and frequency $20\%$. By what factor does dynamic power change?

<details class="nb-hint">
<summary>Hint</summary>

$P \propto V^2 f$.

</details>

<details class="nb-sol">
<summary>Solution</summary>

$0.9^2 \times 0.8 = 0.648$: power falls by about $35\%$.

</details>

</div>

## 15.6 Memory, I/O, parallel and embedded {#s15-6}

<div class="nb nb-problem nb-block" id="problem-15-53">

<strong>Problem 15.53</strong> (Number of sets)

A 32-bit processor has a 4-way set-associative 1 KB cache with 16-byte lines. How many sets? Split the address.

<details class="nb-hint">
<summary>Hint</summary>

Lines $=$ size$/$line, sets $=$ lines$/$ways.

</details>

<details class="nb-sol">
<summary>Solution</summary>

$64$ lines, $16$ sets; offset $4$ bits, index $4$, tag $24$.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-15-54">

<strong>Problem 15.54</strong> (Two levels of cache)

L1 hit rate $0.85$, L2 (local) hit rate $0.60$. What fraction of accesses reach main memory? With hit times $1$ and $12$ cycles and memory $120$ cycles, what is the AMAT?

<details class="nb-hint">
<summary>Hint</summary>

Multiply miss rates.

</details>

<details class="nb-sol">
<summary>Solution</summary>

$0.15 \times 0.40 = 0.06$. AMAT $= 1 + 0.15 \times (12 + 0.4 \times 120) = 10.0$ cycles.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-15-55">

<strong>Problem 15.55</strong> (Kinds of misses)

Which are true? (i) A miss caused by a working set larger than the cache is a capacity miss; (ii) higher associativity reduces compulsory misses; (iii) larger blocks reduce compulsory misses for sequential data; (iv) a fully associative cache has no conflict misses; (v) a direct-mapped cache never has a lower miss rate than a fully associative LRU cache of the same size.

<details class="nb-hint">
<summary>Hint</summary>

Sections [9.7](../09-memory/#sec-coa-3c) and [9.4](../09-memory/#sec-coa-replacement).

</details>

<details class="nb-sol">
<summary>Solution</summary>

(i), (iii) and (iv). Associativity only removes conflict misses; (v) is false: a loop over one block more than the cache holds defeats LRU but not direct mapping (trace 2 in [Section 9.4](../09-memory/#sec-coa-replacement)).

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-15-56">

<strong>Problem 15.56</strong> 🌶 (Write policies)

(a) Which policy updates the cache but not main memory until the line is evicted? (b) A direct-mapped cache with two 16-byte lines executes W0, W4, R32, W8, W36, R0 (byte addresses). Count memory writes and block reads for write-back + write-allocate and for write-through + no-write-allocate.

<details class="nb-hint">
<summary>Hint</summary>

Addresses 0, 4, 8 are block 0; 32 and 36 are block 2; both map to line 0.

</details>

<details class="nb-sol">
<summary>Solution</summary>

(a) Write-back. (b) Write-back + allocate: $3$ memory writes (dirty evictions) and $5$ block reads. Write-through + no-allocate: $4$ memory writes (every write) and $2$ block reads. Both have one hit (W4 and W36 respectively); simulated with the cache simulator.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-15-57">

<strong>Problem 15.57</strong> (Interleaving)

With 8 memory modules and low-order interleaving, which module holds word address `0x2F`, and which bits choose the module?

<details class="nb-hint">
<summary>Hint</summary>

Low-order: address mod 8.

</details>

<details class="nb-sol">
<summary>Solution</summary>

Module $7$ (word $5$ within it); the low three address bits select the module, so consecutive addresses fall in consecutive modules.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-15-58">

<strong>Problem 15.58</strong> (Pins and chips)

A memory has 18 address lines and 16 data lines: what is its size? How many $32\text{K} \times 8$ chips build a $256\text{K} \times 16$ memory, and what decoder selects them?

<details class="nb-hint">
<summary>Hint</summary>

$2^{18}$ words of 2 bytes.

</details>

<details class="nb-sol">
<summary>Solution</summary>

$2^{18} \times 2$ bytes $= 512$ KB. $8$ rows $\times$ $2$ columns $= 16$ chips, with a 3-to-8 decoder on the top three address bits.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-15-59">

<strong>Problem 15.59</strong> (DRAM and flash)

(a) Order these DRAM read steps: (1) the sense amplifier drives the bit line to a full level and restores the cell; (2) precharge the bit lines to half the supply; (3) the bit line moves slightly up or down; (4) assert the word line. (b) Which statement does not describe flash: (i) non-volatile; (ii) erased in blocks; (iii) limited write endurance; (iv) any byte can be rewritten in place without erasing?

<details class="nb-hint">
<summary>Hint</summary>

[Section 9.2](../09-memory/#sec-coa-mainmem).

</details>

<details class="nb-sol">
<summary>Solution</summary>

(a) 2, 4, 3, 1. (b) (iv): bits can only be programmed one way, so rewriting needs a block erase first.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-15-60">

<strong>Problem 15.60</strong> 🌶 (Trace a small cache)

A cache holds 4 one-byte blocks. Trace the block addresses 1, 5, 9, 1, 5, 2, 1 for direct mapping, 2-way LRU and fully associative LRU. How many hits each?

<details class="nb-hint">
<summary>Hint</summary>

Direct mapped: block mod 4; 2-way: block mod 2.

</details>

<details class="nb-sol">
<summary>Solution</summary>

Direct mapped: all miss ($1, 5, 9$ share line $1$), $0$ hits. 2-way LRU: odd blocks share set $1$ and evict each other; only the last access to $1$ hits: $1$ hit. Fully associative LRU: `MMMHHMH`, $3$ hits.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-15-61">

<strong>Problem 15.61</strong> 🌶 (Row or column?)

`int a[128][128]` is summed on a 16 KB, 4-way cache with 64-byte lines (cold start). How many misses in row order and in column order?

<details class="nb-hint">
<summary>Hint</summary>

A column steps $512$ bytes $= 8$ lines; how many sets does that reach?

</details>

<details class="nb-sol">
<summary>Solution</summary>

Row order: $1024$ misses ($16$ ints per line). Column order: $16384$, every access: the column’s lines fall into only $8$ of the $64$ sets ($32$ lines of capacity for $128$ lines per column), so nothing survives to the next column.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-15-62">

<strong>Problem 15.62</strong> (DMA slow-down)

A device sends $38400$ bit/s in 8-bit characters to memory by cycle-stealing DMA. The processor executes $4$ million memory cycles per second. By how much is it slowed down?

<details class="nb-hint">
<summary>Hint</summary>

One stolen cycle per character.

</details>

<details class="nb-sol">
<summary>Solution</summary>

$4800$ characters per second, so $4800 / 4 \times 10^6 = 0.12\%$.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-15-63">

<strong>Problem 15.63</strong> 🌶🌶 (Store buffers)

Initially $x = y = 0$. Thread 0: `x = 1; r0 = y;`. Thread 1: `y = 1; r1 = x;`. Which outcomes are possible on x86 without fences? (i) $r_0 = 0, r_1 = 1$; (ii) $r_0 = 1, r_1 = 0$; (iii) $r_0 = 1, r_1 = 1$; (iv) $r_0 = 0, r_1 = 0$. Which are possible under sequential consistency?

<details class="nb-hint">
<summary>Hint</summary>

A store can sit in the store buffer while the next load executes.

</details>

<details class="nb-sol">
<summary>Solution</summary>

On x86 (TSO) all four; SC forbids (iv). The litmus program in [Section 12.3](../12-parallel/#sec-coa-consistency) observed (iv) thousands of times without fences and never with them.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-15-64">

<strong>Problem 15.64</strong> (Embedded basics)

(a) Which are true about `volatile`? (i) It forces every access in the source to happen; (ii) it makes `x++` atomic; (iii) a status register can be `const volatile`; (iv) it inserts memory barriers between cores. (b) An 8 MHz timer clock with prescaler $8$ must interrupt every $2$ ms: compare value?

<details class="nb-hint">
<summary>Hint</summary>

Tick $= 8/8\,\text{MHz} = 1\,\mu$s.

</details>

<details class="nb-sol">
<summary>Solution</summary>

(a) (i) and (iii). (b) $2000$ counts (fits a 16-bit timer).

</details>

</div>

## 15.7 Machine check of the answers {#s15-7}

The output of `problems.py`, which recomputes the numbers used in the solutions (tags are problem numbers; problems answered by other programs or by reasoning alone have no line):

```text {filename="Output of problems.py (Python 3.11)"}
[ 1] 1101 0110 1011b = 0xd6b | 7A3Ch = 31292 | 9876 = 0x2694
[ 1] 645o = 421 | 5B9h = 0b10110111001
[ 2] 45&45 = 45 45^45 = 0 45&54 = 36 45|54 = 63
[ 3] SM 10010111 1C 11101000 2C 11101001 range 2C 8 bits -128 127
[ 4] 90 + 40 -> -126, overflow True
[ 4] -90 + -40 -> 126, overflow True
[ 4] -90 + 40 -> -50, overflow False
[ 4] 127 + 1 -> -128, overflow True
[ 4] -128 + -1 -> 127, overflow True
[ 4] 64 + 63 -> 127, overflow False
[ 5] -13.625 -> c15a0000 | 0x41C80000 -> 25.0 | 0x80000000 -> -0.0
[ 8] little-endian bytes at 0x200..0x203: d4 c3 b2 a1 | big-endian: a1 b2 c3 d4
[10] (AB+C)(AB+C') == AB on all inputs: True
[12] [(xy)+(x'y')]' == x xor y: True
[12] NAND with inverted inputs == OR: True
[13] prod M(1,2,3,5,6,7,10,14,15): ON-set [0, 4, 8, 9, 11, 12, 13]
[13] minimal SOP ["C'D' + AC' + AB'D"] POS ["(C' + D)(B' + C')(A + D')"]
[14] XY + X'Z + YZ: ON [1, 3, 6, 7] minimal ["X'Z + XY"]
[15] sum m(0,1,2,5,8,9,10) + d(13,15): ["C'D + B'D'"]
[16] F(1,0,1), F(1,1,1) = 1 1 -> both 1, no common term; add AC
[18] tests for A s-a-0: ['101']
[19] S2S1S0 = 110 -> D appears on O6
[19] S2S1S0 = 101 -> D appears on O5
[20] sum m(0,3,5,6), selects A,B: I0..I3 = ["C'", 'C', 'C', "C'"]
[21] 32-bit ripple: carry 64 sum 63 | CLA blocks: carry 17 sum 18
[22] 64:1 from 4:1 muxes: 21 | 128:1 from 2:1: 127 | 6-to-64 decoder: 8 + 1 = 9
[24] 25 MHz / 2 = 12.5 MHz; three stages: 3.125 MHz
[25] X=0, Q=0,1: X' xor Q -> [1, 0] | X xor Q' -> [1, 0]
[25] X=1, Q=0,1: X' xor Q -> [0, 1] | X xor Q' -> [0, 1]
[26] QA QB from 00 : 00 -> 10 -> 11 -> 01 -> 00
[26] QA QB from 11 : 11 -> 01 -> 00 -> 10 -> 11
[27] from 0110: 0110 0011 1001 1100 1110 1111 0111
[29] Tmin = 5.2 ns, fmax = 192 MHz; hold slack = -0.4 ns
[29] without skew: Tmin = 5.9 ns, hold slack +0.3
[30] self-loop: hold slack = 1.0 + 0.1 - 1.4 = -0.3 ns
[35] 1101 overlapping: Mealy 4 states (matched prefix 0..3), Moore 5
[36] 2-address space 16 -> one-address max 384 -> zero-address max 5376
[37] (R1): 0x500 | 0x80(R1): 0x99 | (R1+R2): 0x44 | @0x200: 0x500 | @(R1): 0x77
[38] target = 0x3FFC + 4 - 0x40 = 0x3fc0
[42] sub $t1,$s2,$s3 = 0x02534822
[42] decode 0x8FA80010: op 0x23 rs 29 rt 8 imm 16
[43] horizontal 50 bits; vertical fields [3, 3, 4, 3, 3] = 16 -> word 30
[44] unpipelined latency 320 ns; clock 115 ns; pipelined latency 575
[44] 1000 instr: 115460 ns vs 320000 ns, speedup 2.77
[45] pipelined units: 15 cycles; non-pipelined units: 29
[47] split total cycles 15 stalls 6
[47] fwd total cycles 11 stalls 2
[48] CPI 2.20; MIPS at 800 MHz 363.6; 2e9 instr 5.500 s
[49] CPI = 1 + 0.2 x 0.35 x 3 = 1.21
[49] 2-bit mispredictions: 10 of 60; 1-bit: 19
[51] p = 0.6, s = 10: 2.17x; limit 2.5x; 70% on 16 cores: 2.91x
[52] V x 0.9, f x 0.8: power x 0.648
[53] 1 KB, 16 B lines, 4-way: sets 16 | offset 4, index 4, tag 24
[54] to memory: 0.15 x 0.40 = 0.060; AMAT = 1 + 0.15 x (12 + 0.4 x 120) = 10.0
[56] write-back+allocate mem writes 3 block reads 5 hits 1
[56] write-through+no-allocate mem writes 4 block reads 2 hits 1
[57] address 0x2F with 8 modules, low-order: module 7 word 5
[58] 18 address, 16 data: 512 KB | 256K x 16 from 32K x 8: 16 chips
[60] direct     MMMMMMM  hits 0
[60] 2-way LRU  MMMMMMH  hits 1
[60] full LRU   MMMHHMH  hits 3
[61] row order misses 1024 | column order 16384
[62] 38400 bit/s -> 4800 bytes/s; 4 MIPS: slow-down 0.12%
[64] 8 MHz, prescaler 8, 2 ms: 2000 counts; 16-bit overflow ok: True
```
