---
title: IBM
weight: 4
---

IBM's coding round can include a **project question** instead of a classic DSA problem: you get an existing Node.js (JavaScript) backend for a ticket-booking app, and you have to finish **one function**, `validatePromoCode`, so that the project's tests pass. Nothing else in the codebase needs to change.

This section explains exactly what that question is, how to solve it in the exam, and a two-day plan with a practice project you can download and run.

## At a glance

| | |
|---|---|
| **Question type** | Fill in one function inside an existing project (not a from-scratch DSA problem) |
| **Language / stack** | JavaScript, Node.js backend (the code has a `services` folder, so it is a routes → controllers → services layout) |
| **Where the function is** | `services/` folder, in a file named like `promoCode…` (for example `promoCodeService.js`) |
| **What to write** | 5 to 8 `if` checks inside `validatePromoCode` |
| **How errors are reported** | `throw new Error("message")`, **not** `res.status(400).json(...)`. One `if` already in the function shows the pattern |
| **What decides your score** | The project's test cases: each one checks a rule and the exact error message |
| **Platform, time limit, number of questions in the round** | *not stated* |
| **Also reported for IBM** | A bash scripting question on a CSV file (top 20 rows, sorted ascending by one column and descending by another). It has its own local prep site, not part of this Playbook |

## Pages

{{< cards >}}
  {{< card link="01-promo-code-question" title="1 · The promo-code question" subtitle="What is asked, how the project is laid out, the 8 rules, the full solution with throw, and the traps that fail tests." icon="code" >}}
  {{< card link="02-two-day-prep" title="2 · Two-day prep" subtitle="Day 1: the JavaScript and project basics plus the main drill. Day 2: three similar drills, a timed redo and the exam checklist." icon="calendar" >}}
{{< /cards >}}

## Practice project

[Download ibm-promo-practice.zip](/downloads/ibm-promo-practice.zip) (5 KB). It is a small copy of the exam setup: a `services` folder with `validatePromoCode` half written (one rule given, seven `TODO`s), three more practice functions, and 34 tests. Needs Node 18 or newer and nothing else; run `npm test` inside the folder. Out of the box 10 tests pass and 24 fail; the goal is 34 out of 34.

{{< callout type="info" >}}
**Editor's note.** The project, its field names and its error messages follow the version of the question you described. The real exam's field names and messages may differ slightly, which is why the method on page 1 starts with reading the model and the tests before writing any code.
{{< /callout >}}
