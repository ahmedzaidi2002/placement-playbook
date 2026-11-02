---
title: "Routing"
weight: 3
---

1 question asked by Cisco. Try each one first, then open the toggle: it gives the answer, why it is right, and the idea behind it explained from scratch.

### 1 · Q17, which route does Router1 use for Host A

*Asked by: Cisco (OA, Sep 2025)*

Refer to the exhibit. Host A (10.10.13.214) sits behind Switch1 on Router1's
10.10.10.0/28 interface. Router1's routing table holds connected routes 10.10.10.0/28,
10.10.11.0/30 and 10.10.12.0/30; OSPF routes 10.10.13.0/25, 10.10.13.128/28,
10.10.13.144/28, 10.10.13.160/29 and 10.10.13.208/29, all via 10.10.10.1; BGP routes to
209.165.200.224/27, 209.165.201.0/27 and 209.165.202.128/27; and a default route via
10.10.11.2. Which prefix does Router1 use for traffic to Host A?

- **(a)** 10.10.10.0/28
- **(b)** 10.10.13.0/25
- **(c)** 10.10.13.144/28
- **(d)** 10.10.13.208/29

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) 10.10.13.208/29**

**Why.** A router uses the longest (most specific) prefix that contains the destination. 10.10.13.208/29 covers .208–.215, which includes .214. 10.10.13.0/25 covers only .0–.127 and 10.10.13.144/28 covers .144–.159, so neither contains .214. The default route is only for when nothing matches.

**Concept: longest-prefix match.** Each route is an address range. Among all ranges containing the destination, the smallest (largest prefix length) wins. A /29 is a block of 8 addresses, a /28 of 16, a /25 of 128.

{{< /details >}}
