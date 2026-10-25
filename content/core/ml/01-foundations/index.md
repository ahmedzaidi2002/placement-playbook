---
title: "1 · The setup: what ML is and how it fails"
linkTitle: "1 The setup"
weight: 1
math: true
---
Every question in this book is secretly about one sentence: **we choose a function using a finite sample, and we are judged on data we have not seen.** This chapter fixes the vocabulary that one-line MCQs love to blur.

## 1.1 What machine learning is {#ml-1-1}

Instead of writing the rules yourself, you show the computer examples and it works out the rule: *data + answers → model → predictions*. A 1,000-email labelled set becomes a spam filter.

- **AI** is the broad goal of machines that act intelligently. **ML** is one way to get there: systems that learn patterns from data. **Deep learning** is one kind of ML, using many-layered neural networks.
- **Features** are the inputs (area, rooms, city), the **label** is the answer (price), the **model** is the learned map $f(\text{features}) \to \text{label}$, and the **algorithm** is the recipe that produces the model (k-NN, a decision tree).

<div class="nb nb-remark">

<strong>Interview one-liner</strong> — "Explain ML to a child": *if I show you many photos of cats and dogs and tell you which is which, soon you can name a new photo yourself. ML is a computer learning the same way, from examples.*

</div>

## 1.2 The kinds of learning problem {#ml-1-2}

The type of problem is set by **what supervision you have at training time**, not by the algorithm.

| Regime | What you have | Example |
|---|---|---|
| Supervised | pairs $(x_i, y_i)$ | price of a flat; fraud or not |
| Unsupervised | only $x_i$ | customer segments; anomaly scores |
| Semi-supervised | a few labels, many unlabelled $x$ | 200 labelled photos, 50,000 unlabelled |
| Self-supervised | labels made from the input itself | mask a word and predict it (BERT pre-training) |
| Reinforcement | actions, states and a delayed reward | a bot learning a game from wins and losses |

Within supervised learning: a **number on a scale** is **regression**; a **category** is **classification** (binary, multiclass, or **multilabel** if several labels can be on at once).

<div class="nb nb-remark">

<strong>Trap</strong> — "Predicting goals in a match (0, 1, 2, …) is classification because the output is discrete." Counts are ordered and arithmetic on them is meaningful, so it is regression (Poisson regression). Discreteness alone does not make a problem classification; *unordered categories* do. And "customer segmentation" is clustering unless someone hands you segment labels.

</div>

<div class="nb nb-remark">

<strong>Trap</strong> — Self-supervised is not the same as unsupervised. Both use unlabelled data, but self-supervised learning trains an ordinary supervised loss on a pretext task. If an option says "BERT pre-training is unsupervised", many keys accept it; the precise word is self-supervised.

</div>

Two more distinctions that appear as MCQ options:

- **Parametric** models have a fixed number of parameters whatever $n$ is (linear and logistic regression). **Non-parametric** models grow with the data (k-NN stores all of it; a full tree can have $n$ leaves).
- **Discriminative** models learn $p(y \mid x)$ or a boundary directly (logistic regression, SVM). **Generative** models learn $p(x \mid y)$ and $p(y)$ and apply Bayes' rule (naive Bayes, LDA).

## 1.3 Loss, risk and the best you can do {#ml-1-3}

<div class="nb nb-definition">

<strong>Definition</strong> — A **loss** $\ell(\hat y, y)$ scores one prediction (squared $(\hat y - y)^2$, absolute $|\hat y - y|$, 0-1, log-loss). The **risk** is its expectation over the whole population; the **empirical risk** is its average over your sample. **Empirical risk minimisation** picks the model with the lowest empirical risk in a chosen family.

</div>

Even a perfect learner cannot beat the noise in $y$ given $x$. The best possible classifier for the data distribution is the **Bayes classifier**, and its error is the **Bayes error** (the irreducible error).

<div class="nb nb-remark">

<strong>Trap</strong> — "Bayes error is the error of naive Bayes." No: it is a property of the distribution, the floor for every classifier. Naive Bayes is one particular, usually sub-optimal, classifier.

</div>

**No free lunch:** averaged over all possible problems, every learner is equally good. Learning works only because real problems have structure (smoothness, linearity, sparsity, locality); the assumptions a model makes are its **inductive bias**. "Which algorithm is best?" has no answer without the data.

## 1.4 Train, validation, test {#ml-1-4}

- **Training set:** fits the parameters.
- **Validation set** (or cross-validation): chooses among models and **hyperparameters**, settings not learnt by fitting (degree, $k$, $\lambda$, tree depth).
- **Test set:** touched **once**, at the end, for an honest score.

Typical splits: 70/15/15, 60/20/20 or 80/10/10; with millions of rows a 1% test set is already tens of thousands of examples. With little data, use k-fold cross-validation (chapter 11).

<div class="nb nb-example">

<strong>Example</strong> (Why you need a third set)

Take 50 "models" that are pure coin flips and score each on a balanced validation set of 100 points. Every one has true accuracy 0.5, yet the best validation score averages about **0.61**. On fresh data the winner scores 0.50. Picking the best of many by a score inflates that score.

</div>

<div class="nb nb-remark">

<strong>Trap</strong> — Tuning on the test set ("I tried a few depths and kept the best test accuracy") turns it into a validation set, and the reported number is optimistic. Interviewers probe this with "how many times did you look at the test set?"

</div>

Before any clever model, score a **baseline**: predict the mean (regression) or the majority class (classification). If 80% of customers stay, "always stay" is already 80% accurate; your model must beat that.

## 1.5 Over- and underfitting {#ml-1-5}

The **generalisation gap** is test (or validation) error minus training error.

| Symptom | Diagnosis | First fixes |
|---|---|---|
| Train good, test much worse (train 99%, test 70%) | **Overfitting**, high variance | more data, regularisation, simpler model, early stopping, bagging, augmentation |
| Bad on both (train 62%, test 60%) | **Underfitting**, high bias | richer model, better features, less regularisation |

<div class="nb nb-example">

<strong>Example</strong> (The degree sweep)

Fit polynomials to 15 noisy points from $\sin 2\pi x$ (noise variance 0.09). Median MSE over 200 runs: degree 1 gives train 0.238 / test 0.323 (underfits); degree 3 gives 0.065 / **0.124** (best); degree 9 gives 0.037 / 0.777 (threads every noisy point). Training error falls with capacity; test error is U-shaped.

</div>

<div class="nb nb-remark">

<strong>Trap</strong> — "A small gap means a good model." A constant predictor has a tiny gap and is useless; you need low training error *and* a small gap. And "training error keeps falling, so we are improving" says nothing about generalisation: watch validation error.

</div>

## 1.6 The i.i.d. assumption and leakage {#ml-1-6}

All of the above assumes training and future points are **independent and identically distributed**. Each half fails in its own way:

- **Not independent:** several rows per patient, user or session; consecutive time steps. A random row split puts the same patient in train and test and the model scores by recognising the patient. Split **by group** or **by time**.
- **Not identically distributed** (distribution shift): **covariate shift** ($p(x)$ changes: a new city), **label shift** ($p(y)$ changes: fraud doubles in a festival sale), **concept drift** ($p(y \mid x)$ changes: what counts as spam evolves).

**Data leakage** is information that will not exist at prediction time sneaking into training. Classic cases: scaling or imputing on all data before splitting; a feature like "account closed date" to predict churn; shuffling a time series. Chapter 11 has the full catalogue.

## 1.7 The workflow {#ml-1-7}

Define the problem and metric → collect → clean → split → baseline → train → evaluate → tune → deploy → monitor, usually several times round. When asked "walk me through your project", tell it in this order: the problem and metric, cleaning, the features you built and why, the baseline, the stronger models compared with cross-validation, the result, and what you would improve.

<div class="nb nb-moral">

The regime comes from the supervision you have; training error measures fit, the gap measures luck you mistook for signal, and the test set is looked at once.

</div>
