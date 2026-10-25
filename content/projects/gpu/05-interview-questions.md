---
title: "3 · Interview questions"
weight: 5
---

Questions an interviewer can reasonably ask about these two projects, grouped by topic, with model answers. **Cover the answer, say yours out loud, then open it.** Answers are written to be spoken in 20 to 60 seconds; the "Depth" lines are for follow-ups.

Evidence labels (Measured, Code, Reasoned, Rule of thumb) are explained on the [section landing page](../). When an answer uses a number, it is the one recorded for the single Colab run.

## A. The project as a whole

{{< details title="A1. Walk me through the project in one minute." >}}

I wrote two CUDA programs from scratch to learn GPU programming properly. The first is a tiled 2D convolution: multi-channel, multiple filters, zero padding, with shared-memory tiling and a halo. The second is a parallel Borůvka minimum spanning tree on a road graph with terrain-adjusted costs, built from atomics, pointer jumping and a Blelloch prefix-sum used for edge compaction. Both are checked against CPU reference implementations and I ran them on a real GPU with compute-sanitizer. The MST ran about 13 times faster than sequential Kruskal on a 200K-vertex, 1.2M-edge graph, in one run including copies. The convolution was an honest negative result: the tiled kernel was not faster than the naive one at 3×3, and I can explain why.

{{< /details >}}

{{< details title="A2. Why did you build these? Was this coursework?" >}}

To understand GPU programming by implementing standard algorithms myself, and to have concrete material for systems and GPU discussions. It is not a coursework submission and I do not present it as research. The algorithms are standard (tiled stencil, Borůvka, Blelloch scan); the work is in implementing them correctly, testing them properly and understanding the performance.

*If pushed on the course:* I took GPU programming (CS6023) at IIT Madras; this repo is separate self-study material and uses my own implementations.

{{< /details >}}

{{< details title="A3. What was the hardest bug or design problem?" >}}

For the MST: **ties**. With equal-weight edges, components can choose different edges that form a cycle longer than two in the hook graph, and pointer jumping then has no root. The fix was a strict total order on edges, `(weight, edge index)`, built with two `atomicMin` passes because a packed key would overflow 64 bits for large weights. For the convolution: **barrier placement**. Out-of-range threads must still take part in loading and in every `__syncthreads()`, so I guard only the compute and the store, never the barrier.

{{< /details >}}

{{< details title="A4. What would you do differently / what are the limitations?" >}}

MST: the atomics on hot components serialise, per-round arrays are `O(V)` even when few components remain, and the host reads a counter or flag every iteration, which stalls the pipeline. Convolution: every filter's blocks reload the same input tile, filters could sit in constant memory, and I would add register tiling and vectorised loads. For both I would profile with Nsight before optimising, and I would benchmark many runs across sizes rather than one.

{{< /details >}}

## B. GPU fundamentals

{{< details title="B1. What is a warp? What is warp divergence?" >}}

A warp is 32 threads that execute the same instruction together (SIMT). If threads of one warp take different branches, the hardware runs each path in turn with the other lanes masked off, so the warp pays for both. Divergence only matters within a warp; different warps can branch independently at no cost.

{{< /details >}}

{{< details title="B2. Explain the memory hierarchy and how you used it." >}}

Registers (private, fastest), shared memory (per block, on-chip, programmer-managed), L1/L2 caches, global memory (large, hundreds of cycles of latency), constant memory (read-only, fast broadcast). In the convolution, the accumulator is in a register, the tile and the filter slice are in shared memory, and the image, filters and output are in global memory. In the MST everything lives in global memory except the scan, which stages blocks of 256 elements in shared memory.

{{< /details >}}

{{< details title="B3. What is coalescing and where does your code rely on it?" >}}

When a warp's 32 threads access 32 consecutive words, the hardware serves them with one or two memory transactions; scattered accesses can need up to 32. In the convolution `threadIdx.x` indexes the fast axis, so tile loads and output stores are contiguous. In the MST the edge arrays are read coalesced, but `comp[eu[i]]` is a gather by vertex id, which is not, and that is inherent to graph algorithms.

{{< /details >}}

{{< details title="B4. What is a bank conflict? Does your code have any?" >}}

Shared memory has 32 banks of 4-byte words. If threads of a warp access different words in the same bank the accesses serialise. The convolution inner loop reads consecutive words (no conflict) and the filter value is the same for all threads (broadcast, no conflict). The Blelloch scan has strided accesses that conflict at higher strides; the standard fix is index padding, which I have not implemented and would list as a known improvement.

{{< /details >}}

{{< details title="B5. What is occupancy and is higher always better?" >}}

Resident warps divided by the SM's maximum. It lets the SM hide memory latency by switching warps. It is limited by registers per thread, shared memory per block and block size. Higher is not always better: a kernel with enough independent work per thread can saturate the hardware at lower occupancy, and chasing occupancy by cutting registers can cause spills.

{{< /details >}}

{{< details title="B6. How do you synchronise threads on a GPU?" >}}

Within a block, `__syncthreads()`. Across blocks inside one kernel there is no barrier; you end the kernel and launch another, because launch boundaries on a stream act as global barriers. That is why one Borůvka round is several small kernels. Atomics provide safe concurrent updates to a single location but do not order other memory.

{{< /details >}}

{{< details title="B7. What is wrong with an early return before __syncthreads()?" >}}

If only some threads of a block reach the barrier, the behaviour is undefined (hang or wrong results). All threads of the block must reach it. So I guard the work with `if (x < W && y < H)` but let every thread run the loads and the barriers.

{{< /details >}}

{{< details title="B8. Are kernel launches and errors synchronous?" >}}

No. Launches are asynchronous with respect to the host, and kernel execution errors surface later. I check `cudaGetLastError()` after launches (catches launch-configuration errors) and `cudaDeviceSynchronize()` at the end (surfaces execution errors). A blocking `cudaMemcpy` also synchronises. All CUDA calls go through a `CUDA_CHECK` macro that throws with file and line.

{{< /details >}}

{{< details title="B9. Why wrap device memory in a class?" >}}

RAII. `DevBuf<T>` calls `cudaFree` in its destructor, so if an exception is thrown halfway through the algorithm (for example a failed CUDA call) nothing leaks. It is non-copyable to prevent double frees.

{{< /details >}}

{{< details title="B10. When is a GPU the wrong tool?" >}}

Small inputs (fixed launch, allocation and transfer costs dominate), sequential dependency chains, heavy divergence, irregular memory access with little arithmetic, and workloads where moving the data over PCIe costs more than the computation saves.

{{< /details >}}

## C. 2D convolution

{{< details title="C1. What exactly does the kernel compute? Convolution or correlation?" >}}

Cross-correlation: the filter is not flipped. For output `(k, y, x)` it sums `img[c][y + r − R/2][x + s − S/2] × flt[k][c][r][s]` over channels and filter taps, with zero outside the image. This is what deep-learning libraries call convolution.

{{< /details >}}

{{< details title="C2. Explain the tiled kernel." >}}

One block computes a 32×8 tile of one output map. For each input channel, all threads cooperatively load the input tile plus a halo of `R−1` rows and `S−1` columns, and the filter slice, into shared memory, synchronise, accumulate from shared memory into a register, synchronise again, and move to the next channel. Cells outside the image are loaded as zero, which is the padding.

{{< /details >}}

{{< details title="C3. Why do you need the halo?" >}}

A thread at the edge of the tile needs neighbours that belong to the adjacent tile. The halo is that extra border, `R/2` on each vertical side and `S/2` on each horizontal side, loaded redundantly by this block.

{{< /details >}}

{{< details title="C4. Why two __syncthreads()?" >}}

The first ensures the tile and filter are completely loaded before anyone reads. The second ensures everyone has finished reading before the next channel iteration overwrites the buffers. Missing the second is a race that only shows up with several channels.

{{< /details >}}

{{< details title="C5. How much shared memory does it use? What if the filter is huge?" >}}

`((BY + R − 1)(BX + S − 1) + R·S) × 4` bytes: 1396 bytes for 3×3 with the 32×8 tile. The host checks against 48 KB; in `Auto` mode, a filter too big for that falls back to the naive global-memory kernel. With the default tile the largest odd square filter that fits is 67×67.

{{< /details >}}

{{< details title="C6. How does padding work without branches in the inner loop?" >}}

The branch is in the load, not the compute loop: when staging the tile each cell is checked against the image bounds and written as 0 if outside. The compute loop reads shared memory with no checks.

{{< /details >}}

{{< details title="C7. Your tiled and naive kernels took the same time. Why?" >}}

For a 3×3 filter, neighbouring reads are already served by L1/L2 cache, so shared-memory staging saves little. The wall time includes allocation and copying, and the output is 64-bit (about 67 MB for 8 maps of 1 M pixels), so the copy likely dominates the kernel. I did not profile it, so I call that the likely explanation, not a proven one. To confirm: Nsight Systems for copy vs kernel time, Nsight Compute for DRAM traffic, and try 7×7 and 15×15 filters, where reuse per pixel is much higher.

{{< /details >}}

{{< details title="C8. What is the halo overhead and how do you trade tile size?" >}}

Loads per output pixel are `(BX+S−1)(BY+R−1) / (BX·BY)`: 340/256 ≈ 1.33 for 3×3 at 32×8. Bigger tiles shrink the relative halo but use more shared memory per block, which can lower occupancy, and must still fit in the block-size limit.

{{< /details >}}

{{< details title="C9. How would you make it faster?" >}}

Compute several filters per block from one staged tile (reuse across `K`), put small filters in constant memory, add register tiling (each thread computes a small patch), vectorised loads, and use 32-bit output when sums fit. For production use, convert to a matrix multiplication (im2col or implicit GEMM) on tensor cores, or Winograd/FFT for suitable sizes. That is what cuDNN does.

{{< /details >}}

{{< details title="C10. Why int image and long long output?" >}}

Pixel values and filter weights fit in 32 bits, but a sum over `C·R·S` products can exceed 2³¹, so I accumulate in 64-bit. The trade-off is double the output traffic.

{{< /details >}}

{{< details title="C11. Why is the grid 3-D with filters on z?" >}}

A simple mapping: each z-slice is an independent output map. It also keeps the filter index uniform within a block. The limitation is that `gridDim.z` and `gridDim.y` cap at 65535, which the wrapper checks.

{{< /details >}}

## D. Parallel Borůvka MST

{{< details title="D1. Explain Borůvka's algorithm." >}}

Start with every vertex as its own component. In each round, every component picks its lightest outgoing edge; all those edges are added; components joined by them merge. Repeat until no edge leaves any component. Every component merges with at least one other each round, so the number of components at least halves and there are at most `⌈log₂ V⌉` rounds.

{{< /details >}}

{{< details title="D2. Why Borůvka and not Kruskal or Prim on a GPU?" >}}

Kruskal needs edges processed in sorted order with union-find state, which is sequential. Prim grows one tree one edge at a time. Borůvka's work in a round is data-parallel: every edge and every component can be handled independently, and the number of rounds is logarithmic.

{{< /details >}}

{{< details title="D3. Walk me through one round on the GPU." >}}

(1) Compact the edge list to edges between different components, using flag + exclusive scan + scatter. (2) Find each component's lightest outgoing edge with two `atomicMin` passes. (3) Make each component point at the component on the other end of its edge. (4) Break mutual pairs: the smaller id becomes the root and only the other adds the edge weight. (5) Pointer-jump until every component points at its root. (6) Relabel every vertex with its root. Each step is its own kernel since the next one needs all of the previous one's results.

{{< /details >}}

{{< details title="D4. Why do ties break the algorithm, and how did you fix it?" >}}

With equal weights, components can pick different edges forming a cycle of length greater than two in the hook graph (a triangle of equal edges, each picking a different one), so there is no root. I compare edges by `(weight, index)`, a strict total order. Along a path of hooks the keys of the chosen edges are non-increasing; a cycle would need all keys equal, which means the same edge, and one edge joins only two components, so the only possible cycles are mutual pairs.

{{< /details >}}

{{< details title="D5. Why two atomicMin passes instead of one packed key?" >}}

Adjusted weights can need more than 32 bits (base up to 10⁹ times 5), so packing weight and index in one 64-bit word would overflow. Pass 1 finds the minimum weight, pass 2 finds the smallest index among edges with that weight, giving the lexicographic minimum.

{{< /details >}}

{{< details title="D6. What is pointer jumping and why does it need two buffers?" >}}

Repeatedly set `p[c] = p[p[c]]`. The distance each node reaches doubles each step, so a tree of depth `d` flattens in `O(log d)` steps. If threads read and write the same array in one step, a thread may read a pointer another thread has already updated; results then depend on scheduling. Reading from array A and writing to array B, then swapping, makes every step well-defined.

{{< /details >}}

{{< details title="D7. How do you count each edge's weight exactly once?" >}}

For a mutual pair both components chose the same edge, so only the larger id adds its weight (the smaller becomes the root). Every non-mutual component adds its own chosen edge. Edges chosen by different components are different edges, so nothing is double counted. The sum is a 64-bit `atomicAdd`; the modulo is applied only at the end.

{{< /details >}}

{{< details title="D8. Why not apply the modulus while summing?" >}}

Edges must be compared by true cost. The modulus applies only to the final output sum. Using 64-bit exact sums avoids overflow for the sizes involved, and nothing in the comparisons uses modded values.

{{< /details >}}

{{< details title="D9. What does the graph being disconnected change?" >}}

Nothing structurally: the algorithm stops when no edge leaves any component and yields a minimum spanning forest. The edge count is less than `V − 1`; the driver prints a warning, and the tests compare against Kruskal's edge count too.

{{< /details >}}

{{< details title="D10. Where are the performance bottlenecks?" >}}

Atomic contention on high-degree components, uncoalesced gathers `comp[eu[i]]`, the host reading the survivor count and the pointer-jump flag every iteration, and `O(V)` per-round arrays even after most components have merged. I have not profiled to rank them, so I would measure before optimising.

{{< /details >}}

{{< details title="D11. How would you reduce atomic contention?" >}}

Sort the edges by component and do a segmented min-reduce, or reduce within a warp (shuffle) or block (shared memory) first and then issue one atomic per warp/block, or give high-degree vertices special handling.

{{< /details >}}

{{< details title="D12. Why an edge list and not CSR?" >}}

Each round touches edges independently and compacts them, so a flat list with one thread per edge is simple, balanced, and shrinks easily. CSR gives neighbour access in `O(1)` but is awkward to compact; it suits traversal algorithms such as BFS better.

{{< /details >}}

{{< details title="D13. Prove it terminates in at most log V rounds." >}}

Each component with an outgoing edge hooks onto another, so each tree in the merged result contains at least two old components. The number of components that still have outgoing edges at least halves per round, so after `⌈log₂ V⌉` rounds none remain. The code throws if it ever exceeds 64 rounds, as a bug trap.

{{< /details >}}

{{< details title="D14. Trace the sample." >}}

Five vertices, adjusted weights `e0=6, e1=10, e2=1, e3=12, e4=4, e5=25, e6=3`. Round 1: components 1 and 2 both choose `e2` (1), 3 and 4 both choose `e6` (3), 0 chooses `e0` (6): pay 1 + 3 + 6 = 10, components become `{0,1,2}` and `{3,4}`. Round 2: the surviving crossing edges are `e3, e4, e5`; both sides choose `e4` (4): total 14. Round 3: no crossing edges, stop. (Full table in [2b](../03-boruvka-mst/#a-hand-trace-on-the-sample).)

{{< /details >}}

## E. Scan and compaction

{{< details title="E1. What is a prefix sum and why is it central on GPUs?" >}}

`out[i]` is the sum of all elements before `i`. It converts per-element decisions into positions: each surviving element needs to know how many survive before it. That is the basis of compaction, sorting (radix), and many load-balancing tricks.

{{< /details >}}

{{< details title="E2. Blelloch vs Hillis-Steele?" >}}

Hillis-Steele does `O(n log n)` additions in `log n` steps and is simple. Blelloch does `O(n)` additions with an up-sweep (a reduction tree) and a down-sweep, taking about `2 log n` steps. Blelloch is work-efficient, which matters when `n` exceeds the number of processors.

{{< /details >}}

{{< details title="E3. How does your scan handle arrays larger than a block?" >}}

Scan each block of 256 and save the block total; recursively scan the array of block totals; add each block's scanned total back to its elements. Because it recurses, there is no limit on `n`. For 1.2 M elements it needs three levels.

{{< /details >}}

{{< details title="E4. How does compaction work?" >}}

Write 1 for kept elements and 0 otherwise, take the exclusive scan so each kept element has its output position, then each kept element writes itself to that position. Order is preserved, which keeps the edge-index tie-break consistent between rounds.

{{< /details >}}

{{< details title="E5. Why is the scan exclusive here?" >}}

For compaction, the exclusive scan value of a kept element is exactly its destination index, and the total number kept is `pos[last] + keep[last]`.

{{< /details >}}

## F. Testing, measurement and honesty

{{< details title="F1. How do you know it is correct?" >}}

Three layers. Self-checking tests compare against independent CPU references (naive convolution loops; Kruskal with union-find) on spec examples plus random, structured and tie-heavy inputs at several block and tile sizes. I also seeded bugs (broken padding, missing `__syncthreads`, dropped scan offsets, no 2-cycle breaking, inconsistent tie-break) to confirm the tests catch them. Finally I ran everything on a real GPU with `compute-sanitizer` memcheck, racecheck and synccheck, all clean.

{{< /details >}}

{{< details title="F2. How did you test without a GPU?" >}}

I wrote a small CPU emulation of the CUDA subset I used: blocks run one at a time, threads in a block are fibers, and `__syncthreads()` is a real barrier. It validated indexing and algorithm logic on the unchanged kernel source. It cannot catch warp-level behaviour, real races or `nvcc` errors, so I then verified on a real GPU in Colab.

{{< /details >}}

{{< details title="F3. What does 13× mean exactly?" >}}

CPU Kruskal 258.7 ms versus GPU Borůvka 19.6 ms (7 rounds) for a random graph of 200 000 vertices and 1.2 M edges, one run on a Colab GPU, with allocation and host-device copies included in the GPU time. It is a single run against a single-threaded baseline on one graph family, so it indicates a clear win at this size, not a general constant.

{{< /details >}}

{{< details title="F4. Is that a fair comparison?" >}}

It is fair in the sense that the copies are counted against the GPU. It is limited in that the CPU baseline is straightforward Kruskal, not a tuned or parallel CPU implementation, there is no variance across runs, and I did not profile where the 19.6 ms goes. I would rerun many times, sweep sizes and compare to a stronger CPU baseline before quoting anything stronger.

{{< /details >}}

{{< details title="F5. Would the speedup hold for tiny graphs or real road networks?" >}}

For tiny graphs no: fixed costs dominate and the CPU wins. For real road networks I would expect different behaviour (low degree, near-planar, possibly more rounds and different contention) and have not measured it. <span style="color:#7c3aed"><strong>[Reasoned]</strong></span>

{{< /details >}}

{{< details title="F6. What does compute-sanitizer check?" >}}

`memcheck`: out-of-bounds and misaligned accesses and leaks. `racecheck`: data races on shared memory. `synccheck`: invalid use of barriers. `initcheck`: reads of uninitialised global memory (not in my run). They are slow, so I ran them on small inputs.

{{< /details >}}

{{< details title="F7. Is global-memory racecheck covered?" >}}

`racecheck` covers shared-memory hazards only. Global-memory races between blocks are not detected by it. In this code the cross-block writes are atomics, or each thread owns its own output, which I argued by design; the tests and `memcheck` do not prove their absence. Be honest about that.

{{< /details >}}

## G. Curveballs

{{< details title="G1. If I gave you a 100 million edge graph, what breaks?" >}}

Device memory first: with 4-byte endpoints, 8-byte weights and double buffers, the edge arrays alone are about `E × (4 + 4 + 8) × 2` bytes = 3.2 GB for `E = 10⁸`, plus flags and scan outputs. <span style="color:#7c3aed"><strong>[Reasoned]</strong></span> I would need out-of-core or multi-GPU partitioning, and `int` edge counts would need checking (the code rejects more than `INT_MAX` edges).

{{< /details >}}

{{< details title="G2. How would you speed up the pointer-jumping loop?" >}}

Avoid the host round-trip by running a fixed `⌈log₂ V⌉` jumps, or loop on the device (dynamic parallelism, a persistent kernel, or a CUDA graph), keeping the "changed" flag on the device.

{{< /details >}}

{{< details title="G3. Could you use thrust / cub instead of writing your own scan?" >}}

Yes, and in production code I would: `cub::DeviceScan` and `thrust::exclusive_scan` are tuned and well tested. I wrote my own to understand the algorithm and its memory behaviour. My version is for learning and I would not claim it beats the library.

{{< /details >}}

{{< details title="G4. How would you convolve with a 31×31 filter?" >}}

Shared memory then becomes a real constraint: tile + halo of `(8+30)(32+30)` ints is about 9.4 KB plus 3.8 KB for the filter slice, still under 48 KB, and reuse per pixel is high, so tiling should now pay off. Beyond that, split the filter into chunks, use constant memory, or use FFT-based convolution for large kernels.

{{< /details >}}

{{< details title="G5. Why not use streams or overlap copies with compute?" >}}

Not needed for a reference implementation, but it is the obvious next step: pinned host memory plus `cudaMemcpyAsync` on several streams, tiling the image into bands, so copying band `i+1` overlaps with computing band `i`. This would address the transfer cost that dominates the convolution timing.

{{< /details >}}

{{< details title="G6. What is the difference between a thread block and a warp for synchronisation?" >}}

A block can use `__syncthreads()`. Warps are scheduled together but you should not rely on implicit warp-synchronous execution; use explicit primitives (`__syncwarp()`, shuffles) on modern GPUs because independent thread scheduling means lanes of a warp are no longer guaranteed lock-step.

{{< /details >}}

## Rapid-fire (one line each)

| Question | Short answer |
|---|---|
| Threads per warp? | 32 |
| Max threads per block? | 1024 |
| Which blocks can synchronise? | None, within one kernel. Use a new launch |
| Shared memory banks? | 32, 4 bytes each |
| Why guard `i < n`? | Grid is rounded up to whole blocks |
| Scan work (Blelloch)? | `O(n)` |
| Pointer jumping steps? | `O(log depth)` |
| Borůvka max rounds? | `⌈log₂ V⌉` |
| Why total order on edges? | Only 2-cycles can occur |
| Tiled vs naive at 3×3? | Same time; cache and the copy dominate |
