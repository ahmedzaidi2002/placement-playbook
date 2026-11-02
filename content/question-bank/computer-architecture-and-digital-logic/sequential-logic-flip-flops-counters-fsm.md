---
title: "Sequential logic (flip-flops, counters, FSM)"
weight: 2
---

30 questions asked by Qualcomm, Texas Instruments. Try each one first, then open the toggle: it gives the answer, why it is right, and the idea behind it explained from scratch.

### 1 · Computer Architecture

*Asked by: Qualcomm (60-question online assessment)*

The initial content of a 4-bit register is `1011`. It is shifted **4 times to the right**, with the serial input `111010`. What is the content of the register after four shifts?

- **(a)** 101011
- **(b)** 1100
- **(c)** 1011
- **(d)** 101110

{{< details title="Answer and explanation" closed="true" >}}

**Answer: no reliable pick** (the question appears flawed)

**Why.** Shifting 1011 right four times with serial inputs 1, 1, 1, 0 entering at the MSB gives 0111; reading the input from the other end gives 1010. Neither is an option, and two options are 6 bits wide for a 4-bit register.

**Concept: shift registers.** On each clock every bit moves one place, the serial input fills the vacated end, and the bit at the other end falls out. After n shifts in an n-bit register, the contents are entirely the last n serial inputs (in order).

{{< /details >}}

### 2 · Flip-flops (CA section)

*Asked by: Qualcomm (Delhi campus 2024, Q38)*

A J-K flip-flop has its J input connected to logic 1 and its K input connected to its own Q output. When clock pulses are applied, the flip-flop will:

- **(a)** Go to 0 and stay there
- **(b)** Change its state at each clock pulse
- **(c)** Go to 1 and stay there
- **(d)** Retain its initial state

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) it changes state at each clock pulse**

**Why.** If Q = 0: J = 1, K = Q = 0 → set to 1. If Q = 1: J = 1, K = 1 → toggle to 0. So it alternates on every clock.

**Concept: JK flip-flop.** J = K = 0 hold, J = 1 K = 0 set, J = 0 K = 1 reset, J = K = 1 toggle. Characteristic equation Q⁺ = JQ′ + K′Q.

{{< /details >}}

### 3 · Latches and flip-flops

*Asked by: Qualcomm (BITS Hyderabad 2024, Q52)*

What is the difference between a latch and a flip-flop?

- **(a)** Latches are used in synchronous circuits and flip-flops in asynchronous circuits
- **(b)** Latches are level-triggered and flip-flops are edge-triggered
- **(c)** Latches store bits and flip-flops store data
- **(d)** Latches are analog and flip-flops are digital

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) latches are level-triggered and flip-flops are edge-triggered**

**Why.** A latch is transparent (output follows input) while its enable is at the active level. A flip-flop samples its input only at a clock edge.

**Concept: why edge-triggering matters.** In a pipeline of registers, edge-triggered flip-flops ensure each stage captures exactly once per clock; transparent latches could let data race through several stages in one phase.

{{< /details >}}

### 4 · Latches and flip-flops

*Asked by: Qualcomm (BITS Hyderabad 2025, Q51)*

Find the mode of operation of the given SR latch during the period starting at e (e to f).

<figure class="nb-fig"><img src="/companies/qualcomm/core/sr-wave.svg" alt="Figure for question 4" loading="lazy"></figure>

- **(a)** Reset
- **(b)** Set
- **(c)** Hold
- **(d)** Prohibit

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) prohibited**

**Why.** Between e and f both S and R are 1, the forbidden input for a NOR SR latch (both outputs forced to 0, and the result is unpredictable when they are released). Other intervals: a–b prohibited, b–c reset, c–d hold, d–e reset, f–g reset.

**Concept: SR latch modes.** S = R = 0 hold; S = 1 set; R = 1 reset; S = R = 1 invalid (for NOR latches; for NAND latches the invalid input is S = R = 0 with active-low inputs).

{{< /details >}}

### 5 · Latches and flip-flops

*Asked by: Qualcomm (BITS Hyderabad 2025, Q56)*

A flip-flop has inputs P and N with the behaviour below. What is its characteristic equation?

| P | N | Qnext |
|:-:|:-:|:-:|
| 0 | 0 | Q′ |
| 0 | 1 | Q′ |
| 1 | 0 | Q′ |
| 1 | 1 | 1 |

- **(a)** Q′ + PN
- **(b)** PQ′N
- **(c)** Q + PN′
- **(d)** P′ + QN′

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) Q′ + PN**

**Why.** Qnext is Q′ in three rows and 1 when P = N = 1. So Qnext = Q′ (most of the time) OR PN (forces 1): Q′ + PN. Check the P = N = 1 row: Q′ + 1 = 1 ✓.

**Concept: characteristic equations.** Write Qnext as a function of the inputs and the present state Q, from the table (K-map with Q as a variable if needed).

{{< /details >}}

### 6 · Latches and flip-flops

*Asked by: Qualcomm (Delhi campus 2024)*

What is the next-state equation of a T flip-flop?

- **(a)** Qn+1 = T + Qn
- **(b)** Qn+1 = T ⊙ Qn
- **(c)** Qn+1 = (T + Qn)(T·Qn)
- **(d)** Qn+1 = T ⊕ Qn

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) Qn+1 = T ⊕ Qn**

**Why.** T = 0 holds (Q⁺ = Q), T = 1 toggles (Q⁺ = Q′). So Q⁺ = T′Q + TQ′ = T ⊕ Q.

**Concept: T flip-flop.** The building block of binary counters: each stage toggles when all lower bits are 1.

{{< /details >}}

### 7 · Latches and flip-flops

*Asked by: Qualcomm (2025 paper (campus not named), Q44)*

How is a D flip-flop converted into a T flip-flop?

- **(a)** D = Q′
- **(b)** D = 0
- **(c)** D = Q
- **(d)** D = 1

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) D = Q′**

**Why.** In general, D = T ⊕ Q makes a D flip-flop act like a T flip-flop. With T held at 1 (always toggle), D = Q′.

**Concept: divide-by-2.** A D flip-flop with Q′ fed back to D toggles every clock, so its output is a square wave at half the clock frequency.

{{< /details >}}

### 8 · Latches and flip-flops

*Asked by: Qualcomm (BITS Goa 2024, Q43)*

The output of the 2:1 MUX is fed to a D flip-flop, and the Q output of the flip-flop is fed back to the select line of the MUX. The set-up works as a:

<figure class="nb-fig"><img src="/companies/qualcomm/core/mux-dff.svg" alt="Figure for question 8" loading="lazy"></figure>

- **(a)** JK flip-flop
- **(b)** RS flip-flop
- **(c)** D flip-flop
- **(d)** Mod-3 counter

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) JK flip-flop**

**Why.** The MUX gives D = Q′·J + Q·K′ (Q selects between the J path and the K′ path). That is exactly the JK characteristic equation Q⁺ = JQ′ + K′Q.

**Concept: building flip-flops from others.** Feed the D input with the target flip-flop's next-state equation; a MUX controlled by Q is a neat way to implement "if Q = 0 then X else Y".

{{< /details >}}

### 9 · Latches and flip-flops

*Asked by: Qualcomm (Delhi campus 2024, Q47)*

A circuit diagram of a J-K flip-flop built from gates is shown. What is the output Q if J = 1 and K = 0?

<figure class="nb-fig"><img src="/companies/qualcomm/core/jk-from-gates.svg" alt="Figure for question 9" loading="lazy"></figure>

- **(a)** Last state
- **(b)** 1
- **(c)** 0
- **(d)** Undefined

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) 1**

**Why.** With K = 0, the reset-side gate is held at 0, so it can't reset. With J = 1, the set-side gate drives the set input on the clock. J = 1, K = 0 is the set condition: Q = 1.

**Concept: JK from gates.** A JK is an SR flip-flop with feedback: S = JQ′ and R = KQ, which makes J = K = 1 toggle instead of being invalid.

{{< /details >}}

### 10 · Latches and flip-flops

*Asked by: Qualcomm (BITS Hyderabad 2025, Q52)*

If the inputs to a JK flip-flop are J = 01010101 and K = 10001101 (one bit per clock, left first), what is Q′?

- **(a)** 01010101
- **(b)** 01110110
- **(c)** 10010101
- **(d)** 10001001

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) 10001001**

**Why.** Apply each (J, K) pair in turn:

| J | 0 | 1 | 0 | 1 | 0 | 1 | 0 | 1 |
|---|---|---|---|---|---|---|---|---|
| K | 1 | 0 | 0 | 0 | 1 | 1 | 0 | 1 |
| action | reset | set | hold | set | reset | toggle | hold | toggle |
| Q | 0 | 1 | 1 | 1 | 0 | 1 | 1 | 0 |

The first pair resets, so the starting state doesn't matter. Q′ = 10001001.

**Concept: trace sequential circuits step by step.** Make a table of inputs, the action they cause, and the resulting state for each clock.

{{< /details >}}

### 11 · Latches and flip-flops

*Asked by: Qualcomm (IISc 2024, Q44)*

The initial output of the flip-flop shown is 0 and the clock frequency is 12 kHz. What is the output frequency?

<figure class="nb-fig"><img src="/companies/qualcomm/core/sr-toggle.svg" alt="Figure for question 11" loading="lazy"></figure>

- **(a)** 6 kHz
- **(b)** 12 kHz
- **(c)** 3 kHz
- **(d)** 48 kHz

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) 6 kHz**

**Why.** S is fed from Q′ and R from Q, so each clock edge sets a reset flip-flop or resets a set one: it toggles. A toggling flip-flop completes one output cycle every two clock cycles: 12/2 = 6 kHz.

**Concept: frequency division.** Each toggle stage halves the frequency; n stages divide by 2ⁿ.

{{< /details >}}

### 12 · Latches and flip-flops

*Asked by: Qualcomm (BITS Goa 2024, Q57)*

The circuit has three flip-flops: A is a D flip-flop with D_A = BC, B is a T flip-flop with T_B = 1, and C is a JK flip-flop with J_C = K_C = B′, all on one clock. The present state ABC = 101. What is the state after 6 clock pulses?

<figure class="nb-fig"><img src="/companies/qualcomm/core/three-ff.svg" alt="Figure for question 12" loading="lazy"></figure>

- **(a)** 010
- **(b)** 101
- **(c)** 000
- **(d)** 110

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) 000**

**Why.** A⁺ = BC, B⁺ = B′, C⁺ = C ⊕ B′ (JK with J = K = B′ toggles C when B = 0). From 101: → 010 → 000 → 011 → 101 → ..., a cycle of 4. Six pulses = one full cycle + 2 → 000.

**Concept: state sequences repeat.** Find the cycle length, then use (pulses mod cycle length) instead of simulating every pulse.

{{< /details >}}

### 13 · Registers and sequential design

*Asked by: Qualcomm (IISc 2024, Q47)*

The serial-in parallel-out shift register shown has feedback X = (D₃ ⊕ D₂) ⊕ (D₁D₀)′. If its initial state is 1111, what is the content of the register after the 3rd clock pulse?

<figure class="nb-fig"><img src="/companies/qualcomm/core/sipo.svg" alt="Figure for question 13" loading="lazy"></figure>

- **(a)** 1011
- **(b)** 0111
- **(c)** 0110
- **(d)** 1101

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) 1011**

**Why.** The serial input enters at the D₀ end and data shifts toward D₃:

| Clock | X from the current state | D₃D₂D₁D₀ |
|:-:|---|:-:|
| 0 | | 1111 |
| 1 | (1⊕1)⊕(1·1)′ = 0 | 1110 |
| 2 | (1⊕1)⊕(1·0)′ = 1 | 1101 |
| 3 | (1⊕1)⊕(0·1)′ = 1 | 1011 |

(If the input entered at D₃ instead, the answer would be 1101.)

**Concept: feedback shift registers.** Compute the feedback from the current state, shift, insert it, repeat.

{{< /details >}}

### 14 · Registers and sequential design

*Asked by: Qualcomm (BITS Hyderabad 2025, Q57)*

In the figure, a MUX is placed in front of every flip-flop with a common select S. How do the flip-flops behave in normal mode and in scan mode?

<figure class="nb-fig"><img src="/companies/qualcomm/core/scan-chain.svg" alt="Figure for question 14" loading="lazy"></figure>

- **(a)** As flip-flops in both modes
- **(b)** As usual in scan mode and as a shift register in normal mode
- **(c)** As a shift register in both modes
- **(d)** As usual in normal mode and as a shift register in scan mode

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) normal flip-flops in normal mode and a shift register in scan mode**

**Why.** This is a scan chain. With S = 0 each flip-flop captures its functional input D. With S = 1 each captures the previous flip-flop's Q, so the chain shifts test data in from SI and out through SO.

**Concept: scan design.** A tester can shift any state into all flip-flops, run one functional clock, and shift the result out, which makes deep sequential logic testable like combinational logic.

{{< /details >}}

### 15 · Registers and sequential design

*Asked by: Qualcomm (IISc 2024, Q49)*

Consider the counter table below. It is required to design the counter with J-K flip-flops. Find the input J_C.

| C | B | A | → C | B | A |
|:-:|:-:|:-:|:-:|:-:|:-:|
| 0 | 0 | 0 | 0 | 1 | 0 |
| 0 | 0 | 1 | 1 | 0 | 0 |
| 0 | 1 | 0 | 0 | 1 | 1 |
| 0 | 1 | 1 | 0 | 0 | 1 |
| 1 | 0 | 0 | 1 | 1 | 0 |
| 1 | 0 | 1 | 0 | 0 | 0 |
| 1 | 1 | 0 | 0 | 0 | 0 |
| 1 | 1 | 1 | 0 | 0 | 0 |

- **(a)** A′B′
- **(b)** AB
- **(c)** A′B
- **(d)** AB′

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) AB′**

**Why.** J_C matters only when C = 0 (when C = 1, J_C is a don't-care). C goes 0 → 1 only from 001, so J_C = 1 at CBA = 001 and 0 at 000, 010, 011. Using the don't-cares, J_C = AB′.

**Concept: JK excitation table.** 0 → 0: J = 0, K = x. 0 → 1: J = 1, K = x. 1 → 0: J = x, K = 1. 1 → 1: J = x, K = 0. The many don't-cares make JK designs simple.

{{< /details >}}

### 16 · Registers and sequential design

*Asked by: Qualcomm (IISc 2024, Q46)*

JK flip-flops are used to design a sequence detector for 1001 (overlap allowed); the output is 1 when the sequence is detected, e.g. input 10010100110101010100100110. Two flip-flops A and B are needed. What are their input equations (X is the input)?

- **(a)** JA = B′X′, KA = B′ + X, JB = X + A, KB = X
- **(b)** JA = BX′, KA = B′ + X, JB = X + A, KB = X′
- **(c)** JA = B′X′, KA = B′ + X′, JB = X′ + A, KB = X′
- **(d)** JA = BX, KA = B + X, JB = X + A′, KB = X

{{< details title="Answer and explanation" closed="true" >}}

**Answer: no reliable pick** (none of the options detects 1001; (b) is the closest)

**Why.** A Mealy detector with states S0 = 00 (nothing), S1 = 01 (seen "1"), S2 = 11 ("10"), S3 = 10 ("100"); on X = 1 from S3, output 1 and go to S1 (overlap). Deriving the JK inputs gives JA = BX′, KA = B′ + X, JB = X, KB = AX′, Z = AB′X. Option (b) matches the A equations exactly but not the B ones, and checking all 24 state assignments shows none of the options detects 1001.

**Concept: sequence detectors.** Each state means "how much of the pattern have I seen so far". On a mismatch, fall back to the longest suffix of the input that is still a prefix of the pattern (that is what makes overlap work).

{{< /details >}}

### 17 · Counters

*Asked by: Qualcomm (2025 paper (campus not named), Q47)*

How many flip-flops are needed for a mod-35 counter?

- **(a)** 5
- **(b)** 4
- **(c)** 6
- **(d)** 7

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) 6**

**Why.** n flip-flops give 2ⁿ states; we need 2ⁿ ≥ 35. 2⁵ = 32 is too few, 2⁶ = 64 is enough.

**Concept: minimum flip-flops = ⌈log₂(states)⌉.**

{{< /details >}}

### 18 · Counters

*Asked by: Qualcomm (2025 paper (campus not named), Q46)*

A binary counter with N flip-flops counts from 0 to 783. What is N?

- **(a)** 10
- **(b)** 11
- **(c)** 9
- **(d)** 8

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) 10**

**Why.** 0 to 783 is 784 states; 2⁹ = 512 < 784 ≤ 1024 = 2¹⁰.

**Concept: same rule.** Don't forget that counting from 0 to N needs N + 1 states.

{{< /details >}}

### 19 · Counters

*Asked by: Qualcomm (2025 paper (campus not named), Q43)*

A counter is clocked at 256 kHz and the output of its last flip-flop is 2 kHz. What is the MOD number?

- **(a)** 100
- **(b)** 125
- **(c)** 128
- **(d)** 208

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) 128**

**Why.** A mod-N counter's last stage outputs one cycle per N clock cycles: N = 256 kHz/2 kHz = 128.

**Concept: MOD number = frequency division ratio.**

{{< /details >}}

### 20 · Counters

*Asked by: Qualcomm (2025 paper (campus not named), Q50)*

How many flip-flops are needed to build the counter with the state diagram shown?

<figure class="nb-fig"><img src="/companies/qualcomm/core/ring-states.svg" alt="Figure for question 20" loading="lazy"></figure>

- **(a)** 3
- **(b)** 2
- **(c)** 1
- **(d)** 4

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) 4**

**Why.** The states are 4-bit words used directly as outputs, so each bit needs its own flip-flop. (Three flip-flops would suffice only for a binary-encoded 8-state machine followed by decoding.)

**Concept: state encoding.** Binary encoding uses the fewest flip-flops; one-hot or output-coded encodings use more flip-flops but simpler logic.

{{< /details >}}

### 21 · Counters

*Asked by: Qualcomm (BITS Hyderabad 2025, Q49)*

A 4-bit ripple **down** counter is at state 1000. How many flip-flops change state after 3 clock pulses?

- **(a)** 2
- **(b)** 1
- **(c)** 3
- **(d)** 4

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) 3**

**Why.** Down-counting: 1000 → 0111 → 0110 → 0101. Comparing 1000 with 0101, three bits differ. (If the question means the flip-flops that toggle on the 3rd pulse alone, 0110 → 0101, the answer would be 2.)

**Concept: ripple counters.** Each flip-flop is clocked by the previous one's output, so changes ripple through the stages one after another; that delay limits speed and causes brief invalid states.

{{< /details >}}

### 22 · Counters

*Asked by: Qualcomm (Delhi campus 2024, Q54)*

The given circuit is a cascade of 4 J-K flip-flops. It works as a:

<figure class="nb-fig"><img src="/companies/qualcomm/core/mod10.svg" alt="Figure for question 22" loading="lazy"></figure>

- **(a)** Mod-5 asynchronous DOWN counter
- **(b)** Mod-5 asynchronous UP counter
- **(c)** Mod-10 asynchronous UP counter
- **(d)** Mod-10 asynchronous DOWN counter

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) mod-10 asynchronous up counter**

**Why.** J = K = 1 on every stage, so each toggles; each is clocked by the previous Q: a ripple counter (counting up with negative-edge flip-flops). The AND of Q₁ and Q₃ clears all stages when the count reaches 1010 (ten), so it counts 0–9.

**Concept: truncated counters.** Detect the first unwanted state (N) and use it to reset the counter, giving mod-N. Only the bits that are 1 in N need to be ANDed.

{{< /details >}}

### 23 · Counters

*Asked by: Qualcomm (BITS Goa 2024, Q54)*

In the counter of the figure (4 J-K flip-flops, J₀ = K₀ = HIGH, the other J = K pairs driven by NAND gates of the Q outputs), the counter locks after some initial states into two final states, toggling alternately between them. Identify the states.

<figure class="nb-fig"><img src="/companies/qualcomm/core/lockup-pair.svg" alt="Figure for question 23" loading="lazy"></figure>

- **(a)** 1001 and 0110
- **(b)** 1110 and 0001
- **(c)** 1010 and 0101
- **(d)** 1111 and 0000

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) 1010 and 0101**

**Why.** In a lock-up pair every bit toggles on every clock, so every J = K input must be 1 in both states, i.e. every NAND must see a 0 in both. 1111 ↔ 0000 is impossible (in 1111 some NAND gets all-ones inputs). Simulating the readable wirings, the pair that survives is 1010 ↔ 0101.

**Concept: lock-up states.** Counters that don't use all 2ⁿ states can get stuck in unused states after power-up or noise. Good designs make every unused state lead back into the main sequence (self-starting).

{{< /details >}}

### 24 · Timing

*Asked by: Qualcomm (IISc 2024, Q51)*

What is the maximum frequency of operation of a flip-flop if t_setup = 1 ns, t_pd = 5 ns and t_ns = 2 ns (total negative slack)?

- **(a)** 165 MHz
- **(b)** 98 MHz
- **(c)** 205 MHz
- **(d)** 125 MHz

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) 125 MHz**

**Why.** Without slack the minimum period would be t_pd + t_setup = 6 ns (about 167 MHz). A negative slack of 2 ns means the path misses that target by 2 ns, so the achievable period is 8 ns: 1/8 ns = 125 MHz. (165 MHz is the trap that ignores the slack.)

**Concept: setup timing.** T_clk ≥ t_clk→q + t_logic + t_setup (+ skew). Slack = required time − arrival time; negative slack means the path is too slow for the target clock.

{{< /details >}}

### 25 · Timing

*Asked by: Qualcomm (IISc 2024, Q56)*

In the figure below, timing analysis shows that the Gate signal arrives later than the CLK input. What is the effect and how can it be removed?

<figure class="nb-fig"><img src="/companies/qualcomm/core/clock-gating.svg" alt="Figure for question 25" loading="lazy"></figure>

- **(a)** Glitch will occur and it can be removed by A gating signal
- **(b)** Glitch will occur and it can be removed either by A gating signal or B gating signal
- **(c)** Glitch will occur and it cannot be removed by A gating signal or B gating signal
- **(d)** Glitch will occur and it can be removed by B gating signal

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) a glitch occurs; the "A gating" signal removes it**

**Why.** Gate falls while CLK is high, so the flip-flop sees a narrow sliver pulse (a glitch), and its rise in the next high phase clips the following pulse. For an AND clock gate, the enable must change only while CLK is low. "A gating" has the same meaning as Gate but switches during the low phase, so it removes the glitch; "B gating" switches while low but is inverted, so it would pass the wrong pulses.

**Concept: clock gating.** Turning off the clock to idle logic saves power, but the enable must be stable while the clock is high. Real designs use an integrated clock-gating cell: a latch (transparent when CLK is low) followed by an AND.

{{< /details >}}

### 26 · Timing

*Asked by: Qualcomm (BITS Hyderabad 2024, Q58)*

For the net in the figure, how do we represent the net delay?

<figure class="nb-fig"><img src="/companies/qualcomm/core/net-delay.svg" alt="Figure for question 26" loading="lazy"></figure>

- **(a)** f(C_net + C_pin)
- **(b)** f(C_pin)
- **(c)** f(R_net)
- **(d)** f(R_net, C_net + C_pin)

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) f(R_net, C_net + C_pin)**

**Why.** Interconnect delay is an RC delay: the wire's resistance charges the wire's capacitance plus the load pin's input capacitance. Elmore delay ≈ R_net (C_net/2 + C_pin).

**Concept: wire delay.** In modern chips, wires can be slower than gates; delay grows with length² for unbuffered wires, so long nets get repeaters.

{{< /details >}}

### 27 · D flip-flop with feedback

*Asked by: Texas Instruments (IISc 2023)*

A D flip-flop with $D = \overline Q$ is clocked at 10 kHz. Output frequency?

{{< details title="Answer and explanation" closed="true" >}}

**Answer: 5 kHz**

**Why.** With D = Q′ the flip-flop toggles on every clock edge, so its output completes one cycle every two clock cycles: 10/2 = 5 kHz.

**Concept: divide-by-2 flip-flop** (see above).

{{< /details >}}

### 28 · setup or hold?

*Asked by: Texas Instruments (NIT Calicut 2023)*

A D flip-flop's Q feeds back to D through a 0.2 ns delay; $T_{cq} = 1.5$ ns,
$T_{su} = 1$ ns, $T_h = 2$ ns, and CLK reaches it through CLK_BUF (delay 0). (A) Which
violation? (B) What CLK_BUF delay raises the frequency by 1.5$\times$?

- **(a)** A: setup violation; B: 0.5 ns
- **(b)** A: hold violation; B: the CLK_BUF delay does not affect the frequency
- **(c)** A: hold violation; B: 0.5 ns
- **(d)** A: no violation; B: the CLK_BUF delay does not affect the frequency

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) hold violation; the CLK_BUF delay doesn't affect the frequency**

**Why.** After a clock edge, the new data reaches D at T_cq + 0.2 = 1.7 ns, but the input must stay stable for T_h = 2 ns after the edge: a hold violation. With a single flip-flop, launch and capture use the same buffered clock, so the buffer delay cancels out and can't change the maximum frequency.

**Concept: setup vs hold.** Setup: data must arrive early enough before the next edge (limits max frequency). Hold: data must not change too soon after the current edge (independent of frequency; fixed by adding delay to the data path).

{{< /details >}}

### 29 · a 2-bit JK counter

*Asked by: Texas Instruments (IISc 2023)*

$J_A = \overline{Q_B}$, $K_A = Q_B$, $J_B = K_B = Q_A$ (read from the photo), common clock,
starting at $Q_AQ_B = 10$. State after 3 clocks?

{{< details title="Answer and explanation" closed="true" >}}

**Answer: 10**

**Why.** J_A = Q_B′, K_A = Q_B, J_B = K_B = Q_A. From Q_AQ_B = 10: A sets (J = 1), B toggles → 11. Then A resets (K = 1), B toggles → 00. Then A sets, B holds (J = K = 0) → 10. Period 3, so after 3 clocks it is back at 10. (The candidate's 11 is wrong if the wiring is read correctly.)

**Concept: synchronous counter analysis.** For each state, compute every flip-flop's inputs from the present state, apply the JK rules, and get the next state; continue until a state repeats.

{{< /details >}}

### 30 · master-slave flip-flop

*Asked by: Texas Instruments (IISc 2023)*

In a master-slave flip-flop, when does the output change?

{{< details title="Answer and explanation" closed="true" >}}

**Answer: when the slave changes**, i.e. at the clock edge that passes the master's value to the slave

**Why.** The master latch follows the input during one clock level; at the clock edge it closes and the slave opens, copying the master's stored value to the output. So the output changes only at that edge.

**Concept: master–slave flip-flops.** Two latches with opposite enables make an edge-triggered flip-flop: the master captures, the slave presents. At no moment is there a transparent path from input to output.

{{< /details >}}
