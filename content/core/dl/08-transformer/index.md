---
title: "8 · Attention and the Transformer"
linkTitle: "8 Transformer"
weight: 8
math: true
---
The Transformer is the architecture behind essentially every large language model and much of modern vision and speech, and the most common "explain it / implement it" request in ML interviews. This chapter builds it piece by piece with the shapes written out, says why the scores are divided by $\sqrt{d_k}$, counts parameters, and then puts your from-scratch translation model in that vocabulary.

## 8.1 Attention as a soft dictionary lookup {#dl-8-1}

A dictionary returns the value whose key **equals** the query. Attention returns a **blend** of all values, weighted by how well each key matches the query:

$$\text{output} = \sum_i \alpha_i v_i, \qquad \alpha_i = \text{softmax}_i\big(\text{score}(q, k_i)\big).$$

Because the weights come from a softmax, the lookup is differentiable and learnable. Attention entered deep learning to fix the **seq2seq bottleneck** (chapter 7): instead of squeezing the source into one vector, the decoder at each step takes a fresh weighted average of all encoder states. **Additive (Bahdanau)** attention scores with a small network; **multiplicative (Luong)** with a dot product. The Transformer keeps the dot product, adds a scale, and uses attention between positions of the **same** sequence (**self-attention**) as its main operation, dropping recurrence entirely.

## 8.2 Scaled dot-product attention {#dl-8-2}

With queries, keys and values stacked as rows, $Q \in \mathbb R^{T_q\times d_k}$, $K \in \mathbb R^{T_k \times d_k}$, $V \in \mathbb R^{T_k\times d_v}$:

$$\text{Attention}(Q, K, V) = \text{softmax}\!\left(\frac{QK^\top}{\sqrt{d_k}}\right) V.$$

The score matrix is $T_q \times T_k$; the softmax runs over each row (over keys), so each row of weights sums to 1; the output is $T_q \times d_v$.

**Why divide by $\sqrt{d_k}$.** If the components of $q$ and $k$ are independent with mean 0 and variance 1, then $q^\top k = \sum_{i=1}^{d_k} q_i k_i$ has mean 0 and **variance $d_k$**. For $d_k = 64$ the scores have standard deviation 8, the softmax becomes nearly one-hot, its Jacobian $\text{diag}(p) - pp^\top$ is nearly zero, and gradients through the attention weights vanish. Dividing by $\sqrt{d_k}$ restores unit variance whatever the head size.

<div class="nb nb-remark">

<strong>Trap</strong> — "We divide by $\sqrt{d_k}$ to normalise the attention weights" (the softmax already does that) or "to reduce computation". The reason is the **variance of the dot product**: scaling keeps the softmax out of saturation so gradients flow. It is $\sqrt{d_k}$, not $d_k$, because the standard deviation scales with the square root of the variance.

</div>

**Masks** set blocked scores to $-\infty$ **before** the softmax, so blocked positions get weight exactly 0 and rows still sum to 1:

- **Causal (look-ahead) mask:** query $i$ may attend only to keys $j \le i$. Needed in decoders so a position cannot see the token it is trained to predict; it is what lets a whole sequence be trained in parallel with teacher forcing.
- **Padding mask:** padding positions in a batch are blocked as keys.

<div class="nb nb-remark">

<strong>Trap</strong> — Masking *after* the softmax (multiplying weights by 0/1) leaves rows that no longer sum to one. And the causal mask is needed in training precisely because future tokens *are* present then.

</div>

## 8.3 Multi-head attention {#dl-8-3}

One attention pattern per layer is limiting (a word may need its syntactic head, its coreferent and the previous word at once). **Multi-head attention** runs $h$ attentions in parallel on learned projections of size $d_k = d_{\text{model}}/h$ and concatenates them:

| Step | Shape |
|---|---|
| input $X$ | $(B, T, d_{\text{model}})$ |
| $Q, K, V = XW_Q, XW_K, XW_V$ | $(B, T, d_{\text{model}})$ each |
| split into heads | $(B, h, T, d_k)$ |
| scores $QK^\top/\sqrt{d_k}$ (+ mask) | $(B, h, T, T)$ |
| softmax, times $V$ | $(B, h, T, d_k)$ |
| merge heads, output projection $W_O$ | $(B, T, d_{\text{model}})$ |

**Parameters:** four $d_{\text{model}} \times d_{\text{model}}$ projections with biases, $4d_{\text{model}}^2 + 4d_{\text{model}}$: 1,050,624 for $d_{\text{model}} = 512$. **Independent of $h$**: more heads means smaller heads, not more parameters.

<div class="nb nb-remark">

<strong>Trap</strong> — Self-attention without positional information is **permutation-equivariant**: shuffle the tokens and the outputs shuffle the same way. "The dog bit the man" and "the man bit the dog" would give the same set of vectors. That is why positional encodings are not optional.

</div>

## 8.4 Positional encodings {#dl-8-4}

- **Sinusoidal** (original): $PE_{p,2i} = \sin(p/10000^{2i/d})$, $PE_{p,2i+1} = \cos(\cdot)$, added to the embeddings. Each pair of dimensions is a clock at its own frequency; shifting by $k$ positions is a fixed rotation, so relative offsets are linearly accessible. No parameters, defined for any length.
- **Learned absolute** embeddings (BERT, GPT-2): a trainable table, undefined beyond the maximum length.
- **RoPE** (rotary): rotate query and key pairs by an angle proportional to position, so their dot product depends only on the **relative** offset. Used by many recent LLMs.
- **ALiBi:** no embeddings; add a penalty proportional to $|i - j|$ to the scores, per head. Designed to extrapolate to longer sequences.

## 8.5 The Transformer block, encoder and decoder {#dl-8-5}

Each layer has two kinds of sublayer, each wrapped in a **residual connection** and **LayerNorm**:

- **Self-attention** mixes information **across positions**.
- A **position-wise feed-forward network** $\text{FFN}(x) = W_2\,\phi(W_1 x + b_1) + b_2$, the same MLP at every position, with hidden size $d_{ff}$ (typically $4d_{\text{model}}$) and ReLU or GELU. It mixes information **across features** and holds about two thirds of the parameters.

**Post-LN** (original): $X \leftarrow \text{LN}(X + \text{Sublayer}(X))$. **Pre-LN** (most modern models): $X \leftarrow X + \text{Sublayer}(\text{LN}(X))$, which keeps a clean identity path, trains more stably at depth and is far less sensitive to warm-up.

The **decoder** layer has three sublayers: **masked** self-attention over the target prefix, **cross-attention** (queries from the decoder; keys and values from the encoder output), and the FFN. Cross-attention scores have shape $(B, h, T_{\text{tgt}}, T_{\text{src}})$. The output layer often shares weights with the input embedding (**weight tying**).

| Family | Attention | Use |
|---|---|---|
| Encoder-only (BERT) | bidirectional | understanding: classification, retrieval |
| Decoder-only (GPT) | causal | generation |
| Encoder–decoder (original, T5) | both + cross | sequence-to-sequence, e.g. translation |

## 8.6 Counting and cost {#dl-8-6}

- **Encoder layer:** attention $4d^2 + 4d$, FFN $2d\,d_{ff} + d_{ff} + d$, two LayerNorms $4d$. With $d_{ff} = 4d$ that is about $12d^2$: a third in attention, two thirds in the FFN. For $d = 512$, $d_{ff} = 2048$: 3,152,384.
- **Decoder layer:** one more attention block and LayerNorm.
- **Rule of thumb** for big models: about $12 L d^2$ plus embeddings ($V \times d$).
- **Complexity per layer:** projections and FFN $O(n d^2)$; the score matrix $O(n^2 d)$ time and $O(n^2)$ memory per head. Attention dominates once $n > 2d$, which motivates sparse, linear and windowed attention and FlashAttention.

| Layer type | Cost per layer | Sequential steps | Longest path between positions |
|---|---|---|---|
| Self-attention | $O(n^2 d)$ | $O(1)$ | $O(1)$ |
| Recurrent | $O(n d^2)$ | $O(n)$ | $O(n)$ |
| Convolution, kernel $k$ | $O(k n d^2)$ | $O(1)$ | $O(\log_k n)$ dilated |

**KV cache:** at generation, keys and values of past tokens never change (causal mask), so they are stored per layer and head; each new token computes only its own $q, k, v$. Memory $= 2 \times L \times n_{\text{kv heads}} \times d_{\text{head}} \times T \times$ bytes. **Multi-query** (one shared K/V head) and **grouped-query** attention shrink it. **FlashAttention** computes exact attention block by block with an online softmax, never materialising the $n\times n$ matrix: same FLOPs, far less memory traffic.

<div class="nb nb-remark">

<strong>Trap</strong> — "The KV cache stores attention weights" or "queries". It stores **keys and values** of past tokens; weights are recomputed each step because the new query changes them. It speeds up **generation**, not training.

</div>

## 8.7 In my project: a Transformer from scratch for German → English {#dl-8-7}

<div class="nb nb-remark">

<strong>In my project</strong> — [DA6401 Assignment 3](../../../projects/transformer/): the original encoder–decoder Transformer implemented **from scratch** in PyTorch (`nn.MultiheadAttention` not allowed), trained on **Multi30k** (about 29k short caption pairs) for German → English translation.

</div>

| | |
|---|---|
| Configuration | 3 encoder + 3 decoder layers, $d_{\text{model}} = 256$, 8 heads (so $d_k = 32$), $d_{ff} = 512$ |
| Size | 8,988,165 trainable parameters |
| Training | Adam, **Noam** schedule (4,000 warm-up steps), **label smoothing** $\varepsilon = 0.1$, teacher forcing, Kaggle T4 GPUs |
| Decoding and metric | **greedy** decoding; corpus **BLEU** with SacreBLEU |
| Result | best validation BLEU **39.76** (30-epoch run, epoch 22); six runs of the 15-epoch configuration: test BLEU **38.03 ± 0.73** |
| Ablations | removing $1/\sqrt{d_k}$ cost about **5 BLEU**; learned positional embeddings about **2 BLEU** worse than sinusoidal; label smoothing no difference beyond noise |

Things an interviewer can push on, with short answers:

- **What did you implement yourself?** Scaled dot-product and multi-head attention with masks, sinusoidal positional encodings, the encoder and decoder stacks with residuals and LayerNorm, the label-smoothed loss, the Noam schedule and greedy decoding.
- **Which masks, where?** A padding mask on the source keys in encoder self-attention and cross-attention; padding plus causal mask in decoder self-attention.
- **Post-LN or pre-LN?** Post-LN, as in the original paper, plus an extra final LayerNorm that really belongs to the pre-LN design: redundant, since every post-LN layer already ends with a LayerNorm. A good "what would you change" answer.
- **Positions:** a sinusoidal table stored as a buffer (not counted in the parameters), with embeddings multiplied by $\sqrt{d_{\text{model}}}$ so they are not tiny next to the encoding's unit-sized entries.
- **Why did removing the scaling hurt by 5 BLEU?** Section 8.2: with $d_k = 32$ unscaled scores have standard deviation about 5.7, the softmax saturates and attention gradients vanish.
- **The warm-up trap.** One epoch was 227 steps, so warm-up lasted about 17.6 epochs; the 15-epoch runs never reached the peak learning rate (chapter 4).
- **Greedy vs beam search.** The assignment asked for greedy; the original paper used beam size 4. Beam search would likely add a little BLEU at $k$ times the decoding cost.
- **An honest BLEU caveat.** References and outputs were lower-cased and spaCy-tokenised, while SacreBLEU expects detokenised text and warns about it. The numbers are comparable across the project's own runs, not directly with published Multi30k BLEU.
- **BLEU itself** is a brevity penalty times the geometric mean of clipped n-gram precisions; it rewards surface overlap and misses paraphrases (chapter 9).

<div class="nb nb-moral">

Attention is a softmax-weighted average of values, with weights from query–key dot products scaled by $\sqrt{d_k}$ to keep the softmax soft. A Transformer layer is attention (mix positions) plus an MLP (mix features), each wrapped in a residual and LayerNorm; positions must be injected; cost is quadratic in length.

</div>
