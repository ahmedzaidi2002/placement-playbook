---
title: "5 · Logistic regression and the perceptron"
linkTitle: "5 Logistic regression"
weight: 5
math: true
---
The most-asked classifier in placement interviews: it is a linear model, a probabilistic model and a one-neuron neural network at once, and it is the baseline teams actually ship first. Know its loss, its one-line gradient, why it is not trained with MSE, and how to pick its threshold.

## 5.1 From a score to a probability {#ml-5-1}

A linear score $z = w^\top x + b$ can be any real number; we want $P(y = 1 \mid x) \in (0, 1)$. Model the **log-odds** as linear:

$$\log\frac{p}{1-p} = w^\top x + b \quad\Longleftrightarrow\quad p = \sigma(z) = \frac{1}{1 + e^{-z}}.$$

Values to know: $\sigma(0) = 0.5$, $\sigma(2) = 0.881$, $\sigma(-2) = 0.119$, and $\sigma(-z) = 1 - \sigma(z)$, $\sigma'(z) = \sigma(z)(1 - \sigma(z)) \le \tfrac14$.

**Reading a coefficient:** one unit more of $x_j$ adds $w_j$ to the log-odds, so it **multiplies the odds by $e^{w_j}$**. A weight of 0.7 roughly doubles the odds ($e^{0.7} = 2.01$).

<div class="nb nb-example">

<strong>Example</strong> (Score an applicant)

$z = -3 + 0.8\cdot\text{income} + 1.2\cdot\text{has\_job}$, applicant with income 2 and a job: $z = -0.2$, $p = \sigma(-0.2) = 0.450$. At threshold 0.5 the answer is "no".

</div>

<div class="nb nb-remark">

<strong>Trap</strong> — "Logistic regression is a regression algorithm because of its name." It is a **classifier**; it regresses the log-odds. And its decision boundary $w^\top x + b = 0$ is a hyperplane: it is a **linear classifier** despite the non-linear sigmoid (thresholding $\sigma(z)$ at 0.5 is thresholding $z$ at 0).

</div>

## 5.2 Log-loss and its gradient {#ml-5-2}

Each label is a coin flip with probability $p_i$; the negative log-likelihood is the **log-loss** (binary cross-entropy):

$$J(w) = -\frac{1}{n}\sum_i \big[y_i \log p_i + (1-y_i)\log(1-p_i)\big], \qquad \nabla J = \frac{1}{n}X^\top(p - y).$$

The gradient is **"prediction minus target, times input"**, the same form as linear regression, and the same $p - y$ reappears for softmax and in neural networks. The loss is **convex**, so gradient descent cannot get stuck in a bad local minimum. There is no closed form; fit by gradient descent, Newton's method (IRLS, converges in a handful of steps) or L-BFGS (scikit-learn's default).

<div class="nb nb-remark">

<strong>Trap</strong> — On perfectly separable data the unregularised maximum-likelihood weights do not exist: scaling $w$ up keeps lowering the loss, so $\|w\| \to \infty$ and probabilities become over-confident. Regularise. Note that scikit-learn's `LogisticRegression` is **L2-regularised by default** and its `C` is the **inverse** of the strength: larger C means weaker regularisation.

</div>

## 5.3 Why not MSE for classification? {#ml-5-3}

Three reasons, in the order interviewers like them:

1. **Vanishing gradient when confidently wrong.** For a positive example with $z = -5$, the cross-entropy gradient in $z$ is $p - 1 \approx -0.993$; the MSE gradient picks up an extra factor $p(1-p)$ and is only $-0.013$. The most wrong prediction learns slowest.
2. **Non-convexity.** $(1 - \sigma(z))^2$ is not convex; log-loss is.
3. **Wrong likelihood.** MSE is the Gaussian likelihood; labels are Bernoulli. Log-loss heavily punishes confident mistakes ($-\log p \to \infty$ as $p \to 0$), which gives calibrated probabilities.

## 5.4 Many classes {#ml-5-4}

**Softmax regression** keeps one weight vector per class:

$$P(y = k \mid x) = \frac{e^{z_k}}{\sum_j e^{z_j}}.$$

Probabilities are positive and sum to 1; the loss is categorical cross-entropy and the gradient is again $P - Y$. With two classes softmax reduces exactly to the sigmoid of $z_1 - z_0$. Implementations subtract $\max_k z_k$ first to avoid overflow.

Binary-only learners (SVMs, perceptrons) are extended by:

- **One-vs-rest:** $K$ classifiers, class $k$ against all others; predict the most confident.
- **One-vs-one:** $K(K-1)/2$ classifiers, one per pair, majority vote. For $K = 10$ that is 10 versus 45.

<div class="nb nb-remark">

<strong>Trap</strong> — **Multilabel is not multiclass.** If an article can be both "sports" and "business", use $K$ independent sigmoids with binary cross-entropy. A softmax forces the probabilities to compete and sum to 1.

</div>

## 5.5 Thresholds and imbalance {#ml-5-5}

Logistic regression outputs a probability; the decision is a separate step. If missing a positive costs $c_{FN}$ and a false alarm costs $c_{FP}$, predict positive when

$$p > \frac{c_{FP}}{c_{FP} + c_{FN}}.$$

The default 0.5 assumes equal costs. Fraud that costs ₹5,000 when missed against ₹100 of friction for a wrong block gives a threshold of $100/5100 \approx 0.02$.

On data with 5% positives, a model at threshold 0.5 had precision 1.0 but recall 0.29; lowering the threshold to 0.2 gave precision 0.64, recall 0.55. "Always predict 0" scored 95% accuracy with zero recall. Lowering the threshold and using balanced class weights both trade precision for recall; choose the point from the business cost on a precision–recall curve.

<div class="nb nb-remark">

<strong>Trap</strong> — "With imbalanced data, always oversample." Reweighting or resampling changes the predicted probabilities (they no longer estimate the true $P(y = 1 \mid x)$) and is often equivalent to moving the threshold. First try: keep the model, pick the threshold on validation data, report PR-AUC.

</div>

## 5.6 Generalised linear models, in one table {#ml-5-6}

| Model | Distribution of $y$ | Link | Target |
|---|---|---|---|
| Linear regression | Gaussian | identity | real values |
| Logistic regression | Bernoulli | logit $\log\frac{\mu}{1-\mu}$ | binary |
| Poisson regression | Poisson | $\log \mu$ | counts |
| Softmax regression | categorical | multinomial logit | $K$ classes |

## 5.7 The perceptron and XOR {#ml-5-7}

The **perceptron** predicts $\text{sign}(w^\top x)$ and, on each mistake, updates $w \leftarrow w + y_i x_i$. If the data are linearly separable with margin $\gamma$ and $\|x_i\| \le R$, it makes at most $(R/\gamma)^2$ mistakes (**perceptron convergence theorem**), in any order. On non-separable data it never stops.

**XOR cannot be learnt by one neuron**: no line separates $\{(0,1), (1,0)\}$ from $\{(0,0), (1,1)\}$. The best any line can do is 75%. Two ways out, both interview staples:

- **Add a feature:** with $x_1 x_2$ appended, XOR becomes linearly separable (the idea behind kernels, chapter 7).
- **Add a hidden layer:** XOR = OR and not AND, two neurons feeding a third (the opening of the [Deep Learning](../../dl/01-neurons/) book).

<div class="nb nb-remark">

<strong>Trap</strong> — "A single-layer perceptron can learn any Boolean function." Only linearly separable ones: AND, OR, NAND, NOR, NOT. Not XOR or XNOR.

</div>

<div class="nb nb-moral">

Logistic regression = linear score + sigmoid + Bernoulli likelihood: convex loss, gradient $(p - y)x$, a linear boundary, and probabilities you threshold by cost.

</div>
