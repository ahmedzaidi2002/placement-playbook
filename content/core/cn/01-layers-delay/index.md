---
title: "1 · Layers, devices and delay"
linkTitle: "1 Layers and delay"
weight: 1
math: true
---
## 1.1 Why layers {#cn-1-1}

Each layer offers a service to the layer above and uses the one below, so each can change independently (Wi-Fi replaced Ethernet without changing TCP). On the way down, each layer adds its own **header** (**encapsulation**); on the way up, each layer strips it.

| OSI layer | Job | Data unit | Protocols / examples | Device |
|---|---|---|---|---|
| 7 Application | services for the user | message | HTTP, DNS, SMTP, FTP | |
| 6 Presentation | format, encryption, compression | | TLS, JPEG | |
| 5 Session | dialogues, checkpoints | | RPC sessions | |
| 4 Transport | process-to-process, reliability | **segment** (TCP) / datagram (UDP) | TCP, UDP | |
| 3 Network | host-to-host, routing | **packet** | IP, ICMP, OSPF | **router** |
| 2 Data link | node-to-node over one link, MAC | **frame** | Ethernet, Wi-Fi, PPP, ARP | **switch**, bridge |
| 1 Physical | bits on the wire | **bit** | cables, radio | **hub**, repeater |

The **TCP/IP model** has 4 (or 5) layers: Application (OSI 5–7), Transport, Internet (network), Link (data link + physical).

<div class="nb nb-remark">

<strong>OA</strong> — Router = layer 3, switch/bridge = layer 2, hub/repeater = layer 1. A switch reads MAC addresses only; a router reads IP addresses. Gateways can work up to layer 7.

</div>

- **Connection-oriented** (TCP, phone call): set up a connection first, then reliable ordered delivery. **Connectionless** (UDP, IP, letters): each packet sent independently.

## 1.2 Topologies {#cn-1-2}

| Topology | Cables for $n$ nodes | One failure |
|---|---|---|
| Bus | 1 backbone | backbone break kills all |
| Star | $n$ (to a central hub/switch) | central device fails → all fail; one cable → only that node |
| Ring | $n$ | one break can stop the ring (unless dual ring) |
| Mesh (full) | $n(n-1)/2$ | very robust; expensive |

Full mesh of 6 nodes: $6 \times 5/2 = $ **15** links (each node needs 5 ports).

## 1.3 The four delays {#cn-1-3}

| Delay | Formula | Depends on |
|---|---|---|
| **Transmission** $T_t$ | $L/R$ (packet bits / link rate) | packet size, bandwidth |
| **Propagation** $T_p$ | $d/v$ (distance / signal speed, ≈ $2 \times 10^8$ m/s) | distance |
| **Queuing** | waiting in the router's buffer | traffic |
| **Processing** | header check, routing lookup | router speed |

<div class="nb nb-example">

<strong>Example</strong> (One packet, one link)

$L = 1500$ bytes $= 12{,}000$ bits, $R = 10$ Mbps, distance 2000 km, $v = 2 \times 10^8$ m/s. $T_t = 12000/10^7 = $ **1.2 ms**; $T_p = 2 \times 10^6 / 2 \times 10^8 = $ **10 ms**. The last bit arrives after $T_t + T_p = $ **11.2 ms**.

</div>

**Units:** link rates are decimal (1 Mbps $= 10^6$ bits/s); file sizes are often binary (1 KB $= 1024$ bytes). Read which the question means. Bytes × 8 = bits.

**Bandwidth–delay product** $= R \times T_p$: the number of bits "in flight" on the link. Above: $10^7 \times 0.01 = $ **100,000 bits**. A sender must be allowed to have about $R \times \text{RTT}$ bits unacknowledged to keep the link full.

## 1.4 Store-and-forward and packet switching {#cn-1-4}

A router receives a whole packet before forwarding it. Sending $P$ packets of $L$ bits over $N$ links of rate $R$:

$$T = (N + P - 1)\,\frac{L}{R} + N\,T_p.$$

<div class="nb nb-example">

<strong>Example</strong> (Why packets beat whole messages)

A 1 MB ($8 \times 10^6$ bits) message over 3 links of 1 Mbps, propagation ignored.
- As one message: each hop takes 8 s → $3 \times 8 = $ **24 s**.
- As 1000 packets of 8000 bits (8 ms each): $(3 + 1000 - 1) \times 8$ ms $= $ **8.016 s**: the hops work in parallel (pipelining).

</div>

**Circuit switching** (old telephone): reserve a path first; guaranteed rate, wasted when idle. **Packet switching** (Internet): share links on demand; efficient, but queuing delay and loss under congestion.

**Queuing:** with packets arriving at $a$ per second, $L$ bits each, on a link of rate $R$, the **traffic intensity** is $La/R$. Near 1, queuing delay grows sharply; above 1, the queue grows without bound and packets are dropped.

<div class="nb nb-moral">

Transmission delay = L/R (size), propagation delay = d/v (distance). Router is layer 3, switch layer 2, hub layer 1. Packet switching pipelines hops: (N + P − 1)·L/R.

</div>
