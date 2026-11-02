@@ fk-digits
**Answer: (a) 3**

**Why.** Subtract 2 from the first digit: 334 → 134, 459 → 259, 626 → 426, 672 → 472. Digit sums: 8, 16, 12, 13. Three of them (8, 16, 12) are even.

**Concept: careful digit manipulation.** These are attention-to-detail questions. Change only what the rule says (the first digit), then compute. Shortcut: subtracting 2 from one digit lowers the digit sum by 2, which keeps its parity, so you only need the parity of the original digit sums: 10, 18, 14, 15 → three even.

@@ kla-d-20
**Answer: (d) 8**

**Why.** A two-digit number is 10a + b; reversed, 10b + a. Their sum is 11a + 11b = 11(a + b). For this to be a perfect square it needs another factor 11, so a + b must be a multiple of 11. Since a + b ≤ 18, a + b = 11, giving 121 = 11². The numbers: 29, 38, 47, 56, 65, 74, 83, 92, which is 8 numbers.

**Concept: place value.** A two-digit number "ab" means 10a + b. Writing numbers this way turns digit puzzles into algebra. A perfect square has every prime factor an even number of times, so one factor of 11 must be paired by another.

@@ maq-gcd
**Answer: (c) 24**

**Why.** 23400 = 2³ × 3² × 5² × 13. It has only three factors of 2, so no common divisor can be divisible by 16; that rules out 48 and 96. 72 = 8 × 9 needs 3², and 272304 = 2⁴ × 3 × 5673 has only one factor of 3, so 72 fails. 24 = 2³ × 3 divides all three.

**Concept: HCF via prime factors.** The highest common factor takes each prime to the **lowest** power it has across the numbers. In MCQs you can eliminate options quickly: if one number has only 2³, nothing with 2⁴ or more can divide it.

@@ or-remainder
**Answer: (d) none of the above** (the remainder is 60)

**Why.** 92 × 21 = 1932 and 1992 − 1932 = 60.

**Concept: division with remainder.** Dividend = divisor × quotient + remainder, with 0 ≤ remainder < divisor. Find the largest multiple of 92 that does not exceed 1992 and subtract.

@@ plutus-q1
**Answer: 405**

**Why.**
1. Trailing zeros come from factors of 10 = 2 × 5. Factorials have far more 2s than 5s, so the number of zeros = number of factors 5 in N!.
2. That count is Z(N) = ⌊N/5⌋ + ⌊N/25⌋ + ⌊N/125⌋ + ...
3. Z(400) = 80 + 16 + 3 = 99. Z only changes at multiples of 5, so try 405: Z(405) = 81 + 16 + 3 = 100.
4. Nothing between 401 and 404 adds a 5, so 405 is the smallest.

**Concept: Legendre's formula.** The power of a prime p in N! is ⌊N/p⌋ + ⌊N/p²⌋ + ... . ⌊N/5⌋ counts multiples of 5, ⌊N/25⌋ adds the extra 5 in multiples of 25, and so on. Some zero counts are impossible: Z jumps by 2 at multiples of 25 (for example, no factorial ends in exactly 5 zeros, since 24! has 4 and 25! has 6).

@@ qc-n-peculiar
**Answer: cannot be determined** (the definition of "peculiar" is cut off in the photo).

**What the question is testing.** A four-digit number abcd is usually split into "the number formed by the first two digits" (10a + b) and "the last two digits" (10c + d). Such definitions turn into an equation in place values; list the numbers that satisfy it in ascending order and add the ones asked for. Without the rest of the definition, none of the options can be checked.

**Concept: place value splits.** A four-digit number = 100 × (first two digits) + (last two digits). Writing it this way is the first step for any "number formed by its digits" puzzle.

@@ wf-q7
**Answer: (c) 0**

**Why.** A number leaves the same remainder mod 9 as its digit sum. The digit sum is 8 × 63 = 504, and 504 = 9 × 56, so the remainder is 0.

**Concept: divisibility by 9 (and 3).** Since 10 leaves remainder 1 when divided by 9, every power of 10 does too. So a number's value mod 9 equals the sum of its digits mod 9. That is why "digit sum divisible by 9" means "number divisible by 9".

@@ wf-q9
**Answer: (a) 0 and 0**

**Why.** 30 = 2 × 3 × 5 = 10 × 3.
- Divisible by 10: the last digit y = 0.
- Divisible by 3: digit sum 5 + 6 + 7 + x + 0 = 18 + x must be a multiple of 3, so x is 0, 3, 6 or 9.
Only (a) satisfies both.

**Concept: split a divisor into coprime factors.** A number is divisible by 30 exactly when it is divisible by 10 and by 3 (they share no factor). Test each with its simple rule: last digit 0 for 10, digit sum for 3.

@@ axx-ball
**Answer: (b) 33 ft**

**Why.** The ball first falls 27 ft. After that, each bounce goes up and comes down the same height: 2.7, 0.27, 0.027, ... Total = 27 + 2 × (2.7 + 0.27 + ...) = 27 + 2 × 2.7/(1 − 0.1) = 27 + 2 × 3 = 33 ft.

**Concept: infinite geometric series.** A series a + ar + ar² + ... with |r| < 1 adds up to a/(1 − r). Each bounce is 10% of the last, so r = 0.1. Remember the first drop is counted once, every later height twice (up and down).

@@ epam-q11
**Answer: (d) January ₹12,500, February ₹15,250.50, increase 22.00%**

**Why.** January savings = 31.25% of 40,000 = 12,500. February = 33.89% of 45,000 = 15,250.50. Increase = 2,750.50/12,500 ≈ 22.00%.

**Concept: percentage increase is measured from the starting value.** Change % = (new − old)/old × 100. The spending breakdown is noise; only the savings percentage and income matter.

@@ go-2
**Answer: (b) 36**

**Why.** Males = 4/10 × 1000 = 400. Know German: 30% of 400 = 120. Adults among them 70%, so non-adults 30%: 0.3 × 120 = 36.

**Concept: chained percentages.** Each percentage applies to the group just before it. Work down the chain: total → males → German speakers → not adults. "Not adults" is the complement, 100 − 70 = 30%.

@@ ion-q10
**Answer: (a) 29.577%**

**Why.** Area = length × breadth stays fixed. If length becomes 1.42 times, breadth must become 1/1.42 ≈ 0.70423 times. Decrease = 1 − 0.70423 = 0.29577, i.e. 29.577%.

**Concept: inverse proportion.** When a product must stay constant, increasing one factor by r% means the other falls by r/(100 + r) × 100%. Here 42/142 × 100 ≈ 29.58%. The decrease is always smaller than the increase.

@@ qc60-04
**Answer: (b) Rs 2313**

**Why.** Monisha saves 65% and Rohit 55% of their salaries. 0.65M : 0.55R = 5 : 4, so 2.6M = 2.75R and M : R = 2.75 : 2.6 = 55 : 52. M = 4500 × 55/107 ≈ 2313.

**Concept: savings = income − spending.** Spending 35% means saving 65%. Turn the savings ratio into an income ratio, then split the known total in that ratio (a share of a total in ratio a : b is total × a/(a + b)).

@@ sie-decrease
**Answer: 64**

**Why.** Decreasing by 12.5% leaves 87.5% = 0.875 of the number. 0.875x = 56, so x = 64.

**Concept: reverse percentages.** To undo a percentage change, divide by the multiplier; do not add 12.5% back (56 × 1.125 = 63, which is wrong because 12.5% of 56 is smaller than 12.5% of the original). 12.5% = 1/8, so the result is 7/8 of the original: 56 ÷ 7 × 8 = 64.

@@ ti-dog-cat
**Answer: (a) 150%**

**Why.** 24 hours = 1440 minutes. Barks: 1440/2 = 720. Meows: 1440/5 = 288. Excess = (720 − 288)/288 × 100 = 150%.

**Concept: "exceed by what percent" uses the smaller quantity as the base.** Also note the ratio of rates is 5/2 = 2.5, i.e. 150% more; the actual counts are not needed.

@@ ti-jia
**Answer: (a) Rs 2000**

**Why.** After spending 20%, 80% remains. Then 5% of that goes, leaving 95% of it. So 0.8 × 0.95 X = 0.76X = 1520, X = 2000.

**Concept: successive percentages multiply.** "5% of the remainder" applies to what is left, not to X. Multiply the remaining fractions, then divide the final amount by their product.

@@ ti-plot
**Answer: (b) 100/11 %**

**Why.** Length × 1.1, so breadth must become 1/1.1 = 10/11 of itself, a decrease of 1/11 = 100/11 % ≈ 9.09%.

**Concept: keeping a product constant.** Same rule as for any area: a rise of r% in one side needs a fall of r/(100 + r) × 100% in the other: 10/110 × 100 = 100/11.
