---
title: "6 · Interview questions"
weight: 6
---

Questions an interviewer can reasonably ask about this project, grouped by topic, with model answers. **Cover the answer, say yours out loud, then open it.** Answers are written to be spoken in 20 to 60 seconds; "Depth" lines are for follow-ups. Evidence labels are explained on the [section landing page](../).

No answer below quotes a final accuracy, F1, IoU or Dice: those are <span style="color:#f7921d"><strong>[Not recorded]</strong></span> outside the W&B report. If asked for one, say where it is, and read it from there.

## A. The project as a whole

{{< details title="A1. Walk me through the project in one minute." >}}

It was the second deep-learning assignment at IIT Madras. I built **VGG11 from scratch** in PyTorch, with BatchNorm and my own Dropout layer, and trained it to classify the 37 breeds in the Oxford-IIIT Pet dataset. I then reused that encoder as a frozen backbone for two more tasks: a regression head that predicts the pet's head bounding box, trained with MSE plus a custom IoU loss, and a **U-Net-style decoder with transposed convolutions and skip connections** for three-class trimap segmentation. Finally a `MultiTaskPerceptionModel` runs the shared encoder once and returns the breed logits, the box and the mask together, loading the three trained checkpoints. It was graded by an autograder on architecture shapes, dropout statistics, IoU-loss correctness and a private test set.

{{< /details >}}

{{< details title="A2. Was this your own design or a template?" >}}

The assignment gave a skeleton: file names, class names and the required behaviour. The architecture decisions inside it were mine to make and justify: where BatchNorm and Dropout go, frozen versus fine-tuned encoder, the loss for segmentation, the augmentations and the training recipe. The VGG11 topology itself is fixed by the paper. I do not present it as research; it is a coursework implementation.

{{< /details >}}

{{< details title="A3. What was the hardest part?" >}}

Getting the three tasks to share one backbone cleanly. The encoder had to serve three consumers: a flat bottleneck for two FC heads and five skip maps for the decoder, so I made the encoder return both optionally. Then the checkpoints had to line up by module name so the unified model could load an encoder from one file and heads from the others. Later, reading my own code critically, I found a subtle flaw in how I froze the encoder (BatchNorm statistics still update in train mode), which is a good example of why you also have to look at buffers, not just `requires_grad`.

{{< /details >}}

{{< details title="A4. What would you change?" >}}

First, put the frozen encoder in eval mode so its BN statistics do not drift, and measure the effect. Second, make the checkpoint loader raise on a missing key prefix instead of silently leaving a head random. Third, fix a small label-noise source in the segmentation augmentation (rotation fills the mask with the foreground class). Then add mAP and pixel accuracy to an inference script, and try GIoU for boxes and CE + Dice for segmentation.

{{< /details >}}

## B. VGG and convolutional fundamentals

{{< details title="B1. Why does VGG stack 3×3 convolutions instead of using bigger filters?" >}}

Two stacked 3×3 layers cover the same 5×5 region as one 5×5 layer, three cover 7×7, but with fewer weights (`2·9C² = 18C²` against `25C²`) and with an extra non-linearity between them, which makes the function more expressive. Depth from small filters is the whole VGG idea. <span style="color:#d6336c"><strong>[Paper]</strong></span>

{{< /details >}}

{{< details title="B2. Draw the VGG11 encoder with shapes." >}}

Input `3×224×224`. Block 1: one conv to 64, then pool to 112. Block 2: one conv to 128, pool to 56. Block 3: two convs to 256, pool to 28. Block 4: two convs to 512, pool to 14. Block 5: two convs to 512, pool to **`512×7×7`**. That is 8 convs; with three FC layers it is 11 weight layers, hence "11". Every conv is 3×3, stride 1, padding 1, so only the pools change the size. <span style="color:#0071bc"><strong>[Measured]</strong></span>

*Depth:* the FC head is `25088 → 4096 → 4096 → classes`.

{{< /details >}}

{{< details title="B3. Where are the parameters?" >}}

Mostly in the first FC layer. The encoder is about **9.2 M** parameters, the classifier head about **119.7 M**, so the model is **128.9 M**, about 93 % of it in the two big FC layers (`25088×4096` alone is 102.8 M). That is VGG's known inefficiency; modern networks replace the FC head with global average pooling. <span style="color:#0071bc"><strong>[Measured]</strong></span>

{{< /details >}}

{{< details title="B4. Why is the input size fixed at 224?" >}}

Because of the first FC layer: it expects a flattened `512×7×7 = 25088` vector, and `7 = 224 / 2⁵`. Any other input size changes the bottleneck size and the linear layer shape no longer matches. A fully convolutional head or adaptive pooling would remove the restriction. <span style="color:#009b55"><strong>[Code]</strong></span>

{{< /details >}}

{{< details title="B5. What does BatchNorm do, and why before the ReLU?" >}}

During training it normalises each channel with the **batch** mean and variance, then applies a learned scale and shift; during evaluation it uses **running averages** of those statistics. That keeps layer inputs in a stable range, so you can use higher learning rates and converge faster, and it adds mild regularisation from batch noise. I put it between conv and ReLU so the ReLU sees a centred pre-activation, which is the usual convention for BN-VGG. <span style="color:#d6336c"><strong>[Paper]</strong></span> Putting it after ReLU also works and some people prefer it; I did not compare.

{{< /details >}}

{{< details title="B6. What goes wrong with BatchNorm and a batch of size 1?" >}}

In training mode `BatchNorm1d` cannot compute a variance from one sample and raises an error; I hit that when the unified model was left in `train()` mode. `BatchNorm2d` over a feature map still has many values per channel, so it does not crash, but batch-statistics become noisy with tiny batches. At inference you use the running statistics, so a single image is fine. <span style="color:#0071bc"><strong>[Measured]</strong></span>

{{< /details >}}

{{< details title="B7. Why dropout only in the FC layers?" >}}

That is where the parameters are, and so where co-adaptation and overfitting live. Convolutional layers share weights across positions and have far fewer parameters, and their neighbouring activations are highly correlated, so dropping single activations barely regularises them. The original VGG also used dropout only on the first two FC layers. I did not put it before the output layer because that would add noise right where the logits are formed. <span style="color:#d6336c"><strong>[Paper]</strong></span>

{{< /details >}}

{{< details title="B8. How are the weights initialised, and why?" >}}

Convs use **Kaiming normal** with `fan_out` and ReLU gain, which keeps activation variance roughly constant through ReLU layers; the FC layers use `N(0, 0.01)` as in the VGG paper; BN starts at scale 1, shift 0; all biases 0. With BatchNorm in every block the network is much less sensitive to the exact init than the original VGG, which needed a staged, shallow-to-deep initialisation. <span style="color:#d6336c"><strong>[Paper]</strong></span>

{{< /details >}}

{{< details title="B9. Why does the model output logits and not probabilities?" >}}

The loss (`CrossEntropyLoss`) applies a numerically stable log-softmax internally, so feeding it probabilities would apply softmax twice and lose precision. Also the grader only needs the arg-max, which is the same for logits and probabilities.

{{< /details >}}

## C. Custom Dropout

{{< details title="C1. Explain your dropout implementation." >}}

In training mode I draw a Bernoulli mask with keep probability `1 − p`, multiply the input by it, and divide by `1 − p` (**inverted dropout**). That keeps the expected value of each unit unchanged, so at test time the layer is just the identity. In eval mode it returns the input untouched, which makes inference deterministic. It subclasses `nn.Module` and does not use `nn.Dropout` or `F.dropout`, as the assignment required. <span style="color:#009b55"><strong>[Code]</strong></span>

{{< /details >}}

{{< details title="C2. Why divide by 1 − p? Show the expectation." >}}

A unit survives with probability `q = 1 − p`. Without scaling, `E[mask·x] = q·x`, so training and test activations would differ by a factor `q`. With scaling, `E[mask·x / q] = (q·x)/q = x`. The variance does change (`x²·p/(1−p)`), which is the source of the dropout/BatchNorm interaction. <span style="color:#7c3aed"><strong>[Reasoned]</strong></span>

{{< /details >}}

{{< details title="C3. How did you test it?" >}}

I ran it on a large tensor of ones: at `p = 0.5` about 50.1 % of entries were zero, the surviving value was exactly 2.0 and the mean was about 1.0; at `p = 0.2` the survivors were 1.25 and 20.2 % were zeroed. In `eval()` the output was identical to the input. Invalid probabilities (negative or 1.0) raise `ValueError`. Those are the three properties the grader's unit test checks. <span style="color:#0071bc"><strong>[Measured]</strong></span>

{{< /details >}}

{{< details title="C4. Why must p be less than 1?" >}}

The scale factor is `1 / (1 − p)`, which is infinite at `p = 1`, and at `p = 1` every unit would be dropped anyway. `p = 0` is allowed and makes the layer an identity, which is how I ran the "no dropout" experiment. <span style="color:#009b55"><strong>[Code]</strong></span>

{{< /details >}}

{{< details title="C5. Do dropout and BatchNorm work well together?" >}}

There is a known tension: dropout changes activation variance between training and evaluation, and a BatchNorm layer after it learns statistics under dropout noise that no longer apply at test time. In my head the first BatchNorm1d comes before any dropout, but the second follows a Linear that took dropped-out inputs. I did not isolate the effect; the p = 0 / 0.2 / 0.5 W&B runs are where it would show. <span style="color:#d6336c"><strong>[Paper]</strong></span> Li et al. (2019)

{{< /details >}}

## D. Localization and the IoU loss

{{< details title="D1. How does your localizer work?" >}}

It reuses the trained VGG11 encoder, flattens the `512×7×7` bottleneck, and passes it through two FC layers (4096, then 1024, with BatchNorm, ReLU and dropout) to a final linear layer of four numbers: `x_center, y_center, width, height` in **224-pixel** coordinates, with no output activation. It is trained on `MSE + IoU loss`, and the best epoch by validation IoU is kept.

{{< /details >}}

{{< details title="D2. Write the IoU loss and explain every step." >}}

Convert both boxes from centre format to corners (`x ± w/2`, `y ± h/2`). The intersection rectangle runs from the larger of the two top-left corners to the smaller of the two bottom-right corners; its width and height are clamped at zero so disjoint boxes get zero area. The union is the two box areas minus the intersection. `IoU = I / (U + ε)` and the loss is `1 − IoU`, so it lies in `[0, 1]`. I use `abs()` on widths and heights in the area so a negative early prediction does not give a negative area. <span style="color:#009b55"><strong>[Code]</strong></span>

{{< /details >}}

{{< details title="D3. What is the weakness of an IoU loss?" >}}

If the predicted and true boxes do not overlap, the intersection is zero and **its gradient is zero** too, so the loss gives no signal about which way to move. I measured exactly zero gradient for a fully disjoint pair. That is why the assignment adds MSE (it always pulls the box towards the target), and why GIoU, DIoU and CIoU exist. <span style="color:#0071bc"><strong>[Measured]</strong></span>

{{< /details >}}

{{< details title="D4. Why MSE plus IoU and not one of them?" >}}

MSE gives a gradient for any distance, but it treats the four numbers independently and does not match the metric (a 5-pixel error matters more on a small box). IoU matches the metric and is scale-invariant, but is flat for non-overlapping boxes. The sum covers both. A caveat: MSE is in raw pixels, so early on it is thousands while IoU is at most 1, and the IoU term only matters once the boxes are close. <span style="color:#7c3aed"><strong>[Reasoned]</strong></span>

{{< /details >}}

{{< details title="D5. Why no sigmoid or ReLU on the box output?" >}}

The targets are pixel values up to 224 and the spec said to keep the output "appropriate for the coordinate space". A sigmoid would need rescaling and saturate near the edges; a ReLU forbids negative intermediate values. A plain linear layer is the simplest option. The cost: nothing forces width and height to be positive or the box inside the image, so I would clamp the output at inference. <span style="color:#7c3aed"><strong>[Reasoned]</strong></span>

{{< /details >}}

{{< details title="D6. Did you freeze the encoder? Why?" >}}

Yes, for both localization and segmentation. Freezing keeps one identical backbone across the three tasks, so the unified model can load one encoder from the classifier checkpoint and pair it with any head. The price is that the backbone was optimised for breed recognition, not for geometry; fine-tuning (maybe with a small learning rate) would probably help each head but would give three different encoders and force an interference trade-off in the unified model. I did not claim that fine-tuning is worse; that is what the transfer-learning experiment in the report is for. <span style="color:#7c3aed"><strong>[Reasoned]</strong></span>

*Trap:* "Is the encoder really frozen?" Honest answer: its weights are, but its BatchNorm running statistics still update in `train()` mode, which I found when reviewing the code.

{{< /details >}}

{{< details title="D7. The grader uses mAP. What is the difference from IoU?" >}}

IoU measures how well one predicted box overlaps one ground-truth box. Average precision treats a prediction as correct if its IoU passes a threshold, ranks predictions by a confidence score, and integrates precision over recall; mAP averages over classes or thresholds. My localizer outputs a single box with **no confidence**, so how mAP is computed depends on the grader's convention, which I do not know; my in-repo metric is mean IoU only. <span style="color:#009b55"><strong>[Code]</strong></span>

{{< /details >}}

{{< details title="D8. Where would your box predictor fail?" >}}

The target is the **head**, not the body, so full-body shots with an unusual pose can mislead it; occlusion, very small pets (a cell of the 7×7 bottleneck covers 32×32 pixels) and cluttered backgrounds are the other obvious cases. Because the head is a linear map from a frozen classification feature, a high-confidence breed prediction can sit next to a poor box. <span style="color:#7c3aed"><strong>[Reasoned]</strong></span>

{{< /details >}}

## E. Segmentation

{{< details title="E1. Why a U-Net, and what do the skip connections do?" >}}

Pooling throws away exact spatial detail, so decoding only from the `7×7` bottleneck gives blurry masks. The skips feed the pre-pool feature maps of the encoder directly into the matching decoder stage by concatenation, so the decoder has both high-level context from below and sharp edges from the encoder. They also shorten the gradient path.

{{< /details >}}

{{< details title="E2. Why transposed convolutions, and why kernel 2 stride 2?" >}}

The assignment requires learnable upsampling instead of fixed interpolation. `ConvTranspose2d(kernel=2, stride=2)` exactly doubles height and width and, because kernel equals stride, each output pixel is covered by exactly one kernel position, so there is no overlap pattern that produces checkerboard artefacts. <span style="color:#7c3aed"><strong>[Reasoned]</strong></span>

{{< /details >}}

{{< details title="E3. Walk me through the channel counts in one decoder stage." >}}

Take stage 2: the previous output is `512×14×14`; the up-convolution takes it to `256×28×28`; I concatenate the encoder skip `s4` (`512×28×28`) giving `768` channels; two 3×3 convs take `768 → 512 → 256`. Stage 1 starts from the bottleneck (`512×7×7`) and `s5`; the last stage ends at `32×224×224` before a 1×1 conv produces 3 logits per pixel. <span style="color:#0071bc"><strong>[Measured]</strong></span>

{{< /details >}}

{{< details title="E4. Why cross-entropy for segmentation?" >}}

The three trimap classes (pet, background, boundary) are mutually exclusive, so each pixel is a 3-way classification and softmax cross-entropy is the natural, stable loss. Dice loss optimises overlap directly but has weak or noisy gradients when predictions are almost uniform, and binary cross-entropy would treat the classes as independent. The limitation: CE weights every pixel equally and the boundary class is thin and rare, so I would try a weighted CE or a CE + Dice combination. <span style="color:#7c3aed"><strong>[Reasoned]</strong></span>

{{< /details >}}

{{< details title="E5. Why is pixel accuracy misleading and Dice better?" >}}

Background pixels dominate, so predicting "background" everywhere gives a high pixel accuracy but a foreground Dice of zero. Dice per class is `2TP / (2TP + FP + FN)`, the harmonic mean of precision and recall, so it does not reward the majority class and it penalises both missed and spurious foreground. <span style="color:#7c3aed"><strong>[Reasoned]</strong></span>

{{< /details >}}

{{< details title="E6. How are the trimap labels handled?" >}}

The PNG stores 1 = pet, 2 = background, 3 = boundary. I subtract 1 to get class indices 0, 1, 2 for `CrossEntropyLoss`, and resize the mask with the image so labels stay integers. In the augmentation I found that rotation fills the mask with 0, which is the pet class after the shift; that is a small label-noise source I would fix with an ignore label. <span style="color:#0071bc"><strong>[Measured]</strong></span>

{{< /details >}}

## F. The unified model

{{< details title="F1. How does one forward pass produce three outputs?" >}}

The encoder runs once and returns the bottleneck and the skip maps. The flattened bottleneck feeds the classifier and the box head; the bottleneck plus the skips feed the decoder. The `forward` returns a dictionary with `classification`, `localization` and `segmentation`. <span style="color:#0071bc"><strong>[Measured]</strong></span> For a batch of 2 the shapes were `(2,37)`, `(2,4)`, `(2,3,224,224)`.

{{< /details >}}

{{< details title="F2. How do you assemble the model from three checkpoints?" >}}

I rebuild the same modules under the same names and load each checkpoint by key prefix: the encoder and classifier head from `classifier.pth`, `regression_head.*` from `localizer.pth`, and `up1…dec_block5, final_conv` from `unet.pth`. The checkpoints are dictionaries with `state_dict`, `epoch` and `best_metric`, and the loader accepts either that or a plain state dict. <span style="color:#009b55"><strong>[Code]</strong></span>

{{< /details >}}

{{< details title="F3. What are the risks of that design?" >}}

Names must match exactly, and the loader is lenient: a wrong prefix loads nothing without an error (I reproduced it), a missing file only prints a warning, and the encoder's BN statistics come from the classifier only. I would make the loader strict. The constructor also downloads the weights from Drive on every call and the model starts in train mode. <span style="color:#0071bc"><strong>[Measured]</strong></span>

{{< /details >}}

{{< details title="F4. Did the shared backbone suffer task interference?" >}}

I cannot give a measured answer: the heads were trained on a **frozen** classifier encoder, so there is no gradient interference by construction; instead the heads are limited by features optimised for classification. With joint fine-tuning, classification (invariance to position) and segmentation or localization (sensitivity to position) would pull the encoder in different directions. The report's reflection question (2.8) asks about exactly this. <span style="color:#7c3aed"><strong>[Reasoned]</strong></span>

{{< /details >}}

## G. Training and evaluation

{{< details title="G1. How did you train, and with what settings?" >}}

Adam with weight decay `1e-4`, `lr = 1e-3` and `StepLR` halving the rate every 10 epochs. Classification 80 epochs at batch 32 with dropout 0.3; localization 30 epochs at batch 32; segmentation 40 epochs at batch 16. For each task I kept the best epoch by its validation metric (macro-F1, IoU, Dice). The classifier is trained first because its encoder is the backbone for the others. <span style="color:#009b55"><strong>[Code]</strong></span>

{{< /details >}}

{{< details title="G2. What did you do about class imbalance?" >}}

A `WeightedRandomSampler` with inverse-frequency weights **and** a class-weighted cross-entropy. Doing both compensates twice; since the dataset is close to balanced I expect little effect either way, and I did not run an ablation, so I would not claim it helped. <span style="color:#009b55"><strong>[Code]</strong></span>

{{< /details >}}

{{< details title="G3. Why macro-F1 as the classification metric?" >}}

It is the grader's metric, and it averages the per-class F1 with equal weight, so rare classes count as much as common ones; accuracy would hide poor performance on small classes.

{{< /details >}}

{{< details title="G4. What was your final accuracy / F1 / Dice?" >}}

I do not carry those numbers in my head and I do not want to misquote them; they are in the public W&B report for the assignment. What I can speak to confidently is the design, the settings I trained with, and the checks that the architecture and the losses behave as specified. <span style="color:#f7921d"><strong>[Not recorded]</strong></span>

{{< /details >}}

{{< details title="G5. How do you know the code is correct?" >}}

Structurally: shapes through every block, parameter counts that add up exactly (encoder + heads = unified model), and the autograder's contract (names, shapes, dropout statistics, IoU values). Behaviourally: hand-computed IoU cases, a dropout statistics test, a loader run on all three tasks, and a code review that found real defects (BN statistics in the frozen encoder, silent partial loading, mask label noise). I could not re-verify accuracy offline because the trained weights are on Drive. <span style="color:#0071bc"><strong>[Measured]</strong></span>

{{< /details >}}

## H. Follow-up traps

{{< details title="H1. Did you use pretrained weights or torchvision's VGG?" >}}

No. The assignment forbade pre-built VGG models; I wrote the layers with `torch.nn`. The ImageNet mean and standard deviation are used only to normalise inputs, and everything is trained from scratch on the Pet data.

{{< /details >}}

{{< details title="H2. Is your `weight_decay` the same as AdamW?" >}}

No. `torch.optim.Adam(weight_decay=…)` adds the decay to the gradient (L2), which Adam then rescales; AdamW decouples the decay from the adaptive step. The assignment did not specify, and I did not compare. <span style="color:#7c3aed"><strong>[Reasoned]</strong></span>

{{< /details >}}

{{< details title="H3. What did the BatchNorm ablation show?" >}}

The assignment asked for a with/without-BN comparison of convergence and the maximum stable learning rate. The final code has no switch to turn BN off, so that experiment needs a modified copy of the model, and I do not carry the numbers; they are in the W&B report. The mechanism is the standard one: normalised inputs make the loss surface better conditioned, so larger learning rates stay stable.

{{< /details >}}

{{< details title="H4. Could the unified model run on a different image size?" >}}

Not the classifier and box heads: they depend on the `7×7` bottleneck through a fixed-size linear layer. The segmentation decoder alone is fully convolutional and would work on any size divisible by 32, but the unified model flattens the bottleneck, so it is fixed at 224×224. <span style="color:#009b55"><strong>[Code]</strong></span>

{{< /details >}}
