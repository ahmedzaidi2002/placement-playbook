---
title: "Machine Learning"
weight: 7
sidebar:
  open: false
---

Classical machine learning the way placement rounds ask it: one-line concept MCQs, one-minute numericals done by hand, "which statements are true" multi-selects, and interview follow-ups that go three "why?"s deep. Each topic gives the idea, the one or two formulas worth remembering, a small worked example where an OA would set one, and the trap a question-setter plants.

There is no code in this book and only the maths you need to answer. The derivations, proofs and from-scratch implementations are in the source PDFs listed at the bottom.

<div class="nb nb-moral">

Where the marks are: a 49-question sample of real non-coding ML/DL papers (Info Edge, Fujitsu, Qualcomm, EXL) had 22 deep-learning questions, 9 on supervised models, 7 on optimisation, losses and regularisation, 6 on preprocessing and NLP, 3 on unsupervised learning, and 1 each on evaluation and statistics. Interviews add evaluation, statistics and "walk me through your project".

</div>

## Contents

**Part: Foundations**

- [1 · The setup: what ML is and how it fails](01-foundations/)
- [2 · Data preparation and feature engineering](02-data-prep/)

**Part: Supervised learning**

- [3 · Linear regression](03-linear-regression/)
- [4 · Bias, variance and regularisation](04-bias-variance/)
- [5 · Logistic regression and the perceptron](05-logistic/)
- [6 · Naive Bayes, LDA and k-nearest neighbours](06-bayes-knn/)
- [7 · Support vector machines](07-svm/)
- [8 · Decision trees](08-trees/)
- [9 · Ensembles: bagging, random forests, boosting](09-ensembles/)

**Part: Without labels, and doing it properly**

- [10 · Unsupervised and semi-supervised learning](10-unsupervised/)
- [11 · Evaluation and model selection](11-evaluation/)
- [12 · Statistics and maths interviewers ask](12-stats-maths/)

**Part: Revision**

- [13 · Rapid-fire: 80 questions with spoken answers](13-rapidfire/)
- [14 · OA practice problems](14-problems/)

## How to use it

1. **Two weeks before an OA:** read chapters 1, 3, 4, 5, 8, 9, 10 and 11, then do chapter 14.
2. **The night before an interview:** chapter 13 out loud, then the green "moral" box at the end of each chapter.
3. **For your own projects:** the deep-learning side (VGG11, Transformer) is in the companion [Deep Learning](../dl/) book.

## Sources

Condensed from five documents in `placement prep/core notes/`:

- *Classical Machine Learning* (the Napkin-style book, 170 pages, 142 problems): the structure, the worked numbers and the traps.
- *Deep Learning* (its companion): only where the two overlap (perceptron, losses).
- Cantilever *ML Series* Parts 1 to 3 (Basics, Core Algorithms, Evaluation): the "which step / which algorithm / which metric when" tables, company-tagged interview questions and the MCQ style.

Every worked number on these pages is either taken from those sources, where it was computed by code, or recomputed by hand here.
