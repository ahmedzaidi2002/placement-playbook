---
title: "5 · Medium access, Ethernet and switches"
linkTitle: "5 MAC and LANs"
weight: 5
math: true
---
When many stations share one channel, the **medium access control (MAC)** protocol decides who sends.

## 5.1 ALOHA {#cn-5-1}

- **Pure ALOHA:** send whenever you have a frame; on collision, wait a random time and resend. Vulnerable period = **2 frame times**.
- **Slotted ALOHA:** send only at the start of a time slot. Vulnerable period = **1 frame time**.

With $G$ = average frames attempted per frame time:

| | Throughput $S$ | Maximum |
|---|---|---|
| Pure ALOHA | $S = G e^{-2G}$ | $1/(2e) \approx$ **18.4%** at $G = 0.5$ |
| Slotted ALOHA | $S = G e^{-G}$ | $1/e \approx$ **36.8%** at $G = 1$ |

<div class="nb nb-example">

<strong>Example</strong> (ALOHA)

200-bit frames on a 200 kbps channel (frame time 1 ms); stations together attempt 1000 frames/s, so $G = 1$. Pure: $S = e^{-2} = 0.135$ → **135** frames/s succeed. Slotted: $S = e^{-1} = 0.368$ → **368** frames/s.

</div>

## 5.2 CSMA and CSMA/CD {#cn-5-2}

**CSMA:** listen before sending; send only if the channel is idle. Collisions still happen because of propagation delay (two stations both see "idle"). Variants: 1-persistent, non-persistent, p-persistent.

**CSMA/CD** (classic wired Ethernet): keep listening while sending; on a collision, stop, send a jam signal, and wait a random back-off (**binary exponential back-off**: after the $n$-th collision pick a wait of $0$ to $2^n - 1$ slot times, $n$ capped at 10, give up after 16 attempts).

<div class="nb nb-theorem nb-block">

<strong>Minimum frame size for CSMA/CD</strong>

A sender must still be transmitting when news of a collision returns from the far end (after $2T_p$), so

$$T_t \ge 2T_p \quad\Longrightarrow\quad L_{\min} = 2 \times T_p \times R.$$

</div>

<div class="nb nb-example">

<strong>Example</strong> (Minimum frame)

10 Mbps, 2500 m cable, $v = 2 \times 10^8$ m/s: $T_p = 12.5\ \mu$s, so $L_{\min} = 2 \times 12.5 \times 10^{-6} \times 10^7 = $ **250 bits**. Real Ethernet uses **512 bits (64 bytes)** to allow for repeaters. At 100 Mbps with the same frame size, the maximum cable length shrinks 10×.

</div>

**CSMA/CA** (Wi-Fi): wireless stations cannot detect collisions while sending, so they **avoid** them: wait, back off randomly before sending, and use ACKs; optionally RTS/CTS (chapter 11).

**Taking turns:** polling (a master asks each station) and **token passing** (a token circulates; only the holder sends). No collisions, but overhead and a single point of failure.

## 5.3 Ethernet and MAC addresses {#cn-5-3}

- **MAC address:** 48 bits (6 bytes), written `3C:22:FB:12:AB:01`; burned into the network card; first 3 bytes identify the vendor. `FF:FF:FF:FF:FF:FF` is broadcast.
- **Ethernet frame:** preamble, destination MAC, source MAC, type (e.g. IPv4), data (**46–1500 bytes**, so the MTU is 1500), CRC-32.

## 5.4 Hubs, switches, routers {#cn-5-4}

| Device | Layer | Collision domains | Broadcast domains |
|---|---|---|---|
| Hub / repeater | 1 | one for all ports | one |
| Switch / bridge | 2 | **one per port** | one (per VLAN) |
| Router | 3 | one per port | **one per port** |

**How a switch learns:** for every incoming frame it records "source MAC → this port" in its **MAC table**. To forward: if the destination is known, send only on that port; if unknown (or broadcast), **flood** to all other ports.

**VLANs** split one physical switch into several logical LANs (separate broadcast domains); traffic between VLANs needs a router. Trunk links carry several VLANs using 802.1Q tags.

**Spanning Tree Protocol (STP):** redundant switch links create loops where broadcast frames circulate forever (broadcast storms). STP elects a root bridge and blocks some ports so that the active links form a **tree** with no loops; blocked links take over if an active one fails.

## 5.5 ARP {#cn-5-5}

To send to an IP address on the local network, a host needs the target's MAC address. **ARP:** broadcast "who has 192.168.1.20?"; the owner replies (unicast) with its MAC; the answer is cached in the **ARP table**. To reach a host on another network, the sender ARPs for its **default gateway's** MAC, not the remote host's. (**RARP** did the reverse; replaced by DHCP.)

<div class="nb nb-moral">

Pure ALOHA peaks at 18.4%, slotted at 36.8%. CSMA/CD needs frames of at least $2 T_p R$ bits. Switches split collision domains, routers split broadcast domains. ARP turns an IP address into a MAC address on the local link.

</div>
