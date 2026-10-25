---
title: "8 · Input/output"
linkTitle: "8 Input/output"
weight: 8
math: true
---
## 8.1 Addressing devices {#coa-8-1}

- **Memory-mapped I/O:** device registers occupy ordinary memory addresses; normal load/store instructions access them (ARM, most modern systems). Uses part of the address space.
- **Isolated (port-mapped) I/O:** a separate I/O address space with special instructions (`IN`/`OUT` on x86).

## 8.2 Three ways to transfer data {#coa-8-2}

| Method | How | CPU cost |
|---|---|---|
| **Programmed I/O** | the CPU polls the device's status register in a loop, then moves each word | CPU busy-waits the whole time |
| **Interrupt-driven I/O** | the device interrupts when ready; the CPU moves the word in a handler | one interrupt per word |
| **DMA** | a DMA controller moves a whole block between device and memory; one interrupt at the end | only set-up + one interrupt per block |

<div class="nb nb-example">

<strong>Example</strong> (Why DMA)

A device delivers 1 MB/s. With an interrupt per 4-byte word: 250,000 interrupts/s; at 2 µs each that is 0.5 s of CPU per second = **50%** of the CPU. With DMA in 4 KB blocks: 256 interrupts/s → about **0.05%**.

</div>

**DMA modes:**

- **Burst (block) mode:** the DMA controller holds the bus for a whole block; the CPU waits for memory meanwhile.
- **Cycle stealing:** the controller takes the bus for one word at a time, between CPU memory cycles; the CPU slows slightly but keeps running.
- **Transparent mode:** DMA uses the bus only when the CPU is not using it.

## 8.3 Interrupts {#coa-8-3}

On an interrupt the CPU finishes the current instruction, saves the PC and status, jumps to the **interrupt service routine (ISR)** found through the **interrupt vector table**, and returns with a return-from-interrupt instruction.

- **Maskable** interrupts can be disabled; **non-maskable (NMI)** cannot (power failure, hardware error).
- **Vectored:** the device supplies its handler's address; **non-vectored:** a fixed address.
- **Priority:** a **daisy chain** passes the acknowledge signal down a line of devices (nearest = highest priority); a **programmable interrupt controller** (8259, APIC) arbitrates many sources.
- Intel 8085, a common exam example: TRAP (non-maskable, highest), RST 7.5, RST 6.5, RST 5.5, INTR (lowest).

## 8.4 Buses {#coa-8-4}

A bus has **address**, **data** and **control** lines. **Synchronous** buses use a shared clock; **asynchronous** buses use handshaking. **Bus arbitration** decides which master (CPU, DMA) uses the bus: centralised (daisy chain, polling, independent requests) or distributed. Bus bandwidth = width × clock rate (64 bits at 100 MHz → 800 MB/s).

<div class="nb nb-moral">

Programmed I/O wastes the CPU on polling; interrupts cost one handler per word; DMA moves whole blocks with one interrupt. Memory-mapped I/O uses ordinary loads and stores.

</div>
