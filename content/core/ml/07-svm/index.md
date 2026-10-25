---
title: "7 · Support vector machines"
linkTitle: "7 SVM"
weight: 7
math: true
---
OA papers ask the conceptual layer: what support vectors are, the effect of $C$ and $\gamma$, which losses are convex. Interviews ask *why*: why maximise the margin, why only some points matter, what the kernel trick actually saves.

## 7.1 The margin {#ml-7-1}

Many lines separate separable data; the perceptron returns whichever it hits first. The SVM picks the one **farthest from the closest points of both classes**: build the widest road that keeps the two neighbourhoods on opposite sides. A boundary far from every training point is robust to small perturbations of them.

For $f(x) = w^\top x + b$ with labels $\pm 1$, fix the scale so the closest points satisfy $y_i f(x_i) = 1$. The street then has width $2/\|w\|$, so **maximising the margin is minimising $\|w\|$**:

$$\text{Hard margin: } \min_{w,b}\ \tfrac12\|w\|^2 \quad\text{s.t.}\quad y_i(w^\top x_i + b) \ge 1 \ \ \forall i.$$

This is a convex quadratic programme: one global optimum.

<div class="nb nb-example">

<strong>Example</strong> (Street width from the weights)

A trained linear SVM has $w = (3, 4)$, $b = -2$. $\|w\| = 5$, so the street is $2/5 = 0.4$ wide. The point $(1, 1)$ has $f = 3 + 4 - 2 = 5$: positive side, at distance $5/5 = 1$ from the hyperplane.

</div>

## 7.2 Soft margin and the hinge loss {#ml-7-2}

Real classes overlap, so let point $i$ violate the margin by a slack $\xi_i \ge 0$ at a price $C$:

$$\min_{w,b,\xi}\ \tfrac12\|w\|^2 + C\sum_i \xi_i \quad\text{s.t.}\quad y_i f(x_i) \ge 1 - \xi_i.$$

At the optimum $\xi_i = \max(0,\ 1 - y_i f(x_i))$, the **hinge loss**. So a soft-margin SVM is **hinge loss plus L2 regularisation**, the same shape as ridge-penalised logistic regression with a different loss.

- $\xi_i = 0$: outside the street. $0 < \xi_i \le 1$: inside the street but correctly classified. $\xi_i > 1$: misclassified.
- **Small $C$:** violations are cheap, the street is wide, many support vectors, heavily regularised (high bias).
- **Large $C$:** violations are expensive, the street narrows to fit the training data (high variance); $C \to \infty$ is the hard margin.

<div class="nb nb-remark">

<strong>Trap</strong> — $C$ is the **inverse** of regularisation strength. "Increasing $C$ increases regularisation" is the wrong option.

</div>

## 7.3 Support vectors and the dual {#ml-7-3}

Solving with Lagrange multipliers $\alpha_i$ gives the **dual problem** and the classifier

$$f(x) = \sum_i \alpha_i y_i\, x_i^\top x + b, \qquad 0 \le \alpha_i \le C.$$

Complementary slackness (a KKT condition) says each point either sits outside the street with $\alpha_i = 0$ or has $\alpha_i > 0$:

- $\alpha_i = 0$: outside the street; deleting it and retraining gives the **same** classifier.
- $0 < \alpha_i < C$: exactly on the margin.
- $\alpha_i = C$: inside the street or misclassified.

The points with $\alpha_i > 0$ are the **support vectors**; only they define the boundary.

<div class="nb nb-remark">

<strong>Trap</strong> — Support vectors are not just the points on the margin lines. In a soft-margin SVM every point with $y_i f(x_i) \le 1$ (on the margin, inside it, or misclassified) is one.

</div>

**Why bother with the dual?** (i) The data enter only through inner products $x_i^\top x_j$, which is what makes kernels possible. (ii) The solution is sparse in $\alpha$. (iii) It has one variable per example, which helps when $d \gg n$. For large $n$ with a linear kernel, primal solvers (LinearSVC, SGD on the hinge loss) are faster.

## 7.4 Kernels {#ml-7-4}

Points inside a circle versus outside cannot be split by a line in 2-D, but adding $x_1^2 + x_2^2$ as a third coordinate makes them linearly separable. A **kernel** computes the inner product in such a lifted space **without ever forming it**: $K(x, z) = \phi(x)^\top\phi(z)$.

<div class="nb nb-example">

<strong>Example</strong> (The quadratic kernel)

For $x = (1, 2)$, $z = (3, 1)$: $x^\top z = 5$, so $K = (x^\top z + 1)^2 = 36$. The explicit map has 6 coordinates and its dot product is also 36. For $d = 100$ and degree 3 the explicit map has 176,851 coordinates; the kernel still costs one 100-dimensional dot product.

</div>

| Kernel | $K(x, z)$ | Feature space |
|---|---|---|
| Linear | $x^\top z$ | the input itself |
| Polynomial | $(\gamma x^\top z + r)^p$ | all monomials up to degree $p$ |
| RBF (Gaussian) | $\exp(-\gamma \lVert x - z\rVert^2)$ | infinite-dimensional |
| Sigmoid | $\tanh(\gamma x^\top z + r)$ | not always a valid kernel |

A function is a valid kernel (**Mercer**) if every Gram matrix it produces is symmetric positive semi-definite.

**$\gamma$ in the RBF kernel** is an inverse length scale. Large $\gamma$: each support vector's influence is very local, the boundary wraps around individual points (low bias, high variance, nearly every point a support vector). Small $\gamma$: smooth, almost linear boundary. The RBF kernel needs **scaled** features. On concentric circles a linear SVM scores 0.58 (chance) and an RBF SVM 1.00.

<div class="nb nb-remark">

<strong>Trap</strong> — "Kernel SVMs are slow because of the high dimension." The dimension never appears; the cost is in $n$. The Gram matrix is $n \times n$ and training is roughly $O(n^2)$ to $O(n^3)$, which is why kernel SVMs are rarely used beyond a few hundred thousand points. Prediction costs one kernel evaluation per support vector.

</div>

## 7.5 Regression, probabilities and solvers {#ml-7-5}

- **SVR** replaces the hinge with the **ε-insensitive loss** $\max(0, |y - f(x)| - \varepsilon)$: errors inside a tube of half-width $\varepsilon$ are free. A wider tube gives a sparser, smoother model.
- **Probabilities:** SVMs output scores, not probabilities. **Platt scaling** fits a sigmoid on held-out scores.
- **SMO** (what LIBSVM, behind scikit-learn's SVC, uses) repeatedly optimises two $\alpha$'s at a time in closed form, because the constraint $\sum \alpha_i y_i = 0$ means you cannot change one alone.

## 7.6 Convex surrogate losses {#ml-7-6}

With margin $m = y f(x)$, we cannot train the 0-1 loss directly (it is a step: non-convex with zero gradient almost everywhere), so every classifier minimises a convex upper bound:

| Loss | Formula | Used by |
|---|---|---|
| 0-1 | $\mathbb{1}[m \le 0]$ | the true objective, never optimised directly |
| Hinge | $\max(0, 1 - m)$ | SVM |
| Logistic | $\log(1 + e^{-m})$ | logistic regression |
| Exponential | $e^{-m}$ | AdaBoost |
| Perceptron | $\max(0, -m)$ | perceptron |
| Squared | $(1 - m)^2$ | also punishes being "too right", a poor classification loss |

Hinge and logistic losses behave alike for misclassified points. Hinge is exactly zero once $m \ge 1$, which creates sparse support vectors; logistic keeps pushing every point and yields probabilities.

<div class="nb nb-remark">

<strong>Trap</strong> — "The hinge loss is not convex because it is not differentiable." Convexity does not need differentiability ($|x|$ is convex); use subgradients.

</div>

<div class="nb nb-moral">

SVM = hinge loss + L2 penalty. The dual depends on the data only through inner products, so kernels give non-linear boundaries, and complementary slackness makes the solution depend only on the support vectors. $C$ and $\gamma$ both raise variance as they grow.

</div>
