@@ ion-q1
**Answer: none of the options; the 4th term is 43.** (Option (a), 7, is the 3rd term, probably what the setter meant if they counted from a₀.)

**Why.** a₁ = 2; a₂ = 4 − 2 + 1 = 3; a₃ = 9 − 3 + 1 = 7; a₄ = 49 − 7 + 1 = 43.

**Concept: recursive sequences.** A recurrence defines each term from the previous one. Compute term by term and keep careful count of the index. (This is Sylvester's sequence 2, 3, 7, 43, 1807, ..., where each term is one more than the product of all earlier terms.)

@@ ion-q7
**Answer: (c) 0.954**

**Why.** 27 = 3³, so log 27 = 3 log 3 → log 3 = 1.431/3 = 0.477. 9 = 3², so log 9 = 2 × 0.477 = 0.954.

**Concept: log of a power.** log(aⁿ) = n log a. Write both numbers as powers of the same base (here 3) and the logs become multiples of one value.

@@ ion-q9
**Answer: (a) 7**

**Why.** |x − 2| ≤ 3 means −3 ≤ x − 2 ≤ 3, i.e. −1 ≤ x ≤ 5. The integers are −1, 0, 1, 2, 3, 4, 5: seven of them.

**Concept: absolute-value inequalities.** |x − a| ≤ r means x is within distance r of a: a − r ≤ x ≤ a + r. Count integers in [p, q] as q − p + 1.

@@ mw-iitb-2
**Answer: (d) 7/5**

**Why.** 1 + 2/7 + (2/7)² + ... = 1/(1 − 2/7) = 1/(5/7) = 7/5.

**Concept: infinite geometric series.** a + ar + ar² + ... = a/(1 − r) when |r| < 1. Here a = 1 (the i = 0 term) and r = 2/7.

@@ sig-sets
**Answer: (b) {8, 26, 36, 79}**

**Why.** A − B keeps the elements of A that are not in B. 15, 78, 90 and 29 are in both, so they go; 8, 26, 36, 79 remain.

**Concept: set difference.** A − B = {x : x ∈ A and x ∉ B}. It is not symmetric: B − A would be {98, 67, 75, 34}, option (c), a trap.

@@ mw-iisc-15
**Answer: (a) definite** (an improper definite integral)

**Why.** It has limits (−∞ and +∞), so when it converges it gives a number. An indefinite integral has no limits and gives a family of functions (+ C).

**Concept: improper integrals.** An integral with an infinite limit is defined as a limit of ordinary definite integrals: ∫ from −∞ to ∞ = lim of ∫ from −a to b as a, b → ∞. It is still "definite" in kind.

@@ mw-iisc-17
**Answer: (d) Ce⁻²ᵗ + 3**

**Why.** Homogeneous part: dx/dt + 2x = 0 gives x = Ce⁻²ᵗ. Particular solution: try a constant x = k, then 0 + 2k = 6, k = 3. General solution = Ce⁻²ᵗ + 3.

**Concept: first-order linear ODEs.** Solution = (solution of the equation with right side 0) + (any one particular solution). For a constant right side, try a constant. Check: as t → ∞, x → 3, the steady state where dx/dt = 0.

@@ ti-ode
**Answer: x(∞) = 2.4**

**Why.** As t → ∞, the input 12(1 − e⁻²ᵗ) → 12, and the system settles (both roots of s² + 6s + 5 = 0 are negative: −1, −5), so x' and x'' → 0. Then 5x(∞) = 12, x(∞) = 2.4.

**Concept: steady state.** If a linear system is stable (all characteristic roots have negative real part), its output settles to a constant for a constant input. At steady state all derivatives are zero, so just solve the algebraic equation that remains (final value theorem).

@@ ti-rms
**Answer: y_avg = k x_avg and y_rms = |k| x_rms**

**Why.** Average is linear: mean of kx = k × mean of x. RMS = √(mean of x²); for y = kx, mean of y² = k² × mean of x², so y_rms = |k| x_rms.

**Concept: average and RMS.** The average is a plain mean; the RMS (root mean square) squares values first, so it measures size regardless of sign. Scaling a signal by k scales both by k (the RMS by |k|, since it is never negative).

@@ mw-iiitd-1
**Answer: (b) nk/2**

**Why.** Each of the n vertices has degree k, so the degrees add to nk. Every edge has two ends and is counted twice in that sum, so edges = nk/2.

**Concept: handshake lemma.** Sum of all degrees = 2 × number of edges. (So in any graph, the number of odd-degree vertices is even.)

@@ mw-iiitd-6
**Answer: (d) 15**

**Why.** 2⁴ = 16 ≡ −1 (mod 17), so 2⁸ ≡ 1. 2021 = 8 × 252 + 5, so 2²⁰²¹ ≡ 2⁵ = 32 ≡ 15 (mod 17).

**Concept: modular exponent cycles.** Find a small power that is ≡ 1 (or −1); then powers repeat with that period, and you only need the exponent's remainder.

@@ mw-iisc-20
**Answer: (a) 1**

**Why.** 101 is prime and does not divide 2, so by Fermat's little theorem 2¹⁰⁰ ≡ 1 (mod 101).

**Concept: Fermat's little theorem.** If p is prime and p does not divide a, then a^(p−1) ≡ 1 (mod p). It turns huge powers into easy remainders.

@@ mw-iitb-11
**Answer: (b) x ≡ (c/g)(a/g)⁻¹ (mod b/g)**

**Why.** Divide ax + by = c by g: (a/g)x + (b/g)y = c/g. Taken modulo b/g, the y term disappears: (a/g)x ≡ c/g. Since a/g and b/g share no factors, a/g has an inverse modulo b/g, so x ≡ (c/g)(a/g)⁻¹.

**Concept: linear Diophantine equations.** ax + by = c has integer solutions exactly when gcd(a, b) divides c. The x-values repeat every b/g. The modular inverse a⁻¹ (mod m) exists when gcd(a, m) = 1, and is found by the extended Euclidean algorithm.

@@ mw-iitb-6
**Answer: (b) 7** (as the repeated digit sum; the plain digit sum is 115, not an option)

**Why.** The digit sum is congruent to the number mod 9. 2⁶ = 64 ≡ 1 (mod 9), and 100 = 6 × 16 + 4, so 2¹⁰⁰ ≡ 2⁴ = 16 ≡ 7 (mod 9). The repeated digit sum (digital root) is 7. Check: the actual digit sum is 115, and 1 + 1 + 5 = 7.

**Concept: digital root = value mod 9.** Adding a number's digits repeatedly until one digit remains gives n mod 9 (with 9 instead of 0). Useful for checking big arithmetic.

@@ mw-nitdl-1
**Answer: (d) symmetry**

**Why.** A partial order (like ≤ or "divides") is reflexive (a ≤ a), antisymmetric (a ≤ b and b ≤ a means a = b) and transitive. Symmetry (a ≤ b implies b ≤ a) would make it an equivalence relation instead. The candidate's "anti-symmetry" is wrong.

**Concept: relation properties.**
- Equivalence relation: reflexive, symmetric, transitive (e.g. "same remainder mod 5").
- Partial order: reflexive, antisymmetric, transitive (e.g. ⊆, ≤, divides).

@@ mw25-recurrence
**Answer: (a) 2ⁿ⁺¹ − n − 2**

**Why.** Check T(1) = 4 − 1 − 2 = 1 ✓. Check the recurrence: 2T(n − 1) + n = 2(2ⁿ − (n − 1) − 2) + n = 2ⁿ⁺¹ − 2n − 2 + n = 2ⁿ⁺¹ − n − 2 ✓. Neat derivation: set U(n) = T(n) + n + 2; then U(n) = 2U(n − 1), so U doubles each step from U(1) = 4, giving U(n) = 2ⁿ⁺¹.

**Concept: verify by substitution.** For MCQs on recurrences, plug each option into the base case and the recurrence; the one that satisfies both is the answer. To solve T(n) = 2T(n − 1) + n, absorb the extra term with a shift (T + n + 2) that turns it into pure doubling.

@@ qc-iisc-bond
**Answer: (a) 2**

**Why.** Removing a cut disconnects G. If removing a bond F left three or more components, the edges of F between just two of those components would already disconnect G, a smaller cut, contradicting that F is minimal. So exactly 2 components.

**Concept: cuts and bonds.** An edge cut is a set of edges whose removal disconnects the graph. A bond is a minimal one: removing any edge from it makes it no longer a cut. Bonds always split a connected graph into exactly two pieces.

@@ ti-branches
**Answer: (b) 13**

**Why.** For a connected network, independent loops = branches − nodes + 1. So branches = loops + nodes − 1 = 4 + 10 − 1 = 13.

**Concept: graph theory for circuits.** A spanning tree of n nodes has n − 1 branches. Each extra branch closes one independent loop. So loops = b − (n − 1). This counts the independent mesh equations in circuit analysis.

@@ mw-iisc-16
**Answer: (b) ±(3i − 2j + k)/√14**

**Why.** A vector perpendicular to both a and b is their cross product: a × b = (2·2 − 1·1)i − (1·2 − 1·0)j + (1·1 − 2·0)k = 3i − 2j + k. Its length is √(9 + 4 + 1) = √14; divide to get a unit vector, with ± for both directions.

**Concept: cross product.** a × b is perpendicular to both a and b. Unit vector = vector ÷ its length. Quick check: (3, −2, 1)·(1, 2, 1) = 3 − 4 + 1 = 0 ✓.

@@ ie-q1
**Answer: (b) discrete random variable** (the photo ticks (a))

**Why.** A discrete random variable takes a finite or countable list of values (like 0, 1, 2, ...). A continuous one takes any value in an interval (uncountably many).

**Concept: discrete vs continuous.** Discrete: counts (number of heads), described by a probability mass function. Continuous: measurements (height), described by a density, where any single exact value has probability 0.

@@ ie-q3
**Answer: (c) null hypothesis**

**Why.** The null hypothesis H₀ is the default claim (no effect, no difference) that we assume true and try to reject with data.

**Concept: hypothesis testing.** Assume H₀, compute how surprising the data would be (the p-value). If it is very surprising, reject H₀ in favour of the alternative H₁. Failing to reject is not proving H₀.

@@ ie-q4
**Answer: (b) Gaussian**

**Why.** The sum of independent normal variables is normal, with mean μ_X + μ_Y and variance σ²_X + σ²_Y.

**Concept: normal distributions are closed under addition.** Means add, and for independent variables variances add (standard deviations do not).

@@ ie-q5
**Answer: (d) 2**

**Why.** A fair die gives an expected 300/6 = 50 per face. χ² = Σ (O − E)²/E = (16 + 16 + 16 + 16 + 0 + 36)/50 = 100/50 = 2.

**Concept: chi-square goodness of fit.** It measures how far observed counts are from expected ones, scaled by the expected count. Small values mean the data fit; compare with a χ² table (here 5 degrees of freedom) to decide.

@@ ie-q6
**Answer: (b) p < 0.05**

**Why.** By convention a result is called significant if p < 0.05, i.e. data this extreme would happen less than 5% of the time if H₀ were true.

**Concept: p-value.** The probability, assuming H₀, of getting data at least as extreme as observed. Smaller p = stronger evidence against H₀. The 5% threshold is a convention, not a law.

@@ ie-q7
**Answer: (a) mean < median < mode**

**Why.** A left-skewed distribution has a long tail of small values. Those few extreme low values pull the mean down most; the median is less affected; the mode sits at the peak, on the right.

**Concept: skewness.** The mean follows the tail. Right (positive) skew: mode < median < mean. Left (negative) skew: mean < median < mode.

@@ ie-q8
**Answer: (e) all unchanged**

**Why.** Pearson correlation uses each variable's deviations from its own mean. Adding or subtracting a constant shifts every value and its mean equally, so the deviations, and the correlation, stay the same.

**Concept: correlation is shift- and scale-invariant.** r(aX + b, cY + d) = r(X, Y) when a and c are both positive (the sign flips if one is negative). It measures linear association, not location or units.

@@ or-java-reverse
**Answer: (d) it reverses the contents of the array** (between low and high)

**Why.** It swaps data[low] and data[high], then recurses on the inner part (low + 1, high − 1), stopping when the pointers meet or cross. That is exactly reversal.

**Concept: two-pointer reversal.** Swap the outermost pair and move both ends inward. Recursion depth is n/2; an iterative loop does the same with O(1) extra space.

@@ sig-bubble
**Answer: (a) 9 10 11 22 45**

**Why.** Bubble sort orders the array ascending. Java passes the array's reference by value, so the method sorts the same array the caller holds, and printing it shows the sorted order.

**Concept: Java passes references by value.** For an array or object, the method gets a copy of the reference, pointing to the same object; changing its contents is visible to the caller. Reassigning the parameter to a new array would not be.

@@ sig-java-sqrt
**Answer: (c) 4** (printed as 4.0)

**Why.** The loop is Newton's method for √16: result = (temp + 16/temp)/2. From 8: 5, 4.1, 4.001..., converging to 4.0, where two successive values are equal and the loop stops.

**Concept: Newton's method for square roots.** To find √N, repeat x ← (x + N/x)/2. If x is too big, N/x is too small, and their average is closer. It converges very fast (the number of correct digits roughly doubles each step).

@@ qc-n-initblocks
**Answer: (c) both** (Java)

**Why.** A static initialisation block runs once, when the class is loaded. An instance initialisation block runs every time an object is created, before the constructor body.

**Concept: Java initialisation order.** On class load: static fields and static blocks, in order. On each `new`: superclass constructor, then instance fields and instance blocks, then the rest of the constructor.

@@ qc-n-override
**Answer: (c) only (I)**

**Why.** (I) True: a method a subclass cannot inherit (e.g. private) cannot be overridden. (II) False: a static method cannot be overridden, but a subclass **can** re-declare it (method hiding). (III) False: instance methods are exactly the ones that get overridden.

**Concept: overriding vs hiding.** Overriding replaces an inherited instance method and is chosen at run time by the object's type. A static method with the same signature in a subclass hides the parent's, and the call is chosen at compile time by the reference type.

@@ wbd-20
**Answer: (a) Person created, Superhero created, Batman created**

**Why.** Every constructor first calls its superclass constructor (an implicit `super()`), so construction runs from the top of the hierarchy down: Person, then Superhero, then Batman.

**Concept: constructor chaining.** A subclass object contains its superclass part, which must be built first. If you don't write `super(...)`, Java inserts `super()` as the first statement.

@@ wbd-26
**Answer: (c) compiler error**

**Why.** Two separate errors: `Batman.greet()` tries to override a `final` method, which is not allowed; and `Superhero` has no `show()` method, so `myHero.show()` cannot compile.

**Concept: `final` and static typing.** A `final` method cannot be overridden. The compiler checks method calls against the reference's declared type (Superhero), not the object's run-time type.

@@ ie-q40
**Answer: (b) keys can be accessed via values** (false)

**Why.** A dictionary maps keys to values; lookup goes key → value only. To find a key from a value you must search all entries.

**Concept: Python dict.** A hash table: average O(1) lookup by key. Keys must be hashable (immutable); values can be anything. Since Python 3.7, dicts keep insertion order, though not sorted order.

@@ mw-iitb-40
**Answer: `dlrowolleh`**

**Why.** `s[::-1]` takes the whole string with step −1, i.e. backwards.

**Concept: slicing `s[start:stop:step]`.** Omitted start/stop mean "from the beginning/end in the step's direction". A negative step walks backwards, so `[::-1]` reverses any sequence.

@@ fj-kgp-pc4
**Answer: (c) the GIL ensures only one thread executes Python bytecode at a time**

**Why.** In CPython, the Global Interpreter Lock lets only one thread run Python code at once. CPU-bound threads therefore do not run in parallel (use processes); I/O-bound threads still help, because the GIL is released while waiting.

**Concept: the GIL.** It exists to keep CPython's reference counting thread-safe. It is a lock, not a memory manager or an exception tool. For parallel computation use `multiprocessing` or libraries (NumPy) that release the GIL.

@@ ie-q37
**Answer: (d) all of the above**

**Why.** Python supports classes and objects (OOP), plain functions and control structures (structured), and first-class functions, lambdas, map/filter (functional).

**Concept: multi-paradigm languages.** A paradigm is a style of organising code; many modern languages let you mix them.

@@ mw-iitb-41
**Answer: the script's name**

**Why.** `sys.argv` holds the command-line words: `argv[0]` is the program (script) name, and the user's arguments start at `argv[1]`.

**Concept: command-line arguments.** Same convention as C's `argv`. `len(sys.argv) − 1` is the number of user arguments.

@@ fj-kgp-pc5
**Answer: (b) [2, 4, 6, 8]**

**Why.** `map(func, list)` applies `func` to each element: 1×2, 2×2, 3×2, 4×2. `list(...)` turns the lazy map object into a list.

**Concept: `map`.** `map(f, xs)` = [f(x) for x in xs], computed lazily in Python 3.

@@ mw-iitb-42
**Answer: `[]`**

**Why.** `range(5, -5, -2)` gives 5, 3, 1, −1, −3, all odd. The filter keeps only even numbers, so nothing passes, and mapping over nothing gives an empty list.

**Concept: `range(start, stop, step)`.** Stops before `stop`. Starting from an odd number with step −2 gives only odd numbers.

@@ mw-iitb-43
**Answer: (c) [0, None, 1, None, 2, None]**

**Why.** The default `x=[]` is created once and shared by every call. In each call, `x.append(i)` adds i and returns `None`; the outer `x.append(...)` then adds that `None`. After three calls: 0, None, 1, None, 2, None.

**Concept: mutable default arguments.** Default values are evaluated once, when the function is defined. A mutable default (list, dict) keeps changes between calls. Use `x=None` and create the list inside instead. Also, `list.append` returns `None`.

@@ mw-iitb-44
**Answer: the values 1, 2, 3** (a lazy `map` object in Python 3; `list(...)` gives [1, 2, 3])

**Why.** `incr` adds 1 to each element.

**Concept: lazy iterators in Python 3.** `map`, `filter` and `zip` return iterators that compute on demand; printing them shows an object, not the values.

@@ exl-pandas
**Answer: option (1): 2023-02-28 → 87.75, 2023-03-31 → 55.00**

**Why.**
1. `freq='W'` makes weekly bins ending on Sundays: up to Feb 5 (values 1–5, sum 15), Feb 12 (63), Feb 19 (112), Feb 26 (161), and Mar 5 (Feb 27–28, sum 55). Each week is labelled by its end date.
2. `.resample('M').mean()` groups those weekly sums by month end: February has 15, 63, 112, 161 → mean 87.75; March has 55.

**Concept: grouping by time.** `pd.Grouper(freq='W')` bins dates into weeks (ending Sunday by default) and labels each bin by its end. `resample('M')` (written `'ME'` in new pandas) then regroups by calendar month. Watch which label each bin gets.

@@ ie-q31
**Answer: (a) from the beginning up to index 3**

**Why.** `[:4]` takes indices 0, 1, 2, 3; the stop index is excluded.

**Concept: half-open slices.** `a[start:stop]` includes start and excludes stop, so it has stop − start elements.

@@ ie-q32
**Answer: (b) `reshape()`**

**Why.** `a.reshape(r, c)` returns the same data viewed with a new shape (the total size must match).

**Concept: reshape.** Data stays in the same order in memory; only the way it is split into dimensions changes.

@@ ie-q33
**Answer: (a) `describe()`**

**Why.** `df['col'].describe()` gives count, mean, standard deviation, min, quartiles and max.

**Concept: quick data summaries.** `describe()` for numbers, `value_counts()` for categories, `info()` for types and missing values.

@@ ie-q35
**Answer: (d) all of the above**

**Why.** `pd.DataFrame(list)`, `pd.DataFrame(dict)` and `pd.read_csv(file)` all produce DataFrames.

**Concept: DataFrame sources.** A DataFrame is a table of labelled columns; it can be built from lists, dicts of columns, NumPy arrays, CSV/Excel files and SQL queries.

@@ porter-marines
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

@@ ie-q34
**Answer: (b) `to_csv()`**

**Why.** `df.to_csv('file.csv', index=False)` writes the DataFrame to CSV; `pd.read_csv` reads one.

**Concept: pandas I/O pairs.** read_csv / to_csv, read_excel / to_excel, read_json / to_json.

@@ ie-q36
**Answer: (c) −1**

**Why.** In `a.reshape(-1, 3)`, NumPy works out the −1 dimension from the total size (e.g. 12 elements → 4 rows).

**Concept: inferred dimension.** Only one dimension can be −1; it is total size ÷ product of the others.

@@ ie-q38
**Answer: (b) `df['C'].nunique()`**

**Why.** `nunique()` returns the number of distinct values; `unique()` returns the values themselves; the other method names do not exist.

**Concept: unique values.** `unique()` → array of distinct values, `nunique()` → their count, `value_counts()` → each value's frequency.

@@ mw-iitb-39
**Answer: 25**

**Why.** b takes 0, 2, 4, 6, 8; a adds b + 1 each time: 1 + 3 + 5 + 7 + 9 = 25.

**Concept: `range(0, 10, 2)`.** Starts at 0, steps by 2, stops before 10. (The sum of the first n odd numbers is n², here 5² = 25.)

@@ devrev-q5
**Answer: (c) 127.0.0.1**

**Why.** 127.0.0.1 is the standard loopback address: packets sent to it never leave the machine, so pinging it tests the host's own TCP/IP stack.

**Concept: loopback.** The whole 127.0.0.0/8 block is reserved for loopback; 127.0.0.1 ("localhost") is the conventional one.

@@ maq-q28
**Answer: (d) 255.255.254.0** (/23)

**Why.** 172.29.0.0 is a class B network (/16), leaving 16 bits. 70 subnets need 7 subnet bits (2⁷ = 128 ≥ 70). That leaves 9 host bits: 2⁹ − 2 = 510 hosts ≥ 480. Mask: 16 + 7 = 23 ones = 255.255.254.0.

**Concept: subnetting.** Borrow s bits from the host part for 2ˢ subnets; the remaining h bits give 2ʰ − 2 usable hosts (network and broadcast addresses are reserved). Pick s so both counts are enough.

@@ mw-iiitd-11
**Answer: (c) 191.254.1.29**

**Why.** /16 + 11 subnet bits = /27, so subnets are blocks of 32 addresses. 191.254.0.32 and 191.254.0.96 are block starts (subnet addresses, not hosts). 191.254.1.29 lies in the block 191.254.1.0–1.31 and is not its first or last address, so it is a valid host. (d) is a different network.

**Concept: network, broadcast and host addresses.** In each block, the first address is the subnet ID and the last is the broadcast; everything in between can be a host. Block size = 2^(32 − prefix).

@@ mw-iiitd-9
**Answer: (b) data link layer**

**Why.** The data link layer (layer 2) packages data into frames with MAC addresses. The network layer uses packets, the transport layer segments.

**Concept: OSI data units.** Physical: bits. Data link: frames. Network: packets. Transport: segments (TCP) or datagrams (UDP). Upper layers: data/messages.

@@ or-arp
**Answer: (a) to convert IP addresses to MAC addresses**

**Why.** To send a frame on a local network you need the receiver's MAC address. ARP broadcasts "who has this IP?" and the owner replies with its MAC. DNS does (b), TLS (c), routing protocols (d).

**Concept: ARP.** It links layer 3 (IP) to layer 2 (MAC) on the local link. Results are cached in the ARP table.

@@ or-ring
**Answer: (b) all devices are affected**

**Why.** In a simple (single, one-way) ring every message passes through every node, so one failed node breaks the loop for everyone. (Dual rings like FDDI can route around a failure, but that is not the textbook answer.)

**Concept: topologies and failure.** Bus: a cable break splits the network. Star: a node failure affects only that node (the hub is the weak point). Ring: one failure breaks the ring. Mesh: many paths, most robust.

@@ cisco2-routing
**Answer: (d) 10.10.13.208/29**

**Why.** A router uses the longest (most specific) prefix that contains the destination. 10.10.13.208/29 covers .208–.215, which includes .214. 10.10.13.0/25 covers only .0–.127 and 10.10.13.144/28 covers .144–.159, so neither contains .214. The default route is only for when nothing matches.

**Concept: longest-prefix match.** Each route is an address range. Among all ranges containing the destination, the smallest (largest prefix length) wins. A /29 is a block of 8 addresses, a /28 of 16, a /25 of 128.

@@ acc-int-hr
**How to answer.** Prepare short STAR stories (Situation, Task, Action, Result) for conflict, changing someone's mind, and a difficulty in an internship. Have a genuine reason for "why Accenture" and "why analytics", and know the company's main domains. If you mention a hobby, be ready to talk about it in detail.

**Concept: the STAR method.** Describe the situation and your task in one or two lines, spend most of the answer on what **you** did, and end with a measurable result and what you learned. It keeps behavioural answers specific and short.

@@ acc-int-tech
**How to prepare.**
- Linked list reversal with three pointers: prev = null, cur = head; repeat: next = cur.next, cur.next = prev, prev = cur, cur = next. Return prev.
- Circular lists: detect a cycle with Floyd's slow/fast pointers; traverse a known circular list until you come back to the start node.
- Qualitative variables: one-hot encoding for unordered categories, ordinal encoding for ordered ones.
- Know every line of your resume and be able to explain your project code.

**Concept: Floyd's cycle detection.** Move one pointer one step and another two steps at a time. If there is a cycle, the fast pointer eventually laps the slow one and they meet; if fast reaches null, there is no cycle. O(n) time, O(1) space.

@@ google-tree-root
**Answer (approach).**
1. Any vertex with at most 2 neighbours can be the root (a tree always has a leaf, so one exists).
2. Levels alternate in colour exactly when every edge joins two different colours, which does not depend on the root. If some edge has equal colours, return −1; otherwise return any vertex of degree ≤ 2.
3. With colours in the cyclic order R → B → W → R, a child's colour must follow its parent's. For each edge with different colours exactly one direction is allowed, so each edge fixes which end is the parent. A valid root exists iff no vertex gets two parents, exactly one vertex gets none (the root), and the root has at most 2 children. O(n).

**Why.** When a tree is rooted at r, every other vertex uses one neighbour as its parent, so with at most 3 neighbours it has at most 2 children. Only the root could have 3 children, so the root must have degree ≤ 2.

**Concept: rooting a tree.** Picking a root orients every edge from parent to child. Degree constraints and colour rules become constraints on these orientations; check them edge by edge in linear time.

@@ jsw-sjt-argument
**Answer: (c) agree to disagree and end the argument**

**Why.** It stops the escalation while keeping the friendship and respect. Walking away (a) is second best; confronting (b) or insulting back (d) escalates.

**Concept: situational judgement tests.** They reward calm, respectful, constructive responses that solve the problem and preserve relationships, over avoidance or retaliation.

@@ jsw-sjt-jobs
**Answer: no single correct option; (c) or (d) are usually rewarded.**

**Why.** Trying to negotiate a better package (shorter hours with the higher-paid job, or higher pay with the shorter-hours job) is proactive and balanced, rather than accepting a trade-off without trying.

**Concept: judgement questions test reasoning.** In an interview, explain what matters to you at this stage (learning, money, time) and why; there is rarely one right choice.
