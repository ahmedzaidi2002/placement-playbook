---
title: "12 · Parallel and modern hardware"
linkTitle: "12 Parallel and modern hardware"
weight: 12
math: true
---
Since single cores stopped getting much faster ([Section 11.3](../11-perf/#sec-coa-power)), performance comes from parallelism at every level: several operations per instruction (SIMD), several threads per core, several cores per chip, thousands of lanes on a GPU. This chapter covers the taxonomy, the memory-consistency rules that make shared-memory programming subtle, GPUs at interview depth, NUMA, and what all of it means for code that has to be fast.

## 12.1 Flynn’s taxonomy and SIMD {#sec-coa-flynn}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> one `paddd` instruction adding four pairs of 32-bit integers.</em>

</div>

| Class | Meaning | Examples |
|:--|:--|:--|
| SISD | single instruction stream, single data stream | a classic scalar core |
| SIMD | one instruction applied to many data elements | vector units (SSE/AVX, ARM NEON/SVE), GPUs (as SIMT) |
| MISD | many instructions on one data stream | rare; sometimes cited for redundant fault-tolerant systems |
| MIMD | independent instruction streams on independent data | multicore processors, clusters |

<div class="nb-caption" id="table-12-1">

<strong>Table 12.1.</strong> Flynn’s taxonomy.

</div>

A <strong>SIMD</strong> (vector) instruction operates on a register holding several elements: $128$-bit SSE registers hold four 32-bit integers or floats, $256$-bit AVX registers eight. Compilers <strong>auto-vectorise</strong> simple loops:

```c {filename="simd-s.c"}
// flags: -O3 -masm=intel
// A plain loop; at -O3 gcc vectorises it with SSE2 (4 ints per instruction).
int sum(const int *a, int n) {
    int s = 0;
    for (int i = 0; i < n; i++) s += a[i];
    return s;
}
```

```text {filename="Assembly from gcc -S (gcc 13.3, -std=c11, x86-64 Linux, -O3 -masm=intel), the vector part"}
.L4:
    movdqu  xmm2, XMMWORD PTR [rax]
    add rax, 16
    paddd   xmm0, xmm2
    cmp rax, rdx
    jne .L4
    movdqa  xmm1, xmm0
    mov edx, esi
    psrldq  xmm1, 8
    and edx, -4
    paddd   xmm0, xmm1
    movdqa  xmm1, xmm0
    psrldq  xmm1, 4
    paddd   xmm0, xmm1
    movd    eax, xmm0
```

The loop body loads $16$ bytes (`movdqu`) and adds four integers at once (`paddd`); after the loop, two shift-and-add steps combine the four partial sums (a horizontal reduction), and a scalar tail (not shown) handles the last $n \bmod 4$ elements. Vectorisation needs independent iterations, contiguous data and no aliasing the compiler cannot rule out (`restrict` helps); a data-dependent branch or a pointer chase in the loop body usually prevents it.

<div class="nb nb-remark" id="remark-12-1-1">

<strong>Remark 12.1.1</strong> — Reordering a floating-point reduction changes the result ([Section 1.3](../01-data/#sec-coa-ieee)), so gcc vectorises float sums only with `-ffast-math` or `-fassociative-math`; integer sums, as here, are always safe.

</div>

## 12.2 Multicore and multithreading {#sec-coa-multicore}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> a 4-core chip whose cores share an L3 cache but keep private L1 and L2.</em>

</div>

<div class="nb nb-definition" id="definition-12-2-1">

<strong>Definition 12.2.1</strong>. A <strong>multicore</strong> processor has several cores on one chip, usually with private L1 (and L2) caches kept coherent ([Section 9.10](../09-memory/#sec-coa-coherence)) and a shared last-level cache. <strong>Hardware multithreading</strong> keeps several thread contexts in one core: fine-grained (switch every cycle), coarse-grained (switch on long stalls such as cache misses), or <strong>simultaneous multithreading</strong> (SMT, Intel’s Hyper-Threading: instructions from several threads issue in the same cycle into a superscalar core’s units). SMT hides latency and fills idle units; it does not double performance, because the threads share caches and execution units.

</div>

<div class="nb nb-definition" id="fact-12-2-2">

<strong>Fact 12.2.2</strong> (Shared memory vs message passing). Multicore chips are shared-memory multiprocessors: threads communicate through loads and stores, and hardware coherence keeps caches consistent. Clusters communicate by message passing (MPI, sockets), with no shared address space. In a <strong>NUMA</strong> (non-uniform memory access) machine, every socket has its own memory controller; any core can reach any memory, but remote memory is slower than local, so the OS tries to allocate a thread’s memory on its own node (first-touch placement) and to keep the thread there.

</div>

## 12.3 Memory consistency {#sec-coa-consistency}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> two threads each store to one variable and then load the other: on x86 both loads can return the old value.</em>

</div>

<div class="nb nb-definition" id="definition-12-3-1">

<strong>Definition 12.3.1</strong>. Coherence is about one location; the <strong>memory consistency model</strong> is about the order in which a core’s accesses to <em>different</em> locations become visible to other cores. <strong>Sequential consistency</strong> (SC): the result is as if all memory operations of all threads were interleaved in one order that respects each thread’s program order. <strong>Total store order</strong> (TSO, x86): like SC except that a store may be delayed in a <strong>store buffer</strong> while later loads (to other addresses) go ahead; a core always sees its own stores. ARM and POWER are weaker still: most reorderings are allowed unless a fence or an acquire/release instruction forbids them.

</div>

The test runs thread $T_0$ below and a mirror-image $T_1$ (`y = 1; r1 = x`) on two pinned cores for $200{,}000$ synchronised rounds, first without and then with a fence:

```c {filename="sb-litmus.c, lines 19–29",linenos=table,linenostart=19}
static void *t0(void *arg) {
    (void)arg; pin(0);
    for (int i = 0; i < RUNS; i++) {
        while (atomic_load(&go0) != i + 1) ;               /* wait for round i */
        atomic_store_explicit(&x, 1, memory_order_relaxed);
        if (fence) atomic_thread_fence(memory_order_seq_cst);   /* mfence */
        r0[i] = atomic_load_explicit(&y, memory_order_relaxed);
        atomic_store(&done0, i + 1);
    }
    return NULL;
}
```

```text {filename="Output (gcc 13.3, -std=c11, x86-64 Linux, -O2 -pthread; one run, counts vary)"}
without fences: r0 = r1 = 0 in 15925 of 200000 runs
with fences   : r0 = r1 = 0 in 0 of 200000 runs
```

<div class="nb nb-example nb-block" id="example-12-3-2">

<strong>Example 12.3.2</strong> (The store-buffer litmus test)

Under SC at least one thread’s store precedes the other’s load, so $r_0 = r_1 = 0$ is impossible. On this x86 machine it happened in thousands of the $200{,}000$ rounds: each core’s store waited in its store buffer while its load read the other variable from the cache. A full fence between the store and the load (`mfence`, which `atomic_thread_fence(memory_order_seq_cst)` compiles to) drains the store buffer first, and the outcome disappeared. This store-load reordering is exactly why Peterson’s and Dekker’s algorithms are incorrect on real hardware without fences (the OS book discusses the algorithms).

</div>

<div class="nb nb-definition" id="fact-12-3-3">

<strong>Fact 12.3.3</strong> (What programmers use). Nobody writes fences by hand in ordinary code: locks contain the necessary barriers, and C11/C++11 atomics express intent: `memory_order_release` on a store and `memory_order_acquire` on the load that reads it make everything written before the release visible after the acquire; `seq_cst` (the default) gives SC for the atomics. A data race on a plain variable is undefined behaviour in C and C++, whatever the hardware does. `volatile` is <em>not</em> a synchronisation primitive: it stops the compiler from removing accesses, but provides neither atomicity nor ordering between cores.

</div>

<div class="nb nb-moral">

Coherence makes every core agree on each location; consistency says how much the order of different locations can be scrambled. x86 reorders a store with a later load; fences and atomics put the order back.

</div>

## 12.4 GPUs {#sec-coa-gpu}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> 32 threads of a warp executing one instruction in lock step; an `if` that splits them runs both halves one after the other.</em>

</div>

<div class="nb nb-definition" id="definition-12-4-1">

<strong>Definition 12.4.1</strong>. A GPU runs thousands of lightweight threads, grouped (in NVIDIA’s terms) into <strong>warps</strong> of $32$ that execute the same instruction at the same time on different data: <strong>SIMT</strong> (single instruction, multiple threads). Warps are grouped into thread blocks that run on one streaming multiprocessor (SM) and can share its fast on-chip <strong>shared memory</strong>. Instead of large caches and branch prediction, a GPU hides memory latency by switching among many resident warps every cycle: while one waits for memory, another computes. This is why GPUs need very large amounts of parallel work to be efficient.

</div>

```text {filename="Output of gpu.py (Python 3.11)"}
 0 threads take A, 32 take B: warp time 20 cycles, lane utilisation 100%
 8 threads take A, 24 take B: warp time 30 cycles, lane utilisation 58%
16 threads take A, 16 take B: warp time 30 cycles, lane utilisation 50%
32 threads take A,  0 take B: warp time 10 cycles, lane utilisation 100%
stride  1:  1 transaction(s) of 128 B for 128 useful bytes (100% used)
stride  2:  2 transaction(s) of 128 B for 128 useful bytes (50% used)
stride  4:  4 transaction(s) of 128 B for 128 useful bytes (25% used)
stride 32: 32 transaction(s) of 128 B for 128 useful bytes (3% used)
```

<div class="nb nb-definition" id="fact-12-4-2">

<strong>Fact 12.4.2</strong> (Divergence and coalescing). When threads of a warp take different branches, the warp executes each path in turn with the other threads masked off (<strong>branch divergence</strong>): with $8$ threads on a $10$-cycle path and $24$ on a $20$-cycle one, the warp needs $30$ cycles and only $58\%$ of the lanes do useful work. Memory accesses of a warp are <strong>coalesced</strong> into as few transactions as possible when consecutive threads access consecutive addresses; with the model’s $128$-byte transactions, a stride of $1$ needs one transaction, a stride of $32$ needs $32$ and wastes $97\%$ of the bandwidth. (Transaction sizes differ between GPU generations; the principle does not.) That is why GPU code prefers structure-of-arrays layouts to arrays of structures.

</div>

## 12.5 What matters for fast and low-latency code {#sec-coa-lowlatency}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> a trading system whose critical path must stay in L1 and never mispredict a branch.</em>

</div>

The previous chapters reduce to a short checklist, which is also what interviewers at performance-minded firms want to hear:

- <strong>Cache lines.</strong> Lay data out contiguously and in access order; keep the hot working set small ([Section 9.8](../09-memory/#sec-coa-cachecode)); align and pad data written by different threads to separate lines (false sharing); prefer arrays and flat structures to pointer chasing.
- <strong>Branches.</strong> A misprediction costs a pipeline refill: the experiment below puts it on the order of ten nanoseconds (some twenty cycles) on this machine. Make branches predictable, or remove them (conditional moves, branch-free arithmetic, [Section 1.6](../01-data/#sec-coa-bits)), and sort data so that a data-dependent branch becomes predictable.
- <strong>Prefetching.</strong> Hardware prefetchers detect sequential and strided streams; random access defeats them. Software prefetch hints help only when the address is known well ahead of use.
- <strong>Memory ordering and atomics.</strong> Atomic read-modify-write operations and fences are typically tens of cycles each; contended cache lines cost far more (the false-sharing run in [Section 9.8](../09-memory/#sec-coa-cachecode)). Share less, batch more, use single-writer designs and per-core data.
- <strong>The OS.</strong> Pin threads to cores, avoid system calls and page faults on the hot path (pre-fault and lock memory, use huge pages to reduce TLB misses), and keep NUMA locality.
- <strong>Measure.</strong> Use hardware performance counters (cache misses, branch misses, IPC) with `perf`; intuition about performance is wrong often enough to be dangerous.

The branch experiment: the same loop, the same data, once in random order and once sorted (compiled at `-O0` so that the compiler keeps the branch):

```c {filename="branch-sort.c, lines 13–23",linenos=table,linenostart=13}
static double run(const unsigned char *d, long *sum) {
    struct timespec t0, t1;
    clock_gettime(CLOCK_MONOTONIC, &t0);
    long s = 0;
    for (int rep = 0; rep < 50; rep++)
        for (int i = 0; i < N; i++)
            if (d[i] >= 128) s += d[i];          /* taken about half the time */
    clock_gettime(CLOCK_MONOTONIC, &t1);
    *sum = s;
    return (t1.tv_sec - t0.tv_sec) * 1e3 + (t1.tv_nsec - t0.tv_nsec) * 1e-6;
}
```

```text {filename="Output (gcc 13.3, -std=c11, x86-64 Linux, -O0; one run)"}
same sum: yes
random order:  367.3 ms
sorted order:  138.9 ms
about 9.1 ns per misprediction
```

<div class="nb nb-moral">

Parallel hardware rewards independent work on contiguous data and punishes shared writes, unpredictable branches and pointer chasing, from SIMD lanes to GPU warps to multicore caches.

</div>
