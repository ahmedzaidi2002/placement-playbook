---
title: "Cryptarithms (letters for digits)"
weight: 14
---

4 questions asked by ION Group, JSW. Try each one first, then open the toggle: it gives the answer, why it is right, and the idea behind it explained from scratch.

### 1 · Q5, SEND + MORE = MONEY

*Asked by: ION Group (SDE OA, Jul 2025)*

In the equation SEND $+$ MORE $=$ MONEY, where each letter is a unique digit 0-9, what is
the value of M?

- **(a)** 0
- **(b)** 1
- **(c)** 2
- **(d)** 3

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) 1**

**Why.** Two four-digit numbers add to less than 20,000, so a five-digit sum must start with 1: M = 1. (The full solution is 9567 + 1085 = 10652.)

**Concept: leading-digit carry in cryptarithms.** When a sum has one more digit than its longest addend, that extra leading digit is the final carry, and a carry from adding two numbers is at most 1.

{{< /details >}}

### 2 · POINT + ZERO = ENERGY

*Asked by: JSW (Aptitude test)*

If POINT $+$ ZERO $=$ ENERGY (each letter a different digit), then
$E + N + E + R + G + Y = {?}$

- **(a)** 17
- **(b)** 19
- **(c)** 18
- **(d)** 16

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) 17**

**Why.** A five-digit plus a four-digit number gives a six-digit result, so the sum is at least 100,000: E = 1 and POINT ≥ 90,000, so P = 9. Searching the remaining digits gives one solution: 98504 + 3168 = 101672. E + N + E + R + G + Y = 1 + 0 + 1 + 6 + 7 + 2 = 17.

**Concept: start cryptarithms from the leading columns.** The size of the result fixes the first digits (carries are 0 or 1). Then work column by column, tracking carries, and use "all letters are different" to prune.

{{< /details >}}

### 3 · TAP + OFF = FILE

*Asked by: JSW (Aptitude test)*

For the cryptarithm TAP $+$ OFF $=$ FILE, assume $T = 8$, $A = 3$ and $P = 5$. What is
the value of LATE?

- **(a)** 8346
- **(b)** 4638
- **(c)** 4386
- **(d)** 1286

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) 4386**

**Why.** A three-digit plus a three-digit sum has four digits, so F = 1. Units: P + F = 5 + 1 = 6 = E (no carry). Tens: A + F = 3 + 1 = 4 = L. So L = 4, A = 3, T = 8, E = 6: LATE = 4386. (Two full solutions exist, 835 + 211 and 835 + 911, but both give L = 4, E = 6.)

**Concept: you only need the letters asked.** Fill columns until every letter in the target word is known; the rest can stay ambiguous.

{{< /details >}}

### 4 · MAC + MAAR = JOCKO

*Asked by: JSW (Aptitude test)*

What is the sum of 3 times A, 2 times M and 2 times C, if MAC $+$ MAAR $=$ JOCKO (each
letter a different digit)?

- **(a)** 38
- **(b)** 31
- **(c)** 33
- **(d)** 36

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) 31**

**Why.** MAC + MAAR = JOCKO: a three-digit plus a four-digit number giving five digits forces J = 1, then MAAR ≥ 9000 so M = 9 and O = 0. The unique solution is 932 + 9338 = 10270 (A = 3, C = 2, R = 8, K = 7). 3A + 2M + 2C = 9 + 18 + 4 = 31.

**Concept: carries pin down leading letters.** A five-digit sum from a four-digit addend means a carry out of the thousands column, which needs the addend to start with 9 (with a carry in). Then solve the remaining columns.

{{< /details >}}
