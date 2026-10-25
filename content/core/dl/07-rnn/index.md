---
title: "7 · Recurrent networks"
linkTitle: "7 RNNs"
weight: 7
math: true
---
Text, speech, sensor streams and prices arrive as sequences of varying length, where an element's meaning depends on what came before. Recurrent networks carry a hidden state from step to step. OAs ask why feedback connections help, why LSTMs suit time series, and LSTM parameter counts; interviews ask for the gates, why gradients vanish through time, and why Transformers replaced RNNs.

## 7.1 The vanilla RNN {#dl-7-1}

$$h_t = \tanh(W_{xh} x_t + W_{hh} h_{t-1} + b), \qquad \hat y_t = W_{hy} h_t, \qquad h_0 = 0.$$

The **feedback** connection $W_{hh}h_{t-1}$ makes $h_t$ a summary of $x_1, \dots, x_t$, so the output can depend on the whole past. The **same weights** are used at every step (weight sharing along time), so one network handles any length with a fixed number of parameters. Unrolled, an RNN is a deep feed-forward network with one layer per time step and tied weights.

<div class="nb nb-example">

<strong>Example</strong> (Three steps by hand)

One unit, $w_x = 0.5$, $w_h = 0.8$, no bias, inputs $1, 0.5, -1$: $h_1 = \tanh(0.5) = 0.462$; $h_2 = \tanh(0.25 + 0.8\cdot0.462) = 0.551$; $h_3 = \tanh(-0.5 + 0.8\cdot0.551) = -0.059$.

</div>

<div class="nb nb-remark">

<strong>Trap</strong> — "Why are feedback connections used in RNNs?" Not to speed up training or reduce overfitting: they let the network carry information from earlier inputs to later steps (memory), so outputs depend on context and any length is handled with fixed weights.

</div>

## 7.2 Backpropagation through time {#dl-7-2}

Training unrolls the network over the sequence and backpropagates through the unrolled graph (**BPTT**); because the weights are shared, the gradient for $W_{hh}$ is the **sum** of its gradients at every step. The gradient reaching an early state is a product of $T - k$ Jacobians with the **same** matrix $W_{hh}$ and tanh derivatives, so it **vanishes or explodes exponentially in the time lag**. With $W_{hh}$ scaled to spectral radius 0.9, the gradient 59 steps back is about $10^{-15}$ of the one at the end. Even radius 1.5 vanished, because large weights saturate the tanh.

Remedies: **gradient clipping by norm** for explosions (standard for RNNs); **truncated BPTT** (backpropagate only $k$ steps; cheaper, but blind to longer dependencies); orthogonal initialisation of $W_{hh}$; and above all **gated cells**.

## 7.3 LSTM and GRU {#dl-7-3}

The **LSTM** adds a cell state $c_t$ and three sigmoid gates computed from $x_t$ and $h_{t-1}$:

| Gate | Role |
|---|---|
| forget $f_t$ | how much of the old cell to **keep** |
| input $i_t$ | how much new content to **write** |
| candidate $g_t$ (tanh) | the content to write |
| output $o_t$ | how much of the cell to **expose** as $h_t$ |

$$c_t = f_t \odot c_{t-1} + i_t \odot g_t, \qquad h_t = o_t \odot \tanh(c_t).$$

**Why it remembers:** the cell is updated **additively**. Along the cell path the gradient is multiplied only by the forget gate, $\partial c_t/\partial c_{t-1} = \text{diag}(f_t)$: no repeated matrix product and no tanh squashing in between. With $f = 0.95$ a signal survives 50 steps at 0.077; a vanilla path with factor at most 0.5 gives $10^{-15}$. It is the ResNet shortcut idea applied in time.

<div class="nb nb-example">

<strong>Example</strong> (One LSTM step, scalar state)

$x = 1$, $h_{t-1} = 0$, $c_{t-1} = 0.5$, input weights 0.5, 1, 1, 0.5 for $i, f, g, o$, everything else 0: $i = \sigma(0.5) = 0.62$, $f = \sigma(1) = 0.73$, $g = \tanh 1 = 0.76$, $o = 0.62$; $c_t = 0.73\cdot0.5 + 0.62\cdot0.76 = 0.84$; $h_t = 0.62\tanh(0.84) = 0.43$.

</div>

At a default initialisation the forget gate sits near $\sigma(0) = 0.5$ and an LSTM forgets as fast as a vanilla RNN. **Initialising the forget-gate bias to a positive value** (1 or more) is a standard trick for this reason.

**GRU:** merges cell and hidden state and uses two gates, an **update** gate $z$ that interpolates between keeping the old state and writing the candidate (the same additive path), and a **reset** gate $r$ deciding how much of the past feeds the candidate. Fewer parameters, often similar accuracy.

<div class="nb nb-theorem nb-block">

<strong>Parameter counts</strong> (input size $D$, hidden size $H$, one bias per gate block)

$$\text{RNN: } H(D + H) + H, \qquad \text{GRU: } 3\big[H(D + H) + H\big], \qquad \text{LSTM: } 4\big[H(D + H) + H\big].$$

PyTorch keeps two bias vectors per block, adding another $H$, $3H$ or $4H$. A bidirectional layer doubles the count; a stacked layer $l > 1$ has input size $H$ (or $2H$ if the layer below is bidirectional).

</div>

<div class="nb nb-example">

<strong>Example</strong> (LSTM, $D = 50$, $H = 64$)

One bias: $4[64\cdot114 + 64] = 4\cdot7{,}360 = 29{,}440$. PyTorch convention: $+ 256 = 29{,}696$. A GRU of the same size: $3\cdot7{,}360 = 22{,}080$ (PyTorch $22{,}272$).

</div>

<div class="nb nb-remark">

<strong>Trap</strong> — "LSTMs solve the vanishing gradient problem completely." They mitigate it along the cell path while the forget gate stays open; with $f < 1$ the signal still decays, and the path through $h$ still vanishes. They do not fix exploding gradients either: clip.

</div>

## 7.4 Sequence-to-sequence, teacher forcing, beam search {#dl-7-4}

- **Patterns:** many-to-one (classification), many-to-many aligned (tagging), and many-to-many unaligned: the **encoder–decoder (seq2seq)**, where an encoder reads the source into a final state that initialises a decoder generating the target token by token. Squeezing a whole sentence into one vector is the **bottleneck that attention removes** (chapter 8).
- **Bidirectional** RNNs (one reads left to right, one right to left) help whenever the whole input is available (tagging, encoding), but not for left-to-right generation.
- **Teacher forcing:** during training, feed the decoder the **true** previous token, not its own prediction. Stable and parallel across time for the loss, but at inference the model must consume its own outputs, a distribution it never saw: **exposure bias**; early mistakes compound. Scheduled sampling is one mitigation.
- **Decoding:** **greedy** takes the best token each step; **beam search** keeps the $k$ best partial sequences by total log-probability.

<div class="nb nb-example">

<strong>Example</strong> (Greedy is not optimal)

First token probabilities $a{:}\,0.5$, $b{:}\,0.4$. After $a$ the best next token has 0.4; after $b$ it has 0.9. Greedy picks $a$ and ends with probability 0.08 over three steps; beam search with $k = 2$ keeps $b$ alive and finds a sequence of probability 0.144, the true optimum.

</div>

Beam search favours short outputs (each token multiplies by a probability below 1), so scores are length-normalised. For open-ended generation, sampling (chapter 9) is less repetitive.

## 7.5 RNNs for time series, and where Transformers win {#dl-7-5}

**Why LSTMs suit time series:** ordered processing, variable-length history, **constant cost per new observation** without reprocessing history, gates that keep slow trends while reacting to recent changes, modest data and memory needs. Still, strong baselines (seasonal naive, exponential smoothing, gradient-boosted trees on lag features) are hard to beat and should be tried first.

**Where Transformers win:** **parallelism** (an RNN must compute $h_1, h_2, \dots$ in order; attention processes all positions of a training sequence at once); **path length** (positions $i$ and $j$ interact in one attention step instead of $|i - j|$ recurrent steps, so long-range dependencies are easier); **scaling** with data and compute. Their cost: attention is quadratic in length and generation needs a growing KV cache, not a fixed-size state; this is why recurrent and state-space models remain alive for very long sequences and streaming.

**CTC** (speech, handwriting) lets a network emit one symbol or a blank per frame when the alignment is unknown: merge repeats, then delete blanks (`hh-e-ll-ll-oo` → `hello`); the blank allows genuine double letters.

<div class="nb nb-moral">

An RNN is a deep network unrolled in time with tied weights; its gradients are repeated matrix products, hence vanishing and exploding. LSTM and GRU add an additive, gated memory path; Transformers replace recurrence with attention for parallelism and short paths.

</div>
