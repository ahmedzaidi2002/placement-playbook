---
title: "Sets and Venn diagrams"
weight: 7
---

10 questions asked by Accenture, EPAM, JSW, KLA, Oracle. Try each one first, then open the toggle: it gives the answer, why it is right, and the idea behind it explained from scratch.

### 1 · Q21-25, sets

*Asked by: Accenture (IDC paper)*

(21) 70 students paint; 52 use green, 38 use both green and red; how many use red?
[24 / 42 / 56 / 70] (22) 100 delegates speak English, 40 French, 20 both; how many speak at
least one? [110 / 100 / 140 / 120] (23) Of 50 students, 30 cleared both tasks, 37 bridge
crossing, 38 rock climbing; how many cleared none? [0 / 3 / 5 / 9] (24) 2000 attended; 1500 as
learners, 800 as trainers; how many only as trainers? [200 / 500 / 800 / 1500] (25) 400 readers
read science fiction or literature or both; 250 read science fiction, 230 literature; how many
read both? [80 / 160 / 220 / 400]

{{< details title="Answer and explanation" closed="true" >}}

**Answers: (21) 56 (22) 120 (23) 5 (24) 500 (25) 80**

**Why.**
- (21) Everyone uses green or red: 70 = 52 + R − 38 → R = 56.
- (22) At least one = 100 + 40 − 20 = 120.
- (23) Cleared at least one = 37 + 38 − 30 = 45; none = 50 − 45 = 5.
- (24) Only trainers = total − learners = 2000 − 1500 = 500 (everyone attended in at least one role).
- (25) Both = 250 + 230 − 400 = 80.

**Concept: inclusion–exclusion for two sets.** |A ∪ B| = |A| + |B| − |A ∩ B|. People in both groups get counted twice when you add the two group sizes, so subtract the overlap once. Any one of the four numbers (A, B, both, either) follows from the other three. "Neither" = total − |A ∪ B|.

{{< /details >}}

### 2 · Q21-27, sets and votes

*Asked by: Accenture (Dec paper)*

Of 727 club members, 600 favour cricket and 173 favour both cricket and hockey; everyone
favours at least one. (21) How many favour hockey? [250 / 300 / 560 / 600] (22) Only hockey?
[127 / 280 / 326 / 494] Game 1: 40, game 2: 67, game 3: 46; games 1&3: 8, 1&2: 26, 2&3:
28, all three: 2. (23) Only game 1? [3 / 8 / 15 / 23] (24) Only game 3? [12 / 16 / 32 / 46]
(25) Only game 2? [2 / 7 / 15 / 37] Bhimsingh won by 2000 votes with 55% of the total votes;
10% of the voters did not vote. (26) Votes for Bhimsingh? [2000 / 2750 / 4250 / 5500]
(27) Votes for the loser? [2000 / 2250 / 3500 / 4000]

{{< details title="Answer and explanation" closed="true" >}}

**Answers: (21) 300 (22) 127 (23) 8 (24) 12 (25) 15 (26) 5500 (27) 3500**

**Why.**
- (21) 727 = 600 + H − 173 → H = 300. (22) Only hockey = 300 − 173 = 127.
- (23) Only game 1 = 40 − 26 − 8 + 2 = 8. (24) Only game 3 = 46 − 8 − 28 + 2 = 12. (25) Only game 2 = 67 − 26 − 28 + 2 = 15.
- (26)–(27) Taking 55% as a share of all voters: 10% did not vote, so the loser has 35%. The 20% gap = 2000 votes, so there are 10,000 voters: winner 5500, loser 3500.

**Concept: "only" regions in a three-set Venn diagram.** Only A = |A| − |A∩B| − |A∩C| + |A∩B∩C|. You subtract both pairwise overlaps, but that removes the triple overlap twice, so add it back once. Drawing the three circles and filling from the centre outward avoids mistakes.

{{< /details >}}

### 3 · Q21-24, sets

*Asked by: Accenture (On-campus recall)*

(21) Of 36 students, 20 know English, 8 know both Hindi and English, 6 know neither. How many
know Hindi? (22) Of 100 students, 74 passed maths, 76 science and 60 both. How many failed both?
(23) In a library $2/3$ of the people have books, 12 have magazines, 6 have both, and 2 are
only watching. How many people are there? (24) 40 play football, 25 cricket, 15 both; each
plays at least one. How many players?

{{< details title="Answer and explanation" closed="true" >}}

**Answers: (21) 18 (22) 10 (23) 24 (24) 50**

**Why.**
- (21) 36 − 6 = 30 know at least one: 30 = 20 + H − 8 → H = 18.
- (22) Passed at least one = 74 + 76 − 60 = 90; failed both = 10.
- (23) N = (2N/3 + 12 − 6) + 2 → N/3 = 8 → N = 24.
- (24) 40 + 25 − 15 = 50.

**Concept: total = (at least one) + (neither).** Inclusion–exclusion gives "at least one"; the rest of the group is "neither". In (23), people only watching are the "neither" group.

{{< /details >}}

### 4 · Q22, three-subject test

*Asked by: EPAM (EPAM freshers test)*

Every student took Physics, Chemistry and Maths. 37 passed Physics, 4 passed only Physics
and Maths, 12 passed only Physics, 30 passed Chemistry, 40 passed Maths, and 29 passed at
least two subjects. Which of the following cannot be determined?

- **(a)** Number who passed both Physics and Chemistry
- **(b)** Number who passed only Chemistry
- **(c)** Number who passed only Maths
- **(d)** None of the above

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) the number who passed only Maths**

**Why.** Let t = passed all three, a = only Physics and Chemistry, b = only Chemistry and Maths.
1. Physics: 12 (only P) + 4 (only P and M) + a + t = 37 → a + t = 21. So "both Physics and Chemistry" = a + t = 21 is known.
2. At least two: a + 4 + b + t = 29 → b = 4.
3. Only Chemistry = 30 − (a + t) − b = 30 − 21 − 4 = 5: known.
4. Only Maths = 40 − 4 − b − t = 32 − t, which depends on t: unknown.

**Concept: Venn regions as unknowns.** A three-set diagram has 7 regions. Write each given total as a sum of regions; whatever can be expressed using only known combinations is determined, and anything still containing a free unknown is not.

{{< /details >}}

### 5 · three languages in a town of 400

*Asked by: JSW (Aptitude test)*

In a town of 400 people, 185 speak Latin, 165 speak German and 160 speak French. 40 people
speak only French and Latin, 20 speak only German and Latin, and 10 speak only French and
German. How many people speak only one language?

- **(a)** 303
- **(b)** 310
- **(c)** 250
- **(d)** 300

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) 310** (assuming everyone speaks at least one language)

**Why.** Let t speak all three. "Only two" groups total 40 + 20 + 10 = 70.
- Adding the three language totals counts each "exactly two" person twice and each "all three" person three times: 185 + 165 + 160 = 510 = (only one) + 2 × 70 + 3t.
- Town: (only one) + 70 + t = 400.
- From the first, only one = 370 − 3t. Then 370 − 3t + 70 + t = 400 → t = 20, so only one = 310.

**Concept: counting by multiplicity.** Sum of set sizes = (exactly one) + 2 × (exactly two) + 3 × (exactly three). Combined with the total count, this is often the fastest way through three-set problems.

{{< /details >}}

### 6 · only mathematics, from a Venn diagram

*Asked by: JSW (Aptitude test)*

A Venn diagram of 100 students shows mathematics only $= x$, both subjects $= 28$, physics
only $= x(x - 10)$, and neither $= 36$. Find the probability that a randomly chosen student
studies only mathematics.

- **(a)** $6/100$
- **(b)** $28/100$
- **(c)** $17/100$
- **(d)** $12/100$

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) 12/100**

**Why.** All regions add to 100: x + 28 + x(x − 10) + 36 = 100 → x² − 9x − 36 = 0 → (x − 12)(x + 3) = 0 → x = 12. P(only maths) = 12/100.

**Concept: Venn regions sum to the total.** Every student lies in exactly one region (only maths, both, only physics, neither). A count cannot be negative, so discard x = −3.

{{< /details >}}

### 7 · Q7, sets

*Asked by: KLA (IIT Delhi 2023)*

Last year 26 members of a club travelled to England, 26 to France and 32 to Italy.
No member travelled to both England and France, 6 travelled to both England and
Italy, and 11 travelled to both France and Italy. How many members travelled to at
least one of these three countries?

- **(a)** 67
- **(b)** 52
- **(c)** 73
- **(d)** 71

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) 67**

**Why.** Nobody visited both England and France, so nobody visited all three. Inclusion–exclusion: 26 + 26 + 32 − 0 − 6 − 11 + 0 = 67. (Regions: England only 20, France only 15, Italy only 15, England & Italy 6, France & Italy 11.) The photo's tick on 52 comes from a wrongly filled diagram.

**Concept: inclusion–exclusion for three sets.** |A∪B∪C| = |A| + |B| + |C| − |A∩B| − |A∩C| − |B∩C| + |A∩B∩C|. If any pairwise overlap is empty, the triple overlap is empty too.

{{< /details >}}

### 8 · only cricket

*Asked by: Oracle (HackerRank MCQ test)*

In a group of students, 60% like football and 40% like cricket. What percentage of students
like only cricket if 12% like neither football nor cricket?

- **(a)** 28
- **(b)** 14
- **(c)** 56
- **(d)** 42

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) 28%**

**Why.** 12% like neither, so 88% like at least one. Both = 60 + 40 − 88 = 12%. Only cricket = 40 − 12 = 28%.

**Concept: inclusion–exclusion with percentages.** Treat percentages like counts out of 100.

{{< /details >}}

### 9 · sports enthusiasts

*Asked by: Oracle (HackerRank MCQ test)*

In a company, 100 employees are randomly selected. 50 like watching football, 40 like
watching hockey and the rest like both. Find the number of employees who like to watch at
least one of the games.

- **(a)** 40
- **(b)** 90
- **(c)** 80
- **(d)** 20

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) 80** (the intended key; the wording is inconsistent)

**Why.** The setter means: 50 like football, 40 like hockey (totals), and the "rest", 100 − 50 − 40 = 10, like both. At least one = 50 + 40 − 10 = 80.

**Concept: totals vs "only".** "50 like football" normally means the whole football circle, including those who like both. Under that reading the union is 80. If 50 and 40 meant "only", the union would be 100, which is not offered.

{{< /details >}}

### 10 · Group Membership 3, three languages

*Asked by: Oracle (HackerRank 2025)*

A survey of 300 people was taken. Given the results, find how many people speak all
three languages: 85% speak English, 40% Spanish and 20% French; 32% speak both
English and Spanish, 13% both English and French, and 10% both Spanish and French.

- **(a)** 30
- **(b)** 32
- **(c)** 10
- **(d)** 60

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) 30**

**Why.** At least one = 85 + 40 + 20 − 32 − 13 − 10 + x = 90 + x percent. Everyone surveyed speaks at least one language, so 90 + x = 100 → x = 10%. 10% of 300 = 30 people. (Option (c), 10, is the percentage, a trap.)

**Concept: solving for the triple overlap.** If the union is known (here 100%), the three-set formula has one unknown, |A∩B∩C|. Convert to people at the end.

{{< /details >}}
