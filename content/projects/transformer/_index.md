---
title: "Transformer"
weight: 2
sidebar:
  open: false
---

This book documents Assignment 3 of the DA6401 Deep Learning course: a Transformer implemented from scratch in PyTorch for German-to-English translation, the theory behind every component, the experiments and ablations, and the questions an interviewer is likely to ask. Code is quoted from the project with its location, written like `model.py:40`, which means line 40 of `model.py`.

Three kinds of evidence are used, and every number in this chapter comes from one of them.

- <strong>Code.</strong> Locations like `model.py:40` are relative to the working copy `sem~2/dl/assignment~3/` `da6401_assignment_3-main/`. A snapshot of its four Python files is kept in `data/a3/src/` of these notes, and every code listing below is read from that snapshot, so the line numbers are real.
- <strong>Weights &amp; Biases.</strong> Run ids like `r9ec0v3x` refer to the W&amp;B project `da6401-a3` (under my institute W&amp;B account), read through the W&amp;B API on 29 September 2026. All plots in [Section 1.4](experiments/) are drawn from that export.
- <strong>My own re-evaluation.</strong> On 29 September 2026 I re-ran the saved local checkpoint on the test set and recomputed attention maps, on CPU, with the project’s own code. These results are labelled as such.

Anything that could not be established is marked <strong>UNKNOWN</strong> and listed in [Section 1.5](wrapup/).

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> translating <em>“Leute Reparieren das Dach eines Hauses.”</em> into <em>“people repair the roof of a house .”</em>, which is what the trained model actually outputs for the fifth test sentence.</em>

</div>

The assignment is to implement the Transformer of [&#91;Vas+17&#93;](references/#ref-vaswani2017) from scratch in PyTorch and use it for German$\to$English <strong>neural machine translation</strong> on the Multi30k dataset [&#91;Ell+16&#93;](references/#ref-elliott2016): about $29$ thousand short image captions, each written in both languages. “From scratch” is meant literally: `nn.MultiheadAttention` is not allowed, so attention, masking, positional encodings, the encoder–decoder stacks, the label-smoothed loss, the Noam learning-rate schedule and greedy decoding are all my own code. The second half of the assignment is a public W&amp;B report with five ablation studies.

What I built is a $3$-layer encoder–decoder Transformer with $d_{\text{model}} = 256$, $8$ heads and $d_{\text{ff}} = 512$: $8{,}988{,}165$ trainable parameters. It was trained on Kaggle (Tesla T4 GPUs) with Adam, the Noam schedule and label smoothing $\varepsilon = 0.1$, and evaluated with corpus BLEU from SacreBLEU [&#91;Pos18&#93;](references/#ref-post2018) on greedy-decoded output.

<div class="nb nb-moral">

Best validation BLEU: $39.76$ (30-epoch run `r9ec0v3x`, epoch 22). Six runs of the same 15-epoch configuration gave test BLEU $38.03 \pm 0.73$. Removing the $1/\sqrt{d_k}$ scaling cost about $5$ BLEU and learned positional embeddings about $2$; label smoothing made no difference beyond run-to-run noise.

</div>

Those BLEU numbers come with an important caveat, explained in [Section What the BLEU numbers really measure](implementation/#sec-a3-bleu-caveat): the project scores lower-cased, tokenised text against references rebuilt from the vocabulary, so unknown words match for free. Scored against the real references, the local checkpoint drops from $38.98$ to $36.96$ BLEU, and to $31.33$ if the references keep their original casing and punctuation.

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> Task 1 (attention), which the autograder tests in isolation.</em>

</div>

The problem statement is `DA6401_Assignment_3_2026.pdf` (three pages). A course announcement, saved at the top of `SKILL.md` in the assignment folder, added one requirement: a method `Transformer.infer(german_sentence)` that does the whole pipeline, because the hidden-test autograder runs, for every test sentence,

```python
model = Transformer().to(self.device)
model.eval()
english_sentence = model.infer(german_sentence)
```

so every constructor argument needs a default, and the vocabulary, tokenisers and the trained weights (downloaded with `gdown`) must all be loaded inside `Transformer.__init__`. The same announcement says the Gradescope submission opened on 9 May 2026; the deadline is UNKNOWN.

## 1.0.i Constraints {#s1-0-i}

- Allowed libraries: `torch`, `numpy`, `matplotlib`, `scikit-learn`, `wandb`, `datasets`, `spacy`, `bleu`, `tqdm`. The code uses `sacrebleu` (the comment at `train.py:167` calls it “the permitted BLEU library”); whether `sacrebleu` counts as the permitted `bleu` is UNKNOWN.
- Implement the <em>base</em> architecture of the paper; build it from `nn.Linear`/`nn.Module`; use `nn.LayerNorm`.
- Tokenise and preprocess with spaCy only.
- Use only Multi30k (`bentrevett/multi30k` on Hugging Face).
- Follow the official skeleton (`da6401_assignment_3-main.zip` in the folder).

## 1.0.ii Task-by-task status {#s1-0-ii}

| <strong>Item</strong> | <strong>Where</strong> | <strong>Marks</strong> | <strong>Status</strong> |
|:--|:--|:--|:--|
| Scaled dot-product attention | `model.py:40-66` | 10 (tests) | done |
| Multi-head attention | `model.py:115-178` | (same 10) | done |
| Padding and causal masks | `model.py:74-105` | (same 10) | done |
| Sinusoidal PE as a buffer | `model.py:190-226` | 10 (tests) | done |
| Add &amp; Norm (Pre- or Post-LN) | `model.py:287-364` | – | Post-LN; justification see below |
| Position-wise FFN | `model.py:259-276` | – | done |
| Label smoothing $\varepsilon = 0.1$ | `train.py:27-63` | – | done |
| Noam scheduler | `lr_scheduler.py:16-57` | 10 (tests) | done |
| Greedy decoding | `train.py:132-158` | – | done |
| Test BLEU of best checkpoint | `train.py:166-224` | 20 | done; score UNKNOWN |
| `infer()`, no-argument constructor | `model.py:445-628` | – | done; output not detokenised |
| 2.1 Noam vs fixed LR | `nk7bpdip`, `vfe597s4` | 10 | done; see [Section 1.4.v](experiments/#sec-a3-abl21) |
| 2.2 with/without $1/\sqrt{d_k}$ | `0kax3ah0`, `wptvqi13` | 10 | done |
| 2.3 attention heads | `t9jaqwy1` | 10 | partial; see [Section 1.4.vii](experiments/#sec-a3-abl23) |
| 2.4 sinusoidal vs learned PE | `965l9hi6`, `9dg7ccnk` | 10 | done |
| 2.5 label smoothing | `xk9wrmw2`, `uc5mn6hd` | 10 | done |

<div class="nb nb-remark" id="remark-1-0-1">

<strong>Remark 1.0.1</strong> (The Post-LN justification) — The problem statement asks for the choice of Pre- or Post-LayerNorm to be justified in the report. The report text generated by the last cell of `wandb_experiments.ipynb` has no such paragraph. The W&amp;B API shows the report was last updated on 19 May 2026, after it was generated, so it may have been edited by hand; whether it contains the justification is UNKNOWN. The only justification in the code is the comment “We are using Post-LayerNorm as in the original paper” (`model.py:284`).

</div>

## 1.0.iii Deliverables {#s1-0-iii}

The submission is the code (a public GitHub repository), the trained weights on Google Drive (fetched by `gdown`), and the public W&amp;B report “DA6401 Assignment 3 — Transformer NMT Ablation Study”. The final marks are UNKNOWN.

## Contents

- [1.1 · Dataset and preprocessing](data/)
- [1.2 · Theory and background](theory/)
- [1.3 · Architecture and implementation](implementation/)
- [1.4 · Experiments and the W&amp;B report](experiments/)
- [1.5 · Results and discussion](wrapup/)
- [A · Glossary of notations](notation/)
- [References](references/)
