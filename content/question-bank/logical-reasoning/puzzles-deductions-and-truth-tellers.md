---
title: "Puzzles, deductions and truth-tellers"
weight: 1
---

19 questions asked by Flipkart, Grey Orange, ION Group, JSW, KLA, MAQ Software, Oracle, Texas Instruments. Try each one first, then open the toggle: it gives the answer, why it is right, and the idea behind it explained from scratch.

### 1 · hill stations and cars (2)

*Asked by: Flipkart (Neev 2025)*

With the same clues, which statement is correct about the couple who went to Kollur?

- **(a)** The couple travelled in Swift car
- **(b)** The couple travelled in Fiat car
- **(c)** None of the given statement is correct
- **(d)** The couple travelled in Nissan car

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) Swift**

**Why.** The clues have one solution (see the Nissan question): David and Jansi went to Kollur, and clue II says Jansi travelled in the Swift.

**Concept: grid puzzles.** Make a table with one row per man and columns for wife, place and car. Fill direct facts first, then use "not" clues to eliminate, and repeat until each cell has one value.

{{< /details >}}

### 2 · hill stations and cars (1)

*Asked by: Flipkart (Neev 2025)*

Five men (Raj, Shyam, Murali, Vijendra, David) went with their wives (Asha, Jansi,
Mamatha, Sindhu, Ramya) to five hill stations (Agumbe, Virajpet, Kodachadri, Sagara,
Kollur) in five cars (Hyundai, Swift, Skoda, Fiat, Nissan).
(I) Raj went to Agumbe but not in the Hyundai, and Shyam is the husband of Asha, but they
did not go to Kollur. (II) Murali went to Virajpet, and Jansi travelled in the Swift with
her husband. (III) Mamatha went to Kodachadri with her husband but not in the Hyundai.
(IV) Neither Sindhu nor Mamatha is David's wife, and the couple in the Skoda went to
Sagara. (V) Ramya did not go to Kollur or Virajpet, and Vijendra did not travel in the
Fiat. Who travelled in the Nissan?

- **(a)** Murali
- **(b)** Vijendra
- **(c)** Raj
- **(d)** David

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) Vijendra**

**Why.** Fill the grid from the direct facts:
- Raj → Agumbe; Murali → Virajpet; Shyam's wife is Asha and they did not go to Kollur.
- The Skoda couple went to Sagara; Mamatha went to Kodachadri; Ramya went neither to Kollur nor Virajpet.
- Jansi rode the Swift, but clue II does not say she is Murali's wife (that reading makes the puzzle impossible).
Working through the eliminations gives one solution: Raj–Ramya, Agumbe, Fiat; Shyam–Asha, Sagara, Skoda; Murali–Sindhu, Virajpet, Hyundai; Vijendra–Mamatha, Kodachadri, Nissan; David–Jansi, Kollur, Swift.

**Concept: elimination grids.** In matching puzzles each person gets exactly one item from each category. Every "X is not Y" removes one cell; when a row or column has one cell left, it is forced. Be careful not to read extra facts into a clue.

{{< /details >}}

### 3 · hill stations and cars (3)

*Asked by: Flipkart (Neev 2025)*

With the same clues, which husband-wife pair is correct?

- **(a)** Raj - Sindhu
- **(b)** Murali - Jansi
- **(c)** Vijendra - Mamatha
- **(d)** David - Ramya

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) Vijendra – Mamatha**

**Why.** From the unique solution above.

**Concept: answer from the full grid.** Once the grid is complete, all follow-up questions are look-ups.

{{< /details >}}

### 4 · Q3, Travel Puzzle 2

*Asked by: Grey Orange (OA, Oct 2024)*

Four couples, the Maceys, Makins, Salmons and Ainsworths, each used a different mode of
transport (car, airplane, bus or ship) to reach their vacation destination, and left
from different cities: Miami, Memphis, Dallas and Washington. Which transport did the
Salmons use?

1. Parker is not married to Paula and did not travel by airplane.
2. David Macey and his wife departed from Miami and did not travel by car.
3. Richard and his wife Rebecca did not travel by bus and did not depart from Memphis.
4. Mike is not married to Ruby Ainsworth. Mike travelled by bus and did not depart from Dallas.
5. Kinsley is not married to Mr. Makin and departed from Washington.
6. The Salmons did not travel by airplane.
7. The couple from Memphis travelled by ship.

- **(a)** bus
- **(b)** airplane
- **(c)** ship
- **(d)** car

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) bus**

**Why.**
1. Mike travelled by bus, so he is not from Memphis (that couple used the ship), not from Dallas (clue 4) and not from Miami (the Maceys are from Miami): Mike is from Washington.
2. Kinsley departed from Washington (clue 5), so she is Mike's wife, and they are not the Makins.
3. Ruby is an Ainsworth but not Mike's wife; Parker is not Paula's husband, so Parker married Ruby, and David Macey married Paula.
4. Richard and Rebecca are left as the Makins, so Mike and Kinsley are the Salmons, who travelled by bus.

**Concept: start from the most constrained person.** Mike has a fixed transport and several "not" clues, so his city is forced first, and everything else chains from there.

{{< /details >}}

### 5 · Q8, Magic Boxes

*Asked by: Grey Orange (OA, Oct 2024)*

There are $n$ boxes with numbers $M[i]$. You start with a ball of size 1; putting it in
box $i$ multiplies its size by $M[i]$, and each box can be used at most once. You win if
the last digit of the ball's size equals $d$. The following scenarios are wins if played
properly; give the maximum possible size of the ball after winning each game.

1. $n = 6$, $d = 4$, $M = \{8, 2, 1, 13, 4, 11\}$
2. $n = 5$, $d = 6$, $M = \{2, 2, 2, 2, 2\}$
3. $n = 6$, $d = 3$, $M = \{9, 4, 8, 11, 5, 17\}$

- **(a)** 1144 16 1673
- **(b)** 1144 16 1683
- **(c)** 704 16 1683
- **(d)** 744 16 1673

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) 1144, 16, 1683**

**Why.**
1. All boxes: 8 × 2 × 1 × 13 × 4 × 11 = 9152 (ends in 2). Dropping 8 gives 1144 (ends in 4), the largest product ending in 4.
2. Powers of 2 end in 2, 4, 8, 6, repeating. 2⁴ = 16 ends in 6; 2⁵ = 32 does not. So 16.
3. Using 5 with any even number ends in 0, and 5 with only odd numbers ends in 5, so leave 5 out. 9 × 11 × 17 = 1683 ends in 3 and is the largest such product.

**Concept: last digits only depend on last digits.** The units digit of a product is the units digit of the product of the units digits. Powers cycle with a short period (2 → 4 → 8 → 6). Multiplying by 5 and an even number always ends in 0.

{{< /details >}}

### 6 · Q3, who is the engineer

*Asked by: ION Group (SDE OA, Jul 2025)*

On a train, S, R and J are the fireman, brakeman and engineer, not necessarily in that
order. Also aboard are three businessmen with the same names: Mr. S, Mr. R and Mr. J.

1. Mr. R lives in Dehradun.
2. The brakeman lives exactly halfway between Noida and Dehradun.
3. Mr. J earns exactly Rs. 4,00,000 per year.
4. The brakeman's nearest neighbour, one of the passengers, earns exactly three times
    as much as the brakeman.
5. S beats the fireman in badminton.
6. The passenger whose name is the same as the brakeman's lives in Noida.

Who is the engineer?

- **(a)** Cannot be determined
- **(b)** S is the Engineer
- **(c)** J is the Engineer
- **(d)** R is the Engineer

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) S is the engineer**

**Why.**
1. The brakeman lives halfway between Noida and Dehradun, and his nearest neighbour is a passenger. Mr. R lives in Dehradun, and the passenger named like the brakeman lives in Noida, so the neighbour is neither. The neighbour earns 3 × the brakeman's salary; Mr. J earns 4,00,000, not divisible by 3, so the neighbour is not Mr. J. So the neighbour is Mr. S, and the passenger in Noida is Mr. J.
2. The passenger in Noida has the brakeman's name, so J is the brakeman.
3. S beats the fireman, so S is not the fireman: S is the engineer (and R the fireman).

**Concept: eliminate with each clue.** This is Dudeney's classic puzzle. Combine clues that talk about the same person (the neighbour) and rule out candidates using numbers (divisibility by 3) and places.

{{< /details >}}

### 7 · who robbed the bank

*Asked by: JSW (Aptitude test)*

Tom, Martin and Garry are suspects in a bank robbery; only one of them is guilty. Tom
says he is innocent. Martin says he is innocent. Garry says Martin is the guilty one. Who
robbed the bank, if only one statement is true?

- **(a)** Tom
- **(b)** Martin
- **(c)** Garry
- **(d)** None of the mentioned

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) Tom**

**Why.** Try each suspect as the robber and count true statements.
- Tom guilty: Tom's "I am innocent" false; Martin's true; Garry's ("Martin is guilty") false → exactly one true. ✓
- Martin guilty: Tom true, Martin false, Garry true → two true. ✗
- Garry guilty: Tom true, Martin true, Garry false → two true. ✗

**Concept: case testing for truth-teller puzzles.** Assume each possibility in turn and check it against the condition ("only one statement is true"). Exactly one case should survive.

{{< /details >}}

### 8 · Q1, breaking a chocolate bar

*Asked by: KLA (IIT Delhi 2023)*

Santa and Banta play a game with a chocolate bar 15 squares long and 20 squares wide.
Santa begins by breaking the bar in two along any division. Banta then picks up any
piece and breaks it in two, and so on. Who will be the first player who cannot make
any more moves?

- **(a)** Santa
- **(b)** Cannot be determined
- **(c)** Banta

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) Banta**

**Why.** Each break turns one piece into two, so the number of pieces grows by exactly 1 per move. From 1 piece to 15 × 20 = 300 single squares needs 299 moves, no matter how you break. Santa makes moves 1, 3, 5, ..., 299 (the last one), so Banta is the first who cannot move.

**Concept: invariants.** Look for a quantity that changes by a fixed amount each move (here, pieces + 1). Then the total number of moves is fixed, and parity decides who moves last.

{{< /details >}}

### 9 · Q8, black and white balls

*Asked by: KLA (IIT Delhi 2023)*

A bag contains 25 white balls and 50 black ones; a separate pile of black balls is
also available. The following two-step operation is repeated. First, two balls are
drawn at random from the bag. Then:

- if both are black, one is put back in the bag and the other thrown away;
- if one is black and the other white, the white one is put back and the black
    one thrown away;
- if both are white, both are thrown away and a black ball from the pile is put
    into the bag.

The bag loses a ball at each step, so eventually it holds a single ball. What colour
is it?

- **(a)** Black
- **(b)** Cannot be determined, but most likely Black
- **(c)** White
- **(d)** Cannot be determined, but most likely White

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) White**

**Why.** Watch the number of white balls: the black-black and black-white cases leave it unchanged; the white-white case removes 2. So it changes only by 0 or −2, and its parity (odd/even) never changes. It starts at 25, odd, so it can never become 0. When one ball is left, it must be the white one.

**Concept: parity invariant.** If a quantity always changes by an even amount, it stays odd or even forever. This decides the final state without simulating any draws.

{{< /details >}}

### 10 · Q12, spokes

*Asked by: KLA (IIT Delhi 2023)*

A bicycle shop has some unique bicycles. Each bike is identical, and each bike's
front and back wheels have at least one spoke each. You don't know how many bicycles
are in the shop, but you know there are between 200 and 300 spokes in total.
If you knew the exact number of spokes, you would be able to figure out the number of
bicycles. You don't know the exact number of spokes, but just knowing the fact that
you would be able to figure it out with that information lets you deduce the answer.
How many bicycles and spokes are there?

- **(a)** 17 bicycles 17 spokes
- **(b)** 16 bicycles 16 spokes
- **(c)** 15 bicycles, 15 spokes
- **(d)** 20 bicycles 11 spokes
- **(e)** It was not many years

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) 17 bicycles with 17 spokes each** (289 spokes)

**Why.** With b ≥ 2 identical bicycles of s spokes each (s ≥ 2: two wheels, at least one spoke each), the total is S = b × s. Knowing S lets you find b only if S can be written as b × s in exactly one way with both ≥ 2. That happens only when S is the square of a prime: p² = p × p and nothing else. Between 200 and 300 the only such number is 289 = 17².

**Concept: unique factorisation as information.** "I could work it out if I knew S" tells you S has a special property. A number has exactly one factor pair (other than 1 × itself) only if it is a prime squared. (The last option is a stray from another question.)

{{< /details >}}

### 11 · Q21, same place same time

*Asked by: KLA (IIT Delhi 2023)*

You start at 8 am from Delhi and drive towards Jaipur (at variable speed, taking random
breaks), reaching Jaipur at 12 noon. The next day you start at 8 am from Jaipur, take
the same road back and reach Delhi at 12 noon (again at variable speed, with random
breaks). How likely is it that there is a point on the road which you crossed at the
same time of day on both journeys?

- **(a)** 0%
- **(b)** Anywhere between 0% to 100%
- **(c)** 100%
- **(d)** 50%

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) 100%**

**Why.** Imagine both trips happening on the same day: one car leaves Delhi at 8 am for Jaipur, another leaves Jaipur at 8 am for Delhi, on the same road, both finishing at noon. They must pass each other somewhere. At that moment they are at the same point at the same time of day, so that point exists on every pair of trips.

**Concept: the intermediate value theorem.** Let d(t) = (position on day 1) − (position on day 2). It starts negative at 8 am (Delhi vs Jaipur) and ends positive at noon, and changes continuously, so it is zero at some moment. Speeds and breaks do not matter.

{{< /details >}}

### 12 · Q23, fastest horses

*Asked by: KLA (IIT Delhi 2023)*

You have 25 horses and want the fastest 3. In each race only 5 horses can run at the
same time. What is the minimum number of races needed to find the three fastest
horses without using a stopwatch?

- **(a)** 7
- **(b)** 10
- **(c)** 8
- **(d)** 5

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) 7**

**Why.**
1. Races 1–5: five heats of five. The bottom two of each heat cannot be top 3.
2. Race 6: the five heat winners. Its winner is the fastest overall. Horses from heats whose winner came 4th or 5th are out.
3. Remaining candidates for 2nd and 3rd: 2nd and 3rd of race 6, 2nd and 3rd from the overall winner's heat, and 2nd from the heat of race 6's runner-up. That is 5 horses: race 7 decides.

**Concept: eliminate by "who can't be in the top k".** A horse beaten by k horses that are known to be faster cannot be in the top k. Tracking who beat whom shrinks the field to one final race.

{{< /details >}}

### 13 · Q11, measuring 45 minutes with two ropes

*Asked by: MAQ Software (TalentDecrypt test, 2025)*

You have two ropes, each taking exactly 60 minutes to burn, but they burn unevenly. How can
you measure 45 minutes?

- **(a)** Burn one rope halfway then the other fully.
- **(b)** Burn one rope from both ends and the other from one end.
- **(c)** Burn both ropes from one end.
- **(d)** Burn both ropes from both ends.

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) burn one rope from both ends and the other from one end**

**Why.** Rope 1, lit at both ends, burns out in 30 minutes, however unevenly. At that moment rope 2 (lit at one end) has 30 minutes of burning left; light its other end, and it finishes in 15 minutes. Total 30 + 15 = 45.

**Concept: lighting both ends halves the time.** Uneven burning means you cannot measure by length, only by time. Two flames meeting somewhere still use up the rope's total burn time twice as fast.

{{< /details >}}

### 14 · road network, where does the journey end

*Asked by: Oracle (HackerRank MCQ test)*

There is a network of eight cities (vertices) connected by roads. A traveller must drive on
each road segment once, but can visit a city multiple times if necessary; the start and end
points need not match. New roads are constructed between $C$ and $G$, and between $H$ and $F$.
If the journey begins at $B$, where will it end?
[figure: see the original PDF]
(Figure redrawn from the video frames; the new roads $C$-$G$ and $H$-$F$ are added to it.)

- **(a)** E
- **(b)** B
- **(c)** H
- **(d)** G

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) E**

**Why.** A route using every road exactly once is an Euler path. It exists only if 0 or 2 cities have an odd number of roads, and then it must start at one odd city and end at the other. After adding C–G and H–F, the degrees are A 2, B 3, C 4, D 2, E 3, F 4, G 4, H 4. Starting at B (odd), the journey ends at E, the other odd city. (The photo's G has even degree and cannot be an end.)

**Concept: Euler paths.** Every time you pass through a city you use one road in and one out, an even number. Only the start and end can have odd degree. So count each city's roads; the odd ones are the endpoints.

{{< /details >}}

### 15 · five people, sports and colours

*Asked by: Oracle (HackerRank MCQ test)*

Jack, Matthew, Albert, Peter and Sebastian each play one of football, cricket, volleyball,
badminton and squash; are from South Korea, the UK, India, China and Russia; and have
favourite colours brown, green, red, black and yellow (all different).
(1) Jack's favourite colour is red; he is not from India or China. (2) Albert plays football;
his favourite colour is not yellow and he is not from the UK. (3) Peter and Sebastian have
yellow and green as favourite colours, in some order. (4) Matthew plays badminton; he is from
Russia. (5) Peter and Sebastian are from China and the UK, in some order. (6) Brown is the
favourite colour of the person from India. (7) Green is the favourite colour of the person
from China. (8) The person from South Korea plays squash and the person from the UK plays
volleyball; one of them has yellow as favourite colour.
Whose favourite colour is black?

- **(a)** Matthew
- **(b)** Albert
- **(c)** Peter
- **(d)** Sebastian

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) Matthew**

**Why.** Peter and Sebastian take China and the UK; Matthew is from Russia; Jack is not from India or China, so Jack is from South Korea and Albert from India. India's colour is brown (Albert). Jack is red; Peter and Sebastian have yellow and green. The only colour left, black, goes to Matthew. (The photo ticks Albert, who is brown.)

**Concept: fill the most constrained categories first.** Countries were nearly forced by clues 4, 5 and 1, and each country clue then fixed a colour. The asked item often falls out before the whole grid is complete.

{{< /details >}}

### 16 · the butcher's weights

*Asked by: Texas Instruments (IIT ISM 2024)*

Weights 1, 2, 4, ..., 64 kg on one pan only; customers 1 to 128 buy their number of kg. How
many are disappointed?

- **(a)** 0
- **(b)** 1
- **(c)** 2
- **(d)** 3

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) 1**

**Why.** With weights 1, 2, 4, ..., 64 on one pan, every whole number from 1 to 1 + 2 + ... + 64 = 127 can be made (each weight is either used or not, like binary digits). Only customer 128 cannot be served.

**Concept: binary representation.** Every whole number has exactly one binary form, a sum of distinct powers of 2. Weights 2⁰ to 2⁶ cover 0 to 2⁷ − 1 = 127.

{{< /details >}}

### 17 · truth-tellers in a chess club

*Asked by: Texas Instruments (IISc, second set)*

Teams T1, T2, T3: one always tells the truth, one always lies, one alternates. They meet on
Tuesday, Friday and Sunday, each team preferring a different day. T1: "Tuesday is the most
comfortable day and Friday is comfortable for T2." T2: "Friday is comfortable for T3 and
Sunday for T1." T3: "Tuesday is the most comfortable day and T1 is comfortable with
Sunday." Which team tells the truth?

- **(a)** T1
- **(b)** T2
- **(c)** T3
- **(d)** Cannot be determined

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) T2**

**Why.** Try each team as the truth-teller and check consistency. Only one assignment works: T1 prefers Sunday and always lies, T2 prefers Tuesday and tells the truth, T3 prefers Friday and alternates. T2's statements (Friday for T3, Sunday for T1) are then both true.

**Concept: truth-teller / liar / alternator.** A truth-teller's statements are all true, a liar's all false, and an alternator's two statements have opposite truth values. Assume a type for one speaker, derive the facts, and check whether the others' statements fit their types.

{{< /details >}}

### 18 · E's profession

*Asked by: Texas Instruments (IIT ISM 2024)*

Six people A-F (doctor, engineer, manager, jeweller, painter, lawyer) with family clues. E's
profession?

{{< details title="Answer and explanation" closed="true" >}}

**Answer: Lawyer**

**Why.** The family clues (not reproduced in the source) leave exactly one profession for E after the others are placed.

**Concept: elimination grids.** List people and professions in a table and cross out every pairing a clue forbids until each row has one choice left.

{{< /details >}}

### 19 · the shoe store theft

*Asked by: Texas Instruments (IIT ISM 2024)*

Only W1, W2, W3 could be guilty; W3 never acts without W1; W2 cannot climb high walls (needed).
Is W1 guilty?

{{< details title="Answer and explanation" closed="true" >}}

**Answer: Yes, W1 is guilty**

**Why.** Someone among W1, W2, W3 is guilty. W2 cannot climb high walls, which the theft needed, so W2 is out. If W3 is guilty, W1 was with him (W3 never acts without W1). Either way W1 is guilty. (The IISc candidate's "insufficient" is wrong.)

**Concept: proof by cases.** If every possible case leads to the same conclusion, that conclusion is certain.

{{< /details >}}
