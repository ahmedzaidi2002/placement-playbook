---
title: "Memory management and paging"
weight: 2
---

14 questions asked by DevRev, MathWorks, Oracle, Qualcomm, Texas Instruments. Try each one first, then open the toggle: it gives the answer, why it is right, and the idea behind it explained from scratch.

### 1 · Q3, memory pool for dynamic allocation

*Asked by: DevRev (HackerEarth OA)*

In an operating system, which of these options refers to the area in memory that is used
as a pool for dynamic memory allocation?

- **(a)** Stack
- **(b)** Heap
- **(c)** Virtual memory
- **(d)** Data segment

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) heap**

**Why.** `malloc`/`new` carve blocks out of the heap. The stack holds call frames and local variables; the data segment holds initialised globals and statics; virtual memory is the whole address-space mechanism.

**Concept: process memory layout.** From low to high addresses: text (code), data (initialised globals), bss (zero-initialised globals), heap (grows up), ..., stack (grows down).

{{< /details >}}

### 2 · Q22, thrashing

*Asked by: MathWorks (IISc 2024)*

Which of these reduce thrashing? (more than one answer)

- **(a)** Decrease the degree of multiprogramming
- **(b)** Increase the RAM
- **(c)** Decrease the page size
- **(d)** None of these

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) and (b)**

**Why.** Thrashing happens when processes don't have enough frames for their working sets and spend their time paging. Running fewer processes (a) or adding RAM (b) gives each process room. Smaller pages do not fix a shortage of memory.

**Concept: thrashing.** CPU utilisation collapses because the CPU waits on page faults. The OS sees low CPU use and admits more processes, making it worse. Cure: reduce multiprogramming, using the working-set model or page-fault-frequency control.

{{< /details >}}

### 3 · why "virtual" memory

*Asked by: Oracle (HackerRank MCQ test)*

Why is a virtual memory address called "virtual"?

- **(a)** This memory address does not map to the actual memory cell that corresponds to the address number.
- **(b)** This memory is the same as physical memory.
- **(c)** This memory cannot be accessed by applications at run time.
- **(d)** This memory address is always present even after a system is restarted.

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) the address does not map directly to the physical memory cell with that number**

**Why.** A virtual address is translated by the MMU through page tables to some physical frame, which can be anywhere, or the page may not be in RAM at all (it may be on disk).

**Concept: virtual memory.** Each process sees its own large, private address space. The OS and hardware map pages of it to physical frames on demand. Benefits: isolation, programs larger than RAM, easy sharing.

{{< /details >}}

### 4 · Q59, proportional frame allocation

*Asked by: Qualcomm (Nov 2024)*

There are 55 frames to be divided between two processes P1 and P2; P1 has 17 pages and P2
[cut off in the source].

- **(a)** 19 frames for P1 and 36 frames for P2.
- **(b)** 17 frames for P1 and 30 frames for P2.
- **(c)** 20 frames for P1 and 35 frames for P2.
- **(d)** 25 frames for P1 and 30 frames for P2.

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) 19 frames for P1 and 36 for P2** (most likely; P2's page count is cut off)

**Why.** Proportional allocation gives each process frames in proportion to its size: aᵢ = (sᵢ / S) × m. Option (a) fits P2 having 32 pages: 55 × 17/49 ≈ 19.1 and 55 × 32/49 ≈ 35.9. (b) does not use all 55 frames.

**Concept: frame allocation.** Equal allocation splits frames evenly; proportional allocation gives bigger processes more. Priority-based allocation weights by priority instead of size.

{{< /details >}}

### 5 · Q30, page stealing

*Asked by: Qualcomm (HirePro, Aug 2025)*

Which one of the given options is correct about page stealing?

- **(a)** It cleans up all the dirty pages.
- **(b)** It shows that the system is efficient.
- **(c)** It takes the page frames out and makes space for the newer page.
- **(d)** It takes the larger disk space for pages that are paged out.

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) it takes page frames away to make space for newer pages**

**Why.** Page stealing takes frames (often from other processes) when memory is needed. Frequent stealing is a sign of memory pressure, not efficiency.

**Concept: page replacement.** When no frame is free, the OS picks a victim page (by LRU, clock, etc.), writes it to disk if dirty, and reuses its frame.

{{< /details >}}

### 6 · OS Fundamentals

*Asked by: Qualcomm (60-question online assessment)*

A buddy-system allocator manages **8 MB** of memory. Requests arrive in this order:

- P2 requests 99K
- P4 requests 119K
- P1 requests 201K
- P5 requests 91K
- P1 releases
- P3 requests 55K
- P2 releases

What is the internal fragmentation when process P1 releases its memory?

- **(a)** 136K
- **(b)** 135K
- **(c)** 335K
- **(d)** 29K

{{< details title="Answer and explanation" closed="true" >}}

**Answer: no reliable pick** (the key cannot be derived; the nearest listed option is (a) 136K)

**Why.** A buddy allocator rounds each request up to a power of two: P2 99K → 128K (29K wasted), P4 119K → 128K (9K), P1 201K → 256K (55K), P5 91K → 128K (37K). Total internal fragmentation before P1 leaves is 130K; after P1 leaves, 75K. Neither matches an option.

**Concept: buddy system.** Memory is split into halves repeatedly until a block just big enough (a power of two) is found. Freed blocks merge with their "buddy" if it is also free. Rounding up causes internal fragmentation.

{{< /details >}}

### 7 · Operating Systems

*Asked by: Qualcomm (60-question online assessment)*

Segment table (base, length): segment 0 = (402, 245), segment 1 = (341, 449), segment 2 = (111, 23).

What are the physical addresses for these logical addresses, and does a segmentation fault occur for any of them?

- (I) segment 0, offset 402
- (II) segment 2, offset 25

- **(a)** Segmentation Fault for both addresses
- **(b)** 804, 48
- **(c)** 743, 48
- **(d)** 402, Segmentation fault for second address

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) segmentation fault for both addresses**

**Why.** A segment's offset must be smaller than its length. (I) segment 0: offset 402 ≥ length 245 → fault. (II) segment 2: offset 25 ≥ length 23 → fault. (Otherwise the physical address would be base + offset.)

**Concept: segmentation.** A logical address is (segment, offset). The hardware checks offset < limit (length); if it passes, physical = base + offset; if not, it traps (segmentation fault).

{{< /details >}}

### 8 · Memory management

*Asked by: Qualcomm (BITS Hyderabad 2024, Q26)*

Which of the statements given below is/are true about **dynamic partitioning**?

I. Partitions are of fixed length and their number is variable.  
II. Holes are created in memory over time.  
III. Partitions are not of the same length and they vary in number.

- **(a)** Only (I) and (II)
- **(b)** Only (I)
- **(c)** Only (III)
- **(d)** Only (II) and (III)

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) only (II) and (III)**

**Why.** Dynamic (variable) partitioning gives each process exactly the size it needs, so partitions differ in size and number (III). As processes leave, free gaps ("holes") appear between allocated blocks (II): external fragmentation. Fixed-length partitions (I) describe static partitioning.

**Concept: fixed vs variable partitions.** Fixed partitions waste space inside blocks (internal fragmentation). Variable partitions waste space between blocks (external fragmentation), fixed by compaction or paging.

{{< /details >}}

### 9 · Memory management

*Asked by: Qualcomm (IIIT Delhi 2025, Q38)*

Which of the following statements about memory fragmentation is true?

- **(a)** Such issues only occur in heap memory.
- **(b)** Using malloc() instead of calloc() prevents these issues.
- **(c)** These issues occur only in stack memory.
- **(d)** They can be caused by repeated allocation and deallocation.

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) they can be caused by repeated allocation and deallocation**

**Why.** Allocating and freeing blocks of different sizes over time leaves scattered gaps that are too small to use. It is not limited to the heap (physical memory fragments too), and malloc vs calloc only differ in zero-filling.

**Concept: fragmentation.** External: free memory is split into small pieces. Internal: allocated blocks are larger than requested. Pools of fixed-size blocks avoid external fragmentation.

{{< /details >}}

### 10 · Memory management

*Asked by: Qualcomm (NIT Durgapur)*

Which of the given statements is/are **not** true regarding memory management?

I. Memory management refers to management of primary memory.  
II. Memory management refers to management of secondary memory.

- **(a)** Both (I) and (II)
- **(b)** Only (II)
- **(c)** Neither (I) nor (II)
- **(d)** Only (I)

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) only (II)** is not true

**Why.** In OS terms, "memory management" means managing main (primary) memory: allocation, protection, paging, swapping. Secondary storage is handled by file-system and disk management. (Swapping moves pages to disk, but what is managed is still main memory.)

**Concept: OS subsystems.** Process management, memory management (RAM), file systems and storage management (disks), I/O management (devices).

{{< /details >}}

### 11 · Virtual memory

*Asked by: Qualcomm (BITS Hyderabad 2025, Q30)*

The working-set size of a process should be increased (to minimise page faults) when the page-fault rate is:

- **(a)** Constant
- **(b)** Low
- **(c)** High
- **(d)** Varying

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) high**

**Why.** A high page-fault rate means the process has too few frames for its working set, so the OS should give it more. A very low rate means some frames can be taken away.

**Concept: page-fault-frequency control.** Set an upper and lower bound on the fault rate: above the upper bound add frames; below the lower bound remove frames.

{{< /details >}}

### 12 · free holes

*Asked by: Texas Instruments (IIT ISM 2024)*

Variable partitions of 100, 200, 300; after some terminate, holes of 50, 150, 250 remain. Which
fragmentation?

{{< details title="Answer and explanation" closed="true" >}}

**Answer: external fragmentation**

**Why.** The free memory exists (50 + 150 + 250 = 450) but is split into separate holes between partitions; a request larger than 250 cannot be met even though the total is enough.

**Concept: external fragmentation.** Free space is outside allocated blocks but scattered. Compaction (moving blocks together) or paging solves it.

{{< /details >}}

### 13 · first fit

*Asked by: Texas Instruments (IIT ISM 2024)*

Fixed blocks 120, 80, 200, 60; requests 70, 90, 50, 130 by first fit. Which fragmentation?

{{< details title="Answer and explanation" closed="true" >}}

**Answer: both internal and external fragmentation**

**Why.** First fit: 70 → 120 (50 wasted inside), 90 → 200 (110 wasted), 50 → 80 (30 wasted): internal fragmentation. 130 cannot be placed, although 60 + 50 + 110 + 30 free space exists in total, just not in one block: external fragmentation.

**Concept: first fit.** Put each request in the first block large enough. Fast, but leaves leftovers in fixed blocks (internal) and can strand total free space in pieces (external).

{{< /details >}}

### 14 · fixed partitions

*Asked by: Texas Instruments (IIT BHU 2023)*

Fixed partitions 600, 200, 100, 500 (from the diagram); three processes of 200 each are placed
by first fit. Ratio of internal to external fragmentation?

- **(a)** 1:1
- **(b)** 2:3
- **(c)** 2:1
- **(d)** 1:2

{{< details title="Answer and explanation" closed="true" >}}

**Answer: no option matches the textbook definitions** (the candidate chose 1:1)

**Why.** First fit places the three 200 processes in the 600, 200 and 500 partitions, wasting 400 + 0 + 300 = 700 inside them (internal). The 100 partition stays free; whether it counts as "external" fragmentation depends on the definition, and no ratio in the options follows cleanly.

**Concept: fixed-partition fragmentation.** With fixed partitions, unused space inside an allocated partition is internal fragmentation; a whole free partition too small for any waiting process is usually called external.

{{< /details >}}
