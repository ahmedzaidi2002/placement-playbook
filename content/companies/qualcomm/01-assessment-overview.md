---
title: 1 · Assessment overview
weight: 1
---

The questions on these pages were transcribed from screenshots of the HirePro exam window. Some screenshots were low resolution, so the wording is as close to the original as was legible.

## How to use the pages

Each question shows its section tag, the question, and the four options. The answer is hidden inside a **Show answer and explanation** toggle. Click it to open the correct option and a short explanation. For code questions the code is shown in a block so you can trace it on paper first.

## Section mix

| Section | Questions | What shows up |
|---|---|---|
| Aptitude | Q1–Q20 | Coordinate geometry, cone and hemisphere volume, ages, salary ratio, combinations, mixtures, a 7-post lantern puzzle (Q8–Q12), series, a data table (Q14–Q17), relative speed, conditional probability |
| Programming basics | Q21–Q40 | Binary to hex, buddy system, logic gates, C pointers and operators, selection sort, priority scheduling, linked lists, binary search, assembler, subroutine calls, queue overflow, error spotting |
| Computer science | Q41–Q60 | Pipeline timing, circular queue, OOP (messages, encapsulation, polymorphism), Boolean simplification, 2D arrays and pointers, matrix multiply, binary search complexity, deadlock detection, schedulers, segmentation |

## Confidence in the answers

Answers come from working each question out, not from an official key. Each answer carries a confidence level.

- **High**: the answer follows directly and unambiguously. No label is shown.
- **Medium**: the answer is sound but depends on compiler behaviour or on reading an ambiguous question. The toggle says so.
- **Flagged**: no reliable answer. Four questions are in this group.

## Flagged questions

| Q | Why it is flagged |
|---|---|
| Q5 | `2015 : ? :: 1418 : 67`. No rule that maps 1418 to 67 could be found after trying digit sums, products, splits, squares, reversals and factorisations. |
| Q22 | Buddy system. The internal fragmentation comes to 130K at P1's release (75K after it leaves); neither is an option. Nearest listed option is 136K. |
| Q33 | 4-bit shift register. The derived result is `0111` (or `1010` if the serial input is read from the other end); neither is an option, and two options are 6 bits wide for a 4-bit register. The question looks flawed. |
| Q41 | Pipeline "variance". Non-pipelined latency is 280 ns, pipelined is 384 ns, difference 104 ns (not an option). 216 ns is the only derivable option and relies on a non-standard reading. |

## Missing pieces in the source

- The **lantern puzzle clues** (Q8–Q12) were not transcribed. Only the final arrangement is available, so those five questions are answered from it.
- The **applications table** (Q14–Q17) was not transcribed. The figures needed for the solutions are listed above Q14.
- Q24 (function-pointer recursion) was only partly legible; the code block shows the pieces that were.

## Answers marked in the exam that turned out wrong

| Q | Marked | Correct |
|---|---|---|
| Q11 | Post 7 | Post 6 |
| Q53 | `-42 5 1120 1220` | `-45 4 1239 1235` |

> **Editor's note.** Q35 was corrected after running the code: the source workbook said `1 -11`, but the `if` body still runs after the short-circuit, so the output is `1 -11 1 -11`. The Q35 toggle explains why.

## Source

The source workbook is `Qualcomm_Assessment_60Q_Summary.xlsx` (sheets: *Question Bank* and *Notes*). Time limit, marking scheme, cut-off and what came after the assessment were *not stated* in it.
