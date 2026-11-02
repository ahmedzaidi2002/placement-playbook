---
title: "Selection, scheduling and constraints"
weight: 12
---

5 questions asked by Accenture, EPAM, Oracle. Try each one first, then open the toggle: it gives the answer, why it is right, and the idea behind it explained from scratch.

### 1 · Q52-55, selection criteria

*Asked by: Accenture (IDC paper)*

A call-centre manager must (1) hold a management degree, (2) have at least 4 years of similar
experience at another call centre, (3) be more than 30 years old on 1 July 2003, and (4) have
6 months of international exposure. If (1) fails but the candidate has over 2 years of
international experience, the VP Operations interviews; if (4) fails, the HR manager
interviews. (52) Shakuntala: management degree, 3 years at a call centre, 29 years old.
(53) Rajiv: engineer, born 17/12/1974, manager in a hotel for 4 years. (54) Soma: 4 years at
two call centres, management degree, turned 30 in December 2002, no foreign posting mentioned.
(55) Salina: 4+ years at a call centre, MBA, 2 years with the UN in Singapore; age not given.

{{< details title="Answer and explanation" closed="true" >}}

**Answers: (52) rejected (53) not considered (54) interviewed by HR (55) data insufficient**

**Why.**
- (52) Shakuntala has only 3 years' experience (needs 4) and is 29 (needs over 30): fails, no exception applies.
- (53) Rajiv, born Dec 1974, is 28 on 1 July 2003, and has no call-centre experience: fails.
- (54) Soma meets the degree, experience and age conditions (30 in Dec 2002, so over 30 on 1 July 2003); only international exposure is missing, which sends her to the HR manager.
- (55) Salina's age is not given, so we cannot decide.

**Concept: rule tables.** Check each condition for each candidate. A failure in a condition with an exception goes to the named interviewer; any other failure rejects; missing information means "data insufficient". Compute ages on the stated date, not today.

{{< /details >}}

### 2 · Q51-55, team selection

*Asked by: Accenture (Previous year)*

From boys M, N, O, P, Q, R and girls G, H, I, J, K a team of six is chosen: M and J go
together; O cannot go with N; I cannot go with J; N goes with H; P and Q go together; K and R
go together. (51) Two girls, one of them I: the others? [GMRPQ / HNOPQ / KOPQR / KRMNP]
(52) Four boys including O and R: the others? [HIPQ / GKPQ / GJPQ / GJMP] (53) Four boys: which
cannot be the team? [GJMOPQ / HJMNPQ / JKMNOR / JKMPQR] (54) K and P in, three boys: the others?
[GIRQ / GJRM / HIRQ / IJRQ] (55) Three girls including J and K: the others? [GHNR / MNOG / MORG
/ NHOR]

{{< details title="Answer and explanation" closed="true" >}}

**Answers: (51) KOPQR (52) GKPQ (53) JKMNOR (54) GIRQ (55) MORG**

**Why (key rules):** M with J; O not with N; I not with J; N with H; P with Q; K with R.
- (53) JKMNOR has N and O together, which is forbidden.
- (51) With I, J is out, so M is out. Two girls including I: the second must be K (bringing R) or G or H; K O P Q R works (no J, no N).
- (52), (54), (55) are checked the same way against every pairing rule.

**Concept: pairing constraints.** Turn rules into "must go together" pairs and "cannot go together" pairs. Choosing one member of a "must" pair forces the other; check every option against all rules.

{{< /details >}}

### 3 · Q12, three-member team

*Asked by: EPAM (EPAM freshers test)*

A three-member team is formed from six consultants P, Q, R, S, T and U. If P is selected,
T must also be. Exactly one of R and S must be on every team. U cannot serve with T. Which
team is *not* permissible?

- **(a)** P-R-U
- **(b)** Q-R-T
- **(c)** Q-S-U
- **(d)** P-S-T

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) P-R-U**

**Why.** If P is chosen, T must be too. P-R-U has P without T (and T could not join anyway, since U cannot serve with T). The other teams satisfy all rules.

**Concept: conditional rules.** "If P then T" is broken only when P is in and T is out. Check each option for exactly that pattern.

{{< /details >}}

### 4 · Q15, valid conference schedule

*Asked by: EPAM (EPAM freshers test)*

Teams A, B, C and D present once each in four slots (9:00, 11:00, 2:00 and 4:00). Team A
cannot present first or last. If team B presents first, team D must present immediately
after. Team D must present in a slot after team B. If team C presents last, team A must
present immediately before. Which sequence is valid?

- **(a)** B, D, A, C
- **(b)** A, C, B, D
- **(c)** D, B, C, A
- **(d)** B, A, C, D

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) B, D, A, C**

**Why.** B first → D second ✓. D after B ✓. A third (not first or last) ✓. C last → A just before it ✓. (b) has A first, (c) has A last, (d) has B first without D second.

**Concept: check each option against each rule.** For "if X then Y" rules, an option fails only when X happens without Y.

{{< /details >}}

### 5 · recipe ingredients

*Asked by: Oracle (HackerRank MCQ test)*

The ingredients are apricots, bacon, cake, donuts, eggs, figs, grapes, hazelnuts and ice
cream. (1) If bacon is not used, then grapes, hazelnuts and ice cream are not used. (2) If
apricots are used then bacon and cake are used. (3) If donuts are not used, apricots are not
used. (4) Apricots and eggs are used. [cut off in the source] (the question line is off screen; the
options suggest "what is the minimum number of ingredients used?")

- **(a)** 2
- **(b)** 3
- **(c)** 4
- **(d)** 5

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) 5** (under the assumed question, "minimum number of ingredients used")

**Why.** Apricots and eggs are used (4). Apricots → bacon and cake (2). By the contrapositive of (3), apricots used → donuts used. Nothing else is forced. Minimum: apricots, eggs, bacon, cake, donuts = 5.

**Concept: contrapositive.** "If not donuts then not apricots" is the same as "if apricots then donuts". Apply every rule forward from the known facts and count what is forced.

{{< /details >}}
