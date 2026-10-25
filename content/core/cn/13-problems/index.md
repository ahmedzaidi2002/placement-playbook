---
title: "13 · Practice problems"
linkTitle: "13 Practice"
weight: 13
math: true
---
Fifteen OA-style numericals on new examples. Try, then open the solution.

<div class="nb nb-problem nb-block" id="problem-cn-1">

<strong>Problem 1</strong> (Delay)

1000-byte packet, 1 Mbps link, 4000 km, $v = 2 \times 10^8$ m/s. Time until the last bit arrives?

<details class="nb-sol">
<summary>Solution</summary>

$T_t = 8000/10^6 = 8$ ms; $T_p = 4 \times 10^6/2 \times 10^8 = 20$ ms; total **28 ms**.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-cn-2">

<strong>Problem 2</strong> (Store-and-forward)

5 packets of 1000 bits over 4 links of 1 Mbps, propagation ignored. Total time?

<details class="nb-sol">
<summary>Solution</summary>

Each packet takes 1 ms per link: $(4 + 5 - 1) \times 1 = $ **8 ms**.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-cn-3">

<strong>Problem 3</strong> (Channel capacity)

(a) Noiseless 4 kHz channel with 8 levels. (b) 1 MHz channel with SNR 20 dB.

<details class="nb-sol">
<summary>Solution</summary>

(a) Nyquist: $2 \times 4000 \times 3 = $ **24 kbps**. (b) $S/N = 100$; Shannon: $10^6 \log_2 101 \approx $ **6.66 Mbps**.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-cn-4">

<strong>Problem 4</strong> (CRC)

Data `1011`, generator `101`. Transmitted frame?

<details class="nb-sol">
<summary>Solution</summary>

Append two zeros: `101100`. `101` XOR `101` = `000`; bring down 1 → `001`; bring down 0 → `010`; bring down 0 → `100` XOR `101` = `001`. Remainder **`01`** → frame **`101101`**.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-cn-5">

<strong>Problem 5</strong> (Hamming)

How many check bits correct any single error in 11 data bits? What can a code with $d_{\min} = 4$ do?

<details class="nb-sol">
<summary>Solution</summary>

$2^r \ge 11 + r + 1$ → $r = $ **4** ($16 \ge 16$). $d_{\min} = 4$: detects 3 errors, corrects 1.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-cn-6">

<strong>Problem 6</strong> (Sliding window)

$T_t = 2$ ms, $T_p = 4$ ms. Stop-and-wait efficiency? Window for 100%? Sequence-number bits for GBN and SR?

<details class="nb-sol">
<summary>Solution</summary>

$a = 2$, $\eta = 1/5 = $ **20%**. Window $\ge 1 + 2a = 5$. GBN: $2^k - 1 \ge 5$ → $k = 3$. SR: $2^{k-1} \ge 5$ → $k = 4$.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-cn-7">

<strong>Problem 7</strong> (ALOHA)

$G = 0.25$ frames per frame time. Throughput for pure and slotted ALOHA?

<details class="nb-sol">
<summary>Solution</summary>

Pure: $0.25\,e^{-0.5} = $ **0.152**. Slotted: $0.25\,e^{-0.25} = $ **0.195**.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-cn-8">

<strong>Problem 8</strong> (CSMA/CD)

1 Gbps Ethernet with a 512-bit minimum frame, $v = 2 \times 10^8$ m/s. Maximum cable length?

<details class="nb-sol">
<summary>Solution</summary>

$T_t = 512$ ns $\ge 2T_p$ → $T_p \le 256$ ns → $d \le 256 \times 10^{-9} \times 2 \times 10^8 = $ **51.2 m**. (That is why Gigabit Ethernet extended the minimum frame for half-duplex.)

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-cn-9">

<strong>Problem 9</strong> (Address analysis)

`10.10.10.77/27`: network, broadcast, usable range?

<details class="nb-sol">
<summary>Solution</summary>

Mask .224, block 32; 77 lies in 64–95. Network **10.10.10.64**, broadcast **10.10.10.95**, hosts .65–.94 (**30**).

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-cn-10">

<strong>Problem 10</strong> (Subnets and aggregation)

(a) How many /28 subnets fit in a /24, with how many hosts each? (b) Aggregate `172.16.8.0/24` through `172.16.15.0/24`.

<details class="nb-sol">
<summary>Solution</summary>

(a) $2^4 = $ **16** subnets of **14** hosts. (b) Eight aligned /24s (8 is a multiple of 8) → **`172.16.8.0/21`**.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-cn-11">

<strong>Problem 11</strong> (Fragmentation)

A 2400-byte datagram (20-byte header) meets an MTU of 1000. Fragment sizes, offsets and MF flags?

<details class="nb-sol">
<summary>Solution</summary>

Data 2380 bytes; per fragment at most 980, rounded down to a multiple of 8 = **976**. Fragments carry 976, 976, 428 bytes; offsets **0, 122, 244**; MF = 1, 1, 0.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-cn-12">

<strong>Problem 12</strong> (Window-limited throughput)

TCP window 32 KB, RTT 50 ms. Maximum throughput?

<details class="nb-sol">
<summary>Solution</summary>

$32768 \times 8/0.05 \approx $ **5.24 Mbps**.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-cn-13">

<strong>Problem 13</strong> (Congestion window)

ssthresh = 8 MSS, cwnd starts at 1, no losses. After how many RTTs does cwnd first reach 12?

<details class="nb-sol">
<summary>Solution</summary>

Slow start 1 → 2 → 4 → 8 (3 RTTs), then +1 per RTT: 9, 10, 11, 12 (4 more). **7 RTTs.**

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-cn-14">

<strong>Problem 14</strong> (Token bucket)

Bucket 2 Mb, token rate 1 Mbps, maximum output 5 Mbps, bucket full. How long can it send at 5 Mbps?

<details class="nb-sol">
<summary>Solution</summary>

$S = B/(M - R) = 2/(5 - 1) = $ **0.5 s**.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-cn-15">

<strong>Problem 15</strong> (RSA)

$p = 5$, $q = 11$, $e = 3$. Find $d$ and encrypt $m = 2$.

<details class="nb-sol">
<summary>Solution</summary>

$n = 55$, $\varphi = 40$; $3d \equiv 1 \pmod{40}$ → $d = $ **27** ($81 = 2 \times 40 + 1$). Ciphertext $2^3 \bmod 55 = $ **8**.

</details>

</div>
