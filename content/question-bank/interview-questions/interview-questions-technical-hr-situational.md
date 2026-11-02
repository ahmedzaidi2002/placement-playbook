---
title: "Interview questions (technical, HR, situational)"
weight: 1
---

5 questions asked by Accenture, Google, JSW. Try each one first, then open the toggle: it gives the answer, why it is right, and the idea behind it explained from scratch.

### 1 · HR questions reported

*Asked by: Accenture (Interviews)*

Reported HR questions: favourite subject and why; why Accenture, why analytics or data
science; which domains Accenture operates in; difficulties faced during internships and how you
tackled them; how you would finish work with someone you have a conflict with; a situation
where you changed someone's opinion; your weakest course and how you managed; hobbies (one
candidate was asked to narrate the story of a recent film); whether you are willing to face
complex client problems; future study plans and location preference; and "do you have any
questions for us?".

{{< details title="Answer and explanation" closed="true" >}}

**How to answer.** Prepare short STAR stories (Situation, Task, Action, Result) for conflict, changing someone's mind, and a difficulty in an internship. Have a genuine reason for "why Accenture" and "why analytics", and know the company's main domains. If you mention a hobby, be ready to talk about it in detail.

**Concept: the STAR method.** Describe the situation and your task in one or two lines, spend most of the answer on what **you** did, and end with a measurable result and what you learned. It keeps behavioural answers specific and short.

{{< /details >}}

### 2 · technical questions reported

*Asked by: Accenture (Interviews)*

Reported technical questions: traversing and reversing a linked list, and circular linked
lists; cyber security and cloud basics; explaining a resume project in depth; for the Data
Science Analyst role, SQL queries, basic Python, probability and statistics, and ML basics;
in the managerial round, semi-case questions such as "how would you model a qualitative
variable" and regression and optimisation algorithms.

{{< details title="Answer and explanation" closed="true" >}}

**How to prepare.**
- Linked list reversal with three pointers: prev = null, cur = head; repeat: next = cur.next, cur.next = prev, prev = cur, cur = next. Return prev.
- Circular lists: detect a cycle with Floyd's slow/fast pointers; traverse a known circular list until you come back to the start node.
- Qualitative variables: one-hot encoding for unordered categories, ordinal encoding for ordered ones.
- Know every line of your resume and be able to explain your project code.

**Concept: Floyd's cycle detection.** Move one pointer one step and another two steps at a time. If there is a cycle, the fast pointer eventually laps the slow one and they meet; if fast reaches null, there is no cycle. O(n) time, O(1) space.

{{< /details >}}

### 3 · rooting a tree as a binary tree, with coloured levels

*Asked by: Google (Interview round 1)*

You are given an undirected acyclic graph (a tree) in which every vertex has at most 3
neighbours, as an adjacency list.

1. Return a vertex that can be the root of a valid binary tree.
2. *Follow-up.* The vertices are coloured black and white. Return a root of a
    valid binary tree whose levels alternate in colour (B-W-B-W...{} or
    W-B-W-B...), or $-1$ if there is none.
3. *Follow-up.* The vertices are coloured red, black and white. Return a root of
    a valid binary tree whose levels follow the order R-B-W-R-B-W..., starting
    from any of the three colours (B-W-R...{} and W-R-B...{} are allowed, but
    B-R-W is not), or $-1$ if there is none.

{{< details title="Answer and explanation" closed="true" >}}

**Answer (approach).**
1. Any vertex with at most 2 neighbours can be the root (a tree always has a leaf, so one exists).
2. Levels alternate in colour exactly when every edge joins two different colours, which does not depend on the root. If some edge has equal colours, return −1; otherwise return any vertex of degree ≤ 2.
3. With colours in the cyclic order R → B → W → R, a child's colour must follow its parent's. For each edge with different colours exactly one direction is allowed, so each edge fixes which end is the parent. A valid root exists iff no vertex gets two parents, exactly one vertex gets none (the root), and the root has at most 2 children. O(n).

**Why.** When a tree is rooted at r, every other vertex uses one neighbour as its parent, so with at most 3 neighbours it has at most 2 children. Only the root could have 3 children, so the root must have degree ≤ 2.

**Concept: rooting a tree.** Picking a root orients every edge from parent to child. Degree constraints and colour rules become constraints on these orientations; check them edge by edge in linear time.

{{< /details >}}

### 4 · situational judgement, heated argument

*Asked by: JSW (Aptitude test)*

You are in a heated argument with a friend and both of you are becoming disrespectful and
insulting. What is the best reaction?

- **(a)** Walk away from the argument.
- **(b)** Confront the friend about their behaviour.
- **(c)** Agree to disagree and end the argument.
- **(d)** Continue the argument and insult the friend back.

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) agree to disagree and end the argument**

**Why.** It stops the escalation while keeping the friendship and respect. Walking away (a) is second best; confronting (b) or insulting back (d) escalates.

**Concept: situational judgement tests.** They reward calm, respectful, constructive responses that solve the problem and preserve relationships, over avoidance or retaliation.

{{< /details >}}

### 5 · situational judgement, two job offers

*Asked by: JSW (Aptitude test)*

You have been offered two jobs: one with a higher salary but longer working hours, and one
with a lower salary but shorter working hours. What do you do?

- **(a)** Choose the job with the higher salary.
- **(b)** Choose the job with the shorter working hours.
- **(c)** Negotiate shorter working hours with the job with a higher salary.
- **(d)** Negotiate a higher salary with the job with shorter working hours.

{{< details title="Answer and explanation" closed="true" >}}

**Answer: no single correct option; (c) or (d) are usually rewarded.**

**Why.** Trying to negotiate a better package (shorter hours with the higher-paid job, or higher pay with the shorter-hours job) is proactive and balanced, rather than accepting a trade-off without trying.

**Concept: judgement questions test reasoning.** In an interview, explain what matters to you at this stage (learning, money, time) and why; there is rarely one right choice.

{{< /details >}}
