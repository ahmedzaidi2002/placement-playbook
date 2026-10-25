---
title: "10 · I/O, disk scheduling and RAID"
linkTitle: "10 I/O and disks"
weight: 10
math: true
---
## 10.1 How the CPU talks to devices {#os-10-1}

| Method | How | When |
|---|---|---|
| **Programmed I/O (polling)** | the CPU loops checking a status register and moves every byte itself | very fast devices; wastes CPU otherwise |
| **Interrupt-driven I/O** | the CPU starts the operation and does other work; the device interrupts when done | most devices |
| **DMA** (direct memory access) | a DMA controller copies a whole block between device and memory, then interrupts once | large transfers (disk, network) |

- **Character devices:** byte streams, no seeking (keyboard, mouse, terminal, serial port, printer, `/dev/null`).
- **Block devices:** fixed-size blocks, random access, can hold a file system (hard disk, SSD, USB drive, CD-ROM).
- A network card is neither (a network interface).

**Buffering** (holding data in transit, to handle speed or size mismatches; double buffering lets the device fill one buffer while the process uses the other), **caching** (keeping a copy for faster later access), **spooling** (a disk queue for a device that cannot interleave jobs, like a printer).

## 10.2 Disk access time {#os-10-2}

A hard disk has platters → **tracks** (circles) → **sectors**; the same track on all platters is a **cylinder**.

$$\text{access time} = \text{seek time} + \text{rotational latency} + \text{transfer time}.$$

Average rotational latency = half a rotation.

<div class="nb nb-example">

<strong>Example</strong> (Disk access time)

7200 RPM disk, 4 ms average seek, 100 MB/s transfer, read 4 KB. One rotation = $60/7200 = 8.33$ ms, so average rotational latency = **4.17 ms**. Transfer = $4\text{ KB} / 100\text{ MB/s} \approx 0.04$ ms. Total ≈ $4 + 4.17 + 0.04 = $ **8.2 ms**: almost all of it mechanics.

</div>

## 10.3 Disk scheduling: one example, every algorithm {#os-10-3}

**Setup used for every algorithm:** cylinders 0–199, head at **53**, moving towards **higher** cylinders. Request queue (in arrival order): **98, 183, 37, 122, 14, 124, 65, 67.**

<div class="nb nb-example">

<strong>Example</strong> (FCFS: serve in arrival order)

53 → 98 → 183 → 37 → 122 → 14 → 124 → 65 → 67

Movement: 45 + 85 + 146 + 85 + 108 + 110 + 59 + 2 = **640 cylinders**. Fair, but zig-zags.

</div>

<div class="nb nb-example">

<strong>Example</strong> (SSTF: shortest seek time first)

Always go to the nearest pending request: 53 → 65 → 67 → 37 → 14 → 98 → 122 → 124 → 183

Movement: 12 + 2 + 30 + 23 + 84 + 24 + 2 + 59 = **236 cylinders**. Much better, but far requests can **starve**, and it is not optimal.

</div>

<div class="nb nb-example">

<strong>Example</strong> (SCAN: elevator, goes to the end)

Move up serving requests, go all the way to cylinder 199, then reverse: 53 → 65 → 67 → 98 → 122 → 124 → 183 → **199** → 37 → 14

Movement: (199 − 53) + (199 − 14) = 146 + 185 = **331 cylinders**.

</div>

<div class="nb nb-example">

<strong>Example</strong> (C-SCAN: one direction only)

Move up to 199, jump back to 0, continue upwards: 53 → 65 → 67 → 98 → 122 → 124 → 183 → 199 → **0** → 14 → 37

Movement: 146 (up to 199) + 199 (return jump) + 37 = **382 cylinders** if the return is counted, **183** if not (books differ: state your convention). Gives more uniform waiting times than SCAN.

</div>

<div class="nb nb-example">

<strong>Example</strong> (LOOK: like SCAN but turns at the last request)

53 → 65 → 67 → 98 → 122 → 124 → **183** → 37 → 14

Movement: (183 − 53) + (183 − 14) = 130 + 169 = **299 cylinders**.

</div>

<div class="nb nb-example">

<strong>Example</strong> (C-LOOK: like C-SCAN but turns at the last request)

53 → 65 → 67 → 98 → 122 → 124 → 183 → **14** → 37

Movement: 130 + 169 (jump back to 14) + 23 = **322 cylinders** (153 without counting the jump).

</div>

| Algorithm | Head movement | Starvation? |
|---|---|---|
| FCFS | 640 | no |
| SSTF | **236** | yes |
| SCAN | 331 | no |
| C-SCAN | 382 (183) | no |
| LOOK | 299 | no |
| C-LOOK | 322 (153) | no |

<div class="nb nb-remark">

<strong>Conventions change the answer</strong> — the initial direction, whether SCAN goes to the last cylinder (SCAN) or the last request (LOOK), and whether the C-SCAN/C-LOOK return jump is counted. Read the question; state your assumption. For **SSDs** there is no seek, so position-based scheduling is pointless.

</div>

## 10.4 RAID {#os-10-4}

| Level | Idea | Usable capacity ($n$ disks) | Survives |
|---|---|---|---|
| **RAID 0** | striping | $n$ | no failure |
| **RAID 1** | mirroring | 1 disk (half for a pair) | one disk of each mirror |
| **RAID 5** | striping + one parity block per stripe, rotated across disks | $n - 1$ | **1** failure |
| **RAID 6** | two parities | $n - 2$ | **2** failures |
| **RAID 10** | mirrored pairs, striped | $n/2$ | one per mirror pair |

<div class="nb nb-example">

<strong>Example</strong> (RAID capacity)

Eight 4 TB disks (32 TB raw): RAID 0 → 32 TB, no redundancy; RAID 5 → 28 TB, survives 1 failure; RAID 6 → **24 TB**, survives 2; RAID 10 → 16 TB.

</div>

RAID is **not a backup**: it does not protect against deletion, corruption or ransomware. RAID 4 has one dedicated parity disk (a bottleneck); RAID 5 removes that by rotating parity.

## 10.5 SSDs {#os-10-5}

Flash is written in **pages** but erased only in large **blocks**, and cannot overwrite in place. The SSD writes updates to new pages and later garbage-collects old blocks (**write amplification**); **wear levelling** spreads erases evenly; **TRIM** tells the SSD which blocks are free. No seek or rotation, so random reads are nearly as fast as sequential.

<div class="nb nb-moral">

Disks pay milliseconds for mechanics, so the OS reorders requests: SSTF minimises movement but can starve; SCAN/LOOK are fair elevators. RAID 5 survives one failure with $n-1$ disks of capacity, RAID 6 two with $n-2$.

</div>
