---
title: 1 · C and data structures
weight: 1
---

TI's slide says: **Basic C programming: pointers, algorithms, stacks/queues.** NCG candidates also need **data structures up to basic graphs (BST, hashing, linked lists)**. Interns need **data structures up to linked lists**. Questions in TI papers are short: trace a piece of C, name the complexity, or fill in one missing line.

{{< callout type="info" >}}
**Intern?** Read Parts 1–4 and skip Part 5 (BST, hashing, graphs). Questions marked *NCG* in their title are the ones you can skip.
{{< /callout >}}

## Part 1 · Pointers

A **pointer** is a variable that holds an address. `int *p = &x;` means "p holds the address of x"; `*p` reads or writes x through it.

```c
int x = 10;
int *p = &x;   // p stores the address of x
*p = 20;       // x is now 20
int **pp = &p; // pointer to a pointer: **pp is x
```

**Pointer arithmetic moves in elements, not bytes.** If `p` is an `int *`, `p + 1` is 4 bytes ahead (one `int`); if it is a `double *`, 8 bytes ahead. Subtracting two pointers into the same array gives the number of elements between them.

**Arrays and pointers.** An array name turns into a pointer to its first element in most expressions, so `a[i]` is exactly `*(a + i)`. Two places it does *not* decay: `sizeof(a)` (gives the whole array's size) and `&a` (a pointer to the whole array).

```c
int a[4] = {10, 20, 30, 40};
int *p = a + 1;          // points at 20
printf("%d %d %d", *p + 1, *(p + 1), p[-1]);   // 21 30 10
```

**`const` with pointers.** Read the declaration right to left:

| Declaration | Read as | Can change `*p`? | Can change `p`? |
|---|---|:-:|:-:|
| `const int *p` (same as `int const *p`) | p is a pointer to a const int | no | yes |
| `int *const p` | p is a const pointer to int | yes | no |
| `const int *const p` | const pointer to const int | no | no |

**Function pointers.** `void (*fp)(int)` is a pointer to a function that takes an `int` and returns nothing. The brackets matter: `void *fp(int)` declares a *function* returning `void *`. Function pointers make **callbacks** possible (like the `compare` argument of `qsort`). TI's drivers use tables of them for interrupt handlers.

**Common pointer bugs** (TI likes "find the bug" questions):

- **Dangling pointer**: returning the address of a local variable; the local dies when the function returns.
- **Uninitialised pointer**: `int *p; *p = 5;` writes to a random address.
- **Memory leak**: `malloc` without `free`.
- **Off by one**: `char s[5] = "hello";` has no room for `'\0'`.

## Part 2 · Recursion and complexity

A recursive function needs a **base case** that stops it and a **step** that moves towards the base case. Each call gets its own stack frame, so recursion depth costs stack space. That matters on a microcontroller with 1–2 KB of stack.

**Counting operations** is enough for every complexity question seen in TI papers:

| Pattern | Count | Big-O |
|---|---|---|
| One loop over `n` | n | O(n) |
| Two nested loops over `n` | n² | O(n²) |
| `for i` then `for j = i+1..n` (all pairs) | n(n−1)/2 | O(n²) |
| Halve the range each step (binary search) | log₂ n | O(log n) |
| Split in half, do linear work, recurse (merge sort) | n log n | O(n log n) |

**Space**: count the extra memory the algorithm allocates, not the input. A loop with one moving pointer is O(1) extra space.

## Part 3 · Arrays, searching and sorting

- **Binary search** needs a sorted array. Compare with the middle; if `A[mid] > value`, search `low..mid-1`, else `mid+1..high`. O(log n).
- **Sliding window**: to find the best sum of `k` consecutive elements, add the element entering the window and subtract the one leaving. O(n) instead of O(nk).

| Sort | Best | Average | Worst | Extra space | Stable? | Note |
|---|---|---|---|---|:-:|---|
| Bubble | n | n² | n² | 1 | yes | |
| Insertion | n | n² | n² | 1 | yes | **Online**: can sort data as it arrives; fast on nearly sorted input |
| Selection | n² | n² | n² | 1 | no | fewest swaps |
| Merge | n log n | n log n | n log n | n | yes | good for linked lists |
| Quick | n log n | n log n | n² | log n | no | fastest in practice |
| Heap | n log n | n log n | n log n | 1 | no | |

## Part 4 · Stacks, queues and linked lists

**Stack**: last in, first out. `push` and `pop` at the top. Used for function calls, undo, bracket matching, and converting recursion into a loop.

**Queue**: first in, first out. `enqueue` at the rear, `dequeue` at the front. Used for buffers (a UART receive buffer is a **circular queue**), BFS, and scheduling.

A **circular queue** in an array keeps `front` and `rear` indices and wraps them with `% size`, so freed slots are reused. To tell full from empty, keep a count or leave one slot unused.

**Linked list**: nodes connected by `next` pointers. Insertion and deletion are O(1) once you are at the spot; finding the spot is O(n). No random access.

```c
struct Node { int v; struct Node *next; };

struct Node *reverse(struct Node *head) {   // tested: 1 2 3 -> 3 2 1
    struct Node *prev = NULL;
    while (head) {
        struct Node *nxt = head->next;   // save the rest
        head->next = prev;               // flip one link
        prev = head;                     // move both pointers forward
        head = nxt;
    }
    return prev;
}
```

**Detecting a loop (Floyd's cycle-finding)**: move `slow` one step and `fast` two steps. If they ever meet there is a loop; if `fast` hits `NULL` there is none. O(n) time, O(1) space.

**Circular linked list**: the last node points back to the head. Traversal uses `do { ... } while (temp != head);` so it visits the head once. Inserting at the **beginning** means: link the new node before head, make the last node point to it, then set `head = new`. Without the last step, the same code inserts at the **end**.

## Part 5 · BST, hashing and graphs (NCG)

**Binary search tree**: left subtree < node < right subtree. Search, insert and delete take O(h), where h is the height: O(log n) when balanced, O(n) when the input arrives sorted (the tree becomes a chain). **Inorder traversal of a BST gives the keys in sorted order.**

| Traversal | Order |
|---|---|
| Preorder | node, left, right |
| Inorder | left, node, right |
| Postorder | left, right, node |
| Level order | by depth, using a queue (BFS) |

**Hashing**: map a key to a slot with a hash function, for example `h(k) = k mod m`. Two keys landing in the same slot is a **collision**. Two ways to handle it:

- **Chaining**: each slot holds a linked list.
- **Open addressing**: look for another slot. *Linear probing* tries h, h+1, h+2, … (wrapping round).

Average O(1) lookup if the table is not too full. The **load factor** is n/m.

**Graphs**: vertices and edges. Store as an **adjacency matrix** (O(V²) space, O(1) edge check) or **adjacency list** (O(V + E) space, better for sparse graphs).

- **BFS** uses a queue and visits by distance. It finds shortest paths in unweighted graphs.
- **DFS** uses a stack (or recursion) and goes deep first. It is used for cycle detection and topological sort.
- **Kruskal's MST**: sort edges by weight and add the smallest edge that does not form a cycle, until V − 1 edges are chosen.
- **Dijkstra**: shortest paths with non-negative weights, using a min-heap.

{{< callout type="info" >}}
**Remember.** `a[i]` is `*(a + i)`. Pointer difference counts elements. Read `const` right to left. Floyd's algorithm detects loops in O(1) space. Insertion sort is the online sort. Inorder of a BST is sorted. Kruskal = sort edges and avoid cycles.
{{< /callout >}}

---

## Questions

### C1 · A recursive power

*TI · IIT BHU 2023*

```c
float WHATISIT(float x, int n) {
    if (n >= 1)
        return (n == 0) ? 1 : x * WHATISIT(x, n - 1);
    else
        return (n == 0) ? 1 : (1 / x) * WHATISIT(x, n + 1);
}
```

What do `WHATISIT(2, 3)` and `WHATISIT(0.5, -3)` return?

- **A.** 6, 1.5
- **B.** 4, .25
- **C.** 8, 8
- **D.** Endless loop

{{< details title="Show answer" closed="true" >}}
**Answer: C. 8, 8** (compiled and run). The function computes x<sup>n</sup>: for positive n it multiplies by x and steps n down; for negative n it multiplies by 1/x and steps n up. 2³ = 8 and 0.5⁻³ = 2³ = 8. Both branches reach n = 0, so there is no endless loop.
{{< /details >}}

### C2 · Filling an array through a pointer

*TI · BITS Pilani*

```c
int numbers[5];
int *p;
p = numbers;      *p = 10;
p++;              *p = 20;
p = &numbers[2];  *p = 30;
p = numbers + 3;  *p = 40;
p = numbers;      *(p + 4) = 50;
for (int n = 0; n < 5; n++) printf("%d,", numbers[n]);
```

{{< details title="Show answer" closed="true" >}}
**Output: `10,20,30,40,50,`** Each line reaches the next element a different way: `p++`, `&numbers[2]`, `numbers + 3`, and `*(p + 4)`. All of them are the same pointer arithmetic.
{{< /details >}}

### C3 · Function pointers

*TI · IISc 2023*

`void fun(int a)` prints its argument. Which of these, put in place of `XXX`, lets `(*fun_ptr)(10);` call `fun`?

1. `void (*fun_ptr)(int) = &fun;`
2. `void (*fun_ptr)(int); fun_ptr = &fun;`

- **A.** Only 1
- **B.** Only 2
- **C.** Both
- **D.** Neither

{{< details title="Show answer" closed="true" >}}
**Answer: C. Both.** One declares and initialises in one line; the other declares and then assigns. `&fun` and plain `fun` are the same here, because a function name decays to a pointer to it.
{{< /details >}}

### C4 · A generic search

*TI · IISc 2023*

A search function takes an array as `void *`, the element size, the key, and a callback `int compare(void *a, void *b)` that compares two `int`s. It searches for 7 in `{2, 5, 7, 90, 70}` and prints `"The index is %d"`. What is printed?

{{< details title="Show answer" closed="true" >}}
**"The index is 2".** The point of the question is the technique: with `void *` plus an element size plus a compare callback, one search function works for any type. This is the same idea as `qsort` and `bsearch` in the C library. Indices start at 0, so 7 is at index 2.
{{< /details >}}

### C5 · A string without a terminator

*TI · NIT Calicut 2023*

```c
char ABC[5] = "hello";
printf("%d", *(ABC + 4));
```

- **A.** 111
- **B.** 0
- **C.** Garbage value
- **D.** Runtime error

{{< details title="Show answer" closed="true" >}}
**Answer: A. 111** (compiled and run). `*(ABC + 4)` is `ABC[4]` = `'o'`, ASCII 111. C allows the initialiser to fill the array exactly and drops the `'\0'`, so `ABC` is not a valid string. Printing it with `%s` would run past the end, but this code only reads one character. (C++ rejects the declaration.)
{{< /details >}}

### C6 · Pointer difference

*MathWorks · IIT Bombay 2024*

```c
int x = 4;
int *p = &x;
int *k = p++;
int r = p - k;
printf("%d", r);
```

- **A.** 4
- **B.** 2
- **C.** 1
- **D.** 5

{{< details title="Show answer" closed="true" >}}
**Answer: C. 1.** `k` gets the old `p`, then `p` moves one `int` ahead. Pointer subtraction counts elements, not bytes, so the result is 1 (not 4).
{{< /details >}}

### C7 · A constant pointer

*MathWorks · IIT Bombay 2024*

Which declares a **constant pointer** to an `int`?

- **A.** `const int *p;`
- **B.** `int* const p;`
- **C.** `int const *p;`
- **D.** `int const *const p;`

{{< details title="Show answer" closed="true" >}}
**Answer: B.** Read right to left: "p is a const pointer to int". A and C are pointers to a const int (the pointer can move, the value cannot change through it). D is both const.
{{< /details >}}

### C8 · Pointer into the middle of an array

*Practice*

```c
int arr[] = {10, 20, 30, 40};
int *pp = arr + 1;
printf("%d %d %d", *pp + 1, *(pp + 1), pp[-1]);
```

{{< details title="Show answer" closed="true" >}}
**Output: `21 30 10`** (compiled and run). `*pp + 1` is (20) + 1 because `*` binds tighter than `+`. `*(pp + 1)` is the next element, 30. `pp[-1]` is `*(pp - 1)`, the element before, 10. Negative indices are legal as long as you stay inside the array.
{{< /details >}}

### C9 · Max of row minima

*TI · IIT BHU 2023*

For an n × n matrix, find the minimum of each row and then the largest of those minima. Time complexity?

- **A.** O(n)
- **B.** O(n log n)
- **C.** O(n²)
- **D.** O(n³)

{{< details title="Show answer" closed="true" >}}
**Answer: C. O(n²).** Every one of the n² entries must be read once to find the row minima; the final max over n values adds only O(n).
{{< /details >}}

### C10 · Reversing an array

*TI · IIT BHU 2023*

```c
for (i = 0, j = N - 1; i < j; i++, j--) {
    temp = A[i];
    A[i] = A[j];
    A[j] = temp;
}
```

Statement A: the code reverses the array. Statement B: it runs in linear time.

{{< details title="Show answer" closed="true" >}}
**Both are true.** Two pointers meet in the middle after N/2 swaps, so the work is O(N). (The loop header was garbled in the original screenshot; this is the standard form.)
{{< /details >}}

### C11 · Counting print calls

*TI · IIT BHU 2023*

```c
for (i = 1; i <= n - 1; i++)
    for (j = i + 1; j <= n; j++)
        print(i, j);
```

How many times is `print` called?

- **A.** n²
- **B.** n² − n
- **C.** (n² − n)/2
- **D.** n²/2

{{< details title="Show answer" closed="true" >}}
**Answer: C. (n² − n)/2.** One call per pair i < j, which is "n choose 2" = n(n − 1)/2. Check with n = 3: pairs (1,2), (1,3), (2,3) = 3 = (9 − 3)/2.
{{< /details >}}

### C12 · Binary search

*TI · IIT ISM 2024*

In a recursive binary search `binarySearch(A, value, low, high)`, if `A[mid] > value`, what should the next call be?

{{< details title="Show answer" closed="true" >}}
**`binarySearch(A, value, low, mid - 1)`**. The value can only be in the lower half. Using `mid` instead of `mid - 1` can loop forever when `low == mid`.
{{< /details >}}

### C13 · Sliding window

*TI · IIT ISM 2024*

What is the time complexity of finding the maximum sum of k consecutive elements with a sliding window?

{{< details title="Show answer" closed="true" >}}
**O(n).** Compute the first window's sum, then for each step add the entering element and subtract the leaving one: O(1) per step. The naive method that re-adds k elements each time is O(nk).
{{< /details >}}

### C14 · Merge sort variant

*TI · BITS Pilani*

A merge sort has base cases for n = 1 and n = 2 and a linear-time merge. Its complexity?

- **A.** O(n²)
- **B.** O(n³)
- **C.** O(n)
- **D.** None of these

{{< details title="Show answer" closed="true" >}}
**Answer: D. None of these.** It is still O(n log n): T(n) = 2T(n/2) + O(n). Extra base cases change only the constant.
{{< /details >}}

### C15 · Sorting while data arrive

*TI · IISc (second set)*

New elements may be added while the sort is still running. Which algorithm fits?

- **A.** Selection sort
- **B.** Merge sort
- **C.** Heap sort
- **D.** Insertion sort

{{< details title="Show answer" closed="true" >}}
**Answer: D. Insertion sort.** It is an **online** algorithm: it keeps a sorted prefix and inserts each new element into it, so it never needs the whole input up front.
{{< /details >}}

### C16 · A queue and a stack

*TI · IISc (second set)*

```c
q.enqueue(3);
q.enqueue(5);
q.enqueue(2);
s.push(q.dequeue());
s.push(q.dequeue());
s.pop();
```

What are `q.front()` and `s.top()` now?

{{< details title="Show answer" closed="true" >}}
**`q.front()` = 2 and `s.top()` = 3.** The queue gives 3 first, then 5; the stack holds 3, 5 with 5 on top. `pop` removes 5, leaving 3 on top. The queue still holds 2.
{{< /details >}}

### C17 · Printing a circular list

*TI · IIT BHU 2023*

What is the auxiliary space of this traversal?

```c
do {
    print(temp->data);
    temp = temp->next;
} while (temp != first);
```

- **A.** O(1)
- **B.** O(n)
- **C.** O(2n)
- **D.** None

{{< details title="Show answer" closed="true" >}}
**Answer: A. O(1).** Only one pointer, `temp`, is used, however long the list is.
{{< /details >}}

### C18 · What does `sample()` do?

*TI · BITS Pilani*

A new node `ptr` is added to a circular linked list. If the list is empty, `ptr` points to itself. Otherwise the code walks `temp` to the last node, then runs:

```c
ptr->next = head;
temp->next = ptr;
head = ptr;
```

- **A.** Insert at the beginning
- **B.** Insert at the end
- **C.** Search
- **D.** None

{{< details title="Show answer" closed="true" >}}
**Answer: A. Insert at the beginning**, because of the last line `head = ptr`. Without that line, the same two links would make it an insert at the end. Candidate keys say "insert at the end"; that is wrong.
{{< /details >}}

### C19 · Deleting from a circular list

*TI · IIT ISM 2024*

To delete node `cur`, whose predecessor is `prev`, from a circular list with head pointer `head`, which statements are needed?

{{< details title="Show answer" closed="true" >}}
**`prev->next = cur->next;`** and, if `cur == head`, also **`head = cur->next;`**, then `free(cur)`. If the list had only one node (`cur->next == cur`), set `head = NULL` instead. (Exact options were not captured.)
{{< /details >}}

### C20 · Detecting a loop

*TI · IIT ISM 2024* (also in TI's own prep slides)

How do you detect a loop in a linked list?

{{< details title="Show answer" closed="true" >}}
**Floyd's cycle-finding algorithm** (tortoise and hare): `slow` moves one node, `fast` moves two. They meet if and only if there is a loop. O(n) time, O(1) space. A hash set of visited nodes also works but costs O(n) space, which is expensive on embedded targets.
{{< /details >}}

### C21 · Reverse a linked list

*Practice*

Write a function that reverses a singly linked list in place and returns the new head. What are its time and space costs?

{{< details title="Show answer" closed="true" >}}
Use three pointers: `prev`, `head`, `nxt`. See the `reverse` function in Part 4 above (compiled and run: 1 → 2 → 3 becomes 3 → 2 → 1). **O(n) time, O(1) extra space.** The order inside the loop matters: save `head->next` before overwriting it.
{{< /details >}}

### C22 · Selling or splitting (NCG)

*TI · BITS Pilani*

A fruit worth n can be sold for n, or split into three fruits worth n/2, n/3 and n/4 (integer division), which can themselves be sold or split. Complete:

```c
int Solve(int n) {
    if (n == 0)
        return 0;
    return X;
}
```

{{< details title="Show answer" closed="true" >}}
**`X = max(n, Solve(n/2) + Solve(n/3) + Solve(n/4))`**. At each fruit, take the better of selling it whole or splitting it. Example: 12 → 6 + 4 + 3 = 13 > 12. For large n, memoise `Solve` so each value is computed once.
{{< /details >}}

### C23 · BST traversal (NCG)

*Practice*

Insert 50, 30, 70, 20, 40, 60, 80 into an empty BST in that order. Give the preorder and inorder traversals.

{{< details title="Show answer" closed="true" >}}
The tree is perfectly balanced: 50 at the root, 30 and 70 below it, then 20, 40, 60, 80 as leaves.

- **Preorder** (node, left, right): 50 30 20 40 70 60 80
- **Inorder** (left, node, right): 20 30 40 50 60 70 80, sorted as always for a BST

Had the keys arrived sorted (20, 30, …, 80), the tree would be a chain of height 7 and search would be O(n).
{{< /details >}}

### C24 · Hashing with linear probing (NCG)

*Practice*

A hash table has 7 slots, `h(k) = k mod 7`, and uses linear probing. Insert 50, 700, 76, 85, 92, 73, 101 in that order. Where does each key end up?

{{< details title="Show answer" closed="true" >}}
| Key | h(k) | Probes | Slot |
|---|---|---|---|
| 50 | 1 | — | 1 |
| 700 | 0 | — | 0 |
| 76 | 6 | — | 6 |
| 85 | 1 | 1 taken | 2 |
| 92 | 1 | 1, 2 taken | 3 |
| 73 | 3 | 3 taken | 4 |
| 101 | 3 | 3, 4 taken | 5 |

Final table, slots 0 to 6: **700, 50, 85, 92, 73, 101, 76**. Notice the **primary clustering**: keys pile up in one run, so later inserts probe longer.
{{< /details >}}

### C25 · Sort edges, avoid cycles (NCG)

*TI · BITS Pilani*

An algorithm repeatedly adds the smallest edge that does not form a cycle, until it has V − 1 edges. Which algorithm is it?

{{< details title="Show answer" closed="true" >}}
**Kruskal's minimum spanning tree algorithm.** Sorting the edges costs O(E log E); a union-find structure checks for cycles in near-constant time per edge. (Prim's grows one tree from a start vertex instead.)
{{< /details >}}

### C26 · TSP with an unreachable city (NCG)

*TI · IIT ISM 2024*

In the dynamic-programming solution of the travelling salesman problem, what happens if city k cannot be reached?

{{< details title="Show answer" closed="true" >}}
**The cost is infinite**: no valid tour exists, because a tour must visit every city. In code, unreachable edges are stored as a large "infinity" value, and the final answer stays infinity.
{{< /details >}}
