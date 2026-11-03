---
title: 6 · Aptitude
weight: 6
---

Every TI online test starts with an **aptitude section: 20 questions in about 30 minutes** (roughly 90 seconds each). This page has the **20 aptitude questions from the TI assessment of 8 October 2026**, each with a full worked solution, and a list of the topics that those 20 questions test, in the order to study them.

{{< callout type="info" >}}
**How the answers were checked.** The answer key in the source PDF was compared against an independent solve. Every numeric answer was re-derived by hand and re-checked by script (the Q8 number machine, Q10 work schedule, Q5 letter pairs, Q9, Q12, Q17). Three questions are loosely worded: **Q2** (blood relation), **Q4** (school assignment) and **Q17** (which of A, B is faster). Their toggles say exactly which assumption the options force.
{{< /callout >}}

## What the 20 questions test

The PDF tags each question with a section name. Grouped by the skill they actually need:

| Skill | Questions | How many |
|---|---|:-:|
| **Ordering and seating** (left/right, before/after, queue positions) | Q1, Q3, Q14, Q20 | 4 |
| **Assignment and conditional logic** | Q4, Q15 | 2 |
| **Word problems that reduce to linear equations** | Q6, Q9, Q16, Q17 | 4 |
| **Probability** (dice, "books together") | Q13, Q18 | 2 |
| **Time and work** | Q10 | 1 |
| **Permutations and combinations** | Q11 | 1 |
| **Series, letter-number patterns, number machine** | Q8, Q19 | 2 |
| **Counting figures** (triangles in a grid) | Q12 | 1 |
| **Blood relations** | Q2 | 1 |
| **Letters of a word / alphabet positions** | Q5 | 1 |
| **Calendar** (days of the week) | Q7 | 1 |

Seven of the twenty (ordering, assignment, if-then rules, blood relation) are pure *reading and arranging* questions. They are the cheapest marks if you have a method, and the most expensive if you try to hold the picture in your head.

## Topics to study, in order

Study in this order: the early topics are the ones where a fixed method gives you full marks.

### 1 · Ordering, seating and queues (Q1, Q3, Q14, Q20)

- **Method:** draw empty slots `_ _ _ _ _ _` and put the *most definite* clue in first (a fixed end, "exactly in the centre"). Then place relative clues ("just to the left of", "just after").
- "Just to the left of X" means *adjacent*. "To the left of X" only means *somewhere before*. Mixing these up is the usual mistake.
- Statements like "A before B" are a chain: write `C → A → B` and read the first element.
- **Queue counting:** if A is *p*-th from the left and B is *q*-th from the right with *m* people between them, the total is *p + m + 1 + q* when A is on the left of B. When the order is not stated, try **both** orders and throw away the one that breaks another condition (Q14).

### 2 · Word problems to linear equations (Q6, Q9, Q16, Q17)

- Let the **smallest or the most-referenced quantity** be the variable (Sia = *S* in Q6; Basic = *b* in Q9).
- Write every other quantity in terms of it, then write the total as one equation.
- "The difference between A and B is 3" is **two cases**: A − B = 3 or B − A = 3. Check which case your options allow (Q17).
- **Weighted average:** total revenue = average × number of people (Q9).
- **Piecewise pay:** "x for the first 10 m, y for each extra metre" means pay = x + y × max(0, metres − 10) (Q16).

### 3 · Probability (Q13, Q18)

- Probability = favourable outcomes ÷ total outcomes, when all outcomes are equally likely.
- **Two dice:** 36 outcomes. Sum counts: 2→1, 3→2, 4→3, **5→4**, 6→5, 7→6, 8→5, 9→4, 10→3, 11→2, 12→1.
- **"k particular items together" among n:** treat the k as one block. Favourable arrangements = (n − k + 1)! × k!. Total = n!. So P = (n − k + 1)! k! / n!.

### 4 · Time and work (Q10)

- Convert to **units of work per day** using the LCM of the day-counts. P, Q, R take 12, 15, 20 days: take total work = LCM = 60 units, so they do **5, 4, 3 units a day**.
- Working together *adds* rates. When the problem restricts who may work on which day, list the **allowed daily totals**, then pick the largest allowed one each day.

### 5 · Permutations and combinations (Q11)

- **Choose first, then arrange.** *nCr* picks a group, *r!* orders it.
- **Restriction ("X must not be in slot 1"):** count all arrangements and subtract the forbidden ones, or count the allowed positions for X first, then fill the rest.
- *nCr* = n! / (r!(n − r)!), *nPr* = n! / (n − r)!.

### 6 · Calendar / odd days (Q7)

- A week has 7 days, so only **days mod 7** matters. 15 days later = +1 day. 100 days = +2. 365 days = +1 (non-leap year), 366 days = +2.
- Order the week on paper: Sun Mon Tue Wed Thu Fri Sat, then move forward by the remainder.

### 7 · Blood relations (Q2)

- Build a **family tree**, never solve it in words. Work **from the right end of the sentence** and substitute step by step.
- Standard reductions: *"my father's father's only son"* = my father (his father has only one son, and my father is one). *"Son-in-law of X"* = husband of X's daughter.
- When the wording allows two readings, **use the answer options to pick the one that has an answer.**

### 8 · Series, letter patterns, number machines (Q8, Q19, Q5)

- Learn the alphabet positions: **A=1, B=2, … Z=26**. Opposite letter = 27 − position (A↔Z, E↔V).
- In a mixed letter-number series, look at each *slot* separately: first letters go +1, the third goes +2, the fourth goes −2, the numbers go −2. **The position of the number can itself move** (Q19).
- **Number machine:** find what each step does by checking the *sum*, *difference*, *product*, *square*, *digit sum* of the previous step. A quick test is to see whether Step I + Step II equals the digit sum of the input (Q8). Decode the rule from one example, then **confirm it on every column** before applying it.
- For "pairs of letters with as many letters between them as in the alphabet": compute *(distance in word − 1)* and *(distance in alphabet − 1)* for each pair (Q5).

### 9 · Counting figures (Q12)

- A triangle needs **three different directions** of line. In a square grid with only horizontal and vertical lines plus one diagonal, every triangle has its hypotenuse on the diagonal and its legs on the grid lines.
- For an n × n grid with one full diagonal: **n(n + 1) triangles.** For n = 5 that is **30**.

### 10 · If-then constraints (Q15)

- "If A then B" is false only when A is true and B is false. Its useful twin: "not B ⇒ not A".
- With **two teams**, a player not in team 1 is in team 2. **Test each option against every rule** and eliminate on the first violation; do not try to build the answer from scratch.

### Beyond these 20

TI says only "aptitude"; this paper shows the style. For safety, add a one-hour pass over **percentages, ratio and proportion, speed-distance-time, simple/compound interest and profit-loss**, the standard campus-test set. They are *not* in these 20 questions, so treat them as extra cover. Good sources: R.S. Aggarwal *Quantitative Aptitude* and *Verbal and Non-Verbal Reasoning*. The Qualcomm section's [aptitude page](/companies/qualcomm/02-aptitude/) has twenty more questions of the same flavour for practice.

## Questions

Try each one before opening its toggle. Q1 to Q20 follow the numbering of the source PDF (*Texas_Instruments_All_60_Questions.pdf*, pages 1 to 20), so you can cross-check any question against it. The label *TI · assessment 8 Oct 2026* plus the section name is the PDF's own tag.

#### Q1 · Pens on a shelf

*TI · assessment 8 Oct 2026 · Logical Reasoning*

There are four pens: a red pen, a black pen, a green pen and a blue pen. The pens need to be kept in a shelf from left to right. The red pen should be on the left. The black pen should be kept just after the red pen and the blue pen should be on the right. The green pen should be on the left of the blue pen but on the right of the black pen. Which of the following pen is kept on the left of the black pen?

- **A.** Red
- **B.** Green
- **C.** Blue
- **D.** Cannot be determined

{{< details title="Show answer" closed="true" >}}
**Answer: A. Red.**

Four slots, left to right.

1. "Red should be on the left" → red in slot 1.
2. "Black just after red" → black in slot 2 (just after = adjacent).
3. "Blue on the right" → blue in slot 4.
4. "Green is on the right of black but on the left of blue" → green is between slots 2 and 4 → slot 3.

```text
Red | Black | Green | Blue
 1      2       3      4
```

The pen on the left of black is **Red**.

**Topic:** ordering. **Trap:** none, but place the end clues (red left, blue right) first and the rest falls out.
{{< /details >}}

#### Q2 · Photograph and family

*TI · assessment 8 Oct 2026 · Puzzles*

Pointing to a photograph Rita said "he is the son-in-law of the grand mother of my father's father's only son". How is Rita's father related to the wife of the man in photograph?

- **A.** Son-in-law
- **B.** Brother-in-law
- **C.** Nephew
- **D.** Brother

{{< details title="Show answer" closed="true" >}}
**Answer: C. Nephew**, but the sentence is ambiguous. The options force this reading.

**Step 1 · simplify the right end of the sentence.** Rita's father's father is Rita's grandfather. His *only son* is therefore **Rita's father**. So the sentence says: the man in the photo is the **son-in-law of the grandmother of Rita's father**.

**Step 2 · who is the man?** Call Rita's father F. The man in the photo is the husband of one **daughter of F's grandmother**. Which daughter is not stated, so there are two kinds of case:

| The daughter is… | The man in the photo | His wife | F is the wife's… | In the options? |
|---|---|---|---|---|
| F's **own mother** (possible only if the grandmother is F's mother's mother) | F's father, i.e. Rita's grandfather | F's mother | **Son** | No |
| **Any other daughter** of the grandmother, i.e. an aunt of F (his father's sister or his mother's sister) | F's uncle by marriage | F's aunt | **Nephew** | **Yes, option C** |

Only the second kind gives an answer among the four options, and it covers most of the possible daughters, so the intended answer is **C. Nephew**.

**Lesson:** when a relation puzzle is ambiguous, check each reading against the option list and keep the one that gives an option. Draw the tree; do not solve it in words. The source key also marks this question "ambiguous, C likely intended".
{{< /details >}}

#### Q3 · Marathon finish order

*TI · assessment 8 Oct 2026 · Logical Reasoning*

Four runners (R1, R2, R3 and R4) completed a marathon. R1 finished before R4 but after R2. R2 finished after R3. Who finished the marathon first?

- **A.** R1
- **B.** R2
- **C.** R3
- **D.** R4

{{< details title="Show answer" closed="true" >}}
**Answer: C. R3.**

Turn each sentence into an "earlier → later" arrow:

- "R1 before R4 but after R2" → R2 → R1 → R4
- "R2 after R3" → R3 → R2

Join the two chains at R2:

```text
R3 → R2 → R1 → R4     (left = finished first)
```

R3 is first. All four runners appear in one chain, so the order is fully fixed.
{{< /details >}}

#### Q4 · Five teachers, four schools

*TI · assessment 8 Oct 2026 · Logical Reasoning*

Five teachers I, J, K, L and M teach in four different schools. M and K do not teach in DPS, L teaches in St. Paul's and I teaches in St. Xavier's. If two teachers out of the five teach in Model school, which school does M teach in?

- **A.** St. Paul's
- **B.** St. Xavier's
- **C.** Model School
- **D.** Cannot be determined

{{< details title="Show answer" closed="true" >}}
**Answer: C. Model School.**

The question says the five teachers teach in **four different schools**: DPS, St. Paul's, St. Xavier's and Model. The natural reading is that every one of the four schools has at least one teacher. That is the assumption this answer needs.

1. L is in St. Paul's. I is in St. Xavier's.
2. Model has two teachers, so DPS, St. Paul's and St. Xavier's are left with the other three teachers; the five teachers split 1 (Paul's) + 1 (Xavier's) + 2 (Model) + 1 (DPS).
3. DPS needs exactly one teacher. M and K are *not* in DPS, and I and L are already placed. So **J** is in DPS.
4. The remaining two teachers, **K and M**, must be the two in Model school.

M teaches in **Model School**.

**Why not D?** If a school were allowed to be empty, M could also sit in St. Paul's or St. Xavier's, and the answer would not be fixed. "Four different schools" is what removes that option. The source key also states this assumption.
{{< /details >}}

#### Q5 · Pairs of letters in PRECISE

*TI · assessment 8 Oct 2026 · Puzzles*

How many such pairs of letters are there in the word 'PRECISE' which has as many letter between them (from both the sides) as in the alphabets from A to Z?

- **A.** 0
- **B.** 1
- **C.** 2
- **D.** 3

{{< details title="Show answer" closed="true" >}}
**Answer: A. 0.**

For a pair of letters, count the letters between them **in the word** and the letters between them **in the alphabet**. The pair qualifies only if the two counts are equal.

Alphabet positions: P = 16, R = 18, E = 5, C = 3, I = 9, S = 19.

The word is P(1) R(2) E(3) C(4) I(5) S(6) E(7). All 21 pairs, written as *(letters between in the word, letters between in the alphabet)*:

- **P:** R (0, 1), E (1, 10), C (2, 12), I (3, 6), S (4, 2), E (5, 10)
- **R:** E (0, 12), C (1, 14), I (2, 8), S (3, 0), E (4, 12)
- **E (3rd):** C (0, 1), I (1, 3), S (2, 13), E (3, no letters between E and E in the alphabet)
- **C:** I (0, 5), S (1, 15), E (2, 1)
- **I:** S (0, 9), E (1, 3)
- **S:** E (0, 13)

In no pair are the two numbers equal, so the answer is **0**. The closest misses are P–S (4 vs 2) and C–E (2 vs 1).

Reading "from both the sides" as "count from either end of the word" does not change this: the number of letters between two letters is the same whichever end you count from. Only a far-fetched reading that treats the word as a circle (counting the long way round) would make one pair, C–I, match; that is not the convention, and the key's answer is 0.
{{< /details >}}

#### Q6 · Five friends' piggy banks

*TI · assessment 8 Oct 2026 · Logical Reasoning*

Five friends - Rohan, Sia, Tanu, Varun, and Zoya - save money in their piggy banks.

- Together, they save ₹1,150.
- Rohan saves ₹150 more than Sia.
- Tanu saves twice as much as Sia.
- Varun saves the same amount as Rohan.
- Zoya saves ₹50 less than Sia.

How much does Tanu save?

- **A.** ₹250
- **B.** ₹280
- **C.** ₹300
- **D.** ₹320

{{< details title="Show answer" closed="true" >}}
**Answer: C. ₹300.**

Let Sia save ₹S. Everyone else in terms of S:

| Person | Amount |
|---|---|
| Sia | S |
| Rohan | S + 150 |
| Tanu | 2S |
| Varun | S + 150 (same as Rohan) |
| Zoya | S − 50 |

Total: S + (S + 150) + 2S + (S + 150) + (S − 50) = 6S + 250 = 1150.

6S = 900, so **S = 150**.

Tanu = 2 × 150 = **₹300**.

**Check:** Sia 150, Rohan 300, Tanu 300, Varun 300, Zoya 100. Sum = 1150 ✓.
{{< /details >}}

#### Q7 · Day after 15 days

*TI · assessment 8 Oct 2026 · Puzzles*

If today is Wednesday, ______ will be the day of the week after 15 days.

{{< details title="Show answer" closed="true" >}}
**Answer: Thursday.**

The week repeats every 7 days, so only the remainder matters: 15 = 2 × 7 + **1**.

After 14 days (two full weeks) it is Wednesday again. One more day makes it **Thursday**.

**Quick rule:** (number of days) mod 7 = how many days to move forward in the week. Sun, Mon, Tue, **Wed, Thu**, Fri, Sat: one step from Wednesday is Thursday.
{{< /details >}}

#### Q8 · Number arrangement machine

*TI · assessment 8 Oct 2026 · Puzzles*

A number arrangement machine, when given an input line of numbers, rearranges them following a particular rule in each step. The following is an illustration of input and rearrangement:

| | | | | | | |
|---|---|---|---|---|---|---|
| **Input** | 531842 | 764125 | 902317 | 648531 | 287964 | 413256 |
| **Step I** | 8 | 12 | 3 | 15 | 21 | 9 |
| **Step II** | 15 | 13 | 19 | 12 | 15 | 12 |
| **Step III** | 289 | 313 | 370 | 369 | 666 | 225 |
| **Step IV** | 64 (spans first two) | | 353 (spans middle two) | | 1 (spans last two) | |
| **Step V** | 10 | | 11 | | 1 | |

Step V is the last step of the rearrangement. As per the rules followed in the above steps, find the output for the input below.

| | | | | | | |
|---|---|---|---|---|---|---|
| **Input** | 825431 | 370962 | 641528 | 954210 | 718346 | 260871 |

Step V of the above input is ______.

{{< details title="Show answer" closed="true" >}}
**Answer: 3, 6, 18.**

**Decoding the machine (find the rule from the example, then test it on all six columns).**

*Steps I and II.* Add the digits of the first input: 5+3+1+8+4+2 = 23. Step I + Step II = 8 + 15 = **23**. This holds in all six columns, so Steps I and II split the six digits into two groups. Trying the six digit positions, only one split works for every column: **Step I = the digits in positions 2, 3, 5** (the *prime* positions) and **Step II = the digits in positions 1, 4, 6**.

Check on 531842: positions 2, 3, 5 are 3, 1, 4 → 3+1+4 = **8** ✓. Positions 1, 4, 6 are 5, 8, 2 → **15** ✓.

*Step III.* Square and add the two: 8² + 15² = 64 + 225 = **289** ✓. Also 12² + 13² = 313 ✓, 3² + 19² = 370 ✓, and so on.

*Step IV.* The six Step III numbers are 289, 313, 370, 369, 666, 225. The outputs are 64, 353, 1. Pair the numbers **from the outside in** (1st with 6th, 2nd with 5th, 3rd with 4th) and take the **difference**:

- 1st and 6th: 289 − 225 = **64** ✓
- 2nd and 5th: 666 − 313 = **353** ✓
- 3rd and 4th: 370 − 369 = **1** ✓

*Step V.* The **digit sum** of each: 6+4 = **10**, 3+5+3 = **11**, **1** ✓. (10 is not reduced again, so it is one pass of digit-summing, not repeated.)

**Applying it to the new input.**

| Input | Positions 2, 3, 5 (Step I) | Positions 1, 4, 6 (Step II) | Step III = I² + II² |
|---|---|---|---|
| 825431 | 2+5+3 = 10 | 8+4+1 = 13 | 100 + 169 = **269** |
| 370962 | 7+0+6 = 13 | 3+9+2 = 14 | 169 + 196 = **365** |
| 641528 | 4+1+2 = 7 | 6+5+8 = 19 | 49 + 361 = **410** |
| 954210 | 5+4+1 = 10 | 9+2+0 = 11 | 100 + 121 = **221** |
| 718346 | 1+8+4 = 13 | 7+3+6 = 16 | 169 + 256 = **425** |
| 260871 | 6+0+7 = 13 | 2+8+1 = 11 | 169 + 121 = **290** |

Step IV, outside in: |269 − 290| = **21**, |365 − 425| = **60**, |410 − 221| = **189**.

Step V, digit sums: 2+1 = **3**, 6+0 = **6**, 1+8+9 = **18**.

**Step V = 3, 6, 18.** The same rules were run by script on the example (they reproduce every row) and on the new input.
{{< /details >}}

#### Q9 · Streaming plans

*TI · assessment 8 Oct 2026 · Quant Math Ability*

A U.S. streaming service offers three plans: Basic at USD 15, Standard at USD 25, and Pro at USD 45 per month. There are 600 subscribers in total, and the average monthly revenue per subscriber is USD 26. Also, the number of Pro subscribers is 60 less than the number of Basic subscribers. How many Standard subscribers are there?

- **A.** 280
- **B.** 340
- **C.** 320
- **D.** 300

{{< details title="Show answer" closed="true" >}}
**Answer: D. 300.**

Let b = Basic, s = Standard, p = Pro subscribers.

1. Total: b + s + p = 600.
2. Pro is 60 less than Basic: p = b − 60.
3. Revenue: average × subscribers = 26 × 600 = 15 600, so 15b + 25s + 45p = 15 600.

**Eliminate p and s.** From (1) and (2): s = 600 − b − (b − 60) = 660 − 2b.

Substitute into (3):

15b + 25(660 − 2b) + 45(b − 60) = 15 600
15b + 16 500 − 50b + 45b − 2 700 = 15 600
10b + 13 800 = 15 600
10b = 1 800, so **b = 180**.

Then p = 180 − 60 = 120, and s = 600 − 180 − 120 = **300**.

**Check:** 15 × 180 = 2 700; 25 × 300 = 7 500; 45 × 120 = 5 400. Total = 15 600, and 15 600 / 600 = 26 ✓.
{{< /details >}}

#### Q10 · Wall built by three men

*TI · assessment 8 Oct 2026 · Quant Math Ability*

Three men P, Q and R working individually take 12 days, 15 days and 20 days respectively to construct a wall. Find the minimum time required to construct a wall if not more than 2 men are working together on a day and no same pair of men work on two consecutive days.

- **A.** 6.5 days
- **B.** 7 days
- **C.** 7.5 days
- **D.** 8 days

{{< details title="Show answer" closed="true" >}}
**Answer: B. 7 days.**

**Step 1 · rates.** Take the wall as LCM(12, 15, 20) = **60 units** of work.

- P does 60 / 12 = 5 units a day.
- Q does 60 / 15 = 4 units a day.
- R does 60 / 20 = 3 units a day.

**Step 2 · allowed daily outputs.** At most 2 men work on any day, so the biggest days are pairs:

| Pair | Units a day |
|---|:-:|
| P + Q | 9 |
| P + R | 8 |
| Q + R | 7 |

**Step 3 · the restriction.** The same pair may not work on two days in a row. So the best plan alternates the two *best* pairs: P+Q (9), then P+R (8), then P+Q (9), and so on.

| Day | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| Pair | PQ | PR | PQ | PR | PQ | PR | PQ |
| Units | 9 | 8 | 9 | 8 | 9 | 8 | 9 |
| Running total | 9 | 17 | 26 | 34 | 43 | 51 | **60** |

**Step 4 · why not fewer days.** Within 6 days the most you can do is 3 × 9 + 3 × 8 = 51 < 60 (you cannot use 9 twice in a row). So 6 days is not enough. On day 7 the plan needs exactly 9, which PQ supplies after a PR day. The wall is finished exactly at the end of day 7.

The answer is **7 days**. A script that tries every allowed sequence of pairs and singles also returns 7.
{{< /details >}}

#### Q11 · Event schedule

*TI · assessment 8 Oct 2026 · Quant Math Ability*

A management club has 5 distinct technical activities and 4 distinct strategy activities. For a short event, exactly 2 technical activities and exactly 1 strategy activity must be selected. The selected 3 activities will be conducted in three distinct slots: Slot 1, Slot 2, and Slot 3. The strategy activity must not be conducted in Slot 1. In how many ways can the event schedule be prepared?

- **A.** 120
- **B.** 140
- **C.** 160
- **D.** 180

{{< details title="Show answer" closed="true" >}}
**Answer: C. 160.**

**Choose, then arrange.**

1. Choose the 2 technical activities: 5C2 = **10** ways.
2. Choose the 1 strategy activity: 4C1 = **4** ways.
3. Arrange the 3 chosen activities in 3 slots with the strategy activity **not in Slot 1**:
   - All arrangements: 3! = 6.
   - Strategy in Slot 1 (forbidden): the other 2 activities fill Slots 2 and 3 in 2! = 2 ways.
   - Allowed: 6 − 2 = **4**.

   (Or directly: the strategy activity has 2 allowed slots (2 or 3), and the two technical ones fill the other two slots in 2! ways: 2 × 2 = 4.)

Total = 10 × 4 × 4 = **160**.

**Trap:** forgetting that the 3 activities are *distinct* and the slots are *distinct*, so order matters. Without the restriction the answer would be 10 × 4 × 6 = 240.
{{< /details >}}

#### Q12 · Triangles in a grid

*TI · assessment 8 Oct 2026 · Puzzles*

Use the figure given below to answer the question below. What is the number of triangles in the figure?

<div style="max-width:260px;margin:1rem 0">
<svg viewBox="0 0 220 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="A 5 by 5 square grid with the diagonal from the top-left corner to the bottom-right corner" style="width:100%;height:auto">
<g stroke="currentColor" stroke-width="1.5" fill="none">
<rect x="10" y="10" width="200" height="200"/>
<line x1="50" y1="10" x2="50" y2="210"/><line x1="90" y1="10" x2="90" y2="210"/><line x1="130" y1="10" x2="130" y2="210"/><line x1="170" y1="10" x2="170" y2="210"/>
<line x1="10" y1="50" x2="210" y2="50"/><line x1="10" y1="90" x2="210" y2="90"/><line x1="10" y1="130" x2="210" y2="130"/><line x1="10" y1="170" x2="210" y2="170"/>
<line x1="10" y1="10" x2="210" y2="210" stroke-width="2.5"/>
</g>
</svg>
</div>

- **A.** 30
- **B.** 27
- **C.** 20
- **D.** 15

{{< details title="Show answer" closed="true" >}}
**Answer: A. 30.**

The figure is a 5 × 5 grid of small squares with **one** diagonal, from the top-left corner to the bottom-right corner.

**Which triangles can exist?** A triangle needs three sides in three different directions. The only directions in this figure are horizontal, vertical and the diagonal. So every triangle has **one side on the diagonal, one horizontal side and one vertical side**: a right-angled isosceles triangle whose hypotenuse lies on the diagonal.

**Counting them.** Number the grid points along each side 0 to 5. The diagonal passes through the points (0,0), (1,1), …, (5,5). Pick any two of those 6 points as the ends of the hypotenuse: C(6, 2) = **15** ways. For each pair, the third vertex can be on either side of the diagonal (above or below), which gives **2** triangles.

Total = 15 × 2 = **30**.

**Same count by size** (legs of length k small squares; there are 6 − k hypotenuse positions, each on 2 sides):

| Leg length k | 1 | 2 | 3 | 4 | 5 | Total |
|---|:-:|:-:|:-:|:-:|:-:|:-:|
| Triangles | 10 | 8 | 6 | 4 | 2 | **30** |

The ten k = 1 triangles are the half-squares the diagonal cuts out of the five squares it crosses.

**General rule:** for an n × n grid with one full diagonal, there are n(n + 1) triangles. With n = 5 that is 30.
{{< /details >}}

#### Q13 · Three books together

*TI · assessment 8 Oct 2026 · Quant Math Ability*

15 books are placed on a table. The probability that three of the books will always be together is x/y. The value of x is 1 and the value of y is ______.

{{< details title="Show answer" closed="true" >}}
**Answer: 35.**

"Three particular books are together" is the standard block problem.

- **Total** arrangements of 15 books in a row: 15!.
- **Favourable:** glue the 3 books into one block. Now there are 15 − 3 + 1 = 13 objects, arranged in 13! ways. Inside the block the 3 books can be ordered in 3! ways. So favourable = 13! × 3!.

P = 13! × 3! / 15! = 3! / (15 × 14) = 6 / 210 = **1/35**.

So x = 1 and **y = 35**.

**Shortcut:** for n books, P(k particular books together) = (n − k + 1)! k! / n!. Here that is 13! 3! / 15! = 1/35.
{{< /details >}}

#### Q14 · Doctors in a queue

*TI · assessment 8 Oct 2026 · Logical Reasoning*

In a queue of more than 10 doctors, Dr. A is 9th from the left end and Dr. B is 3rd from the right end, there are three doctors between Dr. A and Dr. B. A total of ______ doctors are there in the queue.

{{< details title="Show answer" closed="true" >}}
**Answer: 15.**

The statement does not say which of A and B is nearer the left, so try both.

**Case 1: B is to the right of A.** A is at position 9. Three doctors between them occupy positions 10, 11, 12. So B is at position 13. B is 3rd from the right, so there are 2 doctors after B.

Total = 13 + 2 = **15**. (15 > 10, so the condition "more than 10" holds.)

**Case 2: B is to the left of A.** Three doctors between them occupy positions 6, 7, 8, so B is at position 5. B is 3rd from the right, so only 2 doctors stand after B, and the total would be 5 + 2 = 7. That is impossible, because A alone is at position 9, and it also breaks "more than 10".

Only Case 1 works. **Total = 15.**

**Formula check:** (from left to A) 9 + 3 doctors between + B + 2 after B = 9 + 3 + 1 + 2 = 15. ✓

**Topic:** queue counting. **Trap:** assuming B is on the right without checking; here the "more than 10" clause is the tie-breaker.
{{< /details >}}

#### Q15 · Football teams

*TI · assessment 8 Oct 2026 · Logical Reasoning*

Seven football players namely Gaurav, Harsh, Kunal, Lalit, Manish, Naman and Ojha are to be selected for one of the college teams, the Phoenix and the Devils.

- If Gaurav is selected for the Phoenix, then Harsh will be selected for the Devils.
- If Kunal is selected for the Phoenix, then Lalit and Manish will be selected for the Devils.
- Naman is selected on a different team than Ojha.
- Manish is selected on a different team than Gaurav.
- If Ojha is selected for the Phoenix, then Harsh will also play for the Phoenix.

Which of these could be a complete and accurate list of players in the Phoenix team?

- **A.** Gaurav, Kunal, Ojha
- **B.** Harsh, Manish, Naman, Ojha
- **C.** Kunal, Harsh, Lalit, Ojha
- **D.** Lalit, Manish, Naman

{{< details title="Show answer" closed="true" >}}
**Answer: D. Lalit, Manish, Naman.**

"Complete list of the Phoenix team" means everyone **not** listed is in the Devils. Check each option against all five rules and reject it at the first violation.

| Option | Phoenix | Rule broken? |
|---|---|---|
| A | Gaurav, Kunal, Ojha | **Rule 5.** Ojha is in Phoenix, so Harsh must be in Phoenix. Harsh is not listed, so he is in the Devils. ✗ |
| B | Harsh, Manish, Naman, Ojha | **Rule 3.** Naman and Ojha must be on different teams, but both are in Phoenix. ✗ |
| C | Kunal, Harsh, Lalit, Ojha | **Rule 2.** Kunal is in Phoenix, so Lalit must be in the Devils, but Lalit is in Phoenix. ✗ |
| D | Lalit, Manish, Naman | Devils: Gaurav, Harsh, Kunal, Ojha. Rule 1: Gaurav is not in Phoenix, so nothing is required. Rule 2: Kunal is not in Phoenix. Rule 3: Naman (Phoenix), Ojha (Devils) ✓. Rule 4: Manish (Phoenix), Gaurav (Devils) ✓. Rule 5: Ojha is not in Phoenix. ✓ |

Only **D** breaks nothing.

**Topic:** if-then rules. **Method:** elimination by option is faster than constructing a team.
{{< /details >}}

#### Q16 · Painter's earnings

*TI · assessment 8 Oct 2026 · Quant Math Ability*

A painter is paid x rupees for painting every 10 metres of a wall and y rupees for painting every extra metre. During one week, he painted 10 metres on Monday, 13 metres on Tuesday, 12 metres on Wednesday, 11 metres on Thursday, and 12 metres on Friday. What is his average daily earnings in rupees for the five-day week?

- **A.** x + (8/5)y
- **B.** (5x + 9y)/5
- **C.** 10x + (8/5)y
- **D.** 5x + 8y

{{< details title="Show answer" closed="true" >}}
**Answer: A. x + (8/5)y.**

Each day's pay = x (for the first 10 m) + y × (metres beyond 10).

| Day | Metres | Extra metres | Pay |
|---|:-:|:-:|---|
| Mon | 10 | 0 | x |
| Tue | 13 | 3 | x + 3y |
| Wed | 12 | 2 | x + 2y |
| Thu | 11 | 1 | x + y |
| Fri | 12 | 2 | x + 2y |

Weekly total = 5x + (0 + 3 + 2 + 1 + 2)y = **5x + 8y**.

Average per day = (5x + 8y) / 5 = **x + (8/5)y**.

**Trap:** option D is the *weekly total*, not the daily average. Divide by the 5 days.
{{< /details >}}

#### Q17 · Speeds of A, B, C and D

*TI · assessment 8 Oct 2026 · Quant Math Ability*

The difference between A's speed and B's speed is 3 km/hr. C's speed is twice that of A and B's speed is twice that of D. The difference between C and D speed is 30 km/hr. The speed of B is:

- **A.** 18 km/hr
- **B.** 19 km/hr
- **C.** 21 km/hr
- **D.** 24 km/hr

{{< details title="Show answer" closed="true" >}}
**Answer: D. 24 km/hr.**

Let D = d. Then B = 2d. Let A = a. Then C = 2a.

- C − D = 30 gives **2a − d = 30**.
- "Difference between A and B is 3" has **two cases**:

| Case | Equation | Solve | B |
|---|---|---|---|
| A is faster (a − 2d = 3) | a = 2d + 3; 2(2d + 3) − d = 30; 3d = 24 | d = 8, a = 19 | **16** (not an option) |
| B is faster (2d − a = 3) | a = 2d − 3; 2(2d − 3) − d = 30; 3d = 36 | d = 12, a = 21 | **24** |

Only the second case gives a value in the options, so **B = 24 km/hr**.

**Check:** D = 12, B = 24, A = 21, C = 42. B − A = 3 ✓. C = 2A ✓. B = 2D ✓. C − D = 30 ✓.

The wording does not say which of A and B is faster. The options settle it. Notice that 19 (option B) is A's speed in the other case, a decoy for people who solve the first case and stop at a.
{{< /details >}}

#### Q18 · Two dice, sum 5

*TI · assessment 8 Oct 2026 · Quant Math Ability*

Two dice are thrown simultaneously. What is the probability that the sum of the numbers shown on the two dice is 5?

- **A.** 1/6
- **B.** 1/9
- **C.** 2/27
- **D.** 1/12

{{< details title="Show answer" closed="true" >}}
**Answer: B. 1/9.**

Two dice have 6 × 6 = **36** equally likely outcomes. Pairs (first, second) with sum 5:

(1, 4), (2, 3), (3, 2), (4, 1): **4 outcomes**.

P = 4 / 36 = **1/9**.

**Trap:** (1, 4) and (4, 1) are *different* outcomes because the dice are distinct. Counting them once gives 2/36 = 1/18, which is not an option.
{{< /details >}}

#### Q19 · Letter-number series

*TI · assessment 8 Oct 2026 · Puzzles*

Which of the following will come in place of the question mark (?) in the following sequence so that it completes the sequence?

L12QK, MS10I, NUG8, O6WE, (?)

- **A.** P4YC
- **B.** PY4C
- **C.** PYC4
- **D.** PW4C

{{< details title="Show answer" closed="true" >}}
**Answer: B. PY4C.**

Split each term into its letters and its number.

| Term | Letters, in order | Number | Position of the number |
|---|---|:-:|:-:|
| L12QK | L, Q, K | 12 | 2nd symbol |
| MS10I | M, S, I | 10 | 3rd symbol |
| NUG8 | N, U, G | 8 | 4th symbol |
| O6WE | O, W, E | 6 | 2nd symbol |
| **?** | P, Y, C | 4 | 3rd symbol |

Each part follows its own rule:

- **First letter:** L, M, N, O, then **P** (+1 each step).
- **Second letter:** Q, S, U, W, then **Y** (+2 each step).
- **Third letter:** K, I, G, E, then **C** (−2 each step).
- **Number:** 12, 10, 8, 6, then **4** (−2 each step).
- **Where the number sits:** 2nd, 3rd, 4th, 2nd, so it cycles through 2, 3, 4 and the next position is the **3rd**.

Put P, Y, C in order and slot 4 into the 3rd symbol: **P Y 4 C = PY4C**.

**Why not the others:** A puts the 4 in 2nd place, but the cycle has moved on to the 3rd. C puts it last (4th). D has W as the second letter, but Q, S, U, W continues with Y.
{{< /details >}}

#### Q20 · Six people in a row

*TI · assessment 8 Oct 2026 · Logical Reasoning*

Arpita, Purna, Rina, Xola, Sofia and Zain are sitting in a row. Sofia and Zain are in the center. Arpita and Purna are at the ends. Rina is sitting just to the left of Arpita. ______ is to the immediate right of Purna.

{{< details title="Show answer" closed="true" >}}
**Answer: Xola.**

Six seats, numbered 1 to 6 from the left.

1. Sofia and Zain are in the centre → seats 3 and 4 (in some order).
2. Arpita and Purna are at the ends → seats 1 and 6.
3. Rina is just to the left of Arpita. Seat 1 has nobody to its left, so Arpita cannot be in seat 1. Arpita is in **seat 6**, Rina in **seat 5**, and Purna in **seat 1**.
4. The only person left is Xola, who takes **seat 2**.

```text
Purna | Xola | Sofia/Zain | Zain/Sofia | Rina | Arpita
  1      2        3           4          5       6
```

The person to the immediate right of Purna (seat 2) is **Xola**. The order of Sofia and Zain does not matter for this question.
{{< /details >}}

## Revision card (aptitude)

- [ ] Draw slots for every ordering puzzle; place fixed ends first; "just left" means adjacent
- [ ] Queue total = positions up to A + people between + 1 (for B) + people after B; try both orders when it is not stated
- [ ] Word problem: one variable for the base quantity, one equation for the total; "difference of 3" is two cases
- [ ] Time and work: total = LCM, rates add; restricted-pair problems alternate the two best pairs
- [ ] P(k particular items together among n) = (n − k + 1)! k! / n!; two dice: 36 outcomes, sum 5 has 4
- [ ] Choose first, then arrange; subtract forbidden arrangements
- [ ] Days mod 7; alphabet positions A=1 … Z=26
- [ ] Number machine: decode from one column, then verify on all columns before using the rule
- [ ] n × n grid with one diagonal has n(n + 1) triangles
- [ ] Blood relations: simplify from the right; if ambiguous, let the options choose the reading
