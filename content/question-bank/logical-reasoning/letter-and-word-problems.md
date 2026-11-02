---
title: "Letter and word problems"
weight: 15
---

3 questions asked by Flipkart, Qualcomm. Try each one first, then open the toggle: it gives the answer, why it is right, and the idea behind it explained from scratch.

### 1 · ACCLIMATIZED reversed

*Asked by: Flipkart (Neev 2025)*

The word ACCLIMATIZED is rewritten with its letters in reverse order. What is the fifth
letter from the left?

- **(a)** Z
- **(b)** I
- **(c)** T
- **(d)** A

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) T**

**Why.** ACCLIMATIZED reversed is DEZITAMILCCA. Letters from the left: D, E, Z, I, **T**.

**Concept: reverse first, then count.** Write the reversed word out; counting backwards in your head causes off-by-one slips. The 5th from the left in the reversed word is the 5th from the right in the original.

{{< /details >}}

### 2 · letter pairs in ESCAPE

*Asked by: Flipkart (Neev 2025)*

How many pairs of letters are there in the word ESCAPE which have as many letters between
them in the word as in the alphabet? (Options mostly hidden by the selection.)

{{< details title="Answer and explanation" closed="true" >}}

**Answer: 2**

**Why.** Alphabet positions: E 5, S 19, C 3, A 1, P 16, E 5. A pair qualifies when the gap in the word equals the gap in the alphabet.
- E–C: word positions 1 and 3 (gap 2), alphabet 5 and 3 (gap 2). Yes.
- S–P: word positions 2 and 5 (gap 3), alphabet 19 and 16 (gap 3). Yes.
No other pair of the 15 works.

**Concept: compare position differences.** For letters at word positions i < j, they have j − i − 1 letters between them in the word. In the alphabet the count is |a − b| − 1. So check |a − b| = j − i. Count each pair once, in either direction.

{{< /details >}}

### 3 · Q2, letter pairs in CHORDAMESODERM

*Asked by: Qualcomm (Nov 2024 (HirePro))*

How many pairs of letters are there in the word CHORDAMESODERM which have as many letters
between them in the word as in the English alphabet?

- **(a)** 5
- **(b)** 4
- **(c)** 6
- **(d)** 3

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) 4** (H–M, D–M, O–R and D–E; the photo ticks 6)

**Why.** For each pair of letters at word positions i < j, compare j − i with the difference of their alphabet positions. CHORDAMESODERM: H(8) at 2 and M(13) at 7: 5 = 5. Similarly D–M, O–R and D–E qualify; no others do (checked over all pairs).

**Concept: same method as above.** Go letter by letter from the left and check the next few letters to its right (a pair can only work if the alphabet gap is small enough to fit in the word).

{{< /details >}}
