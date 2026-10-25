---
title: "4 · Bias, variance and regularisation"
linkTitle: "4 Bias and variance"
weight: 4
math: true
---
Chapter 1 showed test error as a U-shape in model capacity. This chapter explains the U and gives you the dial that moves along it: a penalty $\lambda$ on the size of the weights. Nearly every "effect of $\lambda$" and "bagging versus boosting" question in an OA is this chapter in disguise.

## 4.1 The decomposition {#ml-4-1}

For squared loss, at a test point, averaged over training sets:

$$\mathbb{E}\big[(y - \hat f(x))^2\big] = \underbrace{\sigma^2}_{\text{noise}} + \underbrace{\big(f(x) - \mathbb{E}\hat f(x)\big)^2}_{\text{bias}^2} + \underbrace{\mathbb{E}\big(\hat f(x) - \mathbb{E}\hat f(x)\big)^2}_{\text{variance}}.$$

Think of an archer. **Noise** is wind you cannot control. **Bias** is a misaligned sight: the average arrow lands off-centre. **Variance** is a shaky hand: arrows scatter around their own average. A rigid model has a steady hand and a bad sight; a flexible one has a good sight and a shaky hand.

- **Underfitting = high bias:** bad on training data too.
- **Overfitting = high variance:** great on training data, much worse on new data.

## 4.2 What moves which term {#ml-4-2}

| Change | Bias | Variance |
|---|---|---|
| More training data (same model) | about the same | ↓ |
| More features, higher degree, deeper tree | ↓ | ↑ |
| Larger $\lambda$ (ridge, lasso, weight decay) | ↑ | ↓ |
| Larger $k$ in k-NN | ↑ | ↓ |
| Bagging / random forest | about the same | ↓ |
| Boosting | ↓ | ↑ slowly |
| Early stopping (fewer iterations) | ↑ | ↓ |

<div class="nb nb-remark">

<strong>Trap</strong> — "More data reduces bias." More data shrinks variance; it cannot fix a model class that cannot represent the truth (a line fitted to a parabola stays wrong with a billion points). This is the diagnostic: if **training** error is high, more data will not help; if the **gap** is large, it will.

</div>

## 4.3 Ridge (L2) {#ml-4-3}

$$\min_w \ \|y - Xw\|^2 + \lambda \|w\|_2^2 \qquad\Longrightarrow\qquad \hat w = (X^\top X + \lambda I)^{-1} X^\top y$$

The intercept is not penalised. $X^\top X + \lambda I$ is always invertible for $\lambda > 0$, so ridge has a unique solution even with duplicated features or more features than rows.

<div class="nb nb-example">

<strong>Example</strong> (Shrinking one slope)

Centred data with $\sum x_i y_i = 8$ and $\sum x_i^2 = 10$: $\hat w = 8/(10 + \lambda)$, i.e. $0.8$ at $\lambda = 0$, $0.4$ at $\lambda = 10$, $0.16$ at $\lambda = 40$. Weights shrink smoothly towards 0 but never reach it.

</div>

Ridge shrinks most along the low-variance directions of the data, where the estimate is noisiest. In Bayesian terms it is the **MAP estimate with a Gaussian prior** on the weights; large $\lambda$ means "I strongly believe the weights are small".

## 4.4 Lasso (L1) and elastic net {#ml-4-4}

$$\text{Lasso: } \min_w \tfrac{1}{2n}\|y - Xw\|^2 + \lambda\|w\|_1 \qquad \text{Elastic net: mix of } \|w\|_1 \text{ and } \|w\|_2^2.$$

**Lasso sets some weights exactly to zero**, so it selects features. Three explanations, any one is enough in an interview:

1. **Subgradient:** the derivative of $|w|$ at 0 is the whole interval $[-1, 1]$, so small coefficients are thresholded to exactly zero. Ridge's penalty $w^2$ has derivative 0 at 0 and only rescales.
2. **Geometry:** the L1 constraint region is a diamond with corners on the axes; the elliptical loss contours usually touch it at a corner, where some coordinates are 0. The L2 region is round and has no corners.
3. **Prior:** lasso is MAP under a **Laplace** prior, sharply peaked at zero.

<div class="nb nb-example">

<strong>Example</strong> (Soft versus proportional shrinkage)

With orthonormal features and OLS coefficients $(3, -1.2, 0.4, -0.1)$: lasso with threshold 0.5 gives $(2.5, -0.7, 0, 0)$, subtracting 0.5 and zeroing the small ones; ridge with $\lambda = 1$ gives $(1.5, -0.6, 0.2, -0.05)$, halving everything. Lasso shrinks by the same **amount**, ridge by the same **factor**.

</div>

**Elastic net** exists for correlated groups: lasso picks one of two near-copies arbitrarily and zeroes the other (and can flip between bootstrap samples); ridge splits the weight; elastic net is sparse across groups and shares within a group. Lasso also selects at most $n$ features when $d > n$; elastic net removes that limit.

<div class="nb nb-remark">

<strong>Trap</strong> — "Lasso's zero coefficients prove those features are irrelevant." A zeroed feature can be strongly predictive but redundant given a correlated one that was kept.

</div>

<div class="nb nb-remark">

<strong>Trap</strong> — Ridge and lasso are **not** scale-invariant: the penalty treats a feature in rupees and one in crores alike. Standardise first (also for SVM, k-NN and PCA). OLS and trees do not need it.

</div>

## 4.5 The effect of λ, the OA way {#ml-4-5}

The penalised objective $E_{\text{aug}}(w) = E_{\text{in}}(w) + \lambda\,\Omega(w)$ is data fit plus complexity. Answers to memorise:

- $\lambda = 0$: no regularisation, lowest training error, highest variance.
- $\lambda \to \infty$: weights go to 0, the model predicts a constant (the mean, since the intercept is not penalised): maximal bias, underfits.
- Increasing $\lambda$: **training error never decreases**; validation error usually falls then rises; weights shrink; the effective number of parameters drops.
- $\lambda$ is a hyperparameter chosen by validation or cross-validation, never on the training set (training error would always pick $\lambda = 0$).
- In neural networks the same penalty is **weight decay**: each step multiplies the weights by $(1 - 2\eta\lambda)$.

<div class="nb nb-remark">

<strong>Trap</strong> — Three plausible wrong options: "regularisation reduces training error" (it increases it), "large $\lambda$ causes overfitting" (it causes underfitting), "$\lambda$ is learnt by gradient descent with $w$" (then it would go to 0).

</div>

## 4.6 Early stopping and double descent {#ml-4-6}

**Early stopping** is implicit regularisation: gradient descent from small weights fits the strong directions first, so stopping after $t$ steps behaves like ridge with $\lambda \approx 1/(\eta t)$. Watch validation error and keep the best checkpoint.

**Double descent:** for interpolating models (minimum-norm least squares, large networks), test error peaks where the number of parameters just equals the number of points ($p \approx n$) and then **falls again** as parameters grow. "More parameters always means more overfitting" is false for such models, which is part of why huge neural networks generalise.

<div class="nb nb-moral">

Underfitting is bias, overfitting is variance. $\lambda$ is a bias dial: zero gives the raw fit, infinity gives a constant, validation finds the middle. L1 zeroes weights, L2 shrinks them.

</div>
