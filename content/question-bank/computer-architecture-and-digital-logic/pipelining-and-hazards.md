---
title: "Pipelining and hazards"
weight: 6
---

11 questions asked by Cisco, Qualcomm, Texas Instruments. Try each one first, then open the toggle: it gives the answer, why it is right, and the idea behind it explained from scratch.

### 1 · Q15, what speeds up a pipelined RISC program

*Asked by: Cisco (OA, Sep 2025)*

In a pipelined RISC computer where all arithmetic instructions have the same CPI (cycles
per instruction), which of the following actions would improve the execution time of a
typical program?

1. Increasing the clock cycle rate.
2. Disallowing any forwarding in the pipeline.
3. Doubling the sizes of the instruction cache and the data cache without changing
    the clock cycle time.

- **(a)** II only
- **(b)** I only
- **(c)** III only
- **(d)** I and III

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) I and III**

**Why.** Execution time = instruction count × CPI × cycle time. A faster clock (I) shortens the cycle time. Bigger caches (III) mean fewer misses and fewer stall cycles, lowering the effective CPI. Removing forwarding (II) adds data-hazard stalls and slows things down.

**Concept: the CPU performance equation.** Time = IC × CPI × T. Every optimisation attacks one factor: compilers and ISA (IC), pipelining and caches (CPI), circuit design and process (T).

{{< /details >}}

### 2 · Q53, average CPI

*Asked by: Qualcomm (Nov 2024); Qualcomm (Delhi campus 2024, Q46)*

Instructions executed on a 400 MHz processor:
| Instruction type | CPI | Mix |
|---|---|---|
| Branch | 2 | 30% |
| Arithmetic and logic | 5 | 66.10% |
| Load/store | 7 | 3.90% |
What will be the average CPI if the program is executed on a uniprocessor system?

- **(a)** 14
- **(b)** 7.89
- **(c)** 4.6
- **(d)** 6.6

{{< details title="Answer and explanation" closed="true" >}}

**Answer: none matches exactly; the weighted average is 4.178, and (c) 4.6 (ticked) is the nearest**

**Why.** Average CPI = Σ CPIᵢ × fractionᵢ = 2(0.30) + 5(0.661) + 7(0.039) = 0.6 + 3.305 + 0.273 = 4.178. The table may have been misread or the question has an error; the method is what matters.

**Concept: weighted CPI.** Different instruction types take different numbers of cycles; the program's CPI is their frequency-weighted average. MIPS = clock rate (MHz) / CPI.

{{< /details >}}

### 3 · Q44, unpipelined latency

*Asked by: Qualcomm (Nov 2024)*

An unpipelined processor with 5 stages has execution stages of 90 ns, 70 ns, 10 ns, 40 ns
and 130 ns. What is the instruction latency of the unpipelined stage? (Assume an overhead of
5 ns.)

- **(a)** 345 ns
- **(b)** 340 ns
- **(c)** 135 ns
- **(d)** 130 ns

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) 340 ns** (the 5 ns latch overhead belongs to the pipelined design)

**Why.** Without pipelining, one instruction passes through every stage back to back: 90 + 70 + 10 + 40 + 130 = 340 ns. The pipelined clock would be the slowest stage plus overhead, 130 + 5 = 135 ns (option (c)). If the question means adding one overhead, 345 is the alternative reading.

**Concept: latency vs throughput.** Pipelining does not shorten one instruction's latency (it slightly lengthens it with latch overhead); it raises throughput by overlapping instructions.

{{< /details >}}

### 4 · Computer Architecture

*Asked by: Qualcomm (60-question online assessment)*

Calculate the **variance** in instruction latency of the pipeline (earlier non-pipelined) with stage times 40 ns, 50 ns, 60 ns, 30 ns, 50 ns, 50 ns and a clock skew of 4 ns.

- **(a)** 280ns
- **(b)** 224ns
- **(c)** 220ns
- **(d)** 216ns

{{< details title="Answer and explanation" closed="true" >}}

**Answer: no reliable pick** (if forced, (d) 216 ns = 280 − 64, based on a non-standard reading of "variance")

**Why.** Non-pipelined latency = 40 + 50 + 60 + 30 + 50 + 50 = 280 ns. Pipelined clock = max stage + skew = 60 + 4 = 64 ns, so pipelined latency = 6 × 64 = 384 ns; the difference is 104 ns, not an option. 216 = 280 − 64 is the only option that can be built from the numbers.

**Concept: pipeline clock period.** The clock must fit the slowest stage plus register/skew overhead. Unbalanced stages waste time in the faster ones, so designers balance stage delays.

{{< /details >}}

### 5 · Pipelining

*Asked by: Qualcomm (NIT Durgapur, Q37)*

When instructions cannot be overlapped in a pipeline because both need the same resource, it is called a:

- **(a)** Structural hazard
- **(b)** Both data and structural hazard
- **(c)** Control hazard
- **(d)** Data hazard

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) structural hazard**

**Why.** Two instructions needing the same hardware resource at the same time (one memory port, one ALU) is a structural hazard. Data hazards come from operand dependences; control hazards from branches.

**Concept: three hazard types.** Structural (fix: duplicate resources, e.g. separate instruction and data caches). Data (fix: forwarding, stalls). Control (fix: branch prediction, delayed branches, flushing).

{{< /details >}}

### 6 · Pipelining

*Asked by: Qualcomm (Delhi campus 2024, Q24)*

The mechanism to identify a hazard and stall the pipeline until the hazard is resolved is called:

- **(a)** Pipeline intralock
- **(b)** Pipeline flush
- **(c)** Pipeline interlock
- **(d)** Pipeline lock

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) pipeline interlock**

**Why.** The interlock is the hardware that detects a dependence and inserts stall cycles (bubbles) until it clears. Flushing discards wrong-path instructions after a mispredicted branch.

**Concept: interlocks vs forwarding.** Forwarding passes a result straight from a later stage to an earlier one, avoiding most stalls; interlocks stall only when forwarding can't help (e.g. a load followed immediately by its use).

{{< /details >}}

### 7 · Pipelining

*Asked by: Qualcomm (BITS Goa 2024, Q38)*

Which of the following prevent **data** hazards in a pipeline?

I. Increasing latch latency  
II. Decreasing cycle time  
III. Introducing pipeline bubbles  
IV. Delayed branching and branch prediction

- **(a)** All (I), (II), (III) and (IV)
- **(b)** Only (IV)
- **(c)** Only (I) and (II)
- **(d)** Only (III)

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) only (III)**

**Why.** Inserting bubbles (stalling) holds a dependent instruction until its operand is ready. Delayed branching and prediction address control hazards; changing latch latency or cycle time doesn't remove a dependence.

**Concept: data hazard types.** RAW (read after write: true dependence), WAR (write after read: anti-dependence), WAW (write after write: output dependence). In-order 5-stage pipelines only face RAW; out-of-order CPUs remove WAR/WAW with register renaming.

{{< /details >}}

### 8 · Pipelining

*Asked by: Qualcomm (Delhi campus 2024, Q52)*

A processor has five functional units with latencies 20 ns, 16 ns, 20 ns, 20 ns and 14 ns. Pipelining adds 1 ns of latch overhead per stage. What is the speed-up of the pipelined design over the single-cycle datapath?

- **(a)** 4.3
- **(b)** 4.5
- **(c)** 6.0
- **(d)** 6.4

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) 4.3**

**Why.** Single-cycle: one instruction takes the sum of all units, 20 + 16 + 20 + 20 + 14 = 90 ns. Pipelined clock = slowest stage + overhead = 20 + 1 = 21 ns, and in steady state one instruction finishes per cycle. Speed-up = 90/21 ≈ 4.29.

**Concept: pipeline speed-up.** Ideal speed-up = number of stages (5), reduced by unbalanced stages (the clock follows the slowest) and latch overhead.

{{< /details >}}

### 9 · Performance

*Asked by: Qualcomm (BITS Hyderabad 2025, Q46)*

What is the throughput of a 750 MHz processor whose cache miss penalty adds 2.52 cycles per instruction (base CPI 1)?

- **(a)** 716.62 MIPS
- **(b)** 581.84 MIPS
- **(c)** 213 MIPS
- **(d)** 299 MIPS

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) 213 MIPS**

**Why.** Effective CPI = base 1 + 2.52 stall cycles = 3.52. MIPS = clock (MHz)/CPI = 750/3.52 ≈ 213. (299 ≈ 750/2.52 is the trap that forgets the base CPI.)

**Concept: memory stalls add to CPI.** CPI_effective = CPI_base + (misses per instruction × miss penalty). Cache performance often matters more than raw clock speed.

{{< /details >}}

### 10 · instruction dependence

*Asked by: Texas Instruments (BITS Pilani)*

Instruction $j$ writes a register that the earlier instruction $i$ reads. Which dependence?

{{< details title="Answer and explanation" closed="true" >}}

**Answer: anti-dependence (WAR)**

**Why.** j writes a register that the earlier i reads. If j's write happened before i's read, i would read the wrong value: a write-after-read hazard.

**Concept: name dependences.** WAR and WAW occur only because two instructions reuse the same register name, not because data flows between them; renaming to different physical registers removes them.

{{< /details >}}

### 11 · a pipeline

*Asked by: Texas Instruments (IIT ISM 2024)*

Stages take 2, 1, 3, 1 cycles; a new instruction starts every cycle. Cycles for 5 instructions?

- **(a)** 10
- **(b)** 11
- **(c)** 12
- **(d)** 13

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) 11** (as intended)

**Why.** The first instruction takes 2 + 1 + 3 + 1 = 7 cycles; with a new instruction starting every cycle, the remaining 4 each finish one cycle later: 7 + 4 = 11. (Strictly, a 3-cycle stage that is not itself pipelined could accept only one instruction every 3 cycles, which would make it longer.)

**Concept: pipeline timing.** Total cycles for n instructions = (cycles for the first) + (n − 1) × (issue interval), when nothing stalls.

{{< /details >}}
