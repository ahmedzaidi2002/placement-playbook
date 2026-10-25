---
title: "5 · Datapath, control and pipelining"
linkTitle: "5 CPU and pipelining"
weight: 5
math: true
---
## 5.1 The instruction cycle {#coa-5-1}

**Fetch** (MAR ← PC; MDR ← Mem[MAR]; IR ← MDR; PC ← PC + 1) → **decode** → fetch operands → **execute** → write back → check for interrupts → repeat.

- **Single-cycle datapath:** every instruction finishes in one long cycle, set by the slowest instruction (a load). Simple, wasteful.
- **Multi-cycle datapath:** each instruction takes several short cycles (one per step), so simple instructions finish sooner.

## 5.2 Hardwired vs microprogrammed control {#coa-5-2}

| | Hardwired | Microprogrammed |
|---|---|---|
| Control signals from | combinational logic | a **control memory** of microinstructions |
| Speed | **faster** | slower |
| Changing it | redesign the circuit | rewrite the microcode |
| Used in | RISC | CISC (complex instructions) |

**Horizontal microcode:** one bit per control signal (wide, fast, parallel). **Vertical microcode:** encoded fields that must be decoded (narrow, slower). Control-memory address field = $\lceil \log_2(\text{number of microinstructions}) \rceil$ bits (600 microinstructions → 10 bits).

## 5.3 Pipelining {#coa-5-3}

Split instruction execution into $k$ stages so $k$ instructions are in progress at once, like an assembly line. Classic RISC: **IF** (fetch), **ID** (decode, read registers), **EX** (execute), **MEM** (memory access), **WB** (write back).

Pipelining improves **throughput**, not the latency of one instruction (which gets slightly worse because of latch overhead).

<div class="nb nb-theorem nb-block">

<strong>Pipeline timing</strong>

Clock period $T = $ (slowest stage) + (latch delay). $n$ instructions on a $k$-stage pipeline take

$$(k + n - 1) \times T, \qquad \text{speed-up} = \frac{n \times T_{\text{non-pipelined}}}{(k + n - 1)\,T} \ \xrightarrow{\ n \to \infty\ }\ \frac{T_{\text{non-pipelined}}}{T} \le k.$$

</div>

<div class="nb nb-example">

<strong>Example</strong> (Speed-up)

Stage delays 60, 80, 70, 90, 50 ns, latch 10 ns. Clock = $90 + 10 = $ **100 ns**. Non-pipelined: $60 + 80 + 70 + 90 + 50 = 350$ ns per instruction. For 100 instructions: non-pipelined $35{,}000$ ns; pipelined $(5 + 99) \times 100 = 10{,}400$ ns; speed-up **3.37**. As $n \to \infty$: $350/100 = $ **3.5** (not 5: the stages are unbalanced and latches add time).

</div>

## 5.4 Hazards {#coa-5-4}

| Hazard | Cause | Fixes |
|---|---|---|
| **Structural** | two instructions need the same hardware (one memory for instructions and data) | duplicate resources (separate instruction and data caches) |
| **Data** | an instruction needs a result not yet written | **forwarding (bypassing)**, stalls, instruction reordering |
| **Control** | the next instruction depends on a branch outcome | stall, **branch prediction**, delayed branch |

**Data dependences:** **RAW** (read after write, a true dependence; the only one that hurts an in-order pipeline), **WAR** (anti-dependence) and **WAW** (output dependence), which matter in out-of-order machines and are removed by **register renaming**.

<div class="nb nb-example">

<strong>Example</strong> (Stalls)

`ADD R1, R2, R3` followed by `SUB R4, R1, R5` (RAW on R1).
- **No forwarding:** SUB must wait until ADD writes R1 in WB: **2 stall cycles** if registers are written in the first half of a cycle and read in the second half (3 otherwise).
- **With forwarding:** ADD's EX result goes straight to SUB's EX: **0 stalls**.
- **Load-use:** `LW R1, 0(R2)` then `ADD R4, R1, R5`: the data appears only after MEM, so even with forwarding there is **1 stall**.

</div>

**CPI with stalls:** $\text{CPI} = 1 + \text{stall cycles per instruction}$. Example: 20% of instructions are branches with a 2-cycle penalty → $\text{CPI} = 1 + 0.2 \times 2 = $ **1.4**.

## 5.5 Branch prediction {#coa-5-5}

- **Static:** predict not taken, or predict backward branches taken (loops).
- **Dynamic:** a **1-bit predictor** remembers the last outcome (mispredicts twice per loop). A **2-bit saturating counter** must be wrong twice before changing its prediction (mispredicts once per loop exit). **Branch target buffer (BTB)** caches target addresses.
- **Delayed branch:** the instruction after a branch always executes (old MIPS); the compiler fills that slot.

## 5.6 Beyond one instruction per cycle {#coa-5-6}

- **Superscalar:** fetch and issue several instructions per cycle (CPI < 1).
- **Out-of-order execution:** run instructions when their operands are ready (Tomasulo, reorder buffer to retire in order).
- **Superpipelining:** many more, shorter stages.
- **VLIW:** the compiler packs independent operations into one long instruction.
- **Precise interrupts:** all instructions before the faulting one complete, none after it does.

<div class="nb nb-moral">

Pipelining raises throughput, not single-instruction latency. Time = (k + n − 1) × clock; clock = slowest stage + latch. RAW hazards are fixed by forwarding, except the load-use case (1 stall). CPI = 1 + stalls per instruction.

</div>
