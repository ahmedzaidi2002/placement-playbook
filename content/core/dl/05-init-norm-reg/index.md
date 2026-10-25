---
title: "5 · Initialisation, normalisation and regularisation"
linkTitle: "5 Init, norm, regularisation"
weight: 5
math: true
---
Three families of tricks keep deep networks trainable and stop them memorising: the scale of the initial weights, layers that renormalise activations, and penalties or noise that restrict what the network can fit. The OA questions are short but have popular wrong answers ("BatchNorm behaves the same at inference", "dropout increases capacity", "what does $\lambda$ do"); interviews ask why each one works.

## 5.1 Initialisation: Xavier and He {#dl-5-1}

All-equal weights never break symmetry (chapter 3), so weights must be random. But the **scale** matters: each layer multiplies the activation scale by some gain, and over $L$ layers the gains multiply. For $z = \sum_i W_i h_i$ with $n$ inputs, $\text{Var}(z) = n\,\sigma_w^2\,\mathbb E[h^2]$, so:

| Scheme | Weight variance | For |
|---|---|---|
| **Xavier (Glorot)** | $\dfrac{2}{n_{\text{in}} + n_{\text{out}}}$ (uniform bound $\sqrt{6/(n_{\text{in}} + n_{\text{out}})}$) | tanh, roughly linear activations |
| **He (Kaiming)** | $\dfrac{2}{n_{\text{in}}}$ | ReLU, which zeroes half its input |

<div class="nb nb-example">

<strong>Example</strong> (A 256 → 128 layer, and 50 layers deep)

Xavier uniform bound $\sqrt{6/384} = 0.125$; He normal std $\sqrt{2/256} = 0.088$. Through 50 ReLU layers of width 256: with std $\sqrt{1/n}$ the activations shrink to $4\times10^{-8}$ of their input scale (a factor $1/\sqrt2$ per layer); with He they stay about 1; with $\sqrt{3/n}$ they explode to $3\times10^4$.

</div>

<div class="nb nb-remark">

<strong>Trap</strong> — "Use Xavier for ReLU networks." Xavier assumes a roughly linear activation; ReLU discards half the signal and needs He's factor 2. (He for tanh saturates the units.) Biases are usually initialised to 0; the random weights already break symmetry.

</div>

## 5.2 Batch normalisation {#dl-5-2}

For each feature (each channel, for convolutions, pooled over the spatial positions too), over the mini-batch:

$$\hat x_i = \frac{x_i - \mu_B}{\sqrt{\sigma_B^2 + \varepsilon}}, \qquad y_i = \gamma\,\hat x_i + \beta,$$

with learnable $\gamma$ (scale) and $\beta$ (shift) per feature, so the layer can undo the normalisation if that is better: BN does not reduce what the layer can represent.

<div class="nb nb-example">

<strong>Example</strong> (BatchNorm by hand)

One feature takes 1, 2, 3, 6 in a batch: mean 3, variance 3.5 (divide by $B$), so the outputs are $(-1.07, -0.53, 0, 1.60)$. A second feature that is the first times ten gives the **same** $\hat x$: BN is invariant to the scale of its input.

</div>

**Train versus inference.** At inference there may be one example, and predictions must not depend on the rest of the batch. So during training BN keeps **running averages** of mean and variance (PyTorch: momentum 0.1, starting at mean 0 and variance 1, updated with the unbiased variance), and in `eval()` mode it uses those instead. After the batch above, the running mean is $0.9\cdot 0 + 0.1\cdot 3 = 0.3$, so at inference the input 3, which mapped to 0 inside the batch, maps to about 2.31.

<div class="nb nb-remark">

<strong>Trap</strong> — "BatchNorm behaves the same at training and inference." It does not: training uses the current batch's statistics (and updates the running averages), inference uses the frozen running averages. **Forgetting `model.eval()`** changes predictions and keeps corrupting the running statistics: the most common BN bug. A training-mode batch of one cannot be normalised at all.

</div>

**Why BN helps:** the original story is "reducing internal covariate shift". Later analysis suggests the main benefit is a **smoother, better-conditioned loss landscape** that tolerates much larger learning rates; the honest interview answer mentions both and says the second has more support. Side effects: mild regularisation from batch noise, and a **bias before BN is redundant** (BN subtracts the mean; $\beta$ takes its place). A 10-layer sigmoid MLP stuck near $\ln 2$ without BN trained fine with it, even at a 10× larger learning rate.

## 5.3 LayerNorm, GroupNorm, RMSNorm {#dl-5-3}

The normalisation layers differ only in **which axes** the mean and variance are taken over:

| Layer | Normalises over | Notes |
|---|---|---|
| BatchNorm | each channel, across the batch (and space) | depends on the batch; running stats; weak with small batches |
| **LayerNorm** | each example, across its features | no batch dependence; identical in train and test; **the standard in Transformers and RNNs** |
| InstanceNorm | each example and channel, across space | style transfer |
| GroupNorm | each example, across groups of channels | tiny batches (detection, segmentation) |
| RMSNorm | like LayerNorm without centring or $\beta$ | cheaper; many recent LLMs |

Each has $2C$ learnable parameters ($\gamma$, $\beta$). `BatchNorm2d(64)` has 128 parameters plus 128 non-learnable buffers (running mean and variance).

## 5.4 Dropout {#dl-5-4}

During training, zero each unit independently with probability $p$. **Inverted dropout**, used by every framework, divides the survivors by $1 - p$, so the expected activation is unchanged and **nothing happens at test time**.

<div class="nb nb-example">

<strong>Example</strong> (Inverted dropout)

$p = 0.5$, mask $(1, 0, 1, 0)$: activations $(2, 4, 6, 8)$ become $(4, 0, 12, 0)$ in training and stay $(2, 4, 6, 8)$ at test time.

</div>

**Why it regularises:** no unit can rely on a specific other unit (it discourages co-adapted features), and each step trains one of $2^n$ thinned sub-networks that share weights, so the test-time network approximates an average of an exponential ensemble.

<div class="nb nb-remark">

<strong>Trap</strong> — "Dropout is applied at test time" or "multiply the weights by $p$ at test time". With inverted dropout nothing happens at test time; the *original* formulation scaled by the keep probability $1 - p$ at test instead. Keeping dropout on at test time on purpose is **MC dropout**, a different technique for uncertainty estimates.

</div>

Dropout preserves the **mean** but not the **variance** of activations, so a BatchNorm placed after dropout sees a different variance at test time than in training (the "variance shift").

<div class="nb nb-remark">

<strong>In my project</strong> (VGG11) — The [VGG11](../../../projects/vgg11/) had to use a **hand-written dropout** (no `nn.Dropout`): inverted dropout, element-wise. Where it sits and why, which is what an interviewer will ask:

- **Only after BN + ReLU of the first two fully connected layers**, where nearly all the parameters are and co-adaptation is worst.
- **Not in the convolutional blocks:** convolutional features are spatially correlated, so dropping single activations barely regularises them (spatial dropout would drop whole channels), and weight sharing already regularises.
- **The U-Net has no dropout at all.**
- An honest caveat: the second `BatchNorm1d` follows a linear layer that consumed dropped-out inputs, so it is exposed to the variance shift above.
- Convolutions were initialised with **Kaiming normal** (ReLU gain), biases 0, because the network was trained from scratch with no pretrained weights.

</div>

## 5.5 Weight decay: the λ in E + λΣw² {#dl-5-5}

Adding $\lambda\|w\|^2$ to the training error pulls weights towards 0; one SGD step multiplies them by $1 - 2\eta\lambda$ before the data gradient acts, hence **weight decay**. Small weights mean a smoother function: larger $\lambda$ trades higher bias for lower variance. On a degree-9 polynomial fitted to 12 noisy points, test MSE was 6.55 at $\lambda = 10^{-8}$, 0.09 at the best $\lambda$, and 0.39 at $\lambda = 10$.

<div class="nb nb-remark">

<strong>Trap</strong> — "Increasing $\lambda$ increases model complexity" or "decreases training error": both backwards. Larger $\lambda$: smaller weights, simpler effective model, higher training error, and (up to a point) lower test error. Biases are normally not penalised. Under Adam, use AdamW (chapter 4).

</div>

## 5.6 Other regularisers, and reading the curves {#dl-5-6}

- **Data augmentation:** label-preserving transformations (crops, flips, colour jitter; for text, back-translation or masking). Often the strongest regulariser for vision.
- **Early stopping:** watch validation loss, keep the best checkpoint, stop after a patience. It behaves much like L2.
- **Label smoothing, mixup** (train on blends of two examples and their labels), **stochastic depth**, ensembling, weight sharing, smaller models.

| Curves | Diagnosis | Remedies |
|---|---|---|
| Training loss keeps falling, validation bottoms out and rises | **overfitting** | more data or augmentation, regularisation, early stopping, smaller model |
| Both plateau high, small gap | **underfitting** | bigger model, longer training, less regularisation, better features |

<div class="nb nb-remark">

<strong>Trap</strong> — Validation loss *below* training loss is not a bug by itself: dropout and augmentation are on when the training loss is recorded, and the training loss is averaged over an epoch in which the model was still improving. It becomes a bug when the validation set overlaps the training set.

</div>

<div class="nb nb-moral">

Initialise so signals neither vanish nor explode (He for ReLU); normalise (BN for CNNs, LN for Transformers); regularise with decoupled weight decay, dropout and augmentation; and read the gap between the two curves before reaching for any of them.

</div>
