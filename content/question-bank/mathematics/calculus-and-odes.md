---
title: "Calculus and ODEs"
weight: 4
---

4 questions asked by MathWorks, Texas Instruments. Try each one first, then open the toggle: it gives the answer, why it is right, and the idea behind it explained from scratch.

### 1 · Q15, integral over the real line

*Asked by: MathWorks (IISc 2024)*

An integral from $-\infty$ to $+\infty$ is:

- **(a)** definite
- **(b)** indefinite
- **(c)** none of these

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) definite** (an improper definite integral)

**Why.** It has limits (−∞ and +∞), so when it converges it gives a number. An indefinite integral has no limits and gives a family of functions (+ C).

**Concept: improper integrals.** An integral with an infinite limit is defined as a limit of ordinary definite integrals: ∫ from −∞ to ∞ = lim of ∫ from −a to b as a, b → ∞. It is still "definite" in kind.

{{< /details >}}

### 2 · Q17, a linear ODE

*Asked by: MathWorks (IISc 2024)*

The general solution of $\dfrac{dx}{dt} + 2x = 6$ is:

- **(a)** $Ce^{-2t} + 1$
- **(b)** $Ce^{-t} + 1$
- **(c)** $Ce^{-t} + 3$
- **(d)** $Ce^{-2t} + 3$

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) Ce⁻²ᵗ + 3**

**Why.** Homogeneous part: dx/dt + 2x = 0 gives x = Ce⁻²ᵗ. Particular solution: try a constant x = k, then 0 + 2k = 6, k = 3. General solution = Ce⁻²ᵗ + 3.

**Concept: first-order linear ODEs.** Solution = (solution of the equation with right side 0) + (any one particular solution). For a constant right side, try a constant. Check: as t → ∞, x → 3, the steady state where dx/dt = 0.

{{< /details >}}

### 3 · steady state of an ODE

*Asked by: Texas Instruments (IISc 2023); Texas Instruments (NIT Calicut 2023)*

$x'' + 6x' + 5x = 12(1 - e^{-2t})$ with zero initial conditions. $x(\infty)$?

{{< details title="Answer and explanation" closed="true" >}}

**Answer: x(∞) = 2.4**

**Why.** As t → ∞, the input 12(1 − e⁻²ᵗ) → 12, and the system settles (both roots of s² + 6s + 5 = 0 are negative: −1, −5), so x' and x'' → 0. Then 5x(∞) = 12, x(∞) = 2.4.

**Concept: steady state.** If a linear system is stable (all characteristic roots have negative real part), its output settles to a constant for a constant input. At steady state all derivatives are zero, so just solve the algebraic equation that remains (final value theorem).

{{< /details >}}

### 4 · rms and average of kx

*Asked by: Texas Instruments (NIT Calicut 2023)*

$x$ is periodic with rms $x_r$ and average $x_a$; $y = kx$. Which holds?

{{< details title="Answer and explanation" closed="true" >}}

**Answer: y_avg = k x_avg and y_rms = |k| x_rms**

**Why.** Average is linear: mean of kx = k × mean of x. RMS = √(mean of x²); for y = kx, mean of y² = k² × mean of x², so y_rms = |k| x_rms.

**Concept: average and RMS.** The average is a plain mean; the RMS (root mean square) squares values first, so it measures size regardless of sign. Scaling a signal by k scales both by k (the RMS by |k|, since it is never negative).

{{< /details >}}
