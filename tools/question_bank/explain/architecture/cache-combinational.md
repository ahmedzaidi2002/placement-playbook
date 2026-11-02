@@ mw-iisc-10
**Answer: write-back**

**Why.** In write-back, a write updates only the cache line and marks it "dirty"; main memory is updated later, when the line is evicted. In write-through, every write updates both cache and memory.

**Concept: write policies.** Write-through is simple and keeps memory always current, but costs memory bandwidth on every write (usually softened with a write buffer). Write-back saves bandwidth when a line is written many times, at the cost of complexity (dirty bits, coherence).

@@ mw-iisc-2
**Answer: (b) size of the cache** (adding cache levels, (c), is also defensible)

**Why.** A larger cache holds more of the program's working set, so more accesses hit. More cache levels can raise the combined hit rate. RAM size doesn't change cache hits, and access speed changes the hit **time**, not the hit rate. (Mapping/associativity and replacement policy matter too.)

**Concept: why caches work.** Locality: programs reuse recent data (temporal) and nearby data (spatial). Hit rate depends on capacity, block size, associativity and replacement policy.

@@ mw-iisc-7
**Answer: (b) to select the memory module**

**Why.** In low-order interleaving, consecutive addresses go to consecutive modules (word 0 in module 0, word 1 in module 1, ...). So the lowest bits choose the module and the higher bits the word inside it.

**Concept: interleaving for bandwidth.** Sequential accesses hit different modules, which can work in parallel, so a burst of consecutive words is fetched faster than from one module.

@@ qc-n-cache
**Answer: (d) capacity miss**

**Why.** If the working set is larger than the whole cache, blocks get evicted before they are reused even with perfect placement: capacity misses.

**Concept: the 3 Cs of cache misses.** Compulsory (cold): first access to a block. Capacity: cache too small for the working set. Conflict: too many blocks map to the same set (limited associativity), even though the cache has space elsewhere.

@@ qc25-cache
**Answer: (d) 0.1008**

**Why.** An access reaches main memory only if it misses L1 **and** misses L2. With L2's hit rate measured among L1 misses (a local hit rate): (1 − 0.58)(1 − 0.76) = 0.42 × 0.24 = 0.1008.

**Concept: multi-level caches.** Global miss rate = product of local miss rates. Average access time = L1 hit time + L1 miss rate × (L2 hit time + L2 local miss rate × memory time).

@@ qcc-arch-40
**Answer: (d) cache memory** (counting registers as level 1)

**Why.** From the CPU outwards: registers (level 1), cache (level 2), main memory (level 3), secondary storage (level 4). (Books that start at level 0 for registers would call main memory the second level.)

**Concept: memory hierarchy.** Each level is larger, slower and cheaper per byte than the one above it. Caching frequently used data in the faster level gives the illusion of a memory that is both big and fast.

@@ qcc-arch-41
**Answer: (d) only (I), write back**

**Why.** Write back writes only to the cache block, marks it dirty, and writes it to memory when the block is replaced. Write through updates memory on every write.

**Concept: write policies** (see above). On a write miss, write-back caches usually "write-allocate" (fetch the block, then write), write-through caches often don't.

@@ qcc-arch-42
**Answer: (d) only (I), (IV) and (V)**

**Why.** A DRAM sends the row address first (high-order bits, latched by RAS) and then the column address on the same pins (low-order bits, latched by CAS). Multiplexing halves the address pins (I). (IV) is true. (V) is meant as the column statement (it misprints "row address strobe" for CAS).

**Concept: DRAM addressing.** Cells are in a grid. Activating a row (RAS) copies the whole row into sense amplifiers; the column address (CAS) then picks bits from that row. Reading more columns from an already-open row is fast.

@@ qcc-arch-43
**Answer: (b) (III), (I), (II)**

**Why.** Put the address in the Memory Address Register, assert the read signal, wait for memory, and the word arrives in the Memory Data Register for the CPU.

**Concept: MAR and MDR.** MAR holds the address being accessed; MDR (or MBR) holds the data going to or from memory. Every memory access goes through these two registers.

@@ qcc-dig-77
**Answer: (c) ultraviolet rays**

**Why.** UV light through the chip's quartz window gives the electrons trapped on the floating gates enough energy to escape, erasing the whole chip. EEPROM and flash erase electrically instead.

**Concept: ROM family.** ROM (fixed at manufacture), PROM (programmed once), EPROM (UV-erasable), EEPROM (electrically erasable byte by byte), Flash (electrically erasable in blocks, dense and cheap).

@@ ti-cache-sets
**Answer: (b) 16**

**Why.** 256-byte cache ÷ 8-byte lines = 32 lines. 2-way set-associative means 2 lines per set: 32/2 = 16 sets.

**Concept: cache geometry.** Sets = cache size / (line size × associativity). An address splits into tag | set index (log₂ sets bits) | byte offset (log₂ line size bits).

@@ ti-dram
**Answer: (c) step 3**

**Why.** When the row is activated, the tiny cell capacitor shares its charge with the large bit-line capacitance. The bit line moves only slightly above or below the precharge level, by an amount proportional to the cell's capacitance, so a smaller cell gives a weaker signal for the sense amplifier.

**Concept: charge sharing in DRAM.** ΔV ≈ (V_cell − V_pre) × C_cell/(C_cell + C_bitline). Because C_bitline is much bigger, ΔV is small (tens of mV), which is why sensitive sense amplifiers and periodic refresh are needed.

@@ ti-flash
**Answer: (a) it can erase data byte-wise** (does not describe flash)

**Why.** Flash erases whole blocks, never single bytes. NOR flash exists, so (c) does describe flash. (Flash also has limited write endurance, so (b) is doubtful too, but no option pairs (a) with (b).)

**Concept: NOR vs NAND flash.** NOR: random byte reads, can execute code in place, slower writes (used for firmware). NAND: denser and cheaper, read in pages (used in SSDs and memory cards).

@@ ti-memory-size
**Answer: (e) none** (it is 64 KB)

**Why.** 16 address lines select 2¹⁶ = 65,536 locations; 8 data lines mean each location is 1 byte. Size = 65,536 bytes = 64 KB.

**Concept: memory size from pins.** Size = 2^(address lines) × (data lines) bits.

@@ ti-prep-3
**Answer: (1) an array; (2) row-major; (3) Floyd's cycle-finding algorithm**

**Why.** (1) Array elements are contiguous, so each cache line brought in serves several elements (spatial locality); linked-list nodes are scattered. (2) C stores 2-D arrays row by row, so looping row-major walks memory sequentially. (3) Slow and fast pointers detect a loop in O(1) space.

**Concept: cache-friendly code.** Access memory sequentially and reuse data while it is in cache. Looping over a C matrix column by column jumps a whole row each step and can be many times slower.

@@ ti-sram-dram
**Answer: SRAM as cache combined with DRAM as main memory**

**Why.** DRAM is dense and cheap per bit (one transistor + one capacitor) but slower and needs refresh; SRAM is fast but uses six transistors per bit. Using a small SRAM cache in front of a large DRAM gives both speed and capacity.

**Concept: SRAM vs DRAM.** SRAM: flip-flop storage, fast, no refresh, expensive (caches, registers). DRAM: capacitor storage, dense, refresh needed (main memory).

@@ qc-iisc-bool
**Answer: (c) 1**

**Why.** Let X = AR. Then X + X′ = 1 (complement law), and 1 + SP = 1 (anything OR 1 is 1).

**Concept: spot the complement pair.** Treat a repeated sub-expression as a single variable; X + X′ = 1 and X·X′ = 0 collapse expressions instantly.

@@ qc-iisc-ttl
**Answer: (d) only (I)** (the intended answer)

**Why.** TTL is a logic family, a technology for building gates (strictly not a "type of gate", but that is the intended reading). (II) is plainly false: changing logic states is what digital circuits do.

**Concept: logic families.** TTL (bipolar transistors), CMOS (complementary MOSFETs, dominant today), ECL (very fast, power-hungry). They differ in speed, power, noise margin and fan-out.

@@ qc25-intersection
**Answer: (c) (II) and (IV)**

**Why.** For AND, 1 is the identity (P·1 = P) and 0 is the annihilator (P·0 = 0).

**Concept: identity and null laws.** AND: P·1 = P, P·0 = 0. OR: P + 0 = P, P + 1 = 1. These are the Boolean counterparts of multiplying by 1 and 0.

@@ qc25-lsi
**Answer: (a) more than 100**

**Why.** Integration scales: SSI (fewer than about 12 gates), MSI (12–99), LSI (100 to about 10,000), VLSI (more).

**Concept: integration levels** track how many gates fit on one chip; modern processors are far beyond VLSI, with billions of transistors.

@@ qc60-23
**Answer: (b) EXOR**

**Why.** XOR outputs 1 when exactly one input is 1 (the inputs differ) and 0 when both are 0 or both are 1.

**Concept: XOR uses.** Parity checking, adders (the sum bit is A ⊕ B ⊕ C_in), comparators (A ⊕ B = 0 means equal), and controlled inversion (A ⊕ 1 = A′).

@@ qc60-46
**Answer: (a) B′D + C′D**

**Why.** BC′D + C′D = C′D(B + 1) = C′D (absorption). So the expression becomes B′D + C′D.

**Concept: absorption law.** X + XY = X: if the bigger term is true, the smaller one adds nothing. Factor out common parts to see it.

@@ qcc-arch-10
**Answer: (c) B**

**Why.** AB + AB′ = A(B + B′) = A, and A′C + AC = C(A′ + A) = C. The expression is A + C, so B has no effect.

**Concept: combining adjacent terms.** XY + XY′ = X: two terms that differ in one variable merge (this is exactly what grouping in a K-map does).

@@ qcc-arch-11
**Answer: (d) P + Q**

**Why.** Idempotent law: X·X = X, with X = P + Q.

**Concept: idempotence.** X·X = X and X + X = X: repeating an input changes nothing.

@@ qcc-arch-12
**Answer: (b) R·(1 + P′)** (which equals R)

**Why.** (P′ + R)·R = P′R + R·R = P′R + R = R(P′ + 1) = R. Only option (b) equals R; it is the step just before simplifying 1 + P′ to 1.

**Concept: absorption in product form.** (X + Y)·Y = Y, the dual of X·Y + Y = Y.

@@ qcc-arch-13
**Answer: (c) HT**

**Why.** Absorption with X = HT: HT + HT·C = HT(1 + C) = HT.

**Concept: absorption law** X + XY = X.

@@ qcc-arch-14
**Answer: (b) only (I)**

**Why.** (I) regroups the operands, (X + Y) + Z = X + (Y + Z): associative. (II) swaps their order: commutative.

**Concept: associative vs commutative.** Associative: grouping doesn't matter. Commutative: order doesn't matter. Both hold for AND and OR (and XOR).

@@ qcc-arch-15
**Answer: (c) X + 1 = X** is incorrect

**Why.** X + 1 = 1 (dominance/null law): OR with 1 is always 1.

**Concept: null laws.** X + 1 = 1 and X·0 = 0.

@@ qcc-arch-16
**Answer: (b) NAND**

**Why.** NAND(A, 1) = (A·1)′ = A′. EXNOR with 1 gives A; NOR with 1 gives 0. (XOR with 1 would also invert, but it isn't offered.)

**Concept: universal gates.** NAND alone (or NOR alone) can build any logic function: NOT (tie inputs or set one to 1), AND (NAND + NOT), OR (NOTs on inputs, then NAND).

@@ qcc-arch-17
**Answer: (c) NAND**

**Why.** NAND outputs 0 only when every input is 1, and 1 otherwise.

**Concept: NAND truth table** = inverted AND.

@@ qcc-arch-18
**Answer: (a) EXNOR**

**Why.** The output is 1 exactly when the inputs are equal (00 or 11): XNOR, also called equivalence.

**Concept: XNOR = NOT XOR** = A·B + A′·B′. Used as a 1-bit equality comparator.

@@ qcc-arch-19
**Answer: (b) 8**

**Why.** Each input can be 0 or 1: 2 × 2 × 2 = 2³ = 8 combinations.

**Concept: truth table size.** n inputs → 2ⁿ rows.

@@ qcc-arch-20
**Answer: (c) only (III), a demultiplexer**

**Why.** One data input routed to one of several outputs by select lines is a demultiplexer. A multiplexer is the reverse (many inputs, one output); an encoder has many inputs and no select lines.

**Concept: MUX vs DEMUX vs decoder vs encoder.** MUX: select one of 2ⁿ inputs. DEMUX: send one input to one of 2ⁿ outputs. Decoder: n-bit code → one active output of 2ⁿ (a DEMUX with input fixed at 1). Encoder: the reverse.

@@ qcc-arch-21
**Answer: (b) an inverter**

**Why.** The difference bit of a full subtractor is the same 3-input XOR as the full adder's sum. The borrow is B_out = A′B + A′B_in + B·B_in, which is the adder's carry formula with A complemented. So one inverter on A (for the borrow path) converts it.

**Concept: subtraction via addition.** In two's complement, A − B = A + B′ + 1, so adders become subtractors with inverters on one input and carry-in = 1.

@@ qcc-dig-05
**Answer: (c) A + B′**

**Why.** Let X = A + B′. Then (X + C′)(X + C) = X + CC′ = X + 0 = X.

**Concept: distributive law (product of sums).** (X + Y)(X + Z) = X + YZ, the "OR distributes over AND" law that has no counterpart in ordinary arithmetic.

@@ qcc-dig-06
**Answer: (c) one OR gate**

**Why.** X + X′Y = (X + X′)(X + Y) = 1·(X + Y) = X + Y.

**Concept: redundancy law.** X + X′Y = X + Y: if X is false, X′ is true anyway, so the X′ factor adds nothing.

@@ qcc-dig-07
**Answer: (a) B**

**Why.** First term: (A + A′CD)B = AB + A′BCD. Second: D′ + C′D = D′ + C′, so it gives A′B(C′ + D′). Since C′ + D′ = (CD)′, F = AB + A′B[CD + (CD)′] = AB + A′B = B.

**Concept: spot a complementary pair inside.** CD and (CD)′ add to 1, which collapses the bracket; then AB + A′B = B.

@@ qcc-dig-08
**Answer: (d) (A + B + C′)(A′ + C′)(A + B)(B′ + C′)**

**Why.** De Morgan turns the complement of an OR of terms into the AND of each term's complement: (A′B′C)′ = A + B + C′, (AC)′ = A′ + C′, (A′B′)′ = A + B, (BC)′ = B′ + C′.

**Concept: De Morgan's laws.** (X + Y)′ = X′Y′ and (XY)′ = X′ + Y′. To complement any expression: swap AND/OR and complement every literal.

@@ qcc-dig-09
**Answer: no reliable pick** (no option equals the simplified expression AB + BC)

**Why.** A′(A + B) = A′B, so AB + A′B = B. Then B(A + B) = B and B(A + C) = AB + BC. The options expand to AC + BC, AB + AC + BC, C + AB′ and AB + AC; none is AB + BC. The question looks misprinted.

**Concept: check by expanding.** When options are given in complemented forms, expand each with De Morgan into sum-of-products and compare with your simplified answer.

@@ qcc-dig-10
**Answer: (d)**

**Why.** X's minterms (1, 2, 4, 7, 8, 11, 13, 14) are exactly the 4-bit numbers with an odd number of 1s, so X = A ⊕ B ⊕ C ⊕ D. For Y, group its zeros (maxterms 3, 5, 7, 8, 10, 11, 12, 13) on a K-map: 0-11 → (A + C′ + D′), -101 → (B′ + C + D′), 1-00 → (A′ + C + D), 101- → (A′ + B + C′). That is option (d).

**Concept: parity functions and POS from a K-map.** XOR of all inputs = 1 for an odd number of 1s (checkerboard K-map, cannot be simplified). For product-of-sums, group the 0s; each group gives a sum term with variables complemented where they are 1.

@@ qcc-dig-11
**Answer: (c) 16**

**Why.** 2⁴ = 16 input combinations, one row each.

**Concept: truth table size** = 2ⁿ for n inputs.

@@ qcc-dig-12
**Answer: no reliable pick** (the photo is blurred around G7; as read, every option gives F = 1; if G7 is a two-input gate, only A = B = C = 0 works, probably the intended answer)

**Why.** As read: F = XNOR(G7, C) with G7 = XNOR(G5, G6, C), so the C terms cancel and F = G5 ⊕ G6. With G5 = A + G4 and G6 = XNOR(A, G4): A = 0 gives F = G4 ⊕ G4′ = 1, and A = 1 gives F = G4′; for A = B = C = 1, G4 = 0, so F = 1 again.

**Concept: work backwards and simplify XOR chains.** XNOR(X, C) = X ⊕ C′; two appearances of the same signal in an XOR chain cancel (C ⊕ C = 0).

@@ qcc-dig-13
**Answer: (d) (AB)′**

**Why.** Z is pulled to ground only when both series transistors conduct (A = B = 1); otherwise the resistor pulls Z high. Output 0 only for A = B = 1: NAND.

**Concept: MOS logic structure.** Series pull-down transistors give NAND (all must be on); parallel pull-downs give NOR (any one is enough).

@@ qcc-dig-14
**Answer: (a) A + B**

**Why.** The first two NANDs have their inputs tied together, so they act as inverters: A′ and B′. The last NAND gives (A′B′)′ = A + B by De Morgan.

**Concept: OR from NANDs.** Invert the inputs, then NAND: (A′·B′)′ = A + B. Three NAND gates make an OR.

@@ qcc-dig-15
**Answer: (a) A + B**

**Why.** Y = [(A + B)′ · (BC)′]′ = (A + B) + BC (De Morgan) = A + B (absorption: B + BC = B).

**Concept: De Morgan then absorption.** Remove the outer bar first, then simplify.

@@ qcc-dig-16
**Answer: (b) Q = 0** (for every input, so (a) is false too)

**Why.** G1·G3 = (A ⊕ B)·AB = 0 always (if A and B differ, AB = 0), so the upper NAND is always 1. G3·G5 = AB·(A + B)′ = 0 always, so the lower NAND is always 1. Q = 1 ⊕ 1 = 0.

**Concept: look for terms that can never be true together.** A product of mutually exclusive conditions is identically 0, which fixes downstream gates regardless of inputs.

@@ qcc-dig-17
**Answer: (d) 111**

**Why.** The circuit computes Y = A′ + B′ + C′ = (ABC)′, which is 0 only when A = B = C = 1.

**Concept: OR of inverted inputs = NAND** (De Morgan).

@@ qcc-dig-18
**Answer: (c) four two-input NORs and one four-input NOR**

**Why.** Peel the bars from inside: (CD′)′ = C′ + D, so (B(C′ + D))′ = B′ + CD′, and Y = A′ + B(C′ + D) = (A′ + B)(A′ + C′ + D). A product of sums maps to NOR–NOR: Y = NOR(NOR(A′, B), NOR(A′, C′, D)). That needs two NORs as inverters (for A′ and C′), NOR(A′, B) and the output NOR (four two-input NORs), plus one four-input NOR (one input tied low) for the three-literal sum.

**Concept: NOR–NOR = product of sums.** A POS expression (X)(Y) = ((X)′ + (Y)′)′ becomes two levels of NOR gates, just as SOP becomes NAND–NAND.

@@ qcc-dig-19
**Answer: (b) 2:1 multiplexer**

**Why.** X enables the In1 buffer and X′ enables the In0 buffer, so exactly one input drives the shared output: Out = X·In1 + X′·In0.

**Concept: tri-state buffers.** Output is the input when enabled, and high-impedance (disconnected) when not. Several can share one wire as long as only one is enabled at a time: the basis of buses.

@@ qcc-dig-20
**Answer: (b) D₀ = 1, D₁ = 0, select = input**

**Why.** A 2:1 MUX gives Y = S′D₀ + SD₁ = S′·1 + S·0 = S′.

**Concept: MUX as a universal block.** A 2ⁿ:1 MUX can implement any function of n variables by putting the variables on the select lines and the truth-table outputs on the data inputs.

@@ qcc-dig-21
**Answer: (d) AB + A′B′**

**Why.** f = A′B′·I₀ + A′B·I₁ + AB′·I₂ + AB·I₃ = A′B′·1 + 0 + 0 + AB·1 = A′B′ + AB (XNOR).

**Concept: MUX output formula.** Each data input is ANDed with the minterm of its select code; the output ORs them all.

@@ qcc-dig-22
**Answer: (c) A + B + x and B ⊕ x**

**Why.** First: Y = A′B′x + A′B + AB′ + AB = A′B′x + (A + B) = A + B + x (redundancy law). Second: the inputs depend only on S₁ = B (x when B = 0, x′ when B = 1), so Y = B′x + Bx′ = B ⊕ x.

**Concept: MUX with a variable on the data inputs.** Putting a variable (or its complement) on data lines lets a 4:1 MUX implement functions of 3 variables.

@@ qcc-dig-23
**Answer: (b) A XOR B**

**Why.** The 74LS139's outputs are active-low: Y0 = m₀′, Y3 = m₃′. The input bubbles on the gate invert them back, the OR gives m₀ + m₃ = A′B′ + AB (XNOR), and the output bubble inverts that: Y = A ⊕ B.

**Concept: active-low signals.** A bubble means inversion. Matching bubbles cancel (a bubble output into a bubble input), which is how active-low decoders combine neatly with NAND gates.

@@ qcc-dig-24
**Answer: (d) 4**

**Why.** The two MSBs go to the 2:4 decoder, whose four outputs enable four 3:8 decoders, each driven by the three LSBs: 4 × 8 = 32 outputs.

**Concept: decoder trees.** Larger decoders are built hierarchically: the high bits choose which smaller decoder is enabled, the low bits choose the output within it.

@@ qcc-dig-25
**Answer: (a) 17**

**Why.** Equality: E = (A₂ ⊙ B₂)(A₁ ⊙ B₁)(A₀ ⊙ B₀). Each XNOR costs 5 NANDs (4 for an XOR + 1 to invert): 15. The 3-input AND = a 3-input NAND + an inverting NAND: 2. Total 17. (Counts vary slightly with the XOR form used; 17 is the standard textbook count.)

**Concept: equality comparators.** Two numbers are equal when every pair of bits is equal: AND of the bitwise XNORs.

@@ qcc-dig-26
**Answer: (b) 1K × 5**

**Why.** Address inputs: two 4-bit digits (8) + carry/borrow in (1) + the add/subtract control (1) = 10 bits → 2¹⁰ = 1K words. Outputs: the 4-bit result digit + carry/borrow out = 5 bits.

**Concept: ROM as a lookup table.** Any combinational function can be stored in a ROM: inputs become the address, outputs the stored word. Size = 2^(inputs) × (outputs).
