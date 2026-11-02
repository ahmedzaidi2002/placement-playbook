---
title: "Number systems and computer arithmetic"
weight: 3
---

25 questions asked by Qualcomm, Texas Instruments. Try each one first, then open the toggle: it gives the answer, why it is right, and the idea behind it explained from scratch.

### 1 · Q38, hex to decimal

*Asked by: Qualcomm (IISc)*

What is the decimal form of $(1\mathrm{CDE})_{16}$?

- **(a)** 9513
- **(b)** 7787
- **(c)** 7391
- **(d)** 6596

{{< details title="Answer and explanation" closed="true" >}}

**Answer: the true value is 7390; the intended option is (c) 7391** (the options are off by one)

**Why.** 1CDE₁₆ = 1 × 4096 + 12 × 256 + 13 × 16 + 14 = 4096 + 3072 + 208 + 14 = 7390.

**Concept: positional value.** A digit's value = digit × base^(position). In hex, positions are worth 1, 16, 256, 4096, ...; letters A–F are 10–15.

{{< /details >}}

### 2 · Q40, hex to binary

*Asked by: Qualcomm (IISc)*

What is $(4\mathrm{ED})_{16}$ in binary?

- **(a)** 1110 0100 1101
- **(b)** 0100 1110 1101
- **(c)** 0100 1101 1111
- **(d)** 1101 1111 0100

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) 0100 1110 1101**

**Why.** Each hex digit is exactly 4 bits: 4 = 0100, E = 1110, D = 1101.

**Concept: hex ↔ binary.** Because 16 = 2⁴, convert digit by digit in groups of four bits; no arithmetic needed.

{{< /details >}}

### 3 · Q24, decimal to hex

*Asked by: Qualcomm (IISc)*

What is the hexadecimal value of $(6789)_{10}$?

- **(a)** $(F5511)_{16}$
- **(b)** $(ABCD)_{16}$
- **(c)** $(1A85)_{16}$
- **(d)** $(B150C)_{16}$

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) 1A85₁₆**

**Why.** Repeated division by 16: 6789 = 424 × 16 + 5; 424 = 26 × 16 + 8; 26 = 1 × 16 + 10 (A); 1. Read the remainders bottom-up: 1, A, 8, 5.

**Concept: decimal → base b.** Divide by b repeatedly and collect remainders; the last remainder is the most significant digit. Check: 1 × 4096 + 10 × 256 + 8 × 16 + 5 = 6789.

{{< /details >}}

### 4 · octal to decimal

*Asked by: Qualcomm (Nov 2024)*

What is the decimal equivalent of $(556)_8$?

- **(a)** $(366)_8$
- **(b)** Given number is not in octal format.
- **(c)** $(663)_{10}$
- **(d)** $(366)_{10}$

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) 366₁₀**

**Why.** 556₈ = 5 × 64 + 5 × 8 + 6 = 320 + 40 + 6 = 366.

**Concept: octal digits are 0–7.** Positions are worth 1, 8, 64, 512, ... (Option (a) writes the decimal value with a wrong base label.)

{{< /details >}}

### 5 · Q48, 32-bit signed type

*Asked by: Qualcomm (Nov 2024)*

Which data type given in the options is a 32-bit signed integer?

- **(a)** WORD
- **(b)** SWORD
- **(c)** SDWORD
- **(d)** DWORD

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) SDWORD**

**Why.** In MASM: BYTE/SBYTE are 8-bit, WORD/SWORD 16-bit, DWORD/SDWORD 32-bit; the S prefix means signed.

**Concept: data sizes.** Byte 8 bits, word 16, double word 32, quad word 64 (in x86 naming, from the original 16-bit 8086).

{{< /details >}}

### 6 · Q22, 23 AND 23

*Asked by: Qualcomm (HirePro, Aug 2025)*

What is the decimal result of the AND operation on A = 23 and B = 23?

- **(a)** 26
- **(b)** 15
- **(c)** 23
- **(d)** 25

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) 23**

**Why.** ANDing a number with itself keeps every bit unchanged: x & x = x.

**Concept: bitwise identities.** x & x = x, x | x = x, x ^ x = 0, x & 0 = 0, x | 0 = x.

{{< /details >}}

### 7 · Q21, binary to hexadecimal

*Asked by: Qualcomm (HirePro, Aug 2025)*

What is the hexadecimal equivalent of the binary number 11011011?

- **(a)** 85Dh
- **(b)** 12h
- **(c)** DBh
- **(d)** 33Fh

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) DBh**

**Why.** Split into groups of four from the right: 1101 = D, 1011 = B.

**Concept: binary → hex** in 4-bit groups.

{{< /details >}}

### 8 · Computer Architecture

*Asked by: Qualcomm (60-question online assessment)*

What will be the conversion result of the given number in hexadecimal format? 101110101

- **(a)** `17F`
- **(b)** `175`
- **(c)** `77F`
- **(d)** `17E`

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) 175**

**Why.** Group in fours from the right: 1 | 0111 | 0101 → 1, 7, 5 → 175₁₆. (Pad the leftmost group with zeros: 0001.)

**Concept: always group from the right** (the least significant end); padding goes on the left.

{{< /details >}}

### 9 · Computer Architecture

*Asked by: Qualcomm (60-question online assessment)*

Which one of the given options correctly represents the hexadecimal value of (0011 0101 1111 1010)2?

- **(a)** `30AF`
- **(b)** `35FA`
- **(c)** `13FC`
- **(d)** `30FB`

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) 35FA**

**Why.** 0011 = 3, 0101 = 5, 1111 = F, 1010 = A.

**Concept: binary → hex** in 4-bit groups.

{{< /details >}}

### 10 · Computer Architecture

*Asked by: Qualcomm (60-question online assessment)*

What is the hexadecimal equivalent of the below given binary number? 1101110

- **(a)** `6eh`
- **(b)** `5dh`
- **(c)** `3fh`
- **(d)** `1fh`

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) 6Eh**

**Why.** 110 | 1110 → 0110 = 6, 1110 = E.

**Concept: binary → hex**, padding the left group with zeros.

{{< /details >}}

### 11 · Number systems

*Asked by: Qualcomm (BITS Goa 2024, Q50) · Qualcomm (IIIT Delhi 2025, Q30)*

What will be the decimal equivalent of the number (011.101)₂?

- **(a)** Given number is invalid binary number
- **(b)** 3.625
- **(c)** 3
- **(d)** 2.625

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) 3.625**

**Why.** Integer part 011 = 3. Fraction .101 = 1 × 2⁻¹ + 0 × 2⁻² + 1 × 2⁻³ = 0.5 + 0.125 = 0.625. Total 3.625.

**Concept: binary fractions.** Places after the point are worth 1/2, 1/4, 1/8, ... Some decimal fractions (like 0.1) have no exact binary form, which is why floating-point rounding errors occur.

{{< /details >}}

### 12 · Number systems

*Asked by: Qualcomm (BITS Hyderabad 2024, Q38)*

Convert (5613)₈ to decimal.

- **(a)** 4900
- **(b)** 2955
- **(c)** 1500
- **(d)** 3955

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) 2955**

**Why.** 5 × 512 + 6 × 64 + 1 × 8 + 3 = 2560 + 384 + 8 + 3 = 2955.

**Concept: octal place values** are powers of 8: 1, 8, 64, 512.

{{< /details >}}

### 13 · Number systems

*Asked by: Qualcomm (BITS Hyderabad 2025, Q25)*

What is the decimal equivalent of (1111011011000)₂?

- **(a)** 458
- **(b)** 7596
- **(c)** 7896
- **(d)** 785

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) 7896**

**Why.** Group into hex from the right: 1 | 1110 | 1101 | 1000 = 1ED8₁₆ = 4096 + 14 × 256 + 13 × 16 + 8 = 4096 + 3584 + 208 + 8 = 7896.

**Concept: use hex as a shortcut.** Converting a long binary number to hex first, then to decimal, means far fewer terms to add.

{{< /details >}}

### 14 · Number systems

*Asked by: Qualcomm (BITS Hyderabad 2025, Q28) · Qualcomm (IIIT Delhi 2025, Q27)*

Convert (10101010101011)₂ into hexadecimal.

- **(a)** (2CCC)₁₆
- **(b)** (2AAB)₁₆
- **(c)** (2BBB)₁₆
- **(d)** (2BBC)₁₆

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) 2AAB₁₆**

**Why.** Group in fours from the right: 10 | 1010 | 1010 | 1011 = 2, A, A, B.

**Concept: binary → hex** in 4-bit groups from the right.

{{< /details >}}

### 15 · Number systems

*Asked by: Qualcomm (Delhi campus 2024, Q26)*

Convert (9ED)₁₆ to octal.

- **(a)** 4776
- **(b)** 4855
- **(c)** 4765
- **(d)** 4755

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) 4755₈**

**Why.** 9ED₁₆ = 1001 1110 1101. Regroup in threes from the right: 100 111 101 101 = 4, 7, 5, 5.

**Concept: hex ↔ octal via binary.** Hex digits are 4 bits and octal digits 3 bits, so go through binary and regroup.

{{< /details >}}

### 16 · Number systems

*Asked by: Qualcomm (2025 paper (campus not named), Q21)*

Convert 109 (decimal) to hexadecimal.

- **(a)** 4D
- **(b)** 100D
- **(c)** 6D
- **(d)** 109F

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) 6D**

**Why.** 109 = 6 × 16 + 13, and 13 is D.

**Concept: decimal → hex** by dividing by 16 (quotient and remainder).

{{< /details >}}

### 17 · Number systems

*Asked by: Qualcomm (Delhi campus 2024, Q47)*

What is the correct 2's complement representation of (−55)₁₀ in 8 bits?

- **(a)** 11001001
- **(b)** 01010101
- **(c)** 10110101
- **(d)** 11101101

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) 11001001**

**Why.** +55 = 0011 0111. Invert all bits: 1100 1000. Add 1: 1100 1001.

**Concept: two's complement.** −x is (invert all bits of x) + 1. Check: the MSB is 1 (negative), and 11001001 = −128 + 73 = −55. Two's complement lets the same adder handle signed and unsigned numbers.

{{< /details >}}

### 18 · Number systems

*Asked by: Qualcomm (IIIT Delhi 2025, Q23)*

What is the binary equivalent of (−56)₁₀ (24-bit two's complement)?

- **(a)** (000000000000000001001000)₂
- **(b)** (000000000000000000001000)₂
- **(c)** (111111111111111111101000)₂
- **(d)** (111111111111111111001000)₂

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) 1111 1111 1111 1111 1100 1000**

**Why.** +56 = 0011 1000. Invert and add 1 (8 bits): 1100 1000. Sign-extend to 24 bits by filling with copies of the sign bit (1s). (Option (c) is −24.)

**Concept: sign extension.** To widen a two's complement number, copy its sign bit into the new high bits; the value stays the same.

{{< /details >}}

### 19 · Number systems

*Asked by: Qualcomm (IISc 2024, Q40)*

What is the 2's complement of the decimal number 95 (7 bits)?

- **(a)** 1100111
- **(b)** 0100001
- **(c)** 0101010
- **(d)** 1100110

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) 0100001**

**Why.** 95 = 101 1111 (7 bits). Invert: 010 0000. Add 1: 010 0001.

**Concept: two's complement as an operation.** "2's complement of x" means 2ⁿ − x: here 128 − 95 = 33 = 0100001.

{{< /details >}}

### 20 · Codes and number systems

*Asked by: Qualcomm (BITS Goa 2024, Q53)*

Excess-3 code can be used to perform the addition and subtraction of which of the following effectively?

- **(a)** Hexadecimal
- **(b)** Octal
- **(c)** BCD
- **(d)** Binary

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) BCD**

**Why.** Excess-3 is BCD + 3. It is self-complementing (the 9's complement of a digit is its bitwise inverse), and a decimal carry out of a digit appears as a natural binary carry, which makes BCD addition and subtraction easy.

**Concept: BCD codes.** BCD stores each decimal digit in 4 bits (8421). XS-3 adds 3 to each digit; Gray code changes one bit between consecutive values.

{{< /details >}}

### 21 · Codes and number systems

*Asked by: Qualcomm (BITS Goa 2024, Q45)*

A BCD to excess-2 (XS-2) code converter is designed with input B₀B₁B₂B₃ and output A₀A₁A₂A₃. What is the expression for A₂?

- **(a)** B₂′B₃ + B₁′B₃
- **(b)** B₃′B₁′ + B₁B₂
- **(c)** B₂′B₁ + B₁′B₂
- **(d)** B₂′B₁ + B₁B₃

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) B₂′B₁ + B₁′B₂**

**Why.** Treat the subscript as the bit weight (B₀ = LSB). XS-2 = BCD + 0010. Bit 0 is unchanged; bit 1 is inverted, with a carry into bit 2 when B₁ = 1. So A₂ = B₂ ⊕ B₁ = B₂′B₁ + B₁′B₂.

**Concept: code converters as adders.** Adding a constant bit by bit: each output bit is the input bit XOR the carry coming in, and carries propagate only where the constant has 1s or earlier carries.

{{< /details >}}

### 22 · Codes and number systems

*Asked by: Qualcomm (BITS Hyderabad 2024, Q56)*

What is the result of (771)₈ + (543)₈ in hexadecimal?

- **(a)** 35C
- **(b)** 1314
- **(c)** 1534
- **(d)** 34C

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) 35C**

**Why.** 771₈ = 7 × 64 + 7 × 8 + 1 = 505; 543₈ = 5 × 64 + 4 × 8 + 3 = 355. Sum 860 = 3 × 256 + 5 × 16 + 12 = 35C₁₆. (1534 is the sum in octal.)

**Concept: convert to one base before adding** (or add in octal, then convert). Watch which base the answer is asked in.

{{< /details >}}

### 23 · Codes and number systems

*Asked by: Qualcomm (BITS Hyderabad 2025, Q60)*

Which statements are true about the 2-out-of-5 code?

I. It is an even-parity code.  
II. It is an unweighted code.  
III. There are exactly two 1s in each group.

- **(a)** Only (I) and (II)
- **(b)** Only (I) and (III)
- **(c)** All (I), (II) and (III)
- **(d)** Only (II) and (III)

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) all three**

**Why.** Every code word has exactly two 1s out of five bits (III), so the number of 1s is always even (I). It is usually listed as non-weighted: the 0-1-2-4-7 weights fit every digit except 0 (11000) (II).

**Concept: error-detecting codes.** A 2-out-of-5 code detects any single-bit error (the count of 1s would change). C(5, 2) = 10 code words, exactly enough for the decimal digits.

{{< /details >}}

### 24 · number format for low power

*Asked by: Texas Instruments (NIT Calicut 2023)*

Data around a steady state of 0 fluctuate slightly. Which number format minimises dynamic
power?

- **(a)** 1's complement
- **(b)** 2's complement
- **(c)** Signed magnitude
- **(d)** Dynamic power does not depend on the representation

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) signed magnitude**

**Why.** Dynamic power grows with how many bits toggle. A small swing across 0 in signed magnitude flips only the sign bit and a few low bits. In two's complement, going from +1 (0000...01) to −1 (1111...11) toggles every bit.

**Concept: switching activity.** CMOS dynamic power ∝ α C V² f, where α is how often bits toggle. Choosing encodings that toggle fewer bits for typical data saves power.

{{< /details >}}

### 25 · sign-magnitude

*Asked by: Texas Instruments (IIT BHU 2023)*

The sign-magnitude representation of $-15$ is:

- **(a)** 1111
- **(b)** 1111
- **(c)** 11111
- **(d)** 1110

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) 11111**

**Why.** Sign-magnitude uses a sign bit (1 = negative) followed by the magnitude: 15 = 1111, so −15 = 1 1111.

**Concept: signed number formats.** Sign-magnitude (sign bit + value; has +0 and −0), 1's complement (invert bits; also two zeros), 2's complement (invert + 1; one zero, used by all modern CPUs).

{{< /details >}}
