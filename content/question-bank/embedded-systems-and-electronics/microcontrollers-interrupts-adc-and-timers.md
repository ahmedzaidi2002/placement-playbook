---
title: "Microcontrollers, interrupts, ADC and timers"
weight: 2
---

18 questions asked by MathWorks, Qualcomm, Texas Instruments. Try each one first, then open the toggle: it gives the answer, why it is right, and the idea behind it explained from scratch.

### 1 · Q1, I2C

*Asked by: MathWorks (IISc 2024)*

I2C is a:

- **(a)** single-master, single-slave bus
- **(b)** multi-master, single-slave bus
- **(c)** single-master, multi-slave bus
- **(d)** multi-master, multi-slave bus

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) multi-master, multi-slave**

**Why.** Every I²C device has an address, any master can start a transfer, and arbitration on the SDA line resolves collisions when two masters start at once.

**Concept: I²C.** Two wires (SDA data, SCL clock) with pull-up resistors, open-drain outputs. Slower than SPI but needs fewer pins and supports many devices on one bus.

{{< /details >}}

### 2 · Q4, ARM Abort mode

*Asked by: MathWorks (IISc 2024)*

During what scenarios is Abort mode entered? (more than one answer possible)

- **(a)** Handling undefined instructions
- **(b)** An attempt to access memory fails
- **(c)** No memory is available
- **(d)** The processor is in rest state

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) an attempt to access memory fails**

**Why.** ARM enters Abort mode on a prefetch abort (fetching an instruction from an invalid address) or a data abort (invalid data access). Undefined instructions use Undefined mode.

**Concept: ARM processor modes.** User, FIQ, IRQ, Supervisor (SVC, system calls/reset), Abort (memory faults), Undefined (unknown instructions), System. Each exception switches to its mode with banked registers.

{{< /details >}}

### 3 · Q5, interrupts

*Asked by: MathWorks (IISc 2024)*

An interrupt diverts the execution of the processor to:

- **(a)** the interrupt service routine
- **(b)** the counter word register
- **(c)** the execution unit
- **(d)** the control unit

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) the interrupt service routine**

**Why.** On an interrupt the processor saves its state and jumps to the ISR for that interrupt; when the ISR finishes, it restores state and resumes the interrupted code.

**Concept: interrupts vs polling.** Interrupts let hardware signal events immediately instead of the CPU repeatedly checking (polling), saving time and power.

{{< /details >}}

### 4 · Q6, ignorable interrupt

*Asked by: MathWorks (IISc 2024)*

An interrupt that can be temporarily ignored is a:

- **(a)** vectored interrupt
- **(b)** non-maskable interrupt
- **(c)** maskable interrupt
- **(d)** negative-priority interrupt

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) maskable interrupt**

**Why.** A maskable interrupt can be disabled (masked) by software, e.g. during a critical section. A non-maskable interrupt (NMI) cannot be ignored; it is used for emergencies like power failure.

**Concept: interrupt masking.** Disabling interrupts briefly protects shared data in embedded code; keep such sections short to avoid missing events.

{{< /details >}}

### 5 · Data converters

*Asked by: Qualcomm (BITS Goa 2024, Q47)*

A 4-bit R-2R ladder DAC has V_ref = 3 V. What is the analog output for the input 0101?

- **(a)** 0.6252 V
- **(b)** 0.9375 V
- **(c)** 1.2542 V
- **(d)** 1.4891 V

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) 0.9375 V**

**Why.** An n-bit DAC outputs V_ref × D/2ⁿ: 3 × 5/16 = 0.9375 V (0101 = 5).

**Concept: R-2R ladder DAC.** A network of only two resistor values that halves the current at each stage, so each bit contributes a binary-weighted share of V_ref. Easy to make accurately on a chip.

{{< /details >}}

### 6 · Data converters

*Asked by: Qualcomm (BITS Hyderabad 2025, Q48)*

How many equal intervals are there in a 16-bit DAC?

- **(a)** 65535
- **(b)** 16383
- **(c)** 23412
- **(d)** 23441

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) 65535**

**Why.** 16 bits give 2¹⁶ = 65,536 output levels, which divide the range into 65,536 − 1 = 65,535 equal steps.

**Concept: levels vs steps.** n bits → 2ⁿ levels and 2ⁿ − 1 intervals between the lowest and highest output (like fence posts and gaps).

{{< /details >}}

### 7 · Data converters

*Asked by: Qualcomm (BITS Hyderabad 2025, Q50)*

What is the SNR of a 16-bit ADC (in dB)?

- **(a)** 67
- **(b)** 98
- **(c)** 75
- **(d)** 86

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) 98 dB**

**Why.** An ideal N-bit converter's quantisation SNR for a full-scale sine is 6.02N + 1.76 dB = 6.02 × 16 + 1.76 ≈ 98 dB.

**Concept: each bit adds about 6 dB.** One more bit halves the quantisation step, which halves the noise amplitude (20 log 2 ≈ 6 dB).

{{< /details >}}

### 8 · Data converters

*Asked by: Qualcomm (IIIT Delhi 2025, Q58)*

Which one of the options given below is **not** a component of a SAR-type analog-to-digital converter?

- **(a)** R-2R ladder
- **(b)** Digital-to-analog converter
- **(c)** Op-amp
- **(d)** Comparator

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) op-amp**

**Why.** A SAR ADC's defining blocks are the successive-approximation register, a DAC (often an R-2R ladder), a comparator and a sample-and-hold. A separate op-amp is not one of them (though a DAC may use one internally).

**Concept: SAR ADC.** Binary search on voltage: set the MSB, compare the DAC output with the input, keep or clear the bit, move to the next bit. N bits take N comparisons.

{{< /details >}}

### 9 · Data converters

*Asked by: Qualcomm (Delhi campus 2024, Q52)*

The full-scale output and full-scale error of an 8-bit DAC are 2 mA and ±0.6% F.S. What is the possible output range for the binary input 10010000?

- **(a)** 1468 to 1504 µA
- **(b)** 1666 to 1702 µA
- **(c)** 1264 to 1302 µA
- **(d)** 1865 to 1897 µA

{{< details title="Answer and explanation" closed="true" >}}

**Answer: no reliable pick** (the computed range is 1117–1141 µA, not offered)

**Why.** Step = 2 mA/255 ≈ 7.84 µA. 10010000 = 144, so the ideal output is 144 × 7.84 ≈ 1129 µA. Full-scale error ±0.6% × 2 mA = ±12 µA, giving 1117–1141 µA. The options are 36 µA wide (±0.9% F.S.), so the question's numbers were probably changed.

**Concept: full-scale error.** Specified as a percentage of the full-scale output and applies equally to every code: output = ideal ± (error% × full scale).

{{< /details >}}

### 10 · jump if bit set

*Asked by: Texas Instruments (IIT ISM 2024)*

Which 8051 instruction jumps if a given bit is set?

- **(a)** JC
- **(b)** JZ
- **(c)** JB
- **(d)** JNZ

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) JB**

**Why.** `JB bit, label` jumps if the given bit is 1. JC jumps on the carry flag; JZ/JNZ test whether the accumulator is zero.

**Concept: 8051 bit instructions.** The 8051 has bit-addressable memory and instructions like SETB, CLR, JB, JNB, JBC for single-bit control, handy for I/O pins.

{{< /details >}}

### 11 · 8085 factorial

*Asked by: Texas Instruments (IIT BHU 2023)*

```c
MULTIPLY:      MOV E, B
               MVI A, 00H
MULTIPLYLOOP:  ADD D
               XXX
               MOV D, A
               RET
```

What replaces
XXX?

- **(a)** DCR E; JNZ MULTIPLYLOOP
- **(b)** DCR E
- **(c)** JNZ MULTIPLYLOOP
- **(d)** HLT

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) DCR E; JNZ MULTIPLYLOOP**

**Why.** The routine multiplies by repeated addition: add D to A, decrement the counter E, and loop until E reaches 0. Both instructions are needed: DCR E updates the counter and sets the Zero flag; JNZ loops while it isn't zero.

**Concept: loops in assembly.** Counter in a register, decrement it (which sets flags), conditional jump back. The 8085 has no multiply instruction, so multiplication is repeated addition (or shift-and-add).

{{< /details >}}

### 12 · ADC step size

*Asked by: Texas Instruments (NIT Calicut 2023)*

Step size of a 10-bit ADC for 0-10 V?

{{< details title="Answer and explanation" closed="true" >}}

**Answer: about 9.77 mV**

**Why.** Step size (1 LSB) = full-scale range/2ⁿ = 10 V/1024 ≈ 9.77 mV.

**Concept: ADC resolution.** The smallest input change the converter can distinguish. More bits or a smaller range give finer resolution.

{{< /details >}}

### 13 · AVR branch range

*Asked by: Texas Instruments (IISc 2023)*

In an AVR loop ending with `BRNE LOOP`, which is true about the branch target?

{{< details title="Answer and explanation" closed="true" >}}

**Answer: conditional branches like BRNE are short relative jumps** (a 7-bit signed offset, −64 to +63 words)

**Why.** BRNE encodes the target as a small offset from the current instruction, so the loop target must be within that range; for farther targets use a reversed branch over an RJMP/JMP.

**Concept: relative vs absolute jumps.** Relative branches store a small offset (compact, position-independent); absolute jumps store the full address (reach anywhere, longer instruction).

{{< /details >}}

### 14 · microcontroller memories

*Asked by: Texas Instruments (IISc 2023)*

Which memories can a microcontroller have?

{{< details title="Answer and explanation" closed="true" >}}

**Answer: SRAM, EEPROM and Flash**

**Why.** Flash holds the program (non-volatile, rewritten rarely), SRAM holds variables and the stack (fast, volatile), EEPROM holds small settings that must survive power-off and change occasionally (byte-erasable).

**Concept: volatile vs non-volatile.** Volatile memory (SRAM, DRAM) loses data without power; non-volatile (Flash, EEPROM, ROM) keeps it.

{{< /details >}}

### 15 · which implementation is fastest?

*Asked by: Texas Instruments (TI prep guide)*

A cacheless processor has L1 RAM $>$ L2 RAM $>$ FLASH in speed; `.bss` and `.stack`
are in L1, `.data` and `.heap` in L2. `compute_sum` adds a range into (1) the
global `global_sum` directly, (2) a local `local_sum` copied at the end, (3) a
`static int local_sum = 0` copied at the end. Slowest and fastest?

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (3) slowest, (2) fastest** (official solution)

**Why.** The local `local_sum` lives on the stack (in fast L1), and is copied to the global once at the end: fastest. The global (in .bss, L1 here) is fine too, but every iteration writes to memory. In the official solution, the static `local_sum` sits in .data (in slower L2) and is touched every iteration: slowest. (Most compilers place a zero-initialised static in .bss instead, which would change this.)

**Concept: memory placement matters on embedded systems.** Without a cache, every access goes to the memory the variable lives in. Keep hot variables in fast memory (locals on a fast stack) and write results out once.

{{< /details >}}

### 16 · reading with a bad low byte

*Asked by: Texas Instruments (TI prep guide)*

A 16K $\times$ 8 memory reads 4 bytes at a time, but at 105 $^\circ$C the least significant
byte of every read is garbage. Write a correct 4-byte read.

{{< details title="Answer and explanation" closed="true" >}}

**Answer: read twice at offset addresses and splice the bytes**

```c
hi = read4bytes(addr);
lo = read4bytes(addr + 1);
return (hi & ~0xFF) | ((lo >> 8) & 0xFF);
```

**Why.** The first read gives correct bytes 1–3 (only byte 0 is garbage). Reading from addr + 1 shifts everything by one byte, so the wanted byte 0 of the original word arrives in byte 1 of the second read, which is reliable. Combine the good parts.

**Concept: working around hardware faults with masks and shifts.** `x & ~0xFF` clears the low byte; `(y >> 8) & 0xFF` extracts byte 1 of y into the low position; `|` merges them.

{{< /details >}}

### 17 · reference ripple

*Asked by: Texas Instruments (NIT Calicut 2023)*

10-bit ADC with a 5 V reference. Maximum peak-to-peak ripple on the reference?

{{< details title="Answer and explanation" closed="true" >}}

**Answer: nearly 5 mV** (about 1 LSB)

**Why.** 1 LSB = 5 V/1024 ≈ 4.9 mV. Ripple on the reference shifts every conversion threshold; to keep errors within about 1 LSB, ripple must stay below roughly that size (stricter designs aim for ½ LSB).

**Concept: reference accuracy.** An ADC measures the input relative to its reference, so any noise or ripple on the reference appears directly as conversion error.

{{< /details >}}

### 18 · 8051 UART transmit

*Asked by: Texas Instruments (BITS Pilani)*

```cpp
void UART_TxChar(char ch) {
    SBUF = ch;
    while (TI == 0);
}
```

What is missing?

- **(a)** TI is not cleared
- **(b)** TI is not initialised
- **(c)** Both
- **(d)** Neither

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) TI is not cleared**

**Why.** The 8051 sets the TI flag when a byte has been sent, but never clears it automatically. Without `TI = 0;` after the wait, the next call finds TI already 1 and doesn't wait, so characters overwrite each other.

**Concept: flag-based polling.** Many peripheral flags must be cleared by software to arm them for the next event. Typical pattern: write data, wait for the flag, clear the flag.

{{< /details >}}
