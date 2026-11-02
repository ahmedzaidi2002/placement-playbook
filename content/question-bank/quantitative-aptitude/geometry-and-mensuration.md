---
title: "Geometry and mensuration"
weight: 13
---

6 questions asked by ION Group, NVIDIA, Oracle, Qualcomm, Texas Instruments. Try each one first, then open the toggle: it gives the answer, why it is right, and the idea behind it explained from scratch.

### 1 · Q6, rectangle area

*Asked by: ION Group (SDE OA, Jul 2025)*

The difference between the length and the breadth of a rectangle is 23 m. If its
perimeter is 206 m, what is its area in square metres?

- **(a)** 1520
- **(b)** 2420
- **(c)** 2480
- **(d)** 2520

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) 2520 m²**

**Why.** Perimeter 206 means 2(l + b) = 206, so l + b = 103. With l − b = 23: l = (103 + 23)/2 = 63 and b = 40. Area = 63 × 40 = 2520.

**Concept: sum and difference give both numbers.** Larger = (sum + difference)/2, smaller = (sum − difference)/2. The perimeter of a rectangle gives the sum of its sides (halve it first).

{{< /details >}}

### 2 · Q3, right triangle

*Asked by: NVIDIA (SSE NCG, Nov 2024)*

$ABC$ is right-angled at $A$. The hypotenuse is 26 and the area is 120 square units.
What is its perimeter?

- **(a)** 48
- **(b)** 52
- **(c)** 60
- **(d)** None of the above

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) 60**

**Why.** Let the legs be b and c.
1. Pythagoras: b² + c² = 26² = 676.
2. Area = bc/2 = 120, so bc = 240.
3. (b + c)² = b² + c² + 2bc = 676 + 480 = 1156, so b + c = 34.
4. Perimeter = 34 + 26 = 60. (The legs are 10 and 24.)

**Concept: right triangles and the (b + c)² trick.** In a right triangle the two legs are perpendicular, so the area is half their product, and Pythagoras ties them to the hypotenuse. You need b + c, not b and c separately, and (b + c)² = b² + c² + 2bc gives it directly. Recognising the 5-12-13 triple scaled by 2 (10-24-26) is even faster.

{{< /details >}}

### 3 · painted cube

*Asked by: Oracle (HackerRank MCQ test)*

A cube is painted green on all surfaces and cut into 1000 identical cubes. How many of the
smaller cubes have three faces painted?

- **(a)** 8
- **(b)** 10
- **(c)** 100
- **(d)** 64

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) 8**

**Why.** 1000 small cubes means the big cube is cut 10 × 10 × 10. A small cube shows three painted faces only if it sits at a corner of the big cube, where three outer faces meet. A cube has 8 corners, so 8 small cubes, whatever the number of cuts.

**Concept: painted-cube counting.** For an n × n × n cube painted outside:
- 3 faces painted: the 8 corners.
- 2 faces: along the edges, minus corners: 12(n − 2).
- 1 face: inside each face: 6(n − 2)².
- 0 faces: the hidden core: (n − 2)³.
For n = 10 that is 8, 96, 384 and 512, which add to 1000.

{{< /details >}}

### 4 · Problem Solving

*Asked by: Qualcomm (60-question online assessment)*

A point P lies on the line x + y = 8 and satisfies angle APB = 90 deg, where A(1,1) and B(7,5). If the x-coordinate of P is less than its y-coordinate, then P is:

- **(a)** (1, 7)
- **(b)** (7, 1)
- **(c)** (3, 5)
- **(d)** (2, 6)

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) (2, 6)**

**Why.**
1. Angle APB = 90° means P lies on the circle with AB as diameter. Its centre is the midpoint of A(1,1) and B(7,5): (4, 3). Radius² = (7 − 4)² + (5 − 3)² = 13.
2. P is on x + y = 8, so put y = 8 − x into (x − 4)² + (y − 3)² = 13: (x − 4)² + (5 − x)² = 13 → 2x² − 18x + 41 = 13 → x² − 9x + 14 = 0 → x = 2 or 7.
3. The points are (2, 6) and (7, 1). The condition x < y picks (2, 6).

**Concept: angle in a semicircle (Thales' theorem).** Any point that sees a segment AB at a right angle lies on the circle having AB as its diameter. So "∠APB = 90°" turns into a circle equation, and intersecting it with the given line gives P. A quick check: slopes PA = 5/1 and PB = −1/5 multiply to −1, confirming the right angle.

{{< /details >}}

### 5 · Problem Solving

*Asked by: Qualcomm (60-question online assessment)*

A cone and a hemisphere have the same base radius 7 cm. The height of the cone is 24 cm. They are joined along their circular bases to form a solid. What is the total volume of the solid? (Take pi = 22/7)

- **(a)** 2150 2/3 cm³
- **(b)** 1750 2/3 cm³
- **(c)** 1850 2/3 cm³
- **(d)** 1950 2/3 cm³

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) 1950 2/3 cm³**

**Why.**
- Cone: (1/3)πr²h = (1/3)(22/7)(49)(24) = 1232 cm³.
- Hemisphere: (2/3)πr³ = (2/3)(22/7)(343) = 718 2/3 cm³.
- Total = 1950 2/3 cm³.

**Concept: volumes of composite solids.** When solids are joined along a face, their volumes simply add. Know the formulas: cone (1/3)πr²h, sphere (4/3)πr³, so hemisphere (2/3)πr³, cylinder πr²h. With π = 22/7 and r = 7, the 7s cancel neatly.

{{< /details >}}

### 6 · a circular plot

*Asked by: Texas Instruments (IISc 2023)*

A circle's area grows by 21%. By what percent does its circumference grow?

{{< details title="Answer and explanation" closed="true" >}}

**Answer: 10%**

**Why.** Area = πr². If the area becomes 1.21 times, r² becomes 1.21 times, so r becomes √1.21 = 1.1 times. Circumference = 2πr grows in the same ratio as r: 10%.

**Concept: scaling lengths vs areas.** If every length scales by k, areas scale by k² and volumes by k³. Going backwards, an area factor of 1.21 means a length factor of √1.21 = 1.1. Circumference is a length, so it grows 10%, not 21%.

{{< /details >}}
