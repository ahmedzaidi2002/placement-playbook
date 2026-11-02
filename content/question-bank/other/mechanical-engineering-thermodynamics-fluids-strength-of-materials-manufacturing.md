---
title: "Mechanical engineering (thermodynamics, fluids, strength of materials, manufacturing)"
weight: 1
---

22 questions asked by Siemens Energy. Try each one first, then open the toggle: it gives the answer, why it is right, and the idea behind it explained from scratch.

### 1 · M22, radius of a beam in bending

*Asked by: Siemens Energy (MNNIT Allahabad (Mettl))*

A circular bar on a simple span carries a central load. Find its radius if the permissible
stress is 150 N/mm^2 and the maximum bending moment is 750 000 N mm.

- **(a)** 18 mm
- **(b)** 23 mm
- **(c)** 37 mm
- **(d)** 45 mm

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) 18 mm** (the diameter is 37 mm; the photo has 37 selected, which is the diameter, not the radius)

**Why.** For a solid circular section, bending stress σ = 32M/(πd³). So d = ∛(32 × 750,000/(150π)) = ∛50,930 ≈ 37.1 mm, and the radius is about 18.5 mm.

**Concept: bending stress.** σ = My/I. For a circle, I = πd⁴/64 and y = d/2, so σ = 32M/(πd³). The section modulus Z = I/y = πd³/32 measures bending strength.

{{< /details >}}

### 2 · M20, exponential failure

*Asked by: Siemens Energy (MNNIT Allahabad (Mettl))*

A bulb has a constant failure rate of 0.004 per hour. Find the probability of failure within
250 hours and the MTTF, assuming an exponential distribution.

- **(a)** Probability of failure = 0.8, MTTF = 250
- **(b)** Probability of failure = 0.7, MTTF = 500
- **(c)** Probability of failure = 0.6, MTTF = 250
- **(d)** Probability of failure = 0.5, MTTF = 500

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) probability 0.6, MTTF 250 hours**

**Why.** With a constant failure rate λ, the time to failure is exponential: P(fail by t) = 1 − e^(−λt) = 1 − e^(−0.004 × 250) = 1 − e⁻¹ ≈ 0.632, closest to 0.6. Mean time to failure = 1/λ = 250 hours.

**Concept: exponential reliability.** Reliability R(t) = e^(−λt). It is "memoryless": an old bulb is as good as a new one. At t = MTTF, about 63% have failed.

{{< /details >}}

### 3 · M9, statements about CNC machines

*Asked by: Siemens Energy (MNNIT Allahabad (Mettl))*

Which statements about CNC machines are correct? A. CNC stands for Computer Numerical
Control. B. A stepper motor is used as a drive unit. C. The accuracy of machinery is slightly
less than NC machines. D. A mini computer is used for the generation of the program in the
form of a file.

- **(a)** A & D only
- **(b)** A & C only
- **(c)** B & C only
- **(d)** C & D only

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) A & D only**

**Why.** A is true (Computer Numerical Control). D is true (a computer stores and generates the part program as a file). C is false: CNC machines are **more** accurate than NC. (B is true in practice, steppers or servos drive the axes, but no option contains B without C.)

**Concept: NC vs CNC.** NC machines read a punched tape program; CNC machines use an onboard computer that stores, edits and runs programs, with feedback for higher accuracy.

{{< /details >}}

### 4 · M15, gas from a cylinder feels cold

*Asked by: Siemens Energy (MNNIT Allahabad (Mettl))*

Why does the stream of gas coming out of a pressurised cylinder feel cold?

- **(a)** Because the moisture present in the cylinder condenses
- **(b)** Because work is being done at the expense of thermal energy
- **(c)** Because the gas in the cylinder is thermally insulated
- **(d)** Because the velocity of the gas is high

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) work is done at the expense of thermal energy**

**Why.** The escaping gas expands rapidly, pushing the surrounding air (doing work). The expansion is too fast for heat to flow in (adiabatic), so the energy comes from the gas's internal energy, and its temperature drops.

**Concept: adiabatic expansion.** First law: ΔU = Q − W. With Q ≈ 0, doing work (W > 0) lowers U, and for a gas lower internal energy means lower temperature. (The Joule–Thomson effect adds to the cooling for real gases.)

{{< /details >}}

### 5 · M27, connecting rod buckling

*Asked by: Siemens Energy (MNNIT Allahabad (Mettl))*

For a connecting rod to buckle equally about the X and Y axes (the Y-axis along the longer
length of the cross-section), what should the relation between the moments of inertia be?

- **(a)** Equal
- **(b)** $I_{xx} = 3 I_{yy}$
- **(c)** $I_{xx} = 4 I_{yy}$
- **(d)** $I_{xx} = 2 I_{yy}$

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) I_xx = 4 I_yy**

**Why.** About one axis the rod buckles as pin-ended (effective length L); about the other its ends act as fixed (effective length L/2). Euler's load P = π²EI/Lₑ². For equal loads, I/Lₑ² must match: I_xx/L² = I_yy/(L/2)², so I_xx = 4 I_yy.

**Concept: Euler buckling.** Critical load P = π²EI/Lₑ², with effective length Lₑ depending on end conditions (pinned-pinned L, fixed-fixed L/2, fixed-free 2L). Design for equal strength about both axes.

{{< /details >}}

### 6 · M13, heat removed per unit work

*Asked by: Siemens Energy (MNNIT Allahabad (Mettl))*

What is the ratio of useful heat removed to the work done in a refrigeration system called?

- **(a)** Coefficient of work
- **(b)** Coefficient of performance
- **(c)** Efficiency
- **(d)** Energy conversion ratio

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) coefficient of performance**

**Why.** For a refrigerator, COP = heat removed from the cold space / work input = Q_L/W. It is usually greater than 1.

**Concept: COP vs efficiency.** Efficiency (output ÷ input) of a heat engine is below 1. A refrigerator or heat pump moves heat rather than creating it, so it can move more heat than the work it uses: COP > 1 is normal.

{{< /details >}}

### 7 · M14, efficiency of a heat engine

*Asked by: Siemens Energy (MNNIT Allahabad (Mettl))*

A heat engine takes in 100 J and does 40 J of useful work; the remaining 60 J is lost. How
efficient is the engine?

- **(a)** 35%
- **(b)** 40%
- **(c)** 60%
- **(d)** 77%

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) 40%**

**Why.** Efficiency = useful work out / heat in = 40/100 = 40%.

**Concept: thermal efficiency.** η = W/Q_in = 1 − Q_out/Q_in. No engine can beat the Carnot limit 1 − T_cold/T_hot.

{{< /details >}}

### 8 · M19, gear speeds

*Asked by: Siemens Energy (MNNIT Allahabad (Mettl))*

A 20-tooth gear meshes with a 50-tooth gear. If the smaller gear turns at 1000 rpm, what is
the speed of the larger one?

- **(a)** 250 rpm
- **(b)** 400 rpm
- **(c)** 2000 rpm
- **(d)** 5000 rpm

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) 400 rpm**

**Why.** Meshing gears have the same tooth speed at the contact point: N₁T₁ = N₂T₂. N₂ = 1000 × 20/50 = 400 rpm.

**Concept: gear ratio.** Speed is inversely proportional to the number of teeth; torque is directly proportional. A small gear driving a big one slows down and increases torque.

{{< /details >}}

### 9 · M11, hardness test of mineralogists

*Asked by: Siemens Energy (MNNIT Allahabad (Mettl))*

Which hardness test is preferred by mineralogists to help identify minerals?

- **(a)** Brinell Hardness test
- **(b)** Vickers hardness test
- **(c)** Scratch hardness test
- **(d)** Rockwell hardness test

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) scratch hardness test**

**Why.** Mineralogists use the Mohs scale: which mineral can scratch which (talc 1 … diamond 10).

**Concept: hardness tests.** Scratch (Mohs) for minerals; indentation tests for metals: Brinell (steel ball, large indent), Vickers (diamond pyramid, any hardness), Rockwell (depth of indentation, quick).

{{< /details >}}

### 10 · M24, cost of heating a room

*Asked by: Siemens Energy (MNNIT Allahabad (Mettl))*

An insulated room $5 \times 8 \times 4$ m is heated from 10 °C to 30 °C by a 1 kW heater
with 80% efficiency; no air leaves. Electricity costs ₹10 per kWh. Find the cost
($c_v$ of air $= 0.75$ kJ/kg K, density 1.25 kg/m^3).

- **(a)** 8.34
- **(b)** 10.43
- **(c)** 10
- **(d)** 9.65

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) ₹10.43**

**Why.** Air mass = volume × density = (5 × 8 × 4) × 1.25 = 200 kg. Heat = m c_v ΔT = 200 × 0.75 × 20 = 3000 kJ = 0.833 kWh (1 kWh = 3600 kJ). With 80% efficiency, electricity used = 0.833/0.8 = 1.042 kWh, costing about ₹10.42.

**Concept: c_v for a closed room.** No air leaves, so the air is heated at constant volume and c_v applies (with leakage at constant pressure, c_p would). Account for heater efficiency by dividing.

{{< /details >}}

### 11 · M4, mechanical advantage 5

*Asked by: Siemens Energy (MNNIT Allahabad (Mettl))*

A machine is designed to lift a load of 500 N. If its mechanical advantage is 5, what force
must be applied?

{{< details title="Answer and explanation" closed="true" >}}

**Answer: 100 N**

**Why.** Mechanical advantage = load/effort, so effort = 500/5 = 100 N.

**Concept: mechanical advantage.** A machine multiplies force at the cost of distance: a smaller effort moves through a larger distance (ignoring friction).

{{< /details >}}

### 12 · M8, not a machining operation

*Asked by: Siemens Energy (MNNIT Allahabad (Mettl))*

Which one of the operations is not part of machining, where raw material is converted to
the final shape by removing material?

- **(a)** Turning
- **(b)** Milling
- **(c)** Drilling
- **(d)** Molding

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) molding**

**Why.** Turning, milling and drilling remove material with a cutting tool. Moulding shapes material by forcing it into a mould without removing any.

**Concept: manufacturing families.** Subtractive (machining), formative (casting, moulding, forging), additive (3D printing), joining (welding).

{{< /details >}}

### 13 · M30, heated tube length for mercury

*Asked by: Siemens Energy (MNNIT Allahabad (Mettl))*

Liquid mercury flows at 1.5 kg/s through a 30 mm tube, entering at 20 °C and leaving at
40 °C. The wall is held at 50 °C, $h = 4200$ W/m^2 °C and
$c_p = 140$ J/kg °C. What is the approximate tube length for constant heat flux?

- **(a)** 0.5 m
- **(b)** 0.8 m
- **(c)** 1 m
- **(d)** 1.3 m

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) 0.5 m**

**Why.** Heat needed: Q = ṁ c_p ΔT = 1.5 × 140 × 20 = 4200 W. With constant heat flux and the wall–fluid difference taken as 50 − 30 = 20 °C (mean bulk temperature 30 °C): Q = h (πdL) ΔT → L = 4200/(4200 × π × 0.03 × 20) ≈ 0.53 m.

**Concept: convective heat transfer.** Q = h A ΔT, where A = πdL for a tube. Energy balance on the fluid (ṁ c_p ΔT) gives Q; solve for the length.

{{< /details >}}

### 14 · M7, bottles and caps

*Asked by: Siemens Energy (MNNIT Allahabad (Mettl))*

For a project manufacturing cold-drink bottles, _____ is used for the bottles while
_____ is used for the caps.

- **(a)** Injection moulding; Rotational moulding
- **(b)** Blow moulding; Injection moulding
- **(c)** Compression moulding; Injection moulding
- **(d)** Rotational moulding; Compression moulding

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) blow moulding for bottles, injection moulding for caps**

**Why.** Hollow, thin-walled bottles are made by inflating a heated plastic tube inside a mould (blow moulding). Small precise parts with threads, like caps, are made by injecting molten plastic into a closed mould (injection moulding).

**Concept: plastic processes.** Injection (solid, precise parts), blow (hollow containers), rotational (large hollow items like tanks), compression (thermosets), extrusion (constant profiles like pipes).

{{< /details >}}

### 15 · M28, material removal rate in drilling

*Asked by: Siemens Energy (MNNIT Allahabad (Mettl))*

A 7 mm drill runs at 1000 rpm with a penetration rate of 1 mm/min. Calculate the material
removal rate.

- **(a)** $4.85 \times 10^{-5}$ m^3/min
- **(b)** $3.75 \times 10^{-5}$ m^3/min
- **(c)** $4.75 \times 10^{-5}$ m^3/min
- **(d)** $3.85 \times 10^{-5}$ m^3/min

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) by its digits** (MRR = 38.5 mm³/min = 3.85 × 10⁻⁸ m³/min; the options' exponent is off)

**Why.** Volume removed per minute = hole area × penetration rate = (π × 7²/4) × 1 = 38.5 mm³/min. The spindle speed isn't needed when the penetration (feed) rate per minute is given.

**Concept: material removal rate in drilling.** MRR = (πD²/4) × f × N, where f is feed per revolution and N is rpm; f × N is the penetration rate per minute.

{{< /details >}}

### 16 · M29, hollow pipe as a beam

*Asked by: Siemens Energy (MNNIT Allahabad (Mettl))*

A hollow steel pipe with moment of inertia 267 035 mm^4 is a simply
supported beam of span 1.5 m. With a permissible stress of 150 N/mm^2,
what concentrated load can it carry at mid-span?

- **(a)** 1.68 kN
- **(b)** 2.51 kN
- **(c)** 3.13 kN
- **(d)** 4.27 kN

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) 2.51 kN** (the ticked option; it can't be fully checked because the outer diameter is not given)

**Why.** For a central load on a simply supported span, M = WL/4. Bending: M = σI/y, with y the outer radius. So W = 4σI/(Ly). (b) corresponds to y ≈ 42.5 mm, i.e. an 85 mm outer diameter pipe.

**Concept: beam design.** Find the maximum bending moment from the loading, then use σ = My/I to find the load that keeps stress within the permitted value.

{{< /details >}}

### 17 · M3, pump versus compressor

*Asked by: Siemens Energy (MNNIT Allahabad (Mettl))*

What is the main difference between a pump and a compressor? (The option texts are cut off
on the right.)

{{< details title="Answer and explanation" closed="true" >}}

**Answer: a pump moves and pressurises a liquid; a compressor raises the pressure of a gas by reducing its volume**

**Why.** Liquids are nearly incompressible, so a pump mainly adds pressure and flow. Gases compress, so a compressor squeezes them into a smaller volume, raising pressure (and temperature).

**Concept: incompressible vs compressible flow.** That difference drives the different designs (and why compressors need cooling).

{{< /details >}}

### 18 · M1, Reynolds number

*Asked by: Siemens Energy (MNNIT Allahabad (Mettl))*

What is the Reynolds number, and what does it indicate about the flow of a fluid?

- **(a)** It is the ratio of inertial forces to viscous forces; it indicates whether the flow is laminar or turbulent.
- **(b)** It is the ratio of pressure forces to viscous forces; it indicates heat transfer in the fluid.
- **(c)** It is the ratio of gravitational forces to viscous forces; it indicates the density of the fluid.
- **(d)** It is the ratio of the velocity of sound to the flow velocity; it indicates the compressibility of the fluid.

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) inertial forces over viscous forces; indicates laminar or turbulent flow**

**Why.** Re = ρvL/μ. Low Re: viscosity dominates, smooth layered (laminar) flow. High Re: inertia dominates, chaotic (turbulent) flow. In pipes the transition is around Re ≈ 2300. (Option (d) describes the inverse of the Mach number.)

**Concept: dimensionless numbers.** They let you compare flows at different scales. Reynolds (inertia/viscosity), Mach (speed/sound speed), Prandtl (momentum/heat diffusion), Nusselt (convection/conduction).

{{< /details >}}

### 19 · M10, ore melted into two liquid layers

*Asked by: Siemens Energy (MNNIT Allahabad (Mettl))*

In which process are all components of an ore or concentrate completely melted and
separated into two liquid layers?

- **(a)** Roasting
- **(b)** Smelting
- **(c)** Leaching
- **(d)** Electrowinning

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) smelting**

**Why.** In smelting the charge is fully melted and separates into two liquid layers: the heavier metal (or matte) at the bottom and the lighter slag on top.

**Concept: extractive metallurgy.** Roasting (heat in air to convert ores, no melting), smelting (melt and separate), leaching (dissolve in a solution), electrowinning (deposit metal from solution by electrolysis).

{{< /details >}}

### 20 · M17, outflow from a 4 m tank

*Asked by: Siemens Energy (MNNIT Allahabad (Mettl))*

A tank of height 4 m is filled with a fluid of density 1000 kg/m^3. A hole
is opened at the bottom. What is the speed of the fluid leaving the tank?

- **(a)** 7.67 m/s
- **(b)** 8.86 m/s
- **(c)** 11.18 m/s
- **(d)** 14.14 m/s

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) 8.86 m/s**

**Why.** Torricelli's law: v = √(2gh) = √(2 × 9.81 × 4) = √78.5 ≈ 8.86 m/s. Density doesn't matter.

**Concept: Torricelli from Bernoulli.** Potential energy per unit mass at the top (gh) becomes kinetic energy at the hole (v²/2), the same as free fall from height h.

{{< /details >}}

### 21 · M18, torque on a 25 mm shaft

*Asked by: Siemens Energy (MNNIT Allahabad (Mettl))*

A shaft of diameter 25 mm is subjected to a torsional shear stress of 80 MPa. What is the
maximum torque it can withstand?

- **(a)** 24.55 N-m
- **(b)** 245.436 N-mm
- **(c)** 245.436 N-m
- **(d)** 24.55 N-mm

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) 245.436 N·m**

**Why.** For a solid shaft, τ = 16T/(πd³), so T = πd³τ/16 = π × 25³ × 80/16 ≈ 245,437 N·mm = 245.4 N·m. "245.436 N-mm" has the right digits but the wrong unit (off by 1000).

**Concept: torsion of shafts.** τ = Tr/J with polar moment J = πd⁴/32, giving τ = 16T/(πd³). Always track units (N·mm vs N·m).

{{< /details >}}

### 22 · M16, U-tube manometer

*Asked by: Siemens Energy (MNNIT Allahabad (Mettl))*

A U-tube partly filled with water is connected to a gas supply. The height difference
between the arms is 30 cm and the gas pressure in the tube is 10 kPa. What is the pressure
of the gas supply? ($g = 9.81$, water density 998 kg/m^3.)

- **(a)** 12.937 kPa
- **(b)** 120.8 kPa
- **(c)** 13.5 kPa
- **(d)** 10.5 kPa

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) 12.937 kPa**

**Why.** The supply pressure exceeds the tube pressure by the water column: ρgh = 998 × 9.81 × 0.30 ≈ 2937 Pa = 2.937 kPa. 10 + 2.937 = 12.937 kPa. (The question says "absolute", but the numbers only work as gauge readings; adding atmospheric pressure would give about 114 kPa, not an option.)

**Concept: manometers.** Pressure difference = ρ g h, where h is the height difference between the two liquid surfaces. Gauge pressure is relative to the atmosphere; absolute = gauge + atmospheric.

{{< /details >}}
