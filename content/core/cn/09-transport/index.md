---
title: "9 · Transport: UDP and TCP"
linkTitle: "9 UDP and TCP"
weight: 9
math: true
---
## 9.1 Ports and sockets {#cn-9-1}

The network layer delivers to a **host**; the transport layer delivers to a **process**, identified by a 16-bit **port** (0–1023 well-known, 1024–49151 registered, above that ephemeral). A TCP connection is identified by the 4-tuple (source IP, source port, destination IP, destination port).

## 9.2 UDP vs TCP {#cn-9-2}

| | UDP | TCP |
|---|---|---|
| Connection | none | yes (handshake) |
| Reliability, order | no | yes (ACKs, retransmission, sequence numbers) |
| Flow / congestion control | no | yes |
| Header | **8 bytes** | **20–60 bytes** |
| Unit | datagram (message boundaries kept) | byte stream (no boundaries) |
| Used by | DNS, DHCP, VoIP, video streaming, games, QUIC | HTTP/1.1 and HTTP/2, SMTP, FTP, SSH |

Choose UDP when speed and low latency matter more than every packet arriving (late voice data is useless anyway).

## 9.3 TCP connection setup and teardown {#cn-9-3}

**Three-way handshake:**

1. Client → server: **SYN**, seq = $x$.
2. Server → client: **SYN-ACK**, seq = $y$, ack = $x + 1$.
3. Client → server: **ACK**, ack = $y + 1$.

Random initial sequence numbers stop old or forged segments being accepted. Why three and not two: both sides must confirm the other's starting sequence number, and a delayed old SYN must not open a connection.

**Teardown (four-way):** FIN → ACK, then the other side's FIN → ACK (connections close each direction separately). The side that closes first waits in **TIME_WAIT** for 2 × MSL (maximum segment lifetime) so a lost final ACK can be resent and old duplicates die out.

**SYN flood attack:** an attacker sends many SYNs without completing the handshake, filling the server's half-open queue. Defence: **SYN cookies** (encode the state in the server's sequence number instead of storing it).

## 9.4 Reliability {#cn-9-4}

- **Sequence numbers count bytes**; ACKs are **cumulative** ("next byte I expect").
- **Retransmission** on timeout, or on **3 duplicate ACKs** (fast retransmit, before the timer fires).
- **Timeout** from measured RTTs: $\text{EstimatedRTT} = 0.875 \times \text{EstimatedRTT} + 0.125 \times \text{SampleRTT}$, $\text{Timeout} = \text{EstimatedRTT} + 4 \times \text{DevRTT}$. Example: estimate 100 ms, new sample 120 ms → new estimate $87.5 + 15 = $ **102.5 ms**.

## 9.5 Flow control {#cn-9-5}

The receiver advertises its free buffer space as the **receive window** (rwnd); the sender never has more unacknowledged bytes than that. Purpose: do not overwhelm the **receiver**. A window of 0 pauses the sender (it probes periodically).

**Throughput limit:** at most one window per RTT. With a 64 KB window and a 100 ms RTT: $65535 \times 8 / 0.1 \approx $ **5.2 Mbps**, however fast the link. (The window-scale option allows larger windows.)

**Small packets:** **Nagle's algorithm** holds back small segments while data is unacknowledged; **delayed ACKs** wait briefly to combine ACKs; **silly window syndrome** (tiny window updates) is avoided on both sides.

## 9.6 Congestion control {#cn-9-6}

Purpose: do not overwhelm the **network**. The sender keeps a **congestion window** (cwnd) and sends at most $\min(\text{cwnd}, \text{rwnd})$.

- **Slow start:** cwnd starts at 1 MSS and **doubles every RTT** (+1 MSS per ACK) until it reaches the threshold **ssthresh**.
- **Congestion avoidance:** above ssthresh, cwnd grows by **1 MSS per RTT** (linear).
- **On timeout** (severe): ssthresh = cwnd / 2, cwnd = 1, slow start again (TCP Tahoe and Reno).
- **On 3 duplicate ACKs** (mild): ssthresh = cwnd / 2, cwnd = ssthresh (**fast recovery**, TCP Reno), then linear growth.
- This **AIMD** behaviour (additive increase, multiplicative decrease) makes competing flows converge to a fair share.

<div class="nb nb-example">

<strong>Example</strong> (cwnd over time)

ssthresh = 16 MSS, cwnd starts at 1. Per RTT: **1, 2, 4, 8, 16** (slow start), then **17, 18, 19, 20** (congestion avoidance). A **timeout** at cwnd = 20 → ssthresh = 10, cwnd = **1** → 1, 2, 4, 8, 10, 11, … If instead **3 duplicate ACKs** arrive at cwnd = 20 (Reno) → ssthresh = 10, cwnd = **10** → 11, 12, …

</div>

Modern Linux uses **CUBIC** (window grows as a cubic function of time since the last loss); Google's **BBR** models bandwidth and RTT instead of reacting to loss.

## 9.7 Traffic shaping {#cn-9-7}

- **Leaky bucket:** output at a constant rate, whatever the input bursts; excess overflows (dropped).
- **Token bucket:** tokens arrive at rate $R$ into a bucket of capacity $B$; sending a byte uses a token. Allows **bursts** up to the bucket size. With maximum output rate $M$, a full bucket allows a burst of $S = B/(M - R)$ seconds.

<div class="nb nb-example">

<strong>Example</strong> (Token bucket burst)

Bucket $B = 1$ Mb, token rate $R = 2$ Mbps, line rate $M = 10$ Mbps: $S = 1/(10 - 2) = $ **0.125 s** at full speed, then the rate drops to 2 Mbps.

</div>

**QUIC** (used by HTTP/3): reliable, encrypted transport built on **UDP**, with a faster handshake (0–1 RTT) and no head-of-line blocking between streams.

<div class="nb nb-moral">

TCP = handshake (SYN, SYN-ACK, ACK) + byte sequence numbers + cumulative ACKs + flow control (rwnd, protects the receiver) + congestion control (cwnd: slow start doubles, then +1 per RTT, halve on loss). UDP = 8-byte header and nothing else.

</div>
