---
title: "Strings, numbers and operators"
weight: 3
---

4 questions asked by Info Edge, MathWorks. Try each one first, then open the toggle: it gives the answer, why it is right, and the idea behind it explained from scratch.

### 1 · Q34, writing CSV

*Asked by: Info Edge (Data Science II)*

Which function is commonly used to write a CSV file from a Pandas dataframe?

- **(a)** write_csv()
- **(b)** to_csv()
- **(c)** out_csv()
- **(d)** in_csv()

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) `to_csv()`**

**Why.** `df.to_csv('file.csv', index=False)` writes the DataFrame to CSV; `pd.read_csv` reads one.

**Concept: pandas I/O pairs.** read_csv / to_csv, read_excel / to_excel, read_json / to_json.

{{< /details >}}

### 2 · Q36, reshape with -1

*Asked by: Info Edge (Data Science II)*

In NumPy, if a dimension is given as ___ in a reshaping operation, the other dimensions are
automatically calculated.

- **(a)** 0
- **(b)** 1
- **(c)** -1
- **(d)** Infinity

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) −1**

**Why.** In `a.reshape(-1, 3)`, NumPy works out the −1 dimension from the total size (e.g. 12 elements → 4 rows).

**Concept: inferred dimension.** Only one dimension can be −1; it is total size ÷ product of the others.

{{< /details >}}

### 3 · Q38, number of unique values

*Asked by: Info Edge (Data Science II)*

Which is the correct way to get the number of unique values in a column `'C'` of a Pandas
dataframe `df`?

- **(a)** df.C.count_unique()
- **(b)** df['C'].nunique()
- **(c)** df['C'].unique()
- **(d)** df.C.find_unique()

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) `df['C'].nunique()`**

**Why.** `nunique()` returns the number of distinct values; `unique()` returns the values themselves; the other method names do not exist.

**Concept: unique values.** `unique()` → array of distinct values, `nunique()` → their count, `value_counts()` → each value's frequency.

{{< /details >}}

### 4 · Q39, a loop sum

*Asked by: MathWorks (IIT Bombay 2024)*

`a = 0; for b in range(0, 10, 2): a += b + 1`; then `a` is?

{{< details title="Answer and explanation" closed="true" >}}

**Answer: 25**

**Why.** b takes 0, 2, 4, 6, 8; a adds b + 1 each time: 1 + 3 + 5 + 7 + 9 = 25.

**Concept: `range(0, 10, 2)`.** Starts at 0, steps by 2, stops before 10. (The sum of the first n odd numbers is n², here 5² = 25.)

{{< /details >}}
