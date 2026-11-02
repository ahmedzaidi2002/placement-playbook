---
title: "Percentages"
weight: 9
---

9 questions asked by Axxela, EPAM, Grey Orange, ION Group, Qualcomm, Siemens Energy, Texas Instruments. Try each one first, then open the toggle: it gives the answer, why it is right, and the idea behind it explained from scratch.

### 1 · Q15, a bouncing tennis ball

*Asked by: Axxela (NIT Bhopal 2024)*

A tennis-ball maker claims its balls always rise to 10% of the height from which they were
dropped. If a ball is dropped from 27 feet, about how far does it travel before coming to
rest?

- **(a)** 32.4
- **(b)** 33
- **(c)** 34.6
- **(d)** 36

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) 33 ft**

**Why.** The ball first falls 27 ft. After that, each bounce goes up and comes down the same height: 2.7, 0.27, 0.027, ... Total = 27 + 2 × (2.7 + 0.27 + ...) = 27 + 2 × 2.7/(1 − 0.1) = 27 + 2 × 3 = 33 ft.

**Concept: infinite geometric series.** A series a + ar + ar² + ... with |r| < 1 adds up to a/(1 − r). Each bounce is 10% of the last, so r = 0.1. Remember the first drop is counted once, every later height twice (up and down).

{{< /details >}}

### 2 · Q11, savings in January and February

*Asked by: EPAM (EPAM freshers test)*

In January a person earned ₹40,000 and spent 35% on rent, 20% on food, 10% on
transport and 3.75% on utilities, saving 31.25%. In February the income rose to
₹45,000, with 33% on rent, 18% on food, 11% on transport, 3.82% on utilities and
33.89% saved. What were the savings in each month, and the percentage increase?

- **(a)** January ₹12,600, February ₹15,250.50, increase 21.03%
- **(b)** January ₹13,000, February ₹15,000, increase 15.38%
- **(c)** January ₹12,800, February ₹15,280, increase 19.38%
- **(d)** January ₹12,500, February ₹15,250.50, increase 22.00%

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) January ₹12,500, February ₹15,250.50, increase 22.00%**

**Why.** January savings = 31.25% of 40,000 = 12,500. February = 33.89% of 45,000 = 15,250.50. Increase = 2,750.50/12,500 ≈ 22.00%.

**Concept: percentage increase is measured from the starting value.** Change % = (new − old)/old × 100. The spending breakdown is noise; only the savings percentage and income matter.

{{< /details >}}

### 3 · Q2, male youths who speak German

*Asked by: Grey Orange (OA, Oct 2024)*

30% of the males living in a society know how to speak German. 70% of the males who
know German are adults. The ratio of males to females is $4 : 6$ and the total number
of people is 1000. Calculate the number of males who know German and are not adults.

- **(a)** 40
- **(b)** 36
- **(c)** 360
- **(d)** None of these

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) 36**

**Why.** Males = 4/10 × 1000 = 400. Know German: 30% of 400 = 120. Adults among them 70%, so non-adults 30%: 0.3 × 120 = 36.

**Concept: chained percentages.** Each percentage applies to the group just before it. Work down the chain: total → males → German speakers → not adults. "Not adults" is the complement, 100 − 70 = 30%.

{{< /details >}}

### 4 · Q10, keep the area of a rectangle

*Asked by: ION Group (SDE OA, Jul 2025)*

The length of a rectangle is increased by 42%. By what percentage should the breadth be
decreased so that the area does not change?

- **(a)** 29.577
- **(b)** 30.323
- **(c)** 25.565
- **(d)** None of these

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) 29.577%**

**Why.** Area = length × breadth stays fixed. If length becomes 1.42 times, breadth must become 1/1.42 ≈ 0.70423 times. Decrease = 1 − 0.70423 = 0.29577, i.e. 29.577%.

**Concept: inverse proportion.** When a product must stay constant, increasing one factor by r% means the other falls by r/(100 + r) × 100%. Here 42/142 × 100 ≈ 29.58%. The decrease is always smaller than the increase.

{{< /details >}}

### 5 · Problem Solving

*Asked by: Qualcomm (60-question online assessment)*

The sum of the salaries of Monisha and Rohit is Rs 4500. Monisha spends 35% of her salary and Rohit spends 45% of his salary. If their savings are in ratio 5:4, then what is the salary of Monisha?

- **(a)** Rs 2175
- **(b)** Rs 2313
- **(c)** Rs 2500
- **(d)** Rs 3177

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) Rs 2313**

**Why.** Monisha saves 65% and Rohit 55% of their salaries. 0.65M : 0.55R = 5 : 4, so 2.6M = 2.75R and M : R = 2.75 : 2.6 = 55 : 52. M = 4500 × 55/107 ≈ 2313.

**Concept: savings = income − spending.** Spending 35% means saving 65%. Turn the savings ratio into an income ratio, then split the known total in that ratio (a share of a total in ratio a : b is total × a/(a + b)).

{{< /details >}}

### 6 · C1, decreased by 12.5 per cent

*Asked by: Siemens Energy (MNNIT Allahabad (Mettl))*

When a number is decreased by 12.5%, the result is 56. What is the original number?

{{< details title="Answer and explanation" closed="true" >}}

**Answer: 64**

**Why.** Decreasing by 12.5% leaves 87.5% = 0.875 of the number. 0.875x = 56, so x = 64.

**Concept: reverse percentages.** To undo a percentage change, divide by the multiplier; do not add 12.5% back (56 × 1.125 = 63, which is wrong because 12.5% of 56 is smaller than 12.5% of the original). 12.5% = 1/8, so the result is 7/8 of the original: 56 ÷ 7 × 8 = 64.

{{< /details >}}

### 7 · barks and meows

*Asked by: Texas Instruments (IIT BHU 2023)*

A dog barks every 2 minutes and a cat meows every 5 minutes. In 24 hours the barks exceed the
meows by about what percent?

- **(a)** 150%
- **(b)** 250%
- **(c)** 100%
- **(d)** 50%

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) 150%**

**Why.** 24 hours = 1440 minutes. Barks: 1440/2 = 720. Meows: 1440/5 = 288. Excess = (720 − 288)/288 × 100 = 150%.

**Concept: "exceed by what percent" uses the smaller quantity as the base.** Also note the ratio of rates is 5/2 = 2.5, i.e. 150% more; the actual counts are not needed.

{{< /details >}}

### 8 · pocket money

*Asked by: Texas Instruments (IISc, second set)*

Jia spends 20% of her pocket money $X$ on necessary purchases and 5% of the remainder on
transport, and is left with Rs. 1520. What is $X$?

- **(a)** Rs. 2000
- **(b)** Rs. 5500
- **(c)** Rs. 2500
- **(d)** Rs. 6080

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) Rs 2000**

**Why.** After spending 20%, 80% remains. Then 5% of that goes, leaving 95% of it. So 0.8 × 0.95 X = 0.76X = 1520, X = 2000.

**Concept: successive percentages multiply.** "5% of the remainder" applies to what is left, not to X. Multiply the remaining fractions, then divide the final amount by their product.

{{< /details >}}

### 9 · a rectangular plot

*Asked by: Texas Instruments (IISc, second set)*

The length of a rectangular plot is increased by 10%. By what percent must the breadth be
decreased to keep the area the same?

- **(a)** 120/13
- **(b)** 100/11
- **(c)** 120/11
- **(d)** 100/9

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) 100/11 %**

**Why.** Length × 1.1, so breadth must become 1/1.1 = 10/11 of itself, a decrease of 1/11 = 100/11 % ≈ 9.09%.

**Concept: keeping a product constant.** Same rule as for any area: a rise of r% in one side needs a fall of r/(100 + r) × 100% in the other: 10/110 × 100 = 100/11.

{{< /details >}}
