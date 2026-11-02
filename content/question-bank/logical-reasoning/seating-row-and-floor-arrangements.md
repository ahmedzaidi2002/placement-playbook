---
title: "Seating, row and floor arrangements"
weight: 2
---

19 questions asked by EPAM, JSW, KLA, MAQ Software, Oracle, Qualcomm, Siemens Energy, Texas Instruments. Try each one first, then open the toggle: it gives the answer, why it is right, and the idea behind it explained from scratch.

### 1 · Q9, seven people in a row

*Asked by: EPAM (EPAM freshers test)*

Seven people, G, H, I, J, K, L and M, sit in a row facing forward. G is not at either
end. There are exactly three people between H and K. J is to the left of M but not next to
it. L is not adjacent to I. What is the correct seating order?

- **(a)** H, G, K, L, J, I, M
- **(b)** H, G, L, K, J, I, M
- **(c)** H, G, K, J, L, I, M
- **(d)** H, G, L, J, K, I, M

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) H, G, L, J, K, I, M**

**Why.** Exactly three people between H and K: only (d) has H in seat 1 and K in seat 5. It also fits the rest: G in seat 2 (not an end), J (4) left of M (7) and not next to it, L (3) not next to I (6).

**Concept: test options against the strictest clue.** When the options are full arrangements, check the most restrictive clue first; it usually eliminates all but one.

{{< /details >}}

### 2 · ten cars in two facing rows

*Asked by: JSW (Aptitude test)*

Ten cars (red, black, green, white, yellow, pink, blue, grey, violet, orange), numbered 1
to 10, are parked in two rows of five facing each other; each car is exactly opposite one
car of the other row. No odd-numbered car is opposite another odd-numbered car, and no two
even-numbered cars are adjacent. Left and right are as seen by each driver.

1. The pink car is numbered 8 and is not in the same row as cars 4 and 6.
2. White and yellow are adjacent to car 6, but white is not at an end.
3. Blue is numbered 5 and is not in the same row as cars 3 and 6.
4. Red is neither adjacent nor opposite to blue or green.
5. Pink is at the right end of its row.
6. Car 6 is second from the right in its row.
7. Black is even-numbered and opposite car 1.
8. Violet and orange are in the same row; car 6 is not to the left of car 7.
9. Green is odd-numbered but not 1, and in the same row as blue.
10. Yellow is opposite car 2 and numbered neither 3 nor 1.

**Q1.** Which numbers are parked in the same row? Options: 1, 3, 4, 6, 9 /
2, 3, 8, 9, 10 / 5, 7, 8, 2, 9 / 4, 1, 9, 7, 10.
**Q2.** If the green car is adjacent to the grey car, which car is opposite car 4?
Options: 7, 5, cannot be determined, 1.

{{< details title="Answer and explanation" closed="true" >}}

**Answers: Q1: 1, 3, 4, 6, 9. Q2: 5.**

**Why.**
- One odd car per facing pair (no odd opposite odd) and no two adjacent evens force one row to hold evens in columns 1, 3, 5 and the other in columns 2, 4.
- Pink 8 is at a right end; car 6 is second from the right, so 6 and 8 are in different rows. Blue 5 is with 8 (not with 3 and 6), and 4 is with 6 (not with pink 8).
- Black is opposite car 1, yellow opposite car 2, green is odd and with 5, and so on. Every arrangement that satisfies all ten clues has rows {1, 3, 4, 6, 9} and {2, 5, 7, 8, 10}, and when green is next to grey, car 5 is opposite car 4.

**Concept: two facing rows.** Draw two rows of five boxes with columns linking opposite cars. Remember that "left" and "right" flip for the facing row. Parity clues (odd/even) often fix the pattern of the rows before any colour is placed.

{{< /details >}}

### 3 · Q18, floor puzzle

*Asked by: KLA (IIT Delhi 2023)*

Eight persons live on eight different floors of a building; the ground floor is
numbered 1 and the top floor 8. Y lives on an even-numbered floor. Two persons live
between Y and K. T lives on one of the floors above H, and both live on even-numbered
floors. O lives just above L. Two persons live between Y and X. M does not live above
Y. X lives on one of the floors below K. Who lives on the topmost floor?

- **(a)** K
- **(b)** T
- **(c)** O
- **(d)** Y

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) T**

**Why.** K and X are both 3 floors from Y, with X below K, so X = Y − 3 and K = Y + 3. Y is even and floors run 1–8, so Y = 4: X on 1, K on 7. T and H are on even floors with T above H; the free even floors are 2 and 8, so H = 2, T = 8. M is not above Y, so M = 3. O just above L fills 5 and 6. Order from the bottom: X, H, M, Y, L, O, K, T. (The photo ticks K, from working that put T on floor 7, which is odd.)

**Concept: "two persons between" means a gap of 3 floors.** Floors that have n people between them differ by n + 1. Use the parity and "above/below" clues to pick between the two possible directions.

{{< /details >}}

### 4 · Q12, seven students on three benches

*Asked by: MAQ Software (TalentDecrypt test, 2025)*

Seven students A to G sit on benches I, II and III, at least two per bench and at least one
girl per bench. C, a girl, does not sit with A, E or D. F, a boy, sits with only B. A sits
on bench I with his best friends. G sits on bench III. E is the brother of C. Which group
consists of girls?

- **(a)** BCD
- **(b)** BAC
- **(c)** CDF
- **(d)** BFC

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) BCD**

**Why.** F sits with only B, so {F, B} is a bench and, since F is a boy, B is its girl. C cannot sit with A, D or E, so C joins G on bench III. That leaves {A, D, E} on bench I. A ("his") and E ("brother") are boys, so D is the girl there. Girls: B, C, D.

**Concept: grouping puzzles.** Start with clues that fix a whole group ("F sits with only B"), then place people with "not with" restrictions, then use gender words (his, brother) to identify the remaining girls.

{{< /details >}}

### 5 · standing order

*Asked by: Oracle (HackerRank MCQ test)*

Peter, Tyson, Richard, Steve and Quinn stand in a row. (1) Peter is next to Quinn and Steve
is next to Richard. (2) Steve is not next to Tyson. (3) Tyson is in the leftmost position.
(4) Richard is second from the right. (5) Peter stands somewhere to the right of both Quinn
and Tyson. (6) Peter and Richard are next to each other. Who is in the middle?

- **(a)** Peter
- **(b)** Richard
- **(c)** Steve
- **(d)** Quinn

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) Peter**

**Why.** Tyson is in seat 1 and Richard in seat 4. Steve and Peter are both next to Richard, so they take seats 3 and 5. Peter must be next to Quinn, and seat 5 has no free neighbour, so Peter is in seat 3, Steve in 5 and Quinn in 2. Check: Steve (5) is not next to Tyson (1), and Peter is right of Quinn and Tyson. Order: Tyson, Quinn, Peter, Richard, Steve. The middle seat holds Peter.

**Concept: fix the absolute positions first.** Clues with "leftmost" or "second from the right" place people directly; then use "next to" clues to fill the gaps.

{{< /details >}}

### 6 · circular seating (1)

*Asked by: Qualcomm (Nov 2024)*

Six people, Sonu, Monu, Jim, Akash, Anvesha and Kapil, sit around a circular table facing the
centre. Anvesha is not sitting between Monu and Akash. Some people are sitting between Monu and
Akash. Sonu sits just left of Kapil. Jim is fourth to the right of Sonu.
Who sits second to the right of Sonu?

- **(a)** Jim
- **(b)** Kapil
- **(c)** Akash
- **(d)** Anvesha

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) Anvesha**

**Why.** Six seats. Sonu sits just left of Kapil, so Kapil is first to Sonu's right. Jim is fourth to Sonu's right. Some people sit between Monu and Akash but Anvesha is not one of them, so Monu and Akash sit on either side of Jim, and Anvesha takes the remaining seat, second to Sonu's right. Going round to Sonu's left: Sonu, Monu/Akash, Jim, Akash/Monu, Anvesha, Kapil. Swapping Monu and Akash does not change the answer. The photo ticks Kapil, who is only first to the right.

**Concept: circular seating facing the centre.** For someone facing the centre, their right is anticlockwise and their left is clockwise (seen from above). Fix one person, place others relative to them, and keep track of both possible placements when a clue allows a swap.

{{< /details >}}

### 7 · circular seating (2)

*Asked by: Qualcomm (Nov 2024)*

Same arrangement as the previous question. Who sits exactly between Akash and Monu?

- **(a)** Anvesha
- **(b)** Kapil
- **(c)** Jim
- **(d)** Sonu

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) Jim**

**Why.** In the arrangement Sonu, Monu/Akash, Jim, Akash/Monu, Anvesha, Kapil, Jim is the one person between Monu and Akash ("some people sit between them" and Anvesha is not that person).

**Concept: re-use the solved circle.** Follow-up questions are look-ups once the circle is fixed.

{{< /details >}}

### 8 · circular seating (3)

*Asked by: Qualcomm (Nov 2024)*

Same arrangement. Who sits second to the right of Kapil?

- **(a)** Either Akash or Monu
- **(b)** Anvesha
- **(c)** Jim
- **(d)** Either Sonu or Monu

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) either Akash or Monu**

**Why.** Two seats to Kapil's right lands on the seat next to Anvesha on the far side, which Monu and Akash can swap between them.

**Concept: answer with the ambiguity.** If a clue leaves two people interchangeable, an option naming "either" of them is the correct one.

{{< /details >}}

### 9 · circular seating (4)

*Asked by: Qualcomm (Nov 2024)*

Same arrangement. Who sits second to the left of Sonu?

- **(a)** Jim
- **(b)** Kapil
- **(c)** Monu
- **(d)** Anvesha

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) Jim**

**Why.** With six seats, fourth to the right equals second to the left (4 + 2 = 6). Jim is fourth to Sonu's right, so he is second to Sonu's left.

**Concept: positions around a circle wrap.** In a circle of n, k places to the right = n − k places to the left.

{{< /details >}}

### 10 · circular seating (5)

*Asked by: Qualcomm (Nov 2024)*

Same arrangement. Who is sitting opposite to Jim?

- **(a)** Kapil
- **(b)** Akash
- **(c)** Monu
- **(d)** Sonu

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) Kapil**

**Why.** Opposite in a circle of six means three seats away. From Jim, three seats in either direction is Kapil.

**Concept: opposite seats.** In a circle of n (n even), the person opposite is n/2 seats away.

{{< /details >}}

### 11 · Logical Reasoning

*Asked by: Qualcomm (60-question online assessment)*

Seven smart lanterns (Aurora, Beacon, Corona, Dusk, Ember, Flare, Glow) on Posts 1-7. What is the difference between the post numbers of Ember and Beacon?

- **(a)** 4
- **(b)** 2
- **(c)** 5
- **(d)** 3

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) 5**

**Why.** The clues (not transcribed in the source) give the arrangement, Post 1 to 7: Aurora, Beacon, Glow, Flare, Corona, Dusk, Ember. Ember is on 7 and Beacon on 2: |7 − 2| = 5.

**Concept: linear arrangements.** Place items with absolute clues first, then relative ones; once the order is fixed, each follow-up is a look-up.

{{< /details >}}

### 12 · Logical Reasoning

*Asked by: Qualcomm (60-question online assessment)*

Which lantern is mounted on Post 3?

- **(a)** Corona
- **(b)** Dusk
- **(c)** Glow
- **(d)** Flare

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) Glow**

**Why.** From the arrangement Aurora (1), Beacon (2), Glow (3), Flare (4), Corona (5), Dusk (6), Ember (7), Post 3 holds Glow.

**Concept: look-up from the solved order.**

{{< /details >}}

### 13 · Logical Reasoning

*Asked by: Qualcomm (60-question online assessment)*

If all of them are installed in alphabetical order with Aurora being installed nearest to the post and so on, then the installation of how many of them will be the same as the original arrangement?

- **(a)** 1
- **(b)** 3
- **(c)** 4
- **(d)** 2

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) 2**

**Why.** Alphabetical: Aurora, Beacon, Corona, Dusk, Ember, Flare, Glow. Actual: Aurora, Beacon, Glow, Flare, Corona, Dusk, Ember. Only Aurora (1) and Beacon (2) are in the same position.

**Concept: compare position by position.** Write both orders one above the other and count matching columns.

{{< /details >}}

### 14 · Logical Reasoning

*Asked by: Qualcomm (60-question online assessment)*

At which post is Dusk installed?

- **(a)** Post 7
- **(b)** Post 6
- **(c)** Post 4
- **(d)** Post 5

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) Post 6**

**Why.** From the arrangement, Dusk is on Post 6. (Post 7 was marked in the exam, which is Ember's post.)

**Concept: look-up from the solved order.**

{{< /details >}}

### 15 · Logical Reasoning

*Asked by: Qualcomm (60-question online assessment)*

What is the sum of the post numbers of Flare and Corona?

- **(a)** 7
- **(b)** 9
- **(c)** 8
- **(d)** 11

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) 9**

**Why.** Flare is on Post 4 and Corona on Post 5: 4 + 5 = 9.

**Concept: look-up from the solved order.**

{{< /details >}}

### 16 · A7, five girls in a row

*Asked by: Siemens Energy (MNNIT Allahabad (Mettl))*

Five girls Q, S, R, T and U sit in a row facing north. U is second from the right end and
is adjacent to neither S nor R. The number of people between U and R equals the number
between Q and T. Who sits at the left end?

- **(a)** Q
- **(b)** T
- **(c)** R
- **(d)** S

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) S**

**Why.** Seats 1–5 from the left: U is second from the right, seat 4. U is not next to S or R, so seats 3 and 5 hold Q and T, which puts one person (U) between Q and T. So one person sits between U and R as well: R is in seat 2. S is left with seat 1, the left end.

**Concept: equal-gap clues.** "As many people between U and R as between Q and T" links two pairs; fix the one you can, then apply the same gap to the other.

{{< /details >}}

### 17 · five students in a row

*Asked by: Texas Instruments (IISc, second set)*

A and B are adjacent; C and D are adjacent; A is not next to E, who is at the left end; B is
second from the right; C is to the right of both D and E; B and C are together.
Conclusions: (1) B is between C and A. (2) A is between C and B.

- **(a)** Only (1) is incorrect
- **(b)** Only (2) is incorrect
- **(c)** Either (1) or (2) is incorrect
- **(d)** Neither is incorrect

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) only (2) is incorrect**

**Why.** E is at the left end, B is second from the right (seat 4). A is next to B but not to E, so A is in seat 5 (seat 3 would also be possible, but C must be next to B and D, and to the right of D and E). The only order is E D C B A. So B is between C and A (1 true) and A is not between C and B (2 false).

**Concept: place fixed seats, then neighbours.** End seats and "second from the right" are absolute; "next to" clues then fill the rest.

{{< /details >}}

### 18 · a hexagonal table

*Asked by: Texas Instruments (IISc, second set)*

Adam, Abe, Pepa, Jill, Bob and Ron sit at the corners of a hexagonal table facing the centre.
Adam is second to the left of Ron; Abe is a neighbour of Pepa and Jill; Bob is second to the
left of Jill. Who sits opposite Adam?

- **(a)** Bob
- **(b)** Jill
- **(c)** Ron
- **(d)** Pepa

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) Jill**

**Why.** Seat the six around the hexagon and apply the clues: Adam is second to the left of Ron, Bob is second to the left of Jill, and Abe sits between Pepa and Jill. All arrangements that satisfy these (under either reading of "left") put Jill opposite Adam. The NIT candidate's Pepa is wrong.

**Concept: circular seating.** Fix one person, then place others using "second to the left" (two seats away) and "neighbour" clues. Opposite seats in a hexagon are three apart.

{{< /details >}}

### 19 · eight houses

*Asked by: Texas Instruments (IIT ISM 2024)*

Eight houses for scientists A-H with clues (B not next to A; C just left of D; E in a middle
house; F between E and D; ...). Which is incorrect: (1) G is between B and H; (2) H is
between E and A?

{{< details title="Answer and explanation" closed="true" >}}

**Answer: neither conclusion is determined** (both can be true or false depending on the arrangement).

**Why.** Enumerating all arrangements that satisfy the clues shows every combination of truth values for (1) and (2) is possible, so the question as transcribed has no definite answer.

**Concept: "is incorrect" needs certainty.** A conclusion is definitely incorrect only if no valid arrangement makes it true. If some arrangements make it true and others false, it is undetermined.

{{< /details >}}
