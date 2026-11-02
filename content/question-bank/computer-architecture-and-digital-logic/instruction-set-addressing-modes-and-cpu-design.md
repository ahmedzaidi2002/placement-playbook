---
title: "Instruction set, addressing modes and CPU design"
weight: 4
---

18 questions asked by MathWorks, NVIDIA, Qualcomm, Texas Instruments. Try each one first, then open the toggle: it gives the answer, why it is right, and the idea behind it explained from scratch.

### 1 · Q3, accumulator

*Asked by: MathWorks (IISc 2024)*

What is the purpose of the accumulator?

- **(a)** Storing data and performing logical operations
- **(b)** Storing data and performing arithmetic operations
- **(c)** Perform arithmetic and logical operations
- **(d)** Store address and data

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) to perform arithmetic and logical operations** (as the register used by them)

**Why.** The accumulator holds one operand and receives the result of every ALU operation, arithmetic and logical. (a) and (b) each name only one kind; (d) describes address registers.

**Concept: accumulator architectures.** Early CPUs (8085, 8051) route most operations through one register (A): `ADD B` means A ← A + B. This keeps instructions short.

{{< /details >}}

### 2 · Q11, where arguments live

*Asked by: NVIDIA (SSE NCG, Nov 2024)*

Where are the arguments passed to a function stored?

- **(a)** Stack
- **(b)** Registers
- **(c)** Stack and Registers
- **(d)** Depends on the calling convention

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) it depends on the calling convention** (the handwritten key picks "stack and registers")

**Why.** The ABI decides. 32-bit x86 cdecl passes all arguments on the stack. x86-64 System V passes the first six integer arguments in registers (rdi, rsi, rdx, rcx, r8, r9) and the rest on the stack. ARM passes the first four in r0–r3.

**Concept: calling conventions.** A contract between caller and callee: where arguments and return values go, which registers the callee must preserve, and who cleans up the stack.

{{< /details >}}

### 3 · assembly representation

*Asked by: Qualcomm (Nov 2024)*

The question begins "Add the value ..." and asks "Which one of the given options is the
correct representation ..."; the rest is [cut off in the source].

- **(a)** SUB [1],4,5
- **(b)** NZ 4, 5, SUB [0], [1], [2]
- **(c)** ADD [0],[1],[2],NZ,4,5
- **(d)** SUB [1][0],4,5

{{< details title="Answer and explanation" closed="true" >}}

**Answer: not answerable** (the instruction and format are cut off in the photo)

**Concept: instruction formats.** An instruction has an opcode and operands; the question would specify which operands are sources and which is the destination, and whether there is a condition (like NZ). Read the stated convention before choosing.

{{< /details >}}

### 4 · MOV instructions

*Asked by: Qualcomm (Nov 2024); Qualcomm (BITS Hyderabad 2025, Q26)*

Which of the instruction(s) given below is/are correct? (I) `MOV BL, AL, DL`
(II) `MOV BH` (III) `MOV SP, AX`

- **(a)** Only (I)
- **(b)** Only (I) and (II)
- **(c)** Only (II) and (III)
- **(d)** Only (III)

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) only (III)**

**Why.** MOV takes exactly two operands (destination, source). `MOV SP, AX` is a valid 16-bit register-to-register move. (I) has three operands and (II) only one.

**Concept: MOV rules on x86.** Two operands of the same size; not both memory; no immediate into a segment register; CS cannot be a destination.

{{< /details >}}

### 5 · Q49, general registers

*Asked by: Qualcomm (Nov 2024)*

Which of these is/are general register(s)? (I) Data registers. (II) Pointer registers.

- **(a)** Only (II)
- **(b)** Both (I) and (II)
- **(c)** Only (I)
- **(d)** Neither (I) nor (II)

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) both**

**Why.** In the 8086 the general registers are the data registers (AX, BX, CX, DX) and the pointer and index registers (SP, BP, SI, DI).

**Concept: 8086 register groups.** General (data, pointer, index), segment (CS, DS, SS, ES), instruction pointer (IP) and flags.

{{< /details >}}

### 6 · Computer Architecture

*Asked by: Qualcomm (60-question online assessment)*

Whenever a subroutine is called, the program counter details are stored in:

- **(a)** Queue
- **(b)** Linked List
- **(c)** Doubly Linked List
- **(d)** Stack

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) stack**

**Why.** On a call, the return address (the PC) is pushed onto the stack; on return it is popped. Nested calls return in reverse order, which is exactly LIFO.

**Concept: the call stack.** Each call pushes a frame (return address, saved registers, locals). This is why deep recursion can overflow the stack.

{{< /details >}}

### 7 · Registers and instruction sets

*Asked by: Qualcomm (BITS Goa 2024, Q58)*

Which of the below given is/are 32-bit pointer register(s)?

I. EAX  
II. ESP  
III. EBP

- **(a)** All (I), (II) and (III)
- **(b)** Only (II) and (III)
- **(c)** Only (II)
- **(d)** Only (I)

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) only (II) and (III)**

**Why.** ESP (stack pointer) and EBP (base pointer) are the x86 pointer registers. EAX is the accumulator, a general-purpose data register.

**Concept: ESP and EBP.** ESP points to the top of the stack; EBP traditionally marks the start of the current function's frame, so locals and arguments are at fixed offsets from it.

{{< /details >}}

### 8 · Registers and instruction sets

*Asked by: Qualcomm (BITS Hyderabad 2025, Q36)*

Which of the given registers is/are data registers?

I. EBX  
II. EIP  
III. EDX

- **(a)** Only (I)
- **(b)** Only (I) and (III)
- **(c)** Only (II)
- **(d)** All (I), (II) and (III)

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) only (I) and (III)**

**Why.** EAX, EBX, ECX and EDX are the general-purpose data registers. EIP is the instruction pointer (program counter).

**Concept: x86 register roles.** EAX accumulator, EBX base, ECX counter (loops, shifts), EDX data (multiply/divide), ESI/EDI source/destination index, ESP/EBP stack, EIP next instruction.

{{< /details >}}

### 9 · Registers and instruction sets

*Asked by: Qualcomm (IIIT Delhi 2025, Q37)*

Consider the flags I) Sign flag, II) Direction flag, III) Carry flag. Which belong to the **control** flags?

- **(a)** Only (II) and (III)
- **(b)** Only (I) and (II)
- **(c)** Only (II)
- **(d)** Only (I)

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) only (II)**

**Why.** The x86 control flags are TF (trap/single-step), IF (interrupt enable) and DF (direction for string instructions). Sign and carry are status flags, set by ALU results.

**Concept: status vs control flags.** Status flags report the result of the last operation (CF, ZF, SF, OF, PF, AF). Control flags are set by the programmer to change how the CPU behaves.

{{< /details >}}

### 10 · Registers and instruction sets

*Asked by: Qualcomm (BITS Goa 2024, Q34)*

In which of the conditions given in the options is the parity bit of the EFLAGS register set?

- **(a)** The most significant byte of the result has an odd number of 1 bits
- **(b)** The most significant byte of the result has an even number of 1 bits
- **(c)** The least significant byte of the result contains an even number of 1 bits
- **(d)** The least significant 2 bits of the result have an odd number of 1 bits

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) the least significant byte has an even number of 1s**

**Why.** x86's PF looks only at the low 8 bits of the result and is set for even parity.

**Concept: parity.** Counting 1s mod 2. Parity bits detect single-bit errors in transmission; x86 keeps PF for compatibility with the 8080.

{{< /details >}}

### 11 · Registers and instruction sets

*Asked by: Qualcomm (NIT Durgapur, Q40)*

Consider the mnemonics A) MOV and B) LEA. Which statement(s) is/are correct?

I. Both A and B are data-movement instructions.  
II. Both A and B store the machine status words in them.  
III. A helps in moving the instruction from source to destination.  
IV. B helps in loading the effective address into the register.

- **(a)** Only (II) and (IV)
- **(b)** Only (III)
- **(c)** Only (I), (III) and (IV)
- **(d)** Only (I) and (IV)

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) only (I) and (IV)**

**Why.** Both MOV and LEA are data-transfer instructions (I). LEA loads the computed **address**, not the memory contents, into a register (IV). MOV moves data, not instructions (III false), and neither stores the status word (II false).

**Concept: LEA.** `LEA EAX, [EBX + 4*ECX + 8]` computes the address expression and puts the result in EAX without touching memory. Compilers also use it as a fast add-and-multiply.

{{< /details >}}

### 12 · Registers and instruction sets

*Asked by: Qualcomm (NIT Durgapur)*

Which one of the given options is correct with respect to the instruction `SUB R3, 3, R4`?

- **(a)** The contents present in the register R4 is subtracted by 3 and it is stored in R4.
- **(b)** The contents present in the register R4 is substituted by 3 and it is stored in R4.
- **(c)** The contents present in the register R4 is subtracted by 3 and it is stored in R3.
- **(d)** The contents present in the register R3 is subtracted by 3 and it is stored in R4.

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) R4 ← R3 − 3**

**Why.** Reading with the sources first and the destination last (the same convention as `ADD L, M, C`), R3 minus 3 is stored in R4. (In MIPS/ARM style, destination first, it would mean R3 ← 3 − R4, which matches no option.)

**Concept: operand order is a convention.** Intel syntax: destination first; AT&T syntax and some textbook formats: destination last. Always check which one a question uses.

{{< /details >}}

### 13 · Registers and instruction sets

*Asked by: Qualcomm (NIT Durgapur)*

Which of the options is correct with respect to the operation performed by the three-address translation of the assembly code `ADD L, M, C`?

- **(a)** Moves the contents of L to M then add M with C that has contents of L and store the result in C.
- **(b)** Moves the contents of M to C and add L and C that has the contents of M and store the result in C.
- **(c)** Moves the contents of M to L and then add the contents with C and later store the result in C.
- **(d)** Add the contents of L and M and store the result in C.

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) add L and M and store the result in C**

**Why.** A three-address instruction names two sources and a destination: C ← L + M, in one instruction with no intermediate moves.

**Concept: 0-, 1-, 2- and 3-address instructions.** 3-address: `ADD C, A, B`. 2-address: `ADD A, B` (A ← A + B). 1-address: accumulator machines (`ADD B`). 0-address: stack machines (`ADD` pops two, pushes one).

{{< /details >}}

### 14 · Registers and instruction sets

*Asked by: Qualcomm (Delhi campus 2024)*

What result is stored at location 2000H after this 8085 program, if the contents of (1000H) = AAH?

`LDA 1000H` · `CMA` · `STA 2000H`

- **(a)** 11H
- **(b)** 88H
- **(c)** AAH
- **(d)** 55H

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) 55H**

**Why.** LDA 1000H loads A = AAH = 1010 1010. CMA complements A: 0101 0101 = 55H. STA 2000H stores it.

**Concept: complement in hex.** The 1's complement of a hex digit d is F − d: A → 5, so AAH → 55H.

{{< /details >}}

### 15 · Buses and I/O

*Asked by: Qualcomm (Delhi campus 2024, Q25)*

The bus design that uses a handshake method and has no clock is:

- **(a)** Asynchronous bus
- **(b)** Daisy chain
- **(c)** Synchronous bus
- **(d)** Processor bus

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) asynchronous bus**

**Why.** An asynchronous bus coordinates transfers with request/acknowledge handshake signals instead of a common clock, so devices of different speeds can share it.

**Concept: synchronous vs asynchronous buses.** Synchronous: every transfer takes a fixed number of clock cycles (simple, fast, but all devices must keep up). Asynchronous: each transfer is paced by handshakes (flexible, more control signals).

{{< /details >}}

### 16 · Control unit

*Asked by: Qualcomm (IISc 2024, Q43)*

Which is not a part of a hardwired control unit?

- **(a)** Logic gates
- **(b)** Counters
- **(c)** ROM
- **(d)** Decoders

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) ROM**

**Why.** A hardwired control unit is built from gates, decoders and a step counter. A ROM holding control words is the control memory of a **microprogrammed** control unit.

**Concept: hardwired vs microprogrammed control.** Hardwired: fast, fixed logic (RISC). Microprogrammed: each instruction runs a small program of control words from ROM; easier to change and to support complex instructions (classic CISC).

{{< /details >}}

### 17 · RISC stages

*Asked by: Texas Instruments (NIT Calicut 2023)*

In how many stages does a RISC instruction execute?

- **(a)** 4
- **(b)** 5
- **(c)** 3
- **(d)** 7

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) 5**

**Why.** The classic RISC pipeline has five stages: instruction fetch (IF), decode/register read (ID), execute (EX), memory access (MEM), write back (WB).

**Concept: the 5-stage pipeline.** Each stage takes one cycle, so up to five instructions are in flight at once and, ideally, one completes every cycle.

{{< /details >}}

### 18 · a feedback shift register

*Asked by: Texas Instruments (NIT Calicut 2023)*

A 4-bit register loaded with 1010 shifts right on each clock, and the serial input (MSB) comes
from a network of two AND gates on the register outputs (figure). After how many clocks is the
content 1010 again?

- **(a)** 3
- **(b)** 7
- **(c)** 11
- **(d)** 15

{{< details title="Answer and explanation" closed="true" >}}

**Answer: cannot be determined** (the gate inputs are illegible in the photo)

**Concept: feedback shift registers.** The next serial input is a function of the current bits; the sequence of states eventually repeats. For linear feedback (XOR) with a good choice of taps, an n-bit register cycles through 2ⁿ − 1 states.

{{< /details >}}
