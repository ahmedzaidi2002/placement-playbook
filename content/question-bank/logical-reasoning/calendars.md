---
title: "Calendars"
weight: 17
---

1 question asked by Texas Instruments. Try each one first, then open the toggle: it gives the answer, why it is right, and the idea behind it explained from scratch.

### 1 · a calendar

*Asked by: Texas Instruments (IISc, second set)*

21 August 1995 was a Monday, and 1996 was a leap year. What day was 24 August 1998?

- **(a)** Monday
- **(b)** Thursday
- **(c)** Friday
- **(d)** Sunday

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) Monday**

**Why.** From 21 Aug 1995 to 21 Aug 1998 is 3 years: 365 + 366 (1996 is a leap year and 29 Feb 1996 falls in between) + 365 = 1096 days. 1096 = 156 × 7 + 4, so 21 Aug 1998 is Monday + 4 = Friday. Three days later, 24 Aug 1998, is Monday.

**Concept: odd days.** An ordinary year shifts the weekday by 1 (365 = 52 weeks + 1 day), a leap year by 2. Count the year-shifts between the dates, add the extra days, and reduce mod 7.

{{< /details >}}
