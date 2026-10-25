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

## A.2 Graphs and explanations (the MTP chapter) {#sa-2}

- $A$: adjacency matrix; $\tilde A = A + I$: with self-loops; $\tilde D_{ii} = \sum_j \tilde A_{ij}$: its degree matrix; $\hat A = \tilde D^{-1/2}\tilde A\,\tilde D^{-1/2}$: the renormalised adjacency of the GCN.
- $H^{(l)}$: node representations after layer $l$ (with $H^{(0)} = X$); $W^{(l)}$: the weight matrix of layer $l$; $L$: number of message-passing layers.
- $t$ or $v$: the node whose prediction is explained; $\hat y$: the class the model predicts for it.
- $G_c(v)$: the computation graph of $v$ ([Proposition 1.2.1](../background/#proposition-1-2-1)); $G_S \subseteq G_c$: an explanation subgraph.
- $M$: the learnable edge mask (real numbers); $\sigma(M)$: the mask after the sigmoid, with values in $(0,1)$; $F$: the feature mask.
- $H(p) = -p\log p - (1-p)\log(1-p)$: binary entropy; $\overline H$: its mean over entries.
- $\lambda_s, \lambda_e$: coefficients of the size and the entropy regularisers.
- $\mathrm{fid}_+$, $\mathrm{fid}_-$: positive and negative fidelity; $F_1$: F1 score of the SAR class.
- <strong>AUROC</strong>: area under the ROC curve; <em>pooled</em> over all explained nodes’ edges unless stated.

## A.3 Code and experiments {#sa-3}

- `file.py:40`: line 40 of `file.py`, relative to the project folder named at the start of the chapter.
- <span style="color:#009b55"><strong>[R]</strong></span>, <span style="color:#0071bc"><strong>[F]</strong></span>, <span style="color:#f7921d"><strong>[L]</strong></span> (MTP chapter): a number that I re-ran on 2 October 2026, that I read from a result file, or that appears only in my project notes.
