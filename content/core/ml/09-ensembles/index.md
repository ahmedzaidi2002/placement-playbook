---
title: "9 · Ensembles: bagging, random forests, boosting"
linkTitle: "9 Ensembles"
weight: 9
math: true
---
If an OA has one classical-ML question beyond linear models, it is usually here: the 63.2% bootstrap number, "bagging reduces variance, boosting reduces bias", "which is true of random forests", or a feature-importance trap. Interviews add AdaBoost's weight, gradient boosting as gradient descent, and XGBoost's leaf formula.

## 9.1 The bootstrap and 63.2% {#ml-9-1}

A **bootstrap sample** draws $n$ rows with replacement from $n$. A given row is missed by all $n$ draws with probability $(1 - 1/n)^n$, so

$$P(\text{row appears}) = 1 - \Big(1 - \frac{1}{n}\Big)^n \ \xrightarrow{\ n\to\infty\ }\ 1 - e^{-1} \approx 0.632.$$

$n = 2$: 0.75; $n = 10$: 0.651; $n = 1000$: 0.632. The other **36.8%** of rows are **out-of-bag** (OOB) for that sample.

<div class="nb nb-remark">

<strong>Trap</strong> — 63.2% is the fraction of **distinct original rows** in a bootstrap sample, not its size (which is $n$) and not a per-draw probability (that is $1/n$). "Probability a given row is *not* in the sample" is $(1 - 1/n)^n \approx 0.368$.

</div>

## 9.2 Bagging and random forests {#ml-9-2}

**Bagging** (bootstrap aggregating): fit the same learner on $B$ bootstrap samples and average (regression) or vote (classification). Why it works: if $B$ models each have variance $\sigma^2$ and pairwise correlation $\rho$, their average has variance

$$\rho\,\sigma^2 + \frac{1-\rho}{B}\,\sigma^2.$$

Averaging kills the second term but not the first. So the base models should be **low-bias, high-variance** (deep trees), and as **decorrelated** as possible.

A **random forest** bags deep trees and, at every split, considers only a **random subset of features** (typically $\sqrt{d}$ for classification), which decorrelates the trees further.

- **OOB error:** predict each row using only the trees that did not see it: a nearly free validation estimate (it matched 5-fold CV to within 0.001 in the book's test).
- **More trees never overfit a forest:** test error stabilises as $B$ grows; more trees cost compute, not accuracy. Tune `max_features` and `min_samples_leaf`, not $B$.

<div class="nb nb-example">

<strong>Example</strong> (Forest vote)

Five trees vote Yes, No, Yes, Yes, No: the forest predicts Yes (3 to 2). Variance of an average of 10 trees each with variance 4 and correlation 0.25: $0.25\cdot 4 + 0.75\cdot 4/10 = 1.3$; with infinitely many trees it never drops below $\rho\sigma^2 = 1$.

</div>

<div class="nb nb-remark">

<strong>Trap</strong> — "Random forests reduce bias." They reduce **variance**; a forest's bias is about that of one deep tree (slightly higher, because feature subsampling weakens each tree).

</div>

## 9.3 Feature importance and its traps {#ml-9-3}

- **Mean decrease in impurity** (MDI, scikit-learn's `feature_importances_`): the total impurity drop from splits on each feature. **Biased** towards high-cardinality and continuous features: a column of random noise can rank above a real binary feature, because a continuous column offers hundreds of thresholds to fit noise.
- **Permutation importance:** shuffle one column in **held-out** data and measure the score drop. Puts noise at about zero.
- **Correlated features split the credit:** add a near-copy of the top feature and each copy looks half as important.

<div class="nb nb-remark">

<strong>Trap</strong> — Importance is not causal effect. "Your forest says `customer_id` is the top feature, why?" wants: MDI bias towards many-valued features, plus check for leakage. Prefer permutation importance on validation data, drop-column importance or SHAP values.

</div>

## 9.4 AdaBoost {#ml-9-4}

**Boosting** builds an additive model $F(x) = \sum_m \alpha_m h_m(x)$ **sequentially**, each weak learner focusing on what the previous ones got wrong.

1. Start with equal weights $w_i = 1/n$.
2. Fit a weak learner (a stump) minimising the weighted error $\varepsilon_m$; set $\alpha_m = \tfrac12 \ln\dfrac{1 - \varepsilon_m}{\varepsilon_m}$.
3. Multiply weights of misclassified points by $e^{\alpha_m}$ and of correct ones by $e^{-\alpha_m}$; renormalise. Predict $\text{sign}\big(\sum_m \alpha_m h_m(x)\big)$.

<div class="nb nb-example">

<strong>Example</strong> (One round)

Ten points, a stump misclassifies three: $\varepsilon_1 = 0.3$, $\alpha_1 = \tfrac12\ln(0.7/0.3) = 0.424$. After renormalising, each mistake has weight $1/6$ and each correct point $1/14$: the mistakes now carry **half** the total weight, so the next stump must find something new. In the book's example three stumps classify all ten points although no single stump beats 70%.

</div>

AdaBoost minimises the **exponential loss**, which grows fast for negative margins, so it pours weight onto mislabelled points: its main weakness on noisy labels.

## 9.5 Gradient boosting {#ml-9-5}

Treat the predictions as the parameters and do gradient descent on the loss: fit a small tree $h_m$ to the **negative gradient** (the pseudo-residuals) and add a shrunken copy,

$$F_m(x) = F_{m-1}(x) + \nu\, h_m(x), \qquad 0 < \nu \le 1.$$

For squared loss the pseudo-residual is the ordinary residual $y - F$; for log-loss it is $y - p$; for absolute loss it is $\text{sign}(y - F)$, which is why boosting can use robust losses.

<div class="nb nb-example">

<strong>Example</strong> (One round by hand)

$y = (1, 3, 6, 8)$ at $x = 1..4$, $\nu = 0.5$. Start at the mean, $F_0 = 4.5$. Residuals $(-3.5, -1.5, 1.5, 3.5)$; the best stump splits at $x \le 2.5$ and predicts $(-2.5, -2.5, 2.5, 2.5)$. Add half: $F_1 = (3.25, 3.25, 5.75, 5.75)$.

</div>

Boosting **can overfit** as rounds grow. Control it with a small learning rate (0.01 to 0.1) and **early stopping** on validation loss, shallow trees (depth 3 to 8), and row and column subsampling. A smaller rate needs more trees; $\nu \times M$ is roughly constant at the optimum.

## 9.6 XGBoost, LightGBM, CatBoost {#ml-9-6}

**XGBoost** uses a second-order (Newton) step and regularises the tree itself. With per-example gradients $g_i$ and Hessians $h_i$ summed per leaf into $G$ and $H$:

$$w^\star = -\frac{G}{H + \lambda}, \qquad \text{Gain} = \frac12\left[\frac{G_L^2}{H_L + \lambda} + \frac{G_R^2}{H_R + \lambda} - \frac{(G_L + G_R)^2}{H_L + H_R + \lambda}\right] - \gamma.$$

$\lambda$ shrinks leaf values; $\gamma$ is the minimum gain a split must earn (pre-pruning); `min_child_weight` is a minimum $H$ per leaf. For squared loss $g = \hat y - y$ and $h = 1$, so a leaf is a shrunk mean residual.

<div class="nb nb-example">

<strong>Example</strong> (XGBoost leaf)

A leaf gets squared-error gradients $(-2, -1, 0.5, -1.5)$, $h = 1$ each, $\lambda = 2$: $G = -4$, $H = 4$, so $w = 4/6 = 0.667$. With $\lambda = 0$ it would be the plain mean residual, 1.0.

</div>

The engineering that made it win: shrinkage and column subsampling; **sparsity-aware splits** that learn a default direction for missing values; histogram / quantile split finding; parallel, cache-aware, out-of-core computation.

**LightGBM:** histogram splits, **leaf-wise** growth (split the leaf with the largest gain; controlled by `num_leaves`, can overfit small data), gradient-based one-side sampling, exclusive feature bundling, native categoricals. Usually faster. **CatBoost:** ordered target statistics for categorical features (no target leakage), ordered boosting, symmetric trees. Differences of half a percent between them are noise; tuning matters more than the library.

**Stacking** trains a meta-model on the base models' **out-of-fold** predictions (otherwise it learns to trust whichever model overfits most). It helps when base models are good and make different errors.

## 9.7 Bagging versus boosting {#ml-9-7}

| | Bagging / random forest | Boosting (AdaBoost, GBM, XGBoost) |
|---|---|---|
| Training | parallel, independent | sequential, each fixes the last |
| Base learner | strong, low bias, high variance (deep trees) | weak, high bias (stumps, shallow trees) |
| Main effect | **reduces variance** | **reduces bias** (and variance, via shrinkage) |
| More rounds | never hurts | can overfit; needs early stopping |
| Label noise | robust | AdaBoost sensitive |
| Votes | equal | weighted by $\alpha_m$ or shrinkage |

Which to try: an **overfitting** tree → random forest; an **underfitting** model → boosting.

<div class="nb nb-moral">

Average decorrelated low-bias models to kill variance (forests); add shrunken corrections along the loss gradient to kill bias (boosting). XGBoost is that with a Newton step, $\lambda$ on leaf values and $\gamma$ per leaf.

</div>
