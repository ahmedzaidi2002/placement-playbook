---
title: "4 · Results, cost and status"
weight: 4
---

## The headline finding

Revelio's playback leg, run over **11,103 VPN IPs**, recorded **2,374 BLOCK** decisions: a **21.4% block rate**. <span style="color:#0071bc"><strong>[Report]</strong></span>

| Source | Block rate |
|---|---|
| Contractual benchmark | about 50% |
| Revelio (this tool) | **21.4%** |
| Third-party audit, 2025 | about 20% |

Two separate measurements landing within about a point of each other is the credibility argument. In plain words: **DIANA catches roughly two of every five VPN streams it is contractually expected to catch** (21.4 / 50 = 0.43 <span style="color:#7c3aed"><strong>[Reasoned]</strong></span>).

Check the arithmetic before you say it: 2,374 / 11,103 = 21.38%, which rounds to 21.4%.

### How far to trust 21.4% (be able to say this)

- **Sampling error is small.** A rough 95% interval for a proportion of 0.214 on 11,103 trials is about plus or minus 0.8 points (standard error is the square root of 0.214 x 0.786 / 11,103, about 0.39 points). <span style="color:#7c3aed"><strong>[Reasoned]</strong></span>
- **But the sample is not random.** It is whatever VPN IPs the config pool contains. The report notes that an earlier run was about 62% ProtonVPN, and that Proton is blocked well. So the *overall* rate depends on provider mix, which is exactly why the weekly version uses a balanced, seeded sampler and reports a per-provider breakdown.
- **"Within a point of about 20%"** compares against an approximate figure from a different audit with a different IP set. It supports "consistent with", not "identical to".
- **Ground truth is assumed.** The IPs are known VPN endpoints because you connected through them, so every ALLOW is a miss. Rotation could make a config stale (see below), which would bias the number slightly toward fewer true VPN IPs.

### Other numbers in the report

| Number | What it is |
|---|---|
| 21.4% | Block rate, 2,374 of 11,103 |
| about 50% | Contractual benchmark |
| about 20% | Third-party audit (2025) and GeoComply (Aug 2025) |
| 28,326 | Configs discovered across 6 providers |
| 29 | Configs tunnel-tested across 5 providers: 26 healthy, 3 broken (ExpressVPN, missing CA cert) |
| 16 / 16 | Offline unit tests passing |
| 10 | Parallel shards in the pipeline |
| 110 of 9,134 | Tests where self-reported IP differed from the IP HBO Max saw (about 1.2%) |
| 100 to 500 | IPs per weekly run (requirement: at least 100, preferably 500) |
| about 62% | ProtonVPN share of the earlier skewed run |
| 75 s vs 30 s | The `wait_for_tunnel` hang vs its timeout |
| 5.01 s | Bail time after the fix (20 s silent process, 5 s timeout) |
| about 10 years | Validity window of the `st` token (exp minus iat) |
| about 15,000 / 8 | NordVPN public config files / server IPs that differed from the year-old collection |

### Provider config rotation (anecdotal)

No provider publishes how often its configs rotate. A single ProtonVPN config stayed valid over a year, which may be why Proton is blocked well, while poorly blocked providers (for example SurfShark) appear to rotate faster. Of nearly 15,000 NordVPN files downloaded, **only 8 server IPs** differed from the year-old collection. The design therefore treats the config pool as a slowly changing, committed asset and proposes a per-provider **change detector** to turn the anecdote into data. <span style="color:#0071bc"><strong>[Report]</strong></span>

## Cost (estimates)

The report labels every figure here as an estimate. <span style="color:#0071bc"><strong>[Report]</strong></span>

| Line item | Steady-state cost |
|---|---|
| VPN subscriptions (5 providers, shared) | about USD 462 a year (about USD 38.50 a month); about USD 15 a month amortized during the first roughly 2-year intro term |
| Enrichment (ipapi.is) | USD 0: free tier is enough at 100 to 500 lookups a week |
| Storage (artifacts and committed history), Pages, secrets | USD 0 |
| GitHub Actions minutes | USD 0 within the Enterprise allocation (worst case about USD 10 to 13 a month if metered) |
| HBO Max account (Method B only) | about USD 11 a month, or USD 0 with an existing test account |
| **Totals** | about USD 462 a year (Method A, VPN only) vs about USD 594 a year (Method B including HBO Max) |
| Engineering effort | about 2 to 3 engineer-weeks to productize (not a rebuild: the probe already worked) |

The real long pole was **approvals**, not engineering: VPN subscriptions and a security review of the privileged-networking workflow.

{{< callout type="warning" >}}
**The resume's "USD 26 a month IPinfo Core" figure does not appear in the report.** The report says only that the original enrichment came from "one paid API (ipinfo)". <span style="color:#f7921d"><strong>[Confirm]</strong></span> where the 26 came from (the IPinfo plan page, a team doc, a Slack thread) and be ready to say so. Do not present it as a measured saving; present it as the list price of the dependency that was removed.
{{< /callout >}}

## Status at the end of the internship

Framing in the report: **prototype validated, production is the next step.** The hard unknowns (does the tunnel work, does the auth chain work, what does it cost, where should it run) are de-risked. What remains is integration and approvals, not invention. <span style="color:#0071bc"><strong>[Report]</strong></span>

| State | Item |
|---|---|
| Done | Probe Dockerized, self-tested and bug-fixed; 29 configs tunnel-tested across 5 providers |
| Done | HBO Max auth chain reverse-engineered; first real 200 / ALLOW decision captured |
| Done | Enrichment-over-HTTP path found, removing the in-cluster dependency |
| Done | Infra decision made and documented; GitHub Actions system built and validated end to end (tunnels, real BLOCKs, sharding, enrichment, dashboard, alerting) |
| **Left** | Real VPN provider subscriptions and credentials: the single hard blocker to a full unattended run |
| **Left** | Security review of privileged networking on shared runners |
| **Left** | Wire per-environment secrets, curate the committed config pool, validate in int (manual plus one scheduled run), then enable the prd schedule |

**What to say when asked "is it in production?"** "No. It's built and validated end to end, with real tunnels and real DIANA blocks, but the weekly schedule isn't enabled in prod yet. It needs the VPN provider subscriptions and a security review of the privileged-networking workflow. I handed over the design record, the workflows and the runbook." Say it before they ask. It costs nothing and it protects every other claim.

## What you learned (the five reflections)

1. **Reviewing others' work is as core as writing your own.** Engineers spent as much time reviewing as producing.
2. **The breadth of tech inside one team is large:** Java / Spring services, Kafka, Databricks jobs, Kubernetes and CI, third-party VPN and geolocation ecosystems.
3. **Security and compliance review is the real bottleneck.** The infra decision came down as much to "which option gets approved faster" as to "which is technically better".
4. **Cross-team accountability is healthy.** A tool built by one team to check another team's system reframed how trust works.
5. **Knowing what to build and why matters more than typing speed.** The best work was the research, the design fork and the infrastructure call, not a file of code.

<span style="color:#0071bc"><strong>[Report]</strong></span>

## Artifacts you produced

- Architecture decision record: Method A vs Method B, with impact, performance and cost.
- Requirements-to-modifications map for CONS-12973.
- HBO Max auth-chain writeup: the chain, the Arkose finding, the long-lived token, the enrichment-decode mechanism.
- Dockerization and findings: one-command setup, timeout fix, 29-config tunnel results.
- Infra decision (final): options A / B / C, the reversal, the comparison matrix.
- The GitHub Actions system: productized probe, sharded reusable workflow, per-environment callers, enrichment, pass/fail rule, Pages dashboard.
- A 10-minute internship presentation to senior engineers and product managers.
