---
title: "7 · Must-know before the interview"
weight: 7
---

The day-before page. Everything here is in the earlier sections; this is the compressed version.

## The 60-second pitch

> At Warner Bros. Discovery I worked in Fraud & Abuse Prevention on an audit of DIANA, the service that decides whether an HBO Max stream is coming through a VPN. Dashboards showed blocks, but nobody had measured the real catch rate against known VPN traffic. InfoSec had a one-off script that did it by hand. I turned that into a weekly, automated, stored and trended audit. I chose to measure the real user-visible decision rather than a replica of the rule, found a sanctioned way past the login bot check, Dockerized and hardened the probe, and built a sharded GitHub Actions pipeline with enrichment, correctness guards and alerting. The measured block rate was 21.4% against a roughly 50% contractual target, consistent with an independent audit. It's validated end to end; production is waiting on VPN subscriptions and a security review.

## The 2-minute version (add these)

- **Why it mattered:** the dashboard metric can't tell you detection quality without ground truth.
- **The fork:** direct detector call vs real playback. Chose playback for fidelity.
- **The unblock:** Arkose blocks raw login; asked InfoSec; reused the ~10-year token after decoding its lifetime.
- **The find:** enrichment via the response's session state, over plain HTTP, removing the in-cluster Kafka dependency.
- **The bug:** a blocking `readline()` turned a 30 s timeout into 75 s; fixed with `select()`.
- **The decision:** Docker to prove it, Actions to ship it; reversed my own Kubernetes recommendation when the evidence changed.

## Numbers to have ready

| Number | Meaning |
|---|---|
| **21.4%** | Block rate: 2,374 of 11,103 VPN IPs |
| **~50%** | Contractual benchmark |
| **~20%** | Independent 2025 audit |
| **100 to 500** | IPs per weekly run (requirement) |
| **28,326 / 6** | Configs / providers in the pool |
| **29 (26 + 3)** | Configs tunnel-tested: healthy / broken |
| **16** | Offline unit tests, all passing |
| **10** | Parallel shards |
| **75 s vs 30 s** | The hang vs the timeout; fixed to 5.01 s on a 5 s test |
| **110 / 9,134** | IP-mismatch tests (about 1.2%) |
| **~10 years** | Token lifetime (exp minus iat) |
| **90%** | Error rate above which the run fails |
| **~USD 462 to 594 / yr** | Estimated run cost |
| **2 to 3 weeks** | Estimated effort to productize |

## Claims to avoid

| Do not say | Say instead |
|---|---|
| "I built Revelio" | "I productized InfoSec's Revelio" |
| "I measured the 21.4%" (flat) | "The original probe had reproduced it; I made it repeatable and added the guards" |
| "It's in production" | "Validated end to end; prod schedule awaits subscriptions and security review" |
| "PagerDuty fires on every block" | "It pages when the pipeline fails, more than 90% errors or zero decisions" |
| "It scans 11,103 IPs every week" | "Each run is 100 to 500; 11,103 was the headline sample" |
| "I bypassed Arkose" | "I asked InfoSec; there's no bypass; I used the approved long-lived token" |
| "I changed DIANA" | "I audit it from outside; DIANA is unchanged" |
| "I saved USD 26 a month" (as measured) | "It removed a paid dependency; the plan price is about 26" (once confirmed) |
| Any token, cookie name or internal endpoint | Keep to the architecture level |

## One-page cheat sheet

```text
WHAT     Revelio = audit AROUND DIANA (VPN detection for HBO Max). DIANA is not modified.
HOW      real VPN tunnel (OpenVPN) -> real playbackInfo -> 200=ALLOW (miss) / 403 access.denied.vpn.usage=BLOCK
KPI      BLOCK / (BLOCK+ALLOW);  OTHER-DENY (geo) and ERROR excluded
RESULT   21.4% (2,374/11,103) vs ~50% target vs ~20% 2025 audit
BEFORE   InfoSec one-off: manual CLI, skewed (62% Proton), CSV, creds on disk, paid ipinfo
MINE     measurement design | Docker+hardening | infra decision | Actions system | auth spike

DESIGN   Method A (call GeoGuard, replicate rule): fast, drifts, no observed IP
         Method B (real playback): real decision, slower  <- chosen
AUTH     Arkose blocks raw login. No bypass (asked InfoSec). Reuse ~10-yr "st" JWT (exp - iat).
ENRICH   original: paid ipinfo.  spike: session-state decoded over HTTP (no Kafka).
         shipped: free ipapi.is inline; on-network decode adds observed-IP + ip_mismatch.
GUARDS   off-VPN control must ALLOW (expired cookie)  |  exit IP != runner IP (leak)
INFRA    A inside DIANA: no (noisy neighbour)  B Actions: chosen  C K8s CronJob: future (28k sweep)
         reversal: C on paper -> B because built+validated, weak points solved
DOCKER   proves probe locally (make selftest/test/report; 16 offline tests); dropped in prod
BUG      blocking readline() -> 75 s on a 30 s timeout -> select() bounded read -> 5.01 s
PIPELINE preflight -> audit (10 shards, provider pinned to 1 shard, sequential, fail-fast:false)
         -> merge (enrich + 4-way decision + pass/fail) -> publish (history.jsonl + Pages) -> notify (PagerDuty)
FAIL     ERROR rate > 90% or zero decisions. Low block rate = finding, not page.
STATUS   built + validated; NOT in prod. Needs VPN subscriptions + security review.
COST     ~USD 462/yr VPN (+ ~USD 11/mo HBO Max); enrichment/storage/Pages free; estimates.
```

## Self-test

Answer out loud without looking.

1. What is DIANA and what does Revelio do to it?
2. What was already there and what did you add?
3. Why real playback over a direct detector call?
4. What do the two correctness guards protect against?
5. How did you get past login, and who told you how?
6. What did the session-state discovery enable?
7. Explain the 75 second bug in two sentences.
8. Why provider-per-shard and sequential?
9. What makes a run fail, and why not a low block rate?
10. Why did you drop Docker in production?
11. Why did you reverse your Kubernetes recommendation?
12. What is left before production?
13. Where does the headline 21.4% come from, and how confident are you?
14. What is the weakest word in each resume bullet, and what is your sentence for it?

**Answers.** (1) DIANA decides ALLOW or BLOCK on VPN traffic; Revelio audits it from outside by driving real VPN traffic through the real path. (2) InfoSec had the manual probe; I added design, hardening, infra and the weekly pipeline. (3) Fidelity: real playback measures the user-visible decision, a replica can drift. (4) Expired cookie faking blocks; a failed tunnel measuring the runner. (5) Asked InfoSec; reused the long-lived token after decoding its lifetime. (6) Enrichment over plain HTTP, no in-cluster Kafka, so Actions was viable. (7) Blocking `readline()` never rechecked the deadline; `select()` bounded each wait. (8) Provider session caps per account. (9) More than 90% errors or zero decisions; a low rate is the finding. (10) A runner is already a fresh VM; Docker added nothing there. (11) The Actions version was built and validated and its weak points were solved. (12) Subscriptions, security review, secrets, int validation, enable prd. (13) InfoSec's probe reproduced it; about plus or minus 0.8 sampling error; provider mix matters. (14) See [section 5](../05-resume-bullets/).
