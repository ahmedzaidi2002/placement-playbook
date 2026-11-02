---
title: "Algorithms and output prediction in Java"
weight: 2
---

3 questions asked by Oracle, Sigmoid. Try each one first, then open the toggle: it gives the answer, why it is right, and the idea behind it explained from scratch.

### 1 · recursive swap

*Asked by: Oracle (HackerRank MCQ test)*

Consider the Java method below. What does it do?

```java
public static void function_1(int[] data, int low, int high) {
    if (low < high) {
        int temp = data[low];
        data[low] = data[high];
        data[high] = temp;
        function_1(data, low + 1, high - 1);
    }
}
```

- **(a)** The sum of all the elements of the array
- **(b)** The product of all the elements in the array
- **(c)** The last element of the array
- **(d)** Reverses the contents of the array.

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) it reverses the contents of the array** (between low and high)

**Why.** It swaps data[low] and data[high], then recurses on the inner part (low + 1, high − 1), stopping when the pointers meet or cross. That is exactly reversal.

**Concept: two-pointer reversal.** Swap the outermost pair and move both ends inward. Recursion depth is n/2; an iterative loop does the same with O(1) extra space.

{{< /details >}}

### 2 · output of a bubble sort

*Asked by: Sigmoid (Campus hiring 2026)*

`arr = {11, 9, 10, 45, 22}` is passed to a function that does a standard bubble sort
in place; then the elements are printed. What is the output?

- **(a)** 9 10 11 22 45
- **(b)** 45 22 11 10 9
- **(c)** 0 0 1 1 1

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) 9 10 11 22 45**

**Why.** Bubble sort orders the array ascending. Java passes the array's reference by value, so the method sorts the same array the caller holds, and printing it shows the sorted order.

**Concept: Java passes references by value.** For an array or object, the method gets a copy of the reference, pointing to the same object; changing its contents is visible to the caller. Reassigning the parameter to a new array would not be.

{{< /details >}}

### 3 · Newton iteration in Java

*Asked by: Sigmoid (Campus hiring 2026)*

What is the output? `SomeFunction(16)` starts with `result = number / 2` and
repeats `temp = result; result = (temp + number / temp) / 2;` while
`(temp - result) != 0`, then returns `result`; `main` prints it.

- **(a)** 16
- **(b)** 8
- **(c)** 4
- **(d)** 2

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) 4** (printed as 4.0)

**Why.** The loop is Newton's method for √16: result = (temp + 16/temp)/2. From 8: 5, 4.1, 4.001..., converging to 4.0, where two successive values are equal and the loop stops.

**Concept: Newton's method for square roots.** To find √N, repeat x ← (x + N/x)/2. If x is too big, N/x is too small, and their average is closer. It converges very fast (the number of correct digits roughly doubles each step).

{{< /details >}}
