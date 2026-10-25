---
title: "10 · Unsupervised and semi-supervised learning"
linkTitle: "10 Unsupervised"
weight: 10
math: true
---
Without labels there is no test accuracy to hide behind, so questions go to mechanics and assumptions: when does k-means stop, why does it need $k$ and scaling, what does EM alternate, why standardise before PCA. OA papers favour the k-means stopping question and the PCA scaling question.

## 10.1 k-means {#ml-10-1}

k-means looks for $k$ centroids minimising the **inertia** (within-cluster sum of squared distances). **Lloyd's algorithm** alternates two steps:

1. **Assign** each point to its nearest centroid.
2. **Update** each centroid to the mean of its points.

<div class="nb nb-example">

<strong>Example</strong> (One assignment)

Centres $C_1 = (1, 1)$, $C_2 = (5, 4)$. The point $(2, 3)$ is $\sqrt{1 + 4} = 2.24$ from $C_1$ and $\sqrt{9 + 1} = 3.16$ from $C_2$, so it joins cluster 1.

</div>

**When it stops.** Each step can only lower the inertia, the inertia is bounded below and there are finitely many assignments, so k-means **always terminates**, at a **local** minimum (the global one is NP-hard). In practice it stops when any of these holds: no point changes cluster; centroids move less than a tolerance; the inertia drop is tiny; or `max_iter` is reached.

<div class="nb nb-remark">

<strong>Trap</strong> — "k-means stops when inertia reaches zero" (only if $k = n$) or "when every cluster has the same size" (never a criterion). It always converges, but maybe badly: hence several restarts (`n_init`) and **k-means++** seeding, which picks each new seed with probability proportional to its squared distance from the seeds already chosen.

</div>

**Choosing $k$:** the inertia always falls as $k$ grows, so look for the **elbow**, or maximise the **silhouette** $s = \dfrac{b - a}{\max(a, b)} \in [-1, 1]$, where $a$ is a point's mean distance to its own cluster and $b$ to the nearest other cluster.

**Assumptions:** roughly spherical clusters of similar size in a Euclidean space. So **scale features first**; it is sensitive to outliers (means are not robust; k-medoids uses actual points); and it cannot find non-convex shapes such as two interleaved half-moons.

## 10.2 Hierarchical clustering and DBSCAN {#ml-10-2}

**Agglomerative clustering** starts with singletons and repeatedly merges the closest pair of clusters, giving a **dendrogram** you can cut at any height (no $k$ needed in advance). Linkage: **single** (closest pair, prone to chaining), **complete** (farthest pair, compact clusters), **average**, **Ward** (smallest variance increase, closest to k-means). Cost $O(n^3)$ time and $O(n^2)$ memory: thousands of points, not millions.

**DBSCAN** groups points in dense regions. With radius $\varepsilon$ and threshold `min_samples`: a **core** point has at least `min_samples` neighbours (itself included) within $\varepsilon$; a **border** point is within $\varepsilon$ of a core point but not core; everything else is **noise**. Strengths: arbitrary shapes, no $k$, explicit outliers. Weaknesses: one global density (clusters of different densities break it; HDBSCAN fixes this), choosing $\varepsilon$, high dimensions. On two moons, k-means scores an adjusted Rand index of 0.27, DBSCAN 1.00.

## 10.3 Gaussian mixtures and EM {#ml-10-3}

A **Gaussian mixture** models the density as $\sum_k \pi_k \mathcal N(x; \mu_k, \Sigma_k)$. We do not know which component made each point, so **EM** alternates:

- **E-step:** compute each point's **responsibility** for each component, $r_{ik} = P(z_i = k \mid x_i)$.
- **M-step:** re-estimate weights, means and covariances with those soft counts.

The likelihood **never decreases** (EM is coordinate ascent on a lower bound), and it converges to a local optimum. k-means is the hard limit: responsibilities rounded to 0/1 and equal spherical covariances shrinking to zero. GMMs give soft assignments, elliptical clusters and a density usable for anomaly detection; choose $k$ with BIC. A component can collapse onto one point (variance → 0, likelihood → ∞), hence a small covariance regulariser.

## 10.4 PCA {#ml-10-4}

Find the unit direction $u$ that maximises the variance of the projected, **centred** data. The answer is the top eigenvector of the covariance matrix $S$, and the variance captured is its eigenvalue. Each next component is the top direction orthogonal to the previous ones. Libraries compute it with the SVD of the centred data.

<div class="nb nb-example">

<strong>Example</strong> (Explained variance)

Eigenvalues $4.0, 2.5, 1.0, 0.3, 0.2$ (total 8.0). PC1 explains $4/8 = 50\%$; the first two 81.25%; the first three 93.75%. So **3 components** keep at least 90%.

</div>

**Why standardise first:** PCA maximises variance, which depends on units. In the wine data, proline has variance about 99,000 and hue 0.05; unscaled, PC1 "explains" 99.8% and is just the proline axis. After standardising, PC1 explains 36%, and clustering on two components recovers the wine types far better (adjusted Rand 0.90 vs 0.37).

<div class="nb nb-remark">

<strong>Trap</strong> — Precise answer: standardise when variance differences are artefacts of units; do not when all features share a unit and their variances mean something (pixel intensities). **Always centre.** Also: PCA is unsupervised, so the top components need not be the most predictive; it is linear; components are defined only up to sign.

</div>

Choose $k$ by cumulative explained variance (90 to 95%), a scree-plot elbow, or downstream validation. Uses: compression, denoising, visualisation, decorrelating features, speeding up distance-based methods.

## 10.5 ICA, t-SNE and UMAP {#ml-10-5}

- **ICA** unmixes independent, **non-Gaussian** sources (two speakers, two microphones). PCA only decorrelates and cannot do this.
- **t-SNE** and **UMAP** are for **visualisation**. They preserve local neighbourhoods; cluster sizes and distances between clusters in the picture mean nothing, results depend on perplexity/neighbours and the seed, and standard t-SNE has no transform for new points.

## 10.6 Anomaly detection and association rules {#ml-10-6}

**Isolation forest:** random trees with random splits; anomalies are few and different, so they are isolated near the root (short average path). Alternatives: low GMM density, one-class SVM, local outlier factor, reconstruction error of PCA or an autoencoder.

**Association rules** over transactions: $\text{support}(A)$ is the fraction of baskets containing $A$; $\text{confidence}(A \Rightarrow B) = \text{support}(A \cup B)/\text{support}(A)$; $\text{lift} = \text{confidence}/\text{support}(B)$.

<div class="nb nb-example">

<strong>Example</strong> (Chips and cola)

1,000 orders: 200 have chips, 300 cola, 120 both. Support(both) = 0.12; confidence(chips ⇒ cola) = 120/200 = 0.6; lift = 0.6/0.3 = **2.0**: buying chips doubles the chance of cola.

</div>

<div class="nb nb-remark">

<strong>Trap</strong> — High confidence alone misleads when the consequent is common ("anything ⇒ bread" when 83% of baskets have bread). Lift corrects for it: lift 1 means independence. Confidence is not symmetric; lift is. **Apriori** prunes candidates using "every subset of a frequent itemset is frequent".

</div>

## 10.7 Semi- and self-supervised learning, in one section {#ml-10-7}

Unlabelled data help only if $p(x)$ says something about $p(y \mid x)$: **smoothness**, **cluster** (the boundary should pass through low-density regions) or **manifold** assumptions.

- **Self-training (pseudo-labelling):** train on labels, label the unlabelled points you are most sure of, retrain. Risk: **confirmation bias**, early mistakes become training labels.
- **Label propagation:** build a similarity graph and let labels flow along edges.
- **Consistency regularisation** (FixMatch, Mean Teacher): predictions should not change under augmentation of an unlabelled input.
- **Contrastive learning:** two augmented views of the same example should be closer to each other than to anything else in the batch (the InfoNCE loss; see the [Deep Learning](../../dl/10-generative/) book).

<div class="nb nb-remark">

<strong>Trap</strong> — "More data never hurts." More *labelled* data essentially never hurts; *unlabelled* data can, when the assumption is wrong. With six labels, label spreading lifted accuracy from 0.82 to 0.94 on two moons but lost to plain logistic regression where the clusters ran across the labels. Always compare against the supervised baseline.

</div>

<div class="nb nb-moral">

k-means is coordinate descent on inertia (it always stops, maybe badly); EM is coordinate ascent on a likelihood bound; PCA is an eigenproblem on the covariance, so scale before it unless units agree.

</div>
