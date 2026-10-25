---
title: "4 · Instruction set architecture and addressing modes"
linkTitle: "4 ISA and addressing"
weight: 4
math: true
---
## 4.1 Instruction formats {#coa-4-1}

An instruction = **opcode** (what to do) + **operand fields** (where the data is). By the number of addresses:

| Format | Example for $X = A + B$ | Machine type |
|---|---|---|
| 3-address | `ADD X, A, B` | |
| 2-address | `MOV X, A` ; `ADD X, B` | |
| 1-address | `LOAD A` ; `ADD B` ; `STORE X` | **accumulator** machine |
| 0-address | `PUSH A` ; `PUSH B` ; `ADD` ; `POP X` | **stack** machine |

Fewer addresses → shorter instructions, but more of them.

**Key registers:** **PC** (program counter: address of the next instruction), **IR** (instruction register), **MAR** (memory address register), **MDR/MBR** (memory data register), **AC** (accumulator), **SP** (stack pointer), status/**flags** (zero, carry, sign, overflow).

## 4.2 Encoding numericals (expanding opcodes) {#coa-4-2}

With a fixed instruction length, unused opcode patterns of a longer-address format can be **expanded** into opcodes for shorter formats.

<div class="nb nb-example">

<strong>Example</strong> (Expanding opcode)

12-bit instructions, 4-bit address fields. Two-address instructions use $12 - 8 = 4$ opcode bits → 16 patterns. If **13** two-address instructions exist, **3** patterns are left; each can be followed by 4 more opcode bits for a one-address instruction → at most $3 \times 2^4 = $ **48** one-address instructions.

</div>

<div class="nb nb-example">

<strong>Example</strong> (Field sizes)

32-bit instructions, 64 registers, 3-register format: each register field needs $\log_2 64 = 6$ bits, three fields = 18 bits, leaving **14 bits** for the opcode (16,384 opcodes).

</div>

## 4.3 Addressing modes {#coa-4-3}

| Mode | Effective address (EA) / operand | Use |
|---|---|---|
| **Immediate** | the operand is in the instruction | constants |
| **Direct** (absolute) | EA = address field | global variables |
| **Indirect** | EA = Mem[address field] | pointers |
| **Register** | operand is in a register | fastest |
| **Register indirect** | EA = register | pointer in a register |
| **Indexed** | EA = address field + index register | arrays |
| **Base (displacement)** | EA = base register + offset | struct fields, stack frames |
| **PC-relative** | EA = PC + offset | branches; position-independent code |
| **Auto-increment / decrement** | EA = register, then register ± size | walking through arrays, stacks |

<div class="nb nb-example">

<strong>Example</strong> (Effective addresses)

A 2-word instruction at address 200 has address field **500**; after fetching, PC = **202**. Register R = **400**. Mem[500] = **800**.

| Mode | EA | Operand |
|---|---|---|
| Immediate | — | **500** |
| Direct | 500 | Mem[500] = 800 |
| Indirect | Mem[500] = **800** | Mem[800] |
| Register indirect | R = **400** | Mem[400] |
| Indexed (R) | 500 + 400 = **900** | Mem[900] |
| PC-relative | 202 + 500 = **702** | Mem[702] |

</div>

## 4.4 RISC vs CISC {#coa-4-4}

| | RISC | CISC |
|---|---|---|
| Instructions | few, simple, **fixed length** | many, complex, **variable length** |
| Memory access | only load/store | many instructions access memory |
| Addressing modes | few | many |
| Registers | many | fewer |
| Control | hardwired | often microprogrammed |
| Pipelining | easy | harder (decoded into micro-ops internally) |
| Examples | ARM, RISC-V, MIPS | x86 |

**MIPS formats (32 bits):** R-type `op | rs | rt | rd | shamt | funct` (6-5-5-5-5-6), I-type `op | rs | rt | immediate(16)`, J-type `op | address(26)`.

**Calling conventions:** the first few arguments go in registers (x86-64 Linux: `rdi, rsi, rdx, rcx, r8, r9`), the return value in `rax`; the rest on the stack.

<div class="nb nb-moral">

Accumulator machines use 1-address instructions, stack machines 0-address. Expanding opcodes: leftover patterns × 2^(freed bits). Indirect = memory holds the address; indexed = field + register; PC-relative = PC + offset.

</div>
