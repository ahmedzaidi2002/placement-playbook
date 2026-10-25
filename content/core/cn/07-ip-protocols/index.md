---
title: "7 · IP, fragmentation, ICMP, DHCP, NAT, IPv6"
linkTitle: "7 IP and helpers"
weight: 7
math: true
---
## 7.1 The IPv4 header {#cn-7-1}

20 bytes without options (up to 60). Key fields: **version** (4), **header length** (in 4-byte words), **total length**, **identification / flags / fragment offset** (for fragmentation), **TTL** (time to live: decremented at every router; at 0 the packet is dropped and an ICMP message is sent; stops endless loops), **protocol** (6 = TCP, 17 = UDP, 1 = ICMP), **header checksum** (recomputed at every hop because TTL changes), source and destination addresses.

IP is **best-effort**: no guarantee of delivery, order or no duplicates. TCP adds those.

## 7.2 Fragmentation {#cn-7-2}

If a packet is larger than the next link's **MTU** (1500 bytes on Ethernet), a router splits it. Each fragment gets its own IP header and the same identification. The **fragment offset** is in units of **8 bytes**, so every fragment's data (except the last) must be a multiple of 8. The **MF** (more fragments) flag is 1 on all but the last. Reassembly happens only at the destination. The **DF** (don't fragment) flag forbids it (the router drops the packet and sends ICMP "fragmentation needed").

<div class="nb nb-example">

<strong>Example</strong> (Fragmenting)

A 4000-byte datagram (20-byte header + 3980 data) meets an MTU of 1500. Each fragment can carry $1500 - 20 = 1480$ data bytes (a multiple of 8).

| Fragment | Data bytes | Offset (÷8) | MF |
|---|---|---|---|
| 1 | 1480 | 0 | 1 |
| 2 | 1480 | 185 | 1 |
| 3 | 1020 | 370 | 0 |

Total length fields: 1500, 1500, 1040.

</div>

## 7.3 ICMP: ping and traceroute {#cn-7-3}

**ICMP** carries error and control messages for IP: destination unreachable, time exceeded, echo request/reply.

- **ping** sends ICMP echo requests and measures the round-trip time.
- **traceroute** sends packets with TTL = 1, 2, 3, …; each router where TTL hits 0 replies "time exceeded", revealing the path hop by hop.

## 7.4 DHCP and NAT {#cn-7-4}

**DHCP** gives a host its IP address, mask, default gateway and DNS server automatically, as a lease. Four steps, **DORA**: **D**iscover (client broadcasts), **O**ffer (server), **R**equest (client), **A**ck (server). Uses UDP ports 67 (server) and 68 (client).

**NAT** (network address translation) lets many devices with **private** addresses share one public address. The router rewrites the source address and port of outgoing packets and keeps a translation table to map replies back. Saves IPv4 addresses and hides internal hosts, but breaks end-to-end connectivity (inbound connections need port forwarding).

## 7.5 IPv6 {#cn-7-5}

- **128-bit** addresses, written in hex: `2001:0db8:0000:0000:0000:ff00:0042:8329` → shortened `2001:db8::ff00:42:8329` (drop leading zeros; one run of zero groups becomes `::`).
- Simpler **fixed 40-byte header**; no header checksum; **no fragmentation by routers** (only the sender fragments, after path-MTU discovery); options moved to extension headers.
- No broadcast (multicast instead); built-in auto-configuration (SLAAC).
- Transition: **dual stack**, **tunnelling** (IPv6 inside IPv4), translation.

<div class="nb nb-moral">

TTL stops loops; fragment offsets count 8-byte units and only the destination reassembles. DHCP is DORA; NAT maps many private addresses to one public one. IPv6: 128 bits, fixed 40-byte header, no router fragmentation.

</div>
