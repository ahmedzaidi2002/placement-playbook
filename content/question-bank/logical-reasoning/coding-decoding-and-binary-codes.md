---
title: "Coding-decoding and binary codes"
weight: 10
---

5 questions asked by Accenture, Axxela, JSW, Texas Instruments. Try each one first, then open the toggle: it gives the answer, why it is right, and the idea behind it explained from scratch.

### 1 · Q36-40, binary code with * and \$

*Asked by: Accenture (IDC paper)*

`*` stands for 0 and <code>&#36;</code> for 1, and a <code>&#36;</code> doubles in value for every place
it moves left (binary: 4 is <code>&#36;&#42;&#42;</code>, 3 is <code>&#36;&#36;</code>).
(36) $11 \times 17/10 + 2 \times 5 + 3/10$ is: [<code>&#36;&#42;&#36;&#36;&#42;</code> / <code>&#36;&#42;&#36;&#36;&#36;</code> /
<code>&#36;&#36;&#36;&#42;&#36;</code> / <code>&#36;&#42;&#42;&#36;&#36;</code>] (37) 260 is: [<code>&#36;&#42;&#42;&#42;&#42;&#36;&#42;&#42;</code> /
<code>&#36;&#36;&#42;&#36;&#36;&#36;&#36;&#36;</code> / <code>&#36;&#36;&#42;&#36;&#36;&#36;&#36;&#42;&#42;</code> / <code>&#36;&#42;&#42;&#42;&#42;&#42;&#36;&#42;&#42;</code>] (38) $60/17$ is:
[<code>&#36;&#36;&#36;&#42;&#36;&#42;&#42;&#42; / &#36;&#36;&#42;&#42;&#36;&#36;</code> / <code>&#36;&#36;&#36;&#42;&#42;&#42;&#42;&#42; / &#36;&#36;&#42;&#42;&#36;&#36;</code> /
<code>&#36;&#42;&#36;&#36;&#42;&#36;&#42;&#42; / &#36;&#36;&#42;&#42;&#36;&#36;</code> / <code>&#36;&#36;&#42;&#36;&#42;&#36;&#42;&#42; / &#36;&#36;&#42;&#42;&#36;&#36;</code>] (39) <code>&#36;&#42;&#42;&#42;&#36;</code>
is: [<code>&#36;&#36;&#36; / &#36;&#42;</code> / <code>&#36;&#42;&#36;&#42;&#42; - &#36;&#36;</code> / <code>&#36;&#42;&#36;&#42;&#36; - &#36;&#36;</code> /
<code>&#36;&#36;&#36;&#42;&#42;&#42;&#36; - &#36;&#36;</code>] (40) $30^2$ is: [<code>(&#36;&#36;&#42;&#36;&#36;)^&#36;&#42; + &#36;&#42;&#36;&#42;&#36;&#36;&#42;&#36;</code> /
<code>(&#36;&#36;&#42;&#36;&#36;)^&#36;&#42; + &#36;&#36;&#42;&#42;&#42;&#42;&#36;</code> / <code>(&#36;&#36;&#42;&#36;&#36;)^&#36;&#36; + &#36;&#42;&#36;&#42;&#42;&#42;&#42;</code> /
<code>(&#36;&#36;&#42;&#36;&#36;)^&#36;&#36; + &#36;&#42;&#36;&#42;&#42;&#36;</code>]

{{< details title="Answer and explanation" closed="true" >}}

**Answers: (36) <code>&#36;&#36;&#36;&#42;&#36;</code> (37) <code>&#36;&#42;&#42;&#42;&#42;&#42;&#36;&#42;&#42;</code> (38) the third option (39) <code>&#36;&#42;&#36;&#42;&#42; - &#36;&#36;</code> (40) the first option (it has a printed typo)**

**Why.** Read `*` as 0 and <code>&#36;</code> as 1: these are binary numbers.
- (36) 11 × 17/10 + 2 × 5 + 3/10 = 18.7 + 10 + 0.3 = 29 = 11101₂.
- (37) 260 = 256 + 4 = 100000100₂.
- (38) 60/17 = 180/51; 180 = 10110100₂ and 51 = 110011₂.
- (39) <code>&#36;&#42;&#42;&#42;&#36;</code> = 10001₂ = 17 = 20 − 3 = 10100₂ − 11₂.
- (40) 30² = 900 = 27² + 171; the first option is (11011)^(10) + 10101101, i.e. 729 + 173, two off (171 would be 10101011), so it has a typo but is the only one built on 27².

**Concept: binary numbers.** Each place is worth double the place to its right: 1, 2, 4, 8, 16, ... To convert a decimal number, subtract the largest power of 2 that fits, mark 1 there, and repeat. Example: 29 = 16 + 8 + 4 + 1 → 11101.

{{< /details >}}

### 2 · Q33-37, binary code

*Asked by: Accenture (Dec paper)*

With `*` = 0 and <code>&#36;</code> = 1 in binary: (33) 601 is [<code>&#36;&#42;&#42;&#36;&#36;&#42;&#42;&#36;&#36;&#36;</code> /
<code>&#36;&#42;&#36;&#36;&#36;&#36;&#36;&#42;&#36;&#36;</code> / <code>&#36;&#42;&#42;&#36;&#42;&#36;&#36;&#42;&#42;&#36;</code> / <code>&#36;&#42;&#36;&#36;&#36;&#42;&#36;&#42;&#36;&#36;</code>]
(34) $\operatorname{lcm}(18, 20, 36)/90$ is [<code>&#36;&#42;</code> / <code>&#36;&#36;</code> / <code>&#36;&#36;&#42;</code> /
<code>&#36;&#36;&#36;&#36;</code>] (35) 454 is [<code>&#36;&#42;&#36;&#36;&#36;&#42;&#42;&#42;&#36;</code> / <code>&#36;&#36;&#42;&#36;&#36;&#36;&#36;&#42;&#42;</code> /
<code>&#36;&#36;&#36;&#42;&#42;&#42;&#36;&#36;&#42;</code> / <code>&#36;&#42;&#36;&#42;&#36;&#42;&#42;&#42;&#36;</code>] (36) (<code>&#36;&#36;&#42;&#36;&#42;</code>) to the power (<code>&#36;&#42;</code>) is
[450 / 550 / 650 / 676] (37) $3 \times \text{average}(64, 74, 104)$ is [<code>&#36;&#36;&#36;&#36;&#42;&#42;&#36;&#42;</code>
/ <code>&#36;&#42;&#42;&#42;&#42;&#36;&#36;&#42;</code> / <code>&#36;&#42;&#42;&#42;&#36;&#42;&#36;&#42;</code> / <code>&#36;&#36;&#42;&#42;&#36;&#42;&#36;&#36;</code>]

{{< details title="Answer and explanation" closed="true" >}}

**Answers: (33) <code>&#36;&#42;&#42;&#36;&#42;&#36;&#36;&#42;&#42;&#36;</code> (34) <code>&#36;&#42;</code> (35) <code>&#36;&#36;&#36;&#42;&#42;&#42;&#36;&#36;&#42;</code> (36) 676 (37) <code>&#36;&#36;&#36;&#36;&#42;&#42;&#36;&#42;</code>**

**Why.**
- (33) 601 = 512 + 64 + 16 + 8 + 1 = 1001011001₂.
- (34) LCM(18, 20, 36) = 180; 180/90 = 2 = 10₂.
- (35) 454 = 256 + 128 + 64 + 4 + 2 = 111000110₂.
- (36) <code>&#36;&#36;&#42;&#36;&#42;</code> = 26, <code>&#36;&#42;</code> = 2, so 26² = 676.
- (37) 3 × average(64, 74, 104) = the sum = 242 = 11110010₂.

**Concept: binary conversion.** Same method as above. Also note "3 × average of 3 numbers = their sum", which saves a division.

{{< /details >}}

### 3 · Q1, coding REASON

*Asked by: Axxela (NIT Bhopal 2024)*

If REASON is coded as PGYUMP, then DIRECT will be coded as?

- **(a)** BKPGAV
- **(b)** FKTGEV
- **(c)** FGTCER
- **(d)** BGPCAR

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) BKPGAV**

**Why.** REASON → PGYUMP: R−2 = P, E+2 = G, A−2 = Y (wrapping back from A), S+2 = U, O−2 = M, N+2 = P. The shifts alternate −2, +2. Apply to DIRECT: D−2 = B, I+2 = K, R−2 = P, E+2 = G, C−2 = A, T+2 = V.

**Concept: letter-shift codes.** Write the alphabet positions (A = 1 ... Z = 26) of the word and its code, find the shift for each letter, and look for a pattern (constant, alternating, increasing). Shifts wrap around: A − 2 = Y.

{{< /details >}}

### 4 · coding PARTY with two letter matrices

*Asked by: JSW (Aptitude test)*

Each letter is coded by its row number then its column number in one of two matrices.
Matrix 1 (rows and columns 0-4), row by row: P R Y F Q / Q F R Y P / R Q P Y F /
F P Q R Y / Y Q P F R. Matrix 2 (rows and columns 5-9): T Z A G W / Z A G W T /
W T A G Z / A G W T Z / G T Z W A. Which set of numbers can represent the word PARTY?

- **(a)** 40, 02, 13, 20, 66
- **(b)** 12, 20, 44, 76, 96
- **(c)** 14, 31, 42, 77, 99
- **(d)** 00, 66, 44, 88, 23

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) 00, 66, 44, 88, 23**

**Why.** A code is row digit then column digit. Check (d) letter by letter: 00 is row 0, column 0 of matrix 1 = P; 66 is row 6, column 6 of matrix 2 = A; 44 = R; 88 = T; 23 = Y. Every other option fails early (e.g. (a)'s 40 is Y, (b)'s 12 is R, (c)'s 31 is P, not A).

**Concept: check options, don't build the code.** Each letter appears many times in the matrices, so many codes are possible. It is faster to test each option's numbers against the grid and reject an option at its first wrong letter.

{{< /details >}}

### 5 · encoding words

*Asked by: Texas Instruments (IIT BHU 2023)*

Annual is encoded ESTKIU and Quarter UZGYJNJ. Encode Week.

- **(a)** IJKR
- **(b)** IJJR
- **(c)** IKKR
- **(d)** KIJR

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) IJKR**

**Why.** Annual → ESTKIU and Quarter → UZGYJNJ: the i-th letter is shifted forward by i + 3 (A+4 = E, N+5 = S, N+6 = T, ...). For WEEK: E+5 = J, E+6 = K, K+7 = R. W+4 runs past Z, and the examples do not wrap consistently: in Quarter, T+8 (position 28) becomes J, which would put position 27 at I; in Annual, U+7 (also 28) becomes K. Following Quarter gives I. Only IJKR has J, K, R in places 2–4, so it is the answer either way.

**Concept: increasing shift codes.** When the shift grows with position, write the shifts out (4, 5, 6, 7, ...). Use the letters that do not wrap to pick the option, since the examples here are not fully consistent at the wrap-around.

{{< /details >}}
