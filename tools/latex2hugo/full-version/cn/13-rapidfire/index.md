---
title: "13 · Interview rapid-fire"
linkTitle: "13 Interview rapid-fire"
weight: 13
math: true
---
Short answers to the questions that come up again and again, in the tone of a candidate answering out loud. Each points back to the section that explains it.

## 13.1 Layers and the physical layer {#s13-1}

1. <strong>Name the OSI layers and a protocol at each.</strong><br>Physical (Ethernet PHY, 802.11 radio), data link (Ethernet MAC, PPP), network (IP, ICMP), transport (TCP, UDP), session, presentation (TLS sits awkwardly across these), application (HTTP, DNS) ([Section 1.1](../01-layering/#sec-cn-layers)).
2. <strong>Which layer uses frames? Packets? Segments?</strong><br>Frames: data link. Packets (datagrams): network. Segments: transport (UDP calls its unit a datagram).
3. <strong>Why layering?</strong><br>Each layer can change independently behind a fixed service interface; the cost is header overhead and information hiding (TCP cannot tell congestion loss from radio loss).
4. <strong>Transmission vs propagation delay?</strong><br>$L/R$ depends on packet size and link rate; $d/v$ on distance. A bigger packet does not travel slower; it takes longer to push out ([Section 1.3](../01-layering/#sec-cn-delay)).
5. <strong>What is the bandwidth–delay product?</strong><br>$R \times \mathrm{RTT}$: the data in flight needed to keep the pipe full; a window smaller than it caps throughput at $W/\mathrm{RTT}$.
6. <strong>What happens if one node fails in a ring?</strong><br>In a simple ring the loop is broken and the whole ring stops; a dual counter-rotating ring (FDDI) wraps around the failure ([Section 1.2](../01-layering/#sec-cn-topology)).
7. <strong>Star vs mesh?</strong><br>Star: $n$ links, the centre is a single point of failure. Full mesh: $n(n-1)/2$ links, no single point of failure.
8. <strong>Nyquist vs Shannon?</strong><br>Nyquist: $2B\log_2 L$ for a noiseless channel. Shannon: $B\log_2(1+S/N)$ for a noisy one, regardless of levels ([Section 2.1](../02-physical/#sec-cn-capacity)).
9. <strong>Baud vs bit rate?</strong><br>Baud is symbols per second; bit rate $=$ baud $\times \log_2 M$.
10. <strong>Why Manchester encoding?</strong><br>A transition in every bit gives clock recovery and no DC, at twice the signal rate.
11. <strong>Circuit vs packet switching?</strong><br>Circuits reserve capacity end to end (guaranteed, wasteful when idle); packets share links on demand (efficient for bursty traffic, variable delay).

## 13.2 Data link layer and LANs {#s13-2}

12. <strong>Why does bit stuffing exist?</strong><br>So that the flag `01111110` never appears inside data: insert a `0` after five `1`s ([Section 3.1](../03-errors/#sec-cn-framing)).
13. <strong>Parity vs checksum vs CRC?</strong><br>Parity catches odd numbers of flipped bits; the Internet checksum is a cheap one’s-complement sum, blind to reordering; a CRC is polynomial division that catches all bursts up to its degree ([Section 3.3](../03-errors/#sec-cn-crc)).
14. <strong>Can a CRC correct errors?</strong><br>No, it only detects them. Hamming codes correct (one bit per codeword).
15. <strong>How many errors does a code with minimum distance $d$ handle?</strong><br>Detects $d-1$, corrects $\lfloor (d-1)/2 \rfloor$.
16. <strong>Stop-and-wait efficiency?</strong><br>$1/(1+2a)$ with $a = T_p/T_t$ ([Section 4.1](../04-arq/#sec-cn-sw)).
17. <strong>Go-Back-N vs Selective Repeat?</strong><br>GBN: receiver window $1$, cumulative ACKs, resend everything after a loss, $W \le 2^k-1$. SR: buffer out-of-order frames, resend only losses, $W \le 2^{k-1}$ ([Section 4.2](../04-arq/#sec-cn-gbn)).
18. <strong>Why must the SR window be at most half the sequence space?</strong><br>Otherwise, when all ACKs are lost, retransmitted old frames fall inside the receiver’s new window and are accepted as new data.
19. <strong>Maximum throughput of pure and slotted ALOHA?</strong><br>$1/(2e) \approx 18.4\%$ and $1/e \approx 36.8\%$ ([Section 5.1](../05-mac-lan/#sec-cn-aloha)).
20. <strong>Why does Ethernet have a minimum frame size?</strong><br>So that a sender is still transmitting when a collision from the far end can reach it: $L_{\min} = 2dR/v$ ([Section 5.2](../05-mac-lan/#sec-cn-csma)).
21. <strong>Why can’t Wi-Fi use CSMA/CD?</strong><br>A transmitting radio cannot hear collisions, and the collision may happen at a receiver it cannot hear; so CSMA/CA with ACKs and optional RTS/CTS ([Section 12.1](../12-wireless-setpieces/#sec-cn-wifi)).
22. <strong>Hub vs switch vs router?</strong><br>Layer 1 repeater (one collision domain), layer 2 learning bridge (separate collision domains, one broadcast domain), layer 3 forwarder (separate broadcast domains) ([Section 5.3](../05-mac-lan/#sec-cn-ethernet)).
23. <strong>How does a switch learn?</strong><br>From source MAC addresses of arriving frames; it floods unknown destinations and broadcasts, filters frames whose destination is on the incoming port.
24. <strong>Why VLANs?</strong><br>Several isolated broadcast domains on one set of switches; trunks carry an 802.1Q tag with a 12-bit VLAN ID.
25. <strong>Why STP?</strong><br>Redundant switch links create loops and broadcast storms (no TTL in Ethernet); STP elects a root by lowest bridge ID and blocks ports to leave a tree ([Section 5.4](../05-mac-lan/#sec-cn-stp)).
26. <strong>What is ARP for?</strong><br>Finding the MAC address of an IPv4 address on the local link: broadcast request, unicast reply, cached ([Section 5.5](../05-mac-lan/#sec-cn-arp)).
27. <strong>Gratuitous ARP?</strong><br>An ARP for your own address: detects duplicates and updates caches after failover.
28. <strong>Size limits of an Ethernet frame?</strong><br>64 to 1518 bytes (1522 with a VLAN tag), payload 46 to 1500.

## 13.3 IP, addressing and routing {#s13-3}

29. <strong>Which address tests your own TCP/IP stack?</strong><br>Loopback, `127.0.0.1` (any of `127/8`); it never leaves the host ([Section 6.3](../06-addressing/#sec-cn-vlsm)).
30. <strong>Private address ranges?</strong><br>`10/8`, `172.16/12`, `192.168/16` (RFC 1918). `169.254/16` is link-local, not private.
31. <strong>Usable hosts in a /26?</strong><br>$2^6 - 2 = 62$: network and broadcast addresses excluded.
32. <strong>How do you choose a mask for $N$ subnets of $H$ hosts?</strong><br>Smallest $s$ with $2^s \ge N$, smallest $h$ with $2^h - 2 \ge H$, require prefix $+ s + h \le 32$ ([Section 6.2](../06-addressing/#sec-cn-choosemask)).
33. <strong>What is CIDR and why was it introduced?</strong><br>Prefixes of any length instead of classes A/B/C: less waste and aggregatable routes.
34. <strong>What is longest-prefix match?</strong><br>Among routes containing the destination, use the most specific one; `0.0.0.0/0` is the fallback ([Section 6.4](../06-addressing/#sec-cn-lpm)).
35. <strong>What is VLSM?</strong><br>Different prefix lengths inside one block, allocated largest first on aligned boundaries.
36. <strong>What does TTL do?</strong><br>Limits a packet’s hop count so routing loops cannot keep it alive; at $0$ the router drops it and sends ICMP Time Exceeded.
37. <strong>Where are fragments reassembled?</strong><br>Only at the destination. Offsets are in 8-byte units; MF is $0$ only on the last fragment ([Section 7.2](../07-ip/#sec-cn-frag)).
38. <strong>What is path MTU discovery?</strong><br>Send with DF set; routers that would fragment return ICMP “fragmentation needed” with their MTU; the sender shrinks its packets.
39. <strong>How does ping work?</strong><br>ICMP Echo Request (type 8) and Echo Reply (type 0) ([Section 7.3](../07-ip/#sec-cn-icmp)).
40. <strong>How does traceroute work?</strong><br>Probes with TTL $1, 2, 3, \dots$; each router on the path answers Time Exceeded; the destination answers Port Unreachable.
41. <strong>What does DHCP do, and how?</strong><br>Leases an address, mask, gateway and DNS servers: Discover, Offer, Request, Ack over UDP 67/68; relay agents cross routers ([Section 7.4](../07-ip/#sec-cn-dhcp)).
42. <strong>ARP vs RARP vs DHCP?</strong><br>ARP: IP to MAC. RARP: own MAC to own IP (obsolete). DHCP: full configuration over UDP.
43. <strong>What is NAT and what does it break?</strong><br>Rewrites private addresses and ports to a public one; breaks unsolicited inbound connections, protocols carrying addresses in their payload, and adds per-flow state.
44. <strong>IPv4 vs IPv6 header?</strong><br>IPv6: fixed 40 bytes, 128-bit addresses, no checksum, no router fragmentation, extension headers, flow label ([Section 7.5](../07-ip/#sec-cn-ipv6)).
45. <strong>Does IPv6 have broadcast or ARP?</strong><br>Neither: multicast and Neighbor Discovery replace them.
46. <strong>Routing vs forwarding?</strong><br>Routing computes the table (control plane, seconds); forwarding looks up each packet (data plane, nanoseconds) ([Chapter 8](../08-routing/)).
47. <strong>Distance vector vs link state?</strong><br>DV: tell neighbours about everyone, Bellman–Ford, slow convergence, count to infinity. LS: flood your links to everyone, Dijkstra, fast convergence.
48. <strong>What is count to infinity, and the fixes?</strong><br>After a failure, routers keep learning the dead route from each other, raising its cost step by step; split horizon and poison reverse fix two-router loops only ([Section 8.1](../08-routing/#sec-cn-dv)).
49. <strong>RIP, OSPF, BGP in one line each?</strong><br>RIP: distance vector, hop count up to 15, UDP 520. OSPF: link state, areas, IP protocol 89. BGP: path vector between ASes, policy-driven, TCP 179 ([Section 8.3](../08-routing/#sec-cn-protocols)).
50. <strong>How does BGP avoid loops?</strong><br>It carries the AS path and rejects routes containing its own AS.

## 13.4 Transport {#s13-4}

51. <strong>TCP vs UDP?</strong><br>Connection, reliability, ordering, flow and congestion control, byte stream (TCP) against bare datagrams with ports and a checksum (UDP) ([Section 9.6](../09-transport/#sec-cn-sockets)).
52. <strong>When would you choose UDP?</strong><br>When late data is useless or the application does its own reliability: DNS, VoIP, video calls, games, QUIC.
53. <strong>Why a three-way handshake?</strong><br>Both ISNs must be sent and acknowledged, and a stale SYN must not open a connection ([Section 9.2](../09-transport/#sec-cn-tcp-header)).
54. <strong>Why is the ISN random?</strong><br>To avoid confusion with old connections on the same 4-tuple and to stop off-path attackers from injecting segments.
55. <strong>Why TIME\_WAIT, and who enters it?</strong><br>The side that closes first waits $2\,$MSL to re-ACK a lost final FIN and to let old segments die.
56. <strong>Too many TIME\_WAIT sockets on a client: fixes?</strong><br>Connection reuse and pooling, a wider ephemeral range, `tcp_tw_reuse`.
57. <strong>What is a half-close?</strong><br>One side has sent FIN but still receives (CLOSE\_WAIT on the other side until it closes).
58. <strong>What do SYN and FIN cost in sequence space?</strong><br>One number each; pure ACKs cost none.
59. <strong>Flow control vs congestion control?</strong><br>rwnd protects the receiver; cwnd protects the network; the sender uses $\min(\text{rwnd}, \text{cwnd})$ ([Section 9.4](../09-transport/#sec-cn-congestion)).
60. <strong>Explain slow start.</strong><br>cwnd starts small and doubles every RTT until ssthresh or a loss.
61. <strong>What is AIMD?</strong><br>Additive increase (1 MSS per RTT), multiplicative decrease (halve on loss): converges to fairness.
62. <strong>Tahoe vs Reno?</strong><br>Both halve ssthresh on loss; on three duplicate ACKs Tahoe restarts at cwnd $=1$, Reno continues from ssthresh (fast recovery); on timeout both go to $1$.
63. <strong>Why three duplicate ACKs, not one?</strong><br>Reordering produces one or two duplicates; three is strong evidence of loss.
64. <strong>How is RTO computed?</strong><br>RFC 6298: SRTT and RTTVAR by EWMA ($1/8$, $1/4$), RTO $=$ SRTT $+ 4\,$RTTVAR, minimum $1$ s, doubling on timeout; Karn: no samples from retransmissions.
65. <strong>What is Nagle’s algorithm, and when do you disable it?</strong><br>Coalesce small writes while data is unacknowledged; disable (`TCP_NODELAY`) for latency-sensitive traffic, especially with delayed ACKs.
66. <strong>What is silly window syndrome?</strong><br>Tiny window updates causing tiny segments; fixed by advertising only sizeable windows and not sending tiny segments.
67. <strong>What happens when rwnd is 0?</strong><br>The sender stops and sends periodic zero-window probes (persist timer) until the window opens.
68. <strong>What is a SYN flood, and SYN cookies?</strong><br>Spoofed SYNs fill the half-open queue; SYN cookies encode the connection state in the server’s ISN so nothing is stored.
69. <strong>What is QUIC?</strong><br>A UDP-based, encrypted transport with streams, 1-RTT (0-RTT) setup and connection migration; HTTP/3 runs on it ([Section 9.5](../09-transport/#sec-cn-quic)).
70. <strong>`accept()` vs `listen()`?</strong><br>`listen` makes the socket passive and the kernel completes handshakes into a queue; `accept` dequeues one and returns a new descriptor.
71. <strong>select vs poll vs epoll?</strong><br>select: bitsets, $O(n)$, a 1024-descriptor limit; poll: an array, $O(n)$; epoll: register once, $O(\text{ready})$, edge or level triggered.
72. <strong>Is TCP message-oriented?</strong><br>No, a byte stream: one `write` may arrive in several `read`s and vice versa; frame your messages.

## 13.5 Application layer and security {#s13-5}

73. <strong>Recursive vs iterative DNS?</strong><br>Recursive: the server returns the final answer. Iterative: it may return a referral. Hosts ask resolvers recursively; resolvers walk the tree iteratively ([Section 10.1](../10-application/#sec-cn-dns)).
74. <strong>A vs CNAME vs MX?</strong><br>Address; alias to another name; mail servers for the domain.
75. <strong>Does DNS use TCP?</strong><br>Yes, for large responses and zone transfers; UDP 53 otherwise.
76. <strong>What is in `/etc/hosts`?</strong><br>Static name-to-address mappings consulted before DNS on most systems.
77. <strong>HTTP/1.1 vs HTTP/2 vs HTTP/3?</strong><br>Persistent connections; binary multiplexed streams over one TCP connection; the same over QUIC without transport head-of-line blocking ([Section 10.2](../10-application/#sec-cn-http)).
78. <strong>Which methods are idempotent?</strong><br>GET, HEAD, OPTIONS, PUT, DELETE; POST and PATCH are not.
79. <strong>401 vs 403? 502 vs 504?</strong><br>Not authenticated vs not allowed. Upstream sent a bad response vs upstream timed out.
80. <strong>What does 304 mean?</strong><br>Not Modified: the client’s cached copy is still valid (conditional GET with `If-Modified-Since` or `If-None-Match`).
81. <strong>Cookies vs sessions vs JWT?</strong><br>A cookie is client storage sent back automatically; a session is server-side state found by an ID; a JWT is signed client-held state, easy to scale, hard to revoke ([Section 10.3](../10-application/#sec-cn-state)).
82. <strong>L4 vs L7 load balancer?</strong><br>L4 forwards connections by IP and port; L7 terminates HTTP and routes requests by host, path, headers or cookies.
83. <strong>Forward proxy vs reverse proxy?</strong><br>Acts for clients vs acts for servers.
84. <strong>What is a CDN?</strong><br>Geographically distributed caches reached via DNS or anycast, cutting RTT and origin load.
85. <strong>WebSocket vs long polling?</strong><br>WebSocket upgrades one connection to full duplex; long polling holds a request open until there is news and then reconnects ([Section 10.4](../10-application/#sec-cn-apis)).
86. <strong>Active vs passive FTP?</strong><br>Active: the server connects back to the client for data. Passive: the client opens the data connection, which works through NATs.
87. <strong>SMTP vs IMAP vs POP3?</strong><br>SMTP pushes mail between servers; IMAP and POP3 let users pull it, IMAP keeping it synchronised on the server ([Section 10.5](../10-application/#sec-cn-mail)).
88. <strong>Symmetric vs asymmetric encryption?</strong><br>One shared key, fast; key pairs, slow but solve key distribution and give signatures. TLS uses both ([Section 11.1](../11-security/#sec-cn-crypto)).
89. <strong>What does a certificate prove?</strong><br>That a CA vouches that this public key belongs to this name; the client checks the chain, dates and name ([Section 11.2](../11-security/#sec-cn-tls)).
90. <strong>What happens in a TLS 1.3 handshake?</strong><br>Client sends a DH key share; server answers with its share, certificate, a signature over the transcript and Finished; one RTT.
91. <strong>What is forward secrecy?</strong><br>Session keys from ephemeral DH, so a stolen long-term key cannot decrypt past recorded traffic.
92. <strong>Hash vs MAC vs signature?</strong><br>Unkeyed fingerprint; keyed integrity between key holders; private-key proof anyone can verify.
93. <strong>How does ARP spoofing work, and the defence?</strong><br>Forged ARP replies redirect a victim’s traffic to the attacker; dynamic ARP inspection, static gateway entries, TLS ([Section 11.3](../11-security/#sec-cn-attacks)).
94. <strong>XSS vs CSRF?</strong><br>XSS runs attacker script in the trusted site; CSRF makes the browser send a cookie-authenticated request to it. Escaping/CSP vs SameSite cookies and tokens.
95. <strong>How do you prevent SQL injection?</strong><br>Parameterised queries, never string concatenation.
