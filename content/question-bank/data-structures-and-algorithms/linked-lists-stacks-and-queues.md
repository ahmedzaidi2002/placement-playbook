---
title: "Linked lists, stacks and queues"
weight: 1
---

19 questions asked by EPAM, ION Group, MathWorks, Oracle, Paytm, Qualcomm, Texas Instruments, Warner Bros. Discovery. Try each one first, then open the toggle: it gives the answer, why it is right, and the idea behind it explained from scratch.

### 1 · Q3, enqueue into a non-circular array queue

*Asked by: EPAM (EPAM freshers test)*

Consider the array representation of a non-circular queue,
$Q = \{3, 3, 2, 2, 2, 2, \_, \_, \_, \_, \_\}$ (six filled slots followed by empty ones).
What is the maximum number of enqueue operations that can be performed, after which an
overflow condition will occur? Assume one-based indexing.

- **(a)** 6
- **(b)** 5
- **(c)** 7
- **(d)** 1

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) 5** (reading the photo as 11 slots with 6 used)

**Why.** In a linear (non-circular) queue, new elements go only after the rear. With 6 filled slots in an array of 11, only the 5 empty slots after the rear can be used; the 6th enqueue overflows. Slots freed at the front by dequeues are not reused, which is the weakness a circular queue fixes.

**Concept: linear vs circular queue.** Linear: rear only moves forward, so space at the front is wasted after dequeues ("false overflow"). Circular: indices wrap with `% size`, so every free slot can be reused.

{{< /details >}}

### 2 · Q5, what does oper() do to a linked list

*Asked by: EPAM (EPAM freshers test)*

What operation does the function `oper` perform on a linked list?

```cpp
void oper(Node** head_ref, int new_data) {
    Node* new_node = new Node();
    Node* last = *head_ref;
    new_node->data = new_data;
    new_node->next = NULL;
    if (*head_ref == NULL) { *head_ref = new_node; return; }
    while (last->next != NULL) last = last->next;
    last->next = new_node;
    return;
}
```

- **(a)** It inserts a node at the beginning of the linked list.
- **(b)** It inserts a node after a given node in the linked list.
- **(c)** It inserts a node at the end of the linked list.
- **(d)** It deletes the last element of the linked list.

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) it inserts a node at the end of the linked list**

**Why.** The new node's `next` is NULL. An empty list gets it as the head. Otherwise the loop walks to the last node and links the new node after it. O(n) per insertion; keeping a tail pointer makes it O(1).

**Concept: why `Node**`.** To change the caller's head pointer (when the list is empty), the function needs the address of that pointer, i.e. a pointer to a pointer.

{{< /details >}}

### 3 · Q20, queue operations

*Asked by: ION Group (SDE OA, Jul 2025)*

`enqueue()` adds an element to a queue and `deque()` removes one. What does this
pseudocode print?
`enqueue(5); enqueue(8); deque(); enqueue(3); enqueue(7); deque(); enqueue(10);
deque(); PRINT q.front()`

- **(a)** 7
- **(b)** 3
- **(c)** 8
- **(d)** 10

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) 7**

**Why.** [5] → [5, 8] → dequeue → [8] → [8, 3] → [8, 3, 7] → dequeue → [3, 7] → [3, 7, 10] → dequeue → [7, 10]. The front is 7.

**Concept: FIFO.** A queue removes the element that has waited longest. Track the queue's contents after each operation.

{{< /details >}}

### 4 · Q24, postfix evaluation

*Asked by: MathWorks (IISc 2024)*

The value of the postfix expression `6 3 2 4 + - *` lies:

- **(a)** between $-5$ and $-15$
- **(b)** between 5 and $-5$
- **(c)** between 5 and 15
- **(d)** between 15 and $-100$

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) between 15 and −100** (the value is −18)

**Why.** Postfix: push 6, 3, 2, 4. `+` pops 2 and 4 → 6. `−` pops 3 and 6 → 3 − 6 = −3. `*` pops 6 and −3 → −18.

**Concept: evaluating postfix with a stack.** Push numbers; on an operator, pop the top two (the first popped is the right operand), apply, push the result. The final stack holds the answer.

{{< /details >}}

### 5 · infix to postfix

*Asked by: Oracle (HackerRank MCQ test)*

What is the postfix expression for the infix expression `a+b*c+(d*e)`?

- **(a)** abc*+de*+
- **(b)** abc+*de*+
- **(c)** a+bc*de+*
- **(d)** abc*+(de)*+

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) `abc*+de*+`**

**Why.** `*` binds tighter than `+`, and `+` is left-associative: ((a + (b*c)) + (d*e)). In postfix each operator follows its operands: a, then b c *, then +, then d e *, then +.

**Concept: infix to postfix.** Postfix (reverse Polish) writes operators after their operands and needs no brackets. Convert with the shunting-yard algorithm: output operands immediately, hold operators on a stack, and pop operators of higher or equal precedence before pushing a new one.

{{< /details >}}

### 6 · Convert an Expression, maximum stack length

*Asked by: Paytm (HackerRank, Sep 2025)*

What is the maximum length of the stack when converting the infix expression
$(a-b)*c/(d/f-g)*h$ to postfix?

- **(a)** 5
- **(b)** 2
- **(c)** 3
- **(d)** 4

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) 3**

**Why.** Only operators and parentheses go on the stack. `(` `−` → depth 2; `)` empties it. `*` pushed; `/` pops it (same precedence, left-associative) and is pushed. Then `(` and `/` → `/ ( /`: depth 3. `−` pops the inner `/` and gives `/ ( −`: still 3. `)` unwinds to `/`; the last `*` replaces it. Maximum 3.

**Concept: shunting-yard stack depth.** The stack holds pending operators. Equal-precedence left-associative operators pop each other, so the stack only grows with nesting and rising precedence.

{{< /details >}}

### 7 · Max Stack

*Asked by: Paytm (HackerRank, Sep 2025)*

Find the maximum length the stack will have when performing: Push(10); Pop();
Push(17); Push(29); Push(6); Pop(); Push(10); Push(77); Pop();

- **(a)** 3
- **(b)** 5
- **(c)** 4
- **(d)** None of the above

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) 4**

**Why.** Stack sizes after each operation: 1, 0, 1, 2, 3, 2, 3, 4, 3. The maximum is 4, after Push(77).

**Concept: track size, not contents.** For "maximum height" questions, keep a running count (+1 push, −1 pop).

{{< /details >}}

### 8 · top and bottom of the stack

*Asked by: Paytm (HackerRank, Sep 2025)*

In the postfix expression `6 3 2 * / 3 2 1 * - +`, what are the values of the top
and the bottom of the stack just before the second `*` is performed?

- **(a)** 1,1
- **(b)** 6,1
- **(c)** 1,2
- **(d)** 3,1

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) 1, 1**

**Why.** Push 6, 3, 2; `*` → 3 × 2 = 6, stack [6, 6]; `/` → 6 / 6 = 1, stack [1]. Push 3, 2, 1: [1, 3, 2, 1]. Just before the second `*`, the top is 1 and the bottom is 1.

**Concept: postfix evaluation with a stack** (see above): pop two, apply, push the result.

{{< /details >}}

### 9 · Q23, stack operations

*Asked by: Qualcomm (IISc)*

A stack $S$ has capacity 5. What is $S$ after Push(2), Push(1), Pop(), Push(3), Pop(), Pop(),
Pop()?

- **(a)** 3
- **(b)** Underflow
- **(c)** 2 3
- **(d)** 2

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) underflow**

**Why.** Push 2 → [2]; Push 1 → [2, 1]; Pop → [2]; Push 3 → [2, 3]; Pop → [2]; Pop → []; Pop on an empty stack → underflow.

**Concept: overflow and underflow.** Overflow = pushing onto a full stack (capacity reached). Underflow = popping from an empty one. Implementations check `top == -1` before popping.

{{< /details >}}

### 10 · Q32, incorrect statement about stacks

*Asked by: Qualcomm (HirePro, Aug 2025)*

Which one of the given options is incorrect about stacks?

- **(a)** Balancing of symbols is one of the applications of stacks.
- **(b)** Stack is said to be in underflow state if it is empty.
- **(c)** Stacks can be implemented using both array and trees.
- **(d)** TOP equal to zero implies only one element in the stack.

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c)** is incorrect

**Why.** Stacks are implemented with arrays or linked lists, not trees. (a) Bracket balancing is a classic stack application. (b) An empty stack cannot be popped (underflow). (d) With the usual convention top = −1 for empty, top = 0 means exactly one element.

**Concept: stack applications.** Matching brackets, undo, function calls (the call stack), expression evaluation and conversion, DFS, backtracking.

{{< /details >}}

### 11 · Data Structures Basics

*Asked by: Qualcomm (60-question online assessment)*

A doubly linked list is `A <-> X <-> Y <-> B -> NULL`. Three steps are applied in order:

1. Insert a new node **P** with `prev = NULL` and `next = current head`.
2. The **3rd node's** `next` is set to **B**, and **B's** `prev` is set to **X**.
3. Insert a new node **M** with `prev = B` and `next = NULL`.

What is the order of the elements?

- **(a)** A → P → X → Y → M
- **(b)** P → A → X → B → M
- **(c)** A → X → Y → M → P
- **(d)** P → A → Y → B → M

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) P → A → X → B → M**

**Why.** Step 1 puts P before A as the new head. Step 2 makes the 3rd node (X, counting P, A, X) point to B and B's prev point to X, bypassing Y. Step 3 appends M after B.

**Concept: doubly linked list updates.** Each node has `prev` and `next`. Removing or bypassing a node means fixing both directions: the previous node's `next` and the following node's `prev`.

{{< /details >}}

### 12 · Data Structures Basics

*Asked by: Qualcomm (60-question online assessment)*

Queue Q of size 5 containing: A P Q. What will be the queue after: Enqueue(J), Dequeue(), Enqueue(M), Enqueue(D), Enqueue(X)?

- **(a)** M D P Q J _
- **(b)** _ A P Q J D
- **(c)** _ M P Q J D
- **(d)** Overflow

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) overflow**

**Why.** In a linear queue of size 5: A P Q → enqueue J → A P Q J (rear at slot 4) → dequeue removes A (front moves on, but the slot is not reused) → enqueue M fills slot 5 → enqueue D: rear is already at the last slot, so overflow. (Even counting only live elements, P Q J M D is 5, and X would overflow.)

**Concept: linear queue limits.** Rear only moves forward. Once it reaches the end, further enqueues overflow even if dequeued slots at the front are free. A circular queue avoids this.

{{< /details >}}

### 13 · Data Structures

*Asked by: Qualcomm (60-question online assessment)*

Which of the given options is true about the singly linked list?

- **(a)** The reference part of the last node in the singly linked list must be NULL.
- **(b)** No node can be inserted in the middle of the singly linked list.
- **(c)** Using singly linked list, trees and graphs cannot be created.
- **(d)** The address of the first node is always stored in a reference node of the previous node.

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) the last node's reference must be NULL**

**Why.** The tail's `next` is NULL to mark the end. Inserting in the middle is possible (b false); trees and graphs are built from linked nodes (c false); the head has no previous node (d false).

**Concept: singly linked lists.** Each node stores data and a pointer to the next. You reach any node by walking from the head; NULL marks the end.

{{< /details >}}

### 14 · deleting from a circular list

*Asked by: Texas Instruments (IIT ISM 2024)*

To delete `cur` (with predecessor `prev`) from a circular list with `head`:

{{< details title="Answer and explanation" closed="true" >}}

**Answer: `prev->next = cur->next;` (and if `cur == head`, move `head` to `cur->next`), then free `cur`.**

**Why.** Linking the predecessor directly to the successor removes `cur` from the cycle. If `cur` was the head, the head pointer must move too, or it would point at freed memory. (If it was the only node, the list becomes empty.)

**Concept: deleting from a circular list.** Same as a normal list, but there is no NULL end, so be careful with the head and with the one-node case (`cur->next == cur`).

{{< /details >}}

### 15 · detecting a loop

*Asked by: Texas Instruments (IIT ISM 2024)*

How do you detect a loop in a linked list?

{{< details title="Answer and explanation" closed="true" >}}

**Answer: Floyd's cycle-finding algorithm** (slow and fast pointers)

**Why.** Move one pointer one step and another two steps at a time. If there is a loop, the fast pointer eventually catches the slow one inside it; if fast reaches NULL, there is no loop. O(n) time, O(1) space. (A hash set of visited nodes also works, with O(n) space.)

**Concept: why the pointers must meet.** Inside the loop the fast pointer gains one step per move on the slow one, so the gap shrinks by 1 each move until it is 0. To find the loop's start, reset one pointer to the head and move both one step at a time; they meet at the start.

{{< /details >}}

### 16 · a queue and a stack

*Asked by: Texas Instruments (IISc, second set)*

```cpp
q.enqueue(3);
q.enqueue(5);
q.enqueue(2);
s.push(q.dequeue());
s.push(q.dequeue());
s.pop();
```

{{< details title="Answer and explanation" closed="true" >}}

**Answer: `q.front()` is 2 and `s.top()` is 3**

**Why.** Queue after enqueues: [3, 5, 2]. Dequeue 3 → push → s = [3]. Dequeue 5 → push → s = [3, 5]. Pop → s = [3]. The queue now holds [2].

**Concept: FIFO vs LIFO.** The queue gives back the oldest element; the stack gives back the newest. Track both containers step by step.

{{< /details >}}

### 17 · Q15, stack from queues

*Asked by: Warner Bros. Discovery (HireVue, Nov 2024)*

For a stack with $n$ elements, would it be unfeasible to implement stack operations on
queues in the case of a large dataset?

- **(a)** Yes, because of its time complexity $O(n)$
- **(b)** Yes, because of its time complexity $O(\log n)$
- **(c)** Yes, because extra memory is required
- **(d)** No, it should be feasible

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) No, it is feasible**

**Why.** With two queues (or one queue rotated), one of push or pop costs O(n) and the other O(1). That is slower than a native stack but workable, and it uses O(n) memory, the same as the data itself.

**Concept: stack from queues.** To pop the newest item from a FIFO structure, move the other n − 1 items around it. Interviews ask this to test understanding of both structures, not as a practical design.

{{< /details >}}

### 18 · Q25, linked list versus array

*Asked by: Warner Bros. Discovery (HireVue, Nov 2024)*

Which of the following points is/are true about the linked list data structure when
compared with an array?

- **(a)** It is easy to insert and delete elements in Linked List
- **(b)** Random access is not allowed in a typical implementation of Linked Lists
- **(c)** The size of array has to be pre-decided, linked lists can change their size any time.
- **(d)** All of the above

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) all of the above**

**Why.** Inserting or deleting at a known node needs no shifting (a). Getting the k-th element needs a walk from the head (b). Nodes are allocated one at a time, so the list grows and shrinks freely (c).

**Concept: arrays vs linked lists.** Arrays: contiguous, O(1) index access, cache-friendly, costly inserts. Linked lists: scattered nodes, O(n) access, cheap inserts/deletes, extra memory for pointers.

{{< /details >}}

### 19 · Q7, stack as a linked list

*Asked by: Warner Bros. Discovery (HireVue, Nov 2024)*

Which of the following is true about a linked-list implementation of a stack?

- **(a)** In push operation, if new nodes are inserted at the beginning of the linked list, then in pop operation, nodes must be removed from the end.
- **(b)** In push operation, if new nodes are inserted at the end, then in pop operation, nodes must be removed from the beginning.
- **(c)** Both of the above
- **(d)** None of the above

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) none of the above**

**Why.** A stack is LIFO, so pop must remove from the **same** end that push inserts at, normally the head (O(1) both ways). (a) and (b) push and pop at opposite ends, which is a queue.

**Concept: linked-list stack.** Push = insert at head; pop = remove head. Both O(1), no capacity limit.

{{< /details >}}
