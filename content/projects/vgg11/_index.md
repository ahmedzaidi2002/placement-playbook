---
title: "VGG11 Multi-Task (DL Assignment 2)"
weight: 4
sidebar:
  open: false
---

**DA6401 Assignment 2** (IIT Madras, Deep Learning): a **VGG11 built from scratch in PyTorch** (with BatchNorm and a hand-written Dropout), then reused as the shared backbone of a four-part visual perception pipeline on the Oxford-IIIT Pet dataset: **breed classification**, **head localization**, **U-Net segmentation** and a **unified multi-task model** that does all three in one forward pass.

This section is the study guide for it. It answers what the code does, why each design choice was made, how it was trained and checked, what is wrong or fragile in it, and what an interviewer can ask.

{{< cards >}}
  {{< card link="01-assignment-and-data" title="1 · The assignment and the data" subtitle="What was asked, how it was graded, the Oxford-IIIT Pet files, the loader, the augmentations and the train/val split." icon="clipboard-list" >}}
  {{< card link="02-vgg11-architecture" title="2 · VGG11 and CustomDropout" subtitle="Layer-by-layer shapes and parameter counts, where BatchNorm and Dropout sit and why, initialisation, the inverted-dropout layer." icon="chip" >}}
  {{< card link="03-task-heads" title="3 · The three heads and the unified model" subtitle="Classifier, box regressor with the IoU loss, the transposed-convolution U-Net with skips, and how multitask.py reloads three checkpoints." icon="share" >}}
  {{< card link="04-training-and-evaluation" title="4 · Training and evaluation" subtitle="train.py walk-through, the exact recipe that was run, metrics, and what the results do and do not show." icon="beaker" >}}
  {{< card link="05-checks-and-pitfalls" title="5 · Checks and known pitfalls" subtitle="What I measured by running the code, and the bugs, fragilities and honest caveats found by reading it." icon="exclamation" >}}
  {{< card link="06-interview-questions" title="6 · Interview questions" subtitle="About 40 questions with model answers, grouped by topic, plus follow-up traps." icon="chat" >}}
  {{< card link="07-must-know-checklist" title="7 · Must-know before the interview" subtitle="The 60-second pitch, numbers to have ready, claims to avoid, a one-page cheat sheet and a self-test." icon="clipboard-check" >}}
{{< /cards >}}

## At a glance

| | |
|---|---|
| Task | One shared **VGG11-BN encoder** feeding three heads on Oxford-IIIT Pet (37 breeds, head bounding boxes, 3-class trimaps) |
| Input | `3 × 224 × 224`, ImageNet mean/std normalised; **no pretrained weights** (everything trained from scratch) |
| Encoder | 8 conv layers (each Conv→BatchNorm→ReLU) in 5 blocks, each block ending in a 2×2 max-pool. Output `512 × 7 × 7` |
| Classifier head | `25088 → 4096 → 4096 → 37`, BatchNorm1d + ReLU + CustomDropout after the first two |
| Localizer head | `25088 → 4096 → 1024 → 4`, outputs `[x_center, y_center, width, height]` in 224-pixel coordinates |
| Segmentation head | 5 × (ConvTranspose2d ×2 → concat skip → 2 convs), then 1×1 conv to 3 classes |
| Losses | Class-weighted cross-entropy · MSE + custom IoU loss · pixel-wise cross-entropy |
| Selection metrics | Macro-F1 · mean IoU · mean Dice (3 classes) |
| Size | Encoder 9.23 M params; classifier model 128.9 M; U-Net 24.3 M; unified model 251.0 M |
| Graded on | Autograder: architecture shapes (5), dropout unit tests (10), IoU loss tests (5), private test set F1 / mAP / Dice (30); public W&B report (50) |

Parameter counts and shapes are <span style="color:#0071bc"><strong>[Measured]</strong></span>, see [section 5](05-checks-and-pitfalls/).

## Evidence labels used in these pages

Every non-obvious statement carries one of these, so you know how hard to lean on it in an interview.

- <span style="color:#0071bc"><strong>[Measured]</strong></span> Came out of a script I ran on the code on 2026-10-23 (PyTorch 2.11, CPU, random weights, a tiny synthetic Pet-shaped dataset). It proves shapes, counts and layer behaviour, **not** accuracy.
- <span style="color:#009b55"><strong>[Code]</strong></span> Read directly from the source. You can point at the line.
- <span style="color:#7c3aed"><strong>[Reasoned]</strong></span> Derived by arithmetic or argument from the code or from standard deep-learning facts. **Not** measured on this project. Say "I'd expect" when you use it.
- <span style="color:#d6336c"><strong>[Paper]</strong></span> A fact from the VGG paper (Simonyan and Zisserman, 2014, arXiv 1409.1556) or another cited paper.
- <span style="color:#f7921d"><strong>[Not recorded]</strong></span> A result that exists only in the online W&B report or on the grader. No local file stores it, so these pages do not quote it.

{{< callout type="warning" >}}
**What these pages do not contain: final accuracy, F1, IoU or Dice numbers.** The training ran on Kaggle; the only local W&B run folder is a 5-second stub with no metrics, and the notebook was saved without outputs. The numbers live in the public W&B report linked below. Do not state a score in an interview unless you have re-read it from that report. The pages also do not use the draft `REPORT.md` from the earlier folder: it describes a different design (no BatchNorm1d, fine-tuned encoder) and its "observations" are template text written before any run.
{{< /callout >}}

## Where the code lives

- Final version: `C:\ahmed\journey\assignmnet 2\this is it\deep_learning_a_2-main` (own git repo, 09-04-2026). This is the version documented here.
- GitHub: [ahmedzaidi2002/da-assignment-2](https://github.com/ahmedzaidi2002/da-assignment-2)
- W&B report (public): [report link](https://api.wandb.ai/links/ahmedzaidi2002-indian-institute-of-technology-madras/gchgk281)
- Training recipe: `C:\ahmed\journey\assignmnet 2\assignment2-2.ipynb` (Kaggle notebook; no saved outputs)
- Earlier copies exist under `IIT M\sem 2\dl\assignment 2` and `assignment 2 new` and `journey\assignmnet 2\results`; they differ (for example `vgg11.py` is 3.4 to 4.4 KB there against 8.4 KB here, and I did not diff them) and are **not** what this section describes.

```text
models/vgg11.py          VGG11Encoder (conv backbone, optional skip maps) and VGG11 (encoder + FC head)
models/layers.py         CustomDropout (inverted dropout, no torch.nn.Dropout)
models/classification.py VGG11Classifier  (thin wrapper around VGG11)
models/localization.py   VGG11Localizer   (encoder + 4-value regression head)
models/segmentation.py   VGG11UNet        (encoder + transposed-conv decoder with skip connections)
models/multitask.py      MultiTaskPerceptionModel (one encoder, three heads, loads 3 checkpoints)
losses/iou_loss.py       IoULoss = 1 - IoU, reductions none | mean | sum
data/pets_dataset.py     OxfordIIITPetDataset (3 tasks, albumentations)
train.py                 trainers for classification / localization / segmentation / all
multitask.py             root re-export for the autograder
inference.py             empty stub (docstring only)
```

## How to use these pages

1. Read [section 1](01-assignment-and-data/) and [section 2](02-vgg11-architecture/) once. Be able to draw the encoder with its shapes from memory.
2. Read [section 3](03-task-heads/) with `models/` open next to you. Be able to explain the U-Net channel arithmetic and the IoU formula.
3. Read [section 4](04-training-and-evaluation/) and [section 5](05-checks-and-pitfalls/) so you can answer "what went wrong?" and "how do you know it works?" without hesitation.
4. Cover the answers in [section 6](06-interview-questions/) and say them out loud.
5. The day before, use only [section 7](07-must-know-checklist/).
