---
title: "MTP Project"
weight: 1
sidebar:
  open: false
---

This book documents my M.Tech project on the explainability of graph neural networks for fraud detection: the theory behind it, every experiment that was run, every number with the file it comes from, and the questions an interviewer is likely to ask. Code is quoted from the project with its location, written like `model.py:40`, which means line 40 of `model.py`.

Each number or table in this chapter carries one of three evidence levels, marked next to it (a mark after a table’s caption sentence covers the whole table), and I trust them in this order.

- <span style="color:#009b55"><strong>[R]</strong></span> <strong>Re-run.</strong> On 2 October 2026 I recomputed the number on my laptop (Python 3.13.7, `torch 2.11.0+cpu`, PyG 2.8.0.post1) with the project’s own code, on AMLSim data that I regenerated locally, and it matched. The scripts and their output logs are kept in `data/mtp/verify/`.
- <span style="color:#0071bc"><strong>[F]</strong></span> <strong>File.</strong> Read from a result file (JSON, CSV or Markdown table) that the experiment itself wrote, under `results/` of the project folder. Not re-run.
- <span style="color:#f7921d"><strong>[L]</strong></span> <strong>Log.</strong> Stated in the project’s own notes (`CLAUDE.md` and `documentations/*.md`) and nowhere else: I found no file or script that reproduces it. Believe it less.

Code locations such as `cora_gcn.py:23` refer to the snapshots kept in `data/mtp/src/` (verbatim copies of the project files, so the line numbers are real); [Section 1.8](wrapup/) maps each snapshot back to its place in the project. Paths without a prefix are relative to `MTech project(Phase 1)/`. Whatever I could not establish is marked <strong>UNKNOWN</strong> and collected in [Section 1.8](wrapup/).

<div class="nb nb-moral">

The one-sentence version of the project: graph neural networks flag suspicious accounts, post-hoc explainers such as GNNExplainer are supposed to say <em>why</em>, and I am measuring whether those explanations can be trusted, starting by getting the measurement itself right. Nothing here has been run on real blockchain data yet.

</div>

## Contents

- [1.1 · Overview](overview/)
- [1.2 · Problem statement and background](background/)
- [1.3 · B1: a GCN and GNNExplainer from the source papers, on Cora](cora/)
- [1.4 · B2: the evaluation flaw that turned $0.71$ into $0.48$](flaw/)
- [1.5 · B3: reproducing GNNExplainer’s synthetic benchmarks](synthetic/)
- [1.6 · B4: IBM’s AMLSim, end to end, on a cloud machine](amlsim_setup/)
- [1.7 · B5: the 30-configuration sweep on AMLSim](sweep/)
- [1.8 · The answers I should have ready](wrapup/)
- [A · Glossary of notations](notation/)
- [References](references/)
