---
title: "Computer Networks"
weight: 5
math: true
sidebar:
  open: false
---

The networking topics that placement OAs and interviews ask, cut down to what matters: definitions, the idea behind each protocol, and a worked example wherever there is a numerical (delays, Nyquist/Shannon, CRC, sliding windows, ALOHA, subnetting, fragmentation, TCP congestion window).

## Contents

**Part: Bottom layers**

- [1 · Layers, devices and delay](01-layers-delay/)
- [2 · The physical layer](02-physical/)
- [3 · Framing and error control](03-error-control/)
- [4 · Flow control: stop-and-wait, Go-Back-N, Selective Repeat](04-flow-arq/)
- [5 · Medium access, Ethernet and switches](05-mac-lan/)

**Part: Network and transport**

- [6 · IPv4 addressing and subnetting](06-ip-addressing/)
- [7 · IP, fragmentation, ICMP, DHCP, NAT, IPv6](07-ip-protocols/)
- [8 · Routing](08-routing/)
- [9 · Transport: UDP and TCP](09-transport/)

**Part: Top layers**

- [10 · The application layer](10-application/)
- [11 · Security, wireless and "what happens when you type a URL"](11-security-wireless/)

**Part: Revision**

- [12 · Interview rapid-fire](12-rapidfire/)
- [13 · Practice problems](13-problems/)

<div class="nb nb-moral">

Highest-yield: subnetting and CIDR (chapter 6), TCP handshake / flow / congestion control (chapter 9), OSI layers and devices (chapter 1), sliding-window efficiency (chapter 4), and the "type a URL" walkthrough (chapter 11).

</div>

The full-length version is kept in `tools/latex2hugo/full-version/cn/` and in the PDF.
