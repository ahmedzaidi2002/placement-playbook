---
title: "1.8 · The answers I should have ready"
linkTitle: "1.8 The answers I should have ready"
weight: 8
math: true
---
## 1.8.i Ten seconds {#s1-8-i}

I am measuring how far explanations of GNN fraud predictions can be trusted, and so far I have found and fixed a flaw in how they are scored, reproduced a published explainer benchmark, and built a simulated-bank testbed with known laundering patterns.

## 1.8.ii One minute {#s1-8-ii}

GNNs can flag suspicious accounts but give only a score; investigators need the evidence, so post-hoc explainers such as GNNExplainer extract the few transfers the model relied on. Building on a previous report from my lab, I (1) wrote a GCN and GNNExplainer from the two papers and checked the GCN layer bit for bit against PyTorch Geometric; (2) reproduced the explainer’s benchmark on two of four synthetic datasets, after finding a normalisation step that is in the authors’ code but not in the paper; (3) set up IBM’s AMLSim, which plants known laundering patterns in simulated bank transfers; and (4) found that my scoring counted edges that cannot influence the prediction, which had inflated an AUROC of $0.48$ to $0.71$. With that fixed, a sweep of $30$ model configurations showed that a two-layer GCN on richer features lifts explanation AUROC from $0.48$ to $0.73$ and detection F1 from $0.13$ to $0.34$.

## 1.8.iii Two minutes: add these three things {#s1-8-iii}

- <strong>What I would flag as uncertain, unprompted:</strong> the F1 rests on seven or eight positive test nodes per simulation; I quoted the best of thirty configurations by looking at test-split numbers; and $0.73$ is below what trivial rankings score: ranking edges by how few transactions the two accounts share gives $0.85$ at one hop and $0.80$ at two hops (a check I added on 2 October), because the planted alerts are one-off transfers.
- <strong>What it is not:</strong> no real blockchain data yet, no new explainer, and the topic is not formally fixed with my guide.
- <strong>What is next:</strong> a model-randomisation test and edge betweenness as a further control on the two-layer models; an audit of whether AMLSim’s alerts really have the shapes they are labelled with; a PGExplainer comparison under the same protocol; and, later, a real dataset such as Elliptic.

<div class="nb nb-remark" id="remark-1-8-1">

<strong>Remark 1.8.1</strong> (Process and tooling) — The code was developed with Claude Code as the coding assistant, and the project’s `CLAUDE.md` describes that workflow. In an interview I should be ready to say so plainly and, more importantly, to explain any function, any equation and any number in this chapter <em>without</em> the assistant: that is what this chapter is for. What I must be able to defend are the choices (which evaluation to trust, what to re-run, what to call a result and what to call an artefact), the reading of the papers and of the authors’ code, and the checks in [Section 1.3.ix](../cora/#sec-mtp-checks) and [Section 1.1](../overview/).

</div>

## 1.8.iv Rapid-fire answers {#sec-mtp-rapid}

| Question | One-line answer |
|:--|:--|
| What is a GCN layer? | $H' = \sigma(\hat A H W)$, $\hat A = \tilde D^{-1/2}(A+I)\tilde D^{-1/2}$: average yourself and your neighbours, transform, apply ReLU. |
| How many hops does an $L$-layer GCN see? | Exactly $L$; the $3$-hop feature-perturbation test leaves a $2$-layer model’s logits bit for bit unchanged. |
| What does GNNExplainer optimise? | A soft edge mask $\sigma(M)$ that keeps the model’s <em>predicted</em> class, plus a size penalty and an entropy penalty, with the model frozen. |
| Why the entropy term? | It pushes every mask value to $0$ or $1$, so “kept or not” is well defined. |
| Computation graph? | The edges that can carry a message to the node within $L$ layers: those whose receiver is within $L-1$ hops of it. |
| Induced $k$-hop subgraph? | Every edge between nodes within $k$ hops; larger than the computation graph, and what PyG’s `k_hop_subgraph` returns. |
| The flaw in one sentence? | Scoring the induced set counted edges that cannot influence the prediction and that PyG sets to exactly $0$, inflating AUROC: $0.71$ became $0.48$. |
| What is AUROC? | The probability that a random positive edge outranks a random negative one, ties counting a half; $0.5$ is chance. |
| Pooled or per-node? | Pooled: one AUROC over all explained nodes’ edges (the headline); per-node averages one AUROC per node. |
| Fidelity$^+$? | The share of explained nodes whose prediction changes when the explanation is removed (messages weighted $1-m_e$). |
| SAR? | Suspicious activity report: here, the label of an account belonging to a planted alert. |
| Why F1 and not accuracy? | Only about $5\%$ of accounts are SAR; “always licit” scores $95\%$ accuracy. |
| The label leak? | `prior_sar_count` is true for every SAR account ($72/72$) and almost none of the others; dropped before training. |
| Why one edge per account pair? | $121{,}457$ transactions collapse to $6984$ pairs; per-transaction edges make the mask $17\times$ bigger for no extra truth. |
| What is `gcn2_rich`? | A $2$-layer GCN on $20$ transaction-derived features. |
| Its numbers? | Explanation AUROC $0.734$, test F1 $0.339$, Fidelity$^+$ $0.68$; baseline $0.483$, $0.127$, $0.49$. |
| The trade-off? | Every configuration with F1 above $0.5$ has explanation AUROC $0.50$–$0.61$: good features let the model ignore the alert edges. |
| The undocumented detail? | Per-layer L2 normalisation of node embeddings in the authors’ model; removing it costs $0.23$ AUROC on BA-Shapes, and adding it alone to a plain GCN lifts $0.46$ to $0.90$ there (half the gap on BA-Community, nothing reliable on Tree-Cycles). |
| Which benchmarks reproduced? | BA-Shapes ($0.829$) and BA-Community ($0.844$); Tree-Cycles and Tree-Grid do not, and neither does the authors’ code. |
| Why does Tree-Cycles fail? | The explainer keeps a small <em>sufficient</em> part of the cycle and the rest is noise at a common floor. |
| Why Python $3.8$? | AMLSim pins `networkx==1.11`, which imports `fractions.gcd`, removed in Python $3.9$. |
| Why build MASON from source? | No binary exists; a zip export drops the LFS-stored `pom.xml` and jars; so clone with LFS, `mvn package`, `install:install-file`. |
| What was the Windows bug? | `csv.writer` plus text-mode files gave `\r\r\n`; Java saw blank lines; `newline=""` fixed it. |
| Does it replicate on new data? | Three fresh simulations, configurations fixed in advance: baseline AUROC $0.414$ and F1 $0.097$; `gcn2_rich` $0.731$ and $0.40$; plain `gcn2` only $0.44$. |
| Is $0.73$ good? | Far above chance, but below a one-line rule: fewer transactions on the pair scores $0.80$ on the two-hop edges ($0.85$ at one hop), lower sender degree $0.77$. The GCN cannot see those counts, so this is not a failure of the explainer. |
| What is missing? | Real data, model randomisation, edge betweenness, an alert-shape audit, PGExplainer. |

- <strong>No real data.</strong> Everything is synthetic (benchmarks, AMLSim). AMLSim has three hand-specified alert shapes and a strong, simple signature (few repeated transfers, low-degree counterparties).
- <strong>The explainers.</strong> Only GNNExplainer, with untuned PyG defaults; no PGExplainer, no other method. A GNNExplainer explanation describes what the <em>model</em> used, is non-convex and seed-dependent, and need not be connected.
- <strong>Small positive classes.</strong> $65$, $60$ and $63$ alert transactions per simulation; $7$ or $8$ positive test nodes. Standard deviations over $3$ simulations are rough.
- <strong>Selection.</strong> One configuration quoted out of thirty on test-split numbers ([Section I picked one configuration out of thirty by looking at test-split numbers](../sweep/#sec-mtp-bestof30)). A held-out check on three fresh simulations ([Section A held-out replication on three new simulations](../sweep/#sec-mtp-fresh)) reproduced its AUROC ($0.731$ against $0.734$); the other twenty-nine configurations were not re-run there.
- <strong>Ground truth.</strong> For two-layer models, $28\%$ of scored positives belong to a neighbouring alert ([Section The ground truth counts other alerts’ edges as positive (two-layer models)](../sweep/#sec-mtp-ownalert)); AMLSim’s realised alert shapes have not been audited against their labels.
- <strong>Controls.</strong> Model-free rankings beat the explainer at both depths (checked at two hops only on 2 October); model randomisation and edge betweenness have not been run.
- <strong>Reproducibility.</strong> The synthetic pipeline and the one-layer linear baseline reproduce exactly across the two environments; every AMLSim configuration with a hidden non-linearity moves (F1 by up to $0.06$, AUROC by up to $0.04$; [Section Sensitivity to the software environment](../sweep/#sec-mtp-envdiff)).
- <strong>Two datasets not reproduced</strong> (Tree-Cycles, Tree-Grid), and the authors’ code cannot reproduce them either.
- <strong>Scope.</strong> The direction is not formally fixed with the guide; AMLSim’s adoption is not confirmed.

| Cora GCN (B1) | $2$ layers, hidden $16$, dropout $0.5$ on the input of both layers, Adam lr $0.01$, weight decay $5\cdot10^{-4}$ on layer $1$ only, $200$ epochs, early stopping patience $10$ on validation loss (never triggered), Glorot init, no bias; seeds $42, 0, 1, 2, 3, 4$ |
|:--|:--|
| Cora explainer (B1) | Adam lr $0.01$, $300$ epochs, coefficients $0.005$ (edge size, sum), $1.0$ (edge entropy), $1.0$ (feature size), $0.1$ (feature entropy), mask init $0.1\cdot \mathcal N(0,1)$, threshold $0.5$, target = predicted class, seed $42$ |
| Synthetic, “paper” model (B3) | $3$ layers, hidden $20$, sum aggregation, no self-loops, bias, L2-normalised embeddings after every layer, ReLU, concatenated readout, Adam lr $0.001$, weight decay $0.005$, clip $2.0$, $1000$ epochs, stratified $80/10/10$, selection by validation accuracy (ties: validation loss) |
| Synthetic, Kipf model (B3) | $3$ layers, hidden $32$, self-loops and symmetric normalisation, no dropout, Adam lr $0.01$, no weight decay; otherwise as above |
| Synthetic explainer (B3) | PyG `GNNExplainer`, $200$ epochs, defaults (lr $0.01$, edge size $0.005$ on a sum, edge entropy $1.0$), `'model'`, edges only; $100$ seeded random motif nodes $\times$ $3$ seeds |
| AMLSim simulator (B4) | `paramFiles/1K`: $1446$ accounts, $3+3+4$ planted alerts, $720$ steps from $2017$-$01$-$01$; seeds $0,1,2$ (and $3,4,5$ for the replication) |
| AMLSim classifiers (B5) | hidden $32$, Adam lr $0.01$, no weight decay, no dropout, clip $2.0$, $1000$ epochs, inverse-frequency class weights, stratified node split $80/10/10$, selection by validation SAR-F1 (ties: validation loss) |
| AMLSim explainer (B5) | PyG `GNNExplainer`, $200$ epochs, defaults, `'model'`, edges only; every SAR node ($72, 67, 70$); scored on the computation graph |

Dates from `CLAUDE.md` (the changelog) and the files’ own timestamps.

| 2026-08-16 | Four candidate ideas drafted for the guide; resume framing locked. |
|:--|:--|
| 2026-08-26 | Hub context file `CLAUDE.md` first written (baseline report, peers, datasets, API notes). |
| 2026-08-27 | PyG environment on a Lightning Studio; BA-Shapes baseline (a first version of B3; its numbers were later superseded). |
| 2026-08-28 | GNNExplainer paper read in detail. |
| 2026-08-31 | <strong>B4:</strong> AMLSim built and verified on the Studio; first Phase-1 run on AMLSim, headline $0.7111$. |
| 2026-09-01 | Scope cut to Phase 0–1; attack/defence prototype deleted. |
| 2026-09-06 | <strong>B1:</strong> Cora clean-room GCN and GNNExplainer built and run. |
| 2026-09-12 | <strong>B2, B5:</strong> evaluation flaw found ($0.7111\to0.483$); $30$-configuration sweep; `amlsim-v2-improvements.md`. |
| 2026-09-15 | <strong>B3:</strong> four synthetic datasets re-run under the corrected protocol; Cora six-seed accuracy and connectivity flag; AMLSim review (own-alert); implementation folders consolidated. |
| 2026-09-22/23 | Explainer landscape and PGExplainer reproducibility reports read; PGExplainer analysis and plan written (nothing implemented). |
| 2026-09-27 | Authors’ GNNExplainer code run unmodified on all four benchmarks. |
| 2026-09-30 | Research note on prior work and architecture for GNNExplainer/PGExplainer on AMLSim. |
| 2026-10-02 | AMLSim rebuilt on the Windows laptop; the numbers in this chapter marked <span style="color:#009b55"><strong>[R]</strong></span> re-checked; new in these notes (not in the project’s own results): a held-out replication on three fresh simulations, a model-free control at two hops, the sufficiency test of the L2 step, the torchmetrics sigmoid finding. |

Project folder: the local working copy `MTech project(Phase 1)/` of the project. Snapshots in `data/mtp/src/` (verbatim, CRLF normalised) and where they come from:

| Snapshot | Original (relative to `MTech project(Phase 1)/`) |
|:--|:--|
| `cora_gcn.py`, `cora_train.py`, `cora_explain.py`, `cora_config.py` | `final implementations/GCN and GNNexplainer/src/{gcn,train,explain,config}.py` |
| `cora_sanity.py` | `final implementations/GCN and GNNexplainer/scripts/run_sanity_checks.py` |
| `syn_datasets.py`, `syn_train_gcn.py`, `syn_run_experiment.py` | `implementations/gcn_gnnexplainer/{datasets,train_gcn,run_experiment}.py` |
| `aml_dataset.py`, `aml_evaluation.py`, `aml_training.py`, `aml_models.py`, `aml_rich_features.py`, `aml_run_configs.py`, `aml_sanity_edge_sets.py` | `implementations/amlsim/{amlsim_dataset,evaluation,training,models,rich_features,run_configs,sanity_check_edge_sets}.py` |
| `authors_models.py` | `implementations/authors_gnnexplainer/repo_47e6973/models.py` (the authors’ repository, commit `47e6973`) |
| Result files used | `results/amlsim/{summary.md,configs/*.json,logs/*.log}`, `results/gcn_gnnexplainer/combined_results.json`, `results/authors_gnnexplainer/summary.md`, `final implementations/GCN and GNNexplainer/results/` |
| Project notes used | `CLAUDE.md`; `documentations/{amlsim-gcn+GNNexplainer, amlsim-v2-improvements, gcn_gnnexplainer, research-amlsim-explainers-2026-09, pgexplainer-analysis-and-plan}.md`; the Cora `docs/` |
| AMLSim | `AMLSim/` (clone of `IBM/AMLSim`, five lines patched; `outputs/` holds simulations $0$–$5$) |
| Re-run scripts of 2 October | `data/mtp/verify/` in these notes |
| Regenerating the tables | `data/mtp/make_data.py` |

Other tools: Maven and MASON under `%USERPROFILE%\tools`; the Lightning Studio holds the original simulator outputs and the August to September code (`amlsim_v2/`).

## 1.8.v Software environments {#s1-8-v}

Different experiments ran in different environments, which matters for reproducibility ([Section Sensitivity to the software environment](../sweep/#sec-mtp-envdiff)).

| Experiment | Environment |
|:--|:--|
| Cora (B1), synthetic benchmarks (B3), my re-runs of 2 October | Windows laptop, CPU, Python $3.13.7$, `torch 2.11.0+cpu`, PyG $2.8.0.\mathrm{post1}$ |
| AMLSim sweep (B2, B5) and the AMLSim simulations of the logged runs | Lightning Studio (CPU), conda env `cloudspace` with `torch 2.8.0`, PyG $2.8.0$ (it had been $2.4.1$/$2.6.1$ in August; the August pipeline re-ran unchanged under $2.8.0$ and reproduced every number) <span style="color:#f7921d"><strong>[L]</strong></span>; AMLSim itself in env `amlsim` (Python $3.8$, Java $21$) |
| Authors’ released GNNExplainer code ([Section 1.5.vii](../synthetic/#sec-mtp-authorsrun)) | laptop, Python $3.8$ from `uv`, `torch 1.6.0+cpu`, `networkx 2.4`, `tensorboardX 1.9` and period versions of the rest |

- <strong>GNN, GCN</strong>: graph neural network; graph convolutional network (Kipf and Welling), a GNN whose layer is $\sigma(\hat A H W)$.
- <strong>Message passing</strong>: each layer sends a vector along every edge and sums at the receiver. <strong>Receptive field</strong>: the nodes that can influence a node’s output ($L$ hops for $L$ layers).
- <strong>Computation graph</strong> $G_c$: the nodes and edges that can influence one prediction ([Proposition 1.2.1](../background/#proposition-1-2-1)). <strong>Induced $k$-hop subgraph</strong>: every edge among the nodes within $k$ hops; larger than $G_c$.
- <strong>Post-hoc explainer</strong>: explains a trained model without changing it. <strong>GNNExplainer</strong>: learns a soft edge mask by gradient descent. <strong>PGExplainer</strong> [&#91;Luo+20&#93;](../references/#ref-luo2020): learns a small network that predicts masks, trained once and applied to new instances (planned, not done).
- <strong>Mask</strong>, <strong>hard mask</strong>: the learned edge weights in $(0,1)$; PyG’s boolean mask of entries that received a gradient.
- <strong>Planted motif</strong>, <strong>ground truth</strong>: structure inserted by the generator, whose edges are the “correct” explanation.
- <strong>AUROC</strong>, <strong>pooled</strong>, <strong>per-node</strong>: see [Section 1.2.x](../background/#sec-mtp-metrics). <strong>Tie</strong>: equal scores.
- <strong>Fidelity$^\pm$</strong>, <strong>characterisation score</strong>: see [Section 1.2.x](../background/#sec-mtp-metrics).
- <strong>SAR</strong>: suspicious activity report; here, the label of an account that belongs to a planted alert. <strong>Alert</strong>: one planted laundering pattern (fan-in, fan-out or cycle).
- <strong>Fan-in / fan-out / cycle</strong>: many accounts pay one account / one account pays many / money returns to its origin.
- <strong>MASON</strong>: Java multi-agent simulation toolkit under AMLSim. <strong>Maven</strong>: Java build tool. <strong>Git LFS</strong>: stores large files outside the repository and leaves small pointer files in it.
- <strong>Leak</strong>: a feature that encodes the label (here `prior_sar_count`). <strong>Winner’s curse</strong>: the best of many noisy trials overstates the true performance.
- <strong>Transductive</strong>: the whole graph is visible during training; only some labels are used.

Everything marked <strong>UNKNOWN</strong> or not yet run, in one place.

1. Whether the baseline report’s Table 5.1 comes from its author’s runs or was quoted from the paper.
2. Why six seeds were used for the Cora accuracy.
3. The reason the August script measured $93$–$95\%$ for the $3$-hop neighbourhood where the September script and my re-run give $97\%$ (the August script is on the Studio only).
4. <em>Why</em> per-layer L2 normalisation matters for explainability; and whether it is sufficient on its own (the result of adding it to a Kipf GCN is in [Section 1.5.v](../synthetic/#sec-mtp-l2)).
5. Whether `gcn2_rich`’s explanation AUROC survives a model-randomisation test, and how it compares with edge betweenness (the degree and transaction-count rules are answered: they score higher, [Section The same control at two hops (new: run on 2 October for these notes; not part of the project’s own results)](../sweep/#sec-mtp-heur2)).
6. Whether the planted alerts really form their declared shapes in AMLSim’s output (an audit is planned).
7. Whether any of this transfers to real transaction graphs (Elliptic and others: not run).
8. Whether the guide approves AMLSim and the final topic.
9. The script behind the earlier L2 ablation ($0.455\to0.807\to0.477$) and the earlier “faithful port” of the authors’ code: neither was saved.
10. Whether Tree-Cycles and Tree-Grid can be reproduced by any pipeline at all.

<div class="nb nb-problem nb-block" id="problem-1a">

<strong>Problem 1A</strong>

Give the two-minute version of the project to someone who does not know graph neural networks, and then say the three things you are least sure of.

<details class="nb-hint">
<summary>Hint</summary>

Account $\to$ transfers $\to$ score $\to$ evidence. Uncertainty: sample size, selection, controls.

</details>

<details class="nb-sol">
<summary>Solution</summary>

See [Section 1.8](#). A bank’s model gives each account a suspicion score; an explainer says which transfers it relied on; I measure how well those explanations recover laundering patterns that a simulator planted. Least sure: (i) the F1 gain rests on seven or eight positive test accounts per simulation; (ii) I quoted the best of thirty configurations; (iii) a trivial ranking (few transactions on the pair) scores higher than the explainer, $0.80$ against $0.73$ at two hops.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-1b">

<strong>Problem 1B</strong>

Derive $\hat A = \tilde D^{-1/2}\tilde A\tilde D^{-1/2}$ for the path $0 - 1 - 2$ and apply it to $X = (1, 0, 4)^\top$. Why do we add the identity, and why normalise symmetrically rather than by $\tilde D^{-1}$?

<details class="nb-hint">
<summary>Hint</summary>

$\tilde A = A + I$ has degrees $(2,3,2)$. Entry $(i,j)$ of $\hat A$ is $1/\sqrt{\tilde d_i\tilde d_j}$ on edges.

</details>

<details class="nb-sol">
<summary>Solution</summary>

$\hat A = \left(\begin{smallmatrix}1/2 & 1/\sqrt6 & 0\\ 1/\sqrt6 & 1/3 & 1/\sqrt6\\ 0 & 1/\sqrt6 & 1/2\end{smallmatrix}\right)$, so $\hat A X = (0.5,\; 5/\sqrt6 = 2.041,\; 2.0)^\top$. The identity lets a node keep its own features. Dividing by $\sqrt{\tilde d_i\tilde d_j}$ rather than by the receiver’s degree alone makes the operator symmetric and penalises <em>both</em> a high-degree sender and a high-degree receiver; the row-normalised $\tilde D^{-1}\tilde A$ is a plain average, which ignores the sender’s degree and is not symmetric.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-1c">

<strong>Problem 1C</strong>

Count the trainable parameters of the Cora GCN ($1433$ features, $16$ hidden units, $7$ classes, no bias), and say how many of them weight decay acts on.

<details class="nb-hint">
<summary>Hint</summary>

Two weight matrices. Weight decay is applied to the first layer only.

</details>

<details class="nb-sol">
<summary>Solution</summary>

$1433\cdot16 + 16\cdot7 = 22{,}928 + 112 = 23{,}040$. Weight decay ($5\cdot10^{-4}$) acts on the first matrix, $22{,}928$ parameters (`cora_train.py:57-64`).

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-1d">

<strong>Problem 1D</strong>

The six Cora seeds gave test accuracies $0.825, 0.804, 0.816, 0.825, 0.813, 0.808$. Compute the mean, the population standard deviation and the sample standard deviation. Which one does the project’s “$\pm0.008$” use, and is it “matching $81.5\%$”?

<details class="nb-hint">
<summary>Hint</summary>

Sum $= 4.891$.

</details>

<details class="nb-sol">
<summary>Solution</summary>

Mean $= 4.891/6 = 0.8152$. Squared deviations sum to $3.75\cdot10^{-4}$, so the population s.d. is $\sqrt{3.75\cdot10^{-4}/6} = 0.0079$ and the sample s.d. is $\sqrt{3.75\cdot10^{-4}/5} = 0.0087$. The “$\pm0.008$” is the population value. Yes, $0.8152$ equals the paper’s $0.815$ to three digits; but a single seed can be $0.011$ away in either direction, and the saved checkpoint ($0.825$) is the top of the range.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-1e">

<strong>Problem 1E</strong>

What does “bit-exact against `GCNConv`” mean, how did you check it, and what would make it fail?

<details class="nb-hint">
<summary>Hint</summary>

`allclose` against `equal`; same operations in the same order.

</details>

<details class="nb-sol">
<summary>Solution</summary>

Every float of the output is identical. The project’s test uses `allclose` with tolerance $10^{-6}$ and prints a maximum difference of $0$; I added `torch.equal` over six random layers $\times$ three thread counts $\times$ with and without edge weights, and over the whole trained model (logits identical, accuracy $0.8250$ for both). It holds because both compute $XW$, add self-loops, sum degrees with a scatter, take $d^{-1/2}$, multiply and scatter-sum in the same order. It would fail, at the $10^{-7}$ level, with a different edge order, on a GPU, or with a bias.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-1f">

<strong>Problem 1F</strong>

Show that minimising the mean binary entropy of $\sigma(m)$ drives a mask value above $0.5$ up and one below $0.5$ down. Why does GNNExplainer want that?

<details class="nb-hint">
<summary>Hint</summary>

$H(p) = -p\log p - (1-p)\log(1-p)$; differentiate in $p$.

</details>

<details class="nb-sol">
<summary>Solution</summary>

$\dfrac{dH}{dp} = \log \dfrac{1-p}{p}$, which is negative for $p>0.5$ and positive for $p<0.5$. Gradient descent moves $p$ against the gradient: up if $p>0.5$, down if $p<0.5$, so values are pushed to $1$ or $0$. The size term alone only pushes masks toward $0$; the entropy term makes the result binary, so that “kept or not” is well defined and the threshold is not a delicate choice (on node $1786$ every value ended above $0.86$ or below $0.07$).

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-1g">

<strong>Problem 1G</strong>

Directed graph with edges $a\to t$, $d\to t$, $b\to a$, $e\to d$, $a\to d$, $c\to b$. Which edges are in the computation graph of $t$ for a one-layer and for a two-layer message-passing network? Which edge would a $3$-layer network add?

<details class="nb-hint">
<summary>Hint</summary>

Keep an edge $u\to v$ iff $v$ can reach $t$ in at most $L-1$ steps.

</details>

<details class="nb-sol">
<summary>Solution</summary>

$L=1$: only edges whose receiver is $t$: $a\to t$, $d\to t$. $L=2$: receivers that reach $t$ in at most one step are $t$, $a$, $d$, so also $b\to a$, $e\to d$, $a\to d$ (five edges); $c\to b$ is excluded because $b$ needs two steps. $L=3$: $b$ now reaches $t$ in two steps ($b\to a\to t$), so $c\to b$ joins.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-1h">

<strong>Problem 1H</strong> 🌶

On the edges that can influence a node, an explainer gives the two positive edges the scores $0.9$ and $0.4$ and the three negative edges $0.7$, $0.2$ and $0.5$. Compute the AUROC. Now add $6$ edges that cannot influence the node, all negatives, all with score exactly $0$. Compute the new AUROC. Then say why this inflates AUROC although nothing about the explanation changed, and what pulls the other way in AMLSim.

<details class="nb-hint">
<summary>Hint</summary>

Count the (positive, negative) pairs the positive edges win; ties count $\tfrac12$.

</details>

<details class="nb-sol">
<summary>Solution</summary>

Before: $0.9$ beats all three negatives ($3$ wins) and $0.4$ beats only $0.2$ ($1$ win): $4$ of $6$ pairs, AUROC $0.667$. After: both positives also beat all six zeros, which adds $12$ wins and $12$ pairs: $16/18 = 0.889$. The general formula is $(aN + Z)/(N+Z)$ with $a$ the original AUROC, $N$ the original number of negatives and $Z$ the zero-scored ones ($(2+6)/9 = 0.889$ here). It inflates because every genuine positive outranks a constant block of negatives for free. In AMLSim the extras also include positives (the reverse copy of an alert edge) which score $0$ and lose to every non-zero negative, so the measured inflation ($0.48\to0.71$) is smaller than the formula alone suggests.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-1i">

<strong>Problem 1I</strong>

Why does PyG’s `GNNExplainer` give <em>exactly</em> $0$ to edges outside the computation graph, and how did you verify it? What would break the equivalence?

<details class="nb-hint">
<summary>Hint</summary>

Gradient at the first step; where is the mask multiplied?

</details>

<details class="nb-sol">
<summary>Solution</summary>

It stores `hard_edge_mask = edge_mask.grad != 0` after the first optimisation step and sets every other entry to $0.0$ in post-processing. An edge outside $G_c$ gets exactly zero gradient because PyG multiplies the <em>message</em> by the mask after normalisation, so the mask does not enter any degree. I checked that the set of non-zero entries equals the computation graph for six SAR nodes at depths $1$–$3$ ($18$ of $18$), and for every SAR node of simulation $0$ at depths $1$ and $2$ ([Section 1.4.iv](../flaw/#sec-mtp-alltest)). A hand-written explainer that feeds the mask in as an edge weight <em>before</em> the degrees are computed would break it, because removing an edge changes its endpoints’ degrees and therefore other messages.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-1j">

<strong>Problem 1J</strong>

You believed $0.71$ in August. What was the line of reasoning, where was the error, and what would have caught it earlier?

<details class="nb-hint">
<summary>Hint</summary>

Why does a depth sweep that improves AUROC deserve suspicion?

</details>

<details class="nb-sol">
<summary>Solution</summary>

A $3$-layer model scored below chance, I showed that its $3$-hop neighbourhood was almost the whole graph, and a depth sweep made the number rise monotonically as the neighbourhood shrank: $0.42$, $0.57$, $0.71$. That looked like a principled fix, but I had changed the model to change the evaluation and had not asked which scored edges could reach the prediction. Counting that on 12 September showed that two thirds of the one-layer scored set were edges that cannot matter and were tied at zero. What would have caught it: checking the tie structure of the scores, a random baseline on the same set, and the question “can this edge influence this output?” for the scored set.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-1k">

<strong>Problem 1K</strong>

Pooled versus per-node AUROC: define both, say which one the headline is, and say what each can hide. Use the `gcn1` and `gcn2_rich` values ($0.4832$ and $0.5000$; $0.7344$ and $0.7834$).

<details class="nb-hint">
<summary>Hint</summary>

One concatenated edge list against an average over nodes.

</details>

<details class="nb-sol">
<summary>Solution</summary>

Pooled: concatenate all explained nodes’ scored edges and compute one AUROC, which is the paper’s framing and the headline; it is dominated by nodes with many edges (hubs). Per-node: one AUROC per node (nodes with a single class skipped) and then the mean, which weights every node equally, is noisy for nodes with only a few edges, and does not require mask values to be comparable across nodes, which the pooled version does. The two differ here by $0.02$ for the baseline and $0.05$ for `gcn2_rich`; reporting only one would hide how much the hubs matter.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-1l">

<strong>Problem 1L</strong>

Which two datasets did you reproduce, which two did not, and what are the distances to both targets? Why would a “pass” on two of four be a fair thing to put on a resume?

<details class="nb-hint">
<summary>Hint</summary>

BA-Shapes $0.8294$, BA-Community $0.8439$; targets $0.912$ and $0.925$, $0.828$ and $0.836$.

</details>

<details class="nb-sol">
<summary>Solution</summary>

Reproduced: BA-Shapes ($0.083$ and $0.096$ below the two targets, with seeds $0.760, 0.817, 0.912$) and BA-Community ($0.016$ and $0.008$ above). Not reproduced: Tree-Cycles ($0.552$ against $0.948$) and Tree-Grid ($0.584$ against $0.875$); the authors’ released code cannot reproduce them either ($0.647$, $0.671$ after fixing its scorer), and an independent reproduction measured $0.540$ on Tree-Cycles. It is fair because the claim states the count and the tolerance, and because the failures are documented as failures of the published numbers and not of my pipeline alone.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-1m">

<strong>Problem 1M</strong> 🌶

What is the undocumented architecture detail, where exactly is it, how did you establish that it matters, and what does your evidence <em>not</em> show?

<details class="nb-hint">
<summary>Hint</summary>

Two lines in `GraphConv.forward`; one-at-a-time ablation on BA-Shapes.

</details>

<details class="nb-sol">
<summary>Solution</summary>

Per-layer L2 normalisation of node embeddings: `y = F.normalize(y, p=2, dim=2)` when `normalize_embedding` is set (`authors_models.py:77-78`), switched on for every layer by `GcnEncoderGraph` (`authors_models.py:120`). The paper PDF and the baseline report do not mention it. Evidence: on BA-Shapes ($3$ seeds $\times$ $100$ nodes) the authors’ architecture scores $0.829$, the same architecture without the L2 step $0.600$, and a plain Kipf GCN $0.463$; the L2 step accounts for $63\%$ of the gap. In the other direction, adding <em>only</em> the L2 step to the Kipf GCN gives $0.896 \pm 0.025$ on BA-Shapes (a test I added on 2 October; on BA-Community $0.790$ against $0.731$ and $0.844$, on Tree-Cycles no reliable change). It does not show that the other differences are irrelevant (the remaining $37\%$ of the first gap comes from sum aggregation without self-loops or normalisation, the concatenated readout and the training settings, which I did not separate), nor <em>why</em> the L2 step matters.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-1n">

<strong>Problem 1N</strong>

Why does GNNExplainer score near chance on Tree-Cycles although the classifier is $99.6\%$ accurate?

<details class="nb-hint">
<summary>Hint</summary>

Think about <em>sufficient</em> subsets, and what the ground truth asks for.

</details>

<details class="nb-sol">
<summary>Solution</summary>

The objective asks for a small subset of the neighbourhood that preserves the prediction. About $4$ or $5$ of a node’s $\approx10$ cycle edges suffice, so the size term drives the other cycle edges and all tree edges to a common floor of about $0.07$; under Adam every edge whose gradient points downward moves the same distance, so the order inside the floor is noise. The ground truth says “the whole cycle”, so recall is about half and the AUROC is decided by that noise. Accuracy and explainability are different properties: the model need not rely on every edge of the motif.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-1o">

<strong>Problem 1O</strong>

Why did downloading MASON as a zip from GitHub fail with “non-parseable POM”, and what is the sequence of commands that works?

<details class="nb-hint">
<summary>Hint</summary>

What does a Git LFS pointer file look like?

</details>

<details class="nb-sol">
<summary>Solution</summary>

The repository stores `pom.xml` and the jars with Git LFS. A zip export contains only the pointer files (a few lines of text starting `version https://git-lfs`), which Maven tries to parse as XML. The fix is a real clone with `git-lfs` (`git clone --branch v20`), then `mvn -pl mason -am package` to build `mason-20.jar`, then `mvn install:install-file -DgroupId=mason -DartifactId=mason -Dversion=20 -Dpackaging=jar` so that AMLSim’s `pom.xml` finds it; on Windows add `-DpomFile=` with a standalone pom, because the embedded one names a parent that Maven Central does not have.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-1p">

<strong>Problem 1P</strong>

Why does AMLSim force Python $\le 3.8$? Show how you would demonstrate it in two commands.

<details class="nb-hint">
<summary>Hint</summary>

`networkx==1.11`, `fractions.gcd`.

</details>

<details class="nb-sol">
<summary>Solution</summary>

AMLSim pins `networkx==1.11` (the README says version $2$ is too slow on large graphs); that version executes `from fractions import gcd`, which was removed in Python $3.9$. In a Python $3.13$ environment `python -c "import networkx"` raises `ImportError: cannot import name 'gcd' from 'fractions'`; with a $3.8$ interpreter `python -c "import fractions; print(hasattr(fractions,'gcd'))"` prints `True`.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-1q">

<strong>Problem 1Q</strong> 🌶

The Java simulator died on Windows with “Index 5 out of bounds for length 1”. Explain the cause from the bytes `13 13 10` and the CSV header.

<details class="nb-hint">
<summary>Hint</summary>

How many columns does the header have? What does a Java line reader do with `\r\r\n`?

</details>

<details class="nb-sol">
<summary>Solution</summary>

The header has seven columns (`ACCOUNT_ID, ..., IS_SAR, BANK_ID`); index $5$ is `IS_SAR`. Python’s `csv.writer` ends rows with `\r\n`; opening the file in text mode on Windows turns the `\n` into `\r\n`, giving `\r\r\n`. Java’s line reader treats a lone `\r` as a line end, so there is an empty line after every row; splitting an empty line yields one column, and reading column $5$ throws. `open(f, "w", newline="")` stops the translation.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-1r">

<strong>Problem 1R</strong>

Why is the test F1 so noisy, and how much can one node move it? Use `gcn2_rich` on simulation $0$ (precision $0.40$, recall $0.50$, $8$ positive test nodes).

<details class="nb-hint">
<summary>Hint</summary>

$F_1 = 2\mathrm{TP}/(\text{predicted positives} + \text{actual positives})$.

</details>

<details class="nb-sol">
<summary>Solution</summary>

Recall $0.5$ of $8$ means $\mathrm{TP}=4$; precision $0.4$ means $10$ predicted positives; $F_1 = 8/18 = 0.444$. One more true positive (same $10$ predictions): $10/18 = 0.556$, $+0.11$. One false positive fewer ($9$ predictions): $8/17 = 0.471$, $+0.026$ (this is exactly the change seen between the Studio and laptop runs of this simulation). With $7$ or $8$ positive test nodes per simulation and standard deviations of $0.04$ to $0.15$ across three simulations, many differences between configurations are not significant.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-1s">

<strong>Problem 1S</strong> 🌶🌶

Explain the trade-off between detection F1 and explanation AUROC in the sweep: what configurations show it, what is the measured mechanism, and what does Fidelity$^+$ add?

<details class="nb-hint">
<summary>Hint</summary>

Think about what the classifier no longer needs once node statistics reveal the label.

</details>

<details class="nb-sol">
<summary>Solution</summary>

All five configurations with test F1 above $0.5$ have explanation AUROC between $0.50$ and $0.61$ (for example F1 $0.65$ with AUROC $0.50$), and four of them have Fidelity$^+$ of only $0.29$–$0.36$. Rich node features and per-edge transaction counts let the classifier decide from a node’s own statistics, so it stops routing evidence through the alert edges: removing any edge barely changes its prediction (low Fidelity$^+$), and there is nothing edge-shaped for GNNExplainer to find. Fidelity$^+$ is the independent check that the drop in AUROC is the model’s behaviour and not an artefact of the ground truth: it measures reliance on the explanation without using the labels.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-1t">

<strong>Problem 1T</strong> 🌶🌶

How do you know GNNExplainer on AMLSim does something a simple rule would not? What did you measure, what did you find, and what remains?

<details class="nb-hint">
<summary>Hint</summary>

For a one-hop model, an explanation is a ranking of the incoming edges.

</details>

<details class="nb-sol">
<summary>Solution</summary>

I scored GNNExplainer against model-free and model-based rankings of a SAR node’s incoming edges. Inverting the number of raw transactions between the two accounts scores $0.85$, inverted neighbour degree $0.73$, random $0.50$; and under `gcn1_mlp` the model’s own SAR probability for the neighbour scores $0.83$, above GNNExplainer’s $0.68$ (the project’s log has $0.84$, $0.72$, $0.81$ and $0.69$; the difference in the first two is a torchmetrics sigmoid artefact, in the last two a software-environment effect). So for one-hop models a trivial rule or the model’s own beliefs beat the explainer, and part of any AUROC gain is the classifier. At two hops, where there is no one-line model-based heuristic, the same rules still score above the headline: $0.80$ for few transactions and $0.77$ for low sender degree against $0.73$ (a check I added on 2 October). Remaining: a model-randomisation test; until then $0.73$ is not a claim of superiority.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-1u">

<strong>Problem 1U</strong> 🌶🌶

A ranking of edges has scores $30, 25, 3, 2, 1, 20, 18, 0.5$ and labels $1, 0, 1, 0, 0, 1, 0, 0$. Compute its AUROC exactly. PyG’s `groundtruth_metrics` returns $0.7333$ for it. Explain the difference, and say why it mattered for the project’s heuristic table.

<details class="nb-hint">
<summary>Hint</summary>

`torchmetrics` treats scores outside $[0,1]$ as logits and applies a sigmoid. In float32, $\sigma(x)$ is exactly $1$ from about $x=17$.

</details>

<details class="nb-sol">
<summary>Solution</summary>

Positives $\{30, 3, 20\}$, negatives $\{25, 2, 1, 18, 0.5\}$, so $15$ pairs. $30$ beats all five, $3$ beats $2, 1, 0.5$, and $20$ beats all but $25$: $5+3+4 = 12$ wins, AUROC $= 12/15 = 0.8$. After the sigmoid, $30, 25, 20, 18$ all become exactly $1.0$, while $3, 2, 1, 0.5$ become $0.953, 0.881, 0.731, 0.622$. Now $30$ ties with $25$ and $18$ (two half-points) and beats the other three: $4$; $3$ loses to $25$ and $18$ and beats the rest: $3$; $20$ ties with $25$ and $18$ and beats the rest: $4$. Total $11$, AUROC $= 11/15 = 0.733$. In the heuristic table this squashed the degree and transaction-count rows (degrees and counts are far above $1$): “neighbour’s degree” showed $0.341$ and its inversion $0.720$, which cannot both be right because inverting a ranking turns $a$ into $1-a$; the exact values are $0.272$ and $0.728$. Mask values and probabilities lie in $[0,1]$ and are untouched, so the headline AUROCs are not affected.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-1v">

<strong>Problem 1V</strong> 🌶🌶

“A one-line rule scores $0.80$ and your explainer $0.73$, so the explainer is useless.” Answer, and say which experiment would separate “the explainer is poor” from “the model is poor” and from “the benchmark is easy”.

<details class="nb-hint">
<summary>Hint</summary>

What can the model see that the rule can see, and the other way round? What should happen to an explanation metric when the model’s weights are randomised?

</details>

<details class="nb-sol">
<summary>Solution</summary>

Not useless, but $0.73$ cannot be presented as a good number. The rule uses the number of raw transactions on a pair, which the GCN never sees (it has no edge features), and an explainer can only report what the <em>model</em> used, so the rule can win without the explainer failing at its task. What the comparison does show is that this benchmark is easy to rank without any model: alert transfers are one-off transfers between low-degree accounts, so a large part of every AUROC in B5 measures the simulator’s signature. To separate the three explanations: (i) <em>explainer poor</em>: give the model the transaction count (the `inverse_count` edge weights do this) and see whether the explanation follows; in the sweep it did not, the AUROC fell to $0.5$–$0.6$ while F1 rose, which suggests the model then stopped using the alert edges; (ii) <em>model poor</em>: compare the mask with the ranking by the model’s own neighbour probability (at one hop the latter wins, $0.83$ against $0.68$); (iii) <em>benchmark easy</em>: a model-randomisation test. If the AUROC stays well above $0.5$ with random weights it is measuring the data, not the model; I expect some of that, because the GCN normalisation gives low-degree neighbours more weight and alert edges connect low-degree accounts, but this is a guess; the test has not been run.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-1w">

<strong>Problem 1W</strong>

Explain the own-alert issue: why does it affect two-layer models and not one-layer models, and what did re-labelling show?

<details class="nb-hint">
<summary>Hint</summary>

Which edges does a two-layer computation graph contain that a one-layer one does not?

</details>

<details class="nb-sol">
<summary>Solution</summary>

In a one-layer model every scored edge enters the target, so an alert edge there is the target’s own alert’s (each alert account is in exactly one alert). A two-layer computation graph also contains edges into the target’s neighbours, which can belong to a different alert: $548$ of $1985$ scored positives ($28\%$). Counting them as positives is not wrong about the model, but it asks the explainer to find edges of an alert the target is not part of. Re-labelling with own-alert truth gave $0.734\to0.729$ for `gcn2_rich` and $0.697\to0.734$ for plain `gcn2`: the headline stands. The first reading, that the explanation quality belongs to the two layers and not to the rich features, was overturned on 2 October: on three fresh simulations plain `gcn2` scores $0.44$ and `gcn2_rich` $0.73$ ([Section A held-out replication on three new simulations](../sweep/#sec-mtp-fresh)).

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-1x">

<strong>Problem 1X</strong> 🌶🌶

“You ran thirty configurations and quote the best on the test split.” Respond, and design the cleanest confirmation you can afford.

<details class="nb-hint">
<summary>Hint</summary>

Winner’s curse; what was selected on what?

</details>

<details class="nb-sol">
<summary>Solution</summary>

Inside each configuration nothing used test data. But quoting the best of thirty by test-split numbers is optimistic, and I say so. The effect is bounded: the gain over the baseline ($+0.25$ AUROC) is much larger than the spread among the top configurations, several two-layer configurations land at $0.65$–$0.70$, and the baseline was fixed in advance. The clean confirmation is new data with the configuration fixed in advance: simulate fresh seeds and run the configurations chosen beforehand, or select the configuration on validation nodes and report only on test nodes. I did the first on 2 October ([Section A held-out replication on three new simulations](../sweep/#sec-mtp-fresh)): on three new simulations `gcn2_rich` scores AUROC $0.731$ (originally $0.734$) and F1 $0.40$ (originally $0.34$), against $0.414$ and $0.097$ for the baseline; the by-product was less comfortable: plain `gcn2`, which had looked as good, scored $0.44$.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-1y">

<strong>Problem 1Y</strong>

The resume says $2.6\times$. What is the exact ratio, and what would you say if asked?

<details class="nb-hint">
<summary>Hint</summary>

$0.3393/0.1271$.

</details>

<details class="nb-sol">
<summary>Solution</summary>

$2.67\times$; the printed $0.34/0.13 = 2.62$ is consistent with $2.6\times$, but the unrounded ratio rounds to $2.7$, and the project’s own write-up says $2.7\mathrm{x}$. I would say “about two and a half to two and three-quarter times”, and add that with seven or eight positive test nodes it is the least certain number on the page.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-1z">

<strong>Problem 1Z</strong>

“Where is the blockchain in a blockchain project?” and “Did you write this yourself?”

<details class="nb-hint">
<summary>Hint</summary>

State what was run; state the workflow.

</details>

<details class="nb-sol">
<summary>Solution</summary>

The title says <em>fraud detection</em> for a reason: the baseline report is about blockchain forensics, but everything I have run uses synthetic benchmarks and AMLSim, a simulator of bank transfers; Elliptic and other chains are on the list and not yet touched. On the second: the code was developed with Claude Code as an assistant under my direction, which the project’s own notes say; what I can and must be able to do unaided is read and derive every method, explain each number and its provenance, and say which checks I ran and which I did not.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-1aa">

<strong>Problem 1AA</strong> 🌶

What would you do next, in order, and what result would change your plan?

<details class="nb-hint">
<summary>Hint</summary>

Controls before conclusions; ground truth before topology.

</details>

<details class="nb-sol">
<summary>Solution</summary>

(1) Audit whether each alert’s realised edges form its declared shape and how many lie inside members’ two-hop computation graphs; (2) run edge betweenness, model randomisation and candidate-count strata on the two-layer models (degree and inverse transaction count are done: they beat $0.73$); (3) tune GNNExplainer’s regularisers by hard top-$k$ fidelity and check that fidelity ranks configurations like ground truth does; (4) a second AMLSim parameter set with more alerts; (5) a PGExplainer reproduction gated on matching the authors’ own numbers, then a head-to-head. The 2 October control already shows that a trivial rule beats $0.73$ at two hops, so the finding to take seriously is that AMLSim’s alerts are explained by simple structure; if model randomisation also fails to push the explainer to chance, the thesis question changes from “which explainer” to “what do these benchmarks measure”.

</details>

</div>
