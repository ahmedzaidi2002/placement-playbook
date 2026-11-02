@@ fk-hill-kollur
**Answer: (a) Swift**

**Why.** The clues have one solution (see the Nissan question): David and Jansi went to Kollur, and clue II says Jansi travelled in the Swift.

**Concept: grid puzzles.** Make a table with one row per man and columns for wife, place and car. Fill direct facts first, then use "not" clues to eliminate, and repeat until each cell has one value.

@@ fk-hill-nissan
**Answer: (b) Vijendra**

**Why.** Fill the grid from the direct facts:
- Raj → Agumbe; Murali → Virajpet; Shyam's wife is Asha and they did not go to Kollur.
- The Skoda couple went to Sagara; Mamatha went to Kodachadri; Ramya went neither to Kollur nor Virajpet.
- Jansi rode the Swift, but clue II does not say she is Murali's wife (that reading makes the puzzle impossible).
Working through the eliminations gives one solution: Raj–Ramya, Agumbe, Fiat; Shyam–Asha, Sagara, Skoda; Murali–Sindhu, Virajpet, Hyundai; Vijendra–Mamatha, Kodachadri, Nissan; David–Jansi, Kollur, Swift.

**Concept: elimination grids.** In matching puzzles each person gets exactly one item from each category. Every "X is not Y" removes one cell; when a row or column has one cell left, it is forced. Be careful not to read extra facts into a clue.

@@ fk-hill-pair
**Answer: (c) Vijendra – Mamatha**

**Why.** From the unique solution above.

**Concept: answer from the full grid.** Once the grid is complete, all follow-up questions are look-ups.

@@ go-3
**Answer: (a) bus**

**Why.**
1. Mike travelled by bus, so he is not from Memphis (that couple used the ship), not from Dallas (clue 4) and not from Miami (the Maceys are from Miami): Mike is from Washington.
2. Kinsley departed from Washington (clue 5), so she is Mike's wife, and they are not the Makins.
3. Ruby is an Ainsworth but not Mike's wife; Parker is not Paula's husband, so Parker married Ruby, and David Macey married Paula.
4. Richard and Rebecca are left as the Makins, so Mike and Kinsley are the Salmons, who travelled by bus.

**Concept: start from the most constrained person.** Mike has a fixed transport and several "not" clues, so his city is forced first, and everything else chains from there.

@@ go-8
**Answer: (b) 1144, 16, 1683**

**Why.**
1. All boxes: 8 × 2 × 1 × 13 × 4 × 11 = 9152 (ends in 2). Dropping 8 gives 1144 (ends in 4), the largest product ending in 4.
2. Powers of 2 end in 2, 4, 8, 6, repeating. 2⁴ = 16 ends in 6; 2⁵ = 32 does not. So 16.
3. Using 5 with any even number ends in 0, and 5 with only odd numbers ends in 5, so leave 5 out. 9 × 11 × 17 = 1683 ends in 3 and is the largest such product.

**Concept: last digits only depend on last digits.** The units digit of a product is the units digit of the product of the units digits. Powers cycle with a short period (2 → 4 → 8 → 6). Multiplying by 5 and an even number always ends in 0.

@@ ion-q3
**Answer: (b) S is the engineer**

**Why.**
1. The brakeman lives halfway between Noida and Dehradun, and his nearest neighbour is a passenger. Mr. R lives in Dehradun, and the passenger named like the brakeman lives in Noida, so the neighbour is neither. The neighbour earns 3 × the brakeman's salary; Mr. J earns 4,00,000, not divisible by 3, so the neighbour is not Mr. J. So the neighbour is Mr. S, and the passenger in Noida is Mr. J.
2. The passenger in Noida has the brakeman's name, so J is the brakeman.
3. S beats the fireman, so S is not the fireman: S is the engineer (and R the fireman).

**Concept: eliminate with each clue.** This is Dudeney's classic puzzle. Combine clues that talk about the same person (the neighbour) and rule out candidates using numbers (divisibility by 3) and places.

@@ jsw-robbery
**Answer: (a) Tom**

**Why.** Try each suspect as the robber and count true statements.
- Tom guilty: Tom's "I am innocent" false; Martin's true; Garry's ("Martin is guilty") false → exactly one true. ✓
- Martin guilty: Tom true, Martin false, Garry true → two true. ✗
- Garry guilty: Tom true, Martin true, Garry false → two true. ✗

**Concept: case testing for truth-teller puzzles.** Assume each possibility in turn and check it against the condition ("only one statement is true"). Exactly one case should survive.

@@ kla-d-01
**Answer: (c) Banta**

**Why.** Each break turns one piece into two, so the number of pieces grows by exactly 1 per move. From 1 piece to 15 × 20 = 300 single squares needs 299 moves, no matter how you break. Santa makes moves 1, 3, 5, ..., 299 (the last one), so Banta is the first who cannot move.

**Concept: invariants.** Look for a quantity that changes by a fixed amount each move (here, pieces + 1). Then the total number of moves is fixed, and parity decides who moves last.

@@ kla-d-08
**Answer: (c) White**

**Why.** Watch the number of white balls: the black-black and black-white cases leave it unchanged; the white-white case removes 2. So it changes only by 0 or −2, and its parity (odd/even) never changes. It starts at 25, odd, so it can never become 0. When one ball is left, it must be the white one.

**Concept: parity invariant.** If a quantity always changes by an even amount, it stays odd or even forever. This decides the final state without simulating any draws.

@@ kla-d-12
**Answer: (a) 17 bicycles with 17 spokes each** (289 spokes)

**Why.** With b ≥ 2 identical bicycles of s spokes each (s ≥ 2: two wheels, at least one spoke each), the total is S = b × s. Knowing S lets you find b only if S can be written as b × s in exactly one way with both ≥ 2. That happens only when S is the square of a prime: p² = p × p and nothing else. Between 200 and 300 the only such number is 289 = 17².

**Concept: unique factorisation as information.** "I could work it out if I knew S" tells you S has a special property. A number has exactly one factor pair (other than 1 × itself) only if it is a prime squared. (The last option is a stray from another question.)

@@ kla-d-21
**Answer: (c) 100%**

**Why.** Imagine both trips happening on the same day: one car leaves Delhi at 8 am for Jaipur, another leaves Jaipur at 8 am for Delhi, on the same road, both finishing at noon. They must pass each other somewhere. At that moment they are at the same point at the same time of day, so that point exists on every pair of trips.

**Concept: the intermediate value theorem.** Let d(t) = (position on day 1) − (position on day 2). It starts negative at 8 am (Delhi vs Jaipur) and ends positive at noon, and changes continuously, so it is zero at some moment. Speeds and breaks do not matter.

@@ kla-d-23
**Answer: (a) 7**

**Why.**
1. Races 1–5: five heats of five. The bottom two of each heat cannot be top 3.
2. Race 6: the five heat winners. Its winner is the fastest overall. Horses from heats whose winner came 4th or 5th are out.
3. Remaining candidates for 2nd and 3rd: 2nd and 3rd of race 6, 2nd and 3rd from the overall winner's heat, and 2nd from the heat of race 6's runner-up. That is 5 horses: race 7 decides.

**Concept: eliminate by "who can't be in the top k".** A horse beaten by k horses that are known to be faster cannot be in the top k. Tracking who beat whom shrinks the field to one final race.

@@ maq-q11
**Answer: (b) burn one rope from both ends and the other from one end**

**Why.** Rope 1, lit at both ends, burns out in 30 minutes, however unevenly. At that moment rope 2 (lit at one end) has 30 minutes of burning left; light its other end, and it finishes in 15 minutes. Total 30 + 15 = 45.

**Concept: lighting both ends halves the time.** Uneven burning means you cannot measure by length, only by time. Two flames meeting somewhere still use up the rope's total burn time twice as fast.

@@ or-euler
**Answer: (a) E**

**Why.** A route using every road exactly once is an Euler path. It exists only if 0 or 2 cities have an odd number of roads, and then it must start at one odd city and end at the other. After adding C–G and H–F, the degrees are A 2, B 3, C 4, D 2, E 3, F 4, G 4, H 4. Starting at B (odd), the journey ends at E, the other odd city. (The photo's G has even degree and cannot be an end.)

**Concept: Euler paths.** Every time you pass through a city you use one road in and one out, an even number. Only the start and end can have odd degree. So count each city's roads; the odd ones are the endpoints.

@@ or-sports
**Answer: (a) Matthew**

**Why.** Peter and Sebastian take China and the UK; Matthew is from Russia; Jack is not from India or China, so Jack is from South Korea and Albert from India. India's colour is brown (Albert). Jack is red; Peter and Sebastian have yellow and green. The only colour left, black, goes to Matthew. (The photo ticks Albert, who is brown.)

**Concept: fill the most constrained categories first.** Countries were nearly forced by clues 4, 5 and 1, and each country clue then fixed a colour. The asked item often falls out before the whole grid is complete.

@@ ti-butcher
**Answer: (b) 1**

**Why.** With weights 1, 2, 4, ..., 64 on one pan, every whole number from 1 to 1 + 2 + ... + 64 = 127 can be made (each weight is either used or not, like binary digits). Only customer 128 cannot be served.

**Concept: binary representation.** Every whole number has exactly one binary form, a sum of distinct powers of 2. Weights 2⁰ to 2⁶ cover 0 to 2⁷ − 1 = 127.

@@ ti-chess
**Answer: (b) T2**

**Why.** Try each team as the truth-teller and check consistency. Only one assignment works: T1 prefers Sunday and always lies, T2 prefers Tuesday and tells the truth, T3 prefers Friday and alternates. T2's statements (Friday for T3, Sunday for T1) are then both true.

**Concept: truth-teller / liar / alternator.** A truth-teller's statements are all true, a liar's all false, and an alternator's two statements have opposite truth values. Assume a type for one speaker, derive the facts, and check whether the others' statements fit their types.

@@ ti-profession
**Answer: Lawyer**

**Why.** The family clues (not reproduced in the source) leave exactly one profession for E after the others are placed.

**Concept: elimination grids.** List people and professions in a table and cross out every pairing a clue forbids until each row has one choice left.

@@ ti-shoe
**Answer: Yes, W1 is guilty**

**Why.** Someone among W1, W2, W3 is guilty. W2 cannot climb high walls, which the theft needed, so W2 is out. If W3 is guilty, W1 was with him (W3 never acts without W1). Either way W1 is guilty. (The IISc candidate's "insufficient" is wrong.)

**Concept: proof by cases.** If every possible case leads to the same conclusion, that conclusion is certain.

@@ go-5
**Answer: (d) 1**

**Why.** In the Narcos column the known ranks are 4, 5, 9, 2, 6, 3, 7, 10, so D and H share the remaining ranks 1 and 8. H already gave rank 1 (to Mind Hunter), and a person uses each rank only once, so H gave Narcos 8 and D gave it 1.

**Concept: Latin-square reasoning.** When each row and each column must use each value once, a missing cell is whatever value is absent from both its row and its column.

@@ sie-rank
**Answer: (b) 22nd**

**Why.** Total = 12 + 20 − 1 = 31. Max is two places above Smith: 10th from the top. From the bottom: 31 − 10 + 1 = 22nd.

**Concept: rank from both ends.** Total = (rank from top) + (rank from bottom) − 1, because the person is counted twice. "Higher" means closer to the top.

@@ ti-athletes
**Answer: (a) 24th**

**Why.** A1 is 13th from the left and 6 places to the right of A2, so A2 is 13 − 6 = 7th from the left. From the right: 30 − 7 + 1 = 24th.

**Concept: positions in a row.** Convert everything to one end first. Left + right position = total + 1.

@@ ti-bella
**Answer: (c) 48**

**Why.** To use as few books as possible, let B1 and B2 overlap their counts: put B2 to the left of B1 with one book (B3) between them. B1 is 24th from the left, so B2 is 22nd from the left. B2 is 27th from the right: total = 22 + 27 − 1 = 48.

**Concept: minimum and maximum arrangements.** "Minimum total" means the counts from each end should overlap as much as possible, so place the two items in the order that makes them share books.

@@ ti-coffee
**Answer: (a) 6** is the intended key, but the data are inconsistent.

**Why.** The key subtracts the three groups: 40 − 8 (I last) − 16 (I before H) − 10 (I before C) = 6. That treats overlapping groups as separate. Done properly: people who rank I first are counted in both "I before H" and "I before C", and those with I in the middle in exactly one of them. So 2 × first + middle = 16 + 10 = 26, while first + middle = 40 − 8 = 32. That gives first = −6, impossible: the numbers in the question cannot all be right.

**Concept: overlapping groups.** Before subtracting groups from a total, check whether they overlap. If they do, use inclusion–exclusion (or count by cases as above).

@@ ti-meal-prep
**Answer: (c) only 3**

**Why.** T2 = 3 × T5 > T5 > T1 = 2 × T4 > T4 = T3. So T2 is the most effective (3 follows). T5 is not the most (1 fails), and T4 ties with T3 as least, not T5 (2 fails).

**Concept: build a chain.** Turn each comparison into an inequality and link them into one ordering from greatest to least; then read off the conclusions.

@@ ti-meal-prep-2
**Answer: conclusions 1, 2 and 3 all follow and 4 does not, so no option is exact** (the key writes "1 & 2 or 1 & 3").

**Why.** Same chain: T2 > T5 > T1 > T4. So T5 ≥ T1 (1), T2 > T5 (2) and T2 > T1 (3) all hold; T4 > T1 (4) is false.

**Concept: check every conclusion against the chain.** An option is correct only if it lists exactly the conclusions that follow.

@@ ti-parking
**Answer: (b) 54**

**Why.** V3 is 19th from the left and 11 places to the right of V1, so V1 is 8th from the left. V2 is 20 places to the right of V1: 28th from the left. V2 is 27th from the right: total = 28 + 27 − 1 = 54.

**Concept: anchor everything to one end.** Convert relative positions ("n to the right of") into positions from the left, then use left + right − 1 = total.

@@ ti-sister
**Answer: (b) only 2**

**Why.** Given: S > P and R > T. Add (2) S > R: then S > R > T and S > P, so S is the oldest. (1) R > P does not compare R and S. (3) T youngest does not decide between S and R.

**Concept: data sufficiency with orderings.** The oldest is the person nobody is above. Check whether each statement leaves exactly one such person.

@@ epam-q9
**Answer: (d) H, G, L, J, K, I, M**

**Why.** Exactly three people between H and K: only (d) has H in seat 1 and K in seat 5. It also fits the rest: G in seat 2 (not an end), J (4) left of M (7) and not next to it, L (3) not next to I (6).

**Concept: test options against the strictest clue.** When the options are full arrangements, check the most restrictive clue first; it usually eliminates all but one.

@@ jsw-parking
**Answers: Q1: 1, 3, 4, 6, 9. Q2: 5.**

**Why.**
- One odd car per facing pair (no odd opposite odd) and no two adjacent evens force one row to hold evens in columns 1, 3, 5 and the other in columns 2, 4.
- Pink 8 is at a right end; car 6 is second from the right, so 6 and 8 are in different rows. Blue 5 is with 8 (not with 3 and 6), and 4 is with 6 (not with pink 8).
- Black is opposite car 1, yellow opposite car 2, green is odd and with 5, and so on. Every arrangement that satisfies all ten clues has rows {1, 3, 4, 6, 9} and {2, 5, 7, 8, 10}, and when green is next to grey, car 5 is opposite car 4.

**Concept: two facing rows.** Draw two rows of five boxes with columns linking opposite cars. Remember that "left" and "right" flip for the facing row. Parity clues (odd/even) often fix the pattern of the rows before any colour is placed.

@@ kla-d-18
**Answer: (b) T**

**Why.** K and X are both 3 floors from Y, with X below K, so X = Y − 3 and K = Y + 3. Y is even and floors run 1–8, so Y = 4: X on 1, K on 7. T and H are on even floors with T above H; the free even floors are 2 and 8, so H = 2, T = 8. M is not above Y, so M = 3. O just above L fills 5 and 6. Order from the bottom: X, H, M, Y, L, O, K, T. (The photo ticks K, from working that put T on floor 7, which is odd.)

**Concept: "two persons between" means a gap of 3 floors.** Floors that have n people between them differ by n + 1. Use the parity and "above/below" clues to pick between the two possible directions.

@@ maq-q12
**Answer: (a) BCD**

**Why.** F sits with only B, so {F, B} is a bench and, since F is a boy, B is its girl. C cannot sit with A, D or E, so C joins G on bench III. That leaves {A, D, E} on bench I. A ("his") and E ("brother") are boys, so D is the girl there. Girls: B, C, D.

**Concept: grouping puzzles.** Start with clues that fix a whole group ("F sits with only B"), then place people with "not with" restrictions, then use gender words (his, brother) to identify the remaining girls.

@@ or-standing
**Answer: (a) Peter**

**Why.** Tyson is in seat 1 and Richard in seat 4. Steve and Peter are both next to Richard, so they take seats 3 and 5. Peter must be next to Quinn, and seat 5 has no free neighbour, so Peter is in seat 3, Steve in 5 and Quinn in 2. Check: Steve (5) is not next to Tyson (1), and Peter is right of Quinn and Tyson. Order: Tyson, Quinn, Peter, Richard, Steve. The middle seat holds Peter.

**Concept: fix the absolute positions first.** Clues with "leftmost" or "second from the right" place people directly; then use "next to" clues to fill the gaps.

@@ qc-n-seat-1
**Answer: (d) Anvesha**

**Why.** Six seats. Sonu sits just left of Kapil, so Kapil is first to Sonu's right. Jim is fourth to Sonu's right. Some people sit between Monu and Akash but Anvesha is not one of them, so Monu and Akash sit on either side of Jim, and Anvesha takes the remaining seat, second to Sonu's right. Going round to Sonu's left: Sonu, Monu/Akash, Jim, Akash/Monu, Anvesha, Kapil. Swapping Monu and Akash does not change the answer. The photo ticks Kapil, who is only first to the right.

**Concept: circular seating facing the centre.** For someone facing the centre, their right is anticlockwise and their left is clockwise (seen from above). Fix one person, place others relative to them, and keep track of both possible placements when a clue allows a swap.

@@ qc-n-seat-2
**Answer: (c) Jim**

**Why.** In the arrangement Sonu, Monu/Akash, Jim, Akash/Monu, Anvesha, Kapil, Jim is the one person between Monu and Akash ("some people sit between them" and Anvesha is not that person).

**Concept: re-use the solved circle.** Follow-up questions are look-ups once the circle is fixed.

@@ qc-n-seat-3
**Answer: (a) either Akash or Monu**

**Why.** Two seats to Kapil's right lands on the seat next to Anvesha on the far side, which Monu and Akash can swap between them.

**Concept: answer with the ambiguity.** If a clue leaves two people interchangeable, an option naming "either" of them is the correct one.

@@ qc-n-seat-4
**Answer: (a) Jim**

**Why.** With six seats, fourth to the right equals second to the left (4 + 2 = 6). Jim is fourth to Sonu's right, so he is second to Sonu's left.

**Concept: positions around a circle wrap.** In a circle of n, k places to the right = n − k places to the left.

@@ qc-n-seat-5
**Answer: (a) Kapil**

**Why.** Opposite in a circle of six means three seats away. From Jim, three seats in either direction is Kapil.

**Concept: opposite seats.** In a circle of n (n even), the person opposite is n/2 seats away.

@@ qc60-08
**Answer: (c) 5**

**Why.** The clues (not transcribed in the source) give the arrangement, Post 1 to 7: Aurora, Beacon, Glow, Flare, Corona, Dusk, Ember. Ember is on 7 and Beacon on 2: |7 − 2| = 5.

**Concept: linear arrangements.** Place items with absolute clues first, then relative ones; once the order is fixed, each follow-up is a look-up.

@@ qc60-09
**Answer: (c) Glow**

**Why.** From the arrangement Aurora (1), Beacon (2), Glow (3), Flare (4), Corona (5), Dusk (6), Ember (7), Post 3 holds Glow.

**Concept: look-up from the solved order.**

@@ qc60-10
**Answer: (d) 2**

**Why.** Alphabetical: Aurora, Beacon, Corona, Dusk, Ember, Flare, Glow. Actual: Aurora, Beacon, Glow, Flare, Corona, Dusk, Ember. Only Aurora (1) and Beacon (2) are in the same position.

**Concept: compare position by position.** Write both orders one above the other and count matching columns.

@@ qc60-11
**Answer: (b) Post 6**

**Why.** From the arrangement, Dusk is on Post 6. (Post 7 was marked in the exam, which is Ember's post.)

**Concept: look-up from the solved order.**

@@ qc60-12
**Answer: (b) 9**

**Why.** Flare is on Post 4 and Corona on Post 5: 4 + 5 = 9.

**Concept: look-up from the solved order.**

@@ sie-girls
**Answer: (d) S**

**Why.** Seats 1–5 from the left: U is second from the right, seat 4. U is not next to S or R, so seats 3 and 5 hold Q and T, which puts one person (U) between Q and T. So one person sits between U and R as well: R is in seat 2. S is left with seat 1, the left end.

**Concept: equal-gap clues.** "As many people between U and R as between Q and T" links two pairs; fix the one you can, then apply the same gap to the other.

@@ ti-five-students
**Answer: (b) only (2) is incorrect**

**Why.** E is at the left end, B is second from the right (seat 4). A is next to B but not to E, so A is in seat 5 (seat 3 would also be possible, but C must be next to B and D, and to the right of D and E). The only order is E D C B A. So B is between C and A (1 true) and A is not between C and B (2 false).

**Concept: place fixed seats, then neighbours.** End seats and "second from the right" are absolute; "next to" clues then fill the rest.

@@ ti-hexagon
**Answer: (b) Jill**

**Why.** Seat the six around the hexagon and apply the clues: Adam is second to the left of Ron, Bob is second to the left of Jill, and Abe sits between Pepa and Jill. All arrangements that satisfy these (under either reading of "left") put Jill opposite Adam. The NIT candidate's Pepa is wrong.

**Concept: circular seating.** Fix one person, then place others using "second to the left" (two seats away) and "neighbour" clues. Opposite seats in a hexagon are three apart.

@@ ti-staff
**Answer: neither conclusion is determined** (both can be true or false depending on the arrangement).

**Why.** Enumerating all arrangements that satisfy the clues shows every combination of truth values for (1) and (2) is possible, so the question as transcribed has no definite answer.

**Concept: "is incorrect" needs certainty.** A conclusion is definitely incorrect only if no valid arrangement makes it true. If some arrangements make it true and others false, it is undetermined.

@@ acc-idc-criteria
**Answers: (52) rejected (53) not considered (54) interviewed by HR (55) data insufficient**

**Why.**
- (52) Shakuntala has only 3 years' experience (needs 4) and is 29 (needs over 30): fails, no exception applies.
- (53) Rajiv, born Dec 1974, is 28 on 1 July 2003, and has no call-centre experience: fails.
- (54) Soma meets the degree, experience and age conditions (30 in Dec 2002, so over 30 on 1 July 2003); only international exposure is missing, which sends her to the HR manager.
- (55) Salina's age is not given, so we cannot decide.

**Concept: rule tables.** Check each condition for each candidate. A failure in a condition with an exception goes to the named interviewer; any other failure rejects; missing information means "data insufficient". Compute ages on the stated date, not today.

@@ acc-prev-team
**Answers: (51) KOPQR (52) GKPQ (53) JKMNOR (54) GIRQ (55) MORG**

**Why (key rules):** M with J; O not with N; I not with J; N with H; P with Q; K with R.
- (53) JKMNOR has N and O together, which is forbidden.
- (51) With I, J is out, so M is out. Two girls including I: the second must be K (bringing R) or G or H; K O P Q R works (no J, no N).
- (52), (54), (55) are checked the same way against every pairing rule.

**Concept: pairing constraints.** Turn rules into "must go together" pairs and "cannot go together" pairs. Choosing one member of a "must" pair forces the other; check every option against all rules.

@@ epam-q12
**Answer: (a) P-R-U**

**Why.** If P is chosen, T must be too. P-R-U has P without T (and T could not join anyway, since U cannot serve with T). The other teams satisfy all rules.

**Concept: conditional rules.** "If P then T" is broken only when P is in and T is out. Check each option for exactly that pattern.

@@ epam-q15
**Answer: (a) B, D, A, C**

**Why.** B first → D second ✓. D after B ✓. A third (not first or last) ✓. C last → A just before it ✓. (b) has A first, (c) has A last, (d) has B first without D second.

**Concept: check each option against each rule.** For "if X then Y" rules, an option fails only when X happens without Y.

@@ or-ingredients
**Answer: (d) 5** (under the assumed question, "minimum number of ingredients used")

**Why.** Apricots and eggs are used (4). Apricots → bacon and cake (2). By the contrapositive of (3), apricots used → donuts used. Nothing else is forced. Minimum: apricots, eggs, bacon, cake, donuts = 5.

**Concept: contrapositive.** "If not donuts then not apricots" is the same as "if apricots then donuts". Apply every rule forward from the known facts and count what is forced.

@@ axx-group
**Answer: (c) 735**

**Why.** In 195, 456 and 267 the digits add to 15. 735: 7 + 3 + 5 = 15. The others give 14, 14 and 16.

**Concept: find the shared property.** Check digit sums, products, divisibility and digit patterns until one property holds for all the given numbers.

@@ axx-hexagons
**Answer: (d) M**

**Why.** With A = 1, ..., Z = 26, the middle letter of each row is the sum of the two ends: E(5) + H(8) = 13 = M; N(14) + A(1) = 15 = O; I(9) + D(4) = 13 = M.

**Concept: letters as numbers.** Convert letters to positions and look for arithmetic between them.

@@ axx-letter-blanks
**Answer: (b) abba**

**Why.** Filled in: a b **a**a **b**b aaa **b**bb aaa**a** bbbb → runs a, b, aa, bb, aaa, bbb, aaaa, bbbb, with lengths 1, 1, 2, 2, 3, 3, 4, 4.

**Concept: look for runs.** In letter-blank series, group repeated letters and see how the run lengths change.

@@ axx-letters
**Answer: (b) W**

**Why.** Positions C 3, E 5, H 8, L 12, Q 17: gaps 2, 3, 4, 5, then 6 → 23 = W. Check: +7 = 30 → 30 − 26 = 4 = D, +8 = 12 = L. ✓

**Concept: increasing gaps with wrap-around.** After Z, continue from A (subtract 26).

@@ axx-series-206
**Answer: (c) 113**

**Why.** Term n = n³ + (2n − 1)²: 1 + 1 = 2, 8 + 9 = 17, 27 + 25 = 52, 64 + 49 = 113, 125 + 81 = 206.

**Concept: combined power series.** Fast growth hints at cubes; subtract the nearest cube (2 − 1, 17 − 8, 52 − 27 = 1, 9, 25) and recognise odd squares.

@@ axx-series-290
**Answer: (b) 170**

**Why.** Sums of squares of consecutive primes: 2² + 3² = 13, 3² + 5² = 34, 5² + 7² = 74, 7² + 11² = 170, 11² + 13² = 290.

**Concept: prime-based series.** If no difference pattern appears, try primes, squares and cubes as building blocks.

@@ axx-series-c10g
**Answer: (d) L28P**

**Why.** First letters C, F, I, L (+3); numbers 10, 16, 22, 28 (+6); last letters G, J, M, P (+3).

**Concept: split alphanumeric terms.** Treat each part (first letter, number, last letter) as its own series.

@@ axx-triangles
**Answer: (d) 500**

**Why.** Centre = product of corners ÷ 10: 15 × 6 × 4 = 360 → 36; 6 × 7 × 5 = 210 → 21; 50 × 10 × 10 = 5000 → 500.

**Concept: test products and sums of the surrounding numbers.** When the centre is bigger than the corners, try products, then scale.

@@ fk-alnum
**Answer: (b) D17T**

**Why.** First letters go back one (G, F, E → D); numbers rise by 4 (5, 9, 13 → 17); last letters go forward one (Q, R, S → T).

**Concept: separate the parts.** Each position in the term follows its own simple rule.

@@ kla-d-19
**Answer: (d) 198**

**Why.** Differences: 16, 34, 58; second differences: 18, 24 (rising by 6). Next second difference 30, next difference 58 + 30 = 88, next term 110 + 88 = 198. (The terms are n³ + 3n² − 2.)

**Concept: third differences.** If the second differences change by a constant, the series is a cubic. Keep extending the difference table.

@@ maq-q17
**Answer: (b) L**

**Why.** Two interleaved series: positions 1, 3, 5: R, P, N (back 2 each); positions 2, 4, 6: T, R, P (back 2). The next term (7th) continues R, P, N → L.

**Concept: interleaved series.** If neighbouring terms look unrelated, split odd and even positions.

@@ maq-series
**Answer: ambiguous; (d) 9, 10 is the only option consistent with part of the pattern.**

**Why.** Odd positions: 2, 4, 6, 8, so 10 is next at position 9. Even positions 3, 5, 4 follow no clear rule. (d) is the only option containing 10, but it would need 9 at position 8 (from 3, 5, 4 that is not a clear rule either).

**Concept: when a series has no clean rule, prefer the option that continues the clearest sub-pattern.**

@@ qc-n-box
**Answer: not determinable from the photo** (no rule fits the three boxes as transcribed; a corner number was probably misread).

**Concept: number-box puzzles.** Usual rules combine opposite corners (products or sums) and write the two results side by side, e.g. (TL × BR)(TR × BL). Test candidate rules on every box before applying one to the last.

@@ qc-n-series
**Answer: (b) D8**

**Why.** Letters move forward 10 places: J (10) → T (20) → D (30 − 26 = 4) → N (14) → X (24). Numbers at odd positions 7, 8, 9 and at even positions 5, 6.

**Concept: big letter jumps wrap around.** A constant shift larger than the alphabet's remaining letters continues from A.

@@ qc60-05
**Answer: no reliable pick.**

**Why.** No rule maps 1418 to 67: digit sums, products, splitting into 14 and 18 (sum 32, product 252), squares, reversals and factorisations were all tested, and none gives 67. Without that rule, 2015's partner cannot be derived.

**Concept: analogy questions need a rule that fits the example exactly.** Try splitting the number into parts and combining them (add, multiply, subtract); if nothing fits, the question is likely mis-transcribed.

@@ qc60-13
**Answer: (c) I45**

**Why.** Letters advance by 2 (A, C, E, G → I). Numbers rise by 10 (5, 15, 25, 35 → 45).

**Concept: letter and number parts move independently.** Here the number is also 5 × (letter position) − 0: A1 → 5, C3 → 15, I9 → 45.

@@ ti-alnum
**Answer: (a) CE2**

**Why.** The number equals the first letter's position minus 1: K (11) → 10, P (16) → 15, U (21) → 20, X (24) → 23. The second letter is two after the first (K–M, P–R, U–W, X–Z). The next first letter is C (X + 5 wraps to 3), so the term is C, E, 3 − 1 = 2: CE2. (The BHU candidate's CE22 misses the rule.)

**Concept: link the parts of a term.** Sometimes the number is derived from a letter in the same term rather than from the previous term.

@@ ti-grid
**Answer: (b) 10**

**Why.** In each row, middle = (product of the left number's digits) − (product of the right number's digits). Grid A: 3×5 − 2×6 = 3, 4×5 − 3×1 = 17, 3×9 − 3×2 = 21. Grid B, row 2: 6×2 − 2×1 = 10.

**Concept: digit operations within a row.** Check every row of the example grid before trusting the rule.

@@ ti-grid-small
**Answer: (a) 10** (the rule is uncertain)

**Why.** In grid B each edge number equals its two corners plus the centre: 4 + 5 + 4 = 13, 5 + 6 + 4 = 15, 2 + 6 + 4 = 12. So ? = 4 + 2 + 4 = 10. Grid A does not follow this rule cleanly, so treat the answer with caution.

**Concept: test each candidate rule on all given grids.**

@@ epam-q16
**Answer: (c) statement 1 false, 2 true, 3 true**

**Why.** This tests facts, not syllogism rules. Not every bacterial disease spreads between people (tetanus does not), so 1 is false. Some fungal infections (ringworm) are contagious, so 2 is true. A bacterial disease is by definition not fungal, so 3 is true.

**Concept: read what is being tested.** Syllogism questions usually say "assume the statements are true". When they ask whether statements **are** true, use real-world knowledge.

@@ jsw-syllogism
**Answer: (d) only either II or IV, and III follow**

**Why.**
- III: some flowers are doors and all doors are roads, so those flowers are roads: some roads are flowers. ✓
- I: all doors are roads and no road is fruit, so no door is a fruit. ✗
- II and IV: nothing fixes whether fruits and flowers overlap, but "some fruits are flowers" and "no fruit is a flower" are exact opposites, so exactly one is true: "either II or IV".

**Concept: complementary pairs.** When two conclusions about the same two sets are "some A are B" and "no A is B", one of them must be true even if neither is certain: the answer is "either ... or". Draw Venn diagrams to test each conclusion.

@@ sig-genius
**Answer: (b) invalid**

**Why.** Both geniuses and creative people lie outside the conformists, but two groups that both avoid a third group can be completely separate. Nothing links creative people to geniuses.

**Concept: two negatives prove nothing.** From "no A is C" and "no B is C" you cannot conclude anything about A and B. Draw C, then A and B outside it: they may or may not overlap.

@@ sig-graduates
**Answer: (a) always true**

**Why.** "Only graduates are eligible" means eligible → graduate. The applicants who are not graduates are therefore not eligible, so some applicants are not eligible.

**Concept: "only A are B" means "all B are A".** Its contrapositive: not A → not B. Apply it to the non-graduate applicants.

@@ ti-syllogism
**Answer: (e) no conclusion follows**

**Why.** Each conclusion is possible but none is forced. (1) frogs might all be eagles; (2) a dog might be a bat that is not a frog; (3) the cats that are dogs need not be bats; (4) some eagles could be cats. (The NIT candidate's "only 1" is wrong.)

**Concept: a conclusion follows only if it holds in every possible diagram.** Try to draw a Venn diagram where the statements hold and the conclusion fails; if you can, it does not follow.

@@ ti-tapioca
**Answer: (b) ACD**

**Why.** A: no plant root is edible. C: tapioca is edible. Therefore D: tapioca is not a plant root. This is a valid argument (if tapioca were a root, it would be inedible, contradicting C).

**Concept: valid syllogism form.** "No X is Y; Z is Y; so Z is not X." Validity is about the form, not whether the facts are true in real life.
