---
title: "Data sufficiency"
weight: 6
---

8 questions asked by Accenture, Texas Instruments. Try each one first, then open the toggle: it gives the answer, why it is right, and the idea behind it explained from scratch.

### 1 · Q31-35, data sufficiency

*Asked by: Accenture (IDC paper)*

Answer 1 if statement I alone suffices, 2 if II alone, 3 if both are needed, 4 if the question
cannot be answered. (31) What is $P$? I: $P, Q$ are integers. II: $PQ = 10$, $P + Q = 5$.
(32) Who scored highest among Sumit, Amit, Namit (all different)? I: Sumit $>$ Namit.
II: Amit is not below Sumit, who is not below Namit. (33) How many hours do the boys and girls
take to put up a tent? I: 4 boys and 7 girls. II: a girl takes 5 hours, a boy 3 hours.
(34) If $p, q, r, s, t$ are in arithmetic progression, is $r$ the largest? I: $t > 0$.
II: $p, q < 0$. (35) Is $X > 0$ a whole number? I: $2X$ is even. II: $3X$ is odd.

{{< details title="Answer and explanation" closed="true" >}}

**Answers: (31) 4 (32) 2 (33) 3 (34) rigorously 3 (the recorded key says 2) (35) 1**

**Why.**
- (31) P + Q = 5 and PQ = 10 would make P a root of x² − 5x + 10 = 0, whose discriminant 25 − 40 is negative: no real P exists, so the question cannot be answered.
- (32) II says Amit ≥ Sumit ≥ Namit, and all scores differ, so Amit is highest. I alone does not place Amit.
- (33) You need both the team (I) and each person's time (II): rate = 4/3 + 7/5 tents per hour.
- (34) In an arithmetic progression that is not constant, the largest term is at an end, so the middle term r is never the largest. I (t > 0) and II (p, q < 0) together show p < 0 < t, so the progression is not constant and the answer is "no". Either alone still allows a constant progression where all terms are equal.
- (35) 2X even means X is a whole number (X = 1, 2, ...), so I suffices. II (3X odd) allows X = 1/3.

**Concept: data sufficiency.** You do not solve the problem; you decide whether each statement gives exactly one answer. Test I alone, then II alone, then both. A definite "no" is a sufficient answer too. Look for hidden cases (a constant AP, a non-integer value) that let a statement fit two different answers.

{{< /details >}}

### 2 · Q28-32, data sufficiency

*Asked by: Accenture (Dec paper)*

Answer 1 (I alone), 2 (II alone), 3 (both), 4 (none). (28) Is $x/2 > y/3$? I: $3x < 2y$.
II: $4x > 3y$. (29) Taxes are due on a certain day; the tax authority reminds payers ten days
before via newspapers. Can the day be found? I: the advert appeared on 24 February. II: the year
is not a leap year. (30) Is $z$ odd? I: $y + 3z$ is odd. II: $2y + 7z$ is odd. (31) How long is
the train journey from Delhi to Allahabad? I: 10 hours Delhi-Lucknow. II: 6 hours
Lucknow-Allahabad. (32) What is the percentage profit on mangoes? I: cost $= 2/3$ of sale
price. II: 100 mangoes sell for Rs 240.

{{< details title="Answer and explanation" closed="true" >}}

**Answers: (28) 1 (29) 3 (30) 2 (31) strictly 4 (key: 3) (32) 1**

**Why.**
- (28) x/2 > y/3 is the same as 3x > 2y. I says 3x < 2y, a definite "no": sufficient. (The key's 2 is wrong: 4x > 3y does not settle it.)
- (29) You need the advert date (I) and whether February has 29 days (II) to count 10 days forward: both.
- (30) 2y is even, so 2y + 7z odd forces 7z odd, so z is odd: II suffices. I (y + 3z odd) depends on y.
- (31) Delhi–Lucknow plus Lucknow–Allahabad gives the journey only if the train goes via Lucknow, which neither statement says: strictly 4.
- (32) Cost = 2/3 of the sale price gives profit = (1 − 2/3)/(2/3) = 50%: I suffices. II gives only the selling price.

**Concept: parity rules and sufficiency.** Even × anything = even; even + odd = odd. A statement that answers "no" for sure is still sufficient. Do not assume facts the statements do not give (like the route via Lucknow).

{{< /details >}}

### 3 · Q31-32, data sufficiency

*Asked by: Accenture (On-campus recall)*

A: I alone, B: II alone, C: both, D: neither. (31) A boy has Rs 4 in 1-rupee and 50-paise
coins. How many of each? I: 5 coins in all. II: more 1-rupee coins than 50-paise coins.
(32) Is $1/a + 1/b = 8$? I: $a$ is a positive integer. II: $b$ is any number.

{{< details title="Answer and explanation" closed="true" >}}

**Answers: (31) A (32) D**

**Why.**
- (31) With x one-rupee and y fifty-paise coins: x + y/2 = 4. I adds x + y = 5, which gives x = 3, y = 2: unique. II (x > y) allows (4, 0) and (3, 2).
- (32) Knowing a is a positive integer and b is any number says nothing about 1/a + 1/b.

**Concept: two equations, two unknowns.** A value equation plus a count equation pins down two unknowns. An inequality usually leaves several possibilities.

{{< /details >}}

### 4 · enough fuel for 600 miles?

*Asked by: Texas Instruments (IISc, second set)*

A bus with a full tank of unknown size and efficiency must go 600 miles. (1) The driver drives
at constant speed. (2) After 150 miles, three quarters of the tank is left. (3) After 450
miles, three quarters of the tank is left. Which statements suffice?

- **(a)** 1 and 2
- **(b)** 1 and 3
- **(c)** All three
- **(d)** 1 and 2 or 1 and 3
- **(e)** None

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) 1 and 2, or 1 and 3**

**Why.** With constant speed (1) fuel use per mile is constant. Then (2) "a quarter of the tank used in 150 miles" gives a range of 600 miles, enough. Or (3) "a quarter used in 450 miles" gives 1800 miles, enough. Either pair answers the question.

**Concept: data sufficiency with alternatives.** When two different statement pairs each suffice, the answer is "either pair". Constant consumption is what lets one reading predict the whole range.

{{< /details >}}

### 5 · same age and college

*Asked by: Texas Instruments (BITS Pilani)*

200 students attend. Must two share an age and a college? (1) Ages are 18-22. (2) About 15
colleges.

{{< details title="Answer and explanation" closed="true" >}}

**Answer: both statements together**

**Why.** Ages 18–22 give 5 possible ages, and 15 colleges: 5 × 15 = 75 possible (age, college) pairs. 200 students > 75, so two must share a pair. Either statement alone leaves the number of pairs unknown. (The key's "only 2" is wrong.)

**Concept: pigeonhole principle.** If n items go into fewer than n boxes, some box holds two. Here a "box" is a combination of age and college, so you need both counts.

{{< /details >}}

### 6 · cookie teams

*Asked by: Texas Instruments (IISc, second set)*

Teams of 3 sell cookies. Did some member sell at least 2 boxes? (1) The team sold 6 in total.
(2) All three sold different numbers.

{{< details title="Answer and explanation" closed="true" >}}

**Answer: either statement alone suffices**

**Why.** (1) 6 boxes among 3 people: if each sold at most 1, the total would be at most 3, so someone sold at least 2. (2) Three different non-negative numbers: the largest is at least 2 (the smallest possible set is 0, 1, 2).

**Concept: pigeonhole and extremes.** The average argument (total ÷ people) gives a lower bound for the maximum. Distinct values force a spread that also bounds the maximum.

{{< /details >}}

### 7 · did Jamie pay more?

*Asked by: Texas Instruments (IISc, second set)*

John bought a TV in a sale for Rs. 15000 and sold it to Jamie. Which statements tell whether
John made a profit? (I) Jamie sold it to Jake for 20000. (II) Jamie got a 20% discount on
John's marked price. (III) John's tag said 25000.

{{< details title="Answer and explanation" closed="true" >}}

**Answer: II and III together**

**Why.** III gives John's marked price (25,000); II says Jamie paid 20% less: 20,000. John paid 15,000, so he made a profit. Jamie's resale price (I) says nothing about what Jamie paid John.

**Concept: profit needs both cost and selling price.** Only use statements about the transaction you are asked about.

{{< /details >}}

### 8 · Zoey's age

*Asked by: Texas Instruments (IIT BHU 2023)*

Zoey's age in 2050? (I) When Zoey was born her father was 32, four years older than her
mother. (II) Her mother was born in the first leap year after 1970.

{{< details title="Answer and explanation" closed="true" >}}

**Answer: both together**

**Why.** II: the first leap year after 1970 is 1972, so the mother was born in 1972. I: at Zoey's birth her father was 32 and her mother 28, so Zoey was born in 2000. In 2050 she is 50.

**Concept: chain the statements.** Each statement alone gives a relationship without an anchor date; together they fix the date.

{{< /details >}}
