---
title: IBM
weight: 4
---

IBM's coding round includes a **project question**: you get a working Node.js / Express codebase for an event-ticketing platform called **ShowPass**, opened in a **Web IDE** with a terminal, and you have to **fix the promo-code validation**. Promo codes are being accepted when they should be rejected: deleted codes, expired codes, codes for another event, used-up codes, and orders below the minimum ticket count.

This section gives you the question as it appeared, the exact steps to solve it in the exam, the code, and a two-day plan with a practice project that copies the exam setup (server, curl scripts, `arguments.json`).

## At a glance

| | |
|---|---|
| **Where it appears** | Question 2 of the test (section S2 in the left bar); what Question 1 was is *not stated* |
| **Environment** | Web IDE with a built-in terminal; you start the Express server yourself |
| **Stack** | JavaScript, Node.js, Express |
| **Task** | Fix promo-code validation so that **deleted** codes are not found, **dates** (start and end) are enforced, **usage limits** are enforced, **event-specific** codes only work on their event, and the **minimum ticket quantity** is enforced |
| **Rules in detail** | `technical-specs/promo_code_validation.md`: response structure, validation rules, edge cases |
| **Architecture** | `documents/ARCHITECTURE.md` |
| **API docs** | Swagger at `/api-docs` while the server runs |
| **Testing helpers** | `curl_scripts/`: `01_register_user.sh`, `02_login.sh`, `15_create_promo_code.sh`, `16_validate_promo_code.sh`, `17_create_order.sh`; all inputs come from `arguments.json`; more in `curl_scripts/HELPER.md` |
| **How errors are raised** | Thrown from the service (`throw new …Error("message")`), not sent with `res` |
| **Time limit, scoring, hidden tests** | *not stated* |
| **Also reported for IBM** | A bash scripting question on a CSV file (top 20 rows, sorted ascending by one column and descending by another). It has its own local prep site, not part of this Playbook |

## Pages

{{< cards >}}
  {{< card link="01-promo-code-question" title="1 · The ShowPass promo-code question" subtitle="The statement, the files to open, the exact exam steps, the fix, and how to prove it with the curl scripts." icon="code" >}}
  {{< card link="02-two-day-prep" title="2 · Two-day prep" subtitle="Day 1: JavaScript basics, reading an Express project, the exam-shaped drill. Day 2: four similar drills, a timed redo and the checklist." icon="calendar" >}}
{{< /cards >}}

## Practice project

[Download ibm-promo-practice.zip](/downloads/ibm-promo-practice.zip) (14 KB). It copies the exam's shape: a buggy `validatePromoCode` in `src/services/`, a soft-deleted code, a server you start with `npm start`, and a `curl_scripts/` folder with the same script names and an `arguments.json`. It has 53 tests: 19 on the exam task plus 34 on the extra drills. Needs Node 18 or newer, no `npm install`.

{{< callout type="info" >}}
**Editor's note.** The statement, file names and script names come from your screenshots of the question. The field names, error classes and messages inside the real codebase were not visible, so the pages use the most likely ones (matching the Django version of the same question you were sent) and show you where to read the real ones in the first five minutes.
{{< /callout >}}
