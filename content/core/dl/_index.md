---
title: "Deep Learning"
weight: 8
math: true
sidebar:
  open: false
---

Deep learning from a single neuron to Transformers and LLMs, written for the two places it is tested: the online assessment (output shapes, parameter counts, a softmax by hand, "what is the purpose of Adam", "which layer reduces spatial size") and the interview (backprop for an MLP, why $\sqrt{d_k}$, BatchNorm at train vs test time, ResNet, LSTM gates, and "walk me through your project").

No code and no long derivations: each topic gives the idea, the formula worth remembering, at most one small worked example, and the trap a question-setter plants. It assumes the [Machine Learning](../ml/) book's logistic-regression chapter.

<div class="nb nb-moral">

Deep learning is the largest share of placement ML questions: 22 of a 49-question sample of real non-coding OA papers. Those 22 were mostly shapes, counts and one-minute numerics on CNNs, activations, losses and optimisers.

</div>

## Your two projects

Two chapters go a little deeper because your resume puts them on the table. Look for the **"In my project"** boxes:

- **[CNNs](06-cnn/)**: VGG11 from scratch with BatchNorm and a custom dropout, the U-Net decoder with transposed convolutions and skips, the IoU loss and Dice, the multi-task model ([full project notes](../../projects/vgg11/)).
- **[Attention and the Transformer](08-transformer/)**: the from-scratch encoder–decoder for German→English, the $1/\sqrt{d_k}$ ablation, Noam warm-up, label smoothing, greedy decoding and BLEU ([full project notes](../../projects/transformer/)).

## Contents

**Part: Foundations**

- [1 · Neurons, the perceptron and the MLP](01-neurons/)
- [2 · Activations, output layers and losses](02-activations-losses/)
- [3 · Backpropagation](03-backprop/)
- [4 · Optimisers and learning-rate schedules](04-optimisers/)
- [5 · Initialisation, normalisation and regularisation](05-init-norm-reg/)

**Part: Architectures**

- [6 · Convolutional networks](06-cnn/)
- [7 · Recurrent networks](07-rnn/)
- [8 · Attention and the Transformer](08-transformer/)

**Part: Modern deep learning**

- [9 · Language models and LLMs](09-llm/)
- [10 · Generative and representation learning](10-generative/)
- [11 · Training in practice](11-practice/)

**Part: Revision**

- [12 · Rapid-fire: 80 questions with spoken answers](12-rapidfire/)
- [13 · OA practice problems](13-problems/)

## How to use it

1. **Before an OA:** chapters 1, 2, 4, 5 and 6, then chapter 13. Shapes and parameter counts are free marks.
2. **Before an interview:** chapters 3, 5, 6 and 8 for depth; chapter 12 out loud the night before.
3. **If the interviewer asks about your projects:** the "In my project" boxes in chapters 2, 4, 5, 6 and 8, then the full project pages.

## Sources

Condensed from the *Deep Learning* Napkin-style book in `placement prep/core notes/` (153 pages, 98 rapid-fire questions, 73 OA problems), whose numbers were all computed by code and checked against PyTorch. Project facts come from the Playbook's [VGG11](../../projects/vgg11/) and [Transformer](../../projects/transformer/) pages.
