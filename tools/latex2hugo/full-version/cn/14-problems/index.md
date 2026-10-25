---
title: "14 · A few harder problems to think about"
linkTitle: "14 A few harder problems to think about"
weight: 14
math: true
---
The problems follow the patterns of online assessments and GATE-style papers: numericals, “which statements are true (more than one may be)”, and route or address selection. Every number in a solution was computed by a script in `code/` (the `prob_*.py` files and the chapter scripts they reuse). Hints are in the <em>Hint</em> drop-down under each problem, solutions in the <em>Solution</em> drop-down under each problem. Chilis mark the harder ones.

## 14.1 Layers, topologies and delay {#s14-1}

<div class="nb nb-problem nb-block" id="problem-14-1">

<strong>Problem 14.1</strong> (Which layer, which unit)

Which of the following statements are true? (More than one may be.)

1. Frames are the protocol data units of the data link layer.
2. The physical layer adds a trailer to each frame for error detection.
3. A layer-2 switch must implement the network layer to forward frames.
4. A router forwards packets using the destination IP address and must also implement the data link and physical layers on each interface.
5. In the TCP/IP model the transport-layer PDU of UDP is called a datagram.

<details class="nb-hint">
<summary>Hint</summary>

Who computes the FCS? What does a switch read in a frame?

</details>

<details class="nb-sol">
<summary>Solution</summary>

(a), (d), (e). The FCS trailer is added by the data link layer, not the physical layer (b is false). A switch reads only MAC addresses and needs no IP (c is false), though a managed switch may run IP for its own management interface.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-14-2">

<strong>Problem 14.2</strong> (Ring failure)

Eight stations form a single token ring. The network interface of station 5 burns out and stops repeating. (i) What happens to communication between stations 1 and 2, who are adjacent and both before station 5? (ii) What changes if the stations are on an FDDI-style dual counter-rotating ring? (iii) On the dual ring, what does a second failure, at station 1, do?

<details class="nb-hint">
<summary>Hint</summary>

Who removes a frame from a token ring, and where does the token have to go?

</details>

<details class="nb-sol">
<summary>Solution</summary>

(i) All communication stops, including between 1 and 2: the token can no longer circulate, and a sender only removes its frame when it returns round the loop. (ii) The neighbours of station 5 (stations 4 and 6) wrap the primary ring onto the secondary ring; the seven survivors form one loop and keep working. (iii) Two failures cut the doubled ring in two places: it splits into two islands, $\{2,3,4\}$ and $\{6,7,8\}$, that cannot reach each other (`topology.py` shows the same effect with six stations: $4$ of $12$ ordered pairs survive).

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-14-3">

<strong>Problem 14.3</strong> (Store-and-forward with headers)

A $4$ MB file ($4\times10^6$ bytes) is sent over $4$ links in series, each $8$ Mbps and $500$ km long ($v = 2\times10^8$ m/s). It is split into packets with a $1000$-byte payload and a $40$-byte header. Ignoring queuing and processing, when does the last bit arrive? How long would it take as a single message with one $40$-byte header?

<details class="nb-hint">
<summary>Hint</summary>

$T = (N+P-1)(L+h)/R + N\,T_p$.

</details>

<details class="nb-sol">
<summary>Solution</summary>

$P = 4000$ packets of $8320$ bits, $1.04$ ms each; $T_p = 2.5$ ms per link. $T = (4 + 4000 - 1)\times 1.04\text{ ms} + 4 \times 2.5\text{ ms} = 4.17312$ s. As one message: $4 \times (32{,}000{,}320/8\times10^6) + 0.01 = 16.01016$ s. Pipelining makes the four hops cost almost as little as one.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-14-4">

<strong>Problem 14.4</strong> (The window is the bottleneck)

A host downloads over a $100$ Mbps path with an RTT of $80$ ms. The receiver advertises a window of $65{,}535$ bytes and does not use window scaling. What is the best possible throughput and the link utilisation? What window-scale shift would let one connection fill the path?

<details class="nb-hint">
<summary>Hint</summary>

Throughput $\le W/\mathrm{RTT}$; compare $W$ with the bandwidth–delay product.

</details>

<details class="nb-sol">
<summary>Solution</summary>

$65535 \times 8 / 0.08 = 6.5535$ Mbps, a utilisation of $6.55\%$. The BDP is $10^8 \times 0.08 / 8 = 10^6$ bytes, so the window must grow by a factor $10^6/65535 \approx 15.3$: the smallest shift is $s = 4$ (factor $16$).

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-14-5">

<strong>Problem 14.5</strong> 🌶 (Best packet size)

A $2$ MB ($16\times10^6$-bit) message crosses $5$ store-and-forward links of equal rate. Each packet carries a $256$-bit header. Propagation and processing are negligible. Into how many packets should the message be split to minimise the delivery time, and what is the payload per packet?

<details class="nb-hint">
<summary>Hint</summary>

Minimise $(N+P-1)(M/P + h)$; only $(N-1)M/P + Ph$ depends on $P$.

</details>

<details class="nb-sol">
<summary>Solution</summary>

$P = \sqrt{(N-1)M/h} = \sqrt{4 \times 16\times10^6/256} = 500$ packets of $32{,}000$ bits of payload. An exhaustive search over integer $P$ gives the same $500$. Fewer packets lose pipelining; more packets waste time on headers.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-14-6">

<strong>Problem 14.6</strong> (When does propagation dominate?)

Packets are $1250$ bytes. For link rates of $1$, $10$ and $100$ Mbps, at what link length does the propagation delay equal the transmission delay ($v = 2\times10^8$ m/s)? What does that imply for $a = T_p/T_t$ on a $200$ km link at $100$ Mbps?

<details class="nb-hint">
<summary>Hint</summary>

Solve $d/v = L/R$.

</details>

<details class="nb-sol">
<summary>Solution</summary>

$d = vL/R$: $2000$ km, $200$ km and $20$ km. At $100$ Mbps a $200$ km link has $a = 10$: ten packets fit on the wire, so stop-and-wait would idle the link most of the time ([Chapter 4](../04-arq/)).

</details>

</div>

## 14.2 Physical layer {#s14-2}

<div class="nb nb-problem nb-block" id="problem-14-7">

<strong>Problem 14.7</strong> (Shannon, then Nyquist)

A $4$ kHz channel has an SNR of $30$ dB. (i) What is its Shannon capacity? (ii) A designer decides to run it at $32$ kbps with a multilevel baseband signal. How many levels does Nyquist require? (iii) What answer to (i) does a student get who forgets to convert the decibels?

<details class="nb-hint">
<summary>Hint</summary>

$30$ dB is a power ratio of $10^{3}$.

</details>

<details class="nb-sol">
<summary>Solution</summary>

(i) $C = 4000\log_2(1001) \approx 39{,}869$ bit/s. (ii) $32000 = 2 \cdot 4000 \log_2 L$ gives $L = 2^4 = 16$ levels. (iii) $4000\log_2 31 \approx 19{,}817$ bit/s, about half the correct value (`prob_phys.py`).

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-14-8">

<strong>Problem 14.8</strong> (Baud or bits)

Which statements are true? (More than one may be.)

1. A 64-QAM modem at $4000$ baud carries $24$ kbps.
2. Manchester encoding of $100$ Mbps would need $200$ Mbaud.
3. In NRZ-I, a long run of $1$s produces no transitions.
4. Differential Manchester has a transition in the middle of every bit.
5. 4B/5B coding raises the signal rate by $25\%$.

<details class="nb-hint">
<summary>Hint</summary>

$\log_2 64$; two signal elements per bit; which bit value inverts in NRZ-I?

</details>

<details class="nb-sol">
<summary>Solution</summary>

(a), (b), (d), (e). In NRZ-I every $1$ inverts the level, so a run of $1$s toggles every bit; it is a run of $0$s that stays flat (c is false). That is why 4B/5B, which limits runs of $0$s to three, is paired with NRZ-I.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-14-9">

<strong>Problem 14.9</strong> (A TDM frame)

Ten $64$ kbps voice channels are multiplexed by synchronous TDM with one $8$-bit slot per channel per frame and one synchronisation bit per frame. Find the frame rate, the frame length, the link rate and the fraction of the link that carries voice.

<details class="nb-hint">
<summary>Hint</summary>

Each channel must send one byte per frame.

</details>

<details class="nb-sol">
<summary>Solution</summary>

$64000/8 = 8000$ frames/s; $10 \times 8 + 1 = 81$ bits per frame; link $8000 \times 81 = 648$ kbps; efficiency $640/648 \approx 0.988$.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-14-10">

<strong>Problem 14.10</strong> (Circuit or packets)

A $2$ Mbit message crosses $6$ hops of $2$ Mbps, with $2$ ms of propagation per hop. Packets are $8000$ bits (headers ignored). For which circuit setup times is circuit switching faster than store-and-forward packet switching?

<details class="nb-hint">
<summary>Hint</summary>

Compare $s + x/b + kd$ with $x/b + (k-1)p/b + kd$.

</details>

<details class="nb-sol">
<summary>Solution</summary>

Circuit switching wins when $s < (k-1)p/b = 5 \times 8000 / (2\times10^6) = 20$ ms. Packet switching takes $1 + 0.02 + 0.012 = 1.032$ s in total.

</details>

</div>

## 14.3 Framing and error control {#s14-3}

<div class="nb nb-problem nb-block" id="problem-14-11">

<strong>Problem 14.11</strong> (A CRC by hand)

Compute the CRC for the data `1010001101` with the generator $x^5+x^4+x^2+1$, and write the transmitted frame.

<details class="nb-hint">
<summary>Hint</summary>

The generator is `110101`; append five zeros and divide modulo 2.

</details>

<details class="nb-sol">
<summary>Solution</summary>

Remainder `01110`; frame `101000110101110`. Dividing the frame by the generator leaves `00000` (`prob_errors.py`).

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-14-12">

<strong>Problem 14.12</strong> (Correct the codeword)

A Hamming(7,4) code with even parity has parity bits at positions $1$, $2$ and $4$ and data bits at $3$, $5$, $6$, $7$. The word `1011011` is received (position $1$ first). Which bit is wrong, and what were the four data bits?

<details class="nb-hint">
<summary>Hint</summary>

XOR together the positions of all the $1$ bits.

</details>

<details class="nb-sol">
<summary>Solution</summary>

The $1$s are at positions $1,3,4,6,7$; $1\oplus3\oplus4\oplus6\oplus7 = 7$, so bit $7$ is wrong. The corrected word is `1011010`, and the data bits (positions $3,5,6,7$) are `1010`. Re-encoding `1010` gives `1011010` again.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-14-13">

<strong>Problem 14.13</strong> (Distance of a code)

The code has the four codewords `00000`, `01011`, `10101`, `11110`. How many errors can it detect, and how many can it correct?

<details class="nb-hint">
<summary>Hint</summary>

Compute all six pairwise distances.

</details>

<details class="nb-sol">
<summary>Solution</summary>

$d_{\min} = 3$ (for example `00000` and `01011`); it detects $2$ and corrects $1$.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-14-14">

<strong>Problem 14.14</strong> (Internet checksum)

Compute the Internet checksum of the three 16-bit words `1234`, `F00F`, `ABCD` (hex), and verify it as the receiver would.

<details class="nb-hint">
<summary>Hint</summary>

Add in one’s complement: every carry out of the top bit is added back at the bottom.

</details>

<details class="nb-sol">
<summary>Solution</summary>

$\texttt{1234} + \texttt{F00F} = \texttt{10243} \to \texttt{0244}$; $\texttt{0244} + \texttt{ABCD} = \texttt{AE11}$. The checksum is $\lnot \texttt{AE11} = \texttt{51EE}$. The receiver adds all four words and gets `FFFF`.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-14-15">

<strong>Problem 14.15</strong> (Unstuff it)

Between two flags an HDLC receiver finds the body

$$
\texttt{0111110111110011111010}.
$$

What data did the sender’s network layer hand down?

<details class="nb-hint">
<summary>Hint</summary>

Delete every `0` that follows five consecutive `1`s.

</details>

<details class="nb-sol">
<summary>Solution</summary>

`0111111111101111110`: three stuffed zeros removed. Stuffing that again reproduces the received body.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-14-16">

<strong>Problem 14.16</strong> 🌶 (CRC statements)

Which statements are true? (More than one may be.)

1. With $G(x) = x+1$ every double-bit error is detected.
2. With $G(x) = x+1$ every error flipping an odd number of bits is detected.
3. A CRC with a degree-$16$ generator that has a constant term detects every burst of length $16$ or less.
4. If $G(x)$ divides the error polynomial $E(x)$, the receiver accepts the frame.
5. A Hamming code for $32$ data bits needs $5$ check bits.

<details class="nb-hint">
<summary>Hint</summary>

$x+1$ is plain parity. For (e), use $2^r \ge m+r+1$.

</details>

<details class="nb-sol">
<summary>Solution</summary>

(b), (c), (d). $x+1$ divides $x^i + x^j$, so double errors escape (a is false). For $m = 32$, $r = 5$ gives $32 < 38$; $r = 6$ is needed (e is false).

</details>

</div>

## 14.4 Flow control and ARQ {#s14-4}

<div class="nb nb-problem nb-block" id="problem-14-17">

<strong>Problem 14.17</strong> (Satellite link)

A $1.5$ Mbps geostationary link has a one-way propagation delay of $270$ ms; frames are $1000$ bytes. (i) What is the efficiency and throughput of stop-and-wait? (ii) What is the smallest window that keeps the link busy, and how many sequence-number bits does it need with Go-Back-N and with Selective Repeat? (iii) What efficiency does a window of $63$ give?

<details class="nb-hint">
<summary>Hint</summary>

$a = T_p/T_t$; GBN needs $2^k-1 \ge W$, SR needs $2^{k-1} \ge W$.

</details>

<details class="nb-sol">
<summary>Solution</summary>

$T_t = 8000/1.5\times10^6 = 5.333$ ms, $a = 50.625$. (i) $\eta = 1/(1+2a) = 0.00978$, about $14.7$ kbps. (ii) $W \ge 1+2a = 102.25$, so $W = 103$: $7$ bits for GBN ($127 \ge 103$), $8$ bits for SR ($128 \ge 103$). (iii) $63/102.25 = 0.616$.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-14-18">

<strong>Problem 14.18</strong> 🌶🌶 (Count the transmissions)

Eight frames are sent with a window of $3$. Use the model of `arq_sim.py`: one time unit per frame, ACKs (never lost) return $4$ units after a frame ends, timeout $6$ units, and every fourth transmission (counting retransmissions) is lost. How many transmissions does Go-Back-N need? Selective Repeat?

<details class="nb-hint">
<summary>Hint</summary>

Number the transmissions as they happen and mark every fourth as lost. In GBN, a timeout resends the oldest unacknowledged frame and everything after it.

</details>

<details class="nb-sol">
<summary>Solution</summary>

GBN: $19$ transmissions, `1 2 3 4x 5 6 4 5x 6 7 5 6x 7 8 6 7x 8 7 8`. SR: $10$ transmissions, `1 2 3 4x 5 6 4 7x 8 7`. Each GBN loss costs a window of retransmissions, and those retransmissions themselves run into the “every fourth” rule; SR pays only for the lost frames.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-14-19">

<strong>Problem 14.19</strong> (Window statements)

Sequence numbers have $5$ bits. Which statements are true? (More than one may be.)

1. Go-Back-N can use a send window of $32$.
2. Selective Repeat can use send and receive windows of $16$.
3. Go-Back-N’s receiver needs a buffer for $31$ out-of-order frames.
4. In Selective Repeat the sender keeps one timer per outstanding frame.
5. With a cumulative ACK, a lost ACK can be compensated by a later one.

<details class="nb-hint">
<summary>Hint</summary>

$W_s + W_r \le 2^k$.

</details>

<details class="nb-sol">
<summary>Solution</summary>

(b), (d), (e). GBN’s maximum is $2^5 - 1 = 31$ (a is false), and its receiver window is $1$: it discards out-of-order frames and needs no reordering buffer (c is false).

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-14-20">

<strong>Problem 14.20</strong> (Lossy stop-and-wait)

On a link with $a = 0.5$, each frame is lost with probability $0.2$ (ACKs are never lost, and a timeout costs exactly one cycle). What is the efficiency of stop-and-wait, and how many times is a frame sent on average?

<details class="nb-hint">
<summary>Hint</summary>

Transmissions per frame are geometric.

</details>

<details class="nb-sol">
<summary>Solution</summary>

$1/(1-p) = 1.25$ transmissions per frame; $\eta = (1-p)/(1+2a) = 0.8/2 = 0.4$.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-14-21">

<strong>Problem 14.21</strong> (The whole cycle)

A $4$ Mbps link carries $4000$-bit frames with stop-and-wait. $T_p = 2$ ms, the ACK is $400$ bits and the receiver needs $0.5$ ms to process a frame before acknowledging it. Find the efficiency and the throughput.

<details class="nb-hint">
<summary>Hint</summary>

Cycle $= T_t + T_p + T_{\text{proc}} + T_{t,\text{ack}} + T_p$.

</details>

<details class="nb-sol">
<summary>Solution</summary>

$1 + 2 + 0.5 + 0.1 + 2 = 5.6$ ms; $\eta = 1/5.6 = 0.1786$; throughput $4000/5.6\text{ ms} \approx 714.3$ kbps.

</details>

</div>

## 14.5 Medium access and LANs {#s14-5}

<div class="nb nb-problem nb-block" id="problem-14-22">

<strong>Problem 14.22</strong> (ALOHA in frames per second)

Stations share a $250$ kbps channel with $250$-bit frames. (i) Under pure ALOHA the stations together attempt $500$ frames per second. How many get through? (ii) Under slotted ALOHA they attempt $1000$ per second. How many get through?

<details class="nb-hint">
<summary>Hint</summary>

First find the frame time and $G$, the attempts per frame time.

</details>

<details class="nb-sol">
<summary>Solution</summary>

$T = 1$ ms. (i) $G = 0.5$, $S = 0.5e^{-1} = 0.1839$ per frame time, about $184$ frames/s, the pure-ALOHA maximum. (ii) $G = 1$, $S = e^{-1} = 0.3679$: about $368$ frames/s, the slotted maximum.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-14-23">

<strong>Problem 14.23</strong> (Minimum frame, maximum span)

(i) A $1$ Gbps CSMA/CD network spans $100$ m with $v = 2\times10^8$ m/s. What is the minimum frame length? (ii) A $100$ Mbps CSMA/CD network uses $512$-bit minimum frames. What is the largest span the formula allows?

<details class="nb-hint">
<summary>Hint</summary>

$L_{\min} = 2dR/v$.

</details>

<details class="nb-sol">
<summary>Solution</summary>

(i) $2 \times 100 \times 10^9 / (2\times10^8) = 1000$ bits ($125$ bytes). (ii) $d = Lv/(2R) = 512$ m.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-14-24">

<strong>Problem 14.24</strong> 🌶 (Who goes first after a collision)

Stations A and B collide for the first time and run binary exponential backoff. What is the probability that A transmits before B on the next attempt, and that they collide again? What are the same probabilities if they had just collided for the second time?

<details class="nb-hint">
<summary>Hint</summary>

After the $n$-th collision each picks $K$ uniformly from $0..2^n-1$; enumerate the pairs.

</details>

<details class="nb-sol">
<summary>Solution</summary>

After the first collision $K \in \{0,1\}$: A first with probability $1/4$ (A picks $0$, B picks $1$), collision again $1/2$. After the second, $K \in \{0..3\}$: A first $6/16 = 3/8$, collision $4/16 = 1/4$. The repeated-collision probability halves each time.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-14-25">

<strong>Problem 14.25</strong> (Count the domains)

A switch SW connects hosts h1, h2, a hub (hosts h3–h5), a bridge, and a router. The bridge’s other port leads to a second hub with hosts h6–h9. The router’s other interface leads to switch SW2 with hosts h10–h12. How many collision domains and broadcast domains are there?

<details class="nb-hint">
<summary>Hint</summary>

Every cable is a segment; hubs merge segments; switches and bridges separate collision domains; routers separate broadcast domains.

</details>

<details class="nb-sol">
<summary>Solution</summary>

$10$ collision domains (SW–h1, SW–h2, the first hub with its cables, SW–bridge, the second hub with its cables, SW–router, router–SW2, and SW2’s three host links) and $2$ broadcast domains (one per router interface). `prob_mac.py` counts the same.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-14-26">

<strong>Problem 14.26</strong> (The purpose of ARP)

Which statements about ARP are true? (More than one may be.)

1. ARP finds the MAC address that belongs to an IPv4 address on the local network.
2. An ARP request is sent to the broadcast MAC address and the reply is unicast.
3. To reach a host on another network, a host sends an ARP request for that remote host’s IP address, and the routers forward it.
4. A gratuitous ARP can reveal that two hosts are using the same IP address.
5. ARP replies are authenticated, so ARP spoofing requires breaking a key.

<details class="nb-hint">
<summary>Hint</summary>

ARP requests are link-layer broadcasts. What do routers do with those?

</details>

<details class="nb-sol">
<summary>Solution</summary>

(a), (b), (d). For a remote destination the host ARPs for its default gateway’s address; routers do not forward ARP (c is false). ARP has no authentication at all, which is exactly why spoofing is easy (e is false).

</details>

</div>

## 14.6 IPv4 addressing {#s14-6}

<div class="nb nb-problem nb-block" id="problem-14-27">

<strong>Problem 14.27</strong> (Pick the mask)

The network `172.24.0.0/16` must be divided into at least $100$ subnets with at least $300$ hosts on each. Which subnet mask should be used?

<details class="nb-hint">
<summary>Hint</summary>

$2^s \ge 100$ and $2^h - 2 \ge 300$; is there room for both?

</details>

<details class="nb-sol">
<summary>Solution</summary>

$s = 7$ ($128$ subnets), $h = 9$ ($510$ hosts), $16 + 7 + 9 = 32$: exactly one answer, `/23` $=$ `255.255.254.0`. (`/22` gives only $64$ subnets; `/24` only $254$ hosts.)

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-14-28">

<strong>Problem 14.28</strong> (Valid host with borrowed bits)

The network `190.100.0.0` (class B) is subnetted using $11$ bits of the host part. Which of these is a valid host address: `190.100.7.32`, `190.100.7.63`, `190.100.7.95`, `190.100.7.130`, `190.100.8.0`?

<details class="nb-hint">
<summary>Hint</summary>

$/16 + 11 = /27$, blocks of $32$ in the last octet.

</details>

<details class="nb-sol">
<summary>Solution</summary>

Only `190.100.7.130` ($130 = 128 + 2$, inside `190.100.7.128/27`). `.32` and `8.0` are subnet addresses (multiples of $32$); `.63` and `.95` are broadcasts ($32+31$, $64+31$).

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-14-29">

<strong>Problem 14.29</strong> 🌶🌶 (Which route?)

A router’s table holds these routes:

| Prefix | Next hop | Prefix | Next hop |
|:--|:--|:--|:--|
| `10.30.1.0/28` | connected, Gi0/0 | `10.30.5.0/24` | `10.30.1.18` |
| `10.30.1.16/28` | connected, Gi0/1 | `10.30.5.64/26` | `10.30.1.19` |
| `10.30.0.0/16` | `10.30.1.2` | `0.0.0.0/0` | `10.30.1.1` |
| `10.30.4.0/22` | `10.30.1.3` |  |  |

Where does it send packets for `10.30.5.100`, `10.30.5.20`, `10.30.6.7`, `10.30.1.20`, `10.30.9.9` and `10.31.0.1`?

<details class="nb-hint">
<summary>Hint</summary>

List every matching prefix for each destination; the longest wins.

</details>

<details class="nb-sol">
<summary>Solution</summary>

`10.30.5.100` $\to$ `/26` via `10.30.1.19` ($100 \in [64,128)$); `10.30.5.20` $\to$ `/24` via `10.30.1.18`; `10.30.6.7` $\to$ `10.30.4.0/22` via `10.30.1.3` ($6 \in [4,8)$); `10.30.1.20` $\to$ connected Gi0/1 ($20 \in [16,32)$); `10.30.9.9` $\to$ `/16` via `10.30.1.2`; `10.31.0.1` $\to$ default via `10.30.1.1`.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-14-30">

<strong>Problem 14.30</strong> (Test the stack)

A developer wants to check that the TCP/IP stack on her own machine works, without involving the network card. Which address should she ping? (a) `0.0.0.0` (b) `255.255.255.255` (c) `127.0.0.1` (d) her default gateway.

<details class="nb-hint">
<summary>Hint</summary>

Which block never leaves the host?

</details>

<details class="nb-sol">
<summary>Solution</summary>

(c). Any address in `127.0.0.0/8` is looped back inside the host. Pinging the gateway tests the NIC, the cable and the gateway too; `255.255.255.255` is the limited broadcast; `0.0.0.0` is not a valid destination.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-14-31">

<strong>Problem 14.31</strong> (Read a block)

For the interface `10.45.130.77/19`, give the mask, the network address, the broadcast address and the number of usable hosts.

<details class="nb-hint">
<summary>Hint</summary>

Interesting octet: the third, block size $32$.

</details>

<details class="nb-sol">
<summary>Solution</summary>

Mask `255.255.224.0`; $130$ lies in $[128, 160)$, so the network is `10.45.128.0` and the broadcast `10.45.159.255`; $2^{13} - 2 = 8190$ hosts.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-14-32">

<strong>Problem 14.32</strong> 🌶 (VLSM in a /24)

Allocate subnets from `192.168.40.0/24` for LANs of $100$, $50$ and $20$ hosts and two point-to-point links, using the smallest possible block for each and allocating largest first. What is left over?

<details class="nb-hint">
<summary>Hint</summary>

Block sizes $128$, $64$, $32$, $4$, $4$.

</details>

<details class="nb-sol">
<summary>Solution</summary>

$100 \to$ `.0/25`, $50 \to$ `.128/26`, $20 \to$ `.192/27`, links `.224/30` and `.228/30`. Left over: `.232/29` and `.240/28` ($24$ addresses).

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-14-33">

<strong>Problem 14.33</strong> (Aggregation and counting)

Which statements are true? (More than one may be.)

1. `130.12.32.0/24` to `130.12.35.0/24` aggregate to `130.12.32.0/22`.
2. `130.12.33.0/24` to `130.12.36.0/24` aggregate to a single `/22`.
3. A class C network with mask `255.255.255.240` gives $16$ subnets of $14$ hosts.
4. `172.32.10.10` is a private address.
5. `169.254.3.4` is an address a host gives itself when DHCP fails.

<details class="nb-hint">
<summary>Hint</summary>

An aggregate of four /24s must start at a multiple of $4$ in the third octet.

</details>

<details class="nb-sol">
<summary>Solution</summary>

(a), (c), (e). Run (b) is not aligned: it collapses to `.33/24`, `.34/23`, `.36/24`. The private block `172.16.0.0/12` ends at `172.31.255.255`, so (d) is false.

</details>

</div>

## 14.7 IP, ICMP, NAT and IPv6 {#s14-7}

<div class="nb nb-problem nb-block" id="problem-14-34">

<strong>Problem 14.34</strong> (Fragment it)

A host sends a $5000$-byte IPv4 datagram ($20$-byte header) across a link with MTU $1420$. List the fragments with total length, offset field and MF flag. Which data bytes does the last fragment carry?

<details class="nb-hint">
<summary>Hint</summary>

$1420 - 20 = 1400$ is already a multiple of $8$.

</details>

<details class="nb-sol">
<summary>Solution</summary>

$4980$ data bytes: three fragments of $1420$ ($1400$ data) at offsets $0$, $175$, $350$ with MF $=1$, and a last one of $800$ bytes ($780$ data) at offset $525$ with MF $=0$. It carries data bytes $4200$ to $4979$.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-14-35">

<strong>Problem 14.35</strong> 🌶 (Fragments with options)

A $2400$-byte datagram has a $24$-byte header (options included) and meets an MTU of $900$. Assume every fragment carries the full $24$-byte header. Give the fragments.

<details class="nb-hint">
<summary>Hint</summary>

$900 - 24 = 876$ is not a multiple of $8$.

</details>

<details class="nb-sol">
<summary>Solution</summary>

Data per fragment $\lfloor 876/8 \rfloor \times 8 = 872$. Fragments: $896$ bytes (data $872$, offset $0$, MF $1$); $896$ ($872$, offset $109$, MF $1$); $656$ ($632$, offset $218$, MF $0$). (In reality only options marked “copy” are repeated in every fragment.)

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-14-36">

<strong>Problem 14.36</strong> (Read the header)

An IPv4 header has HLEN $= 6$ and total length `0x0200`. How long are the header, the options and the data?

<details class="nb-hint">
<summary>Hint</summary>

HLEN counts $4$-byte words.

</details>

<details class="nb-sol">
<summary>Solution</summary>

Header $24$ bytes, so $4$ bytes of options; total $512$ bytes, data $488$.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-14-37">

<strong>Problem 14.37</strong> (ICMP and friends)

Which statements are true? (More than one may be.)

1. Traceroute relies on routers returning ICMP Time Exceeded when TTL reaches $0$.
2. A router that cannot forward a packet because DF is set and the MTU is too small sends ICMP Destination Unreachable.
3. An ICMP error is sent back when a packet carrying an ICMP error is dropped.
4. IPv4 routers reassemble fragments before forwarding them onto a larger-MTU link.
5. Ping uses ICMP echo request and echo reply.

<details class="nb-hint">
<summary>Hint</summary>

Think about storms of errors about errors, and about where reassembly happens.

</details>

<details class="nb-sol">
<summary>Solution</summary>

(a), (b), (e). (b) is type $3$ code $4$, the basis of path MTU discovery. No ICMP error is ever generated about an ICMP error (c is false), and only the destination reassembles (d is false).

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-14-38">

<strong>Problem 14.38</strong> (NAT and DHCP)

Which statements are true? (More than one may be.)

1. With PAT, two inside hosts that both use source port $5000$ can talk to the same server at the same time.
2. A host behind NAT can accept an incoming connection without any configuration on the NAT.
3. The DHCP DISCOVER message is sent from `0.0.0.0` to `255.255.255.255`.
4. DHCP runs directly on IP, without a transport protocol.
5. A DHCP relay agent is needed when the server is on a different subnet.

<details class="nb-hint">
<summary>Hint</summary>

What does a PAT box key its table on? What is DHCP’s transport?

</details>

<details class="nb-sol">
<summary>Solution</summary>

(a), (c), (e). PAT gives the two flows different public ports (a). Unsolicited inbound traffic matches no mapping and is dropped unless a port is forwarded (b is false). DHCP runs over UDP, ports $67$ and $68$ (d is false).

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-14-39">

<strong>Problem 14.39</strong> (Compress IPv6 addresses)

Write in shortest form:

1. `2001:0db8:0000:0000:0008:0800:200c:417a`
2. `ff02:0000:0000:0000:0000:0000:0000:0001`
3. `2001:0db8:0000:0001:0000:0000:0000:0001`

<details class="nb-hint">
<summary>Hint</summary>

Drop leading zeros in each group; replace the longest run of zero groups by `::`, once.

</details>

<details class="nb-sol">
<summary>Solution</summary>

`2001:db8::8:800:200c:417a`, `ff02::1` and `2001:db8:0:1::1` (the single zero group after `db8` stays; the longer run of three is compressed).

</details>

</div>

## 14.8 Routing {#s14-8}

<div class="nb nb-problem nb-block" id="problem-14-40">

<strong>Problem 14.40</strong> (One Bellman–Ford update)

Router X has neighbours A, B, C at link costs $3$, $1$, $4$. It receives these distance vectors (to destinations A, B, C, D, E): from A $(0,2,5,4,9)$, from B $(2,0,6,7,3)$, from C $(5,6,0,1,2)$. Compute X’s new vector and next hops. (Break ties in favour of the alphabetically first neighbour.)

<details class="nb-hint">
<summary>Hint</summary>

For each destination take $\min_v c(X,v) + D_v(y)$.

</details>

<details class="nb-sol">
<summary>Solution</summary>

To A: $\min(3, 1+2, 4+5) = 3$ (via A; via B ties). To B: $1$ via B. To C: $4$ via C (via B costs $7$). To D: $\min(7, 8, 5) = 5$ via C. To E: $\min(12, 4, 6) = 4$ via B.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-14-41">

<strong>Problem 14.41</strong> (Dijkstra by hand)

Links: S–A $4$, S–B $1$, B–A $2$, A–C $1$, B–C $5$, C–D $3$, B–D $8$, A–D $6$. Run Dijkstra from S: in what order are nodes finished, and what is S’s forwarding table?

<details class="nb-hint">
<summary>Hint</summary>

Always finish the closest unfinished node, then relax its edges.

</details>

<details class="nb-sol">
<summary>Solution</summary>

Order S(0), B(1), A(3), C(4), D(7). Every destination’s path starts S–B: A via S–B–A ($3$), C via S–B–A–C ($4$), D via S–B–A–C–D ($7$, cheaper than S–B–D at $9$). So the forwarding table sends everything to next hop B.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-14-42">

<strong>Problem 14.42</strong> (Routing statements)

Which statements are true? (More than one may be.)

1. Poison reverse prevents count to infinity in every topology.
2. In link-state routing every router computes routes from the same complete map.
3. RIP treats a metric of $16$ as unreachable.
4. OSPF messages are carried in UDP datagrams.
5. BGP prevents loops by rejecting routes whose AS path already contains its own AS.
6. A router must run a routing protocol in order to forward packets.

<details class="nb-hint">
<summary>Hint</summary>

Loops of three routers; protocol number $89$; static routes.

</details>

<details class="nb-sol">
<summary>Solution</summary>

(b), (c), (e). Poison reverse only cures two-router loops (a is false). OSPF runs directly over IP as protocol $89$ (d is false). Static routes and a default route are enough to forward (f is false).

</details>

</div>

## 14.9 Transport: TCP and UDP {#s14-9}

<div class="nb nb-problem nb-block" id="problem-14-43">

<strong>Problem 14.43</strong> (Window after a timeout)

A TCP Tahoe sender starts with cwnd $=1$ MSS and ssthresh $=32$ MSS. Every window is acknowledged in one RTT, except that a timeout occurs in round $12$. What is cwnd in rounds $7$, $12$, $13$, $17$, $18$ and $19$? (Use the per-round model of [Section 9.4](../09-transport/#sec-cn-congestion).)

<details class="nb-hint">
<summary>Hint</summary>

$1, 2, 4, \dots$ up to $32$, then $+1$ per round. On the timeout ssthresh becomes half of the window in use.

</details>

<details class="nb-sol">
<summary>Solution</summary>

Rounds $1$–$6$: $1, 2, 4, 8, 16, 32$; then $33$ in round $7$, …, $38$ in round $12$. Timeout: ssthresh $= 19$, cwnd $= 1$ in round $13$; then $2, 4, 8, 16$ (round $17$), $19$ (round $18$, capped at ssthresh, not $32$), $20$ (round $19$).

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-14-44">

<strong>Problem 14.44</strong> 🌶🌶 (Reno with both kinds of loss)

A Reno sender starts with cwnd $=1$, ssthresh $=16$. Three duplicate ACKs arrive in round $8$ and a timeout occurs in round $14$. Give cwnd for rounds $5$ to $20$.

<details class="nb-hint">
<summary>Hint</summary>

Three duplicate ACKs: ssthresh $=$ cwnd$/2$ and Reno continues from ssthresh in congestion avoidance. Timeout: back to $1$.

</details>

<details class="nb-sol">
<summary>Solution</summary>

Rounds $5$–$8$: $16, 17, 18, 19$. Loss at $19$: ssthresh $9$, so $9, 10, 11, 12, 13, 14$ in rounds $9$–$14$. Timeout at $14$: ssthresh $7$; rounds $15$–$20$: $1, 2, 4, 7, 8, 9$ (round $18$ stops at $7$).

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-14-45">

<strong>Problem 14.45</strong> (Sequence numbers)

A client with ISN $1000$ completes the handshake and sends segments of $500$, $700$ and $300$ bytes, then closes. Give each segment’s sequence number, the server’s cumulative ACK after all three, the sequence number of the client’s FIN and the ACK that acknowledges it.

<details class="nb-hint">
<summary>Hint</summary>

The SYN uses number $1000$.

</details>

<details class="nb-sol">
<summary>Solution</summary>

Segments at $1001$, $1501$, $2201$. Cumulative ACK $2501$. The FIN carries seq $2501$ and is acknowledged with ack $2502$.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-14-46">

<strong>Problem 14.46</strong> (One RTO update)

SRTT is $200$ ms and RTTVAR $50$ ms when a new RTT sample of $280$ ms arrives. Compute the new RTTVAR, SRTT and RTO with the RFC 6298 constants (ignore the $1$ s floor).

<details class="nb-hint">
<summary>Hint</summary>

Update RTTVAR first, with the old SRTT.

</details>

<details class="nb-sol">
<summary>Solution</summary>

RTTVAR $= 0.75 \cdot 50 + 0.25 \cdot |200 - 280| = 57.5$ ms; SRTT $= 0.875 \cdot 200 + 0.125 \cdot 280 = 210$ ms; RTO $= 210 + 4 \cdot 57.5 = 440$ ms.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-14-47">

<strong>Problem 14.47</strong> (Window and wrap-around)

(i) What is the maximum throughput of a TCP connection with a $65{,}535$-byte window and a $20$ ms RTT? (ii) At $2.5$ Gbps, how long until the sequence numbers wrap, and why does it matter?

<details class="nb-hint">
<summary>Hint</summary>

$W/\mathrm{RTT}$; $2^{32}$ bytes.

</details>

<details class="nb-sol">
<summary>Solution</summary>

(i) $65535 \times 8 / 0.02 \approx 26.2$ Mbps. (ii) $2^{32} \times 8 / 2.5\times10^9 \approx 13.7$ s, far less than an MSL of $120$ s: an old duplicate could be mistaken for new data, so timestamps (PAWS) are needed.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-14-48">

<strong>Problem 14.48</strong> (Token bucket burst)

A token bucket of $1$ MB is filled at $10$ Mbps ($1.25$ MB/s) and feeds a $100$ Mbps line. Starting full, for how long can the host send at the full line rate?

<details class="nb-hint">
<summary>Hint</summary>

$S = B/(M-R)$ with everything in bytes per second.

</details>

<details class="nb-sol">
<summary>Solution</summary>

$S = 10^6 / (12.5\times10^6 - 1.25\times10^6) \approx 88.9$ ms, during which about $1.11$ MB leave (the bucket plus the tokens that arrived meanwhile).

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-14-49">

<strong>Problem 14.49</strong> 🌶 (TCP statements)

Which statements are true? (More than one may be.)

1. The side that sends the first FIN ends up in TIME\_WAIT.
2. A pure ACK segment consumes one sequence number.
3. `accept()` sends the SYN+ACK.
4. Fast retransmit is triggered by three duplicate ACKs, before the timer expires.
5. UDP preserves message boundaries; TCP does not.
6. SYN cookies let a server keep no state for half-open connections.

<details class="nb-hint">
<summary>Hint</summary>

Who completes the handshake for a listening socket?

</details>

<details class="nb-sol">
<summary>Solution</summary>

(a), (d), (e), (f). Only SYN and FIN (and data) consume sequence numbers (b is false). The kernel completes handshakes for a listening socket on its own; `accept()` only dequeues a finished connection (c is false).

</details>

</div>

## 14.10 Application layer {#s14-10}

<div class="nb nb-problem nb-block" id="problem-14-50">

<strong>Problem 14.50</strong> 🌶 (Page load time)

A browser must resolve a name (three DNS round trips of $3$, $20$ and $26$ ms, nothing cached) and then fetch a base HTML page that references $8$ small objects on the same server; the RTT to the server is $40$ ms and transmission times are negligible. How long does the page take with (i) non-persistent HTTP, one connection at a time; (ii) non-persistent HTTP with $4$ parallel connections; (iii) persistent HTTP without pipelining; (iv) persistent HTTP with pipelining?

<details class="nb-hint">
<summary>Hint</summary>

Each non-persistent object costs $2$ RTTs; persistence pays the handshake once.

</details>

<details class="nb-sol">
<summary>Solution</summary>

DNS costs $49$ ms in every case. (i) $49 + 18 \times 40 = 769$ ms. (ii) base page $2$ RTTs, then two rounds of $4$ objects at $2$ RTTs each: $49 + 6 \times 40 = 289$ ms. (iii) handshake $+$ base page $+ 8$ requests: $49 + 10 \times 40 = 449$ ms. (iv) handshake, base page, all $8$ objects in one RTT: $49 + 3 \times 40 = 169$ ms.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-14-51">

<strong>Problem 14.51</strong> (DNS statements)

Which statements are true? (More than one may be.)

1. A host’s resolver library usually sends a recursive query to its configured resolver.
2. Root servers answer queries for `www.example.com` with the final address.
3. A CNAME record maps a name to another name.
4. DNS uses only UDP.
5. Lowering a record’s TTL before changing it shortens the time stale answers survive in caches.
6. The mail servers for a domain are found through its MX records.

<details class="nb-hint">
<summary>Hint</summary>

What does a root server know?

</details>

<details class="nb-sol">
<summary>Solution</summary>

(a), (c), (e), (f). Root servers only refer the resolver to the TLD servers (b is false). DNS uses TCP for large responses and zone transfers (d is false).

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-14-52">

<strong>Problem 14.52</strong> (HTTP semantics)

Which statements are true? (More than one may be.)

1. PUT is idempotent; POST is not.
2. A `304 Not Modified` response carries the full body again.
3. `401` means the client is not authenticated; `403` that it is but is not allowed.
4. HTTP/2 removes head-of-line blocking completely, including at the TCP level.
5. A `502` from a load balancer means the upstream returned an invalid response.
6. HTTP/1.1 requires a `Host` header.

<details class="nb-hint">
<summary>Hint</summary>

Where does HTTP/2 still block?

</details>

<details class="nb-sol">
<summary>Solution</summary>

(a), (c), (e), (f). A 304 has no body: the client reuses its cached copy (b is false). HTTP/2 multiplexes streams but a lost TCP segment still stalls all of them; only QUIC (HTTP/3) removes that (d is false).

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-14-53">

<strong>Problem 14.53</strong> (Sessions, tokens and FTP)

Which statements are true? (More than one may be.)

1. The payload of a signed JWT is readable by anyone who holds the token.
2. Revoking a server-side session is immediate; revoking a JWT before it expires needs extra state such as a deny-list.
3. An `HttpOnly` cookie cannot be read by page JavaScript.
4. In active-mode FTP the client opens the data connection to the server.
5. IMAP keeps mail on the server so that several devices see the same folders.

<details class="nb-hint">
<summary>Hint</summary>

Signed is not encrypted. In active mode, who calls whom for data?

</details>

<details class="nb-sol">
<summary>Solution</summary>

(a), (b), (c), (e). In active mode the <em>server</em> connects back to the client (from port $20$); passive mode is the one where the client opens the data connection (d is false).

</details>

</div>

## 14.11 Security {#s14-11}

<div class="nb nb-problem nb-block" id="problem-14-54">

<strong>Problem 14.54</strong> (RSA by hand)

With $p = 43$, $q = 59$ and $e = 13$, find $n$, $\varphi(n)$ and the private exponent $d$. Encrypt $m = 88$.

<details class="nb-hint">
<summary>Hint</summary>

$d$ is the inverse of $e$ modulo $\varphi(n)$: extended Euclid.

</details>

<details class="nb-sol">
<summary>Solution</summary>

$n = 2537$, $\varphi(n) = 42 \times 58 = 2436$, $d = 937$ ($13 \times 937 = 12181 = 5 \times 2436 + 1$). $c = 88^{13} \bmod 2537 = 1226$, and $1226^{937} \bmod 2537 = 88$ (`prob_sec.py`).

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-14-55">

<strong>Problem 14.55</strong> (Diffie–Hellman by hand)

With $p = 29$, $g = 2$, Alice picks $a = 9$ and Bob $b = 13$. What do they send, and what key do they agree on? Is $2$ a generator modulo $29$?

<details class="nb-hint">
<summary>Hint</summary>

Square-and-multiply modulo $29$.

</details>

<details class="nb-sol">
<summary>Solution</summary>

$A = 2^9 \bmod 29 = 19$, $B = 2^{13} \bmod 29 = 14$; key $14^9 \bmod 29 = 19^{13} \bmod 29 = 3$. The order of $2$ modulo $29$ is $28$, so $2$ generates the whole group.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-14-56">

<strong>Problem 14.56</strong> 🌶 (Security statements)

Which statements are true? (More than one may be.)

1. For $100$ users to talk pairwise with symmetric keys, $4950$ keys are needed.
2. A digital signature is made with the signer’s public key.
3. Plain Diffie–Hellman is safe against a man in the middle.
4. TLS 1.3 always provides forward secrecy.
5. A CRC protects a message against deliberate tampering.
6. HTTPS hides the URL path from an eavesdropper on the network.
7. Parameterised queries prevent SQL injection.

<details class="nb-hint">
<summary>Hint</summary>

$\binom{100}{2}$; which key only the signer has; what authenticates DH values?

</details>

<details class="nb-sol">
<summary>Solution</summary>

(a), (d), (f), (g). Signatures use the private key (b is false). Unauthenticated DH is exactly what a MITM defeats (c is false). An attacker recomputes a CRC (e is false). HTTPS encrypts the request line and headers, so the path is hidden; the server’s address (and usually its name) is not.

</details>

</div>

## 14.12 Wireless and the set pieces {#s14-12}

<div class="nb nb-problem nb-block" id="problem-14-57">

<strong>Problem 14.57</strong> (Wireless statements)

Which statements are true? (More than one may be.)

1. 802.11 uses CSMA/CD because collisions are easy to detect on radio.
2. In the hidden-terminal problem, two senders that cannot hear each other collide at a common receiver.
3. RTS/CTS helps because stations near the receiver hear the CTS and stay silent.
4. 802.11 acknowledges unicast frames at the link layer.
5. The exposed-terminal problem causes collisions.

<details class="nb-hint">
<summary>Hint</summary>

Can a radio listen while it transmits?

</details>

<details class="nb-sol">
<summary>Solution</summary>

(b), (c), (d). Wi-Fi uses CSMA/CA, because a transmitting radio cannot detect a collision (a is false). An exposed terminal defers needlessly: it wastes capacity but causes no collision (e is false).

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-14-58">

<strong>Problem 14.58</strong> (Round trips to the first byte)

A browser needs $60$ ms to resolve a name (nothing cached) and has a $40$ ms RTT to the server. Ignoring transmission and server time, when does the first byte of the HTML arrive with TCP + TLS 1.2, with TCP + TLS 1.3, and with QUIC (HTTP/3) to a new server?

<details class="nb-hint">
<summary>Hint</summary>

Count the round trips of each handshake, then one for the request.

</details>

<details class="nb-sol">
<summary>Solution</summary>

TCP $1$ + TLS 1.2 $2$ + HTTP $1$: $60 + 4 \times 40 = 220$ ms. With TLS 1.3: $60 + 3 \times 40 = 180$ ms. QUIC combines transport and TLS in one RTT: $60 + 2 \times 40 = 140$ ms.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-14-59">

<strong>Problem 14.59</strong> 🌶 (What does the URL walk use?)

Which of the following happen when a laptop with an empty ARP cache and an empty DNS cache opens `https://www.example.com` for the first time? (More than one may be.)

1. An ARP request for the IP address of `www.example.com`.
2. An ARP request for the default gateway’s IP address.
3. A DNS query over UDP to the configured resolver.
4. A TCP handshake to port $80$ before the one to port $443$.
5. A TLS handshake in which the server presents a certificate for `www.example.com`.
6. ICMP Time Exceeded messages from every router on the path.

<details class="nb-hint">
<summary>Hint</summary>

The server is not on the laptop’s subnet. Which port does an `https` URL imply?

</details>

<details class="nb-sol">
<summary>Solution</summary>

(b), (c), (e). A remote destination is reached through the gateway, so the laptop ARPs for the gateway (a is false). An `https` URL goes straight to port $443$ (d is false, unless the user typed a plain `http` URL and was redirected). Time Exceeded is what traceroute provokes, not normal traffic (f is false).

</details>

</div>
