---
title: "7 · Memory management and paging"
linkTitle: "7 Memory and paging"
weight: 7
math: true
---
## 7.1 Logical vs physical addresses {#os-7-1}

The CPU generates **logical (virtual) addresses**; the **MMU** (memory-management unit, hardware) translates them to **physical addresses** at run time. This lets every process use the same addresses (each starts at 0) without clashing, and lets the OS move processes around.

**Address binding** can happen at compile time (fixed address), load time (the loader relocates the code), or **execution time** (translation on every access; what modern systems do).

- **Static linking** copies library code into each executable; **dynamic linking** loads shared libraries (`.so`, `.dll`) at run time, so one copy in RAM serves all processes.

## 7.2 Contiguous allocation and fragmentation {#os-7-2}

Each process gets one contiguous block.

- **Internal fragmentation:** wasted space **inside** an allocated block (you got 4 KB, needed 3 KB).
- **External fragmentation:** enough free memory **in total**, but split into holes too small to use.
- **Compaction** moves processes to merge holes (expensive; needs run-time binding).

**Placement policies** for a request: **first fit** (first hole big enough; fastest), **best fit** (smallest hole big enough), **worst fit** (largest hole), **next fit** (first fit starting where the last search stopped).

<div class="nb nb-example">

<strong>Example</strong> (First, best, worst fit)

Holes (in order): 100, 500, 200, 300, 600 KB. Requests in order: 212, 417, 112, 426 KB.

- **First fit:** 212 → 500 (leaves 288); 417 → 600 (leaves 183); 112 → 288 (leaves 176); 426 → **no hole fits, must wait**.
- **Best fit:** 212 → 300 (88 left); 417 → 500 (83); 112 → 200 (88); 426 → 600 (174). **All fit.**
- **Worst fit:** 212 → 600 (388 left); 417 → 500 (83); 112 → 388 (276); 426 → **must wait**.

Best fit wins here; in general first fit and best fit beat worst fit.

</div>

<div class="nb nb-remark">

<strong>Which fragmentation?</strong> — Fixed partitions: internal (and external). Variable partitions: external only. **Paging: internal only** (part of the last page). **Segmentation: external.**

</div>

## 7.3 Paging {#os-7-3}

<div class="nb nb-definition">

<strong>Definition</strong> — Physical memory is divided into fixed-size **frames**, logical memory into **pages** of the same size. The **page table** (one per process) maps page number → frame number. A logical address splits into a **page number** $p$ (high bits) and an **offset** $d$ (low bits):

$$p = \left\lfloor \frac{\text{address}}{\text{page size}} \right\rfloor, \quad d = \text{address} \bmod \text{page size}, \quad \text{physical} = \text{frame}(p) \times \text{page size} + d.$$

</div>

Paging removes external fragmentation (any free frame works) at the cost of one translation per access.

<div class="nb nb-example">

<strong>Example</strong> (Address translation)

Page size 1 KB (1024 bytes). Logical address 2500: page $= \lfloor 2500/1024 \rfloor = 2$, offset $= 2500 - 2048 = 452$. If the page table maps page 2 → frame 5, the physical address is $5 \times 1024 + 452 = $ **5572**.

</div>

<div class="nb nb-example">

<strong>Example</strong> (Bits and page-table size)

32-bit logical addresses, 4 KB pages ($2^{12}$): offset = **12 bits**, page number = $32 - 12 = $ **20 bits**, so $2^{20}$ (about a million) pages. With 4-byte entries the page table is $2^{20} \times 4 = $ **4 MB per process**. If physical memory is 1 GB ($2^{30}$), there are $2^{30}/2^{12} = 2^{18}$ frames, so a frame number needs 18 bits.

</div>

**Page-table entry bits:** frame number, **valid/present** (else page fault), **protection** (read/write/execute), **referenced** (used recently), **dirty** (modified; must be written back before eviction).

**Page size trade-off:** larger pages → smaller page tables, fewer TLB misses, but more internal fragmentation. Smaller pages → the reverse. (So "smaller pages give a smaller page table" is false.)

## 7.4 TLB and effective access time {#os-7-4}

Every memory access needs a page-table lookup first, which would double memory time. The **TLB** (translation lookaside buffer) is a small, fast cache of recent page → frame translations. On a context switch it is flushed unless entries carry an address-space ID.

<div class="nb nb-theorem nb-block">

<strong>Effective access time</strong> (TLB time $t$, memory time $m$, hit ratio $h$, single-level page table)

$$\text{EAT} = h\,(t + m) + (1 - h)\,(t + 2m).$$

For a $k$-level page table, a miss costs $t + (k+1)m$. (If the question says TLB time is negligible, drop $t$.)

</div>

<div class="nb nb-example">

<strong>Example</strong> (EAT)

$t = 20$ ns, $m = 100$ ns, $h = 0.8$: $\text{EAT} = 0.8 \times 120 + 0.2 \times 220 = 96 + 44 = $ **140 ns** (40% slower than raw memory). With $h = 0.98$: $0.98 \times 120 + 0.02 \times 220 = $ **122 ns**.

</div>

## 7.5 Page tables for large address spaces {#os-7-5}

A flat table for a 64-bit space would be enormous, and most of it unused. Solutions:

- **Multi-level (hierarchical) paging:** page the page table itself; only the parts in use exist. x86-64 uses 4 levels (cost: up to 4 extra memory reads on a TLB miss).
- **Hashed page table:** hash the page number into a table of chains.
- **Inverted page table:** one entry **per physical frame** (not per page), saying which process and page it holds. Small, but lookup needs a search or hash.

## 7.6 Segmentation {#os-7-6}

A logical address is (segment number, offset). Each segment (code, data, stack…) has a **base** and a **limit**; the access is legal only if offset < limit, and the physical address is base + offset. It matches the program's logical parts, but segments vary in size, so **external fragmentation** returns. **Segmented paging** pages each segment to get both benefits.

<div class="nb nb-example">

<strong>Example</strong> (Segment translation)

Segment 0: base 2000, limit 600. Segment 1: base 5200, limit 300. Segment 2: base 3600, limit 900. Address (2, 77) → $3600 + 77 = $ **3677**. Address (1, 300) → **trap** (offset 300 is not < limit 300). Address (0, 599) → **2599**.

</div>

<div class="nb nb-moral">

Paging = page number + offset, physical = frame × page size + offset; it ends external fragmentation and the TLB makes the extra lookup cheap. EAT = h(t+m) + (1−h)(t+2m).

</div>
