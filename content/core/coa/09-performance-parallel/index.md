---
title: "9 · Performance and parallel hardware"
linkTitle: "9 Performance and parallelism"
weight: 9
math: true
---
## 9.1 The iron law of performance {#coa-9-1}

<div class="nb nb-theorem nb-block">

<strong>CPU time</strong>

$$\text{CPU time} = \text{instruction count} \times \text{CPI} \times \text{clock period} = \frac{\text{instructions} \times \text{CPI}}{\text{clock rate}}.$$

$\text{MIPS} = \dfrac{\text{clock rate}}{\text{CPI} \times 10^6}$.

</div>

<div class="nb nb-example">

<strong>Example</strong> (Average CPI)

Mix: 50% ALU (1 cycle), 20% loads (3), 20% stores (2), 10% branches (2). $\text{CPI} = 0.5 + 0.6 + 0.4 + 0.2 = $ **1.7**. At 1 GHz: $\text{MIPS} = 1000/1.7 \approx 588$; $10^9$ instructions take **1.7 s**.

</div>

<div class="nb nb-remark">

<strong>Trap: MIPS</strong> — a higher MIPS rating does not mean a faster program: a compiler that uses more, simpler instructions raises MIPS while the program takes longer. Compare **execution time**. Average speed-ups over several programs with the **geometric mean**.

</div>

## 9.2 Amdahl's and Gustafson's laws {#coa-9-2}

<div class="nb nb-theorem nb-block">

<strong>Amdahl's law</strong>

If a fraction $p$ of the time is sped up by a factor $s$:

$$\text{Speed-up} = \frac{1}{(1 - p) + p/s} \ \le\ \frac{1}{1 - p}.$$

</div>

<div class="nb nb-example">

<strong>Example</strong> (Amdahl)

80% of a program parallelises perfectly. On 4 cores: $1/(0.2 + 0.8/4) = 1/0.4 = $ **2.5×**. With infinitely many cores: $1/0.2 = $ **5×**, never more. The serial 20% caps everything.

</div>

**Gustafson's law:** if the problem grows with the number of processors (so the parallel part keeps them all busy), the scaled speed-up is $(1 - p) + p \cdot n$: nearly linear. Amdahl answers "same problem, faster?"; Gustafson answers "bigger problem, same time?".

## 9.3 Power {#coa-9-3}

Dynamic power of CMOS: $P = \alpha\, C\, V^2 f$ (activity factor, capacitance, voltage squared, frequency). Lowering the voltage by 10% cuts dynamic power to $0.81\times$; that is why clock speeds stopped rising around 2005 (the **power wall**) and chips went multicore. **DVFS** (dynamic voltage and frequency scaling) lowers $V$ and $f$ when full speed is not needed.

## 9.4 Flynn's taxonomy {#coa-9-4}

| Class | Meaning | Example |
|---|---|---|
| **SISD** | single instruction, single data | a classic single-core CPU |
| **SIMD** | single instruction, multiple data | vector units (SSE, AVX), GPUs (roughly) |
| **MISD** | multiple instructions, single data | rare (fault-tolerant systems) |
| **MIMD** | multiple instructions, multiple data | multicore CPUs, clusters |

## 9.5 Multicore, threads and GPUs {#coa-9-5}

- **Multicore:** several cores on one chip, each with private L1/L2 and a shared L3; caches kept consistent by a coherence protocol (MESI, chapter 7).
- **Hardware multithreading:** one core keeps several thread contexts. **Fine-grained** switches every cycle; **coarse-grained** switches on long stalls; **simultaneous multithreading (SMT, Hyper-Threading)** issues instructions from several threads in the same cycle.
- **Shared-memory** (UMA: equal access time; NUMA: memory closer to some cores is faster) vs **distributed-memory** (message passing between nodes).
- **Memory consistency:** sequential consistency is the intuitive model; real CPUs reorder memory operations (x86 lets a later load pass an earlier store), so concurrent code needs fences or atomics.
- **GPUs:** thousands of simple cores running the same instruction on many data items (SIMT, warps of 32 threads); great for regular data-parallel work (graphics, matrix multiplication, deep learning), poor for branchy serial code.

## 9.6 Embedded systems, briefly {#coa-9-6}

- Device registers are accessed through pointers declared **`volatile`**, so the compiler re-reads them every time instead of caching the value.
- An ISR and the main loop that share a multi-byte variable can see a **torn read** (half old, half new) on a small CPU; disable interrupts around the read or use atomic types.
- A **watchdog timer** resets the system if the software stops "kicking" it; **timers** generate periodic interrupts and PWM.

<div class="nb nb-moral">

CPU time = instructions × CPI / clock rate; compare execution time, not MIPS. Amdahl: speed-up ≤ 1/(serial fraction). Power ∝ V²f, which is why we got multicore.

</div>
