---
title: "7 · Must-know before the interview"
weight: 7
---

The one-page preparation for the VGG11 multi-task project. If you only have the evening before, read this page and nothing else, then do the self-test at the bottom. Evidence labels are explained on the [section landing page](../).

## 1. The 60-second pitch (memorise the shape, not the words)

> It was a deep-learning course assignment: build **VGG11 from scratch** in PyTorch (no pre-built model), with **BatchNorm** after every conv and my **own inverted-dropout layer** in the FC head, and train it on the Oxford-IIIT Pet breeds. I reused that encoder, **frozen**, for two more heads: a **box regressor** trained on MSE plus a **custom IoU loss**, and a **U-Net decoder with transposed convolutions and skip connections** for trimap segmentation. A `MultiTaskPerceptionModel` runs the encoder **once** and returns breed logits, a box and a mask, loading three checkpoints. I also reviewed my own code afterwards and found real defects: the frozen encoder's **BatchNorm statistics still update**, the checkpoint loader fails **silently**, and my rotation augmentation puts **foreground labels in the mask border**.

Then stop and let them ask. The defects you name yourself make the rest more believable. The scores are in the W&B report; do not recite them from memory.

## 2. Numbers and facts to have ready

| Fact | Value | Label |
|---|---|---|
| Input size and bottleneck | 3×224×224 → 512×7×7 | Measured |
| Layers | 8 conv (each +BN +ReLU) + 3 FC = 11 weight layers | Code |
| Skip maps (pre-pool) | 64×224², 128×112², 256×56², 512×28², 512×14² | Measured |
| Encoder parameters | 9 225 984 (about 9.2 M) | Measured |
| `VGG11` classifier model | 128 939 813 (about 129 M); FC head is 119.7 M of it | Measured |
| Localizer / U-Net / unified | 116.2 M / 24.3 M / 251.0 M | Measured |
| Original VGG11 size (1000 classes, no BN) | about 133 M | Paper |
| Outputs | `[B,37]` logits · `[B,4]` box (cx, cy, w, h; 224-pixel space) · `[B,3,224,224]` logits | Measured |
| Dropout | inverted; mask keep-prob `1−p`; survivors × `1/(1−p)`; identity in `eval()`; `p ∈ [0,1)` | Code, Measured |
| IoU loss | `1 − I/(U+ε)`; `mean` default, `sum`, `none`; zero gradient for disjoint boxes | Code, Measured |
| Localizer loss | `MSE + IoULoss`, encoder frozen | Code |
| Segmentation loss | `CrossEntropyLoss` over 3 trimap classes | Code |
| Classes | 37 breeds; trimap 0 = pet, 1 = background, 2 = boundary | Code |
| Split | 80 / 20, `random.seed(42)`, rebuilt per task | Code |
| Optimiser | Adam, `weight_decay 1e-4`, `StepLR(10, 0.5)` | Code |
| Settings run on Kaggle | Cls 80 ep, bs 32, lr 1e-3, p 0.3 · Loc 30 ep, bs 32 · Seg 40 ep, bs 16 | Code (notebook) |
| Model selection | best val macro-F1 · best val IoU · best val Dice | Code |
| Final F1 / IoU / Dice | in the public W&B report | Not recorded |

## 3. Things you must be able to explain without looking

### Architecture
- The five blocks with channels and sizes, and why `7 = 224/2⁵` fixes the input size.
- Where BN and Dropout sit and the reason for each; why BN before ReLU; why dropout only in the FC head.
- Why the encoder returns skip maps *before* each pool.
- Why 93 % of the parameters are in the FC head.

### CustomDropout
- Inverted scaling and the expectation proof; deterministic in eval; why `p < 1`.
- How you tested it (zero fraction, kept value 1/(1−p), eval identity).

### Localization
- Output format and space; no output activation and what that costs.
- The IoU loss step by step; the zero-gradient limitation; why MSE is added; the scale mismatch.
- Frozen encoder: why, what it costs, and the BN-statistics flaw.

### Segmentation
- U-Net wiring and one stage's channel arithmetic (768 = 256 + 512).
- Transposed conv (kernel 2, stride 2); cross-entropy vs Dice; Dice vs pixel accuracy.

### Unified model and honesty
- One encoder pass, three outputs, three checkpoints merged by key prefix.
- Silent loading, `gdown` on construction, train mode left on.
- What was **measured** (shapes, counts, unit tests) and what was **not** (accuracy).

## 4. Claims to avoid

- **Any specific F1, IoU, mAP or Dice score** unless you have just re-read it in the W&B report.
- "The frozen encoder is identical across tasks." The weights are; the BatchNorm running statistics are not.
- "Class weighting improved accuracy." It is applied twice and was never ablated.
- "The model was pretrained." Everything is trained from scratch; ImageNet statistics are only for normalising inputs.
- "BN placement before ReLU is proven best." It is the convention; you did not compare.
- "The localizer outputs a confidence." It outputs four numbers only.
- "The tests prove accuracy." They prove shapes, counts and layer behaviour.
- Anything from the older `REPORT.md` draft (it describes a different design and contains pre-written "observations").

## 5. Cheat sheet

### Shapes

```text
input                 3 x 224 x 224
block1  conv 3->64    64 x 224 x 224   -> pool 64 x 112 x 112     (s1)
block2  conv 64->128  128 x 112 x 112  -> pool 128 x 56 x 56      (s2)
block3  conv ->256 x2 256 x 56 x 56    -> pool 256 x 28 x 28      (s3)
block4  conv ->512 x2 512 x 28 x 28    -> pool 512 x 14 x 14      (s4)
block5  conv ->512 x2 512 x 14 x 14    -> pool 512 x 7 x 7        (s5, then bottleneck)
classifier head       25088 -> 4096 -> 4096 -> 37
localizer head        25088 -> 4096 -> 1024 -> 4
decoder               up(512->512)+s5 -> 512 | up(512->256)+s4 -> 256 | up(256->128)+s3 -> 128
                      up(128->64)+s2 -> 64   | up(64->32)+s1 -> 32    | 1x1 conv -> 3
```

### Formulas

```text
inverted dropout:  y = x * mask / (1 - p),   mask ~ Bernoulli(1 - p),   y = x in eval
IoU loss:          1 - I / (A_p + A_t - I + eps),   boxes (cx, cy, w, h) -> corners
Dice (per class):  2 TP / (2 TP + FP + FN)
StepLR:            lr = lr0 * 0.5 ** floor((epoch - 1) / 10)
```

### Pipeline order

```text
train classifier -> classifier.pth
train localizer  (encoder from classifier.pth, frozen) -> localizer.pth
train U-Net      (encoder from classifier.pth, frozen) -> unet.pth
MultiTaskPerceptionModel: encoder + classifier from #1, regression_head from #2, decoder from #3
```

## 6. Self-test

Answer out loud, then check against the pages.

1. Draw the VGG11 encoder with channel counts and spatial sizes after each block.
2. Why is the first FC layer so large, and what would you replace it with?
3. Show that inverted dropout keeps the expected activation unchanged.
4. Compute the IoU loss for boxes `(50,50,20,20)` and `(60,50,20,20)`. (Answer: 1 − 200/600 ≈ 0.667.)
5. Why is the gradient of the IoU loss zero for disjoint boxes, and what fixes it?
6. In the U-Net, why does the second decoder stage concatenate 768 channels?
7. Why does a model that predicts only "background" score well on pixel accuracy and badly on Dice?
8. What is wrong with the way the encoder is frozen?
9. What happens if you pass a checkpoint with the wrong key prefix to `MultiTaskPerceptionModel`?
10. What do you say if asked for your final test-set score?
