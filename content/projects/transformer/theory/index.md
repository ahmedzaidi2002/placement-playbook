---
title: "1.2 · Theory and background"
linkTitle: "1.2 Theory and background"
weight: 2
math: true
---
This section is the minimum theory needed to understand every line of the implementation. Everything is stated for the configuration I actually used: $d_{\text{model}} = 256$, $h = 8$ heads, $d_k = d_{\text{model}}/h = 32$, $d_{\text{ff}} = 512$, $N = 3$ layers.

## 1.2.i Sequence-to-sequence and teacher forcing {#s1-2-i}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> predicting <em>“roof”</em> from the German sentence and the English prefix <em>“people repair the”</em>.</em>

</div>

A translation model defines the probability of an English sentence $\bm{y} = (y_1, \dots, y_m)$ given a German sentence $\bm{x}$ one token at a time:

$$
p(\bm{y} \mid \bm{x}) = \prod_{t=1}^{m} p(y_t \mid y_1, \dots, y_{t-1}, \bm{x}).
$$

The <strong>encoder</strong> reads $\bm{x}$ once and produces one vector per source token (the <strong>memory</strong>); the <strong>decoder</strong> reads the English prefix and the memory and outputs a distribution over the next English word.

<div class="nb nb-definition" id="definition-1-2-1">

<strong>Definition 1.2.1</strong>. In <strong>teacher forcing</strong>, the decoder is trained on the <em>true</em> prefix, not on its own predictions. If the target is $[\texttt{<sos>}, y_1, \dots, y_m, \texttt{<eos>}]$, the decoder input is everything except the last token and the gold output is everything except the first, so position $t$ is trained to predict the token after it.

</div>

This is exactly `train.py:89-90`: `tgt_input = tgt_batch[:, :-1]` and `tgt_gold = tgt_batch[:, 1:]`. Because of the causal mask (below) all $m+1$ positions are trained in parallel in a single forward pass.

## 1.2.ii Scaled dot-product attention {#s1-2-ii}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> the query for <em>“lädt”</em> (loads) scoring every German token as a key.</em>

</div>

<div class="nb nb-definition" id="definition-1-2-2">

<strong>Definition 1.2.2</strong>. Given queries $\bm{Q} \in \mathbb R^{n_q \times d_k}$, keys $\bm{K} \in \mathbb R^{n_k \times d_k}$ and values $\bm{V} \in \mathbb R^{n_k \times d_v}$,

$$
\operatorname{Attention}(\bm{Q}, \bm{K}, \bm{V}) = \operatorname{softmax}\!\left( \frac{\bm{Q} \bm{K}^{\top}}{\sqrt{d_k}} \right) \bm{V},
$$

with the softmax taken along each row. Row $i$ of the $n_q \times n_k$ matrix $\bm{A} = \operatorname{softmax}(\bm{Q}\bm{K}^{\top} / \sqrt{d_k})$ is a probability distribution saying how much query $i$ looks at each key; the output row $i$ is the matching average of the values.

</div>

Why divide by $\sqrt{d_k}$? The paper’s argument is the following computation.

<div class="nb nb-theorem nb-block" id="proposition-1-2-3">

<strong>Proposition 1.2.3</strong> (Dot products grow like $\sqrt{d_k}$)

Let $\bm{q}, \bm{k} \in \mathbb R^{d_k}$ have independent components with mean $0$ and variance $1$. Then $\mathbb E[\bm{q} \cdot \bm{k}] = 0$ and $\operatorname{Var}(\bm{q} \cdot \bm{k}) = d_k$. Hence $\bm{q} \cdot \bm{k} / \sqrt{d_k}$ has variance $1$ whatever $d_k$ is.

</div>

<div class="nb nb-proof">

<em>Proof.</em> $\bm{q} \cdot \bm{k} = \sum_{i=1}^{d_k} q_i k_i$ is a sum of $d_k$ independent terms, each with $\mathbb E[q_i k_i] = \mathbb E[q_i]\mathbb E[k_i] = 0$ and $\operatorname{Var}(q_i k_i) = \mathbb E[q_i^2]\mathbb E[k_i^2] = 1$. Variances of independent terms add.

</div>

Large logits are a problem because of how the softmax differentiates.

<div class="nb nb-theorem nb-block" id="lemma-1-2-4">

<strong>Lemma 1.2.4</strong> (Softmax Jacobian)

If $\bm{p} = \operatorname{softmax}(\bm{z})$ then $\dfrac{\partial p_i}{\partial z_j} = p_i(\delta_{ij} - p_j)$. In particular, if $\bm{p}$ is close to one-hot, every entry of the Jacobian is close to $0$.

</div>

<div class="nb nb-proof">

<em>Proof.</em> Differentiate $p_i = e^{z_i} / \sum_k e^{z_k}$ with the quotient rule. If $p_a \approx 1$ and all other $p_i \approx 0$, then every product $p_i(\delta_{ij}-p_j)$ has a factor close to $0$.

</div>

<div class="nb nb-moral">

Unscaled logits have standard deviation $\sqrt{d_k}$ ($\approx 5.66$ here), which pushes the softmax towards one-hot rows where its gradient vanishes. Dividing by $\sqrt{d_k}$ keeps the logits at unit scale at initialisation.

</div>

[Section 1.4.vi](../experiments/#sec-a3-abl22) shows that the real training run does not quite follow this story.

## 1.2.iii Multi-head attention {#s1-2-iii}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> $8$ heads of width $32$ sharing one $256$-wide residual stream.</em>

</div>

<div class="nb nb-definition" id="definition-1-2-5">

<strong>Definition 1.2.5</strong>. With $h$ heads and $d_k = d_{\text{model}} / h$,

$$
\begin{gather*}
		\operatorname{MultiHead}(\bm{Q}, \bm{K}, \bm{V}) = \operatorname{Concat}(\mathrm{head}_1, \dots, \mathrm{head}_h)\, \bm{W}^O, \\
		\mathrm{head}_i = \operatorname{Attention}(\bm{Q} \bm{W}_i^Q,\ \bm{K} \bm{W}_i^K,\ \bm{V} \bm{W}_i^V),
	\end{gather*}
$$

where $\bm{W}_i^Q, \bm{W}_i^K, \bm{W}_i^V \in \mathbb R^{d_{\text{model}} \times d_k}$ and $\bm{W}^O \in \mathbb R^{h d_k \times d_{\text{model}}}$.

</div>

Each head can attend to a different kind of relation (the previous word, the noun of an article, and so on) at the same total cost as one wide head. In code the $h$ projections of width $d_k$ are stored side by side as one $d_{\text{model}} \times d_{\text{model}}$ matrix, and the heads are split by a reshape ([Section 1.3.v](../implementation/#sec-a3-impl-mha)).

<div class="nb nb-definition" id="fact-1-2-6">

<strong>Fact 1.2.6</strong> (Cost). One multi-head attention block has $4(d_{\text{model}}^2 + d_{\text{model}})$ parameters ($263{,}168$ here). Self-attention over $n$ tokens costs $\mathcal{O}\!\left(n^2 d_{\text{model}}\right)$ time and $\mathcal{O}\!\left(h n^2\right)$ memory for the attention matrices.

</div>

## 1.2.iv Masking {#s1-2-iv}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> position $3$ of the English prefix must not see position $4$.</em>

</div>

A <strong>mask</strong> marks score entries that must receive zero attention. Setting those scores to $-\infty$ before the softmax makes their weights exactly $0$, and the other weights in the row still sum to $1$. Two masks are needed:

- a <strong>padding mask</strong>, so no query attends to `<pad>` positions (encoder self-attention, decoder self-attention and cross-attention);
- a <strong>causal</strong> or look-ahead mask in decoder self-attention, so position $t$ only sees positions $\le t$. Without it teacher forcing would let the decoder read the answer.

## 1.2.v Positional encoding {#s1-2-v}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> the $256$-dimensional vector added to the embedding of the $5$th token.</em>

</div>

Attention treats its inputs as a set: permuting the tokens permutes the outputs in the same way. Word order must therefore be added to the input explicitly.

<div class="nb nb-definition" id="definition-1-2-7">

<strong>Definition 1.2.7</strong>. The <strong>sinusoidal positional encoding</strong> of position $pos$ is

$$
\operatorname{PE}_{(pos,\,2i)} = \sin \!\left(\frac{pos}{10000^{2i/d_{\text{model}}}}\right), \qquad
		\operatorname{PE}_{(pos,\,2i+1)} = \cos \!\left(\frac{pos}{10000^{2i/d_{\text{model}}}}\right),
$$

for $0 \le i < d_{\text{model}}/2$. It is added to the (scaled) token embedding.

</div>

Dimension pair $i$ oscillates with angular frequency $\omega_i = 10000^{-2i/d_{\text{model}}}$, so the wavelengths $2\pi/\omega_i$ form a geometric progression from $2\pi$ up to almost $2\pi \cdot 10000$: the fast pairs distinguish neighbouring positions, the slow pairs coarse location.

<div class="nb nb-theorem nb-block" id="proposition-1-2-8">

<strong>Proposition 1.2.8</strong> (Relative positions are linear)

For every offset $k$ there is a fixed matrix $\bm{R}_k$, depending on $k$ but not on $pos$, with $\operatorname{PE}_{pos+k} = \bm{R}_k\, \operatorname{PE}_{pos}$ for all $pos$.

</div>

<div class="nb nb-proof">

<em>Proof.</em> Look at one pair of coordinates with frequency $\omega$. By the angle-addition formulas,

$$
\begin{pmatrix} \sin \omega(pos+k) \\ \cos \omega(pos+k) \end{pmatrix}
		= \begin{pmatrix} \cos \omega k & \sin \omega k \\ -\sin \omega k & \cos \omega k \end{pmatrix}
		\begin{pmatrix} \sin \omega \, pos \\ \cos \omega \, pos \end{pmatrix}.
$$

Take $\bm{R}_k$ block-diagonal with one such rotation per frequency.

</div>

So a linear layer can in principle learn “attend $k$ positions back” once, for every position. The formula is also defined for every integer $pos$, including lengths never seen in training; this is the theoretical reason the spec gives for sinusoidal encodings extrapolating ([Section 1.4.viii](../experiments/#sec-a3-abl24)). A <strong>learned positional embedding</strong> instead stores one free vector per position (`nn.Embedding(max_len, d_model)`).

## 1.2.vi Position-wise feed-forward network {#s1-2-vi}

$$
\operatorname{FFN}(\bm{x}) = \max(0,\ \bm{x} \bm{W}_1 + \bm{b}_1)\, \bm{W}_2 + \bm{b}_2,
	\qquad \bm{W}_1 \in \mathbb R^{d_{\text{model}} \times d_{\text{ff}}},\ \bm{W}_2 \in \mathbb R^{d_{\text{ff}} \times d_{\text{model}}}.
$$

The same two-layer network is applied to every position separately. Attention mixes information <em>between</em> positions; the FFN transforms each position. Here it has $2 \cdot 256 \cdot 512 + 512 + 256 = 262{,}912$ parameters.

## 1.2.vii Residual connections and layer normalisation {#s1-2-vii}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> $\bm{x} \mapsto \operatorname{LayerNorm}(\bm{x} + \mathrm{Dropout}(\operatorname{MultiHead}(\bm{x},\bm{x},\bm{x})))$.</em>

</div>

<div class="nb nb-definition" id="definition-1-2-9">

<strong>Definition 1.2.9</strong>. For $\bm{x} \in \mathbb R^{d_{\text{model}}}$ with mean $\mu$ and variance $\sigma^2$ over its $d_{\text{model}}$ features, <strong>layer normalisation</strong> [&#91;BKH16&#93;](../references/#ref-ba2016) is

$$
\operatorname{LayerNorm}(\bm{x}) = \bm \gamma \odot \frac{\bm{x} - \mu}{\sqrt{\sigma^2 + \varepsilon}} + \bm \beta
$$

with learned $\bm \gamma, \bm \beta \in \mathbb R^{d_{\text{model}}}$ ($2d_{\text{model}} = 512$ parameters).

</div>

There are two ways to combine a sub-layer $F$ with a residual connection:

$$
\text{Post-LN: } \bm{x} \leftarrow \operatorname{LayerNorm}\bigl(\bm{x} + F(\bm{x})\bigr), \qquad
	\text{Pre-LN: } \bm{x} \leftarrow \bm{x} + F\bigl(\operatorname{LayerNorm}(\bm{x})\bigr).
$$

Post-LN is what the original paper uses and what I implemented. Xiong et al. [&#91;Xio+20&#93;](../references/#ref-xiong2020) showed that at initialisation Post-LN has large gradients near the output layer, which is why it needs a learning-rate warm-up; Pre-LN keeps an un-normalised residual path and can be trained without warm-up.

<div class="nb nb-remark" id="remark-1-2-10">

<strong>Remark 1.2.10</strong> — Pre-LN needs one extra $\operatorname{LayerNorm}$ at the very end of each stack, because its residual stream is never normalised. Post-LN does not, since every layer already ends with $\operatorname{LayerNorm}$. My implementation is Post-LN <em>and</em> adds that final $\operatorname{LayerNorm}$ ([Section 1.3.viii](../implementation/#sec-a3-impl-layers)).

</div>

## 1.2.viii Label smoothing {#s1-2-viii}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> the target for the word <em>“roof”</em>: $0.9$ on <em>roof</em> and $0.1/5892 \approx 1.7 \times 10^{-5}$ on each other word.</em>

</div>

With a one-hot target the cross-entropy keeps decreasing as the logit of the correct word grows, so the model is always pushed towards more confidence. <strong>Label smoothing</strong> [&#91;Sze+16&#93;](../references/#ref-szegedy2016) trains against a softened target instead. In this implementation, for gold word $y$ and vocabulary size $V$,

$$
q'_k = \begin{cases} 1 - \varepsilon & k = y, \\ \varepsilon/(V-1) & k \ne y, \end{cases}
	\qquad \mathcal L(\bm{p}) = -\sum_{k=1}^{V} q'_k \log p_k .
$$

<div class="nb nb-theorem nb-block" id="proposition-1-2-11">

<strong>Proposition 1.2.11</strong> (The smoothed loss has a floor)

$\mathcal L(\bm{p}) = H(\bm{q}') + D_{\mathrm{KL}}(\bm{q}' \,\|\, \bm{p}) \ge H(\bm{q}')$, with equality exactly when $\bm{p} = \bm{q}'$. For $V = 5893$ and $\varepsilon = 0.1$,

$$
H(\bm{q}') = -(1-\varepsilon)\log(1-\varepsilon) - \varepsilon \log \frac{\varepsilon}{V-1} \approx 1.193 \text{ nats},
$$

so the per-token training loss can never go below $1.193$ (a perplexity of $e^{1.193} \approx 3.30$).

</div>

<div class="nb nb-proof">

<em>Proof.</em> Expand $D_{\mathrm{KL}}(\bm{q}' \| \bm{p}) = \sum_k q'_k \log q'_k - \sum_k q'_k \log p_k = -H(\bm{q}') + \mathcal L(\bm{p})$, and use $D_{\mathrm{KL}} \ge 0$ (Gibbs’ inequality) with equality iff $\bm{p} = \bm{q}'$. The numerical value is $0.9 \cdot 0.1054 + 0.1 \cdot 10.984$.

</div>

<div class="nb nb-theorem nb-block" id="corollary-1-2-12">

<strong>Corollary 1.2.12</strong>

At the optimum, the correct word’s logit exceeds every other logit by exactly $\log \frac{(1-\varepsilon)(V-1)}{\varepsilon} \approx 10.88$: the model is rewarded for a <em>finite</em> margin rather than an infinite one.

</div>

This is the regularising effect: the model cannot become arbitrarily confident. It is also why the smoothed and unsmoothed runs in [Section 1.4.ix](../experiments/#sec-a3-abl25) have training losses that cannot be compared directly.

## 1.2.ix Optimiser and the Noam schedule {#s1-2-ix}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> learning rate $2.5 \times 10^{-7}$ at step $1$, $9.9 \times 10^{-4}$ at step $4000$.</em>

</div>

Adam [&#91;KB15&#93;](../references/#ref-kingma2015) keeps running averages of the gradient and its square, $m_t = \beta_1 m_{t-1} + (1-\beta_1) g_t$ and $v_t = \beta_2 v_{t-1} + (1-\beta_2) g_t^2$, and updates by $-\eta_t\, \hat m_t / (\sqrt{\hat v_t} + \epsilon)$ with bias-corrected $\hat m_t, \hat v_t$. The paper, and my code, use $\beta_1 = 0.9$, $\beta_2 = 0.98$, $\epsilon = 10^{-9}$.

<div class="nb nb-definition" id="definition-1-2-13">

<strong>Definition 1.2.13</strong>. The <strong>Noam schedule</strong> with warm-up $w$ is

$$
\eta(s) = d_{\text{model}}^{-1/2} \cdot \min \bigl(s^{-1/2},\ s \cdot w^{-3/2}\bigr),
		\qquad s = 1, 2, \dots
$$

</div>

<div class="nb nb-theorem nb-block" id="proposition-1-2-14">

<strong>Proposition 1.2.14</strong> (Shape of the Noam schedule)

$\eta$ increases linearly for $s \le w$, decreases like $s^{-1/2}$ for $s \ge w$, and its maximum is at $s = w$, where $\eta(w) = (d_{\text{model}}\, w)^{-1/2}$.

</div>

<div class="nb nb-proof">

<em>Proof.</em> $s^{-1/2} \le s\, w^{-3/2}$ iff $s^{3/2} \ge w^{3/2}$ iff $s \ge w$. So the minimum is the linear term before $w$ and the decaying term after, and the two agree at $s = w$.

</div>

<div class="nb nb-example nb-block" id="example-1-2-15">

<strong>Example 1.2.15</strong> (My numbers)

With $d_{\text{model}} = 256$ and $w = 4000$: $\eta(1) = 2.47 \times 10^{-7}$, peak $\eta(4000) = 1/\sqrt{1{,}024{,}000} = 9.88 \times 10^{-4}$. One epoch is $227$ steps, so warm-up lasts $4000/227 \approx 17.6$ epochs.

</div>

That last number turns out to matter a great deal ([Section The warm-up trap](../experiments/#sec-a3-warmup-trap)).

## 1.2.x Greedy decoding {#s1-2-x}

At test time there is no gold prefix. <strong>Greedy decoding</strong> starts from `<sos>`, repeatedly appends the most probable next word $\hat y_t = \operatorname*{arg max}_y p(y \mid \hat y_{<t}, \bm{x})$, and stops at `<eos>` or a length limit. It is cheap but can commit early to a bad prefix. The paper used beam search (beam size $4$); the assignment asks for greedy decoding.

## 1.2.xi BLEU {#sec-a3-bleu-theory}

<div class="nb nb-definition" id="definition-1-2-16">

<strong>Definition 1.2.16</strong>. For a corpus of hypotheses and references, let $p_n$ be the <strong>modified $n$-gram precision</strong>: the number of hypothesis $n$-grams that also occur in the reference (each reference $n$-gram can be matched at most as many times as it occurs), divided by the number of hypothesis $n$-grams, summed over the whole corpus. With total hypothesis length $c$ and reference length $r$, the <strong>brevity penalty</strong> is $\operatorname{BP} = \min(1, e^{1 - r/c})$ and

$$
\mathrm{BLEU} = \operatorname{BP} \cdot \exp \Bigl( \tfrac14 \sum_{n=1}^{4} \log p_n \Bigr),
$$

usually reported $\times 100$ [&#91;Pap+02&#93;](../references/#ref-papineni2002).

</div>

BLEU depends heavily on tokenisation and casing. SacreBLEU [&#91;Pos18&#93;](../references/#ref-post2018) exists to make it comparable: it expects <em>detokenised</em> text and applies its own standard tokenisation (`13a`) and, by default, is case-sensitive.
