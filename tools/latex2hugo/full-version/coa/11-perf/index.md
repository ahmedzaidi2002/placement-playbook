---
title: "11 · Performance"
linkTitle: "11 Performance"
weight: 11
math: true
---
“Faster” means less execution time for a given program, and almost every performance question reduces to one equation. This chapter states it, computes CPI from an instruction mix, shows why MIPS misleads, and covers Amdahl’s and Gustafson’s laws and the power equation behind frequency scaling.

## 11.1 The iron law {#sec-coa-ironlaw}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> a 600 MHz processor with an instruction mix whose average CPI is $1.75$.</em>

</div>

<div class="nb nb-theorem nb-block" id="theorem-11-1-1">

<strong>Theorem 11.1.1</strong> (The iron law of performance)

$$
\text{CPU time} = \frac{\text{instructions}}{\text{program}} \times
	\frac{\text{cycles}}{\text{instruction}} \times \frac{\text{seconds}}{\text{cycle}}
	= \frac{\text{IC} \times \text{CPI}}{f}.
$$

The ISA and the compiler set the instruction count, the microarchitecture sets the CPI (pipelining, caches, prediction), and the circuit technology and the pipeline depth set the clock. Improving one term often worsens another.

</div>

<div class="nb nb-definition" id="definition-11-1-2">

<strong>Definition 11.1.2</strong>. With instruction classes of frequency $w_i$ and cycles $c_i$, the average $\text{CPI} = \sum_i w_i c_i$. <strong>MIPS</strong> (million instructions per second) $= f/(\text{CPI}\times 10^6)$; <strong>MFLOPS</strong> counts floating-point operations instead. Performance is $1/\text{time}$, and “$X$ is $n$ times faster than $Y$” means $\text{time}_Y/\text{time}_X = n$.

</div>

```text {filename="Output of perf.py (Python 3.11)"}
CPI = 1 x 0.45 + 3 x 0.2 + 2 x 0.1 + 2 x 0.25 = 1.75
MIPS = f / (CPI x 10^6) = 600 / 1.75 = 342.9; 10^9 instructions take 2.917 s
compiler A: IC 1.0e+09, CPI 2.0: time 3.333 s, MIPS 300
compiler B: IC 1.6e+09, CPI 1.5: time 4.000 s, MIPS 400
Amdahl, 80% sped up 4x: 2.50x; limit 1/0.2 = 5x
  95% parallel on    8 cores: Amdahl   5.93x, Gustafson (scaled)    7.65x
  95% parallel on   64 cores: Amdahl  15.42x, Gustafson (scaled)   60.85x
  95% parallel on 1024 cores: Amdahl  19.64x, Gustafson (scaled)  972.85x
to get 3x overall with p = 0.8 the part must speed up 6x
V and f x 0.9: power x 0.729, time x 1.111, energy per task x 0.810
V and f x 0.8: power x 0.512, time x 1.250, energy per task x 0.640
V and f x 0.5: power x 0.125, time x 2.000, energy per task x 0.250
speed-ups 2.0 and 0.5: arithmetic mean 1.25, geometric mean 1.00
```

<div class="nb nb-example nb-block" id="example-11-1-3">

<strong>Example 11.1.3</strong> (Average CPI and the MIPS trap)

The mix gives $\text{CPI} = 0.45 + 0.6 + 0.2 + 0.5 = 1.75$, so $600/1.75 = 342.9$ MIPS and $10^9$ instructions in $2.917$ s. Compiler B’s code has the better CPI and the higher MIPS rating ($400$ against $300$) but runs <em>slower</em> ($4.0$ against $3.3$ s) because it executes $60\%$ more instructions. MIPS ignores the instruction count, so it can only compare machines with the same ISA running the same binary; MFLOPS has the same flaw for different floating-point operation mixes. Only time is a reliable metric.

</div>

<div class="nb nb-definition" id="fact-11-1-4">

<strong>Fact 11.1.4</strong> (Benchmarks). Real programs are the only honest benchmark; standard suites (SPEC CPU for processors, others for specific domains) report each program’s speed-up over a reference machine and combine them with the <strong>geometric mean</strong>, which, unlike the arithmetic mean, gives the same ranking whichever machine is the reference: speed-ups of $2$ and $0.5$ average $1.25$ arithmetically, but the machine is no faster overall, as the geometric mean ($1.00$) says.

</div>

## 11.2 Amdahl’s law and Gustafson’s law {#sec-coa-amdahl}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> speeding up $80\%$ of a program four times gives only $2.5\times$ overall, and never more than $5\times$.</em>

</div>

<div class="nb nb-theorem nb-block" id="theorem-11-2-1">

<strong>Theorem 11.2.1</strong> (Amdahl’s law)

If a fraction $p$ of the execution time is sped up by a factor $s$, the overall speed-up is

$$
S = \frac{1}{(1-p) + p/s} \;\le \; \frac{1}{1-p}.
$$

On $n$ processors with parallel fraction $p$, $S(n) = 1/((1-p) + p/n)$.

</div>

<div class="nb nb-theorem nb-block" id="theorem-11-2-2">

<strong>Theorem 11.2.2</strong> (Gustafson’s law)

If the problem grows with the machine so that the parallel part takes the same time on $n$ processors as before, the <strong>scaled speed-up</strong> is $S(n) = (1-p) + p\,n$, where $p$ is the parallel fraction measured on the parallel machine.

</div>

The output above compares them for $p = 0.95$: Amdahl caps the speed-up at $20$ however many cores there are ($19.64$ on $1024$), Gustafson’s scaled speed-up keeps growing ($972.85$). Both are right; they answer different questions: Amdahl fixes the problem size (strong scaling), Gustafson fixes the time and lets the problem grow (weak scaling).

<div class="nb nb-remark" id="remark-11-2-3">

<strong>Remark 11.2.3</strong> (Amdahl in reverse) — “How much must the $80\%$ part be sped up to make the program $3\times$ faster?” Solve $1/(0.2 + 0.8/s) = 3$: $s = 6$. And to make it $5\times$ faster, $s$ would have to be infinite. The serial fraction decides what is possible; make the common case fast.

</div>

## 11.3 Power and energy {#sec-coa-power}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> lowering voltage and frequency by $20\%$ halves the power and saves a third of the energy of a task.</em>

</div>

<div class="nb nb-theorem nb-block" id="theorem-11-3-1">

<strong>Theorem 11.3.1</strong> (Dynamic power)

A CMOS gate dissipates power each time its output switches, charging or discharging its load capacitance:

$$
P_{\text{dynamic}} = \alpha \, C\, V^2 f,
$$

where $\alpha$ is the activity factor (fraction of the capacitance switched per cycle), $C$ the capacitance, $V$ the supply voltage and $f$ the clock frequency. Static (leakage) power flows whenever the circuit is powered and grows as transistors shrink and thresholds drop.

</div>

<div class="nb nb-definition" id="fact-11-3-2">

<strong>Fact 11.3.2</strong> (Dynamic voltage and frequency scaling). A lower $f$ allows a lower $V$, so scaling both by $k$ scales dynamic power by $k^3$ and, since the task takes $1/k$ as long, its dynamic energy by $k^2$ (output above: at $0.8$, power $\times 0.512$, energy $\times 0.64$). Lowering $f$ alone saves power but not energy. The other levers are $\alpha$ (clock gating stops the clock to idle blocks; data encodings with fewer toggles, [Section 1.7](../01-data/#sec-coa-lowpower)) and $C$ (smaller transistors and shorter wires).

</div>

<div class="nb nb-remark" id="remark-11-3-3">

<strong>Remark 11.3.3</strong> (Why clock frequencies stopped rising) — Around the mid-2000s supply voltages could no longer be lowered much (leakage grows as the threshold voltage drops), so higher frequencies meant more power per area than could be cooled: the <strong>power wall</strong>. Designers turned to more cores at moderate frequency ([Chapter 12](../12-parallel/)), which is exactly why Amdahl’s law became an everyday concern.

</div>

<div class="nb nb-moral">

Time is the only true metric: IC $\times$ CPI $/ f$. The serial fraction bounds what parallelism buys, and $V^2$ is why lowering voltage is the most effective way to save energy.

</div>
