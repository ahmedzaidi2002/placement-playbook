---
title: "Number system, HCF/LCM, remainders"
weight: 12
---

8 questions asked by Flipkart, KLA, MAQ Software, Oracle, Plutus, Qualcomm, Wells Fargo. Try each one first, then open the toggle: it gives the answer, why it is right, and the idea behind it explained from scratch.

### 1 · four three-digit numbers

*Asked by: Flipkart (Neev 2025)*

Numbers: 334, 459, 626, 672. If 2 is subtracted from the first digit of each number, for
how many of them will the sum of the digits be even?

- **(a)** 3
- **(b)** 2
- **(c)** 0
- **(d)** 1

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) 3**

**Why.** Subtract 2 from the first digit: 334 → 134, 459 → 259, 626 → 426, 672 → 472. Digit sums: 8, 16, 12, 13. Three of them (8, 16, 12) are even.

**Concept: careful digit manipulation.** These are attention-to-detail questions. Change only what the rule says (the first digit), then compute. Shortcut: subtracting 2 from one digit lowers the digit sum by 2, which keeps its parity, so you only need the parity of the original digit sums: 10, 18, 14, 15 → three even.

{{< /details >}}

### 2 · Q20, digit reversal

*Asked by: KLA (IIT Delhi 2023)*

How many two-digit numbers are there which, when added to the number formed by
interchanging their digits, give a perfect square?

- **(a)** 10
- **(b)** 4
- **(c)** 0
- **(d)** 8

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) 8**

**Why.** A two-digit number is 10a + b; reversed, 10b + a. Their sum is 11a + 11b = 11(a + b). For this to be a perfect square it needs another factor 11, so a + b must be a multiple of 11. Since a + b ≤ 18, a + b = 11, giving 121 = 11². The numbers: 29, 38, 47, 56, 65, 74, 83, 92, which is 8 numbers.

**Concept: place value.** A two-digit number "ab" means 10a + b. Writing numbers this way turns digit puzzles into algebra. A perfect square has every prime factor an even number of times, so one factor of 11 must be paired by another.

{{< /details >}}

### 3 · largest common divisor of three numbers

*Asked by: MAQ Software (TalentDecrypt test, 2025)*

What is the largest integer that divides 23400, 272304 and 205248 without remainder?

- **(a)** 72
- **(b)** 48
- **(c)** 24
- **(d)** 96

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) 24**

**Why.** 23400 = 2³ × 3² × 5² × 13. It has only three factors of 2, so no common divisor can be divisible by 16; that rules out 48 and 96. 72 = 8 × 9 needs 3², and 272304 = 2⁴ × 3 × 5673 has only one factor of 3, so 72 fails. 24 = 2³ × 3 divides all three.

**Concept: HCF via prime factors.** The highest common factor takes each prime to the **lowest** power it has across the numbers. In MCQs you can eliminate options quickly: if one number has only 2³, nothing with 2⁴ or more can divide it.

{{< /details >}}

### 4 · remainder

*Asked by: Oracle (HackerRank MCQ test)*

What is the remainder of 1992 divided by 92?

- **(a)** 0
- **(b)** 1
- **(c)** 40
- **(d)** None of the above

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) none of the above** (the remainder is 60)

**Why.** 92 × 21 = 1932 and 1992 − 1932 = 60.

**Concept: division with remainder.** Dividend = divisor × quotient + remainder, with 0 ≤ remainder < divisor. Find the largest multiple of 92 that does not exceed 1992 and subtract.

{{< /details >}}

### 5 · trailing zeros

*Asked by: Plutus (OA)*

What is the smallest $N$ such that $N!$ ends in exactly 100 zeros?

{{< details title="Answer and explanation" closed="true" >}}

**Answer: 405**

**Why.**
1. Trailing zeros come from factors of 10 = 2 × 5. Factorials have far more 2s than 5s, so the number of zeros = number of factors 5 in N!.
2. That count is Z(N) = ⌊N/5⌋ + ⌊N/25⌋ + ⌊N/125⌋ + ...
3. Z(400) = 80 + 16 + 3 = 99. Z only changes at multiples of 5, so try 405: Z(405) = 81 + 16 + 3 = 100.
4. Nothing between 401 and 404 adds a 5, so 405 is the smallest.

**Concept: Legendre's formula.** The power of a prime p in N! is ⌊N/p⌋ + ⌊N/p²⌋ + ... . ⌊N/5⌋ counts multiples of 5, ⌊N/25⌋ adds the extra 5 in multiples of 25, and so on. Some zero counts are impossible: Z jumps by 2 at multiples of 25 (for example, no factorial ends in exactly 5 zeros, since 24! has 4 and 25! has 6).

{{< /details >}}

### 6 · peculiar numbers

*Asked by: Qualcomm (Nov 2024)*

A four-digit number is called peculiar if the sum of the number formed by the first
[cut off in the source] ... numbers are arranged in ascending order, find the sum of peculiar numbers just
[cut off in the source].

- **(a)** 2876
- **(b)** 4175
- **(c)** 3876
- **(d)** 4285

{{< details title="Answer and explanation" closed="true" >}}

**Answer: cannot be determined** (the definition of "peculiar" is cut off in the photo).

**What the question is testing.** A four-digit number abcd is usually split into "the number formed by the first two digits" (10a + b) and "the last two digits" (10c + d). Such definitions turn into an equation in place values; list the numbers that satisfy it in ascending order and add the ones asked for. Without the rest of the definition, none of the options can be checked.

**Concept: place value splits.** A four-digit number = 100 × (first two digits) + (last two digits). Writing it this way is the first step for any "number formed by its digits" puzzle.

{{< /details >}}

### 7 · remainder

*Asked by: Wells Fargo (SHL test, Oct 2022)*

Find the remainder when $888\ldots8$ (the digit 8 repeated 63 times) is divided by 9.

- **(a)** 4
- **(b)** 8
- **(c)** 0
- **(d)** 1

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) 0**

**Why.** A number leaves the same remainder mod 9 as its digit sum. The digit sum is 8 × 63 = 504, and 504 = 9 × 56, so the remainder is 0.

**Concept: divisibility by 9 (and 3).** Since 10 leaves remainder 1 when divided by 9, every power of 10 does too. So a number's value mod 9 equals the sum of its digits mod 9. That is why "digit sum divisible by 9" means "number divisible by 9".

{{< /details >}}

### 8 · divisibility by 30

*Asked by: Wells Fargo (SHL test, Oct 2022)*

The number $567xy$ is divisible by 30. The possible values of $x$ and $y$ respectively
can be

- **(a)** 0 and 0
- **(b)** 1 and 0
- **(c)** 2 and 0
- **(d)** 0 and 1

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) 0 and 0**

**Why.** 30 = 2 × 3 × 5 = 10 × 3.
- Divisible by 10: the last digit y = 0.
- Divisible by 3: digit sum 5 + 6 + 7 + x + 0 = 18 + x must be a multiple of 3, so x is 0, 3, 6 or 9.
Only (a) satisfies both.

**Concept: split a divisor into coprime factors.** A number is divisible by 30 exactly when it is divisible by 10 and by 3 (they share no factor). Test each with its simple rule: last digit 0 for 10, digit sum for 3.

{{< /details >}}
