@@ cisco2-pipeline
**Answer: (d) I and III**

**Why.** Execution time = instruction count × CPI × cycle time. A faster clock (I) shortens the cycle time. Bigger caches (III) mean fewer misses and fewer stall cycles, lowering the effective CPI. Removing forwarding (II) adds data-hazard stalls and slows things down.

**Concept: the CPU performance equation.** Time = IC × CPI × T. Every optimisation attacks one factor: compilers and ISA (IC), pipelining and caches (CPI), circuit design and process (T).

@@ qc-n-cpi
**Answer: none matches exactly; the weighted average is 4.178, and (c) 4.6 (ticked) is the nearest**

**Why.** Average CPI = Σ CPIᵢ × fractionᵢ = 2(0.30) + 5(0.661) + 7(0.039) = 0.6 + 3.305 + 0.273 = 4.178. The table may have been misread or the question has an error; the method is what matters.

**Concept: weighted CPI.** Different instruction types take different numbers of cycles; the program's CPI is their frequency-weighted average. MIPS = clock rate (MHz) / CPI.

@@ qc-n-pipeline
**Answer: (b) 340 ns** (the 5 ns latch overhead belongs to the pipelined design)

**Why.** Without pipelining, one instruction passes through every stage back to back: 90 + 70 + 10 + 40 + 130 = 340 ns. The pipelined clock would be the slowest stage plus overhead, 130 + 5 = 135 ns (option (c)). If the question means adding one overhead, 345 is the alternative reading.

**Concept: latency vs throughput.** Pipelining does not shorten one instruction's latency (it slightly lengthens it with latch overhead); it raises throughput by overlapping instructions.

@@ qc60-41
**Answer: no reliable pick** (if forced, (d) 216 ns = 280 − 64, based on a non-standard reading of "variance")

**Why.** Non-pipelined latency = 40 + 50 + 60 + 30 + 50 + 50 = 280 ns. Pipelined clock = max stage + skew = 60 + 4 = 64 ns, so pipelined latency = 6 × 64 = 384 ns; the difference is 104 ns, not an option. 216 = 280 − 64 is the only option that can be built from the numbers.

**Concept: pipeline clock period.** The clock must fit the slowest stage plus register/skew overhead. Unbalanced stages waste time in the faster ones, so designers balance stage delays.

@@ qcc-arch-32
**Answer: (a) structural hazard**

**Why.** Two instructions needing the same hardware resource at the same time (one memory port, one ALU) is a structural hazard. Data hazards come from operand dependences; control hazards from branches.

**Concept: three hazard types.** Structural (fix: duplicate resources, e.g. separate instruction and data caches). Data (fix: forwarding, stalls). Control (fix: branch prediction, delayed branches, flushing).

@@ qcc-arch-33
**Answer: (c) pipeline interlock**

**Why.** The interlock is the hardware that detects a dependence and inserts stall cycles (bubbles) until it clears. Flushing discards wrong-path instructions after a mispredicted branch.

**Concept: interlocks vs forwarding.** Forwarding passes a result straight from a later stage to an earlier one, avoiding most stalls; interlocks stall only when forwarding can't help (e.g. a load followed immediately by its use).

@@ qcc-arch-34
**Answer: (d) only (III)**

**Why.** Inserting bubbles (stalling) holds a dependent instruction until its operand is ready. Delayed branching and prediction address control hazards; changing latch latency or cycle time doesn't remove a dependence.

**Concept: data hazard types.** RAW (read after write: true dependence), WAR (write after read: anti-dependence), WAW (write after write: output dependence). In-order 5-stage pipelines only face RAW; out-of-order CPUs remove WAR/WAW with register renaming.

@@ qcc-arch-35
**Answer: (a) 4.3**

**Why.** Single-cycle: one instruction takes the sum of all units, 20 + 16 + 20 + 20 + 14 = 90 ns. Pipelined clock = slowest stage + overhead = 20 + 1 = 21 ns, and in steady state one instruction finishes per cycle. Speed-up = 90/21 ≈ 4.29.

**Concept: pipeline speed-up.** Ideal speed-up = number of stages (5), reduced by unbalanced stages (the clock follows the slowest) and latch overhead.

@@ qcc-arch-36
**Answer: (c) 213 MIPS**

**Why.** Effective CPI = base 1 + 2.52 stall cycles = 3.52. MIPS = clock (MHz)/CPI = 750/3.52 ≈ 213. (299 ≈ 750/2.52 is the trap that forgets the base CPI.)

**Concept: memory stalls add to CPI.** CPI_effective = CPI_base + (misses per instruction × miss penalty). Cache performance often matters more than raw clock speed.

@@ ti-dependency
**Answer: anti-dependence (WAR)**

**Why.** j writes a register that the earlier i reads. If j's write happened before i's read, i would read the wrong value: a write-after-read hazard.

**Concept: name dependences.** WAR and WAW occur only because two instructions reuse the same register name, not because data flows between them; renaming to different physical registers removes them.

@@ ti-pipeline
**Answer: (b) 11** (as intended)

**Why.** The first instruction takes 2 + 1 + 3 + 1 = 7 cycles; with a new instruction starting every cycle, the remaining 4 each finish one cycle later: 7 + 4 = 11. (Strictly, a 3-cycle stage that is not itself pipelined could accept only one instruction every 3 cycles, which would make it longer.)

**Concept: pipeline timing.** Total cycles for n instructions = (cycles for the first) + (n − 1) × (issue interval), when nothing stalls.

@@ qc60-33
**Answer: no reliable pick** (the question appears flawed)

**Why.** Shifting 1011 right four times with serial inputs 1, 1, 1, 0 entering at the MSB gives 0111; reading the input from the other end gives 1010. Neither is an option, and two options are 6 bits wide for a 4-bit register.

**Concept: shift registers.** On each clock every bit moves one place, the serial input fills the vacated end, and the bit at the other end falls out. After n shifts in an n-bit register, the contents are entirely the last n serial inputs (in order).

@@ qcc-arch-45
**Answer: (b) it changes state at each clock pulse**

**Why.** If Q = 0: J = 1, K = Q = 0 → set to 1. If Q = 1: J = 1, K = 1 → toggle to 0. So it alternates on every clock.

**Concept: JK flip-flop.** J = K = 0 hold, J = 1 K = 0 set, J = 0 K = 1 reset, J = K = 1 toggle. Characteristic equation Q⁺ = JQ′ + K′Q.

@@ qcc-dig-30
**Answer: (b) latches are level-triggered and flip-flops are edge-triggered**

**Why.** A latch is transparent (output follows input) while its enable is at the active level. A flip-flop samples its input only at a clock edge.

**Concept: why edge-triggering matters.** In a pipeline of registers, edge-triggered flip-flops ensure each stage captures exactly once per clock; transparent latches could let data race through several stages in one phase.

@@ qcc-dig-31
**Answer: (d) prohibited**

**Why.** Between e and f both S and R are 1, the forbidden input for a NOR SR latch (both outputs forced to 0, and the result is unpredictable when they are released). Other intervals: a–b prohibited, b–c reset, c–d hold, d–e reset, f–g reset.

**Concept: SR latch modes.** S = R = 0 hold; S = 1 set; R = 1 reset; S = R = 1 invalid (for NOR latches; for NAND latches the invalid input is S = R = 0 with active-low inputs).

@@ qcc-dig-32
**Answer: (a) Q′ + PN**

**Why.** Qnext is Q′ in three rows and 1 when P = N = 1. So Qnext = Q′ (most of the time) OR PN (forces 1): Q′ + PN. Check the P = N = 1 row: Q′ + 1 = 1 ✓.

**Concept: characteristic equations.** Write Qnext as a function of the inputs and the present state Q, from the table (K-map with Q as a variable if needed).

@@ qcc-dig-33
**Answer: (d) Qn+1 = T ⊕ Qn**

**Why.** T = 0 holds (Q⁺ = Q), T = 1 toggles (Q⁺ = Q′). So Q⁺ = T′Q + TQ′ = T ⊕ Q.

**Concept: T flip-flop.** The building block of binary counters: each stage toggles when all lower bits are 1.

@@ qcc-dig-34
**Answer: (a) D = Q′**

**Why.** In general, D = T ⊕ Q makes a D flip-flop act like a T flip-flop. With T held at 1 (always toggle), D = Q′.

**Concept: divide-by-2.** A D flip-flop with Q′ fed back to D toggles every clock, so its output is a square wave at half the clock frequency.

@@ qcc-dig-35
**Answer: (a) JK flip-flop**

**Why.** The MUX gives D = Q′·J + Q·K′ (Q selects between the J path and the K′ path). That is exactly the JK characteristic equation Q⁺ = JQ′ + K′Q.

**Concept: building flip-flops from others.** Feed the D input with the target flip-flop's next-state equation; a MUX controlled by Q is a neat way to implement "if Q = 0 then X else Y".

@@ qcc-dig-36
**Answer: (b) 1**

**Why.** With K = 0, the reset-side gate is held at 0, so it can't reset. With J = 1, the set-side gate drives the set input on the clock. J = 1, K = 0 is the set condition: Q = 1.

**Concept: JK from gates.** A JK is an SR flip-flop with feedback: S = JQ′ and R = KQ, which makes J = K = 1 toggle instead of being invalid.

@@ qcc-dig-37
**Answer: (d) 10001001**

**Why.** Apply each (J, K) pair in turn:

| J | 0 | 1 | 0 | 1 | 0 | 1 | 0 | 1 |
|---|---|---|---|---|---|---|---|---|
| K | 1 | 0 | 0 | 0 | 1 | 1 | 0 | 1 |
| action | reset | set | hold | set | reset | toggle | hold | toggle |
| Q | 0 | 1 | 1 | 1 | 0 | 1 | 1 | 0 |

The first pair resets, so the starting state doesn't matter. Q′ = 10001001.

**Concept: trace sequential circuits step by step.** Make a table of inputs, the action they cause, and the resulting state for each clock.

@@ qcc-dig-38
**Answer: (a) 6 kHz**

**Why.** S is fed from Q′ and R from Q, so each clock edge sets a reset flip-flop or resets a set one: it toggles. A toggling flip-flop completes one output cycle every two clock cycles: 12/2 = 6 kHz.

**Concept: frequency division.** Each toggle stage halves the frequency; n stages divide by 2ⁿ.

@@ qcc-dig-39
**Answer: (c) 000**

**Why.** A⁺ = BC, B⁺ = B′, C⁺ = C ⊕ B′ (JK with J = K = B′ toggles C when B = 0). From 101: → 010 → 000 → 011 → 101 → ..., a cycle of 4. Six pulses = one full cycle + 2 → 000.

**Concept: state sequences repeat.** Find the cycle length, then use (pulses mod cycle length) instead of simulating every pulse.

@@ qcc-dig-40
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

@@ qcc-dig-41
**Answer: (d) normal flip-flops in normal mode and a shift register in scan mode**

**Why.** This is a scan chain. With S = 0 each flip-flop captures its functional input D. With S = 1 each captures the previous flip-flop's Q, so the chain shifts test data in from SI and out through SO.

**Concept: scan design.** A tester can shift any state into all flip-flops, run one functional clock, and shift the result out, which makes deep sequential logic testable like combinational logic.

@@ qcc-dig-42
**Answer: (d) AB′**

**Why.** J_C matters only when C = 0 (when C = 1, J_C is a don't-care). C goes 0 → 1 only from 001, so J_C = 1 at CBA = 001 and 0 at 000, 010, 011. Using the don't-cares, J_C = AB′.

**Concept: JK excitation table.** 0 → 0: J = 0, K = x. 0 → 1: J = 1, K = x. 1 → 0: J = x, K = 1. 1 → 1: J = x, K = 0. The many don't-cares make JK designs simple.

@@ qcc-dig-43
**Answer: no reliable pick** (none of the options detects 1001; (b) is the closest)

**Why.** A Mealy detector with states S0 = 00 (nothing), S1 = 01 (seen "1"), S2 = 11 ("10"), S3 = 10 ("100"); on X = 1 from S3, output 1 and go to S1 (overlap). Deriving the JK inputs gives JA = BX′, KA = B′ + X, JB = X, KB = AX′, Z = AB′X. Option (b) matches the A equations exactly but not the B ones, and checking all 24 state assignments shows none of the options detects 1001.

**Concept: sequence detectors.** Each state means "how much of the pattern have I seen so far". On a mismatch, fall back to the longest suffix of the input that is still a prefix of the pattern (that is what makes overlap work).

@@ qcc-dig-44
**Answer: (c) 6**

**Why.** n flip-flops give 2ⁿ states; we need 2ⁿ ≥ 35. 2⁵ = 32 is too few, 2⁶ = 64 is enough.

**Concept: minimum flip-flops = ⌈log₂(states)⌉.**

@@ qcc-dig-45
**Answer: (a) 10**

**Why.** 0 to 783 is 784 states; 2⁹ = 512 < 784 ≤ 1024 = 2¹⁰.

**Concept: same rule.** Don't forget that counting from 0 to N needs N + 1 states.

@@ qcc-dig-46
**Answer: (c) 128**

**Why.** A mod-N counter's last stage outputs one cycle per N clock cycles: N = 256 kHz/2 kHz = 128.

**Concept: MOD number = frequency division ratio.**

@@ qcc-dig-47
**Answer: (d) 4**

**Why.** The states are 4-bit words used directly as outputs, so each bit needs its own flip-flop. (Three flip-flops would suffice only for a binary-encoded 8-state machine followed by decoding.)

**Concept: state encoding.** Binary encoding uses the fewest flip-flops; one-hot or output-coded encodings use more flip-flops but simpler logic.

@@ qcc-dig-48
**Answer: (c) 3**

**Why.** Down-counting: 1000 → 0111 → 0110 → 0101. Comparing 1000 with 0101, three bits differ. (If the question means the flip-flops that toggle on the 3rd pulse alone, 0110 → 0101, the answer would be 2.)

**Concept: ripple counters.** Each flip-flop is clocked by the previous one's output, so changes ripple through the stages one after another; that delay limits speed and causes brief invalid states.

@@ qcc-dig-49
**Answer: (c) mod-10 asynchronous up counter**

**Why.** J = K = 1 on every stage, so each toggles; each is clocked by the previous Q: a ripple counter (counting up with negative-edge flip-flops). The AND of Q₁ and Q₃ clears all stages when the count reaches 1010 (ten), so it counts 0–9.

**Concept: truncated counters.** Detect the first unwanted state (N) and use it to reset the counter, giving mod-N. Only the bits that are 1 in N need to be ANDed.

@@ qcc-dig-50
**Answer: (c) 1010 and 0101**

**Why.** In a lock-up pair every bit toggles on every clock, so every J = K input must be 1 in both states, i.e. every NAND must see a 0 in both. 1111 ↔ 0000 is impossible (in 1111 some NAND gets all-ones inputs). Simulating the readable wirings, the pair that survives is 1010 ↔ 0101.

**Concept: lock-up states.** Counters that don't use all 2ⁿ states can get stuck in unused states after power-up or noise. Good designs make every unused state lead back into the main sequence (self-starting).

@@ qcc-dig-51
**Answer: (d) 125 MHz**

**Why.** Without slack the minimum period would be t_pd + t_setup = 6 ns (about 167 MHz). A negative slack of 2 ns means the path misses that target by 2 ns, so the achievable period is 8 ns: 1/8 ns = 125 MHz. (165 MHz is the trap that ignores the slack.)

**Concept: setup timing.** T_clk ≥ t_clk→q + t_logic + t_setup (+ skew). Slack = required time − arrival time; negative slack means the path is too slow for the target clock.

@@ qcc-dig-52
**Answer: (a) a glitch occurs; the "A gating" signal removes it**

**Why.** Gate falls while CLK is high, so the flip-flop sees a narrow sliver pulse (a glitch), and its rise in the next high phase clips the following pulse. For an AND clock gate, the enable must change only while CLK is low. "A gating" has the same meaning as Gate but switches during the low phase, so it removes the glitch; "B gating" switches while low but is inverted, so it would pass the wrong pulses.

**Concept: clock gating.** Turning off the clock to idle logic saves power, but the enable must be stable while the clock is high. Real designs use an integrated clock-gating cell: a latch (transparent when CLK is low) followed by an AND.

@@ qcc-dig-53
**Answer: (d) f(R_net, C_net + C_pin)**

**Why.** Interconnect delay is an RC delay: the wire's resistance charges the wire's capacitance plus the load pin's input capacitance. Elmore delay ≈ R_net (C_net/2 + C_pin).

**Concept: wire delay.** In modern chips, wires can be slower than gates; delay grows with length² for unbuffered wires, so long nets get repeaters.

@@ ti-dff-toggle
**Answer: 5 kHz**

**Why.** With D = Q′ the flip-flop toggles on every clock edge, so its output completes one cycle every two clock cycles: 10/2 = 5 kHz.

**Concept: divide-by-2 flip-flop** (see above).

@@ ti-hold
**Answer: (b) hold violation; the CLK_BUF delay doesn't affect the frequency**

**Why.** After a clock edge, the new data reaches D at T_cq + 0.2 = 1.7 ns, but the input must stay stable for T_h = 2 ns after the edge: a hold violation. With a single flip-flop, launch and capture use the same buffered clock, so the buffer delay cancels out and can't change the maximum frequency.

**Concept: setup vs hold.** Setup: data must arrive early enough before the next edge (limits max frequency). Hold: data must not change too soon after the current edge (independent of frequency; fixed by adding delay to the data path).

@@ ti-jk-counter
**Answer: 10**

**Why.** J_A = Q_B′, K_A = Q_B, J_B = K_B = Q_A. From Q_AQ_B = 10: A sets (J = 1), B toggles → 11. Then A resets (K = 1), B toggles → 00. Then A sets, B holds (J = K = 0) → 10. Period 3, so after 3 clocks it is back at 10. (The candidate's 11 is wrong if the wiring is read correctly.)

**Concept: synchronous counter analysis.** For each state, compute every flip-flop's inputs from the present state, apply the JK rules, and get the next state; continue until a state repeats.

@@ ti-master-slave
**Answer: when the slave changes**, i.e. at the clock edge that passes the master's value to the slave

**Why.** The master latch follows the input during one clock level; at the clock edge it closes and the slave opens, copying the master's stored value to the output. So the output changes only at that edge.

**Concept: master–slave flip-flops.** Two latches with opposite enables make an edge-triggered flip-flop: the master captures, the slave presents. At no moment is there a transparent path from input to output.
