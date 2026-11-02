---
title: "Probability and statistics"
weight: 2
---

7 questions asked by Info Edge. Try each one first, then open the toggle: it gives the answer, why it is right, and the idea behind it explained from scratch.

### 1 · Q1, countable values

*Asked by: Info Edge (Data Science II)*

A random variable that assumes a finite or a countably infinite number of values is called:

- **(a)** Continuous random variable
- **(b)** Discrete random variable
- **(c)** Irregular random variable
- **(d)** Regular random variable

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) discrete random variable** (the photo ticks (a))

**Why.** A discrete random variable takes a finite or countable list of values (like 0, 1, 2, ...). A continuous one takes any value in an interval (uncountably many).

**Concept: discrete vs continuous.** Discrete: counts (number of heads), described by a probability mass function. Continuous: measurements (height), described by a density, where any single exact value has probability 0.

{{< /details >}}

### 2 · Q3, hypothesis tested for rejection

*Asked by: Info Edge (Data Science II)*

The assumed hypothesis that is tested for rejection while considering it to be true is called:

- **(a)** Simple Hypothesis
- **(b)** Statistical Hypothesis
- **(c)** Null Hypothesis
- **(d)** Alternate Hypothesis

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) null hypothesis**

**Why.** The null hypothesis H₀ is the default claim (no effect, no difference) that we assume true and try to reject with data.

**Concept: hypothesis testing.** Assume H₀, compute how surprising the data would be (the p-value). If it is very surprising, reject H₀ in favour of the alternative H₁. Failing to reject is not proving H₀.

{{< /details >}}

### 3 · Q4, sum of normals

*Asked by: Info Edge (Data Science II)*

$X$ and $Y$ are independent normally distributed random variables. The distribution of their
sum is:

- **(a)** Exponential
- **(b)** Gaussian
- **(c)** Gamma
- **(d)** t-Distribution

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) Gaussian**

**Why.** The sum of independent normal variables is normal, with mean μ_X + μ_Y and variance σ²_X + σ²_Y.

**Concept: normal distributions are closed under addition.** Means add, and for independent variables variances add (standard deviations do not).

{{< /details >}}

### 4 · Q5, chi-square for a die

*Asked by: Info Edge (Data Science II)*

Rolling a die 300 times gives 54 ones, 46 twos, 54 threes, 46 fours, 50 fives and 56 sixes.
To test whether the die is fair, what is the goodness-of-fit test statistic?

- **(a)** 7.8
- **(b)** 3.6
- **(c)** 10.1
- **(d)** 2

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) 2**

**Why.** A fair die gives an expected 300/6 = 50 per face. χ² = Σ (O − E)²/E = (16 + 16 + 16 + 16 + 0 + 36)/50 = 100/50 = 2.

**Concept: chi-square goodness of fit.** It measures how far observed counts are from expected ones, scaled by the expected count. Small values mean the data fit; compare with a χ² table (here 5 degrees of freedom) to decide.

{{< /details >}}

### 5 · Q6, typical significance level

*Asked by: Info Edge (Data Science II)*

What is a typical p-value for which a statistical test may be significant?

- **(a)** > 0.95
- **(b)** < 0.05
- **(c)** > 0.5
- **(d)** < 0.25

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) p < 0.05**

**Why.** By convention a result is called significant if p < 0.05, i.e. data this extreme would happen less than 5% of the time if H₀ were true.

**Concept: p-value.** The probability, assuming H₀, of getting data at least as extreme as observed. Smaller p = stronger evidence against H₀. The 5% threshold is a convention, not a law.

{{< /details >}}

### 6 · Q7, left-skewed distribution

*Asked by: Info Edge (Data Science II)*

If a distribution is left skewed, then:

- **(a)** mean < median < mode
- **(b)** mode < median < mean
- **(c)** mean < mode < median
- **(d)** median < mode < mean

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) mean < median < mode**

**Why.** A left-skewed distribution has a long tail of small values. Those few extreme low values pull the mean down most; the median is less affected; the mode sits at the peak, on the right.

**Concept: skewness.** The mean follows the tail. Right (positive) skew: mode < median < mean. Left (negative) skew: mean < median < mode.

{{< /details >}}

### 7 · Q8, shifting variables

*Asked by: Info Edge (Data Science II)*

The Pearson correlation coefficients of $(X, Y)$, $(Y, Z)$ and $(X, Z)$ are $C_1, C_2, C_3$.
You add 2 to every value of $X$, subtract 2 from every value of $Y$, and leave $Z$ unchanged;
the new coefficients are $D_1, D_2, D_3$. How do they relate?

- **(a)** D1 = C1, D2 < C2, D3 > C3
- **(b)** D1 = C1, D2 > C2, D3 > C3
- **(c)** D1 = C1, D2 > C2, D3 < C3
- **(d)** D1 = C1, D2 < C2, D3 < C3
- **(e)** D1 = C1, D2 = C2, D3 = C3

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (e) all unchanged**

**Why.** Pearson correlation uses each variable's deviations from its own mean. Adding or subtracting a constant shifts every value and its mean equally, so the deviations, and the correlation, stay the same.

**Concept: correlation is shift- and scale-invariant.** r(aX + b, cY + d) = r(X, Y) when a and c are both positive (the sign flips if one is negative). It measures linear association, not location or units.

{{< /details >}}
