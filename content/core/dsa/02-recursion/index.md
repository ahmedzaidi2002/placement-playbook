---
title: "2 · Recursion, divide and conquer, backtracking"
linkTitle: "2 Recursion"
weight: 2
math: true
---
## 2.1 Recursion {#dsa-2-1}

A recursive function solves a problem by calling itself on smaller inputs. It needs:

1. **Base case(s)** that stop the recursion.
2. **Progress** towards the base case on every call.

Each call gets a **stack frame** (parameters, locals, return address), so recursion depth = stack space; too deep → **stack overflow**. **Tail recursion** (the recursive call is the last action) can be turned into a loop.

<div class="nb nb-example">

<strong>Example</strong> (Counting calls)

Naive Fibonacci $F(n) = F(n-1) + F(n-2)$ makes about $1.6^n$ calls (it recomputes the same values); $F(30)$ needs over a million calls. **Memoisation** (store each answer) cuts it to $O(n)$: this is dynamic programming (chapter 11).

</div>

## 2.2 Divide and conquer {#dsa-2-2}

**Divide** the problem into smaller pieces, **conquer** them recursively, **combine** the answers.

| Algorithm | Divide | Combine | Time |
|---|---|---|---|
| Binary search | look at one half | nothing | $O(\log n)$ |
| Merge sort | split in half | merge two sorted halves | $O(n \log n)$ |
| Quicksort | partition around a pivot | nothing | $O(n \log n)$ average |
| Counting inversions | merge sort, counting cross pairs while merging | add counts | $O(n \log n)$ |
| Karatsuba multiplication | 3 half-size products instead of 4 | shifts and adds | $O(n^{1.585})$ |
| Strassen matrix multiplication | 7 half-size products instead of 8 | additions | $O(n^{2.81})$ |
| Closest pair of points | split by x | check a strip of width $2d$ | $O(n \log n)$ |

## 2.3 Backtracking {#dsa-2-3}

Build a solution step by step; as soon as a partial solution cannot lead to a valid answer, **undo the last choice** and try the next one. It is a depth-first search over the tree of choices, with **pruning**.

- Classic problems: **N-Queens**, Sudoku, generating subsets ($2^n$), permutations ($n!$), combination sum, word search in a grid, rat in a maze, graph colouring.
- Template: choose → explore (recurse) → un-choose.
- Worst case stays exponential; pruning is what makes it practical.

<div class="nb nb-example">

<strong>Example</strong> (N-Queens, 4 × 4)

Place one queen per row. Row 1, column 1 → row 2 can only use column 3 or 4 → … dead ends force backtracking until the solution (2, 4, 1, 3) is found (queen in column 2 of row 1, column 4 of row 2, and so on). 4-Queens has exactly 2 solutions; 8-Queens has 92.

</div>

<div class="nb nb-moral">

Recursion needs a base case and progress; depth = stack space. Divide and conquer splits, solves, combines. Backtracking = DFS over choices, undoing a choice as soon as it cannot succeed.

</div>
