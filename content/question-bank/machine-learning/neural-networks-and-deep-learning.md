---
title: "Neural networks and deep learning"
weight: 1
---

22 questions asked by Fujitsu, Info Edge, Qualcomm. Try each one first, then open the toggle: it gives the answer, why it is right, and the idea behind it explained from scratch.

### 1 · Q3, convolution output shape

*Asked by: Fujitsu (IISc 2023)*

What is the shape of the output activation map when an input image of shape
$32 \times 32 \times 3$ is convolved with 6 filters of shape $5 \times 5$?

- **(a)** $32\times32\times8$
- **(b)** $28\times28\times6$
- **(c)** $28\times26\times9$
- **(d)** $26\times32\times8$

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) 28 × 28 × 6**

**Why.** With stride 1 and no padding, each spatial size is (32 − 5)/1 + 1 = 28. Each filter (implicitly 5 × 5 × 3, spanning all input channels) produces one output channel, so 6 filters give 6 channels.

**Concept: conv output size.** Output = ⌊(N − F + 2P)/S⌋ + 1, for input size N, filter F, padding P, stride S. The output depth equals the number of filters.

{{< /details >}}

### 2 · Q4, softmax confidence

*Asked by: Fujitsu (IISc 2023)*

Image classification with 5 classes $\{0, 1, 2, 3, 4\}$: the output logits of the
model for one image are $[3.2, 5.1, 0.8, 2.2, 3.9]$. What is the confidence of the model
in its prediction (softmax output)?

- **(a)** 65.82%
- **(b)** 66.51%
- **(c)** 69.00%
- **(d)** 71.33%

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) 65.82%**

**Why.** The predicted class is 1 (largest logit, 5.1). Subtract the max for easy maths: e⁰ / (e⁻¹·⁹ + e⁰ + e⁻⁴·³ + e⁻²·⁹ + e⁻¹·²) = 1 / (0.150 + 1 + 0.014 + 0.055 + 0.301) = 1/1.519 ≈ 0.658.

**Concept: softmax.** pᵢ = e^(zᵢ) / Σⱼ e^(zⱼ) turns any scores into probabilities that add to 1. Subtracting the maximum logit first gives the same result and avoids overflow.

{{< /details >}}

### 3 · Q6, cross-entropy loss

*Asked by: Fujitsu (IISc 2023)*

Same model and logits $[3.2, 5.1, 0.8, 2.2, 3.9]$ as the previous question. Compute the
cross-entropy loss, given that the ground truth is class 4. (Multiple answers may be
selected.)

- **(a)** 0.7128
- **(b)** 0.6890
- **(c)** 0.7028
- **(d)** 0.6699

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) 0.7028** (only with log base 10; with the natural log it is 1.618)

**Why.** Cross-entropy for the true class 4 = −log p₄, with p₄ = e³·⁹/Σ = 0.1982. −ln(0.1982) = 1.618 (not an option); −log₁₀(0.1982) = 0.7029 ≈ 0.7028. So the paper used log base 10.

**Concept: cross-entropy loss.** For one example it is −log(probability assigned to the correct class): 0 if the model is certain and right, large if it gives the right class a small probability. ML libraries always use the natural log.

{{< /details >}}

### 4 · ML Q10, sequence to sequence

*Asked by: Fujitsu (IIT Kharagpur 2023)*

Which deep learning architecture is suitable for sequence-to-sequence tasks like machine
translation?

- **(a)** Convolution Neural Network (CNN)
- **(b)** Recurrent Neural Network (RNN)
- **(c)** Gated Recurrent Unit (GRU)
- **(d)** Transformer

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) Transformer**

**Why.** Encoder–decoder RNNs (including GRU/LSTM) were the original sequence-to-sequence models, so (b) and (c) are not wrong historically, but the Transformer (introduced in "Attention Is All You Need" for machine translation) is today's standard answer.

**Concept: why Transformers won.** Self-attention lets every word look at every other word directly (no step-by-step recurrence), so long-range dependencies are easier and training parallelises across the sequence.

{{< /details >}}

### 5 · ML Q2, reducing spatial size

*Asked by: Fujitsu (IIT Kharagpur 2023)*

Which layer is used in neural networks for reducing the spatial dimensions of the input
data?

- **(a)** Dense Layer
- **(b)** Convolution layer
- **(c)** Pooling layer
- **(d)** Batch Normalization layer

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) pooling layer**

**Why.** Pooling (e.g. 2 × 2 max-pooling with stride 2) halves height and width by keeping one value per window. Strided convolutions can also downsample, but reducing spatial size is the purpose of pooling. (The screenshot ticks (b).)

**Concept: pooling.** Max pooling keeps the strongest activation in each window, making features slightly position-invariant and cutting computation for later layers. It has no learnable weights.

{{< /details >}}

### 6 · ML Q3, activation function

*Asked by: Fujitsu (IIT Kharagpur 2023)*

What is the purpose of the activation function in a neural network?

- **(a)** To reduce overfitting
- **(b)** To compute the gradient during backpropagation
- **(c)** To introduce non-linearity into the model
- **(d)** To initialize network weights

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) to introduce non-linearity**

**Why.** A stack of linear layers is still one linear function (W₂(W₁x) = (W₂W₁)x). Activations like ReLU between layers let the network represent non-linear functions. (The screenshot ticks (d).)

**Concept: universal approximation.** With non-linear activations, even one hidden layer can approximate any continuous function given enough units; without them depth adds nothing.

{{< /details >}}

### 7 · ML Q4, fine-tuning

*Asked by: Fujitsu (IIT Kharagpur 2023)*

What is fine-tuning in the context of large language models?

- **(a)** Adjusting the model's physical hardware for better performance
- **(b)** The process of training the model on specific tasks or datasets
- **(c)** Modifying the model's core architecture
- **(d)** Converting the model's output into different languages

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) training the model further on specific tasks or datasets**

**Why.** Fine-tuning continues training a pre-trained model (all weights, or a small set as in LoRA) on task-specific data, so it adapts its general knowledge to the task.

**Concept: pre-training vs fine-tuning.** Pre-training on huge general data learns broad patterns; fine-tuning on smaller labelled data specialises the model. Much cheaper than training from scratch.

{{< /details >}}

### 8 · ML Q5, image classification

*Asked by: Fujitsu (IIT Kharagpur 2023)*

In deep learning, which type of neural network architecture is typically used for image
classification tasks?

- **(a)** Recurrent Neural Network (RNN)
- **(b)** Convolutional Neural Network (CNN)
- **(c)** Long Short-Term Memory (LSTM)
- **(d)** Feedforward Neural Network (FNN)

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) CNN**

**Why.** Convolutional networks use small shared filters that detect local patterns (edges, textures, parts) anywhere in the image, building up to whole objects in deeper layers.

**Concept: inductive bias.** CNNs build in the assumptions that nearby pixels are related and that a pattern means the same thing wherever it appears (translation equivariance), which makes them data-efficient for images.

{{< /details >}}

### 9 · ML Q9, vanishing gradients

*Asked by: Fujitsu (IIT Kharagpur 2023)*

What is the vanishing gradient problem in deep learning?

- **(a)** The loss function becomes unstable.
- **(b)** The weights of the neural network become too large.
- **(c)** Gradients become too small during backpropagation, hindering learning in deep networks.
- **(d)** The network converges too quickly

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) gradients become too small during backpropagation, hindering learning in deep networks**

**Why.** Backpropagation multiplies many per-layer derivatives. With sigmoid/tanh these are often below 1 (sigmoid's is at most 0.25), so the product shrinks exponentially with depth and early layers barely learn. (The screenshot ticks (d).)

**Concept: fixes for vanishing gradients.** ReLU-family activations (derivative 1 for positive inputs), residual connections, careful initialisation (Xavier/He), normalisation layers, and gated RNNs (LSTM/GRU).

{{< /details >}}

### 10 · Q21, time series

*Asked by: Info Edge (Data Science II)*

Which architecture may be more suitable for learning time-series data than the others?

- **(a)** LSTM
- **(b)** CNN
- **(c)** ANN
- **(d)** All three architectures are equally suitable

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) LSTM**

**Why.** An LSTM is a recurrent network that carries a memory (cell state) across time steps, with gates deciding what to keep or forget, so it can learn long-range patterns in sequences.

**Concept: sequence models.** RNN: hidden state passed step to step (struggles with long memory). LSTM/GRU: gated memory. Transformers and temporal CNNs are newer alternatives.

{{< /details >}}

### 11 · Q22, parameters FC vs CNN

*Asked by: Info Edge (Data Science II)*

Which of the following is TRUE?

- **(a)** A fully connected neural network and a CNN having the same number of layers have the same number of parameters.
- **(b)** A fully connected neural network has fewer parameters than a CNN having the same number of layers.
- **(c)** A fully connected neural network has more parameters than a CNN having the same number of layers.
- **(d)** The number of parameters in a CNN cannot be determined.

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) a fully connected network has more parameters than a CNN with the same number of layers**

**Why.** A dense layer connects every input to every output (e.g. 1000 × 1000 = 1M weights). A conv layer reuses one small kernel at every position (e.g. 3 × 3 × channels), so it needs far fewer weights.

**Concept: parameter sharing.** Reusing weights across positions reduces parameters, memory and overfitting.

{{< /details >}}

### 12 · Q23, limitations of deep learning

*Asked by: Info Edge (Data Science II)*

What is/are the key limitation(s) of deep learning?

- **(a)** Large training datasets required
- **(b)** High computation resources required
- **(c)** Weak explainability
- **(d)** All the above

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) all of the above**

**Why.** Deep learning typically needs large labelled datasets, a lot of compute (GPUs) and is hard to explain (millions of weights, no simple rules).

**Concept: when to prefer simpler models.** For small tabular datasets or when explanations are required (credit, medicine), gradient-boosted trees or linear models are often better choices.

{{< /details >}}

### 13 · Q24, model capacity

*Asked by: Info Edge (Data Science II)*

Which is TRUE about model capacity (the ability of a neural network to approximate complex
functions)?

- **(a)** As the number of hidden layers increases the model capacity also increases
- **(b)** As dropout ratio increases model capacity increases
- **(c)** As learning rate increases model capacity increases
- **(d)** None of the above

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) more hidden layers increase model capacity**

**Why.** More layers (or units) let the network represent more complex functions. Dropout **reduces** effective capacity (it's a regulariser); the learning rate affects training, not capacity.

**Concept: capacity.** How complex a function a model can fit. Too little → underfitting; too much (without regularisation) → overfitting.

{{< /details >}}

### 14 · Q25, non-linearity

*Asked by: Info Edge (Data Science II)*

Which of the following gives non-linearity to a neural network?

- **(a)** Stochastic Gradient Descent
- **(b)** Rectified Linear Unit
- **(c)** Convolution Function
- **(d)** None of the above

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) ReLU**

**Why.** ReLU(x) = max(0, x) is a non-linear activation. SGD is an optimiser; convolution is a linear operation.

**Concept: activation functions.** Sigmoid (0–1, saturates), tanh (−1–1, saturates), ReLU (cheap, no saturation for positive inputs, but can "die" at 0), Leaky ReLU/GELU (variants).

{{< /details >}}

### 15 · Q26, probabilistic outputs

*Asked by: Info Edge (Data Science II)*

Which layer of a CNN converts numerical values to probabilistic values?

- **(a)** Max Pooling
- **(b)** SoftMax
- **(c)** Convolution
- **(d)** DropOut

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) softmax**

**Why.** Softmax turns the final layer's scores into probabilities that are positive and add to 1.

**Concept: output layers.** Multi-class: softmax + cross-entropy. Binary or multi-label: sigmoid per output + binary cross-entropy. Regression: linear output + MSE.

{{< /details >}}

### 16 · Q27, feedback connections

*Asked by: Info Edge (Data Science II)*

Which of the following networks have feedback connections?

- **(a)** Convolutional Neural Network
- **(b)** Recurrent Neural Network
- **(c)** Multi-Layer Perceptron
- **(d)** None of the Above

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) recurrent neural network**

**Why.** In an RNN the hidden state at time t feeds back as input at time t + 1: a feedback loop. CNNs and MLPs are feed-forward.

**Concept: unrolling.** An RNN over a sequence of length T can be drawn as T copies of the same layer connected in a chain, sharing weights; training uses backpropagation through time.

{{< /details >}}

### 17 · Q28, weight sharing

*Asked by: Info Edge (Data Science II)*

In which neural network architecture does weight sharing occur?

- **(a)** Convolutional Neural Network
- **(b)** Artificial Neural Network
- **(c)** Deep Belief Network
- **(d)** Both A and B

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) CNN**

**Why.** One kernel's weights are applied at every position of the image. (RNNs also share weights across time steps, but they are not an option.)

**Concept: weight sharing** reduces parameters and makes the network detect the same feature anywhere.

{{< /details >}}

### 18 · Q29, loss function

*Asked by: Info Edge (Data Science II)*

Which of the following is a loss function?

- **(a)** Sigmoid function
- **(b)** Cross entropy
- **(c)** ReLU
- **(d)** All of the above

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) cross entropy**

**Why.** Cross-entropy measures how wrong predicted probabilities are and is minimised during training. Sigmoid and ReLU are activation functions.

**Concept: loss functions.** Classification: cross-entropy, hinge. Regression: MSE (squared error), MAE (absolute error), Huber (a mix).

{{< /details >}}

### 19 · Q30, ResNet

*Asked by: Info Edge (Data Science II)*

Which problem can be mitigated in a neural network by using ResNet?

- **(a)** Overfitting problem
- **(b)** Vanishing gradient problem
- **(c)** Bias
- **(d)** None of the Above

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) vanishing gradients**

**Why.** ResNet's skip connections add a layer's input to its output (y = F(x) + x). The gradient can flow straight back through the identity path, so very deep networks (100+ layers) still train.

**Concept: residual learning.** Each block only has to learn a correction F(x) to the identity, which is easier than learning a full transformation, and it never makes things worse than skipping the block.

{{< /details >}}

### 20 · Q41, computer vision statements

*Asked by: Qualcomm (IISc)*

A computer-vision system analyses traffic images and identifies vehicles violating rules using
a deep-learning algorithm and a neural network. Which are valid? (i) The deep-learning algorithm
enables the computer to learn by itself about the visual data. (ii) The neural network helps the
algorithm by breaking the images into pixels and giving them appropriate tags.

- **(a)** Only i
- **(b)** Only ii
- **(c)** Neither i nor ii
- **(d)** Both i and ii

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) both** (both statements paraphrase a standard "what is computer vision" explainer; the photo ticks (a))

**Why.** (i) Deep learning lets the computer learn visual patterns from data by itself. (ii) A CNN processes an image as pixels and learns to tag (classify) what they show.

**Concept: computer vision pipeline.** Pixels → convolutional feature extraction → classification or detection (bounding boxes) → decisions (e.g. flagging a rule violation).

{{< /details >}}

### 21 · Q57, neurotransmitters

*Asked by: Qualcomm (IISc)*

The substances that convey the impulse between neurons (via a synapse) are known as:

- **(a)** neurotransmitters
- **(b)** ions
- **(c)** enzymes
- **(d)** electrons

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) neurotransmitters**

**Why.** At a synapse, the sending neuron releases chemical messengers (neurotransmitters) that cross the gap and stimulate the receiving neuron.

**Concept: biological inspiration.** In artificial networks, the "synapse strength" becomes a numeric weight, and the neuron's firing becomes an activation function.

{{< /details >}}

### 22 · Q49, XOR and the perceptron

*Asked by: Qualcomm (IISc)*

Can a two-class data set following the XOR pattern be classified with a perceptron?

- **(a)** No
- **(b)** Yes
- **(c)** Can be done with bias adjustment
- **(d)** Depends on the transfer function applied on the perceptron

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) No**

**Why.** XOR's positive points (0,1) and (1,0) and negative points (0,0) and (1,1) sit on opposite corners of a square; no single straight line separates them. A perceptron's decision boundary is a straight line, so it cannot.

**Concept: linear separability.** A single-layer perceptron only solves linearly separable problems. Adding a hidden layer (a multi-layer perceptron) solves XOR, which is why hidden layers matter.

{{< /details >}}
