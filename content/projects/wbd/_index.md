---
title: "Warner Bros. Discovery Internship"
weight: 5
sidebar:
  open: false
---

Summer 2026 software-engineering internship in **Fraud & Abuse Prevention** (Trust & Safety, Consumer org) at Warner Bros. Discovery. The project, **Revelio**, turned a one-off InfoSec script into a repeatable audit of how well **DIANA**, the VPN-detection service in front of HBO Max, actually blocks VPN traffic.

This is the only industry experience on the resume, so expect most of the interview time to land here. These pages are written so that every one of the five resume bullets can be explained, defended and, where needed, qualified.

{{< callout type="warning" >}}
**Private notes.** The source report is marked *Confidential, internal use*. These pages name internal systems (DIANA, Flash, Fred, Draco), tickets and the HBO Max auth flow. Keep this site local. If it is ever hosted publicly, remove this section first. In an interview, stay at the level the resume already uses: no tokens, no cookie names, no internal endpoints.
{{< /callout >}}

{{< cards >}}
  {{< card link="01-problem-and-context" title="1 · The problem and what existed" subtitle="DIANA, the measurement gap, the original Revelio from InfoSec, and exactly what was left for you to do." icon="search" >}}
  {{< card link="02-design-decisions" title="2 · Design decisions" subtitle="Method A vs Method B, the auth-chain spike, the enrichment discovery, and the Docker to GitHub Actions decision with its reversal." icon="light-bulb" >}}
  {{< card link="03-the-build" title="3 · The build" subtitle="Dockerized probe, the select() timeout bug, tunnel tests, then the sharded GitHub Actions pipeline, guards, alerting and dashboard." icon="cog" >}}
  {{< card link="04-results-and-status" title="4 · Results, cost and status" subtitle="The 21.4% finding with its limits, the numbers, the cost estimate and what is honestly not finished." icon="chart-bar" >}}
  {{< card link="05-resume-bullets" title="5 · Defending each resume bullet" subtitle="The five bullets one by one: what each means, the evidence, the soft spot, and the sentence to say." icon="clipboard-check" >}}
  {{< card link="06-interview-questions" title="6 · Interview questions" subtitle="About 40 questions with model answers: the project, design, networking and security, CI/CD, statistics, and behavioural." icon="chat" >}}
  {{< card link="07-must-know-checklist" title="7 · Must-know before the interview" subtitle="60-second and 2-minute pitches, numbers to have ready, claims to avoid, a one-page cheat sheet and a self-test." icon="clipboard-list" >}}
{{< /cards >}}

## At a glance

| | |
|---|---|
| Team | Fraud & Abuse Prevention, under Trust & Safety, Consumer org |
| Dates | May 2026 to July 2026 |
| Project | Revelio, "DIANA Simulated VPN Attack" (Jira CONS-12973 audit, CONS-70694 infra, CONS-69913 design) |
| What DIANA is | WBD's real-time VPN / anonymizer detection service: decides ALLOW or BLOCK on an HBO Max stream request |
| What Revelio does | Connects through a real VPN, sends a real HBO Max playback request, reads DIANA's real answer (HTTP 200 = ALLOW, 403 = BLOCK) |
| Headline result | 21.4% block rate (2,374 of 11,103 VPN IPs) against a contractual target of about 50%; a 2025 third-party audit found about 20% |
| Your three deliverables | The measurement design, the Dockerized probe, the infrastructure decision (and the GitHub Actions system built to prove it) |
| Status at the end | Prototype validated, production path built and proven; blocked on VPN provider subscriptions and a security review |

## The one-paragraph version

DIANA's dashboards showed traffic being blocked, but nobody had independently checked its catch rate against known VPN traffic. An InfoSec research script (Revelio) could do that once, by hand, on a laptop. I turned it into something a team can run weekly and trust: I read DIANA's service code and chose to measure the real user-visible decision rather than a replica of the rule, reverse-engineered the undocumented HBO Max auth flow to find a sanctioned way past the bot check, Dockerized and hardened the probe, then built and validated a sharded GitHub Actions pipeline with enrichment, correctness guards, alerting and a trend dashboard. The result matched an independent audit: DIANA catches roughly two in five of the VPN streams it is contractually expected to.

## Evidence labels used in these pages

- <span style="color:#0071bc"><strong>[Report]</strong></span> Stated in your internship report (`Ahmed_Zaidi_Internship_Report.pdf`). You can say it as fact.
- <span style="color:#7c3aed"><strong>[Reasoned]</strong></span> Derived here by arithmetic or argument from the report's numbers. Not stated in the report. Say "I'd expect" or "roughly".
- <span style="color:#f7921d"><strong>[Confirm]</strong></span> On the resume but **not** in the report, or worded differently there. Check it against your own memory and the repo before you rely on it.

{{< callout type="info" >}}
**What these pages were built from.** Only the internship report. The Revelio repository itself is not on this machine, so no code line, test name or commit is cited. If an interviewer asks for a detail the report does not give (a function name, a workflow filename), say what you remember and do not guess.
{{< /callout >}}
