---
title: "5 · Checks and known pitfalls"
weight: 5
---

This page answers two interview questions: **"how do you know it works?"** and **"what would you fix?"** Evidence labels are explained on the [section landing page](../).

## What I checked, and what that proves

On 2026-10-23 I ran the project's real modules in a CPU-only PyTorch 2.11 session with **random weights** and a **synthetic** 20-image Pet-shaped dataset (random pixels, random trimaps, XMLs for 12 of the 20). The script imports the repository code unchanged. `gdown` was replaced by a stub so nothing was downloaded.

| Check | Result | Verdict |
|---|---|---|
| Encoder shapes through 5 blocks, eval mode | bottleneck `(2, 512, 7, 7)`; skips `s1…s5` = `64×224²`, `128×112²`, `256×56²`, `512×28²`, `512×14²` | Matches standard VGG11 topology |
| Parameter counts | encoder 9 225 984; `VGG11` 128 939 813; localizer 116 200 196; U-Net 24 324 131; unified 251 012 172 | Sums are consistent (see [section 3](../03-task-heads/)) |
| Unified forward, batch 2 and batch 1, eval | `(2,37)`, `(2,4)`, `(2,3,224,224)`; batch 1 works in eval | Output contract satisfied |
| `CustomDropout` | 0.5012 zeroed at p = 0.5, kept value exactly 2.0; 0.2015 at p = 0.2, kept value 1.25; `eval()` bit-identical; p = −0.1 and 1.0 rejected | Passes the three things the grader tests |
| `IoULoss` | 0 for identical, 1 for disjoint, 0.6667 for a 10 px shift, 0.75 for a contained box, 1.0 for zero-size boxes, finite gradient for negative width, `mean`/`sum` correct | Passes hand-computed cases |
| Dataset loader, three tasks, two splits | tensor `(3,224,224)`; box in 224 space; mask values `{0,1,2}` in both splits | Works with albumentations 2.0.8 |
| Frozen-encoder BN buffers (see pitfall 1) | running mean **changed** in `train()` although all encoder parameters had `requires_grad=False` | **Confirmed defect** |
| Segmentation augmentation label noise (see pitfall 6) | 8.2 % of an all-background mask became class 0 when the transform fired | **Confirmed defect** |

**What this does not prove.** It does not prove that the trained networks are accurate. No trained checkpoint was available locally (they are on Google Drive and in a W&B artifact), so I did not evaluate F1, IoU or Dice. Equally, a shape and unit-test pass says nothing about generalisation. <span style="color:#f7921d"><strong>[Not recorded]</strong></span> for the real scores: read them from the W&B report.

## Pitfalls, from most to least serious

### 1. "Frozen" encoder is not fully frozen: BatchNorm statistics still move <span style="color:#0071bc"><strong>[Measured]</strong></span>

For localization and segmentation the trainer sets `requires_grad = False` on the encoder and gives the optimiser only the head. But it calls `model.train()` on the **whole** model each epoch. A BatchNorm layer in training mode updates its **running mean and variance** on every forward pass, whether or not its parameters need gradients, and uses the current **batch** statistics for normalising.

<span style="color:#0071bc"><strong>[Measured]</strong></span> After one forward pass of a `VGG11Localizer` in `train()` with every encoder parameter frozen, `encoder.conv_block1[1].running_mean` had changed and `num_batches_tracked` was 1.

Why it matters <span style="color:#7c3aed"><strong>[Reasoned]</strong></span>:

1. During localizer (and U-Net) training the head receives features normalised with **batch statistics** of the Pet images. After training, `localizer.pth` and `unet.pth` hold encoder buffers that **drifted** from the classifier's.
2. `MultiTaskPerceptionModel` loads the encoder **only** from `classifier.pth`, so at inference the encoder normalises with the **classifier's** running statistics, not the ones the box head and decoder saw when they were trained.
3. The code comment in `_load_checkpoints` says all three checkpoints "share exactly the same encoder weights". That is true for the learnable weights and false for the BN buffers.

I did not measure how much accuracy this costs because the checkpoints are not local. The effect is probably small if the classifier's running statistics are close to the Pet dataset's statistics, which they are in the same domain. The fix is one line: put the frozen encoder in eval mode, for example `model.encoder.eval()` after each `model.train()`.

### 2. Constructing `MultiTaskPerceptionModel` downloads files and can overwrite your local checkpoints <span style="color:#0071bc"><strong>[Measured]</strong></span>

The first lines of `__init__` call `gdown.download(id=…, output=classifier_path / localizer_path / unet_path)`. <span style="color:#0071bc"><strong>[Measured]</strong></span> With a stubbed `gdown`, constructing the model made exactly three calls, writing to the three paths you pass in. Consequences <span style="color:#7c3aed"><strong>[Reasoned]</strong></span>:

- It needs internet on **every** construction, and a `PermissionError` or network failure kills the constructor.
- If you pass your freshly trained local files as the paths (as the notebook's last cell does), `gdown` writes the Drive copies **over them**. If the Drive copies were stale, the sanity check tests the stale weights, not the ones just trained.
- The calls run **before** `super().__init__()`. That works because they touch no module state, but it is unusual, and the docstring that follows them has become a bare string expression (it is no longer the function's docstring).
- The Drive files must not be deleted until the marks are released (the submission guide says so), because the grader's constructor downloads them.

The submission guide mandates these lines, so they are not a mistake; the point is to know what they do.

### 3. The unified model is left in `train()` mode <span style="color:#0071bc"><strong>[Measured]</strong></span>

After construction `model.training` is `True`. In that state dropout is active in both FC heads and `BatchNorm1d` raises `ValueError: Expected more than 1 value per channel when training` for a **batch of one**. <span style="color:#0071bc"><strong>[Measured]</strong></span> In `eval()` the same single image works. The autograder presumably calls `.eval()`; if it did not, the outputs would be stochastic. Always call `model.eval()` before inference and wrap it in `torch.no_grad()`.

### 4. Silent partial checkpoint loading <span style="color:#0071bc"><strong>[Measured]</strong></span>

`_load_submodule` extracts the keys with a given prefix and only loads **if any were found** (`if sub:`). <span style="color:#0071bc"><strong>[Measured]</strong></span> A checkpoint whose keys all had the wrong prefix loaded "successfully": no error, no warning beyond the "Loading classifier checkpoint" line, and the model stayed random. A missing file likewise only prints a warning. For a grader this is the dangerous failure mode: the model runs, produces plausible shapes, and gives chance-level scores. A safer version would raise when a required prefix is absent.

### 5. IoU loss is blind to disjoint boxes, and MSE swamps it early <span style="color:#0071bc"><strong>[Measured]</strong></span>

Zero gradient for a fully disjoint prediction was measured, and the pixel-scale MSE term is much larger than the `[0, 1]` IoU term at the start (see [section 3](../03-task-heads/)). Together they mean the IoU loss mostly **refines** boxes that already overlap. GIoU or DIoU would also give a gradient for far-apart boxes; the assignment fixed the plain IoU formulation.

### 6. Label noise from segmentation augmentation <span style="color:#0071bc"><strong>[Measured]</strong></span>

`ShiftScaleRotate(border_mode=0)` fills uncovered mask area with 0, which is the **foreground** class after the `−1` shift: 8.2 % of pixels in the test, about 3 % per sample in training given `p = 0.4`. See [section 1](../01-assignment-and-data/).

### 7. Class weights applied twice, and the validation loss is weighted <span style="color:#009b55"><strong>[Code]</strong></span>

See [section 4](../04-training-and-evaluation/). Not harmful on a near-balanced dataset, but it is untested.

### 8. Smaller issues <span style="color:#009b55"><strong>[Code]</strong></span>

- **`inference.py` is empty** (docstring only), and the repository has **no mAP** implementation although mAP is the box metric the grader uses. The in-repo IoU is the only localization number.
- `VGG11Localizer`'s docstring says the box is in "original image pixel space", but the loader emits **224-pixel** coordinates. The fixed input size makes the grader consistent with the latter.
- The Dice in `train.py` averages three classes; if the grader's Dice is foreground-only the two numbers differ.
- Each task's train/val split is rebuilt from a differently filtered list and seeds the global `random` generator.
- `requirements.txt` leaves `albumentations` unpinned and does not list `gdown`, which `multitask.py` imports.
- `train.py --task all` applies the same epochs and learning rate to all three tasks.
- Nothing in the repository's Python code logs to W&B.

## What I would do next

1. Put the frozen encoder in `eval()` mode, then re-train the two heads and compare the three scores before and after. This is the single most informative experiment.
2. Make `_load_submodule` raise on a missing prefix, and make `multitask.py` skip the download when the file already exists.
3. Use a mask fill value that the loss ignores in the segmentation augmentation.
4. Add mAP and pixel-accuracy computation to an `inference.py`, and log everything to W&B from `train.py`.
5. Try GIoU for the box loss and normalised coordinates for the MSE term, and a combined cross-entropy + Dice loss for the U-Net (the boundary class is rare and thin).
6. Pin library versions in `requirements.txt`.
