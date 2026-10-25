---
title: "10 · Generative and representation learning"
linkTitle: "10 Generative models"
weight: 10
math: true
---
Discriminative models learn $p(y \mid x)$. Generative models learn $p(x)$ well enough to sample from it; representation learning learns features without labels. Interviews ask for the VAE objective and the reparameterisation trick, the GAN game and its failure modes, the idea of diffusion, and how contrastive learning, word2vec and Vision Transformers produce representations.

## 10.1 Autoencoders {#dl-10-1}

An autoencoder maps $x$ to a low-dimensional code $z$ and back, trained to minimise reconstruction error. The **bottleneck** forces it to keep what matters. With linear layers and squared error it learns exactly the **PCA** subspace; non-linear autoencoders generalise PCA to curved manifolds. Variants: **denoising** (reconstruct $x$ from a corrupted input, learning robust features) and **sparse** autoencoders.

A plain autoencoder is **not a good generator**: nothing makes the code space dense, so decoding a random $z$ usually gives garbage. The VAE fixes this.

## 10.2 Variational autoencoders {#dl-10-2}

Latent $z \sim \mathcal N(0, I)$, a decoder $p_\theta(x \mid z)$, and an encoder $q_\phi(z \mid x) = \mathcal N(\mu(x), \sigma^2(x))$ approximating the intractable posterior. The VAE maximises the **evidence lower bound (ELBO)**:

$$\log p(x) \ \ge\ \underbrace{\mathbb E_{q}\big[\log p_\theta(x \mid z)\big]}_{\text{reconstruction}} - \underbrace{\text{KL}\big(q_\phi(z \mid x)\,\|\,\mathcal N(0, I)\big)}_{\text{keeps the latent space smooth and samplable}}.$$

For diagonal Gaussians the KL has a closed form per dimension, $\tfrac12(\mu^2 + \sigma^2 - 1 - \log\sigma^2)$: 0 at $\mu = 0, \sigma = 1$; 0.818 at $\mu = 1, \sigma = 0.5$. Networks output $\log\sigma^2$ so the variance needs no constraint.

**The reparameterisation trick:** sampling $z \sim \mathcal N(\mu, \sigma^2)$ is not differentiable in $\mu, \sigma$. Write $z = \mu + \sigma \odot \varepsilon$ with $\varepsilon \sim \mathcal N(0, I)$: the randomness moves into an input, $z$ becomes a deterministic, differentiable function of $(\mu, \sigma)$, and ordinary backprop gives low-variance gradients.

<div class="nb nb-remark">

<strong>Trap</strong> — "The KL term makes VAE reconstructions sharp." It does the opposite: it trades reconstruction quality for a well-behaved latent space, and Gaussian decoders average plausible outputs, so VAE samples tend to be **blurry**. If the KL term wins completely, the decoder ignores $z$ (**posterior collapse**); weighting it ($\beta$-VAE) trades the two.

</div>

## 10.3 Generative adversarial networks {#dl-10-3}

A **generator** $G(z)$ plays against a **discriminator** $D(x) \in (0, 1)$:

$$\min_G \max_D\ \ \mathbb E_{x \sim p_{\text{data}}}\log D(x) + \mathbb E_{z}\log\big(1 - D(G(z))\big).$$

For a fixed generator the best discriminator is $D^\star(x) = \dfrac{p_{\text{data}}(x)}{p_{\text{data}}(x) + p_g(x)}$, and the generator then minimises a **Jensen–Shannon divergence**, zero exactly when $p_g = p_{\text{data}}$. A discriminator outputting 0.5 everywhere means the generator has matched the data.

In practice $G$ maximises $\log D(G(z))$ (the **non-saturating** loss), because early on $D$ rejects fakes easily and $\log(1 - D(G(z)))$ has almost no gradient. **Failure modes:** **mode collapse** (the generator covers a few modes that fool $D$), oscillation instead of convergence, vanishing generator gradients when $D$ is too good. **WGAN** uses a Wasserstein-distance critic with a Lipschitz constraint (gradient penalty), giving a smoother loss that tracks sample quality.

## 10.4 Diffusion models {#dl-10-4}

A fixed **forward process** adds Gaussian noise in $T$ small steps; a network learns to **reverse** it. Composing Gaussians gives any step in one shot:

$$x_t = \sqrt{\bar\alpha_t}\,x_0 + \sqrt{1 - \bar\alpha_t}\,\varepsilon, \qquad \bar\alpha_t = \prod_{s \le t}(1 - \beta_s).$$

**Training:** pick a random step, noise a clean example in one shot, and **regress the noise**: $\|\varepsilon - \varepsilon_\theta(x_t, t)\|^2$. **Sampling:** start from pure noise and apply the learned denoising step $T$ times (faster samplers skip steps). Compared with GANs: stable training and good mode coverage, at the price of many network evaluations per sample. Text-to-image systems condition on a text embedding and often run diffusion in an autoencoder's latent space.

**Normalising flows**, in one line: compose invertible maps with tractable Jacobian determinants, so the exact likelihood is available; architectures must be invertible.

## 10.5 Representation learning without labels {#dl-10-5}

**Contrastive learning** pulls representations of **positive pairs** together and pushes all other pairs apart. **SimCLR** makes positives from two random augmentations of one image; **CLIP** pairs an image with its caption. With normalised embeddings and a temperature $\tau$, the **InfoNCE** loss is a cross-entropy over the batch's similarity matrix with the matching pair on the diagonal. Larger batches mean more negatives and a harder, more informative task. CLIP's joint space gives **zero-shot classification**: embed "a photo of a {class}" for each class and pick the nearest. What the augmentations leave unchanged is what the representation learns to ignore.

**word2vec (skip-gram)** learns word vectors by predicting context words from a centre word; **negative sampling** replaces the full softmax over the vocabulary with $1 + k$ binary classifications (the true context word against $k$ noise words). Words in similar contexts get similar vectors. Unlike Transformer embeddings these are **static**: one vector per word regardless of context.

**Vision Transformers (ViT):** cut an image into $P\times P$ patches, project each linearly (a convolution with kernel and stride $P$), add position embeddings and a `[CLS]` token, and run a standard Transformer encoder. A $224\times224$ image with $P = 16$ gives **196** patch tokens; halving $P$ to 8 gives 784 tokens and about 16× the attention cost. ViTs have weaker built-in priors than CNNs (no locality or translation equivariance by construction), so they need more data or stronger augmentation, and scale very well when they get it.

<div class="nb nb-moral">

VAE: maximise reconstruction minus KL and backpropagate through $\mu + \sigma\odot\varepsilon$. GAN: a two-player game whose optimum matches the data distribution, hard to balance. Diffusion: learn to predict the noise. Contrastive learning: classify which pair belongs together.

</div>
