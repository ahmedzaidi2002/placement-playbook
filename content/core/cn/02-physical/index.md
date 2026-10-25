---
title: "2 · The physical layer"
linkTitle: "2 Physical layer"
weight: 2
math: true
---
## 2.1 Bandwidth, baud, bit rate {#cn-2-1}

- **Bandwidth** $B$ (Hz): the range of frequencies a channel passes. In everyday use, "bandwidth" also means bit rate.
- **Baud rate:** symbols (signal changes) per second. **Bit rate** = baud × bits per symbol. With $L$ levels, each symbol carries $\log_2 L$ bits.
- **Decibels:** $\text{SNR}_{\text{dB}} = 10 \log_{10}(S/N)$. So 10 dB = 10×, 20 dB = 100×, 30 dB = 1000×.

## 2.2 Nyquist and Shannon {#cn-2-2}

<div class="nb nb-theorem nb-block">

<strong>The two limits</strong>

- **Nyquist (noiseless):** $C = 2B \log_2 L$ bits/s, with $L$ signal levels.
- **Shannon (noisy):** $C = B \log_2(1 + S/N)$ bits/s, with $S/N$ as a plain ratio (convert from dB first). No number of levels can beat it.

</div>

<div class="nb nb-example">

<strong>Example</strong> (Phone line)

$B = 3000$ Hz.
- Nyquist with 4 levels: $2 \times 3000 \times \log_2 4 = $ **12,000 bps**.
- Shannon with SNR 30 dB ($S/N = 1000$): $3000 \times \log_2 1001 \approx 3000 \times 9.97 \approx $ **30,000 bps**.
- Levels needed to reach that with Nyquist: $2 \times 3000 \times \log_2 L = 30000$ → $\log_2 L = 5$ → **32 levels**.

</div>

<div class="nb nb-remark">

<strong>Trap</strong> — Plugging decibels straight into Shannon's formula. 30 dB means $S/N = 1000$, not 30.

</div>

## 2.3 Line coding {#cn-2-3}

How bits become voltages:

- **NRZ:** high = 1, low = 0. Long runs of the same bit lose clock sync and give a DC component.
- **NRZ-I:** a transition means 1.
- **Manchester:** every bit has a transition in the middle (1 = low→high, 0 = high→low in the IEEE convention). Self-clocking, no DC, but needs **twice the bandwidth** (classic 10 Mbps Ethernet).
- **Differential Manchester:** a transition at the start of a bit means 0 (used by Token Ring).
- **4B/5B:** maps every 4 data bits to a 5-bit code with enough 1s for clock recovery (25% overhead), then NRZ-I.

## 2.4 Modulation, media, multiplexing {#cn-2-4}

- **Modulation:** ASK (amplitude), FSK (frequency), PSK (phase), **QAM** (amplitude + phase; 16-QAM carries 4 bits per symbol).
- **Guided media:** twisted pair (Ethernet, phone), coaxial cable, **optical fibre** (light; highest bandwidth, immune to electrical interference). **Unguided:** radio, microwave, infrared.
- **Multiplexing** (sharing one link): **FDM** (different frequency bands, radio/TV), **TDM** (time slots, in turn), **WDM** (different light wavelengths in a fibre), **CDMA** (everyone at once, separated by orthogonal codes; cellular).

## 2.5 Switching {#cn-2-5}

| | Circuit switching | Packet switching |
|---|---|---|
| Setup | dedicated path first | none |
| Resources | reserved, wasted when idle | shared on demand |
| Delay | constant after setup | variable (queuing) |
| Example | old telephone | the Internet |

<div class="nb nb-moral">

Nyquist = 2B log₂L (no noise); Shannon = B log₂(1 + S/N) (convert dB first: 30 dB = 1000). Manchester is self-clocking but doubles the bandwidth.

</div>
