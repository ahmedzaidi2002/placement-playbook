---
title: "Blood relations"
weight: 9
---

5 questions asked by Accenture, ION Group, MAQ Software, Siemens Energy. Try each one first, then open the toggle: it gives the answer, why it is right, and the idea behind it explained from scratch.

### 1 · Q26-30, relations, directions, words

*Asked by: Accenture (IDC paper)*

(26) A man says to a lady, "Your mother's husband's sister is my aunt." How is the lady
related to the man? [daughter / granddaughter / mother / sister] (27) A man faces west, turns
45° clockwise, then 180° clockwise, then 270° anticlockwise. Which way does he face? [south /
north-west / west / south-west] (28) In a row of 60, Ram is 17th from the front; his position
from the end? [25 / 43 / 44 / 45] (29) Facing north-west, a man turns 90° clockwise and then
135° anticlockwise. Direction? [east / west / north / south] (30) Which three-letter word
completes VA___E, S___TER, ___ER? [STR / TER / CAT / WAT]

{{< details title="Answer and explanation" closed="true" >}}

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

{{< /details >}}

### 2 · Q38-40, relations and directions

*Asked by: Accenture (Dec paper)*

(38) Pointing to a man, Saroj said, "He is the brother of my uncle's daughter." How is he
related to Saroj? [son / cousin / nephew / uncle] (39) Sita and Mona are Narain's wives and
Bindu is Mona's step-daughter. How is Sita related to Bindu? [sister / mother-in-law / mother /
none] (40) If south-east is called east, north-west is called west, and so on, what is north
called? [east / north-west / north-east / north]

{{< details title="Answer and explanation" closed="true" >}}

**Answers: (38) cousin (39) mother (40) north-west**

**Why.**
- (38) The uncle's daughter is Saroj's cousin; her brother is also the uncle's child, so a cousin too.
- (39) Bindu is Narain's daughter but Mona's step-daughter, so Mona is not her mother. Narain's other wife, Sita, is.
- (40) South-east is renamed east: every direction moves 45° anticlockwise (SE → E). Applying the same shift, north becomes north-west. (The key's north-east is wrong.)

**Concept: renamed directions are a rotation.** Find how far one known pair has turned (SE → E is 45° anticlockwise) and apply that same turn to the asked direction.

{{< /details >}}

### 3 · Q2, family of six

*Asked by: ION Group (SDE OA, Jul 2025)*

In a family of 6 people: A is the father of B; B is the sister of C; D is the mother of E;
E is the son of A; F is the daughter of D. Who is C's mother?

- **(a)** D
- **(b)** F
- **(c)** A
- **(d)** Can't be determined

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) D**

**Why.** B is the sister of C, so B and C share a parent; A is B's father, so A is C's father too. E is A's son and D is E's mother, so D is A's wife. With one couple in a family of six (A, D and their children B, C, E, F), D is C's mother.

**Concept: draw a family tree.** Put each person in a box, connect parents to children, and mark gender as you learn it. Puzzles like this assume a single married couple unless they say otherwise.

{{< /details >}}

### 4 · Q10, the person in the photograph

*Asked by: MAQ Software (TalentDecrypt test, 2025)*

Pointing to a person in a photograph, Anjali said, "He is the only son of the father of my
sister's brother." How is that person related to Anjali?

- **(a)** Mother
- **(b)** Maternal uncle
- **(c)** Cousin
- **(d)** None of these

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) none of these** (he is her brother)

**Why.** Anjali's sister's brother is Anjali's brother (or Anjali's own sibling). His father is Anjali's father. "The only son of my father" is Anjali's brother.

**Concept: collapse the chain from the inside out.** Replace the innermost phrase first ("my sister's brother" → my brother), then the next ("his father" → my father), and so on.

{{< /details >}}

### 5 · A9, Allen and Bob's brother

*Asked by: Siemens Energy (MNNIT Allahabad (Mettl))*

Introducing Allen, Bob said, "He is the father of my only brother's daughter's
daughter." How is Allen related to Bob's brother?

- **(a)** Father
- **(b)** Husband
- **(c)** Son-in-law
- **(d)** Brother

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) son-in-law**

**Why.** Bob's only brother has a daughter; her daughter's father is the daughter's husband. So Allen is married to Bob's brother's daughter: Allen is the brother's son-in-law.

**Concept: relation chains.** "Father of X's daughter" is X's husband (or X himself if X is male). Work through the chain one link at a time.

{{< /details >}}
