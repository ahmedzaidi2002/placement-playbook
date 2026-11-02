---
title: "HDL (Verilog, VHDL, SystemVerilog)"
weight: 8
---

3 questions asked by Texas Instruments. Try each one first, then open the toggle: it gives the answer, why it is right, and the idea behind it explained from scratch.

### 1 · a 256-bit select

*Asked by: Texas Instruments (NIT Calicut 2023)*

```c
wire [255:0] a, b, c;
assign c = sel_line ? a : b;
```

Which follow? (1) a slow design;
(2) `sel_line` drives 256 loads; (3) 256 parallel MUXes.

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (2) and (3)**

**Why.** `c = sel_line ? a : b` on 256-bit buses synthesises to 256 parallel 2:1 multiplexers (3), and the single `sel_line` drives the select input of all 256 (2), a high fan-out net that needs buffering. It is not inherently slow: the MUXes work in parallel.

**Concept: RTL describes hardware, not sequential code.** One line of Verilog can create hundreds of gates; think about the hardware each statement implies (fan-out, width, depth).

{{< /details >}}

### 2 · SystemVerilog fork and join

*Asked by: Texas Instruments (IISc 2023)*

Two loops share `int a` inside `fork ... join X` (one counts up with `#20`,
one down with `#10`). For which X does the simulation loop forever?

{{< details title="Answer and explanation" closed="true" >}}

**Answer: join_any or join_none** (the loops keep running)

**Why.** With `join`, the parent waits for both loops, which keep resetting each other forever. With `join_any` or `join_none` the parent continues, but the forked loops are still running in the background and keep the simulation alive indefinitely (unless killed with `disable fork`).

**Concept: fork–join variants.** `join`: wait for all threads. `join_any`: wait for the first to finish. `join_none`: don't wait at all. Threads started by fork keep running until they end or are disabled.

{{< /details >}}

### 3 · what does this VHDL describe?

*Asked by: Texas Instruments (NIT Calicut 2023)*

In `process(CLK)`, on a rising edge of CLK: if RESET is 1 then Q gets 0, else if SET is 1
then Q gets 1, else if CE is 1 then Q gets D.

- **(a)** Behavioural model of a synchronous D flip-flop
- **(b)** Behavioural model of an asynchronous D flip-flop
- **(c)** A 4-bit synchronous up counter
- **(d)** None of these

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) behavioural model of a synchronous D flip-flop**

**Why.** Everything happens inside the rising-edge branch: reset, set and the clock-enabled load all take effect only on the clock edge. So it is a D flip-flop with synchronous reset/set and a clock enable.

**Concept: synchronous vs asynchronous reset.** Synchronous: checked inside the clock-edge condition, acts only at the edge. Asynchronous: in the sensitivity list and checked before the edge condition, acts immediately.

{{< /details >}}
