---
title: "A · Glossary of notations"
linkTitle: "A Glossary of notations"
weight: 901
math: true
---
## A.1 Machine learning {#sa-1}

- $\bm{x}, \bm{q}, \bm{k}$: vectors are bold lower-case; $\bm{X}, \bm{Q}, \bm{K}, \bm{V}, \bm{W}$: matrices are bold upper-case.
- $\bm{A}^{\top}$: transpose of $\bm{A}$.
- $d_{\text{model}}$: width of the residual stream (embedding size).
- $d_{\text{ff}}$: inner width of the position-wise feed-forward network.
- $h$: number of attention heads; $d_k = d_{\text{model}} / h$: width of one head.
- $N$: number of encoder layers (equal to the number of decoder layers).
- $V$: vocabulary size; $V_{\text{src}}$, $V_{\text{tgt}}$ for source and target.
- $B$: batch size; $n$, $m$: source and target lengths in tokens.
- $\operatorname{softmax}(\bm{z})_i = e^{z_i} / \sum_j e^{z_j}$.
- $\varepsilon$ or $\varepsilon_{\text{ls}}$: label-smoothing mass.
- $\operatorname{CE}(\bm{p}, \bm{q}) = -\sum_i p_i \log q_i$: cross-entropy of $\bm{q}$ relative to $\bm{p}$.
- $D_{\mathrm{KL}}(\bm{p} \,\|\, \bm{q}) = \sum_i p_i \log (p_i / q_i)$: Kullback–Leibler divergence.
- $\mathcal{O}\!\left(f\right)$: asymptotic upper bound.

## A.2 Code and experiments {#sa-2}

- `file.py:40`: line 40 of `file.py`, relative to the project folder named at the start of the chapter.
- `r9ec0v3x`: a Weights &amp; Biases run id.
