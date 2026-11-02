@@ mw-iisc-43
**Answer: (b) and (c)**

**Why.** MATLAB arrays start at index 1, so `x(0)` is an error: loop from 1 (b). Indexing uses parentheses, not square brackets: `x(k1) = ...` (c). Preallocation only improves speed, `pi` is built in, and a descending loop like 9:−2:5 is legal.

**Concept: MATLAB indexing.** 1-based, with parentheses: `A(i, j)`. Square brackets build arrays (`[1 2 3]`); curly braces index cell arrays (`C{2}`).

@@ mw-iisc-44
**Answer: (b) adding the folder to the operating system path**

**Why.** MATLAB looks for functions in the current folder and on its own search path, never on the OS `PATH`. Changing folder (a), adding to the MATLAB path (c) or calling by full path (d) all work.

**Concept: MATLAB search path.** Set with `addpath` / `savepath` or the "Set Path" dialog. The OS PATH is for finding executables, not MATLAB functions.

@@ mw-iisc-45
**Answer: (c) `[A; B]` and (e) `vertcat(A, B)`** (and (b) `{A, B}` if that is what the option shows: a 1 × 2 cell array)

**Why.** A is 3 × 3 and B is 4 × 3: they have the same number of columns, so they stack vertically into 7 × 3. Side by side (`[A, B]`, `horzcat`) needs equal row counts, so it fails.

**Concept: concatenation rules.** `;` (vertical) needs equal column counts; `,` or space (horizontal) needs equal row counts. Cell arrays `{}` can hold anything, of any size.

@@ mw-iisc-46
**Answer: (b) 6**

**Why.** A nested function shares the parent function's workspace, so `nestfun1` sets the same `x` to 5. Then `x = x + 1` gives 6.

**Concept: nested vs local functions.** A nested function (defined inside another's `function ... end`) can see and change the parent's variables. A local function (defined after it in the file) has its own separate workspace.

@@ mw-iisc-47
**Answer: (b) `A(3,:) = []` and (f) `A = A(1:2,:)`**

**Why.** Assigning `[]` to row 3 (all columns `:`) deletes it; keeping rows 1–2 does the same. (a) deletes column 3; `()` is not an empty matrix; there is no such `delete` function.

**Concept: deleting elements.** Assign the empty matrix: `A(i, :) = []` deletes row i, `A(:, j) = []` deletes column j.

@@ mw-iisc-48
**Answer: (c) only**

**Why.** Parentheses index a cell array and return cells: x1 and x2 are 1 × 1 cells (not double or string), x3 = A(3:5) is a 1 × 3 cell, and n = length(A) = 5. Braces `A{1}` would give the contents.

**Concept: () vs {} on cell arrays.** `C(i)` returns a smaller cell array (the box); `C{i}` returns what is inside the box.

@@ mw-iisc-49
**Answer: 4 times**

**Why.** A MATLAB `for` loop takes its values from the precomputed list 1:4. Assigning k = 5 changes k only for the rest of that iteration; the next iteration uses the next list value. So all four iterations print.

**Concept: for-loop variables in MATLAB.** Unlike C, changing the loop variable does not affect how many times the loop runs. Use a `while` loop if you need to change the counter.

@@ mw-iisc-50
**Answer: (c) 2 1 4 3**

**Why.** MATLAB resolves a name in this order: variables, explicitly imported names, nested functions, local functions, private functions, class methods and constructors, the current folder, then the rest of the path. So imported (2) → nested (1) → private (4) → current folder (3).

**Concept: name resolution.** When two things share a name, the earlier one in the precedence list wins. That is why a variable named `sum` hides the built-in `sum` function.

@@ sie-bar-radius
**Answer: (a) 18 mm** (the diameter is 37 mm; the photo has 37 selected, which is the diameter, not the radius)

**Why.** For a solid circular section, bending stress σ = 32M/(πd³). So d = ∛(32 × 750,000/(150π)) = ∛50,930 ≈ 37.1 mm, and the radius is about 18.5 mm.

**Concept: bending stress.** σ = My/I. For a circle, I = πd⁴/64 and y = d/2, so σ = 32M/(πd³). The section modulus Z = I/y = πd³/32 measures bending strength.

@@ sie-bulb
**Answer: (c) probability 0.6, MTTF 250 hours**

**Why.** With a constant failure rate λ, the time to failure is exponential: P(fail by t) = 1 − e^(−λt) = 1 − e^(−0.004 × 250) = 1 − e⁻¹ ≈ 0.632, closest to 0.6. Mean time to failure = 1/λ = 250 hours.

**Concept: exponential reliability.** Reliability R(t) = e^(−λt). It is "memoryless": an old bulb is as good as a new one. At t = MTTF, about 63% have failed.

@@ sie-cnc
**Answer: (a) A & D only**

**Why.** A is true (Computer Numerical Control). D is true (a computer stores and generates the part program as a file). C is false: CNC machines are **more** accurate than NC. (B is true in practice, steppers or servos drive the axes, but no option contains B without C.)

**Concept: NC vs CNC.** NC machines read a punched tape program; CNC machines use an onboard computer that stores, edits and runs programs, with feedback for higher accuracy.

@@ sie-cold-gas
**Answer: (b) work is done at the expense of thermal energy**

**Why.** The escaping gas expands rapidly, pushing the surrounding air (doing work). The expansion is too fast for heat to flow in (adiabatic), so the energy comes from the gas's internal energy, and its temperature drops.

**Concept: adiabatic expansion.** First law: ΔU = Q − W. With Q ≈ 0, doing work (W > 0) lowers U, and for a gas lower internal energy means lower temperature. (The Joule–Thomson effect adds to the cooling for real gases.)

@@ sie-connecting-rod
**Answer: (c) I_xx = 4 I_yy**

**Why.** About one axis the rod buckles as pin-ended (effective length L); about the other its ends act as fixed (effective length L/2). Euler's load P = π²EI/Lₑ². For equal loads, I/Lₑ² must match: I_xx/L² = I_yy/(L/2)², so I_xx = 4 I_yy.

**Concept: Euler buckling.** Critical load P = π²EI/Lₑ², with effective length Lₑ depending on end conditions (pinned-pinned L, fixed-fixed L/2, fixed-free 2L). Design for equal strength about both axes.

@@ sie-cop
**Answer: (b) coefficient of performance**

**Why.** For a refrigerator, COP = heat removed from the cold space / work input = Q_L/W. It is usually greater than 1.

**Concept: COP vs efficiency.** Efficiency (output ÷ input) of a heat engine is below 1. A refrigerator or heat pump moves heat rather than creating it, so it can move more heat than the work it uses: COP > 1 is normal.

@@ sie-engine
**Answer: (b) 40%**

**Why.** Efficiency = useful work out / heat in = 40/100 = 40%.

**Concept: thermal efficiency.** η = W/Q_in = 1 − Q_out/Q_in. No engine can beat the Carnot limit 1 − T_cold/T_hot.

@@ sie-gears
**Answer: (b) 400 rpm**

**Why.** Meshing gears have the same tooth speed at the contact point: N₁T₁ = N₂T₂. N₂ = 1000 × 20/50 = 400 rpm.

**Concept: gear ratio.** Speed is inversely proportional to the number of teeth; torque is directly proportional. A small gear driving a big one slows down and increases torque.

@@ sie-hardness
**Answer: (c) scratch hardness test**

**Why.** Mineralogists use the Mohs scale: which mineral can scratch which (talc 1 … diamond 10).

**Concept: hardness tests.** Scratch (Mohs) for minerals; indentation tests for metals: Brinell (steel ball, large indent), Vickers (diamond pyramid, any hardness), Rockwell (depth of indentation, quick).

@@ sie-heater
**Answer: (b) ₹10.43**

**Why.** Air mass = volume × density = (5 × 8 × 4) × 1.25 = 200 kg. Heat = m c_v ΔT = 200 × 0.75 × 20 = 3000 kJ = 0.833 kWh (1 kWh = 3600 kJ). With 80% efficiency, electricity used = 0.833/0.8 = 1.042 kWh, costing about ₹10.42.

**Concept: c_v for a closed room.** No air leaves, so the air is heated at constant volume and c_v applies (with leakage at constant pressure, c_p would). Account for heater efficiency by dividing.

@@ sie-lever
**Answer: 100 N**

**Why.** Mechanical advantage = load/effort, so effort = 500/5 = 100 N.

**Concept: mechanical advantage.** A machine multiplies force at the cost of distance: a smaller effort moves through a larger distance (ignoring friction).

@@ sie-machining
**Answer: (d) molding**

**Why.** Turning, milling and drilling remove material with a cutting tool. Moulding shapes material by forcing it into a mould without removing any.

**Concept: manufacturing families.** Subtractive (machining), formative (casting, moulding, forging), additive (3D printing), joining (welding).

@@ sie-mercury
**Answer: (a) 0.5 m**

**Why.** Heat needed: Q = ṁ c_p ΔT = 1.5 × 140 × 20 = 4200 W. With constant heat flux and the wall–fluid difference taken as 50 − 30 = 20 °C (mean bulk temperature 30 °C): Q = h (πdL) ΔT → L = 4200/(4200 × π × 0.03 × 20) ≈ 0.53 m.

**Concept: convective heat transfer.** Q = h A ΔT, where A = πdL for a tube. Energy balance on the fluid (ṁ c_p ΔT) gives Q; solve for the length.

@@ sie-moulding
**Answer: (b) blow moulding for bottles, injection moulding for caps**

**Why.** Hollow, thin-walled bottles are made by inflating a heated plastic tube inside a mould (blow moulding). Small precise parts with threads, like caps, are made by injecting molten plastic into a closed mould (injection moulding).

**Concept: plastic processes.** Injection (solid, precise parts), blow (hollow containers), rotational (large hollow items like tanks), compression (thermosets), extrusion (constant profiles like pipes).

@@ sie-mrr
**Answer: (d) by its digits** (MRR = 38.5 mm³/min = 3.85 × 10⁻⁸ m³/min; the options' exponent is off)

**Why.** Volume removed per minute = hole area × penetration rate = (π × 7²/4) × 1 = 38.5 mm³/min. The spindle speed isn't needed when the penetration (feed) rate per minute is given.

**Concept: material removal rate in drilling.** MRR = (πD²/4) × f × N, where f is feed per revolution and N is rpm; f × N is the penetration rate per minute.

@@ sie-pipe
**Answer: (b) 2.51 kN** (the ticked option; it can't be fully checked because the outer diameter is not given)

**Why.** For a central load on a simply supported span, M = WL/4. Bending: M = σI/y, with y the outer radius. So W = 4σI/(Ly). (b) corresponds to y ≈ 42.5 mm, i.e. an 85 mm outer diameter pipe.

**Concept: beam design.** Find the maximum bending moment from the loading, then use σ = My/I to find the load that keeps stress within the permitted value.

@@ sie-pump
**Answer: a pump moves and pressurises a liquid; a compressor raises the pressure of a gas by reducing its volume**

**Why.** Liquids are nearly incompressible, so a pump mainly adds pressure and flow. Gases compress, so a compressor squeezes them into a smaller volume, raising pressure (and temperature).

**Concept: incompressible vs compressible flow.** That difference drives the different designs (and why compressors need cooling).

@@ sie-reynolds
**Answer: (a) inertial forces over viscous forces; indicates laminar or turbulent flow**

**Why.** Re = ρvL/μ. Low Re: viscosity dominates, smooth layered (laminar) flow. High Re: inertia dominates, chaotic (turbulent) flow. In pipes the transition is around Re ≈ 2300. (Option (d) describes the inverse of the Mach number.)

**Concept: dimensionless numbers.** They let you compare flows at different scales. Reynolds (inertia/viscosity), Mach (speed/sound speed), Prandtl (momentum/heat diffusion), Nusselt (convection/conduction).

@@ sie-smelting
**Answer: (b) smelting**

**Why.** In smelting the charge is fully melted and separates into two liquid layers: the heavier metal (or matte) at the bottom and the lighter slag on top.

**Concept: extractive metallurgy.** Roasting (heat in air to convert ores, no melting), smelting (melt and separate), leaching (dissolve in a solution), electrowinning (deposit metal from solution by electrolysis).

@@ sie-tank
**Answer: (b) 8.86 m/s**

**Why.** Torricelli's law: v = √(2gh) = √(2 × 9.81 × 4) = √78.5 ≈ 8.86 m/s. Density doesn't matter.

**Concept: Torricelli from Bernoulli.** Potential energy per unit mass at the top (gh) becomes kinetic energy at the hole (v²/2), the same as free fall from height h.

@@ sie-torque
**Answer: (c) 245.436 N·m**

**Why.** For a solid shaft, τ = 16T/(πd³), so T = πd³τ/16 = π × 25³ × 80/16 ≈ 245,437 N·mm = 245.4 N·m. "245.436 N-mm" has the right digits but the wrong unit (off by 1000).

**Concept: torsion of shafts.** τ = Tr/J with polar moment J = πd⁴/32, giving τ = 16T/(πd³). Always track units (N·mm vs N·m).

@@ sie-u-tube
**Answer: (a) 12.937 kPa**

**Why.** The supply pressure exceeds the tube pressure by the water column: ρgh = 998 × 9.81 × 0.30 ≈ 2937 Pa = 2.937 kPa. 10 + 2.937 = 12.937 kPa. (The question says "absolute", but the numbers only work as gauge readings; adding atmospheric pressure would give about 114 kPa, not an option.)

**Concept: manometers.** Pressure difference = ρ g h, where h is the height difference between the two liquid surfaces. Gauge pressure is relative to the atmosphere; absolute = gauge + atmospheric.
