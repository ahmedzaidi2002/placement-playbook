---
title: "15 · A few harder problems to think about"
linkTitle: "15 A few harder problems to think about"
weight: 15
math: true
---
These problems are in the shapes that online assessments use: numericals, “which of these statements are true (more than one may be)”, and “what does this print”. The C programs were compiled and run with gcc 13.3, glibc 2.39, Linux 6.18 x86-64; every numerical answer was computed by `prob-answers.py` with the simulators of the earlier chapters. Hints and solutions are at the back of the book (the <em>Hint</em> drop-down under each problem, the <em>Solution</em> drop-down under each problem); the raw verification output is in the last section of this chapter. Chilis mark the harder ones.

## 15.1 Processes and signals {#sec-os-prob-proc}

<div class="nb nb-problem nb-block" id="problem-15-1">

<strong>Problem 15.1</strong> 🌶 (Dashes and pluses)

How many `-` and how many `+` does this program print, and on how many lines, (a) on a terminal, (b) into a pipe?

```c {filename="prob-buffer.c"}
// flags: -D_GNU_SOURCE
// norun (prob-buffer.sh runs it on a terminal and into a pipe)
#include <stdio.h>
#include <unistd.h>
#include <sys/wait.h>

int main(void) {
    printf("-");
    if (fork() == 0) {
        printf("+");
        fork();
    }
    printf("\n");
    while (wait(NULL) > 0) {}
    return 0;
}
```

<details class="nb-hint">
<summary>Hint</summary>

Is there a newline in the stdio buffer at the moment of the first `fork`?

</details>

<details class="nb-sol">
<summary>Solution</summary>

The same in both cases: three lines, `-`, `-+`, `-+`; three dashes and two pluses. The `"-"` has no newline, so it is still in the buffer when `fork` copies the process, even on a line-buffered terminal. The child adds `+` and forks again, so two processes hold `"-+"`. Each of the three processes flushes its own copy at the `"\n"`. Counting calls instead of buffers gives the wrong answer “one dash”.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-15-2">

<strong>Problem 15.2</strong> 🌶🌶 (A loop with a break)

How many lines does this program print?

```c {filename="prob-fork-loop.c"}
// flags: -D_GNU_SOURCE
// norun (prob-buffer.sh counts its lines)
#include <stdio.h>
#include <unistd.h>
#include <sys/wait.h>

int main(void) {
    setvbuf(stdout, NULL, _IONBF, 0);   // unbuffered: one write per printf
    for (int i = 0; i < 4; i++) {
        if (i % 2 == 0)
            fork();
        else if (fork() == 0)
            break;
    }
    printf("x\n");
    while (wait(NULL) > 0) {}
    return 0;
}
```

<details class="nb-hint">
<summary>Hint</summary>

Track how many processes are still looping after each iteration, and how many have left the loop.

</details>

<details class="nb-sol">
<summary>Solution</summary>

10\. After $i=0$: 2 processes looping. At $i=1$ each creates a child that breaks: 2 looping, 2 out. At $i=2$ the looping ones double: 4 looping, 2 out. At $i=3$ each of the 4 creates a child that breaks: 4 looping, 6 out. All $10$ print once.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-15-3">

<strong>Problem 15.3</strong> (Short-circuit forks)

How many times does `1` appear?

```c
if (fork() || fork())
    fork();
printf("1\n");
```

<details class="nb-hint">
<summary>Hint</summary>

In the parent the first `fork` is nonzero, so the second is skipped.

</details>

<details class="nb-sol">
<summary>Solution</summary>

5\. P creates A. In P the condition is already true (first fork nonzero), so P creates B. In A the first fork returned 0, so A calls the second fork, creating C; in A that fork is nonzero, so A creates D; in C it is 0, so C skips the body. Processes P, A, B, C, D: five lines (`prob-or.c`).

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-15-4">

<strong>Problem 15.4</strong> (What `system()` does)

Which statements are true for glibc’s `system(cmd)` on Linux? (A) It creates exactly one child process itself. (B) `cmd` is executed by `/bin/sh -c`. (C) `system("cd /tmp")` changes the caller’s current directory. (D) It returns before `cmd` finishes. (E) The total number of processes created can exceed one.

<details class="nb-hint">
<summary>Hint</summary>

What does the shell do with an external command?

</details>

<details class="nb-sol">
<summary>Solution</summary>

A, B, E. `system` makes one child (a vfork-style `clone` via `posix_spawn`) running `sh -c cmd` and waits for it, so D is false. The shell may create more processes: dash forks once per external command ([Section 2.4](../02-processes/#sec-os-fork)). C is false: `cd` runs in the child shell, and a child cannot change its parent’s directory.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-15-5">

<strong>Problem 15.5</strong> (Zombies)

Which are true? (A) A zombie is removed by sending it `SIGKILL`. (B) A zombie is removed when its parent calls `wait`. (C) A process becomes a zombie when it terminates before its parent has waited for it. (D) A zombie still holds its memory pages. (E) If the parent exits without waiting, its zombie children are reaped by `init`.

<details class="nb-hint">
<summary>Hint</summary>

What exactly is left of a zombie?

</details>

<details class="nb-sol">
<summary>Solution</summary>

B, C, E. Only the process-table entry (PID, exit status, usage) remains; memory and files are already freed (D false). It is already dead, so `SIGKILL` has no effect (A false; `zombie.c` shows the state stays `Z`).

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-15-6">

<strong>Problem 15.6</strong> (Ending a process)

Which signals terminate a process by default? Which of those can the process catch? `SIGTERM`, `SIGKILL`, `SIGINT`, `SIGSTOP`, `SIGCHLD`, `SIGHUP`. Which two would you use, in which order, to stop a server?

<details class="nb-hint">
<summary>Hint</summary>

One of them only pauses; one is ignored by default.

</details>

<details class="nb-sol">
<summary>Solution</summary>

Terminate by default: `SIGTERM`, `SIGKILL`, `SIGINT`, `SIGHUP` (`SIGSTOP` stops, `SIGCHLD` is ignored). All can be caught except `SIGKILL` (and `SIGSTOP`). Send `SIGTERM` first so the server can clean up, then `SIGKILL` if it has not exited after a timeout.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-15-7">

<strong>Problem 15.7</strong> (What the OS keeps)

Which of these are kept in the process control block? (A) saved program counter and registers; (B) the page-table root; (C) the list of open files; (D) the contents of the process’s heap; (E) scheduling priority and state.

<details class="nb-hint">
<summary>Hint</summary>

The PCB describes the process; it does not contain its memory.

</details>

<details class="nb-sol">
<summary>Solution</summary>

A, B, C, E. The heap lives in the process’s own pages; the PCB only points to the memory map.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-15-8">

<strong>Problem 15.8</strong> (Cheaper context switches)

Which of these reduce the time of a context switch? (A) more register sets in the CPU; (B) switching between threads of one process instead of between processes; (C) a TLB tagged with address-space identifiers; (D) a longer time quantum; (E) less memory to swap when the incoming process must be brought in.

<details class="nb-hint">
<summary>Hint</summary>

Separate the cost of one switch from the number of switches.

</details>

<details class="nb-sol">
<summary>Solution</summary>

A, B, C, E. A longer quantum reduces how <em>often</em> the switch happens, not how long one switch takes ([Section 2.3](../02-processes/#sec-os-ctxswitch)).

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-15-9">

<strong>Problem 15.9</strong> (Transitions)

In the five-state model, which transitions cannot happen? ready $\to$ running, running $\to$ ready, blocked $\to$ running, ready $\to$ blocked, running $\to$ blocked, blocked $\to$ ready, new $\to$ running.

<details class="nb-hint">
<summary>Hint</summary>

Who decides that a process runs?

</details>

<details class="nb-sol">
<summary>Solution</summary>

blocked $\to$ running, ready $\to$ blocked and new $\to$ running. Only the dispatcher puts a process on the CPU, and only from ready; only a running process can block itself.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-15-10">

<strong>Problem 15.10</strong> (Exit codes)

A child calls `exit(300)`; a second child calls `exit(-2)`. What does the parent read with `WEXITSTATUS`?

<details class="nb-hint">
<summary>Hint</summary>

How many bits of the status reach the parent?

</details>

<details class="nb-sol">
<summary>Solution</summary>

$44$ and $254$: only the low 8 bits survive ($300 \bmod 256 = 44$, $-2 \bmod 256 = 254$), as `wait-status.c` showed for $256 \to 0$.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-15-11">

<strong>Problem 15.11</strong> 🌶🌶 (Shared offsets)

What does this program print?

```c {filename="prob-fd.c"}
// flags: -D_GNU_SOURCE
// norun (prob-buffer.sh runs it)
#include <stdio.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/wait.h>

int main(void) {
    const char *f = "/tmp/os-book-prob.txt";
    int a = open(f, O_WRONLY | O_CREAT | O_TRUNC, 0644);
    write(a, "12345", 5);
    if (fork() == 0) {
        int b = open(f, O_WRONLY);
        write(b, "ab", 2);
        write(a, "XY", 2);
        _exit(0);
    }
    wait(NULL);
    write(a, "!", 1);
    close(a);
    char buf[32] = {0};
    int r = open(f, O_RDONLY);
    read(r, buf, sizeof buf - 1);
    printf("%s\n", buf);
    unlink(f);
    return 0;
}
```

<details class="nb-hint">
<summary>Hint</summary>

`a` is shared with the child through `fork`; `b` is a separate `open`.

</details>

<details class="nb-sol">
<summary>Solution</summary>

`ab345XY!`. After `"12345"` the shared offset of `a` is 5. The child’s own `open` has offset 0 and overwrites `12` with `ab`. The child’s write through `a` goes to offset 5 (`XY`) and moves the <em>shared</em> offset to 7, so the parent’s `"!"` lands at 7.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-15-12">

<strong>Problem 15.12</strong> (IPC statements)

Which are true? (A) `read` on an empty pipe returns 0 while some write end is still open. (B) Writing to a pipe whose read ends are all closed raises `SIGPIPE`. (C) An anonymous pipe can connect two unrelated processes. (D) After set-up, shared memory needs no system call per access. (E) A POSIX message queue preserves message boundaries.

<details class="nb-hint">
<summary>Hint</summary>

When exactly does `read` return 0?

</details>

<details class="nb-sol">
<summary>Solution</summary>

B, D, E. A: `read` blocks while a writer exists and returns 0 only when the pipe is empty and all write ends are closed. C: anonymous pipes are inherited through `fork`; unrelated processes need a FIFO or a socket.

</details>

</div>

## 15.2 Threads {#sec-os-prob-threads}

<div class="nb nb-problem nb-block" id="problem-15-13">

<strong>Problem 15.13</strong> (Shared or private)

For threads of one process, which are shared? (A) global variables (B) the stack (C) the heap (D) open file descriptors (E) the program counter (F) signal handlers (G) `errno`.

<details class="nb-hint">
<summary>Hint</summary>

What does each thread need to run independently?

</details>

<details class="nb-sol">
<summary>Solution</summary>

A, C, D, F. Each thread has its own stack, registers (including the PC) and thread-local `errno`.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-15-14">

<strong>Problem 15.14</strong> (User-level threads)

Which are true of a pure user-level thread library (many-to-one)? (A) Thread switches need no system call. (B) Two threads can run in parallel on two cores. (C) A blocking `read` in one thread blocks all of them. (D) The kernel schedules each thread separately. (E) The application can choose its own scheduling policy.

<details class="nb-hint">
<summary>Hint</summary>

The kernel sees one schedulable entity.

</details>

<details class="nb-sol">
<summary>Solution</summary>

A, C, E. B and D need kernel threads.

</details>

</div>

## 15.3 CPU scheduling {#sec-os-prob-sched}

<div class="nb nb-problem nb-block" id="problem-15-15">

<strong>Problem 15.15</strong> (Release times and an idle CPU)

Processes A, B, C, D have release (arrival) times $0, 1, 10, 11$ and bursts $3, 5, 2, 4$. Under FCFS, give each completion time and the average turnaround time.

<details class="nb-hint">
<summary>Hint</summary>

The CPU is idle between B’s completion and C’s arrival.

</details>

<details class="nb-sol">
<summary>Solution</summary>

A 3, B 8, CPU idle 8–10, C 12, D 16. Turnarounds $3, 7, 2, 5$, average $4.25$. “Release time” is the arrival time.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-15-16">

<strong>Problem 15.16</strong> 🌶 (SRTF)

Arrivals and bursts: P1 (0, 9), P2 (1, 4), P3 (2, 2), P4 (3, 5), P5 (5, 1). Using SRTF, find the average waiting time and P1’s waiting time.

<details class="nb-hint">
<summary>Hint</summary>

Re-decide at every arrival; compare with what is <em>left</em> of the running process.

</details>

<details class="nb-sol">
<summary>Solution</summary>

Gantt: P1 0–1, P2 1–2, P3 2–4, P2 4–5, P5 5–6, P2 6–8, P4 8–13, P1 13–21. Average waiting time $4.00$ (average turnaround $8.20$); P1 waits $21-0-9=12$.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-15-17">

<strong>Problem 15.17</strong> 🌶 (Round robin, $q=3$)

P1 (0, 8), P2 (2, 5), P3 (4, 2), P4 (6, 4); quantum 3; a process arriving when a quantum expires is queued before the preempted one. Give the completion times, the average waiting time and the average response time. What happens with $q=8$?

<details class="nb-hint">
<summary>Hint</summary>

Write the ready queue after every event.

</details>

<details class="nb-sol">
<summary>Solution</summary>

Gantt: P1 0–3, P2 3–6, P1 6–9, P3 9–11, P4 11–14, P2 14–16, P1 16–18, P4 18–19. Completion P1 18, P2 16, P3 11, P4 19; average waiting time $8.25$, average response time $2.75$. With $q=8$ no process is ever preempted (8 is the longest burst) and the schedule is exactly FCFS.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-15-18">

<strong>Problem 15.18</strong> (HRRN)

At $t=10$ the CPU becomes free. Waiting: J1 (arrived 2, burst 6), J2 (arrived 5, burst 2), J3 (arrived 6, burst 4). Which runs next under HRRN?

<details class="nb-hint">
<summary>Hint</summary>

Ratio $=(w+s)/s$.

</details>

<details class="nb-sol">
<summary>Solution</summary>

J2: ratios J1 $(8+6)/6=2.33$, J2 $(5+2)/2=3.50$, J3 $(4+4)/4=2.00$.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-15-19">

<strong>Problem 15.19</strong> (Who starves)

Which can starve a process? FCFS, SJF, SRTF, round robin, non-preemptive priority without aging, HRRN, multilevel queue with fixed priorities.

<details class="nb-hint">
<summary>Hint</summary>

Look for a rule that can prefer newcomers forever.

</details>

<details class="nb-sol">
<summary>Solution</summary>

SJF, SRTF, priority without aging, fixed-priority multilevel queue. FCFS, RR and HRRN cannot starve.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-15-20">

<strong>Problem 15.20</strong> (Scheduling statements)

Which are correct? (I) SPN’s throughput is higher than FCFS’s. (II) SRT gives the minimum average waiting time among all schedulers. (III) HRRN is preemptive. (IV) Round robin with an infinite quantum behaves like FCFS. (V) FCFS has the lowest overhead of the classic algorithms.

<details class="nb-hint">
<summary>Hint</summary>

Stallings’ comparison table rates throughput and overhead.

</details>

<details class="nb-sol">
<summary>Solution</summary>

I, II, IV, V. HRRN is non-preemptive. (For II, assume known burst times.)

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-15-21">

<strong>Problem 15.21</strong> 🌶🌶 (Rate-monotonic or not)

Set 1: $(C,T) = (1,3), (1,5), (1,9)$. Set 2: $(2,4), (3,7)$. For each, does the Liu–Layland test prove RMS schedulability? Is the set schedulable by RMS? By EDF?

<details class="nb-hint">
<summary>Hint</summary>

The bound is sufficient, not necessary; simulate over the hyperperiod when it fails.

</details>

<details class="nb-sol">
<summary>Solution</summary>

Set 1: $U=0.6444\le0.7798$, so yes by the test; schedulable by both. Set 2: $U=0.9286>0.8284$, so the test says nothing; simulating RMS over the hyperperiod 28 shows no deadline miss, so it is RMS-schedulable anyway; EDF works since $U\le1$.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-15-22">

<strong>Problem 15.22</strong> (Nice values)

Three CPU-bound tasks on one CPU have nice values $0$, $2$ and $-3$ (weights 1024, 655, 1991). What share does each get under the fair scheduler?

<details class="nb-hint">
<summary>Hint</summary>

Share $=w_i/\sum w$.

</details>

<details class="nb-sol">
<summary>Solution</summary>

$27.9\%$, $17.8\%$, $54.3\%$.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-15-23">

<strong>Problem 15.23</strong> (Predicting the burst)

With $\alpha=0.25$, $\tau_0=12$, and actual bursts $8, 16, 4$, what is the prediction for the fourth burst?

<details class="nb-hint">
<summary>Hint</summary>

$\tau_{n+1}=\alpha t_n+(1-\alpha)\tau_n$, three times.

</details>

<details class="nb-sol">
<summary>Solution</summary>

$11$, then $12.25$, then $10.1875$.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-15-24">

<strong>Problem 15.24</strong> (Switch overhead)

Quantum 20 ms, context switch 2 ms. What fraction of CPU time is useful if every process uses its full quantum? If every process blocks after 6 ms?

<details class="nb-hint">
<summary>Hint</summary>

One switch per scheduling decision.

</details>

<details class="nb-sol">
<summary>Solution</summary>

$20/22 = 90.9\%$; $6/8 = 75\%$.

</details>

</div>

## 15.4 Synchronization {#sec-os-prob-sync}

<div class="nb nb-problem nb-block" id="problem-15-25">

<strong>Problem 15.25</strong> (Initial value)

A counting semaphore ends at $4$ after $12$ `wait` and $5$ `signal` operations. What was its initial value?

<details class="nb-hint">
<summary>Hint</summary>

Each wait subtracts one, each signal adds one.

</details>

<details class="nb-sol">
<summary>Solution</summary>

$4+12-5=11$.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-15-26">

<strong>Problem 15.26</strong> (Number of signals)

A counting semaphore starts at $3$. After $15$ waits and some signals its value is $-2$. How many signals were performed, and how many processes are blocked?

<details class="nb-hint">
<summary>Hint</summary>

A negative value counts blocked processes.

</details>

<details class="nb-sol">
<summary>Solution</summary>

$-2-3+15=10$ signals; two processes are blocked.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-15-27">

<strong>Problem 15.27</strong> (Hardware or software)

Which are hardware-based solutions to the critical-section problem? (I) `test_and_set` (II) `compare_and_swap` (III) Peterson’s solution (IV) Lamport’s bakery (V) disabling interrupts on a uniprocessor.

<details class="nb-hint">
<summary>Hint</summary>

Which need special instructions or privileged hardware control?

</details>

<details class="nb-sol">
<summary>Solution</summary>

I, II and V. Peterson and the bakery algorithm use ordinary loads and stores (software).

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-15-28">

<strong>Problem 15.28</strong> (Synchronisation in an RTOS)

In an RTOS, an interrupt handler must tell a task that data has arrived, and two tasks of different priorities share a buffer. Which primitives fit? (A) a binary semaphore given by the ISR and taken by the task; (B) a mutex with priority inheritance for the buffer; (C) a mutex taken by the ISR; (D) disabling the scheduler for the whole time the buffer is used; (E) an event flag set by the ISR.

<details class="nb-hint">
<summary>Hint</summary>

Separate “must happen in order” from “must not happen together”. Can an ISR block?

</details>

<details class="nb-sol">
<summary>Solution</summary>

A, B, E. Signalling (order) uses a semaphore or an event flag that the ISR posts; mutual exclusion between tasks uses a mutex, with priority inheritance against inversion. An ISR must not block, so it cannot take a mutex (C). D works only for very short sections and hurts every other task’s latency.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-15-29">

<strong>Problem 15.29</strong> (Possible values)

`x = 5`. T1 executes `x = x * 3`, T2 executes `x = x + 4`, each as load, compute, store. Which final values are possible?

<details class="nb-hint">
<summary>Hint</summary>

Two serial orders, plus each lost update.

</details>

<details class="nb-sol">
<summary>Solution</summary>

$9, 15, 19, 27$: serial orders give $27$ ($(5+4)\times3$) and $19$ ($5\times3+4$); lost updates give $15$ (T2’s store overwritten) and $9$ (T1’s overwritten).

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-15-30">

<strong>Problem 15.30</strong> (Orders)

Semaphores `s` $=0$, `t` $=0$. T1: `print A; wait(s); print B; signal(t)`. T2: `print C; signal(s); wait(t); print D`. Which outputs are possible? Can it deadlock?

<details class="nb-hint">
<summary>Hint</summary>

B needs C’s signal first; D needs B.

</details>

<details class="nb-sol">
<summary>Solution</summary>

`ACBD` and `CABD`; no deadlock. A and C race; B comes after both; D after B.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-15-31">

<strong>Problem 15.31</strong> 🌶🌶 (Three incrementers)

`x = 0`; three threads each execute `x++` twice (load, add, store). What are the minimum and maximum final values?

<details class="nb-hint">
<summary>Hint</summary>

To lose almost everything, one thread must load early and store last, twice.

</details>

<details class="nb-sol">
<summary>Solution</summary>

Minimum $2$, maximum $6$, and every value in between is reachable (exhaustive search, `prob-answers.py`). Schedule for 2: T1 loads 0; T2 and T3 run all their increments ($x=4$); T1 stores 1, wiping them out; T1’s second increment makes $x=2$. It cannot go lower: the last store comes from some thread’s second increment, which loaded a value written after that thread’s own first store, so at least 1.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-15-32">

<strong>Problem 15.32</strong> (A flawed lock)

Two processes use `flag[i] = 1; while (flag[j]) ; ` CS `flag[i] = 0;`. Which requirements hold?

<details class="nb-hint">
<summary>Hint</summary>

What if both set their flags at the same time?

</details>

<details class="nb-sol">
<summary>Solution</summary>

Mutual exclusion holds. Progress fails: if both set their flags before either tests, both spin forever (deadlock). Bounded waiting is moot once progress fails.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-15-33">

<strong>Problem 15.33</strong> (Swapped waits)

A producer executes `wait(mutex); wait(empty);` … `signal(mutex); signal(full);`. Describe a run that deadlocks.

<details class="nb-hint">
<summary>Hint</summary>

Start with a full buffer.

</details>

<details class="nb-sol">
<summary>Solution</summary>

Buffer full ($\texttt{empty}=0$). The producer takes `mutex`, then blocks on `empty` while holding it. The consumer blocks on `wait(mutex)` and can never free a slot. Hold and wait plus circular wait: deadlock.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-15-34">

<strong>Problem 15.34</strong> (Inversion)

Which are true? (A) Priority inversion needs at least three priority levels to be unbounded. (B) Under priority inheritance, the high-priority task’s priority is lowered. (C) Disabling preemption while holding the lock also bounds the inversion. (D) The Mars Pathfinder resets were fixed by enabling priority inheritance on a mutex.

<details class="nb-hint">
<summary>Hint</summary>

What does the medium task do?

</details>

<details class="nb-sol">
<summary>Solution</summary>

A, C, D. B is false: the <em>low</em> task temporarily inherits the high priority.

</details>

</div>

## 15.5 Deadlocks {#sec-os-prob-deadlock}

<div class="nb nb-problem nb-block" id="problem-15-35">

<strong>Problem 15.35</strong> (Necessary or sufficient)

A: “Circular wait is necessary for deadlock.” B: “Circular wait is sufficient for deadlock.” Which are true?

<details class="nb-hint">
<summary>Hint</summary>

Think of a cycle through resources with several instances.

</details>

<details class="nb-sol">
<summary>Solution</summary>

Only A. With multiple instances a cycle can exist without deadlock ([Section 6.1](../06-deadlock/#sec-os-deadlock-def)).

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-15-36">

<strong>Problem 15.36</strong> (Prevention)

A: “Allowing resource preemption alone prevents deadlocks.” B: “Preventing circular wait alone prevents deadlocks.” True or false?

<details class="nb-hint">
<summary>Hint</summary>

All four conditions are necessary.

</details>

<details class="nb-sol">
<summary>Solution</summary>

Both true: removing any one necessary condition makes deadlock impossible. (In practice preemption only applies to resources whose state can be saved, which is why ordering is what real code uses.)

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-15-37">

<strong>Problem 15.37</strong> 🌶🌶 (Banker’s)

Total $(9,5,7)$. Allocation P0 $(2,1,0)$, P1 $(1,1,2)$, P2 $(3,0,1)$, P3 $(0,2,1)$; Max P0 $(5,3,2)$, P1 $(2,2,4)$, P2 $(6,1,3)$, P3 $(1,4,2)$. Is the state safe? Should P1’s request $(1,0,1)$ be granted? P3’s $(1,1,0)$ (judged from the original state)?

<details class="nb-hint">
<summary>Hint</summary>

Available $=(3,1,3)$. Compute Need first.

</details>

<details class="nb-sol">
<summary>Solution</summary>

Need: P0 $(3,2,2)$, P1 $(1,1,2)$, P2 $(3,1,2)$, P3 $(1,2,1)$. Safe: $\langle P1, P2, P3, P0\rangle$. P1’s request: grant (still safe in the same order). P3’s request is available but leaves $(2,0,3)$, from which no process’s need fits: unsafe, deny.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-15-38">

<strong>Problem 15.38</strong> (Enough resources)

Five processes each need up to 4 units of one resource. What is the smallest number of units that makes deadlock impossible? With 6 units and processes needing 3 each, how many processes can run deadlock-free?

<details class="nb-hint">
<summary>Hint</summary>

$\sum(S_i-1)+1$.

</details>

<details class="nb-sol">
<summary>Solution</summary>

$5\times3+1=16$. For the second, $n\cdot2+1\le6$ gives $n\le2$.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-15-39">

<strong>Problem 15.39</strong> (Name the failure)

Classify: (a) two threads each hold one lock and wait for the other’s; (b) two threads each detect a conflict, release, back off for exactly 1 ms and retry, forever; (c) a low-priority job never runs because high-priority jobs keep arriving.

<details class="nb-hint">
<summary>Hint</summary>

Who is running in each case?

</details>

<details class="nb-sol">
<summary>Solution</summary>

(a) deadlock; (b) livelock (they keep changing state in response to each other without progress; random back-off fixes it); (c) starvation.

</details>

</div>

## 15.6 Memory management {#sec-os-prob-mem}

<div class="nb nb-problem nb-block" id="problem-15-40">

<strong>Problem 15.40</strong> (The pool)

In a C program, which region serves as the pool for dynamic memory allocation, and which statements are true? (A) `malloc` gets memory from the heap. (B) Local arrays live on the heap. (C) The heap grows with `brk` or by `mmap`. (D) Globals live in the data or bss segment.

<details class="nb-hint">
<summary>Hint</summary>

`layout.c` printed one address of each region.

</details>

<details class="nb-sol">
<summary>Solution</summary>

The heap. A, C, D are true; locals live on the stack (B false).

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-15-41">

<strong>Problem 15.41</strong> 🌶 (First fit into fixed blocks)

Fixed blocks of 110, 70, 190, 50 KB (not split). Requests 60, 85, 45, 120 KB arrive in that order and are placed by first fit. Which request fails, and what kind of fragmentation is there?

<details class="nb-hint">
<summary>Hint</summary>

Is the memory left over enough for the failing request?

</details>

<details class="nb-sol">
<summary>Solution</summary>

$60\to110$, $85\to190$, $45\to70$; 120 fails, and only the 50 KB block is free. The waste inside the allocated blocks is internal fragmentation: $50+105+25=180$ KB. It is <em>not</em> external fragmentation: the free memory (50) is less than the request.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-15-42">

<strong>Problem 15.42</strong> (Fixed partitions ratio)

Partitions of 400, 120, 250 and 300 KB; three processes of 150 KB each arrive and are placed by first fit. What is the ratio of internal to external fragmentation?

<details class="nb-hint">
<summary>Hint</summary>

Count the leftover partition that no process can use as external.

</details>

<details class="nb-sol">
<summary>Solution</summary>

$150\to400$, $150\to250$, $150\to300$ (120 is too small). Internal $250+100+150=500$; the unused 120 partition is external; ratio $500:120=25:6$.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-15-43">

<strong>Problem 15.43</strong> (Holes)

With variable partitions, after some processes end the free holes are 60, 140 and 220 KB, and a 300 KB request fails. What fragmentation is this, and what would compaction give?

<details class="nb-hint">
<summary>Hint</summary>

Total free versus largest hole.

</details>

<details class="nb-sol">
<summary>Solution</summary>

External fragmentation: 420 KB free in total, no hole of 300. Compaction makes one hole of 420.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-15-44">

<strong>Problem 15.44</strong> (Page-table size)

Virtual addresses of 34 bits, 8 KiB pages, 4 GiB of physical memory, and each PTE holds the frame number plus 3 bits (valid, dirty, protection), rounded up to whole bytes. How large is a flat page table?

<details class="nb-hint">
<summary>Hint</summary>

The frame number width comes from the physical memory.

</details>

<details class="nb-sol">
<summary>Solution</summary>

$2^{21}$ entries; frame number $32-13=19$ bits, PTE $22$ bits $\to3$ bytes; table $2^{21}\times3$ B $=6$ MiB.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-15-45">

<strong>Problem 15.45</strong> (How many levels)

48-bit virtual addresses, 16 KiB pages, 8-byte PTEs, every table exactly one page. How many levels?

<details class="nb-hint">
<summary>Hint</summary>

Bits of index per level $=\log_2(\text{page}/\text{PTE})$.

</details>

<details class="nb-sol">
<summary>Solution</summary>

Offset 14 bits, 2048 entries per table $=11$ bits per level, $\lceil34/11\rceil=4$ levels.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-15-46">

<strong>Problem 15.46</strong> 🌶 (TLB hit ratio)

TLB lookup 5 ns, memory access 80 ns, a 3-level page table. What hit ratio keeps the effective access time at or below 100 ns?

<details class="nb-hint">
<summary>Hint</summary>

$\text{EAT}=h(t+m)+(1-h)(t+4m)$.

</details>

<details class="nb-sol">
<summary>Solution</summary>

$85h+325(1-h)\le100 \Rightarrow h\ge 225/240 = 0.9375$.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-15-47">

<strong>Problem 15.47</strong> (Translate)

1 KiB pages; the page table maps page 0 to frame 5, page 1 to frame 9, page 14 to frame 2. Translate virtual address `0x3A7F`.

<details class="nb-hint">
<summary>Hint</summary>

10 offset bits.

</details>

<details class="nb-sol">
<summary>Solution</summary>

Page $\texttt{0x3A7F} \gg 10 = 14$, offset `0x27F`; frame 2 gives $2\cdot1024+\texttt{0x27F} = \texttt{0xA7F}$.

</details>

</div>

## 15.7 Virtual memory {#sec-os-prob-vm}

<div class="nb nb-problem nb-block" id="problem-15-48">

<strong>Problem 15.48</strong> (Why virtual)

Which statements explain why a virtual address is called “virtual”? (A) It does not correspond to a fixed physical location. (B) The page it names may be on disk or not yet allocated. (C) It is generated by the compiler, not the CPU. (D) Two processes can use the same virtual address for different data.

<details class="nb-hint">
<summary>Hint</summary>

Who issues the address, and who decides where it goes?

</details>

<details class="nb-sol">
<summary>Solution</summary>

A, B, D. The CPU issues virtual addresses (C is false); the MMU and the OS decide what physical frame, if any, backs them.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-15-49">

<strong>Problem 15.49</strong> 🌶🌶 (Count the faults)

Reference string `3 1 4 1 5 9 2 6 5 3 5 8 9 7 9 3`, 4 frames, initially empty. Count the page faults for FIFO, LRU, OPT and Clock (reference bit set on load).

<details class="nb-hint">
<summary>Hint</summary>

OPT is the lower bound; check your FIFO and LRU against it.

</details>

<details class="nb-sol">
<summary>Solution</summary>

FIFO 13, LRU 12, OPT 9, Clock 13.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-15-50">

<strong>Problem 15.50</strong> 🌶🌶 (Belady)

For `4 1 2 0 4 1 5 4 1 2 0 2 5 2`, compare FIFO with 3 and 4 frames, and LRU with 3 and 4 frames.

<details class="nb-hint">
<summary>Hint</summary>

LRU is a stack algorithm.

</details>

<details class="nb-sol">
<summary>Solution</summary>

FIFO: 9 faults with 3 frames, 10 with 4 (Belady’s anomaly). LRU: 10 with 3, 8 with 4; it cannot show the anomaly.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-15-51">

<strong>Problem 15.51</strong> (Proportional allocation)

71 frames are divided between P1 (23 pages) and P2 (117 pages) by proportional allocation. How many frames does each get?

<details class="nb-hint">
<summary>Hint</summary>

$a_i=\lfloor s_i m/S\rfloor$, $S=140$.

</details>

<details class="nb-sol">
<summary>Solution</summary>

P1 $\lfloor11.66\rfloor=11$, P2 $\lfloor59.34\rfloor=59$; one frame is left for the free pool (or given to the larger remainder, P1, if the policy rounds).

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-15-52">

<strong>Problem 15.52</strong> (Page stealing)

Which is correct about page stealing? (A) It is a sign of an efficient system. (B) It is taking page frames from other processes’ working sets. (C) It should be the goal of memory tuning. (D) It means taking larger disk space for paged-out pages.

<details class="nb-hint">
<summary>Hint</summary>

Global replacement.

</details>

<details class="nb-sol">
<summary>Solution</summary>

B.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-15-53">

<strong>Problem 15.53</strong> (Thrashing cures)

Which reduce thrashing? (A) lowering the degree of multiprogramming (B) adding RAM (C) a larger swap partition (D) a faster CPU (E) working-set based allocation (F) admitting more processes when CPU utilisation drops.

<details class="nb-hint">
<summary>Hint</summary>

Thrashing means the working sets do not fit.

</details>

<details class="nb-sol">
<summary>Solution</summary>

A, B, E. C and D do not change whether working sets fit; F is what causes the collapse.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-15-54">

<strong>Problem 15.54</strong> 🌶 (Effective access time)

Memory access 60 ns. A page fault takes 2 ms if the victim is clean and 6 ms if dirty; 30% of victims are dirty. Fault rate $p=10^{-5}$. What is the effective access time?

<details class="nb-hint">
<summary>Hint</summary>

Average the fault service time first.

</details>

<details class="nb-sol">
<summary>Solution</summary>

Average service $0.7\times2+0.3\times6=3.2$ ms; EAT $=(1-10^{-5})\times60 + 10^{-5}\times 3.2\times10^6 = 92.0$ ns, half again as slow as memory.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-15-55">

<strong>Problem 15.55</strong> (Working set)

References (time 0 first): `1 2 3 2 4 2 3 5 5 6 5 6`. With window $\Delta=4$, what is the working set at $t=5$ and at $t=11$?

<details class="nb-hint">
<summary>Hint</summary>

The last four references up to and including $t$.

</details>

<details class="nb-sol">
<summary>Solution</summary>

$t=5$: references $3,2,4,2$, set $\{2,3,4\}$. $t=11$: $5,6,5,6$, set $\{5,6\}$.

</details>

</div>

## 15.8 Files, I/O and the system {#sec-os-prob-fs}

<div class="nb nb-problem nb-block" id="problem-15-56">

<strong>Problem 15.56</strong> (Maximum file size)

An inode has 10 direct pointers, one single indirect and one double indirect pointer. Blocks are 2 KiB and pointers 4 bytes. What is the largest file?

<details class="nb-hint">
<summary>Hint</summary>

$k=512$ pointers per block.

</details>

<details class="nb-sol">
<summary>Solution</summary>

$(10+512+512^2)\times2048 = 262{,}666\times2048 = 537{,}939{,}968$ bytes, about $513$ MiB.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-15-57">

<strong>Problem 15.57</strong> (Character devices)

Which are character devices? keyboard, hard disk, `/dev/null`, terminal, SSD, mouse, USB flash drive, serial port.

<details class="nb-hint">
<summary>Hint</summary>

Byte streams versus random-access blocks.

</details>

<details class="nb-sol">
<summary>Solution</summary>

Keyboard, `/dev/null`, terminal, mouse, serial port. Disks, SSDs and flash drives are block devices.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-15-58">

<strong>Problem 15.58</strong> 🌶🌶 (Disk head movement)

Queue `95 180 34 119 11 123 62 64`, head at 50 moving towards higher cylinders, cylinders 0–199. Total head movement for FCFS, SSTF, SCAN, C-SCAN (counting the return), LOOK and C-LOOK?

<details class="nb-hint">
<summary>Hint</summary>

SCAN goes to 199 before turning; LOOK turns at 180.

</details>

<details class="nb-sol">
<summary>Solution</summary>

FCFS 644, SSTF 236 (62 64 34 11 95 119 123 180), SCAN 337, C-SCAN 382, LOOK 299, C-LOOK 322 (`disk.py`’s functions on this queue).

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-15-59">

<strong>Problem 15.59</strong> (RAID capacity)

Six 2 TB disks. Usable capacity and guaranteed number of tolerated failures for RAID 0, 5, 6 and 10?

<details class="nb-hint">
<summary>Hint</summary>

Parity costs one or two disks; mirroring half.

</details>

<details class="nb-sol">
<summary>Solution</summary>

RAID 0: 12 TB, 0; RAID 5: 10 TB, 1; RAID 6: 8 TB, 2; RAID 10: 6 TB, 1 guaranteed (up to 3 if each failure is in a different mirror pair).

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-15-60">

<strong>Problem 15.60</strong> (Busy together)

Which technique keeps the CPU and the I/O devices busy at the same time by queueing a slow device’s work on disk: buffering, caching, spooling or polling?

<details class="nb-hint">
<summary>Hint</summary>

Think of the printer.

</details>

<details class="nb-sol">
<summary>Solution</summary>

Spooling. Buffering overlaps a job’s I/O with its own computation; multiprogramming is the more general answer when spooling is not offered.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-15-61">

<strong>Problem 15.61</strong> (`/etc/hosts`)

Which are true? (A) It maps host names to IP addresses statically. (B) With `hosts: files dns` in `nsswitch.conf`, an entry there overrides DNS. (C) It is consulted by `dig`. (D) Changing it affects only that machine.

<details class="nb-hint">
<summary>Hint</summary>

Who reads the file: the C library or the DNS server?

</details>

<details class="nb-sol">
<summary>Solution</summary>

A, B, D. `dig` queries DNS servers directly and ignores the file.

</details>

</div>

<div class="nb nb-problem nb-block" id="problem-15-62">

<strong>Problem 15.62</strong> (Links)

`echo hi > a; ln a b; ln -s a c; rm a`. What is the link count of `b`, and what do `cat b` and `cat c` print?

<details class="nb-hint">
<summary>Hint</summary>

`links.sh` did exactly this.

</details>

<details class="nb-sol">
<summary>Solution</summary>

Link count 1; `cat b` prints `hi`; `cat c` fails with “No such file or directory” (the symlink dangles).

</details>

</div>

## 15.9 Checking the numbers {#sec-os-prob-check}

The verification runs behind the solutions, for after you have tried the problems.

```text {filename="Terminal session (bash, Linux 6.18)"}
$ ./prob-buffer          (terminal)
-
-+
-+
$ ./prob-buffer | cat    (pipe)
-
-+
-+
$ ./prob-fork-loop | wc -l
10
$ ./prob-or | wc -l
5
$ ./prob-fd
ab345XY!
```

```text {filename="Output (Python 3.11)"}
P11 FCFS with an idle gap
   CT: {'A': 3, 'B': 8, 'C': 12, 'D': 16} avg TAT 4.25
P12 SRTF
   [0]P1 [1]P2 [2]P3 [4]P2 [5]P5 [6]P2 [8]P4 [13]P1 [21]
   avg WT 4.00, avg TAT 8.20, P1 WT 12
P13 RR q = 3
   [0]P1 [3]P2 [6]P1 [9]P3 [11]P4 [14]P2 [16]P1 [18]P4 [19]
   CT: {'P1': 18, 'P2': 16, 'P3': 11, 'P4': 19} avg WT 8.25, avg RT 2.75
   q = 8 equals FCFS: True
P15 HRRN choice at t = 10
   J1: (8 + 6)/6 = 2.33
   J2: (5 + 2)/2 = 3.50
   J3: (4 + 4)/4 = 2.00
P16 RMS / EDF
   [(1, 3), (1, 5), (1, 9)]: U = 0.6444, bound 0.7798
   [(2, 4), (3, 7)]: U = 0.9286, bound 0.8284
   RMS on (2,4),(3,7) over 28: misses none
   EDF on (2,4),(3,7) over 28: misses none
P17 CFS share: nice 0 (1024) vs nice 2 (655) vs nice -3 (1991)
   27.9%, 17.8%, 54.3%
P18 exponential average, alpha = 0.25, tau0 = 12, bursts 8 16 4
   -> 11.0000
   -> 12.2500
   -> 10.1875
P19 RR utilisation, q = 20 ms, switch 2 ms; bursts of 6 ms
   CPU-bound 0.9091; I/O-bound 0.7500
P21 semaphores
   initial = 4 + 12 - 5 = 11
   signals = -2 - 3 + 15 = 10
P23 x = 5; T1: x = x * 3  ||  T2: x = x + 4
   values: [9, 15, 19, 27]
P24 outputs with s = 0, t = 0
   outputs: ['ACBD', 'CABD'] deadlock possible: False
P25 x = 0, three threads each x++ twice (load/add/store)
   values: [2, 3, 4, 5, 6]
P30 Banker
   available [3, 1, 3] need [[3, 2, 2], [1, 1, 2], [3, 1, 2], [1, 2, 1]]
   safe sequence: ['P1', 'P2', 'P3', 'P0']
   P1 requests [1, 0, 1]: grant ['P1', 'P2', 'P3', 'P0']
   P3 requests [1, 1, 0]: deny
P31 5 processes needing 4 each -> R = 16
    6 units, 3 needed each -> at most 2 processes
P33 fixed partitions [110, 70, 190, 50], requests 60 85 45 120, first fit
   60 -> 110 (waste 50)
   85 -> 190 (waste 105)
   45 -> 70 (waste 25)
   120: no partition; free [50]
   internal total 180
P34 partitions [400, 120, 250, 300], three processes of 150, first fit
   placement [150, None, 150, 150], internal 500, unused 120
P35 page table: VA 34 bits, 8 KiB pages, 4 GiB RAM, PTE = frame + 3 bits
   entries 2^21, frame bits 19, PTE 22 bits -> 3 B, table 6 MiB
P36 levels: 48-bit VA, 16 KiB pages, 8-byte PTEs
   offset 14, index bits/level 11, levels 4
P37 TLB: t = 5 ns, m = 80 ns, 3-level table; hit ratio for EAT <= 100 ns
   h >= 0.9375
P38 address 0x3A7F, 1 KiB pages, page table 0->5, 1->9, 14->2
   VPN 14, offset 0x27F, frame 2, PA 0xA7F
P40 page faults, 4 frames
   FIFO: 13
   LRU: 12
   OPT: 9
   Clock: 13
P41 Belady check on 4 1 2 0 4 1 5 4 1 2 0 2 5 2
   FIFO 3..5 frames: [9, 10, 5]  LRU: [10, 8, 5]
P42 proportional allocation: 71 frames, P1 23 pages, P2 117 pages
   P1 11.66 -> 11, P2 59.34 -> 59
P44 EAT: memory 60 ns, fault 2 ms (clean) / 6 ms (dirty, 30%), p = 1e-5
   average fault 3.2 ms, EAT 92.00 ns
P45 working set, window 4
   t = 5: [2, 3, 4]
   t = 11: [5, 6]
P46 inode: 10 direct, 1 single, 1 double; 2 KiB blocks, 4 B pointers
   262666 blocks = 537939968 B = 0.5010 GiB
P48 disk: queue 95 180 34 119 11 123 62 64, head 50 moving up, 0..199
   fcfs  95 180 34 119 11 123 62 64               total 644
   sstf  62 64 34 11 95 119 123 180               total 236
   scan  62 64 95 119 123 180 199 34 11           total 337
   cscan 62 64 95 119 123 180 199 0 11 34         total 382
   look  62 64 95 119 123 180 34 11               total 299
   clook 62 64 95 119 123 180 11 34               total 322
P49 RAID with six 2 TB disks
   RAID 0: 12 TB, RAID 5: 10 TB, RAID 6: 8 TB, RAID 10: 6 TB
P10 exit(300) status: 44 ; exit(-2): 254
```
