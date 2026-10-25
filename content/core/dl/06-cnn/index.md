---
title: "6 · Convolutional networks"
linkTitle: "6 CNNs"
weight: 6
math: true
---
Placement OAs spend most of their deep-learning numerics here: output shapes with padding and stride, parameter counts, "which layer reduces spatial size", "why does a CNN have fewer parameters than a fully connected network". This chapter gives one formula for each, then the architectures an interviewer expects you to know by their key idea, and then your own VGG11 / U-Net project in that vocabulary.

## 6.1 Why convolution {#dl-6-1}

Images have three properties a fully connected layer ignores:

- **Locality:** nearby pixels are related, so each output looks at a small neighbourhood (its **receptive field**): sparse connectivity.
- **Stationarity:** an edge detector useful in one corner is useful everywhere, so the same weights are used at every position: **weight sharing**.
- **Translation:** shifting the input shifts the feature map (**equivariance**); pooling adds a little **invariance**.

<div class="nb nb-example">

<strong>Example</strong> (Weight sharing in numbers)

From a $32\times32\times3$ image to a $32\times32\times16$ map: a $3\times3$ convolution needs $(3\cdot3\cdot3 + 1)\cdot 16 = 448$ parameters; a fully connected layer producing the same 16,384 outputs needs about 50 million. A convolution's count does not depend on the image size at all.

</div>

<div class="nb nb-remark">

<strong>Trap</strong> — "Why fewer parameters than a dense layer?" **Weight sharing plus local connectivity**, not pooling (no parameters) and not ReLU. And fewer parameters is not less computation: the shared kernel is applied at every position, so convolutions are cheap in parameters but expensive in multiply–adds.

</div>

## 6.2 The operation {#dl-6-2}

What every library calls convolution is **cross-correlation**: slide the kernel and take elementwise products and sums, with no flip. (True convolution flips the kernel; since the kernel is learned, the network simply learns the flipped one.) A layer maps $C_{\text{in}}$ channels to $C_{\text{out}}$: each output channel has its own $C_{\text{in}} \times k \times k$ kernel spanning all input channels, plus one bias. PyTorch stores the weight as $(C_{\text{out}}, C_{\text{in}}, k, k)$.

## 6.3 Output shapes, parameters, cost {#dl-6-3}

<div class="nb nb-theorem nb-block">

<strong>The three formulas</strong>

$$n_{\text{out}} = \left\lfloor \frac{n + 2p - d(k-1) - 1}{s} \right\rfloor + 1 \qquad \text{params} = (k^2 C_{\text{in}} + 1)\,C_{\text{out}} \qquad \text{MACs} = k^2 C_{\text{in}} C_{\text{out}} H_{\text{out}} W_{\text{out}}$$

with input size $n$, kernel $k$, stride $s$, padding $p$ on each side, dilation $d$ (usually 1, giving $\lfloor (n + 2p - k)/s\rfloor + 1$). The same size formula holds for pooling windows. "Same" padding for odd $k$ and stride 1 is $p = (k-1)/2$.

</div>

<div class="nb nb-example">

<strong>Example</strong> (The OA layer)

$32\times32\times3$ input, ten $5\times5$ filters, stride 1, no padding: $n_{\text{out}} = 32 - 5 + 1 = 28$, output $28\times28\times10$, parameters $(25\cdot3 + 1)\cdot10 = 760$, and $5\cdot5\cdot3\cdot10\cdot28\cdot28 = 588{,}000$ multiply–adds. AlexNet's first layer, $227$ in, $k = 11$, $s = 4$: $\lfloor 216/4\rfloor + 1 = 55$. A ResNet stem, $224$, $k = 7$, $s = 2$, $p = 3$: $\lfloor 223/2\rfloor + 1 = 112$.

</div>

<div class="nb nb-remark">

<strong>Trap</strong> — Three ways to get these wrong: forgetting the floor, applying padding once instead of on both sides, using $k$ instead of $d(k-1) + 1$ for a dilated kernel. The output's channel count is the **number of filters**, never the input channel count. "FLOPs" sometimes means MACs and sometimes 2 × MACs: say which.

</div>

The pattern of a CNN: **spatial size shrinks, channels grow**; the parameters concentrate in the late, wide layers, the computation in the early, high-resolution ones.

## 6.4 Receptive field, pooling, 1×1 and depthwise convolutions {#dl-6-4}

**Receptive field:** two stacked $3\times3$ convolutions see a $5\times5$ patch with $18C^2$ weights (one $5\times5$ needs $25C^2$); three see $7\times7$ with $27C^2$ instead of $49C^2$, and add two extra non-linearities. **That is the VGG argument.** Strides and pooling grow the receptive field geometrically; dilation grows it without losing resolution (segmentation). The *effective* receptive field is smaller than the theoretical one: the gradient concentrates near the centre.

**Pooling:** max-pooling outputs each window's maximum, average-pooling the mean; $2\times2$ with stride 2 halves height and width, has **zero parameters**, and max-pooling sends the gradient only to each window's winner. **Global average pooling** averages each channel over the whole map, giving one number per channel and letting the network accept any input size.

<div class="nb nb-remark">

<strong>Trap</strong> — "Which layer reduces spatial size?" Pooling with stride > 1, or a convolution with stride > 1 (or without padding). Not ReLU, not BatchNorm, not dropout, and not a $1\times1$ convolution with stride 1, which changes only the channel count.

</div>

- **$1\times1$ convolution:** a fully connected layer applied at every pixel, mixing channels: $C_{\text{in}}C_{\text{out}} + C_{\text{out}}$ parameters. Used as a **bottleneck** before an expensive $3\times3$ (a ResNet bottleneck $256 \to 64 \to 64 \to 256$ has about 70k weights against 1.18M for two $3\times3$ layers at width 256).
- **Depthwise-separable** (MobileNet): one $k\times k$ filter per input channel, then a $1\times1$ to mix channels. Cost ratio $1/C_{\text{out}} + 1/k^2$, about 0.12 for $3\times3$ at 256 channels.
- **Transposed convolution** upsamples: each input value scatters a scaled copy of the kernel into the output. Output size $(n - 1)s - 2p + k$; $k = s = 2$ doubles 16 to 32. It is literally the backward pass of a convolution with respect to its input. When $k$ is not divisible by $s$ the overlaps are uneven and cause **checkerboard artefacts**.

## 6.5 Architectures worth knowing {#dl-6-5}

| Architecture | Key idea |
|---|---|
| LeNet (1990s) | conv–pool–conv–pool–FC, the template |
| AlexNet (2012) | a big LeNet on GPUs with ReLU, dropout, augmentation; started the deep-learning era |
| **VGG** | only $3\times3$ convolutions in stages separated by $2\times2$ max-pools. VGG-16: 138M parameters, **89% in the FC head** (the first FC layer, $7\cdot7\cdot512 \to 4096$, alone has 103M) |
| Inception | parallel $1\times1$, $3\times3$, $5\times5$ and pooling branches, $1\times1$ bottlenecks |
| **ResNet** | residual blocks $h + F(h)$; ResNet-18 has 11.7M parameters |
| DenseNet | each layer gets all previous feature maps in its block |
| MobileNet | depthwise-separable convolutions for phones |
| EfficientNet | scale depth, width and resolution together |

**ResNet and the degradation problem.** Adding layers to a plain network beyond a point makes **training** error worse. That is not overfitting (overfitting lowers training error); it is an **optimisation** failure: a deeper net could copy the shallower one and set extra layers to the identity, yet gradient descent does not find it. A residual block computes $h + F(h)$, so the identity is the default ($F = 0$ is easy), and $\partial h_{l+1}/\partial h_l = I + \partial F/\partial h_l$ always contains the identity path, so gradients reach early layers undiminished. When shapes change, the shortcut is a $1\times1$ convolution with stride 2.

<div class="nb nb-remark">

<strong>Trap</strong> — "ResNet solves overfitting" or "works because it has more parameters". The identity shortcut adds **no** parameters and fixes an optimisation problem. If a plain 56-layer net has higher *training* error than a 20-layer one, adding dropout is the wrong fix.

</div>

## 6.6 Transfer learning and fine-tuning {#dl-6-6}

Early layers learn edges and textures, middle layers parts, late layers task-specific concepts, so features transfer.

- **Feature extraction:** freeze the pretrained backbone and train only a new head. Fast, needs little data.
- **Fine-tuning:** start from the pretrained weights and keep training some or all layers, with a learning rate 10–100× smaller.

Small dataset, similar to the pretraining data → feature extraction; large dataset → fine-tune most or all layers. Preprocess exactly as in pretraining (same normalisation, resolution), and keep frozen BatchNorm layers in `eval()` mode.

<div class="nb nb-remark">

<strong>Trap</strong> — "Fine-tuning means training only the last layer." That is feature extraction (linear probing). Fine-tuning updates pretrained weights.

</div>

## 6.7 Detection and segmentation {#dl-6-7}

**IoU** (intersection over union) $= |A \cap B| / |A \cup B|$. Boxes $(0, 0, 10, 10)$ and $(5, 0, 15, 10)$ overlap in 50 of $100 + 100 - 50 = 150$: IoU $= 0.333$. A detection counts as correct if IoU with a ground-truth box exceeds a threshold (often 0.5); **mAP** averages the area under precision–recall curves over classes.

**Non-maximum suppression:** detectors propose many overlapping boxes per object; keep the highest-scoring one and delete others overlapping it beyond a threshold.

- **Two-stage** (R-CNN → Fast → Faster R-CNN): propose regions (Faster R-CNN learns them with a region proposal network over **anchors**), then classify and refine each.
- **One-stage** (YOLO, SSD, RetinaNet): predict classes and box offsets densely in one pass; faster; focal loss handles the extreme background imbalance.
- **Semantic segmentation** labels every pixel. **U-Net** is an encoder–decoder whose **skip connections concatenate** high-resolution encoder features into the decoder to recover fine boundaries. **Instance segmentation** (Mask R-CNN) adds a mask per detected box.

## 6.8 In my project: VGG11, U-Net and a multi-task model {#dl-6-8}

<div class="nb nb-remark">

<strong>In my project</strong> — [DA6401 Assignment 2](../../../projects/vgg11/): **VGG11 built from scratch** in PyTorch with BatchNorm and a hand-written dropout, trained with **no pretrained weights** on Oxford-IIIT Pet ($3\times224\times224$ inputs), reused as one shared encoder for three tasks.

</div>

**The encoder.** 8 convolution layers in 5 blocks (each conv → BatchNorm → ReLU), each block ending in a $2\times2$ max-pool, so $224 \to 112 \to 56 \to 28 \to 14 \to 7$ and the output is $512\times7\times7$ (25,088 numbers). All convolutions are $3\times3$ with padding 1, so only the pools change spatial size. The encoder has 9.23M parameters.

**The three heads, and the vocabulary to describe them:**

| Head | Shape | Loss | Metric |
|---|---|---|---|
| Breed classifier (37 classes) | $25088 \to 4096 \to 4096 \to 37$, BN1d + ReLU + custom dropout after the first two | class-weighted cross-entropy | macro-F1 |
| Box localiser | $25088 \to 4096 \to 1024 \to 4$, outputs $(x_c, y_c, w, h)$ in pixels | MSE + IoU loss | mean IoU |
| Segmentation (3-class trimap) | U-Net decoder: 5 × (transposed conv ×2 → concatenate skip → 2 convs), then a $1\times1$ conv to 3 classes | pixel-wise cross-entropy | mean Dice |

Model sizes: classifier 128.9M (almost all in the FC head, exactly the VGG imbalance above), U-Net 24.3M, unified model 251.0M.

Things an interviewer can push on, with short answers:

- **Why transposed convolutions?** The assignment required learnable upsampling (no bilinear or unpooling). Each doubles the size: $7 \to 14 \to \dots \to 224$.
- **Where do the skips come from?** The block outputs **before** each max-pool, so the deepest skip is $512\times14\times14$, matching the upsampled bottleneck; concatenation (not addition) keeps both sets of features.
- **Why an IoU loss on top of MSE?** MSE on raw pixel coordinates treats a 10-pixel error the same for a tiny and a huge box; IoU is scale-invariant and measures what the metric measures. Caveats found in the project: MSE on raw pixels starts in the thousands while the IoU term is at most 1, so MSE dominates early; and an IoU loss has **zero gradient when the boxes do not overlap**.
- **Why Dice, not pixel accuracy?** Background pixels dominate a trimap, so "background everywhere" already scores high pixel accuracy with a foreground Dice near 0. Dice $= 2TP/(2TP + FP + FN)$ is the harmonic mean of precision and recall per class.
- **Why class-weighted cross-entropy?** To stop frequent breeds dominating; a side effect is that the logged validation loss is not comparable to an unweighted one.
- **The unified model** loads the three trained checkpoints onto **one shared encoder** and runs all three heads in one forward pass.

The final scores are only in the W&B report, not in any local file: read them from there before quoting a number.

<div class="nb nb-moral">

Shapes: $\lfloor (n + 2p - k)/s\rfloor + 1$. Parameters: $(k^2 C_{\text{in}} + 1)C_{\text{out}}$. Weight sharing explains the small counts; stride and pooling shrink space; residual shortcuts make depth trainable; skips and transposed convolutions bring resolution back for segmentation.

</div>
