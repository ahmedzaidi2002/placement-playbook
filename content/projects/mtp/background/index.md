---
title: "1.2 · Problem statement and background"
linkTitle: "1.2 Problem statement and background"
weight: 2
math: true
---
<div class="nb-proto">

<em><span>Prototypical example for this section:</span> an investigator is shown that account 24 was flagged as suspicious, and asks which of its transfers made the model say so.</em>

</div>

## 1.2.i The problem {#s1-2-i}

Fraud and money-laundering detectors increasingly work on a <strong>transaction graph</strong>: nodes are accounts or wallet addresses, edges are transfers, and a GNN classifies each node as licit or illicit from its own features and those of its neighbours. The output is a probability. A bank’s compliance team, a regulator or a court needs more than that: it needs the <em>evidence</em>, meaning the few transfers and neighbours the model relied on. A <strong>post-hoc explainer</strong> produces it after training, without changing the model; GNNExplainer is the standard one for graphs.

The catch is that an explanation is itself a model output, and it can be wrong or unstable in ways nobody notices unless it is scored against a known truth. That needs data in which the truth is planted: the synthetic benchmarks of the GNNExplainer paper (house-shaped and cycle-shaped motifs) and, closer to banking, IBM’s AMLSim, which plants fan-in, fan-out and cycle laundering patterns inside normal traffic. My work measures how well GNNExplainer recovers those planted patterns, and what changes that number.

## 1.2.ii The baseline I started from {#sec-mtp-baseline}

The previous M.Tech report in my lab, Pavitra Khare’s <em>Blockchain-Forensics: Explainable AI for Malicious Activity Detection</em> (December 2025, 65 pages), proposes a three-stage pipeline:

1. <strong>Detection:</strong> a 2-layer GCN classifying nodes as licit or illicit.
2. <strong>Explanation:</strong> GNNExplainer, which learns a continuous mask over the edges of the node’s computation graph by minimising the conditional entropy of the prediction, with size and discreteness regularisers.
3. <strong>Semantic interpretation:</strong> rules mapping the explanation’s shape to a forensic typology: a long path suggests a peel chain, a star suggests smurfing or structuring, a cycle suggests round-tripping, a dense subgraph suggests a fraud ring.

It is evaluated only on the four synthetic benchmarks. Its Table 5.1 (explanation accuracy, AUC) reads:

| Dataset | GNNExplainer | GRAD | ATT |
|:--|:-:|:-:|:-:|
| BA-Shapes | $0.912$ | $0.871$ | $0.805$ |
| BA-Community | $0.828$ | $0.741$ | $0.721$ |
| Tree-Cycles | $0.939$ | $0.901$ | $0.825$ |
| Tree-Grid | $0.860$ | $0.665$ | $0.611$ |

These are $0.013$, $0.008$, $0.009$ and $0.015$ below the GNNExplainer paper’s own Table 1 ($0.925$, $0.836$, $0.948$, $0.875$). The report introduces the table with the sentence “the values are consistent with reported results in the GNNExplainer literature and are used here for comparative analysis” <span style="color:#009b55"><strong>[R]</strong></span> (read in the PDF), which leans towards quoted values but does not say so. Whether they come from its author’s own runs or are quoted from the paper is <strong>UNKNOWN</strong>; I treat both sets as <em>targets</em> and never as numbers to match exactly. The report’s own future-work chapter lists a unified comparison with PGExplainer, larger and noisier real graphs, a full end-to-end pipeline and temporal extensions.

## 1.2.iii What my work adds {#s1-2-iii}

|  | Starting point | What I did |
|:--|:--|:--|
| Model | “2-layer GCN” | 3-layer models on the synthetic sets (2 layers leave BA-Shapes near $40\%$ accuracy); both the authors’ architecture and the standard Kipf GCN |
| Scoring | AUC of the explanation mask against motif edges; the exact edge set is not stated in the report (PyG’s official BA-Shapes example scores the whole $k$-hop <em>induced</em> subgraph) | edges that can reach the prediction only, ground truth restricted to the node’s own motif ([Section 1.4](../flaw/)) |
| Data | four synthetic benchmarks | \+ Cora (to understand the methods), + AMLSim (planted laundering patterns on simulated bank transfers) |
| Evidence | numbers in a table | per-seed values, standard deviations, controls, and every deviation from the papers written down |

## 1.2.iv The datasets and what each is for {#sec-mtp-datasets}

| Dataset | Kind | Explanation ground truth? | Used for |
|:--|:--|:--|:--|
| Cora | real citation graph, $2708$ nodes | none | understanding the two methods (B1) |
| BA-Shapes, BA-Community, Tree-Cycles, Tree-Grid | synthetic, planted motifs | yes: the motif edges | reproducing the paper (B3) |
| AMLSim `paramFiles/1K` | simulated bank transfers, $1446$ accounts | yes: the edges of the planted alerts (fan-in, fan-out, cycle) | B2, B4, B5 |
| Elliptic, Elliptic++, Ethereum phishing | real blockchain graphs | none | <strong>not used yet</strong> |

## 1.2.v Where this sits in the literature {#sec-mtp-related}

From the research note of 30 September 2026 (web search, OpenAlex and reading, <span style="color:#f7921d"><strong>[L]</strong></span>); I have not repeated the search, and some papers were read only in part.

- <strong>Explainers on AMLSim.</strong> I found no work that scores GNNExplainer or PGExplainer against AMLSim’s planted alerts. The nearest are a Chalmers MSc thesis (node-level Shapley importance on a larger AMLSim fork, 2024), a 2024 IEEE Access paper that says it used GNNExplainer on AMLSim but shows no explanation output, and a 2026 preprint that scores GNNExplainer against laundering rings on IBM’s <em>AML</em> dataset, a different simulator (mean Jaccard $21.4\%$ against $10.5\%$ for attention and $1.0\%$ for random). So on AMLSim there is no external number to compare with, and my numbers are first measurements, not improvements over anything.
- <strong>Reproducing GNNExplainer.</strong> An independent group (ML Reproducibility Challenge 2020 [&#91;Ho21&#93;](../references/#ref-holdijk2021)) re-implemented GNNExplainer and PGExplainer from scratch and measured $0.540$ AUC for GNNExplainer on Tree-Cycles, in line with my $0.55$; the PGExplainer authors told them that the GNNExplainer numbers in the PGExplainer paper were copied from the original paper because their own re-implementation gave “lackluster results”.
- <strong>On fraud graphs the ranking of explainers depends on the metric.</strong> Against ground truth, with thresholds tuned on a labelled validation day, PGExplainer beat GNNExplainer ($\mathrm{F}_1$ $0.43$ against $0.28$; Alipay transaction data, AAAI 2023); with fidelity metrics GNNExplainer won (GraphFramEx on eBay fraud data [&#91;Ama+22&#93;](../references/#ref-amara2022); a 2025 medical-claims study). So I do not assume either is better.
- <strong>Why GNNExplainer first.</strong> It is what the baseline report uses, it is the explainer that most attack and defence papers target (relevant to the original Idea 1), and PyG ships it. PGExplainer [&#91;Luo+20&#93;](../references/#ref-luo2020) is inductive and faster, which suits a deployed pipeline; a faithful reproduction is planned but not started.

## 1.2.vi How the scope changed {#sec-mtp-scope}

- <strong>16 August 2026.</strong> Four candidate ideas were drafted for the guide: (1) robustness of GNN explanations to adversarial edge manipulation, (2) undetailed, (3) agreement between several explainers in the spirit of Byzantine agreement, (4) a safe fallback of real-data validation on Elliptic. Idea 1 was the lead.
- <strong>27 August.</strong> PyG environment working; BA-Shapes baseline (a first version of what became B3).
- <strong>1 September.</strong> Scope cut to “environment plus GCN and GNNExplainer baseline” on my own decision. A prototype of a GXAttack-style attack and an XGNNCert-style defence, built and evaluated on BA-Shapes only, was deleted. The single observation kept: on that one testbed the attack did not beat a random-perturbation control on a confound-free metric. It is unconfirmed and not a result.
- <strong>22–23 September.</strong> PGExplainer researched in depth and a faithful-reproduction plan written (`documentations/pgexplainer-analysis-and-plan.md`). Nothing was implemented.
- <strong>Now.</strong> The topic is not formally fixed with the guide; `CLAUDE.md` calls it “ongoing, exploring”. The working priority is AMLSim-style practical explainability.

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> a 2-layer GCN on Cora, which mixes each node with its neighbours twice.</em>

</div>

## 1.2.vii The GCN {#s1-2-vii}

Let $A$ be the symmetric adjacency matrix of a graph with $N$ nodes, $X \in \mathbb R^{N\times C}$ the node features, $\tilde A = A + I$ the adjacency with self-loops and $\tilde D_{ii} = \sum_j \tilde A_{ij}$ its degree matrix. One layer of Kipf and Welling [&#91;KW17&#93;](../references/#ref-kipf2017) is

$$
H^{(l+1)} = \sigma \big(\hat A\, H^{(l)} W^{(l)}\big), \qquad \hat A = \tilde D^{-1/2}\tilde A\,\tilde D^{-1/2},
$$

which for one node reads

$$
\bm{h}_i^{(l+1)} = \sigma \Big(\sum_{j \in \mathcal N(i)\cup \{i\}} \frac{1}{\sqrt{\tilde d_i\,\tilde d_j}}\;\bm{h}_j^{(l)} W^{(l)}\Big).
$$

The two-layer model is $Z = \operatorname{softmax}\big(\hat A\,\operatorname{ReLU}(\hat A X W^{(0)})\,W^{(1)}\big)$. Each ingredient has a job.

- <strong>Self-loops</strong> ($+I$): a node keeps its own features instead of replacing them with its neighbours’.
- <strong>Symmetric normalisation</strong> ($\tilde D^{-1/2}\cdot \tilde D^{-1/2}$): without it, $\tilde A H$ sums neighbours, so a node with $100$ neighbours gets a vector $100$ times larger than a node with one. Kipf and Welling call the rescaled form the <em>renormalisation trick</em>; it avoids numerical instability and exploding gradients when layers are stacked.
- <strong>Depth $L$</strong>: $L$ layers mix information from nodes at most $L$ hops away and from nothing else.
- <strong>Semi-supervised training</strong>: the loss is the cross-entropy on the labelled nodes only ($140$ of $2708$ on Cora), yet every node’s features and edges enter the forward pass.

With $C=1433$ input features, $16$ hidden units and $7$ classes, the model has $1433\cdot16 + 16\cdot7 = 23{,}040$ parameters (no bias terms).

## 1.2.viii Which edges can influence a prediction {#sec-mtp-compgraph}

This is the fact that bullet B2 is about.

<div class="nb nb-theorem nb-block" id="proposition-1-2-1">

<strong>Proposition 1.2.1</strong> (Computation graph)

In an $L$-layer message-passing network, let $t$ be the node whose output is read. A change to the message sent along a directed edge $u \to v$ can change the output at $t$ only if there is a directed path from $v$ to $t$ with at most $L-1$ edges.

</div>

<div class="nb nb-proof">

<em>Proof.</em> The message on $u\to v$ is used at some layer $\ell \in \{1,\dots,L\}$ and changes the state of $v$ at that layer. Information then moves one edge per layer, so it can reach $t$ only through the remaining $L-\ell$ layers, which needs a path from $v$ to $t$ of length at most $L-\ell \le L-1$. If $v=t$ the path is empty.

</div>

So for $L=1$ the edges that matter are exactly the incoming edges of $t$. For $L=2$ they are the incoming edges of $t$ and of every neighbour that sends to $t$. Everything else in the $L$-hop neighbourhood, for example an edge between two neighbours of $t$ when $L=1$, cannot matter. Ying et al. call this edge set the computation graph $G_c$ and explain a prediction inside it.

<div class="nb nb-remark" id="remark-1-2-2">

<strong>Remark 1.2.2</strong> (Degree normalisation) — The proposition is about <em>messages</em>. In a GCN the weight of a message also contains the degrees of its two endpoints, so removing an edge between two nodes slightly changes the weights of other messages those nodes send. Whether that leaks influence depends on where the explainer’s mask enters. My hand-written explainer feeds the mask in as an edge weight <em>before</em> the degrees are computed ([Section 1.3.vi](../cora/#sec-mtp-explainer)). PyTorch Geometric multiplies the <em>message</em> by the mask after it has been normalised (`message_passing.py:743-768` of PyG 2.8), so degrees never see the mask, and for PyG’s explainer the proposition is exact. That is why, in [Section 1.4.iii](../flaw/#sec-mtp-flawmech), the set of non-zero mask entries equals the computation graph in every tested case.

</div>

## 1.2.ix GNNExplainer {#sec-mtp-gnnexp}

Ying et al. [&#91;Yin+19&#93;](../references/#ref-ying2019) explain the prediction $\hat y$ of a trained, frozen GNN $\Phi$ at node $v$ by finding a small subgraph $G_S \subseteq G_c(v)$ (and a few feature dimensions) that keeps the prediction. They formalise “important” as mutual information,

$$
\max_{G_S}\; \mathrm{MI}\big(Y, G_S\big) = H(Y) - H\big(Y \mid G = G_S\big),
$$

and since $H(Y)$ is constant for a fixed model, this is the same as minimising the conditional entropy $H(Y\mid G=G_S)$. Searching all subgraphs is exponential, so each edge gets a learnable real number $M_{jk}$, squashed by a sigmoid into $(0,1)$ and used as a soft edge weight: $G_S \approx A_c \odot \sigma(M)$. For the question “why did the model predict $\hat y$?” the objective becomes a cross-entropy against the <em>predicted</em> class, to which two regularisers are added:

$$
\min_{M}\; -\log P_\Phi \big(\hat y \mid A_c\odot \sigma(M), X_c\big)
	\;+\; \lambda_s \sum_{e}\sigma(M_e)
	\;+\; \lambda_e\, \overline{H}\big(\sigma(M)\big),
$$

where $H(p) = -p\log p - (1-p)\log(1-p)$ is the binary entropy and the overline is the mean over edges. The size term pushes masks to $0$ unless the prediction needs the edge; the entropy term pushes every mask value to $0$ or $1$, so that the result reads as “in” or “out”. The paper does not give $\lambda_s$ and $\lambda_e$. The reference code and PyG both use $0.005$ (on a <em>sum</em>) and $1.0$; my Cora project and the PyG runs in B3 and B5 use the same values. The optimisation is non-convex, so the result depends on the random initialisation and the coefficients. In PyG’s vocabulary, `explanation_type='model'` explains what the model <em>predicted</em> (the objective above), while `'phenomenon'` explains a given target such as the true label; all my runs use `'model'`, and the authors’ released code uses the true label, which answers a different question.

## 1.2.x Scoring an explanation {#sec-mtp-metrics}

When the truth is planted, an explanation is scored as a binary classification of edges: positive if the edge belongs to the planted motif or alert, with the mask value as the score.

<div class="nb nb-definition" id="definition-1-2-3">

<strong>Definition 1.2.3</strong> (AUROC). For a random positive edge $e^+$ and a random negative edge $e^-$, $\mathrm{AUROC} = \Pr[s(e^+) > s(e^-)] + \tfrac12\Pr[s(e^+) = s(e^-)]$. It is $0.5$ for a scorer that carries no information and $1$ for a perfect ranking.

</div>

- <strong>Pooled AUROC</strong>: concatenate the scored edges of all explained nodes and compute one AUROC. This is the paper’s framing (one edge-classification task) and the headline number everywhere in this chapter. <strong>Per-node AUROC</strong>: one AUROC per explained node, then the mean; nodes whose edges are all positive or all negative are skipped. The two differ: for the AMLSim baseline `gcn1` they are $0.4832$ and $0.5000$, and for `gcn2_rich` $0.7344$ and $0.7834$ <span style="color:#0071bc"><strong>[F]</strong></span>.
- <strong>Kept-edge precision and recall</strong>: threshold the mask at $0.5$ and count how many kept edges are positive (precision) and how many positives are kept (recall). They explain <em>why</em> an AUROC is what it is: GNNExplainer typically keeps a small <em>sufficient</em> subset of a motif (high precision, low recall), which a ground truth saying “the whole motif” punishes.
- <strong>Fidelity</strong> (PyG’s `fidelity`, from GraphFramEx [&#91;Ama+22&#93;](../references/#ref-amara2022); for explanations of the model’s own prediction): $\mathrm{fid}_+ = 1 - \frac1N\sum_i \mathbb 1[\hat y_i^{\,\text{complement}} = \hat y_i]$ and $\mathrm{fid}_- = 1 - \frac1N\sum_i \mathbb 1[\hat y_i^{\,\text{explanation}} = \hat y_i]$, where the explanation graph weights messages by $m_e$ and the complement by $1-m_e$. High $\mathrm{fid}_+$ means removing the explanation changes the prediction, low $\mathrm{fid}_-$ means keeping only the explanation preserves it. In this project the call is made once per explained node and the results are averaged, using the <em>soft</em> mask (`aml_run_configs.py:174-176`). The <strong>characterisation score</strong> is the harmonic mean $\big(\tfrac{0.5}{\mathrm{fid}_+} + \tfrac{0.5}{1-\mathrm{fid}_-}\big)^{-1}$.
- <strong>SAR-F1</strong>: the F1 score of the SAR class (label $1$), $F_1 = 2PR/(P+R)$, on the test split. Accuracy is useless here because only about $5\%$ of accounts are SAR.

## 1.2.xi Why constant scores inflate AUROC {#sec-mtp-toy}

This is the mechanism behind B2, so it is worth being able to do on a whiteboard.

<div class="nb nb-example nb-block" id="example-1-2-4">

<strong>Example 1.2.4</strong> (Zero-tied negatives)

An explainer scores the four edges that can influence a node as $0.80$ (the one positive), and $0.60$, $0.30$, $0.90$ (three negatives). The positive beats two of the three negatives, so $\mathrm{AUROC} = 2/3 = 0.667$. Now add $Z = 8$ further edges that cannot influence the prediction. The explainer leaves them at exactly $0$ and they are all negatives. The positive beats all eight of them as well: $\mathrm{AUROC} = (2 + 8)/(3 + 8) = 10/11 = 0.909$, although the explanation has not changed at all.

</div>

In general, if the genuine edges have $N$ negatives and AUROC $a$, and $Z$ zero-scored negatives are added (all genuine positives score above $0$), then

$$
\mathrm{AUROC}' = \frac{a N + Z}{N + Z}.
$$

This is only a first approximation: in AMLSim the extra edges also contain a few <em>positives</em> (the reverse copy of an alert edge, which cannot matter either), and those score $0$ and lose to every non-zero negative, which pulls the other way. The measured inflation, $0.48 \to 0.71$, is smaller than the formula would give for that reason ([Section 1.4.iii](../flaw/#sec-mtp-flawmech)).
