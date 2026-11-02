---
title: "MATLAB"
weight: 2
---

8 questions asked by MathWorks. Try each one first, then open the toggle: it gives the answer, why it is right, and the idea behind it explained from scratch.

### 1 · Q43, fixing MATLAB code

*Asked by: MathWorks (IISc 2024)*

Which changes fix this MATLAB code?

```matlab
x = 0; y = 0;
for k1 = 0:9
    x[k1] = k1*pi;
    for k2 = 9:-2:5
        y(k2) = k2;
    end
end
```

- **(a)** Preallocate x and y
- **(b)** Line 3: use k1 = 1:9
- **(c)** Line 4: use x(k1) = ...
- **(d)** Initialise pi
- **(e)** Line 5: use k2 = 5:2:9

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) and (c)**

**Why.** MATLAB arrays start at index 1, so `x(0)` is an error: loop from 1 (b). Indexing uses parentheses, not square brackets: `x(k1) = ...` (c). Preallocation only improves speed, `pi` is built in, and a descending loop like 9:−2:5 is legal.

**Concept: MATLAB indexing.** 1-based, with parentheses: `A(i, j)`. Square brackets build arrays (`[1 2 3]`); curly braces index cell arrays (`C{2}`).

{{< /details >}}

### 2 · Q44, undefined function

*Asked by: MathWorks (IISc 2024)*

MATLAB reports "Undefined function or variable `my_func`". Which will NOT resolve
the error?

- **(a)** Change the current folder to the folder that contains the file
- **(b)** Add the folder to the operating system path
- **(c)** Add the folder to the MATLAB path
- **(d)** Call the function with its full path

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) adding the folder to the operating system path**

**Why.** MATLAB looks for functions in the current folder and on its own search path, never on the OS `PATH`. Changing folder (a), adding to the MATLAB path (c) or calling by full path (d) all work.

**Concept: MATLAB search path.** Set with `addpath` / `savepath` or the "Set Path" dialog. The OS PATH is for finding executables, not MATLAB functions.

{{< /details >}}

### 3 · Q45, joining matrices

*Asked by: MathWorks (IISc 2024)*

`A<code> is &#36;3 &#92;times 3&#36; and </code>B` is $4 \times 3$. Which commands are valid? (select
all)

- **(a)** [A, B]
- **(b)** {A, B} (braces unclear in the photo)
- **(c)** [A; B]
- **(d)** horzcat(A, B)
- **(e)** vertcat(A, B)

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) `[A; B]` and (e) `vertcat(A, B)`** (and (b) `{A, B}` if that is what the option shows: a 1 × 2 cell array)

**Why.** A is 3 × 3 and B is 4 × 3: they have the same number of columns, so they stack vertically into 7 × 3. Side by side (`[A, B]`, `horzcat`) needs equal row counts, so it fails.

**Concept: concatenation rules.** `;` (vertical) needs equal column counts; `,` or space (horizontal) needs equal row counts. Cell arrays `{}` can hold anything, of any size.

{{< /details >}}

### 4 · Q46, nested functions

*Asked by: MathWorks (IISc 2024)*

What does `main` return?

```matlab
function x = main
    x = 0;
    nestfun1;
    function nestfun1
        x = 5;
    end
    x = x + 1;
end
```

- **(a)** 1
- **(b)** 6
- **(c)** 0
- **(d)** Error

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) 6**

**Why.** A nested function shares the parent function's workspace, so `nestfun1` sets the same `x` to 5. Then `x = x + 1` gives 6.

**Concept: nested vs local functions.** A nested function (defined inside another's `function ... end`) can see and change the parent's variables. A local function (defined after it in the file) has its own separate workspace.

{{< /details >}}

### 5 · Q47, deleting a row

*Asked by: MathWorks (IISc 2024)*

Which commands remove the third row of a $3 \times 3$ matrix `A`, leaving
$2 \times 3$? (select all)

- **(a)** A(:,3) = []
- **(b)** A(3,:) = []
- **(c)** A(:,3) = ()
- **(d)** A(3,:) = ()
- **(e)** delete(A, 3, 'row')
- **(f)** A = A(1:2,:)

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) `A(3,:) = []` and (f) `A = A(1:2,:)`**

**Why.** Assigning `[]` to row 3 (all columns `:`) deletes it; keeping rows 1–2 does the same. (a) deletes column 3; `()` is not an empty matrix; there is no such `delete` function.

**Concept: deleting elements.** Assign the empty matrix: `A(i, :) = []` deletes row i, `A(:, j) = []` deletes column j.

{{< /details >}}

### 6 · Q48, cell arrays

*Asked by: MathWorks (IISc 2024)*

`A = {[1,2,3], 'SampleText', 1, 2, 3};` then

```matlab
x1 = A(1);
x2 = A(2);
x3 = A(3:5);
n = length(A);
```

Which are true? (select all)

- **(a)** x1 is of type double
- **(b)** x2 is of type string
- **(c)** x3 is a cell array with 3 elements
- **(d)** n is equal to 1

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) only**

**Why.** Parentheses index a cell array and return cells: x1 and x2 are 1 × 1 cells (not double or string), x3 = A(3:5) is a 1 × 3 cell, and n = length(A) = 5. Braces `A{1}` would give the contents.

**Concept: () vs {} on cell arrays.** `C(i)` returns a smaller cell array (the box); `C{i}` returns what is inside the box.

{{< /details >}}

### 7 · Q49, changing the loop variable

*Asked by: MathWorks (IISc 2024)*

How many times is MATLAB printed?

```matlab
for k = 1:4
    if k == 2
        k = 5;
    end
    disp('MATLAB')
end
```

{{< details title="Answer and explanation" closed="true" >}}

**Answer: 4 times**

**Why.** A MATLAB `for` loop takes its values from the precomputed list 1:4. Assigning k = 5 changes k only for the rest of that iteration; the next iteration uses the next list value. So all four iterations print.

**Concept: for-loop variables in MATLAB.** Unlike C, changing the loop variable does not affect how many times the loop runs. Use a `while` loop if you need to change the counter.

{{< /details >}}

### 8 · Q50, function precedence

*Asked by: MathWorks (IISc 2024)*

Order by MATLAB's precedence (highest first): (1) nested functions, (2) imported
functions, (3) functions in the current folder, (4) private functions.

- **(a)** 1 3 4 2
- **(b)** 3 4 1 2
- **(c)** 2 1 4 3
- **(d)** 3 2 1 4

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) 2 1 4 3**

**Why.** MATLAB resolves a name in this order: variables, explicitly imported names, nested functions, local functions, private functions, class methods and constructors, the current folder, then the rest of the path. So imported (2) → nested (1) → private (4) → current folder (3).

**Concept: name resolution.** When two things share a name, the earlier one in the precedence list wins. That is why a variable named `sum` hides the built-in `sum` function.

{{< /details >}}
