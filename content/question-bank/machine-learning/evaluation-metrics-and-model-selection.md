---
title: "Evaluation metrics and model selection"
weight: 6
---

1 question asked by Fujitsu. Try each one first, then open the toggle: it gives the answer, why it is right, and the idea behind it explained from scratch.

### 1 · ML Q6, BIC

*Asked by: Fujitsu (IIT Kharagpur 2023)*

What is the purpose of the Bayesian Information Criterion (BIC) in model selection?

- **(a)** Maximizing Likelihood
- **(b)** Minimizing model complexity
- **(c)** Minimizing Model bias
- **(d)** Minimizing Overfitting

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) minimising overfitting** (the closest option; BIC balances fit against complexity)

**Why.** BIC = k ln n − 2 ln L̂. The likelihood term rewards fit; the k ln n term penalises the number of parameters. Picking the model with the lowest BIC trades fit against complexity, which guards against overfitting. It certainly does not minimise bias (the ticked option); the penalty accepts a little more bias to reduce variance.

**Concept: information criteria.** AIC = 2k − 2 ln L̂ and BIC = k ln n − 2 ln L̂. Lower is better. BIC's penalty grows with sample size, so it prefers simpler models than AIC.

{{< /details >}}
