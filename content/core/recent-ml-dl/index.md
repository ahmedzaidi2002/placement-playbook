---
title: "Recent ML/DL: what is hot in AI"
linkTitle: "Recent ML/DL"
weight: 9
math: true
---

A one-page review of the topics that AI/ML interviewers in late 2026 expect you to be able to talk about. It is a **snapshot (October 2026)**: the concepts below have been stable for a year or more, but product names, model versions and benchmark numbers change monthly, so none are quoted here. Know the idea, the cost, and the trade-off; look up the version.

It assumes the [Deep Learning](../dl/) book, mainly [Transformers](../dl/08-transformer/) and [LLMs](../dl/09-llm/).

<div class="nb nb-moral">

The Transformer is still the backbone of frontier models. "Post-transformer" architectures are mostly efficiency alternatives and **hybrids** (some attention layers kept), not replacements that have won. For jobs, the order of value is: LLM fundamentals, agents, RAG, fine-tuning, inference optimisation, evaluation. Architecture research comes after, unless the role is research.

</div>

## Priority map

| Tier | Topics | Depth expected |
| --- | --- | --- |
| **1. Must know** | LLM internals, post-training, RAG, agents, inference optimisation, evaluation and safety | Explain, give numbers, name trade-offs |
| **2. Should know** | Reasoning models, multimodal models, LLMOps and serving | Explain the idea and where it fails |
| **3. Know the concept** | SSMs and hybrids, linear attention, diffusion and flow matching, world models and JEPA, neuro-symbolic | One paragraph and one trade-off each |

## 1 · LLM internals worth having at your fingertips

- **Self-attention** costs $O(n^2 d)$ time and $O(n^2)$ memory for sequence length $n$ (naively). **FlashAttention** is an *exact* kernel that avoids writing the $n \times n$ matrix to GPU memory, so it saves memory traffic, not FLOPs.
- **Positional information:** the original sinusoidal encodings were replaced in most open models by **rotary embeddings (RoPE)**, which rotate query/key pairs by position-dependent angles so attention depends on *relative* distance. Long-context extension is mostly done by rescaling these angles.
- **KV cache:** during generation, keys and values of past tokens are stored so each new token costs one step, not a full recompute. It is the main memory cost of long contexts.
- **Cache size** $= 2 \times L \times h_{kv} \times d_{head} \times n \times \text{bytes}$ per sequence ($L$ layers, $h_{kv}$ key/value heads).
- **GQA / MQA:** many query heads share few key/value heads, shrinking the KV cache by the sharing factor with small quality loss.
- **MoE:** only $k$ of $E$ experts run per token, so compute follows *active* parameters while memory follows *total* parameters ([DL ch. 9](../dl/09-llm/#dl-9-6)).

<div class="nb nb-example">

<strong>Example</strong> (KV cache)

A 7B-style model: 32 layers, 32 KV heads, head size 128, fp16. Per token: $2 \times 32 \times 32 \times 128 \times 2 = 524{,}288$ bytes $= 0.5$ MiB. At 4096 tokens that is **2 GiB per sequence**. With GQA using 8 KV heads it drops to 0.5 GiB. Ten concurrent users at 4k tokens need 20 GiB of cache before counting weights.

</div>

<div class="nb nb-remark">

<strong>Trap</strong> — "Longer context means the model uses it well". Long-context models often degrade on information buried in the middle; "supports $N$ tokens" is a capacity claim, not a quality claim. Test retrieval at depth.

</div>

## 2 · Post-training: turning a base model into an assistant

The usual pipeline is **pretraining → SFT → preference optimisation → (reasoning) RL**.

| Stage | What it does | Note |
| --- | --- | --- |
| SFT | Supervised fine-tuning on (instruction, good answer) pairs | Teaches format and style, little new knowledge |
| RLHF | Reward model trained on human preferences, then PPO with a KL penalty | Heavy: reward model, value model, instability |
| DPO | Loss directly on (chosen, rejected) pairs, no reward model or RL loop | Simple and stable; offline |
| RLVR | RL where the reward is a **programmatic check** (answer matches, tests pass) | Behind most recent reasoning gains |
| LoRA / QLoRA | Train low-rank adapters; QLoRA keeps the frozen base in 4-bit | Fine-tune a 7B on one GPU |

- **DPO loss:** $-\log \sigma\!\Big(\beta\big[\log\tfrac{\pi_\theta(y_w)}{\pi_{ref}(y_w)} - \log\tfrac{\pi_\theta(y_l)}{\pi_{ref}(y_l)}\big]\Big)$. Raise the likelihood of the chosen answer relative to the reference model, lower the rejected one; $\beta$ controls how far you may drift.
- **GRPO** (used for reasoning models) drops the learned critic: sample a group of answers to the same prompt and use the group's normalised reward as the advantage, $A_i = (r_i - \bar r)/\sigma_r$.
- **Synthetic data and distillation:** a strong model writes or filters training data for a smaller one. Quality filtering and diversity matter more than volume; training repeatedly on a model's own unfiltered output degrades it ("model collapse").

<div class="nb nb-example">

<strong>Example</strong> (GRPO advantage)

Four sampled answers get rewards $(1, 0, 0, 1)$. Mean $0.5$, standard deviation $0.5$, so advantages are $(+1, -1, -1, +1)$: correct answers are reinforced, wrong ones suppressed, with no value network.

</div>

<div class="nb nb-remark">

<strong>Trap</strong> — "Fine-tune to add knowledge". Fine-tuning mostly changes behaviour, format and tone; for fresh or private facts use retrieval. Fine-tune when you need a consistent style, a structured output, or a cheaper small model for a narrow task.

</div>

## 3 · Reasoning models and test-time compute

A **reasoning model** is trained (largely with RLVR) to produce a long chain of thought before the final answer. The new scaling axis is **inference-time compute**: more thinking tokens, or more samples, gives better answers on maths, code and planning, at higher latency and cost.

- **Self-consistency / majority vote:** sample $N$ answers, return the most common.
- **Best-of-$N$ with a verifier:** a reward model or test-runner picks the best. Works when checking is easier than generating.
- **pass@k:** probability that at least one of $k$ samples is correct; with per-sample success $p$ and independent samples, $1 - (1-p)^k$. For $p = 0.3$, $k = 5$: $1 - 0.7^5 = 0.83$.
- **Limits:** longer reasoning can "overthink" simple questions, the written chain of thought is not guaranteed to be the real cause of the answer, and gains are strongest where answers can be verified.

<div class="nb nb-moral">

Training-time scaling made models bigger; test-time scaling lets a fixed model spend more compute on hard questions. The enabling ingredient is a cheap, reliable **verifier**.

</div>

## 4 · Agentic AI

An **agent** is an LLM in a loop: observe, decide (plan), call a tool, read the result, repeat until done or stopped.

- **Building blocks:** tool/function calling (model emits structured arguments, your code runs them), planning (ReAct-style think-then-act, or plan-then-execute), memory (short-term = context window; long-term = a store retrieved on demand), and guardrails.
- **MCP (Model Context Protocol):** an open protocol for exposing tools and data to models through a standard client–server interface, so one integration works across many applications.
- **Workflows vs agents:** a fixed pipeline with LLM steps is cheaper, predictable and easier to test; let the model choose the path only when the task needs it. Start with the simplest design that works.
- **Multi-agent systems:** specialised agents (planner, coder, reviewer) coordinating by messages. Helpful for parallel or separable work; they multiply cost, latency and failure modes.
- **Why they fail:** errors compound over steps (a per-step success of 95% over 10 independent steps gives $0.95^{10} \approx 0.60$), tools return unexpected output, context fills up, and loops never terminate. Mitigate with step limits, validation of tool output, retries, checkpoints and human approval for irreversible actions.
- **Security:** **indirect prompt injection** (instructions hidden in a web page, email or document the agent reads) is the central risk. Treat retrieved content as untrusted, give tools least privilege, and require confirmation for side effects.

## 5 · Advanced RAG

Basic RAG (chunk → embed → top-$k$ → prompt) fails on keyword-heavy queries, vague questions and multi-hop questions. The standard upgrades:

| Problem | Fix |
| --- | --- |
| Embeddings miss exact terms (IDs, names) | **Hybrid search:** BM25 + dense vectors, merged with reciprocal rank fusion, $\sum 1/(k + \text{rank})$ with $k \approx 60$ |
| Top-$k$ contains near-misses | **Reranker:** a cross-encoder rescoring the top 50–100 down to 5 |
| User question is vague or conversational | **Query rewriting**, expansion, or decomposition into sub-queries |
| Chunks lose context | Better chunking (by structure), overlap, parent-document retrieval, contextual headers |
| Multi-hop or "summarise everything" questions | **GraphRAG:** build an entity–relation graph and retrieve over it |
| Model ignores or misuses evidence | Cite sources, allow "not found", check faithfulness |

**Evaluate retrieval and generation separately.** Retrieval: recall@k, MRR, nDCG. Generation: **faithfulness** (is every claim supported by the retrieved text?), answer relevance, context precision.

<div class="nb nb-remark">

<strong>Trap</strong> — blaming the LLM for a wrong answer when the right chunk was never retrieved. Check recall@k first; most RAG failures are retrieval failures.

</div>

## 6 · Multimodal models

- **Vision–language models:** an image encoder (a ViT, often CLIP-style) turns the image into patch embeddings; a **projector** maps them into the LLM's token space; the LLM then treats them like text tokens. A $224 \times 224$ image with $16 \times 16$ patches gives $14 \times 14 = 196$ visual tokens, so high-resolution images and video are expensive in context.
- **CLIP** trains an image encoder and a text encoder with a **contrastive loss** so matching pairs have high cosine similarity and mismatched pairs low. This gives multimodal embeddings, used for search and zero-shot classification.
- **Audio and speech:** speech-to-text models, text-to-speech, and models that take and produce audio directly for low-latency voice assistants. **Video** adds time: frame sampling and temporal tokens.
- Typical failures: counting, fine spatial reasoning, reading dense small text, and hallucinating details not in the image.

## 7 · Inference optimisation and serving

Generation has two phases: **prefill** (process the prompt in parallel; compute-bound) and **decode** (one token at a time; **memory-bandwidth-bound**, because every step reads all the weights).

<div class="nb nb-example">

<strong>Example</strong> (Decode speed limit)

A 7B model in fp16 is 14 GB. On a GPU with 1 TB/s memory bandwidth, one decode step must read 14 GB, so a single stream cannot exceed about $1000/14 \approx 71$ tokens/s. In int4 (3.5 GB) the bound is about 285 tokens/s. **Batching** shares one weight read across many requests, which is why throughput rises with batch size.

</div>

| Technique | Idea | Effect |
| --- | --- | --- |
| Quantisation (int8, int4, fp8) | Fewer bits per weight/activation | Less memory and traffic; small quality loss |
| Distillation | Small student mimics large teacher | Cheaper model |
| **Continuous batching** | Add and remove requests every step instead of waiting for a full batch | Much higher GPU utilisation |
| **PagedAttention** (vLLM) | Store KV cache in fixed-size blocks like OS pages | Little fragmentation, more concurrent users |
| Prefix caching | Reuse KV for a shared prompt prefix | Cheaper repeated system prompts |
| **Speculative decoding** | Small draft model proposes $\gamma$ tokens; big model verifies them in one pass | Same output distribution, fewer big-model passes |
| Parallelism | Tensor / pipeline / expert parallel across GPUs | Fit and speed up big models |

- **Speculative decoding speed-up:** with per-token acceptance rate $\alpha$ and $\gamma$ drafted tokens, the expected tokens per big-model pass is $\frac{1-\alpha^{\gamma+1}}{1-\alpha}$. For $\alpha = 0.8$, $\gamma = 4$: $\frac{1-0.8^5}{0.2} \approx 3.4$.
- **Metrics:** time to first token (TTFT, dominated by prefill), time per output token (TPOT), throughput (tokens/s across users), and cost per million tokens. Latency and throughput trade off through batch size.

## 8 · Evaluation, safety and LLMOps

- **Benchmarks** saturate and leak into training data (**contamination**), so build a **task-specific eval set** from real traffic and score it automatically on every change.
- **LLM-as-judge** scales evaluation but has known biases: preference for longer answers, for the first option, and for its own family's style. Calibrate against human labels on a sample.
- **Hallucination:** measure with faithfulness checks against sources and with abstention tests (does it say "I don't know" when it should?).
- **Safety:** direct and indirect prompt injection, jailbreaks, data leakage, over-refusal. Defence is layered: input and output filters, least-privilege tools, sandboxing, and monitoring; no single guardrail is sufficient.
- **LLMOps:** trace every request (prompt, retrieved chunks, tool calls, latency, tokens), log user feedback, version prompts and models, use regression evals before deploys, set budgets and rate limits, and route easy queries to a cheaper model. Cost and latency are product requirements, not afterthoughts.

## 9 · Emerging architectures: know the concept and the trade-off

| Idea | One-line explanation | Trade-off / maturity |
| --- | --- | --- |
| **State space models** (S4, **Mamba**) | A recurrent state updated per token, with input-dependent (selective) dynamics. $O(n)$ time and **constant memory per generated token**, no KV cache | Weaker at exact recall and copying from far back in context |
| **Hybrids** | Mostly SSM (or linear-attention) layers plus a few attention layers, often with MoE (e.g. Jamba, Nemotron-H) | Best-documented practical route; shipped by several labs |
| **Linear attention / recurrent variants** | Reformulate attention as a running state so cost is linear in $n$ (gated linear attention, delta-rule variants, RWKV) | Active area; usually hybridised with some full attention |
| **Diffusion models** | Learn to reverse a gradual noising process; sample by iterative denoising | Dominant for images and video; diffusion for *text* is still research |
| **Flow matching** | Train a network to predict the velocity of a (near-)straight path from noise to data; simpler training and fewer sampling steps than classic diffusion | Increasingly used in image/video generators |
| **World models and JEPA** | Predict the *latent* representation of the future or of masked parts, not pixels, then use it for planning and control | Promising for robotics and video understanding; mostly research |
| **Neuro-symbolic** | Neural nets for perception, explicit logic/solvers for exactness (e.g. LLM writes a program that a solver or interpreter runs) | Practical form today: tool use and code execution |

<div class="nb nb-moral">

Interview answer on "will SSMs replace Transformers?": attention gives precise random access to the whole context at quadratic cost; SSMs give cheap fixed-size memory but lossy recall. Hybrids take both, which is why they are the realistic near-term outcome.

</div>

## Rapid-fire: say it in 20 seconds

1. **Why is decoding slow?** Each token needs a full read of the weights (memory-bandwidth-bound) and reads a growing KV cache.
2. **What does the KV cache store, and what does GQA change?** Past keys and values per layer; GQA shares KV heads across query heads, shrinking the cache.
3. **FlashAttention: fewer FLOPs?** No. Same maths, fewer memory reads and writes by tiling.
4. **LoRA vs full fine-tuning?** LoRA trains low-rank adapters (a fraction of a percent of parameters), the base stays frozen; full fine-tuning updates everything.
5. **DPO vs RLHF?** DPO optimises preference pairs directly, with no reward model or RL loop.
6. **What is RLVR?** RL with a programmatic reward, such as a checker or unit tests; no learned reward model.
7. **What is test-time compute?** Spending more inference compute (longer chains, more samples, verification) to get better answers from a fixed model.
8. **When does best-of-$N$ help?** When a reliable verifier exists.
9. **What is an agent?** An LLM in a loop with tools, memory and a stopping rule.
10. **What is MCP?** An open protocol that standardises how models connect to tools and data sources.
11. **Why can agents fail on long tasks?** Per-step errors multiply, context fills, and tool outputs are unreliable.
12. **What is indirect prompt injection?** Malicious instructions placed in content the model reads (pages, emails, files); mitigate with least privilege, untrusted-content handling and confirmation for side effects.
13. **How do you improve a bad RAG system?** Measure recall@k first; then hybrid search, reranking, better chunking and query rewriting.
14. **Why hybrid search?** Dense vectors handle meaning, BM25 handles exact terms; fuse the rankings.
15. **What does quantisation buy?** Smaller weights, less memory traffic, faster decode; not fewer FLOPs by itself.
16. **What is continuous batching / PagedAttention?** Per-step scheduling of requests, and KV cache in paged blocks to avoid fragmentation.
17. **What is speculative decoding?** A draft model proposes tokens, the large model verifies in one pass; output distribution unchanged.
18. **How would you evaluate an LLM feature?** A task-specific eval set from real data, automatic scoring plus human-calibrated LLM judge, regression runs on every change, and monitoring in production.
19. **Why is Mamba efficient, and what does it lose?** Constant-size recurrent state, linear time, no KV cache; loses exact long-range recall.
20. **Diffusion vs flow matching?** Both transform noise to data; flow matching trains a velocity field along simple paths, usually with simpler training and fewer steps.
21. **What is JEPA?** Predict abstract latent features of missing or future data rather than raw pixels.

## Suggested learning order

1. **Foundations:** Transformers, PyTorch, the LLM training pipeline, fine-tuning, inference ([Deep Learning](../dl/) chapters 8–9).
2. **Applications:** embeddings, vector search, RAG, tool calling, small agent workflows.
3. **Production:** serving (vLLM-style batching and caching), quantisation, evals, tracing, GPU efficiency.
4. **Frontier:** reasoning-model training, SSMs and hybrids, world models.

<div class="nb nb-remark">

<strong>Caveat</strong> — headline numbers about this field (benchmark scores, agent success rates, adoption percentages, price drops) vary by source and date and often come from vendor or blog posts. Quote mechanisms and trade-offs in an interview; if you cite a figure, name the source and date.

</div>
