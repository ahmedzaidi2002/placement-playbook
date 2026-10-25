---
title: "8 · Virtual memory and page replacement"
linkTitle: "8 Virtual memory"
weight: 8
math: true
---
## 8.1 Virtual memory and demand paging {#os-8-1}

<div class="nb nb-definition">

<strong>Definition</strong> — **Virtual memory** gives each process a large private address space, only part of which is in physical memory; the rest is on disk (or not created yet). With **demand paging**, a page is loaded only when it is first used.

</div>

Touching a page that is not in memory causes a **page fault**:

1. The MMU finds the page-table entry invalid and traps to the kernel.
2. The kernel checks the address is legal (if not → segmentation fault).
3. It finds a free frame; if none, a **replacement algorithm** picks a victim (written to disk first if dirty).
4. It reads the page from disk into the frame, updates the page table.
5. It restarts the instruction that faulted.

<div class="nb nb-theorem nb-block">

<strong>Effective access time with page faults</strong> (fault rate $p$, memory time $m$, fault service time $F$)

$$\text{EAT} = (1 - p)\,m + p\,F.$$

</div>

<div class="nb nb-example">

<strong>Example</strong> (Why faults must be rare)

$m = 200$ ns, $F = 8$ ms $= 8{,}000{,}000$ ns, one fault in 1,000 accesses ($p = 0.001$): $\text{EAT} = 0.999 \times 200 + 0.001 \times 8{,}000{,}000 \approx 8{,}200$ ns: **40 times slower** than memory. To stay within 10% slowdown (220 ns) you need $p < 0.0000025$, about one fault per 400,000 accesses.

</div>

## 8.2 Page-replacement algorithms {#os-8-2}

| Algorithm | Evicts | Note |
|---|---|---|
| **FIFO** | the page loaded longest ago | simple; suffers Belady's anomaly |
| **OPT** (optimal, Belady) | the page whose next use is **furthest in the future** | fewest faults, but needs the future: a benchmark only |
| **LRU** | the page **not used for the longest time** | close to OPT; exact LRU is costly in hardware |
| **Clock / second chance** | circular scan: if reference bit = 1, clear it and move on; evict the first page with bit 0 | practical approximation of LRU |
| **LFU / MFU** | least / most frequently used | rarely good |

Every worked example below uses the reference string **1 2 3 4 1 2 5 1 2 3 4 5** with **3 frames**, starting empty. "F" = fault, "–" = hit; the frames are shown after each reference.

<div class="nb nb-example">

<strong>Example</strong> (FIFO, 3 frames)

| Ref | 1 | 2 | 3 | 4 | 1 | 2 | 5 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Frames | 1 | 1 2 | 1 2 3 | 4 2 3 | 4 1 3 | 4 1 2 | 5 1 2 | 5 1 2 | 5 1 2 | 5 3 2 | 5 3 4 | 5 3 4 |
| | F | F | F | F | F | F | F | – | – | F | F | – |

**9 faults.** Each fault replaces the oldest page.

</div>

<div class="nb nb-example">

<strong>Example</strong> (LRU, 3 frames)

| Ref | 1 | 2 | 3 | 4 | 1 | 2 | 5 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Frames | 1 | 1 2 | 1 2 3 | 4 2 3 | 4 1 3 | 4 1 2 | 5 1 2 | 5 1 2 | 5 1 2 | 3 1 2 | 3 4 2 | 3 4 5 |
| | F | F | F | F | F | F | F | – | – | F | F | F |

**10 faults.** At reference 3 (10th), the least recently used of {5, 1, 2} is 5; at 4 it is 1; at 5 it is 2.

</div>

<div class="nb nb-example">

<strong>Example</strong> (OPT, 3 frames)

| Ref | 1 | 2 | 3 | 4 | 1 | 2 | 5 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Frames | 1 | 1 2 | 1 2 3 | 1 2 4 | 1 2 4 | 1 2 4 | 1 2 5 | 1 2 5 | 1 2 5 | 3 2 5 | 3 4 5 | 3 4 5 |
| | F | F | F | F | – | – | F | – | – | F | F | – |

**7 faults** (the minimum). At reference 4, page 3 is used furthest in the future, so it goes; at 5, page 4 goes; at 3, pages 1 and 2 are never used again (evict either).

</div>

So on this string: **OPT 7 < FIFO 9 < LRU 10**. LRU is usually better than FIFO, but not on every string. On the textbook string `7 0 1 2 0 3 0 4 2 3 0 3 2 1 2 0 1 7 0 1` with 3 frames the counts are **FIFO 15, LRU 12, OPT 9**.

## 8.3 Belady's anomaly {#os-8-3}

For FIFO, **more frames can cause more faults**. The string above with 4 frames gives **10** FIFO faults, more than the 9 with 3 frames.

LRU and OPT are **stack algorithms** (the pages kept with $n$ frames are always a subset of those kept with $n+1$), so they never show the anomaly. FIFO and Clock can.

## 8.4 Frame allocation {#os-8-4}

- **Equal allocation:** $m$ frames among $n$ processes → $\lfloor m/n \rfloor$ each.
- **Proportional allocation:** process $i$ of size $s_i$ gets $a_i = s_i \times m / S$, with $S = \sum s_i$.

<div class="nb nb-example">

<strong>Example</strong> (Proportional allocation)

62 frames, a 10-page process and a 127-page process: $10 \times 62/137 \approx$ **4** frames and $127 \times 62/137 \approx$ **57** frames. Equal allocation would give each 31 and waste 21 on the small one.

</div>

- **Local replacement:** a process evicts only its own pages. **Global replacement:** it can take frames from any process (better throughput, but one process can hurt others).

## 8.5 Thrashing {#os-8-5}

<div class="nb nb-definition">

<strong>Definition</strong> — **Thrashing**: a process (or the whole system) spends more time paging than executing, because it does not have enough frames for the pages it actively uses.

</div>

The vicious circle: faults block processes → CPU utilisation drops → a naive scheduler admits **more** processes → even fewer frames each → more faults.

- **Working set** $W(t, \Delta)$ = the pages used in the last $\Delta$ references. If the total working-set size exceeds the number of frames, suspend a process.
- **Page-fault frequency (PFF):** if a process faults too often, give it more frames; too rarely, take some away.

<div class="nb nb-remark">

<strong>OA: what reduces thrashing?</strong> — Yes: reduce the degree of multiprogramming, add RAM, working-set or PFF allocation, local replacement, better program locality. No: adding processes, a faster CPU, a bigger swap area or disk.

</div>

## 8.6 Copy-on-write and memory-mapped files {#os-8-6}

- **Copy-on-write (COW):** after `fork`, parent and child share all pages marked read-only; a page is copied only when one of them writes to it. So `fork` followed by `exec` copies almost nothing.
- **Memory-mapped files (`mmap`):** a file is mapped into the address space and read through page faults; programs and shared libraries are loaded this way.

## 8.7 Kernel memory allocators {#os-8-7}

- **Buddy system:** memory in blocks of $2^k$ pages; a request is rounded up to a power of two, larger blocks split in halves ("buddies"), and freed buddies merge back. Fast, but up to ~50% internal fragmentation (a 33 KB request gets 64 KB).
- **Slab allocator:** a cache of ready-made objects per type (process descriptors, inodes); no fragmentation for those objects and very fast reuse.

<div class="nb nb-moral">

OPT is the lower bound, LRU the target, Clock the real implementation, and FIFO the only one here that can get worse with more frames. Thrashing is fixed by running fewer processes, not more.

</div>
