---
title: "3 · The build"
weight: 3
---

Two phases: first the **Dockerized, hardened probe**, then the **GitHub Actions system**. Everything here is from the internship report unless labelled otherwise. <span style="color:#0071bc"><strong>[Report]</strong></span>

## Phase 1: Dockerizing and hardening the probe

Ticket: "Docker and Local Setup for Revelio". The goal was a tool that runs and verifies with **one command, on any machine, with no credentials**, so you can prove the environment is sound before touching anything real.

Packaged with a Dockerfile, a `docker-compose.yml`, an entrypoint and a WBD-style Makefile.

| Command | Result |
|---|---|
| `make selftest` | Builds the image, verifies the environment: **READY**. Confirmed `openvpn 2.6.14`, `/dev/net/tun` present, **28,326 configs across 6 providers** discovered |
| `make test` | **16 / 16 offline unit tests** pass: decision classifier, header building, balanced sampling, env helpers. No network or credentials needed |
| `make report` | Sample log to CSV pipeline works end to end |

The image was verified clean: no secrets or configs baked in.

**Why "offline" matters.** A test that needs a VPN, a cookie and a live service is slow, flaky and cannot run in CI. The 16 tests cover the *pure logic* (classifying a response, building headers, sampling, parsing environment), which is where bugs hide and where a test is cheap.

### A real bug: the `wait_for_tunnel` hang

A NordVPN config that hit a network-level "connection refused" took about **75 seconds** even though the connect timeout was **30 seconds**.

- **Root cause.** The wait loop read the VPN process's output with a blocking `readline()`. If the VPN process went silent, `readline()` blocked and the deadline was **never re-checked**.
- **Fix.** Replace it with a `select()`-based bounded read, so each wait is capped by the time left before the deadline.
- **Proof.** Deterministic: a process kept silent for 20 s with a 5 s timeout now bails at **5.01 s**.

```text
before:  while not timed_out:  line = proc.stdout.readline()   # blocks forever if proc is silent
after:   while time_left > 0:  ready = select([proc.stdout], [], [], time_left)
                               if ready: line = proc.stdout.readline()
                               # loop re-checks the deadline every iteration
```

(The snippet is a sketch of the idea, not the repo's code.) <span style="color:#7c3aed"><strong>[Reasoned]</strong></span>

### Tunnel health across 5 providers

Using **intentionally fake credentials**, 29 real configs were tested. Reaching `AUTH_FAILED` after a full TLS handshake proves the tunnel, network path and certificate chain are healthy; only the deliberately wrong password fails, which is the last possible failure point.

| Provider | Configs | Outcome | Typical time |
|---|---|---|---|
| NordVPN | 12 | 12 / 12 healthy | 2 to 5 s |
| SurfShark | 4 | 4 / 4 healthy | 2 to 3 s |
| PrivateInternetAccess | 5 | 5 / 5 healthy | 1 to 3 s (fastest) |
| ProtonVPN | 5 | 5 / 5 healthy | 7 to 10 s (slowest) |
| ExpressVPN | 3 | **3 / 3 broken** | fails before auth |
| **Total** | **29** | **26 healthy, 3 broken caught** | |

ExpressVPN failed because the scraped `.ovpn` files were **missing their CA certificate**: a config-pipeline defect, not a code bug, and exactly the stale-pool problem a weekly audit is meant to surface.

### The proof point: first real DIANA decision

Using a manually captured cookie and playback body from a real browser session, the pre-flight control check returned **control OK (HTTP 200, ALLOW)**. The first time a real HBO Max response was read and classified by the probe: auth chain, classifier and request shape all worked against a live backend.

## Phase 2: the GitHub Actions system

A set of GitHub Actions workflows plus the productized probe, laid out to drop into the team's fraud-and-abuse-prevention repository following its existing `geoguard-db-update` conventions.

```text
weekly schedule + manual dispatch
        |
   preflight          validate the HBO cookie off-VPN (expired cookie -> fail fast)
        |
   audit              10 parallel shards, fail-fast: false
        |             each shard: open tunnel -> capture exit IP -> POST playbackInfo -> 200/403
        |                         -> capture session state
   merge              concatenate shards -> enrich each exit IP inline (ipapi.is:
        |             ASN / ISP / category / residential / region) -> apply pass/fail rule
   publish            append ONE line to committed history.jsonl + GitHub Pages dashboard (Chart.js)
        |
   notify (on failure) -> PagerDuty
```

### What each piece does

| Capability | How it works |
|---|---|
| **Safe sharding** | Work splits across **10 parallel shards**. In the default *provider* mode each provider is pinned to **exactly one shard** and its configs run **sequentially**, so at most one session per provider account is live. This avoids tripping providers' concurrent-session caps. Tested across 5 real providers |
| **Inline enrichment** | The merge job looks up each tunnel exit IP against the public **ipapi.is** API: ASN, ISP, category (vpn / proxy / hosting), residential, city, country. No internal network needed. An optional on-network decode path adds the authoritative service-observed IP and `ip_mismatch` as a later cross-check |
| **Explicit decision** | Every attempt is normalized to **BLOCK / ALLOW / OTHER-DENY / ERROR**, so geo-blocks and errors never contaminate the headline KPI |
| **Correctness guards** | Off-VPN control check (must ALLOW, or the cookie expired) and a leak check (exit IP must differ from the runner's IP) |
| **Failure rule** | A run **fails** (and pages PagerDuty) only if the **ERROR rate is above 90%** or there are **zero decisions**. A *low block rate is not a failure*: that is an audit finding, alerted separately on the data |
| **Storage and retention** | The full result of each run is a workflow artifact. One compact summary line per run is committed to `history.jsonl`, which is tiny and doubles as the 1-year durable record |
| **Dashboard** | GitHub Pages: headline block rate, block-rate and per-provider trends, the category / ASN / region slices, a run-history table |
| **Environments** | Per-environment callers (dev / int / stg / prd) with schedule and manual triggers, so it can be validated in int before prd is enabled |

**Validated end to end:** real OpenVPN tunnels built from GitHub-hosted runners, real exit IPs captured, real HBO Max `playbackInfo` requests sent, real DIANA BLOCK decisions recorded, with provider-aware sharding across five providers, inline enrichment, the pass/fail rule and the trend dashboard all running.

### Why each design choice is there

| Choice | Reason |
|---|---|
| One provider pinned to one shard, sequential inside it | Providers cap concurrent sessions per account. Parallelising across providers gives speed without breaking that cap |
| `fail-fast: false` | One broken provider or shard should not cancel the other nine and lose the whole week's data |
| Preflight off-VPN control check | An expired cookie makes every request look denied, which would be recorded as a spectacular block rate and be completely wrong |
| Leak check | If the tunnel did not come up, you would be measuring the runner's IP, not a VPN's |
| Four-way decision (BLOCK / ALLOW / OTHER-DENY / ERROR) | The KPI is `BLOCK / (BLOCK + ALLOW)`. Geo-blocks and errors are neither, and must not move it |
| Failure rule only on infra health | The audit's job is to report a number. A low number is the finding, not an outage. Paging on it would train people to ignore the pager |
| Committed `history.jsonl` instead of S3 or a database | One tiny line per week is cheap, versioned, reviewable, and removes AWS from the approval path |

## What is intentionally *not* built

- No change to DIANA.
- No in-cluster Kafka dependency.
- No Docker in the production workflow.
- No full-pool (28k) sweep in one run. That is the documented trigger for revisiting Kubernetes.
