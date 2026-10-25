---
title: "2 · Design decisions"
weight: 2
---

Four decisions carry the internship. Each is written as **options, criteria, choice, and what you would say if challenged**. These are the parts that show engineering judgement, so know them cold.

## Decision 1: how to measure (Method A vs Method B)

Before writing code you read DIANA's service code (Java / Spring) to find **where in the decision path VPN detection happens**, so the audit would measure the real thing and not a stand-in. That surfaced a fork. <span style="color:#0071bc"><strong>[Report]</strong></span>

```text
                     fresh VPN exit IP (captured through the tunnel)
                                   |
        +--------------------------+---------------------------+
        |                                                      |
  Method A: ask the detector directly              Method B: drive the real product
  call GeoGuard's lookup, replicate                POST a real HBO Max playbackInfo through
  the rule client-side                             the tunnel, read the 200 / 403
        |                                                      |
  measures the detection layer in isolation        measures the real, user-visible decision
```

| Dimension | Method A: direct GeoGuard lookup | Method B: HBO Max playback (chosen) |
|---|---|---|
| What it measures | A client-side **replica** of DIANA's rule (`isAnonymousVpn && !isResidentialProxy`) | The real 200 / 403 decision, the same number external audits report |
| Fidelity | Ignores overrides, simulation mode and last-seen, so it can **drift** from the contract number | Exercises DIANA's live online decision path exactly |
| Setup cost | Lowest: one token-protected HTTP call | Needs an entitled HBO Max account and cookie automation |
| Observed-IP requirement | Cannot capture the service-observed IP | Uniquely enables the "IP as seen by Max" and mismatch checks |
| Speed | About 0.1 to 0.3 s per IP, deterministic, parallelizable | About 2 to 5 s per attempt, more failure modes to guard |

**Choice: Method B.** The audit exists to report the number a real user experiences. Method A is cheaper but measures a *copy* of the rule that can quietly diverge from production, and it structurally cannot answer the observed-IP requirements. Method B also reuses the exact leg of the original tool that had already reproduced the ~20% figure, so it was the lower-risk build.

**If challenged: "A is 10x faster, why not that?"** Speed was never the bottleneck: the weekly run is 100 to 500 IPs. The risk was measuring the wrong thing. A fast, deterministic measurement of a replica is worse than a slower measurement of the real decision.

### The requirements-to-modifications map

You also produced a document mapping every requirement to a concrete change, with the explicit constraint that **DIANA itself does not change**. Highlights: an explicit normalized decision field; a balanced, seeded sampler; durable storage with retention; the enrichment join; and **two correctness guards**. <span style="color:#0071bc"><strong>[Report]</strong></span>

| Guard | What it catches |
|---|---|
| **Off-VPN control check**: a known non-VPN request must come back ALLOW | An expired cookie, which would otherwise return denials and fake a high block rate |
| **Leak check**: the tunnel's exit IP must differ from the runner's own IP | A tunnel that silently failed, so you would be measuring the runner and not a VPN |

## Decision 2: getting past login (the auth spike)

Automating HBO Max login is blocked by **Arkose** bot protection. A raw HTTP login returns `arkose.invalid.token`. The official methodology mentioned "Arkose bypass strings", so you asked InfoSec whether one existed for internal automation. <span style="color:#0071bc"><strong>[Report]</strong></span>

Their answer: **no bypass string exists.** Log in manually once and get a valid HBO Max auth token that is good for about 10 years, then reuse it. They described it as a legacy known issue, with auth tokens due to be reworked.

You then identified the exact artifact (a long-lived `st` cookie) and **confirmed its validity window by decoding the JWT**: the difference between its `exp` and `iat` claims is about 10 years. That became the sanctioned workaround, with the caveat that it is a workaround, not a permanent architecture.

To get there you captured a full Chrome DevTools network trace (a HAR) against the **int** test environment, redacted every sensitive value, filtered out third-party ad and analytics noise, and mapped the real sequence:

```text
client                             HBO Max gateway                   Arkose (FunCaptcha)
  | 1. GET v2_token?realm=bolt  --->  |   anonymous bootstrap
  | 2.  <--- x-wbd-session-state      |   anonymous session established
  | 3. login ------------------------>|   triggers a bot check
  |                                   | 4. challenge ---------------->   blocks raw HTTP clients
  |
  |  WORKAROUND: skip login, reuse the ~10-year "st" token
  |
  | 5. POST playbackInfo (cookie: st + session) --->
  | 6. <--- 200 = ALLOW   |   403 access.denied.vpn.usage = BLOCK
```

Findings worth remembering <span style="color:#0071bc"><strong>[Report]</strong></span>:

- **Ordering.** Bootstrap (`v2_token`) happens *before* login. You corrected a teammate's proposed automation diagram that had it reversed.
- **Arkose** sits at a specific `/fc/gt2/...` FunCaptcha path, and Fred (the team's own fraud system) also fires during login.
- **This is not a bot-detection bypass.** You asked the owning team, they confirmed no bypass exists, and you used a token mechanism they described and sanctioned, in a test environment. Say that sentence if anyone raises ethics.

## Decision 3: enrichment without Kafka (the highest-leverage find)

The original design assumed that category, ASN and region data had to come from DIANA's **internal Kafka event stream**, reachable only from inside the cluster. That would have forced the job to run in-cluster. <span style="color:#0071bc"><strong>[Report]</strong></span>

You found a **server-side endpoint that decodes the response's `x-wbd-session-state`** into plain JSON (IP, ASN, ISP, categories, residential flag, city, country) over ordinary HTTP. That removed the one dependency that made an in-cluster deployment feel mandatory, and it is what later made GitHub Actions viable.

Two byproducts:

1. **Proxy-over-VPN tripwire.** The IP a VPN *self-reports* can differ from the IP HBO Max *actually sees* when a provider routes streaming through a residential proxy. Comparing the two gives an `ip_mismatch` signal. It was rare (**110 of 9,134 tested**, about 1.2% <span style="color:#7c3aed"><strong>[Reasoned]</strong></span>) but expected to rise as DIANA improves.
2. **Cost.** A free public API (ipapi.is) can enrich the tunnel exit IP in the shipped pipeline, and the session-state decode gives the authoritative service-side view when on the network. See [section 5, bullet 5](../05-resume-bullets/) for how this maps to the resume line about IPinfo.

## Decision 4: where to run it weekly (Docker to GitHub Actions)

Revelio's needs <span style="color:#0071bc"><strong>[Report]</strong></span>:

- It must **build real VPN tunnels**, which needs `NET_ADMIN` and `/dev/net/tun`. That rules out serverless runtimes.
- Test 100 to 500 IPs per run without being cut off.
- Enrich results without depending on an internal-only system.
- Above all, **zero risk to DIANA's live traffic**.

| Option | Summary | Verdict |
|---|---|---|
| **A: inside DIANA** | Ride along with DIANA's own deployment | Ruled out: a heavy, privileged, multi-hour tunnel job next to a latency-sensitive production service is a noisy-neighbour risk |
| **B: GitHub Actions** | Scheduled workflow, mirroring the team's existing `geoguard-db-update` pattern; fresh single-use Linux VMs with full sudo and TUN | **Chosen** |
| **C: Kubernetes CronJob** | Purpose-built in-cluster batch job | Kept as the documented future path: the textbook primitive, but entirely net-new to build and security-review |

| Factor | A: DIANA | B: GitHub Actions | C: Kubernetes |
|---|---|---|---|
| Zero risk to DIANA's live traffic | No | Yes | Yes |
| Can build VPN tunnels (privileged) | Only by risking DIANA | Yes, proven | Not yet built |
| 100 to 500 IPs per run today | Yes | Yes | Not yet built |
| Safe parallelism across providers | n/a | Yes, tested across 5 | In theory |
| Enrichment without internal-only systems | n/a | Yes, inline | Yes |
| At least 1-year retention | n/a | Yes, committed history | Yes, via S3 |
| Full ~28k-config pool in one run | n/a | No, impractical (6-hour job cap) | Yes |
| Working today | n/a | **Yes** | No |
| Setup and maintenance cost | Low | Lowest, already paid | Higher, not yet spent |

### The honest reversal

Your earlier on-paper analysis recommended **Option C**, mainly for "no time cap" and because existing design docs already assumed an in-cluster job. You flagged that choosing otherwise was not a call to make unilaterally, since it meant surfacing a **stakeholder-alignment issue**, not just an engineering preference. Then two things changed the calculus <span style="color:#0071bc"><strong>[Report]</strong></span>:

1. **Working beats theoretical.** Option B had actually been built and validated end to end (real tunnels, real DIANA blocks, safe sharding, inline enrichment, alerting, dashboard). Option C was unbuilt and would need a security review with no internal precedent.
2. **Its two weak points were solved.** The fragile-sharding worry was answered by a proven provider-aware sharding mode, and the "needs in-cluster Kafka" worry was answered by the plain-HTTP enrichment path from the spike.

### The move away from Docker

Docker was right for **local, one-command reproducibility**. But a GitHub-hosted runner is already a fresh Linux VM: it can install OpenVPN directly and be destroyed after every run. So production runs the scripts **directly on the runner, with no Docker layer and no AWS**. Storage became a tiny committed history file instead of S3 or Databricks, and enrichment became a free public API instead of paid ipinfo or in-cluster Kafka. *Docker proved the probe; GitHub Actions shipped it.* <span style="color:#0071bc"><strong>[Report]</strong></span>

Option C stays the documented path if the audit ever needs to sweep the **full ~28,000-config pool in one run**, the one thing GitHub Actions' 6-hour per-job cap cannot comfortably do.

{{< callout type="info" >}}
**Why this matters for the resume.** Bullet 3 says you Dockerized the probe, and bullet 4 says you deployed a GitHub Actions pipeline. An interviewer will notice that the final system has no Docker in it. The answer above is the one to give: Docker was the right tool for the phase it served, and you chose to drop it when the platform made it redundant. That reads as judgement, not inconsistency.
{{< /callout >}}
