---
title: "Series and pattern completion"
weight: 3
---

19 questions asked by Axxela, Flipkart, KLA, MAQ Software, Qualcomm, Texas Instruments. Try each one first, then open the toggle: it gives the answer, why it is right, and the idea behind it explained from scratch.

### 1 · Q10, number group

*Asked by: Axxela (NIT Bhopal 2024)*

Find the alternative that matches the group 195, 456, 267.

- **(a)** 572
- **(b)** 824
- **(c)** 735
- **(d)** 367

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) 735**

**Why.** In 195, 456 and 267 the digits add to 15. 735: 7 + 3 + 5 = 15. The others give 14, 14 and 16.

**Concept: find the shared property.** Check digit sums, products, divisibility and digit patterns until one property holds for all the given numbers.

{{< /details >}}

### 2 · Q12, letters in hexagons

*Asked by: Axxela (NIT Bhopal 2024)*

Which letter replaces the question mark? Rows: E M H / N O A / I ? D.

- **(a)** A
- **(b)** E
- **(c)** H
- **(d)** M

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) M**

**Why.** With A = 1, ..., Z = 26, the middle letter of each row is the sum of the two ends: E(5) + H(8) = 13 = M; N(14) + A(1) = 15 = O; I(9) + D(4) = 13 = M.

**Concept: letters as numbers.** Convert letters to positions and look for arithmetic between them.

{{< /details >}}

### 3 · Q2, fill the letter series

*Asked by: Axxela (NIT Bhopal 2024)*

Which group of letters, put in the blanks in order, completes the series
`ab_ab_aaa_bbaaa_bbbb`?

- **(a)** abab
- **(b)** abba
- **(c)** aabb
- **(d)** baba

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) abba**

**Why.** Filled in: a b **a**a **b**b aaa **b**bb aaa**a** bbbb → runs a, b, aa, bb, aaa, bbb, aaaa, bbbb, with lengths 1, 1, 2, 2, 3, 3, 4, 4.

**Concept: look for runs.** In letter-blank series, group repeated letters and see how the run lengths change.

{{< /details >}}

### 4 · Q5, letter series

*Asked by: Axxela (NIT Bhopal 2024)*

C, E, H, L, Q, ?, D, L

- **(a)** U
- **(b)** W
- **(c)** V
- **(d)** X

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) W**

**Why.** Positions C 3, E 5, H 8, L 12, Q 17: gaps 2, 3, 4, 5, then 6 → 23 = W. Check: +7 = 30 → 30 − 26 = 4 = D, +8 = 12 = L. ✓

**Concept: increasing gaps with wrap-around.** After Z, continue from A (subtract 26).

{{< /details >}}

### 5 · Q16, 2, 17, 52, ?, 206

*Asked by: Axxela (NIT Bhopal 2024)*

2, 17, 52, ___, 206

- **(a)** 73
- **(b)** 85
- **(c)** 113
- **(d)** 184

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) 113**

**Why.** Term n = n³ + (2n − 1)²: 1 + 1 = 2, 8 + 9 = 17, 27 + 25 = 52, 64 + 49 = 113, 125 + 81 = 206.

**Concept: combined power series.** Fast growth hints at cubes; subtract the nearest cube (2 − 1, 17 − 8, 52 − 27 = 1, 9, 25) and recognise odd squares.

{{< /details >}}

### 6 · Q14, 13, 34, 74, ?, 290

*Asked by: Axxela (NIT Bhopal 2024)*

Find the missing number: 13, 34, 74, ___, 290.

- **(a)** 168
- **(b)** 170
- **(c)** 172
- **(d)** 174

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) 170**

**Why.** Sums of squares of consecutive primes: 2² + 3² = 13, 3² + 5² = 34, 5² + 7² = 74, 7² + 11² = 170, 11² + 13² = 290.

**Concept: prime-based series.** If no difference pattern appears, try primes, squares and cubes as building blocks.

{{< /details >}}

### 7 · Q9, C10G F16J I22M

*Asked by: Axxela (NIT Bhopal 2024)*

Complete the series: C10G, F16J, I22M, ___

- **(a)** P28L
- **(b)** P26L
- **(c)** L27P
- **(d)** L28P

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) L28P**

**Why.** First letters C, F, I, L (+3); numbers 10, 16, 22, 28 (+6); last letters G, J, M, P (+3).

**Concept: split alphanumeric terms.** Treat each part (first letter, number, last letter) as its own series.

{{< /details >}}

### 8 · Q21, numbers around triangles

*Asked by: Axxela (NIT Bhopal 2024)*

Find the missing number. Triangle 1 has corners 15, 6, 4 and centre 36; triangle 2 has
corners 6, 7, 5 and centre 21; triangle 3 has corners 50, 10, 10 and centre ?.

- **(a)** 140
- **(b)** 220
- **(c)** 320
- **(d)** 500

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) 500**

**Why.** Centre = product of corners ÷ 10: 15 × 6 × 4 = 360 → 36; 6 × 7 × 5 = 210 → 21; 50 × 10 × 10 = 5000 → 500.

**Concept: test products and sums of the surrounding numbers.** When the centre is bigger than the corners, try products, then scale.

{{< /details >}}

### 9 · G5Q, F9R, E13S, ?

*Asked by: Flipkart (Neev 2025)*

What comes in the position of "?" in the alphanumeric series G5Q, F9R, E13S, ?

- **(a)** D19T
- **(b)** D17T
- **(c)** D21T
- **(d)** None of these

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) D17T**

**Why.** First letters go back one (G, F, E → D); numbers rise by 4 (5, 9, 13 → 17); last letters go forward one (Q, R, S → T).

**Concept: separate the parts.** Each position in the term follows its own simple rule.

{{< /details >}}

### 10 · Q19, number sequence

*Asked by: KLA (IIT Delhi 2023)*

Find the next term in the sequence: 2, 18, 52, 110, ...

- **(a)** 212
- **(b)** 216
- **(c)** 258
- **(d)** 198

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) 198**

**Why.** Differences: 16, 34, 58; second differences: 18, 24 (rising by 6). Next second difference 30, next difference 58 + 30 = 88, next term 110 + 88 = 198. (The terms are n³ + 3n² − 2.)

**Concept: third differences.** If the second differences change by a constant, the series is a cubic. Keep extending the difference table.

{{< /details >}}

### 11 · Q17, letter series R T P R N P

*Asked by: MAQ Software (TalentDecrypt test, 2025)*

Which is the next letter in the series R, T, P, R, N, P?

- **(a)** S
- **(b)** L
- **(c)** N
- **(d)** R

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) L**

**Why.** Two interleaved series: positions 1, 3, 5: R, P, N (back 2 each); positions 2, 4, 6: T, R, P (back 2). The next term (7th) continues R, P, N → L.

**Concept: interleaved series.** If neighbouring terms look unrelated, split odd and even positions.

{{< /details >}}

### 12 · next pair in 2, 3, 4, 5, 6, 4, 8

*Asked by: MAQ Software (TalentDecrypt test, 2025)*

Choose the next pair in the series 2, 3, 4, 5, 6, 4, 8.

- **(a)** 4, 8
- **(b)** 10, 4
- **(c)** 9, 4
- **(d)** 9, 10

{{< details title="Answer and explanation" closed="true" >}}

**Answer: ambiguous; (d) 9, 10 is the only option consistent with part of the pattern.**

**Why.** Odd positions: 2, 4, 6, 8, so 10 is next at position 9. Even positions 3, 5, 4 follow no clear rule. (d) is the only option containing 10, but it would need 9 at position 8 (from 3, 5, 4 that is not a clear rule either).

**Concept: when a series has no clean rule, prefer the option that continues the clearest sub-pattern.**

{{< /details >}}

### 13 · Q11, number boxes

*Asked by: Qualcomm (Nov 2024)*

Which number replaces the question mark? Each box has numbers at its four corners
(top-left, top-right, bottom-left, bottom-right) and a number inside:
$(3, 4, 2, 2) \to 30$; $(7, 4, 4, 5) \to 1217$; $(8, 4, 7, 5) \to 1589$; $(11, 6, 5, 7) \to\ ?$

- **(a)** 159
- **(b)** 107
- **(c)** 5918
- **(d)** 3178

{{< details title="Answer and explanation" closed="true" >}}

**Answer: not determinable from the photo** (no rule fits the three boxes as transcribed; a corner number was probably misread).

**Concept: number-box puzzles.** Usual rules combine opposite corners (products or sums) and write the two results side by side, e.g. (TL × BR)(TR × BL). Test candidate rules on every box before applying one to the last.

{{< /details >}}

### 14 · letter-number series

*Asked by: Qualcomm (Nov 2024)*

What is the missing term? J7, T5, ___, N6, X9

- **(a)** W4
- **(b)** D8
- **(c)** L5
- **(d)** Z7

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) D8**

**Why.** Letters move forward 10 places: J (10) → T (20) → D (30 − 26 = 4) → N (14) → X (24). Numbers at odd positions 7, 8, 9 and at even positions 5, 6.

**Concept: big letter jumps wrap around.** A constant shift larger than the alphabet's remaining letters continues from A.

{{< /details >}}

### 15 · Puzzles

*Asked by: Qualcomm (60-question online assessment)*

The 2nd number is analogous to the 1st in the same way the 4th is analogous to the 3rd. Find the unit digit of the 2nd term.

`2015 : ? :: 1418 : 67`

- **(a)** 2
- **(b)** 1
- **(c)** 0
- **(d)** 5

{{< details title="Answer and explanation" closed="true" >}}

**Answer: no reliable pick.**

**Why.** No rule maps 1418 to 67: digit sums, products, splitting into 14 and 18 (sum 32, product 252), squares, reversals and factorisations were all tested, and none gives 67. Without that rule, 2015's partner cannot be derived.

**Concept: analogy questions need a rule that fits the example exactly.** Try splitting the number into parts and combining them (add, multiply, subtract); if nothing fits, the question is likely mis-transcribed.

{{< /details >}}

### 16 · Puzzles

*Asked by: Qualcomm (60-question online assessment)*

Identify the next term: A5, C15, E25, G35, ?

- **(a)** J50
- **(b)** H40
- **(c)** I45
- **(d)** I40

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) I45**

**Why.** Letters advance by 2 (A, C, E, G → I). Numbers rise by 10 (5, 15, 25, 35 → 45).

**Concept: letter and number parts move independently.** Here the number is also 5 × (letter position) − 0: A1 → 5, C3 → 15, I9 → 45.

{{< /details >}}

### 17 · alphanumeric series

*Asked by: Texas Instruments (IIT BHU 2023)*

Next term: KM10, PR15, UW20, XZ23, ...

- **(a)** CE2
- **(b)** EG22
- **(c)** CE22
- **(d)** EG2

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) CE2**

**Why.** The number equals the first letter's position minus 1: K (11) → 10, P (16) → 15, U (21) → 20, X (24) → 23. The second letter is two after the first (K–M, P–R, U–W, X–Z). The next first letter is C (X + 5 wraps to 3), so the term is C, E, 3 − 1 = 2: CE2. (The BHU candidate's CE22 misses the rule.)

**Concept: link the parts of a term.** Sometimes the number is derived from a letter in the same term rather than from the previous term.

{{< /details >}}

### 18 · grids A and B

*Asked by: Texas Instruments (IIT BHU 2023)*

Grid A: 35 3 26 / 45 17 31 / 39 21 32. Grid B: 57 30 51 / 62 ? 21 / 36 10 42. Find ?.

- **(a)** 11
- **(b)** 10
- **(c)** 9
- **(d)** 8

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) 10**

**Why.** In each row, middle = (product of the left number's digits) − (product of the right number's digits). Grid A: 3×5 − 2×6 = 3, 4×5 − 3×1 = 17, 3×9 − 3×2 = 21. Grid B, row 2: 6×2 − 2×1 = 10.

**Concept: digit operations within a row.** Check every row of the example grid before trusting the rule.

{{< /details >}}

### 19 · grids with a missing value

*Asked by: Texas Instruments (IIT ISM 2024)*

Grid A: 3 9 4 / 8 2 14 / 3 12 6. Grid B: 4 13 5 / ? 4 15 / 2 12 6. Find ?.

- **(a)** 10
- **(b)** 11
- **(c)** 12
- **(d)** 14

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) 10** (the rule is uncertain)

**Why.** In grid B each edge number equals its two corners plus the centre: 4 + 5 + 4 = 13, 5 + 6 + 4 = 15, 2 + 6 + 4 = 12. So ? = 4 + 2 + 4 = 10. Grid A does not follow this rule cleanly, so treat the answer with caution.

**Concept: test each candidate rule on all given grids.**

{{< /details >}}
