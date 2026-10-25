---
title: "14 · Interview rapid-fire"
linkTitle: "14 Interview rapid-fire"
weight: 14
math: true
---
Short answers to the questions that come up again and again, in the words a strong candidate would use out loud. Each points to the section that explains it.

## 14.1 Data representation {#s14-1}

1. <strong>Why two’s complement?</strong><br>One zero, the same adder for signed and unsigned, subtraction as $a + \bar b + 1$, and sign extension by copying the top bit ([Section 1.2](../01-data/#sec-coa-signed)).
2. <strong>Range of an $n$-bit two’s-complement number?</strong><br>$-2^{n-1}$ to $2^{n-1}-1$; one more negative value than positive, so $-(\text{INT\_MIN})$ overflows.
3. <strong>When does a signed addition overflow?</strong><br>When both operands have the same sign and the result has the other; in hardware, $V = c_{n-1} \oplus c_n$.
4. <strong>Carry flag vs overflow flag?</strong><br>$C$ is unsigned overflow (carry out of the top bit), $V$ is signed overflow. The same addition can set either, both or neither.
5. <strong>Layout of an IEEE single?</strong><br>1 sign, 8 exponent (bias 127), 23 fraction bits with a hidden leading 1: 24 bits of precision, about 7 decimal digits ([Section 1.3](../01-data/#sec-coa-ieee)).
6. <strong>Why is `0.1 + 0.2 != 0.3`?</strong><br>None of the three is exactly representable in binary; the rounded sum differs from the rounded $0.3$ by one ulp. Compare with a tolerance.
7. <strong>What are subnormals for?</strong><br>Gradual underflow: exponent field $0$ means $0.F \times 2^{-126}$, filling the gap between $0$ and the smallest normal so that $x - y = 0$ only when $x = y$.
8. <strong>Largest integer a float holds exactly in sequence?</strong><br>$2^{24}$; $2^{24}+1$ rounds back to $2^{24}$. For doubles, $2^{53}$.
9. <strong>NaN == NaN?</strong><br>False; a NaN compares unequal to everything, itself included. Test with `isnan`.
10. <strong>Little vs big endian?</strong><br>Little-endian puts the least significant byte at the lowest address (x86, ARM in practice); network byte order is big-endian ([Section 1.5](../01-data/#sec-coa-layout)).
11. <strong>Why does a struct have padding?</strong><br>So every member is naturally aligned; tail padding keeps array elements aligned. Order members by decreasing size to minimise it.
12. <strong>`x & (x-1)`?</strong><br>Clears the lowest set bit; zero exactly when $x$ is $0$ or a power of two.
13. <strong>Which number format minimises switching power for small signals around zero?</strong><br>Sign-magnitude: a sign change flips only the sign bit and a few low bits, while two’s complement flips all the high bits ([Section 1.7](../01-data/#sec-coa-lowpower)).

## 14.2 Digital logic {#s14-2}

14. <strong>Universal gates?</strong><br>NAND and NOR: each can build NOT, AND and OR alone. AND/OR alone cannot make NOT ([Section 2.2](../02-boolean/#sec-coa-universal)).
15. <strong>How many 2-input NANDs for an XOR?</strong><br>Four.
16. <strong>Consensus theorem?</strong><br>$AB + \bar AC + BC = AB + \bar AC$; the redundant term $BC$ is what removes a static hazard.
17. <strong>What is a static-1 hazard?</strong><br>A momentary $0$ on an output that should stay $1$ when one input changes, because two paths of opposite polarity have different delays; fixed by covering adjacent $1$s with a common term ([Section 2.5](../02-boolean/#sec-coa-hazards)).
18. <strong>Minterm vs maxterm lists?</strong><br>$\sum m$ lists the $1$s, $\prod M$ the $0$s; the two lists are complementary.
19. <strong>Why Gray code on K-map axes and in FIFOs?</strong><br>Adjacent values differ in one bit, so adjacency is visible and a value sampled mid-change is either the old or the new one.
20. <strong>Mux vs decoder vs demux?</strong><br>A mux selects one input to the output; a decoder raises one of $2^n$ outputs; a demux routes one input to the selected output (a decoder with data as enable).
21. <strong>Ripple-carry vs carry-lookahead?</strong><br>Ripple carry waits $2$ gate delays per bit; lookahead computes carries from generate/propagate signals in a constant number of levels per block ([Section 3.2](../03-combinational/#sec-coa-cla)).
22. <strong>Latch vs flip-flop?</strong><br>A latch is level-sensitive (transparent while enabled); a flip-flop samples at a clock edge ([Section 4.1](../04-sequential/#sec-coa-latches)).
23. <strong>What holds a NOR latch? A NAND latch?</strong><br>Both inputs $0$ for NOR, both $1$ for NAND: the non-controlling values.
24. <strong>When does a master–slave flip-flop’s output change?</strong><br>At the clock edge that closes the master and opens the slave, the falling edge in the usual arrangement.
25. <strong>What is race-around?</strong><br>A level-triggered JK with $J = K = 1$ toggles repeatedly while the clock is high; master–slave or edge triggering cures it.
26. <strong>D flip-flop with $D = \bar Q$?</strong><br>Toggles every edge: divides the clock frequency by 2.
27. <strong>$D = X \oplus Q$?</strong><br>A T flip-flop with $T = X$.
28. <strong>Maximum period of an $n$-bit LFSR?</strong><br>$2^n - 1$; the all-zero state locks it up.
29. <strong>Ripple vs synchronous counter?</strong><br>Ripple stages clock each other, so the count settles after $n$ delays with false intermediate states; synchronous counters change all bits on one clock.
30. <strong>Mealy vs Moore?</strong><br>Mealy outputs depend on state and input (fewer states, react in the same cycle); Moore outputs depend on state only (registered, one cycle later).
31. <strong>Setup vs hold?</strong><br>Setup: data stable before the edge (limits $f_{\max}$); hold: data stable after the edge (independent of the clock period) ([Section 4.6](../04-sequential/#sec-coa-timing)).
32. <strong>How does clock skew affect timing?</strong><br>Capture clock later than launch helps setup and hurts hold.
33. <strong>Can you fix a hold violation by slowing the clock?</strong><br>No; add delay in the data path.
34. <strong>What is metastability?</strong><br>An unresolved state when setup/hold are violated; reduced exponentially by giving it time to resolve, as in a two-flip-flop synchronizer.
35. <strong>Blocking vs nonblocking in Verilog?</strong><br>`=` updates immediately; `<=` updates all targets at the end of the time step. Use `<=` for flip-flops ([Section 4.7](../04-sequential/#sec-coa-hdl)).
36. <strong>`join` vs `join_any` vs `join_none`?</strong><br>Wait for all threads, for the first, or not at all.
37. <strong>What do observability and controllability buy you in test?</strong><br>Fewer test vectors and cycles for the same fault coverage; scan chains maximise both.

## 14.3 ISA, datapath and control {#s14-3}

38. <strong>What is an ISA?</strong><br>The hardware/software contract: instructions, registers, addressing modes, memory model, exceptions; not the implementation.
39. <strong>What is the accumulator for?</strong><br>It holds one implicit operand and the result of ALU operations, so instructions need only one address ([Section 5.1](../05-isa/#sec-coa-formats)).
40. <strong>RISC vs CISC in one line?</strong><br>RISC: few simple fixed-length instructions, load–store, many registers, easy to pipeline; CISC: rich variable-length instructions with memory operands.
41. <strong>Which addressing mode makes position-independent code possible?</strong><br>PC-relative (and base-register addressing).
42. <strong>Is `MOV SP, AX` legal on x86? `MOV [BX], [SI]`?</strong><br>The first yes; the second no: at most one memory operand ([Section 5.4](../05-isa/#sec-coa-x86)).
43. <strong>General registers on the 8086?</strong><br>Data registers AX, BX, CX, DX and pointer/index registers SP, BP, SI, DI.
44. <strong>Where are function arguments?</strong><br>x86-64 System V: first six integer arguments in `rdi, rsi, rdx, rcx, r8, r9`, the rest on the stack; 32-bit cdecl: all on the stack ([Section 5.6](../05-isa/#sec-coa-calling)).
45. <strong>Caller-saved vs callee-saved?</strong><br>The caller must preserve caller-saved registers itself across a call; a callee must restore callee-saved registers it uses.
46. <strong>Single-cycle vs multi-cycle datapath?</strong><br>Single-cycle: CPI 1, clock set by the slowest instruction; multi-cycle: short clock, CPI $> 1$, units reused.
47. <strong>Hardwired vs microprogrammed control?</strong><br>Gates (fast, rigid) vs control words in a ROM (flexible, slower) ([Section 6.3](../06-control/#sec-coa-microprog)).
48. <strong>Horizontal vs vertical microcode?</strong><br>One bit per signal (wide, parallel) vs encoded fields (narrow, needs decoders).

## 14.4 Pipelining and performance {#s14-4}

49. <strong>Does pipelining reduce instruction latency?</strong><br>No; it raises throughput and usually increases latency ([Section 7.1](../07-pipeline/#sec-coa-pipetiming)).
50. <strong>Time for $n$ instructions on a $k$-stage pipeline?</strong><br>$(k + n - 1)$ cycles; the clock is the slowest stage plus latch overhead.
51. <strong>The three hazards?</strong><br>Structural (resources), data (operands), control (next PC).
52. <strong>RAW, WAR, WAW?</strong><br>True, anti and output dependences; only RAW is fundamental, renaming removes the other two.
53. <strong>Which stall survives forwarding in the 5-stage MIPS?</strong><br>The load-use stall: one cycle.
54. <strong>What is a branch delay slot?</strong><br>The instruction after a branch that always executes; the compiler fills it with useful work or a NOP.
55. <strong>1-bit vs 2-bit predictor on a loop?</strong><br>Two mispredictions per loop vs one ([Section 7.4](../07-pipeline/#sec-coa-branchpred)).
56. <strong>What is a BTB?</strong><br>A cache of branch targets indexed by PC, so a taken branch can redirect fetch in IF.
57. <strong>Precise exception?</strong><br>Everything before the faulting instruction completed, nothing after it changed state; needed for restartable page faults.
58. <strong>What does a reorder buffer do?</strong><br>Lets instructions execute out of order but commit in order, keeping exceptions precise and making speculation undoable.
59. <strong>Superscalar vs VLIW?</strong><br>Hardware finds parallel instructions at run time vs the compiler packs them into one long instruction.
60. <strong>Iron law?</strong><br>Time $=$ IC $\times$ CPI $/ f$ ([Section 11.1](../11-perf/#sec-coa-ironlaw)).
61. <strong>Why is MIPS a bad metric?</strong><br>It ignores instruction count: more, simpler instructions raise MIPS and can still run slower.
62. <strong>Amdahl’s law?</strong><br>$1/((1-p) + p/s)$; the serial fraction caps the speed-up at $1/(1-p)$.
63. <strong>Gustafson’s law?</strong><br>Scaled speed-up $(1-p) + pn$ when the problem grows with $n$.
64. <strong>Dynamic power?</strong><br>$\alpha C V^2 f$; scaling $V$ and $f$ together cuts power cubically ([Section 11.3](../11-perf/#sec-coa-power)).

## 14.5 Memory, I/O and parallel hardware {#s14-5}

65. <strong>Temporal vs spatial locality?</strong><br>Reuse of the same item soon vs use of nearby items soon; caches keep recent data and fetch whole lines ([Section 9.1](../09-memory/#sec-coa-locality)).
66. <strong>SRAM vs DRAM?</strong><br>Six-transistor latch, fast, no refresh, caches vs one transistor and a capacitor, dense, refreshed, main memory.
67. <strong>Why must DRAM write back after a read?</strong><br>The read shares the cell’s charge with the bit line and destroys it; the sense amplifier restores it.
68. <strong>Memory with 16 address and 8 data lines?</strong><br>$2^{16}$ bytes, 64 KB.
69. <strong>Low-order interleaving?</strong><br>The low address bits pick the module, so consecutive words are in different modules and can be accessed in parallel.
70. <strong>Flash facts?</strong><br>Non-volatile, erase-before-write in blocks, limited endurance, wear levelling; NOR for code, NAND for storage.
71. <strong>Address split of a cache?</strong><br>Tag | set index | block offset, with index bits $= \log_2(\text{lines}/\text{ways})$ ([Section 9.3](../09-memory/#sec-coa-cacheorg)).
72. <strong>Direct mapped vs set associative vs fully associative?</strong><br>One place per block, $k$ places, anywhere; more ways, fewer conflict misses, more comparators.
73. <strong>The 3Cs?</strong><br>Compulsory (first touch), capacity (working set too big), conflict (too many blocks in one set); plus coherence misses ([Section 9.7](../09-memory/#sec-coa-3c)).
74. <strong>Write-through vs write-back?</strong><br>Update memory on every write vs only on eviction of a dirty line.
75. <strong>Write-allocate?</strong><br>On a write miss, fetch the block into the cache, then write.
76. <strong>AMAT with two levels?</strong><br>$t_1 + m_1(t_2 + m_2 t_m)$; the fraction reaching memory is $m_1 m_2$ ([Section 9.6](../09-memory/#sec-coa-amat)).
77. <strong>Local vs global miss rate of L2?</strong><br>Misses over L2’s accesses vs misses over all accesses.
78. <strong>Why is column-wise traversal of a C matrix slow?</strong><br>C is row-major; column order uses one element per fetched line and evicts lines before reuse ([Section 9.8](../09-memory/#sec-coa-cachecode)).
79. <strong>What is false sharing?</strong><br>Different variables written by different cores in one cache line; coherence bounces the line. Pad to the line size.
80. <strong>VIPT and its size limit?</strong><br>Index with virtual bits, tag with physical; synonym-free when size$/$ways $\le$ page size ([Section 9.9](../09-memory/#sec-coa-vipt)).
81. <strong>MESI’s E state?</strong><br>Exclusive clean: a later write needs no bus transaction.
82. <strong>Polling vs interrupts vs DMA?</strong><br>CPU waits and moves data vs device signals, CPU moves data vs controller moves data and interrupts at the end ([Chapter 10](../10-io/)).
83. <strong>Cycle stealing vs burst DMA?</strong><br>One bus cycle at a time vs the whole block while the CPU waits.
84. <strong>Vectored interrupt?</strong><br>The source supplies an index into a table of ISR addresses.
85. <strong>Daisy chain?</strong><br>Shared request line, acknowledge passed device to device; priority by position.
86. <strong>Memory-mapped vs port-mapped I/O?</strong><br>Device registers in the memory address space (ordinary loads/stores) vs a separate I/O space (`IN`/`OUT`).
87. <strong>Flynn’s classes?</strong><br>SISD, SIMD, MISD, MIMD ([Section 12.1](../12-parallel/#sec-coa-flynn)).
88. <strong>SC vs TSO?</strong><br>SC keeps every thread’s order globally; TSO (x86) lets a store wait in the store buffer while later loads proceed ([Section 12.3](../12-parallel/#sec-coa-consistency)).
89. <strong>What is a warp and why does divergence hurt?</strong><br>32 threads executing one instruction in lock step; divergent paths execute one after another with lanes masked.
90. <strong>NUMA?</strong><br>Memory attached to each socket; remote accesses are slower, so place data near the thread.
91. <strong>What does `volatile` guarantee?</strong><br>Every access in the source happens, in order among volatile accesses; not atomicity, not inter-core ordering ([Section 13.1](../13-embedded/#sec-coa-volatile)).
92. <strong>Why kick a watchdog from the main loop and not from a timer ISR?</strong><br>The ISR keeps running when the main loop hangs, so the watchdog would never fire.
