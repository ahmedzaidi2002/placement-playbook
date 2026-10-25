---
title: "11 · Evaluation and model selection"
linkTitle: "11 Evaluation"
weight: 11
math: true
---
Most failed ML projects fail at measurement, not modelling: the wrong metric, a leaky split, a test set consulted twenty times. Expect precision and recall from a confusion matrix in one minute, AUC by hand, "accuracy is 97%, is the model good?", and "how did you choose the hyperparameters without fooling yourself?"

## 11.1 The confusion matrix {#ml-11-1}

1,000 transactions, 60 frauds; the model flags 50, of which 40 are fraud:

| | predicted positive | predicted negative |
|---|---|---|
| **actual positive** | TP = 40 | FN = 20 |
| **actual negative** | FP = 10 | TN = 930 |

| Metric | Formula | Here | Question it answers |
|---|---|---|---|
| Accuracy | $\frac{TP+TN}{\text{all}}$ | 0.970 | fraction correct |
| Precision | $\frac{TP}{TP+FP}$ | 0.800 | of the flagged, how many are fraud? |
| Recall (sensitivity, TPR) | $\frac{TP}{TP+FN}$ | 0.667 | of the frauds, how many did we catch? |
| Specificity (TNR) | $\frac{TN}{TN+FP}$ | 0.989 | of the genuine, how many passed? |
| FPR | $\frac{FP}{FP+TN}$ | 0.011 | false-alarm rate |
| F1 | $\frac{2PR}{P+R}$ | 0.727 | harmonic mean of P and R |

A model that says "not fraud" for everyone scores **94%** accuracy with recall 0. With imbalanced classes, accuracy is nearly meaningless.

- **F1** is the *harmonic* mean, so it is dragged towards the smaller of P and R. $F_\beta$ weights recall $\beta$ times as much ($F_2$ for recall-heavy problems).
- **Balanced accuracy** is the mean of TPR and TNR; **MCC** is the correlation between predictions and labels, robust to imbalance.

<div class="nb nb-remark">

<strong>Choose the metric by the cost of a mistake</strong> — Missing a positive is costly (cancer screening, fraud): **recall**. False alarms are costly (a spam filter hiding real mail, wrongly rejecting a loan): **precision**. Both matter: **F1**. Comparing models across thresholds: **ROC-AUC or PR-AUC**.

</div>

<div class="nb nb-remark">

<strong>Trap</strong> — Precision depends on how common positives are; recall and specificity do not. The same model (TPR 0.9, FPR 0.05) deployed where positives are 10% has precision $0.09/(0.09 + 0.045) = 0.67$; where they are 0.5%, precision falls to about 0.08.

</div>

**Multiclass:** compute per-class precision, recall and F1, then average. **Macro** = plain mean (every class equal; use when minority classes matter), **weighted** = mean weighted by class size, **micro** = pool all counts first (for single-label multiclass, micro-F1 = accuracy).

## 11.2 ROC and PR curves {#ml-11-2}

A scoring classifier gives a curve, not a point. Sweep the threshold from high to low:

- **ROC curve:** TPR against FPR. **AUC** summarises it: 0.5 is random ranking, 1.0 perfect, below 0.5 an inverted ranking.
- **PR curve:** precision against recall; **average precision** (PR-AUC) summarises it.

**AUC has a clean meaning:** the probability that a randomly chosen positive is scored above a randomly chosen negative (ties count half).

<div class="nb nb-example">

<strong>Example</strong> (AUC by counting pairs)

Positives score 0.9, 0.6, 0.4; negatives 0.7, 0.3. Of the $3\times 2 = 6$ positive–negative pairs, correctly ordered: 0.9 beats both, 0.6 beats 0.3, 0.4 beats 0.3, so $4/6 = 0.667$.

</div>

AUC is threshold-free and unchanged by any monotone transform of the scores, so it says **nothing about calibration**.

<div class="nb nb-remark">

<strong>Trap</strong> — "AUC 0.9, so the model is great." With 1% positives, a logistic model had ROC-AUC 0.90 but average precision **0.19**: FPR is tiny relative to the huge negative class, yet in absolute numbers the false positives swamp the true ones. For rare positives, report PR-AUC and precision at the operating recall.

</div>

## 11.3 Regression and probabilistic metrics {#ml-11-3}

| Metric | Formula | Notes |
|---|---|---|
| MAE | mean $\lvert e\rvert$ | in the target's units; minimised by the median; robust |
| MSE / RMSE | mean $e^2$ / its root | punishes large misses; minimised by the mean |
| MAPE | mean $\lvert e/y\rvert$ | undefined at $y = 0$; asymmetric |
| $R^2$ | $1 - \text{SS}_{\text{res}}/\text{SS}_{\text{tot}}$ | vs predicting the mean; can be negative on test |

<div class="nb nb-example">

<strong>Example</strong> (MAE vs RMSE)

Errors $2, -2, 4$: MAE $= 8/3 = 2.67$; squares $4, 4, 16$ have mean 8, so RMSE $= \sqrt 8 = 2.83$. RMSE ≥ MAE always; the gap grows with big misses. Report RMSE when a delivery 3 hours late is far worse than three 1-hour delays.

</div>

Probabilities should be judged as probabilities: **log-loss** and the **Brier score** (mean squared error of the probability) are *proper scoring rules*, minimised by the true probabilities.

## 11.4 Cross-validation {#ml-11-4}

**k-fold CV:** split into $k$ folds, train on $k - 1$, validate on the one left out, repeat $k$ times, average. $k = 5$ or $10$ is the usual compromise; leave-one-out ($k = n$) is nearly unbiased but high-variance and costs $n$ fits. In 5-fold CV each model trains on 80% of the data; 1,000 rows give folds of 200.

- **Stratified k-fold:** keeps class proportions (the default for classification).
- **Group k-fold:** all rows of a patient or user stay in one fold.
- **Time-series (forward-chaining):** train on the past, validate on the future; never shuffle.

<div class="nb nb-example">

<strong>Example</strong> (Shuffled CV on a time series)

A trending series and a random forest on the time index: shuffled 5-fold CV reports MAE 0.29 (each validation day sits between training days); forward-chaining reports 1.12, because the forest cannot extrapolate the trend. The second number is what production will see.

</div>

**Counting fits:** a grid of $3 \times 4 \times 2 = 24$ settings with 5-fold CV trains $24 \times 5 = 120$ models.

## 11.5 Leakage {#ml-11-5}

Information in training that will not be available at prediction time:

1. **Preprocessing on all data before splitting:** scaling, imputation, PCA, feature selection, target encoding, SMOTE.
2. **Target leakage:** a feature computed after the outcome ("refund issued" to predict fraud).
3. **Temporal leakage:** random splits of time-ordered data; features from future aggregates.
4. **Group leakage:** the same entity in train and test.
5. **Duplicates** across the split.
6. **Tuning on the test set.**

<div class="nb nb-remark">

<strong>Trap</strong> — "My validation score is much better than expected" is a leakage alarm, not a celebration. The defence: a **pipeline** (every fitted transform inside the CV loop) and a split that mirrors deployment (by time, by group).

</div>

## 11.6 Hyperparameter search, nested CV, AIC and BIC {#ml-11-6}

**Grid search** tries every combination; **random search** explores more values of the parameters that matter for the same budget; **Bayesian optimisation** fits a surrogate and picks promising points; successive halving / Hyperband stop bad configurations early.

The best inner-CV score of any search is **optimistically biased**. **Nested CV** wraps the whole search in an outer loop to estimate the performance of the *procedure*. In one test, the best inner score averaged 0.768, nested CV said 0.750, and the tuned models scored 0.749 on fresh data.

**Information criteria** (lower is better, no validation set needed): $\text{AIC} = 2k - 2\ln\hat L$, $\text{BIC} = k\ln n - 2\ln\hat L$. BIC's penalty is harsher once $n \ge 8$, so it picks smaller models. They compare models on the **same** data; "lower BIC means a more accurate model" is a misreading.

## 11.7 Calibration {#ml-11-7}

A classifier is **calibrated** if, among cases given probability 0.8, about 80% are positive. Check with a reliability diagram or the expected calibration error. Logistic regression is usually well calibrated; **naive Bayes, SVM scores, boosted trees and modern deep nets often are not**. Fix on held-out data with **Platt scaling** (a sigmoid on the scores) or **isotonic regression** (a monotone step function; needs more data). Calibration leaves AUC essentially unchanged.

## 11.8 Which metric when {#ml-11-8}

| Situation | Report |
|---|---|
| Balanced classes | accuracy |
| False alarms costly | precision |
| Misses costly | recall |
| Imbalanced, need both | F1, PR-AUC |
| Compare models across thresholds | ROC-AUC (balanced), PR-AUC (rare positives) |
| Predicting a number | RMSE, MAE, $R^2$ |
| Small data, need a reliable score | k-fold cross-validation |
| Train score far above test score | regularise or get more data |

<div class="nb nb-moral">

Pick the metric from the cost of each error, the split from how the model will be deployed, and never let a number you report have helped choose the model.

</div>
