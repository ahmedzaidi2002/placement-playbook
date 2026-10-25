---
title: "5 · Defending each resume bullet"
weight: 5
---

The five Warner Bros. Discovery bullets are fixed on the resume. This page takes them one at a time and answers four things for each: **what it actually means**, **the evidence behind it**, **the soft spot** an informed interviewer could press, and **the sentence to say**. None of the answers below stretches the facts. Where a bullet is worded more strongly than the report supports, the answer is written so that the *true* version sounds strong, and so that you are never caught defending the stronger reading.

## Bullet 1

> Automated DIANA's VPN-detection audit, replacing a manual script with a weekly pipeline scanning **11,103** IPs.

**What it means.** The original Revelio was a manual, run-once CLI script. You built a scheduled GitHub Actions pipeline around the same probe, so the audit runs weekly with no one at a keyboard.

**Evidence.** <span style="color:#0071bc"><strong>[Report]</strong></span> Weekly schedule plus manual dispatch; preflight, sharded audit, merge, publish, notify. Validated end to end with real tunnels and real DIANA blocks. The 11,103-IP run is the sample behind the headline 21.4%.

**Soft spots.**
1. **11,103 is not the weekly run size.** The requirement is 100 to 500 IPs per run, and the config pool is 28,326. The 11,103 is the large run that produced the headline number.
2. **"Weekly" is the designed cadence, not a running one.** The prd schedule is not enabled yet (needs VPN subscriptions and a security review).

**Say.** "The original was a manual script. I built the scheduled pipeline around it: a weekly workflow that samples a balanced set of VPN IPs, runs them through the real decision path in parallel shards, enriches, stores and trends the result. The 11,103 is the size of the IP set behind the headline measurement; each weekly run is a few hundred. It's validated end to end, and the production schedule is waiting on provider subscriptions and a security review."

## Bullet 2

> Measured a **21.4%** block rate against WBD's ~**50%** target, matching an independent audit.

**What it means.** Of 11,103 known VPN IPs, DIANA blocked 2,374 (21.4%), against a contractual benchmark of about 50%. A 2025 third-party audit found about 20%.

**Evidence.** <span style="color:#0071bc"><strong>[Report]</strong></span> 2,374 / 11,103; the benchmark and the independent audit are stated in the report. <span style="color:#7c3aed"><strong>[Reasoned]</strong></span> 2,374 / 11,103 = 21.38%.

**Soft spot.** **The report credits the first 21.4% to InfoSec's original tool** ("it had already reproduced the ~20% number independently"). If an interviewer asks "did you produce that number?", a flat yes overclaims. It also says Revelio's playback leg "reproduced" it, which is the part your productized pipeline relies on.

**Say.** "InfoSec's original probe had already reproduced the number, 21.4% on 11,103 IPs, which is why my project was productizing it rather than rebuilding it. I made that measurement repeatable and trustworthy: balanced sampling, correctness guards, normalized decisions, trending. The headline result is that DIANA catches about two in five of the VPN streams it's contractually expected to, and it lines up with the independent audit at about 20%."

**If pressed, "so what did you measure?"** "I chose and justified the method (real playback, not a replica of the rule), and I ran and validated the pipeline that reproduces it with the guards in place." Only say you personally re-ran it at full scale if that is what happened; the report does not say. <span style="color:#f7921d"><strong>[Confirm]</strong></span>

## Bullet 3

> Dockerized the VPN probe for one-command self-tests, with **16** offline unit tests.

**What it means.** A Dockerfile, compose file, entrypoint and Makefile so that `make selftest` verifies the environment and `make test` runs 16 offline unit tests, with no credentials and no network.

**Evidence.** <span style="color:#0071bc"><strong>[Report]</strong></span> `make selftest` READY (openvpn 2.6.14, `/dev/net/tun`, 28,326 configs across 6 providers); `make test` 16 / 16 passing (classifier, header building, balanced sampling, env helpers); image verified with no secrets baked in; the `wait_for_tunnel` hang found and fixed; 29 configs tunnel-tested.

**Soft spot.** **The production pipeline has no Docker.** An interviewer reading bullets 3 and 4 together may ask why you Dockerized something and then shipped without it.

**Say.** "Docker was the right tool for local, one-command reproducibility, and it's where I found and fixed a real bug: a blocking read that let a 30-second timeout run to 75 seconds. For production, a GitHub-hosted runner is already a fresh Linux VM that can install OpenVPN directly, so I deliberately dropped the Docker layer. Docker proved the probe; Actions shipped it."

## Bullet 4

> Deployed a GitHub Actions pipeline – **10** parallel shards, IP enrichment, and PagerDuty alerts on block decisions.

**What it means.** A scheduled workflow with 10 parallel shards, inline IP enrichment, and PagerDuty wired into the notify step.

**Evidence.** <span style="color:#0071bc"><strong>[Report]</strong></span> 10 parallel shards, `fail-fast: false`, provider-aware sharding tested across 5 providers; inline enrichment via ipapi.is; a **failure rule** that pages PagerDuty.

**Soft spots.**
1. **"Deployed" overstates the status.** It was built and validated end to end, with the prd schedule not yet enabled.
2. **"PagerDuty alerts on block decisions" is not how the report describes it.** The report says a run fails, and pages, only if the **ERROR rate exceeds 90%** or there are **zero decisions**. A low block rate is "not a failure: that is an audit finding, alerted separately on the data."

**Say.** "The workflow is built and validated end to end in the repo's environments. Alerting is wired to PagerDuty from the notify step. It pages when the pipeline itself is unhealthy: more than 90% of attempts erroring, or no decisions at all. The block decisions are what the audit records and trends, and a low block rate is a finding that's reported on the dashboard and alerted on the data, not a page. I made that split on purpose so the pager only means 'the audit is broken'."

**Do not say** that PagerDuty fires every time DIANA blocks something. That is not what was built, and an engineer will see at once that it would be unusable.

## Bullet 5

> Eliminated a `$26/mo` IPinfo Core dependency, enriching IPs via internal request context instead.

**What it means.** The original tool enriched IPs from a paid API (ipinfo). You removed that dependency. The enrichment now comes from two sources that cost nothing extra.

**Evidence.** <span style="color:#0071bc"><strong>[Report]</strong></span> Original enrichment was "one paid API (ipinfo)". The spike found a server-side endpoint that decodes the response's `x-wbd-session-state` into plain JSON (IP, ASN, ISP, categories, residential, city, country) over ordinary HTTP. The shipped pipeline enriches each tunnel exit IP inline with the free **ipapi.is** API; the session-state decode is the optional on-network path that adds the service-observed IP and `ip_mismatch`.

**Soft spots.**
1. **The USD 26 figure is not in the report.** <span style="color:#f7921d"><strong>[Confirm]</strong></span> its source.
2. **"Internal request context" describes the session-state decode.** The pipeline's default inline lookup is the public ipapi.is API. If an interviewer asks "so what does the pipeline call?", the accurate answer includes both.

**Say.** "The original used a paid ipinfo plan for ASN, ISP and category. In the spike I found that the response's own session state can be decoded into the same geolocation data over plain HTTP, which is the request context the bullet refers to. In the shipped workflow I use a free public API for inline enrichment so it runs without any internal network, and the session-state decode adds the service-observed IP for the mismatch check. Either way the paid dependency is gone. The 26 dollars is the plan price."

(Replace "the plan price" with the real source of the number once you have confirmed it.)

## Cross-bullet traps

| Trap question | Safe answer |
|---|---|
| "Is this in production?" | No. Built and validated end to end. Prod schedule awaits subscriptions and security review. |
| "What was yours vs InfoSec's?" | Theirs: the probe, the playback idea, the first 21.4% run. Mine: the measurement-design decision, the auth-chain spike, the Docker hardening, the infra decision, the Actions system. |
| "Did you change DIANA?" | No. It's an observability harness around DIANA. |
| "How many IPs per week?" | 100 to 500 by requirement. 11,103 was the headline sample. |
| "Why not just call GeoGuard?" | That measures a replica of the rule that can drift, and can't capture the IP HBO Max actually sees. |
| "Why PagerDuty?" | Pipeline health, not the KPI. |
| "Any bug you found?" | The blocking `readline()` that let a 30 s timeout run to 75 s. |

{{< callout type="info" >}}
**One principle.** Every qualified answer above is *stronger* than the bullet, not weaker. "I decided what to measure, I dropped Docker on purpose, and I separated pipeline health from the audit finding" reads as engineering judgement. Defending "alerts on block decisions" as written does not.
{{< /callout >}}
