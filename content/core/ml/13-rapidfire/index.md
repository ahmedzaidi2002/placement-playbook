---
title: "13 · Rapid-fire: 80 questions with spoken answers"
linkTitle: "13 Rapid-fire"
weight: 13
math: true
---
Questions in the form they are asked across the table, with answers you can say in under twenty seconds. Cover the answer, say yours out loud, then compare. If an answer surprises you, read the chapter, not the answer. Questions tagged with a company were reported by candidates in real interviews (from the Cantilever toolkits).

## 13.1 Setup and data {#ml-13-1}

1. **Supervised vs unsupervised?** *(Amazon)* Supervised learns from labelled examples to predict an answer (price, spam or not); unsupervised has no labels and finds structure (customer clusters).
2. **AI vs ML vs deep learning?** AI is the goal of intelligent machines; ML is the subset that learns from data; deep learning is the subset of ML using many-layered neural networks.
3. **Regression or classification?** Look at the answer: a number on a scale is regression, a category is classification.
4. **Why three splits instead of two?** Choosing models on the validation set biases its score upwards; the test set must play no part in any choice.
5. **What is data leakage? Example.** Information unavailable at prediction time sneaking into training: scaling before splitting, or "account closed date" to predict churn.
6. **What is Bayes error?** The error of the best possible classifier for the distribution: the irreducible floor, not the error of naive Bayes.
7. **What is a baseline and why?** A trivial model (predict the mean or majority class) your model must beat; with 80% "stay", "always stay" is already 80% accurate.
8. **How do you handle missing values and outliers?** *(Infosys)* Find them with plots, IQR or z-scores. Missing: drop if very few, else impute (median, mode, model) and add a was-missing flag. Outliers: fix errors, cap or log-transform, or use robust models.
9. **How do you clean a messy dataset?** *(Infosys)* Check shape, types and duplicates; fix types and inconsistent labels ("Pune" vs "pune"); handle missing values and outliers; validate with summary statistics and plots.
10. **One-hot or ordinal?** One-hot for unordered categories; ordinal codes only when a real order exists (S/M/L), or for trees.
11. **Target encoding risk?** Leakage: encode out-of-fold and smooth, or validation scores lie.
12. **Which models need scaling?** k-NN, SVM, k-means, PCA, regularised and gradient-trained linear models, neural nets. Not trees.
13. **When should SMOTE be applied?** Only inside training folds; never before splitting or to validation/test data.
14. **What does IDF do?** Down-weights terms that appear in many documents: $\log(N/\text{df})$.

## 13.2 Linear models and regularisation {#ml-13-2}

15. **Explain linear regression.** *(Infosys)* The target as a weighted sum of features, weights chosen to minimise squared error; assumptions: linearity, independent errors, constant variance; evaluate with RMSE or $R^2$.
16. **Least squares from MLE?** Gaussian noise makes the negative log-likelihood proportional to the sum of squared residuals.
17. **Why not invert $X^\top X$?** It squares the condition number; solve with QR or SVD.
18. **When is $X^\top X$ singular?** Perfect collinearity, or more features than rows; ridge fixes it.
19. **What does multicollinearity damage?** The variance and interpretability of individual coefficients, not predictions in the data range. Diagnose with VIF.
20. **Can $R^2$ be negative?** On test data, yes: worse than predicting the training mean. On training data with an intercept, no.
21. **Why adjusted $R^2$?** Plain $R^2$ never falls when you add a feature, even noise; adjusted $R^2$ penalises the count.
22. **$r = -0.8$; what fraction of variance does a line explain?** $0.64$; the sign disappears.
23. **Gradient descent, and a too-high learning rate?** Step the weights against the slope of the loss; too high overshoots and diverges, too low crawls.
24. **Bias–variance trade-off?** *(Tiger Analytics)* Bias is error from a too-simple model (underfits), variance from a too-sensitive one (overfits); complexity lowers bias and raises variance; pick the point of lowest validation error.
25. **More data reduces bias or variance?** Variance. It cannot fix a model class that cannot represent the truth.
26. **Effect of $\lambda$ in $E + \lambda\sum w^2$?** Larger $\lambda$: smaller weights, higher bias, lower variance, training error up. $\lambda \to 0$: raw fit; $\lambda \to \infty$: a constant.
27. **What is regularisation for?** *(Infosys)* Reducing overfitting by penalising large weights; L1 can zero weights (selects features), L2 shrinks all smoothly; tune strength by CV.
28. **Why does lasso give zeros and ridge not?** The L1 subgradient at 0 is an interval, so small coefficients are thresholded; L2's derivative vanishes at 0 and only shrinks.
29. **When elastic net?** Correlated groups of features: lasso picks one arbitrarily; elastic net shares the weight and stays sparse.
30. **What is double descent?** Test error peaks where the model can just interpolate ($p \approx n$) and falls again as parameters grow.

## 13.3 Classifiers {#ml-13-3}

31. **Linear vs logistic regression?** Linear predicts a number by minimising squared error; logistic predicts a class probability via a sigmoid of a linear score, fitted by maximising likelihood (log-loss).
32. **Is logistic regression a linear classifier?** Yes: its boundary $w^\top x + b = 0$ is a hyperplane.
33. **Gradient of log-loss?** $X^\top(p - y)/n$: prediction minus target, times input.
34. **Why not MSE for logistic regression?** Non-convex in the weights and its gradient vanishes when confidently wrong; log-loss is the Bernoulli likelihood and convex.
35. **What does a logistic coefficient of 0.7 mean?** One unit more multiplies the odds by $e^{0.7} \approx 2$.
36. **Perfectly separable data?** The unregularised MLE does not exist; weights grow forever. Regularise.
37. **Why a softmax layer?** *(Infosys)* Turns raw class scores into positive probabilities that sum to 1; the multiclass version of the sigmoid.
38. **OvR vs OvO for 10 classes?** 10 versus 45 binary classifiers; softmax regression needs neither.
39. **Can a perceptron learn XOR?** No; XOR is not linearly separable. Add $x_1x_2$ as a feature or a hidden layer.
40. **Naive Bayes' assumption?** Features are conditionally independent given the class.
41. **Why Laplace smoothing?** An unseen word would zero the whole product; pseudo-counts are a MAP estimate under a Dirichlet prior.
42. **Naive Bayes' probabilities are bad but accuracy fine, why?** Correlated features are double-counted, pushing probabilities to extremes, but the argmax is often still right.
43. **LDA vs QDA?** Shared covariance gives a linear boundary; class-specific covariances give a quadratic one with many more parameters.
44. **$k = 1$ in k-NN?** Zero training error, highest variance. Large $k$: smoother, more bias. Use an odd $k$ for two classes.
45. **Curse of dimensionality?** In high dimensions distances concentrate and neighbourhoods stop being local, so distance-based methods need exponentially more data.

## 13.4 SVMs, trees and ensembles {#ml-13-4}

46. **What are support vectors?** Points with non-zero dual weight: on the margin, inside it, or misclassified. Only they define the boundary.
47. **What does $C$ do?** Penalty on margin violations: large $C$ narrow margin, low bias; small $C$ wide margin, more regularisation.
48. **What does $\gamma$ do in an RBF kernel?** Inverse length scale: large $\gamma$ makes the boundary wiggle around individual points.
49. **The kernel trick?** The dual needs only inner products; a kernel computes $\phi(x)^\top\phi(z)$ without forming $\phi$.
50. **Valid kernel?** Every Gram matrix it produces is symmetric positive semi-definite.
51. **Is the hinge loss convex?** Yes, though not differentiable at margin 1.
52. **How does a tree choose a split?** The candidate split with the biggest drop in Gini or entropy (information gain) for classification, or in variance for regression.
53. **Entropy and Gini of a 50/50 node?** 1 bit; 0.5.
54. **Why gain ratio?** Information gain favours many-valued features (an ID column gives perfect gain).
55. **Do trees need scaling?** No; splits are invariant to monotone transforms.
56. **Can a regression tree extrapolate?** No; leaves predict averages of training targets.
57. **Probability a row is in a bootstrap sample?** $1 - (1 - 1/n)^n \to 1 - 1/e \approx 63.2\%$.
58. **Bagging vs boosting?** *(Amazon)* Bagging trains in parallel on bootstrap samples and averages (random forest), lowering variance; boosting trains in sequence, each fixing the last (AdaBoost, XGBoost), lowering bias.
59. **Why does a random forest beat one tree?** One deep tree overfits; many trees on bootstrapped rows and random feature subsets, averaged, cancel much of the variance while keeping low bias.
60. **Can more trees overfit a random forest?** No; error stabilises. More boosting rounds can overfit.
61. **OOB error?** Each row scored only by the trees that did not see it; a free validation estimate.
62. **What is wrong with impurity (MDI) importance?** Biased towards high-cardinality and noisy continuous features; splits credit among correlated ones. Use permutation importance on held-out data.
63. **Gradient boosting in one sentence?** Fit each new tree to the negative gradient of the loss at the current predictions and add a shrunken copy.
64. **XGBoost's $\lambda$ and $\gamma$?** $\lambda$ shrinks leaf values ($w^\star = -G/(H + \lambda)$); $\gamma$ is the minimum gain a split must earn.
65. **Learning rate vs number of trees?** A smaller rate needs more trees and generalises better; use early stopping.

## 13.5 Unsupervised and evaluation {#ml-13-5}

66. **When does k-means stop?** When assignments stop changing (or centroids barely move, or iterations run out). Always stops, at a local minimum.
67. **Why k-means++?** Spreads the initial centroids, avoiding bad local minima.
68. **DBSCAN over k-means when?** Arbitrary shapes, unknown $k$, outliers to flag.
69. **EM in one line?** E-step: responsibilities; M-step: weighted MLE; the likelihood never decreases.
70. **Why standardise before PCA?** PCA maximises variance, so the feature with the largest units dominates otherwise.
71. **Can you read cluster distances off a t-SNE plot?** No; it preserves local neighbourhoods, not global geometry.
72. **Which metrics for a classifier?** *(Tiger Analytics)* Start from the confusion matrix: accuracy if balanced; precision, recall, F1 if imbalanced or errors cost differently; ROC-AUC or PR-AUC across thresholds.
73. **Precision vs recall, with examples?** Precision when false alarms are costly (spam filter hiding real mail); recall when misses are costly (cancer screening, fraud).
74. **ROC curve, and AUC = 0.5?** TPR against FPR over all thresholds; 0.5 is random ranking. With heavy imbalance also check the PR curve.
75. **Your model has 95% accuracy. Good?** Depends on the baseline: if 95% of cases are one class it may have learnt nothing. Check the confusion matrix and per-class recall.
76. **How do you handle an imbalanced dataset?** *(Google)* Right metric first (precision, recall, F1, PR-AUC); then class weights, oversampling (SMOTE) or undersampling, threshold tuning, stratified splits.
77. **How do you detect and fix overfitting?** A big train–validation gap or widening learning curve; fix with more data, regularisation, a simpler model, feature selection, early stopping or ensembling.
78. **Cross-validating a time series?** Forward-chaining splits; never shuffle.
79. **What is a p-value?** The probability, if the null is true, of data at least as extreme as observed. Not the probability the null is true.
80. **Twenty tests at 5%?** About a 64% chance of at least one false positive; use Bonferroni or Benjamini–Hochberg.

<div class="nb nb-moral">

If you can say all eighty in under twenty seconds each, you are ready for the conceptual part of any placement ML round.

</div>
