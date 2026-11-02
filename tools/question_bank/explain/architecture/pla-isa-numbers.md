@@ qcc-dig-27
**Answer: (c) B**

**Why.** The OR line collects the product lines ABC, A′B and ABC′. ABC + ABC′ = AB(C + C′) = AB, and AB + A′B = B(A + A′) = B.

**Concept: PLA.** A programmable logic array has a programmable AND plane (makes product terms) feeding a programmable OR plane (sums them). Read each product line from its crosses, then simplify the sum.

@@ qcc-dig-28
**Answer: no reliable pick** (the correct value Σ(0, 2) = A′C′ is not among the three visible options; pick the fourth if it reads Σ(0, 2))

**Why.** The eight AND rows are the minterms m₀…m₇ in order (row 1 taps A′, B′, C′; row 2 taps A′, B′, C; ...). F1's OR line has crosses on rows m₀ and m₂, so F1 = Σ(0, 2) = A′B′C′ + A′BC′ = A′C′. Σ(1, 4, 7) is F2, and Π(0, 2) is the complement of the right answer.

**Concept: minterm notation.** Σ(list) = OR of the minterms whose numbers (ABC read as binary) are listed. Π(list) = AND of maxterms: the function is 0 exactly at those numbers.

@@ qcc-dig-29
**Answer: (a) programmable AND array, fixed OR array**

**Why.** A CPLD is built from PAL-style macrocells: a programmable AND array feeding fixed OR gates. Both programmable is a PLA; fixed AND with programmable OR is a PROM.

**Concept: programmable logic families.** PROM (fixed AND = full decoder, programmable OR), PAL (programmable AND, fixed OR), PLA (both programmable), CPLD (many PAL blocks + interconnect), FPGA (lookup tables + flip-flops + routing).

@@ ti-bool-pos
**Answer: (c) A′CD′ + AB′CD′ + AB′C′D′**

**Why.** The maxterms list where f = 0, so f = 1 at the missing numbers: 2, 6, 8, 10. A′CD′ covers 0010 and 0110 (2, 6); AB′CD′ is 1010 (10); AB′C′D′ is 1000 (8). (Checked on all 16 inputs; the candidate's (a) is wrong.)

**Concept: switching between Σ and Π.** ΠM(list) = Σm(everything not in the list). Writing the function from its few 1s is often easier.

@@ ti-consensus
**Answer: AC′ + BC**

**Why.** AB is the consensus of AC′ and BC (they disagree only on C; the consensus is the product of the rest, A·B). Whenever AB = 1, either C = 0 (so AC′ = 1) or C = 1 (so BC = 1), so AB is redundant.

**Concept: consensus theorem.** XY + X′Z + YZ = XY + X′Z. The term YZ is covered by the other two and can be dropped. Here X = C′, Y = A, Z = B: C′A + CB + AB = C′A + CB.

@@ ti-demux
**Answer: O₄ = S₂ S₁′ S₀′ · Input**

**Why.** Output 4 is active when the select code is 4 = 100: S₂ = 1, S₁ = 0, S₀ = 0. It then passes the input.

**Concept: DEMUX outputs.** Output k = (minterm k of the select lines) AND the data input.

@@ ti-hazard
**Answer: hazard-free, with no races**

**Why.** Z = A + B′ + C is a single OR of literals: no variable appears in both its true and complemented form, so no input change can make two terms hand over to each other (no static hazard). It is combinational with no feedback, so there are no races.

**Concept: static hazards.** A glitch can occur when an output should stay 1 while one term turns off and another turns on, e.g. AB + A′C when B = C = 1 and A changes. The fix is adding the consensus term (BC).

@@ ti-latch
**Answer: (d) cross-coupling**

**Why.** In a latch, each gate's output feeds the other gate's input. This positive feedback loop holds the state after the inputs return to their resting values.

**Concept: storage from feedback.** Two cross-coupled NOR (or NAND) gates form an SR latch with two stable states: the basic one-bit memory cell.

@@ ti-mux-det
**Answer: (b) 3**

**Why.** A MUX with its output fed back to one input is a latch. Use two such MUX latches, one transparent while the clock is high and one while it is low, and a third MUX, selected by the clock, to output whichever latch is currently holding.

**Concept: dual-edge flip-flops.** Data is captured on both clock edges, doubling data rate at the same clock frequency (the idea behind DDR memory).

@@ ti-xnor
**Answer: f is XNOR: (x + y′)(x′ + y), equivalently xy + x′y′** (the primes in the options are too blurred to pick a letter)

**Why.** xy′ + x′y is XOR; its complement is XNOR. By De Morgan, (xy′ + x′y)′ = (x′ + y)(x + y′).

**Concept: XNOR forms.** XNOR = xy + x′y′ (sum of products) = (x + y′)(x′ + y) (product of sums). 1 when the inputs are equal.

@@ ti-xor-circuit
**Answer: (a) XOR**

**Why.** A′B + AB′ is 1 exactly when A and B differ: XOR.

**Concept: XOR = A′B + AB′.** Built from 2 inverters, 2 ANDs and 1 OR, or from 4 NAND gates.

@@ ti-xor-dff
**Answer: a T flip-flop**

**Why.** With D = X ⊕ Q: if X = 0, D = Q (hold); if X = 1, D = Q′ (toggle). That is exactly a T flip-flop with T = X.

**Concept: flip-flop conversions.** Make the D input equal the target flip-flop's next-state equation: T: D = T ⊕ Q; JK: D = JQ′ + K′Q.

@@ qcc-arch-22
**Answer: (a) only (II), synthesis**

**Why.** Synthesis (design) goes from a specification or truth table to a circuit. Analysis goes the other way: from a given circuit to its Boolean functions.

**Concept: design flow.** Specification → truth table → simplified expressions (K-map) → gates. Analysis reverses it to check or understand an existing circuit.

@@ qcc-arch-38
**Answer: (a) SISD**

**Why.** A classic uniprocessor executes one instruction stream on one data stream.

**Concept: Flynn's taxonomy.** SISD (simple CPU), SIMD (one instruction on many data: vector units, GPUs), MISD (rare, fault-tolerant systems), MIMD (multicore and clusters, each core with its own instructions and data).

@@ qcc-arch-39
**Answer: (c) only (I), (II) and (III)**

**Why.** Tightly coupled systems share a common memory and a shared pool of ready jobs (I, II). Loosely coupled systems give each node private memory and its own queue, communicating by messages (III true, IV false).

**Concept: shared-memory vs distributed systems.** Tightly coupled (SMP multicore): easy communication through memory, limited scale. Loosely coupled (clusters): scale further, but communication costs more.

@@ qcc-dig-79
**Answer: (a) testability**

**Why.** Setting a node to a value from the inputs is controllability; seeing its effect at an output is observability. A fault at a node can be tested only if you can do both, which together is testability.

**Concept: design for test (DFT).** Chips are made easier to test by adding controllability and observability, e.g. scan chains that let a tester set and read every flip-flop.

@@ qcc-dig-80
**Answer: (b) fault models**

**Why.** DFT generates test patterns against fault models (stuck-at-0/1, transition, bridging faults) and measures fault coverage. Timing analysis, delay calculation and silicon debugging belong to other parts of the flow.

**Concept: stuck-at fault model.** Assume a single wire is stuck at 0 or 1; a test pattern "detects" it if the output differs from the fault-free circuit. Fault coverage = detected faults / total faults.

@@ ti-observability
**Answer: fewer test cycles**

**Why.** With high observability, the effect of internal faults is visible at outputs quickly, so fewer patterns and cycles are needed to detect them.

**Concept: controllability and observability** together decide how hard a circuit is to test.

@@ ti-rtl
**Answer: a minimum number of transistors**

**Why.** Resistor–transistor logic uses resistors at the inputs and one transistor per input, so it needs very few transistors (the expensive part in early ICs). Its downsides are low speed, poor fan-out and high power.

**Concept: logic family evolution.** RTL → DTL (diodes at inputs) → TTL (multi-emitter transistors, faster) → CMOS (near-zero static power, dominant today).

@@ ti-rtl-mux
**Answer: (2) and (3)**

**Why.** `c = sel_line ? a : b` on 256-bit buses synthesises to 256 parallel 2:1 multiplexers (3), and the single `sel_line` drives the select input of all 256 (2), a high fan-out net that needs buffering. It is not inherently slow: the MUXes work in parallel.

**Concept: RTL describes hardware, not sequential code.** One line of Verilog can create hundreds of gates; think about the hardware each statement implies (fan-out, width, depth).

@@ ti-sv-fork
**Answer: join_any or join_none** (the loops keep running)

**Why.** With `join`, the parent waits for both loops, which keep resetting each other forever. With `join_any` or `join_none` the parent continues, but the forked loops are still running in the background and keep the simulation alive indefinitely (unless killed with `disable fork`).

**Concept: fork–join variants.** `join`: wait for all threads. `join_any`: wait for the first to finish. `join_none`: don't wait at all. Threads started by fork keep running until they end or are disabled.

@@ ti-vhdl
**Answer: (a) behavioural model of a synchronous D flip-flop**

**Why.** Everything happens inside the rising-edge branch: reset, set and the clock-enabled load all take effect only on the clock edge. So it is a D flip-flop with synchronous reset/set and a clock enable.

**Concept: synchronous vs asynchronous reset.** Synchronous: checked inside the clock-edge condition, acts only at the edge. Asynchronous: in the sensitivity list and checked before the edge condition, acts immediately.

@@ mw-iisc-3
**Answer: (c) to perform arithmetic and logical operations** (as the register used by them)

**Why.** The accumulator holds one operand and receives the result of every ALU operation, arithmetic and logical. (a) and (b) each name only one kind; (d) describes address registers.

**Concept: accumulator architectures.** Early CPUs (8085, 8051) route most operations through one register (A): `ADD B` means A ← A + B. This keeps instructions short.

@@ nv-11
**Answer: (d) it depends on the calling convention** (the handwritten key picks "stack and registers")

**Why.** The ABI decides. 32-bit x86 cdecl passes all arguments on the stack. x86-64 System V passes the first six integer arguments in registers (rdi, rsi, rdx, rcx, r8, r9) and the rest on the stack. ARM passes the first four in r0–r3.

**Concept: calling conventions.** A contract between caller and callee: where arguments and return values go, which registers the callee must preserve, and who cleans up the stack.

@@ qc-n-asm
**Answer: not answerable** (the instruction and format are cut off in the photo)

**Concept: instruction formats.** An instruction has an opcode and operands; the question would specify which operands are sources and which is the destination, and whether there is a condition (like NZ). Read the stated convention before choosing.

@@ qc-n-mov
**Answer: (d) only (III)**

**Why.** MOV takes exactly two operands (destination, source). `MOV SP, AX` is a valid 16-bit register-to-register move. (I) has three operands and (II) only one.

**Concept: MOV rules on x86.** Two operands of the same size; not both memory; no immediate into a segment register; CS cannot be a destination.

@@ qc-n-registers
**Answer: (b) both**

**Why.** In the 8086 the general registers are the data registers (AX, BX, CX, DX) and the pointer and index registers (SP, BP, SI, DI).

**Concept: 8086 register groups.** General (data, pointer, index), segment (CS, DS, SS, ES), instruction pointer (IP) and flags.

@@ qc60-34
**Answer: (d) stack**

**Why.** On a call, the return address (the PC) is pushed onto the stack; on return it is popped. Nested calls return in reverse order, which is exactly LIFO.

**Concept: the call stack.** Each call pushes a frame (return address, saved registers, locals). This is why deep recursion can overflow the stack.

@@ qcc-arch-23
**Answer: (b) only (II) and (III)**

**Why.** ESP (stack pointer) and EBP (base pointer) are the x86 pointer registers. EAX is the accumulator, a general-purpose data register.

**Concept: ESP and EBP.** ESP points to the top of the stack; EBP traditionally marks the start of the current function's frame, so locals and arguments are at fixed offsets from it.

@@ qcc-arch-24
**Answer: (b) only (I) and (III)**

**Why.** EAX, EBX, ECX and EDX are the general-purpose data registers. EIP is the instruction pointer (program counter).

**Concept: x86 register roles.** EAX accumulator, EBX base, ECX counter (loops, shifts), EDX data (multiply/divide), ESI/EDI source/destination index, ESP/EBP stack, EIP next instruction.

@@ qcc-arch-25
**Answer: (c) only (II)**

**Why.** The x86 control flags are TF (trap/single-step), IF (interrupt enable) and DF (direction for string instructions). Sign and carry are status flags, set by ALU results.

**Concept: status vs control flags.** Status flags report the result of the last operation (CF, ZF, SF, OF, PF, AF). Control flags are set by the programmer to change how the CPU behaves.

@@ qcc-arch-26
**Answer: (c) the least significant byte has an even number of 1s**

**Why.** x86's PF looks only at the low 8 bits of the result and is set for even parity.

**Concept: parity.** Counting 1s mod 2. Parity bits detect single-bit errors in transmission; x86 keeps PF for compatibility with the 8080.

@@ qcc-arch-28
**Answer: (d) only (I) and (IV)**

**Why.** Both MOV and LEA are data-transfer instructions (I). LEA loads the computed **address**, not the memory contents, into a register (IV). MOV moves data, not instructions (III false), and neither stores the status word (II false).

**Concept: LEA.** `LEA EAX, [EBX + 4*ECX + 8]` computes the address expression and puts the result in EAX without touching memory. Compilers also use it as a fast add-and-multiply.

@@ qcc-arch-29
**Answer: (d) R4 ← R3 − 3**

**Why.** Reading with the sources first and the destination last (the same convention as `ADD L, M, C`), R3 minus 3 is stored in R4. (In MIPS/ARM style, destination first, it would mean R3 ← 3 − R4, which matches no option.)

**Concept: operand order is a convention.** Intel syntax: destination first; AT&T syntax and some textbook formats: destination last. Always check which one a question uses.

@@ qcc-arch-30
**Answer: (d) add L and M and store the result in C**

**Why.** A three-address instruction names two sources and a destination: C ← L + M, in one instruction with no intermediate moves.

**Concept: 0-, 1-, 2- and 3-address instructions.** 3-address: `ADD C, A, B`. 2-address: `ADD A, B` (A ← A + B). 1-address: accumulator machines (`ADD B`). 0-address: stack machines (`ADD` pops two, pushes one).

@@ qcc-arch-31
**Answer: (d) 55H**

**Why.** LDA 1000H loads A = AAH = 1010 1010. CMA complements A: 0101 0101 = 55H. STA 2000H stores it.

**Concept: complement in hex.** The 1's complement of a hex digit d is F − d: A → 5, so AAH → 55H.

@@ qcc-arch-44
**Answer: (a) asynchronous bus**

**Why.** An asynchronous bus coordinates transfers with request/acknowledge handshake signals instead of a common clock, so devices of different speeds can share it.

**Concept: synchronous vs asynchronous buses.** Synchronous: every transfer takes a fixed number of clock cycles (simple, fast, but all devices must keep up). Asynchronous: each transfer is paced by handshakes (flexible, more control signals).

@@ qcc-dig-78
**Answer: (c) ROM**

**Why.** A hardwired control unit is built from gates, decoders and a step counter. A ROM holding control words is the control memory of a **microprogrammed** control unit.

**Concept: hardwired vs microprogrammed control.** Hardwired: fast, fixed logic (RISC). Microprogrammed: each instruction runs a small program of control words from ROM; easier to change and to support complex instructions (classic CISC).

@@ ti-risc
**Answer: (b) 5**

**Why.** The classic RISC pipeline has five stages: instruction fetch (IF), decode/register read (ID), execute (EX), memory access (MEM), write back (WB).

**Concept: the 5-stage pipeline.** Each stage takes one cycle, so up to five instructions are in flight at once and, ideally, one completes every cycle.

@@ ti-shift-register
**Answer: cannot be determined** (the gate inputs are illegible in the photo)

**Concept: feedback shift registers.** The next serial input is a function of the current bits; the sequence of states eventually repeats. For linear feedback (XOR) with a good choice of taps, an n-bit register cycles through 2ⁿ − 1 states.

@@ qc-iisc-1cde
**Answer: the true value is 7390; the intended option is (c) 7391** (the options are off by one)

**Why.** 1CDE₁₆ = 1 × 4096 + 12 × 256 + 13 × 16 + 14 = 4096 + 3072 + 208 + 14 = 7390.

**Concept: positional value.** A digit's value = digit × base^(position). In hex, positions are worth 1, 16, 256, 4096, ...; letters A–F are 10–15.

@@ qc-iisc-4ed
**Answer: (b) 0100 1110 1101**

**Why.** Each hex digit is exactly 4 bits: 4 = 0100, E = 1110, D = 1101.

**Concept: hex ↔ binary.** Because 16 = 2⁴, convert digit by digit in groups of four bits; no arithmetic needed.

@@ qc-iisc-hex
**Answer: (c) 1A85₁₆**

**Why.** Repeated division by 16: 6789 = 424 × 16 + 5; 424 = 26 × 16 + 8; 26 = 1 × 16 + 10 (A); 1. Read the remainders bottom-up: 1, A, 8, 5.

**Concept: decimal → base b.** Divide by b repeatedly and collect remainders; the last remainder is the most significant digit. Check: 1 × 4096 + 10 × 256 + 8 × 16 + 5 = 6789.

@@ qc-n-octal
**Answer: (d) 366₁₀**

**Why.** 556₈ = 5 × 64 + 5 × 8 + 6 = 320 + 40 + 6 = 366.

**Concept: octal digits are 0–7.** Positions are worth 1, 8, 64, 512, ... (Option (a) writes the decimal value with a wrong base label.)

@@ qc-n-sdword
**Answer: (c) SDWORD**

**Why.** In MASM: BYTE/SBYTE are 8-bit, WORD/SWORD 16-bit, DWORD/SDWORD 32-bit; the S prefix means signed.

**Concept: data sizes.** Byte 8 bits, word 16, double word 32, quad word 64 (in x86 naming, from the original 16-bit 8086).

@@ qc25-and
**Answer: (c) 23**

**Why.** ANDing a number with itself keeps every bit unchanged: x & x = x.

**Concept: bitwise identities.** x & x = x, x | x = x, x ^ x = 0, x & 0 = 0, x | 0 = x.

@@ qc25-hex
**Answer: (c) DBh**

**Why.** Split into groups of four from the right: 1101 = D, 1011 = B.

**Concept: binary → hex** in 4-bit groups.

@@ qc60-21
**Answer: (b) 175**

**Why.** Group in fours from the right: 1 | 0111 | 0101 → 1, 7, 5 → 175₁₆. (Pad the leftmost group with zeros: 0001.)

**Concept: always group from the right** (the least significant end); padding goes on the left.

@@ qc60-30
**Answer: (b) 35FA**

**Why.** 0011 = 3, 0101 = 5, 1111 = F, 1010 = A.

**Concept: binary → hex** in 4-bit groups.

@@ qc60-50
**Answer: (a) 6Eh**

**Why.** 110 | 1110 → 0110 = 6, 1110 = E.

**Concept: binary → hex**, padding the left group with zeros.

@@ qcc-arch-01
**Answer: (b) 3.625**

**Why.** Integer part 011 = 3. Fraction .101 = 1 × 2⁻¹ + 0 × 2⁻² + 1 × 2⁻³ = 0.5 + 0.125 = 0.625. Total 3.625.

**Concept: binary fractions.** Places after the point are worth 1/2, 1/4, 1/8, ... Some decimal fractions (like 0.1) have no exact binary form, which is why floating-point rounding errors occur.

@@ qcc-arch-02
**Answer: (b) 2955**

**Why.** 5 × 512 + 6 × 64 + 1 × 8 + 3 = 2560 + 384 + 8 + 3 = 2955.

**Concept: octal place values** are powers of 8: 1, 8, 64, 512.

@@ qcc-arch-03
**Answer: (c) 7896**

**Why.** Group into hex from the right: 1 | 1110 | 1101 | 1000 = 1ED8₁₆ = 4096 + 14 × 256 + 13 × 16 + 8 = 4096 + 3584 + 208 + 8 = 7896.

**Concept: use hex as a shortcut.** Converting a long binary number to hex first, then to decimal, means far fewer terms to add.

@@ qcc-arch-04
**Answer: (b) 2AAB₁₆**

**Why.** Group in fours from the right: 10 | 1010 | 1010 | 1011 = 2, A, A, B.

**Concept: binary → hex** in 4-bit groups from the right.

@@ qcc-arch-05
**Answer: (d) 4755₈**

**Why.** 9ED₁₆ = 1001 1110 1101. Regroup in threes from the right: 100 111 101 101 = 4, 7, 5, 5.

**Concept: hex ↔ octal via binary.** Hex digits are 4 bits and octal digits 3 bits, so go through binary and regroup.

@@ qcc-arch-06
**Answer: (c) 6D**

**Why.** 109 = 6 × 16 + 13, and 13 is D.

**Concept: decimal → hex** by dividing by 16 (quotient and remainder).

@@ qcc-arch-07
**Answer: (a) 11001001**

**Why.** +55 = 0011 0111. Invert all bits: 1100 1000. Add 1: 1100 1001.

**Concept: two's complement.** −x is (invert all bits of x) + 1. Check: the MSB is 1 (negative), and 11001001 = −128 + 73 = −55. Two's complement lets the same adder handle signed and unsigned numbers.

@@ qcc-arch-08
**Answer: (d) 1111 1111 1111 1111 1100 1000**

**Why.** +56 = 0011 1000. Invert and add 1 (8 bits): 1100 1000. Sign-extend to 24 bits by filling with copies of the sign bit (1s). (Option (c) is −24.)

**Concept: sign extension.** To widen a two's complement number, copy its sign bit into the new high bits; the value stays the same.

@@ qcc-arch-09
**Answer: (b) 0100001**

**Why.** 95 = 101 1111 (7 bits). Invert: 010 0000. Add 1: 010 0001.

**Concept: two's complement as an operation.** "2's complement of x" means 2ⁿ − x: here 128 − 95 = 33 = 0100001.

@@ qcc-dig-01
**Answer: (c) BCD**

**Why.** Excess-3 is BCD + 3. It is self-complementing (the 9's complement of a digit is its bitwise inverse), and a decimal carry out of a digit appears as a natural binary carry, which makes BCD addition and subtraction easy.

**Concept: BCD codes.** BCD stores each decimal digit in 4 bits (8421). XS-3 adds 3 to each digit; Gray code changes one bit between consecutive values.

@@ qcc-dig-02
**Answer: (c) B₂′B₁ + B₁′B₂**

**Why.** Treat the subscript as the bit weight (B₀ = LSB). XS-2 = BCD + 0010. Bit 0 is unchanged; bit 1 is inverted, with a carry into bit 2 when B₁ = 1. So A₂ = B₂ ⊕ B₁ = B₂′B₁ + B₁′B₂.

**Concept: code converters as adders.** Adding a constant bit by bit: each output bit is the input bit XOR the carry coming in, and carries propagate only where the constant has 1s or earlier carries.

@@ qcc-dig-03
**Answer: (a) 35C**

**Why.** 771₈ = 7 × 64 + 7 × 8 + 1 = 505; 543₈ = 5 × 64 + 4 × 8 + 3 = 355. Sum 860 = 3 × 256 + 5 × 16 + 12 = 35C₁₆. (1534 is the sum in octal.)

**Concept: convert to one base before adding** (or add in octal, then convert). Watch which base the answer is asked in.

@@ qcc-dig-04
**Answer: (c) all three**

**Why.** Every code word has exactly two 1s out of five bits (III), so the number of 1s is always even (I). It is usually listed as non-weighted: the 0-1-2-4-7 weights fit every digit except 0 (11000) (II).

**Concept: error-detecting codes.** A 2-out-of-5 code detects any single-bit error (the count of 1s would change). C(5, 2) = 10 code words, exactly enough for the decimal digits.

@@ ti-dynamic-power
**Answer: (c) signed magnitude**

**Why.** Dynamic power grows with how many bits toggle. A small swing across 0 in signed magnitude flips only the sign bit and a few low bits. In two's complement, going from +1 (0000...01) to −1 (1111...11) toggles every bit.

**Concept: switching activity.** CMOS dynamic power ∝ α C V² f, where α is how often bits toggle. Choosing encodings that toggle fewer bits for typical data saves power.

@@ ti-signmag
**Answer: (c) 11111**

**Why.** Sign-magnitude uses a sign bit (1 = negative) followed by the magnitude: 15 = 1111, so −15 = 1 1111.

**Concept: signed number formats.** Sign-magnitude (sign bit + value; has +0 and −0), 1's complement (invert bits; also two zeros), 2's complement (invert + 1; one zero, used by all modern CPUs).
