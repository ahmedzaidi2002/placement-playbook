---
title: "Signals and systems"
weight: 4
---

3 questions asked by MathWorks, Texas Instruments. Try each one first, then open the toggle: it gives the answer, why it is right, and the idea behind it explained from scratch.

### 1 · Q13, filtered white noise

*Asked by: MathWorks (IISc 2024)*

Zero-mean white Gaussian noise is passed through an ideal low-pass filter of bandwidth
10 kHz and the output is sampled every $T_s = 0.03$ ms. The samples are:

- **(a)** correlated
- **(b)** statistically independent
- **(c)** uncorrelated
- **(d)** orthogonal

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) correlated**

**Why.** Ideal low-pass filtered white noise has autocorrelation R(τ) ∝ sinc(2Bτ), which is zero only at τ = k/(2B) = 0.05k ms for B = 10 kHz. 0.03 ms is not one of those lags, so neighbouring samples are correlated. (At T_s = 0.05 ms they would be uncorrelated, and being Gaussian, independent.)

**Concept: filtering creates correlation.** White noise is uncorrelated at every lag. A filter "smooths" it, so values close in time become similar. Sampling at exactly the Nyquist interval 1/(2B) lands on the zeros of the sinc.

{{< /details >}}

### 2 · cascade of LTI systems

*Asked by: Texas Instruments (NIT Calicut 2023)*

A cascade of three LTI systems is causal and unstable. What follows?

{{< details title="Answer and explanation" closed="true" >}}

**Answer (intended): at least one of the systems is unstable, and at least one is causal.** Strictly, nothing follows for certain (pole–zero cancellations can hide instability).

**Why.** If all three were stable, the cascade would be stable; so at least one is unstable. If none were causal, the cascade generally would not be causal. Exact cancellation can break both rules, which is why "strictly nothing" is the careful answer.

**Concept: cascading LTI systems.** The overall transfer function is the product H₁H₂H₃. Stability needs all poles of the product in the left half-plane (continuous time); causality relates to the region of convergence.

{{< /details >}}

### 3 · a pure delay block

*Asked by: Texas Instruments (NIT Calicut 2023)*

The input of an LTI system is first passed through $e^{-s}$. New output?

{{< details title="Answer and explanation" closed="true" >}}

**Answer: c(t − 1)** (the output delayed by one second)

**Why.** e^(−s) in the Laplace domain is a pure time delay of 1 s. For an LTI system, delaying the input delays the output by the same amount.

**Concept: time-shift property.** f(t − T) ↔ e^(−sT)F(s). Time invariance means the system responds the same way whenever the input arrives.

{{< /details >}}
