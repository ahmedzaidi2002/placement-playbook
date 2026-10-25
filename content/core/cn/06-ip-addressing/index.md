---
title: "6 · IPv4 addressing and subnetting"
linkTitle: "6 IP addressing"
weight: 6
math: true
---
## 6.1 IPv4 addresses and classes {#cn-6-1}

An IPv4 address is 32 bits, written as four bytes: `192.168.1.10`. It has a **network part** and a **host part**.

| Class | First byte | Default mask | Networks / hosts |
|---|---|---|---|
| A | 1–126 | /8 (255.0.0.0) | $2^{24} - 2$ hosts per network |
| B | 128–191 | /16 (255.255.0.0) | $2^{16} - 2$ hosts |
| C | 192–223 | /24 (255.255.255.0) | 254 hosts |
| D | 224–239 | — | multicast |
| E | 240–255 | — | reserved |

(127.x.x.x is loopback, so class A uses 1–126.)

**Special and private addresses:**

- **Private** (not routed on the Internet, used behind NAT): `10.0.0.0/8`, `172.16.0.0/12` (172.16–172.31), `192.168.0.0/16`.
- **Loopback:** `127.0.0.1`. **APIPA** (no DHCP server found): `169.254.0.0/16`. `0.0.0.0` = "this host"; `255.255.255.255` = limited broadcast.
- In every subnet, the **all-0s host part** is the network address and the **all-1s host part** is the broadcast address; neither can be given to a host. Hence **usable hosts $= 2^h - 2$** for $h$ host bits.

## 6.2 CIDR and masks {#cn-6-2}

**CIDR** writes the network length explicitly: `/n` means the first $n$ bits are the network. Mask for /26 = 26 ones = `255.255.255.192`.

| Prefix | Mask (last byte) | Block size | Usable hosts |
|---|---|---|---|
| /24 | 0 | 256 | 254 |
| /25 | 128 | 128 | 126 |
| /26 | 192 | 64 | 62 |
| /27 | 224 | 32 | 30 |
| /28 | 240 | 16 | 14 |
| /29 | 248 | 8 | 6 |
| /30 | 252 | 4 | 2 (point-to-point links) |

**Network address** = IP AND mask. **Broadcast** = network address with all host bits set to 1.

<div class="nb nb-example">

<strong>Example</strong> (Analyse an address)

`172.16.45.200/20`. Mask = 255.255.**240**.0 (the third byte has 4 network bits). Third byte: $45 \text{ AND } 240 = 32$ (block size 16, and 45 lies in 32–47). Network **172.16.32.0**, broadcast **172.16.47.255**, usable hosts 172.16.32.1 – 172.16.47.254, count $2^{12} - 2 = $ **4094**.

</div>

## 6.3 Subnetting {#cn-6-3}

Borrow $s$ host bits to make $2^s$ subnets, each with $2^{h} - 2$ hosts ($h$ = remaining host bits).

<div class="nb nb-example">

<strong>Example</strong> (Split a /24 into 4 subnets)

`192.168.10.0/24` into 4 → borrow 2 bits → **/26**, block size 64, **62 hosts** each.

| Subnet | Network | Usable hosts | Broadcast |
|---|---|---|---|
| 1 | 192.168.10.0 | .1 – .62 | .63 |
| 2 | 192.168.10.64 | .65 – .126 | .127 |
| 3 | 192.168.10.128 | .129 – .190 | .191 |
| 4 | 192.168.10.192 | .193 – .254 | .255 |

</div>

<div class="nb nb-example">

<strong>Example</strong> (Choose a mask for a host count)

Need subnets with at least 50 hosts each: $2^h - 2 \ge 50$ → $h = 6$ (62 hosts) → mask **/26**. Need 500 hosts: $h = 9$ (510) → **/23**.

</div>

**Is it a valid host?** `192.168.10.127/26` is the broadcast of the second subnet → not assignable. `192.168.10.65/26` → valid.

## 6.4 VLSM and supernetting {#cn-6-4}

- **VLSM** (variable-length subnet masks): give each subnet only the size it needs. Allocate the **largest first**. From 192.168.1.0/24 for LANs of 100, 50 and 20 hosts plus a router link: /25 (126) at .0, /26 (62) at .128, /27 (30) at .192, /30 at .224.
- **Supernetting / route aggregation:** combine contiguous networks into one shorter prefix. `200.1.0.0/24` … `200.1.3.0/24` (four /24s) = **`200.1.0.0/22`**. Requires the block to be aligned (start on a multiple of its size).

## 6.5 Longest-prefix match {#cn-6-5}

A router forwards each packet using the **most specific** (longest) matching prefix in its table.

<div class="nb nb-example">

<strong>Example</strong> (Forwarding)

Table: `10.0.0.0/8 → A`, `10.1.0.0/16 → B`, `10.1.2.0/24 → C`, `0.0.0.0/0 → D` (default).

- 10.1.2.5 → matches /8, /16, /24 → **C**
- 10.1.3.5 → matches /8, /16 → **B**
- 10.2.0.1 → matches /8 → **A**
- 11.0.0.1 → only the default → **D**

</div>

<div class="nb nb-moral">

Usable hosts = $2^h - 2$. Network = IP AND mask; broadcast = all host bits 1. Block size in the interesting byte = 256 − mask byte. Routers pick the longest matching prefix.

</div>
