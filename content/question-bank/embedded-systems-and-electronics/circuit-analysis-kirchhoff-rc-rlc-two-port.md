---
title: "Circuit analysis (Kirchhoff, RC/RLC, two-port)"
weight: 3
---

17 questions asked by Qualcomm, Texas Instruments. Try each one first, then open the toggle: it gives the answer, why it is right, and the idea behind it explained from scratch.

### 1 · Circuits and signals

*Asked by: Qualcomm (BITS Goa 2024, Q59)*

Three resistors of 6 kΩ each and three capacitors of 6 F each are all connected in parallel. What are the effective resistance and capacitance?

- **(a)** 2 kΩ and 2 F
- **(b)** 18 kΩ and 18 F
- **(c)** 18 kΩ and 2 F
- **(d)** 2 kΩ and 18 F

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) 2 kΩ and 18 F**

**Why.** Three equal resistors in parallel: 6 k/3 = 2 kΩ. Capacitors in parallel add: 3 × 6 = 18 F.

**Concept: series vs parallel rules are opposite for R and C.** Resistors: series add, parallel combine as 1/R = Σ1/Rᵢ. Capacitors: parallel add, series combine as 1/C = Σ1/Cᵢ.

{{< /details >}}

### 2 · Circuits and signals

*Asked by: Qualcomm (BITS Goa 2024, Q56)*

A 15 Ω resistor in series with an inductor carries i(t) = 2 + 3 sin(100t + 30°) + 5 sin(…t + 30°) A. Find the RMS current and the power consumed.

- **(a)** √10 A and 315 W
- **(b)** √21 A and 215 W
- **(c)** √15 A and 300 W
- **(d)** √21 A and 315 W

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) √21 A and 315 W**

**Why.** For a sum of a DC term and sinusoids at different frequencies, I²_rms = I₀² + Σ(Iₚₖ²/2) = 4 + 9/2 + 25/2 = 21, so I_rms = √21 A. Only the resistor dissipates power: P = I²_rms R = 21 × 15 = 315 W.

**Concept: RMS of combined signals.** Components at different frequencies are "orthogonal", so their mean squares add. A sine of peak A has RMS A/√2; DC has RMS equal to its value. Inductors and capacitors store and return energy but dissipate none.

{{< /details >}}

### 3 · Circuits and signals

*Asked by: Qualcomm (BITS Hyderabad 2024, Q51)*

A 1 MΩ resistor is connected to a capacitor C. The capacitor voltage drops by 65% in 6.5 s. What is C?

- **(a)** 6.5 µF
- **(b)** 6.2 µF
- **(c)** 1 µF
- **(d)** 15 µF

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) 6.2 µF**

**Why.** After a 65% drop, 35% remains: 0.35 = e^(−t/RC). So RC = 6.5/ln(1/0.35) = 6.5/1.05 ≈ 6.19 s, and C = 6.19 s / 1 MΩ ≈ 6.2 µF.

**Concept: RC discharge.** V(t) = V₀ e^(−t/τ) with τ = RC. After one τ, 37% remains; after 5τ, under 1%.

{{< /details >}}

### 4 · Circuits and signals

*Asked by: Qualcomm (Delhi campus 2024, Q58)*

In voltage measurement, determine the RMS value of the voltage if the peak-to-peak voltage is 6 V.

- **(a)** 2.12 V
- **(b)** 4.14 V
- **(c)** 3.13 V
- **(d)** 1.11 V

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) 2.12 V**

**Why.** Peak-to-peak 6 V → peak 3 V. For a sine wave, RMS = peak/√2 = 3/1.414 ≈ 2.12 V.

**Concept: RMS.** The DC value that would deliver the same power into a resistor. Sine: peak/√2; square wave: peak; triangle: peak/√3.

{{< /details >}}

### 5 · Circuits and signals

*Asked by: Qualcomm (2025 paper (campus not named), Q53)*

How many RC pairs are used in a second-order op-amp low-pass filter?

- **(a)** 8
- **(b)** 1
- **(c)** 4
- **(d)** 2

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) 2**

**Why.** Each RC section contributes one pole; a second-order low-pass (e.g. Sallen–Key) uses two RC pairs around the op-amp.

**Concept: filter order.** An n-th order filter has n poles and rolls off at 20n dB/decade beyond its cutoff. Higher order = sharper transition.

{{< /details >}}

### 6 · Circuits and signals

*Asked by: Qualcomm (IIIT Delhi 2025, Q56)*

Which among the following is the power spectral density (PSD) of Brownian noise?

- **(a)** 1/f
- **(b)** 1
- **(c)** 1/f²
- **(d)** 1/f³

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) 1/f²**

**Why.** Brownian (red) noise is integrated white noise. Integration divides the amplitude spectrum by f, so the power spectrum falls as 1/f². White noise is flat; pink noise is 1/f.

**Concept: coloured noise.** Named by how power density depends on frequency: white (flat), pink (1/f, equal power per octave), Brownian/red (1/f², a random walk).

{{< /details >}}

### 7 · Circuits and signals

*Asked by: Qualcomm (2025 paper (campus not named), Q60)*

Identify the type of relay shown.

<figure class="nb-fig"><img src="/companies/qualcomm/core/relay.svg" alt="Figure for question 7" loading="lazy"></figure>

- **(a)** SPST
- **(b)** DPDT
- **(c)** DPST
- **(d)** SPDT

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) SPST**

**Why.** The figure shows one moving contact (single pole) that closes onto one fixed contact (single throw).

**Concept: switch/relay naming.** Pole = number of separate circuits switched; throw = number of positions each pole can connect to. SPST (simple on/off), SPDT (changeover), DPDT (two changeovers, e.g. for reversing a motor).

{{< /details >}}

### 8 · charge sharing

*Asked by: Texas Instruments (NIT Calicut 2023)*

$C_1 = 3\,\mu$F at 10 V is connected through 5 k$\Omega$ to an uncharged $C_2 = 1\,\mu$F. Final
voltages?

{{< details title="Answer and explanation" closed="true" >}}

**Answer: both end at 7.5 V**

**Why.** Charge is conserved when the capacitors connect: Q = 3 µF × 10 V = 30 µC, shared over 3 + 1 = 4 µF → 30/4 = 7.5 V. The resistor only sets how fast they settle (and dissipates some energy).

**Concept: charge sharing.** Connected capacitors end at a common voltage V = (C₁V₁ + C₂V₂)/(C₁ + C₂). Energy is lost (here 150 µJ → 112.5 µJ) in the resistor, whatever its value.

{{< /details >}}

### 9 · input resistance

*Asked by: Texas Instruments (NIT Calicut 2023)*

Five 60 $\Omega$ resistors form a bridge (T plus two shunts). Input resistance seen by the 9 V
source?

- **(a)** 270
- **(b)** 180
- **(c)** 120
- **(d)** 60

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) 60 Ω**

**Why.** Solving the network with nodal analysis gives an equivalent resistance of 60 Ω. (In a balanced bridge no current flows through the middle branch, which simplifies it.)

**Concept: bridges and nodal analysis.** When series/parallel reduction doesn't apply, write KCL at each node and solve. A balanced bridge (equal ratios on both sides) lets you remove the middle resistor.

{{< /details >}}

### 10 · Kirchhoff's laws

*Asked by: Texas Instruments (IISc 2023)*

Which statement about Kirchhoff's laws is correct?

{{< details title="Answer and explanation" closed="true" >}}

**Answer: as photographed, every option swaps KVL and KCL.** The facts: KCL is used for nodal analysis and KVL for mesh analysis.

**Why.** KCL: currents into a node add to zero (charge is conserved). KVL: voltages around any closed loop add to zero (energy is conserved).

**Concept: node vs mesh analysis.** Nodal analysis writes KCL at each node with node voltages as unknowns; mesh analysis writes KVL around each loop with loop currents as unknowns.

{{< /details >}}

### 11 · maximum power into a resistor

*Asked by: Texas Instruments (NIT Calicut 2023)*

A source with internal impedance $5 + j12\ \Omega$ feeds a purely resistive load. $R_L$ for
maximum power?

- **(a)** 2
- **(b)** 3
- **(c)** 4
- **(d)** 13

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) 13 Ω**

**Why.** For a purely resistive load, maximum power transfer occurs when R_L = |Z_s| = √(5² + 12²) = 13 Ω. (A complex load would instead be the conjugate, 5 − j12.)

**Concept: maximum power transfer.** Resistive source: R_L = R_s. Complex source with a complex load: Z_L = Z_s* (conjugate). Resistive load only: R_L = |Z_s|.

{{< /details >}}

### 12 · a switched RC network

*Asked by: Texas Instruments (NIT Calicut 2023)*

1 V charges 1 $\mu$F through 5 k from $t = 0$; S3 opens at 2.5 ms; S2 closes at 3 ms,
connecting a 1 k load (out2). When does out2 reach 0.2 V?

- **(a)** 2.67 ms
- **(b)** 3.67 ms
- **(c)** 4.67 ms
- **(d)** 5.12 ms

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) 3.67 ms**

**Why.** Charging through 5 k with 1 µF gives τ = 5 ms. At 2.5 ms: V_C = 1 − e^(−0.5) = 0.393 V; with S3 open, this is held until 3 ms. Then it discharges into 1 k with τ = 1 ms: 0.393 e^(−(t−3)/1) = 0.2 → t = 3 + ln(0.393/0.2) ≈ 3.67 ms.

**Concept: piecewise RC transients.** Each switching event starts a new exponential from the voltage at that moment, with the new circuit's time constant.

{{< /details >}}

### 13 · series RLC at 40 MHz

*Asked by: Texas Instruments (NIT Calicut 2023)*

A series RLC resonates at 40 MHz. Which follows?

- **(a)** At 40 MHz the impedance is R
- **(b)** Below 40 MHz it is inductive
- **(c)** Above 40 MHz it is capacitive
- **(d)** All

{{< details title="Answer and explanation" closed="true" >}}

**Answer: only (a)** (at resonance the impedance is R)

**Why.** At resonance X_L = X_C, so they cancel and Z = R. Below resonance the capacitor's reactance (1/ωC) is larger, so the circuit is capacitive; above it the inductor's (ωL) is larger, so inductive. (b) and (c) are reversed.

**Concept: series resonance.** ω₀ = 1/√(LC). The current is largest and in phase with the voltage there. Quality factor Q = ω₀L/R measures how sharp the peak is.

{{< /details >}}

### 14 · current in phase

*Asked by: Texas Instruments (NIT Calicut 2023)*

$R = 10\ \Omega$, $L = 1$ mH, $C = 10\,\mu$F. For which $\omega$ is the current $I\sin\omega t$
(in phase)?

{{< details title="Answer and explanation" closed="true" >}}

**Answer: ω = 10,000 rad/s**

**Why.** The current is in phase with the voltage at resonance: ω = 1/√(LC) = 1/√(10⁻³ × 10⁻⁵) = 1/√(10⁻⁸) = 10⁴ rad/s.

**Concept: resonance** (see above): reactances cancel and the circuit looks purely resistive.

{{< /details >}}

### 15 · rms current

*Asked by: Texas Instruments (NIT Calicut 2023)*

A source $1\sin t$ V in series with 1 $\Omega$ feeds 1 $\Omega$ in parallel with a series 1 F
capacitor and 1 H inductor. The rms value of $i(t)$?

- **(a)** 1/2 A
- **(b)** $1/\sqrt2$ A
- **(c)** 1 A
- **(d)** 2 A

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) 1/√2 A**

**Why.** At ω = 1 rad/s the series L–C branch has impedance j(ωL − 1/ωC) = j(1 − 1) = 0: a short circuit across the parallel 1 Ω. The source then sees only the series 1 Ω, so i = sin t A, with RMS 1/√2 A.

**Concept: series LC at resonance is a short.** (A parallel LC at resonance is an open circuit.) Check for resonance before doing complex algebra.

{{< /details >}}

### 16 · superposition

*Asked by: Texas Instruments (NIT Calicut 2023)*

Superposition applies to which network?

{{< details title="Answer and explanation" closed="true" >}}

**Answer: linear bilateral networks**

**Why.** Superposition (total response = sum of responses to each source alone) holds only for linear elements. "Bilateral" means elements behave the same for both current directions (R, L, C).

**Concept: superposition.** Turn on one source at a time (voltage sources shorted, current sources opened), solve, and add. It doesn't apply to power (which is quadratic) or to non-linear parts like diodes.

{{< /details >}}

### 17 · two-port Z parameters

*Asked by: Texas Instruments (IISc 2023)*

$i_1 = 2V_1 + V_2$, $i_2 = V_1 + V_2$. Find $Z_{12}$.

{{< details title="Answer and explanation" closed="true" >}}

**Answer: Z₁₂ = −1 Ω**

**Why.** The equations give the admittance matrix Y = [[2, 1], [1, 1]]. Z = Y⁻¹. det Y = 2 − 1 = 1, so Z = [[1, −1], [−1, 2]], and Z₁₂ = −1.

**Concept: two-port parameters.** Z-parameters give voltages from currents (V = ZI); Y-parameters give currents from voltages (I = YV). They are inverses of each other: Z = Y⁻¹.

{{< /details >}}
