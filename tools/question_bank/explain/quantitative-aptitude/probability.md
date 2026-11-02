@@ devrev-q4
**Answer: (a) 671/1001**

**Why.**
1. 14 fruits, 4 drawn without replacement: C(14,4) = 1001 equally likely draws.
2. Draws with no orange use only the 11 non-oranges: C(11,4) = 330.
3. P(at least one orange) = 1 − 330/1001 = 671/1001.

**Concept: "at least one" = 1 − P(none).** Counting draws with one, two or three oranges separately works but is slower. The complement has a single case. The /343 options assume drawing with replacement (7³ style), which does not match picking fruits out of a bucket.

@@ fj-iisc-5
**Answer: in the exam pick (d) 1/109**, the key. With the question exactly as worded, the answer is 27/31, which is not an option; the key swaps the lying and truth probabilities.

**Why (Bayes).** Let R = it rains, and "yes" = all three say it rains.
- As stated (each lies with 1/4, so tells the truth with 3/4): P(R | yes) = (1/5)(3/4)³ / [(1/5)(3/4)³ + (4/5)(1/4)³] = 27/(27 + 4) = 27/31.
- Key's reading (truth with 1/4, lie with 3/4): (1/5)(1/64) / [(1/5)(1/64) + (4/5)(27/64)] = 1/(1 + 108) = 1/109.

**Concept: Bayes' theorem.** P(cause | evidence) = P(evidence | cause) P(cause) / P(evidence). Here two "causes" can produce the same evidence: it rains and everyone tells the truth, or it does not rain and everyone lies. Compute both paths, then take the share that came from the cause you want. Independent friends means you multiply their probabilities.

@@ ion-q8
**Answer: (b) 240** (under the intended binomial reading; the wording is muddled)

**Why.** Treat each of a farmer's 6 animals as a hen with probability 1/3 and a cow with probability 2/3, independently. P(exactly 2 hens) = C(6,2)(1/3)²(2/3)⁴ = 15 × 16/729. Expected farmers = 729 × 15 × 16/729 = 240.

**Concept: binomial distribution and expected counts.** If each of n independent trials succeeds with probability p, P(exactly k successes) = C(n,k) pᵏ (1 − p)ⁿ⁻ᵏ. Multiply a probability by the number of farmers to get the expected number of farmers. The 729 = 3⁶ is chosen so the fractions cancel, which tells you this reading is the intended one.

@@ ie-q10
**Answer: (d) 3/8** (the textbook answer)

**Why.** He reports a 6 if (a) it is a 6 and he tells the truth: 1/6 × 3/4 = 3/24, or (b) it is not a 6 and he lies (assumed to say "6"): 5/6 × 1/4 = 5/24. P(actually 6 | reported 6) = (3/24)/(3/24 + 5/24) = 3/8.

**Concept: Bayes with a truthfulness probability.** Split "he says 6" into the true path and the lying path, then take the true path's share. Note the hidden assumption: every lie becomes "6". If a lie picked one of the other five faces at random, the lying path would be 5/6 × 1/4 × 1/5 and the answer would become 3/4.

@@ ie-q2
**Answer: pick (b) 8/4807** (the key); the exact value is 4/4807, which is not an option.

**Why.** All six fruits must be bananas: choose 6 of the 9 bananas out of 6 of 23 fruits: C(9,6)/C(23,6) = 84/100,947 = 4/4807. Option (b) is exactly twice this, almost certainly a typo in the key.

**Concept: drawing without replacement = combinations ratio.** "One by one without replacement" gives the same probability as grabbing 6 at once, because order does not change which fruits you end up with. So P = (ways to pick only bananas)/(ways to pick any 6). Equivalently 9/23 × 8/22 × 7/21 × 6/20 × 5/19 × 4/18.

@@ kla-d-25
**Answer: (d) 1/36**

**Why.** The father says "snow". Paths: snow and he tells the truth: 1/8 × 1/6 = 1/48. No snow and he lies: 7/8 × 5/6 = 35/48. P(snow | claim) = (1/48)/(1/48 + 35/48) = 1/36.

**Concept: Bayes' theorem.** A claim from an unreliable source should update a low prior only a little. Weigh the true path against the false path; the answer is the true path's share of all ways the claim could be made.

@@ mw-iisc-18
**Answer: (d) 7/15**

**Why.** 7 good watches out of 10. P(both good) = C(7,2)/C(10,2) = 21/45 = 7/15. Or step by step: 7/10 × 6/9 = 42/90 = 7/15.

**Concept: dependent events.** Without replacement, the second probability changes after the first pick (6 good left out of 9). Multiply the conditional probabilities along the path.

@@ mw-iisc-19
**Answer: (d) 32/64 = 1/2**

**Why.** With 7 flips, heads and tails can never tie (7 is odd). So either heads > tails or tails > heads. A fair coin treats them symmetrically, so each has probability 1/2.

**Concept: symmetry.** Before computing sums of binomial terms (C(7,4) + C(7,5) + C(7,6) + C(7,7) = 64 of 128), look for a symmetry that splits the outcomes into equally likely halves.

@@ mw-iitb-1
**Answer: (a) 1/6**

**Why.** Sum > 9 means 10, 11 or 12. Sum 10: (4,6), (5,5), (6,4) = 3 ways; sum 11: 2 ways; sum 12: 1 way. Total 6 of 36 = 1/6.

**Concept: list outcomes in a 6 × 6 grid.** Two dice give 36 equally likely ordered pairs. Count pairs that satisfy the condition; remember (4,6) and (6,4) are different outcomes.

@@ mw-iitb-4
**Answer: (c) 0.239** (counting the first 20 Fibonacci numbers from F₀ = 0)

**Why.** Every third Fibonacci number is even (0, 2, 8, 34, ...). F₀ to F₁₉ contain 7 even and 13 odd numbers. P(first even, second odd) = 7/20 × 13/19 = 91/380 ≈ 0.239. (Starting from F₁ = 1 gives 6 even and 0.221, not an option.)

**Concept: parity pattern of Fibonacci numbers.** Odd + odd = even and odd + even = odd, so the parities repeat as even, odd, odd, even, odd, odd, ... with period 3. Then it is a two-step draw without replacement: multiply 7/20 by 13/19.

@@ mw-iitb-5
**Answer: (a) C(10,4)(1/6)⁴(5/6)⁶**

**Why.** Ten independent rolls; "success" = rolling a 2, p = 1/6. Exactly 4 successes: choose which 4 rolls (C(10,4)), multiply (1/6)⁴ for them and (5/6)⁶ for the other 6.

**Concept: binomial probability.** P(k successes in n trials) = C(n,k) pᵏ (1 − p)ⁿ⁻ᵏ. The powers must add to n (4 + 6 = 10), and the C(n,k) must use the same k as the success power. That rules out every other option.

@@ mw-nitd-2
**Answer: (b) 100%**

**Why.** There are at most 366 possible birthdays. With 400 people, at least two must share one.

**Concept: pigeonhole principle.** If more items than boxes are placed into boxes, some box holds at least two. The famous "birthday paradox" (23 people give over 50%) only matters below 367 people.

@@ mw-nitd-3
**Answer: (b) 21/56** (= 3/8)

**Why.** P(second white) = P(W then W) + P(B then W) = 3/8 × 2/7 + 5/8 × 3/7 = 6/56 + 15/56 = 21/56 = 3/8.

**Concept: symmetry of draws.** Without any information about the first ball, every position in the drawing order is equally likely to hold any given ball. So P(second is white) = P(first is white) = 3/8. The total-probability calculation confirms it.

@@ mw-nitdl-2
**Answer: (c) 0.24**

**Why.** Multiples of 7 up to 100: ⌊100/7⌋ = 14. Of 9: ⌊100/9⌋ = 11. Of both (i.e. of 63): 1. By inclusion–exclusion, 14 + 11 − 1 = 24 numbers, probability 24/100.

**Concept: inclusion–exclusion.** |A or B| = |A| + |B| − |A and B|, because numbers in both were counted twice. "Divisible by 7 and 9" means divisible by their LCM, 63.

@@ nv-6
**Answer: (a) 18/203**

**Why.** For one flavour: 10/30 × 9/29 × 8/28. Any of 3 flavours: 3 × 720/24,360 = 2160/24,360 = 18/203.

**Concept: multiply along a path, add across disjoint cases.** Each toffee is eaten, so the counts drop (without replacement). "All the same" means all orange OR all pineapple OR all mango; these cannot happen together, so add their probabilities (all equal here, hence × 3).

@@ plutus-q3
**Answers: 1. $0 for both. 2. Raise the stake the first time you are ahead by one point; your expected value becomes $10/3 ≈ $3.33.**

**Why.**
1. Your score is a fair ±1 random walk from 0 that stops at +2 (you win) or −2 (you lose). By symmetry each player wins with probability 1/2, so the expected value is 0.
2. From score s, the probability you win is (s + 2)/4 (gambler's ruin on −2..2). At s = 1 that is 3/4, so raising to $20 is worth 20 × 3/4 − 20 × 1/4 = $10, which beats waiting. At s ≤ 0 raising has value ≤ 0, so you wait. Let V(s) be your value: V(1) = 10, V(−1) = ½V(0) + ½(−10), V(0) = ½V(1) + ½V(−1). Solving, V(0) = 10/3.

**Concept: expected value and the gambler's ruin.** Expected value = Σ (payoff × probability). In a fair random walk between two barriers, the chance of hitting the upper one first rises linearly with your position. An option you control (when to double) has value: you use it only when the odds favour you, which lifts your expected value above zero.

@@ plutus-q4
**Answer: 50 by maximum likelihood; 99 as an unbiased estimate.** Interviewers want both and why.

**Why.**
- Maximum likelihood: P(seeing 50 | n) = 1/n for n ≥ 50 (and 0 for n < 50). 1/n is largest at the smallest allowed n, so n = 50.
- Unbiased: for one draw X, E[X] = (n + 1)/2, so 2X − 1 has expected value n. With X = 50 the estimate is 99.

**Concept: estimators.** A maximum-likelihood estimate picks the parameter that makes the observed data most probable. An unbiased estimate is right on average over many repetitions. They can differ a lot from one sample. This is the one-sample version of the German tank problem.

@@ qc60-19
**Answer: (c) 37/120**

**Why.** 10 parts: 5 standard (S), 3 rework (J), 2 rejected (R); 3 drawn in order, 10 × 9 × 8 = 720 ordered draws. We need exactly one R, with no J before it.
- R with two S (any order): 3 positions for R × 2 × 5 × 4 = 120 ordered draws, i.e. 20/120 of the probability.
- R, S, J with R before J: 3 orders (R S J, R J S, S R J) × 2 × 5 × 3 = 90, i.e. 15/120.
- R then two J: 2 × 3 × 2 = 12, i.e. 2/120.
Total (120 + 90 + 12)/720 = 222/720 = 37/120. (Confirmed by listing all 720 ordered draws.)

**Concept: split an event into disjoint cases.** When a condition mixes "how many" with "in what order", break it into cases by which items are drawn, count orders that satisfy the condition in each, and add. Ordered draws without replacement have n × (n − 1) × (n − 2) outcomes.

@@ ti-chocolates
**Answer: (a) 1/2**

**Why.** 9 pieces, 3 picked. Exactly one fudge: choose 1 of 2 fudge balls and 2 of the 7 others: 2 × 21 = 42. All choices: C(9,3) = 84. P = 42/84 = 1/2. (The NIT candidate's 1/4 is wrong.)

**Concept: hypergeometric probability.** Drawing without replacement from groups: P = C(good, k) × C(others, n − k) / C(total, n). Choose from each group separately, multiply, divide by all choices.
