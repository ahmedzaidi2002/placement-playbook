@@ exl-missing-values
**Answer: (d) all four**

**Why.** Dropping rows, mean/median imputation, similarity-based imputation (e.g. nearest neighbours) and an explicit "Unknown" category are all standard. Each suits a different situation: dropping when few rows are affected, mean/median for numeric columns, neighbour-based when related records exist, and "Unknown" when missingness itself carries information.

**Concept: missing data.** Ask why values are missing. If at random, simple imputation is fine; if missingness depends on the value (e.g. high earners skip the income field), it biases results, and flagging it explicitly helps.

@@ ie-q13
**Answer: (b) mother tongue of a student**

**Why.** Mother tongue takes values from a set of labels (Hindi, Tamil, ...), with no numeric meaning. Price, rainfall and IQ are numbers.

**Concept: variable types.** Categorical: nominal (no order: language, colour) or ordinal (ordered: low/medium/high). Numerical: discrete (counts) or continuous (measurements). The type decides the encoding and the plots you use.

@@ ie-q15
**Answer: (b) 63%**

**Why.** A bootstrap sample draws n points with replacement. A given point is missed in one draw with probability 1 − 1/n, and in all n draws with (1 − 1/n)ⁿ ≈ 1/e ≈ 0.37. So about 63.2% of the distinct points appear.

**Concept: bootstrapping.** Resample the data with replacement to estimate the variability of a statistic, or (in bagging/random forests) to train many slightly different models. The ~37% left out of each sample are the "out-of-bag" points, a free validation set.

@@ ie-q17
**Answer: (a) it handles many categories with a fixed dimension**

**Why.** Target encoding replaces each category with one number (e.g. the mean target for that category), so a column with 10,000 categories stays one column. One-hot would need 10,000 columns. It does not guarantee better performance and can leak the target (overfit) unless done with cross-validation. (The photo ticks (b).)

**Concept: categorical encodings.** One-hot: one 0/1 column per category (fine for few categories). Ordinal: integers for ordered categories. Target/mean encoding: compact for high cardinality, but needs regularisation.

@@ qc-iisc-idf
**Answer: (a) log(total documents / documents containing the term)**

**Why.** IDF is large for rare terms and near 0 for terms in almost every document (like "the"). The log damps the effect.

**Concept: TF-IDF.** A word's weight in a document = term frequency (how often it appears there) × IDF (how rare it is across documents). Words that are frequent in this document but rare overall get the highest weight.

@@ qc-iisc-neuron
**Answer: (d) 64**

**Why.** Weighted sum = 4×1 + 5×2 + 6×3 = 4 + 10 + 18 = 32. A linear transfer function with constant 2 gives 2 × 32 = 64.

**Concept: artificial neuron.** Output = f(Σ wᵢxᵢ + b). With a linear f(z) = kz the neuron is just a scaled weighted sum; non-linear f (sigmoid, ReLU) is what lets networks learn complex functions.

@@ fj-kgp-ml6
**Answer: (d) minimising overfitting** (the closest option; BIC balances fit against complexity)

**Why.** BIC = k ln n − 2 ln L̂. The likelihood term rewards fit; the k ln n term penalises the number of parameters. Picking the model with the lowest BIC trades fit against complexity, which guards against overfitting. It certainly does not minimise bias (the ticked option); the penalty accepts a little more bias to reduce variance.

**Concept: information criteria.** AIC = 2k − 2 ln L̂ and BIC = k ln n − 2 ln L̂. Lower is better. BIC's penalty grows with sample size, so it prefers simpler models than AIC.

@@ fj-iisc-3
**Answer: (b) 28 × 28 × 6**

**Why.** With stride 1 and no padding, each spatial size is (32 − 5)/1 + 1 = 28. Each filter (implicitly 5 × 5 × 3, spanning all input channels) produces one output channel, so 6 filters give 6 channels.

**Concept: conv output size.** Output = ⌊(N − F + 2P)/S⌋ + 1, for input size N, filter F, padding P, stride S. The output depth equals the number of filters.

@@ fj-iisc-4
**Answer: (a) 65.82%**

**Why.** The predicted class is 1 (largest logit, 5.1). Subtract the max for easy maths: e⁰ / (e⁻¹·⁹ + e⁰ + e⁻⁴·³ + e⁻²·⁹ + e⁻¹·²) = 1 / (0.150 + 1 + 0.014 + 0.055 + 0.301) = 1/1.519 ≈ 0.658.

**Concept: softmax.** pᵢ = e^(zᵢ) / Σⱼ e^(zⱼ) turns any scores into probabilities that add to 1. Subtracting the maximum logit first gives the same result and avoids overflow.

@@ fj-iisc-6
**Answer: (c) 0.7028** (only with log base 10; with the natural log it is 1.618)

**Why.** Cross-entropy for the true class 4 = −log p₄, with p₄ = e³·⁹/Σ = 0.1982. −ln(0.1982) = 1.618 (not an option); −log₁₀(0.1982) = 0.7029 ≈ 0.7028. So the paper used log base 10.

**Concept: cross-entropy loss.** For one example it is −log(probability assigned to the correct class): 0 if the model is certain and right, large if it gives the right class a small probability. ML libraries always use the natural log.

@@ fj-kgp-ml10
**Answer: (d) Transformer**

**Why.** Encoder–decoder RNNs (including GRU/LSTM) were the original sequence-to-sequence models, so (b) and (c) are not wrong historically, but the Transformer (introduced in "Attention Is All You Need" for machine translation) is today's standard answer.

**Concept: why Transformers won.** Self-attention lets every word look at every other word directly (no step-by-step recurrence), so long-range dependencies are easier and training parallelises across the sequence.

@@ fj-kgp-ml2
**Answer: (c) pooling layer**

**Why.** Pooling (e.g. 2 × 2 max-pooling with stride 2) halves height and width by keeping one value per window. Strided convolutions can also downsample, but reducing spatial size is the purpose of pooling. (The screenshot ticks (b).)

**Concept: pooling.** Max pooling keeps the strongest activation in each window, making features slightly position-invariant and cutting computation for later layers. It has no learnable weights.

@@ fj-kgp-ml3
**Answer: (c) to introduce non-linearity**

**Why.** A stack of linear layers is still one linear function (W₂(W₁x) = (W₂W₁)x). Activations like ReLU between layers let the network represent non-linear functions. (The screenshot ticks (d).)

**Concept: universal approximation.** With non-linear activations, even one hidden layer can approximate any continuous function given enough units; without them depth adds nothing.

@@ fj-kgp-ml4
**Answer: (b) training the model further on specific tasks or datasets**

**Why.** Fine-tuning continues training a pre-trained model (all weights, or a small set as in LoRA) on task-specific data, so it adapts its general knowledge to the task.

**Concept: pre-training vs fine-tuning.** Pre-training on huge general data learns broad patterns; fine-tuning on smaller labelled data specialises the model. Much cheaper than training from scratch.

@@ fj-kgp-ml5
**Answer: (b) CNN**

**Why.** Convolutional networks use small shared filters that detect local patterns (edges, textures, parts) anywhere in the image, building up to whole objects in deeper layers.

**Concept: inductive bias.** CNNs build in the assumptions that nearby pixels are related and that a pattern means the same thing wherever it appears (translation equivariance), which makes them data-efficient for images.

@@ fj-kgp-ml9
**Answer: (c) gradients become too small during backpropagation, hindering learning in deep networks**

**Why.** Backpropagation multiplies many per-layer derivatives. With sigmoid/tanh these are often below 1 (sigmoid's is at most 0.25), so the product shrinks exponentially with depth and early layers barely learn. (The screenshot ticks (d).)

**Concept: fixes for vanishing gradients.** ReLU-family activations (derivative 1 for positive inputs), residual connections, careful initialisation (Xavier/He), normalisation layers, and gated RNNs (LSTM/GRU).

@@ ie-q21
**Answer: (a) LSTM**

**Why.** An LSTM is a recurrent network that carries a memory (cell state) across time steps, with gates deciding what to keep or forget, so it can learn long-range patterns in sequences.

**Concept: sequence models.** RNN: hidden state passed step to step (struggles with long memory). LSTM/GRU: gated memory. Transformers and temporal CNNs are newer alternatives.

@@ ie-q22
**Answer: (c) a fully connected network has more parameters than a CNN with the same number of layers**

**Why.** A dense layer connects every input to every output (e.g. 1000 × 1000 = 1M weights). A conv layer reuses one small kernel at every position (e.g. 3 × 3 × channels), so it needs far fewer weights.

**Concept: parameter sharing.** Reusing weights across positions reduces parameters, memory and overfitting.

@@ ie-q23
**Answer: (d) all of the above**

**Why.** Deep learning typically needs large labelled datasets, a lot of compute (GPUs) and is hard to explain (millions of weights, no simple rules).

**Concept: when to prefer simpler models.** For small tabular datasets or when explanations are required (credit, medicine), gradient-boosted trees or linear models are often better choices.

@@ ie-q24
**Answer: (a) more hidden layers increase model capacity**

**Why.** More layers (or units) let the network represent more complex functions. Dropout **reduces** effective capacity (it's a regulariser); the learning rate affects training, not capacity.

**Concept: capacity.** How complex a function a model can fit. Too little → underfitting; too much (without regularisation) → overfitting.

@@ ie-q25
**Answer: (b) ReLU**

**Why.** ReLU(x) = max(0, x) is a non-linear activation. SGD is an optimiser; convolution is a linear operation.

**Concept: activation functions.** Sigmoid (0–1, saturates), tanh (−1–1, saturates), ReLU (cheap, no saturation for positive inputs, but can "die" at 0), Leaky ReLU/GELU (variants).

@@ ie-q26
**Answer: (b) softmax**

**Why.** Softmax turns the final layer's scores into probabilities that are positive and add to 1.

**Concept: output layers.** Multi-class: softmax + cross-entropy. Binary or multi-label: sigmoid per output + binary cross-entropy. Regression: linear output + MSE.

@@ ie-q27
**Answer: (b) recurrent neural network**

**Why.** In an RNN the hidden state at time t feeds back as input at time t + 1: a feedback loop. CNNs and MLPs are feed-forward.

**Concept: unrolling.** An RNN over a sequence of length T can be drawn as T copies of the same layer connected in a chain, sharing weights; training uses backpropagation through time.

@@ ie-q28
**Answer: (a) CNN**

**Why.** One kernel's weights are applied at every position of the image. (RNNs also share weights across time steps, but they are not an option.)

**Concept: weight sharing** reduces parameters and makes the network detect the same feature anywhere.

@@ ie-q29
**Answer: (b) cross entropy**

**Why.** Cross-entropy measures how wrong predicted probabilities are and is minimised during training. Sigmoid and ReLU are activation functions.

**Concept: loss functions.** Classification: cross-entropy, hinge. Regression: MSE (squared error), MAE (absolute error), Huber (a mix).

@@ ie-q30
**Answer: (b) vanishing gradients**

**Why.** ResNet's skip connections add a layer's input to its output (y = F(x) + x). The gradient can flow straight back through the identity path, so very deep networks (100+ layers) still train.

**Concept: residual learning.** Each block only has to learn a correction F(x) to the identity, which is easier than learning a full transformation, and it never makes things worse than skipping the block.

@@ qc-iisc-cv
**Answer: (d) both** (both statements paraphrase a standard "what is computer vision" explainer; the photo ticks (a))

**Why.** (i) Deep learning lets the computer learn visual patterns from data by itself. (ii) A CNN processes an image as pixels and learns to tag (classify) what they show.

**Concept: computer vision pipeline.** Pixels → convolutional feature extraction → classification or detection (bounding boxes) → decisions (e.g. flagging a rule violation).

@@ qc-iisc-synapse
**Answer: (a) neurotransmitters**

**Why.** At a synapse, the sending neuron releases chemical messengers (neurotransmitters) that cross the gap and stimulate the receiving neuron.

**Concept: biological inspiration.** In artificial networks, the "synapse strength" becomes a numeric weight, and the neuron's firing becomes an activation function.

@@ qc-iisc-xor
**Answer: (a) No**

**Why.** XOR's positive points (0,1) and (1,0) and negative points (0,0) and (1,1) sit on opposite corners of a square; no single straight line separates them. A perceptron's decision boundary is a straight line, so it cannot.

**Concept: linear separability.** A single-layer perceptron only solves linearly separable problems. Adding a hidden layer (a multi-layer perceptron) solves XOR, which is why hidden layers matter.

@@ fj-iisc-2
**Answer: (a) overfitting**

**Why.** A validation loss much larger than the training loss means the model does well on data it has seen and poorly on new data: it has memorised the training set. Underfitting shows a high **training** loss with a small gap.

**Concept: diagnosing with learning curves.** High train loss: underfitting (bigger model, more features). Low train, high validation: overfitting (more data, regularisation, dropout, early stopping).

@@ fj-kgp-ml1
**Answer: (d) to perform gradient-based parameter updates**

**Why.** Adam takes gradients (computed by backpropagation) and updates parameters, using running averages of the gradient (momentum) and of its square to give each parameter its own adaptive step size. It doesn't compute gradients or regularise (weight decay is separate; AdamW decouples it). (The screenshot ticks (b).)

**Concept: optimisers.** SGD: w ← w − η∇L. Momentum: follow a running average of gradients. RMSProp/Adam: divide by the root of the average squared gradient, so rarely-updated parameters get bigger steps.

@@ fj-kgp-ml7
**Answer: (b) high variance**

**Why.** An overfitted model changes a lot with the particular training sample: high variance. Low test accuracy (d) is its symptom, not the underlying problem. High bias (ticked) is underfitting.

**Concept: bias–variance trade-off.** Error = bias² + variance + noise. Simple models: high bias, low variance. Complex models: low bias, high variance. Regularisation and more data reduce variance.

@@ ie-q20
**Answer: (d) both log loss and cross-entropy**

**Why.** Log loss is binary cross-entropy; categorical cross-entropy extends it to many classes. MSE is for regression.

**Concept: why cross-entropy for classification.** It heavily penalises confident wrong predictions and gives well-behaved gradients with softmax/sigmoid outputs, unlike MSE.

@@ qc-iisc-convex
**Answer: (b) (II) and (IV)**

**Why.** |x| = max(x, −x) is convex. The pointwise maximum of convex functions is convex (IV). The minimum is not (min(x², (x − 2)²) has two valleys) (III). sin x curves both ways (concave on (0, π)) (I). (The photo ticks (c).)

**Concept: convexity.** A function is convex if the line segment between any two points on its graph lies above the graph (bowl-shaped). Convex losses have no bad local minima, so gradient descent finds the global minimum.

@@ qc-iisc-loss
**Answer: (a) misclassification (0–1) loss**

**Why.** 0–1 loss is a step function (0 if right, 1 if wrong): not convex and with zero gradient almost everywhere. Logistic, exponential and hinge losses are convex surrogates for it.

**Concept: surrogate losses.** We can't optimise 0–1 loss directly, so we minimise a smooth convex upper bound: logistic regression (log loss), SVM (hinge), AdaBoost (exponential).

@@ qc-iisc-reg
**Answer: (c) none of the given options**

**Why.** A large λ lets the penalty (the prior belief that weights are small) dominate; a small λ lets the data dominate. (a) and (b) state both relations backwards; (d) is meaningless. (The photo ticks (b).)

**Concept: L2 regularisation (ridge / weight decay).** Adding λΣw² pulls weights towards 0, giving a smoother model. Bayesian view: it is a Gaussian prior on the weights. Choose λ by validation.

@@ qc-iisc-corr
**Answer: (b) 25%**

**Why.** The fraction of variance in y explained by a linear fit on x is r² = (−0.5)² = 0.25. It is never negative; the sign of r only tells the direction of the relationship.

**Concept: correlation and R².** r ranges from −1 to 1 (strength and direction of a linear relationship). R² = r² for simple linear regression: the share of variance explained.

@@ fj-kgp-ml8
**Answer: (d)** (bagging builds models independently and averages; boosting builds them sequentially, focusing on mistakes)

**Why.** (d) describes the mechanism that defines the two methods. (b) is also true (bagging reduces variance, boosting mainly reduces bias) but describes the effect; (d) is the usual key for this wording. (a) and (c) are reversed.

**Concept: ensembles.** Bagging (random forest): many models on bootstrap samples, averaged; works best with high-variance models like deep trees. Boosting (AdaBoost, XGBoost): each new model corrects the previous ones' errors; turns weak learners into a strong one.

@@ ie-q12
**Answer: (d) both least squares and maximum likelihood**

**Why.** Least squares minimises the sum of squared errors. If the errors are Gaussian, maximising the likelihood gives exactly the same line.

**Concept: least squares = Gaussian MLE.** The Gaussian log-likelihood is −Σ(yᵢ − ŷᵢ)²/(2σ²) + constant, so maximising it means minimising squared error.

@@ ie-q14
**Answer: (c) ii) and iii)**

**Why.** (i) is false: impurity-based importance **is** biased towards features with many categories or continuous values, because they offer more split points. (ii) With correlated features, any of them can serve the model, so importance is shared or arbitrary. (iii) is how the method works: average each feature's impurity decrease over all trees and rank.

**Concept: feature importance.** Impurity-based importance is fast but biased; permutation importance (shuffle a feature and measure the drop in score) is a more reliable check.

@@ ie-q16
**Answer: (d) none of the above**

**Why.** Random forest is bagging (not boosting) and mainly reduces variance; XGBoost is boosting and mainly reduces bias. Each option swaps these.

**Concept: which error each ensemble attacks.** Averaging independent models (bagging) cancels their random fluctuations (variance). Sequentially fitting residuals (boosting) reduces systematic error (bias).

@@ ie-q9
**Answer: (c) 1**

**Why.** Predicted T₂ = 1.5 × 84 + 5 = 131. Error (residual) = actual − predicted = 132 − 131 = 1.

**Concept: residuals.** Residual = observed − predicted. Least squares chooses the line that minimises the sum of squared residuals.

@@ qc-iisc-dt
**Answer: (a) only I and III**

**Why.** Decision trees are used for classification (categorical target) and regression (numeric target): "CART" = Classification And Regression Trees. Association rules and clustering are different (unsupervised) techniques.

**Concept: decision trees.** Split the data on the feature/threshold that best separates the target (by Gini, entropy or variance), recursively. Leaves give a class or an average value.

@@ qc-iisc-fit
**Answer: (a) slope 13.6, intercept 0**

**Why.** x̄ = 3, ȳ = 204/5 = 40.8. Slope m = Σ(x − x̄)(y − ȳ)/Σ(x − x̄)². Deviations of x: −2, −1, 0, 1, 2 (Σ squares = 10); Σ(x − x̄)(y − ȳ) = 136. So m = 13.6 and c = ȳ − m x̄ = 40.8 − 40.8 = 0.

**Concept: least-squares line.** m = cov(x, y)/var(x), and the line always passes through (x̄, ȳ).

@@ qc-iisc-ifthen
**Answer: (c) if-then**

**Why.** Each root-to-leaf path of a decision tree is a rule: "if feature A > 5 and B = yes, then class X".

**Concept: interpretability of trees.** Because they reduce to readable if-then rules, small decision trees are among the most explainable models.

@@ qc-iisc-nb
**Answer: (a) only II, III and IV**

**Why.** Naive Bayes is easy to implement (I is not a limitation). It assumes features are independent given the class (IV), but real features often depend on each other (II), which can cost accuracy (III).

**Concept: naive Bayes.** P(class | features) ∝ P(class) × Π P(featureᵢ | class). The "naive" independence assumption makes it fast and data-efficient (great for text spam filters), even when the assumption is false.

@@ ie-q11
**Answer: (d) clustering**

**Why.** Clustering groups data without labels. Linear regression, SVM and AdaBoost all learn from labelled examples (supervised).

**Concept: supervised vs unsupervised.** Supervised: learn a mapping from inputs to known outputs. Unsupervised: find structure (clusters, components) in inputs alone.

@@ ie-q18
**Answer: (d) all of the above**

**Why.** k-means alternates "assign points to the nearest centroid" and "move centroids to the mean of their points". It can stop when no point changes cluster, when centroids stop moving (these two are equivalent), or when the within-cluster sum of squares is below a threshold. (The photo ticks (c).)

**Concept: k-means.** Minimises the within-cluster sum of squared distances. It always converges, but possibly to a local minimum, so run it with several random starts (k-means++ initialisation helps).

@@ ie-q19
**Answer: (d) none of the above**

**Why.** PCA finds the directions of maximum variance. Without standardisation, features with large units (salary in rupees) dominate the components just because of their scale. None of the options says this; PCA is unsupervised and ignores Y, so (c) (ticked) is wrong.

**Concept: PCA.** Finds orthogonal directions (principal components) that capture the most variance, used to reduce dimensions. Standardise first (zero mean, unit variance) unless all features share the same units.
