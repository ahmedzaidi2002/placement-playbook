---
title: "Syllogisms"
weight: 8
---

6 questions asked by EPAM, JSW, Sigmoid, Texas Instruments. Try each one first, then open the toggle: it gives the answer, why it is right, and the idea behind it explained from scratch.

### 1 · Q16, bacterial and fungal diseases

*Asked by: EPAM (EPAM freshers test)*

Statement 1: All bacterial diseases are communicable diseases. Statement 2: Some fungal
diseases are also communicable diseases. Statement 3: No bacterial diseases are fungal
diseases. Which is correct?

- **(a)** All statements are true
- **(b)** Statement 1 is true, Statement 2 is false, and Statement 3 is true
- **(c)** Statement 1 is false, Statement 2 is true, and Statement 3 is true
- **(d)** All statements are false

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) statement 1 false, 2 true, 3 true**

**Why.** This tests facts, not syllogism rules. Not every bacterial disease spreads between people (tetanus does not), so 1 is false. Some fungal infections (ringworm) are contagious, so 2 is true. A bacterial disease is by definition not fungal, so 3 is true.

**Concept: read what is being tested.** Syllogism questions usually say "assume the statements are true". When they ask whether statements **are** true, use real-world knowledge.

{{< /details >}}

### 2 · doors, roads, fruit and flowers

*Asked by: JSW (Aptitude test)*

Statements: All doors are roads. No road is fruit. Some flowers are doors.
Conclusions: I. Some fruits are doors. II. Some fruits are flowers. III. Some roads are
flowers. IV. No fruit is a flower.

- **(a)** Only either II or IV follows
- **(b)** Only either II or III, and IV follow
- **(c)** Only either II or IV, and I follow
- **(d)** Only either II or IV, and III follow
- **(e)** All the conclusions follow

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) only either II or IV, and III follow**

**Why.**
- III: some flowers are doors and all doors are roads, so those flowers are roads: some roads are flowers. ✓
- I: all doors are roads and no road is fruit, so no door is a fruit. ✗
- II and IV: nothing fixes whether fruits and flowers overlap, but "some fruits are flowers" and "no fruit is a flower" are exact opposites, so exactly one is true: "either II or IV".

**Concept: complementary pairs.** When two conclusions about the same two sets are "some A are B" and "no A is B", one of them must be true even if neither is certain: the answer is "either ... or". Draw Venn diagrams to test each conclusion.

{{< /details >}}

### 3 · geniuses and conformists

*Asked by: Sigmoid (Campus hiring 2026)*

No genius is a conformist. Creative people are never conformists. Conclusion: therefore,
all creative people are geniuses.

- **(a)** Conclusion is valid
- **(b)** Conclusion is invalid
- **(c)** Conclusion is doubtful

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) invalid**

**Why.** Both geniuses and creative people lie outside the conformists, but two groups that both avoid a third group can be completely separate. Nothing links creative people to geniuses.

**Concept: two negatives prove nothing.** From "no A is C" and "no B is C" you cannot conclude anything about A and B. Draw C, then A and B outside it: they may or may not overlap.

{{< /details >}}

### 4 · only graduates are eligible

*Asked by: Sigmoid (Campus hiring 2026)*

Choose the most logical option. If only graduates are eligible for this job, and some
applicants are not graduates, then "some applicants are not eligible for this job":

- **(a)** is always true
- **(b)** is always false
- **(c)** may or may not be true

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) always true**

**Why.** "Only graduates are eligible" means eligible → graduate. The applicants who are not graduates are therefore not eligible, so some applicants are not eligible.

**Concept: "only A are B" means "all B are A".** Its contrapositive: not A → not B. Apply it to the non-graduate applicants.

{{< /details >}}

### 5 · cats, dogs, frogs, bats

*Asked by: Texas Instruments (IISc, second set)*

Some cats are dogs. No dog is a frog. All frogs are bats. Some bats are eagles.
Conclusions: (1) Some frogs are not eagles. (2) No dog is a bat. (3) Some cats are bats.
(4) No eagle is a cat.

- **(a)** Both 2 and 4 follow
- **(b)** 2
- **(c)** 3 and 4 follow
- **(d)** Only 1 follows
- **(e)** No conclusion follows

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (e) no conclusion follows**

**Why.** Each conclusion is possible but none is forced. (1) frogs might all be eagles; (2) a dog might be a bat that is not a frog; (3) the cats that are dogs need not be bats; (4) some eagles could be cats. (The NIT candidate's "only 1" is wrong.)

**Concept: a conclusion follows only if it holds in every possible diagram.** Try to draw a Venn diagram where the statements hold and the conclusion fails; if you can, it does not follow.

{{< /details >}}

### 6 · a syllogism about tapioca

*Asked by: Texas Instruments (IISc, second set)*

Statements: (A) No plant root is edible. (B) Tapioca is not edible. (C) Tapioca is edible.
(D) Tapioca is not a plant root. (E) Tapioca is a stem. Which three form a valid argument?

- **(a)** ACB
- **(b)** ACD
- **(c)** ADE
- **(d)** ABE

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) ACD**

**Why.** A: no plant root is edible. C: tapioca is edible. Therefore D: tapioca is not a plant root. This is a valid argument (if tapioca were a root, it would be inedible, contradicting C).

**Concept: valid syllogism form.** "No X is Y; Z is Y; so Z is not X." Validity is about the form, not whether the facts are true in real life.

{{< /details >}}
