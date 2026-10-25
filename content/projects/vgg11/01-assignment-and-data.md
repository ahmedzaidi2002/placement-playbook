---
title: "1 · The assignment and the data"
weight: 1
---

Source: `DA6401_Assignment_2.pdf` (the spec), `data/pets_dataset.py` (the loader). Evidence labels are explained on the [section landing page](../).

## What was asked

One pipeline, four tasks, built on a single VGG11.

| Task | Requirement (paraphrased from the PDF) | Where it lives |
|---|---|---|
| 1 · Classification | VGG11 **from scratch** with `torch.nn` modules (no pre-built VGG), BatchNorm added, a **custom Dropout** module (no `nn.Dropout`, no `F.dropout`), and a written justification of where BN and Dropout go | `models/vgg11.py`, `models/layers.py` |
| 2 · Localization | Reuse the Task-1 backbone, say whether it is frozen or fine-tuned and why, attach a regression head that outputs exactly `[x_center, y_center, width, height]`, train with a **custom IoU loss** (an `nn.Module`) | `models/localization.py`, `losses/iou_loss.py` |
| 3 · Segmentation | U-Net style with the VGG11 as contracting path, **transposed convolutions** for upsampling (no bilinear or unpooling for the main steps), **concatenate** the aligned encoder map at each stage, state and justify the loss | `models/segmentation.py` |
| 4 · Unified model | One `forward(x)` that returns breed logits, box and segmentation map together | `models/multitask.py` |

Extra rules from the skeleton `README` <span style="color:#009b55"><strong>[Code]</strong></span> (the instructions file shipped with the assignment): VGG11 follows the paper with BN and Dropout as the only allowed changes; train on **normalised** images; the box output is in **pixel space, not normalised**; the localizer trains on **MSE + custom IoU loss**; the IoU loss must lie in `[0, 1]`, support `mean` and `sum` reductions with `mean` as default; paths in `multitask.py` are relative; do not import any package outside the allowed list or the autograder crashes.

Allowed libraries: `torch`, `numpy`, `matplotlib`, `scikit-learn`, `wandb`, `albumentations`. The submission guide additionally requires `gdown` inside `MultiTaskPerceptionModel.__init__` to fetch the three checkpoints from Google Drive.

### How it was graded

| Part | Marks | What the grader does |
|---|---|---|
| Architecture check | 5 | Instantiates `VGG11`, traces a forward pass and checks intermediate feature-map sizes against the standard VGG11 topology |
| Dropout check | 10 | Unit-tests `CustomDropout`: statistics of the mask, inverted `1/(1−p)` scaling, identity when `training=False` |
| IoU loss check | 5 | Pairs of boxes: exact value, numerical stability, gradients |
| Private test set | 30 | Runs `MultiTaskPerceptionModel` on held-out images: **macro-F1** (breed), **mAP** (box), **Dice** (segmentation) |
| W&B report | 50 | Public, interactive: BN effect, dropout p ∈ {0, 0.2, 0.5}, transfer-learning strategies, feature maps, box table, Dice vs pixel accuracy, in-the-wild images, reflection |

The autograder imports exactly four names: `models.vgg11.VGG11`, `models.layers.CustomDropout`, `losses.iou_loss.IoULoss`, `multitask.MultiTaskPerceptionModel` <span style="color:#009b55"><strong>[Code]</strong></span>. That is why the root `multitask.py` only re-exports the class.

## The dataset: Oxford-IIIT Pet

Three kinds of labels for the same images <span style="color:#009b55"><strong>[Code]</strong></span>:

| Label | File | Loader behaviour |
|---|---|---|
| Breed (37 classes) | `annotations/list.txt`, one line per image: `name CLASS-ID SPECIES BREED ID` | Comment lines (`#`) skipped. Class id is 1-based in the file, so the loader subtracts 1 to get `0..36` |
| Head box | `annotations/xmls/<name>.xml` (PASCAL VOC) | Reads the first `bndbox`: `xmin, ymin, xmax, ymax` in original pixels |
| Trimap | `annotations/trimaps/<name>.png` | Values `1` = pet, `2` = background, `3` = boundary; the loader subtracts 1 so the classes are `0, 1, 2` |

The images are not a fixed size, so everything is resized to **224 × 224**, the VGG11 input size (the spec says the size can be hard-coded).

{{< callout type="warning" >}}
**The box is the pet's head, not its body.** The public annotation marks the head. A localizer trained on it learns "where is the head", and a full-body shot still gets a head box. This matters when you explain failure cases.
{{< /callout >}}

### Train / validation split

`OxfordIIITPetDataset(root_dir, split, task, ...)` builds the list of usable samples, shuffles it with `random.seed(42)`, and takes the first **80 %** as `train` and the rest as `val` (`val_split=0.2`) <span style="color:#009b55"><strong>[Code]</strong></span>. There is no separate test split; the real test set is the grader's private one.

Three things worth knowing:

1. The sample list is **filtered per task**. For localization the loader skips every image that has no XML; for segmentation every image that has no trimap. So the three tasks do not see the same images in `train` and `val`. <span style="color:#0071bc"><strong>[Measured]</strong></span> On a synthetic set of 20 images where only 12 had XMLs: classification 16 train / 4 val, localization 9 train / 3 val, segmentation 16 / 4.
2. Because the split is re-shuffled per task, an image that is in the localizer's `val` can be in the classifier's `train`. That does not leak the box label, but it means the validation numbers of the three tasks are not computed on one common held-out set. <span style="color:#7c3aed"><strong>[Reasoned]</strong></span>
3. The call `random.seed(random_seed)` seeds Python's **global** random generator as a side effect of building the dataset. <span style="color:#009b55"><strong>[Code]</strong></span>

As far as I recall the dataset's public documentation, the release ships `list.txt` for all images but bounding-box XMLs for only part of them, so the localization data is a subset. I did not count the files in your copy, so check the data folder before quoting a size.

## Preprocessing and augmentation

All transforms use **albumentations**. Every pipeline ends in `Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])`, the ImageNet statistics <span style="color:#009b55"><strong>[Code]</strong></span>. The code comment says "VGG11 paper uses ImageNet-pretrained weights"; that is loose wording: the network here is trained from scratch, and the constants are simply the standard ImageNet colour statistics (the grader feeds normalised images, so training on normalised images is required).

| Task | Train transform | Val transform |
|---|---|---|
| Classification | RandomResizedCrop 224 (scale 0.6–1.0, ratio 0.75–1.33) · HorizontalFlip 0.5 · ColorJitter 0.6 · ShiftScaleRotate 0.4 (shift 0.05, scale 0.1, rot 15°) · GaussianBlur 0.2 · **CoarseDropout** 0.3 (up to 8 holes of 24 px) | Resize 224 |
| Localization | RandomResizedCrop (scale 0.7–1.0, ratio 0.85–1.15) · HorizontalFlip · ColorJitter 0.5 (milder) · ShiftScaleRotate 0.3 (rot 10°) · GaussianBlur 0.2, with **`BboxParams(pascal_voc, min_visibility=0.2)`** | Resize 224 with the box |
| Segmentation | RandomResizedCrop (scale 0.6–1.0) · HorizontalFlip · ColorJitter 0.5 · ShiftScaleRotate 0.4 · GaussianBlur 0.2 (mask transformed with the image) | Resize 224 |

Design choices visible in the code <span style="color:#009b55"><strong>[Code]</strong></span>:

- **CoarseDropout is used only for classification.** For localization and segmentation the comments say that erasing pixels while keeping the box or mask label would give contradictory supervision.
- The localization pipeline is **bbox-aware**: the box is transformed with the image, and `min_visibility=0.2` drops a box that the crop cut down to less than 20 % of its area.
- If a box is dropped, degenerate after clipping, or unparsable, `__getitem__` falls back to the **next sample** (`idx + 1`). It is a recursive call, so a dataset in which every box is bad would recurse until Python raises `RecursionError`. <span style="color:#7c3aed"><strong>[Reasoned]</strong></span> With real Pet data that does not happen.

### What a localization sample looks like

The loader converts the transformed corner box `(xmin, ymin, xmax, ymax)` to the model's target format:

```python
x_center = (xmin + xmax) / 2
y_center = (ymin + ymax) / 2
width    = xmax - xmin
height   = ymax - ymin
```

The numbers are in the **224 × 224 resized image**, not in the original file's pixels. <span style="color:#0071bc"><strong>[Measured]</strong></span> A synthetic sample returned `[112.0, 107.2, 171.5, 176.3]`, all within 224. The docstring of `VGG11Localizer` says "original image pixel space"; the data pipeline actually defines "pixel space" as the resized 224 grid, and that is the space the grader's box must be in because the image size is fixed.

## Pitfall found in the segmentation augmentation

`ShiftScaleRotate(border_mode=0)` fills the area that rotation and shifting uncover with **zeros**. For the image that is a black border, which is harmless. For the **mask** the fill value is also `0`, which after the `−1` shift is the class **foreground (pet)**. <span style="color:#0071bc"><strong>[Measured]</strong></span> On an all-background mask, forcing this transform (`p = 1`) turned **8.2 %** of the pixels into class 0 (albumentations 2.0.8, 50 trials). In training the transform fires with probability 0.4, so the expected label noise is about 3 % of pixels per sample, concentrated at the image border. <span style="color:#7c3aed"><strong>[Reasoned]</strong></span> A cleaner choice is a mask fill value that the loss ignores (for example `255` with `ignore_index=255`). This is a real but small imperfection and a good example of "I looked for label noise in my augmentation".

## Pitfall: unpinned albumentations

`requirements.txt` says `albumentations>=1.0.0`. The dataset code uses arguments (`CoarseDropout(max_holes=…)`, `ShiftScaleRotate`) that were renamed or deprecated in the 2.x line. <span style="color:#0071bc"><strong>[Measured]</strong></span> The loader constructed and ran for all three tasks on albumentations 2.0.8. <span style="color:#7c3aed"><strong>[Reasoned]</strong></span> A future release may drop the old argument names, so pin the version you trained with.
