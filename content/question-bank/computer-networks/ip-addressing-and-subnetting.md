---
title: "IP addressing and subnetting"
weight: 1
---

3 questions asked by DevRev, MAQ Software, MathWorks. Try each one first, then open the toggle: it gives the answer, why it is right, and the idea behind it explained from scratch.

### 1 · Q5, testing the IP stack on localhost

*Asked by: DevRev (HackerEarth OA)*

Bob wants to test the IP stack on his localhost. Which IP address should he ping?

- **(a)** 127.0.0.0
- **(b)** 1.0.0.127
- **(c)** 127.0.0.1
- **(d)** 127.0.0.255

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) 127.0.0.1**

**Why.** 127.0.0.1 is the standard loopback address: packets sent to it never leave the machine, so pinging it tests the host's own TCP/IP stack.

**Concept: loopback.** The whole 127.0.0.0/8 block is reserved for loopback; 127.0.0.1 ("localhost") is the conventional one.

{{< /details >}}

### 2 · Q28, subnet mask for 70 subnets of 480 hosts

*Asked by: MAQ Software (TalentDecrypt test, 2025)*

Which subnet mask should you use for the network 172.29.0.0 to get 70 subnets with 480 hosts
per subnet?

- **(a)** 255.255.224.0
- **(b)** 255.254.0.0
- **(c)** 255.255.255.0
- **(d)** 255.255.254.0

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) 255.255.254.0** (/23)

**Why.** 172.29.0.0 is a class B network (/16), leaving 16 bits. 70 subnets need 7 subnet bits (2⁷ = 128 ≥ 70). That leaves 9 host bits: 2⁹ − 2 = 510 hosts ≥ 480. Mask: 16 + 7 = 23 ones = 255.255.254.0.

**Concept: subnetting.** Borrow s bits from the host part for 2ˢ subnets; the remaining h bits give 2ʰ − 2 usable hosts (network and broadcast addresses are reserved). Pick s so both counts are enough.

{{< /details >}}

### 3 · Q11, subnetting

*Asked by: MathWorks (IIIT Delhi 2024)*

Which is a valid host address given the network ID 191.254.0.0 while using 11 bits [for
subnetting]? [cut off in the source]

- **(a)** 191.254.0.32
- **(b)** 191.254.0.96
- **(c)** 191.254.1.29
- **(d)** 191.54.1.64

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) 191.254.1.29**

**Why.** /16 + 11 subnet bits = /27, so subnets are blocks of 32 addresses. 191.254.0.32 and 191.254.0.96 are block starts (subnet addresses, not hosts). 191.254.1.29 lies in the block 191.254.1.0–1.31 and is not its first or last address, so it is a valid host. (d) is a different network.

**Concept: network, broadcast and host addresses.** In each block, the first address is the subnet ID and the last is the broadcast; everything in between can be a host. Block size = 2^(32 − prefix).

{{< /details >}}
