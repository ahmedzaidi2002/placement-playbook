@@ acc-idc-detail
**Answers: (41) A (42) A (43) C (44) C (45) C**

**Why.** Compare the items character by character, in small chunks.
- (41), (42): the three items are identical.
- (43): items 1 and 3 are NIINIININN; item 2 (NIININNINN) differs from the 5th letter.
- (44): items 1 and 3 read 4665.8009291; item 2 has 4665.7999291.
- (45): items 1 and 3 read 808088080.8080; item 2 has 808008080.8080.

**Concept: chunked comparison.** These questions test speed without errors. Split each string into blocks of 3–4 characters and compare block by block; check the length first, because a dropped or extra character shifts everything after it.

@@ acc-pap-detail
**Answers: (41) D (42) A (43) D (44) C (45) D**

**Why.**
- (41) GGGGMMMGG has 9 letters; the other two have 10 and differ from each other (MMM vs MGM), so none match. (The key's B looks like a transcription error.)
- (42) Identical.
- (43) 1980886, 1980786, 1979886: all three differ.
- (44) Items 1 and 3 are "papanicolaou"; item 2 ends in "-oi". So C (the key's B is wrong).
- (45) "skeptic", "skeptick", "sckeptic": all differ.

**Concept: count lengths first.** A string that is one character shorter can never match, and you can see it before reading letters. Then compare the remaining items chunk by chunk.

@@ acc-pl-detail
**Answers: (41) C (42) A (43) D**

**Why.** (41) Item 2 has H where items 1 and 3 have N (KKTUJ**N**GD...), so only 1 and 3 match. (42) All three identical. (43) 5738491, 5783491, 5738461: all differ (a swapped pair in item 2, one digit changed in item 3).

**Concept: watch for swaps and single-digit changes.** Setters use transposed neighbours (38 → 83) and one changed digit; reading in fixed-size chunks catches both.

@@ acc-prev-detail
**Answers: (41) C (42) A (43) E (44) D (45) B**

**Why.** (41) Items 1 and 3 end in 7324, item 2 in 7154. (42) Identical. (43) All three differ. (44) Items 2 and 3 read 7666137.8787; item 1 has 7661637. (45) Items 1 and 2 read 101100110.0101; item 3 has 101100100.

**Concept: same as above.** Compare in chunks; a long run of 0s and 1s is easiest to check in groups of three.

@@ acc-idc-reason
**Answers: (26) sister (27) south-west (28) 44 (29) west (30) CAT**

**Why.**
- (26) "Your mother's husband" is the lady's father; his sister is the lady's aunt, and she is also the man's aunt. Sharing that aunt through the same father, they are siblings: the lady is his sister.
- (27) West, +45° clockwise → north-west; +180° → south-east; −270° (anticlockwise) is the same as +90° clockwise → south-west.
- (28) Position from the end = total − position from front + 1 = 60 − 17 + 1 = 44.
- (29) North-west, +90° clockwise → north-east, −135° → west.
- (30) VA**CAT**E, S**CAT**TER, **CAT**ER.

**Concepts.**
- **Blood relations:** translate phrases one link at a time ("mother's husband" = father).
- **Direction turns:** add clockwise turns, subtract anticlockwise ones, and reduce mod 360°. Compass order clockwise: N, NE, E, SE, S, SW, W, NW, 45° apart.
- **Ranking:** front + back = total + 1, because the person is counted from both ends.

@@ acc-pap-rel
**Answers: (38) cousin (39) mother (40) north-west**

**Why.**
- (38) The uncle's daughter is Saroj's cousin; her brother is also the uncle's child, so a cousin too.
- (39) Bindu is Narain's daughter but Mona's step-daughter, so Mona is not her mother. Narain's other wife, Sita, is.
- (40) South-east is renamed east: every direction moves 45° anticlockwise (SE → E). Applying the same shift, north becomes north-west. (The key's north-east is wrong.)

**Concept: renamed directions are a rotation.** Find how far one known pair has turned (SE → E is 45° anticlockwise) and apply that same turn to the asked direction.

@@ ion-q2
**Answer: (a) D**

**Why.** B is the sister of C, so B and C share a parent; A is B's father, so A is C's father too. E is A's son and D is E's mother, so D is A's wife. With one couple in a family of six (A, D and their children B, C, E, F), D is C's mother.

**Concept: draw a family tree.** Put each person in a box, connect parents to children, and mark gender as you learn it. Puzzles like this assume a single married couple unless they say otherwise.

@@ maq-q10
**Answer: (d) none of these** (he is her brother)

**Why.** Anjali's sister's brother is Anjali's brother (or Anjali's own sibling). His father is Anjali's father. "The only son of my father" is Anjali's brother.

**Concept: collapse the chain from the inside out.** Replace the innermost phrase first ("my sister's brother" → my brother), then the next ("his father" → my father), and so on.

@@ sie-allen
**Answer: (c) son-in-law**

**Why.** Bob's only brother has a daughter; her daughter's father is the daughter's husband. So Allen is married to Bob's brother's daughter: Allen is the brother's son-in-law.

**Concept: relation chains.** "Father of X's daughter" is X's husband (or X himself if X is male). Work through the chain one link at a time.

@@ ti-calendar
**Answer: (a) Monday**

**Why.** From 21 Aug 1995 to 21 Aug 1998 is 3 years: 365 + 366 (1996 is a leap year and 29 Feb 1996 falls in between) + 365 = 1096 days. 1096 = 156 × 7 + 4, so 21 Aug 1998 is Monday + 4 = Friday. Three days later, 24 Aug 1998, is Monday.

**Concept: odd days.** An ordinary year shifts the weekday by 1 (365 = 52 weeks + 1 day), a leap year by 2. Count the year-shifts between the dates, add the extra days, and reduce mod 7.

@@ acc-idc-code
**Answers: (36) `$$$*$` (37) `$*****$**` (38) the third option (39) `$*$** - $$` (40) the first option (it has a printed typo)**

**Why.** Read `*` as 0 and `$` as 1: these are binary numbers.
- (36) 11 × 17/10 + 2 × 5 + 3/10 = 18.7 + 10 + 0.3 = 29 = 11101₂.
- (37) 260 = 256 + 4 = 100000100₂.
- (38) 60/17 = 180/51; 180 = 10110100₂ and 51 = 110011₂.
- (39) `$***$` = 10001₂ = 17 = 20 − 3 = 10100₂ − 11₂.
- (40) 30² = 900 = 27² + 171; the first option is (11011)^(10) + 10101101, i.e. 729 + 173, two off (171 would be 10101011), so it has a typo but is the only one built on 27².

**Concept: binary numbers.** Each place is worth double the place to its right: 1, 2, 4, 8, 16, ... To convert a decimal number, subtract the largest power of 2 that fits, mark 1 there, and repeat. Example: 29 = 16 + 8 + 4 + 1 → 11101.

@@ acc-pap-code
**Answers: (33) `$**$*$$**$` (34) `$*` (35) `$$$***$$*` (36) 676 (37) `$$$$**$*`**

**Why.**
- (33) 601 = 512 + 64 + 16 + 8 + 1 = 1001011001₂.
- (34) LCM(18, 20, 36) = 180; 180/90 = 2 = 10₂.
- (35) 454 = 256 + 128 + 64 + 4 + 2 = 111000110₂.
- (36) `$$*$*` = 26, `$*` = 2, so 26² = 676.
- (37) 3 × average(64, 74, 104) = the sum = 242 = 11110010₂.

**Concept: binary conversion.** Same method as above. Also note "3 × average of 3 numbers = their sum", which saves a division.

@@ axx-coding
**Answer: (a) BKPGAV**

**Why.** REASON → PGYUMP: R−2 = P, E+2 = G, A−2 = Y (wrapping back from A), S+2 = U, O−2 = M, N+2 = P. The shifts alternate −2, +2. Apply to DIRECT: D−2 = B, I+2 = K, R−2 = P, E+2 = G, C−2 = A, T+2 = V.

**Concept: letter-shift codes.** Write the alphabet positions (A = 1 ... Z = 26) of the word and its code, find the shift for each letter, and look for a pattern (constant, alternating, increasing). Shifts wrap around: A − 2 = Y.

@@ jsw-matrix
**Answer: (d) 00, 66, 44, 88, 23**

**Why.** A code is row digit then column digit. Check (d) letter by letter: 00 is row 0, column 0 of matrix 1 = P; 66 is row 6, column 6 of matrix 2 = A; 44 = R; 88 = T; 23 = Y. Every other option fails early (e.g. (a)'s 40 is Y, (b)'s 12 is R, (c)'s 31 is P, not A).

**Concept: check options, don't build the code.** Each letter appears many times in the matrices, so many codes are possible. It is faster to test each option's numbers against the grid and reject an option at its first wrong letter.

@@ ti-encoding
**Answer: (a) IJKR**

**Why.** Annual → ESTKIU and Quarter → UZGYJNJ: the i-th letter is shifted forward by i + 3 (A+4 = E, N+5 = S, N+6 = T, ...). For WEEK: E+5 = J, E+6 = K, K+7 = R. W+4 runs past Z, and the examples do not wrap consistently: in Quarter, T+8 (position 28) becomes J, which would put position 27 at I; in Annual, U+7 (also 28) becomes K. Following Quarter gives I. Only IJKR has J, K, R in places 2–4, so it is the answer either way.

**Concept: increasing shift codes.** When the shift grows with position, write the shifts out (4, 5, 6, 7, ...). Use the letters that do not wrap to pick the option, since the examples here are not fully consistent at the wrap-around.

@@ acc-prev-assume
**Answers: (31) A (32) D (33) D (34) B**

**Why.**
- (31) Recommending school at about 5 assumes the child is ready to learn then (I). It does not assume schools refuse children over six (II).
- (32) A duty cut lowers import prices; neither "domestic prices may rise" nor "domestic makers may oppose" is something the decision must assume.
- (33) Limiting tickets because demand is high does not assume reluctance to sell or that nobody wants more than five.
- (34) Raising freight to avoid a loss assumes the extra revenue will help cover the deficit (II). (I is arguably implicit too, but the key takes B.)

**Concept: implicit assumption.** An assumption is something the speaker must take for granted for the statement to make sense. Test: if the assumption were false, would the statement become pointless? If yes, it is implicit. A possible consequence of the statement is not an assumption.

@@ fk-assumption
**Answer: (c) neither**

**Why.** "It is better to finish school by 18" is a general recommendation. It does not require that colleges reject over-18s (I), nor that the child must join college at exactly 18 (II). Both are extreme readings.

**Concept: watch for absolute words.** Assumptions with "must", "only", "do not consider" are usually too strong for a mild statement like "it is better to".

@@ fk-tourist
**Answer: (d) the government generally protects foreign tourists**

**Why.** The administration acted immediately against the attackers, which suggests protection of tourists. Nothing says he was drunk (a), that language caused it (b), or that villagers dislike foreigners in general (c).

**Concept: an inference must follow from the text.** Pick the option that the facts support most directly; reject anything that adds new facts or generalises from one incident.

@@ protium-logic
**Answer: (b)**

**Why.** The statement is "scolds → (hide or complain)". Its contrapositive, "not hide and not complain → not scolded", is logically equivalent, and that is (b). (a) is the converse and (c) the inverse; neither follows.

**Concept: contrapositive.** For "if P then Q":
- Contrapositive "if not Q then not P" is always equivalent.
- Converse "if Q then P" and inverse "if not P then not Q" are not.
When Q is "A or B", "not Q" is "not A and not B" (De Morgan's law).

@@ sig-courses
**Answer: (a) only 1 follows**

**Why.** Extra tutoring addresses the cause (weak understanding). Stopping maths altogether gives up instead of fixing anything, and is impractical.

**Concept: course of action.** A valid action should solve or reduce the problem and be practical. Reject extreme, unrelated or defeatist actions.

@@ ti-drip
**Answer: (a)** (the best-supported reading)

**Why.** The owner says drip irrigation is unnecessary because sprinklers exist. (a) answers exactly that: even with sprinklers, underwatering can still shorten the lawns' life, so the backup has value. (d) just repeats the gardener's own claim; (b) and (c) are damage drip irrigation cannot prevent.

**Concept: strengthen an argument by answering the objection.** The best support closes the gap the other side points to. Restating the conclusion adds nothing.

@@ ti-elevators
**Answer: (4) none of these**

**Why.** All elevators stop at floors 1 and 7, which are odd. So E1 (an "even" elevator) can still go from the ground floor up to 7 and you can reach odd floors without a change: (3) is not a must. (1) and (2) are only true for a direct ride and are not forced either.

**Concept: "must be true".** A statement must be true only if no arrangement consistent with the facts breaks it. One counterexample (E1 stopping at 7) is enough to reject it.

@@ ti-energy
**Answer: (d) whether the consumers had tasted other brands**

**Why.** "Best in the market" is a comparison with other drinks, but the study only tested this one brand. Without comparing, the conclusion does not follow.

**Concept: find the gap between evidence and conclusion.** The evidence (80% felt it helped) supports "it helps", not "it is the best". A flaw question asks what the argument ignores; here, a comparison group.

@@ ti-mud
**Answer: (d) none**

**Why.** "Biking from A to B → mud on sleeves." Mud on Keith's sleeves (a) does not prove he made that trip: mud could come from anywhere. Knowing he travelled from A (b) or to B (c) alone does not complete the trip either.

**Concept: affirming the consequent is a fallacy.** From "if P then Q" and "Q", you cannot conclude P. Only "P" gives "Q" (modus ponens), and "not Q" gives "not P".

@@ ti-platform
**Answer: (d) very few users leave because of the missing amenities**

**Why.** If hardly anyone leaves over the amenities, improving them gains the platform almost nothing, even if users would pay a bit more. That explains why a profit-seeking platform does nothing.

**Concept: resolve the paradox.** The best explanation makes both facts true at once (users would pay more, yet the company does not act). Look for the option that removes the company's incentive.

@@ wf-cr1
**Answer: (b) No**

**Why.** Revenue per applicant is constant, so revenue is proportional to applicants. 30,000 applicants is fewer than 2009 (35k), 2012 (40k) and 2013 (35k), so revenue would be lower than those years. Holding costs to $5000 changes profit, not revenue.

**Concept: revenue vs profit.** Revenue is money coming in; profit is revenue minus costs. A statement about revenue cannot be helped by cutting costs.

@@ wf-cr2
**Answer: (a) Yes** (as the test intends)

**Why.** Every year-on-year change moves the two series in opposite directions: 2009→10 applicants down, cost up; 2010→11 up, down; 2011→12 up, down; 2012→13 down, up.

**Concept: negative correlation in a trend.** When one series rises each time the other falls, they move inversely. (With only five points this is a trend, not a law, but the data never contradicts it.)

@@ wf-cr3
**Answer: (b) could be true**

**Why.** We know "church visit → eats at the bakery", and that he ate at the bakery in June. That does not prove he visited the church: he might have gone to the bakery alone. Nothing rules it out either.

**Concept: one-way implications.** "If P then Q" plus "Q" leaves P possible but not certain. Classify as "definitely true" only if it follows, "cannot be true" only if it contradicts the facts.

@@ wf-cr4
**Answer: (c) the severe penalties serve to deter actors from delaying the movie**

**Why.** The passage lists finishing on time as an obligation and lists heavy penalties for breaches; deterrence is the inference closest to the text. (a) adds "reputation" (not mentioned). (b) and (e) go beyond the text. (d) is contradicted: the director's consent is part of the obligations.

**Concept: inference stays inside the text.** Choose the option that needs the fewest outside assumptions. Words not in the passage ("reputation", "mostly") are red flags.

@@ wf-cr5
**Answer: (a) individual LSAT scores have been fairly consistent across evaluations**

**Why.** The argument assumes a person's score stays the same over time. (a) supports exactly that. (b) helps a little; (c) weakens it (format changed); (d) is about a different test.

**Concept: strengthen by supporting the hidden assumption.** Find the unstated link between evidence and conclusion (past score predicts future score) and pick the option that makes that link more believable.

@@ wf-cr6
**Answer: (a) 150 words of introduction are pasted from an existing email**

**Why.** Worst case today: email 525 words at 35 wpm = 15 min; equations 5 × 4 = 20 at 2 per min = 10 min; total 25 > 21. With 150 words pasted, only 375 are typed: 10.7 + 10 = 20.7 ≤ 21. A 450-word limit (c) still gives 12.9 + 10 = 22.9. (b) and (d) give no guaranteed bound.

**Concept: guarantee means plan for the worst case.** To commit to a deadline you must bound the maximum time, using the upper limits (525 words, 4 equations per section), not the averages.

@@ wf-cr7
**Answer: (a) Yes**

**Why.** Calling freedom of expression "one of the main purposes" of democracy only makes sense if the author values it highly.

**Concept: value assumptions.** When someone names something as a key goal, they implicitly regard it as worth having.

@@ ion-q5
**Answer: (b) 1**

**Why.** Two four-digit numbers add to less than 20,000, so a five-digit sum must start with 1: M = 1. (The full solution is 9567 + 1085 = 10652.)

**Concept: leading-digit carry in cryptarithms.** When a sum has one more digit than its longest addend, that extra leading digit is the final carry, and a carry from adding two numbers is at most 1.

@@ jsw-energy
**Answer: (a) 17**

**Why.** A five-digit plus a four-digit number gives a six-digit result, so the sum is at least 100,000: E = 1 and POINT ≥ 90,000, so P = 9. Searching the remaining digits gives one solution: 98504 + 3168 = 101672. E + N + E + R + G + Y = 1 + 0 + 1 + 6 + 7 + 2 = 17.

**Concept: start cryptarithms from the leading columns.** The size of the result fixes the first digits (carries are 0 or 1). Then work column by column, tracking carries, and use "all letters are different" to prune.

@@ jsw-late
**Answer: (c) 4386**

**Why.** A three-digit plus a three-digit sum has four digits, so F = 1. Units: P + F = 5 + 1 = 6 = E (no carry). Tens: A + F = 3 + 1 = 4 = L. So L = 4, A = 3, T = 8, E = 6: LATE = 4386. (Two full solutions exist, 835 + 211 and 835 + 911, but both give L = 4, E = 6.)

**Concept: you only need the letters asked.** Fill columns until every letter in the target word is known; the rest can stay ambiguous.

@@ jsw-mac
**Answer: (b) 31**

**Why.** MAC + MAAR = JOCKO: a three-digit plus a four-digit number giving five digits forces J = 1, then MAAR ≥ 9000 so M = 9 and O = 0. The unique solution is 932 + 9338 = 10270 (A = 3, C = 2, R = 8, K = 7). 3A + 2M + 2C = 9 + 18 + 4 = 31.

**Concept: carries pin down leading letters.** A five-digit sum from a four-digit addend means a carry out of the thousands column, which needs the addend to start with 9 (with a carry in). Then solve the remaining columns.
