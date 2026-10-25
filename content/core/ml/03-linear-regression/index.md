---
title: "3 · Linear regression"
linkTitle: "3 Linear regression"
weight: 3
math: true
---
The one model every interviewer assumes you can fit by hand in an OA, explain three ways, and criticise. It is also the template for every other model: a hypothesis class, a loss, a closed form or a gradient, and assumptions whose failure you can diagnose.

## 3.1 The model and least squares {#ml-3-1}

$$\hat y = w_0 + w_1 x_1 + \dots + w_d x_d$$

**Ordinary least squares** chooses the weights that minimise the sum of squared residuals $\sum_i (y_i - \hat y_i)^2$. "Linear" means linear **in the parameters**: $y = w_0 + w_1 x + w_2 x^2 + w_3 \log x$ is still linear regression.

Setting the gradient to zero gives the **normal equations** and the closed form

$$X^\top X\, \hat w = X^\top y \quad\Longrightarrow\quad \hat w = (X^\top X)^{-1} X^\top y.$$

The loss is convex, so this is the global minimum. In practice libraries solve it with QR or SVD rather than inverting $X^\top X$ (forming it squares the condition number). Cost $O(nd^2 + d^3)$; for huge $d$ or streaming data use gradient descent.

Three views of the same answer, each worth one interview sentence:

- **Calculus:** the normal equations above.
- **Geometry:** $\hat y$ is the orthogonal projection of $y$ onto the column space of $X$; the residual is perpendicular to every feature. With an intercept, residuals sum to zero and the line passes through $(\bar x, \bar y)$.
- **Probability:** with Gaussian noise $y = w^\top x + \varepsilon$, maximising the likelihood is exactly minimising squared error. (With Laplace noise you get absolute error, which estimates the median.)

## 3.2 One feature, by hand {#ml-3-2}

$$\hat b_1 = \frac{\sum (x_i-\bar x)(y_i-\bar y)}{\sum (x_i-\bar x)^2} = \frac{n\sum x_i y_i - \sum x_i \sum y_i}{n\sum x_i^2 - (\sum x_i)^2} = r\,\frac{s_y}{s_x}, \qquad \hat b_0 = \bar y - \hat b_1 \bar x.$$

<div class="nb nb-example">

<strong>Example</strong> (The OA fit, under two minutes)

$x = (1,2,3,4,5)$, $y = (2,4,5,4,6)$. Sums: $\sum x = 15$, $\sum y = 21$, $\sum xy = 71$, $\sum x^2 = 55$.

$\hat b_1 = \dfrac{5\cdot 71 - 15\cdot 21}{5\cdot 55 - 15^2} = \dfrac{40}{50} = 0.8$, $\quad \hat b_0 = 4.2 - 0.8\cdot 3 = 1.8$.

Fitted values $2.6, 3.4, 4.2, 5.0, 5.8$; $\text{RSS} = 2.4$, $\text{TSS} = 8.8$, so $R^2 = 1 - 2.4/8.8 = 0.727$, which equals $r^2$ ($r = 0.853$). Prediction at $x = 6$: $6.6$.

</div>

<div class="nb nb-remark">

<strong>Trap</strong> — Regressing $x$ on $y$ does **not** give slope $1/\hat b_1$. It gives $r\,s_x/s_y$; the product of the two slopes is $r^2 \le 1$. Also, a slope has units (rupees per square foot), so "a bigger coefficient means a more important feature" is meaningless unless features share a scale.

</div>

Reading a coefficient: $w_j$ is the change in the prediction for a one-unit rise in $x_j$ **with the other features held fixed**. With $\log y$ as the target, $100\,w_j$ is roughly a percentage change.

<div class="nb nb-remark">

<strong>Trap</strong> — "The fit is good, so area *causes* price exactly as the weight says." A good fit shows association, not cause; a hidden factor (location) can drive both.

</div>

## 3.3 Gradient descent {#ml-3-3}

Start anywhere and step downhill: $w \leftarrow w - \alpha \cdot \nabla J(w)$. For MSE the gradient is $\frac{2}{n} X^\top(Xw - y)$, i.e. "error times input", averaged.

<div class="nb nb-example">

<strong>Example</strong> (One step)

Weight 5, slope of the loss 2, learning rate 0.1: $w = 5 - 0.1\cdot 2 = 4.8$.

</div>

- **Learning rate too large:** overshoots and diverges (loss bounces up and down). **Too small:** crawls. Try 0.1, 0.01, 0.001.
- On a quadratic, gradient descent converges only if $\alpha < 2/\lambda_{\max}$ of the Hessian. Unscaled features make $\lambda_{\max}$ huge, forcing a tiny step, which is why you **standardise before gradient descent** even though OLS's answer does not care.
- Batch GD uses all rows per step; **stochastic** GD uses one row; **mini-batch** GD uses a few. Chapter 12 and the [optimisers chapter](../../dl/04-optimisers/) of the DL book have momentum and Adam.

## 3.4 R² and adjusted R² {#ml-3-4}

$$R^2 = 1 - \frac{\text{RSS}}{\text{TSS}}, \qquad R^2_{\text{adj}} = 1 - (1 - R^2)\,\frac{n-1}{n-p-1}$$

$R^2$ is the share of the variance of $y$ explained, relative to always predicting $\bar y$. For simple linear regression with an intercept, $R^2 = r^2$, so a correlation of $-0.8$ means 64% of the variance is explained (the sign disappears).

- On training data with an intercept, $0 \le R^2 \le 1$ and $R^2$ **never decreases** when you add a feature, even a column of noise.
- On test data $R^2$ **can be negative**: the model is worse than predicting the training mean.
- Adjusted $R^2$ penalises the feature count. OA: $R^2 = 0.80$, $n = 50$, $p = 4$ gives $1 - 0.2\cdot 49/45 = 0.782$.

<div class="nb nb-remark">

<strong>Trap</strong> — "High $R^2$ means the model is right" and "low $R^2$ means useless" are both wrong. A line through a curve can have $R^2 = 0.9$ with systematic residuals; a noisy real effect (stock returns) can have $R^2 = 0.02$ and be valuable. And $R^2 = 0.64$ does not mean "64% of points predicted correctly".

</div>

## 3.5 Assumptions and what breaks {#ml-3-5}

| Assumption | How you see it fail | Consequence and fix |
|---|---|---|
| Linearity | curve in residuals vs fitted | biased predictions; add transforms or a non-linear model |
| Independent errors | pattern in residuals vs time | standard errors too small; time-series models |
| Constant variance (homoscedasticity) | funnel-shaped residuals | OLS still unbiased, SEs wrong; log $y$, weighted LS |
| Normal errors | Q–Q plot | matters only for small-sample tests and intervals |
| No perfect collinearity | rank, VIF | no unique solution; drop or combine, ridge |
| No influential outliers | leverage, Cook's distance | one point drags the line; robust loss (Huber) |

<div class="nb nb-remark">

<strong>Trap</strong> — "Linear regression needs $x$ and $y$ to be normally distributed." Nothing is assumed about $x$, and normality (needed only for exact tests) is about the **errors**, not $y$.

</div>

**Gauss–Markov:** with zero-mean, uncorrelated, equal-variance errors, OLS is the **BLUE** (best linear unbiased estimator). "Best among *unbiased*" is the catch: ridge is biased and can have lower error (chapter 4).

## 3.6 Multicollinearity {#ml-3-6}

When features are highly correlated, $X^\top X$ is nearly singular and the individual coefficients get huge variance and can flip sign. Measure it with the **variance inflation factor** $\text{VIF}_j = 1/(1 - R_j^2)$, where $R_j^2$ comes from regressing feature $j$ on the others: above 5 is worrying, above 10 serious.

<div class="nb nb-remark">

<strong>Trap</strong> — Multicollinearity does **not** bias OLS and does **not** hurt predictions on data like the training data. It damages the *interpretation* of individual coefficients. Remedies: drop one of a pair, combine them, ridge, or PCA regression. "The normal equations fail when features are correlated" is also wrong: they fail only with **perfect** collinearity or more features than rows.

</div>

## 3.7 Polynomial features and outliers {#ml-3-7}

Replacing $x$ by $(x, x^2, x^3, \dots)$ keeps the problem linear in $w$, at the cost of dimension (all degree-$\le 2$ terms of 10 features: 66 columns) and of wild extrapolation at high degree. Squared loss lets one large residual dominate: ten points on $y \approx 2x + 1$ with one $y$ replaced by 60 give an OLS slope of 4.23; the **Huber** loss (quadratic for small residuals, linear for large) gives 2.00.

<div class="nb nb-moral">

OLS is calculus, geometry and Gaussian likelihood at once. It is unbiased, sensitive to outliers and collinearity, and only as good as the linearity of the relationship.

</div>
