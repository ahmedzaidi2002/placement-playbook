---
title: "6 · Naive Bayes, LDA and k-nearest neighbours"
linkTitle: "6 Naive Bayes and k-NN"
weight: 6
math: true
---
Two simple families that OAs love: naive Bayes for posterior numericals with Laplace smoothing, and k-NN for "what happens if $k = 1$, if you forget to scale, if you add 100 useless features". The k-NN questions are really about the curse of dimensionality.

## 6.1 Naive Bayes {#ml-6-1}

Bayes' rule says $P(c \mid x) \propto P(c)\, p(x \mid c)$. Modelling $p(x \mid c)$ in many dimensions is hard, so naive Bayes assumes **the features are conditionally independent given the class**:

$$\hat y = \arg\max_c \Big[\log P(c) + \sum_j \log p(x_j \mid c)\Big].$$

Each factor is a one-dimensional count or a mean and variance, so training is one pass over the data and works with tiny datasets and huge vocabularies. Work in **log space**: a product of hundreds of small probabilities underflows to 0.

| Variant | Features | $p(x_j \mid c)$ |
|---|---|---|
| Multinomial | word counts | share of class-$c$ tokens that are word $j$ |
| Bernoulli | word present / absent | absence also counts as evidence |
| Gaussian | continuous | normal density with a per-class mean and variance |

<div class="nb nb-example">

<strong>Example</strong> (Spam posterior, OA style)

$P(\text{spam}) = 0.4$, $P(\text{"free"} \mid \text{spam}) = 0.5$, $P(\text{"free"} \mid \text{ham}) = 0.1$. Spam score $0.4 \times 0.5 = 0.20$, ham score $0.6 \times 0.1 = 0.06$, so $P(\text{spam} \mid \text{"free"}) = 0.20/0.26 = 0.77$.

</div>

## 6.2 Laplace smoothing {#ml-6-2}

A word never seen in a class gets probability 0, and one zero kills the whole product. **Laplace (additive) smoothing** adds a pseudo-count $\alpha$ to every word:

$$\hat\theta_{cj} = \frac{N_{cj} + \alpha}{N_c + \alpha V},$$

with $V$ the vocabulary size and $N_c$ the number of tokens in class $c$. $\alpha = 1$ is Laplace. It is exactly the MAP estimate under a Dirichlet prior.

<div class="nb nb-remark">

<strong>Trap</strong> — The denominator adds $\alpha V$, not $\alpha$ and not $\alpha$ times the number of classes, so the probabilities still sum to one. (For Bernoulli NB it is $(N_{cj} + \alpha)/(N_c + 2\alpha)$ with $N_c$ the number of documents, since each word has two outcomes.)

</div>

## 6.3 Why naive Bayes still works, and its limits {#ml-6-3}

The independence assumption is almost always false, so correlated features ("free", "FREE", "free!!!") are **double-counted** and the probabilities are over-confident. Copying one feature 10 times pushes a correct posterior of 0.57 to 0.95. Yet the **argmax** is often still right, and classification only needs the argmax. That is why NB is a strong, fast text baseline that **ranks well and calibrates badly**.

Other standard limits: the zero-frequency problem without smoothing; Gaussian NB assumes each feature is normal within a class; it cannot learn interactions (XOR of two features is invisible to it); it is high-bias, low-variance, and logistic regression overtakes it as data grow.

<div class="nb nb-remark">

<strong>Trap</strong> — "Naive Bayes assumes the features are independent." Precisely: **conditionally** independent given the class. And "naive Bayes needs normal features" is true only of Gaussian NB.

</div>

## 6.4 LDA and QDA {#ml-6-4}

Model each class as a Gaussian without the naive assumption:

- **LDA** (linear discriminant analysis) uses one **shared** covariance matrix; the quadratic terms cancel and the boundary is a **hyperplane**. For two classes its posterior has exactly the logistic form $\sigma(w^\top x + b)$, but $w$ comes from plugging in means and covariance (generative) rather than maximising the conditional likelihood (discriminative).
- **QDA** gives each class its own covariance: a **quadratic** boundary, many more parameters (higher variance).
- Diagonal covariances give Gaussian naive Bayes.

If the Gaussian assumption holds, LDA is more data-efficient than logistic regression; with heavy tails, outliers or binary features, logistic regression is more robust. LDA is also a supervised dimensionality reduction to at most $K - 1$ directions. (Not to be confused with latent Dirichlet allocation, the topic model.)

## 6.5 k-nearest neighbours {#ml-6-5}

Predict the **majority label of the $k$ closest training points** (or their mean for regression). It is a **lazy**, non-parametric learner: "training" just stores the data; all the cost, $O(nd)$ per query, moves to prediction.

<div class="nb nb-example">

<strong>Example</strong> (Vote by hand)

$k = 3$, the nearest neighbours are cat, dog, cat: predict cat. With $k = 1$ to classify $(1, 1)$ against A $(2,2)$ class X, B $(4,5)$ class Y, C $(1,3)$ class X: distances 1.41, 5, 2, so the nearest is A and the answer is X.

</div>

**$k$ is a bias–variance dial.** $k = 1$: training error exactly 0 (each point is its own neighbour), jagged boundary, maximal variance. $k = n$: always the majority class, maximal bias. Pick $k$ by cross-validation; a common start is near $\sqrt{n}$, and an **odd** $k$ avoids ties for two classes.

### Distances {#ml-6-5-i}

For $a = (1,2,3)$, $b = (4,0,3)$:

| Distance | Formula | Use |
|---|---|---|
| Euclidean (L2) | $\sqrt{\sum (a_i - b_i)^2}$ | default, scaled continuous features |
| Manhattan (L1) | $\sum \lvert a_i - b_i\rvert$ | grids; robust to one big difference |
| Chebyshev (L∞) | $\max \lvert a_i - b_i\rvert$ | worst coordinate matters |
| Cosine | $1 - \frac{a^\top b}{\lVert a\rVert \lVert b\rVert}$ | text and embeddings: direction, not length |
| Hamming | number of differing positions | binary strings, categories |

Mahalanobis distance measures distance in units of the data's own spread and correlation; Euclidean distance on standardised, decorrelated features is Mahalanobis distance.

<div class="nb nb-example">

<strong>Example</strong> (Scaling decides the neighbour)

Customers (₹50,000, 58 years) and (₹52,000, 25 years); query (₹51,800, 57 years). Raw distances 1800 and 202.5, so the nearest is the 25-year-old: a ₹1,600 income gap dwarfs a 32-year age gap. After standardising, the nearest is the 58-year-old. **Scale before k-NN.**

</div>

## 6.6 The curse of dimensionality {#ml-6-6}

Three facts that make distance-based methods fail in high dimension:

1. **Distances concentrate.** For uniform points, the gap between the nearest and farthest neighbour relative to the nearest shrinks from about 35 in 2-D to about 0.1 in 1000-D. When everything is equally far, "nearest" means little.
2. **Neighbourhoods are not local.** To capture 10% of uniform data in $[0,1]^d$ with a cube you need edge $0.1^{1/d}$: 0.79 of each axis at $d = 10$, 0.98 at $d = 100$.
3. **The data needed grows exponentially in $d$.** Adding 100 noise features to a 2-feature problem dropped 7-NN accuracy from 0.97 to 0.63.

k-NN still works on images and embeddings because real data lie near a low-dimensional manifold and learned embeddings make distance meaningful. Remedies: feature selection, PCA or embeddings, metric learning.

<div class="nb nb-remark">

<strong>Trap</strong> — "More features always hurt." Informative features help any model. The curse bites **distance- and density-based** methods through irrelevant dimensions; regularised linear models and tree ensembles suffer far less.

</div>

**Speeding up search:** KD-trees prune well in low dimensions but degrade to brute force beyond roughly 10 to 20. Production systems use **approximate nearest-neighbour** search (locality-sensitive hashing, HNSW graphs, inverted files with product quantisation), trading a little recall for orders of magnitude in speed; this is what vector databases for RAG use.

<div class="nb nb-moral">

Naive Bayes: count, smooth, multiply in log space; it ranks well and calibrates badly. k-NN is only as good as its distance: scale features, drop irrelevant ones, choose $k$ by cross-validation.

</div>
