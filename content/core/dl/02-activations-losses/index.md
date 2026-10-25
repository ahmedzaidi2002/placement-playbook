---
title: "2 · Activations, output layers and losses"
linkTitle: "2 Activations and losses"
weight: 2
math: true
---
Three choices sit at fixed places in every network: the non-linearity between layers, the function that turns the last layer's numbers into a prediction, and the loss that scores it. OAs test them with one-minute numerics ("softmax of these five logits") and with "which of these is a loss and which an activation?". Interviews test why the standard pairings are standard.

## 2.1 Activation functions {#dl-2-1}

The activation is the **only** source of non-linearity in an MLP: weights enter linearly, and the loss sits after the network, so it cannot change which functions the network represents.

| Name | $\phi(z)$ | $\phi'(z)$ | Where used |
|---|---|---|---|
| Sigmoid | $1/(1 + e^{-z})$ | $\sigma(1 - \sigma) \le 1/4$ | outputs (probabilities), LSTM gates |
| tanh | $2\sigma(2z) - 1$, range $(-1, 1)$ | $1 - \tanh^2 \le 1$ | RNN cells |
| ReLU | $\max(0, z)$ | 1 if $z > 0$, else 0 | default for CNNs and MLPs |
| Leaky ReLU | $\max(0.01z, z)$ | 1 or 0.01 | avoids dead units |
| ELU | $z$, or $\alpha(e^z - 1)$ if $z < 0$ | smooth | zero-mean-ish activations |
| GELU | $z\,\Phi(z)$ | smooth | Transformers (BERT, GPT) |
| SiLU / swish | $z\,\sigma(z)$ | smooth | Transformers, modern CNNs |

<div class="nb nb-remark">

<strong>Trap</strong> — "Which component provides non-linearity: weights, biases, activation, loss?" Only the activation. A linear model trained with cross-entropy is still logistic regression, with a linear boundary.

</div>

**Sigmoid and tanh saturate.** Both are nearly flat away from 0 ($\sigma'(5) = 0.0066$). Backprop multiplies one such factor per layer, and since $\sigma' \le 1/4$, ten sigmoid layers shrink a gradient to at most $4^{-10} \approx 10^{-6}$ of its size: the **vanishing gradient** problem in its simplest form. Sigmoid outputs are also all positive, so a following neuron's weight gradients all share one sign and zig-zag. tanh is zero-centred with maximum slope 1, which is why it was preferred for hidden layers before ReLU.

**ReLU** does not saturate for $z > 0$ (gradient exactly 1), is cheap, and gives sparse activations. Its failure mode is the **dead ReLU**: a unit whose input is negative for every example outputs 0, gets 0 gradient, and never recovers.

<div class="nb nb-remark">

<strong>Trap</strong> — "ReLU is not differentiable at 0, so it cannot be trained by gradient descent." Floating-point inputs essentially never hit 0 exactly; frameworks use the subgradient 0 there.

</div>

## 2.2 Output layers: sigmoid and softmax {#dl-2-2}

$$\text{softmax}(z)_k = \frac{e^{z_k}}{\sum_j e^{z_j}}$$

Positive, sums to 1, keeps the order of the logits, unchanged by **adding** a constant to every logit, but changed by **scaling** them.

<div class="nb nb-example">

<strong>Example</strong> (Softmax confidence from five logits)

$z = (2, 1, 0.1, -1, 0.5)$: $e^z = (7.389, 2.718, 1.105, 0.368, 1.649)$, sum 13.229, so softmax $= (0.559, 0.206, 0.084, 0.028, 0.125)$. The model predicts class 1 with 55.9% confidence. A logit gap of 1 is a probability **ratio** of $e \approx 2.72$.

</div>

- **Overflow:** $e^{1000}$ overflows. Subtract $\max_k z_k$ first (shift invariance makes this exact): the **log-sum-exp trick**.
- **Temperature:** dividing logits by $T$ sharpens ($T < 1$) or flattens ($T > 1$) the distribution without changing the argmax. Reappears in distillation and LLM sampling.
- **Sigmoid is two-class softmax:** $\text{softmax}(a, b)_1 = \sigma(a - b)$. A binary classifier needs one logit and a sigmoid.

<div class="nb nb-remark">

<strong>Trap</strong> — **Multilabel is not multiclass.** If an image can contain both a cat and a dog, use $K$ independent sigmoids with binary cross-entropy. A softmax forces the classes to compete, so "cat 0.9, dog 0.8" is impossible under it.

</div>

## 2.3 Cross-entropy, and why its gradient is so clean {#dl-2-3}

Cross-entropy is the negative log-likelihood of the labels: for one example with true class $y$, $L = -\log p_y$. With softmax outputs:

$$\frac{\partial L}{\partial z} = \text{softmax}(z) - y \qquad (\text{"prediction minus one-hot target"}).$$

The true logit is pushed up by $1 - p_y$ and every wrong logit down by its probability: big mistakes get big corrections, and the gradient never saturates while the prediction is wrong.

<div class="nb nb-example">

<strong>Example</strong> (Cross-entropy patterns)

True class 1 in the example above: $L = -\ln 0.559 = 0.582$. Equal logits over $K$ classes give $L = \ln K$. Logits $(5, -2, 0, 1)$ with the true class second: $p_y = 0.001$, a heavy penalty for a confident mistake.

</div>

<div class="nb nb-remark">

<strong>Sanity check at initialisation</strong> — with small random weights the logits are nearly equal, so a $K$-class classifier's first loss should be about $\ln K$ (2.30 for 10 classes). Far from that means a bug: wrong labels, softmax applied twice, a huge initial scale.

</div>

**Binary cross-entropy** with $p = \sigma(z)$: 0.105 for $p = 0.9$ on a positive, 2.303 for $p = 0.1$, $\ln 2 = 0.693$ at $p = 0.5$. Compute it **from the logit** (`BCEWithLogitsLoss`), not from a sigmoid output, or a large negative $z$ underflows to $\log 0 = -\infty$.

**Why not MSE for classification?** With a sigmoid output, the MSE gradient is $(\sigma(z) - y)\,\sigma'(z)$; when confidently wrong ($y = 1$, $z = -5$) the $\sigma'$ factor kills it: 0.0066 against 0.993 for cross-entropy. The most wrong prediction learns slowest. MSE on a sigmoid is also non-convex in $z$; cross-entropy is convex.

## 2.4 Other losses {#dl-2-4}

- **Hinge** $\max(0, 1 - yz)$ (SVMs); the squared loss punishes predictions that are "too right", another reason it is a poor classification loss.
- **Regression:** **MSE** is the Gaussian likelihood and dominated by outliers; **MAE** is robust but its gradient does not shrink near the optimum; **Huber** is quadratic within $\delta$ and linear outside (a residual of 10 costs 9.5 under Huber with $\delta = 1$ against 50 under $\tfrac12 r^2$).
- **Focal loss** multiplies cross-entropy by $(1 - p_y)^\gamma$ to down-weight easy examples when one class (background) vastly outnumbers the rest; it was introduced for one-stage object detectors.
- **Label smoothing** with parameter $\varepsilon$ replaces the one-hot target by $(1 - \varepsilon)\,y + \varepsilon/K$: with $\varepsilon = 0.1$, $K = 5$ the target is 0.92 on the true class and 0.02 elsewhere. The model can no longer drive the loss to 0 by pushing one logit to infinity, which curbs over-confidence.

<div class="nb nb-remark">

<strong>In my project</strong> (Transformer) — The [from-scratch Transformer](../../../projects/transformer/) used label smoothing $\varepsilon = 0.1$, as in the original paper. Its ablation found **no difference beyond run-to-run noise** in BLEU. That is a fair answer to "did label smoothing help?": it is meant to improve calibration and robustness, not necessarily the headline metric. One detail worth knowing: the smoothed target also put mass on the `<pad>` column.

</div>

## 2.5 Which is which: the task → output → loss table {#dl-2-5}

| Task | Output layer | Loss |
|---|---|---|
| Regression | linear (identity) | MSE / MAE / Huber |
| Binary classification | 1 logit, sigmoid | BCE (with logits) |
| Multiclass, one label | $K$ logits, softmax | categorical cross-entropy |
| Multilabel | $K$ logits, $K$ sigmoids | sum of $K$ BCEs |
| Counts | exponential (log-rate) | Poisson NLL |

**Activations:** ReLU, leaky ReLU, ELU, GELU, SiLU, tanh, sigmoid (hidden). **Output maps:** sigmoid, softmax, identity. **Losses:** MSE, MAE, Huber, BCE, CE, hinge, focal, KL divergence, contrastive. Sigmoid and softmax are never losses.

<div class="nb nb-remark">

<strong>Trap</strong> — In PyTorch, `nn.CrossEntropyLoss` takes **logits** and applies log-softmax itself. Adding `nn.Softmax` before it computes softmax twice: training still runs, but gradients shrink and the loss cannot reach its floor. Same for `BCEWithLogitsLoss` after a sigmoid.

</div>

<div class="nb nb-moral">

Hidden layers: ReLU for CNNs and MLPs, GELU/SiLU for Transformers, tanh and sigmoid only inside recurrent cells and gates. Output and loss are chosen together by the task; softmax plus cross-entropy gives the gradient $p - y$.

</div>
