---
title: "Numpy, pandas and libraries"
weight: 1
---

6 questions asked by EXL, Info Edge, Porter. Try each one first, then open the toggle: it gives the answer, why it is right, and the idea behind it explained from scratch.

### 1 · weekly sums resampled to monthly means

*Asked by: EXL (HackerEarth test, 2025)*

What is the output of this code?

```python
import pandas as pd
df = pd.DataFrame({
    'Date': pd.date_range('2023-02-01', '2023-02-28'),
    'Value': [1, 2, ..., 28]})
grouped = df.groupby(pd.Grouper(key='Date', freq='W'))
result = grouped.apply(lambda x: x['Value'].sum()).resample('M').mean()
print(result)
```

Options (index, value): (1) 2023-02-28 87.75, 2023-03-31 55.00; (2) 2023-02-28 87.00,
2023-03-31 55.75; (3) 2023-01-31 87.75, 2023-02-28 55.00; (4) 2023-01-31 55.00,
2023-02-28 87.75.

{{< details title="Answer and explanation" closed="true" >}}

**Answer: option (1): 2023-02-28 → 87.75, 2023-03-31 → 55.00**

**Why.**
1. `freq='W'` makes weekly bins ending on Sundays: up to Feb 5 (values 1–5, sum 15), Feb 12 (63), Feb 19 (112), Feb 26 (161), and Mar 5 (Feb 27–28, sum 55). Each week is labelled by its end date.
2. `.resample('M').mean()` groups those weekly sums by month end: February has 15, 63, 112, 161 → mean 87.75; March has 55.

**Concept: grouping by time.** `pd.Grouper(freq='W')` bins dates into weeks (ending Sunday by default) and labels each bin by its end. `resample('M')` (written `'ME'` in new pandas) then regroups by calendar month. Watch which label each bin gets.

{{< /details >}}

### 2 · Q31, NumPy slicing

*Asked by: Info Edge (Data Science II)*

The NumPy slicing operator `[:4]` would do the following:

- **(a)** Slice the elements from the beginning to index 3
- **(b)** Slice the elements from the beginning to index 4
- **(c)** Slice the last 4 elements
- **(d)** Throw an error

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) from the beginning up to index 3**

**Why.** `[:4]` takes indices 0, 1, 2, 3; the stop index is excluded.

**Concept: half-open slices.** `a[start:stop]` includes start and excludes stop, so it has stop − start elements.

{{< /details >}}

### 3 · Q32, changing shape

*Asked by: Info Edge (Data Science II)*

How can we change the shape of a NumPy array in Python?

- **(a)** By shape()
- **(b)** By reshape()
- **(c)** By ord()
- **(d)** By change()

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) `reshape()`**

**Why.** `a.reshape(r, c)` returns the same data viewed with a new shape (the total size must match).

**Concept: reshape.** Data stays in the same order in memory; only the way it is split into dimensions changes.

{{< /details >}}

### 4 · Q33, summary statistics

*Asked by: Info Edge (Data Science II)*

Which method computes the key statistical parameters of a specified column of a Pandas
dataframe?

- **(a)** describe()
- **(b)** stats()
- **(c)** statistics()
- **(d)** None

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) `describe()`**

**Why.** `df['col'].describe()` gives count, mean, standard deviation, min, quartiles and max.

**Concept: quick data summaries.** `describe()` for numbers, `value_counts()` for categories, `info()` for types and missing values.

{{< /details >}}

### 5 · Q35, creating a DataFrame

*Asked by: Info Edge (Data Science II)*

A Pandas DataFrame in Python can be created from a:

- **(a)** list
- **(b)** dict
- **(c)** csv file
- **(d)** All of the above

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) all of the above**

**Why.** `pd.DataFrame(list)`, `pd.DataFrame(dict)` and `pd.read_csv(file)` all produce DataFrames.

**Concept: DataFrame sources.** A DataFrame is a table of labelled columns; it can be built from lists, dicts of columns, NumPy arrays, CSV/Excel files and SQL queries.

{{< /details >}}

### 6 · Q27, Marines at your positions (pandas)

*Asked by: Porter (OA set 1)*

Write a Python program that

- takes a list as input, `list_input`;
- takes another list as input, `list_pos`;
- creates a pandas Series from `list_input`;
- prints the values of `list_input` at the positions listed in
    `list_pos`.

**Input.** The first line holds space-separated values of any type (the elements of
`list_input`); the second holds space-separated integers, the 0-based positions
`list_pos`. **Output.** The values at those positions, along with the dtype.

**Sample input.** `a b c ...{} z` (the 26 letters) and `0 4 8 14 20`.

{{< details title="Answer and explanation" closed="true" >}}

**Answer: use `s.iloc[list_pos]`**

```python
import pandas as pd
list_input = input().split()
list_pos = list(map(int, input().split()))
s = pd.Series(list_input)
print(s.iloc[list_pos])
```

**Why.** `iloc` selects by position. Plain `s[list_pos]` only works because the default index labels happen to equal positions, and recent pandas warns about positional `[]`. For the sample it prints 0 a, 4 e, 8 i, 14 o, 20 u and a dtype line (`object` in pandas 1–2, `str` in pandas 3).

**Concept: `iloc` vs `loc`.** `iloc` uses integer positions (0, 1, 2, ...); `loc` uses index labels. They differ as soon as the index is not 0..n−1.

{{< /details >}}
