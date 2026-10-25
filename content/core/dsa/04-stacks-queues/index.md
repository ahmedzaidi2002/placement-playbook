---
title: "4 · Stacks and queues"
linkTitle: "4 Stacks and queues"
weight: 4
math: true
---
## 4.1 Stack (LIFO) {#dsa-4-1}

Last in, first out: `push`, `pop`, `top`/`peek`, all **$O(1)$**. Implemented with an array (top index) or a linked list (insert/remove at the head). Popping an empty stack = **underflow**; pushing onto a full fixed-size stack = **overflow**.

**Uses:** function calls (the call stack), undo, browser back, **balanced parentheses**, expression evaluation, DFS, **monotonic stack** (next greater element in $O(n)$).

## 4.2 Queue (FIFO) {#dsa-4-2}

First in, first out: `enqueue` at the rear, `dequeue` at the front, both **$O(1)$**.

- **Circular queue** (array of size $n$): `rear = (rear + 1) % n`. To tell full from empty, either keep a count or leave one slot empty (full when `(rear + 1) % n == front`).
- **Deque:** insert/remove at both ends in $O(1)$ (sliding-window maximum).
- **Priority queue:** remove the highest-priority item first; usually a heap (chapter 7).

**Uses:** BFS, scheduling, buffers, printer queues.

## 4.3 One built from the other {#dsa-4-3}

- **Queue from two stacks:** push onto stack A; to dequeue, if B is empty pour all of A into B, then pop B. Each element moves at most twice → **$O(1)$ amortized**.
- **Stack from two queues** (or one): push = enqueue then rotate the queue so the new item is at the front → push $O(n)$, pop $O(1)$ (or the reverse).

## 4.4 Expressions: infix, postfix, prefix {#dsa-4-4}

- **Infix:** `A + B * C` (needs precedence and parentheses). **Postfix (reverse Polish):** `A B C * +`. **Prefix (Polish):** `+ A * B C`. Postfix and prefix need no parentheses.
- **Infix → postfix (shunting-yard):** operands go straight to the output; for an operator, pop operators of higher (or equal, if left-associative) precedence from the stack first, then push it; `(` is pushed, `)` pops until `(`; at the end pop everything.

<div class="nb nb-example">

<strong>Example</strong> (Convert and evaluate)

`A + B * C - D / E` → postfix **`A B C * + D E / -`**; prefix **`- + A * B C / D E`**.

Evaluate postfix `2 3 4 * + 5 -` with a stack: push 2, 3, 4; `*` → pop 4, 3, push 12; `+` → pop 12, 2, push 14; push 5; `-` → pop 5, 14, push **9**.

</div>

## 4.5 Which outputs can a stack produce? {#dsa-4-5}

Push 1, 2, …, $n$ in order, popping at any time. An output order is possible iff it never contains a pattern $\dots c \dots a \dots b \dots$ with $a < b < c$ (the "312" pattern; e.g. for 1, 2, 3, the order **3, 1, 2** is impossible). The number of possible outputs is the **Catalan number** $C_n = \frac{1}{n+1}\binom{2n}{n}$: 5 for $n = 3$, 14 for $n = 4$.

<div class="nb nb-moral">

Stack = LIFO (calls, undo, parentheses, postfix); queue = FIFO (BFS, scheduling). A queue from two stacks is O(1) amortized. Stack-sortable outputs are counted by Catalan numbers.

</div>
