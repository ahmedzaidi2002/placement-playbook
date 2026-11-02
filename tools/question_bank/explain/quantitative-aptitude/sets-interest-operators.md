@@ acc-idc-sets
**Answers: (21) 56 (22) 120 (23) 5 (24) 500 (25) 80**

**Why.**
- (21) Everyone uses green or red: 70 = 52 + R − 38 → R = 56.
- (22) At least one = 100 + 40 − 20 = 120.
- (23) Cleared at least one = 37 + 38 − 30 = 45; none = 50 − 45 = 5.
- (24) Only trainers = total − learners = 2000 − 1500 = 500 (everyone attended in at least one role).
- (25) Both = 250 + 230 − 400 = 80.

**Concept: inclusion–exclusion for two sets.** |A ∪ B| = |A| + |B| − |A ∩ B|. People in both groups get counted twice when you add the two group sizes, so subtract the overlap once. Any one of the four numbers (A, B, both, either) follows from the other three. "Neither" = total − |A ∪ B|.

@@ acc-pap-club
**Answers: (21) 300 (22) 127 (23) 8 (24) 12 (25) 15 (26) 5500 (27) 3500**

**Why.**
- (21) 727 = 600 + H − 173 → H = 300. (22) Only hockey = 300 − 173 = 127.
- (23) Only game 1 = 40 − 26 − 8 + 2 = 8. (24) Only game 3 = 46 − 8 − 28 + 2 = 12. (25) Only game 2 = 67 − 26 − 28 + 2 = 15.
- (26)–(27) Taking 55% as a share of all voters: 10% did not vote, so the loser has 35%. The 20% gap = 2000 votes, so there are 10,000 voters: winner 5500, loser 3500.

**Concept: "only" regions in a three-set Venn diagram.** Only A = |A| − |A∩B| − |A∩C| + |A∩B∩C|. You subtract both pairwise overlaps, but that removes the triple overlap twice, so add it back once. Drawing the three circles and filling from the centre outward avoids mistakes.

@@ acc-pl-sets
**Answers: (21) 18 (22) 10 (23) 24 (24) 50**

**Why.**
- (21) 36 − 6 = 30 know at least one: 30 = 20 + H − 8 → H = 18.
- (22) Passed at least one = 74 + 76 − 60 = 90; failed both = 10.
- (23) N = (2N/3 + 12 − 6) + 2 → N/3 = 8 → N = 24.
- (24) 40 + 25 − 15 = 50.

**Concept: total = (at least one) + (neither).** Inclusion–exclusion gives "at least one"; the rest of the group is "neither". In (23), people only watching are the "neither" group.

@@ epam-q22
**Answer: (c) the number who passed only Maths**

**Why.** Let t = passed all three, a = only Physics and Chemistry, b = only Chemistry and Maths.
1. Physics: 12 (only P) + 4 (only P and M) + a + t = 37 → a + t = 21. So "both Physics and Chemistry" = a + t = 21 is known.
2. At least two: a + 4 + b + t = 29 → b = 4.
3. Only Chemistry = 30 − (a + t) − b = 30 − 21 − 4 = 5: known.
4. Only Maths = 40 − 4 − b − t = 32 − t, which depends on t: unknown.

**Concept: Venn regions as unknowns.** A three-set diagram has 7 regions. Write each given total as a sum of regions; whatever can be expressed using only known combinations is determined, and anything still containing a free unknown is not.

@@ jsw-languages
**Answer: (b) 310** (assuming everyone speaks at least one language)

**Why.** Let t speak all three. "Only two" groups total 40 + 20 + 10 = 70.
- Adding the three language totals counts each "exactly two" person twice and each "all three" person three times: 185 + 165 + 160 = 510 = (only one) + 2 × 70 + 3t.
- Town: (only one) + 70 + t = 400.
- From the first, only one = 370 − 3t. Then 370 − 3t + 70 + t = 400 → t = 20, so only one = 310.

**Concept: counting by multiplicity.** Sum of set sizes = (exactly one) + 2 × (exactly two) + 3 × (exactly three). Combined with the total count, this is often the fastest way through three-set problems.

@@ jsw-venn
**Answer: (d) 12/100**

**Why.** All regions add to 100: x + 28 + x(x − 10) + 36 = 100 → x² − 9x − 36 = 0 → (x − 12)(x + 3) = 0 → x = 12. P(only maths) = 12/100.

**Concept: Venn regions sum to the total.** Every student lies in exactly one region (only maths, both, only physics, neither). A count cannot be negative, so discard x = −3.

@@ kla-d-07
**Answer: (a) 67**

**Why.** Nobody visited both England and France, so nobody visited all three. Inclusion–exclusion: 26 + 26 + 32 − 0 − 6 − 11 + 0 = 67. (Regions: England only 20, France only 15, Italy only 15, England & Italy 6, France & Italy 11.) The photo's tick on 52 comes from a wrongly filled diagram.

**Concept: inclusion–exclusion for three sets.** |A∪B∪C| = |A| + |B| + |C| − |A∩B| − |A∩C| − |B∩C| + |A∩B∩C|. If any pairwise overlap is empty, the triple overlap is empty too.

@@ or-cricket
**Answer: (a) 28%**

**Why.** 12% like neither, so 88% like at least one. Both = 60 + 40 − 88 = 12%. Only cricket = 40 − 12 = 28%.

**Concept: inclusion–exclusion with percentages.** Treat percentages like counts out of 100.

@@ or-sets-games
**Answer: (c) 80** (the intended key; the wording is inconsistent)

**Why.** The setter means: 50 like football, 40 like hockey (totals), and the "rest", 100 − 50 − 40 = 10, like both. At least one = 50 + 40 − 10 = 80.

**Concept: totals vs "only".** "50 like football" normally means the whole football circle, including those who like both. Under that reading the union is 80. If 50 and 40 meant "only", the union would be 100, which is not offered.

@@ or25-languages
**Answer: (a) 30**

**Why.** At least one = 85 + 40 + 20 − 32 − 13 − 10 + x = 90 + x percent. Everyone surveyed speaks at least one language, so 90 + x = 100 → x = 10%. 10% of 300 = 30 people. (Option (c), 10, is the percentage, a trap.)

**Concept: solving for the triple overlap.** If the union is known (here 100%), the three-set formula has one unknown, |A∩B∩C|. Convert to people at the end.

@@ epam-q18
**Answer: (b) 15000**

**Why.** Alligation: the 8.5% loan is 1.5 below the average and the 11.2% loan is 1.2 above it. Balance: 12000 × 1.5 = X × 1.2 → X = 15000.

**Concept: the weighted average balances deviations.** In a weighted average, (amount below × its distance) = (amount above × its distance), like a see-saw balancing at the mean.

@@ exl-alice-bob
**Answer: none of the options with the numbers as photographed** (the question is flawed; the depreciation rate is printed as "147%", probably garbled).

**Why.** Split 3 units as 1 : 2. Alice's car after 2 years: 1 × (1 − 0.147)² = 0.7276. Bob's deposit: 2 × 1.2² = 2.88. Total 3.6076, up about 20.3%.

**Concept: compound growth and compound depreciation.** Value after n years = P(1 + r)ⁿ for growth and P(1 − r)ⁿ for depreciation. With several parts, compound each part separately, add them, and compare with the starting total.

@@ exl-funds
**Answer: (b) 10%**

**Why.**
1. Fund A interest: 4000 × 6% × 6 = 1440.
2. Split 1 : 2: 480 into B, 960 into C.
3. B earns 480 × 8% × 5 = 192, so C earns 192 + 288 = 480.
4. r_C = 480/(960 × 5) = 10%.

**Concept: simple interest SI = P × R × T / 100.** Interest is earned on the principal only. Rearranged: R = SI × 100/(P × T).

@@ sig-interest
**Answer: none of the options as printed** (with these numbers the sum is Rs 2560).

**Why.** In 2 years: SI at 8% = 0.16P. CI at 10% = (1.1² − 1)P = 0.21P. Difference 0.05P = 128 → P = 2560. If both rates were 10%, the difference would be 0.01P = 128 and P = 12,800, option (b); the question was probably garbled.

**Concept: CI vs SI.** Compound interest earns interest on interest. Over 2 years at the same rate r, CI − SI = P(r/100)², the interest on the first year's interest.

@@ ti-caesar
**Answer: (c) slightly less than 2 years** (the tick)

**Why.** 40% a year compounded half-yearly = 20% per half-year. After 3 half-years: 1.2³ = 1.728; after 4: 1.2⁴ = 2.0736. So the money passes double during the 4th half-year; if growth were continuous within it, the moment is 1.2ᵗ = 2 → t ≈ 3.8 half-years ≈ 1.9 years. (If interest is only credited at the end of each half-year, the balance first exceeds double exactly at 2 years.)

**Concept: compounding frequency.** With annual rate R compounded k times a year, each period uses rate R/k and there are k periods per year: A = P(1 + R/k)^(kn). More frequent compounding grows money slightly faster, so doubling comes a little sooner than at simple 40% (which would take 2.5 years).

@@ wf-q11
**Answer: (c) 8%** (reading "at the end of 5 years" as 5 years from the start)

**Why.** From year 3 to year 5 the amount grows by 5600 − 4960 = 640 in 2 years, so SI = 320 a year. Principal = 4960 − 3 × 320 = 4000. Rate = 320/4000 = 8%. (Read literally as 5 more years, the rate is 2.8%, not offered.)

**Concept: simple interest grows linearly.** Amount = P + P·R·T/100, a straight line in T. The rise between two dates gives the interest per year; going back to T = 0 gives the principal.

@@ acc-idc-ops
**Answers: (46) 13.3 (47) 14.7 (48) the first (49) the first (50) the first (51) the third**

**Why.** Replace the symbols, then use normal order of operations (÷ and × before + and −).
- (46) 9 − 8 ÷ 7 × 5 + 10 = 9 − 5.71 + 10 = 13.29.
- (47) 9 − 15 ÷ 9 × 2 + 9 = 9 − 3.33 + 9 = 14.67.
- (48) 36 − 12 ÷ 4 × 50 + 8 = 36 − 150 + 8 = −106.
- (49) 6 − 7 + 2 × 3 = 5 > 0 ÷ 7 = 0, true.
- (50) 16 + 8 − 6 ÷ 90 × 12 = 24 − 0.8 = 23.2.
- (51) 16 + 18 − 4 ÷ 40 × 8 = 34 − 0.8 = 33.2.

**Concept: substitute first, then BODMAS.** Rewrite the whole expression with real operators before evaluating anything. Precedence follows the real operators (not the printed symbols): division and multiplication left to right, then addition and subtraction.

@@ acc-pl-ops
**Answers: (45) 159 (46) 17**

**Why.**
- (45) 9 − 4 ÷ 4 + 7 × 22 − 3 = 9 − 1 + 154 − 3 = 159.
- (46) 4 − 15 ÷ 3 + 9 × 2 = 4 − 5 + 18 = 17.

**Concept: symbol substitution.** Write the translated expression on paper, then apply BODMAS. Mistakes come from evaluating while translating.
