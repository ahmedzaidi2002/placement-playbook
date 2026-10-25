---
title: "7 · Memory hierarchy and caches"
linkTitle: "7 Memory and caches"
weight: 7
math: true
---
## 7.1 The hierarchy and locality {#coa-7-1}

Registers → L1 cache → L2 → L3 → main memory (DRAM) → SSD/disk. Going down: **bigger, cheaper per byte, slower**.

Caches work because programs have **locality**:

- **Temporal locality:** recently used data will be used again soon (loop variables).
- **Spatial locality:** data near recently used data will be used soon (array elements). That is why caches move whole **blocks (lines)**.

## 7.2 Memory types {#coa-7-2}

| | SRAM | DRAM |
|---|---|---|
| Cell | 6 transistors (flip-flop) | 1 transistor + 1 capacitor |
| Refresh | not needed | needed (capacitor leaks) |
| Speed / cost / density | fast, expensive, low density | slower, cheap, high density |
| Used for | **caches** | **main memory** |

ROM family: ROM, PROM (program once), EPROM (UV erase), EEPROM (electrical erase), **flash** (block erase).

**Chip numericals:** $k$ address lines and $d$ data lines give $2^k \times d$ bits. To build a larger memory from small chips: chips needed $= \frac{\text{total words}}{\text{chip words}} \times \frac{\text{word width}}{\text{chip width}}$.

<div class="nb nb-example">

<strong>Example</strong> (Memory chips)

Build $8\text{K} \times 16$ from $1\text{K} \times 8$ chips: $\frac{8\text{K}}{1\text{K}} \times \frac{16}{8} = 8 \times 2 = $ **16 chips**, in 8 rows of 2. Address lines: 13 ($2^{13} = 8\text{K}$): 10 go to every chip, 3 go to a **3:8 decoder** that selects the row.

</div>

**Interleaving:** spread consecutive words across several memory modules (module = address mod $m$) so they can be accessed in parallel.

## 7.3 Cache mapping and the address split {#coa-7-3}

A memory address is split into **tag | index | offset**:

- **offset** = $\log_2(\text{block size})$ bits (which byte inside the block),
- **index** = $\log_2(\text{number of sets})$ bits (which set),
- **tag** = the rest (which block of memory is there).

| Mapping | Sets | Index bits | Where a block can go |
|---|---|---|---|
| **Direct-mapped** | = number of lines | $\log_2(\text{lines})$ | exactly one line (block mod lines) |
| **$k$-way set-associative** | lines / $k$ | $\log_2(\text{lines}/k)$ | any of the $k$ lines in its set |
| **Fully associative** | 1 | 0 | any line |

<div class="nb nb-example">

<strong>Example</strong> (Address split)

32-bit addresses, **64 KB** cache, **64-byte** blocks → $2^{16}/2^6 = 1024$ lines. Offset = **6** bits.

- **Direct-mapped:** index $\log_2 1024 = $ **10**, tag $32 - 10 - 6 = $ **16**. Tag storage $1024 \times 16$ bits = 16 Kbit (plus valid/dirty bits).
- **4-way:** $1024/4 = 256$ sets → index **8**, tag **18**.
- **Fully associative:** index 0, tag **26**.

Address `0x12345678` in the direct-mapped cache: offset = low 6 bits = `111000` = 56; index = $\lfloor \text{0x5678}/64 \rfloor = 345$; tag = `0x1234`.

</div>

More associativity → fewer **conflict** misses, but slower and more comparators.

## 7.4 Replacement and a traced example {#coa-7-4}

When a set is full: **LRU** (least recently used), **FIFO**, random, or LFU. Direct-mapped caches need no policy (one choice).

<div class="nb nb-example">

<strong>Example</strong> (Same accesses, three mappings)

Cache with **4 lines**; block addresses accessed: **0, 4, 0, 8, 0, 4**.

- **Direct-mapped** (line = block mod 4): all map to line 0 and keep evicting each other → **6 misses**, 0 hits.
- **2-way set-associative, LRU** (set = block mod 2, all in set 0): 0 M, 4 M, 0 H, 8 M (evicts 4), 0 H, 4 M (evicts 8) → **4 misses**, 2 hits.
- **Fully associative, LRU:** 0 M, 4 M, 0 H, 8 M, 0 H, 4 H → **3 misses** (only compulsory ones).

</div>

**The 3 C's of misses:** **compulsory** (first access; reduced by larger blocks or prefetching), **capacity** (cache too small; bigger cache), **conflict** (too many blocks map to the same set; more associativity).

## 7.5 Write policies {#coa-7-5}

| On a write **hit** | Meaning |
|---|---|
| **Write-through** | write cache **and** memory every time (simple, memory always up to date; use a write buffer) |
| **Write-back** | write only the cache, mark the line **dirty**; write memory when the line is evicted (less traffic) |

| On a write **miss** | Meaning |
|---|---|
| **Write-allocate** | load the block, then write (pairs with write-back) |
| **No-write-allocate** | write straight to memory (pairs with write-through) |

## 7.6 Average memory access time {#coa-7-6}

<div class="nb nb-theorem nb-block">

<strong>AMAT</strong>

$$\text{AMAT} = \text{hit time} + \text{miss rate} \times \text{miss penalty}, \qquad \text{two levels: } t_{L1} + m_{L1}\,\big(t_{L2} + m_{L2}\, t_{\text{mem}}\big)$$

with $m_{L2}$ the **local** miss rate of L2 (misses / accesses that reach L2).

</div>

<div class="nb nb-example">

<strong>Example</strong> (AMAT)

One level: hit 1 cycle, miss rate 5%, penalty 100 → $1 + 0.05 \times 100 = $ **6 cycles**.
Two levels: L1 1 cycle with 10% misses, L2 10 cycles with 20% local misses, memory 100 → $1 + 0.1 \times (10 + 0.2 \times 100) = 1 + 3 = $ **4 cycles**. Global L2 miss rate $= 0.1 \times 0.2 = 2\%$.

</div>

<div class="nb nb-remark">

<strong>Two conventions for hit ratio $h$</strong> — **Hierarchical** (check cache first, then memory): $T = h\,T_c + (1-h)(T_c + T_m)$. **Simultaneous** (both looked up together): $T = h\,T_c + (1-h)\,T_m$. Read which one the question means.

</div>

## 7.7 Cache-friendly code and coherence {#coa-7-7}

- Traverse 2-D arrays in **row-major order** in C (consecutive addresses): one miss per block instead of one per access. Blocking/tiling reuses data while it is in the cache. Arrays beat linked lists (pointer chasing has no spatial locality).
- **False sharing:** two cores write different variables in the same cache line, so the line bounces between their caches. Fix: pad to separate lines.
- **Cache coherence** (multicore): every core must see the latest value. **Snooping** protocols like **MESI** (Modified, Exclusive, Shared, Invalid): a write invalidates other copies. Large systems use **directory-based** coherence.

<div class="nb nb-moral">

Address = tag | index | offset; offset = log₂(block), index = log₂(sets). AMAT = hit + miss rate × penalty. More associativity kills conflict misses; write-back + write-allocate saves memory traffic.

</div>
