---
title: "5 · Stacks and queues"
linkTitle: "5 Stacks and queues"
weight: 5
math: true
---
## 5.1 Stacks {#sec-dsa-stack}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> the browser’s Back button, the call stack, undo.</em>

</div>

<div class="nb nb-definition" id="definition-5-1-1">

<strong>Definition 5.1.1</strong>. A <strong>stack</strong> is a LIFO (last in, first out) collection with `push` (add on top), `pop` (remove the top) and `top`/`peek`. A <strong>queue</strong> is FIFO (first in, first out) with `enqueue` at the rear and `dequeue` at the front. A <strong>deque</strong> (double-ended queue) allows both at both ends.

</div>

<div class="nb nb-definition" id="fact-5-1-2">

<strong>Fact 5.1.2</strong> (Implementations).

- Stack on a dynamic array: push/pop at the end, $O(1)$ amortized, best locality.
- Stack on a singly linked list: push/pop at the head, $O(1)$ worst case.
- Queue on a singly linked list with head and tail pointers: enqueue at the tail, dequeue at the head, $O(1)$.
- Queue on an array: a <em>circular</em> buffer (below); the naive version that shifts every element on dequeue is $\Theta(n)$ per operation.

</div>

## 5.2 The circular queue {#sec-dsa-circular}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> a fixed buffer of $n$ cells between a producer and a consumer.</em>

</div>

<div class="nb nb-definition" id="definition-5-2-1">

<strong>Definition 5.2.1</strong>. A <strong>circular queue</strong> stores elements in `a[0..n-1]` with indices `front` and `rear` that advance modulo $n$: enqueue writes `a[rear]` and sets `rear = (rear + 1) % n`; dequeue reads `a[front]` and sets `front = (front + 1) % n`.

</div>

<div class="nb nb-definition" id="fact-5-2-2">

<strong>Fact 5.2.2</strong> (Full or empty?). With only `front` and `rear`, “empty” and “full” both look like `front == rear`. The standard fixes:

1. leave one cell unused: empty iff `front == rear`, full iff `(rear + 1) % n == front`; capacity $n - 1$;
2. keep a separate `count`: empty iff `count == 0`, full iff `count == n`;
3. in the convention where `rear` points <em>at</em> the last element (and starts at $-1$ or at `front - 1`), full is `(rear + 2) % n == front` with one cell unused.

The number of elements in convention 1 is `(rear - front + n) % n`.

</div>

<div class="nb nb-example nb-block" id="example-5-2-3">

<strong>Example 5.2.3</strong> (An OA trace)

$n = 5$, one cell unused, `front = rear = 0`. Enqueue A, B, C, D: `rear` becomes $4$, and the queue is full since $(4 + 1) \bmod 5 = 0 =$ `front`. Dequeue twice: `front = 2`. Enqueue E, F: E goes to cell $4$, `rear` wraps to $0$; F goes to cell $0$, `rear = 1`. Now `(1 + 1) % 5 = 2 = front`: full again, holding C, D, E, F.

</div>

## 5.3 Stacks and queues simulating each other {#sec-dsa-twostacks}

<div class="nb nb-definition" id="fact-5-3-1">

<strong>Fact 5.3.1</strong>.

- <em>Queue from two stacks</em>: push onto `in`; to dequeue, if `out` is empty pour all of `in` into `out`, then pop `out`. Each element is moved at most twice, so every operation is $O(1)$ amortized ($\Theta(n)$ worst case for one dequeue).
- <em>Stack from two queues</em>: on push, enqueue into the empty queue and move all elements of the other queue behind it; push $\Theta(n)$, pop $O(1)$ (or the reverse trade-off). One queue is enough: after enqueueing, rotate the previous $n - 1$ elements to the back.
- <em>Min-stack</em>: store with each element the minimum of the stack below it; `getMin` in $O(1)$.

</div>

## 5.4 Expressions: infix, postfix, prefix {#sec-dsa-expressions}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> a calculator turning `a+b*c` into `abc*+` and then evaluating it with one stack.</em>

</div>

<div class="nb nb-definition" id="definition-5-4-1">

<strong>Definition 5.4.1</strong>. In <strong>infix</strong> notation the operator sits between its operands and needs precedence, associativity and parentheses. In <strong>postfix</strong> (reverse Polish) notation it follows them (`ab+`), in <strong>prefix</strong> (Polish) notation it precedes them (`+ab`). Postfix and prefix need no parentheses.

</div>

<div class="nb nb-remark" id="algorithm-5-4-2">

<strong>Algorithm 5.4.2</strong> (Infix to postfix with an operator stack (Dijkstra’s shunting yard)) — Scan left to right. Operands go straight to the output. `(` is pushed. On `)`, pop to the output until the matching `(`. On an operator $o$, pop to the output every operator on top that has higher precedence, or equal precedence when $o$ is left-associative, then push $o$. At the end pop everything. $\Theta(n)$.

</div>

```cpp {filename="infix.cpp"}
// Infix -> postfix with an operator stack (shunting yard), then evaluate a postfix expression.
#include <cctype>
#include <cstdio>
#include <string>
#include <vector>

int prec(char op) { return op == '^' ? 3 : (op == '*' || op == '/') ? 2 : (op == '+' || op == '-') ? 1 : 0; }
bool rightAssoc(char op) { return op == '^'; }

std::string toPostfix(const std::string& s, bool trace) {
    std::string out, st;                                // st is the operator stack
    for (char c : s) {
        if (std::isalnum((unsigned char)c)) out += c;
        else if (c == '(') st += c;
        else if (c == ')') { while (st.back() != '(') { out += st.back(); st.pop_back(); } st.pop_back(); }
        else {
            while (!st.empty() && st.back() != '(' &&
                   (prec(st.back()) > prec(c) || (prec(st.back()) == prec(c) && !rightAssoc(c)))) {
                out += st.back(); st.pop_back();
            }
            st += c;
        }
        if (trace) std::printf("  read %c   stack %-8s output %s\n", c, st.c_str(), out.c_str());
    }
    while (!st.empty()) { out += st.back(); st.pop_back(); }
    return out;
}

int main() {
    std::printf("a+b*(c^d-e)^(f+g*h)-i\n");
    std::string p = toPostfix("a+b*(c^d-e)^(f+g*h)-i", true);
    std::printf("postfix: %s\n", p.c_str());
    std::printf("a^b^c -> %s,  a-b-c -> %s,  (a+b)*(c-d)/e -> %s\n",
        toPostfix("a^b^c", false).c_str(), toPostfix("a-b-c", false).c_str(), toPostfix("(a+b)*(c-d)/e", false).c_str());
    // evaluate the postfix expression 6 2 3 + - 3 8 2 / + * 2 ^ 3 +
    std::vector<std::string> tok = {"6", "2", "3", "+", "-", "3", "8", "2", "/", "+", "*", "2", "^", "3", "+"};
    std::vector<long> st;
    std::printf("evaluate 6 2 3 + - 3 8 2 / + * 2 ^ 3 +\n");
    for (auto& t : tok) {
        if (std::isdigit((unsigned char)t[0])) st.push_back(std::stol(t));
        else {
            long b = st.back(); st.pop_back();
            long a = st.back(); st.pop_back();
            long r = t == "+" ? a + b : t == "-" ? a - b : t == "*" ? a * b : t == "/" ? a / b : 1;
            if (t == "^") for (long i = 0; i < b; ++i) r *= a;
            st.push_back(r);
        }
        std::printf("  %-2s stack:", t.c_str());
        for (long v : st) std::printf(" %ld", v);
        std::printf("\n");
    }
}
```

```text {filename="Output of infix.cpp"}
a+b*(c^d-e)^(f+g*h)-i
  read a   stack          output a
  read +   stack +        output a
  read b   stack +        output ab
  read *   stack +*       output ab
  read (   stack +*(      output ab
  read c   stack +*(      output abc
  read ^   stack +*(^     output abc
  read d   stack +*(^     output abcd
  read -   stack +*(-     output abcd^
  read e   stack +*(-     output abcd^e
  read )   stack +*       output abcd^e-
  read ^   stack +*^      output abcd^e-
  read (   stack +*^(     output abcd^e-
  read f   stack +*^(     output abcd^e-f
  read +   stack +*^(+    output abcd^e-f
  read g   stack +*^(+    output abcd^e-fg
  read *   stack +*^(+*   output abcd^e-fg
  read h   stack +*^(+*   output abcd^e-fgh
  read )   stack +*^      output abcd^e-fgh*+
  read -   stack -        output abcd^e-fgh*+^*+
  read i   stack -        output abcd^e-fgh*+^*+i
postfix: abcd^e-fgh*+^*+i-
a^b^c -> abc^^,  a-b-c -> ab-c-,  (a+b)*(c-d)/e -> ab+cd-*e/
evaluate 6 2 3 + - 3 8 2 / + * 2 ^ 3 +
  6  stack: 6
  2  stack: 6 2
  3  stack: 6 2 3
  +  stack: 6 5
  -  stack: 1
  3  stack: 1 3
  8  stack: 1 3 8
  2  stack: 1 3 8 2
  /  stack: 1 3 4
  +  stack: 1 7
  *  stack: 7
  2  stack: 7 2
  ^  stack: 49
  3  stack: 49 3
  +  stack: 52
```

<div class="nb nb-remark" id="remark-5-4-3">

<strong>Remark 5.4.3</strong> (Associativity is the trap) — `^` is right-associative, so `a^b^c` means `a^(b^c)` and becomes `abc^^`: reading the second `^` pops nothing, because an equal-precedence right-associative operator stays on the stack. `-` is left-associative, so `a-b-c` becomes `ab-c-`: the second `-` pops the first. In the trace, reading the final `-` pops `^`, `*` and `+`, all of precedence at least that of `-`.

</div>

<div class="nb nb-remark" id="algorithm-5-4-4">

<strong>Algorithm 5.4.4</strong> (Evaluating postfix) — Scan left to right; push operands; on an operator pop $b$ (the top) and then $a$, push $a \circ b$. The order matters for `-`, `/` and `\^`. The trace above evaluates `6 2 3 + - 3 8 2 / + * 2 ^ 3 +` to $52$; the maximum stack depth was $4$.

</div>

<div class="nb nb-definition" id="fact-5-4-5">

<strong>Fact 5.4.5</strong> (Prefix). To convert infix to prefix, reverse the infix string, swap `(` and `)`, convert to postfix (treating equal precedence as <em>right</em>-associative for left-associative operators), and reverse the result. `(a+b)*(c-d)` becomes `*+ab-cd`. A prefix expression is evaluated by scanning right to left with the same stack algorithm, popping $a$ first. An <strong>expression tree</strong> ([Section 6.6](../06-trees/#sec-dsa-exprtree)) gives all three: its preorder, inorder and postorder traversals.

</div>

## 5.5 Other stack applications {#s5-5}

<div class="nb nb-definition" id="fact-5-5-1">

<strong>Fact 5.5.1</strong>.

- <em>Balanced brackets</em>: push openers, pop on a closer and check the match; valid iff the stack is empty at the end. $\Theta(n)$.
- <em>Function calls and recursion</em> ([Section 2.1](../02-recursion/#sec-dsa-callstack)); DFS with an explicit stack.
- <em>Undo/redo</em>: two stacks.
- <em>Monotonic stack</em>: keep the stack increasing (or decreasing); popping on each new element gives the <em>next greater/smaller element</em> of every position in $\Theta(n)$ total, since each element is pushed and popped once. Used for the largest rectangle in a histogram, stock span and trapping rain water.

</div>

<div class="nb nb-definition" id="fact-5-5-2">

<strong>Fact 5.5.2</strong> (Queue and deque applications). BFS ([Section 16.1](../16-graphs/#sec-dsa-bfs)), level-order traversal, buffering and scheduling (round robin), and the <strong>monotonic deque</strong> for the <em>sliding-window maximum</em>: keep indices whose values are decreasing, pop from the back while the new value is larger and from the front when the index leaves the window; $\Theta(n)$ total.

</div>

## 5.6 Which permutations can a stack produce? {#sec-dsa-stackperm}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> push $1, 2, 3$ in order and pop at will: `3 1 2` is impossible.</em>

</div>

<div class="nb nb-theorem nb-block" id="theorem-5-6-1">

<strong>Theorem 5.6.1</strong>

Pushing $1, 2, \ldots, n$ in order onto a stack and popping at arbitrary times can produce exactly $C_n = \frac{1}{n+1}\binom{2n}{n}$ different output orders. An output is impossible iff it contains a pattern $\ldots c \ldots a \ldots b \ldots$ with $a < b < c$ (the “$312$” pattern).

</div>

The brute force in [Section 6.5](../06-trees/#sec-dsa-catalan) confirms $1, 2, 5, 14, 42, \ldots$ stack-permutations out of $n!$. For `3 1 2`: to output $3$ first we must push $1, 2, 3$; the top is then $2$, so $1$ cannot come next.

<div class="nb nb-moral">

A stack reverses and matches (brackets, recursion, operators); a queue preserves order (BFS, buffering). Most “design a structure” questions combine one of them with a hash map.

</div>

## 5.7 A few harder problems to think about {#s5-7}

<div class="nb nb-problem nb-block" id="problem-5a">

<strong>Problem 5A</strong> (Convert)

Convert `(a+b*c)/(d-e)^f^g` to postfix and to prefix.

<details class="nb-hint">
<summary>Hint</summary>

`^` is right-associative and binds tighter than `/`.

</details>

<details class="nb-sol">
<summary>Solution</summary>

The expression is `(a+(b*c)) / ((d-e)^(f^g))`. Postfix: `abc*+de-fg^^/`. Prefix: `/+a*bc^-de^fg`.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-5b">

<strong>Problem 5B</strong> (Circular queue state)

A circular queue of size $8$ uses the one-empty-cell convention. Starting empty with `front = rear = 0`, perform $6$ enqueues, $4$ dequeues and $5$ enqueues. What are `front`, `rear` and the number of elements? Did any enqueue fail?

<details class="nb-hint">
<summary>Hint</summary>

Capacity is $7$.

</details>

<details class="nb-sol">
<summary>Solution</summary>

After $6$ enqueues: `rear = 6`. After $4$ dequeues: `front = 4`, $2$ elements. Five enqueues bring `rear` to $(6 + 5) \bmod 8 = 3$ and the count to $7$ = capacity, so none failed, and now `(3 + 1) % 8 = 4 = front`: the queue is full.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-5c">

<strong>Problem 5C</strong> (Stack permutations)

Which of these can be produced by pushing $1..5$ in order and popping at will? (a) `3 2 5 4 1`; (b) `4 5 3 1 2`; (c) `1 2 3 4 5`; (d) `5 4 3 1 2`.

<details class="nb-hint">
<summary>Hint</summary>

Look for a $312$ pattern: a large value, then a small one, then a medium one.

</details>

<details class="nb-sol">
<summary>Solution</summary>

(a) and (c) are possible. (b) contains $4, 1, 2$; (d) contains $5, 1, 2$ (also $3, 1, 2$): after popping $1$, the element $2$ is buried under it in the stack order, so both are impossible.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-5d">

<strong>Problem 5D</strong> (Evaluate)

Evaluate the postfix expression `8 2 3 ^ / 2 3 * + 5 1 * -`.

<details class="nb-hint">
<summary>Hint</summary>

`2 3 ^` means $2^3$.

</details>

<details class="nb-sol">
<summary>Solution</summary>

$8 / 2^3 = 1$; $1 + 2 \cdot 3 = 7$; $7 - 5 \cdot 1 = 2$.

</details>

</div>
