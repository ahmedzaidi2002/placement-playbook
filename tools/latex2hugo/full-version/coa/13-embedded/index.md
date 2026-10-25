---
title: "13 · Embedded systems"
linkTitle: "13 Embedded systems"
weight: 13
math: true
---
Texas Instruments and Qualcomm build microcontrollers, DSPs and SoCs, and their interviews probe whether you can program hardware directly: device registers, `volatile`, interrupt service routines and the data they share, bit manipulation, DMA, byte order on the wire, timers and clocks. This chapter collects those topics; the C behind them was compiled and run, and the hardware numericals computed.

## 13.1 Memory-mapped registers and `volatile` {#sec-coa-volatile}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> `while ((STATUS & 1) == 0) ` compiled at `-O2`: without `volatile` the loop reads the register once and then spins for ever.</em>

</div>

A microcontroller’s peripherals (GPIO, timers, UARTs, ADCs) are controlled through registers at fixed addresses ([Section 10.1](../10-io/#sec-coa-mmio)). C reaches them through pointers to those addresses, and that is where the optimiser bites:

```c {filename="volatile-s.c"}
// flags: -O2 -masm=intel
// Busy-waiting on a status register, without and with volatile.
#include <stdint.h>
#define STATUS_ADDR 0x40021000u

void wait_plain(void) {            /* the compiler may read the register once */
    uint32_t *status = (uint32_t *)STATUS_ADDR;
    while ((*status & 1u) == 0) { }
}

void wait_volatile(void) {         /* every iteration performs a real load */
    volatile uint32_t *status = (volatile uint32_t *)STATUS_ADDR;
    while ((*status & 1u) == 0) { }
}
```

```text {filename="Assembly from gcc -S (gcc 13.3, -std=c11, x86-64 Linux, -O2 -masm=intel)"}
wait_plain:
    test    BYTE PTR ds:1073876992, 1
    jne .L1
.L3:
    jmp .L3
.L1:
    ret
wait_volatile:
.L6:
    mov eax, DWORD PTR ds:1073876992
    test    al, 1
    je  .L6
    ret
```

<div class="nb nb-example nb-block" id="example-13-1-1">

<strong>Example 13.1.1</strong> (Reading the assembly)

In `wait_plain` the compiler assumed that nothing else changes `*status`, so it tested the bit once; if it was clear, the code jumps to `.L3`, an infinite loop with no load in it. Only the `volatile` version reloads the register on every iteration. The hardware changing the register behind the program’s back is exactly what `volatile` tells the compiler to expect.

</div>

<div class="nb nb-definition" id="definition-13-1-2">

<strong>Definition 13.1.2</strong>. A `volatile`-qualified object may change, or its access may have side effects, in ways the compiler cannot see: every read and write in the source must be performed, in program order relative to other volatile accesses, with the declared width. Use it for memory-mapped registers, for variables shared between an ISR and the main loop, and for variables modified by `longjmp` or signal handlers.

</div>

<div class="nb nb-remark" id="remark-13-1-3">

<strong>Remark 13.1.3</strong> (What `volatile` does not do) — It does not make an access atomic (a 32-bit variable on an 8-bit MCU is still read in pieces), does not order accesses with respect to non-volatile ones, and does not insert the hardware memory barriers multicore code needs ([Section 12.3](../12-parallel/#sec-coa-consistency)). Device register access on a cached, out-of-order core also needs the region mapped as device (uncached, strongly ordered) memory and, where the architecture requires it, barrier instructions (ARM’s `DMB`/`DSB`).

</div>

<div class="nb nb-ques" id="question-13-1-4">

<strong>Question 13.1.4</strong> — Can a variable be both `const` and `volatile`?

</div>

Yes: a read-only status register is the textbook case. `const` means the program may not write it; `volatile` means its value may change anyway.

## 13.2 Bit manipulation on registers {#sec-coa-bitregs}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> set the 3-bit MODE field of a control register to $5$ without disturbing the other $29$ bits.</em>

</div>

```c {filename="bitfields.c"}
#include <stdio.h>
#include <stdint.h>

/* A 32-bit control register: EN bit 0, MODE bits 3..1, PRESCALER bits 15..8. */
#define EN_POS    0u
#define MODE_POS  1u
#define MODE_MASK (0x7u << MODE_POS)
#define PSC_POS   8u
#define PSC_MASK  (0xFFu << PSC_POS)

static uint32_t set_field(uint32_t reg, uint32_t mask, uint32_t pos,
                          uint32_t v) {
    return (reg & ~mask) | ((v << pos) & mask);    /* read-modify-write */
}

struct ctrl_bits {               /* the same layout as a C bit-field struct */
    unsigned en : 1, mode : 3, unused : 4, psc : 8;
};

int main(void) {
    uint32_t reg = 0xA5A50000u;                 /* other bits must survive */
    reg |= 1u << EN_POS;                            /* set EN */
    reg = set_field(reg, MODE_MASK, MODE_POS, 5);   /* MODE = 5 */
    reg = set_field(reg, PSC_MASK, PSC_POS, 63);    /* PRESCALER = 63 */
    printf("reg = 0x%08X\n", reg);
    printf("MODE = %u, PRESCALER = %u, EN = %u\n",
           (reg & MODE_MASK) >> MODE_POS, (reg & PSC_MASK) >> PSC_POS,
           reg >> EN_POS & 1u);
    reg &= ~(1u << EN_POS);                         /* clear EN */
    reg ^= 1u << 31;                                /* toggle bit 31 */
    printf("after clear EN, toggle bit 31: 0x%08X\n", reg);

    struct ctrl_bits b = {.en = 1, .mode = 5, .psc = 63};
    uint32_t raw = 0;
    __builtin_memcpy(&raw, &b, sizeof b < 4 ? sizeof b : 4);
    printf("bit-field struct: sizeof %zu, bits 0x%08X (gcc, x86-64)\n",
           sizeof b, raw);
    return 0;
}
```

```text {filename="Output (gcc 13.3, -std=c11, x86-64 Linux)"}
reg = 0xA5A53F0B
MODE = 5, PRESCALER = 63, EN = 1
after clear EN, toggle bit 31: 0x25A53F0A
bit-field struct: sizeof 4, bits 0x00003F0B (gcc, x86-64)
```

<div class="nb nb-definition" id="fact-13-2-1">

<strong>Fact 13.2.1</strong> (The idioms). Set bit $n$: `reg |= 1u << n`; clear: `reg &= ~(1u << n)`; toggle: `reg ^= 1u << n`; test: `(reg >> n) & 1u`; write a field: `reg = (reg & ~ MASK) | ((v << POS) & MASK)`. Use unsigned constants (`1u`): `1 << 31` overflows a signed `int`.

</div>

<div class="nb nb-remark" id="remark-13-2-2">

<strong>Remark 13.2.2</strong> (Read-modify-write hazards and bit-fields) — A read-modify-write of a register is three steps; an ISR that modifies the same register between the read and the write loses its update. Disable the interrupt around it, or use hardware that avoids it: separate set and clear registers (writing $1$ to a bit of a “set” register sets only that bit), or bit-banding on some ARM Cortex-M parts. C bit-field structs look tempting for registers, and here gcc on x86-64 laid the fields out exactly as the masks did (`0x3F0B`), but bit order, padding and access width are implementation-defined, so portable driver code uses masks and shifts.

</div>

## 13.3 Interrupt service routines and shared data {#sec-coa-isr}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> a 16-bit tick counter updated by a timer ISR and read by the main loop of an 8-bit microcontroller: the read can return a value the counter never had.</em>

</div>

<div class="nb nb-definition" id="fact-13-3-1">

<strong>Fact 13.3.1</strong> (Rules for ISRs). Keep ISRs short: acknowledge the interrupt (clear the peripheral’s flag, or it will fire again immediately), move data to or from a buffer, set a flag, return; do the processing in the main loop or a task. Do not block, sleep, call non-reentrant functions (`malloc`, `printf`) or take locks the main code might hold.

</div>

```text {filename="Output of embedded.py (Python 3.11)"}
prescaler    1, 8-bit timer: tick 0.0625 us, overflow every 0.016 ms
prescaler   64, 8-bit timer: tick 4 us, overflow every 1.024 ms
prescaler   64, 16-bit timer: tick 4 us, overflow every 262.144 ms
prescaler 1024, 16-bit timer: tick 64 us, overflow every 4194.3 ms
1 ms with prescaler 64: compare value 250 (counter runs 0..249)
  9600 baud: divisor 104.17 -> 104, actual 9615 baud, error +0.16%
115200 baud: divisor 8.68 -> 9, actual 111111 baud, error -3.55%
PWM period 1000 counts at 16 MHz = 16 kHz; 30% duty -> compare 300
16-bit counter read in two 8-bit halves, ISR increments it in between:
0x00FF -> 0x0100 mid-read: low byte first gives 0x01FF, high byte first 0x0000
0x12FF -> 0x1300 mid-read: low byte first gives 0x13FF, high byte first 0x1200
0x1234 -> 0x1235 mid-read: low byte first gives 0x1234, high byte first 0x1235
```

<div class="nb nb-example nb-block" id="example-13-3-2">

<strong>Example 13.3.2</strong> (The torn read, in the last lines of the output)

An 8-bit processor reads a 16-bit counter in two instructions. If the ISR increments `0x00FF` to `0x0100` between them, the main loop sees `0x01FF` (low byte first) or `0x0000` (high byte first): values the counter never held. Fixes: disable interrupts around the read (a <strong>critical section</strong>), read twice until two consecutive reads agree, or use a type the processor accesses atomically. And the shared variable must be `volatile`, or the main loop may never re-read it at all.

</div>

<div class="nb nb-remark" id="remark-13-3-3">

<strong>Remark 13.3.3</strong> (Producer/consumer between an ISR and the main loop) — A single-producer, single-consumer <strong>ring buffer</strong> needs no lock: the ISR only writes the head index, the main loop only writes the tail, each index fits in one atomic access, and the buffer is full when advancing the head would reach the tail. Every UART driver is built this way.

</div>

## 13.4 DMA, caches and buffers in embedded systems {#sec-coa-emb-dma}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> an ADC streaming samples into memory by DMA while the CPU processes the previous block.</em>

</div>

Embedded DMA controllers move data between peripherals and memory ([Section 10.3](../10-io/#sec-coa-dma)), usually triggered by the peripheral itself (“ADC sample ready”, “UART byte received”). <strong>Double buffering</strong> (ping-pong): the DMA fills buffer A while the CPU processes B, and a half-transfer or transfer-complete interrupt swaps them; <strong>circular</strong> mode restarts automatically. On a core with a data cache and a DMA engine that does not snoop, the driver must <em>clean</em> (write back) the buffer before the DMA reads it and <em>invalidate</em> it before the CPU reads what the DMA wrote, and the buffer should be aligned to and sized in whole cache lines so that invalidation cannot destroy a neighbour’s data ([Section 9.10](../09-memory/#sec-coa-coherence)).

## 13.5 Byte order on the wire {#sec-coa-emb-wire}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> a 32-bit length field arriving big-endian at offset $3$ of a packet.</em>

</div>

```c {filename="wire-endian.c"}
#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <arpa/inet.h>

/* A header sent big-endian ("network order"): type (16 bits), length (32). */
static void put16(uint8_t *p, uint16_t v) { p[0] = v >> 8; p[1] = v & 0xFF; }
static void put32(uint8_t *p, uint32_t v) {
    p[0] = v >> 24; p[1] = v >> 16 & 0xFF;
    p[2] = v >> 8 & 0xFF; p[3] = v & 0xFF;
}
static uint32_t get32(const uint8_t *p) {
    return (uint32_t)p[0] << 24 | (uint32_t)p[1] << 16 |
           (uint32_t)p[2] << 8 | p[3];
}

int main(void) {
    uint8_t buf[7] = {0};
    put16(buf + 1, 0x0102);            /* fields at odd offsets: unaligned */
    put32(buf + 3, 1000000);
    printf("bytes on the wire:");
    for (int i = 0; i < 7; i++) printf(" %02X", buf[i]);
    printf("\n");
    uint32_t len;
    memcpy(&len, buf + 3, 4);          /* safe unaligned read, but host order */
    printf("memcpy only: %u; ntohl: %u; shifts: %u\n",
           len, ntohl(len), get32(buf + 3));
    printf("__builtin_bswap32(0x%08X) = 0x%08X\n", 0x12345678u,
           __builtin_bswap32(0x12345678u));
    return 0;
}
```

```text {filename="Output (gcc 13.3, -std=c11, x86-64 Linux)"}
bytes on the wire: 00 01 02 00 0F 42 40
memcpy only: 1078071040; ntohl: 1000000; shifts: 1000000
__builtin_bswap32(0x12345678) = 0x78563412
```

<div class="nb nb-definition" id="fact-13-5-1">

<strong>Fact 13.5.1</strong>. Protocols fix a byte order (Internet protocols: big-endian), so parsers must convert: `htons/htonl` and `ntohs/ntohl` (identity on big-endian hosts, a byte swap on little-endian ones), or assemble the value with shifts, which works on any host. Never cast a buffer pointer to `uint32_t *` to read a field: the field may be misaligned (a fault on many cores) and the cast breaks C’s aliasing rules; `memcpy` into a variable and then convert. Two bytes that happen to read the same both ways (`0x0102` vs `0x0201`) are how byte-order bugs hide in testing.

</div>

## 13.6 Clocks, timers, power and watchdogs {#sec-coa-emb-clocks}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> a 16 MHz clock, prescaler $64$, compare value $250$: an interrupt every millisecond.</em>

</div>

<div class="nb nb-definition" id="fact-13-6-1">

<strong>Fact 13.6.1</strong> (Timer and UART arithmetic, from the output above). A timer driven by $f$ through a prescaler $p$ ticks every $p/f$; an $n$-bit timer overflows every $2^n p / f$. For a periodic interrupt of period $T$, set the compare value to $Tf/p$: $1\,\text{ms} \times 16\,\text{MHz}/64 = 250$. A UART with $16\times$ oversampling needs a divisor $f/(16 \cdot \text{baud})$: $104.17$ rounds to $104$ for $9600$ baud ($+0.16\%$ error, fine), but $8.68$ rounds to $9$ for $115200$ baud ($-3.55\%$, too much for reliable reception; such parts use fractional dividers or a different clock). PWM: period $=$ timer period, duty cycle $=$ compare $/$ period.

</div>

<div class="nb nb-definition" id="definition-13-6-2">

<strong>Definition 13.6.2</strong>. A <strong>watchdog timer</strong> counts down independently of the software and resets the system when it reaches zero; healthy software periodically “kicks” (reloads) it, so a hung program is restarted automatically. Kick it from the main loop after checking that every task made progress, never from a timer ISR, which keeps running when the main loop is stuck.

</div>

<div class="nb nb-definition" id="fact-13-6-3">

<strong>Fact 13.6.3</strong> (Power). Microcontrollers save power by stopping clocks: <strong>clock gating</strong> of unused peripherals, then sleep modes that stop the CPU clock (woken by an interrupt), then deep sleep and standby modes that stop most clocks and lower the voltage, at the cost of a longer wake-up and, in the deepest modes, lost RAM contents. Dynamic power follows $\alpha C V^2 f$ ([Section 11.3](../11-perf/#sec-coa-power)); the energy-optimal strategy is often “race to sleep”: run fast, then sleep deeply. Clock sources trade accuracy against power and start-up time: crystal oscillators are accurate, internal RC oscillators start fast but drift, and PLLs multiply a reference clock up to the core frequency.

</div>

<div class="nb nb-moral">

Embedded code talks to hardware through registers: make every such access `volatile`, modify fields with masks, keep ISRs short and their shared data atomic, keep caches and DMA consistent by hand, convert byte order explicitly, and let a watchdog catch what you missed.

</div>
