---
title: "3 · Arrays and strings"
linkTitle: "3 Arrays and strings"
weight: 3
math: true
---
## 3.1 Static arrays {#sec-dsa-static}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> `a[i]` costs the same for $i = 0$ and $i = 10^6$: one multiply, one add, one load.</em>

</div>

<div class="nb nb-definition" id="definition-3-1-1">

<strong>Definition 3.1.1</strong>. An <strong>array</strong> stores $n$ elements of equal size $s$ in one contiguous block. Element $i$ lives at address $\text{base} + i \cdot s$, so <strong>random access</strong> by index is $\Theta(1)$.

</div>

| Operation | Cost | Why |
|:--|:--|:--|
| Read / write `a[i]` | $\Theta(1)$ | address arithmetic |
| Search an unsorted array | $\Theta(n)$ | scan |
| Search a sorted array | $\Theta(\log n)$ | binary search |
| Insert / delete at the end (with spare capacity) | $\Theta(1)$ | nothing moves |
| Insert / delete at position $i$ | $\Theta(n - i)$ | shift the tail |
| Insert at the front | $\Theta(n)$ | shift everything |

<div class="nb-caption" id="table-3-1">

<strong>Table 3.1.</strong> Costs of array operations.

</div>

### 3.1.i Multi-dimensional arrays and address calculation {#s3-1-i}

<div class="nb nb-definition" id="definition-3-1-2">

<strong>Definition 3.1.2</strong>. A two-dimensional array $A[R][C]$ is stored either <strong>row-major</strong> (rows one after another: C, C++, Python’s NumPy default, Java’s arrays of arrays row by row) or <strong>column-major</strong> (columns one after another: Fortran, MATLAB, R, Julia).

</div>

<div class="nb nb-definition" id="fact-3-1-3">

<strong>Fact 3.1.3</strong> (Address formulas). With base address $B$, element size $s$, and indices starting at lower bounds $L_r$ and $L_c$:

$$
\begin{align*}
		\text{row-major:}\quad & \operatorname{addr}(A[i][j]) = B + \big((i - L_r)\,C + (j - L_c)\big)\, s, \\
		\text{column-major:}\quad & \operatorname{addr}(A[i][j]) = B + \big((j - L_c)\,R + (i - L_r)\big)\, s.
	\end{align*}
$$

For three dimensions $A[X][Y][Z]$ in row-major order, the offset of $A[i][j][k]$ is $(i\,YZ + j\,Z + k)\,s$.

</div>

The program checks the row-major formula on a real $4 \times 6$ array of `int`:

```cpp {filename="address.cpp"}
// Where does a[i][j] live? Byte offsets from a[0][0] for a 4 x 6 array of int.
#include <initializer_list>
#include <cstdio>

int a[4][6];

int main() {
    const char* base = (const char*)&a[0][0];
    std::printf("sizeof(int) = %u, sizeof a = %u, sizeof a[0] = %u\n",
        (unsigned)sizeof(int), (unsigned)sizeof a, (unsigned)sizeof a[0]);
    for (int i : {0, 1, 2, 3})
        for (int j : {0, 5})
            std::printf("a[%d][%d] at offset %3d   formula (i*6 + j)*4 = %3d\n",
                i, j, (int)((const char*)&a[i][j] - base), (i * 6 + j) * 4);
}
```

```text {filename="Output of address.cpp"}
sizeof(int) = 4, sizeof a = 96, sizeof a[0] = 24
a[0][0] at offset   0   formula (i*6 + j)*4 =   0
a[0][5] at offset  20   formula (i*6 + j)*4 =  20
a[1][0] at offset  24   formula (i*6 + j)*4 =  24
a[1][5] at offset  44   formula (i*6 + j)*4 =  44
a[2][0] at offset  48   formula (i*6 + j)*4 =  48
a[2][5] at offset  68   formula (i*6 + j)*4 =  68
a[3][0] at offset  72   formula (i*6 + j)*4 =  72
a[3][5] at offset  92   formula (i*6 + j)*4 =  92
```

<div class="nb nb-example nb-block" id="example-3-1-4">

<strong>Example 3.1.4</strong> (An OA-style address numerical)

$A[-5..4][10..19]$ of $4$-byte elements, row-major, starts at address $1000$. Where is $A[0][15]$? There are $C = 10$ columns. The offset is $((0 - (-5))\cdot 10 + (15 - 10)) \cdot 4 = 55 \cdot 4 = 220$, so the address is $1220$. In column-major order with $R = 10$ rows it would be $((15 - 10) \cdot 10 + (0 + 5)) \cdot 4 = 220$ too: a coincidence of the square shape. For $A[-5..4][10..14]$ ($R = 10$ rows, $C = 5$ columns) and the element $A[0][12]$, row-major gives $1000 + (5 \cdot 5 + 2) \cdot 4 = 1108$ and column-major gives $1000 + (2 \cdot 10 + 5) \cdot 4 = 1100$.

</div>

<div class="nb nb-remark" id="remark-3-1-5">

<strong>Remark 3.1.5</strong> (Locality decides speed) — Memory is fetched in cache lines of typically $64$ bytes. Traversing a row-major matrix row by row touches consecutive addresses (one miss per $16$ `int`s); traversing it column by column jumps $C \cdot s$ bytes each step and can miss on every access. Same $\Theta(RC)$ operations, often several times slower. Loop order matters in matrix multiplication for the same reason.

</div>

<div class="nb nb-remark" id="remark-3-1-6">

<strong>Remark 3.1.6</strong> (Special matrices) — A lower-triangular $n \times n$ matrix stored row by row needs $n(n+1)/2$ cells, and element $(i, j)$ with $j \le i$ (0-based) is at offset $i(i+1)/2 + j$. A sparse matrix with $k$ nonzeros is stored as $(i, j, v)$ triplets ($\Theta(k)$ space) or in compressed sparse row form.

</div>

## 3.2 Dynamic arrays {#sec-dsa-dynarray}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> `std::vector`, Java’s `ArrayList`, Python’s `list`.</em>

</div>

<div class="nb nb-definition" id="definition-3-2-1">

<strong>Definition 3.2.1</strong>. A <strong>dynamic array</strong> keeps a <strong>size</strong> $\le$ <strong>capacity</strong>. Appending into spare capacity is $\Theta(1)$; appending when full allocates a block $\gamma$ times larger ($\gamma = 2$ in libstdc++, $1.5$ in MSVC), copies or moves the elements and frees the old block.

</div>

Appending is $O(1)$ <em>amortized</em> and $\Theta(n)$ in the worst single case; the proof and the measured copy count are in [Section 1.4](../01-complexity/#sec-dsa-amortized).

<div class="nb nb-remark" id="remark-3-2-2">

<strong>Remark 3.2.2</strong> (Interview follow-ups) —

- `reserve(n)` pre-allocates and makes $n$ appends truly $O(1)$ each.
- Growing moves the elements, so every pointer, reference and iterator into the vector is invalidated ([Chapter 11](../11-containers/)).
- Inserting in the middle is still $\Theta(n)$: dynamic only means resizable.
- Python’s `list.append` and Java’s `ArrayList.add` are the same structure.

</div>

## 3.3 Strings {#sec-dsa-strings}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> building a string with `s = s + c` in a loop is $\Theta(n^2)$ in Java and Python.</em>

</div>

<div class="nb nb-definition" id="definition-3-3-1">

<strong>Definition 3.3.1</strong>. A string is an array of characters. A C string ends with the `'\0'` terminator, so `strlen` is $\Theta(n)$. `std::string`, Java’s `String` and Python’s `str` store their length, so `size()` is $\Theta(1)$.

</div>

<div class="nb nb-definition" id="fact-3-3-2">

<strong>Fact 3.3.2</strong> (Mutability). Java and Python strings are <strong>immutable</strong>: every concatenation builds a new string, so appending $n$ characters one at a time costs $1 + 2 + \cdots + n = \Theta(n^2)$. Use `StringBuilder` or `''.join(parts)`, which are dynamic arrays ($\Theta(n)$ total). `std::string` is mutable, and `s += c` is amortized $O(1)$; `s = s + c` still builds a temporary copy and is $\Theta(n)$ per step.

</div>

<div class="nb nb-definition" id="fact-3-3-3">

<strong>Fact 3.3.3</strong> (Costs of common string operations). Comparing two strings is $O(\min(|s|, |t|))$, so sorting $n$ strings of length $L$ costs $O(L \cdot n \log n)$. A substring copy is $\Theta(\text{length})$. Hashing a string is $\Theta(|s|)$ (cached once in Java). Naive pattern search is $O(nm)$.

</div>

<div class="nb nb-remark" id="remark-3-3-4">

<strong>Remark 3.3.4</strong> (Small-string optimisation) — Most `std::string` implementations keep short strings (up to $15$ characters in libstdc++ and MSVC) inside the object itself, so they need no heap allocation; moving such a string copies its characters.

</div>

<div class="nb nb-moral">

Arrays win on locality and $\Theta(1)$ indexing and lose on insertion in the middle; that single trade-off drives the choice between almost every pair of containers.

</div>

## 3.4 A few harder problems to think about {#s3-4}

<div class="nb nb-problem nb-block" id="problem-3a">

<strong>Problem 3A</strong> (Column-major address)

$A[1..20][1..30]$ of $8$-byte elements is stored column-major from address $4000$. Find the address of $A[5][12]$.

<details class="nb-hint">
<summary>Hint</summary>

In column-major order the row index moves fastest; there are $R = 20$ rows.

</details>

<details class="nb-sol">
<summary>Solution</summary>

Offset $= ((12 - 1)\cdot 20 + (5 - 1)) \cdot 8 = 224 \cdot 8 = 1792$, so the address is $5792$.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-3b">

<strong>Problem 3B</strong> (Three dimensions)

`int a[3][4][5]` (row-major, $4$-byte `int`) starts at address $0$. What is the byte offset of `a[2][1][3]`?

<details class="nb-hint">
<summary>Hint</summary>

The offset in elements is $i\cdot 4\cdot 5 + j \cdot 5 + k$.

</details>

<details class="nb-sol">
<summary>Solution</summary>

$(2\cdot 20 + 1 \cdot 5 + 3)\cdot 4 = 48 \cdot 4 = 192$.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-3c">

<strong>Problem 3C</strong> (Rotate in place)

Rotate an array of $n$ elements left by $k$ positions in $O(n)$ time and $O(1)$ extra space.

<details class="nb-hint">
<summary>Hint</summary>

Three reversals.

</details>

<details class="nb-sol">
<summary>Solution</summary>

Reverse the first $k$ elements, reverse the remaining $n - k$, then reverse the whole array. Each element moves a constant number of times: $\Theta(n)$ time, $\Theta(1)$ space.

</details>

</div>
