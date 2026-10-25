---
title: "10 · Interview rapid-fire"
linkTitle: "10 Rapid-fire"
weight: 10
math: true
---
## 10.1 Data and logic {#coa-10-1}

1. **Why 2's complement?** One zero, and the same adder does addition and subtraction.
2. **Range of 8-bit 2's complement?** −128 to 127.
3. **When does signed addition overflow?** Two same-sign operands give a result of the other sign.
4. **IEEE single-precision layout?** 1 sign, 8 exponent (bias 127), 23 fraction bits.
5. **Why is 0.1 + 0.2 ≠ 0.3?** 0.1 and 0.2 have no exact binary representation; rounding errors.
6. **Big vs little endian?** Most significant byte at the lowest address vs least significant first (x86).
7. **Why padding in structs?** Alignment: fields sit at multiples of their size so the CPU can load them in one access.
8. **Universal gates?** NAND and NOR.
9. **De Morgan's laws?** $\overline{AB} = \overline{A} + \overline{B}$, $\overline{A+B} = \overline{A}\,\overline{B}$.
10. **Latch vs flip-flop?** Level-triggered vs edge-triggered.
11. **JK with J = K = 1?** Toggles.
12. **Ripple vs synchronous counter?** Each flip-flop clocks the next (slow, delays add) vs a shared clock (fast).
13. **Mealy vs Moore?** Outputs depend on state and inputs vs on state only.
14. **Why carry-lookahead?** Computes carries in parallel instead of waiting for a ripple.

## 10.2 ISA and pipelining {#coa-10-2}

15. **RISC vs CISC?** Few simple fixed-length instructions with load/store vs many complex variable-length instructions.
16. **Hardwired vs microprogrammed control?** Logic circuits (fast, RISC) vs control memory (flexible, CISC).
17. **What does the program counter hold?** The address of the next instruction.
18. **Direct vs indirect addressing?** The field is the operand's address vs the address of the address.
19. **Why PC-relative addressing?** Short branch offsets and position-independent code.
20. **What does pipelining improve?** Throughput, not single-instruction latency.
21. **Three kinds of hazards?** Structural, data, control.
22. **What is forwarding?** Passing a result straight from a later stage to an earlier one, avoiding stalls.
23. **Load-use hazard?** A loaded value needed by the next instruction: 1 stall even with forwarding.
24. **RAW, WAR, WAW?** True dependence vs anti vs output; renaming removes WAR and WAW.
25. **2-bit branch predictor?** Changes its prediction only after two wrong guesses.
26. **Superscalar?** Issues more than one instruction per cycle.

## 10.3 Memory, I/O, performance {#coa-10-3}

27. **Temporal vs spatial locality?** Reuse of the same data soon vs use of nearby data soon.
28. **SRAM vs DRAM?** Fast, no refresh, caches vs dense, cheap, needs refresh, main memory.
29. **Direct-mapped vs set-associative vs fully associative?** One possible line vs one of $k$ in a set vs anywhere.
30. **Three C's of misses?** Compulsory, capacity, conflict.
31. **Write-through vs write-back?** Write memory every time vs only on eviction (dirty bit).
32. **AMAT formula?** Hit time + miss rate × miss penalty.
33. **What is cache coherence?** Keeping copies in different cores' caches consistent (MESI).
34. **False sharing?** Different variables in one cache line written by different cores.
35. **Programmed I/O vs interrupts vs DMA?** Polling vs interrupt per word vs block transfer with one interrupt.
36. **Cycle stealing?** DMA takes the bus one word at a time between CPU cycles.
37. **Memory-mapped vs isolated I/O?** Devices at memory addresses vs a separate I/O space with IN/OUT.
38. **Iron law?** Time = instructions × CPI × clock period.
39. **Amdahl's law?** Speed-up ≤ 1/(serial fraction).
40. **Why multicore instead of faster clocks?** Power grows with V²f (the power wall).
41. **Flynn's classes?** SISD, SIMD, MISD, MIMD.

<div class="nb nb-moral">

Forty-one answers under twenty seconds each cover the COA theory part of most interviews; chapter 11 has the numericals.

</div>
