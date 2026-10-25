---
title: "12 · Interview rapid-fire"
linkTitle: "12 Rapid-fire"
weight: 12
math: true
---
## 12.1 Layers and links {#cn-12-1}

1. **OSI layers in order?** Physical, data link, network, transport, session, presentation, application.
2. **TCP/IP vs OSI?** TCP/IP has 4 layers (link, internet, transport, application); OSI's top three are merged into application.
3. **Hub vs switch vs router?** Layer 1 repeats to all ports; layer 2 forwards by MAC; layer 3 forwards by IP between networks.
4. **Collision domain vs broadcast domain?** Switches split collision domains; routers split broadcast domains.
5. **Transmission vs propagation delay?** Size / rate vs distance / speed.
6. **Bandwidth–delay product?** Bits in flight on a link; the window needed to keep it busy.
7. **Nyquist vs Shannon?** Max rate without noise ($2B \log_2 L$) vs with noise ($B \log_2(1 + S/N)$).
8. **Why CRC over checksum?** CRC catches all burst errors up to its length and more patterns; checksums are cheaper but weaker.
9. **Stop-and-wait problem?** Efficiency $1/(1 + 2a)$: the link idles while waiting for ACKs.
10. **Go-Back-N vs Selective Repeat?** GBN resends everything after a loss, receiver window 1; SR resends only the lost frame, buffers out-of-order frames.
11. **Max window with $k$-bit sequence numbers?** GBN $2^k - 1$, SR $2^{k-1}$.
12. **CSMA/CD vs CSMA/CA?** Detect collisions and back off (wired) vs avoid them with back-off and RTS/CTS (wireless).
13. **Why a minimum Ethernet frame size?** So the sender is still transmitting when a collision from the far end returns: 64 bytes.
14. **What does ARP do?** Finds the MAC address for an IP address on the local network.
15. **What is a VLAN?** A logical LAN (separate broadcast domain) on shared switches.
16. **Why spanning tree?** To remove loops between switches, which cause broadcast storms.

## 12.2 Network layer {#cn-12-2}

17. **Private IP ranges?** 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16.
18. **Hosts in a /26?** $2^6 - 2 = 62$.
19. **What is CIDR?** Classless addressing with an explicit prefix length; allows flexible block sizes and route aggregation.
20. **Longest-prefix match?** The router uses the most specific matching route.
21. **What is NAT?** Mapping many private addresses to one public address using ports.
22. **DHCP steps?** Discover, Offer, Request, Acknowledge.
23. **What is TTL?** A hop counter that drops looping packets.
24. **How does traceroute work?** Increasing TTLs; each router that drops the packet replies with ICMP "time exceeded".
25. **IPv4 vs IPv6?** 32 vs 128 bits; IPv6 has a fixed header, no router fragmentation, no broadcast.
26. **Distance vector vs link state?** Neighbours' tables + Bellman–Ford (RIP) vs full map + Dijkstra (OSPF).
27. **Count-to-infinity fix?** Split horizon, poison reverse, hold-down, small infinity (RIP's 16).
28. **What is BGP?** Path-vector routing between autonomous systems, chosen by policy.

## 12.3 Transport and application {#cn-12-3}

29. **TCP vs UDP?** Reliable ordered connected byte stream with flow and congestion control vs fast connectionless datagrams.
30. **Three-way handshake?** SYN, SYN-ACK, ACK: both sides agree on starting sequence numbers.
31. **Why TIME_WAIT?** To resend a lost final ACK and let old duplicate segments expire.
32. **Flow control vs congestion control?** Protect the receiver (rwnd) vs protect the network (cwnd).
33. **Slow start?** cwnd doubles each RTT up to ssthresh; then grows by 1 MSS per RTT.
34. **Timeout vs 3 duplicate ACKs?** Timeout: cwnd to 1. Duplicate ACKs: halve cwnd (fast recovery).
35. **What does DNS use, and why UDP?** UDP port 53: one small query and reply, no handshake needed.
36. **DNS record types?** A, AAAA, CNAME, MX, NS, PTR.
37. **HTTP/1.1 vs 2 vs 3?** Persistent connections vs multiplexed binary streams vs over QUIC (UDP).
38. **GET vs POST?** Read, idempotent, parameters in the URL vs submit/create, data in the body, not idempotent.
39. **401 vs 403?** Not authenticated vs authenticated but not allowed.
40. **Cookie vs session vs JWT?** Client-stored data / server-stored data keyed by a cookie ID / a signed self-contained token.
41. **Symmetric vs asymmetric encryption?** One shared key, fast vs public/private key pair, slow; used together in TLS.
42. **What does TLS give?** Confidentiality, integrity and server authentication (certificates).
43. **What happens when you type a URL?** DNS → TCP handshake → TLS handshake → HTTP request → response → render.

<div class="nb nb-moral">

Forty-three answers under twenty seconds each cover the theory part of most networking interviews; chapter 13 has the numericals.

</div>
