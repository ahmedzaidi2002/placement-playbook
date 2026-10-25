---
title: "3 · Combinational and sequential circuits"
linkTitle: "3 Circuits"
weight: 3
math: true
---
**Combinational** circuits: output depends only on the current inputs (adders, multiplexers). **Sequential** circuits: output also depends on stored state (flip-flops, counters, registers).

## 3.1 Adders {#coa-3-1}

- **Half adder:** sum $= A \oplus B$, carry $= AB$.
- **Full adder:** sum $= A \oplus B \oplus C_{in}$, carry $= AB + C_{in}(A \oplus B)$. Two half adders + an OR gate.
- **Ripple-carry adder:** $n$ full adders in a chain; the carry ripples through all of them, so delay grows as $2n$ gate delays.
- **Carry-lookahead adder (CLA):** compute every carry in parallel from **generate** $G_i = A_iB_i$ and **propagate** $P_i = A_i \oplus B_i$: $C_{i+1} = G_i + P_iC_i$, expanded so no carry waits for another. Much faster, more gates.
- **Subtraction** with the same adder: $A - B = A + \overline{B} + 1$ (invert $B$, set the carry-in to 1).

## 3.2 Multiplexers, decoders, encoders {#coa-3-2}

| Block | Does | Size |
|---|---|---|
| **Multiplexer (MUX)** | selects one of $2^n$ inputs using $n$ select lines | $2^n$:1 |
| **Demultiplexer** | routes one input to one of $2^n$ outputs | 1:$2^n$ |
| **Decoder** | turns an $n$-bit code into one of $2^n$ active lines | $n$:$2^n$ |
| **Encoder** | the reverse; a **priority encoder** outputs the highest active input | $2^n$:$n$ |

- A $2^n$:1 MUX can implement **any** function of $n$ variables (inputs = truth-table column), or of $n + 1$ variables using the extra variable or its complement on the inputs.
- A decoder + OR gates implements any function in SOP form.
- Building big from small: a **32:1 MUX from 4:1 MUXes** needs $8 + 2 + 1 = $ **11** (8 at the first level, then 2, then one more to choose between those 2).

## 3.3 Latches and flip-flops {#coa-3-3}

A **latch** is level-triggered (transparent while enabled); a **flip-flop** is edge-triggered (changes only on the clock edge).

| Flip-flop | Characteristic equation | Notes |
|---|---|---|
| **SR** | $Q^+ = S + \overline{R}Q$ | $S = R = 1$ is **forbidden** |
| **JK** | $Q^+ = J\overline{Q} + \overline{K}Q$ | $J = K = 1$ **toggles** |
| **D** | $Q^+ = D$ | stores the input; registers are made of D flip-flops |
| **T** | $Q^+ = T \oplus Q$ | $T = 1$ toggles |

**JK table:** $J K = 00$ hold, $01$ reset (0), $10$ set (1), $11$ toggle. The **race-around** problem of a level-triggered JK (toggling many times while the clock is high) is solved by master–slave or edge-triggered designs.

**Frequency division:** a T flip-flop with $T = 1$ (or a D flip-flop with $D = \overline{Q}$) toggles every clock edge, so its output is **half** the clock frequency. $n$ in a chain divide by $2^n$.

## 3.4 Registers and counters {#coa-3-4}

- **Shift registers:** SISO, SIPO, PISO, PIPO (serial/parallel in/out). Shifting left multiplies by 2.
- A **mod-$N$ counter** cycles through $N$ states and needs $\lceil \log_2 N \rceil$ flip-flops (mod-10 → 4).
- **Ripple (asynchronous) counter:** each flip-flop clocks the next; simple, but delays add up. Maximum clock frequency $= 1/(n \times t_{pd})$.
- **Synchronous counter:** all flip-flops share the clock; faster.
- **Ring counter:** $n$ flip-flops, $n$ states. **Johnson (twisted-ring) counter:** $n$ flip-flops, $2n$ states.

<div class="nb nb-example">

<strong>Example</strong> (Ripple counter speed)

A 4-bit ripple counter with 10 ns per flip-flop: the last output settles after $4 \times 10 = 40$ ns, so the maximum clock is $1/40\text{ ns} = $ **25 MHz**. A synchronous version is limited by one flip-flop plus its logic, not by all four.

</div>

## 3.5 State machines {#coa-3-5}

- **Moore machine:** outputs depend only on the **state**. **Mealy machine:** outputs depend on the state **and** the inputs (reacts one cycle earlier, often needs fewer states).
- **Design steps:** state diagram → state table → assign binary codes to states → flip-flop excitation equations → minimise with K-maps.

## 3.6 Timing {#coa-3-6}

Between two flip-flops with combinational logic in between:

- **Setup constraint:** $T_{\text{clock}} \ge t_{\text{clk-to-Q}} + t_{\text{logic,max}} + t_{\text{setup}}$ (sets the maximum frequency).
- **Hold constraint:** $t_{\text{clk-to-Q}} + t_{\text{logic,min}} \ge t_{\text{hold}}$ (independent of the clock period).
- **Metastability:** if an input changes too close to the clock edge, a flip-flop can hover between 0 and 1. Asynchronous inputs pass through a **two-flip-flop synchroniser**.

<div class="nb nb-moral">

Combinational = no memory; sequential = flip-flops. JK with J = K = 1 toggles; a T or D (D = Q̄) flip-flop divides frequency by 2. Mod-N needs ⌈log₂N⌉ flip-flops; ring has n states, Johnson 2n.

</div>
