---
title: "Optimisation, loss functions and regularisation"
weight: 3
---

7 questions asked by Fujitsu, Info Edge, Qualcomm. Try each one first, then open the toggle: it gives the answer, why it is right, and the idea behind it explained from scratch.

### 1 · Q2, generalisation gap

*Asked by: Fujitsu (IISc 2023)*

Let $L_{val}$ and $L_{train}$ denote the loss on validation data and training data. The
generalisation gap is $L_{gap} = L_{val} - L_{train}$. If $L_{gap} \gg 0$, what does it
denote?

- **(a)** Overfitting
- **(b)** Underfitting
- **(c)** Training error
- **(d)** Does not indicate anything

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) overfitting**

**Why.** A validation loss much larger than the training loss means the model does well on data it has seen and poorly on new data: it has memorised the training set. Underfitting shows a high **training** loss with a small gap.

**Concept: diagnosing with learning curves.** High train loss: underfitting (bigger model, more features). Low train, high validation: overfitting (more data, regularisation, dropout, early stopping).

{{< /details >}}

### 2 · ML Q1, Adam

*Asked by: Fujitsu (IIT Kharagpur 2023)*

What is the purpose of the Adam optimizer in deep learning?

- **(a)** To calculate gradients efficiently
- **(b)** To regularize the model
- **(c)** To optimize the learning rate
- **(d)** To perform gradient based parameter updates

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) to perform gradient-based parameter updates**

**Why.** Adam takes gradients (computed by backpropagation) and updates parameters, using running averages of the gradient (momentum) and of its square to give each parameter its own adaptive step size. It doesn't compute gradients or regularise (weight decay is separate; AdamW decouples it). (The screenshot ticks (b).)

**Concept: optimisers.** SGD: w ← w − η∇L. Momentum: follow a running average of gradients. RMSProp/Adam: divide by the root of the average squared gradient, so rarely-updated parameters get bigger steps.

{{< /details >}}

### 3 · ML Q7, overfitting

*Asked by: Fujitsu (IIT Kharagpur 2023)*

What is the primary challenge of overfitting in machine learning?

- **(a)** High Bias
- **(b)** High Variance
- **(c)** Low training accuracy
- **(d)** Low test accuracy

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) high variance**

**Why.** An overfitted model changes a lot with the particular training sample: high variance. Low test accuracy (d) is its symptom, not the underlying problem. High bias (ticked) is underfitting.

**Concept: bias–variance trade-off.** Error = bias² + variance + noise. Simple models: high bias, low variance. Complex models: low bias, high variance. Regularisation and more data reduce variance.

{{< /details >}}

### 4 · Q20, classification loss

*Asked by: Info Edge (Data Science II)*

Which loss function is suitable for classification problems?

- **(a)** Log loss
- **(b)** Cross Entropy loss
- **(c)** Mean Squared Error
- **(d)** Both A and B

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) both log loss and cross-entropy**

**Why.** Log loss is binary cross-entropy; categorical cross-entropy extends it to many classes. MSE is for regression.

**Concept: why cross-entropy for classification.** It heavily penalises confident wrong predictions and gives well-behaved gradients with softmax/sigmoid outputs, unlike MSE.

{{< /details >}}

### 5 · Q43, convex functions

*Asked by: Qualcomm (IISc)*

Which functions are convex? (I) $\sin x$, (II) $|x|$ [cut off in the source] (from the options),
(III) $\min(f_1(x), f_2(x))$ and (IV) $\max(f_1(x), f_2(x))$ with $f_1, f_2$ convex.

- **(a)** Both (I) and (II)
- **(b)** Both (II) and (IV)
- **(c)** Both (II) and (III)
- **(d)** Both (I) and (IV)

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) (II) and (IV)**

**Why.** |x| = max(x, −x) is convex. The pointwise maximum of convex functions is convex (IV). The minimum is not (min(x², (x − 2)²) has two valleys) (III). sin x curves both ways (concave on (0, π)) (I). (The photo ticks (c).)

**Concept: convexity.** A function is convex if the line segment between any two points on its graph lies above the graph (bowl-shaped). Convex losses have no bad local minima, so gradient descent finds the global minimum.

{{< /details >}}

### 6 · Q42, non-convex loss

*Asked by: Qualcomm (IISc)*

Which of these is not a convex loss function?

- **(a)** Misclassification loss
- **(b)** Logistic loss
- **(c)** Exponential loss $e^{-yf(x)}$
- **(d)** Hinge loss

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) misclassification (0–1) loss**

**Why.** 0–1 loss is a step function (0 if right, 1 if wrong): not convex and with zero gradient almost everywhere. Logistic, exponential and hinge losses are convex surrogates for it.

**Concept: surrogate losses.** We can't optimise 0–1 loss directly, so we minimise a smooth convex upper bound: logistic regression (log loss), SVM (hinge), AdaBoost (exponential).

{{< /details >}}

### 7 · Q47, augmented error

*Asked by: Qualcomm (IISc)*

While minimising the augmented error $E' = E + \lambda \sum_i w_i^2$, what is the possible
outcome for different values of $\lambda$?

- **(a)** If $\lambda$ is large, current instances of training data are used
- **(b)** If $\lambda$ is small, prior is more accounted than data
- **(c)** None of the given options
- **(d)** As $\lambda$ tends to 0, the model becomes a long-term memory model

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) none of the given options**

**Why.** A large λ lets the penalty (the prior belief that weights are small) dominate; a small λ lets the data dominate. (a) and (b) state both relations backwards; (d) is meaningless. (The photo ticks (b).)

**Concept: L2 regularisation (ridge / weight decay).** Adding λΣw² pulls weights towards 0, giving a smoother model. Bayesian view: it is a Gaussian prior on the weights. Choose λ by validation.

{{< /details >}}
