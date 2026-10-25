---
title: "8 · Decision trees"
linkTitle: "8 Decision trees"
weight: 8
math: true
---
The most interview-friendly model: you can compute a split by hand in two minutes, draw the result, and explain it to a manager. Trees are also the building block of the models that win most tabular problems (chapter 9), so their quirks matter far beyond this chapter.

## 8.1 Impurity {#ml-8-1}

A classification tree asks yes/no questions that split the data into purer groups. With class proportions $p_k$ in a node:

$$\text{Entropy } H = -\sum_k p_k \log_2 p_k, \qquad \text{Gini } G = 1 - \sum_k p_k^2, \qquad \text{Misclassification} = 1 - \max_k p_k.$$

All three are 0 for a pure node. For two classes the maximum (50/50) is **1 bit** of entropy and a **Gini of 0.5**. Gini is the probability that two labels drawn at random from the node disagree; it avoids a logarithm and is scikit-learn's default. Gini and entropy almost always pick the same split.

<div class="nb nb-example">

<strong>Example</strong> (Gini by hand)

6 yes, 4 no: $1 - 0.6^2 - 0.4^2 = 1 - 0.36 - 0.16 = 0.48$. 8 yes, 2 no: $1 - 0.64 - 0.04 = 0.32$. 9 yes, 1 no: $0.18$.

</div>

**Information gain** is the parent's impurity minus the size-weighted impurity of the children:

$$\text{IG} = H(S) - \sum_v \frac{|S_v|}{|S|} H(S_v).$$

<div class="nb nb-example">

<strong>Example</strong> (Which feature goes at the root?)

14 candidates, 8 accepted an offer and 6 declined: $H = 0.985$ bits. Splitting on CTC gives High (6 yes, 1 no, $H = 0.592$) and Low (2 yes, 5 no, $H = 0.863$). Weighted child entropy $\tfrac{7}{14}(0.592) + \tfrac{7}{14}(0.863) = 0.727$, so $\text{IG} = 0.258$. City and Role each give 0.128, so the root splits on CTC.

</div>

<div class="nb nb-remark">

<strong>Trap</strong> — Information gain favours **many-valued** features: a candidate-ID column gives 14 pure leaves and the maximum gain while being useless. C4.5 corrects this with the **gain ratio** (gain divided by the entropy of the split itself). And misclassification error is a poor splitting criterion: many splits that clearly improve purity leave it unchanged. Use it for pruning, not growing.

</div>

**ID3** (categorical features, multiway splits, information gain), **C4.5** (adds thresholds, gain ratio, missing values, pruning), **CART** (what scikit-learn implements: strictly binary splits, Gini or squared error, cost-complexity pruning).

## 8.2 Growing a tree {#ml-8-2}

- **Continuous features:** sort the values; only midpoints between consecutive distinct values can change the split, so $n$ distinct values give at most $n - 1$ thresholds.
- **Categorical features** with $q$ levels admit $2^{q-1} - 1$ binary splits; for binary targets, ordering levels by their positive rate and trying only the $q - 1$ splits in that order is optimal.
- **Missing values:** CART uses surrogate splits; XGBoost and LightGBM learn a default direction per split.
- **Stop** when a node is pure or hits `max_depth`, `min_samples_split`, `min_samples_leaf` or a minimum impurity decrease.

Growth is **greedy**: finding the smallest consistent tree is NP-hard, and a split with zero gain (XOR!) may be needed to enable great splits below it.

## 8.3 Regression trees {#ml-8-3}

Each leaf predicts the **mean** of its targets; the split criterion is the reduction in squared error (variance reduction).

<div class="nb nb-example">

<strong>Example</strong> (One regression split)

$x = 1, \dots, 6$, $y = (5, 6, 5, 20, 22, 21)$. The best threshold is $x \le 3.5$, with leaf predictions 5.33 and 21.00.

</div>

A regression tree is piecewise constant: it **cannot extrapolate** beyond the range of the training targets and approximates a line by a staircase. That is why trees forecast trending time series badly unless you model differences.

## 8.4 Pruning {#ml-8-4}

Grown to purity, a tree memorises noise: training accuracy reaches 100% while test accuracy peaked several levels earlier. **Pre-pruning** stops early (depth, leaf size). **Post-pruning** grows fully and cuts back; CART's **cost-complexity pruning** minimises training error $+\ \alpha \times$(number of leaves), collapsing the weakest branches first, with $\alpha$ chosen by cross-validation (the same "fit + $\lambda$ × complexity" shape as chapter 4).

## 8.5 What trees are good and bad at {#ml-8-5}

**Strengths:** classification and regression; mixed numeric and categorical features; **no scaling needed** (invariant to any monotone transform of a feature); interactions for free (a path is a conjunction of conditions); missing-value strategies; readable rules; built-in feature importances; fast prediction, $O(\text{depth})$.

**Weaknesses:** **high variance** (resample the data and the root split changes: over 200 bootstraps of one dataset, a depth-1 tree chose 6 different root features); axis-aligned boundaries make a diagonal a staircase; no extrapolation; greedy; biased towards features with many split points; coarse probabilities from small leaves.

<div class="nb nb-remark">

<strong>Trap</strong> — "Decision trees need normalised features" (no), "trees are linear classifiers" (no: piecewise constant, axis-aligned), "trees cannot handle categorical data" (they can in principle; scikit-learn's needs encoding), "a deeper tree always generalises better" (training accuracy rises, test accuracy plateaus or falls).

</div>

<div class="nb nb-moral">

Split greedily on the largest impurity drop, stop or prune before the leaves memorise noise, and expect high variance, which is exactly what ensembles fix.

</div>
