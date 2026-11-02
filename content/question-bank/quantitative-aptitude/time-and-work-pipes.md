---
title: "Time and work, pipes"
weight: 11
---

9 questions asked by EPAM, KLA, MAQ Software, NVIDIA, Qualcomm, Texas Instruments, Wells Fargo. Try each one first, then open the toggle: it gives the answer, why it is right, and the idea behind it explained from scratch.

### 1 · Q19, three workers working different hours

*Asked by: EPAM (EPAM freshers test)*

Three workers A, B and C complete a job in 10, 12 and 15 days respectively, working 2, 3
and 4 hours per day respectively. How many days will they take to finish the job together?

- **(a)** 4
- **(b)** 5
- **(c)** 6
- **(d)** 7

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) 4 days**

**Why.** Each worker keeps their own daily hours, so their "days" figure already includes those hours. Per day: A does 1/10, B 1/12, C 1/15 of the job. Together: 6/60 + 5/60 + 4/60 = 15/60 = 1/4, so 4 days.

**Concept: add rates, not times.** If someone finishes a job in d days, their rate is 1/d of the job per day. Rates add when people work together; time = 1 ÷ combined rate. The hours per day would only matter if they changed their routine.

{{< /details >}}

### 2 · Q13, work and wages

*Asked by: KLA (IIT Delhi 2023)*

A alone can do a piece of work in 6 days and B alone in 8 days. A and B undertook to
do it for Rs 3200. With the help of C, they completed the work in 3 days. How much is
to be paid to C?

- **(a)** 400
- **(b)** 600
- **(c)** 375
- **(d)** 800

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) Rs 400**

**Why.** In 3 days A does 3/6 = 1/2 and B does 3/8 of the work: 7/8 together. C did the remaining 1/8 and is paid 1/8 of 3200 = 400.

**Concept: pay is shared by work done.** Each person's share of the money equals their share of the work. Find each share from rate × time.

{{< /details >}}

### 3 · Q16, men catching sharks

*Asked by: MAQ Software (TalentDecrypt test, 2025)*

40 men can catch 200 sharks in 20 days working 6 hours a day. In how many days can 25 men
catch 300 sharks working 4 hours a day?

- **(a)** 34
- **(b)** 28
- **(c)** 30
- **(d)** 24

{{< details title="Answer and explanation" closed="true" >}}

**Answer: 72 days; none of the options** (the numbers as photographed do not produce any listed answer).

**Why.** One shark takes 40 × 20 × 6/200 = 24 man-hours. 300 sharks need 7200 man-hours. 25 men × 4 hours = 100 man-hours per day, so 72 days.

**Concept: man-hours.** Work is proportional to (men × days × hours per day). Set M₁D₁H₁/W₁ = M₂D₂H₂/W₂ and solve for the unknown.

{{< /details >}}

### 4 · Q1, digging a trench

*Asked by: NVIDIA (SSE NCG, Nov 2024)*

3 men can dig a trench 3 feet deep working 3 hours a day for 3 days. How deep a trench
can 6 men dig working 6 hours a day for 6 days?

- **(a)** 6
- **(b)** 24
- **(c)** 48
- **(d)** 81

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) 24 feet**

**Why.** Depth is proportional to man-hours. 3 × 3 × 3 = 27 man-hours dig 3 ft. 6 × 6 × 6 = 216 man-hours is 8 times as much, so 8 × 3 = 24 ft.

**Concept: direct proportion with several factors.** Doubling men, hours and days each doubles the work, so together they multiply it by 2³ = 8.

{{< /details >}}

### 5 · Q4, Hitesh and Priya

*Asked by: Qualcomm (Nov 2024 (HirePro))*

Hitesh alone can complete a job in 18 days. Had Priya joined him 3 days after he started
working, they would have [cut off in the source]. If they started working together, in how many days would they
complete the work?

- **(a)** 9 days
- **(b)** 6 days
- **(c)** 12 days
- **(d)** 15 days

{{< details title="Answer and explanation" closed="true" >}}

**Answer: not determinable** (the key sentence is cut off in the photo).

**Method.** The missing sentence would say how long they took when Priya joined after 3 days. Hitesh does 1/18 per day. If they finish in T days total: 3/18 + (T − 3)(1/18 + 1/p) = 1, which gives Priya's time p. Together from the start: 1/(1/18 + 1/p) days.

**Concept: work done in phases.** Split the job into periods with different teams, add the work of each period, and set the total to 1.

{{< /details >}}

### 6 · capacity of a pool

*Asked by: Texas Instruments (IIT BHU 2023)*

Pipes P1 and P2 fill a pool in 10 and 20 minutes; P3 drains 12 gallons per minute. Together
they fill it in 30 minutes. Capacity to the nearest integer?

- **(a)** 100
- **(b)** 150
- **(c)** 103
- **(d)** 125

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) 103**

**Why.** Let the capacity be C gallons. P1 fills C/10 per minute, P2 C/20, P3 drains 12. In 30 minutes they fill exactly C: 30(C/10 + C/20 − 12) = C → 3C + 1.5C − 360 = C → 3.5C = 360 → C ≈ 102.9 ≈ 103. (The Apti-3 key's 100 is wrong.)

**Concept: mixing a "fraction per minute" rate with a fixed-volume rate.** A pipe that fills a tank in t minutes adds C/t gallons per minute. Put everything in gallons per minute, then use volume = net rate × time.

{{< /details >}}

### 7 · three pipes in turn

*Asked by: Texas Instruments (IISc 2023)*

A fills in 10 h, B in 20 h, C empties in 30 h; each opens for one hour in turn. The tank is a
quarter full. When does it overflow?

{{< details title="Answer and explanation" closed="true" >}}

**Answer: after 18 h 30 min**

**Why.** Rates per hour: A +1/10 = +6/60, B +1/20 = +3/60, C −1/30 = −2/60. One A-B-C cycle (3 h) adds 7/60. The tank needs 3/4 = 45/60 more.
- After 5 cycles (15 h): +35/60. Within a cycle the peak is after B (+9/60), and 35 + 9 = 44 < 45, so no overflow yet.
- Hour 16 (A): 41; hour 17 (B): 44; hour 18 (C): 42 (in sixtieths).
- Hour 19 (A) needs 3/60 at 6/60 per hour: half an hour. Overflow at 18 h 30 min.

**Concept: cycle problems need a peak check.** Taking full cycles until "enough" can overshoot: the tank may overflow in the middle of a cycle, before the emptying pipe runs. Advance in whole cycles only while (progress + best partial gain) is still short, then go hour by hour.

{{< /details >}}

### 8 · two workers

*Asked by: Texas Instruments (BITS Pilani)*

A and B together finish in 7.5 days; A doing half and then B the other half takes 20 days. How
long does B alone take, if A is faster?

- **(a)** 20
- **(b)** 30
- **(c)** 22
- **(d)** 28

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) 30 days**

**Why.** Let A take a days and B take b days alone.
- Together: 1/a + 1/b = 1/7.5 = 2/15.
- Half by A then half by B: a/2 + b/2 = 20 → a + b = 40.
- 1/a + 1/b = (a + b)/ab = 40/ab = 2/15 → ab = 300. So a and b are roots of x² − 40x + 300 = 0: 10 and 30. A is faster, so B takes 30.

**Concept: sum and product give two numbers.** Once you know a + b and ab, the numbers are the roots of x² − (a + b)x + ab = 0. "Half the work alone" takes half the solo time.

{{< /details >}}

### 9 · hens and eggs

*Asked by: Wells Fargo (SHL test, Oct 2022)*

In a poultry farm, 50 hens give 200 eggs in 2 days. In how many days will 20 hens give
400 eggs?

- **(a)** 15
- **(b)** 10
- **(c)** 5
- **(d)** 8

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) 10 days**

**Why.** One hen lays 200/(50 × 2) = 2 eggs a day. 20 hens lay 40 a day, so 400 eggs take 10 days.

**Concept: unitary method.** Reduce to "one hen, one day", then scale up to the new situation.

{{< /details >}}
