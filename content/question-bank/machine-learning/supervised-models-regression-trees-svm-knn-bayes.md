---
title: "Supervised models (regression, trees, SVM, kNN, Bayes)"
weight: 2
---

9 questions asked by Fujitsu, Info Edge, Qualcomm. Try each one first, then open the toggle: it gives the answer, why it is right, and the idea behind it explained from scratch.

### 1 · ML Q8, bagging vs boosting

*Asked by: Fujitsu (IIT Kharagpur 2023)*

What is the difference between bagging and boosting ensemble techniques in machine
learning?

- **(a)** Bagging combines multiple weak learners sequentially, while boosting combines them in parallel.
- **(b)** Bagging aims to reduce variance, while boosting aims to reduce bias.
- **(c)** Bagging uses a weighted average of model predictions, while boosting uses a majority vote.
- **(d)** Bagging builds multiple models independently and averages their predictions, while boosting builds models sequentially, giving more weight to misclassified examples.

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d)** (bagging builds models independently and averages; boosting builds them sequentially, focusing on mistakes)

**Why.** (d) describes the mechanism that defines the two methods. (b) is also true (bagging reduces variance, boosting mainly reduces bias) but describes the effect; (d) is the usual key for this wording. (a) and (c) are reversed.

**Concept: ensembles.** Bagging (random forest): many models on bootstrap samples, averaged; works best with high-variance models like deep trees. Boosting (AdaBoost, XGBoost): each new model corrects the previous ones' errors; turns weak learners into a strong one.

{{< /details >}}

### 2 · Q12, fitting a line

*Asked by: Info Edge (Data Science II)*

Which methods do we use to find the best-fit line in linear regression?

- **(a)** Least Square Error
- **(b)** Maximum Likelihood
- **(c)** Logarithmic Loss
- **(d)** Both A and B

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) both least squares and maximum likelihood**

**Why.** Least squares minimises the sum of squared errors. If the errors are Gaussian, maximising the likelihood gives exactly the same line.

**Concept: least squares = Gaussian MLE.** The Gaussian log-likelihood is −Σ(yᵢ − ŷᵢ)²/(2σ²) + constant, so maximising it means minimising squared error.

{{< /details >}}

### 3 · Q14, mean decrease in impurity

*Asked by: Info Edge (Data Science II)*

On the mean-decrease-in-impurity method of feature selection in random forests:
(i) impurity-based ranking is not biased towards variables with more categories;
(ii) when two or more features are correlated, from the model's perspective any of them can be
used as the predictor; (iii) the impurity decrease of each feature can be averaged and the
features ranked by this measure. Which are correct?

- **(a)** All i), ii), iii)
- **(b)** i), ii)
- **(c)** ii), iii)
- **(d)** i), iii)

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) ii) and iii)**

**Why.** (i) is false: impurity-based importance **is** biased towards features with many categories or continuous values, because they offer more split points. (ii) With correlated features, any of them can serve the model, so importance is shared or arbitrary. (iii) is how the method works: average each feature's impurity decrease over all trees and rank.

**Concept: feature importance.** Impurity-based importance is fast but biased; permutation importance (shuffle a feature and measure the drop in score) is a more reliable check.

{{< /details >}}

### 4 · Q16, ensembles

*Asked by: Info Edge (Data Science II)*

Which of the following is TRUE?

- **(a)** Random Forest aims at reducing bias of the constituent decision trees
- **(b)** XGBoost aims at reducing variance of the individual trees
- **(c)** Random Forest is a type of boosting algorithm
- **(d)** None of the Above

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) none of the above**

**Why.** Random forest is bagging (not boosting) and mainly reduces variance; XGBoost is boosting and mainly reduces bias. Each option swaps these.

**Concept: which error each ensemble attacks.** Averaging independent models (bagging) cancels their random fluctuations (variance). Sequentially fitting residuals (boosting) reduces systematic error (bias).

{{< /details >}}

### 5 · Q9, error of prediction

*Asked by: Info Edge (Data Science II)*

Sam scored 84 in test $T_1$ and 132 in $T_2$. Using the regression equation
$T_2 = 1.5\,T_1 + 5$, what is the error of prediction for Sam?

- **(a)** 0
- **(b)** -1
- **(c)** 1
- **(d)** None of these

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) 1**

**Why.** Predicted T₂ = 1.5 × 84 + 5 = 131. Error (residual) = actual − predicted = 132 − 131 = 1.

**Concept: residuals.** Residual = observed − predicted. Least squares chooses the line that minimises the sum of squared residuals.

{{< /details >}}

### 6 · Q56, uses of decision trees

*Asked by: Qualcomm (IISc)*

A decision tree can be used for: (I) classification, (II) association, (III) regression,
(IV) clustering.

- **(a)** Only I and III
- **(b)** Only IV
- **(c)** Only II and IV
- **(d)** All I, II, III and IV

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) only I and III**

**Why.** Decision trees are used for classification (categorical target) and regression (numeric target): "CART" = Classification And Regression Trees. Association rules and clustering are different (unsupervised) techniques.

**Concept: decision trees.** Split the data on the feature/threshold that best separates the target (by Gini, entropy or variance), recursively. Leaves give a class or an average value.

{{< /details >}}

### 7 · Q59, straight-line fit

*Asked by: Qualcomm (IISc)*

A straight line $Y = mX + c$ is fitted by least squares to $X = 1..5$, $Y = 14, 27, 40, 55, 68$.
Which is the best fit?

- **(a)** slope = 13.6, intercept = 0
- **(b)** slope = 0, intercept = -13.6
- **(c)** slope = 0, intercept = 13.6
- **(d)** slope = 13.6, intercept = 2

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) slope 13.6, intercept 0**

**Why.** x̄ = 3, ȳ = 204/5 = 40.8. Slope m = Σ(x − x̄)(y − ȳ)/Σ(x − x̄)². Deviations of x: −2, −1, 0, 1, 2 (Σ squares = 10); Σ(x − x̄)(y − ȳ) = 136. So m = 13.6 and c = ȳ − m x̄ = 40.8 − 40.8 = 0.

**Concept: least-squares line.** m = cov(x, y)/var(x), and the line always passes through (x̄, ȳ).

{{< /details >}}

### 8 · Q58, tree classifiers

*Asked by: Qualcomm (IISc)*

Which rule is used to perform classification in tree-based classification algorithms?

- **(a)** do while
- **(b)** switch
- **(c)** if-then
- **(d)** while

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) if-then**

**Why.** Each root-to-leaf path of a decision tree is a rule: "if feature A > 5 and B = yes, then class X".

**Concept: interpretability of trees.** Because they reduce to readable if-then rules, small decision trees are among the most explainable models.

{{< /details >}}

### 9 · Q48, naive Bayes limitations

*Asked by: Qualcomm (IISc)*

Identify the limitations of the naive Bayes classifier: (I) hard to implement, (II) dependencies
exist among variables, (III) loss of accuracy, (IV) class-conditional independence.

- **(a)** Only II, III and IV
- **(b)** Only I, II, III and IV
- **(c)** Only I and II
- **(d)** Only II and III

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) only II, III and IV**

**Why.** Naive Bayes is easy to implement (I is not a limitation). It assumes features are independent given the class (IV), but real features often depend on each other (II), which can cost accuracy (III).

**Concept: naive Bayes.** P(class | features) ∝ P(class) × Π P(featureᵢ | class). The "naive" independence assumption makes it fast and data-efficient (great for text spam filters), even when the assumption is false.

{{< /details >}}
