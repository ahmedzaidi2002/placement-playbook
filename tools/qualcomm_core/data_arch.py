"""Computer Architecture questions (sections "Computer Architecture", "Computer Architecture 2" and "CA")."""
from qdef import Q

ARCH = [
    # ---- number representation ----
    Q('Number systems', [('p0', 50), ('p5', 30)],
      'What will be the decimal equivalent of the number (011.101)₂?',
      ['Given number is invalid binary number', '3.625', '3', '2.625'], 'B',
      'Integer part 011 = 3. Fraction .101 = 1·2⁻¹ + 0·2⁻² + 1·2⁻³ = 0.5 + 0.125 = 0.625. Total **3.625**.'),
    Q('Number systems', [('p1', 38)],
      'Convert (5613)₈ to decimal.', ['4900', '2955', '1500', '3955'], 'B',
      '5·512 + 6·64 + 1·8 + 3 = 2560 + 384 + 8 + 3 = **2955**.'),
    Q('Number systems', [('p3', 25)],
      'What is the decimal equivalent of (1111011011000)₂?', ['458', '7596', '7896', '785'], 'C',
      'Group into hex from the right: 1 1110 1101 1000 = 0x1ED8 = 1·4096 + 14·256 + 13·16 + 8 = **7896**.'),
    Q('Number systems', [('p3', 28), ('p5', 27)],
      'Convert (10101010101011)₂ into hexadecimal.', ['(2CCC)₁₆', '(2AAB)₁₆', '(2BBB)₁₆', '(2BBC)₁₆'], 'B',
      'Group four bits at a time from the right: 10 | 1010 | 1010 | 1011 = 2 A A B, so **(2AAB)₁₆**.'),
    Q('Number systems', [('p4', 26)],
      'Convert (9ED)₁₆ to octal.', ['4776', '4855', '4765', '4755'], 'D',
      '9ED = 1001 1110 1101. Regroup in threes from the right: 100 111 101 101 = 4 7 5 5, so **(4755)₈**.'),
    Q('Number systems', [('p2', 21)],
      'Convert 109 (decimal) to hexadecimal.', ['4D', '100D', '6D', '109F'], 'C',
      '109 = 6·16 + 13, and 13 is D, so **6D**.'),
    Q('Number systems', [('p4', 47)],
      'What is the correct 2\'s complement representation of (−55)₁₀ in 8 bits?',
      ['11001001', '01010101', '10110101', '11101101'], 'A',
      '+55 = 0011 0111. Invert: 1100 1000. Add 1: **1100 1001**.'),
    Q('Number systems', [('p5', 23)],
      'What is the binary equivalent of (−56)₁₀ (24-bit two\'s complement)?',
      ['(000000000000000001001000)₂', '(000000000000000000001000)₂',
       '(111111111111111111101000)₂', '(111111111111111111001000)₂'], 'D',
      '+56 = 0011 1000. Invert and add 1 in 8 bits: 1100 1000. Sign-extend to 24 bits with ones: '
      '**1111 1111 1111 1111 1100 1000**. (Option C is −24.)'),
    Q('Number systems', [('p6', 40)],
      'What is the 2\'s complement of the decimal number 95 (7 bits)?',
      ['1100111', '0100001', '0101010', '1100110'], 'B',
      '95 = 101 1111. Invert: 010 0000. Add 1: **010 0001**.'),
    # ---- Boolean algebra and gates (asked in the CA section) ----
    Q('Boolean algebra and gates', [('p2', 26)],
      'AB + AB′ + A′C + AC is independent of which variable?', ['A', 'AC', 'B', 'C'], 'C',
      'AB + AB′ = A(B + B′) = A and A′C + AC = C, so the expression is **A + C**: B has dropped out.'),
    Q('Boolean algebra and gates', [('p2', 21)],
      'Reduce (P + Q)·(P + Q).', ['PQ + 1', 'PQ', 'P', 'P + Q'], 'D',
      'Idempotent law: X·X = X with X = P + Q.'),
    Q('Boolean algebra and gates', [('p3', 54)],
      'Which one of the given options is the correct reduction of (P′ + R)·R?',
      ['P′ + R', 'R·(1 + P′)', 'P′R + 1', 'P′·R'], 'B',
      '(P′ + R)·R = P′R + R = R(P′ + 1) = R. The only option equal to R is **R·(1 + P′)**, the last step before '
      'simplifying 1 + P′ to 1.'),
    Q('Boolean algebra and gates', [('p7', None)],
      'Which one of the given options is the correct reduction of HT + HTC?', ['1', 'H', 'HT', 'HTC'], 'C',
      'Absorption: X + XY = X with X = HT, so HT + HTC = HT(1 + C) = **HT**.'),
    Q('Boolean algebra and gates', [('p2', 24)],
      'Which of the following are examples of associative rules in Boolean algebra?\n\n'
      'I. (X + Y) + Z = X + (Y + Z)  \nII. X + Y = Y + X',
      ['Both (I) and (II)', 'Only (I)', 'Neither (I) nor (II)', 'Only (II)'], 'B',
      'I regroups operands: associative. II swaps their order: commutative.'),
    Q('Boolean algebra and gates', [('p6', 41)],
      'Which one of the operations given in the options is incorrect?',
      ['X · 1 = X', 'X + 0 = X', 'X + 1 = X', 'X · 0 = 0'], 'C',
      'X + 1 = 1 (null/dominance law), not X.'),
    Q('Boolean algebra and gates', [('p1', 23)],
      'Which one of the gates given in the options can be used as a 2-input NOT gate when one input amongst the '
      'two is set to the constant 1?', ['NOR gate', 'NAND gate', 'OR gate', 'EXNOR gate'], 'B',
      'NAND(A, 1) = (A·1)′ = A′. (XOR with 1 would also invert, but it is not offered; EXNOR with 1 gives A, NOR '
      'with 1 gives 0.)'),
    Q('Boolean algebra and gates', [('p6', 54)],
      'Which logic gate gives an output that is LOW if and only if all the inputs are HIGH?',
      ['EXNOR', 'AND', 'NAND', 'OR'], 'C', 'That is the NAND truth table: it is 0 only for the all-ones input.'),
    Q('Boolean algebra and gates', [('p5', 21)],
      'Consider the truth table below. Which one of the given options corresponds to it?',
      ['EXNOR', 'NOT', 'NAND', 'AND'], 'A',
      'The output is 1 exactly when the inputs are equal, which is XNOR (equivalence).',
      table='| A | B | Y |\n|:-:|:-:|:-:|\n| 0 | 0 | 1 |\n| 0 | 1 | 0 |\n| 1 | 0 | 0 |\n| 1 | 1 | 1 |'),
    Q('Boolean algebra and gates', [('p1', 40)],
      'If a logic gate has three inputs, how many input states (combinations) are there?', ['2', '8', '4', '6'], 'B',
      '2³ = 8.'),
    Q('Boolean algebra and gates', [('p1', 24)],
      'Consider block X in the figure: one data input, several outputs and control (select) lines. X is:\n\n'
      'I. a multiplexer  \nII. an encoder  \nIII. a demultiplexer',
      ['Only (I) and (II)', 'Only (II)', 'Only (III)', 'Only (I)'], 'C',
      'One input routed to one of many outputs under control of select lines is a demultiplexer. A multiplexer '
      'is the reverse (many inputs, one output); an encoder has many inputs and no select lines.',
      fig='demux-block'),
    Q('Boolean algebra and gates', [('p1', 34)],
      'A full adder can be converted into a full subtractor by adding one:',
      ['AND gate', 'Inverter', 'NOR gate', 'OR gate'], 'B',
      'The difference output is the same three-input XOR. The borrow is B_out = A′B + A′B_in + B·B_in, which is '
      'the adder\'s carry with A complemented, so a single inverter on A (for the carry/borrow path) does it.'),
    Q('Digital design flow', [('p5', 50)],
      'Which of the method(s) given below convert(s) the input-output relationship of a circuit into a digital '
      'circuit design?\n\nI. Analysis of combinational logic circuits  \nII. Synthesis of combinational logic circuits',
      ['Only (II)', 'Both (I) and (II)', 'Neither (I) nor (II)', 'Only (I)'], 'A',
      'Synthesis (design) goes from the specification or truth table to a circuit. Analysis goes the other way: '
      'from a given circuit to its Boolean functions.'),
    # ---- registers and instructions ----
    Q('Registers and instruction sets', [('p0', 58)],
      'Which of the below given is/are 32-bit pointer register(s)?\n\nI. EAX  \nII. ESP  \nIII. EBP',
      ['All (I), (II) and (III)', 'Only (II) and (III)', 'Only (II)', 'Only (I)'], 'B',
      'ESP (stack pointer) and EBP (base pointer) are the x86 pointer registers. EAX is the accumulator, a '
      'general-purpose data register.'),
    Q('Registers and instruction sets', [('p3', 36)],
      'Which of the given registers is/are data registers?\n\nI. EBX  \nII. EIP  \nIII. EDX',
      ['Only (I)', 'Only (I) and (III)', 'Only (II)', 'All (I), (II) and (III)'], 'B',
      'EAX, EBX, ECX and EDX are the general-purpose data registers. EIP is the instruction pointer (program '
      'counter).'),
    Q('Registers and instruction sets', [('p5', 37)],
      'Consider the flags I) Sign flag, II) Direction flag, III) Carry flag. Which belong to the **control** flags?',
      ['Only (II) and (III)', 'Only (I) and (II)', 'Only (II)', 'Only (I)'], 'C',
      'In 8086/x86 the control flags are TF (trap), IF (interrupt enable) and DF (direction). Sign and carry are '
      'status flags set by ALU results.'),
    Q('Registers and instruction sets', [('p0', 34)],
      'In which of the conditions given in the options is the parity bit of the EFLAGS register set?',
      ['The most significant byte of the result has an odd number of 1 bits',
       'The most significant byte of the result has an even number of 1 bits',
       'The least significant byte of the result contains an even number of 1 bits',
       'The least significant 2 bits of the result have an odd number of 1 bits'], 'C',
      'x86 PF looks only at the low 8 bits of the result and is set when they contain an even number of ones '
      '(even parity).'),
    Q('Registers and instruction sets', [('p3', 26)],
      'Which of the given instructions are correct?\n\nI. MOV BL, AL, DL  \nII. MOV BH  \nIII. MOV SP, AX',
      ['Only (I) and (II)', 'Only (II) and (III)', 'Only (I)', 'Only (III)'], 'D',
      '`MOV` takes exactly two operands, destination then source, of the same size. I has three operands and II '
      'has one; `MOV SP, AX` copies a 16-bit register into another 16-bit register and is valid.'),
    Q('Registers and instruction sets', [('p7', 40)],
      'Consider the mnemonics A) MOV and B) LEA. Which statement(s) is/are correct?\n\n'
      'I. Both A and B are data-movement instructions.  \nII. Both A and B store the machine status words in them.  \n'
      'III. A helps in moving the instruction from source to destination.  \n'
      'IV. B helps in loading the effective address into the register.',
      ['Only (II) and (IV)', 'Only (III)', 'Only (I), (III) and (IV)', 'Only (I) and (IV)'], 'D',
      'Both are classed as data-transfer instructions (I). LEA loads the computed effective address, not the '
      'memory contents, into a register (IV). III is wrong because MOV moves **data**, not an instruction, and '
      'neither touches the status word (II).'),
    Q('Registers and instruction sets', [('p7', None)],
      'Which one of the given options is correct with respect to the instruction `SUB R3, 3, R4`?',
      ['The contents present in the register R4 is subtracted by 3 and it is stored in R4.',
       'The contents present in the register R4 is substituted by 3 and it is stored in R4.',
       'The contents present in the register R4 is subtracted by 3 and it is stored in R3.',
       'The contents present in the register R3 is subtracted by 3 and it is stored in R4.'], 'D',
      'Read with the sources first and the destination last (the same convention as `ADD L, M, C` below): '
      'R4 ← R3 − 3.',
      conf='medium', note='The operand order is not stated. In MIPS/ARM style (destination first) the instruction '
      'would mean R3 ← 3 − R4, which matches no option, so the source-first reading is the intended one.'),
    Q('Registers and instruction sets', [('p7', None)],
      'Which of the options is correct with respect to the operation performed by the three-address translation '
      'of the assembly code `ADD L, M, C`?',
      ['Moves the contents of L to M then add M with C that has contents of L and store the result in C.',
       'Moves the contents of M to C and add L and C that has the contents of M and store the result in C.',
       'Moves the contents of M to L and then add the contents with C and later store the result in C.',
       'Add the contents of L and M and store the result in C.'], 'D',
      'A three-address instruction names two sources and a destination: C ← L + M, in one instruction with no '
      'intermediate moves.'),
    Q('Registers and instruction sets', [('p4', None)],
      'What result is stored at location 2000H after this 8085 program, if the contents of (1000H) = AAH?\n\n'
      '`LDA 1000H` · `CMA` · `STA 2000H`',
      ['11H', '88H', 'AAH', '55H'], 'D',
      'LDA loads A = AAH = 1010 1010. CMA complements it: 0101 0101 = **55H**. STA stores A at 2000H.',
      conf='medium', note='The section header was not visible in this photo; it sits among the CA2 questions.'),
    # ---- pipelining and performance ----
    Q('Pipelining', [('p7', 37)],
      'When instructions cannot be overlapped in a pipeline because both need the same resource, it is called a:',
      ['Structural hazard', 'Both data and structural hazard', 'Control hazard', 'Data hazard'], 'A',
      'A resource conflict (one memory port, one ALU) is a structural hazard. Data hazards come from operand '
      'dependences, control hazards from branches.'),
    Q('Pipelining', [('p4', 24)],
      'The mechanism to identify a hazard and stall the pipeline until the hazard is resolved is called:',
      ['Pipeline intralock', 'Pipeline flush', 'Pipeline interlock', 'Pipeline lock'], 'C',
      'The pipeline interlock is the hardware that detects the dependence and inserts stalls (bubbles) until it '
      'clears. Flushing discards wrong-path instructions after a mispredicted branch.'),
    Q('Pipelining', [('p0', 38)],
      'Which of the following prevent **data** hazards in a pipeline?\n\n'
      'I. Increasing latch latency  \nII. Decreasing cycle time  \nIII. Introducing pipeline bubbles  \n'
      'IV. Delayed branching and branch prediction',
      ['All (I), (II), (III) and (IV)', 'Only (IV)', 'Only (I) and (II)', 'Only (III)'], 'D',
      'Stalling with bubbles holds the dependent instruction until the operand is ready. Delayed branching and '
      'prediction address control hazards; changing latch latency or cycle time does not remove a dependence.'),
    Q('Pipelining', [('p4', 52)],
      'A processor has five functional units with latencies 20 ns, 16 ns, 20 ns, 20 ns and 14 ns. Pipelining '
      'adds 1 ns of latch overhead per stage. What is the speed-up of the pipelined design over the single-cycle '
      'datapath?',
      ['4.3', '4.5', '6.0', '6.4'], 'A',
      'Single cycle: 20 + 16 + 20 + 20 + 14 = 90 ns per instruction. Pipelined clock = slowest stage + overhead = '
      '20 + 1 = 21 ns, one instruction per cycle in steady state. Speed-up = 90 / 21 ≈ **4.29**.'),
    Q('Performance', [('p3', 46)],
      'What is the throughput of a 750 MHz processor whose cache miss penalty adds 2.52 cycles per instruction '
      '(base CPI 1)?',
      ['716.62 MIPS', '581.84 MIPS', '213 MIPS', '299 MIPS'], 'C',
      'Effective CPI = 1 + 2.52 = 3.52. MIPS = 750 / 3.52 ≈ **213**.',
      conf='medium', note='The photo gives only "miss penalty 2.52" at 750 MHz; 299 ≈ 750 / 2.52 is the trap if '
      'the base CPI is forgotten.'),
    Q('Performance', [('p4', 46)],
      'A 400 MHz processor runs a program with the instruction mix below. What is the average CPI on a '
      'uniprocessor?',
      ['6.6', '4.6', '14', '7.89'], None,
      'Weighted CPI = 0.30·2 + 0.661·5 + 0.039·7 = 0.6 + 3.305 + 0.273 = **4.18**, which is not an option. '
      '4.6 is the nearest and is close to the plain average (2 + 5 + 7) / 3 = 4.67, which ignores the mix.',
      table='| Instruction type | CPI | Mix |\n|---|:-:|:-:|\n| Branch | 2 | 30% |\n'
            '| Arithmetic / logic | 5 | 66.10% |\n| Load / store | 7 | 3.90% |',
      conf='flag', note='The correct weighted CPI (4.18) is not among the options.'),
    Q('Parallel organisation', [('p6', 25)],
      'Uni-processors fall into which of the computer system structure categories given in the options?',
      ['Single instruction, single data (SISD) stream', 'Single instruction, multiple data (SIMD) stream',
       'Multiple instruction, multiple data (MIMD) stream', 'Multiple instruction, single data (MISD) stream'], 'A',
      'Flynn\'s taxonomy: a classic uniprocessor executes one instruction stream on one data stream.'),
    Q('Parallel organisation', [('p3', 31)],
      'Which of these statements about multiprocessors are true?\n\n'
      'I. Tightly coupled systems use a common memory for all processors.  \n'
      'II. In tightly coupled systems, jobs from all processors are kept in the same pool.  \n'
      'III. In loosely coupled systems, each processor has its own private queue.  \n'
      'IV. Memory is shared in loosely coupled systems.',
      ['Only (I)', 'Only (II), (III) and (IV)', 'Only (I), (II) and (III)', 'Only (II) and (III)'], 'C',
      'Tightly coupled = shared memory and a shared ready pool. Loosely coupled = each node has private memory '
      'and its own queue and communicates by messages, so IV is false.'),
    # ---- memory and buses ----
    Q('Memory hierarchy', [('p0', 37)],
      'Which is the second level of memory?', ['Main memory', 'Register', 'Secondary memory', 'Cache memory'], 'D',
      'Counting from the CPU: registers (level 1), cache (level 2), main memory (level 3), secondary storage '
      '(level 4).',
      conf='medium', note='Some textbooks start the count at level 0 for registers, which would make main memory '
      'the second level; with registers as level 1, cache is second.'),
    Q('Caches', [('p4', 36)],
      'In which policy is data written only to the cache block, and the modified block written to main memory '
      'only when it is replaced?\n\nI. Write back  \nII. Write through',
      ['Neither (I) nor (II)', 'Both (I) and (II)', 'Only (II)', 'Only (I)'], 'D',
      'Write back marks the block dirty and writes it to memory on eviction. Write through updates memory on '
      'every write.'),
    Q('Memory organisation', [('p4', 44)],
      'Which of the following statements about DRAM are true?\n\n'
      'I. Address lines are multiplexed to reduce the number of pins.  \n'
      'II. The higher-order bits select a column and are latched by RAS.  \n'
      'III. The lower-order bits select a row and are latched by CAS.  \n'
      'IV. The higher-order bits select a row and are latched by RAS.  \n'
      'V. The lower-order bits select a column and are latched by the row address strobe.',
      ['Only (I), (II) and (III)', 'Only (II) and (III)', 'Only (IV) and (V)', 'Only (I), (IV) and (V)'], 'D',
      'A DRAM sends the row address first (high bits, latched by RAS) and then the column address on the same '
      'pins (low bits, latched by CAS). I and IV are certainly true and only the last option contains both.',
      conf='medium', note='Statement V as printed says "row address strobe"; it should say column address strobe '
      '(CAS). It is clearly meant as the true counterpart of III.'),
    Q('Memory organisation', [('p4', 60)],
      'What is the order of the steps that take place to perform a **read** from a specified memory location?\n\n'
      'I. A read signal is issued by the CPU.  \nII. The word is loaded into the Memory Data Register and used by the CPU.  \n'
      'III. The address of the word to be read is loaded into the Memory Address Register.',
      ['(I), (II) and (III)', '(III), (I) and (II)', '(II), (III) and (I)', '(III), (II) and (I)'], 'B',
      'Put the address in MAR, assert Read, wait for memory, then the word arrives in MDR for the CPU.'),
    Q('Buses and I/O', [('p4', 25)],
      'The bus design that uses a handshake method and has no clock is:',
      ['Asynchronous bus', 'Daisy chain', 'Synchronous bus', 'Processor bus'], 'A',
      'An asynchronous bus coordinates transfers with request/acknowledge handshake signals instead of a common '
      'clock, so devices of different speeds can share it.'),
    Q('Flip-flops (CA section)', [('p4', 38)],
      'A J-K flip-flop has its J input connected to logic 1 and its K input connected to its own Q output. '
      'When clock pulses are applied, the flip-flop will:',
      ['Go to 0 and stay there', 'Change its state at each clock pulse', 'Go to 1 and stay there',
       'Retain its initial state'], 'B',
      'If Q = 0: J = 1, K = 0, so it sets to 1. If Q = 1: J = K = 1, so it toggles to 0. It alternates on every '
      'clock pulse.'),
]
