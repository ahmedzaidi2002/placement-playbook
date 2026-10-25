---
title: "14 · OA practice problems"
linkTitle: "14 OA practice"
weight: 14
math: true
---
Forty problems in the three shapes online assessments use: one-minute numericals, "which statements are true" multi-selects, and short reasoning questions. Aim for a minute or two each with a basic calculator. The hint and the solution are folded under each problem; try it first.

## 14.1 Basics and data preparation {#ml-14-1}

<div class="nb nb-problem nb-block" id="problem-ml-1">

<strong>Problem 1</strong> (Median fill)

Salaries (₹ thousand) are 30, 35, 40, (missing), 90. Fill the gap with the median of the known values.

<details class="nb-hint">
<summary>Hint</summary>

Four known values: the median is the mean of the middle two.

</details>

<details class="nb-sol">
<summary>Solution</summary>

$(35 + 40)/2 = 37.5$. The mean (48.75) would be dragged up by the 90, which is why the median is the safe fill for skewed numbers.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-ml-2">

<strong>Problem 2</strong> (Scaling)

(a) A feature has mean 70 and SD 8: z-score of 58? (b) Min 25, max 125: min–max value of 75? (c) A city column has six values: how many one-hot columns?

<details class="nb-hint">
<summary>Hint</summary>

$z = (x - \mu)/\sigma$; min–max $= (x - \min)/(\max - \min)$.

</details>

<details class="nb-sol">
<summary>Solution</summary>

(a) $(58 - 70)/8 = -1.5$. (b) $(75 - 25)/100 = 0.5$. (c) 6 (5 if you drop one level for an unpenalised linear model).

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-ml-3">

<strong>Problem 3</strong> (Splits and baselines)

(a) 5,000 rows split 70/15/15: how many in validation? (b) 1,200 emails, 300 spam: accuracy of "always not spam"? (c) 2,000 rows, 100 fraud, stratified 75/25 split: fraud rows in the test set?

<details class="nb-hint">
<summary>Hint</summary>

Stratification keeps the fraud rate the same in every part.

</details>

<details class="nb-sol">
<summary>Solution</summary>

(a) 750. (b) $900/1200 = 75\%$. (c) The test set has 500 rows at 5% fraud: 25.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-ml-4">

<strong>Problem 4</strong> (Spot the leak)

A churn model uses tenure, plan type, support calls in the last 30 days, "account closure reason", average bill, and last quarter's churn score. The split is random over customer-months. List the problems.

<details class="nb-hint">
<summary>Hint</summary>

Which feature only exists after churn? Which split mixes the same customer across train and test?

</details>

<details class="nb-sol">
<summary>Solution</summary>

"Account closure reason" is target leakage (it exists only after churn). A random split over customer-months puts the same customer, and future months, in both sets: split by customer and by time. Last quarter's churn score is fine only if it was computed strictly before the prediction date.

</details>

</div>

## 14.2 Regression and regularisation {#ml-14-2}

<div class="nb nb-problem nb-block" id="problem-ml-5">

<strong>Problem 5</strong> (Least-squares line)

Fit $y = b_0 + b_1 x$ to $(2,3), (4,5), (6,6), (8,9), (10,12)$. Give $b_1$, $b_0$, the prediction at $x = 7$ and $R^2$.

<details class="nb-hint">
<summary>Hint</summary>

$\bar x = 6$ is an integer, so use the centred form $\sum(x - \bar x)(y - \bar y)/\sum(x - \bar x)^2$.

</details>

<details class="nb-sol">
<summary>Solution</summary>

$\bar x = 6$, $\bar y = 7$; $\sum dx\,dy = 16 + 4 + 0 + 4 + 20 = 44$, $\sum dx^2 = 40$, so $b_1 = 1.1$, $b_0 = 7 - 6.6 = 0.4$. At $x = 7$: $8.1$. Residuals $0.4, 0.2, -1.0, -0.2, 0.6$ give RSS $= 1.6$; TSS $= 50$; $R^2 = 0.968$.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-ml-6">

<strong>Problem 6</strong> (Slope from summary statistics)

For 100 students, $r = 0.6$ between study hours and score, $s_{\text{hours}} = 2$, $s_{\text{score}} = 10$, mean hours 5, mean score 60. Give the regression line of score on hours, the prediction for 8 hours, and the slope of hours on score.

<details class="nb-hint">
<summary>Hint</summary>

$b_1 = r\,s_y/s_x$ and the line passes through the means.

</details>

<details class="nb-sol">
<summary>Solution</summary>

$b_1 = 0.6 \times 10/2 = 3$, $b_0 = 60 - 15 = 45$; at 8 hours, 69. Hours on score: $0.6 \times 2/10 = 0.12$, not $1/3$.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-ml-7">

<strong>Problem 7</strong> (Predict and step)

(a) Price $= 10 + 0.04\times\text{area} + 5\times\text{rooms}$ (₹ lakh): predict for 1,200 sq ft and 3 rooms. (b) Weight 2, loss slope $-4$, learning rate 0.05: weight after one gradient step?

<details class="nb-hint">
<summary>Hint</summary>

$w \leftarrow w - \alpha \times \text{slope}$; a negative slope moves the weight up.

</details>

<details class="nb-sol">
<summary>Solution</summary>

(a) $10 + 48 + 15 = 73$. (b) $2 - 0.05\times(-4) = 2.2$.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-ml-8">

<strong>Problem 8</strong> (Adjusted R²)

$n = 30$. Model A: 2 features, $R^2 = 0.62$. Model B: 6 features, $R^2 = 0.66$. Which has the higher adjusted $R^2$?

<details class="nb-hint">
<summary>Hint</summary>

$R^2_{\text{adj}} = 1 - (1 - R^2)(n-1)/(n-p-1)$.

</details>

<details class="nb-sol">
<summary>Solution</summary>

A: $1 - 0.38 \times 29/27 = 0.592$. B: $1 - 0.34 \times 29/23 = 0.571$. A wins: B's extra four features do not pay for themselves.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-ml-9">

<strong>Problem 9</strong> (The augmented error, multi-select)

For $E_{\text{aug}}(w) = E_{\text{in}}(w) + \lambda\|w\|^2$, which are true? (a) $\lambda = 0$ gives the unregularised fit. (b) Large $\lambda$ lowers training error. (c) Large $\lambda$ increases bias. (d) $\lambda$ should minimise $E_{\text{in}}$. (e) As $\lambda \to \infty$ the penalised weights go to zero.

<details class="nb-hint">
<summary>Hint</summary>

What would minimising training error choose for $\lambda$?

</details>

<details class="nb-sol">
<summary>Solution</summary>

(a), (c), (e). Larger $\lambda$ raises training error (b false); choosing $\lambda$ by $E_{\text{in}}$ would always give $\lambda = 0$ (d false): use validation.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-ml-10">

<strong>Problem 10</strong> (Lasso vs ridge)

Orthonormal features, OLS coefficients $(1.8, -0.3, 0.6)$. Give the lasso solution with threshold 0.5 and the ridge solution $\hat w/(1 + \lambda)$ with $\lambda = 0.5$.

<details class="nb-hint">
<summary>Hint</summary>

Lasso soft-thresholds: subtract 0.5 from each absolute value, floor at 0, keep the sign.

</details>

<details class="nb-sol">
<summary>Solution</summary>

Lasso $(1.3, 0, 0.1)$: the small coefficient is zeroed. Ridge $(1.2, -0.2, 0.4)$: everything shrunk by the same factor, nothing zero.

</details>

</div>

## 14.3 Classifiers {#ml-14-3}

<div class="nb nb-problem nb-block" id="problem-ml-11">

<strong>Problem 11</strong> (Neuron output and log-loss)

$w = (0.5, -1.0)$, $b = 0.25$, $x = (2, 1)$, true label 1. Compute $z$, $p$, the class at threshold 0.5 and the log-loss.

<details class="nb-hint">
<summary>Hint</summary>

$p = 1/(1 + e^{-z})$ and log-loss $= -\ln p$ for a positive.

</details>

<details class="nb-sol">
<summary>Solution</summary>

$z = 1 - 1 + 0.25 = 0.25$; $p = \sigma(0.25) = 0.562$; class 1; log-loss $= -\ln 0.562 = 0.576$.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-ml-12">

<strong>Problem 12</strong> (Odds ratio)

A churn model's coefficient on "number of complaints" is 0.4. A customer with 2 complaints has churn probability 0.2. What is it with 5 complaints, other features equal?

<details class="nb-hint">
<summary>Hint</summary>

Work in odds: each complaint multiplies the odds by $e^{0.4}$.

</details>

<details class="nb-sol">
<summary>Solution</summary>

Odds $0.2/0.8 = 0.25$; three more complaints multiply by $e^{1.2} = 3.32$, giving 0.830; probability $0.830/1.830 = 0.454$. Not $0.2 + 3\times 0.4$.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-ml-13">

<strong>Problem 13</strong> (Naive Bayes)

$P(\text{spam}) = 0.3$, $P(\text{"offer"} \mid \text{spam}) = 0.6$, $P(\text{"offer"} \mid \text{ham}) = 0.2$. An email contains "offer". $P(\text{spam} \mid \text{"offer"})$?

<details class="nb-hint">
<summary>Hint</summary>

Score each class by prior × likelihood, then normalise.

</details>

<details class="nb-sol">
<summary>Solution</summary>

Spam $0.3 \times 0.6 = 0.18$, ham $0.7 \times 0.2 = 0.14$; $0.18/0.32 = 0.5625$.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-ml-14">

<strong>Problem 14</strong> (Laplace smoothing)

The positive-review class has 500 tokens; vocabulary $V = 1000$. "refund" occurs 0 times in positive reviews and 12 times among 800 negative tokens. Give both smoothed probabilities ($\alpha = 1$) and their ratio.

<details class="nb-hint">
<summary>Hint</summary>

$(N_{cj} + 1)/(N_c + V)$.

</details>

<details class="nb-sol">
<summary>Solution</summary>

Positive $1/1500 = 0.000667$; negative $13/1800 = 0.00722$; the word is about 10.8 times likelier in negative reviews. Without smoothing the positive probability would be 0 and one word would decide the class.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-ml-15">

<strong>Problem 15</strong> (k-NN by hand)

$k = 1$, classify $(3, 3)$. Neighbours: A $(1, 1)$ Red, B $(4, 4)$ Blue, C $(3, 6)$ Red.

<details class="nb-hint">
<summary>Hint</summary>

Compare squared distances; no square roots needed.

</details>

<details class="nb-sol">
<summary>Solution</summary>

Squared distances 8, 2, 9: B is nearest, so **Blue**, even though Red has more points. With $k = 3$ it would be Red.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-ml-16">

<strong>Problem 16</strong> (Distances)

$a = (2, -1, 3)$, $b = (0, 1, 4)$: Euclidean, Manhattan, Chebyshev distance and cosine similarity.

<details class="nb-hint">
<summary>Hint</summary>

Differences $(2, -2, -1)$; $a^\top b$ and both norms for cosine.

</details>

<details class="nb-sol">
<summary>Solution</summary>

Euclidean $\sqrt{4+4+1} = 3$; Manhattan 5; Chebyshev 2. $a^\top b = 0 - 1 + 12 = 11$, $\|a\| = \sqrt{14}$, $\|b\| = \sqrt{17}$; cosine $= 11/15.43 = 0.713$.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-ml-17">

<strong>Problem 17</strong> (Curse of dimensionality)

Data are uniform in $[0, 1]^{50}$. What edge length must a sub-cube have to contain 5% of the data?

<details class="nb-hint">
<summary>Hint</summary>

Volume $= \text{edge}^{50}$.

</details>

<details class="nb-sol">
<summary>Solution</summary>

$0.05^{1/50} = e^{\ln 0.05/50} = e^{-0.060} = 0.94$: a "local" neighbourhood spans 94% of every axis.

</details>

</div>

## 14.4 SVMs, trees and ensembles {#ml-14-4}

<div class="nb nb-problem nb-block" id="problem-ml-18">

<strong>Problem 18</strong> (Margin)

A linear SVM has $w = (1, -2, 2)$, $b = 0.5$. Street width? Is the positive point $(1, 1, 1)$ a support vector?

<details class="nb-hint">
<summary>Hint</summary>

Width $2/\|w\|$; support vectors have $y f(x) \le 1$.

</details>

<details class="nb-sol">
<summary>Solution</summary>

$\|w\| = 3$, width $2/3$. $f = 1 - 2 + 2 + 0.5 = 1.5 > 1$: outside the street, so $\alpha = 0$ and it is **not** a support vector.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-ml-19">

<strong>Problem 19</strong> (Kernels and hinge)

(a) For $x = (1, 2)$, $z = (2, -1)$ compute $(x^\top z + 2)^2$ and the RBF kernel with $\gamma = 0.5$. (b) Scores $(2, 0.5, -0.3, -1.5)$ with labels $(+, +, +, -)$: hinge losses, their mean, and the support vectors.

<details class="nb-hint">
<summary>Hint</summary>

Hinge $= \max(0, 1 - y f)$.

</details>

<details class="nb-sol">
<summary>Solution</summary>

(a) $x^\top z = 0$, so $(0 + 2)^2 = 4$; $\|x - z\|^2 = 1 + 9 = 10$, RBF $= e^{-5} = 0.0067$. (b) Margins $2, 0.5, -0.3, 1.5$; losses $0, 0.5, 1.3, 0$; mean 0.45. Support vectors: the second (inside the street) and the third (misclassified).

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-ml-20">

<strong>Problem 20</strong> (Information gain)

A node has 9 positives and 7 negatives. A split sends $(7, 1)$ left and $(2, 6)$ right. Compute the information gain.

<details class="nb-hint">
<summary>Hint</summary>

Both children have 8 points, so the weights are $\tfrac12$ each.

</details>

<details class="nb-sol">
<summary>Solution</summary>

Parent $H(9/16) = 0.989$; left $H(7/8) = 0.544$; right $H(2/8) = 0.811$; weighted 0.677; gain $0.989 - 0.677 = 0.311$ bits.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-ml-21">

<strong>Problem 21</strong> (Gini decrease)

Parent $(10, 10)$ is split into $(9, 3)$ and $(1, 7)$. Weighted child Gini and the decrease?

<details class="nb-hint">
<summary>Hint</summary>

Gini $= 1 - \sum p^2$; weights 12/20 and 8/20.

</details>

<details class="nb-sol">
<summary>Solution</summary>

Children: $1 - 0.75^2 - 0.25^2 = 0.375$ and $1 - (1/8)^2 - (7/8)^2 = 0.219$. Weighted $0.6(0.375) + 0.4(0.219) = 0.3125$. Decrease from 0.5: **0.1875**.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-ml-22">

<strong>Problem 22</strong> (Bootstrap with $n = 4$)

(a) Probability that row 1 is absent from a bootstrap sample? (b) That all four rows appear? (c) Expected number of distinct rows?

<details class="nb-hint">
<summary>Hint</summary>

(b) counts the orderings of four distinct rows among $4^4$ samples; (c) uses linearity of expectation.

</details>

<details class="nb-sol">
<summary>Solution</summary>

(a) $(3/4)^4 = 0.316$. (b) $4!/4^4 = 24/256 = 0.094$. (c) $4 \times (1 - 0.316) = 2.73$, i.e. 68% of rows (approaching 63.2% as $n$ grows).

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-ml-23">

<strong>Problem 23</strong> (An AdaBoost round)

Five points with equal weights; the first stump misclassifies exactly one. Compute $\varepsilon_1$, $\alpha_1$ and the normalised weights after the update.

<details class="nb-hint">
<summary>Hint</summary>

$\alpha = \tfrac12\ln\frac{1-\varepsilon}{\varepsilon}$; wrong points × $e^{\alpha}$, right points × $e^{-\alpha}$.

</details>

<details class="nb-sol">
<summary>Solution</summary>

$\varepsilon_1 = 0.2$, $\alpha_1 = \tfrac12\ln 4 = 0.693$, so $e^{\alpha} = 2$. Unnormalised: wrong $0.4$, each right $0.1$ (total 0.8). Normalised: the misclassified point gets **0.5**, each of the others 0.125.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-ml-24">

<strong>Problem 24</strong> (Ensembles, multi-select)

Which are true? (a) Random forests reduce bias compared with one deep tree. (b) Boosting trains its learners sequentially. (c) More trees in a random forest cause overfitting. (d) XGBoost uses second derivatives of the loss. (e) OOB error needs a separate validation set. (f) Impurity-based importance is biased towards high-cardinality features.

<details class="nb-hint">
<summary>Hint</summary>

Forests attack variance; OOB uses the rows each tree did not see.

</details>

<details class="nb-sol">
<summary>Solution</summary>

(b), (d), (f).

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-ml-25">

<strong>Problem 25</strong> (XGBoost leaf)

A leaf receives squared-error gradients $g = (-2, -1, 0.5, -1.5)$ with $h = 1$ each. Its weight with $\lambda = 2$? With $\lambda = 0$?

<details class="nb-hint">
<summary>Hint</summary>

$w^\star = -G/(H + \lambda)$.

</details>

<details class="nb-sol">
<summary>Solution</summary>

$G = -4$, $H = 4$: $w = 4/6 = 0.667$; with $\lambda = 0$, $w = 1.0$ (the mean residual). $\lambda$ shrinks leaf values towards 0.

</details>

</div>

## 14.5 Unsupervised, evaluation and statistics {#ml-14-5}

<div class="nb nb-problem nb-block" id="problem-ml-26">

<strong>Problem 26</strong> (k-means with an outlier)

1-D points 1, 2, 3, 8, 9, 10, 25; initial centroids 2 and 9. Do one assignment and update. What happens next?

<details class="nb-hint">
<summary>Hint</summary>

25 is closer to 9 than to 2.

</details>

<details class="nb-sol">
<summary>Solution</summary>

Clusters $\{1, 2, 3\}$ and $\{8, 9, 10, 25\}$; new centroids 2 and 13. Reassigning changes nothing, so it has converged. The outlier dragged the second centroid from 9 to 13: means are not robust (k-medoids would keep 9).

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-ml-27">

<strong>Problem 27</strong> (PCA of a 2×2 covariance)

Centred data have covariance $\begin{pmatrix} 3 & 1 \\ 1 & 3 \end{pmatrix}$. Principal directions, variances along them, the share PC1 explains, and the projection of $(2, 0)$ on PC1?

<details class="nb-hint">
<summary>Hint</summary>

Trace 6 and determinant 8 give the eigenvalues.

</details>

<details class="nb-sol">
<summary>Solution</summary>

Eigenvalues 4 and 2, directions $(1, 1)/\sqrt2$ and $(1, -1)/\sqrt2$. PC1 explains $4/6 = 66.7\%$. Projection $2/\sqrt2 = 1.414$.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-ml-28">

<strong>Problem 28</strong> (Metrics from a confusion matrix)

A test on 500 people: TP 45, FN 5, FP 30, TN 420. Accuracy, precision, recall, specificity, F1?

<details class="nb-hint">
<summary>Hint</summary>

Precision divides by predicted positives, recall by actual positives.

</details>

<details class="nb-sol">
<summary>Solution</summary>

Accuracy $465/500 = 0.93$; precision $45/75 = 0.60$; recall $45/50 = 0.90$; specificity $420/450 = 0.933$; F1 $= 2(0.6)(0.9)/1.5 = 0.72$.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-ml-29">

<strong>Problem 29</strong> (Quick metrics)

(a) F1 for precision 0.75, recall 0.5. (b) RMSE for errors $1, -3, 3, -1$. (c) $R^2$ for $\text{SS}_{\text{res}} = 45$, $\text{SS}_{\text{tot}} = 150$.

<details class="nb-hint">
<summary>Hint</summary>

F1 is the harmonic mean.

</details>

<details class="nb-sol">
<summary>Solution</summary>

(a) $2(0.75)(0.5)/1.25 = 0.6$. (b) Squares mean $(1 + 9 + 9 + 1)/4 = 5$, RMSE $\sqrt5 = 2.24$. (c) $1 - 0.3 = 0.7$.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-ml-30">

<strong>Problem 30</strong> (Counting CV)

(a) 4-fold scores 0.70, 0.75, 0.80, 0.75: CV score? (b) 1,200 rows, 10-fold: rows per validation fold? (c) A $5 \times 3$ grid with 4-fold CV: models trained?

<details class="nb-hint">
<summary>Hint</summary>

Grid size × folds.

</details>

<details class="nb-sol">
<summary>Solution</summary>

(a) 0.75. (b) 120. (c) $15 \times 4 = 60$.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-ml-31">

<strong>Problem 31</strong> (AUC by counting)

Positives score 0.9, 0.6, 0.4; negatives 0.7, 0.3. ROC-AUC?

<details class="nb-hint">
<summary>Hint</summary>

AUC = fraction of positive–negative pairs ordered correctly.

</details>

<details class="nb-sol">
<summary>Solution</summary>

6 pairs; 0.9 beats both, 0.6 beats 0.3, 0.4 beats 0.3: $4/6 = 0.667$.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-ml-32">

<strong>Problem 32</strong> (Precision at a new prevalence)

A classifier has TPR 0.9 and FPR 0.05. Its precision when 10% of cases are positive? When 0.5% are?

<details class="nb-hint">
<summary>Hint</summary>

Per 1,000 cases, count true and false positives.

</details>

<details class="nb-sol">
<summary>Solution</summary>

10%: TP $= 90$, FP $= 45$, precision $0.67$. 0.5%: TP $= 4.5$, FP $= 49.75$, precision $0.08$. Same model, very different precision.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-ml-33">

<strong>Problem 33</strong> (Bayes with base rates)

Prevalence 1%, sensitivity 95%, specificity 90%. $P(\text{disease} \mid +)$?

<details class="nb-hint">
<summary>Hint</summary>

$P(+) = P(+ \mid D)P(D) + P(+ \mid \neg D)P(\neg D)$.

</details>

<details class="nb-sol">
<summary>Solution</summary>

$0.0095/(0.0095 + 0.099) = 0.088$: under 9%.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-ml-34">

<strong>Problem 34</strong> (Poisson)

A server averages 3 errors per hour. Probability of no error in an hour? Of at least 2?

<details class="nb-hint">
<summary>Hint</summary>

$P(k) = e^{-\lambda}\lambda^k/k!$.

</details>

<details class="nb-sol">
<summary>Solution</summary>

$e^{-3} = 0.050$. $P(\ge 2) = 1 - e^{-3}(1 + 3) = 0.801$.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-ml-35">

<strong>Problem 35</strong> (t-test)

16 response times: mean 210 ms, SD 40 ms. Test $H_0: \mu = 200$ two-sided at 5% ($t_{0.975,15} = 2.131$).

<details class="nb-hint">
<summary>Hint</summary>

$t = (\bar x - \mu_0)/(s/\sqrt n)$.

</details>

<details class="nb-sol">
<summary>Solution</summary>

$t = 10/(40/4) = 1.0 < 2.131$: do not reject. "Not significant" is not "no effect": 16 samples cannot resolve a 10 ms difference with this much spread.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-ml-36">

<strong>Problem 36</strong> (Which test?)

(a) Spend of the same 50 users before and after a redesign. (b) Click-through of two independent ad variants. (c) Whether city and payment method are related. (d) Mean delivery time across four warehouses.

<details class="nb-hint">
<summary>Hint</summary>

Same units twice? Proportions? Two categorical variables? More than two means?

</details>

<details class="nb-sol">
<summary>Solution</summary>

(a) Paired t. (b) Two-proportion z-test (or $\chi^2$ on the 2×2 table). (c) $\chi^2$ test of independence. (d) One-way ANOVA.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-ml-37">

<strong>Problem 37</strong> (AIC vs BIC)

$n = 100$. Model A: 3 parameters, $\ln\hat L = -120$. Model B: 6 parameters, $\ln\hat L = -114$. Which does AIC prefer? BIC? ($\ln 100 = 4.605$)

<details class="nb-hint">
<summary>Hint</summary>

AIC $= 2k - 2\ln\hat L$; BIC $= k\ln n - 2\ln\hat L$; lower wins.

</details>

<details class="nb-sol">
<summary>Solution</summary>

AIC: A 246, B 240, so **B**. BIC: A $13.8 + 240 = 253.8$, B $27.6 + 228 = 255.6$, so **A**. BIC's harsher penalty picks the smaller model.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-ml-38">

<strong>Problem 38</strong> (Association rule)

1,000 orders: 200 contain chips, 300 cola, 120 both. Support of the pair, confidence of chips ⇒ cola, and lift. Useful?

<details class="nb-hint">
<summary>Hint</summary>

Lift = confidence / support of the consequent.

</details>

<details class="nb-sol">
<summary>Solution</summary>

Support 0.12; confidence $120/200 = 0.6$; lift $0.6/0.3 = 2.0$. Yes: chips buyers are twice as likely as average to buy cola.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-ml-39">

<strong>Problem 39</strong> (Diagnose from numbers)

Model A: training MSE 4.1, validation 4.3, noise variance believed about 1. Model B: training 0.2, validation 6.0. For each, raise or lower $\lambda$? Would more data help?

<details class="nb-hint">
<summary>Hint</summary>

Compare training error with the noise floor, and the gap.

</details>

<details class="nb-sol">
<summary>Solution</summary>

A underfits (training error far above the noise floor, small gap): lower $\lambda$ or use a richer model; more data will not help. B overfits (huge gap): raise $\lambda$ or simplify; more data will help.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-ml-40">

<strong>Problem 40</strong> (Scaling, true or false)

(a) Standardising features changes a random forest's predictions. (b) k-means results depend on feature units. (c) PCA should run on standardised data when features have different units. (d) Gradient descent on linear regression converges faster after standardising. (e) The scaler should be fitted on train and test together for consistency.

<details class="nb-hint">
<summary>Hint</summary>

Which methods use distances or variances; where does leakage come from?

</details>

<details class="nb-sol">
<summary>Solution</summary>

True: (b), (c), (d). False: (a) trees are invariant to monotone rescaling; (e) fitting on test data leaks.

</details>

</div>
