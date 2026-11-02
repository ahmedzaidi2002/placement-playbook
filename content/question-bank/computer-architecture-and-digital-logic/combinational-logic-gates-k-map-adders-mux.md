---
title: "Combinational logic (gates, K-map, adders, MUX)"
weight: 1
---

52 questions asked by Qualcomm, Texas Instruments. Try each one first, then open the toggle: it gives the answer, why it is right, and the idea behind it explained from scratch.

### 1 · Q22, Boolean reduction

*Asked by: Qualcomm (IISc)*

Which option is the reduced form of $(AR + SP) + (AR)'$?

- **(a)** $AR' + SP$
- **(b)** 0
- **(c)** 1
- **(d)** $AR$

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) 1**

**Why.** Let X = AR. Then X + X′ = 1 (complement law), and 1 + SP = 1 (anything OR 1 is 1).

**Concept: spot the complement pair.** Treat a repeated sub-expression as a single variable; X + X′ = 1 and X·X′ = 0 collapse expressions instantly.

{{< /details >}}

### 2 · Q33, logic gates

*Asked by: Qualcomm (IISc)*

Which is correct about logic gates? (I) TTL (Transistor-Transistor Logic) is a type of logic
gate. (II) The logic state of a terminal can never change.

- **(a)** Only (II)
- **(b)** Both (I) and (II)
- **(c)** Neither (I) nor (II)
- **(d)** Only (I)

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) only (I)** (the intended answer)

**Why.** TTL is a logic family, a technology for building gates (strictly not a "type of gate", but that is the intended reading). (II) is plainly false: changing logic states is what digital circuits do.

**Concept: logic families.** TTL (bipolar transistors), CMOS (complementary MOSFETs, dominant today), ECL (very fast, power-hungry). They differ in speed, power, noise margin and fan-out.

{{< /details >}}

### 3 · Q23, intersection law in Boolean logic

*Asked by: Qualcomm (HirePro, Aug 2025)*

Which equation(s) are correct for the intersection law in Boolean logic?
I) $P \cdot 1 = 0$. II) $P \cdot 1 = P$. III) $P \cdot 0 = P$. IV) $P \cdot 0 = 0$.

- **(a)** Only (II)
- **(b)** Only (III)
- **(c)** Only (II) and (IV)
- **(d)** Only (I) and (IV)

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) (II) and (IV)**

**Why.** For AND, 1 is the identity (P·1 = P) and 0 is the annihilator (P·0 = 0).

**Concept: identity and null laws.** AND: P·1 = P, P·0 = 0. OR: P + 0 = P, P + 1 = 1. These are the Boolean counterparts of multiplying by 1 and 0.

{{< /details >}}

### 4 · Q28, gates in an LSI package

*Asked by: Qualcomm (HirePro, Aug 2025)*

The number of logic gates contained in a single LSI IC package is:

- **(a)** More than 100
- **(b)** 50
- **(c)** 10
- **(d)** Less than 100

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) more than 100**

**Why.** Integration scales: SSI (fewer than about 12 gates), MSI (12–99), LSI (100 to about 10,000), VLSI (more).

**Concept: integration levels** track how many gates fit on one chip; modern processors are far beyond VLSI, with billions of transistors.

{{< /details >}}

### 5 · Computer Architecture

*Asked by: Qualcomm (60-question online assessment)*

Which one of the given logic gates has the output as 1 only if one of the input is 1?

- **(a)** NOR
- **(b)** EXOR
- **(c)** NOT
- **(d)** EXNOR

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) EXOR**

**Why.** XOR outputs 1 when exactly one input is 1 (the inputs differ) and 0 when both are 0 or both are 1.

**Concept: XOR uses.** Parity checking, adders (the sum bit is A ⊕ B ⊕ C_in), comparators (A ⊕ B = 0 means equal), and controlled inversion (A ⊕ 1 = A′).

{{< /details >}}

### 6 · Computer Architecture

*Asked by: Qualcomm (60-question online assessment)*

Which one of the given options is the correct form after simplifying the expression given below? B'D + BC'D + C'D

- **(a)** `B'D + C'D`
- **(b)** `B' + C'D`
- **(c)** `B' + B + C'`
- **(d)** `BD + C'D`

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) B′D + C′D**

**Why.** BC′D + C′D = C′D(B + 1) = C′D (absorption). So the expression becomes B′D + C′D.

**Concept: absorption law.** X + XY = X: if the bigger term is true, the smaller one adds nothing. Factor out common parts to see it.

{{< /details >}}

### 7 · Boolean algebra and gates

*Asked by: Qualcomm (2025 paper (campus not named), Q26)*

AB + AB′ + A′C + AC is independent of which variable?

- **(a)** A
- **(b)** AC
- **(c)** B
- **(d)** C

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) B**

**Why.** AB + AB′ = A(B + B′) = A, and A′C + AC = C(A′ + A) = C. The expression is A + C, so B has no effect.

**Concept: combining adjacent terms.** XY + XY′ = X: two terms that differ in one variable merge (this is exactly what grouping in a K-map does).

{{< /details >}}

### 8 · Boolean algebra and gates

*Asked by: Qualcomm (2025 paper (campus not named), Q21)*

Reduce (P + Q)·(P + Q).

- **(a)** PQ + 1
- **(b)** PQ
- **(c)** P
- **(d)** P + Q

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) P + Q**

**Why.** Idempotent law: X·X = X, with X = P + Q.

**Concept: idempotence.** X·X = X and X + X = X: repeating an input changes nothing.

{{< /details >}}

### 9 · Boolean algebra and gates

*Asked by: Qualcomm (BITS Hyderabad 2025, Q54)*

Which one of the given options is the correct reduction of (P′ + R)·R?

- **(a)** P′ + R
- **(b)** R·(1 + P′)
- **(c)** P′R + 1
- **(d)** P′·R

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) R·(1 + P′)** (which equals R)

**Why.** (P′ + R)·R = P′R + R·R = P′R + R = R(P′ + 1) = R. Only option (b) equals R; it is the step just before simplifying 1 + P′ to 1.

**Concept: absorption in product form.** (X + Y)·Y = Y, the dual of X·Y + Y = Y.

{{< /details >}}

### 10 · Boolean algebra and gates

*Asked by: Qualcomm (NIT Durgapur)*

Which one of the given options is the correct reduction of HT + HTC?

- **(a)** 1
- **(b)** H
- **(c)** HT
- **(d)** HTC

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) HT**

**Why.** Absorption with X = HT: HT + HT·C = HT(1 + C) = HT.

**Concept: absorption law** X + XY = X.

{{< /details >}}

### 11 · Boolean algebra and gates

*Asked by: Qualcomm (2025 paper (campus not named), Q24)*

Which of the following are examples of associative rules in Boolean algebra?

I. (X + Y) + Z = X + (Y + Z)  
II. X + Y = Y + X

- **(a)** Both (I) and (II)
- **(b)** Only (I)
- **(c)** Neither (I) nor (II)
- **(d)** Only (II)

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) only (I)**

**Why.** (I) regroups the operands, (X + Y) + Z = X + (Y + Z): associative. (II) swaps their order: commutative.

**Concept: associative vs commutative.** Associative: grouping doesn't matter. Commutative: order doesn't matter. Both hold for AND and OR (and XOR).

{{< /details >}}

### 12 · Boolean algebra and gates

*Asked by: Qualcomm (IISc 2024, Q41)*

Which one of the operations given in the options is incorrect?

- **(a)** X · 1 = X
- **(b)** X + 0 = X
- **(c)** X + 1 = X
- **(d)** X · 0 = 0

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) X + 1 = X** is incorrect

**Why.** X + 1 = 1 (dominance/null law): OR with 1 is always 1.

**Concept: null laws.** X + 1 = 1 and X·0 = 0.

{{< /details >}}

### 13 · Boolean algebra and gates

*Asked by: Qualcomm (BITS Hyderabad 2024, Q23)*

Which one of the gates given in the options can be used as a 2-input NOT gate when one input amongst the two is set to the constant 1?

- **(a)** NOR gate
- **(b)** NAND gate
- **(c)** OR gate
- **(d)** EXNOR gate

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) NAND**

**Why.** NAND(A, 1) = (A·1)′ = A′. EXNOR with 1 gives A; NOR with 1 gives 0. (XOR with 1 would also invert, but it isn't offered.)

**Concept: universal gates.** NAND alone (or NOR alone) can build any logic function: NOT (tie inputs or set one to 1), AND (NAND + NOT), OR (NOTs on inputs, then NAND).

{{< /details >}}

### 14 · Boolean algebra and gates

*Asked by: Qualcomm (IISc 2024, Q54)*

Which logic gate gives an output that is LOW if and only if all the inputs are HIGH?

- **(a)** EXNOR
- **(b)** AND
- **(c)** NAND
- **(d)** OR

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) NAND**

**Why.** NAND outputs 0 only when every input is 1, and 1 otherwise.

**Concept: NAND truth table** = inverted AND.

{{< /details >}}

### 15 · Boolean algebra and gates

*Asked by: Qualcomm (IIIT Delhi 2025, Q21)*

Consider the truth table below. Which one of the given options corresponds to it?

| A | B | Y |
|:-:|:-:|:-:|
| 0 | 0 | 1 |
| 0 | 1 | 0 |
| 1 | 0 | 0 |
| 1 | 1 | 1 |

- **(a)** EXNOR
- **(b)** NOT
- **(c)** NAND
- **(d)** AND

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) EXNOR**

**Why.** The output is 1 exactly when the inputs are equal (00 or 11): XNOR, also called equivalence.

**Concept: XNOR = NOT XOR** = A·B + A′·B′. Used as a 1-bit equality comparator.

{{< /details >}}

### 16 · Boolean algebra and gates

*Asked by: Qualcomm (BITS Hyderabad 2024, Q40)*

If a logic gate has three inputs, how many input states (combinations) are there?

- **(a)** 2
- **(b)** 8
- **(c)** 4
- **(d)** 6

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) 8**

**Why.** Each input can be 0 or 1: 2 × 2 × 2 = 2³ = 8 combinations.

**Concept: truth table size.** n inputs → 2ⁿ rows.

{{< /details >}}

### 17 · Boolean algebra and gates

*Asked by: Qualcomm (BITS Hyderabad 2024, Q24)*

Consider block X in the figure: one data input, several outputs and control (select) lines. X is:

I. a multiplexer  
II. an encoder  
III. a demultiplexer

<figure class="nb-fig"><img src="/companies/qualcomm/core/demux-block.svg" alt="Figure for question 17" loading="lazy"></figure>

- **(a)** Only (I) and (II)
- **(b)** Only (II)
- **(c)** Only (III)
- **(d)** Only (I)

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) only (III), a demultiplexer**

**Why.** One data input routed to one of several outputs by select lines is a demultiplexer. A multiplexer is the reverse (many inputs, one output); an encoder has many inputs and no select lines.

**Concept: MUX vs DEMUX vs decoder vs encoder.** MUX: select one of 2ⁿ inputs. DEMUX: send one input to one of 2ⁿ outputs. Decoder: n-bit code → one active output of 2ⁿ (a DEMUX with input fixed at 1). Encoder: the reverse.

{{< /details >}}

### 18 · Boolean algebra and gates

*Asked by: Qualcomm (BITS Hyderabad 2024, Q34)*

A full adder can be converted into a full subtractor by adding one:

- **(a)** AND gate
- **(b)** Inverter
- **(c)** NOR gate
- **(d)** OR gate

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) an inverter**

**Why.** The difference bit of a full subtractor is the same 3-input XOR as the full adder's sum. The borrow is B_out = A′B + A′B_in + B·B_in, which is the adder's carry formula with A complemented. So one inverter on A (for the borrow path) converts it.

**Concept: subtraction via addition.** In two's complement, A − B = A + B′ + 1, so adders become subtractors with inverters on one input and carry-in = 1.

{{< /details >}}

### 19 · Boolean algebra

*Asked by: Qualcomm (BITS Goa 2024, Q46)*

Simplify Y = (A + B′ + C′)(A + B′ + C).

- **(a)** A + B
- **(b)** A′ + B
- **(c)** A + B′
- **(d)** A′ + B′

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) A + B′**

**Why.** Let X = A + B′. Then (X + C′)(X + C) = X + CC′ = X + 0 = X.

**Concept: distributive law (product of sums).** (X + Y)(X + Z) = X + YZ, the "OR distributes over AND" law that has no counterpart in ordinary arithmetic.

{{< /details >}}

### 20 · Boolean algebra

*Asked by: Qualcomm (BITS Hyderabad 2025, Q53)*

What is the minimum number of gates needed to implement X + X′Y?

- **(a)** One OR and one NAND
- **(b)** One OR and one NOR
- **(c)** One OR gate
- **(d)** One OR, one AND and one inverter

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) one OR gate**

**Why.** X + X′Y = (X + X′)(X + Y) = 1·(X + Y) = X + Y.

**Concept: redundancy law.** X + X′Y = X + Y: if X is false, X′ is true anyway, so the X′ factor adds nothing.

{{< /details >}}

### 21 · Boolean algebra

*Asked by: Qualcomm (IISc 2024, Q55)*

F = (A + CDA′)B + (D′ + C′D)BA′. What is the simplified expression?

- **(a)** B
- **(b)** A + C + D
- **(c)** AB
- **(d)** C

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) B**

**Why.** First term: (A + A′CD)B = AB + A′BCD. Second: D′ + C′D = D′ + C′, so it gives A′B(C′ + D′). Since C′ + D′ = (CD)′, F = AB + A′B[CD + (CD)′] = AB + A′B = B.

**Concept: spot a complementary pair inside.** CD and (CD)′ add to 1, which collapses the bracket; then AB + A′B = B.

{{< /details >}}

### 22 · Boolean algebra

*Asked by: Qualcomm (2025 paper (campus not named), Q55)*

Find the complement of Y = A′B′C + AC + (A′B′ + BC).

- **(a)** (A + B′ + C′)(A′ + C)(A′ + B′)(B′ + C)
- **(b)** (A + B + C′)(A + C)(A′ + B′)(B + C)
- **(c)** (A′ + B′ + C′)(A + C)(A + B)(B′ + C′)
- **(d)** (A + B + C′)(A′ + C′)(A + B)(B′ + C′)

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) (A + B + C′)(A′ + C′)(A + B)(B′ + C′)**

**Why.** De Morgan turns the complement of an OR of terms into the AND of each term's complement: (A′B′C)′ = A + B + C′, (AC)′ = A′ + C′, (A′B′)′ = A + B, (BC)′ = B′ + C′.

**Concept: De Morgan's laws.** (X + Y)′ = X′Y′ and (XY)′ = X′ + Y′. To complement any expression: swap AND/OR and complement every literal.

{{< /details >}}

### 23 · Boolean algebra

*Asked by: Qualcomm (BITS Goa 2024, Q44)*

Which of the following expressions resembles (AB + A′(A + B))(A + B)(A + C)?

- **(a)** (C′ + A′B′)′
- **(b)** ((A′ + B′)(A′ + C′)(B′ + C′))′
- **(c)** (C′(A′ + B))′
- **(d)** (A′ + B′C′)′

{{< details title="Answer and explanation" closed="true" >}}

**Answer: no reliable pick** (no option equals the simplified expression AB + BC)

**Why.** A′(A + B) = A′B, so AB + A′B = B. Then B(A + B) = B and B(A + C) = AB + BC. The options expand to AC + BC, AB + AC + BC, C + AB′ and AB + AC; none is AB + BC. The question looks misprinted.

**Concept: check by expanding.** When options are given in complemented forms, expand each with De Morgan into sum-of-products and compare with your simplified answer.

{{< /details >}}

### 24 · Boolean algebra

*Asked by: Qualcomm (IISc 2024, Q58)*

If X = f(A, B, C, D) = Σ(1, 2, 4, 7, 8, 11, 13, 14) and Y(A, B, C, D) = Π(3, 5, 7, 8, 10, 11, 12, 13), then the expressions for X and Y respectively are:

- **(a)** A⊕B⊕C⊕D and A′⊕B′⊕C′⊕D′
- **(b)** A⊕B⊕C′⊕D and (A′+C+D′)(B′+C+D′)(A′+C+D)(A′+B′+C′)
- **(c)** ABCD and A⊕B⊕C⊕D
- **(d)** A⊕B⊕C⊕D and (A+C′+D′)(B′+C+D′)(A′+C+D)(A′+B+C′)

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d)**

**Why.** X's minterms (1, 2, 4, 7, 8, 11, 13, 14) are exactly the 4-bit numbers with an odd number of 1s, so X = A ⊕ B ⊕ C ⊕ D. For Y, group its zeros (maxterms 3, 5, 7, 8, 10, 11, 12, 13) on a K-map: 0-11 → (A + C′ + D′), -101 → (B′ + C + D′), 1-00 → (A′ + C + D), 101- → (A′ + B + C′). That is option (d).

**Concept: parity functions and POS from a K-map.** XOR of all inputs = 1 for an odd number of 1s (checkerboard K-map, cannot be simplified). For product-of-sums, group the 0s; each group gives a sum term with variables complemented where they are 1.

{{< /details >}}

### 25 · Boolean algebra

*Asked by: Qualcomm (BITS Goa 2024, Q55)*

How many entries does the truth table of a four-input circuit have?

- **(a)** 12
- **(b)** 8
- **(c)** 16
- **(d)** 4

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) 16**

**Why.** 2⁴ = 16 input combinations, one row each.

**Concept: truth table size** = 2ⁿ for n inputs.

{{< /details >}}

### 26 · Gates and combinational circuits

*Asked by: Qualcomm (BITS Hyderabad 2024, Q42)*

In the circuit below (redrawn from the photo), which input combination makes the output F logic 1?

<figure class="nb-fig"><img src="/companies/qualcomm/core/gates-p1q42.svg" alt="Figure for question 26" loading="lazy"></figure>

- **(a)** A = 0, B = 0, C = 1
- **(b)** A = 0, B = 0, C = 0
- **(c)** A = 0, B = 1, C = 1
- **(d)** A = 1, B = 1, C = 1

{{< details title="Answer and explanation" closed="true" >}}

**Answer: no reliable pick** (the photo is blurred around G7; as read, every option gives F = 1; if G7 is a two-input gate, only A = B = C = 0 works, probably the intended answer)

**Why.** As read: F = XNOR(G7, C) with G7 = XNOR(G5, G6, C), so the C terms cancel and F = G5 ⊕ G6. With G5 = A + G4 and G6 = XNOR(A, G4): A = 0 gives F = G4 ⊕ G4′ = 1, and A = 1 gives F = G4′; for A = B = C = 1, G4 = 0, so F = 1 again.

**Concept: work backwards and simplify XOR chains.** XNOR(X, C) = X ⊕ C′; two appearances of the same signal in an XOR chain cancel (C ⊕ C = 0).

{{< /details >}}

### 27 · Gates and combinational circuits

*Asked by: Qualcomm (BITS Hyderabad 2025, Q47)*

For the NMOS circuit shown, what is Z?

<figure class="nb-fig"><img src="/companies/qualcomm/core/nmos-nand.svg" alt="Figure for question 27" loading="lazy"></figure>

- **(a)** (AB)
- **(b)** (A + B)
- **(c)** (A + B)′
- **(d)** (AB)′

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) (AB)′**

**Why.** Z is pulled to ground only when both series transistors conduct (A = B = 1); otherwise the resistor pulls Z high. Output 0 only for A = B = 1: NAND.

**Concept: MOS logic structure.** Series pull-down transistors give NAND (all must be on); parallel pull-downs give NOR (any one is enough).

{{< /details >}}

### 28 · Gates and combinational circuits

*Asked by: Qualcomm (Delhi campus 2024, Q55)*

What function does this NAND-only circuit implement?

<figure class="nb-fig"><img src="/companies/qualcomm/core/nand-or.svg" alt="Figure for question 28" loading="lazy"></figure>

- **(a)** A + B
- **(b)** AB
- **(c)** (AB)′ + (AB)′
- **(d)** A′ + B′

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) A + B**

**Why.** The first two NANDs have their inputs tied together, so they act as inverters: A′ and B′. The last NAND gives (A′B′)′ = A + B by De Morgan.

**Concept: OR from NANDs.** Invert the inputs, then NAND: (A′·B′)′ = A + B. Three NAND gates make an OR.

{{< /details >}}

### 29 · Gates and combinational circuits

*Asked by: Qualcomm (Delhi campus 2024, Q59)*

Find the output Y of the given circuit.

<figure class="nb-fig"><img src="/companies/qualcomm/core/gates-p4q59.svg" alt="Figure for question 29" loading="lazy"></figure>

- **(a)** A + B
- **(b)** A′ + B′
- **(c)** A + B′
- **(d)** A′ + B

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) A + B**

**Why.** Y = [(A + B)′ · (BC)′]′ = (A + B) + BC (De Morgan) = A + B (absorption: B + BC = B).

**Concept: De Morgan then absorption.** Remove the outer bar first, then simplify.

{{< /details >}}

### 30 · Gates and combinational circuits

*Asked by: Qualcomm (IIIT Delhi 2025, Q55)*

In the combinational circuit shown, the inputs are A = 1 and B = 0. Determine the value of Q.

<figure class="nb-fig"><img src="/companies/qualcomm/core/gates-p5q55.svg" alt="Figure for question 30" loading="lazy"></figure>

- **(a)** Output Q = 1 if we change inputs to A = 0 and B = 1
- **(b)** Output Q = 0
- **(c)** Output Q = 1
- **(d)** None of the above

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) Q = 0** (for every input, so (a) is false too)

**Why.** G1·G3 = (A ⊕ B)·AB = 0 always (if A and B differ, AB = 0), so the upper NAND is always 1. G3·G5 = AB·(A + B)′ = 0 always, so the lower NAND is always 1. Q = 1 ⊕ 1 = 0.

**Concept: look for terms that can never be true together.** A product of mutually exclusive conditions is identically 0, which fixes downstream gates regardless of inputs.

{{< /details >}}

### 31 · Gates and combinational circuits

*Asked by: Qualcomm (IISc 2024, Q50)*

Consider the figure. What is the only word (ABC) it disregards, i.e. gives Y = 0?

<figure class="nb-fig"><img src="/companies/qualcomm/core/or-of-inverted.svg" alt="Figure for question 31" loading="lazy"></figure>

- **(a)** 100
- **(b)** 101
- **(c)** 000
- **(d)** 111

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) 111**

**Why.** The circuit computes Y = A′ + B′ + C′ = (ABC)′, which is 0 only when A = B = C = 1.

**Concept: OR of inverted inputs = NAND** (De Morgan).

{{< /details >}}

### 32 · Gates and combinational circuits

*Asked by: Qualcomm (2025 paper (campus not named), Q42)*

What is the minimum number of NOR gates needed to realise Y = [A · (B · (C · D′)′)′]′ (bars over ABCD′, BCD′, CD′ and D)?

- **(a)** 4 two-input NOR and 2 four-input NOR
- **(b)** 3 two-input NOR and 2 four-input NOR
- **(c)** 4 two-input NOR and 1 four-input NOR
- **(d)** 3 two-input NOR and 1 four-input NOR

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) four two-input NORs and one four-input NOR**

**Why.** Peel the bars from inside: (CD′)′ = C′ + D, so (B(C′ + D))′ = B′ + CD′, and Y = A′ + B(C′ + D) = (A′ + B)(A′ + C′ + D). A product of sums maps to NOR–NOR: Y = NOR(NOR(A′, B), NOR(A′, C′, D)). That needs two NORs as inverters (for A′ and C′), NOR(A′, B) and the output NOR (four two-input NORs), plus one four-input NOR (one input tied low) for the three-literal sum.

**Concept: NOR–NOR = product of sums.** A POS expression (X)(Y) = ((X)′ + (Y)′)′ becomes two levels of NOR gates, just as SOP becomes NAND–NAND.

{{< /details >}}

### 33 · Gates and combinational circuits

*Asked by: Qualcomm (BITS Hyderabad 2024, Q54)*

The circuit-level design using inverters and tri-state buffers shown below can be used as a:

<figure class="nb-fig"><img src="/companies/qualcomm/core/tristate-mux.svg" alt="Figure for question 33" loading="lazy"></figure>

- **(a)** Half adder
- **(b)** 2:1 multiplexer
- **(c)** Full adder
- **(d)** D flip-flop

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) 2:1 multiplexer**

**Why.** X enables the In1 buffer and X′ enables the In0 buffer, so exactly one input drives the shared output: Out = X·In1 + X′·In0.

**Concept: tri-state buffers.** Output is the input when enabled, and high-impedance (disconnected) when not. Several can share one wire as long as only one is enabled at a time: the basis of buses.

{{< /details >}}

### 34 · Multiplexers and decoders

*Asked by: Qualcomm (IIIT Delhi 2025, Q54)*

How can a 2:1 MUX be used as a NOT gate?

- **(a)** D₀ = input, D₁ = 1, select line = 0
- **(b)** D₀ = 1, D₁ = 0, select line = input
- **(c)** D₀ = 1, D₁ = input, select line = 1
- **(d)** D₀ = 0, D₁ = 0, select line = input

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) D₀ = 1, D₁ = 0, select = input**

**Why.** A 2:1 MUX gives Y = S′D₀ + SD₁ = S′·1 + S·0 = S′.

**Concept: MUX as a universal block.** A 2ⁿ:1 MUX can implement any function of n variables by putting the variables on the select lines and the truth-table outputs on the data inputs.

{{< /details >}}

### 35 · Multiplexers and decoders

*Asked by: Qualcomm (Delhi campus 2024, Q56)*

For the 4:1 MUX shown (I₀ = 1, I₁ = 0, I₂ = 0, I₃ = 1, S₁ = A, S₀ = B), what is f?

<figure class="nb-fig"><img src="/companies/qualcomm/core/mux4.svg" alt="Figure for question 35" loading="lazy"></figure>

- **(a)** A′B + A
- **(b)** A′B + AB′
- **(c)** AB
- **(d)** AB + A′B′

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) AB + A′B′**

**Why.** f = A′B′·I₀ + A′B·I₁ + AB′·I₂ + AB·I₃ = A′B′·1 + 0 + 0 + AB·1 = A′B′ + AB (XNOR).

**Concept: MUX output formula.** Each data input is ANDed with the minterm of its select code; the output ORs them all.

{{< /details >}}

### 36 · Multiplexers and decoders

*Asked by: Qualcomm (IISc 2024, Q53)*

A 4:1 MUX has D₀ = x and D₁ = D₂ = D₃ = 1, with select lines S₁ = B and S₀ = A. What is the output? Now D₀ and D₁ are given x, while D₂ and D₃ are given x′. What is the new output?

- **(a)** A ⊕ x and A ⊕ x
- **(b)** A + B + x and A + x
- **(c)** A + B + x and B ⊕ x
- **(d)** A + B + x and A ⊕ x

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) A + B + x and B ⊕ x**

**Why.** First: Y = A′B′x + A′B + AB′ + AB = A′B′x + (A + B) = A + B + x (redundancy law). Second: the inputs depend only on S₁ = B (x when B = 0, x′ when B = 1), so Y = B′x + Bx′ = B ⊕ x.

**Concept: MUX with a variable on the data inputs.** Putting a variable (or its complement) on data lines lets a 4:1 MUX implement functions of 3 variables.

{{< /details >}}

### 37 · Multiplexers and decoders

*Asked by: Qualcomm (2025 paper (campus not named), Q49)*

For the given 74LS139 decoder circuit, what is Y?

<figure class="nb-fig"><img src="/companies/qualcomm/core/decoder-xor.svg" alt="Figure for question 37" loading="lazy"></figure>

- **(a)** A NOR B
- **(b)** A XOR B
- **(c)** A OR B
- **(d)** A NAND B

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) A XOR B**

**Why.** The 74LS139's outputs are active-low: Y0 = m₀′, Y3 = m₃′. The input bubbles on the gate invert them back, the OR gives m₀ + m₃ = A′B′ + AB (XNOR), and the output bubble inverts that: Y = A ⊕ B.

**Concept: active-low signals.** A bubble means inversion. Matching bubbles cancel (a bubble output into a bubble input), which is how active-low decoders combine neatly with NAND gates.

{{< /details >}}

### 38 · Multiplexers and decoders

*Asked by: Qualcomm (Delhi campus 2024, Q46)*

A 5:32 decoder is to be designed. The engineer is provided with one 2:4 decoder and N 3:8 decoders. What is N?

- **(a)** 2
- **(b)** 8
- **(c)** 5
- **(d)** 4

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) 4**

**Why.** The two MSBs go to the 2:4 decoder, whose four outputs enable four 3:8 decoders, each driven by the three LSBs: 4 × 8 = 32 outputs.

**Concept: decoder trees.** Larger decoders are built hierarchically: the high bits choose which smaller decoder is enabled, the low bits choose the output within it.

{{< /details >}}

### 39 · Arithmetic circuits

*Asked by: Qualcomm (IIIT Delhi 2025, Q41)*

Calculate the minimum number of NAND gates required to implement a three-bit magnitude comparator having one output that goes HIGH when the two three-bit numbers are equal.

- **(a)** 17
- **(b)** 16
- **(c)** 14
- **(d)** 15

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) 17**

**Why.** Equality: E = (A₂ ⊙ B₂)(A₁ ⊙ B₁)(A₀ ⊙ B₀). Each XNOR costs 5 NANDs (4 for an XOR + 1 to invert): 15. The 3-input AND = a 3-input NAND + an inverting NAND: 2. Total 17. (Counts vary slightly with the XOR form used; 17 is the standard textbook count.)

**Concept: equality comparators.** Two numbers are equal when every pair of bits is equal: AND of the bitwise XNORs.

{{< /details >}}

### 40 · Programmable logic

*Asked by: Qualcomm (2025 paper (campus not named), Q56)*

A 4-bit BCD adder is implemented in a programmable ROM, and a control input switches it to a subtractor. What ROM size is needed?

- **(a)** 1K × 8
- **(b)** 1K × 5
- **(c)** 32K
- **(d)** 4K × 4

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) 1K × 5**

**Why.** Address inputs: two 4-bit digits (8) + carry/borrow in (1) + the add/subtract control (1) = 10 bits → 2¹⁰ = 1K words. Outputs: the 4-bit result digit + carry/borrow out = 5 bits.

**Concept: ROM as a lookup table.** Any combinational function can be stored in a ROM: inputs become the address, outputs the stored word. Size = 2^(inputs) × (outputs).

{{< /details >}}

### 41 · Programmable logic

*Asked by: Qualcomm (BITS Hyderabad 2025, Q44)*

For the PLA shown, what is the value of F?

<figure class="nb-fig"><img src="/companies/qualcomm/core/pla-or.svg" alt="Figure for question 41" loading="lazy"></figure>

- **(a)** A
- **(b)** ABC′
- **(c)** B
- **(d)** AB′

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) B**

**Why.** The OR line collects the product lines ABC, A′B and ABC′. ABC + ABC′ = AB(C + C′) = AB, and AB + A′B = B(A + A′) = B.

**Concept: PLA.** A programmable logic array has a programmable AND plane (makes product terms) feeding a programmable OR plane (sums them). Read each product line from its crosses, then simplify the sum.

{{< /details >}}

### 42 · Programmable logic

*Asked by: Qualcomm (IIIT Delhi 2025, Q59)*

What is the value of the function F1 (A = MSB, C = LSB) in the PLA shown?

<figure class="nb-fig"><img src="/companies/qualcomm/core/pla-minterms.svg" alt="Figure for question 42" loading="lazy"></figure>

- **(a)** F1 = Σ(1, 4, 7)
- **(b)** F1 = Σ(0, 3, 7)
- **(c)** F1 = Π(0, 2)
- **(d)** (fourth option not visible in the photo)

{{< details title="Answer and explanation" closed="true" >}}

**Answer: no reliable pick** (the correct value Σ(0, 2) = A′C′ is not among the three visible options; pick the fourth if it reads Σ(0, 2))

**Why.** The eight AND rows are the minterms m₀…m₇ in order (row 1 taps A′, B′, C′; row 2 taps A′, B′, C; ...). F1's OR line has crosses on rows m₀ and m₂, so F1 = Σ(0, 2) = A′B′C′ + A′BC′ = A′C′. Σ(1, 4, 7) is F2, and Π(0, 2) is the complement of the right answer.

**Concept: minterm notation.** Σ(list) = OR of the minterms whose numbers (ABC read as binary) are listed. Π(list) = AND of maxterms: the function is 0 exactly at those numbers.

{{< /details >}}

### 43 · Programmable logic

*Asked by: Qualcomm (Delhi campus 2024)*

For a CPLD (complex programmable logic device), the status of the AND array and the OR array will be:

- **(a)** Programmable AND array and fixed OR array
- **(b)** Fixed AND array and fixed OR array
- **(c)** Fixed AND array and programmable OR array
- **(d)** Programmable AND array and programmable OR array

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) programmable AND array, fixed OR array**

**Why.** A CPLD is built from PAL-style macrocells: a programmable AND array feeding fixed OR gates. Both programmable is a PLA; fixed AND with programmable OR is a PROM.

**Concept: programmable logic families.** PROM (fixed AND = full decoder, programmable OR), PAL (programmable AND, fixed OR), PLA (both programmable), CPLD (many PAL blocks + interconnect), FPGA (lookup tables + flip-flops + routing).

{{< /details >}}

### 44 · product of maxterms

*Asked by: Texas Instruments (IISc 2023)*

$f = \prod M(0,1,3,4,5,7,9,11,12,13,14,15)$. Which is equivalent?

- **(a)** (A+C'+D)(A'+B+D)
- **(b)** AC'D + A'BD
- **(c)** A'CD' + AB'CD' + AB'C'D'
- **(d)** (B+C'+D)(A+B'+C'+D)(A'+B+C+D)

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) A′CD′ + AB′CD′ + AB′C′D′**

**Why.** The maxterms list where f = 0, so f = 1 at the missing numbers: 2, 6, 8, 10. A′CD′ covers 0010 and 0110 (2, 6); AB′CD′ is 1010 (10); AB′C′D′ is 1000 (8). (Checked on all 16 inputs; the candidate's (a) is wrong.)

**Concept: switching between Σ and Π.** ΠM(list) = Σm(everything not in the list). Writing the function from its few 1s is often easier.

{{< /details >}}

### 45 · simplify AB + AC' + BC

*Asked by: Texas Instruments (IISc 2023)*

Simplify $AB + AC' + BC$.

{{< details title="Answer and explanation" closed="true" >}}

**Answer: AC′ + BC**

**Why.** AB is the consensus of AC′ and BC (they disagree only on C; the consensus is the product of the rest, A·B). Whenever AB = 1, either C = 0 (so AC′ = 1) or C = 1 (so BC = 1), so AB is redundant.

**Concept: consensus theorem.** XY + X′Z + YZ = XY + X′Z. The term YZ is covered by the other two and can be dropped. Here X = C′, Y = A, Z = B: C′A + CB + AB = C′A + CB.

{{< /details >}}

### 46 · 1-to-8 demultiplexer

*Asked by: Texas Instruments (IISc 2023)*

Output $O_4$ of a 1-to-8 demultiplexer with selects $S_2 S_1 S_0$?

{{< details title="Answer and explanation" closed="true" >}}

**Answer: O₄ = S₂ S₁′ S₀′ · Input**

**Why.** Output 4 is active when the select code is 4 = 100: S₂ = 1, S₁ = 0, S₀ = 0. It then passes the input.

**Concept: DEMUX outputs.** Output k = (minterm k of the select lines) AND the data input.

{{< /details >}}

### 47 · hazards

*Asked by: Texas Instruments (IISc 2023)*

Does $Z = A + B' + C$ have hazards or races?

{{< details title="Answer and explanation" closed="true" >}}

**Answer: hazard-free, with no races**

**Why.** Z = A + B′ + C is a single OR of literals: no variable appears in both its true and complemented form, so no input change can make two terms hand over to each other (no static hazard). It is combinational with no feedback, so there are no races.

**Concept: static hazards.** A glitch can occur when an output should stay 1 while one term turns off and another turns on, e.g. AB + A′C when B = C = 1 and A changes. The fix is adding the consensus term (BC).

{{< /details >}}

### 48 · what keeps a latch latched?

*Asked by: Texas Instruments (NIT Calicut 2023)*

A latch is built from NAND and NOR gates. Which condition keeps it in the latched state?

- **(a)** Low input voltages
- **(b)** Synchronous operation
- **(c)** Gate impedance
- **(d)** Cross-coupling

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) cross-coupling**

**Why.** In a latch, each gate's output feeds the other gate's input. This positive feedback loop holds the state after the inputs return to their resting values.

**Concept: storage from feedback.** Two cross-coupled NOR (or NAND) gates form an SR latch with two stable states: the basic one-bit memory cell.

{{< /details >}}

### 49 · dual-edge storage from MUXes

*Asked by: Texas Instruments (NIT Calicut 2023)*

Store data on both clock edges using only MUXes. How many?

- **(a)** 2
- **(b)** 3
- **(c)** 4
- **(d)** 5

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) 3**

**Why.** A MUX with its output fed back to one input is a latch. Use two such MUX latches, one transparent while the clock is high and one while it is low, and a third MUX, selected by the clock, to output whichever latch is currently holding.

**Concept: dual-edge flip-flops.** Data is captured on both clock edges, doubling data rate at the same clock frequency (the idea behind DDR memory).

{{< /details >}}

### 50 · an equivalent function

*Asked by: Texas Instruments (NIT Calicut 2023)*

Which is equal to $f = [(x y') + (x' y)]'$?

{{< details title="Answer and explanation" closed="true" >}}

**Answer: f is XNOR: (x + y′)(x′ + y), equivalently xy + x′y′** (the primes in the options are too blurred to pick a letter)

**Why.** xy′ + x′y is XOR; its complement is XNOR. By De Morgan, (xy′ + x′y)′ = (x′ + y)(x + y′).

**Concept: XNOR forms.** XNOR = xy + x′y′ (sum of products) = (x + y′)(x′ + y) (product of sums). 1 when the inputs are equal.

{{< /details >}}

### 51 · an equivalent gate

*Asked by: Texas Instruments (NIT Calicut 2023)*

$A$ (inverted) ANDed with $B$, and $B$ (inverted) ANDed with $A$, both into an OR gate. The
equivalent gate?

- **(a)** XOR
- **(b)** XNOR
- **(c)** NAND
- **(d)** NOR

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) XOR**

**Why.** A′B + AB′ is 1 exactly when A and B differ: XOR.

**Concept: XOR = A′B + AB′.** Built from 2 inverters, 2 ANDs and 1 OR, or from 4 NAND gates.

{{< /details >}}

### 52 · XOR in front of a D flip-flop

*Asked by: Texas Instruments (IISc 2023)*

$D = X \oplus Q$. The circuit behaves as:

{{< details title="Answer and explanation" closed="true" >}}

**Answer: a T flip-flop**

**Why.** With D = X ⊕ Q: if X = 0, D = Q (hold); if X = 1, D = Q′ (toggle). That is exactly a T flip-flop with T = X.

**Concept: flip-flop conversions.** Make the D input equal the target flip-flop's next-state equation: T: D = T ⊕ Q; JK: D = JQ′ + K′Q.

{{< /details >}}
