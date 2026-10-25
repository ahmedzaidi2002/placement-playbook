---
title: "6 · IPv4 addressing"
linkTitle: "6 IPv4 addressing"
weight: 6
math: true
---
This is the chapter OAs test most in networks: pick a mask, decide whether an address is a valid host, pick the route a router uses, name the loopback address. All of it is arithmetic on 32-bit numbers, and every example below was computed with Python’s `ipaddress` module (and, where it teaches something, with the bit operations written out).

## 6.1 Addresses, classes and CIDR {#sec-cn-cidr}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> `172.16.45.200/20`: network `172.16.32.0`, broadcast `172.16.47.255`, $4094$ usable hosts.</em>

</div>

### 6.1.i An address names an interface {#s6-1-i}

An IPv4 address is $32$ bits, written as four decimal octets. It identifies a network <em>interface</em>, not a host: a router with three interfaces has three addresses, and a laptop on Wi-Fi and Ethernet has two. Every address splits into a <strong>network part</strong> (the <strong>prefix</strong>), shared by all interfaces on one link, and a <strong>host part</strong>. Routers forward on the prefix alone; that is what makes the Internet’s routing tables finite.

### 6.1.ii Classful addressing {#s6-1-ii}

Originally the split was fixed by the first bits of the address.

```text {filename="Output of classful.py"}
class lead  first octet  default mask      networks      hosts/network
  A   0       0-127      255.0.0.0             128      16777214
  B   10    128-191      255.255.0.0         16384         65534
  C   110   192-223      255.255.255.0     2097152           254
  D   1110  224-239      (multicast)
  E   1111  240-255      (reserved)
10.200.1.1   class A  classful network 10.0.0.0/8
126.0.0.1    class A  classful network 126.0.0.0/8
128.1.2.3    class B  classful network 128.1.0.0/16
191.254.7.9  class B  classful network 191.254.0.0/16
192.0.2.1    class C  classful network 192.0.2.0/24
223.1.1.1    class C  classful network 223.1.1.0/24
230.0.0.5    class D  classful network -
```

Class A has $2^7 = 128$ network numbers, of which $0$ and $127$ are reserved, so $126$ are usable. The scheme wasted addresses badly: an organisation with $2000$ hosts was too big for a class C ($254$ hosts) and got a class B ($65{,}534$), stranding $63{,}000$ addresses.

### 6.1.iii CIDR: the prefix length is written down {#s6-1-iii}

<strong>Classless inter-domain routing</strong> (CIDR, RFC 4632) drops the classes: the prefix length $n$ is given explicitly, as `a.b.c.d/n` or as a <strong>subnet mask</strong> with $n$ leading $1$ bits. The block has $2^{32-n}$ addresses.

<div class="nb nb-definition" id="fact-6-1-1">

<strong>Fact 6.1.1</strong> (The mask arithmetic). For any address $A$ in a block with mask $M$:

$$
\text{network} = A \mathbin{\&} M, \qquad \text{broadcast} = A \mathbin{|} \lnot M,
	\qquad \text{usable hosts} = 2^{32-n} - 2.
$$

The first address (host bits all $0$) names the network; the last (host bits all $1$) is the <strong>directed broadcast</strong> address of that network. Neither can be given to a host.

</div>

```text {filename="Output of cidr.py, lines 1–6"}
address      172.16.45.200   10101100.00010000.00101101.11001000
mask /20     255.255.240.0   11111111.11111111.11110000.00000000
network      172.16.32.0     address AND mask
broadcast    172.16.47.255   address OR (NOT mask)
wildcard     0.0.15.255      NOT mask
addresses    2^(32-20) = 4096; usable hosts 4094: 172.16.32.1 .. 172.16.47.254
```

<div class="nb nb-remark" id="algorithm-6-1-2">

<strong>Algorithm 6.1.2</strong> (Fast mental method: the interesting octet) — Find the octet where the mask is neither $255$ nor $0$ (here the third: $240$). The <strong>block size</strong> is $256 - 240 = 16$. Networks in that octet start at multiples of $16$: $45$ lies in $[32, 48)$, so the network is `172.16.32.0` and the broadcast is `172.16.47.255`.

</div>

### 6.1.iv Subnetting {#s6-1-iv}

<strong>Subnetting</strong> borrows bits from the host part to make several smaller networks from one block: borrowing $s$ bits gives $2^s$ subnets, each $2^{s}$ times smaller.

```text {filename="Output of cidr.py, lines 7–11"}
192.168.10.0/24 split into 4 equal subnets (2 borrowed bits -> /26):
   192.168.10.0/26    hosts 192.168.10.1   - 192.168.10.62  bcast 192.168.10.63
   192.168.10.64/26   hosts 192.168.10.65  - 192.168.10.126 bcast 192.168.10.127
   192.168.10.128/26  hosts 192.168.10.129 - 192.168.10.190 bcast 192.168.10.191
   192.168.10.192/26  hosts 192.168.10.193 - 192.168.10.254 bcast 192.168.10.255
```

<div class="nb nb-remark" id="remark-6-1-3">

<strong>Remark 6.1.3</strong> (Subnet zero and the all-ones subnet) — Very old practice (RFC 950) avoided the first and last subnet, so some textbooks subtract $2$ from the number of subnets as well as from the number of hosts. Modern equipment uses both (RFC 1878 calls the restriction obsolete). Unless a question says otherwise, $s$ borrowed bits give $2^s$ subnets; if the answer options only fit $2^s - 2$, the question is following the old rule.

</div>

```text {filename="Output of cidr.py, lines 12–15"}
special prefix lengths:
   /30: 4 addresses, hosts() gives ['10.0.0.1', '10.0.0.2']
   /31: 2 addresses, hosts() gives ['10.0.0.0', '10.0.0.1']
   /32: 1 addresses, hosts() gives ['10.0.0.5']
```

A `/30` has two usable addresses, the classic choice for a point-to-point link between routers. RFC 3021 allows `/31` on point-to-point links: no broadcast address is needed there, so both addresses are usable (Python’s `hosts()` follows that rule). A `/32` names a single address, used for loopback interfaces and host routes.

<div class="nb nb-moral">

Network $= A \,\&\, M$, broadcast $= A \mid \lnot M$, hosts $= 2^{32-n}-2$. Block size $= 256 -$ the interesting mask octet.

</div>

## 6.2 Choosing a mask, and valid host addresses {#sec-cn-choosemask}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> `172.20.0.0/16` must provide $50$ subnets of $900$ hosts: only `/22` (`255.255.252.0`) works.</em>

</div>

### 6.2.i $N$ subnets of $H$ hosts {#s6-2-i}

<div class="nb nb-remark" id="algorithm-6-2-1">

<strong>Algorithm 6.2.1</strong> (Choosing a subnet mask) — Borrow the smallest $s$ with $2^s \ge N$; keep the smallest $h$ with $2^h - 2 \ge H$. Every prefix length $p$ with $n + s \le p \le 32 - h$ works; if $n + s + h > 32$ the request is impossible. When several masks fit, any of them works and the answer options usually contain only one; if the question asks for “the most subnets”, take the longest prefix, for “the most hosts per subnet” the shortest.

</div>

```python {filename="choose_mask.py, lines 6–19",linenos=table,linenostart=6}
def choose(base, N, H):
    net = ip.IPv4Network(base)
    s = ceil(log2(N)) if N > 1 else 0
    h = ceil(log2(H + 2))
    print(f"{base}: {N} subnets x {H} hosts: s >= {s}, h >= {h}")
    ok = []
    for p in range(net.prefixlen + s, 33 - h):
        subs, hosts = 2 ** (p - net.prefixlen), 2 ** (32 - p) - 2
        ok.append(p)
        mask = ip.IPv4Network(f"0.0.0.0/{p}").netmask
        print(f"   /{p} = {mask}: {subs} subnets of {hosts} hosts")
    if not ok:
        print(f"   impossible: {net.prefixlen}+{s}+{h} > 32")
    return ok
```

```text {filename="Output of choose_mask.py"}
172.20.0.0/16: 50 subnets x 900 hosts: s >= 6, h >= 10
   /22 = 255.255.252.0: 64 subnets of 1022 hosts
10.0.0.0/8: 1000 subnets x 4000 hosts: s >= 10, h >= 12
   /18 = 255.255.192.0: 1024 subnets of 16382 hosts
   /19 = 255.255.224.0: 2048 subnets of 8190 hosts
   /20 = 255.255.240.0: 4096 subnets of 4094 hosts
192.168.5.0/24: 6 subnets x 25 hosts: s >= 3, h >= 5
   /27 = 255.255.255.224: 8 subnets of 30 hosts
192.168.5.0/24: 10 subnets x 20 hosts: s >= 4, h >= 5
   impossible: 24+4+5 > 32
```

For $50 \times 900$: $s = 6$ ($64 \ge 50$) and $h = 10$ ($1022 \ge 900$), and $16+6+10 = 32$ leaves no slack: exactly one mask. With $1000 \times 4000$ in a `/8` there is slack, and three masks qualify. Ten subnets of twenty hosts do not fit in a `/24`: $4 + 5$ bits are needed and only $8$ exist.

<div class="nb nb-remark" id="remark-6-2-2">

<strong>Remark 6.2.2</strong> (The two classic slips) — Hosts need $2^h - 2 \ge H$, not $2^h \ge H$: $30$ hosts need $5$ bits ($30 = 32-2$), but $31$ hosts need $6$. And subnets need $2^s \ge N$: $70$ subnets need $7$ bits ($128$), not $6$ ($64$).

</div>

### 6.2.ii Is this a valid host address? {#s6-2-ii}

<figure class="nb-fig"><img src="fig-1.svg" alt="Figure 1" loading="lazy"></figure>

The question “given network `150.200.0.0` with $10$ bits of subnetting, which address is a valid host” is a test of three things: the prefix is $/16 + 10 = /26$; blocks are $64$ addresses long, starting at multiples of $64$ in the last octet; and an address whose host bits are all $0$ or all $1$ within its block is not a host.

```text {filename="Output of valid_host.py"}
150.200.0.0/16 + 10 borrowed bits -> /26, mask 255.255.255.192
    1024 subnets, 62 hosts each, block size 64
   150.200.3.64     in 150.200.3.64/26    -> subnet (network) address
   150.200.3.127    in 150.200.3.64/26    -> broadcast address
   150.200.3.100    in 150.200.3.64/26    -> VALID host
   150.200.17.192   in 150.200.17.192/26  -> subnet (network) address
   150.200.17.255   in 150.200.17.192/26  -> broadcast address
   150.200.255.254  in 150.200.255.192/26 -> VALID host
   150.200.0.0      in 150.200.0.0/26     -> subnet (network) address
   150.201.0.10     not in 150.200.0.0/16 at all
```

`150.200.3.127` <em>looks</em> ordinary but is the broadcast of `150.200.3.64/26` ($127 = 64 + 63$); `150.200.17.192` is the start of a block ($192 = 3 \times 64$). Divide the last octet by the block size: remainder $0$ is a network, remainder $63$ a broadcast, anything else a host.

<div class="nb nb-moral">

$s$ with $2^s \ge N$, $h$ with $2^h-2 \ge H$, check $n+s+h \le 32$. For a candidate host, find its block (multiples of the block size) and reject the first and last address.

</div>

## 6.3 VLSM, aggregation and special addresses {#sec-cn-vlsm}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> five departments of $500$, $200$, $100$, $50$ and $2$ hosts packed into one `/22`, largest first.</em>

</div>

### 6.3.i Variable-length subnet masks {#s6-3-i}

Equal subnets waste space when needs differ: a point-to-point link needs $2$ addresses, a hostel LAN $500$. <strong>VLSM</strong> gives each subnet its own prefix length.

<div class="nb nb-remark" id="algorithm-6-3-1">

<strong>Algorithm 6.3.1</strong> (VLSM allocation) — Sort the requests by size, largest first. For each, take the smallest power of two $\ge H+2$ and allocate the lowest free block of that size; a block of size $2^k$ must start at a multiple of $2^k$. Largest-first guarantees the alignment never leaves unusable gaps.

</div>

```text {filename="Output of vlsm.py"}
VLSM inside 172.16.8.0/22 (1024 addresses), largest request first:
   Hostel LAN  500 -> 172.16.8.0/23     510 usable, bcast 172.16.9.255
   Labs        200 -> 172.16.10.0/24    254 usable, bcast 172.16.10.255
   Library     100 -> 172.16.11.0/25    126 usable, bcast 172.16.11.127
   Admin        50 -> 172.16.11.128/26   62 usable, bcast 172.16.11.191
   Router link   2 -> 172.16.11.192/30    2 usable, bcast 172.16.11.195
   left over: 172.16.11.196/30, 172.16.11.200/29
              172.16.11.208/28, 172.16.11.224/27
Aggregation: four /24s behind the same next hop
    200.10.4.0/24, 200.10.5.0/24, 200.10.6.0/24, 200.10.7.0/24
      -> 200.10.4.0/22
    200.10.5.0/24, 200.10.6.0/24 -> 200.10.5.0/24, 200.10.6.0/24
      (cannot be merged into one prefix)
    covering prefix 200.10.4.0/22 also claims 200.10.4.0/24, 200.10.7.0/24
```

The allocation lines show that every subnet starts on a multiple of its size, and the leftover space is still in clean, aligned blocks for later use.

### 6.3.ii Supernetting and route aggregation {#s6-3-ii}

The reverse operation, <strong>aggregation</strong> (<strong>supernetting</strong>), merges contiguous prefixes with the same next hop into one shorter prefix, shrinking routing tables: an ISP advertises one `/16` for thousands of customer networks. Contiguous /24s merge into one prefix only if there are $2^k$ of them and the first is aligned on a multiple of $2^k$ (the last lines of the output above). `200.10.5.0/24` and `200.10.6.0/24` cannot be merged: the only single prefix covering both, `200.10.4.0/22`, also claims `.4` and `.7`. A router may still advertise the `/22` if those addresses belong to no one else, or if a more specific route for them exists elsewhere: longest-prefix match ([Section 6.4](#sec-cn-lpm)) then sends their traffic the right way.

### 6.3.iii Special and private addresses {#s6-3-iii}

```text {filename="Output of special.py"}
RFC 1918 block 10.0.0.0/8      10.0.0.0 - 10.255.255.255  (16777216 addresses)
RFC 1918 block 172.16.0.0/12   172.16.0.0 - 172.31.255.255  (1048576 addresses)
RFC 1918 block 192.168.0.0/16  192.168.0.0 - 192.168.255.255  (65536 addresses)
address          RFC1918 loopback link-local multicast py is_private
0.0.0.0          -       -        -          -         yes          
127.0.0.1        -       yes      -          -         yes          
127.45.6.7       -       yes      -          -         yes          
10.1.2.3         yes     -        -          -         yes          
172.31.255.1     yes     -        -          -         yes          
172.32.0.1       -       -        -          -         -            
192.168.1.1      yes     -        -          -         yes          
169.254.10.20    -       -        yes        -         yes          
100.64.0.1       -       -        -          -         -            
192.0.2.10       -       -        -          -         yes          
224.0.0.251      -       -        -          yes       -            
255.255.255.255  -       -        -          -         yes          
8.8.8.8          -       -        -          -         -            
UDP to 127.0.0.1: server bound there got b'ping'
UDP to 127.45.6.7: server bound there got b'ping'
```

| Block | Meaning |
|:--|:--|
| `0.0.0.0/8` | “this network”; `0.0.0.0` as a source means “I do not have an address yet” (DHCP); as a server bind address, “all interfaces” |
| `127.0.0.0/8` | <strong>loopback</strong> (RFC 1122): never leaves the host; any address in the block works, `127.0.0.1` by convention |
| `10/8`, `172.16/12`, `192.168/16` | <strong>private</strong> (RFC 1918): not routed on the Internet, reused by every home and campus behind NAT |
| `169.254.0.0/16` | <strong>link-local</strong> (RFC 3927): self-assigned when DHCP fails; not routed |
| `100.64.0.0/10` | shared address space for carrier-grade NAT (RFC 6598) |
| `192.0.2.0/24` etc. | reserved for documentation (RFC 5737) |
| `224.0.0.0/4` | multicast (class D) |
| `255.255.255.255` | <strong>limited broadcast</strong>: every host on this link; routers never forward it |
| host bits all $1$ | <strong>directed broadcast</strong> for that network; routers do not forward it by default today (RFC 2644), because of amplification attacks |

<div class="nb-caption" id="table-6-1">

<strong>Table 6.1.</strong> Special-purpose IPv4 addresses.

</div>

<div class="nb nb-remark" id="remark-6-3-2">

<strong>Remark 6.3.2</strong> (Testing your own IP stack: ping 127.0.0.1) — To check that TCP/IP itself works on a machine, without any network card or cable involved, use a loopback address: `ping 127.0.0.1` (or `localhost`). The script shows that `127.45.6.7` works too: Linux routes all of `127/8` to the loopback interface. Also in the output: `172.32.0.1` is <em>not</em> private (the block ends at `172.31.255.255`), `169.254.x.x` is link-local, not RFC 1918, and Python’s `is_private` is broader than RFC 1918 (it means “not globally routable”, so it includes loopback, link-local, `0.0.0.0` and the documentation block).

</div>

<div class="nb nb-moral">

VLSM: largest first, aligned blocks. Aggregate only aligned power-of-two runs. Loopback is `127/8`; private is `10/8`, `172.16/12`, `192.168/16`; `169.254/16` is link-local.

</div>

## 6.4 Longest-prefix match {#sec-cn-lpm}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> a router holding `/16`, `/22`, `/24`, `/25` and `/26` routes that all contain `10.20.6.200`: the `/26` wins.</em>

</div>

A host or router’s <strong>forwarding table</strong> maps prefixes to a next hop (a neighbour’s IP address, or “directly connected” on some interface). Prefixes overlap: aggregation creates short prefixes, exceptions create long ones.

<div class="nb nb-definition" id="definition-6-4-1">

<strong>Definition 6.4.1</strong>. <strong>Longest-prefix match</strong>: among all entries whose prefix contains the destination address, use the one with the longest prefix length (the most specific route). The <strong>default route</strong> `0.0.0.0/0` contains every address and is used only when nothing else matches.

</div>

```text {filename="Output of lpm.py"}
forwarding table:
   10.20.0.0/16      via 192.0.2.1 (ISP-A)
   10.20.4.0/22      via 192.0.2.5 (core)
   10.20.6.0/24      connected, eth1
   10.20.6.128/25    via 10.20.6.2 (lab router)
   10.20.6.192/26    via 10.20.6.3 (lab firewall)
   0.0.0.0/0         via 192.0.2.254 (default)
10.20.6.200  matches /16 /22 /24 /25 /26 /0 -> 10.20.6.192/26  lab firewall
10.20.6.150  matches /16 /22 /24 /25 /0     -> 10.20.6.128/25  lab router
10.20.6.20   matches /16 /22 /24 /0         -> 10.20.6.0/24    connected, eth1
10.20.7.9    matches /16 /22 /0             -> 10.20.4.0/22    core
10.20.200.1  matches /16 /0                 -> 10.20.0.0/16    ISP-A
8.8.4.4      matches /0                     -> 0.0.0.0/0       default
integer version agrees: True
```

The same lookup with integers, which is how one reasons on paper:

```python {filename="lpm.py, lines 26–34",linenos=table,linenostart=26}
# the same lookup on integers: (dst & mask) == network, longest prefix wins
def lookup_int(dst):
    d = int(ip.IPv4Address(dst)); best = None
    for n, h in routes:
        m = int(n.netmask)
        if d & m == int(n.network_address):               # prefix matches
            if best is None or n.prefixlen > best[0].prefixlen:
                best = (n, h)                             # the longest so far
    return best
```

<div class="nb nb-remark" id="algorithm-6-4-2">

<strong>Algorithm 6.4.2</strong> (Answering a route-selection question) — For each route, AND the destination with the route’s mask and compare with the route’s network; keep the matches; choose the longest prefix. Directly connected routes are not special here: they win only if they are the longest match. For a host, the same rule decides whether the destination is on the local subnet (deliver directly, ARP for the destination) or not (send to the default gateway, ARP for the gateway).

</div>

<div class="nb nb-remark" id="remark-6-4-3">

<strong>Remark 6.4.3</strong> (Traps in the exhibit questions) — The mask, not the dotted-decimal “look”, decides membership: `10.20.6.150` is in `10.20.6.128/25` but not in `10.20.6.192/26`. A route with a longer prefix wins even if its next hop is “worse” (metric and administrative distance only break ties between routes to the <em>same</em> prefix). And a destination outside every specific prefix goes to the default route; if there is none, the packet is dropped and an ICMP destination unreachable is returned.

</div>

<div class="nb nb-moral">

Most specific route wins: the longest prefix that contains the destination; `/0` is the last resort.

</div>
