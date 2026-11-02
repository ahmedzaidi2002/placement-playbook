---
title: "Cache and memory hierarchy"
weight: 5
---

16 questions asked by MathWorks, Qualcomm, Texas Instruments. Try each one first, then open the toggle: it gives the answer, why it is right, and the idea behind it explained from scratch.

### 1 · Q10, cache writing

*Asked by: MathWorks (IISc 2024)*

(Only the heading was photographed.) Which cache write policy is used when the cache is
updated but main memory is not updated? [cut off in the source]

{{< details title="Answer and explanation" closed="true" >}}

**Answer: write-back**

**Why.** In write-back, a write updates only the cache line and marks it "dirty"; main memory is updated later, when the line is evicted. In write-through, every write updates both cache and memory.

**Concept: write policies.** Write-through is simple and keeps memory always current, but costs memory bandwidth on every write (usually softened with a write buffer). Write-back saves bandwidth when a line is written many times, at the cost of complexity (dirty bits, coherence).

{{< /details >}}

### 2 · Q2, cache hits

*Asked by: MathWorks (IISc 2024)*

What determines the high hit rate of cache memory? (more than one answer possible)

- **(a)** Size of RAM
- **(b)** Size of cache
- **(c)** Number of caches
- **(d)** Cache access speed

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) size of the cache** (adding cache levels, (c), is also defensible)

**Why.** A larger cache holds more of the program's working set, so more accesses hit. More cache levels can raise the combined hit rate. RAM size doesn't change cache hits, and access speed changes the hit **time**, not the hit rate. (Mapping/associativity and replacement policy matter too.)

**Concept: why caches work.** Locality: programs reuse recent data (temporal) and nearby data (spatial). Hit rate depends on capacity, block size, associativity and replacement policy.

{{< /details >}}

### 3 · Q7, memory interleaving

*Asked by: MathWorks (IISc 2024)*

In memory interleaving, the lower-order bits of the address are used to:

- **(a)** get the data
- **(b)** get the address of the module
- **(c)** get the address of the data within the module
- **(d)** all of these

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) to select the memory module**

**Why.** In low-order interleaving, consecutive addresses go to consecutive modules (word 0 in module 0, word 1 in module 1, ...). So the lowest bits choose the module and the higher bits the word inside it.

**Concept: interleaving for bandwidth.** Sequential accesses hit different modules, which can work in parallel, so a burst of consecutive words is fetched faster than from one module.

{{< /details >}}

### 4 · Q27, type of cache miss

*Asked by: Qualcomm (Nov 2024)*

Which type of cache miss occurs when the working set of a process is larger than
[cut off in the source] (the cache)?

- **(a)** Memory Miss
- **(b)** Cold Miss
- **(c)** Conflict Miss
- **(d)** Capacity Miss

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) capacity miss**

**Why.** If the working set is larger than the whole cache, blocks get evicted before they are reused even with perfect placement: capacity misses.

**Concept: the 3 Cs of cache misses.** Compulsory (cold): first access to a block. Capacity: cache too small for the working set. Conflict: too many blocks map to the same set (limited associativity), even though the cache has space elsewhere.

{{< /details >}}

### 5 · Q27, accesses that reach main memory

*Asked by: Qualcomm (HirePro, Aug 2025)*

A processor has an L1 and an L2 cache with hit rates 0.58 and 0.76 respectively. What
fraction of the memory accesses reach main memory?

- **(a)** 0.15
- **(b)** 0.58
- **(c)** 0.3036
- **(d)** 0.1008

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) 0.1008**

**Why.** An access reaches main memory only if it misses L1 **and** misses L2. With L2's hit rate measured among L1 misses (a local hit rate): (1 − 0.58)(1 − 0.76) = 0.42 × 0.24 = 0.1008.

**Concept: multi-level caches.** Global miss rate = product of local miss rates. Average access time = L1 hit time + L1 miss rate × (L2 hit time + L2 local miss rate × memory time).

{{< /details >}}

### 6 · Memory hierarchy

*Asked by: Qualcomm (BITS Goa 2024, Q37)*

Which is the second level of memory?

- **(a)** Main memory
- **(b)** Register
- **(c)** Secondary memory
- **(d)** Cache memory

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) cache memory** (counting registers as level 1)

**Why.** From the CPU outwards: registers (level 1), cache (level 2), main memory (level 3), secondary storage (level 4). (Books that start at level 0 for registers would call main memory the second level.)

**Concept: memory hierarchy.** Each level is larger, slower and cheaper per byte than the one above it. Caching frequently used data in the faster level gives the illusion of a memory that is both big and fast.

{{< /details >}}

### 7 · Caches

*Asked by: Qualcomm (Delhi campus 2024, Q36)*

In which policy is data written only to the cache block, and the modified block written to main memory only when it is replaced?

I. Write back  
II. Write through

- **(a)** Neither (I) nor (II)
- **(b)** Both (I) and (II)
- **(c)** Only (II)
- **(d)** Only (I)

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) only (I), write back**

**Why.** Write back writes only to the cache block, marks it dirty, and writes it to memory when the block is replaced. Write through updates memory on every write.

**Concept: write policies** (see above). On a write miss, write-back caches usually "write-allocate" (fetch the block, then write), write-through caches often don't.

{{< /details >}}

### 8 · Memory organisation

*Asked by: Qualcomm (Delhi campus 2024, Q44)*

Which of the following statements about DRAM are true?

I. Address lines are multiplexed to reduce the number of pins.  
II. The higher-order bits select a column and are latched by RAS.  
III. The lower-order bits select a row and are latched by CAS.  
IV. The higher-order bits select a row and are latched by RAS.  
V. The lower-order bits select a column and are latched by the row address strobe.

- **(a)** Only (I), (II) and (III)
- **(b)** Only (II) and (III)
- **(c)** Only (IV) and (V)
- **(d)** Only (I), (IV) and (V)

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) only (I), (IV) and (V)**

**Why.** A DRAM sends the row address first (high-order bits, latched by RAS) and then the column address on the same pins (low-order bits, latched by CAS). Multiplexing halves the address pins (I). (IV) is true. (V) is meant as the column statement (it misprints "row address strobe" for CAS).

**Concept: DRAM addressing.** Cells are in a grid. Activating a row (RAS) copies the whole row into sense amplifiers; the column address (CAS) then picks bits from that row. Reading more columns from an already-open row is fast.

{{< /details >}}

### 9 · Memory organisation

*Asked by: Qualcomm (Delhi campus 2024, Q60)*

What is the order of the steps that take place to perform a **read** from a specified memory location?

I. A read signal is issued by the CPU.  
II. The word is loaded into the Memory Data Register and used by the CPU.  
III. The address of the word to be read is loaded into the Memory Address Register.

- **(a)** (I), (II) and (III)
- **(b)** (III), (I) and (II)
- **(c)** (II), (III) and (I)
- **(d)** (III), (II) and (I)

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) (III), (I), (II)**

**Why.** Put the address in the Memory Address Register, assert the read signal, wait for memory, and the word arrives in the Memory Data Register for the CPU.

**Concept: MAR and MDR.** MAR holds the address being accessed; MDR (or MBR) holds the data going to or from memory. Every memory access goes through these two registers.

{{< /details >}}

### 10 · Memory devices

*Asked by: Qualcomm (IISc 2024, Q60)*

In the case of an EPROM, which type of rays is used to erase the data stored in memory?

- **(a)** Infrared rays
- **(b)** Supersonic rays
- **(c)** Ultraviolet rays
- **(d)** Microwave rays

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) ultraviolet rays**

**Why.** UV light through the chip's quartz window gives the electrons trapped on the floating gates enough energy to escape, erasing the whole chip. EEPROM and flash erase electrically instead.

**Concept: ROM family.** ROM (fixed at manufacture), PROM (programmed once), EPROM (UV-erasable), EEPROM (electrically erasable byte by byte), Flash (electrically erasable in blocks, dense and cheap).

{{< /details >}}

### 11 · number of cache sets

*Asked by: Texas Instruments (NIT Calicut 2023)*

A 16-bit microprocessor has a 2-way set-associative cache of 256 bytes with 8-byte lines. How
many sets?

- **(a)** 8
- **(b)** 16
- **(c)** 32
- **(d)** 64

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) 16**

**Why.** 256-byte cache ÷ 8-byte lines = 32 lines. 2-way set-associative means 2 lines per set: 32/2 = 16 sets.

**Concept: cache geometry.** Sets = cache size / (line size × associativity). An address splits into tag | set index (log₂ sets bits) | byte offset (log₂ line size bits).

{{< /details >}}

### 12 · reading a DRAM cell

*Asked by: Texas Instruments (NIT Calicut 2023)*

DRAM read steps: (1) precharge the column line to half threshold; (2) assert one row line;
(3) the bit line moves slightly above or below threshold depending on the stored bit; (4) sense
and amplify. Which step is hit directly by a small storage capacitor?

- **(a)** 1
- **(b)** 2
- **(c)** 3
- **(d)** 4

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) step 3**

**Why.** When the row is activated, the tiny cell capacitor shares its charge with the large bit-line capacitance. The bit line moves only slightly above or below the precharge level, by an amount proportional to the cell's capacitance, so a smaller cell gives a weaker signal for the sense amplifier.

**Concept: charge sharing in DRAM.** ΔV ≈ (V_cell − V_pre) × C_cell/(C_cell + C_bitline). Because C_bitline is much bigger, ΔV is small (tens of mV), which is why sensitive sense amplifiers and periodic refresh are needed.

{{< /details >}}

### 13 · flash memory

*Asked by: Texas Instruments (NIT Calicut 2023)*

Which statement does not describe Flash memory?

- **(a)** It can erase data byte-wise
- **(b)** It is used to rewrite data frequently
- **(c)** NOR gates are used to design this memory
- **(d)** Both 1 and 3
- **(e)** None of these

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) it can erase data byte-wise** (does not describe flash)

**Why.** Flash erases whole blocks, never single bytes. NOR flash exists, so (c) does describe flash. (Flash also has limited write endurance, so (b) is doubtful too, but no option pairs (a) with (b).)

**Concept: NOR vs NAND flash.** NOR: random byte reads, can execute code in place, slower writes (used for firmware). NAND: denser and cheaper, read in pages (used in SSDs and memory cards).

{{< /details >}}

### 14 · memory size from pins

*Asked by: Texas Instruments (IISc 2023)*

A memory has 8 data and 16 address lines. Its size?

- **(a)** 128 KB
- **(b)** 256 KB
- **(c)** 512 KB
- **(d)** 1024 KB
- **(e)** None

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (e) none** (it is 64 KB)

**Why.** 16 address lines select 2¹⁶ = 65,536 locations; 8 data lines mean each location is 1 byte. Size = 65,536 bytes = 64 KB.

**Concept: memory size from pins.** Size = 2^(address lines) × (data lines) bits.

{{< /details >}}

### 15 · locality on a Cortex-A72

*Asked by: Texas Instruments (TI prep guide)*

(1) Which linear structure is fastest to loop over? (2) Row-major or column-major for a C 2D
matrix? (3) How to detect a loop in a linked list?

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (1) an array; (2) row-major; (3) Floyd's cycle-finding algorithm**

**Why.** (1) Array elements are contiguous, so each cache line brought in serves several elements (spatial locality); linked-list nodes are scattered. (2) C stores 2-D arrays row by row, so looping row-major walks memory sequentially. (3) Slow and fast pointers detect a loop in O(1) space.

**Concept: cache-friendly code.** Access memory sequentially and reuse data while it is in cache. Looping over a C matrix column by column jumps a whole row each step and can be many times slower.

{{< /details >}}

### 16 · large memory

*Asked by: Texas Instruments (IISc 2023)*

A microcomputer needs a large memory. Which choice?

{{< details title="Answer and explanation" closed="true" >}}

**Answer: SRAM as cache combined with DRAM as main memory**

**Why.** DRAM is dense and cheap per bit (one transistor + one capacitor) but slower and needs refresh; SRAM is fast but uses six transistors per bit. Using a small SRAM cache in front of a large DRAM gives both speed and capacity.

**Concept: SRAM vs DRAM.** SRAM: flip-flop storage, fast, no refresh, expensive (caches, registers). DRAM: capacitor storage, dense, refresh needed (main memory).

{{< /details >}}
