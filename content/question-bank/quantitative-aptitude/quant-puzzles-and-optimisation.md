---
title: "Quant puzzles and optimisation"
weight: 18
---

4 questions asked by KLA, Siemens Energy, Texas Instruments. Try each one first, then open the toggle: it gives the answer, why it is right, and the idea behind it explained from scratch.

### 1 · Q2, four missiles

*Asked by: KLA (IIT Delhi 2023)*

Four missiles start from the four corners of a 2 m square, each homing on to (aiming
at) the missile on its left. The missiles fly at 1 m/s. How long would it take them to
meet? (Ignore gravity.)

- **(a)** 2 sec
- **(b)** Never meet
- **(c)** 1.414 sec
- **(d)** 2.828 sec

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) 2 s**

**Why.** By symmetry the four missiles always sit at the corners of a square that shrinks and rotates. Each missile flies straight at its target, and the target moves at right angles to that line, so the target's motion does not change the distance between them. The gap therefore closes at the full 1 m/s, and the 2 m side is used up in 2 s.

**Concept: relative velocity along the line of sight.** How fast a distance shrinks depends only on the velocity components along the line joining the two objects. A velocity perpendicular to that line rotates the line but does not lengthen or shorten it. (Each missile still travels 2 m along a spiral.)

{{< /details >}}

### 2 · M21, production plan for maximum profit

*Asked by: Siemens Energy (MNNIT Allahabad (Mettl))*

Part A needs 3 h of division X and 2 h of division Y; part B needs 2 h of X and 1 h of Y.
Profits are INR 5000 (A) and 3000 (B). X and Y have 20 and 12 hours a day. Which daily
targets maximise profit?

- **(a)** 4 units of A and 3 units of B
- **(b)** 3 units of A and 4 units of B
- **(c)** 4 units of A and 4 units of B
- **(d)** 0 units of A and 10 units of B

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) 4 units of A and 4 units of B**

**Why.** Constraints: division X: 3A + 2B ≤ 20; division Y: 2A + B ≤ 12. Check the options:
- (a) 4A, 3B: X 18, Y 11, profit 29,000.
- (b) 3A, 4B: X 17, Y 10, profit 27,000.
- (c) 4A, 4B: X 20, Y 12, profit 32,000 (uses both divisions fully).
- (d) 0A, 10B: X 20, Y 10, profit 30,000.
(c) is feasible and the best of all integer plans.

**Concept: linear programming.** Maximise a linear profit subject to linear resource limits. The best plan sits at a corner of the feasible region, typically where the binding constraints meet: solve 3A + 2B = 20 and 2A + B = 12 to get A = 4, B = 4.

{{< /details >}}

### 3 · a reading schedule

*Asked by: Texas Instruments (IIT BHU 2023)*

Monica reads 12 books of 260, 120, 115, 170, 165, 60, 200, 80, 155, 95, 105, 300 pages in
order, 60 pages a day, never starting a new book on the day she finishes one. How many books
are finished at the end of day 32? (Options not in the source.)

{{< details title="Answer and explanation" closed="true" >}}

**Answer: 11 books**

**Why.** She starts a new book only on a new day, so each book takes ⌈pages/60⌉ days: 5, 2, 2, 3, 3, 1, 4, 2, 3, 2, 2, 5. Running totals: 5, 7, 9, 12, 15, 16, 20, 22, 25, 27, 29, 34. The 11th book ends on day 29 and the 12th on day 34, so 11 books are done by day 32.

**Concept: ceiling division.** If a task needs p units and you do 60 per day, but leftover capacity on the last day is wasted, it takes ⌈p/60⌉ days (round up). Cumulative sums then tell you where any day falls.

{{< /details >}}

### 4 · a perfume's stock

*Asked by: Texas Instruments (IISc, second set)*

A perfume launched in March 1997 sells $2/7$ of the stock at the start of each year by 31
December. In which year does the stock fall below $1/4$ of the original?

- **(a)** 2003
- **(b)** 2002
- **(c)** 2001
- **(d)** 2000

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) 2001**

**Why.** Each year 2/7 of the remaining stock is sold, so 5/7 remains. After n years: (5/7)ⁿ. End of 2000 (4 years: 1997–2000): (5/7)⁴ ≈ 0.26, still above 1/4. End of 2001: (5/7)⁵ ≈ 0.19, below 1/4.

**Concept: geometric decay.** Removing a fixed fraction r each period leaves (1 − r)ⁿ after n periods. Count the periods carefully: 1997 is the first year.

{{< /details >}}
