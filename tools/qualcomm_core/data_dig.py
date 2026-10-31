"""Digital Circuits questions (section "Digital Circuits", group "Digital")."""
from qdef import Q

DIG = [
    # ---- codes and Boolean algebra ----
    Q('Codes and number systems', [('p0', 53)],
      'Excess-3 code can be used to perform the addition and subtraction of which of the following effectively?',
      ['Hexadecimal', 'Octal', 'BCD', 'Binary'], 'C',
      'XS-3 is BCD + 3. It is self-complementing (the 9\'s complement of a digit is its bitwise inverse), and a '
      'decimal carry out of a digit appears as a natural binary carry, which makes BCD add and subtract easy.'),
    Q('Codes and number systems', [('p0', 45)],
      'A BCD to excess-2 (XS-2) code converter is designed with input B₀B₁B₂B₃ and output A₀A₁A₂A₃. What is the '
      'expression for A₂?',
      ["B₂′B₃ + B₁′B₃", "B₃′B₁′ + B₁B₂", "B₂′B₁ + B₁′B₂", "B₂′B₁ + B₁B₃"], 'C',
      'Take the subscript as the bit weight (B₀ = LSB). XS-2 = BCD + 0010, so: A₀ = B₀; A₁ = B₁′ with a carry '
      'B₁ into bit 2; A₂ = B₂ ⊕ B₁ = **B₂′B₁ + B₁′B₂**; A₃ = B₃ ⊕ B₂B₁.'),
    Q('Codes and number systems', [('p1', 56)],
      'What is the result of (771)₈ + (543)₈ in hexadecimal?', ['35C', '1314', '1534', '34C'], 'A',
      '771₈ = 505 and 543₈ = 355, sum 860 = 3·256 + 5·16 + 12 = **35C₁₆**. (1534 is the octal sum.)'),
    Q('Codes and number systems', [('p3', 60)],
      'Which statements are true about the 2-out-of-5 code?\n\n'
      'I. It is an even-parity code.  \nII. It is an unweighted code.  \nIII. There are exactly two 1s in each group.',
      ['Only (I) and (II)', 'Only (I) and (III)', 'All (I), (II) and (III)', 'Only (II) and (III)'], 'C',
      'Every code word has exactly two 1s (III), so the number of ones is always even (I). It is usually listed as '
      'non-weighted: the 0-1-2-4-7 weights fit every digit except 0 (11000).'),
    Q('Boolean algebra', [('p0', 46)],
      'Simplify Y = (A + B′ + C′)(A + B′ + C).', ['A + B', 'A′ + B', 'A + B′', 'A′ + B′'], 'C',
      '(X + C′)(X + C) = X + CC′ = X with X = A + B′.'),
    Q('Boolean algebra', [('p3', 53)],
      'What is the minimum number of gates needed to implement X + X′Y?',
      ['One OR and one NAND', 'One OR and one NOR', 'One OR gate', 'One OR, one AND and one inverter'], 'C',
      'X + X′Y = (X + X′)(X + Y) = X + Y, a single OR gate.'),
    Q('Boolean algebra', [('p6', 55)],
      'F = (A + CDA′)B + (D′ + C′D)BA′. What is the simplified expression?', ['B', 'A + C + D', 'AB', 'C'], 'A',
      'First term: AB + A′BCD. Second: D′ + C′D = D′ + C′, giving A′B(C′ + D′). Then\n\n'
      'F = AB + A′B[CD + (CD)′] = AB + A′B = **B**.'),
    Q('Boolean algebra', [('p2', 55)],
      'Find the complement of Y = A′B′C + AC + (A′B′ + BC).',
      ["(A + B′ + C′)(A′ + C)(A′ + B′)(B′ + C)", "(A + B + C′)(A + C)(A′ + B′)(B + C)",
       "(A′ + B′ + C′)(A + C)(A + B)(B′ + C′)", "(A + B + C′)(A′ + C′)(A + B)(B′ + C′)"], 'D',
      'De Morgan turns the OR of four product terms into the AND of their complements: '
      '(A′B′C)′ = A + B + C′, (AC)′ = A′ + C′, (A′B′)′ = A + B, (BC)′ = B′ + C′.'),
    Q('Boolean algebra', [('p0', 44)],
      'Which of the following expressions resembles (AB + A′(A + B))(A + B)(A + C)?',
      ["(C′ + A′B′)′", "((A′ + B′)(A′ + C′)(B′ + C′))′", "(C′(A′ + B))′", "(A′ + B′C′)′"], None,
      'A′(A + B) = A′B, and AB + A′B = B. Then B(A + B) = B and B(A + C) = **AB + BC**. The options expand to '
      'AC + BC, AB + AC + BC, C + AB′ and AB + AC; none is AB + BC. If the last factor were (B + C) the result '
      'would be B, also not offered, so the question looks misprinted.',
      conf='flag', note='No option equals the simplified expression AB + BC.'),
    Q('Boolean algebra', [('p6', 58)],
      'If X = f(A, B, C, D) = Σ(1, 2, 4, 7, 8, 11, 13, 14) and Y(A, B, C, D) = Π(3, 5, 7, 8, 10, 11, 12, 13), '
      'then the expressions for X and Y respectively are:',
      ["A⊕B⊕C⊕D and A′⊕B′⊕C′⊕D′", "A⊕B⊕C′⊕D and (A′+C+D′)(B′+C+D′)(A′+C+D)(A′+B′+C′)",
       "ABCD and A⊕B⊕C⊕D", "A⊕B⊕C⊕D and (A+C′+D′)(B′+C+D′)(A′+C+D)(A′+B+C′)"], 'D',
      'X lists exactly the minterms with an odd number of ones, so X = A⊕B⊕C⊕D (odd parity).\n\n'
      'For Y, group the zeros (3, 5, 7, 8, 10, 11, 12, 13) on a K-map: 0-11 → (A + C′ + D′), -101 → '
      '(B′ + C + D′), 1-00 → (A′ + C + D), 101- → (A′ + B + C′). That is option D. Option A\'s second part is '
      'X again (an even number of inversions does not change parity).'),
    Q('Boolean algebra', [('p0', 55)],
      'How many entries does the truth table of a four-input circuit have?', ['12', '8', '16', '4'], 'C', '2⁴ = 16 rows.'),
    # ---- gates and combinational circuits ----
    Q('Gates and combinational circuits', [('p1', 42)],
      'In the circuit below (redrawn from the photo), which input combination makes the output F logic 1?',
      ['A = 0, B = 0, C = 1', 'A = 0, B = 0, C = 0', 'A = 0, B = 1, C = 1', 'A = 1, B = 1, C = 1'], None,
      'Work backwards. F = XNOR(G7, C) and G7 = XNOR(G5, G6, C), so the two C terms cancel and F = G5 ⊕ G6. '
      'With G5 = A + G4 and G6 = XNOR(A, G4): if A = 0, F = G4 ⊕ G4′ = 1; if A = 1, F = G4′.\n\n'
      'For A = B = C = 1: G1 = 0, G3 = 0, G4 = XNOR(1, 0) = 0, so F = 1 too. As drawn, **every option gives '
      'F = 1**. If G7 is a two-input gate (C going only to G8), F = G5 ⊕ G6 ⊕ C and only **A = 0, B = 0, C = 0** '
      'works, which is probably the intended answer.',
      fig='gates-p1q42', conf='flag',
      note='The photo is blurred around G7. As read, all four options give F = 1.'),
    Q('Gates and combinational circuits', [('p3', 47)],
      'For the NMOS circuit shown, what is Z?', ['(AB)', '(A + B)', '(A + B)′', '(AB)′'], 'D',
      'Z is pulled low only when both series transistors conduct, i.e. A = B = 1; otherwise the resistor pulls it '
      'high. Series pull-down = NAND.', fig='nmos-nand'),
    Q('Gates and combinational circuits', [('p4', 55)],
      'What function does this NAND-only circuit implement?', ['A + B', 'AB', '(AB)′ + (AB)′', 'A′ + B′'], 'A',
      'The first two NANDs have their inputs tied, so they give A′ and B′. The last gives (A′B′)′ = **A + B** '
      '(De Morgan).', fig='nand-or'),
    Q('Gates and combinational circuits', [('p4', 59)],
      'Find the output Y of the given circuit.', ['A + B', 'A′ + B′', 'A + B′', 'A′ + B'], 'A',
      'Y = [(A + B)′ · (BC)′]′ = (A + B) + BC = **A + B** (absorption).', fig='gates-p4q59'),
    Q('Gates and combinational circuits', [('p5', 55)],
      'In the combinational circuit shown, the inputs are A = 1 and B = 0. Determine the value of Q.',
      ['Output Q = 1 if we change inputs to A = 0 and B = 1', 'Output Q = 0', 'Output Q = 1', 'None of the above'], 'B',
      'G1·G3 = (A ⊕ B)·AB = 0 for every input, so the upper NAND is always 1. G3·G5 = AB·(A + B)′ = 0 for every '
      'input, so the lower NAND is always 1. Q = 1 ⊕ 1 = **0**, whatever A and B are (so the first option is '
      'false too).', fig='gates-p5q55'),
    Q('Gates and combinational circuits', [('p6', 50)],
      'Consider the figure. What is the only word (ABC) it disregards, i.e. gives Y = 0?', ['100', '101', '000', '111'], 'D',
      'Y = A′ + B′ + C′ = (ABC)′, which is 0 only for **111**.', fig='or-of-inverted'),
    Q('Gates and combinational circuits', [('p2', 42)],
      'What is the minimum number of NOR gates needed to realise Y = [A · (B · (C · D′)′)′]′ (bars over ABCD′, '
      'BCD′, CD′ and D)?',
      ['4 two-input NOR and 2 four-input NOR', '3 two-input NOR and 2 four-input NOR',
       '4 two-input NOR and 1 four-input NOR', '3 two-input NOR and 1 four-input NOR'], 'C',
      'Peel the bars from inside: (CD′)′ = C′ + D, so (B(C′ + D))′ = B′ + CD′, and Y = A′ + B(C′ + D) = '
      '(A′ + B)(A′ + C′ + D).\n\n'
      'A product of sums is a NOR–NOR circuit: Y = NOR(NOR(A′, B), NOR(A′, C′, D)). That needs two NORs as '
      'inverters (A′, C′), NOR(A′, B) and the output NOR: **four two-input NORs**, plus **one four-input NOR** '
      '(one input tied low) for the three-literal sum.'),
    Q('Gates and combinational circuits', [('p1', 54)],
      'The circuit-level design using inverters and tri-state buffers shown below can be used as a:',
      ['Half adder', '2:1 multiplexer', 'Full adder', 'D flip-flop'], 'B',
      'X enables the In1 buffer and X′ enables the In0 buffer, so exactly one input drives the shared output: '
      'Out = X·In1 + X′·In0.', fig='tristate-mux'),
    Q('Multiplexers and decoders', [('p5', 54)],
      'How can a 2:1 MUX be used as a NOT gate?',
      ['D₀ = input, D₁ = 1, select line = 0', 'D₀ = 1, D₁ = 0, select line = input',
       'D₀ = 1, D₁ = input, select line = 1', 'D₀ = 0, D₁ = 0, select line = input'], 'B',
      'Y = S′D₀ + SD₁ = S′·1 + S·0 = S′ with the input on the select line.'),
    Q('Multiplexers and decoders', [('p4', 56)],
      'For the 4:1 MUX shown (I₀ = 1, I₁ = 0, I₂ = 0, I₃ = 1, S₁ = A, S₀ = B), what is f?',
      ['A′B + A', 'A′B + AB′', 'AB', 'AB + A′B′'], 'D',
      'f = A′B′·I₀ + A′B·I₁ + AB′·I₂ + AB·I₃ = **A′B′ + AB** (XNOR).', fig='mux4'),
    Q('Multiplexers and decoders', [('p6', 53)],
      'A 4:1 MUX has D₀ = x and D₁ = D₂ = D₃ = 1, with select lines S₁ = B and S₀ = A. What is the output? Now '
      'D₀ and D₁ are given x, while D₂ and D₃ are given x′. What is the new output?',
      ['A ⊕ x and A ⊕ x', 'A + B + x and A + x', 'A + B + x and B ⊕ x', 'A + B + x and A ⊕ x'], 'C',
      'First: Y = A′B′x + A′B + AB′ + AB = A′B′x + A + B = **A + B + x**.\n\n'
      'Second: the inputs depend only on S₁ = B (x when B = 0, x′ when B = 1), so Y = B′x + Bx′ = **B ⊕ x**.'),
    Q('Multiplexers and decoders', [('p2', 49)],
      'For the given 74LS139 decoder circuit, what is Y?', ['A NOR B', 'A XOR B', 'A OR B', 'A NAND B'], 'B',
      'The 74LS139 outputs are active-low: Y0 = m₀′ and Y3 = m₃′. The input bubbles invert them back, the OR gives '
      'm₀ + m₃ = A′B′ + AB, and the output bubble inverts that: Y = (A ⊙ B)′ = **A ⊕ B**.', fig='decoder-xor'),
    Q('Multiplexers and decoders', [('p4', 46)],
      'A 5:32 decoder is to be designed. The engineer is provided with one 2:4 decoder and N 3:8 decoders. What is N?',
      ['2', '8', '5', '4'], 'D',
      'The two MSBs go to the 2:4 decoder, whose four outputs enable four 3:8 decoders driven by the three LSBs: '
      '4 × 8 = 32 outputs.'),
    Q('Arithmetic circuits', [('p5', 41)],
      'Calculate the minimum number of NAND gates required to implement a three-bit magnitude comparator having '
      'one output that goes HIGH when the two three-bit numbers are equal.',
      ['17', '16', '14', '15'], 'A',
      'E = (A₂ ⊙ B₂)(A₁ ⊙ B₁)(A₀ ⊙ B₀). Each XNOR costs 5 NANDs (4 for XOR, 1 to invert): 15. The 3-input AND is '
      'a 3-input NAND plus an inverting NAND: 2. Total **17**.',
      conf='medium', note='Counts in other books vary with which XOR form is used; 17 is the standard textbook count.'),
    Q('Programmable logic', [('p2', 56)],
      'A 4-bit BCD adder is implemented in a programmable ROM, and a control input switches it to a subtractor. '
      'What ROM size is needed?', ['1K × 8', '1K × 5', '32K', '4K × 4'], 'B',
      'Address inputs: two 4-bit digits + carry/borrow in + the add/subtract control = 10 bits → 2¹⁰ = 1K words. '
      'Outputs: the 4-bit result digit + carry/borrow out = 5 bits. So **1K × 5**.'),
    Q('Programmable logic', [('p3', 44)],
      'For the PLA shown, what is the value of F?', ['A', 'ABC′', 'B', 'AB′'], 'C',
      'The product lines are ABC, A′B and ABC′. ABC + ABC′ = AB, and AB + A′B = **B**.', fig='pla-or'),
    Q('Programmable logic', [('p5', 59)],
      'What is the value of the function F1 (A = MSB, C = LSB) in the PLA shown?',
      ['F1 = Σ(1, 4, 7)', 'F1 = Σ(0, 3, 7)', 'F1 = Π(0, 2)', '(fourth option not visible in the photo)'], None,
      'The eight AND rows are the minterms m₀ … m₇ in order (row 1 taps A′, B′, C′; row 2 taps A′, B′, C; and so on). '
      'F1\'s OR line has crosses on rows m₀ and m₂, so **F1 = Σ(0, 2) = A′C′**. Σ(1, 4, 7) is F2, and Π(0, 2) is the '
      'complement of the right answer. If the cut-off fourth option reads Σ(0, 2), pick it.',
      fig='pla-minterms', conf='flag', note='The correct value Σ(0, 2) is not among the three visible options.'),
    Q('Programmable logic', [('p4', None)],
      'For a CPLD (complex programmable logic device), the status of the AND array and the OR array will be:',
      ['Programmable AND array and fixed OR array', 'Fixed AND array and fixed OR array',
       'Fixed AND array and programmable OR array', 'Programmable AND array and programmable OR array'], 'A',
      'A CPLD is built from PAL-style macrocells: a programmable AND array feeding a fixed OR. Both programmable is '
      'a PLA; fixed AND with programmable OR is a PROM.'),
    # ---- latches and flip-flops ----
    Q('Latches and flip-flops', [('p1', 52)],
      'What is the difference between a latch and a flip-flop?',
      ['Latches are used in synchronous circuits and flip-flops in asynchronous circuits',
       'Latches are level-triggered and flip-flops are edge-triggered',
       'Latches store bits and flip-flops store data', 'Latches are analog and flip-flops are digital'], 'B',
      'A latch is transparent while its enable is at the active level; a flip-flop samples only at a clock edge.'),
    Q('Latches and flip-flops', [('p3', 51)],
      'Find the mode of operation of the given SR latch during the period starting at e (e to f).',
      ['Reset', 'Set', 'Hold', 'Prohibit'], 'D',
      'Between e and f both S and R are 1, the forbidden input of a NOR SR latch (both outputs are forced to 0). '
      'For the other intervals: a–b prohibited, b–c reset, c–d hold, d–e reset, f–g reset.',
      fig='sr-wave', conf='medium', note='Waveforms read from a photo; the timing of the R dip is approximate.'),
    Q('Latches and flip-flops', [('p3', 56)],
      'A flip-flop has inputs P and N with the behaviour below. What is its characteristic equation?',
      ["Q′ + PN", "PQ′N", "Q + PN′", "P′ + QN′"], 'A',
      'Qnext is Q′ in three rows and 1 when P = N = 1, so Qnext = Q′ + PN.',
      table='| P | N | Qnext |\n|:-:|:-:|:-:|\n| 0 | 0 | Q′ |\n| 0 | 1 | Q′ |\n| 1 | 0 | Q′ |\n| 1 | 1 | 1 |'),
    Q('Latches and flip-flops', [('p4', None)],
      'What is the next-state equation of a T flip-flop?',
      ['Qn+1 = T + Qn', 'Qn+1 = T ⊙ Qn', 'Qn+1 = (T + Qn)(T·Qn)', 'Qn+1 = T ⊕ Qn'], 'D',
      'T = 0 holds, T = 1 toggles: Qn+1 = TQn′ + T′Qn = T ⊕ Qn.'),
    Q('Latches and flip-flops', [('p2', 44)],
      'How is a D flip-flop converted into a T flip-flop?', ['D = Q′', 'D = 0', 'D = Q', 'D = 1'], 'A',
      'In general D = T ⊕ Q. With T held at 1 (a toggle flip-flop), D = Q′.',
      conf='medium', note='The full conversion is D = T ⊕ Q; the options assume T = 1.'),
    Q('Latches and flip-flops', [('p0', 43)],
      'The output of the 2:1 MUX is fed to a D flip-flop, and the Q output of the flip-flop is fed back to the '
      'select line of the MUX. The set-up works as a:',
      ['JK flip-flop', 'RS flip-flop', 'D flip-flop', 'Mod-3 counter'], 'A',
      'D = Q′·J + Q·K′, which is exactly the JK characteristic equation Qnext = JQ′ + K′Q.',
      fig='mux-dff'),
    Q('Latches and flip-flops', [('p4', 47)],
      'A circuit diagram of a J-K flip-flop built from gates is shown. What is the output Q if J = 1 and K = 0?',
      ['Last state', '1', '0', 'Undefined'], 'B',
      'With K = 0 Gate 1 is 0, so it cannot reset; with J = 1 and Q′ = 1 (or already set) Gate 2 drives the set '
      'side on the clock. J = 1, K = 0 is the set condition: Q = **1**.', fig='jk-from-gates'),
    Q('Latches and flip-flops', [('p3', 52)],
      'If the inputs to a JK flip-flop are J = 01010101 and K = 10001101 (one bit per clock, left first), what is Q′?',
      ['01010101', '01110110', '10010101', '10001001'], 'D',
      '| J | 0 | 1 | 0 | 1 | 0 | 1 | 0 | 1 |\n|---|---|---|---|---|---|---|---|---|\n'
      '| K | 1 | 0 | 0 | 0 | 1 | 1 | 0 | 1 |\n| action | reset | set | hold | set | reset | toggle | hold | toggle |\n'
      '| Q | 0 | 1 | 1 | 1 | 0 | 1 | 1 | 0 |\n\n'
      'The first pair resets, so the start state does not matter. Q′ = **10001001**.'),
    Q('Latches and flip-flops', [('p6', 44)],
      'The initial output of the flip-flop shown is 0 and the clock frequency is 12 kHz. What is the output '
      'frequency?', ['6 kHz', '12 kHz', '3 kHz', '48 kHz'], 'A',
      'S is fed from Q′ and R from Q, so every clock edge sets a reset flip-flop or resets a set one: it toggles. '
      'A toggle flip-flop divides the clock by 2, so **6 kHz**.', fig='sr-toggle'),
    Q('Latches and flip-flops', [('p0', 57)],
      'The circuit has three flip-flops: A is a D flip-flop with D_A = BC, B is a T flip-flop with T_B = 1, and C is '
      'a JK flip-flop with J_C = K_C = B′, all on one clock. The present state ABC = 101. What is the state after '
      '6 clock pulses?', ['010', '101', '000', '110'], 'C',
      'A⁺ = BC, B⁺ = B′, C⁺ = C ⊕ B′.\n\n'
      '101 → 010 → 000 → 011 → 101 → …, a cycle of 4. Six pulses = one full cycle + 2, so the state is **000**.',
      fig='three-ff'),
    # ---- registers and sequential design ----
    Q('Registers and sequential design', [('p6', 47)],
      'The serial-in parallel-out shift register shown has feedback X = (D₃ ⊕ D₂) ⊕ (D₁D₀)′. If its initial state '
      'is 1111, what is the content of the register after the 3rd clock pulse?',
      ['1011', '0111', '0110', '1101'], 'A',
      'The serial input enters at the D₀ end (the arrow is on that side) and data shifts toward D₃.\n\n'
      '| Clock | X computed from | Register D₃D₂D₁D₀ |\n|:-:|---|:-:|\n| 0 | | 1111 |\n'
      '| 1 | (1⊕1)⊕(1·1)′ = 0 | 1110 |\n| 2 | (1⊕1)⊕(1·0)′ = 1 | 1101 |\n| 3 | (1⊕1)⊕(0·1)′ = 1 | **1011** |',
      fig='sipo', conf='medium',
      note='If the serial input entered at D₃ instead, the sequence would be 0111, 1011, 1101 and the answer 1101.'),
    Q('Registers and sequential design', [('p3', 57)],
      'In the figure, a MUX is placed in front of every flip-flop with a common select S. How do the flip-flops '
      'behave in normal mode and in scan mode?',
      ['As flip-flops in both modes', 'As usual in scan mode and as a shift register in normal mode',
       'As a shift register in both modes', 'As usual in normal mode and as a shift register in scan mode'], 'D',
      'This is a scan chain (design for test). In normal mode (S = 0) each flip-flop captures its functional input '
      'D; in scan mode (S = 1) each captures the previous flip-flop\'s Q, so the chain shifts test data from SI to SO.',
      fig='scan-chain'),
    Q('Registers and sequential design', [('p6', 49)],
      'Consider the counter table below. It is required to design the counter with J-K flip-flops. Find the input J_C.',
      ["A′B′", 'AB', "A′B", "AB′"], 'D',
      'J_C matters only when C = 0 (when C = 1 it is a don\'t-care). C goes 0 → 1 only from 001, so J_C = 1 at '
      'CBA = 001 and 0 at 000, 010, 011. Using the don\'t-cares, J_C = **AB′**.',
      table='| C | B | A | → C | B | A |\n|:-:|:-:|:-:|:-:|:-:|:-:|\n| 0 | 0 | 0 | 0 | 1 | 0 |\n'
            '| 0 | 0 | 1 | 1 | 0 | 0 |\n| 0 | 1 | 0 | 0 | 1 | 1 |\n| 0 | 1 | 1 | 0 | 0 | 1 |\n'
            '| 1 | 0 | 0 | 1 | 1 | 0 |\n| 1 | 0 | 1 | 0 | 0 | 0 |\n| 1 | 1 | 0 | 0 | 0 | 0 |\n| 1 | 1 | 1 | 0 | 0 | 0 |'),
    Q('Registers and sequential design', [('p6', 46)],
      'JK flip-flops are used to design a sequence detector for 1001 (overlap allowed); the output is 1 when the '
      'sequence is detected, e.g. input 10010100110101010100100110. Two flip-flops A and B are needed. What are '
      'their input equations (X is the input)?',
      ["JA = B′X′, KA = B′ + X, JB = X + A, KB = X", "JA = BX′, KA = B′ + X, JB = X + A, KB = X′",
       "JA = B′X′, KA = B′ + X′, JB = X′ + A, KB = X′", "JA = BX, KA = B + X, JB = X + A′, KB = X"], None,
      'A Mealy detector with S0 = 00 (nothing), S1 = 01 ("1"), S2 = 11 ("10"), S3 = 10 ("100"):\n\n'
      '| State AB | X = 0 | X = 1 |\n|:-:|:-:|:-:|\n| 00 | 00 | 01 |\n| 01 | 11 | 01 |\n| 11 | 10 | 01 |\n'
      '| 10 | 00 | 01, Z = 1 |\n\n'
      'This gives **JA = BX′, KA = B′ + X, JB = X, KB = AX′, Z = AB′X**. Option B matches the A equations exactly '
      'but not the B ones, and a brute-force check of all 24 state assignments shows that none of the four options '
      'detects 1001.',
      conf='flag', note='No option implements the detector; option B is the closest.'),
    # ---- counters ----
    Q('Counters', [('p2', 47)],
      'How many flip-flops are needed for a mod-35 counter?', ['5', '4', '6', '7'], 'C',
      'Need 2ⁿ ≥ 35: 2⁵ = 32 is too small, 2⁶ = 64 works, so **6**.'),
    Q('Counters', [('p2', 46)],
      'A binary counter with N flip-flops counts from 0 to 783. What is N?', ['10', '11', '9', '8'], 'A',
      '784 states: 2⁹ = 512 < 784 ≤ 1024 = 2¹⁰, so **10**.'),
    Q('Counters', [('p2', 43)],
      'A counter is clocked at 256 kHz and the output of its last flip-flop is 2 kHz. What is the MOD number?',
      ['100', '125', '128', '208'], 'C', '256 / 2 = **128**.'),
    Q('Counters', [('p2', 50)],
      'How many flip-flops are needed to build the counter with the state diagram shown?', ['3', '2', '1', '4'], 'D',
      'The states are 4-bit words (0001, 0010, …, 1111) used directly as outputs, so each bit needs its own '
      'flip-flop: **4**. Three would suffice only for a binary-encoded 8-state machine followed by decoding.',
      fig='ring-states', conf='medium', note='Reading: the states themselves are the flip-flop outputs.'),
    Q('Counters', [('p3', 49)],
      'A 4-bit ripple **down** counter is at state 1000. How many flip-flops change state after 3 clock pulses?',
      ['2', '1', '3', '4'], 'C',
      '1000 → 0111 → 0110 → 0101. Comparing 1000 with 0101, three bits differ: **3**.',
      conf='medium', note='If the question means the flip-flops that toggle on the 3rd pulse alone (0110 → 0101), '
      'the answer would be 2.'),
    Q('Counters', [('p4', 54)],
      'The given circuit is a cascade of 4 J-K flip-flops. It works as a:',
      ['Mod-5 asynchronous DOWN counter', 'Mod-5 asynchronous UP counter', 'Mod-10 asynchronous UP counter',
       'Mod-10 asynchronous DOWN counter'], 'C',
      'J = K = 1, so each stage toggles, and each stage is clocked by the previous Q: a ripple counter. The AND of '
      'Q₁ and Q₃ clears everything when the count reaches 1010 (ten), so it counts 0 … 9: **mod-10 up**.',
      fig='mod10', conf='medium',
      note='Assumes negative-edge-triggered flip-flops, the usual ripple up-counter; with positive-edge stages '
      'clocked from Q it would count down, and the clear at Q₁Q₃ would not give a clean mod-10.'),
    Q('Counters', [('p0', 54)],
      'In the counter of the figure (4 J-K flip-flops, J₀ = K₀ = HIGH, the other J = K pairs driven by NAND gates of '
      'the Q outputs), the counter locks after some initial states into two final states, toggling alternately '
      'between them. Identify the states.',
      ['1001 and 0110', '1110 and 0001', '1010 and 0101', '1111 and 0000'], 'C',
      'In a lock-up pair every bit toggles on every clock, so every J = K input must be 1 in both states, i.e. '
      'every NAND must see a 0 in both states. All-ones (1111) gives at least one NAND all-ones inputs, so '
      '1111 ↔ 0000 is impossible. Simulating the readable wirings, the pair that survives in all of them is '
      '**1010 ↔ 0101**.',
      fig='lockup-pair', conf='medium',
      note='The NAND wiring in the photo is partly illegible; the figure shows the resulting lock-up cycle.'),
    # ---- timing ----
    Q('Timing', [('p6', 51)],
      'What is the maximum frequency of operation of a flip-flop if t_setup = 1 ns, t_pd = 5 ns and t_ns = 2 ns '
      '(total negative slack)?', ['165 MHz', '98 MHz', '205 MHz', '125 MHz'], 'D',
      'Without slack the minimum period is t_pd + t_setup = 6 ns (166.7 MHz). Negative slack of 2 ns means the path '
      'misses that target by 2 ns, so the achievable period is 8 ns: **125 MHz**.',
      conf='medium', note='165 MHz is the trap answer that ignores the slack.'),
    Q('Timing', [('p6', 56)],
      'In the figure below, timing analysis shows that the Gate signal arrives later than the CLK input. What is '
      'the effect and how can it be removed?',
      ['Glitch will occur and it can be removed by A gating signal',
       'Glitch will occur and it can be removed either by A gating signal or B gating signal',
       'Glitch will occur and it cannot be removed by A gating signal or B gating signal',
       'Glitch will occur and it can be removed by B gating signal'], 'A',
      'Gate falls while CLK is high, so the flip-flop sees a narrow sliver pulse (a glitch), and its rise in the '
      'next high phase clips the following pulse. For an AND clock gate the enable must change only while CLK is '
      'low. "A gating" has the same meaning as Gate but switches during the low phase, so it removes the glitch. '
      '"B gating" also switches while CLK is low but is inverted, so it would let through the wrong pulses.',
      fig='clock-gating', conf='medium', note='Waveforms read from a photo.'),
    Q('Timing', [('p1', 58)],
      'For the net in the figure, how do we represent the net delay?',
      ['f(C_net + C_pin)', 'f(C_pin)', 'f(R_net)', 'f(R_net, C_net + C_pin)'], 'D',
      'Interconnect delay is an RC delay: the net resistance charging the net capacitance plus the input-pin '
      'capacitance of the load (Elmore delay ≈ R_net·(C_net/2 + C_pin)).',
      fig='net-delay', conf='medium', note='The fourth option was cut off in the photo; it is written here as the '
      'expected R-and-C form.'),
    # ---- logic families and device circuits ----
    Q('Logic families', [('p0', 48)],
      'Which digital IC family consumes the minimum power?', ['ECL', 'DTL', 'TTL', 'CMOS'], 'D',
      'Static CMOS draws almost no current except while switching. ECL is the most power-hungry because its '
      'transistors never saturate and current always flows.'),
    Q('Logic families', [('p2', 45)],
      'Which logic families are non-saturated?', ['RTL and TTL', 'TTL and DCTL', 'DTL and HTL',
                                                  'Schottky TTL and ECL'], 'D',
      'ECL keeps its transistors in the active region; Schottky TTL clamps the base-collector junction with a '
      'Schottky diode so the transistor never saturates. That is why both are fast.'),
    Q('Logic families', [('p5', 52)],
      'Which one of the given families has the highest noise margin?',
      ['Schottky TTL', 'CMOS', 'Standard TTL', 'Low-power Schottky TTL'], 'B',
      'CMOS switches near V_DD/2 with rail-to-rail outputs, giving noise margins of roughly 30–45% of V_DD, '
      'against about 0.4 V for TTL.'),
    Q('Logic families', [('p4', 49)],
      'How many 74ALS00 NAND-gate inputs can be driven by one 74ALS00 NAND-gate output? Given I_OL(max) = 8 mA, '
      'I_IL(max) = 0.1 mA, I_OH(max) = 0.4 mA, I_IH(max) = 20 µA.', ['20', '8', '10', '15'], 'A',
      'LOW: 8 / 0.1 = 80. HIGH: 0.4 mA / 20 µA = 20. Fan-out is the smaller: **20**.'),
    Q('Logic families', [('p6', 57)],
      'The output of an inverter drives a parallel register made of 74AS74 D flip-flops. What is the maximum number '
      'of flip-flop CLR inputs this gate can drive? Given I_IH = 40 µA, I_IL = 1.8 mA, I_OH = 2 mA, I_OL = 20 mA.',
      ['40', '35', '11', '50'], 'C',
      'HIGH: 2 mA / 40 µA = 50. LOW: 20 / 1.8 = 11.1, so 11. Fan-out = min = **11**.'),
    Q('Logic families', [('p1', None)],
      'For the DTL NAND gate shown, V_γ(BE) = 0.5 V, V_CE(sat) = 0.2 V, the drop across a conducting diode is '
      '0.7 V and the diode cut-in voltage is 0.6 V. What is the noise margin when one input is LOW?',
      ['0.9 V', '0.5 V', '0.6 V', '0.8 V'], 'D',
      'With an input at V_CE(sat) = 0.2 V, node P sits at 0.2 + 0.7 = 0.9 V. Q1 starts to turn on when P reaches '
      'the cut-in of D1 + D2 + the base-emitter junction: 0.6 + 0.6 + 0.5 = 1.7 V. Noise margin = 1.7 − 0.9 = '
      '**0.8 V**.', fig='dtl-nand'),
    Q('Logic families', [('p3', 58)],
      'In the TTL NAND circuit shown, input A = +5 V and input B is grounded. Which is true about Q2, Q3 and Q4?',
      ['Q2 OFF, Q3 ON, Q4 OFF', 'Q2 ON, Q3 ON, Q4 OFF', 'Q2 OFF, Q3 OFF, Q4 ON', 'Q2, Q3 and Q4 all OFF'], 'A',
      'B low clamps node Y at about 0.7 V through D3. Turning on D4, Q2 and Q4 would need about 2.1 V, so Q2 and '
      'Q4 are OFF. With Q2 off, R2 pulls Q3\'s base high and Q3 (with D1) pulls the output X HIGH: a NAND with one '
      'input low.', fig='ttl-nand'),
    Q('Logic families', [('p5', 53)],
      'For the TTL NOT gate shown, the diode D at the output node is used:',
      ['to restore the logic level degradation', 'to provide necessary collector-emitter drop across Q2',
       '(option not visible)', '(option not visible)'], None,
      'D keeps Q4 cut off when the output is LOW. Then Q2 and Q3 conduct, so Q4\'s base is only at '
      'V_CE(sat)(Q2) + V_BE(Q3) ≈ 0.9 V, while Q4 plus D plus Q3 in series need about 0.7 + 0.7 + 0.2 = 1.6 V. '
      'Without D both totem-pole transistors could conduct together. Choose the option that says this.',
      fig='ttl-not', conf='flag', note='Two of the four options were cut off; neither visible option is the purpose of D.'),
    Q('Logic families', [('p3', 42)],
      'A sudden flow of static electricity between two electrically charged objects for a very short time is:',
      ['ESD', 'Avalanche breakdown', 'Pinch-off', 'Short circuit'], 'A', 'Electrostatic discharge (ESD).'),
    Q('MOS circuits', [('p3', 41)],
      'In the sampling circuit shown, M1\'s gate is at +3 V, the input is a 0.5 V sine wave at 10 MHz, C_H = 1 pF, '
      'µnCox = 50 µA/V², W/L = 10/1, V_th = 0.7 V, V_DD = 3 V, γ = 0. Find the (worst-case) on-resistance of M1.',
      ['2.5 kΩ', '1.11 kΩ', '5 kΩ', '3.25 kΩ'], 'B',
      'In triode, R_on = 1 / [µnCox (W/L)(V_GS − V_th)] with V_GS = 3 − V_in. It is largest at the input peak, '
      'V_in = 0.5 V: R_on = 1 / (50 µ × 10 × 1.8) = **1.11 kΩ**.',
      fig='sample-switch', conf='medium',
      note='The question says "minimum"; 1.11 kΩ is the value at the input peak, which is the largest (worst-case) '
      'on-resistance and the one used to size the switch.'),
    Q('MOS circuits', [('p0', 42)],
      'A cell in a DRAM must hold 3 V, and the voltage must stay above 1 V. It is refreshed every 10 ms and the '
      'leakage (discharge) current is 0.1 µA. What is the storage capacitance?',
      ['1 nF', '10 mF', '0.5 nF', '0.1 µF'], 'C',
      'C = I·Δt / ΔV = 0.1 µA × 10 ms / (3 − 1) V = 10⁻⁹ / 2 = **0.5 nF**.'),
    # ---- data converters ----
    Q('Data converters', [('p0', 47)],
      'A 4-bit R-2R ladder DAC has V_ref = 3 V. What is the analog output for the input 0101?',
      ['0.6252 V', '0.9375 V', '1.2542 V', '1.4891 V'], 'B', 'V_out = V_ref × D / 2ⁿ = 3 × 5 / 16 = **0.9375 V**.'),
    Q('Data converters', [('p3', 48)],
      'How many equal intervals are there in a 16-bit DAC?', ['65535', '16383', '23412', '23441'], 'A',
      '2¹⁶ levels make 2¹⁶ − 1 = **65535** steps between full scale and zero.'),
    Q('Data converters', [('p3', 50)],
      'What is the SNR of a 16-bit ADC (in dB)?', ['67', '98', '75', '86'], 'B',
      'Ideal SNR = 6.02 N + 1.76 = 6.02 × 16 + 1.76 ≈ **98 dB**.'),
    Q('Data converters', [('p5', 58)],
      'Which one of the options given below is **not** a component of a SAR-type analog-to-digital converter?',
      ['R-2R ladder', 'Digital-to-analog converter', 'Op-amp', 'Comparator'], 'C',
      'A SAR ADC is a successive-approximation register, a DAC (often an R-2R ladder) and a comparator, plus a '
      'sample-and-hold. A separate op-amp is not one of its defining blocks.',
      conf='medium', note='Some DAC implementations use an op-amp internally, so the question relies on the block-level view.'),
    Q('Data converters', [('p4', 52)],
      'The full-scale output and full-scale error of an 8-bit DAC are 2 mA and ±0.6% F.S. What is the possible '
      'output range for the binary input 10010000?',
      ['1468 to 1504 µA', '1666 to 1702 µA', '1264 to 1302 µA', '1865 to 1897 µA'], None,
      'Step = 2 mA / 255 ≈ 7.84 µA. 10010000 = 144, so the ideal output is 144 × 7.84 ≈ 1129 µA, and the error is '
      '±0.6% × 2 mA = ±12 µA: **1117 to 1141 µA**, which is not offered. The options are 36 µA wide, which matches '
      '±0.9% F.S., so the numbers in the question were probably changed.',
      conf='flag', note='The computed range 1117–1141 µA is not among the options.'),
    # ---- circuits, signals and misc ----
    Q('Circuits and signals', [('p0', 59)],
      'Three resistors of 6 kΩ each and three capacitors of 6 F each are all connected in parallel. What are the '
      'effective resistance and capacitance?',
      ['2 kΩ and 2 F', '18 kΩ and 18 F', '18 kΩ and 2 F', '2 kΩ and 18 F'], 'D',
      'Resistors in parallel: 6k / 3 = 2 kΩ. Capacitors in parallel add: 3 × 6 = 18 F.'),
    Q('Circuits and signals', [('p0', 56)],
      'A 15 Ω resistor in series with an inductor carries i(t) = 2 + 3 sin(100t + 30°) + 5 sin(…t + 30°) A. Find '
      'the RMS current and the power consumed.',
      ['√10 A and 315 W', '√21 A and 215 W', '√15 A and 300 W', '√21 A and 315 W'], 'D',
      'I²_rms = 2² + 3²/2 + 5²/2 = 4 + 4.5 + 12.5 = 21, so I_rms = √21 A. Only the resistor dissipates: '
      'P = 21 × 15 = **315 W**.'),
    Q('Circuits and signals', [('p1', 51)],
      'A 1 MΩ resistor is connected to a capacitor C. The capacitor voltage drops by 65% in 6.5 s. What is C?',
      ['6.5 µF', '6.2 µF', '1 µF', '15 µF'], 'B',
      '35% remains: 0.35 = e^(−t/RC), so RC = 6.5 / ln(1/0.35) = 6.5 / 1.05 ≈ 6.19 s and C = 6.19 s / 1 MΩ ≈ **6.2 µF**.'),
    Q('Circuits and signals', [('p4', 58)],
      'In voltage measurement, determine the RMS value of the voltage if the peak-to-peak voltage is 6 V.',
      ['2.12 V', '4.14 V', '3.13 V', '1.11 V'], 'A', 'Peak = 3 V; for a sine, RMS = 3 / √2 = **2.12 V**.'),
    Q('Circuits and signals', [('p2', 53)],
      'How many RC pairs are used in a second-order op-amp low-pass filter?', ['8', '1', '4', '2'], 'D',
      'Each RC section adds one pole; a second-order (e.g. Sallen–Key) low-pass uses **two** RC pairs.'),
    Q('Circuits and signals', [('p5', 56)],
      'Which among the following is the power spectral density (PSD) of Brownian noise?',
      ['1/f', '1', '1/f²', '1/f³'], 'C',
      'Brownian (red) noise is integrated white noise, so its PSD falls as **1/f²**. White noise is flat (1) and '
      'pink noise is 1/f.'),
    Q('Circuits and signals', [('p2', 60)],
      'Identify the type of relay shown.', ['SPST', 'DPDT', 'DPST', 'SPDT'], 'A',
      'One moving contact (single pole) that closes onto one fixed contact (single throw).', fig='relay'),
    Q('Memory devices', [('p6', 60)],
      'In the case of an EPROM, which type of rays is used to erase the data stored in memory?',
      ['Infrared rays', 'Supersonic rays', 'Ultraviolet rays', 'Microwave rays'], 'C',
      'UV light through the quartz window gives the trapped floating-gate electrons enough energy to escape. '
      'EEPROM and flash erase electrically instead.'),
    Q('Control unit', [('p6', 43)],
      'Which is not a part of a hardwired control unit?', ['Logic gates', 'Counters', 'ROM', 'Decoders'], 'C',
      'A hardwired control unit is built from gates, decoders and counters (step counter). A ROM holding control '
      'words is the control memory of a microprogrammed control unit.'),
    Q('Testing', [('p0', 52)],
      'What is the term for how easily any particular node X can be set to logic 1 or 0 through input vectors, '
      'with the error at X propagated to the output?',
      ['Testability', 'Observability', 'Controllability', 'All of the above'], 'A',
      'Setting a node to a value is controllability; seeing its effect at an output is observability. Needing both '
      'is testability.',
      conf='medium', note='The question text in the photo is garbled; this is the reading that fits the options.'),
    Q('Testing', [('p4', 51)],
      'The figure (a verification flow with test-case planning, VIP classes, an execution platform and tracking) '
      'is shown. Which of the following is best suited and used in the areas of DFT?',
      ['Timing analysis', 'Fault models', 'Delay calculation', 'Silicon debugging'], 'B',
      'Design for test generates test patterns against fault models (stuck-at, transition, bridging) and measures '
      'fault coverage; that is the DFT-specific item in the list.',
      conf='medium', note='The figure and the question are only loosely connected in the photo.'),
]
