---
title: "3 · Framing and error control"
linkTitle: "3 Error control"
weight: 3
math: true
---
## 3.1 Framing {#cn-3-1}

The data link layer cuts the bit stream into **frames** and must mark where each starts and ends:

- **Byte count:** a header field gives the length (one corrupted count desynchronises everything).
- **Byte stuffing:** a FLAG byte marks the boundaries; a FLAG or ESC inside the data is preceded by an ESC byte.
- **Bit stuffing:** the flag is `01111110`; the sender inserts a `0` after every five consecutive `1`s in the data, and the receiver removes it.

<div class="nb nb-example">

<strong>Example</strong> (Bit stuffing)

Data `01111110` → after five 1s insert a 0 → sent as `011111010`. The receiver deletes the 0 that follows five 1s.

</div>

## 3.2 Hamming distance {#cn-3-2}

The **Hamming distance** between two codewords is the number of bit positions where they differ (`10110` vs `10011` → 2). The minimum distance $d_{\min}$ of a code decides its power:

<div class="nb nb-theorem nb-block">

<strong>Detect and correct</strong>

- Detects up to $d_{\min} - 1$ bit errors.
- Corrects up to $\lfloor (d_{\min} - 1)/2 \rfloor$ bit errors.
- To **detect** $s$ errors you need $d_{\min} \ge s + 1$; to **correct** $t$ errors, $d_{\min} \ge 2t + 1$.

</div>

Example: $d_{\min} = 5$ → detects 4, corrects 2.

## 3.3 Parity and checksum {#cn-3-3}

- **Single parity bit** (even parity: total number of 1s even): detects any **odd** number of errors, misses even numbers.
- **2-D parity** (row + column parity): detects all 1-, 2- and 3-bit errors and can **correct** a single-bit error.
- **Internet checksum** (IP, TCP, UDP): add the data as 16-bit words in one's-complement arithmetic (wrap carries around) and send the complement. Cheap, weaker than CRC.

## 3.4 CRC (cyclic redundancy check) {#cn-3-4}

Treat bits as a polynomial. With a **generator** of degree $r$ ($r+1$ bits): append $r$ zeros to the data, divide by the generator using XOR (mod-2) division, and send the data followed by the $r$-bit **remainder**. The receiver divides the whole frame; a non-zero remainder means an error.

<div class="nb nb-example">

<strong>Example</strong> (CRC by hand)

Data `1101`, generator `1011` ($x^3 + x + 1$, so $r = 3$). Dividend `1101000`:

- `1101` XOR `1011` = `0110` → bring down 0 → `1100`
- `1100` XOR `1011` = `0111` → bring down 0 → `1110`
- `1110` XOR `1011` = `0101` → bring down 0 → `1010`
- `1010` XOR `1011` = `0001` → remainder **`001`**

Transmitted frame: `1101` + `001` = **`1101001`**. Dividing `1101001` by `1011` leaves 0, so the receiver accepts it.

</div>

**What a CRC with an $r$-bit remainder catches:** all single-bit errors, all odd numbers of errors if the generator has the factor $(x + 1)$, and **all burst errors of length $\le r$**. It is the standard for Ethernet and Wi-Fi frames.

## 3.5 Hamming code (error correction) {#cn-3-5}

To **correct** any single-bit error in $m$ data bits you need $r$ check bits with

$$2^r \ge m + r + 1.$$

<div class="nb nb-example">

<strong>Example</strong> (Check bits)

$m = 4$ → $r = 3$ ($8 \ge 8$): the classic **Hamming(7,4)** code. $m = 7$ → $r = 4$ ($16 \ge 12$). $m = 32$ → $r = 6$ ($64 \ge 39$).

</div>

Check bits sit at positions 1, 2, 4, 8, …; each covers the positions whose binary index has that bit set. On receipt, the failed checks spell out the **position of the wrong bit** (the syndrome), which is flipped back.

**Detection vs correction:** detection + retransmission is cheaper on reliable links (wired); forward error correction is used where retransmission is costly (wireless, satellite, storage).

<div class="nb nb-moral">

Detect $d_{\min} - 1$ errors, correct $\lfloor (d_{\min}-1)/2 \rfloor$. CRC: append $r$ zeros, XOR-divide, send the remainder. Hamming check bits: smallest $r$ with $2^r \ge m + r + 1$.

</div>
