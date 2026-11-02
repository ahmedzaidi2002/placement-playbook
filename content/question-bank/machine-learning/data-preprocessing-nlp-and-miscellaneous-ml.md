---
title: "Data preprocessing, NLP and miscellaneous ML"
weight: 4
---

6 questions asked by EXL, Info Edge, Qualcomm. Try each one first, then open the toggle: it gives the answer, why it is right, and the idea behind it explained from scratch.

### 1 · handling missing values in Power BI

*Asked by: EXL (HackerEarth test, 2025)*

Suzy, working on a data-analysis project in Power BI, found missing values in some records.
Which techniques could she use?

1. Filter out rows with missing values, using the "Filter Rows" transformation in
    the Power Query Editor.
2. Replace missing data with an average or median value.
3. Look at other records in the dataset that are similar to the record with missing
    data, and use them to impute a value.
4. In some cases, create a new category for missing data, such as "Unknown" or
    "Not Applicable".

- **(a)** 1 and 2
- **(b)** 2 and 4
- **(c)** 3 and 4
- **(d)** 1, 2, 3 and 4

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) all four**

**Why.** Dropping rows, mean/median imputation, similarity-based imputation (e.g. nearest neighbours) and an explicit "Unknown" category are all standard. Each suits a different situation: dropping when few rows are affected, mean/median for numeric columns, neighbour-based when related records exist, and "Unknown" when missingness itself carries information.

**Concept: missing data.** Ask why values are missing. If at random, simple imputation is fine; if missingness depends on the value (e.g. high earners skip the income field), it biases results, and flagging it explicitly helps.

{{< /details >}}

### 2 · Q13, categorical variable

*Asked by: Info Edge (Data Science II)*

Identify the categorical variable among the options.

- **(a)** Price of a set of commodities
- **(b)** Mother tongue of a student
- **(c)** Rainfall per year
- **(d)** IQ of an individual

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) mother tongue of a student**

**Why.** Mother tongue takes values from a set of labels (Hindi, Tamil, ...), with no numeric meaning. Price, rainfall and IQ are numbers.

**Concept: variable types.** Categorical: nominal (no order: language, colour) or ordinal (ordered: low/medium/high). Numerical: discrete (counts) or continuous (measurements). The type decides the encoding and the plots you use.

{{< /details >}}

### 3 · Q15, bootstrap coverage

*Asked by: Info Edge (Data Science II)*

In bootstrapping, approximately how much of the original data is sampled?

- **(a)** 54%
- **(b)** 63%
- **(c)** 37%
- **(d)** 50%

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) 63%**

**Why.** A bootstrap sample draws n points with replacement. A given point is missed in one draw with probability 1 − 1/n, and in all n draws with (1 − 1/n)ⁿ ≈ 1/e ≈ 0.37. So about 63.2% of the distinct points appear.

**Concept: bootstrapping.** Resample the data with replacement to estimate the variability of a statistic, or (in bagging/random forests) to train many slightly different models. The ~37% left out of each sample are the "out-of-bag" points, a free validation set.

{{< /details >}}

### 4 · Q17, target encoding

*Asked by: Info Edge (Data Science II)*

In which respect is target encoding primarily advantageous compared to one-hot encoding?

- **(a)** Large number of categories can be efficiently handled with fixed dimension
- **(b)** Ensures better performance of regression problems
- **(c)** Ensures better performance for classification problems
- **(d)** None of the above

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) it handles many categories with a fixed dimension**

**Why.** Target encoding replaces each category with one number (e.g. the mean target for that category), so a column with 10,000 categories stays one column. One-hot would need 10,000 columns. It does not guarantee better performance and can leak the target (overfit) unless done with cross-validation. (The photo ticks (b).)

**Concept: categorical encodings.** One-hot: one 0/1 column per category (fine for few categories). Ordinal: integers for ordered categories. Target/mean encoding: compact for high cardinality, but needs regularisation.

{{< /details >}}

### 5 · Q45, inverse document frequency

*Asked by: Qualcomm (IISc)*

Inverse document frequency (IDF) of a term is:

- **(a)** log(total number of documents / number of documents containing the term)
- **(b)** How many documents the term occurred in
- **(c)** How many documents the term did not occur in
- **(d)** Total number of documents / number of documents containing the term

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) log(total documents / documents containing the term)**

**Why.** IDF is large for rare terms and near 0 for terms in almost every document (like "the"). The log damps the effect.

**Concept: TF-IDF.** A word's weight in a document = term frequency (how often it appears there) × IDF (how rare it is across documents). Words that are frequent in this document but rare overall get the highest weight.

{{< /details >}}

### 6 · neuron output

*Asked by: Qualcomm (IISc)*

A neuron has 3 inputs with values 4, 5 and 6 and weights 1, 2 and 3; its transfer function is
linear with proportionality constant 2. Determine the output.

- **(a)** 60
- **(b)** 232
- **(c)** 34
- **(d)** 64

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) 64**

**Why.** Weighted sum = 4×1 + 5×2 + 6×3 = 4 + 10 + 18 = 32. A linear transfer function with constant 2 gives 2 × 32 = 64.

**Concept: artificial neuron.** Output = f(Σ wᵢxᵢ + b). With a linear f(z) = kz the neuron is just a scaled weighted sum; non-linear f (sigmoid, ReLU) is what lets networks learn complex functions.

{{< /details >}}
