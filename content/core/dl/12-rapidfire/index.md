---
title: "12 · Rapid-fire: 80 questions with spoken answers"
linkTitle: "12 Rapid-fire"
weight: 12
math: true
---
Spoken-length answers, one to three lines: the length an interviewer wants before the follow-up. Read the question, answer aloud, then compare. The last block is about your own two projects.

## 12.1 Foundations, activations and losses {#dl-12-1}

1. **What does a single neuron compute?** An affine function $w^\top x + b$ passed through a fixed non-linearity. With a sigmoid it is logistic regression.
2. **Why can't a perceptron learn XOR?** Its boundary is a hyperplane and XOR's classes are not linearly separable; one hidden layer (OR and not AND) solves it.
3. **Why non-linear activations?** Without them any stack of layers collapses to one affine map.
4. **Is ReLU linear?** Piecewise linear, not linear: $\text{ReLU}(a) + \text{ReLU}(b) \ne \text{ReLU}(a + b)$ in general.
5. **What does universal approximation guarantee, and not?** A wide enough one-hidden-layer network can approximate any continuous function on a compact set; it says nothing about how wide, whether training finds it, or generalisation.
6. **Why deep rather than wide?** Depth composes features; some functions need exponentially many units in one layer but few in many layers.
7. **What increases capacity?** More layers or units, richer inputs. Dropout, weight decay and early stopping reduce effective capacity; learning rate and data size do not change it.
8. **ReLU over sigmoid in hidden layers?** No saturation for positive inputs (gradient exactly 1), cheap, sparse; sigmoid's derivative is at most 1/4, so gradients vanish through depth.
9. **Dead ReLU, and how to avoid it?** A unit negative for all inputs outputs and passes back zero forever. Lower learning rate, He init, leaky ReLU or GELU, normalisation.
10. **Why tanh over sigmoid in hidden layers?** Zero-centred outputs and a larger maximum slope (1 vs 1/4).
11. **Why subtract the max in softmax?** Shift invariance makes it exact and prevents overflow.
12. **Gradient of softmax plus cross-entropy?** $p - y$.
13. **Cross-entropy rather than MSE for classification?** It is the likelihood, and its gradient does not vanish when a sigmoid output is confidently wrong; MSE's does.
14. **Loss at initialisation for $K$ classes?** About $\ln K$; anything else suggests a bug.
15. **Sigmoid or softmax for multilabel?** Independent sigmoids with binary cross-entropy; softmax forces labels to compete.
16. **Why pass logits, not probabilities, to the loss?** The fused log-softmax or log-sigmoid is numerically stable; applying softmax first double-squashes.
17. **Label smoothing?** Targets become $(1-\varepsilon)y + \varepsilon/K$, so the model cannot push logits to infinity; curbs over-confidence.

## 12.2 Backprop, optimisation, normalisation {#dl-12-2}

18. **What is backpropagation?** Reverse-mode automatic differentiation: one backward pass applies the chain rule from the loss to every parameter, reusing intermediate results, at a small multiple of the forward cost.
19. **Why does training use more memory than inference?** Activations are stored for the backward pass, plus gradients and optimiser state.
20. **What causes vanishing and exploding gradients?** The backward pass multiplies one Jacobian per layer (or time step); gains below one shrink exponentially, above one grow.
21. **Why initialise weights randomly?** Equal weights give identical units with identical gradients forever.
22. **Why does gradient descent zig-zag?** Ill-conditioning: the step is limited by the steepest direction, so flat directions crawl and steep ones oscillate.
23. **What does momentum do?** Averages gradients over time: consistent directions accelerate (up to $1/(1-\beta)$), oscillating ones cancel.
24. **What is the purpose of Adam?** Per-parameter step sizes scaled by the inverse RMS of recent gradients, combined with momentum: fast, robust progress with little tuning.
25. **Why does Adam need bias correction?** Its averages start at zero and are biased towards it by $1 - \beta^t$; dividing removes the bias, which matters most early.
26. **Adam vs AdamW?** AdamW applies weight decay directly to the weights, so it is not rescaled by the adaptive denominator.
27. **Can Adam generalise worse than SGD?** Sometimes: on many vision tasks tuned SGD with momentum matches or beats it. Not universal.
28. **Why warm up the learning rate?** Early gradients and Adam's second-moment estimates are unreliable; large early steps can diverge, especially in Transformers.
29. **Batch size and learning rate?** Gradient noise scales like $1/B$; the linear-scaling heuristic raises the rate with the batch, up to a critical batch size.
30. **Clip by norm or by value?** By norm: it keeps the direction. It fixes explosions, not vanishing.
31. **Xavier vs He?** Xavier: variance $2/(n_{\text{in}} + n_{\text{out}})$ for tanh-like activations; He: $2/n_{\text{in}}$ for ReLU, which zeroes half its input.
32. **Why does BatchNorm help?** A smoother, better-conditioned loss that tolerates larger learning rates; mild regularisation. "Internal covariate shift" is the original but weaker explanation.
33. **BatchNorm at train vs test?** Training uses batch statistics and updates running averages; inference uses the frozen running averages. Forgetting `eval()` is the classic bug.
34. **BatchNorm vs LayerNorm?** BN normalises each feature across the batch; LN normalises each example across its features, so it works with batch size one and variable-length sequences.
35. **Why do Transformers use LayerNorm?** Sequences vary in length, batches can be small, and LN behaves identically in training and inference.
36. **Why is a bias before BatchNorm redundant?** BN subtracts the batch mean, removing any constant; $\beta$ takes its place.
37. **Dropout at test time?** With inverted dropout, nothing: survivors were already scaled by $1/(1-p)$ in training.
38. **Why does dropout regularise?** Units cannot co-adapt, and training samples an implicit ensemble of thinned sub-networks.
39. **Effect of $\lambda$ in $E + \lambda\sum w^2$?** Larger $\lambda$ shrinks weights: simpler function, higher training error, lower variance; too large underfits.
40. **Over- vs underfitting from curves?** Overfitting: training loss falls while validation rises. Underfitting: both high and close.

## 12.3 CNNs and RNNs {#dl-12-3}

41. **Convolution output size?** $\lfloor (n + 2p - k)/s\rfloor + 1$ (with dilation, replace $k$ by $d(k-1) + 1$).
42. **Parameters of a conv layer?** $(k^2 C_{\text{in}} + 1)C_{\text{out}}$, independent of image size.
43. **Why fewer parameters than a dense layer?** Local connectivity and weight sharing.
44. **Which layers reduce spatial size?** Pooling and strided or unpadded convolutions; not ReLU, BN or a stride-1 $1\times1$ convolution.
45. **What does a $1\times1$ convolution do?** Mixes channels at each pixel; changes the channel count cheaply (bottlenecks).
46. **Two $3\times3$ instead of one $5\times5$?** Same receptive field, $18C^2$ instead of $25C^2$ weights, one more non-linearity.
47. **Depthwise-separable convolution?** A per-channel spatial filter then a $1\times1$ mix; cost ratio $1/C_{\text{out}} + 1/k^2$.
48. **How does ResNet fix degradation?** Blocks learn a residual added to an identity shortcut, so the identity is easy and gradients flow through the shortcut undiminished.
49. **Is degradation overfitting?** No: the deeper plain network has higher *training* error.
50. **Fine-tuning vs feature extraction?** Feature extraction freezes the backbone and trains a head; fine-tuning also updates pretrained weights with a small learning rate.
51. **IoU and NMS?** IoU is overlap over union; NMS keeps the highest-scoring box and removes others overlapping it beyond a threshold.
52. **U-Net in one line?** An encoder–decoder whose skip connections concatenate high-resolution encoder features into the decoder to recover fine detail.
53. **Why feedback connections in RNNs?** They carry a hidden state across time, so outputs depend on earlier inputs, with fixed weights for any length.
54. **What is BPTT?** Backprop through the network unrolled over time, summing the gradients of the shared weights.
55. **Why do vanilla RNNs struggle with long dependencies?** The gradient is a product of many Jacobians with the same matrix and tanh derivatives, so it vanishes or explodes with the lag.
56. **LSTM gates in one line each?** Forget: what to keep; input: what to write; candidate: the content; output: what to expose.
57. **Why does the LSTM remember?** The cell is updated additively; along it the gradient is multiplied only by the forget gate.
58. **GRU vs LSTM?** Two gates, no separate cell, three weight blocks instead of four; often similar accuracy.
59. **Why LSTMs for time series?** Ordered processing, variable-length history, constant-cost online updates, gated memory of trends.
60. **Teacher forcing and its problem?** Feeding true previous tokens in training; at inference the model sees its own errors (exposure bias).

## 12.4 Attention, Transformers, LLMs, generative {#dl-12-4}

61. **Self-attention in one sentence?** Each position's output is a softmax-weighted average of value vectors, weighted by how well its query matches each key.
62. **Why divide by $\sqrt{d_k}$?** Dot products of unit-variance vectors have variance $d_k$; scaling keeps the softmax from saturating and gradients from vanishing.
63. **Why masks?** Causal masks stop positions seeing the future; padding masks stop attention to padding. Both set scores to $-\infty$ before the softmax.
64. **Why multiple heads?** Several attention patterns in different subspaces at the same parameter cost.
65. **Parameters of a multi-head attention block?** $4d^2 + 4d$, independent of the number of heads.
66. **Why positional encodings?** Self-attention is permutation-equivariant; without positions, word order is invisible.
67. **Complexity of self-attention?** $O(n^2 d)$ time and $O(n^2)$ memory per head; projections are $O(nd^2)$.
68. **What does a KV cache store?** Keys and values of all previous tokens in every layer, so generation computes only the new token's projections.
69. **Transformers over RNNs for seq2seq?** Parallel training, a constant path between any two tokens, better scaling.
70. **Encoder-only, decoder-only, encoder–decoder?** BERT for understanding, GPT for generation, T5 or the original Transformer for sequence-to-sequence.
71. **How does BPE work?** Start from characters or bytes and repeatedly merge the most frequent adjacent pair into a new token.
72. **What is perplexity?** The exponential of the per-token cross-entropy: the effective number of choices per token.
73. **What does LoRA save?** Trainable parameters, gradients and optimiser state: $r(d_{\text{in}} + d_{\text{out}})$ per matrix. Not inference cost after merging.
74. **Temperature, top-k, top-p?** Temperature sharpens or flattens; top-k keeps the $k$ most likely tokens; top-p keeps the smallest set with total probability $\ge p$.
75. **What is RAG, and why do LLMs hallucinate?** Retrieve relevant documents by embedding similarity and put them in the prompt; models hallucinate because they are trained to produce probable text, not true text.
76. **VAE objective and the reparameterisation trick?** Reconstruction minus KL to the prior (the ELBO); write $z = \mu + \sigma\odot\varepsilon$ so sampling is differentiable.
77. **GANs and diffusion in one line each?** A generator–discriminator game whose optimum matches the data distribution; learn to predict the noise added at a random level, then denoise from pure noise.

## 12.5 Your projects {#dl-12-5}

78. **Walk me through your VGG11 project.** VGG11 with BatchNorm and my own inverted dropout, trained from scratch on Oxford-IIIT Pet as one shared encoder ($512\times7\times7$ output) for three heads: 37-breed classification, head-box regression with an IoU loss, and U-Net segmentation with transposed convolutions and skip connections, combined in one multi-task forward pass.
79. **Walk me through your Transformer project.** The original encoder–decoder Transformer from scratch (3+3 layers, $d_{\text{model}}$ 256, 8 heads, about 9M parameters) for German→English on Multi30k, trained with the Noam schedule and label smoothing, decoded greedily and scored with SacreBLEU: best validation BLEU 39.76. Removing the $\sqrt{d_k}$ scaling cost about 5 BLEU.
80. **What would you do differently?** VGG11: a balanced loss between MSE and IoU on normalised box coordinates, and check the BN-after-dropout variance shift. Transformer: shorten the warm-up so short runs reach the peak rate, drop the redundant final LayerNorm, evaluate BLEU on detokenised text, and try beam search.

<div class="nb nb-moral">

If you can say all eighty in under twenty seconds each, and the last three in about a minute each, you are ready for the conceptual part of a deep-learning round.

</div>
