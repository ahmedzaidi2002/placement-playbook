---
title: "8 · Routing"
linkTitle: "8 Routing"
weight: 8
math: true
---
**Forwarding** = moving a packet from an input port to the right output port using the table (fast, per packet). **Routing** = building that table (slow, by protocols).

## 8.1 Distance vector (Bellman–Ford) {#cn-8-1}

Each router knows only its neighbours and the cost to them. Periodically it sends its whole **distance vector** (its best known cost to every destination) to its neighbours, and updates:

$$D_x(y) = \min_{v \in \text{neighbours}} \big( c(x, v) + D_v(y) \big).$$

<div class="nb nb-example">

<strong>Example</strong> (One update)

Router A has neighbours B (link cost 2) and C (cost 5). B reports cost 3 to D; C reports cost 1 to D. A's cost to D $= \min(2 + 3,\ 5 + 1) = $ **5, via B**.

</div>

**Count-to-infinity problem:** good news spreads fast, bad news slowly. If the link to D fails, B may believe C still reaches D (through B itself), and they keep increasing each other's cost by small steps. Fixes: **split horizon** (do not advertise a route back to the neighbour you learned it from), **poison reverse** (advertise it back as infinity), **hold-down timers**, and a small "infinity" (RIP uses **16**).

## 8.2 Link state (Dijkstra) {#cn-8-2}

Every router **floods** the state of its own links to all routers, so each one has the **complete map** and runs **Dijkstra's shortest-path algorithm** itself. Converges faster, no count-to-infinity, but needs more memory and CPU. OSPF and IS-IS are link-state protocols.

| | Distance vector | Link state |
|---|---|---|
| Knows | neighbours' distance vectors | the whole topology |
| Sends | its table, to neighbours | its links, to everyone (flooding) |
| Algorithm | Bellman–Ford | Dijkstra |
| Convergence | slow; count-to-infinity | fast |
| Examples | RIP | OSPF, IS-IS |

## 8.3 Internet routing: RIP, OSPF, BGP {#cn-8-3}

The Internet is a network of **autonomous systems** (AS, one organisation's network each).

- **Intra-domain** (inside an AS, IGP):
  - **RIP:** distance vector, metric = **hop count**, max 15 (16 = unreachable), updates every 30 s, over **UDP 520**. Small networks.
  - **OSPF:** link state, cost based on bandwidth, splits a large network into **areas** with a backbone area 0; runs directly over IP (protocol 89). Large enterprise networks.
- **Inter-domain** (between ASes):
  - **BGP:** a **path-vector** protocol: advertisements carry the full AS path (which also prevents loops). Routes are chosen by **policy** (business relationships), not just shortest path. Runs over **TCP 179**. It is the protocol that glues the Internet together.

## 8.4 Multicast {#cn-8-4}

One sender, a group of receivers (class D addresses, 224–239). Hosts join groups with **IGMP**; routers build distribution trees so each packet crosses each link at most once.

<div class="nb nb-moral">

Distance vector: tell your neighbours what you know (Bellman–Ford; count-to-infinity, RIP). Link state: tell everyone about your links, then run Dijkstra (OSPF). BGP is path-vector routing by policy between autonomous systems.

</div>
