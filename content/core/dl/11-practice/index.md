---
title: "11 · Training in practice"
linkTitle: "11 Training in practice"
weight: 11
math: true
---
Knowing the maths is half of an ML-engineer interview; the other half is whether you can make a model train and know why it does not. This chapter is that working knowledge, without code: the training loop's five critical lines, the bugs that do not crash but quietly ruin results, a debugging routine, memory and mixed precision, and one paragraph each on graph networks and reinforcement learning.

## 11.1 The training loop, in words {#dl-11-1}

Every epoch: switch to **training mode** (dropout on, BatchNorm uses batch statistics); for each shuffled mini-batch, **zero the gradients**, run the forward pass, compute the loss **from logits**, backpropagate, and take an optimiser step. To evaluate: switch to **eval mode** (dropout off, BatchNorm uses running statistics) and run **without building a graph** (no_grad). Those five things (train/eval mode, zero_grad, logits into the loss, no_grad for evaluation, shuffling) carry most of the bugs.

**Broadcasting** (align shapes from the right; each pair of dimensions must be equal or 1) is what makes $XW^\top + b$ work for a batch, and the source of the nastiest shape bug below.

## 11.2 The silent-bug catalogue {#dl-11-2}

Each of these runs without an error message:

| Bug | What happens |
|---|---|
| Forgetting `eval()` | dropout stays random and BN uses batch statistics: two passes on the same input differ, accuracy drops, and the running statistics keep changing |
| Softmax before `CrossEntropyLoss` | softmax applied twice: gradients squashed, the loss cannot reach its floor, confidences meaningless |
| Softmax over the wrong dimension | "probabilities" whose rows do not sum to 1 (normalised over the batch) |
| Predictions $(B, 1)$ vs targets $(B)$ | broadcasting makes a $(B, B)$ difference; a perfect model gets a non-zero MSE |
| Forgetting `zero_grad()` | gradients accumulate; each step uses the sum of all past gradients |
| No shuffling on label-sorted data | every batch has one class; 49.5% vs 92.0% accuracy after one epoch in the book's test |
| Label leakage | a feature that is the label plus noise gives 100% validation accuracy and collapses in deployment |
| Resuming without optimiser state | Adam's moments reset; training diverges from the uninterrupted run |

Others worth naming: evaluating without `no_grad` (memory grows), calling `.item()` inside the forward pass (cuts the graph), augmentation applied to the validation set, normalisation statistics computed including the test split, preprocessing that differs between training and serving, schedulers stepped per batch instead of per epoch.

## 11.3 Debugging a model that does not learn {#dl-11-3}

1. **Check the initial loss:** about $\ln K$ for $K$ balanced classes.
2. **Overfit one small batch:** turn off regularisation and drive the loss on, say, 32 examples to near zero. If that fails, the bug is in the model, loss, labels or optimiser wiring, not in the data.
3. **Check shapes and dtypes** at every stage; print a batch and its labels; look at inputs after augmentation.
4. **Check gradients:** non-zero and finite for every parameter; per-layer norms for vanishing or exploding.
5. **Tune the learning rate first** (a sweep over powers of ten), then the schedule, then regularisation.
6. **Compare with a trivial baseline** and grow the model only after the small version works.

**Reproducibility:** seed Python, NumPy, PyTorch and every data-loader worker; request deterministic algorithms; fix library versions. Even then results differ across hardware, so **report the spread over several seeds**, not one lucky run. **Checkpoints** must hold the model *and* optimiser state, the scheduler, the step and the random-generator states.

## 11.4 Precision, memory and many GPUs {#dl-11-4}

| Format | Largest value | Precision (machine epsilon) |
|---|---|---|
| fp32 | $3.4\times10^{38}$ | $1.2\times10^{-7}$ |
| fp16 | 65,504 | $9.8\times10^{-4}$ |
| bf16 | $3.4\times10^{38}$ | $7.8\times10^{-3}$ |

**Mixed precision** runs matrix products in half precision while keeping fp32 master weights, reductions and the optimiser. fp16 has a narrow range: a gradient of $10^{-8}$ underflows to 0, so **loss scaling** multiplies the loss before backward and divides after. **bf16** keeps fp32's range with fewer mantissa bits, so it needs no loss scaling but is coarser.

**Where training memory goes:** mixed-precision Adam stores fp16 weights (2 bytes) and gradients (2), fp32 master weights (4) and two moments (4 + 4): about **16 bytes per parameter**, so a 7B model needs about 112 GB before activations. Activations scale with batch, sequence length and depth; gradient checkpointing trades recomputation for them. This arithmetic is why LoRA and quantised bases make fine-tuning feasible on one GPU.

**Scaling out:** **data parallelism** (DDP) gives every GPU a full replica and a slice of the batch, and averages gradients with an all-reduce before an identical step. When the model does not fit, **sharded** data parallelism (FSDP/ZeRO) splits parameters, gradients and optimiser state, and tensor or pipeline parallelism split the layers. **Gradient accumulation** emulates a big batch on one device: sum the gradients of $k$ micro-batches (each loss divided by $k$), then step. It is exact for a mean loss, except with BatchNorm, whose statistics depend on the micro-batch.

## 11.5 Graph networks, reinforcement learning and time series {#dl-11-5}

**Graph neural networks.** Molecules, social networks, transactions and recommendations are graphs. A **message-passing** layer updates each node from its neighbours with a permutation-invariant aggregation (sum, mean, max). The **GCN** layer is the simplest: add self-loops, normalise the adjacency symmetrically by degrees ($D^{-1/2}(A + I)D^{-1/2}$), aggregate neighbour features, transform, apply ReLU. $k$ layers see $k$-hop neighbourhoods; too many layers **over-smooth** all nodes to similar vectors. Self-attention is message passing on a complete graph. (Your M.Tech project's [GNN explainability work](../../../projects/mtp/) builds on exactly this layer.)

**Reinforcement learning.** An agent in state $s$ takes action $a$, receives reward $r$, and maximises the expected discounted return $\sum_t \gamma^t r_t$. **Policy gradient** (REINFORCE) raises the log-probability of actions in proportion to the return they led to, with a baseline subtracted to cut variance. **DQN** regresses $Q(s, a)$ towards $r + \gamma\max_{a'}Q_{\text{target}}(s', a')$, stabilised by experience replay and a slowly updated target network. RLHF (chapter 9) is policy optimisation with a learned reward.

**Deep time series.** Frame forecasting as supervised learning with sliding windows (a series of length 100 with 24 input and 6 target steps gives 71 examples). Models: causal dilated 1-D CNNs, LSTMs, Transformers over patches. The traps are not architectural: split by time, compute normalisation on the training period only, and beat seasonal-naive and gradient-boosting baselines first.

<div class="nb nb-moral">

Shuffle, zero the gradients, feed logits to the loss, use eval mode and no_grad for evaluation, checkpoint the optimiser too; when stuck, overfit one batch first.

</div>
