---
title: Core Subjects
weight: 2
cascade:
  type: docs
---

Eight core-subject books, one chapter per page, all written for OAs and interviews: a definition, the one idea behind each topic, the formulas worth remembering, and a worked example wherever there is a numerical to practise (for example, one Gantt chart per scheduling algorithm in OS). No long programs.

Each book ends with a rapid-fire chapter (spoken-length answers, the fastest revision before an interview) and a practice chapter whose solutions are folded under each problem.

{{< cards >}}
  {{< card link="dsa" title="Data Structures and Algorithms" subtitle="14 chapters: complexity, lists, stacks, trees, heaps, hashing, graphs, sorting traces, greedy and DP, cheat sheet." icon="code" >}}
  {{< card link="oop-cpp" title="OOP in C++" subtitle="11 chapters: pillars, constructors and copying, inheritance, virtual functions, smart pointers, SOLID, patterns, LLD." icon="cube" >}}
  {{< card link="os" title="Operating Systems" subtitle="13 chapters: processes, scheduling with one example per algorithm, synchronisation, deadlock, paging, page replacement, disks." icon="terminal" >}}
  {{< card link="dbms" title="DBMS" subtitle="13 chapters: keys, algebra, SQL and interview queries, normalization, transactions, concurrency, recovery, indexing." icon="database" >}}
  {{< card link="cn" title="Computer Networks" subtitle="13 chapters: layers and delay, error control, sliding windows, MAC, subnetting, routing, TCP, application layer, security." icon="globe-alt" >}}
  {{< card link="coa" title="Computer Organization and Architecture" subtitle="11 chapters: data representation, logic, ISA and addressing, pipelining, caches, I/O, performance." icon="chip" >}}
  {{< card link="ml" title="Machine Learning" subtitle="14 chapters: regression, bias–variance, logistic, SVM, trees, ensembles, clustering, PCA, evaluation, statistics, rapid-fire and 40 OA problems." icon="chart-bar" >}}
  {{< card link="dl" title="Deep Learning" subtitle="13 chapters: backprop, optimisers, BatchNorm, CNNs, RNNs, Transformers, LLMs, generative models, with your VGG11 and Transformer projects woven in." icon="sparkles" >}}
  {{< card link="recent-ml-dl" title="Recent ML/DL: what is hot in AI" subtitle="One page: reasoning models, agents, advanced RAG, post-training, inference optimisation, evaluation, SSMs and hybrids, diffusion, world models." icon="lightning-bolt" >}}
{{< /cards >}}

All eight books are hand-written condensations. The first six were cut down from the full LaTeX books, whose generated pages are kept in `tools/latex2hugo/full-version/`; `tools/latex2hugo/convert.py` skips these six books unless run with `--overwrite-condensed`. Machine Learning and Deep Learning are condensed from the PDFs and Cantilever ML toolkits in `core notes/`.
