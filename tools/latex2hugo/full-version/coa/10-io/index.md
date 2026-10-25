---
title: "10 · Input/output organisation"
linkTitle: "10 Input/output organisation"
weight: 10
math: true
---
I/O devices are slow, varied and asynchronous to the processor. The questions are how the processor addresses them, how it learns that a device needs attention (polling or interrupts), and how data move without wasting the processor’s time (DMA). Interrupt <em>handling</em> inside the OS (handlers, bottom halves, device drivers) is in the OS book.

## 10.1 Addressing devices: memory-mapped and port-mapped I/O {#sec-coa-mmio}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> a UART whose data register is read with an ordinary load from address `0x4000C000`.</em>

</div>

<div class="nb nb-definition" id="definition-10-1-1">

<strong>Definition 10.1.1</strong>. A device appears to the processor as a few <strong>registers</strong>: data (in and out), status (ready, busy, error flags) and control (enable, mode, interrupt enable). With <strong>memory-mapped I/O</strong> these registers occupy addresses in the normal address space and are accessed with ordinary loads and stores; with <strong>port-mapped</strong> (<strong>isolated</strong>) I/O they live in a separate I/O address space reached by special instructions (`IN`, `OUT` on x86) and a separate control signal distinguishing I/O cycles from memory cycles.

</div>

|  | Memory-mapped | Port-mapped (isolated) |
|:--|:--|:--|
| instructions | every load, store and addressing mode | only `IN`/`OUT`-style instructions |
| address space | shared: device addresses are taken from memory | separate; full memory range stays available |
| protection | by the MMU, like memory pages | by I/O privilege rules |
| hardware | one set of control signals | extra I/O read/write signals |
| used by | ARM, RISC-V, MIPS, all microcontrollers; PCIe BARs on x86 | x86 legacy devices (keyboard controller, serial ports) |

<div class="nb-caption" id="table-10-1">

<strong>Table 10.1.</strong> Memory-mapped vs port-mapped I/O. The real advantage of memory-mapped I/O is that the whole instruction set works on device registers; neither style is inherently faster on the bus.

</div>

<div class="nb nb-remark" id="remark-10-1-2">

<strong>Remark 10.1.2</strong> — Memory-mapped device registers must not be cached (the processor would read a stale status) or reordered, and the compiler must not optimise accesses away: in C they are accessed through `volatile` pointers ([Section 13.1](../13-embedded/#sec-coa-volatile)), and the MMU or memory protection unit marks their pages as device or uncacheable memory.

</div>

## 10.2 Programmed I/O and interrupts {#sec-coa-interrupts}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> a keyboard polled 100 times per second costs nothing; a network card polled 250,000 times per second costs a tenth of the processor.</em>

</div>

### 10.2.i Programmed I/O {#s10-2-i}

In <strong>programmed I/O</strong> the processor does everything: it polls the status register in a loop until the device is ready, then moves each word itself. Polling is simple and has the lowest latency when the device is almost always ready, but the waiting is wasted work.

```text {filename="Output of io-numbers.py (Python 3.11)"}
polling keyboard, 100 polls/s: 0.004% of the CPU
polling network card, 250,000 polls/s: 10% of the CPU
interrupts, 20000 transfers/s x 1000 cycles: 2.0% of the CPU
19200 bit/s, 8-bit characters: 2400 transfers/s
  cycle stealing takes 2400 of 2000000 cycles/s = 0.12% slow-down
40 MB/s in 4-byte words = 10000000 words/s; at 50 ns per bus cycle: 50% of the bus
P = 2 ms to prepare, T = 20 us to transfer a block:
  burst mode: CPU blocked T/(P+T) = 0.99%, busy P/(P+T) = 99.01%
  cycle stealing (transfer overlaps preparation): blocked T/P = 1.00%,
    busy 1 - T/P = 99.00%
  transparent (interleaved) DMA: blocked 0%
TRAP (RST 4.5)  vector 8 x 4.5 = 36 = 0x0024
RST 5.5         vector 8 x 5.5 = 44 = 0x002C
RST 6.5         vector 8 x 6.5 = 52 = 0x0034
RST 7.5         vector 8 x 7.5 = 60 = 0x003C
```

The first two lines show both sides: polling cost scales with the polling rate, not with the amount of data.

### 10.2.ii Interrupt-driven I/O {#s10-2-ii}

<div class="nb nb-definition" id="definition-10-2-1">

<strong>Definition 10.2.1</strong>. With <strong>interrupt-driven I/O</strong> the device raises an <strong>interrupt request</strong> when it needs service. At the end of the current instruction the processor saves the PC and status, disables further interrupts (or raises its priority level), and jumps to the <strong>interrupt service routine</strong> (ISR), which ends with a return-from-interrupt that restores them. The processor works on other things meanwhile, but each interrupt costs a context save and restore, so for very high data rates the per-interrupt overhead can exceed the cost of polling (the third line of the output: $2\%$ of the CPU for $20{,}000$ interrupts per second at $1000$ cycles each). Interrupt-driven I/O is more efficient, not always faster.

</div>

<div class="nb nb-definition" id="definition-10-2-2">

<strong>Definition 10.2.2</strong> (Kinds of interrupts). <strong>Vectored</strong>: the device (or interrupt controller) supplies an identifier that indexes a table of ISR addresses, so the right ISR runs directly; <strong>non-vectored</strong>: one common handler polls the devices to find the source. <strong>Maskable</strong> interrupts can be disabled by an interrupt-enable bit or mask register; <strong>non-maskable</strong> interrupts (NMI) cannot, and are reserved for emergencies (power failure, memory parity errors, watchdogs). Hardware interrupts come from pins; <strong>software interrupts</strong> (traps, `INT n`, `syscall`) from instructions; <strong>exceptions</strong> from the instruction itself (divide by zero, page fault). The categories overlap: an interrupt can be vectored and maskable at once.

</div>

<div class="nb nb-example nb-block" id="example-10-2-3">

<strong>Example 10.2.3</strong> (The Intel 8085, a favourite of GATE-style questions)

Hardware interrupts TRAP, RST 7.5, RST 6.5, RST 5.5 and INTR, in decreasing priority. TRAP is non-maskable; the others are maskable. TRAP and the RST $n.5$ inputs are vectored to fixed addresses $8n$ (last lines of the output: $0024_{16}$, $002\mathrm{C}_{16}$, $0034_{16}$, $003\mathrm{C}_{16}$); INTR is non-vectored: the device places an instruction (usually one of the software interrupts RST 0–7) on the data bus.

</div>

### 10.2.iii Priority: daisy chains and interrupt controllers {#s10-2-iii}

<figure class="nb-fig"><img src="fig-1.svg" alt="Figure 1" loading="lazy"></figure>

<div class="nb nb-definition" id="definition-10-2-4">

<strong>Definition 10.2.4</strong>. In a <strong>daisy chain</strong>, all devices share one request line, and the acknowledge signal passes through the devices in order; the first requesting device on the chain keeps the acknowledge and puts its vector on the bus. Priority is fixed by position (the device nearest the processor wins), the hardware is minimal, but a far device can starve and a failed device can break the chain. A <strong>priority interrupt controller</strong> (the 8259 PIC, the APIC, ARM’s GIC) instead takes separate request lines, masks and prioritises them in hardware, and supplies the vector. <strong>Nesting</strong>: an ISR may re-enable interrupts so that higher-priority devices can interrupt it.

</div>

## 10.3 Direct memory access {#sec-coa-dma}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> a disk transfer of a 4 KB block: the processor programs the DMA controller with an address and a count, and hears nothing more until the completion interrupt.</em>

</div>

<div class="nb nb-definition" id="definition-10-3-1">

<strong>Definition 10.3.1</strong>. A <strong>DMA controller</strong> moves blocks between a device and memory without the processor. The processor writes the memory address, the word count, the direction and the device into the controller’s registers and continues; the controller requests the bus, transfers the words, decrements the count and raises an interrupt at the end. Modes:

- <strong>burst</strong> (block) mode: the controller keeps the bus for the whole block; the processor is locked out of the bus for that time;
- <strong>cycle stealing</strong>: the controller takes the bus for one word at a time and gives it back, so the processor is delayed by one memory cycle per word;
- <strong>transparent</strong> (interleaved) mode: the controller uses only cycles in which the processor does not need the bus; the processor is never slowed.

</div>

<div class="nb nb-example nb-block" id="example-10-3-2">

<strong>Example 10.3.2</strong> (DMA numericals from the output)

A $19200$ bit/s serial device delivers $2400$ characters per second; with cycle stealing each steals one memory cycle, so a processor executing $2$ million memory cycles per second loses $2400/2\,000\,000 = 0.12\%$. A $40$ MB/s device moving $4$-byte words on a bus with a $50$ ns cycle needs $10^7$ cycles per second, half the bus. With a preparation time $P$ per block and a transfer time $T$: in burst mode the processor is blocked for $T/(P+T)$ of the time; in cycle-stealing mode the transfer overlaps the preparation of the next data, so it is blocked $T/P$ and busy $1 - T/P$ of the time (not $P/T$).

</div>

<div class="nb nb-remark" id="remark-10-3-3">

<strong>Remark 10.3.3</strong> (DMA and caches) — DMA writes go to memory behind the caches’ back: see [Section 9.10](../09-memory/#sec-coa-coherence) for the coherence problem and the cache clean/invalidate rules embedded programmers must follow.

</div>

## 10.4 Buses and arbitration {#sec-coa-buses}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> the processor and a DMA controller both want the bus in the same cycle.</em>

</div>

<div class="nb nb-definition" id="definition-10-4-1">

<strong>Definition 10.4.1</strong>. A <strong>bus</strong> is a shared set of address, data and control lines. A <strong>synchronous</strong> bus uses a common clock and fixed timing; an <strong>asynchronous</strong> bus uses a request / acknowledge handshake, so devices of different speeds can share it. Only one <strong>bus master</strong> drives the bus at a time; <strong>arbitration</strong> chooses it.

- <strong>daisy chaining</strong> (bus grant passed from device to device): cheap, fixed priority, unfair, one failed device breaks the chain;
- <strong>polling</strong>: the arbiter counts through the device numbers on $\lceil \log_2 n \rceil$ poll-count lines and the first requesting device to see its number takes the bus; priority can be changed by changing the count order;
- <strong>independent requests</strong>: each device has its own request and grant lines to a central arbiter, the fastest and most flexible, and the most wires;
- distributed arbitration: devices put their priority codes on shared lines and withdraw when they see a higher one (no central arbiter).

</div>

<div class="nb nb-remark" id="remark-10-4-2">

<strong>Remark 10.4.2</strong> — Modern systems replace shared parallel buses with point-to-point serial links (PCI Express lanes, on-chip networks), but the master/slave, arbitration and DMA vocabulary is unchanged; on-chip buses such as ARM’s AMBA AXI and AHB are what an embedded engineer meets.

</div>

<div class="nb nb-moral">

Polling wastes the CPU when devices are slow, interrupts waste it when events are very frequent, and DMA takes the CPU out of the data path; arbitration decides who uses the bus, at the cost of fairness, wiring or speed.

</div>
