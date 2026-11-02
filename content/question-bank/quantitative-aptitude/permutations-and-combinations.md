---
title: "Permutations and combinations"
weight: 3
---

15 questions asked by EXL, Flipkart, KLA, MathWorks, NVIDIA, Plutus, Qualcomm, Siemens Energy, Texas Instruments. Try each one first, then open the toggle: it gives the answer, why it is right, and the idea behind it explained from scratch.

### 1 · seven people, three not together

*Asked by: EXL (HackerEarth test, 2025)*

Seven people, Alice, Bob, Mike, Tara, Anita, Lisa and Paul, sit in a row. In how many ways
can they sit so that Alice, Mike and Lisa are not seated together?

- **(a)** 5760
- **(b)** 5040
- **(c)** 4680
- **(d)** 4320

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) 4320**

**Why.**
1. All arrangements of 7 people: 7! = 5040.
2. Arrangements where Alice, Mike and Lisa sit together: glue them into one block. Then there are 5 units (the block + 4 others): 5! = 120 ways, and the three can be ordered inside the block in 3! = 6 ways: 720.
3. Not all three together: 5040 − 720 = 4320.

**Concept: complement counting and the "glue" trick.** Counting "not together" directly is messy, so count everything and subtract the "together" cases. To count "together", treat the group as one big person, arrange the units, then multiply by the ways to arrange people inside the group. ("No two of them adjacent" is a stronger condition and would give 1440.)

{{< /details >}}

### 2 · teams with at least three women

*Asked by: Flipkart (Neev 2025)*

Out of 6 women and 4 men, a team of 5 is to be formed with at least three women. In how
many ways can it be done?

- **(a)** 196
- **(b)** 216
- **(c)** 326
- **(d)** 186

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) 186**

**Why.** At least 3 women in a team of 5 from 6 women and 4 men:
- 3 women + 2 men: C(6,3) × C(4,2) = 20 × 6 = 120
- 4 women + 1 man: C(6,4) × C(4,1) = 15 × 4 = 60
- 5 women: C(6,5) = 6
Total = 186.

**Concept: "at least" means add the separate cases.** Split by the exact number of women, count each case with combinations (order inside a team does not matter), and add. C(n, r) = n!/(r!(n − r)!) is the number of ways to choose r from n.

{{< /details >}}

### 3 · Q16, lock codes

*Asked by: KLA (IIT Delhi 2023)*

A three-digit code for certain locks uses the digits 0-9 under these constraints: the
first digit cannot be 0 or 1, the second digit must be 0 or 1, and the second and
third digits cannot both be 0. How many different codes are possible?

- **(a)** 144
- **(b)** 168
- **(c)** 176
- **(d)** 152

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) 152**

**Why.**
1. First digit: anything except 0 and 1: 8 choices. Second: 0 or 1: 2 choices. Third: any of 10. That gives 8 × 2 × 10 = 160.
2. Remove the codes whose second and third digits are both 0: 8 × 1 × 1 = 8.
3. 160 − 8 = 152.

**Concept: multiplication principle, then subtract the forbidden ones.** When choices are made one after another independently, multiply the number of options at each step. If a rule ties two positions together, count without it first and subtract the cases that break it.

{{< /details >}}

### 4 · Q3, non-negative solutions

*Asked by: MathWorks (IIT Bombay 2024)*

How many non-negative integer solutions has $x_1 + x_2 + x_3 = 11$?

- **(a)** 77
- **(b)** 78
- **(c)** 79
- **(d)** 56

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) 78**

**Why.** Distribute 11 identical units into 3 boxes, boxes may be empty: C(11 + 3 − 1, 3 − 1) = C(13, 2) = 78. (The candidate's tick on 56 is wrong.)

**Concept: stars and bars.** Write the 11 units as stars and use 2 bars to cut them into 3 groups, e.g. ★★|★★★★★|★★★★ means (2, 5, 4). Every arrangement of 11 stars and 2 bars in a row is one solution, so the count is "choose 2 bar positions out of 13": C(13, 2). In general, non-negative solutions of x₁ + ... + x_k = n number C(n + k − 1, k − 1).

{{< /details >}}

### 5 · Q4, at least two women

*Asked by: MathWorks (NIT Durgapur 2024); MathWorks (IIIT Delhi 2024)*

A committee of 5 is formed from 6 men and 4 women with at least 2 women. In how many ways?

- **(a)** 145
- **(b)** 215
- **(c)** 186
- **(d)** 340

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) 186**

**Why.** At least 2 women among 5 chosen from 6 men and 4 women:
- 2W 3M: C(4,2) × C(6,3) = 6 × 20 = 120
- 3W 2M: C(4,3) × C(6,2) = 4 × 15 = 60
- 4W 1M: C(4,4) × C(6,1) = 6
Total 186.

**Concept: case split on the restricted group.** Same method as any "at least k" committee: list each allowed exact count, multiply the choices from each group, and add. Check: the complement (0 or 1 woman) is C(6,5) + 4 × C(6,4) = 6 + 60 = 66, and C(10,5) − 66 = 186.

{{< /details >}}

### 6 · Q6, two who refuse

*Asked by: MathWorks (NIT Durgapur 2024)*

A committee of 5 is formed from 10 people; 2 particular people refuse to serve together.
In how many ways?

- **(a)** 252
- **(b)** 196
- **(c)** 120
- **(d)** 90

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) 196**

**Why.** All committees: C(10,5) = 252. Committees with both of the two quarrelling people: they take 2 seats, the other 3 come from the remaining 8: C(8,3) = 56. Allowed = 252 − 56 = 196.

**Concept: subtract the forbidden pairings.** "Two particular people are not together" is easiest by complement: total minus the ones where both are in.

{{< /details >}}

### 7 · Q9, arrangements of COMMUNICATION

*Asked by: NVIDIA (SSE NCG, Nov 2024)*

In how many different ways can the letters of the word "COMMUNICATION" be arranged in
a line?

- **(a)** 5940
- **(b)** 11880
- **(c)** 831600
- **(d)** None of the above

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) none of the above** (the count is 194,594,400)

**Why.** COMMUNICATION has 13 letters: C ×2, O ×2, M ×2, N ×2, I ×2, and U, A, T once. Arrangements = 13!/(2!)⁵ = 6,227,020,800/32 = 194,594,400.

**Concept: permutations with repeated letters.** If letters repeat, swapping two identical letters gives the same word, so divide n! by k! for every letter that appears k times.

{{< /details >}}

### 8 · mathematicians in rooms

*Asked by: Plutus (OA)*

$N$ mathematicians and $k$ rooms: in how many ways can they arrange themselves?

{{< details title="Answer and explanation" closed="true" >}}

**Answer: k^N** under the usual reading (distinct rooms, rooms may stay empty). The statement does not fix the conditions, so know the other cases too.

**Why.** Each of the N mathematicians independently picks one of k rooms: k × k × ... × k = k^N.
- Distinct rooms, none empty: k! × S(N, k) = Σᵢ (−1)ⁱ C(k, i)(k − i)^N (inclusion–exclusion).
- Identical rooms, none empty: S(N, k), the Stirling number of the second kind.

**Concept: functions vs partitions.** Assigning people to labelled rooms is counting functions from N people to k rooms: k^N. Requiring every room to be used means counting onto functions, done by subtracting assignments that miss a room (inclusion–exclusion). If rooms are unlabelled, you only care how people are grouped, which is what S(N, k) counts.

{{< /details >}}

### 9 · Q1, team with one officer

*Asked by: Qualcomm (Nov 2024 (HirePro))*

From 4 officers and 8 jawans, in how many ways can a team of six be chosen to include exactly
one officer?

- **(a)** 275
- **(b)** 250
- **(c)** 224
- **(d)** 330

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) 224**

**Why.** Exactly one officer: choose 1 of 4 officers (4 ways) and the remaining 5 members from the 8 jawans: C(8,5) = 56. Total 4 × 56 = 224.

**Concept: "exactly" fixes each group's count.** Choose from each group separately and multiply.

{{< /details >}}

### 10 · Q12, team with at least two women

*Asked by: Qualcomm (Nov 2024)*

Out of 9 women and 6 men, a team of 3 is to be formed so that at least two members are women.
In how many ways can it be done?

- **(a)** 350 ways
- **(b)** 400 ways
- **(c)** 280 ways
- **(d)** 300 ways

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) 300**

**Why.** At least two women in a team of 3 from 9 women and 6 men:
- 2 women + 1 man: C(9,2) × 6 = 36 × 6 = 216
- 3 women: C(9,3) = 84
Total 300.

**Concept: add the exact cases of an "at least" condition.**

{{< /details >}}

### 11 · Problem Solving

*Asked by: Qualcomm (60-question online assessment)*

A team of 2 people is to be chosen from 7 friends. How many different teams are possible?

- **(a)** 10
- **(b)** 12
- **(c)** 15
- **(d)** 21

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) 21**

**Why.** A team is a set; order does not matter. C(7,2) = 7 × 6/2 = 21.

**Concept: combination vs permutation.** Choosing (unordered) uses C(n, r); arranging (ordered) uses P(n, r) = n!/(n − r)!. Picking A then B gives the same team as B then A, so divide the 7 × 6 ordered picks by 2.

{{< /details >}}

### 12 · C4, tallest boy at an end

*Asked by: Siemens Energy (MNNIT Allahabad (Mettl))*

In how many ways can five boys A to E, of different heights, be seated in a row so that the
tallest boy is at one of the ends?

{{< details title="Answer and explanation" closed="true" >}}

**Answer: 48**

**Why.** The tallest boy takes one of the two end seats: 2 ways. The other 4 boys fill the remaining 4 seats in 4! = 24 ways. Total 2 × 24 = 48.

**Concept: place the restricted item first.** Fix whoever has a condition, then arrange the rest freely and multiply.

{{< /details >}}

### 13 · forming a choir

*Asked by: Texas Instruments (IIT ISM 2024)*

Choose 3 of 7 boys and 2 of 10 girls; one particular boy and girl refuse to be together.

- **(a)** 1460
- **(b)** 1540
- **(c)** 1440
- **(d)** 1600

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) 1440**

**Why.**
1. Without restriction: C(7,3) × C(10,2) = 35 × 45 = 1575.
2. Choirs containing both the particular boy and girl: the other 2 boys from 6, the other girl from 9: C(6,2) × 9 = 15 × 9 = 135.
3. Allowed = 1575 − 135 = 1440.

**Concept: complement for "not together".** Count all choices, subtract the ones containing both people who refuse to be together.

{{< /details >}}

### 14 · rearranging JUDGEMENT

*Asked by: Texas Instruments (IIT BHU 2023)*

In how many arrangements of JUDGEMENT is J between the two Es?

- **(a)** 60,480
- **(b)** 60,420
- **(c)** 50,600
- **(d)** 55,600

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) 60,480**

**Why.** JUDGEMENT has 9 letters with E twice. Pick 3 of the 9 positions for E, J, E: C(9,3) = 84. In those 3 positions the order must be E J E, which is one way. The other 6 letters (U, D, G, M, N, T, all different) fill the rest in 6! = 720 ways. Total 84 × 720 = 60,480.

**Concept: fixed relative order.** When some letters must appear in a particular order (not necessarily side by side), choose the positions for them and place them in that one order; then arrange the rest. Check: total arrangements are 9!/2! = 181,440, and of the 3 orders of {E, E, J} (EEJ, EJE, JEE) exactly one has J between, so 181,440/3 = 60,480.

{{< /details >}}

### 15 · separated As

*Asked by: Texas Instruments (BITS Pilani)*

How many 5-letter strings from A, A, B, M, T have the two As apart?

- **(a)** 24
- **(b)** 36
- **(c)** 32
- **(d)** 34

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) 36**

**Why.** Strings of A, A, B, M, T: 5!/2! = 60. Strings with the two As together: glue AA into one block, 4 units: 4! = 24. Apart: 60 − 24 = 36.

**Concept: complement plus glue.** Same pattern as the seating question: total minus "together", where "together" is counted by treating the identical pair as one unit (no internal swap since the letters are identical).

{{< /details >}}
