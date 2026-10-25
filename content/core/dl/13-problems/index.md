---
title: "13 · OA practice problems"
linkTitle: "13 OA practice"
weight: 13
math: true
---
Thirty-eight problems in OA shape: shapes and parameter counts, one-minute numerics, and "which statements are true". Aim for one to two minutes each with a basic calculator. The hint and solution are folded under each problem; try it first.

## 13.1 Neurons, activations and losses {#dl-13-1}

<div class="nb nb-problem nb-block" id="problem-dl-1">

<strong>Problem 1</strong> (A neuron's output)

Weights $(1.2, -0.7, 0.5)$, bias $-0.4$, input $(1, 2, 3)$. Weighted sum, and the output under sigmoid, tanh and ReLU?

<details class="nb-hint">
<summary>Hint</summary>

Compute $z$ once, then apply each function.

</details>

<details class="nb-sol">
<summary>Solution</summary>

$z = 1.2 - 1.4 + 1.5 - 0.4 = 0.9$. Sigmoid 0.711, tanh 0.716, ReLU 0.9.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-dl-2">

<strong>Problem 2</strong> (MLP parameters)

How many trainable parameters (biases included) in a fully connected network $100 \to 50 \to 50 \to 3$?

<details class="nb-hint">
<summary>Hint</summary>

$(n_{\text{in}} + 1) \times n_{\text{out}}$ per layer.

</details>

<details class="nb-sol">
<summary>Solution</summary>

$101\cdot50 + 51\cdot50 + 51\cdot3 = 5050 + 2550 + 153 = 7{,}753$.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-dl-3">

<strong>Problem 3</strong> (Softmax and cross-entropy)

Logits $(2, 1, -1)$. Softmax probabilities, and the cross-entropy if the true class is the second; if it is the first.

<details class="nb-hint">
<summary>Hint</summary>

$e^2 = 7.389$, $e^1 = 2.718$, $e^{-1} = 0.368$.

</details>

<details class="nb-sol">
<summary>Solution</summary>

Sum 10.475, so $(0.705, 0.259, 0.035)$. True class second: $-\ln 0.259 = 1.35$. True class first: $-\ln 0.705 = 0.35$. The difference is exactly the logit gap, 1.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-dl-4">

<strong>Problem 4</strong> (Edge cases)

(a) A 4-class classifier outputs logits $(1, 1, 1, 1)$: cross-entropy? And for $(101, 101, 101, 101)$? (b) BCE for $p = 0.9$ on a positive, and for a 0.99 prediction of the wrong class?

<details class="nb-hint">
<summary>Hint</summary>

Equal logits mean a uniform softmax, whatever their value.

</details>

<details class="nb-sol">
<summary>Solution</summary>

(a) $\ln 4 = 1.386$ in both cases (softmax is shift-invariant). (b) $-\ln 0.9 = 0.105$; $-\ln 0.01 = 4.605$: confident mistakes are punished hard.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-dl-5">

<strong>Problem 5</strong> (Which are loss functions?)

(a) ReLU (b) hinge (c) softmax (d) Huber (e) cross-entropy (f) GELU (g) KL divergence.

<details class="nb-hint">
<summary>Hint</summary>

A loss compares a prediction with a target and returns a number to minimise.

</details>

<details class="nb-sol">
<summary>Solution</summary>

(b), (d), (e), (g). ReLU and GELU are activations; softmax is an output map.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-dl-6">

<strong>Problem 6</strong> (The tagger)

An image tagger where each image may have several of 20 tags uses a softmax output and categorical cross-entropy. What goes wrong, and what is the fix?

<details class="nb-hint">
<summary>Hint</summary>

What does a softmax force the 20 probabilities to do?

</details>

<details class="nb-sol">
<summary>Solution</summary>

Softmax makes the tags compete and sum to 1, so two tags cannot both be 0.9, and the loss cannot represent several correct labels. Use 20 independent sigmoids with binary cross-entropy (one per tag) and a threshold per tag.

</details>

</div>

## 13.2 Backpropagation and optimisation {#dl-13-2}

<div class="nb nb-problem nb-block" id="problem-dl-7">

<strong>Problem 7</strong> (Gates)

For $f = \max(x, y)\cdot z$ at $x = 1$, $y = 4$, $z = -2$, give $\partial f/\partial x$, $\partial f/\partial y$, $\partial f/\partial z$.

<details class="nb-hint">
<summary>Hint</summary>

Multiply swaps; max routes the gradient to the winner.

</details>

<details class="nb-sol">
<summary>Solution</summary>

$f = -8$. $\partial f/\partial z = \max(x, y) = 4$; the max node receives $z = -2$ and sends it to the winner $y$: $\partial f/\partial y = -2$, $\partial f/\partial x = 0$.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-dl-8">

<strong>Problem 8</strong> (Gradient shapes)

A linear layer maps a batch $X \in \mathbb R^{32\times100}$ to $XW^\top + b$ with $W \in \mathbb R^{50\times100}$. Shapes of $\partial L/\partial W$, $\partial L/\partial b$, $\partial L/\partial X$, and which products give them? ($\Delta = \partial L/\partial \text{output}$.)

<details class="nb-hint">
<summary>Hint</summary>

Each gradient has the shape of the thing it differentiates.

</details>

<details class="nb-sol">
<summary>Solution</summary>

$\partial L/\partial W = \Delta^\top X$, $50\times100$; $\partial L/\partial b = $ column sums of $\Delta$, 50; $\partial L/\partial X = \Delta W$, $32\times100$.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-dl-9">

<strong>Problem 9</strong> (Steps)

60,000 examples, batch size 256 (last partial batch kept). How many optimiser steps in 10 epochs?

<details class="nb-hint">
<summary>Hint</summary>

Round up per epoch.

</details>

<details class="nb-sol">
<summary>Solution</summary>

$\lceil 60000/256\rceil = 235$ per epoch, so 2,350.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-dl-10">

<strong>Problem 10</strong> (Adam's first step)

Gradient $g_1 = -4$, $\eta = 0.01$, default betas, $\varepsilon$ negligible. The first step? What if the gradient were $-0.004$?

<details class="nb-hint">
<summary>Hint</summary>

After bias correction $\hat m_1 = g_1$ and $\hat v_1 = g_1^2$.

</details>

<details class="nb-sol">
<summary>Solution</summary>

The step is $\eta\, g/|g|$: the parameter rises by 0.01 in **both** cases. Adam's first step is independent of the gradient's size.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-dl-11">

<strong>Problem 11</strong> (Clipping)

Gradient $(6, -8, 0)$, threshold 5. Clip by norm, then by value.

<details class="nb-hint">
<summary>Hint</summary>

The norm is 10.

</details>

<details class="nb-sol">
<summary>Solution</summary>

By norm: scale by $5/10$, giving $(3, -4, 0)$, same direction. By value: $(5, -5, 0)$, a different direction.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-dl-12">

<strong>Problem 12</strong> (Momentum with a constant gradient)

PyTorch-style $v \leftarrow \beta v + g$ with constant $g$. The limiting step multiplier, and the number of steps to reach 90% of it, for $\beta = 0.9$ and $0.99$?

<details class="nb-hint">
<summary>Hint</summary>

$v_t = g(1 - \beta^t)/(1 - \beta)$.

</details>

<details class="nb-sol">
<summary>Solution</summary>

Limit $g/(1-\beta)$: $10g$ and $100g$. Need $\beta^t \le 0.1$: $t = 22$ for $\beta = 0.9$, $t = 230$ for $\beta = 0.99$.

</details>

</div>

## 13.3 Initialisation, normalisation, regularisation {#dl-13-3}

<div class="nb nb-problem nb-block" id="problem-dl-13">

<strong>Problem 13</strong> (Init numbers)

For a $512 \to 512$ fully connected layer: Xavier-uniform bound and He-normal standard deviation?

<details class="nb-hint">
<summary>Hint</summary>

$\sqrt{6/(n_{\text{in}} + n_{\text{out}})}$ and $\sqrt{2/n_{\text{in}}}$.

</details>

<details class="nb-sol">
<summary>Solution</summary>

$\sqrt{6/1024} = 0.0765$; $\sqrt{2/512} = 0.0625$.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-dl-14">

<strong>Problem 14</strong> (BatchNorm edge case and count)

(a) BatchNorm in training mode receives the batch $(4, 4, 4, 4)$ for one feature. Output, and what goes wrong? (b) Parameters of `Linear(256, 128, bias=False)` followed by `BatchNorm1d(128)`?

<details class="nb-hint">
<summary>Hint</summary>

(a) The variance is 0, and $\varepsilon$ prevents a division by zero.

</details>

<details class="nb-sol">
<summary>Solution</summary>

(a) $\hat x = 0$ for every example, so the output is $\beta$ for all four: the feature carries no information through this batch. (b) $256\cdot128 + 2\cdot128 = 33{,}024$ learnable (plus 256 running-statistics buffers). The linear bias is dropped because BN's $\beta$ replaces it.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-dl-15">

<strong>Problem 15</strong> (Which are true?)

(a) BatchNorm uses batch statistics at inference. (b) LayerNorm does not depend on the batch size. (c) Dropout increases model capacity. (d) Increasing $\lambda$ in $E + \lambda\sum w^2$ shrinks the weights. (e) He initialisation is designed for ReLU.

<details class="nb-hint">
<summary>Hint</summary>

Two are classic wrong options.

</details>

<details class="nb-sol">
<summary>Solution</summary>

(b), (d), (e).

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-dl-16">

<strong>Problem 16</strong> (Read the curves)

Training loss 0.02, validation loss 0.95 after 50 epochs; at epoch 8 the validation loss was 0.41. Diagnose and list three fixes in the order you would try them.

<details class="nb-hint">
<summary>Hint</summary>

Where did validation loss bottom out?

</details>

<details class="nb-sol">
<summary>Solution</summary>

Overfitting since about epoch 8. Fixes: early stopping (restore the epoch-8 checkpoint); more data or augmentation; regularisation (weight decay, dropout) or a smaller model.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-dl-17">

<strong>Problem 17</strong> (Dropout convention mismatch)

A network is trained with inverted dropout, $p = 0.2$, but deployed with the old convention (multiply activations by $1 - p$ at test time). By what factor are test activations off?

<details class="nb-hint">
<summary>Hint</summary>

Inverted dropout already compensated during training.

</details>

<details class="nb-sol">
<summary>Solution</summary>

Test activations are multiplied by 0.8 for no reason: 20% too small at every dropout layer.

</details>

</div>

## 13.4 Convolutional networks {#dl-13-4}

<div class="nb nb-problem nb-block" id="problem-dl-18">

<strong>Problem 18</strong> (A chain of layers)

$64\times64\times3$ input → conv $3\times3$, 32 filters, stride 1, padding 1 → max-pool $2\times2$ stride 2 → conv $5\times5$, 64 filters, stride 2, padding 2. Output shape and parameters after each layer.

<details class="nb-hint">
<summary>Hint</summary>

$\lfloor (n + 2p - k)/s\rfloor + 1$ and $(k^2C_{\text{in}} + 1)C_{\text{out}}$.

</details>

<details class="nb-sol">
<summary>Solution</summary>

$64\times64\times32$, $(27 + 1)\cdot32 = 896$. Pool: $32\times32\times32$, 0. Conv: $\lfloor (32 + 4 - 5)/2\rfloor + 1 = 16$, so $16\times16\times64$, $(25\cdot32 + 1)\cdot64 = 51{,}264$.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-dl-19">

<strong>Problem 19</strong> (Leftover pixels)

A $7\times7$ input, $3\times3$ kernel, stride 3, no padding. Output size? How many input pixels are never used?

<details class="nb-hint">
<summary>Hint</summary>

The floor discards what does not fit.

</details>

<details class="nb-sol">
<summary>Solution</summary>

$\lfloor 4/3\rfloor + 1 = 2$, so $2\times2$. The windows cover rows and columns 0–5; row 6 and column 6 are never read: $49 - 36 = 13$ pixels.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-dl-20">

<strong>Problem 20</strong> (Receptive field)

conv $3\times3$ (s1), conv $3\times3$ (s2), conv $3\times3$ (s1), max-pool $2\times2$ (s2), conv $3\times3$ (s1). Receptive field of the final unit?

<details class="nb-hint">
<summary>Hint</summary>

$r \leftarrow r + (k - 1)\,j$, then $j \leftarrow j\,s$, starting at $r = j = 1$.

</details>

<details class="nb-sol">
<summary>Solution</summary>

$r$: 3 ($j = 1$), 5 ($j$ becomes 2), 9, 11 ($j$ becomes 4), 19. **19 × 19.**

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-dl-21">

<strong>Problem 21</strong> (Depthwise-separable)

Parameters of a depthwise-separable $3\times3$ convolution $128 \to 256$ (biases on both parts), and of a standard $3\times3$ convolution?

<details class="nb-hint">
<summary>Hint</summary>

Depthwise: one $3\times3$ filter per input channel. Pointwise: a $1\times1$ convolution.

</details>

<details class="nb-sol">
<summary>Solution</summary>

Depthwise $9\cdot128 + 128 = 1{,}280$; pointwise $128\cdot256 + 256 = 33{,}024$; total 34,304. Standard $(9\cdot128 + 1)\cdot256 = 295{,}168$. About 8.6× fewer.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-dl-22">

<strong>Problem 22</strong> (IoU and NMS)

Box A $= (0, 0, 10, 10)$, box B $= (5, 0, 15, 10)$ as $(x_1, y_1, x_2, y_2)$. IoU? Does NMS at threshold 0.5 suppress the lower-scoring one?

<details class="nb-hint">
<summary>Hint</summary>

Union = area A + area B − intersection.

</details>

<details class="nb-sol">
<summary>Solution</summary>

Intersection $5\times10 = 50$; union $150$; IoU $0.333$. Below 0.5, so both boxes survive.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-dl-23">

<strong>Problem 23</strong> (Transposed convolution)

Output sizes: input 16, $k = 2$, $s = 2$, $p = 0$; and input 4, $k = 4$, $s = 2$, $p = 1$.

<details class="nb-hint">
<summary>Hint</summary>

$(n - 1)s - 2p + k$.

</details>

<details class="nb-sol">
<summary>Solution</summary>

$15\cdot2 + 2 = 32$; $3\cdot2 - 2 + 4 = 8$. Both double the size (the first is the U-Net decoder's upsampling step).

</details>

</div>

## 13.5 RNNs, Transformers and LLMs {#dl-13-5}

<div class="nb nb-problem nb-block" id="problem-dl-24">

<strong>Problem 24</strong> (LSTM count)

A single-layer LSTM with input size 100 and hidden size 128: parameters in PyTorch's convention (two bias vectors per gate block)?

<details class="nb-hint">
<summary>Hint</summary>

$4[H(D + H) + 2H]$.

</details>

<details class="nb-sol">
<summary>Solution</summary>

$128\cdot228 = 29{,}184$; plus $256$ gives 29,440; times 4: **117,760** (117,248 with one bias per block).

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-dl-25">

<strong>Problem 25</strong> (Bidirectional head)

A bidirectional single-layer LSTM with hidden size 64 feeds a linear layer classifying the final output into 5 classes. Input size and parameters of the linear layer?

<details class="nb-hint">
<summary>Hint</summary>

Both directions are concatenated.

</details>

<details class="nb-sol">
<summary>Solution</summary>

Input 128; $128\cdot5 + 5 = 645$ parameters.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-dl-26">

<strong>Problem 26</strong> (Attention by hand)

Queries $q_1 = (1, 0)$, $q_2 = (0, 2)$; keys $k_1 = (1, 1)$, $k_2 = (0, 1)$; values $v_1 = 10$, $v_2 = 20$; $d_k = 2$. Both outputs.

<details class="nb-hint">
<summary>Hint</summary>

Scores divided by $\sqrt2$, softmax per query, then a weighted average of the values.

</details>

<details class="nb-sol">
<summary>Solution</summary>

$q_1$: scores $(1, 0)/\sqrt2 = (0.707, 0)$, weights $(0.670, 0.330)$, output $13.3$. $q_2$: scores $(2, 2)/\sqrt2$, equal weights, output $15$.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-dl-27">

<strong>Problem 27</strong> (Block parameters)

Parameters of one multi-head self-attention block with $d_{\text{model}} = 256$, $h = 4$, and of the FFN with $d_{ff} = 1024$, biases included.

<details class="nb-hint">
<summary>Hint</summary>

The head count does not matter.

</details>

<details class="nb-sol">
<summary>Solution</summary>

Attention $4\cdot256^2 + 4\cdot256 = 263{,}168$. FFN $256\cdot1024 + 1024 + 1024\cdot256 + 256 = 525{,}568$: two thirds of the pair, as usual.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-dl-28">

<strong>Problem 28</strong> (Forgot to scale)

Scores for one query over four keys are $(8, 4, 0, -4)$ with $d_k = 64$, but someone forgot to divide by $\sqrt{d_k}$. Compare the weights with and without scaling.

<details class="nb-hint">
<summary>Hint</summary>

$\sqrt{64} = 8$.

</details>

<details class="nb-sol">
<summary>Solution</summary>

Unscaled: about $(0.982, 0.018, 0.0003, 0.00001)$, essentially one-hot (saturated, tiny gradients). Scaled $(1, 0.5, 0, -0.5)$: $(0.455, 0.276, 0.167, 0.102)$.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-dl-29">

<strong>Problem 29</strong> (Cross-attention shapes)

Decoder cross-attention with batch 2, target length 5, source length 9, $d_{\text{model}} = 32$, $h = 4$. Shapes of $Q$, $K$, $V$ (after splitting heads), the scores and the output.

<details class="nb-hint">
<summary>Hint</summary>

Queries come from the decoder, keys and values from the encoder; $d_k = 8$.

</details>

<details class="nb-sol">
<summary>Solution</summary>

$Q$: $(2, 4, 5, 8)$; $K, V$: $(2, 4, 9, 8)$; scores $(2, 4, 5, 9)$; output $(2, 5, 32)$.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-dl-30">

<strong>Problem 30</strong> (KV cache)

24 layers, 16 heads of size 64, fp16, a batch of 8 sequences of 2,048 tokens. KV-cache size? With grouped-query attention using 4 K/V heads?

<details class="nb-hint">
<summary>Hint</summary>

$2 \times L \times n_{\text{kv}} \times d_{\text{head}} \times T \times 2$ bytes per sequence.

</details>

<details class="nb-sol">
<summary>Solution</summary>

Per token $2\cdot24\cdot16\cdot64\cdot2 = 98{,}304$ bytes (96 KiB); per sequence 192 MiB; for 8 sequences **1.5 GiB**. With 4 K/V heads, a quarter: 384 MiB.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-dl-31">

<strong>Problem 31</strong> (LoRA)

LoRA with $r = 16$ on a $1024 \times 4096$ projection: trainable parameters and fraction of the matrix?

<details class="nb-hint">
<summary>Hint</summary>

$r(d_{\text{in}} + d_{\text{out}})$.

</details>

<details class="nb-sol">
<summary>Solution</summary>

$16\cdot5120 = 81{,}920$, i.e. $81920/4194304 = 1.95\%$.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-dl-32">

<strong>Problem 32</strong> (Decoding)

Logits $(2, 1, 0)$. Sampling distribution with temperature 0.5; with top-$k$, $k = 1$; with top-$p$, $p = 0.5$. Which are deterministic?

<details class="nb-hint">
<summary>Hint</summary>

Softmax of $(2, 1, 0)$ is $(0.665, 0.245, 0.090)$.

</details>

<details class="nb-sol">
<summary>Solution</summary>

$T = 0.5$: softmax of $(4, 2, 0)$ = $(0.867, 0.117, 0.016)$. Top-1: $(1, 0, 0)$. Top-$p$ 0.5: the first token alone already has 0.665, so $(1, 0, 0)$. The last two are deterministic (greedy).

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-dl-33">

<strong>Problem 33</strong> (Perplexity)

A language model gives the three tokens of a test sentence probabilities 0.2, 0.5 and 0.1. Perplexity?

<details class="nb-hint">
<summary>Hint</summary>

The inverse geometric mean of the probabilities.

</details>

<details class="nb-sol">
<summary>Solution</summary>

$(0.2\cdot0.5\cdot0.1)^{-1/3} = 0.01^{-1/3} = 4.64$.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-dl-34">

<strong>Problem 34</strong> (Training memory)

Estimate weights, gradients and Adam state for training a 1.3B-parameter model in mixed precision.

<details class="nb-hint">
<summary>Hint</summary>

About 16 bytes per parameter.

</details>

<details class="nb-sol">
<summary>Solution</summary>

$1.3\times10^9 \times 16 \approx 21$ GB, before activations.

</details>

</div>

## 13.6 Generative models {#dl-13-6}

<div class="nb nb-problem nb-block" id="problem-dl-35">

<strong>Problem 35</strong> (VAE KL)

Compute $\text{KL}(\mathcal N(0, 4)\,\|\,\mathcal N(0, 1))$ and $\text{KL}(\mathcal N(2, 1)\,\|\,\mathcal N(0, 1))$.

<details class="nb-hint">
<summary>Hint</summary>

$\tfrac12(\mu^2 + \sigma^2 - 1 - \ln\sigma^2)$.

</details>

<details class="nb-sol">
<summary>Solution</summary>

$\tfrac12(4 - 1 - \ln 4) = 0.807$; $\tfrac12(4 + 1 - 1 - 0) = 2$.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-dl-36">

<strong>Problem 36</strong> (GAN)

The discriminator outputs 0.5 everywhere at the optimum. What does that say about the generator?

<details class="nb-hint">
<summary>Hint</summary>

$D^\star = p_{\text{data}}/(p_{\text{data}} + p_g)$.

</details>

<details class="nb-sol">
<summary>Solution</summary>

$D^\star = 0.5$ everywhere means $p_g = p_{\text{data}}$: the generator has matched the data distribution, and the Jensen–Shannon divergence is 0.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-dl-37">

<strong>Problem 37</strong> (Diffusion)

In DDPM with $\bar\alpha_t = 0.25$, write $x_t$ in terms of $x_0$ and $\varepsilon$, and give the signal-to-noise ratio $\bar\alpha_t/(1 - \bar\alpha_t)$.

<details class="nb-hint">
<summary>Hint</summary>

$x_t = \sqrt{\bar\alpha_t}x_0 + \sqrt{1 - \bar\alpha_t}\,\varepsilon$.

</details>

<details class="nb-sol">
<summary>Solution</summary>

$x_t = 0.5\,x_0 + 0.866\,\varepsilon$; SNR $= 0.25/0.75 = 1/3$.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-dl-38">

<strong>Problem 38</strong> (ViT tokens)

A ViT with $14\times14$ patches on a $224\times224$ image: number of tokens including `[CLS]`, and the shape of each head's attention matrix?

<details class="nb-hint">
<summary>Hint</summary>

$224/14 = 16$ patches per side.

</details>

<details class="nb-sol">
<summary>Solution</summary>

$16^2 + 1 = 257$ tokens; attention matrix $257\times257$ per head.

</details>

</div>
