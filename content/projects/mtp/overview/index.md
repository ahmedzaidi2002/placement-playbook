---
title: "1.1 · Overview"
linkTitle: "1.1 Overview"
weight: 1
math: true
---
<div class="nb-proto">

<em><span>Prototypical example for this section:</span> the second bullet: a headline AUROC of $0.71$ on simulated bank transfers that falls to $0.48$, which is chance, once the scored edges are restricted to the ones that can influence the prediction.</em>

</div>

## 1.1.i The project in one minute {#s1-1-i}

A graph neural network (GNN) can flag a bank account as suspicious, but it returns only a score. An investigator needs evidence: which transfers, which neighbours made the model suspicious. Post-hoc explainers such as <strong>GNNExplainer</strong> [&#91;Yin+19&#93;](../references/#ref-ying2019) answer that by learning which edges the model relied on. The starting point was a previous M.Tech report from my lab on blockchain forensics (Pavitra Khare, December 2025), which ran a GCN plus GNNExplainer pipeline on four synthetic benchmarks and listed real data, a comparison with PGExplainer and temporal extensions as future work (robustness was not on its list). My project asks how far such explanations can be trusted, and it begins with the part everything else rests on: getting the measurement right.

What exists so far, in the order it was done:

1. A GCN [&#91;KW17&#93;](../references/#ref-kipf2017) and GNNExplainer written from the two papers on Cora, with the GCN layer checked bit for bit against PyTorch Geometric’s `GCNConv` ([Section 1.3](../cora/)).
2. A pipeline that trains a GCN on the four synthetic benchmarks of the GNNExplainer paper and scores the explanations against the planted motifs; it matches the paper’s numbers on two of the four, after finding a normalisation step that only the authors’ code contains ([Section 1.5](../synthetic/)).
3. IBM’s AMLSim money-laundering simulator, running on a cloud machine, as a testbed where the laundering patterns are planted and therefore known ([Section 1.6](../amlsim_setup/)).
4. A flaw in how explanation accuracy was being scored, found on AMLSim, which turned a headline AUROC of $0.71$ into $0.48$ ([Section 1.4](../flaw/)).
5. A 30-configuration sweep on AMLSim in which a two-layer GCN raised explanation AUROC from $0.48$ to $0.73$ and detection F1 from $0.13$ to $0.34$ ([Section 1.7](../sweep/)).

What does <em>not</em> exist yet: any experiment on real blockchain data (Elliptic, Ethereum), the PGExplainer comparison (planned, not started), and any adversarial attack on explanations (an earlier direction, set aside on 1 September 2026; see [Section 1.2.vi](../background/#sec-mtp-scope)).

## 1.1.ii The five resume bullets {#s1-1-ii}

The resume entry reads <em>GNN Explainability for Fraud Detection | M.Tech Project, Aug 2026 – Present</em>. The superscripts are the resume’s footnotes: $^{2}$ GCN is Graph Convolutional Network, $^{3}$ AUROC is Area Under the ROC Curve.

1. Building GCN$^2$ and GNNExplainer from source papers, verifying the hand-written GCN bit-exact vs. `GCNConv` and matching $81.5\%$ Cora accuracy (6-seed avg).
2. Diagnosing a GNN-explanation evaluation flaw that credits causally-irrelevant edges, correcting it and collapsing a headline $0.71$ AUROC$^3$ to $0.48$ (chance).
3. Reproducing GNNExplainer’s benchmarks on $2$ of $4$ synthetic datasets within $0.01$–$0.10$ AUROC of published targets by isolating an undocumented architecture detail.
4. Setting up IBM’s AMLSim simulator end-to-end on cloud infrastructure — building a Java dependency from source and pinning a legacy Python $3.8$ environment.
5. Running a $\sim$30-configuration sweep on simulated financial-crime graphs, lifting explanation AUROC $0.48\to0.73$ and detection F1 $0.13\to0.34$ ($2.6\times$).

The bullets are not in chronological order. B4 came first (31 August), B1 is the Cora project of 6 September, B2 was found at the start of the 12 September pass that also produced B5, and B3 is the synthetic re-run of 15 September. [Section 1.8](../wrapup/) has the dates.

## 1.1.iii The numbers at a glance {#s1-1-iii}

| Bullet | What the resume says | Exact value, and where it is measured | Evidence |
|:--|:--|:--|:--|
| B1 | $81.5\%$ | $0.8152$: mean test accuracy of the hand-written 2-layer GCN on Cora over seeds $42, 0, 1, 2, 3, 4$ (population s.d. $0.0079$); the paper reports $0.815$ | <span style="color:#009b55"><strong>[R]</strong></span> |
| B1 | bit-exact | maximum difference to `GCNConv` is exactly $0$ under `torch.equal`, for $6$ random layers $\times$ $3$ thread counts $\times$ (with, without) edge weights, and for the whole trained model | <span style="color:#009b55"><strong>[R]</strong></span> |
| B2 | $0.71$ | $0.7111 \pm 0.0082$: pooled AUROC of GNNExplainer on AMLSim (1-layer GCN, 3 simulations) when scoring <em>every edge between nodes within $k$ hops</em> | <span style="color:#0071bc"><strong>[F]</strong></span> <span style="color:#009b55"><strong>[R]</strong></span> |
| B2 | $0.48$ | $0.4832 \pm 0.0806$: the same trained models and masks, scoring only edges that can reach the prediction | <span style="color:#0071bc"><strong>[F]</strong></span> <span style="color:#009b55"><strong>[R]</strong></span> |
| B3 | $2$ of $4$ | BA-Shapes $0.829 \pm 0.063$ and BA-Community $0.844 \pm 0.012$ with the authors’ architecture (3 seeds $\times$ 100 nodes) | <span style="color:#0071bc"><strong>[F]</strong></span> <span style="color:#009b55"><strong>[R]</strong></span> |
| B3 | $0.01$–$0.10$ | distance to the two published targets per dataset: BA-Shapes $0.083$ and $0.096$ below; BA-Community $0.016$ and $0.008$ <em>above</em> | <span style="color:#0071bc"><strong>[F]</strong></span> |
| B4 | cloud, Java, Python $3.8$ | Lightning AI Studio; MASON 20 built with Maven; `networkx==1.11` needs Python $\le 3.8$ | <span style="color:#f7921d"><strong>[L]</strong></span> <span style="color:#009b55"><strong>[R]</strong></span> |
| B5 | $\sim$30 configurations | exactly $30$ configurations $\times$ $3$ simulations $=90$ trained models | <span style="color:#0071bc"><strong>[F]</strong></span> |
| B5 | $0.48\to0.73$ | $0.4832 \to 0.7344 \pm 0.0214$ (`gcn1` $\to$ `gcn2_rich`); on three fresh simulations $0.414\to0.731$ | <span style="color:#0071bc"><strong>[F]</strong></span> <span style="color:#009b55"><strong>[R]</strong></span> |
| B5 | $0.13\to0.34$ | $0.1271 \to 0.3393 \pm 0.0773$: test SAR-F1, same two configurations (on three fresh simulations: $0.097\to0.400$) | <span style="color:#0071bc"><strong>[F]</strong></span> <span style="color:#009b55"><strong>[R]</strong></span> |
| B5 | $2.6\times$ | $0.3393/0.1271 = 2.67$; see [Remark 1.1.1](#remark-1-1-1) | <span style="color:#0071bc"><strong>[F]</strong></span> |

This section exists so that nothing on the resume can surprise me in an interview. For each claim: what it literally says, what the evidence supports, and the wording I can safely use.

| Claim | What the evidence supports | Safe wording, and the catch |
|:--|:--|:--|
| B1 “bit-exact” | Holds literally: logits of the whole trained model are identical to those of a `GCNConv` twin, and the test accuracy is $0.8250$ for both ([Section 1.3.iv](../cora/#sec-mtp-bitexact)). | The project’s own check uses `allclose` with tolerance $10^{-6}$ and prints a maximum difference of $0$; the strict `torch.equal` test is mine. CPU only, same edge order, no bias. |
| B1 “matching $81.5\%$” | Mean $0.8152$ over six seeds, range $0.804$–$0.825$ | “Matches the paper’s $81.5\%$”, never “beats”. The saved checkpoint is seed 42 ($0.825$), the top of the range. |
| B2 “evaluation flaw” | The scored set contained edges that cannot influence the prediction and that PyG’s GNNExplainer sets to exactly $0$ ([Section 1.4.iii](../flaw/#sec-mtp-flawmech)) | “The scoring set was wrong; the explainer and the models were untouched.” |
| B2 “$0.71\to0.48$” | $0.7111\to0.4832$, same models and masks, only the scored edge set changed | “Chance” means indistinguishable from $0.5$: the three seeds are $0.560, 0.518, 0.372$. |
| B3 “$2$ of $4$” | The other two (Tree-Cycles, Tree-Grid) do not reproduce, and neither does the authors’ own released code ([Section 1.5.vi](../synthetic/#sec-mtp-synthfail)) | Say the count, and then say why. |
| B3 “within $0.01$–$0.10$” | BA-Shapes is $0.083$ and $0.096$ <em>below</em> the two targets; BA-Community is $0.016$ and $0.008$ <em>above</em> them | “Within” is an absolute distance; one BA-Shapes seed is at $0.912$, the others at $0.760$ and $0.817$. |
| B3 “undocumented detail” | Per-layer L2 normalisation of node embeddings, in the authors’ code and in neither the paper PDF nor the report ([Section 1.5.v](../synthetic/#sec-mtp-l2)) | Necessary: removing it drops BA-Shapes from $0.829$ to $0.600$ (the plain GCN has $0.463$). Sufficient on BA-Shapes: adding it alone to the plain GCN gives $0.896$ (a test I added on 2 October). Why it matters is untested. |
| B4 “cloud” | A Lightning AI Studio on the free CPU tier | Not a GPU cluster, not institute HPC. |
| B5 “$\sim$30 configurations” | Exactly $30$, three simulations each | Selection inside a configuration used validation data only. |
| B5 “$0.48\to0.73$ and $0.13\to0.34$” | Both for one configuration (`gcn2_rich`), the one with the highest explanation AUROC of the 30; others reach F1 $0.65$–$0.66$ but their explanation AUROC falls to $0.50$–$0.59$ | The test-split table was used to pick which of 30 to quote: a winner’s-curse risk, see [Section I picked one configuration out of thirty by looking at test-split numbers](../sweep/#sec-mtp-bestof30). Replicated on three fresh simulations ([Section A held-out replication on three new simulations](../sweep/#sec-mtp-fresh)): $0.41\to0.73$ and $0.10\to0.40$. F1 rests on only $7$–$9$ positive test nodes per simulation. |
| B5 “$2.6\times$” | $2.67\times$ unrounded | See [Remark 1.1.1](#remark-1-1-1). |
| Title “Fraud Detection” | No real blockchain graph has been used | An earlier resume version said “Blockchain Fraud Detection”; the data so far is synthetic benchmarks and simulated bank transfers. |

<div class="nb nb-remark" id="remark-1-1-1">

<strong>Remark 1.1.1</strong> (The $2.6\times$ versus $2.67$) — The resume prints $0.13 \to 0.34$ and $2.6\times$. The two printed numbers give $0.34/0.13 = 2.62$, so the resume is consistent with itself. The unrounded values are $0.3393/0.1271 = 2.67$, which rounds to $2.7$, and the project’s own write-up (`documentations/amlsim-v2-improvements.md`, section 7) says “$2.7\mathrm{x}$”. So $2.6\times$ is the floor of the exact ratio. If asked, say “about two and a half to two and three-quarter times”. Changing the resume to $2.7\times$ would make it match its own source.

</div>

<div class="nb nb-remark" id="remark-1-1-2">

<strong>Remark 1.1.2</strong> (The word “blockchain”) — The project started as <em>Explainable AI for Blockchain Fraud Detection</em>, because the baseline report is about blockchain forensics. Everything run so far uses either the synthetic benchmarks of the GNNExplainer paper or AMLSim, which simulates <em>bank</em> transfers. The real blockchain datasets on the list (Elliptic, Elliptic++, the Ethereum phishing network) have not been downloaded. If asked “where is the blockchain?”, the honest answer is that AMLSim is the closest testbed with exact ground truth, and the transfer to real chains is future work.

</div>

## 1.1.iv What I would not say {#s1-1-iv}

- That the project “improves” or “beats” GNNExplainer. I reproduced and re-measured it; I have not proposed a new explainer.
- That $0.73$ is a good absolute number. A trivial rule, “rank a node’s edges by how few transactions the two accounts share”, ranks the planted edges at $0.85$ for the one-hop models and at $0.80$ on the two-hop computation graph, above the explainer’s $0.73$ ([Section 1.7.vii](../sweep/#sec-mtp-heur); the two-hop check is one I ran on 2 October, not part of the original project). That is not a failure of the explainer, which reports what the <em>model</em> used and the model cannot see transaction counts, but it makes $0.73$ a weak absolute number.
- That the explainers work on real fraud. AMLSim is simulated, with a handful of hand-specified laundering patterns ([Section 1.6.ii](../amlsim_setup/#sec-mtp-amldata)).
- That the guide has approved a final direction. As of `CLAUDE.md` (27 September 2026) the topic is “ongoing, exploring”.
- That an explanation shows what is <em>true</em>. It shows what the <em>model</em> used.
