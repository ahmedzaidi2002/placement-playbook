---
title: "9 · Language models and LLMs"
linkTitle: "9 LLMs"
weight: 9
math: true
---
A language model assigns probabilities to sequences of tokens; a large language model is a Transformer trained to do that on a very large corpus and then adapted to follow instructions. Placement OAs mostly ask what fine-tuning means; interviews at AI companies ask how tokenisation works, what decoding knobs do, what LoRA saves, how to serve a model in less memory, and how retrieval reduces hallucination.

## 9.1 Tokens and embeddings {#dl-9-1}

Models see integer **tokens**. Word-level vocabularies cannot handle unseen words; character-level sequences are long. **Subword** tokenisers sit in between: frequent words become one token, rare words split into pieces.

**Byte-pair encoding (BPE):** start from characters (or bytes) and **repeatedly merge the most frequent adjacent pair** into a new token. Unseen words are still encodable as pieces ("sleeper" → `s l eeper`). Production tokenisers work on bytes, learn tens of thousands of merges, and (WordPiece, unigram) differ in how they choose merges.

Consequences worth saying in an interview: costs and context limits are counted in tokens; numbers and rare scripts fragment into many tokens; spelling-level tasks are hard because the model never sees letters.

An **embedding layer** is a lookup table $E \in \mathbb R^{V \times d}$: token $i$ becomes row $i$, equivalent to a one-hot vector times $E$, trained like any other weight.

## 9.2 Objectives and families {#dl-9-2}

- **Causal LM** (GPT, decoder-only): $p(x_1, \dots, x_T) = \prod_t p(x_t \mid x_{<t})$, trained with cross-entropy on every position at once under a causal mask. Natural for generation.
- **Masked LM** (BERT, encoder-only): pick 15% of positions; replace 80% of those with `[MASK]`, 10% with a random token, keep 10%; predict the originals from both sides. The random and kept cases stop the model learning that only `[MASK]` positions matter. Strong representations, not a generator.
- **Sequence-to-sequence** (T5, BART): encoder reads, decoder writes; pre-trained by reconstructing corrupted spans.

**Perplexity** is the exponential of the per-token cross-entropy, the effective number of equally likely choices per token: $\text{PPL} = \exp\big(-\tfrac{1}{T}\sum_t \log p(x_t \mid x_{<t})\big)$. A uniform model over $V$ tokens has perplexity $V$. Perplexities are comparable only with the same tokeniser and test text.

<div class="nb nb-example">

<strong>Example</strong> (Perplexity)

Token probabilities 0.2, 0.5, 0.1: mean negative log-probability $\tfrac13(1.609 + 0.693 + 2.303) = 1.535$, so perplexity $e^{1.535} = 4.64$ (the inverse geometric mean of the probabilities).

</div>

**Scale:** training a dense Transformer costs about $6ND$ FLOPs for $N$ parameters and $D$ tokens. Loss falls as a smooth power law in $N$, $D$ and compute in the regimes studied; one analysis found compute-optimal training at roughly 20 tokens per parameter, but many models train on far more because smaller models are cheaper to serve. Treat such constants as properties of particular fits.

## 9.3 Adapting a pretrained model {#dl-9-3}

From cheapest to most expensive:

1. **Prompting / in-context learning:** no weights change.
2. **Feature extraction (linear probing):** freeze the model, train a small head.
3. **Prompt / prefix tuning:** learn a few virtual-token embeddings; model frozen.
4. **Adapters:** small bottleneck MLPs inserted in each layer; model frozen.
5. **LoRA:** below.
6. **Full fine-tuning:** update every weight with a small learning rate; best quality with plenty of data, but one full model copy per task and optimiser state for every parameter.

**Instruction tuning** is supervised fine-tuning on (instruction, good response) pairs. **RLHF** collects human preferences between pairs of responses, trains a **reward model**, and optimises the policy with RL (typically PPO) plus a KL penalty that keeps it close to the supervised model. **DPO** optimises a classification-style loss directly on preference pairs, with no reward model or RL loop.

**LoRA:** freeze the pretrained $W_0 \in \mathbb R^{d_{\text{out}}\times d_{\text{in}}}$ and learn a low-rank update, $W = W_0 + \tfrac{\alpha}{r} BA$ with $B \in \mathbb R^{d_{\text{out}}\times r}$, $A \in \mathbb R^{r \times d_{\text{in}}}$, $r \ll d$. $B$ starts at zero, so training starts exactly from the pretrained model; afterwards $BA$ can be merged into $W_0$. Trainable parameters per matrix: $r(d_{\text{in}} + d_{\text{out}})$ instead of $d_{\text{in}}d_{\text{out}}$.

<div class="nb nb-example">

<strong>Example</strong> (What LoRA saves)

A $4096 \times 4096$ matrix with rank 8: $8 \times 8192 = 65{,}536$ trainable parameters instead of 16,777,216, i.e. **0.39%**.

</div>

<div class="nb nb-remark">

<strong>Trap</strong> — "LoRA reduces inference latency" or "makes the model smaller". It reduces **trainable** parameters, gradients and optimiser state (and storage per task). After merging, the model has exactly the original size and speed. With a quantised frozen base (QLoRA-style) it also cuts the memory of the frozen weights.

</div>

## 9.4 Decoding {#dl-9-4}

Given next-token logits: **greedy** takes the argmax; **beam search** keeps $k$ hypotheses (chapter 7); sampling reshapes the distribution first:

- **Temperature** $T$: divide logits by $T$; $T \to 0$ is greedy, large $T$ flattens.
- **Top-$k$**: keep the $k$ most likely tokens, renormalise.
- **Top-$p$ (nucleus)**: keep the smallest set with total probability $\ge p$, renormalise. Adapts to how peaked the distribution is, unlike top-$k$.

<div class="nb nb-example">

<strong>Example</strong> (Top-p)

Sorted probabilities $(0.529, 0.321, 0.072, 0.043, \dots)$ have cumulative sums $0.529, 0.849, 0.921, \dots$, so the nucleus for $p = 0.9$ is the first **three** tokens, renormalised to $(0.574, 0.348, 0.078)$.

</div>

Greedy and beam search produce repetitive, generic text in open-ended generation; sampling with moderate temperature and top-$p$ is the usual default there, while greedy suits tasks with one right answer (code, extraction).

## 9.5 Evaluation and its limits {#dl-9-5}

**BLEU** (translation) multiplies a brevity penalty by the geometric mean of clipped n-gram precisions against references. **ROUGE** (summarisation) emphasises recall; ROUGE-L uses the longest common subsequence.

<div class="nb nb-example">

<strong>Example</strong> (BLEU-2)

"the cat is on the mat" against "the cat sat on the mat": unigram precision 5/6, bigram precision 3/5, brevity penalty 1, so BLEU-2 $= \sqrt{0.833 \times 0.6} = 0.707$.

</div>

The limits: a correct paraphrase scores badly; one wrong word can flip meaning at a small cost; none of these measure factuality. Perplexity measures fit to text, not usefulness. LLMs are therefore evaluated on task benchmarks, by human preference, and by other models as judges, each with its own biases (benchmark **contamination** above all). For the BLEU caveats in your own project, see [chapter 8](../08-transformer/#dl-8-7).

## 9.6 Making models cheaper {#dl-9-6}

- **Quantisation:** a 7B-parameter model needs 28 GB of weights in fp32, 14 GB in fp16/bf16, 7 GB in int8, 3.5 GB in 4-bit. One outlier stretches a per-tensor scale for everyone, so practical schemes use per-channel or per-group scales. Post-training quantisation needs no retraining; quantisation-aware training simulates rounding during training.
- **Distillation:** a small student matches a large teacher's **softened** outputs (temperature $T > 1$ reveals which wrong classes are nearly right, the "dark knowledge"), usually mixed with the ordinary label loss; the loss is scaled by $T^2$.
- **Mixture of experts:** replace the FFN by $E$ experts and a router sending each token to the top $k$. Capacity follows total parameters; compute per token follows **active** parameters. Costs: memory for all experts, load balancing, communication.

<div class="nb nb-remark">

<strong>Trap</strong> — "An MoE model with $X$ total parameters runs like a dense $X$ model" (it runs closer to its active size) and "quantisation reduces FLOPs" (it mainly reduces memory and memory traffic; speed-ups need low-precision kernels).

</div>

## 9.7 Retrieval, tools and failure modes {#dl-9-7}

**Retrieval-augmented generation (RAG):** embed documents offline; at query time embed the question, retrieve the top-$k$ most similar chunks (cosine similarity, approximate nearest-neighbour index), and put them in the prompt with an instruction to answer from them and cite them. It gives fresh and private knowledge without retraining and makes answers checkable. Real systems add chunking, re-ranking and hybrid keyword search. **Tool use and agents** extend it: the model emits structured calls (search, code, APIs), the system runs them and feeds results back.

**Hallucination** (fluent, confident, wrong output) follows from training to produce *likely* text rather than *true* text. Mitigations: retrieval with citations, letting the model abstain when the context lacks the answer, lower temperature for factual tasks, verification steps, evaluation sets that measure it. Safety basics: **prompt injection** (instructions hidden in retrieved or user content), leakage of private data, harmful content, bias, and treating model output as **untrusted input** to the rest of the system.

<div class="nb nb-moral">

Pretrain to predict tokens, adapt cheaply (LoRA, instruction tuning, preference optimisation), decode with the right knob, serve with fewer bits, and ground answers in retrieved evidence.

</div>
