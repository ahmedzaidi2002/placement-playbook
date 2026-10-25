---
title: "1 · Neurons, the perceptron and the MLP"
linkTitle: "1 Neurons and the MLP"
weight: 1
math: true
---
Every network, from a two-layer classifier to a 100-layer Transformer, is built from one object: a weighted sum followed by a fixed non-linear function. This chapter shows what one neuron can and cannot do (the XOR story OAs keep asking about), then stacks neurons into the multilayer perceptron whose parameters you should count in your sleep.

## 1.1 The artificial neuron {#dl-1-1}

$$a = \phi(z), \qquad z = w^\top x + b = \sum_i w_i x_i + b.$$

$z$ is the **pre-activation** (weighted sum, logit); $\phi$ is the **activation** (transfer) function: step, sigmoid, tanh or ReLU. With a sigmoid, a neuron is exactly logistic regression.

<div class="nb nb-example">

<strong>Example</strong> (The OA neuron)

Inputs $(1, 0, 1, 1)$, weights $(0.6, -0.9, -0.4, 0.5)$, bias $-0.3$, sigmoid: $z = 0.6 - 0.4 + 0.5 - 0.3 = 0.40$, output $\sigma(0.4) = 0.599$. The input that is 0 contributes nothing whatever its weight, which is what the setter hopes you forget.

</div>

<div class="nb nb-remark">

<strong>Trap</strong> — The neuron applies $\phi$ to the weighted sum; it does not take a weighted sum of $\phi(x_i)$. And dropping the bias forces every decision boundary through the origin.

</div>

The biology analogy (dendrites, synapses, firing threshold) is good for exactly one sentence. Real neurons spike in time, dendrites compute non-linearly, and nobody has shown the brain runs backpropagation.

## 1.2 The perceptron {#dl-1-2}

Rosenblatt's perceptron predicts $\text{sign}(w^\top x + b)$ and learns only from mistakes: if $y_i(w^\top x_i + b) \le 0$, set $w \leftarrow w + \eta y_i x_i$ and $b \leftarrow b + \eta y_i$. Each update strictly increases that point's margin.

- **Convergence theorem:** on linearly separable data with margin $\gamma$ and radius $R$, at most $(R/\gamma)^2$ updates, in any order.
- On **non-separable** data it never stops, and unlike an SVM it does not maximise the margin; the answer depends on the data order.

<div class="nb nb-remark">

<strong>Trap</strong> — "Increase the learning rate to make the perceptron converge faster." Starting from $w = 0$, every weight vector visited with rate $\eta$ is just $\eta$ times the one visited with rate 1, so the mistakes and the number of updates are identical.

</div>

## 1.3 XOR: what one neuron cannot do {#dl-1-3}

XOR is 1 exactly when one input is 1. No line separates $\{(0,1), (1,0)\}$ from $\{(0,0), (1,1)\}$, so **no single neuron computes XOR**, whatever its activation: a single neuron's boundary is always a hyperplane. On XOR the perceptron cycles forever and ends at 50% accuracy.

**Two layers solve it:** XOR = OR and not AND. Hidden unit $h_1$ = OR (weights 1, 1, bias $-0.5$), $h_2$ = AND (weights 1, 1, bias $-1.5$), output = $h_1$ and not $h_2$ (weights $1, -1$, bias $-0.5$). The hidden layer **re-represents** the input so that the classes become linearly separable: that is representation learning in one table.

<div class="nb nb-remark">

<strong>Trap</strong> — "A single-layer perceptron can learn any Boolean function." Only linearly separable ones (AND, OR, NAND, NOR, NOT). Since NAND is one of them and NAND is universal, *networks* of step neurons can compute any Boolean function.

</div>

## 1.4 The multilayer perceptron and parameter counts {#dl-1-4}

An MLP with widths $n_0, n_1, \dots, n_L$ computes $h^{(l)} = \phi(W^{(l)} h^{(l-1)} + b^{(l)})$, usually with no activation on the last layer (it outputs logits).

<div class="nb nb-theorem nb-block">

<strong>Parameter count</strong>

$$\sum_{l=1}^{L} (n_{l-1} + 1)\, n_l$$

Each of the $n_l$ units in layer $l$ has $n_{l-1}$ weights and one bias. Activations and the input layer have no parameters.

</div>

<div class="nb nb-example">

<strong>Example</strong> (An MNIST MLP)

$784 \to 256 \to 128 \to 10$: $785 \cdot 256 = 200{,}960$, $257 \cdot 128 = 32{,}896$, $129 \cdot 10 = 1{,}290$; total **235,146**. A $3$-$4$-$2$ network has $4\cdot4 + 5\cdot2 = 26$ parameters.

</div>

**The non-linearity is not optional.** Delete every $\phi$ and $W^{(2)}(W^{(1)}x + b^{(1)}) + b^{(2)}$ collapses to a single affine map: a deep linear network can represent only what one linear layer can.

<div class="nb nb-remark">

<strong>Trap</strong> — "ReLU is linear, so it adds no non-linearity." ReLU is **piecewise** linear: $\text{ReLU}(-1) + \text{ReLU}(1) \ne \text{ReLU}(0)$. A ReLU network is a piecewise-linear function with possibly a huge number of pieces.

</div>

## 1.5 Universal approximation, and why depth still matters {#dl-1-5}

**Universal approximation theorem:** one hidden layer of any continuous non-polynomial activation, wide enough, can approximate any continuous function on a compact set to any accuracy. The interview answer adds the two caveats: it says nothing about **how wide** (possibly exponential in the input dimension) and nothing about whether **training finds** the weights or whether they **generalise**.

**Depth buys pieces exponentially.** A one-hidden-layer ReLU net with $m$ units on the real line has at most $m + 1$ linear pieces. Composing a 2-unit "tent" layer $L$ times gives $2^L$ pieces with only $2L$ units; a single hidden layer needs at least 63 units for the 64 pieces that 6 tent layers (12 units) make. **Depth multiplies, width adds.**

## 1.6 Capacity {#dl-1-6}

Capacity is the richness of the functions an architecture can represent: a property of the model, not of the data or the optimiser.

- **Increases capacity:** more layers, more units, more input features, removing weight sharing.
- **Reduces effective capacity:** dropout, weight decay, early stopping, data augmentation, weight sharing, bottlenecks.
- **Does not change capacity:** the learning rate, the batch size, the number of epochs, the amount of data.

<div class="nb nb-remark">

<strong>Trap</strong> — "Dropout increases capacity because it trains an ensemble." Each thinned sub-network is smaller, and the averaged predictor is pulled towards simpler functions: dropout **lowers** effective capacity. On 200 points with random labels, a width-16 net memorised 100% without dropout and only 85.5% with dropout 0.5.

</div>

<div class="nb nb-moral">

A neuron is a linear function followed by a fixed non-linearity; one cannot do XOR, two layers can. Count parameters as $(n_{\text{in}} + 1) \times n_{\text{out}}$ per layer. One hidden layer is enough in principle; depth makes it enough in practice.

</div>
