---
title: "3 · Backpropagation"
linkTitle: "3 Backpropagation"
weight: 3
math: true
---
Backpropagation is the chain rule applied to a computation graph in the order that makes it cheap: from the loss backwards, reusing every intermediate product once. Interviews ask you to state it for an MLP, run one step by hand on a tiny network, and explain why gradients vanish or explode with depth.

## 3.1 The chain rule on a graph {#dl-3-1}

A **computation graph** has elementary operations as nodes. Each node needs only its **local gradient**; gradients arrive from above, are multiplied by the local gradient, and are **summed** over every path (fan-out).

<div class="nb nb-example">

<strong>Example</strong> ($f = (x + y)\,z$ at $x = 2, y = -1, z = 3$)

Forward: $q = x + y = 1$, $f = 3$. Backward: $\partial f/\partial z = q = 1$; $\partial f/\partial q = z = 3$, and the add node passes that unchanged to both inputs, so $\partial f/\partial x = \partial f/\partial y = 3$.

</div>

The three gate rules worth saying out loud: an **add** node routes its gradient unchanged to both inputs; a **multiply** node swaps (each input gets the upstream gradient times the *other* input); a **max** node sends the whole gradient to the winner and zero to the rest (that is how max-pooling backpropagates).

**Why reverse mode:** a loss has one output and millions of parameters. Reverse mode gets the whole gradient for the cost of about one extra forward pass; forward mode would need one pass per parameter. Backprop is reverse-mode automatic differentiation.

<div class="nb nb-remark">

<strong>Trap</strong> — Backprop is neither numerical differentiation (one pass per parameter, inexact) nor symbolic differentiation (expressions blow up). It is exact up to floating point and costs a small constant times the forward pass, but it must **store the forward activations**, which is why training needs far more memory than inference.

</div>

## 3.2 Backprop for an MLP {#dl-3-2}

With $z^{(l)} = W^{(l)} h^{(l-1)} + b^{(l)}$, $h^{(l)} = \phi(z^{(l)})$ and the error signal $\delta^{(l)} = \partial L/\partial z^{(l)}$:

$$\delta^{(L)} = p - y \ \ (\text{softmax + CE}), \qquad \delta^{(l)} = \big(W^{(l+1)\top}\delta^{(l+1)}\big) \odot \phi'(z^{(l)}), \qquad \frac{\partial L}{\partial W^{(l)}} = \delta^{(l)} h^{(l-1)\top}, \quad \frac{\partial L}{\partial b^{(l)}} = \delta^{(l)}.$$

In words: one forward pass storing every $z$ and $h$; then, for each layer from the top, an **outer product** for the weight gradient and a **transposed matrix product, masked by $\phi'$**, to pass the error down.

**Shape-matching** is the fastest way to rederive this under pressure: $\partial L/\partial W$ must have the shape of $W$, and there is usually only one way to multiply the available matrices into it. For a batch $X \in \mathbb R^{32 \times 100}$ through a layer with $W \in \mathbb R^{50 \times 100}$: $\partial L/\partial W = \Delta^\top X$ is $50 \times 100$, $\partial L/\partial b$ sums $\Delta$ over the batch (50), and $\partial L/\partial X = \Delta W$ is $32 \times 100$.

## 3.3 One step by hand {#dl-3-3}

<div class="nb nb-example">

<strong>Example</strong> (A 2-2-1 sigmoid network, binary cross-entropy, $\eta = 0.5$)

$x = (1, 0.5)$, target 1. **Forward:** hidden pre-activations $(0.15, 0.35)$, hidden outputs $h = (0.537, 0.587)$; output logit $-0.033$, $\hat y = 0.492$, loss $-\ln 0.492 = 0.710$.

**Backward:** output error $\delta^{(2)} = \hat y - y = -0.508$ (sigmoid + BCE gives this clean form). Output weight gradient $\delta^{(2)} h = (-0.273, -0.298)$. Hidden errors: output weights $(0.5, -0.6)$ times $\delta^{(2)}$ gives $(-0.254, 0.305)$, times $\sigma' = h(1-h) = (0.249, 0.243)$ gives $\delta^{(1)} = (-0.063, 0.074)$. One SGD step lowers the loss on this example from 0.710 to 0.512.

</div>

Two things to notice: the hidden unit with the negative outgoing weight gets a positive $\delta$ (raising it would lower $\hat y$), and the first-layer update is an outer product $\delta^{(1)}x^\top$: one example moves the first layer only along its own input direction.

<div class="nb nb-remark">

<strong>Trap</strong> — With MSE $\tfrac12(\hat y - y)^2$ instead of BCE, the output error picks up an extra factor: $\delta^{(2)} = (\hat y - y)\,\hat y(1 - \hat y)$. The clean $\hat y - y$ belongs to sigmoid + BCE and softmax + CE only. Forgetting which loss the question uses is the most common way to get this OA wrong.

</div>

**Gradient checking:** compare the analytic gradient with the centred difference $\big(L(\theta + h) - L(\theta - h)\big)/2h$. A relative error near $10^{-9}$ means the backward pass is right; a planted bug gives about 1. Use float64, turn off dropout, and avoid ReLU kinks.

## 3.4 Vanishing and exploding gradients {#dl-3-4}

The gradient reaching layer $l$ is a **product of one Jacobian per layer above it**, $W^{(k)\top}\,\text{diag}\,\phi'(z^{(k)})$. A product of many factors behaves like $\rho^{\text{depth}}$: below 1 it **vanishes** exponentially, above 1 it **explodes**.

| 30 layers, width 64 | Gradient at layer 1 relative to layer 30 |
|---|---|
| sigmoid, std $\sqrt{1/n}$ | $5 \times 10^{-19}$ |
| tanh, std $\sqrt{1/n}$ | 0.19 |
| ReLU, He init $\sqrt{2/n}$ | 0.79 |
| ReLU, 1.5× He | $10^{5}$ |

A 1.5× too large initial scale per layer compounds to five orders of magnitude: **initialisation is not a detail**. The fixes, each covered later: ReLU-family activations; variance-preserving initialisation (Xavier, He); normalisation (BatchNorm, LayerNorm); **residual connections** (an identity term in every Jacobian, so the product cannot collapse); gating (LSTM); **gradient clipping** for explosions.

<div class="nb nb-remark">

<strong>Trap</strong> — Vanishing gradients slow learning in the **early** layers (closest to the input), not the late ones. The network then behaves like a shallow model on top of nearly random features.

</div>

**Dying ReLUs:** a large learning-rate step that throws biases far negative, or a bad initialisation, leaves units whose input is negative for every example; their weights never change again. Initialising all biases at $-3$ left 99% of units dead before training. Remedies: smaller learning rate or warm-up, leaky ReLU / GELU, He initialisation with zero biases, normalisation before the ReLU.

## 3.5 What backprop costs {#dl-3-5}

A dense layer costs $n_{\text{in}} n_{\text{out}}$ multiply–adds per example forward. The backward pass needs two products of the same size (gradient for the input and for the weights), so **a training step costs about 3× the forward pass**. Memory: every activation needed by the backward pass is kept, so activation memory grows with depth × batch size × width. **Gradient checkpointing** stores only some layers and recomputes the rest, trading about one extra forward pass for memory.

<div class="nb nb-remark">

<strong>Trap</strong> — "Initialise all weights to zero (or to one constant)." Every unit in a layer then computes the same function and receives the same gradient forever: symmetry is never broken. Initialise randomly (biases can be zero).

</div>

<div class="nb nb-moral">

Backprop = one forward pass storing activations, then per layer from the top: an outer product for the weight gradient and a transposed product masked by $\phi'$ to pass the error down. Depth multiplies Jacobians, so gradients vanish or explode unless activations, initialisation, normalisation and shortcuts keep the per-layer gain near one.

</div>
