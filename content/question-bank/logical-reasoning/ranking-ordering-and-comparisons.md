---
title: "Ranking, ordering and comparisons"
weight: 5
---

9 questions asked by Grey Orange, Siemens Energy, Texas Instruments. Try each one first, then open the toggle: it gives the answer, why it is right, and the idea behind it explained from scratch.

### 1 · Q5, TV Ratings 1

*Asked by: Grey Orange (OA, Oct 2024)*

Ten people, A to J, ranked nine TV shows from 1 to 10 as shown below. No two people gave
the same show the same rank. Blank cells are deliberately hidden. What rank did D give
to *Narcos*?
|  | Black Mirror | Making a Murderer | Narcos | Master of None | Mind Hunter | Ozark | Stranger Things | House of Cards | Haunting of Hill House |
|---|---|---|---|---|---|---|---|---|---|
| A | 2 |  | 4 | 5 | 6 | 7 | 8 | 10 | 1 |
| B | 4 | 7 | 5 | 9 | 10 | 1 | 2 | 3 | 6 |
| C | 1 | 10 | 9 | 8 | 4 | 2 | 3 | 6 | 7 |
| D | 6 |  |  | 2 | 7 |  | 4 | 5 | 8 |
| E | 7 | 8 | 2 | 1 | 5 | 4 | 6 | 9 | 3 |
| F | 3 | 5 | 6 | 4 | 9 | 8 | 7 | 1 | 10 |
| G | 5 | 4 | 3 | 6 |  | 9 |  | 7 | 2 |
| H | 10 | 2 |  | 7 | 1 | 3 | 9 | 4 | 5 |
| I | 8 | 1 | 7 | 10 | 3 | 6 | 5 | 2 | 9 |
| J | 9 |  | 10 | 3 | 2 | 5 | 1 | 8 | 4 |

- **(a)** 10
- **(b)** 9
- **(c)** 8
- **(d)** 1

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) 1**

**Why.** In the Narcos column the known ranks are 4, 5, 9, 2, 6, 3, 7, 10, so D and H share the remaining ranks 1 and 8. H already gave rank 1 (to Mind Hunter), and a person uses each rank only once, so H gave Narcos 8 and D gave it 1.

**Concept: Latin-square reasoning.** When each row and each column must use each value once, a missing cell is whatever value is absent from both its row and its column.

{{< /details >}}

### 2 · A5, Max's rank

*Asked by: Siemens Energy (MNNIT Allahabad (Mettl))*

Smith is ranked 12th from the top and 20th from the bottom. If Max's rank is two positions
higher than Smith's, find Max's rank from the bottom.

- **(a)** 25th
- **(b)** 22nd
- **(c)** 29th
- **(d)** 19th

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) 22nd**

**Why.** Total = 12 + 20 − 1 = 31. Max is two places above Smith: 10th from the top. From the bottom: 31 − 10 + 1 = 22nd.

**Concept: rank from both ends.** Total = (rank from top) + (rank from bottom) − 1, because the person is counted twice. "Higher" means closer to the top.

{{< /details >}}

### 3 · a row of athletes

*Asked by: Texas Instruments (IIT BHU 2023)*

In a row of 30 facing north, A1 is 13th from the left and 6th to the right of A2. A2's
position from the right?

- **(a)** 24th
- **(b)** 7th
- **(c)** 15th
- **(d)** 20th

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) 24th**

**Why.** A1 is 13th from the left and 6 places to the right of A2, so A2 is 13 − 6 = 7th from the left. From the right: 30 − 7 + 1 = 24th.

**Concept: positions in a row.** Convert everything to one end first. Left + right position = total + 1.

{{< /details >}}

### 4 · arranging books

*Asked by: Texas Instruments (IISc, second set)*

B1 is 24th from the left and B2 is 27th from the right; only B3 lies between them. Minimum
number of books?

- **(a)** 58
- **(b)** 55
- **(c)** 48
- **(d)** 50

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) 48**

**Why.** To use as few books as possible, let B1 and B2 overlap their counts: put B2 to the left of B1 with one book (B3) between them. B1 is 24th from the left, so B2 is 22nd from the left. B2 is 27th from the right: total = 22 + 27 − 1 = 48.

**Concept: minimum and maximum arrangements.** "Minimum total" means the counts from each end should overlap as much as possible, so place the two items in the order that makes them share books.

{{< /details >}}

### 5 · a coffee survey

*Asked by: Texas Instruments (IISc 2023)*

40 people rank H, I, C: 1/5 rank I last, 2/5 rank I before H, 1/4 rank I before C. How many
rank I first?

- **(a)** 6
- **(b)** 5
- **(c)** 2
- **(d)** 4

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) 6** is the intended key, but the data are inconsistent.

**Why.** The key subtracts the three groups: 40 − 8 (I last) − 16 (I before H) − 10 (I before C) = 6. That treats overlapping groups as separate. Done properly: people who rank I first are counted in both "I before H" and "I before C", and those with I in the middle in exactly one of them. So 2 × first + middle = 16 + 10 = 26, while first + middle = 40 − 8 = 32. That gives first = −6, impossible: the numbers in the question cannot all be right.

**Concept: overlapping groups.** Before subtracting groups from a total, check whether they overlap. If they do, use inclusion–exclusion (or count by cases as above).

{{< /details >}}

### 6 · meal-prep techniques

*Asked by: Texas Instruments (IIT BHU 2023)*

T1 is twice as effective as T4 but less effective than T5; T2 is thrice T5; T3 equals T4.
Conclusions: (1) T5 is the most effective. (2) T4 and T5 are the least. (3) T2 is the most.

- **(a)** Only 1
- **(b)** Only 2
- **(c)** Only 3
- **(d)** Both 1 and 3

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) only 3**

**Why.** T2 = 3 × T5 > T5 > T1 = 2 × T4 > T4 = T3. So T2 is the most effective (3 follows). T5 is not the most (1 fails), and T4 ties with T3 as least, not T5 (2 fails).

**Concept: build a chain.** Turn each comparison into an inequality and link them into one ordering from greatest to least; then read off the conclusions.

{{< /details >}}

### 7 · meal-prep techniques (variant)

*Asked by: Texas Instruments (IISc, second set)*

T1 is twice as effective as T4 but less than T5; T2 is thrice T5; T3 equals T4. Conclusions:
(1) $T5 \ge T1$, (2) $T2 > T5$, (3) $T2 > T1$, (4) $T4 > T1$.

- **(a)** Only 1 and 2
- **(b)** Only 2 and 4
- **(c)** Only 2 and 3
- **(d)** None

{{< details title="Answer and explanation" closed="true" >}}

**Answer: conclusions 1, 2 and 3 all follow and 4 does not, so no option is exact** (the key writes "1 & 2 or 1 & 3").

**Why.** Same chain: T2 > T5 > T1 > T4. So T5 ≥ T1 (1), T2 > T5 (2) and T2 > T1 (3) all hold; T4 > T1 (4) is false.

**Concept: check every conclusion against the chain.** An option is correct only if it lists exactly the conclusions that follow.

{{< /details >}}

### 8 · a row of parked vehicles

*Asked by: Texas Instruments (BITS Pilani)*

V1 is 20th to the left of V2, which is 27th from the right; V3 is 19th from the left and 11th
to the right of V1. How many vehicles?

- **(a)** 44
- **(b)** 54
- **(c)** 50
- **(d)** 40

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) 54**

**Why.** V3 is 19th from the left and 11 places to the right of V1, so V1 is 8th from the left. V2 is 20 places to the right of V1: 28th from the left. V2 is 27th from the right: total = 28 + 27 − 1 = 54.

**Concept: anchor everything to one end.** Convert relative positions ("n to the right of") into positions from the left, then use left + right − 1 = total.

{{< /details >}}

### 9 · the oldest sister

*Asked by: Texas Instruments (BITS Pilani)*

P is younger than S and R is older than T. Who is oldest? (1) R is older than P. (2) S is
older than R. (3) T is the youngest.

- **(a)** Only 1
- **(b)** Only 2
- **(c)** Only 3
- **(d)** 1 and 2

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) only 2**

**Why.** Given: S > P and R > T. Add (2) S > R: then S > R > T and S > P, so S is the oldest. (1) R > P does not compare R and S. (3) T youngest does not decide between S and R.

**Concept: data sufficiency with orderings.** The oldest is the person nobody is above. Check whether each statement leaves exactly one such person.

{{< /details >}}
