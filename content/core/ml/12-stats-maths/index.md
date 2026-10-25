---
title: "12 · Statistics and maths interviewers ask"
linkTitle: "12 Statistics and maths"
weight: 12
math: true
---
Data-science and many ML rounds spend ten minutes on classical statistics and a few maths facts: Bayes' rule with base rates, MLE versus MAP, convexity, a confidence interval, what a p-value is, which test to use. The answers are short; the follow-ups punish vague ones.

## 12.1 Probability you must have on call {#ml-12-1}

**Bayes' rule:** $P(A \mid B) = \dfrac{P(B \mid A)\,P(A)}{P(B)}$, i.e. posterior ∝ likelihood × prior.

<div class="nb nb-example">

<strong>Example</strong> (Base rates)

A disease has 1% prevalence; the test is 95% sensitive and 90% specific. $P(+) = 0.95\cdot 0.01 + 0.10\cdot 0.99 = 0.1085$, so $P(\text{disease} \mid +) = 0.0095/0.1085 = 0.088$. **Under 9%**: healthy people vastly outnumber sick ones. This is the precision problem of every rare-event classifier.

</div>

- **Expectation is always linear;** $\text{Var}(X + Y) = \text{Var}X + \text{Var}Y + 2\,\text{Cov}(X, Y)$; $\text{Var}(aX + b) = a^2\,\text{Var}X$.
- **Correlation** $r = \text{Cov}(X,Y)/(\sigma_X\sigma_Y) \in [-1, 1]$ is unit-free and measures **linear** association; covariance has units and changes with scale.
- **CLT:** the mean of $n$ i.i.d. draws is approximately normal with standard error $\sigma/\sqrt{n}$, whatever the original distribution. This is why confidence intervals and z-tests work.

<div class="nb nb-remark">

<strong>Trap</strong> — $r = 0$ does not mean independent: $y = x^2$ with $x$ symmetric around 0 has $r = 0$ and total dependence. Pearson's $r$ is sensitive to outliers; Spearman's (correlation of ranks) measures monotone association and is robust.

</div>

## 12.2 Information theory in four lines {#ml-12-2}

$$H(p) = -\sum p_i \log p_i, \qquad H(p, q) = -\sum p_i \log q_i = H(p) + \text{KL}(p\,\|\,q), \qquad \text{KL}(p\,\|\,q) = \sum p_i \log\frac{p_i}{q_i} \ge 0.$$

Minimising cross-entropy is minimising KL to the data distribution, because $H(p)$ does not depend on the model. **KL is not symmetric** and not a distance. Entropy reappears as a tree impurity (chapter 8).

## 12.3 MLE and MAP {#ml-12-3}

**Maximum likelihood** picks the parameters that make the data most probable; take logs because products of many small numbers underflow and the maximiser is unchanged. **MAP** adds a log-prior.

<div class="nb nb-example">

<strong>Example</strong> (A coin)

7 heads in 10: MLE $\hat p = 0.7$. With a Beta(3, 3) prior (two pseudo-heads, two pseudo-tails) the MAP is $(7+2)/(10+4) = 0.643$: the prior pulls towards 1/2, and the pull fades with more data. Laplace smoothing in naive Bayes is exactly this.

</div>

Three losses that are really likelihoods (an interview favourite):

- **Least squares** = MLE under Gaussian noise.
- **Ridge** = MAP with a Gaussian prior on the weights; **lasso** = MAP with a Laplace prior.
- **Cross-entropy / log-loss** = MLE of categorical labels.

<div class="nb nb-remark">

<strong>Trap</strong> — The MLE of a Gaussian variance divides by $n$ and is biased; the unbiased estimate divides by $n - 1$. For (4, 7, 5, 9, 5): mean 6, MLE variance 3.2, unbiased 4.0. NumPy's `var` defaults to $n$; pandas to $n - 1$.

</div>

## 12.4 Convexity {#ml-12-4}

A function is **convex** if the chord between any two points lies on or above the graph. For a convex function every local minimum is global, which is why convex losses are pleasant to train.

- Convex: $x^2$, $|x|$ (not differentiable at 0, still convex), $e^x$, $-\log x$, norms, $\max_i x_i$, log-sum-exp.
- Not convex: $\sin x$ on $\mathbb R$ (the chord from 0 to $\pi$ lies below it), $x^3$ on $\mathbb R$, $\min$ of convex functions.
- **Max of convex functions is convex; min is not**; sums with non-negative weights and composition with an affine map preserve convexity.

<div class="nb nb-remark">

<strong>Trap</strong> — "A convex loss makes the training objective convex." Only if the model is linear in its parameters. Log-loss is convex in the logits, but a neural network's loss is non-convex in its weights.

</div>

**Lagrange multipliers and KKT** in one line: at a constrained optimum, a constraint either binds or its multiplier is zero (**complementary slackness**). That is exactly why only the support vectors have non-zero $\alpha$ in an SVM.

## 12.5 Optimisation facts for follow-ups {#ml-12-5}

- **Gradient descent** on a quadratic converges only for step sizes below $2/\lambda_{\max}$, and its speed depends on the **condition number** $\kappa = \lambda_{\max}/\lambda_{\min}$: long thin valleys make it zig-zag. Standardising features reduces $\kappa$.
- **Momentum** averages gradients over time: oscillating components cancel, consistent ones accumulate; iterations scale with $\sqrt{\kappa}$ instead of $\kappa$.
- **Newton's method** uses curvature and jumps to the minimum of a quadratic in one step; quadratic convergence near the optimum, but $O(d^3)$ per step. **L-BFGS** approximates it cheaply (scikit-learn's logistic regression default).
- **SGD** uses one example or a mini-batch: cheap, noisy, and with a constant step it hovers in a noise ball around the optimum, so the step must **decay**.
- **Coordinate descent** shines when each one-dimensional problem has a closed form (the lasso).

## 12.6 Distributions {#ml-12-6}

| Distribution | Mean | Variance | Typical question |
|---|---|---|---|
| Bernoulli($p$) | $p$ | $p(1-p)$ | one click |
| Binomial($n, p$) | $np$ | $np(1-p)$ | $P(X = 3)$, $n = 10$, $p = 0.2$: $\binom{10}{3}0.2^3 0.8^7 = 0.201$ |
| Geometric($p$) | $1/p$ | $(1-p)/p^2$ | trials until the first success |
| Poisson($\lambda$) | $\lambda$ | $\lambda$ | calls per minute; $P(X=0) = e^{-\lambda}$ |
| Exponential($\lambda$) | $1/\lambda$ | $1/\lambda^2$ | waiting time; **memoryless** |
| Normal($\mu, \sigma^2$) | $\mu$ | $\sigma^2$ | 68–95–99.7 rule; $P(\lvert Z\rvert < 1.96) = 0.95$ |

## 12.7 Confidence intervals and hypothesis tests {#ml-12-7}

A **95% confidence interval** comes from a procedure that covers the true value in 95% of repeated samples. For a mean with unknown $\sigma$: $\bar x \pm t_{0.975,\,n-1}\, s/\sqrt{n}$ (use $t$, not 1.96, for small $n$). For statistics without a formula (a median, AUC) use the **bootstrap**.

<div class="nb nb-remark">

<strong>Trap</strong> — "There is a 95% probability the true mean is in this interval" is the classic wrong reading: the parameter is fixed; the 95% describes the procedure.

</div>

**The vocabulary.** Null hypothesis $H_0$ (no effect) versus the alternative. The **p-value** is the probability, *assuming $H_0$ is true*, of data at least as extreme as observed. Reject if $p < \alpha$.

| | $H_0$ true | $H_0$ false |
|---|---|---|
| Reject | **Type I error** (rate $\alpha$), false positive | correct (power $1 - \beta$) |
| Do not reject | correct | **Type II error** (rate $\beta$), false negative |

<div class="nb nb-remark">

<strong>Trap</strong> — A p-value is **not** the probability that $H_0$ is true, not "the probability the result is due to chance", and not an effect size. With huge $n$, $p = 0.03$ can be a negligible effect; "not significant" is not "no effect". Fix $\alpha$ in advance and do not stop an A/B test the moment $p$ dips below 0.05 (peeking inflates Type I error).

</div>

**Which test:**

| Situation | Test |
|---|---|
| Mean vs a value, $\sigma$ known or $n$ large | z-test |
| Mean vs a value, $\sigma$ unknown | one-sample t |
| Two independent groups' means | two-sample (Welch) t |
| Same units measured twice (before/after) | **paired** t: removes between-unit variation |
| Two categorical variables related? / a die fair? | $\chi^2$ test of independence / goodness of fit |
| Means of 3+ groups | one-way ANOVA (F-test), then post-hoc tests |
| Normality doubtful, small $n$ | Mann–Whitney, Wilcoxon signed-rank |

<div class="nb nb-example">

<strong>Example</strong> (z-test)

Mean load time should be 50 ms; 64 requests average 52 ms with known $\sigma = 8$: $z = (52 - 50)/(8/\sqrt{64}) = 2.0$, two-sided $p = 0.046$. Reject at 5%.

</div>

**A/B test sample size** grows with the inverse square of the effect: detecting a lift from 10% to 12% at $\alpha = 0.05$ and power 0.8 needs about 3,840 users per arm; **halving** the detectable lift roughly **quadruples** $n$.

## 12.8 Multiple testing, causation, Simpson {#ml-12-8}

- **Twenty tests at 5%** with all nulls true give $1 - 0.95^{20} \approx 64\%$ chance of at least one false positive. **Bonferroni** tests each at $\alpha/m$ (conservative); **Benjamini–Hochberg** controls the false discovery rate. The same logic applies to trying many models or features on one validation set.
- **Correlation is not causation:** confounders (ice-cream sales and drownings both follow summer), reverse causation, selection effects. A feature can be predictive without being a lever you can pull.
- **Simpson's paradox:** a treatment better in every subgroup can look worse overall because of who received it. In the kidney-stone data, treatment A wins for small and large stones separately (0.93 vs 0.87, 0.73 vs 0.69) yet loses overall (0.78 vs 0.83), because A was given mostly to the harder cases.

<div class="nb nb-moral">

State $H_0$, pick the test that matches the data's structure (paired? proportions? counts?), report an effect size and interval alongside $p$, and correct for how many things you tested.

</div>
