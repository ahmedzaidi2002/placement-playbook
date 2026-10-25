---
title: "5 · Synchronization"
linkTitle: "5 Synchronization"
weight: 5
math: true
---
## 5.1 Race conditions and the critical-section problem {#sec-os-race}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> four threads doing `counter++` a million times each and ending far short of four million.</em>

</div>

```c {filename="race.c"}
// flags: -D_GNU_SOURCE -pthread
// Four threads each add 1 to a shared counter 1,000,000 times, four ways.
#include <stdio.h>
#include <pthread.h>
#include <stdatomic.h>

enum { THREADS = 4, N = 1000000 };
static volatile long plain;                 // volatile does NOT make ++ atomic
static long locked;
static atomic_long atomic_counter;
static long spun;
static pthread_mutex_t m = PTHREAD_MUTEX_INITIALIZER;
static atomic_flag spin = ATOMIC_FLAG_INIT;

static void *racy(void *a)  { for (int i = 0; i < N; i++) plain++; return a; }
static void *mutexed(void *a) {
    for (int i = 0; i < N; i++) {
        pthread_mutex_lock(&m); locked++; pthread_mutex_unlock(&m);
    }
    return a;
}
static void *atomics(void *a) {
    for (int i = 0; i < N; i++) atomic_fetch_add(&atomic_counter, 1);
    return a;
}
static void *spinning(void *a) {
    for (int i = 0; i < N; i++) {
        while (atomic_flag_test_and_set(&spin)) {}   // TSL: spin until 0 -> 1
        spun++;
        atomic_flag_clear(&spin);                    // release: store 0
    }
    return a;
}

static void run(const char *name, void *(*f)(void *), long (*get)(void)) {
    pthread_t t[THREADS];
    for (int i = 0; i < THREADS; i++) pthread_create(&t[i], NULL, f, NULL);
    for (int i = 0; i < THREADS; i++) pthread_join(t[i], NULL);
    printf("%-28s %8ld of %d\n", name, get(), THREADS * N);
}
static long g1(void) { return plain; }
static long g2(void) { return locked; }
static long g3(void) { return atomic_load(&atomic_counter); }
static long g4(void) { return spun; }

int main(void) {
    run("counter++ (no protection)", racy, g1);
    run("pthread mutex", mutexed, g2);
    run("atomic_fetch_add", atomics, g3);
    run("test-and-set spinlock", spinning, g4);
    return 0;
}
```

```text {filename="One possible output (gcc 13.3, glibc 2.39, Linux 6.18 x86-64)"}
counter++ (no protection)     2009069 of 4000000
pthread mutex                 4000000 of 4000000
atomic_fetch_add              4000000 of 4000000
test-and-set spinlock         4000000 of 4000000
```

`counter++` is three machine steps: load the value into a register, add one, store it back. If two threads both load $41$, both store $42$, and one increment is lost. Which interleaving happens depends on timing, so the result changes from run to run (and `volatile` does not help: it only stops the compiler from caching the value in a register; it makes nothing atomic). The other three versions are correct; the rest of the chapter explains why.

<div class="nb nb-definition" id="definition-5-1-1">

<strong>Definition 5.1.1</strong>. A <strong>race condition</strong> is a situation where the result depends on the relative timing of operations on shared data, at least one of which writes. A <strong>critical section</strong> (CS) is the code that touches the shared data. A solution wraps it as <em>entry section</em> $\to$ CS $\to$ <em>exit section</em> $\to$ remainder, and must guarantee:

1. <strong>Mutual exclusion</strong>: at most one process is in its CS at any time.
2. <strong>Progress</strong>: if no process is in its CS and some want to enter, only those trying (not those in their remainder) take part in deciding who enters, and the decision is not postponed forever. In practice: no deadlock, and a process that does not want the CS cannot block one that does.
3. <strong>Bounded waiting</strong>: after a process asks to enter, there is a bound on how many times others may enter before it does. In practice: no starvation.

No assumption may be made about relative speeds or the number of CPUs.

</div>

<div class="nb nb-remark" id="remark-5-1-2">

<strong>Remark 5.1.2</strong> (How to check a proposed solution) — For mutual exclusion, look for one interleaving that puts two processes in the CS (one is enough to refute). For progress, look for a state where both are stuck in the entry section (deadlock), or where one cannot enter only because the other is in its remainder (strict alternation). For bounded waiting, let one process wait while the other leaves and re-enters repeatedly: if that can go on forever, it fails. Mutual exclusion alone is easy (never let anyone in); the three together are the problem.

</div>

## 5.2 Software solutions and why they need fences {#sec-os-peterson}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> Peterson’s algorithm, correct on paper, losing thousands of updates on a real multicore CPU.</em>

</div>

### 5.2.i Two failed attempts {#s5-2-i}

- <strong>Strict alternation</strong> (`while (turn != i); CS; turn = j;`): mutual exclusion holds, but if process $j$ stays in its remainder, $i$ can never enter twice in a row: progress fails.
- <strong>Flags only</strong> (`flag[i] = 1; while (flag[j]); CS; flag[i] = 0;`): mutual exclusion holds, but if both set their flags at once both wait forever: progress fails (deadlock). Checking the flag before setting one’s own breaks mutual exclusion instead.

### 5.2.ii Peterson’s algorithm {#s5-2-ii}

<div class="nb nb-remark" id="algorithm-5-2-1">

<strong>Algorithm 5.2.1</strong> (Peterson, process $i$, other process $j$) — `flag[i] = true; turn = j; while (flag[j] && turn == j) ; ` CS `flag[i] = false;`

</div>

<div class="nb nb-theorem nb-block" id="theorem-5-2-2">

<strong>Theorem 5.2.2</strong>

On sequentially consistent memory, Peterson’s algorithm satisfies all three requirements for two processes.

</div>

<div class="nb nb-proof">

<em>Proof.</em> <em>Mutual exclusion</em>: suppose both are in the CS, so both flags are true. One of them wrote `turn` last, say $i$ (so `turn`$=j$). Process $j$ had set `flag[j]` before its own write to `turn`, hence before $i$’s; so when $i$ tested its loop condition after writing `turn`, it saw `flag[j]` true and `turn`$=j$ and kept waiting, a contradiction. <em>Progress</em>: `turn` is either $i$ or $j$, so at most one of them waits. <em>Bounded waiting</em>: when $j$ leaves and tries again it sets `turn=i`, so $i$ enters after at most one entry by $j$.

</div>

<strong>Dekker’s algorithm</strong> (the first correct two-process solution) uses flags plus a turn variable that decides only under contention. <strong>Lamport’s bakery algorithm</strong> handles $n$ processes: each takes a ticket one larger than the maximum it sees and enters in (ticket, id) order; ties are possible because ticket taking is not atomic, and the id breaks them. All of these use only loads and stores, which is exactly their weakness:

```c {filename="peterson.c"}
// flags: -D_GNU_SOURCE -pthread
// Peterson's algorithm protecting count++, with and without a full fence
// between "announce" and "check". Lost updates = mutual exclusion violated.
#include <stdio.h>
#include <pthread.h>
#include <stdatomic.h>

enum { N = 2000000 };
static atomic_int flag[2], turn;
static long count;
static int use_fence;

static void lock(int i) {
    int j = 1 - i;
    atomic_store_explicit(&flag[i], 1, memory_order_relaxed);  // I want in
    atomic_store_explicit(&turn, j, memory_order_relaxed);     // you go first
    if (use_fence) atomic_thread_fence(memory_order_seq_cst);
    while (atomic_load_explicit(&flag[j], memory_order_relaxed) &&
           atomic_load_explicit(&turn, memory_order_relaxed) == j) {}
    atomic_thread_fence(memory_order_acquire);
}
static void unlock(int i) {
    atomic_store_explicit(&flag[i], 0, memory_order_release);
}
static void *worker(void *arg) {
    int i = *(int *)arg;
    for (int k = 0; k < N; k++) { lock(i); count++; unlock(i); }
    return NULL;
}

static void trial(int fence) {
    use_fence = fence; count = 0;
    pthread_t t[2]; int id[2] = {0, 1};
    for (int i = 0; i < 2; i++) pthread_create(&t[i], NULL, worker, &id[i]);
    for (int i = 0; i < 2; i++) pthread_join(t[i], NULL);
    printf("%-14s count = %7ld of %d, lost updates: %ld\n",
           fence ? "with fence:" : "without fence:", count, 2 * N,
           2L * N - count);
}

int main(void) { trial(0); trial(1); return 0; }
```

```text {filename="One possible output (gcc 13.3, glibc 2.39, Linux 6.18 x86-64)"}
without fence: count = 3993076 of 4000000, lost updates: 6924
with fence:    count = 4000000 of 4000000, lost updates: 0
```

### 5.2.iii Why it fails: memory ordering {#s5-2-iii}

The proof assumed that the store `flag[i] = true` is visible to the other CPU before the load of `flag[j]`. x86 lets a load complete before an earlier store to a different address has left the CPU’s <strong>store buffer</strong>. Both processes can then read the other’s flag as $0$ and enter together. The minimal test of this effect is the store-buffering litmus test: under sequential consistency the outcome $(a,b)=(0,0)$ is impossible, which the exhaustive explorer of [Section 5.5](#sec-os-interleave) confirms (item 5 of its output); real hardware produces it:

```c {filename="store-buffer.c, lines 14–22",linenos=table,linenostart=14}
static void *t1(void *arg) {
    for (int i = 1; i <= TRIALS; i++) {
        while (atomic_load_explicit(&go1, memory_order_acquire) != i) {}
        atomic_store_explicit(&x, 1, memory_order_relaxed);
        if (fenced) atomic_thread_fence(memory_order_seq_cst);
        a = atomic_load_explicit(&y, memory_order_relaxed);
        atomic_store_explicit(&done1, i, memory_order_release);
    }
    return arg;
```

```text {filename="One possible output (gcc 13.3, glibc 2.39, Linux 6.18 x86-64)"}
no fence: (a,b) = (0,0) in   2624 of 200000 trials
fenced:   (a,b) = (0,0) in      0 of 200000 trials
```

<div class="nb nb-definition" id="definition-5-2-3">

<strong>Definition 5.2.3</strong>. A <strong>memory model</strong> says which reorderings of loads and stores other threads may observe. <strong>Sequential consistency</strong>: as if all operations of all threads were interleaved in program order. x86 (TSO) only lets a later load pass an earlier store; ARM and POWER allow much more. A <strong>fence</strong> (barrier) forbids reordering across it; in C11, `atomic_thread_fence(memory_order_seq_cst)` is a full fence (`mfence` or a `lock`ed instruction on x86). <strong>Acquire</strong> (on a load) keeps later accesses after it, <strong>release</strong> (on a store) keeps earlier accesses before it: lock acquisition is an acquire, unlock a release. The compiler reorders too, so a fence is also a compiler barrier.

</div>

<div class="nb nb-moral">

Software-only mutual exclusion is correct only on sequentially consistent memory; on real CPUs it needs fences, and at that point an atomic instruction is simpler and faster.

</div>

## 5.3 Hardware support {#sec-os-atomics}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> `while (test_and_set(&lock));`: one instruction that reads the old value and writes 1, with no other CPU able to get in between.</em>

</div>

- <strong>Disabling interrupts</strong> around the CS: works on a uniprocessor (no timer, no preemption), is privileged (user code cannot do it), and does nothing for other CPUs. Kernels use it only for very short sections on the local CPU.
- <strong>Atomic read-modify-write instructions</strong>, which the cache-coherence protocol makes indivisible across CPUs:

  - <strong>test-and-set</strong> (TSL): set to 1, return the old value;
  - <strong>swap</strong>/`xchg`: exchange a register and a memory word;
  - <strong>compare-and-swap</strong> (CAS, x86 `lock cmpxchg`): if `*p == expected`, store `new`; return whether it did (or the old value);
  - <strong>fetch-and-add</strong> (`lock xadd`): add and return the old value;
  - <strong>load-linked/store-conditional</strong> (ARM, RISC-V): the store fails if anyone wrote the location since the load.

In `race.c` the spinlock is `atomic_flag_test_and_set` in a loop and the counter is `atomic_fetch_add`; both gave exactly four million.

<div class="nb nb-remark" id="remark-5-3-1">

<strong>Remark 5.3.1</strong> (OA: “which are hardware solutions to the critical-section problem?”) — `test_and_set()` and `compare_and_swap()` are (atomic instructions); disabling interrupts is a hardware mechanism too (uniprocessor only). Peterson’s solution is a <em>software</em> solution, as are Dekker and the bakery algorithm. Semaphores and mutexes are OS/library abstractions built on the hardware instructions.

</div>

<div class="nb nb-remark" id="remark-5-3-2">

<strong>Remark 5.3.2</strong> (A TSL spinlock is not fair) — The simple TSL loop satisfies mutual exclusion and progress but not bounded waiting: the thread that just released may win again every time. Fair versions: a <strong>ticket lock</strong> (fetch-and-add a ticket, wait until `now_serving` equals it) or Silberschatz’s waiting-array algorithm, where the releasing process hands the lock to the next waiting process in cyclic order, giving a bound of $n-1$.

</div>

## 5.4 Locks, semaphores, condition variables, monitors {#sec-os-primitives}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> a lock held for 50 ns should be spun on; a lock held across a disk read should put the waiter to sleep.</em>

</div>

<div class="nb nb-definition" id="definition-5-4-1">

<strong>Definition 5.4.1</strong>. The tools, from lowest to highest level:

- A <strong>spinlock</strong> busy-waits. No context switch, so it is best when the wait is shorter than two switches and the holder is running on another CPU; terrible on a uniprocessor or when the holder can sleep. Kernels use spinlocks with preemption disabled.
- A <strong>mutex</strong> (sleeping lock) blocks the waiter in the kernel. It has an <em>owner</em>: only the locker may unlock. Linux implements it on a <strong>futex</strong>: the uncontended lock and unlock are a single atomic instruction in user space; only a waiter makes a system call.
- A <strong>semaphore</strong> is an integer $S$ with two atomic operations: `wait` (`P`, `down`): decrement, block if the result is negative (or: block while $S=0$, then decrement); `signal` (`V`, `up`): increment and wake one waiter. A <strong>binary</strong> semaphore takes values 0 and 1; a <strong>counting</strong> semaphore counts resources. No owner: any thread may signal.
- A <strong>condition variable</strong> lets a thread sleep until some condition on shared data holds: `wait(cv, m)` atomically releases mutex `m` and sleeps, and re-acquires `m` before returning; `signal`/`broadcast` wakes one/all. It has no memory: a signal with no waiter is lost.
- A <strong>monitor</strong> is a language construct: an object whose methods run under one implicit mutex, plus condition variables (Java `synchronized` with `wait`/`notify`, C\# `lock`).

</div>

<div class="nb nb-remark" id="remark-5-4-2">

<strong>Remark 5.4.2</strong> (Mutex vs binary semaphore) — Both allow one holder, but a mutex has an owner (so it can be recursive, can detect unlock-by-non-owner, and can do priority inheritance), while a semaphore is a signalling counter: one thread waits, another (or an interrupt handler) posts. Use a mutex for mutual exclusion and a semaphore for “wait until something has happened” or counting resources.

</div>

<div class="nb nb-remark" id="remark-5-4-3">

<strong>Remark 5.4.3</strong> (Always wait in a `while` loop) — `while (!condition) pthread_cond_wait(&cv, &m);`, never `if`. With Mesa semantics (pthreads, Java) the signalled thread does not run immediately; another thread can take the mutex and change the condition first, and POSIX also allows spurious wake-ups. (Hoare semantics hand the monitor straight to the woken thread, which makes `if` correct but is rarely implemented.)

</div>

### 5.4.i Semaphore arithmetic {#s5-4-i}

<div class="nb nb-theorem nb-block" id="theorem-5-4-4">

<strong>Theorem 5.4.4</strong>

With the textbook implementation, where the value can go negative and $-k$ means $k$ blocked processes, every `wait` subtracts one and every `signal` adds one, in any order:

$$
S_{\text{final}} = S_{\text{initial}} - \#\text{waits} + \#\text{signals}.
$$

If the final value is $\ge0$, nobody is blocked; if it is $-k$, $k$ processes are blocked.

</div>

```python {filename="sem-arith.py"}
# Counting-semaphore arithmetic. With the textbook implementation (the value
# may go negative; -k means k processes are blocked) every wait subtracts 1
# and every signal adds 1, in any order:  final = initial - waits + signals.
import random

def run(initial, ops):
    s, blocked = initial, 0
    for op in ops:
        if op == 'W':
            s -= 1
            if s < 0: blocked += 1
        else:
            s += 1
            if s <= 0: blocked -= 1           # wakes one blocked process
    return s, blocked

random.seed(1)
for initial, w, v in ((9, 10, 7), (7, 20, 18), (3, 8, 2), (0, 5, 5)):
    finals = set()
    for _ in range(2000):                     # many random orders
        ops = ['W'] * w + ['V'] * v
        random.shuffle(ops)
        finals.add(run(initial, ops))
    (s, blocked), = finals                    # the same for every order
    print(f"initial {initial:>2}, {w:>2} waits, {v:>2} signals -> final {s:>3}"
          f" ({blocked} blocked), formula {initial - w + v:>3}")

# Solve the two OA shapes for the unknown:
print("initial = final + waits - signals: 6 + 10 - 7 =", 6 + 10 - 7)
print("signals = final - initial + waits: 5 - 7 + 20 =", 5 - 7 + 20)
```

```text {filename="Output (Python 3.11)"}
initial  9, 10 waits,  7 signals -> final   6 (0 blocked), formula   6
initial  7, 20 waits, 18 signals -> final   5 (0 blocked), formula   5
initial  3,  8 waits,  2 signals -> final  -3 (3 blocked), formula  -3
initial  0,  5 waits,  5 signals -> final   0 (0 blocked), formula   0
initial = final + waits - signals: 6 + 10 - 7 = 9
signals = final - initial + waits: 5 - 7 + 20 = 18
```

The simulator shuffles the operations 2000 times and gets the same final value every time. (With the “value never below 0” implementation, the formula counts <em>completed</em> waits; blocked ones have not decremented yet.)

<div class="nb nb-moral">

Spin when the wait is shorter than a context switch, sleep otherwise; use mutexes for exclusion, semaphores for counting and signalling, condition variables in a `while`.

</div>

## 5.5 Every interleaving: “which values can $x$ take?” {#sec-os-interleave}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> `x = 10`; one thread does `x = x + 5`, the other `x = x * 2`. Four answers are possible.</em>

</div>

Small puzzles are solved by enumerating interleavings of the machine-level steps. The explorer below does it exhaustively (depth-first search over all states, memoised), with semaphores, and reports deadlocks:

```python {filename="interleave.py, lines 9–47",linenos=table,linenostart=9}
def explore(threads, mem, sems=None, observe=None):
    sems = dict(sems or {})
    keys, skeys = sorted(mem), sorted(sems)
    start = (tuple(0 for _ in threads), tuple(() for _ in threads),
             tuple(mem[k] for k in keys), tuple(sems[k] for k in skeys), '')
    seen, stack, finals, deadlock = {start}, [start], set(), None
    while stack:
        pcs, regs, m, s, out = stack.pop()
        moved = False
        for i, prog in enumerate(threads):
            if pcs[i] == len(prog):
                continue
            ins, R = prog[pcs[i]], dict(regs[i])
            M, S, o = dict(zip(keys, m)), dict(zip(skeys, s)), out
            op = ins[0]
            if op == 'P':
                if S[ins[1]] == 0:
                    continue                      # blocked
                S[ins[1]] -= 1
            elif op == 'V':  S[ins[1]] += 1
            elif op == 'ld': R[ins[1]] = M[ins[2]]
            elif op == 'st': M[ins[1]] = R[ins[2]]
            elif op == 'add': R[ins[1]] = R.get(ins[1], 0) + ins[2]
            elif op == 'mul': R[ins[1]] = R.get(ins[1], 0) * ins[2]
            elif op == 'out': o += ins[1]
            moved = True
            nregs = list(regs); nregs[i] = tuple(sorted(R.items()))
            npcs = list(pcs); npcs[i] += 1
            nxt = (tuple(npcs), tuple(nregs), tuple(M[k] for k in keys),
                   tuple(S[k] for k in skeys), o)
            if nxt not in seen:
                seen.add(nxt); stack.append(nxt)
        if not moved:
            if all(pcs[i] == len(p) for i, p in enumerate(threads)):
                finals.add(observe(dict(zip(keys, m)), out) if observe else
                           tuple(m))
            else:
                deadlock = deadlock or (pcs, dict(zip(skeys, s)))
    return finals, deadlock, len(seen)
```

```text {filename="Output (Python 3.11)"}
1. x = 0; T1: x++  ||  T2: x++
   final x in [1, 2]   (22 states)
2. x = 0; each of two threads does x++ five times
   final x in [2, 3, 4, 5, 6, 7, 8, 9, 10]   (4715 states)
3. x = 10; T1: x = x + 5  ||  T2: x = x * 2
   final x in [15, 20, 25, 30]
4. the same, each update between P(s) and V(s), s = 1
   final x in [25, 30]
5. store buffering: x = y = 0; T1: x = 1; a = y  ||  T2: y = 1; b = x
   (a, b) in [(0, 1), (1, 0), (1, 1)]   -- (0, 0) is impossible here
6. a = b = 0; T1: print A; V(a); P(b); print C  ||  T2: P(a); print B; V(b); print D
   outputs: ['ABCD', 'ABDC']
7. 4 dining philosophers, all pick left first: deadlock reachable: yes, e.g. every one at pc (1, 1, 1, 1)
7. 4 dining philosophers, last picks right first: deadlock reachable: no
```

<div class="nb nb-example nb-block" id="example-5-5-1">

<strong>Example 5.5.1</strong> (Reading the results)

Three observations:

- Two threads each doing `x++` five times can end with $x=2$: T1 loads $0$; T2 runs four complete increments; T1 stores $1$; T2 loads $1$; T1 runs its remaining four increments; T2 stores $2$. In general, with $k\ge1$ increments each, any value from $2$ to $2k$ is reachable.
- `x = x + 5` against `x = x * 2` from $10$: $25$ and $30$ are the two serial orders; $15$ and $20$ are lost updates (one store overwrites the other). With a semaphore around each, only the serial results remain.
- In item 6, B is always printed after A and C after B (the semaphores force it), but C and D race.

</div>

## 5.6 The classical problems {#sec-os-classical}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> a bounded buffer between a producer and a consumer.</em>

</div>

### 5.6.i Producer–consumer (bounded buffer) {#s5-6-i}

Semaphores `empty` $=n$ (free slots), `full` $=0$ (items), `mutex` $=1$:

```c {filename="prodcons.c, lines 12–35",linenos=table,linenostart=12}

static void *producer(void *arg) {
    int base = *(int *)arg;
    for (int i = 1; i <= ITEMS; i++) {
        sem_wait(&empty);                       // wait for a free slot
        sem_wait(&mutex);
        buf[in] = base + i; in = (in + 1) % SLOTS;
        if (++occupied > max_occupied) max_occupied = occupied;
        sem_post(&mutex);
        sem_post(&full);                        // one more item
    }
    return NULL;
}
static void *consumer(void *arg) {
    for (int i = 0; i < ITEMS; i++) {
        sem_wait(&full);                        // wait for an item
        sem_wait(&mutex);
        consumed_sum += buf[out]; out = (out + 1) % SLOTS; occupied--;
        sem_post(&mutex);
        sem_post(&empty);                       // one more free slot
    }
    return arg;
}
```

```text {filename="One possible output (gcc 13.3, glibc 2.39, Linux 6.18 x86-64)"}
sum consumed = 1100010000 (expected 1100010000)
never more than 4 items in a 4-slot buffer: yes
final semaphores: empty = 4, full = 0
```

<div class="nb nb-remark" id="remark-5-6-1">

<strong>Remark 5.6.1</strong> (Swap the two waits and it deadlocks) — If the producer does `wait(mutex)` before `wait(empty)` and the buffer is full, it sleeps holding the mutex; the consumer then blocks on `wait(mutex)` and can never free a slot. The counting wait must come first, the mutex wait second. The order of the two `signal`s does not matter.

</div>

### 5.6.ii Readers–writers {#s5-6-ii}

Many readers may read together; a writer needs exclusive access.

```c
/* First readers-writers problem: readers have priority. */
semaphore rw = 1, mutex = 1;  int readers = 0;
writer: wait(rw);  write();  signal(rw);
reader: wait(mutex);
        if (++readers == 1) wait(rw);     /* first reader locks out writers */
        signal(mutex);
        read();
        wait(mutex);
        if (--readers == 0) signal(rw);   /* last reader lets them in */
        signal(mutex);
```

As long as one reader is inside, new readers walk in, so a steady stream of readers starves writers. The <strong>second readers-writers problem</strong> gives writers priority: a writer that arrives blocks new readers. One more semaphore does it:

```c
/* Writers have priority (readers may starve). */
semaphore rw = 1, mutex = 1, wmutex = 1, readtry = 1;
int readers = 0, writers = 0;
writer: wait(wmutex);
        if (++writers == 1) wait(readtry);   /* first writer bars new readers */
        signal(wmutex);
        wait(rw); write(); signal(rw);
        wait(wmutex);
        if (--writers == 0) signal(readtry);
        signal(wmutex);
reader: wait(readtry); wait(mutex);
        if (++readers == 1) wait(rw);
        signal(mutex); signal(readtry);
        read();
        wait(mutex);
        if (--readers == 0) signal(rw);
        signal(mutex);
```

Fair (FIFO) versions put everybody through one turnstile semaphore first. In practice: `pthread_rwlock_t`, whose preference is implementation-defined (glibc prefers readers by default).

### 5.6.iii Dining philosophers {#s5-6-iii}

Five philosophers, five chopsticks, each needs both neighbours’ chopsticks. “Everyone picks up the left one first” deadlocks when all do it at once: the explorer found it for four philosophers (item 7 above: each holds one chopstick and waits at its second `wait`). Fixes, each breaking one deadlock condition ([Chapter 6](../06-deadlock/)):

- <strong>Ordering</strong>: one philosopher (or all odd ones) picks right first, breaking the cycle; the explorer confirms no deadlock is reachable;
- <strong>At most $n-1$ at the table</strong> (a counting semaphore initialised to $n-1$): one of them always gets both chopsticks;
- <strong>Both or none</strong>: pick up both chopsticks inside one critical section (a monitor with a state per philosopher; Silberschatz’s solution). It is deadlock-free but a philosopher can still starve.

### 5.6.iv Sleeping barber {#s5-6-iv}

One barber, one chair, $n$ waiting chairs. If there are no customers the barber sleeps; an arriving customer wakes him, waits in a free chair, or leaves if all are taken.

```c
semaphore customers = 0, barber = 0, mutex = 1;  int waiting = 0;
barber:   while (1) {
              wait(customers);              /* sleep until someone arrives */
              wait(mutex); waiting--; signal(barber); signal(mutex);
              cut_hair();
          }
customer: wait(mutex);
          if (waiting < CHAIRS) {
              waiting++; signal(customers); signal(mutex);
              wait(barber); get_haircut();
          } else signal(mutex);             /* shop full: leave */
```

The `waiting` counter is needed because a semaphore’s value cannot be read reliably; the mutex makes “check and take a chair” one atomic step. The pattern (a bounded queue of requests served by a pool of workers) is a thread pool.

## 5.7 Priority inversion {#sec-os-inversion}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> Mars Pathfinder (1997): the spacecraft kept resetting itself on Mars.</em>

</div>

<div class="nb nb-definition" id="definition-5-7-1">

<strong>Definition 5.7.1</strong>. <strong>Priority inversion</strong>: a high-priority task H waits for a lock held by a low-priority task L, and a medium-priority task M, which needs no lock, preempts L. H now effectively waits for M, for an unbounded time. <strong>Priority inheritance</strong>: while L holds a lock that H is waiting for, L runs at H’s priority, so M cannot preempt it; L drops back when it releases the lock. (H’s priority does not change.) <strong>Priority ceiling</strong>: every lock has the priority of its highest user, and a task holding it runs at that priority from the start.

</div>

The simulator `inversion.py` runs three tasks on one CPU with preemptive fixed priorities. L (low) arrives at 0, runs 1 unit, locks R, needs 3 units inside, unlocks, runs 1 more. H (high) arrives at 2, runs 1 unit, then needs R for 1 unit, then runs 1 more. M (medium) arrives at 3 and computes for 6 units without any lock. One letter per time unit:

```text {filename="Output (Python 3.11)"}
time               01234567890123
no inheritance:    LLHMMMMMMLLHHL   H done at 13, M at 9, L at 14
with inheritance:  LLHLLHHMMMMMML   H done at 7, M at 13, L at 14
```

Without inheritance H, the most urgent task, finishes at 13, after M (at 9). With inheritance L finishes its critical section at once (positions 3–4), H finishes at 7, and M is delayed instead, which is correct since M is less urgent.

<div class="nb nb-remark" id="remark-5-7-2">

<strong>Remark 5.7.2</strong> (Mars Pathfinder) — On the VxWorks RTOS of the lander, a high-priority bus-management task shared a mutex with a low-priority meteorological-data task; a long-running medium-priority communications task preempted the low one while it held the mutex. The high task missed its deadline, a watchdog noticed, and the system reset itself, repeatedly. The mutex had been created with priority inheritance turned off; engineers turned it on by uploading a change, and the resets stopped.

</div>

## 5.8 Lock-free programming and the ABA problem {#sec-os-aba}

<div class="nb-proto">

<em><span>Prototypical example for this section:</span> a lock-free stack whose `pop` succeeds with a pointer to a node that was freed and reallocated in between.</em>

</div>

<div class="nb nb-definition" id="definition-5-8-1">

<strong>Definition 5.8.1</strong>. A <strong>lock-free</strong> algorithm guarantees that some thread always makes progress, even if others are suspended (no locks, typically a CAS retry loop). <strong>Wait-free</strong> guarantees that every thread finishes in a bounded number of its own steps. Blocking algorithms (locks) guarantee neither: a preempted lock holder stops everyone.

</div>

A lock-free stack pops with `do { old = top; next = old->next; } while (!CAS(&top, old, next));`.

<div class="nb nb-example nb-block" id="example-5-8-2">

<strong>Example 5.8.2</strong> (ABA)

Stack $A \to B \to C$. Thread 1 reads `old = A`, `next = B` and is preempted. Thread 2 pops $A$, pops $B$ (frees it), pushes $A$ back: the stack is $A \to C$. Thread 1 resumes; `top` is $A$ again, so its CAS succeeds and sets `top = B`, a freed node. CAS compares values, and the value went $A \to C \to A$ (hence “ABA”): it cannot tell that the stack changed.

</div>

Fixes: a version counter next to the pointer, compared with a double-width CAS (`cmpxchg16b`) and incremented on every update; LL/SC, which fails on <em>any</em> intervening write; or safe memory reclamation (hazard pointers, epoch-based reclamation, RCU), which makes sure a node is not freed and reused while some thread may still hold it. Garbage collected languages avoid the reuse half of the problem for free.

<div class="nb nb-moral">

CAS checks that a value is the same, not that nothing happened; lock-free code must version its pointers or delay reuse.

</div>
