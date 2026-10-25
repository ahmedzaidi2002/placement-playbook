---
title: "1.5 · Results and discussion"
linkTitle: "1.5 Results and discussion"
weight: 5
math: true
---
## 1.5.i What worked {#s1-5-i}

- The from-scratch model trains cleanly and reaches $39.76$ validation BLEU in $37$ minutes on one T4, with every component written by hand.
- All three autograder-tested pieces (attention, positional encoding, Noam) follow the spec’s contracts exactly, and the logged learning rates match the closed form to every printed digit ([Section 1.3](../implementation/)).
- Choosing the checkpoint by validation BLEU instead of validation loss was right: the two disagree by eight epochs in the 30-epoch run.
- Two ablations give clear, well-above-noise answers: the $1/\sqrt{d_k}$ scaling is worth about $5$ BLEU, and learned positions cost about $2$.

## 1.5.ii What did not {#s1-5-ii}

- The 15-epoch budget never finished warm-up, so ablation 2.1 compared two learning-rate <em>sizes</em> rather than warm-up against no warm-up.
- Ablation 2.2 contradicted its own explanation: the gradients grew instead of vanishing, and the report text predicted the opposite of the data.
- Ablation 2.3’s heatmaps were dropped from the W&amp;B history and include padding.
- Label smoothing’s effect on BLEU is smaller than run-to-run noise, and without seeds or repeats no single comparison under about $1.5$ BLEU can be trusted.

## 1.5.iii Limitations {#s1-5-iii}

- <strong>The metric.</strong> BLEU is computed on lower-cased, tokenised text with `<unk>` in the references; against the real references the same model scores $36.96$ (lower-cased) or $31.33$ (cased) instead of $38.98$.
- <strong>The vocabulary.</strong> Word-level tokens with `min_freq` $=2$ leave $1.7\%$ of test reference words and $3.8\%$ of test source words unknown, and the model can never produce them. Sub-word units (BPE) are the standard fix but were outside the allowed tooling.
- <strong>Decoding.</strong> Greedy search, no beam, no length penalty.
- <strong>Scale.</strong> Half the paper’s width, half its depth, and a quarter of its FFN width, on $29$k sentences.
- <strong>Evidence.</strong> One run per ablation arm, no seeds.

## 1.5.iv Gotchas found in the code {#sec-a3-gotchas}

Each item has its evidence in the section cited.

1. The test BLEU logged at the end of every run is for the last epoch, not the saved best checkpoint (`train.py:427`); for `lm90eh07` the two differ by $1.55$ BLEU ([Section 1.3.xiv](../implementation/#sec-a3-checkpoints)).
2. References are rebuilt from ids, so `<unk>` matches for free, worth about $2$ BLEU ([Section What the BLEU numbers really measure](../implementation/#sec-a3-bleu-caveat)).
3. 15 epochs $= 3405 < 4000$ warm-up steps ([Section The warm-up trap](../experiments/#sec-a3-warmup-trap)).
4. The comment “base configuration from the paper” is wrong (`train.py:288`).
5. `wandb.log(..., step=epoch_num)` was silently ignored ([Section 1.4.vii](../experiments/#sec-a3-abl23)).
6. The attention heatmaps include $24$ padded rows ([Section 1.4.vii](../experiments/#sec-a3-abl23)).
7. A redundant final LayerNorm after Post-LN layers (`model.py:393, 428`).
8. Dropout on the attention output instead of the attention weights, so the attention path is dropped out twice (`model.py:168, 310`).
9. Label smoothing gives mass to the `<pad>` column, and its comment calls cross-entropy a KL divergence (`train.py:41-55`).
10. `infer()` returns lower-case tokenised text with `<unk>`, not detokenised English (`model.py:620-628`).
11. No random seeds anywhere; the same configuration varies by up to $2.5$ BLEU ([Section 1.4.iv](../experiments/#sec-a3-noise)).
12. `wandb_experiments.ipynb` is saved with `TEST_MODE = True` (2 epochs, batch 64), but the logged ablation runs are 15 epochs with batch 128: the file on disk is not the configuration that produced the results.
13. The working copy and the GitHub copy download different Google Drive files (`GDRIVE_FILE_ID`, `model.py:29`).
14. The checkpoint stores Adam’s state, tripling the autograder’s download ([Section 1.3.xiv](../implementation/#sec-a3-checkpoints)).
15. `non_pad_count.item()` forces a GPU sync every batch (`train.py:59`).

<div class="nb nb-moral">

If I did it again: seed everything, run each ablation arm three times, train long enough to leave warm-up, reload the best checkpoint before testing, score against the original references, and log images without a manual step.

</div>

## 1.5.v Environment {#s1-5-v}

The logged runs used Kaggle notebooks with Tesla T4 GPUs, Python 3.12.12, and (from the W&amp;B copy of `requirements.txt` for `r9ec0v3x`) `torch 2.10.0+cu128`, `spacy 3.8.11`, `sacrebleu 2.6.0`, `datasets 4.8.3`, `wandb 0.25.0`, `gdown 5.2.1`, `numpy 2.0.2`. The project’s `requirements.txt` lists the same packages without versions. Kaggle’s P100 GPUs do not work with that PyTorch build ([Section 1.4.ii](../experiments/#sec-a3-history)). My CPU re-evaluation used Python 3.13.7 and `torch 2.11.0+cpu`.

## 1.5.vi Commands {#s1-5-vi}

```python
# install (on Kaggle, keep the preinstalled GPU build of torch)
pip install -r requirements.txt
python -m spacy download de_core_news_sm
python -m spacy download en_core_web_sm
wandb login

# check the learning-rate schedule (plots the Noam curve)
python lr_scheduler.py

# main training run: logs to W&B project "da6401-a3",
# saves transformer_de_en.pt whenever validation BLEU improves
python train.py
```

`train.py` trains for $30$ epochs in the working copy and $15$ in the GitHub copy (`train.py:296`). On Kaggle, `train_kaggle.ipynb` does the same and also uploads the checkpoint as a W&amp;B artifact; it expects the four `.py` files as a Kaggle dataset named `da6401-a3-code` and a secret `WANDB_API_KEY`. The ablations are `wandb_experiments.ipynb` with `TEST_MODE = False`; its last cell builds the W&amp;B report.

Inference, as the autograder runs it (downloads the checkpoint from Google Drive if it is not in the current folder):

```python
from model import Transformer
model = Transformer()
model.eval()
print(model.infer("Leute Reparieren das Dach eines Hauses."))
# my run with the local checkpoint prints: people repair the roof of a house .
```

## 1.5.vii What to expect {#s1-5-vii}

- Runtime on one T4: about $19$ minutes for $15$ epochs, $37$ minutes for $30$ (W&amp;B runtimes $1087$–$1229$ s and $2227$ s), most of it in the per-epoch greedy BLEU evaluation. On a laptop CPU, evaluating test BLEU alone took $92$ s.
- Results: validation BLEU $38.3 \pm 0.6$ at best within $15$ epochs, and about $39$–$40$ within $30$. Without seeds, individual runs will not match these to the digit.

Paths are relative to `sem~2/dl/assignment~3/`.

| File | Purpose |
|:--|:--|
| `DA6401_Assignment_3_2026.pdf` | the problem statement (3 pages) |
| `attention is all you need.pdf` | the paper |
| `SKILL.md` | the course announcement about `infer()` and the autograder, followed by a coding-style guide written for an AI assistant |
| `context.txt` | a concatenation of the README, requirements, `SKILL.md` and the four `.py` files (made on 15 Aug 2026) |
| `da6401_assignment_3-main.zip` | the official skeleton: signatures and docstrings only |
| `transformer_de_en.pt` | local checkpoint: best epoch (14) of `lm90eh07`, 113.5 MB |
| `links/New Text Document.txt` | empty |
| `.claude/settings.local.json` | Claude Code permissions for this folder |
| `da6401_assignment_3-main/` | <strong>working copy</strong>, the version documented here |
| `model.py` | attention, masks, PE, FFN, layers, stacks, `Transformer`, `infer` |
| `train.py` | label-smoothing loss, epoch loop, greedy decoding, BLEU, checkpoints, main experiment |
| `dataset.py` | `Vocab` and `Multi30kDataset` |
| `lr_scheduler.py` | `NoamScheduler` and the plotting helper |
| `train_kaggle.ipynb` | 30-epoch Kaggle training and artifact upload (`r9ec0v3x`) |
| `wandb_experiments.ipynb` | the nine ablation runs and report generation |
| `README.md`, `requirements.txt` | course README; dependency list |
| `wandb/` | the two failed local runs of 9 May |
| `da6401_assignment_3-temp/` | snapshots |
| `da6401_assignment_3-main.zip`, `da6401_assignment_3-main/` | code as of 14 May 17:16 IST; identical to GitHub |
| `da6401_assignment_3/da6401_assignment_3-main/` | clone of the GitHub repository (3 commits, 19 May); differs from the working copy only in `GDRIVE_FILE_ID` and `num_epochs` |

- <strong>Attention</strong>: a weighted average of value vectors, with weights from a softmax of query–key scores.
- <strong>Head</strong>: one of $h$ parallel attention computations of width $d_k = d_{\text{model}}/h$.
- <strong>Memory</strong>: the encoder’s output, which every decoder layer attends to.
- <strong>Teacher forcing</strong>: training the decoder on the true previous words.
- <strong>Causal mask</strong>: hides future positions from decoder self-attention.
- <strong>Padding mask</strong>: hides `<pad>` positions.
- <strong>Post-LN / Pre-LN</strong>: LayerNorm after vs before each residual sub-layer.
- <strong>Label smoothing</strong>: training against a target with $\varepsilon$ of its mass spread over other words.
- <strong>Noam schedule</strong>: linear warm-up to step $w$, then decay as $s^{-1/2}$.
- <strong>Greedy decoding</strong>: pick the most probable word at every step. <strong>Beam search</strong> keeps the $k$ best prefixes instead.
- <strong>BLEU</strong>: geometric mean of $1$- to $4$-gram precisions times a brevity penalty. <strong>SacreBLEU</strong>: a standardised BLEU implementation that expects detokenised text.
- <strong>Detokenisation</strong>: turning “house .” back into “house.”.
- <strong>OOV</strong>: out of vocabulary, mapped to `<unk>`.
- <strong>Perplexity</strong>: $e^{\text{loss}}$, the effective number of equally likely choices.
- <strong>Token accuracy</strong>: fraction of non-pad positions where the argmax is the gold word, under teacher forcing.
- <strong>Prediction confidence</strong>: mean probability given to the gold word.
- <strong>Attention rollout</strong>: combining attention across all layers, including the residual path.
- <strong>Head redundancy</strong>: several heads computing nearly the same attention.
- <strong>Buffer</strong>: a tensor saved with a module but not trained.
- <strong>Xavier initialisation</strong>: uniform weights with variance $2/(\text{fan-in} + \text{fan-out})$.
- <strong>W&amp;B run / artifact / report</strong>: one logged experiment / a versioned file such as a checkpoint / a shareable page of plots and text.

Everything marked UNKNOWN in this chapter, in one place.

1. The marks awarded, and the hidden-test BLEU of the submitted model.
2. Which checkpoint each `GDRIVE_FILE_ID` points to. File times suggest that the GitHub copy’s id (edited 14 May, 11:46 UTC, five minutes after the 30-epoch artifact was uploaded) is the 30-epoch checkpoint, and the working copy’s id (edited 10:29 UTC) the 15-epoch one; this is an inference, not verified.
3. Whether the W&amp;B report was edited after it was generated (it was last updated on 19 May), and in particular whether it contains the required Pre/Post-LN justification.
4. Whether the report’s attention-head panel displays any images.
5. The test BLEU of the epoch-22 checkpoint of `r9ec0v3x`.
6. Why `c7d0z5g9`, `ru9dp751` and `e56jo7r4` stopped.
7. The submission deadline.
8. Whether `sacrebleu` counts as the permitted `bleu` library.
9. Why the model was shrunk from the paper’s base size.

<div class="nb nb-problem nb-block" id="problem-1a">

<strong>Problem 1A</strong>

Count the parameters of one decoder layer with $d_{\text{model}} = 256$ and $d_{\text{ff}} = 512$, and check your answer against $790{,}784$.

<details class="nb-hint">
<summary>Hint</summary>

Two attention blocks, one FFN, three LayerNorms; every `nn.Linear` has a bias.

</details>

<details class="nb-sol">
<summary>Solution</summary>

One attention block has four $256 \times 256$ linears with biases: $4(65536 + 256) = 263{,}168$. The FFN has $256 \cdot 512 + 512 + 512 \cdot 256 + 256 = 262{,}912$. Three LayerNorms have $3 \cdot 512 = 1536$. Total $2 \cdot 263168 + 262912 + 1536 = 790{,}784$.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-1b">

<strong>Problem 1B</strong>

With batch size $128$ on $29{,}000$ sentences and $w = 4000$, after how many epochs does warm-up end? What is the learning rate at the end of epoch 15? Suggest two ways to make a 15-epoch budget reach the decay phase.

<details class="nb-hint">
<summary>Hint</summary>

$\lceil 29000/128 \rceil = 227$ updates per epoch.

</details>

<details class="nb-sol">
<summary>Solution</summary>

$4000/227 \approx 17.6$ epochs. After $15 \cdot 227 = 3405$ updates the optimiser holds $\eta(3406) = 256^{-1/2} \cdot 3406 \cdot 4000^{-3/2} \approx 8.41 \times 10^{-4}$. Either shorten the warm-up (for example $w = 1000$, about four epochs) or use a smaller batch, which gives more updates per epoch; the first keeps the epoch time unchanged.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-1c">

<strong>Problem 1C</strong>

Show that $\operatorname{PE}_{pos} \cdot \operatorname{PE}_{pos+k}$ depends only on $k$, not on $pos$.

<details class="nb-hint">
<summary>Hint</summary>

$\sin a \sin b + \cos a \cos b$.

</details>

<details class="nb-sol">
<summary>Solution</summary>

Each frequency pair contributes $\sin(\omega \, pos)\sin(\omega(pos+k)) + \cos(\omega \, pos)\cos(\omega(pos+k)) = \cos(\omega k)$, so the dot product is $\sum_i \cos(\omega_i k)$.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-1d">

<strong>Problem 1D</strong> 🌶

Show that the logits minimising the smoothed loss make the gold word’s logit exceed every other logit by $\log \frac{(1-\varepsilon)(V-1)}{\varepsilon}$, and evaluate it for this model.

<details class="nb-hint">
<summary>Hint</summary>

The minimiser is $\bm{p} = \bm{q}'$; the log-ratio of two softmax probabilities is the difference of their logits.

</details>

<details class="nb-sol">
<summary>Solution</summary>

At the optimum $p_y / p_k = (1-\varepsilon) / (\varepsilon/(V-1))$ for every $k \neq y$, and $\log(p_y/p_k) = z_y - z_k$. With $V = 5893$ and $\varepsilon = 0.1$ this is $\log(0.9 \cdot 5892 / 0.1) = \log 53028 \approx 10.88$.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-1e">

<strong>Problem 1E</strong>

Explain why building BLEU references from token ids inflates the score, and give a fix that keeps the rest of `evaluate_bleu` unchanged.

<details class="nb-hint">
<summary>Hint</summary>

What does the reference look like for a sentence with a rare word?

</details>

<details class="nb-sol">
<summary>Solution</summary>

Every rare reference word becomes `<unk>`, and a hypothesis that also outputs `<unk>` gets unigram (and possibly longer) matches it did not earn. Keep the raw English sentences next to the ids in the dataset and pass them to `corpus_score` as references, ideally after detokenising the hypotheses too. On the local checkpoint this changes $38.98$ to $36.96$.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-1f">

<strong>Problem 1F</strong> 🌶

Let $\operatorname{LayerNorm}_0$ be LayerNorm with $\bm \gamma = \bm 1$, $\bm \beta = \bm 0$ and $\varepsilon = 0$. Show that $\operatorname{LayerNorm}_0(\operatorname{LayerNorm}_0(\bm{x})) = \operatorname{LayerNorm}_0(\bm{x})$. What does a second LayerNorm with learned $\bm \gamma', \bm \beta'$ do to the output of a layer that already ends in $\operatorname{LayerNorm}$ with $\bm \gamma, \bm \beta$?

<details class="nb-hint">
<summary>Hint</summary>

The output of $\operatorname{LayerNorm}_0$ already has mean $0$ and variance $1$.

</details>

<details class="nb-sol">
<summary>Solution</summary>

$\operatorname{LayerNorm}_0(\bm{x})$ has mean $0$ and variance $1$, so normalising it again changes nothing. With learned parameters, the second norm re-centres and re-scales the vector $\bm \gamma \odot \bm{z} + \bm \beta$ and then applies $\bm \gamma', \bm \beta'$. When $\bm \gamma$ and $\bm \beta$ are the same for every feature (as at initialisation, $\bm \gamma = \bm 1$, $\bm \beta = \bm 0$) it simply replaces them: the output is $\bm \gamma' \odot \bm{z} + \bm \beta'$. It adds $512$ parameters and little expressive power, which is why the final norm is only needed in Pre-LN.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-1g">

<strong>Problem 1G</strong>

After every epoch the notebook calls `wandb.log(metrics)`, then logs the heatmap image with a second `wandb.log` call that passes `step=epoch`. Why is the image dropped, and what are two fixes?

<details class="nb-hint">
<summary>Hint</summary>

What is W&amp;B’s internal step after the first call?

</details>

<details class="nb-sol">
<summary>Solution</summary>

Each `wandb.log` without `step` advances the internal step by one, so after the metrics of epoch $e$ it is already $e+1$, and logging to step $e$ goes backwards, which W&amp;B ignores. Fix: log the image in the same call as the metrics, or log it without `step` (optionally with `epoch` as a field and `wandb.define_metric` to plot against it).

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-1h">

<strong>Problem 1H</strong> 🌶🌶

Design an experiment that actually answers ablation 2.1’s question, “why is the Transformer sensitive to the initial learning rate, and how does warm-up prevent early divergence?”, within a budget of about $3$ GPU-hours.

<details class="nb-hint">
<summary>Hint</summary>

The comparison needs the same peak rate with and without warm-up, and repeats.

</details>

<details class="nb-sol">
<summary>Solution</summary>

Compare, for $3$ seeds each: (a) Noam with $w = 1000$; (b) a constant rate equal to (a)’s peak, $(256 \cdot 1000)^{-1/2} \approx 2 \times 10^{-3}$, with no warm-up; (c) the same constant rate with a linear warm-up of $1000$ steps. Log per-step training loss, the global gradient norm before clipping and the maximum attention weight over the first $2000$ updates. Divergence or loss spikes in (b) but not (a) or (c) isolate warm-up as the cause. Six 15-epoch runs at about $19$ minutes each fit the budget; drop to $10$ epochs to afford all nine.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-1i">

<strong>Problem 1I</strong>

The local checkpoint file is $113{,}502{,}467$ bytes for $8{,}988{,}165$ parameters. Account for the size, and say what the autograder actually needs.

<details class="nb-hint">
<summary>Hint</summary>

What else does `save_checkpoint` store, and how big is Adam’s state?

</details>

<details class="nb-sol">
<summary>Solution</summary>

Parameters in float32: $35.95$ MB. Adam keeps two tensors of the same shape: $71.91$ MB. The sinusoidal buffer: $5.12$ MB. Vocabularies and pickle overhead: the remaining $0.52$ MB. The autograder only needs the model weights and the vocabularies, about $42$ MB (and the buffer could even be recomputed).

</details>

</div>
