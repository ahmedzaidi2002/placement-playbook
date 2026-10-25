---
title: "1.6 · B4: IBM’s AMLSim, end to end, on a cloud machine"
linkTitle: "1.6 B4: IBM’s AMLSim, end to end, on a cloud machine"
weight: 6
math: true
---
<div class="nb-proto">

<em><span>Prototypical example for this section:</span> getting `mvn package` to find a library called `mason:mason:20`, which is not on Maven Central under the coordinates AMLSim’s `pom.xml` asks for, and whose official download link is dead.</em>

</div>

## 1.6.i What AMLSim is, and why it is in the project {#s1-6-i}

AMLSim [&#91;SK21&#93;](../references/#ref-amlsim) is IBM’s multi-agent simulator of anti-money-laundering scenarios. It builds a synthetic bank (accounts, a degree distribution, normal behaviour models such as <em>single</em>, <em>mutual</em>, <em>periodical</em>, <em>forward</em>, <em>fan-in</em>, <em>fan-out</em>) and then <em>plants</em> laundering patterns, called alerts, inside the normal traffic. Every transaction in the output says whether it belongs to an alert. That is the property I need and that the real datasets lack: an explanation ground truth that is exact because the simulator put it there. It sits between the abstract motifs of the GNNExplainer benchmarks and real data with no edge-level truth (Elliptic). A fellow student in my lab had used it for fraud-detection accuracy, which is how it came onto my list; adopting it for the thesis has not been confirmed with the guide.

It is three programs in a row:

1. `scripts/transaction_graph_generator.py conf.json` (Python): reads a parameter folder and writes accounts, a base transaction list, the alert members and the normal-model members to `tmp/<name>/`.
2. The Java simulator `amlsim.AMLSim`, built on the MASON multi-agent toolkit: runs `total_steps` $=720$ simulated days and writes the transaction log `outputs/<name>/tx_log.csv`.
3. `scripts/convert_logs.py conf.json` (Python): turns the log into the final labelled CSVs: `accounts.csv`, `transactions.csv` (with `is_sar` and `alert_id` per transaction), `alert_transactions.csv`, `sar_accounts.csv` (with the alert type), `cash_tx.csv`.

## 1.6.ii What the `1K` parameter set contains {#sec-mtp-amldata}

Everything below was read from the files in `AMLSim/paramFiles/1K` and from the generator’s own log <span style="color:#009b55"><strong>[R]</strong></span>.

| Planted alerts | count | accounts per alert | amounts, period |
|:--|:--|:--|:--|
| fan-in | $3$ | $5$–$10$ | $100$–$200$, $5$–$20$ steps |
| fan-out | $3$ | $5$–$10$ | $100$–$200$, $5$–$20$ steps |
| cycle | $4$ | $5$–$10$ | $100$–$200$, $5$–$20$ steps |

| Normal behaviour model | requested | realised in simulation 0 |
|:--|:-:|:-:|
| single | $500$ | $500$ |
| fan-out | $500$ | $132$ |
| fan-in | $500$ | $153$ |
| forward | $500$ | $500$ |
| mutual | $500$ | $500$ |
| periodical | $500$ | $500$ |

There are $1446$ accounts ($5\times200 + 446$), all US individual accounts at one bank with balances $50{,}000$–$100{,}000$; a single transaction type, `TRANSFER`; and $720$ simulated days from $2017$-$01$-$01$. All ten alerts are SAR (suspicious-activity-report) alerts. The consequences matter for everything later:

- <strong>Only three laundering shapes exist</strong>, planted by a generator I did not write. Whatever an explainer learns here is about these three shapes, and the amounts of alert transfers sit inside the normal range.
- <strong>The categorical columns carry no information</strong>: every account has the same type, country, currency and bank.
- <strong>The positive class is tiny.</strong> Over the three simulations I use there are $72$, $67$ and $70$ SAR accounts ($\approx5\%$ of nodes) and only $65$, $60$ and $63$ alert transactions <span style="color:#009b55"><strong>[R]</strong></span>.

| seed | accounts | transactions | ordered pairs | SAR accounts | alert tx. | SAR accounts by type<br>(fan-in / fan-out / cycle) |
|:-:|--:|--:|--:|--:|--:|:-:|
| 0 | 1446 | 121457 | 6984 | 72 | 65 | 23 / 20 / 29 |
| 1 | 1446 | 121477 | 6973 | 67 | 60 | 23 / 20 / 24 |
| 2 | 1446 | 121564 | 7005 | 70 | 63 | 17 / 18 / 35 |

<span style="color:#009b55"><strong>[R]</strong></span> (Alert-member rows differ slightly from SAR-account rows: simulation 0 lists $73$ alert members, one of whom, account $900$, never became a SAR account.) Each simulation is a separate run of the whole pipeline with its own `random_seed`, not a re-split of one run.

## 1.6.iii The obstacles, and how each was removed {#s1-6-iii}

The pipeline was set up on a Lightning AI Studio on 31 August 2026 (free CPU tier, reached over SSH; chosen over Colab or Kaggle because those are notebook-only, so a coding assistant cannot drive them) and then verified end to end on the bundled `1K` configuration: $1446$ accounts, $8441$ base transactions, ten alerts, the Java simulator running $720$ steps in under a second. <span style="color:#f7921d"><strong>[L]</strong></span> for the Studio steps; the individual facts I could re-check are marked <span style="color:#009b55"><strong>[R]</strong></span>.

1. <strong>Java and Maven.</strong> `sudo apt-get install default-jdk maven` gave OpenJDK $21$ and Maven $3.8.7$. The repository’s `pom.xml` resolves everything else (Commons-Math, JSON, WebGraph, Mockito, JUnit) from Maven Central. The README asks for Java $8$; the code compiles at source level $1.8$ on newer JDKs.
2. <strong>MASON, the one real obstacle.</strong> AMLSim depends on MASON version $20$ (a Java multi-agent simulation toolkit), coordinates `mason:mason:20`, which is not on Maven Central.

   - The README’s download, `cs.gmu.edu/~eclab/projects/mason/mason20.zip`, was dead when I tried it (documented as a $404$). Re-checked on 2 October: it answers `HTTP 301` and redirects to the university home page, so no zip is served <span style="color:#009b55"><strong>[R]</strong></span>.
   - GitHub’s `v20` release for `eclab/mason` has no binary: its only assets are the auto-generated source archives <span style="color:#009b55"><strong>[R]</strong></span>.
   - Downloading that source as a zip fails with a confusing “non-parseable POM”, because the repository stores its jars and its `pom.xml` with <strong>Git LFS</strong> (`.gitattributes` marks `*.jar`, `*.xml`, `*.txt` and others as LFS <span style="color:#009b55"><strong>[R]</strong></span>) and GitHub’s zip export contains only the small <em>pointer files</em>.
   - The fix: `git clone --branch v20` with `git-lfs` (already on the Studio image) instead of a zip; `mvn -pl mason -am package` builds `mason-20.jar`; `mvn install:install-file -DgroupId=mason -DartifactId=mason -Dversion=20 -Dpackaging=jar` installs it into the local Maven repository under exactly the coordinates AMLSim’s `pom.xml` expects. MASON’s own `groupId` is `cs.gmu.edu.eclab`, so using it would not match.
3. <strong>`sh` against `bash`.</strong> The helper scripts `scripts/build_AMLSim.sh` and `run_AMLSim.sh` use bash-only `[[ ... ]]` and start with `#!/usr/bin/env bash`, but the README says to run them with `sh`. On Ubuntu 24.04 `sh` is `dash`, which silently mis-parses the test, concludes that Maven is absent, and falls back to a broken manual `javac` compile. Always `bash scripts/...`.
4. <strong>The legacy Python.</strong> `requirements.txt` pins `networkx==1.11`, which the README says is deliberate (“we do not support version 2.\* due to performance issues when creating a large graph”). That version does `from fractions import gcd`, and `fractions.gcd` was removed from Python’s standard library in $3.9$. I confirmed both halves on 2 October: in a Python $3.13$ environment `import networkx` fails with `ImportError: cannot import name 'gcd' from 'fractions'`; the Python $3.8.20$ interpreter still has `fractions.gcd` <span style="color:#009b55"><strong>[R]</strong></span>. The Studio has one default conda environment (used for PyTorch work), so AMLSim got its own: `conda create -n amlsim python=3.8`, plus `apt install graphviz graphviz-dev` (the headers `pygraphviz` needs to build). The README itself says Python $3.7$; I used $3.8$.

Two things I learned about the Studio, relevant if it comes up: it auto-sleeps after $10$ minutes idle on the free tier (files persist; reconnect to wake it), and over non-interactive SSH `python` is not on the path, so every remote command uses the absolute interpreter.

## 1.6.iv The same pipeline on my Windows laptop (2 October 2026) {#sec-mtp-localaml}

To be able to re-run everything without the Studio, and to check the Studio’s numbers, I rebuilt the pipeline locally. It works, and the data it produces equals the Studio’s data wherever I can compare it ([Section 1.6.ii](#sec-mtp-amldata): the counts per simulation match the numbers written down in August and September).

|  | Studio (31 Aug) | Laptop (2 Oct) |
|:--|:--|:--|
| Java | OpenJDK 21 | Oracle JDK 25 (compiles the source-level-1.8 project fine) |
| Maven | 3.8.7 (apt) | 3.9.16, unzipped from Apache’s archive (checksum verified), not on `PATH` |
| MASON | built from `git clone --branch v20` | same; installed with a standalone `pom.xml` (see below) |
| Python | conda env, 3.8 | `uv venv --python 3.8` (3.8.20) |
| `pygraphviz` | installed | skipped: only an optional plotting script imports it, and it will not build on Windows |

Two Windows-specific problems, both found and fixed that day:

1. <strong>The MASON jar installs with the wrong metadata.</strong> The command `mvn install:install-file` reads the `pom.xml` embedded in the jar, whose parent is `cs.gmu.edu.eclab: mason-build: 20`, which Maven Central does not have; AMLSim’s build then fails with “Could not find artifact `cs.gmu.edu.eclab: mason-build: pom: 20`”. Passing a minimal standalone pom with `-DpomFile=` fixed it.
2. <strong>A doubled carriage return in every CSV.</strong> The generator opens its CSV outputs with `open(f, "w")` and writes with `csv.writer`, whose line terminator is already `\r\n`. On Windows, text mode turns each `\n` into `\r\n` again, giving `\r\r\n`; Java’s line reader sees a blank line after every row, splits the empty line into one column and the simulator dies with “Index 5 out of bounds for length 1” when it asks for the sixth column. The bytes confirm it (`13 13 10` after the header). The fix is `newline=""` on the four writers in `transaction_graph_generator.py` and the one in `convert_logs.py`: five changed lines, visible with `git diff` in the clone.

```python
# in AMLSim/, once:        mvn clean package -DskipTests
# per simulation (conf.json, conf_seed1.json, conf_seed2.json):
.venv\Scripts\python scripts\transaction_graph_generator.py conf.json
mvn -q exec:java "-Dexec.mainClass=amlsim.AMLSim" "-Dexec.args=conf.json"
.venv\Scripts\python scripts\convert_logs.py conf.json
```

The three configuration files differ only in `random_seed` ($0,1,2$) and `simulation_name`. The Java step takes $1$–$3$ seconds.

## 1.6.v What B4 does not claim {#s1-6-v}

- “Cloud infrastructure” is one free-tier CPU Studio, not a cluster and not institute HPC.
- Nothing beyond the bundled `1K` parameter set has been simulated: no larger parameter set, no tuning of the simulator, no export to any other format. Using AMLSim in the thesis is not yet confirmed with the guide.

## 1.6.vi Questions this bullet invites {#s1-6-vi}

What does AMLSim produce, and why is it useful for explainability? Why is MASON a problem and why did the zip download fail? What is Git LFS? What does `install:install-file` do and why those coordinates? Why Python $3.8$ and not the current version? What was the Windows-only bug and how did you find it? What is a SAR account, and what are the alert patterns? Worked answers are in the problems at the end of the chapter.
