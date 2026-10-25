---
title: "6 · Interview questions"
weight: 6
---

Questions an interviewer can reasonably ask about the internship, grouped by topic, with model answers. **Cover the answer, say yours out loud, then open it.** Answers are written to be spoken in 20 to 60 seconds. Evidence labels are explained on the [section landing page](../).

Answers marked <span style="color:#7c3aed"><strong>[Reasoned]</strong></span> are general engineering knowledge applied to the project, not statements from the report. Use "I'd expect" or "in general" with them.

## A. The project as a whole

{{< details title="A1. Walk me through your internship in one minute." >}}

I was on the Fraud & Abuse Prevention team at Warner Bros. Discovery. They own DIANA, the service that decides in real time whether an HBO Max stream is coming through a VPN and should be blocked. Dashboards showed blocks, but nobody had independently measured the real catch rate against known VPN traffic. InfoSec had a research script, Revelio, that did it once by hand. My job was to turn it into a weekly, automated, stored and trended audit. I chose to measure the real user-visible decision rather than a replica of the rule, reverse-engineered the auth flow so it could run unattended, Dockerized and hardened the probe, and then built and validated a sharded GitHub Actions pipeline with enrichment, guards, alerting and a dashboard. The measurement came out at 21.4% against a roughly 50% contractual target, consistent with an independent audit.

{{< /details >}}

{{< details title="A2. What was your contribution versus what already existed?" >}}

InfoSec had built the probe: tunnel through a paid VPN with OpenVPN, send a real playback request, read the 200 or 403. They had already reproduced the roughly 20% figure. What it lacked was everything needed to run unattended and be trusted: no scheduler, a skewed sample (about 62% one provider), the decision implicit in the HTTP status, a CSV read by hand, credentials on disk, one paid enrichment source. I closed those gaps, and the three things I'd point to are the measurement design, the Dockerized and hardened probe, and the infrastructure decision.

{{< /details >}}

{{< details title="A3. Is it in production?" >}}

No. It's built and validated end to end with real tunnels and real DIANA blocks, but the production schedule isn't enabled. The blockers are process, not technical: real VPN provider subscriptions, and a security review of running privileged networking on shared runners. What's left is wiring per-environment secrets, curating the config pool, validating in the integration environment, then enabling prd.

{{< /details >}}

{{< details title="A4. Did you modify DIANA?" >}}

No, and that was a deliberate constraint. Revelio is an observability harness built around DIANA. It drives real VPN traffic through the same live decision path a user hits and records the answer, so it measures the production system without touching it.

{{< /details >}}

{{< details title="A5. What would you do next if you had another month?" >}}

First, unblock production: provider subscriptions, the security review, per-environment secrets, validate in int, enable the schedule. Then a per-provider config change-detector, because rotation is currently anecdotal. Then alerting on the data itself, such as a drop or rise in block rate by provider, since the pager currently only reports pipeline health. If the audit ever needs to sweep the whole 28k-config pool in one run, revisit the Kubernetes CronJob, because GitHub Actions' 6-hour job cap is the limit.

{{< /details >}}

## B. Design decisions

{{< details title="B1. Why measure with real playback instead of calling the detector directly?" >}}

Calling the detector's lookup and replicating the rule client-side is faster, about 0.1 to 0.3 seconds, and deterministic. But it measures a copy of the rule: it ignores overrides, simulation mode and last-seen logic, so it can drift from what a user really experiences, and it can't tell you the IP the service actually saw. The audit's whole point is to report the real, user-visible number, the same one the external audits report. Real playback costs 2 to 5 seconds per attempt and needs an account and cookie handling, but speed wasn't the constraint at 100 to 500 IPs a week. Fidelity was.

{{< /details >}}

{{< details title="B2. Why GitHub Actions and not Kubernetes or running next to DIANA?" >}}

Running next to DIANA was out: a heavy, privileged, multi-hour tunnel job beside a latency-sensitive production service is a noisy-neighbour risk. Between Actions and a Kubernetes CronJob, both give zero risk to DIANA, but Actions was already built and validated, mirrored a pattern the team already used, gave me single-use VMs with full sudo and TUN support, and didn't need a new security review for an in-cluster privileged job. Kubernetes stays the documented path if we need the full 28k pool in one run, which Actions' 6-hour cap can't do.

{{< /details >}}

{{< details title="B3. You first recommended Kubernetes, then reversed. Why?" >}}

My on-paper analysis favoured the CronJob, mainly because there's no time cap and the existing design docs assumed in-cluster. I flagged that choosing otherwise wasn't mine to decide alone, since it was a stakeholder-alignment question. Then two things changed. One, the Actions option had actually been built and validated end to end, while the CronJob was unbuilt and would need a security review with no internal precedent. Two, its two weak points were solved: provider-aware sharding replaced the fragile-sharding worry, and the plain-HTTP enrichment I found in the spike removed the need for in-cluster Kafka. When the evidence changed I changed the recommendation and said why.

{{< /details >}}

{{< details title="B4. Why did you drop Docker for production?" >}}

Docker's value was local reproducibility: one command to verify the environment anywhere. A GitHub-hosted runner is already a fresh Linux VM that gets destroyed after each run, so it can install OpenVPN directly. A Docker layer there adds build time and an image to maintain without adding isolation I don't already have. So production runs the scripts directly. Docker did its job in the phase where I needed to prove and harden the probe.

{{< /details >}}

{{< details title="B5. Why one provider per shard, run sequentially?" >}}

VPN providers cap concurrent sessions per account. If two shards used the same provider's credentials at once, sessions would be dropped and I'd record errors that aren't DIANA decisions. Pinning each provider to one shard and running its configs in sequence guarantees at most one live session per provider account, while the shards still run in parallel across providers.

{{< /details >}}

{{< details title="B6. Why `fail-fast: false`?" >}}

By default a matrix job cancels the remaining shards when one fails. One broken shard, say a provider outage, shouldn't discard the other nine shards' data. With fail-fast off, every shard finishes and the merge step decides what the run means.

{{< /details >}}

{{< details title="B7. Why store results as a committed JSONL line instead of a database or S3?" >}}

One compact summary line per week is tiny, versioned, reviewable in a PR and easy to render on a Pages dashboard. It also removes AWS from the approval path, and approvals were the real bottleneck. The full per-run result is kept as a workflow artifact. If the data ever outgrows a file, S3 or Databricks is the next step.

{{< /details >}}

{{< details title="B8. What are the downsides of committing history to the repo?" >}}

<span style="color:#7c3aed"><strong>[Reasoned]</strong></span> It needs a write-capable token in the workflow, concurrent runs could conflict on the file, the repo grows slowly, and it isn't queryable beyond what a dashboard script reads. With one run a week and about a line per run, those are small. If the audit grew to many runs a day I'd move to a real store.

{{< /details >}}

## C. Measurement and statistics

{{< details title="C1. How is the block rate defined, and what doesn't count?" >}}

Block rate is BLOCK divided by the decisions that are either BLOCK or ALLOW. Each attempt is normalized to BLOCK, ALLOW, OTHER-DENY (a non-VPN denial such as a geo-block) or ERROR. Only BLOCK and ALLOW enter the KPI, so geo-blocks and errors can't inflate or deflate it.

{{< /details >}}

{{< details title="C2. How confident are you in 21.4%?" >}}

On the sampling side, a proportion of 0.214 on 11,103 attempts has a standard error of about 0.4 points, so roughly plus or minus 0.8 for a 95% interval. <span style="color:#7c3aed"><strong>[Reasoned]</strong></span> The bigger uncertainty is that the sample isn't random: it's whatever's in the config pool, and the provider mix matters because some providers are blocked far better than others. An earlier run was about 62% ProtonVPN, which is blocked well. That's why the weekly design uses a balanced seeded sampler and reports per provider as well as overall. And it matches an independent audit at about 20%, which is corroboration, not proof of equality.

{{< /details >}}

{{< details title="C3. What does the correctness guard protect against?" >}}

Two failure modes that would silently corrupt the number. The off-VPN control check sends a known non-VPN request and requires ALLOW. If the cookie has expired, every request would be denied and the audit would report a huge, false block rate, so the pipeline fails fast instead. The leak check requires the tunnel's exit IP to differ from the runner's real IP, because a tunnel that didn't actually come up would mean measuring the runner, not a VPN.

{{< /details >}}

{{< details title="C4. What is the ip_mismatch signal?" >}}

The IP a VPN reports for itself can differ from the IP HBO Max actually sees, when a provider routes streaming traffic through a residential proxy. Comparing the two flags that. It was rare, 110 of 9,134 tests, about 1.2%, but it's expected to grow as DIANA improves and providers adapt, which is why the requirement to test the IP "as seen by Max" matters.

{{< /details >}}

{{< details title="C5. How do you know the VPN IPs are really VPN IPs?" >}}

Because I connect through them: the tool tunnels through a paid VPN exit node, captures the exit IP, and sends the request from there. So every IP in the audit is a genuine VPN exit by construction, and every ALLOW is a miss. The caveat is staleness: configs can rotate. The report found rotation is slow and anecdotal, for example only 8 of nearly 15,000 NordVPN server IPs differed from a year-old collection, which is why the plan includes a per-provider change detector.

{{< /details >}}

{{< details title="C6. The benchmark is 50% and you measured 21.4%. What does that mean?" >}}

DIANA catches about two in five of the VPN streams it's contractually expected to catch (21.4 divided by 50 is about 0.43). It's a finding about detection coverage of the GeoGuard-based rule, not a bug in the pipeline, which is why a low block rate is reported on the dashboard and not paged.

{{< /details >}}

## D. Networking and security

{{< details title="D1. What does it take to build a VPN tunnel in CI?" >}}

OpenVPN needs to create a TUN device and change routing, so the process needs `NET_ADMIN` and access to `/dev/net/tun`, plus sudo. That's why serverless runtimes were ruled out, and why a GitHub-hosted Linux VM with full sudo works. It's also why a security review of privileged networking is part of the path to production.

{{< /details >}}

{{< details title="D2. How did you prove a tunnel is healthy without valid credentials?" >}}

By giving it deliberately fake credentials and checking how far it gets. Reaching `AUTH_FAILED` after a full TLS handshake means the network path, certificate chain and server are all fine. The only thing that fails is the password, which is the last possible step. Anything that fails before auth is a real config defect. That's how I found ExpressVPN's three configs were missing their CA certificate.

{{< /details >}}

{{< details title="D3. What is the long-lived token and how did you confirm its lifetime?" >}}

HBO Max's auth token, the `st` cookie, is a signed JWT. A JWT's payload carries `iat` (issued at) and `exp` (expiry) claims, so I decoded it and took `exp` minus `iat`, which came to about ten years. Decoding doesn't need the signing key, since the payload is just base64. <span style="color:#7c3aed"><strong>[Reasoned]</strong></span> That makes it a stable credential for unattended runs, with the caveat from InfoSec that it's a legacy workaround and tokens are due to be reworked.

{{< /details >}}

{{< details title="D4. Did you bypass bot protection? Is that ethical?" >}}

No bypass. Raw HTTP login hits Arkose, so I asked InfoSec, who own the original tool, whether a bypass string existed for internal automation. They said none exists and described the approved route: log in once manually and reuse the long-lived token. This was in the integration test environment, for an internal audit, with the owning team's blessing. I decoded the token to understand its lifetime, nothing more.

{{< /details >}}

{{< details title="D5. How do you handle secrets in this pipeline?" >}}

Cookies and VPN credentials go in CI secrets, per environment, never in the repo or the image. I verified the Docker image had no secrets or configs baked in. Locally, secrets go into git-ignored files and I refer to paths, not values.

{{< /details >}}

{{< details title="D6. Why is a leak check necessary?" >}}

If the VPN process starts but the tunnel never carries traffic, the request leaves from the runner's own IP. The audit would record DIANA's decision about the runner, not a VPN. Comparing the observed exit IP to the runner's real IP catches that.

{{< /details >}}

## E. CI/CD and engineering

{{< details title="E1. Explain the `wait_for_tunnel` bug." >}}

The code waited for the VPN process to report it was up by calling a blocking `readline()` on its output. If the process went silent, `readline()` blocked and the loop never got back to check the deadline, so a 30 second timeout took about 75 seconds on a refused connection. I replaced it with a `select()`-based bounded read so every wait is capped by the time left. I proved it deterministically: a process kept silent for 20 seconds with a 5 second timeout now returns at 5.01 seconds.

{{< /details >}}

{{< details title="E2. What do your 16 unit tests cover and why are they offline?" >}}

The pure logic: the decision classifier, header building, balanced sampling and environment helpers. Offline matters because a test that needs a VPN, a live cookie and the service is slow, flaky and can't run in CI. The logic where bugs hide doesn't need the network, so it's cheap to test thoroughly. The end-to-end behaviour was verified separately with real tunnels.

{{< /details >}}

{{< details title="E3. How is the pipeline structured?" >}}

Five jobs. Preflight validates the cookie off-VPN and fails fast if it's expired. Audit runs 10 parallel shards, each opening a tunnel, capturing the exit IP and sending the playback request. Merge concatenates shards, enriches each exit IP and applies the pass or fail rule. Publish appends one line to the committed history and updates a Pages dashboard. Notify pages PagerDuty on failure. Triggers are a weekly schedule plus manual dispatch, with dev, int, stg and prd callers.

{{< /details >}}

{{< details title="E4. What does the pipeline alert on?" >}}

Pipeline health. A run fails and pages if more than 90% of attempts error or there are zero decisions. A low block rate is a finding, shown on the dashboard and alerted on the data, not a pager event, because paging on the thing the audit exists to report would make the pager noisy and meaningless.

{{< /details >}}

{{< details title="E5. Why 90% as the error threshold?" >}}

<span style="color:#f7921d"><strong>[Confirm]</strong></span> The report states the threshold but not how it was chosen. A defensible reason is that individual configs fail routinely (stale configs, a provider outage), and a few errors should not page anyone. The point where the audit has effectively produced nothing is when nearly everything errors. If asked, say that and say it's a tunable starting value, not a derived constant.

{{< /details >}}

{{< details title="E6. GitHub Actions limits you ran into or planned around?" >}}

The 6-hour per-job cap means a sweep of the full 28k-config pool in one run isn't practical; at 100 to 500 IPs a run it's fine. Minutes are covered by the org's Enterprise allocation, with a worst case of roughly USD 10 to 13 a month if metered. Concurrency is handled by sharding rather than fighting provider session caps.

{{< /details >}}

{{< details title="E7. How did you test the workflow without prd?" >}}

Per-environment callers (dev, int, stg, prd) with both schedule and manual triggers, so the workflow can be validated in int by manual dispatch and one scheduled run before prd is enabled.

{{< /details >}}

## F. Enrichment and cost

{{< details title="F1. What did the paid dependency do, and what replaced it?" >}}

The original enrichment came from one paid API, ipinfo, giving ASN, ISP and category. I found that the response's session state can be decoded server-side into the same kind of data (IP, ASN, ISP, categories, residential flag, city, country) over plain HTTP. The shipped workflow uses the free ipapi.is API for inline enrichment so it needs no internal network, and the session-state decode is an on-network option that also gives the IP HBO Max actually saw. The paid dependency is gone either way.

{{< /details >}}

{{< details title="F2. Where does the 26 dollars a month come from?" >}}

<span style="color:#f7921d"><strong>[Confirm]</strong></span> Fill this in once you have checked the source. Until then: "That's the plan price of the IPinfo tier the original used, a list price rather than a measured invoice."

{{< /details >}}

{{< details title="F3. What does the whole thing cost to run?" >}}

Mostly VPN subscriptions: about USD 462 a year for five providers shared, plus about USD 11 a month for an HBO Max account if one isn't already available, so roughly USD 462 to 594 a year. Enrichment, storage, Pages and secrets are free, and Actions minutes sit inside the Enterprise allocation. Those are estimates, and the report says so. The long pole was approvals, not money or engineering.

{{< /details >}}

## G. Behavioural

{{< details title="G1. What was the hardest part?" >}}

Getting a real signal at all. The login is protected by Arkose, nothing documented the auth chain end to end, and I couldn't just ask for credentials to automate around it. I captured a network trace against the test environment, redacted it, mapped the actual sequence, asked the owning team the right question, and confirmed their answer by decoding the token myself. That took the project from "can't run unattended" to a design that could.

{{< /details >}}

{{< details title="G2. Tell me about a time you changed your mind." >}}

The infrastructure recommendation. I'd argued for a Kubernetes CronJob on paper. I raised that going another way was a stakeholder question, then, once the Actions version was built and its two weak points were solved, I reversed my recommendation and wrote down why. I think being willing to say "the evidence changed" is part of the job.

{{< /details >}}

{{< details title="G3. How did you work with other teams?" >}}

InfoSec wrote the original tool, so I met them directly and went to them when stuck. The most useful one was the Arkose question, which got me the approved route in one answer instead of weeks of guessing. I also corrected a teammate's draft automation diagram that had the bootstrap and login steps in the wrong order, using the trace as evidence.

{{< /details >}}

{{< details title="G4. What did you learn?" >}}

That security and compliance review time, not engineering time, is often the real critical path: my infra choice came down as much to which option would get approved faster as to which was better technically. And that the valuable work was knowing what to build and defending that decision to experienced engineers, more than the volume of code.

{{< /details >}}

{{< details title="G5. Any mistakes or things you'd do differently?" >}}

Mid-project a real account password was accidentally pasted into an AI chat. It was flagged immediately and rotation was recommended. Since then my rule is to move credentials straight into a git-ignored file and only ever refer to paths. Technically, I'd also write the failure-rule threshold and the sampler quotas down as measured values from the first few runs rather than starting values.

{{< /details >}}

{{< details title="G6. How did you present the work?" >}}

I gave a 10-minute talk to senior engineers and product managers, and left behind a design record, the requirements map, the auth-chain writeup, the Docker findings, the infra decision with its comparison matrix, and the Actions system itself.

{{< /details >}}

## H. Follow-up traps

1. "Who produced the first 21.4%?" InfoSec's tool. You productized and validated the pipeline that makes it repeatable.
2. "How many IPs per weekly run?" 100 to 500 by requirement. 11,103 is the headline sample.
3. "Is the schedule live?" No.
4. "Does PagerDuty fire on a block?" No. On pipeline failure.
5. "Where is the 26 dollars from?" Confirm before the interview.
6. "Can you share the code?" It's WBD's, confidential. Offer to describe the design.
