---
title: "1 · The problem and what existed"
weight: 1
---

## The team and the systems around DIANA

You were embedded in **Fraud & Abuse Prevention**, part of Trust & Safety inside the Consumer org. The team's mission, in one line: decide, in real time, whether a stream request looks abusive, and act on it without hurting real subscribers. <span style="color:#0071bc"><strong>[Report]</strong></span>

| System | What it does |
|---|---|
| **DIANA** | The VPN / IP-block policy engine. Decides ALLOW or BLOCK on streaming requests. The subject of the project. |
| Flash | Mitigation and in-app messaging |
| Fred | Fraud and payment-signal evaluation |
| Draco | Scheduled Databricks jobs |

DIANA relies on **GeoGuard** detection data, shipped as a local MaxMind-format database. On a real request it evaluates a rule and returns a decision. The service is Java / Spring. <span style="color:#0071bc"><strong>[Report]</strong></span>

## The measurement gap

The problem was measurement, not the engine.

- DIANA's dashboards say how much traffic **appears** to be VPN, not how well DIANA **detects** VPN use.
- A metric like "DIANA blocks 0.07% of playback attempts" means nothing without knowing the true VPN rate. You need ground truth: traffic you **know** is VPN.
- Two 2025 audits (a third-party audit and GeoComply, August 2025) put real detection at about **20%**, against a contractual benchmark of about **50%**. After that there was no continuous, trusted visibility.

<span style="color:#0071bc"><strong>[Report]</strong></span>

The fix is an **observability harness built around DIANA**, not a change to DIANA. Connect through real VPNs, ask HBO Max to play something, and record what DIANA decides.

```text
 Revelio (the audit)                     DIANA (production path, unchanged)
 ------------------                      ---------------------------------
 real VPN connection  ->  real HBO Max playback request  ->  "is this a VPN?"  ->  ALLOW / BLOCK
                                                                                      |
 record DIANA's real answer  <-----------------------------------------------------'
```

Say this clearly in an interview: **Revelio does not modify DIANA.** It exercises the same live decision path a real user hits.

## What existed before you (the original Revelio)

Revelio was built by the **InfoSec** team for a Q1 2025 VPN vendor comparison. It already did the hard part: it tunnels through a real, paid VPN exit node with **OpenVPN**, sends a real HBO Max `playbackInfo` request through the tunnel, and reads DIANA's decision off the response.

| Response | Meaning |
|---|---|
| HTTP 200 | **ALLOW**: DIANA missed the VPN |
| HTTP 403 `access.denied.vpn.usage` | **BLOCK**: DIANA caught it |

It had **already reproduced the ~20% figure independently: 21.4% on 11,103 VPN IPs**. That is why the internship was framed as **productization**, not a rebuild. <span style="color:#0071bc"><strong>[Report]</strong></span>

{{< callout type="warning" >}}
**Be precise about credit.** The probe, the tunnel-and-playback idea and the first 21.4% run were InfoSec's. Your work was the layer that makes it repeatable, trustworthy and unattended. The report says this itself ("the bulk of the value was not new code"). Interviewers respect this, and an overclaim here is the easiest way to lose credibility. See [section 5](../05-resume-bullets/).
{{< /callout >}}

## The six gaps you closed

The original was a manual, run-once, laptop-scale script. Each gap below became a piece of your work. <span style="color:#0071bc"><strong>[Report]</strong></span>

| The original had | Which meant | What you built |
|---|---|---|
| A single manual CLI run | No scheduler, no run identity, no unattended operation | Weekly schedule plus manual dispatch in GitHub Actions |
| Round-robin over the whole local config pool | Badly skewed sample: about **62% ProtonVPN** on the prior run | A balanced, seeded sampler with per-provider quotas |
| The decision left implicit in the HTTP status | Geo-blocks and VPN-blocks looked the same | An explicit decision field: BLOCK / ALLOW / OTHER-DENY / ERROR |
| A local CSV read by hand in Excel | No durable storage, no history, no 1-year retention | Run artifacts plus a committed `history.jsonl` and a dashboard |
| Credentials and cookies on disk | No secrets management, no correctness guards | CI secrets, an off-VPN control check, a leak check |
| Enrichment from one paid API (ipinfo) | No category / ASN / region trend slices | Inline enrichment from a free public API, plus an on-network decode path |

The original scripts were `vpn_probe.py` (probe engine), `log_parser.py` (offline enrichment and reporting) and per-provider config downloaders. <span style="color:#0071bc"><strong>[Report]</strong></span>

## The requirements (CONS-12973)

| Requirement |
|---|
| At least 100 IPs tested to an ALLOW / BLOCK decision (preferably 500) |
| At least 5 major VPN providers, including NordVPN and ExpressVPN |
| Runs on a regular cadence, at least weekly (plus about 2-week ramp-stage runs at launch) |
| Stores IP, provider, ALLOW/BLOCK; at least 1-year retention |
| Reports the **% of IPs that resulted in a BLOCK** (the headline KPI) |
| Trend line broken down by category, ASN and region / country |
| IPs tested are those **as seen by HBO Max**, not self-identified (the hardest slice to source) |
| Detect when the self-identified IP differs from the Max-observed IP (proxy-over-VPN tripwire) |
| Auxiliary IP data: ASN, location, vendor category, residential flag |

<span style="color:#0071bc"><strong>[Report]</strong></span> The report tags each with a priority (P0 required for launch, P1 high-value follow-on). The PDF table is hard to read, so if you are asked which ones were P0, say "the cadence, storage, headline KPI and provider coverage were launch requirements" and do not recite the rest from memory.

Notice the numbers: the requirement is **100 to 500 IPs per run**. The **11,103** on your resume is the size of the sample behind the headline result, not the size of each weekly run. See [section 5](../05-resume-bullets/), bullet 1.
