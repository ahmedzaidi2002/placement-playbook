---
title: "2 · Data preparation and feature engineering"
linkTitle: "2 Data preparation"
weight: 2
math: true
---
More model quality comes from clean data and good features than from the choice of algorithm, and most production bugs live here. OAs test the crisp parts (which models need scaling, one-hot versus ordinal, IDF arithmetic, median fill); interviews test judgement ("this feature is 40% missing, what do you do?").

## 2.1 Which step when {#ml-2-1}

| If the data has… | Do this | Example |
|---|---|---|
| A few missing numbers | fill with the **median** | 3 of 1,000 ages blank |
| A mostly empty column | drop the column | 70% of "second phone" blank |
| Missing categories | fill with the mode or "Unknown" | blank city |
| Unordered categories | **one-hot** | city, colour, brand |
| Ordered categories | ordinal codes 0, 1, 2 | size S / M / L |
| Features on very different scales | standardise or min–max | salary next to age |
| Extreme values | look first, then cap or log-transform | a ₹2 crore fresher salary |
| A rare class | stratified split, class weights | 2% fraud |
| Duplicate rows | remove before splitting | one customer entered twice |

## 2.2 Missing values {#ml-2-2}

First ask **why** values are missing:

- **MCAR** (completely at random): dropping rows only costs data.
- **MAR** (depends on other observed features): model-based imputation works.
- **MNAR** (depends on the missing value itself, e.g. high earners skip the income question): the fact of missingness is information.

Options: drop rows (few, MCAR), drop the column (mostly empty), mean/median/mode fill (fast, but shrinks variance), k-NN or model-based imputation, a **missing-indicator** column, or models that handle NaN natively (XGBoost, LightGBM).

<div class="nb nb-example">

<strong>Example</strong> (Median fill, OA style)

Ages 22, 25, 30, (missing), 41. Known values sorted: 22, 25, 30, 41, so the median is $(25+30)/2 = 27.5$.

</div>

<div class="nb nb-example">

<strong>Example</strong> (Missingness is a feature)

Income is missing for 28% of loan applicants, mostly high earners, and the target rises with income. Mean imputation alone: test AUC 0.710. Mean imputation **plus an is-missing flag**: 0.808.

</div>

Use the **median** for skewed numbers (the mean is dragged by the tail) and the **mode** for categories. Fit the imputer on the training data only.

## 2.3 Encoding categories {#ml-2-3}

- **One-hot:** one 0/1 column per level (a colour with 4 values gives 4 columns). Safe; dimension explodes with cardinality. In an unpenalised linear model with an intercept, drop one level, or you hit the **dummy-variable trap** (perfect collinearity).
- **Ordinal / label encoding:** integers. Fine for trees and for truly ordered categories; for linear models it invents an order and a distance (Agra = 3 × Pune) that do not exist.
- **Frequency encoding, feature hashing** (bounded memory, collisions), **learned embeddings** (neural nets).
- **Target (mean) encoding:** replace a level by a smoothed mean of the target, $\text{TE}(c) = \dfrac{n_c \bar y_c + m \bar y}{n_c + m}$. One dense column whatever the cardinality, with rare levels shrunk to the global mean.

<div class="nb nb-remark">

<strong>Trap</strong> — Target encoding computed on the full training set leaks each row's own label. On a 1,500-level noise category: training AUC 0.946, test AUC 0.585, worse than ignoring the column. Done **out-of-fold** (as CatBoost's ordered statistics or scikit-learn's TargetEncoder do), the noise is correctly ignored. "Target encoding always beats one-hot" is only true when it is done out-of-fold with smoothing.

</div>

## 2.4 Scaling {#ml-2-4}

| Method | Formula | Use |
|---|---|---|
| Standardisation (z-score) | $(x - \mu)/\sigma$ | the default; result has mean 0, SD 1 |
| Min–max | $(x - \min)/(\max - \min)$ | bounded inputs, range 0 to 1; one outlier squashes the rest |
| Robust | $(x - \text{median})/\text{IQR}$ | when there are outliers |

Log or Box–Cox transforms handle skew before scaling.

<div class="nb nb-example">

<strong>Example</strong> (The two formulas)

Mean 50, SD 10: the value 65 has $z = (65-50)/10 = 1.5$. Min 10, max 60: the value 30 maps to $(30-10)/50 = 0.4$.

</div>

**Who needs scaling:** anything that uses **distances, margins, variances or penalties, or is trained by gradient descent**: k-NN, k-means, SVM (especially RBF), PCA, ridge/lasso, logistic regression with a penalty, neural networks. **Trees and tree ensembles do not**: a split threshold is unchanged by any monotone rescaling. Unpenalised OLS gives the same predictions either way (only coefficients change).

<div class="nb nb-remark">

<strong>Trap</strong> — "We scaled the whole dataset, then split." The test set's mean and SD leaked into training. Split first, fit the scaler on the training data, then transform both.

</div>

## 2.5 Outliers {#ml-2-5}

Detect with the **IQR rule** (outside $[Q_1 - 1.5\,\text{IQR},\ Q_3 + 1.5\,\text{IQR}]$), z-scores (fragile: the outlier inflates $\sigma$), plots, or an isolation forest. Then decide: a data-entry error (fix or drop), a genuine extreme (keep it; use a robust loss, a log transform or capping), or the signal itself (fraud).

## 2.6 Class imbalance {#ml-2-6}

In order of preference:

1. **Pick the right metric and threshold** (precision, recall, PR-AUC; chapter 11). Accuracy is meaningless when 99% of rows are one class.
2. **Class weights** (`class_weight="balanced"`, `scale_pos_weight`).
3. **Resampling:** under-sample the majority, over-sample the minority, or **SMOTE** (synthetic minority points interpolated between a minority point and a minority neighbour).
4. **Stratified** splits, so every fold keeps the class mix.

<div class="nb nb-remark">

<strong>Trap</strong> — SMOTE before cross-validation: 1,000 rows with 5% positives and a 3-NN model report F1 **0.936**; SMOTE only inside each training fold gives **0.330**. Synthetic points land in validation folds between their own parents. Resample **training data only**, never validation or test, and remember that resampling changes the predicted probabilities.

</div>

## 2.7 Feature selection {#ml-2-7}

- **Filter** methods score features one at a time (correlation, ANOVA F, mutual information, $\chi^2$): fast, blind to interactions and redundancy.
- **Wrapper** methods search subsets with a model (forward/backward selection, recursive feature elimination): expensive, can overfit the validation data.
- **Embedded** methods select while fitting (lasso, tree importances).

Any selection that looks at labels must run **inside** the cross-validation loop. Selecting 20 of 5,000 pure-noise features on all the data and then cross-validating reports 88% accuracy on random labels; inside the loop it reports the truth, about 52%.

## 2.8 Text features: bag of words and TF-IDF {#ml-2-8}

**Bag of words** counts each word (optionally n-grams). **TF-IDF** reweights the count by the word's rarity across the corpus:

$$\text{tf-idf}(t, d) = \text{tf}(t, d)\cdot \log\frac{N}{\text{df}(t)}$$

with $N$ documents and $\text{df}(t)$ the number containing $t$. scikit-learn's default smooths it to $\ln\frac{1+N}{1+\text{df}} + 1$ and then L2-normalises each document.

<div class="nb nb-example">

<strong>Example</strong> (IDF by hand)

Three documents; "the" appears in 2, "cat" in 1. Textbook IDF: "the" $\ln(3/2) = 0.405$, "cat" $\ln 3 = 1.099$. Common words get small weights. State the log base: with $\log_{10}$, "cat" is 0.477.

</div>

TF-IDF vectors are sparse, compared with cosine similarity, and fed to linear models or naive Bayes. They ignore word order beyond n-grams and know no synonyms: that gap is what embeddings fill.

## 2.9 Time series and recommenders, one paragraph each {#ml-2-9}

**Time series** are not i.i.d. Build lag features, rolling statistics (from the past only), calendar and holiday flags; validate with **forward-chaining** splits, never shuffled ones; and remember that tree ensembles cannot extrapolate a trend (model differences instead). Classical models assume **stationarity**; differencing removes trends; ARIMA($p, d, q$) is autoregression plus differencing plus a moving average of past errors.

**Recommenders:** content-based (item features) or collaborative filtering (the rating matrix itself), by item–item similarity or **matrix factorisation** $R \approx UV^\top$ fitted on observed entries only (alternating least squares). Practical issues: implicit feedback, user and item biases, the **cold-start** problem, and ranking metrics such as precision@k and NDCG.

<div class="nb nb-moral">

Fit every transform inside the training fold; scale for distances and penalties, not for trees; treat missingness and rare categories as information to estimate carefully, not noise to paper over.

</div>
