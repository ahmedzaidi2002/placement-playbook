---
title: "Mathematical operations and input-output rules"
weight: 7
---

7 questions asked by Flipkart, JSW, KLA, Qualcomm, Texas Instruments. Try each one first, then open the toggle: it gives the answer, why it is right, and the idea behind it explained from scratch.

### 1 · a six-step process

*Asked by: Flipkart (Neev 2025)*

Consider the following six-step process. Step 1: divide by 2. Step 2: if the result is
less than 30, go to step 3 and continue from there; otherwise proceed to step 4. Step 3:
add 12. Step 4: add 3. Step 5: multiply by 3. Step 6: subtract 40. Which starting value
produces an even result? (The divisor in step 1 is blurred; 2 is the reading that makes
exactly one option work.)

- **(a)** 56
- **(b)** 48
- **(c)** 40
- **(d)** 62

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) 62**

**Why.** 62 ÷ 2 = 31 ≥ 30, skip step 3: 31 + 3 = 34, × 3 = 102, − 40 = 62 (even). The others go through step 3: 56 → 28 → 40 → 43 → 129 → 89; 48 → 24 → 36 → 39 → 117 → 77; 40 → 20 → 32 → 35 → 105 → 65 (all odd).

**Concept: follow branching instructions exactly.** Process flows with conditions are flowcharts: evaluate the condition with the current value, take one branch, and continue. A parity shortcut: the final value is 3(something) − 40, even exactly when "something" is even.

{{< /details >}}

### 2 · input-output with number blocks

*Asked by: JSW (Aptitude test)*

An input-output is given in steps. Step 1 combines the pairs of 2-digit blocks
$(24, 73)$, $(56, 13)$, $(20, 39)$ into $57$, $49$, $19$; step 2 gives the blocks $25$ and
$58$; step 3 gives $10$ and $40$; step 4 gives $50$. Following the same rules, what is the
final output for the input $54\ 62\ 89\ 25\ 11\ 27$?

- **(a)** 17
- **(b)** 12
- **(c)** 51
- **(d)** 67

{{< details title="Answer and explanation" closed="true" >}}

**Answer: not determinable from the photos.**

**Why.** The example fits several rules: steps 3 and 4 look like "product of digits" (2 × 5 = 10, 5 × 8 = 40) then "sum" (10 + 40 = 50), and step 1 fits "difference of the tens digits, sum of the units digits". But step 2's arrows are not legible, and the rules that fit the example do not lead to any option for the new input.

**Concept: input-output puzzles.** Find a rule that reproduces every step of the example, then apply it unchanged. If more than one rule fits, the question is ambiguous; prefer the simplest rule that fits all steps.

{{< /details >}}

### 3 · number arrangement machine, step III

*Asked by: JSW (Aptitude test)*

A machine rearranges a line of numbers step by step.
Input: 58 95 37 43 64 42 11 12.
Step I: 14 58 37 43 64 42 12 00.
Step II: 10 14 58 37 43 42 00 01.
Step III: 13 10 14 43 42 00 01 04.
Step IV: 07 13 10 14 00 01 04 02.
Step V: 00 01 02 04 07 10 13 14 (the last step).
For the input 13 56 66 89 99 23 17 33, what is the difference between the highest and the
lowest number in step III?

- **(a)** 64
- **(b)** 87
- **(c)** 55
- **(d)** 16

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) 55**

**Why.** The rule (it reproduces all five example steps): in each step, the largest remaining input number is replaced by the sum of its digits and moved to the front; the smallest is replaced by the difference of its digits and moved to the end; the last step sorts everything.
- Step I: 99 → 18 at the front, 13 → 02 at the end.
- Step II: 89 → 17, 17 → 06.
- Step III: 66 → 12, 23 → 01: 12 17 18 56 33 02 06 01.
Highest 56, lowest 01: difference 55.

**Concept: machine rearrangement.** Compare consecutive steps to see which numbers moved and how they changed. Usually one or two numbers are processed per step, chosen by size or position.

{{< /details >}}

### 4 · Q17, symbol pattern

*Asked by: KLA (IIT Delhi 2023)*

If $5+2+2 = 101041$, $9+2+4 = 183662$, $8+6+3 = 482466$ and $5+4+5 = 202504$, then
what is $7+2+5$?

- **(a)** 143524
- **(b)** 143542
- **(c)** 145354
- **(d)** 143554

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) 143542**

**Why.** For a + b + c the result is three blocks: a × b, a × c, then (a + c) × b written backwards.
- 5+2+2: 10, 10, 14 → 41. 9+2+4: 18, 36, 26 → 62. 8+6+3: 48, 24, 66. 5+4+5: 20, 25, 40 → 04.
- 7+2+5: 14, 35, 24 → 42, giving 143542. (The photo's 143554 used a wrong last block.)

**Concept: split the output into blocks.** A six-digit answer from three small numbers is usually three two-digit blocks. Find each block's rule from the examples and check it on all of them.

{{< /details >}}

### 5 · Puzzles

*Asked by: Qualcomm (60-question online assessment)*

Find the missing number. 3, 5, 4 → 29 ; 4, 6, 5 → 46 ; 5, 7, 6 → ?

- **(a)** 69
- **(b)** 65
- **(c)** 67
- **(d)** 63

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) 67**

**Why.** Rule: (a + b) × c − a. Check: (3 + 5) × 4 − 3 = 29; (4 + 6) × 5 − 4 = 46. So (5 + 7) × 6 − 5 = 72 − 5 = 67.

**Concept: guess, then verify on every example.** Try simple combinations (sums, products, squares) that land near the outputs, then adjust with a small correction. A rule counts only if it fits all the examples.

{{< /details >}}

### 6 · a strange multiplication

*Asked by: Texas Instruments (IIT ISM 2024)*

$55 \times 53 = 2$, $45 \times 60 = 5$, $65 \times 55 = 1$. Find $89 \times 73$.

- **(a)** 0
- **(b)** 1
- **(c)** 2
- **(d)** 3

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) 3**

**Why.** Take each number's digit difference, then the difference of those: 55 × 53 → |0 − 2| = 2; 45 × 60 → |1 − 6| = 5; 65 × 55 → |1 − 0| = 1. 89 × 73 → |1 − 4| = 3.

**Concept: the symbol is not the real operation.** In coded-operation puzzles look at the digits of each number separately (sum, difference, product) and see what combination gives the output.

{{< /details >}}

### 7 · a strange subtraction

*Asked by: Texas Instruments (IISc, second set)*

In a certain system $62 - 56 = 0$, $48 - 32 = 1$, $55 - 31 = 4$. Find $42 - 28$.

- **(a)** 1
- **(b)** 2
- **(c)** 3
- **(d)** 4

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) 1**

**Why.** Take the true differences: 62 − 56 = 6, 48 − 32 = 16, 55 − 31 = 24. The results 0, 1, 4 are the squares of their tens digits (0, 1, 2). 42 − 28 = 14 → 1² = 1.

**Concept: test the real operation first.** Compute what the symbol normally gives and look for a transformation of that result (here, square of the tens digit).

{{< /details >}}
