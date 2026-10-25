---
title: "3 · Combinational building blocks"
linkTitle: "3 Combinational building blocks"
weight: 3
math: true
---
A <strong>combinational</strong> circuit’s outputs depend only on its present inputs; there is no memory. This chapter builds the medium-scale blocks that every datapath is made of: adders, comparators, multiplexers, decoders and the ALU, with the delay numericals that OAs and interviews ask about.

## 3.1 Adders and subtractors {#sec-coa-adders}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> a 16-bit ripple-carry adder needs $32$ gate delays for its carry-out; a two-level carry-lookahead adder needs $5$.</em>

</div>

### 3.1.i Half adder, full adder, ripple carry {#s3-1-i}

<div class="nb nb-definition" id="definition-3-1-1">

<strong>Definition 3.1.1</strong>. A <strong>half adder</strong> adds two bits: $S = x \oplus y$, $C = xy$. A <strong>full adder</strong> adds three ($x$, $y$ and a carry-in $c$):

$$
S = x \oplus y \oplus c, \qquad C_{\text{out}} = xy + xc + yc = xy + c\,(x \oplus y).
$$

A full adder is two half adders and an OR gate. An $n$-bit <strong>ripple-carry adder</strong> chains $n$ full adders, each carry-out feeding the next carry-in.

</div>

<figure class="nb-fig"><img src="fig-1.svg" alt="Figure 1" loading="lazy"></figure>

<div class="nb nb-theorem nb-block" id="theorem-3-1-2">

<strong>Theorem 3.1.2</strong> (Ripple-carry delay)

Counting one delay per gate level, a carry passes each full adder in $2$ delays (an AND level and an OR level), so $c_n$ is ready after $2n$ delays and the last sum bit after $2n - 1$. The delay is linear in the word length.

</div>

### 3.1.ii Subtraction with the same adder {#s3-1-ii}

$x - y = x + \overline{y} + 1$ in 2’s complement. Put an XOR gate on every $y$ input, driven by a control line $M$: $M = 0$ passes $y$ (add), $M = 1$ inverts it, and the same $M$ feeds $c_0$ to supply the $+1$. Overflow is $V = c_{n-1} \oplus c_n$ ([Section 1.2](../01-data/#sec-coa-signed)). For unsigned operands the carry-out after a subtraction means <em>no borrow</em>: $c_n = 1$ exactly when $x \ge y$. That is the convention of ARM and of the ALU below; x86 instead stores the inverted value (the borrow) in its carry flag after `SUB`.

## 3.2 Carry-lookahead {#sec-coa-cla}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> all four carries of a 4-bit block computed in parallel from $G_i = x_iy_i$ and $P_i = x_i \oplus y_i$, in $3$ gate delays.</em>

</div>

<div class="nb nb-definition" id="definition-3-2-1">

<strong>Definition 3.2.1</strong>. Bit $i$ <strong>generates</strong> a carry if $G_i = x_i y_i$ and <strong>propagates</strong> one if $P_i = x_i \oplus y_i$ (some books use $x_i + y_i$; both work for carries). Then $c_{i+1} = G_i + P_i c_i$, and unrolling gives every carry as a two-level SOP of the $G$s, $P$s and $c_0$:

$$
c_4 = G_3 + P_3G_2 + P_3P_2G_1 + P_3P_2P_1G_0 + P_3P_2P_1P_0c_0.
$$

</div>

A 4-bit block thus gives all carries after $1$ (for $G$, $P$) $+\,2$ (AND–OR) $= 3$ delays, and the sums one XOR later. Full lookahead over $32$ bits would need AND gates with $33$ inputs, so real adders use 4-bit blocks and either ripple the block carries or add a second lookahead level that works on block generate/propagate signals $G^{I} = G_3 + P_3G_2 + P_3P_2G_1 + P_3P_2P_1G_0$ and $P^{I} = P_3P_2P_1P_0$.

Every design below was built gate by gate in Python, checked as an adder on random inputs, and timed under the stated model (unit delay per AND, OR or XOR gate, unlimited fan-in):

```text {filename="Output of adders.py (Python 3.11)"}
 n  design                       carry-out  last sum bit
 4  ripple-carry                         8             7
 4  carry-lookahead                      3             4
16  ripple-carry                        32            31
16  4-bit CLA blocks, rippled            9            10
16  two-level lookahead                  5             8
32  ripple-carry                        64            63
32  4-bit CLA blocks, rippled           17            18
```

<div class="nb nb-example nb-block" id="example-3-2-2">

<strong>Example 3.2.2</strong> (Reading the table)

For $16$ bits: ripple carry $32$ delays; four 4-bit CLA blocks with the block carries rippling, $c_4, c_8, c_{12}, c_{16}$ at $3, 5, 7, 9$ (each block adds $2$), last sum at $10$; with a second lookahead level all block carries are ready at $5$, the last block’s internal carries at $7$ and its last sum bit at $8$. Speed-up of the carry path: $32/5 = 6.4\times$.

</div>

<div class="nb nb-remark" id="remark-3-2-3">

<strong>Remark 3.2.3</strong> (Other fast adders, one line each) — <strong>Carry-select</strong>: compute each upper block twice (carry-in $0$ and $1$) and pick with a mux when the real carry arrives. <strong>Carry-skip</strong>: let a carry jump over a block whose $P^I = 1$. <strong>Carry-save</strong>: do not propagate at all; keep sum and carry vectors separately (used to add many numbers in a multiplier, [Section 8.1](../08-arith/#sec-coa-mult)). Prefix adders (Kogge–Stone, Brent–Kung) compute all carries in $O(\log n)$ levels.

</div>

<div class="nb nb-moral">

Ripple carry is $O(n)$ because each carry waits for the previous one; lookahead computes carries from $G$ and $P$ directly, and two levels of it make a 16-bit add about as fast as five gates.

</div>

## 3.3 Comparators {#sec-coa-comparators}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> $A = B$ for 4-bit words is the AND of four XNORs.</em>

</div>

Equality: $E = \prod_i \overline{a_i \oplus b_i}$. Magnitude, scanning from the most significant bit: with $e_i = \overline{a_i \oplus b_i}$,

$$
(A > B) = a_3\overline{b_3} + e_3a_2\overline{b_2} + e_3e_2a_1\overline{b_1} + e_3e_2e_1a_0\overline{b_0},
$$

and $A < B$ is the same with the roles swapped. A processor does not build these separately: it subtracts and reads the flags (unsigned $A < B$ iff no carry out of $A - B$; signed $A < B$ iff $N \oplus V = 1$).

## 3.4 Multiplexers, demultiplexers, decoders and encoders {#sec-coa-mux}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> a 1-to-8 demultiplexer with select $S_2S_1S_0 = 100$ routes its input to $O_4$, so $O_4 = D\,S_2\,\overline{S_1}\,\overline{S_0}$.</em>

</div>

<div class="nb nb-definition" id="definition-3-4-1">

<strong>Definition 3.4.1</strong>. A $2^n$:1 <strong>multiplexer</strong> (mux) copies one of $2^n$ data inputs to its output, chosen by $n$ select lines: $Y = \sum_k I_k\, m_k(S)$ where $m_k$ is the $k$-th minterm of the selects. A 1:$2^n$ <strong>demultiplexer</strong> does the reverse: $O_k = D \cdot m_k(S)$, all other outputs $0$. An $n$-to-$2^n$ <strong>decoder</strong> raises exactly output $k$ when the input is $k$ (a demux with $D$ used as an enable). An <strong>encoder</strong> does the reverse; a <strong>priority encoder</strong> outputs the index of the highest active request plus a <em>valid</em> bit, so it is defined for any input pattern.

</div>

<figure class="nb-fig"><img src="fig-2.svg" alt="Figure 2" loading="lazy"></figure>

```verilog {filename="blocks.v"}
// MSI building blocks, each written the way synthesis tools expect.
module demux1to8(input d, input [2:0] s, output [7:0] o);
  assign o = d << s;                 // o[k] = d when s == k, else 0
endmodule

module prienc4(input [3:0] r, output reg [1:0] y, output valid);
  assign valid = |r;                 // some request is active
  always @* casez (r)                // highest index wins
    4'b1zzz: y = 2'd3;          // z (or ?) = don't care in casez
    4'b01zz: y = 2'd2;
    4'b001z: y = 2'd1;
    default: y = 2'd0;
  endcase
endmodule

module mux4(input [3:0] i, input [1:0] s, output y);
  assign y = i[s];
endmodule

module tb;
  reg d; reg [2:0] s; wire [7:0] o;
  reg [3:0] r; wire [1:0] y; wire v;
  demux1to8 dm(d, s, o);
  prienc4 pe(r, y, v);
  initial begin
    d = 1;
    $display("1-to-8 demux, d = 1:   s2 s1 s0 -> o7..o0");
    for (int k = 0; k < 8; k++) begin
      s = k; #1 $display("                        %b  %b  %b -> %b", s[2], s[1], s[0], o);
    end
    d = 0; s = 3'b100; #1 $display("d = 0, s = 100        -> %b", o);
    $display("priority encoder: r3..r0 -> y valid");
    for (int k = 0; k < 16; k += 5) begin
      r = k; #1 $display("                  %b   -> %0d %b", r, y, v);
    end
  end
endmodule
```

```text {filename="Simulation output (Icarus Verilog 12, -g2012)"}
1-to-8 demux, d = 1:   s2 s1 s0 -> o7..o0
                        0  0  0 -> 00000001
                        0  0  1 -> 00000010
                        0  1  0 -> 00000100
                        0  1  1 -> 00001000
                        1  0  0 -> 00010000
                        1  0  1 -> 00100000
                        1  1  0 -> 01000000
                        1  1  1 -> 10000000
d = 0, s = 100        -> 00000000
priority encoder: r3..r0 -> y valid
                  0000   -> 0 0
                  0101   -> 2 1
                  1010   -> 3 1
                  1111   -> 3 1
```

<div class="nb nb-remark" id="remark-3-4-2">

<strong>Remark 3.4.2</strong> (The demux trap) — The select value <em>is</em> the output index, with $S_2$ the most significant bit: $O_4$ is selected by $S_2S_1S_0 = 100$, not by “the fourth line” $011$. When $D = 0$ every output is $0$, whatever the select (last demux line of the output).

</div>

<div class="nb nb-example nb-block" id="example-3-4-3">

<strong>Example 3.4.3</strong> (Building big muxes and decoders)

An $n$:1 mux from $k$:1 muxes is a tree: $\lceil n/k\rceil$ at the first level, then $\lceil n/k^2 \rceil$, and so on. A 32:1 mux from 4:1 muxes needs $8 + 2 + 1 = 11$ (the last one uses two of its four inputs); an $n$:1 mux from 2:1 muxes always needs $n - 1$. A 4-to-16 decoder from 2-to-4 decoders with enables needs $4 + 1 = 5$: one decodes the two high bits and enables one of four that decode the two low bits. (Counts from `muxfn.py` below.)

</div>

<div class="nb nb-remark" id="remark-3-4-4">

<strong>Remark 3.4.4</strong> (`assign c = sel ? a : b;` on 256-bit buses) — This synthesises to $256$ two-input muxes in parallel, so the data path from `a` or `b` to `c` is a single mux delay: the design is not slow because the buses are wide. The cost is elsewhere: `sel` has a fan-out of $256$ select inputs, so the tools must insert a buffer tree on it (its delay grows roughly with the logarithm of the fan-out), and the area is $256$ muxes. If `sel` comes late, that buffer tree is on the critical path.

</div>

## 3.5 Implementing functions with muxes, decoders and ROMs {#sec-coa-implement}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> any function of $n$ variables on one $2^{n-1}$:1 mux, with the last variable (or its complement, $0$ or $1$) on each data input.</em>

</div>

<div class="nb nb-remark" id="algorithm-3-5-1">

<strong>Algorithm 3.5.1</strong> (Function on a mux) — Use the first $n-1$ variables as selects. For each select value, look at the two truth-table rows (last variable $0$ and $1$): outputs $00 \to$ data input $0$; $11 \to 1$; $01 \to$ the last variable; $10 \to$ its complement.

</div>

```text {filename="Output of muxfn.py (Python 3.11)"}
F(A,B,C) = sum m(1,2,6,7) on a 4:1 mux with selects A,B:
   AB = 00: I0 = C
   AB = 01: I1 = C'
   AB = 10: I2 = 0
   AB = 11: I3 = 1
   on a 3-to-8 decoder: F = D1 + D2 + D6 + D7 (one 4-input OR gate)
8:1 mux from 2:1 muxes: 7
16:1 mux from 4:1 muxes: 5
32:1 mux from 4:1 muxes: 11
64:1 mux from 4:1 muxes: 21
256:1 mux from 2:1 muxes: 255
ROM for 4 inputs and 8 outputs: 2^4 x 8 = 128 bits
ROM for 8 inputs and 8 outputs: 2^8 x 8 = 2048 bits
ROM for 10 inputs and 4 outputs: 2^10 x 4 = 4096 bits
decoders: 4-to-16 from 2-to-4 (with enable) = 5 ; 5-to-32 from 3-to-8 + one 2-to-4 = 5
```

<div class="nb nb-definition" id="fact-3-5-2">

<strong>Fact 3.5.2</strong> (Decoders and ROMs). A decoder produces all $2^n$ minterms, so any function is the OR of the decoder outputs at its $1$s (the output above). A ROM is exactly that: an address decoder plus a programmable OR array, so a ROM with $n$ address lines and $m$ data bits ($2^n \times m$ bits) implements any $m$ functions of $n$ variables. A <strong>PLA</strong> has a programmable AND array <em>and</em> a programmable OR array, so it stores only the product terms it needs; a <strong>PAL</strong> has a programmable AND array and a fixed OR array. FPGAs use small RAM-based look-up tables (typically 4 to 6 inputs), which are ROMs again.

</div>

## 3.6 The ALU {#sec-coa-alu}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> one adder doing both ADD and SUB, with the zero, negative, carry and overflow flags read off its result.</em>

</div>

A 1-bit ALU slice computes AND, OR and the full-adder sum of $a_i$ and (possibly inverted) $b_i$, and a mux selects the result; $n$ slices with the carry chained make an $n$-bit ALU. The control lines are the operation select, <em>Binvert</em> and the carry-in (both $1$ for subtraction). Flags: $Z$ is the NOR of all result bits, $N$ the top bit, $C$ the carry out of the top bit, $V = c_{n-1} \oplus c_n$.

```verilog {filename="alu.v"}
// 4-bit ALU: one adder does ADD and SUB (b inverted, carry-in 1); flags Z N C V.
module alu4(input [3:0] a, b, input [1:0] op,
            output reg [3:0] y, output z, n, output reg c, v);
  wire sub = (op == 2'b11);
  wire [3:0] bb = sub ? ~b : b;          // the "Binvert" control
  wire [4:0] sum = a + bb + sub;         // carry-in = 1 for subtraction
  always @* begin
    c = 0; v = 0;
    case (op)
      2'b00: y = a & b;
      2'b01: y = a | b;
      default: begin
        y = sum[3:0];
        c = sum[4];                                  // carry out of bit 3
        v = (a[3] == bb[3]) && (y[3] != a[3]);       // signed overflow
      end
    endcase
  end
  assign z = (y == 0);
  assign n = y[3];
endmodule

module tb;
  reg [3:0] a, b; reg [1:0] op;
  wire [3:0] y; wire z, n, c, v;
  alu4 u(a, b, op, y, z, n, c, v);
  task t(input [3:0] x, input [3:0] w, input [1:0] o, input [8*3-1:0] name);
    begin
      a = x; b = w; op = o; #1;
      $display("%s %b, %b -> %b  Z=%b N=%b C=%b V=%b  (signed %0d)",
               name, a, b, y, z, n, c, v, $signed(y));
    end
  endtask
  initial begin
    t(4'b0111, 4'b0001, 2'b10, "ADD");   //  7 + 1: signed overflow
    t(4'b1111, 4'b0001, 2'b10, "ADD");   // -1 + 1: carry, no overflow
    t(4'b0011, 4'b0101, 2'b11, "SUB");   //  3 - 5 = -2: borrow, so C = 0
    t(4'b0101, 4'b0101, 2'b11, "SUB");   //  5 - 5 = 0: Z = 1, C = 1
    t(4'b1000, 4'b0001, 2'b11, "SUB");   // -8 - 1: signed overflow
    t(4'b1100, 4'b1010, 2'b00, "AND");
  end
endmodule
```

```text {filename="Simulation output (Icarus Verilog 12, -g2012)"}
ADD 0111, 0001 -> 1000  Z=0 N=1 C=0 V=1  (signed -8)
ADD 1111, 0001 -> 0000  Z=1 N=0 C=1 V=0  (signed 0)
SUB 0011, 0101 -> 1110  Z=0 N=1 C=0 V=0  (signed -2)
SUB 0101, 0101 -> 0000  Z=1 N=0 C=1 V=0  (signed 0)
SUB 1000, 0001 -> 0111  Z=0 N=0 C=1 V=1  (signed 7)
AND 1100, 1010 -> 1000  Z=0 N=1 C=0 V=0  (signed -8)
```

<div class="nb nb-remark" id="remark-3-6-1">

<strong>Remark 3.6.1</strong> — The fourth and fifth lines are the classic pair: $5 - 5$ gives $Z = 1$ with $C = 1$ (no borrow), and $-8 - 1$ overflows to $+7$ ($V = 1$) although unsigned $8 - 1 = 7$ is fine ($C = 1$). The ALU computes one bit pattern; the flags give both interpretations.

</div>

<div class="nb nb-moral">

Every block in this chapter is a mux, a decoder or an adder in disguise; the ALU is all three wired together under a few control lines.

</div>
