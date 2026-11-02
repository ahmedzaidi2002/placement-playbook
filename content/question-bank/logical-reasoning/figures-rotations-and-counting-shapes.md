---
title: "Figures, rotations and counting shapes"
weight: 11
---

5 questions asked by JSW, Oracle, Qualcomm, Texas Instruments. Try each one first, then open the toggle: it gives the answer, why it is right, and the idea behind it explained from scratch.

### 1 · figure rotated 135 degrees then back 45

*Asked by: JSW (Aptitude test)*

Choose the figure that, after being rotated $135^\circ$ clockwise and then $45^\circ$
counter-clockwise, is identical to the question figure. (The figure and the four options
are drawings and are not reproduced.)

{{< details title="Answer and explanation" closed="true" >}}

**Method** (the figures are drawings and cannot be reproduced): the correct option is the question figure turned 90° counter-clockwise.

**Why.** 135° clockwise then 45° counter-clockwise is a net 90° clockwise. We need an option that becomes the question figure after that net turn, so the option must be the question figure turned back by 90°, i.e. counter-clockwise.

**Concept: compose rotations.** Rotations about the same centre add (clockwise positive, counter-clockwise negative). To find what rotates into a target, undo the net rotation. Check one asymmetric detail (where a small mark points) instead of the whole figure.

{{< /details >}}

### 2 · figure series

*Asked by: Oracle (HackerRank MCQ test)*

Predict the figure in the (?) place. The problem figures are: five dots with lines fanning
down to a point and a star at the bottom right; five dots with lines fanning up from a point
and a star at the bottom centre; three dots joined by lines with a small arc; then (?). The
answer figures (1)-(4) are shown in the photo (figure-series questions cannot be reproduced
exactly in text).

- **(a)** 1
- **(b)** 2
- **(c)** 3
- **(d)** 4

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) 4** (most likely; the figures are too blurred to confirm the rule)

**Why.** The third figure switches to three dots with an arc. Only answer figures 3 and 4 keep three dots with arcs, and 4 also continues the rotation of the lines from figure to figure, which matches the series. The candidate ticked 4.

**Concept: figure series.** Track each element separately (number of dots, direction of lines, position of the star, new parts) and find how each changes per step. The right option continues every element's pattern at once.

{{< /details >}}

### 3 · Q3, water image

*Asked by: Qualcomm (Nov 2024 (HirePro))*

Which is the exact water image of the word POTATO? (The four options are drawings of the word
reflected or rotated; see the source photo.)

{{< details title="Answer and explanation" closed="true" >}}

**Answer: the option where POTATO keeps its left-to-right order but every letter is flipped upside down** (the ticked second option looks like this).

**Why.** A water image is a reflection in a horizontal line (like a lake below the word). Left and right do not change, so P stays first, but top and bottom swap.

**Concept: mirror image vs water image.** Mirror (vertical mirror beside the word): order reversed and each letter flipped left-right. Water (horizontal line below): order kept, each letter flipped top-bottom. Letters symmetric about a horizontal axis (like O, X, H) look unchanged in a water image.

{{< /details >}}

### 4 · counting triangles

*Asked by: Texas Instruments (IIT BHU 2023)*

How many triangles are in the figure (a rectangle with a zig-zag line between its long sides
and one long diagonal)?

- **(a)** 20
- **(b)** 22
- **(c)** 23
- **(d)** 25

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) 22**

**Why.** Counted by listing the figure's line segments and checking every set of three lines that meet pairwise at three different points. (The IISc candidate's 25 over-counts.)

**Concept: systematic triangle counting.** Label every intersection point. A triangle is three points, each pair joined by a straight segment of the figure, not all on one line. Count by the smallest triangles first, then those made of 2, 3, ... pieces, or count by choosing a vertex and listing triangles with it as the top vertex.

{{< /details >}}

### 5 · counting triangles (another figure)

*Asked by: Texas Instruments (NIT Calicut 2023)*

How many triangles are in the figure (a tall rectangle cut into halves, crossing lines and
four small rectangles)?

- **(a)** 21
- **(b)** 20
- **(c)** 18
- **(d)** 16

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) 21** (the candidate's sheet; the photo is too skewed to recount reliably)

**Concept: systematic counting.** Same method as above: label intersection points and count triangles by size, so none is counted twice or missed.

{{< /details >}}
