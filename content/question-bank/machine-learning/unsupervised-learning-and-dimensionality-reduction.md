---
title: "Unsupervised learning and dimensionality reduction"
weight: 5
---

3 questions asked by Info Edge. Try each one first, then open the toggle: it gives the answer, why it is right, and the idea behind it explained from scratch.

### 1 · Q11, unsupervised technique

*Asked by: Info Edge (Data Science II)*

Which of the following is an example of an unsupervised learning technique?

- **(a)** Linear Regression
- **(b)** SVM
- **(c)** AdaBoost
- **(d)** Clustering

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) clustering**

**Why.** Clustering groups data without labels. Linear regression, SVM and AdaBoost all learn from labelled examples (supervised).

**Concept: supervised vs unsupervised.** Supervised: learn a mapping from inputs to known outputs. Unsupervised: find structure (clusters, components) in inputs alone.

{{< /details >}}

### 2 · Q18, k-means stopping

*Asked by: Info Edge (Data Science II)*

Which conditions can be used as a stopping condition in k-means clustering?

- **(a)** Points stop moving from one cluster to another
- **(b)** RSS (within-cluster sum of squares) falls below a threshold for all clusters
- **(c)** Centroids of new clusters do not change
- **(d)** All of the above

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) all of the above**

**Why.** k-means alternates "assign points to the nearest centroid" and "move centroids to the mean of their points". It can stop when no point changes cluster, when centroids stop moving (these two are equivalent), or when the within-cluster sum of squares is below a threshold. (The photo ticks (c).)

**Concept: k-means.** Minimises the within-cluster sum of squared distances. It always converges, but possibly to a local minimum, so run it with several random starts (k-means++ initialisation helps).

{{< /details >}}

### 3 · Q19, standardising before PCA

*Asked by: Info Edge (Data Science II)*

Following the steps of a PCA algorithm, why is it important to standardise your data?

- **(a)** Standardized data is easier to understand
- **(b)** Training is faster with standardized data
- **(c)** It helps in identifying features which can best predict the response variable Y
- **(d)** None of the Above

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) none of the above**

**Why.** PCA finds the directions of maximum variance. Without standardisation, features with large units (salary in rupees) dominate the components just because of their scale. None of the options says this; PCA is unsupervised and ignores Y, so (c) (ticked) is wrong.

**Concept: PCA.** Finds orthogonal directions (principal components) that capture the most variance, used to reduce dimensions. Standardise first (zero mean, unit variance) unless all features share the same units.

{{< /details >}}
