---
title: "Layers, protocols and topologies"
weight: 2
---

3 questions asked by MathWorks, Oracle. Try each one first, then open the toggle: it gives the answer, why it is right, and the idea behind it explained from scratch.

### 1 · Q9, frames

*Asked by: MathWorks (IIIT Delhi 2024)*

Frames are used in which OSI layers?

- **(a)** Network layer
- **(b)** Data link layer
- **(c)** Transport protocol
- **(d)** None of the above

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) data link layer**

**Why.** The data link layer (layer 2) packages data into frames with MAC addresses. The network layer uses packets, the transport layer segments.

**Concept: OSI data units.** Physical: bits. Data link: frames. Network: packets. Transport: segments (TCP) or datagrams (UDP). Upper layers: data/messages.

{{< /details >}}

### 2 · ARP

*Asked by: Oracle (HackerRank MCQ test)*

What is the purpose of ARP (Address Resolution Protocol) in computer networking?

- **(a)** To convert IP addresses to MAC addresses
- **(b)** To convert domain names to IP addresses
- **(c)** To establish a secure connection between client and server
- **(d)** To route packets between networks

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) to convert IP addresses to MAC addresses**

**Why.** To send a frame on a local network you need the receiver's MAC address. ARP broadcasts "who has this IP?" and the owner replies with its MAC. DNS does (b), TLS (c), routing protocols (d).

**Concept: ARP.** It links layer 3 (IP) to layer 2 (MAC) on the local link. Results are cached in the ARP table.

{{< /details >}}

### 3 · ring topology failure

*Asked by: Oracle (HackerRank MCQ test)*

In a ring topology network, if one device fails, how does it affect the network?

- **(a)** Only the failed device is affected
- **(b)** All devices in the network are affected
- **(c)** Only the devices between which the failed device exists are affected
- **(d)** The network continues to function normally

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) all devices are affected**

**Why.** In a simple (single, one-way) ring every message passes through every node, so one failed node breaks the loop for everyone. (Dual rings like FDDI can route around a failure, but that is not the textbook answer.)

**Concept: topologies and failure.** Bus: a cable break splits the network. Star: a node failure affects only that node (the hub is the weak point). Ring: one failure breaks the ring. Mesh: many paths, most robust.

{{< /details >}}
