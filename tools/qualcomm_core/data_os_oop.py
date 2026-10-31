"""OOPS and Operating Systems questions from the eight campus papers.

Q(...) fields: topic, src [(paper, qno)], text, opts, ans ('A'-'D' or None),
expl (markdown), conf ('high' | 'medium' | 'flag'), note (why medium/flagged),
fig (name in figures.ALL), code (C/C++ snippet), table (markdown).
"""
from qdef import Q

OOP = [
    Q('Constructors', [('p4', 54)],
      'The process of defining more than one constructor with different parameter lists in the same class is known as:',
      ['Constructor overriding', 'Constructor chaining', 'Constructor hiding', 'Constructor overloading'], 'D',
      'Same name, different parameter lists, resolved at compile time: that is overloading. Overriding needs a '
      'base and a derived class, and constructors are not inherited, so they cannot be overridden. Chaining is one '
      'constructor calling another (`this(...)` in Java, a delegating constructor in C++).'),
    Q('Inheritance', [('p4', 55)],
      'The figure shows two classes: **Class B → Class A** (B is derived from A, and nothing else is involved). '
      'What type of inheritance is this?',
      ['Multilevel inheritance', 'Single inheritance', 'Multiple inheritance', 'Hybrid inheritance'], 'B',
      'One base and one derived class is single inheritance. Multilevel needs a chain (C → B → A); multiple needs '
      'one class with two or more bases; hybrid mixes these.'),
    Q('Access control', [('p4', 58)],
      'Given a method in a protected class, what access modifier do you use to restrict access to that method to '
      'only the other members of the same class?',
      ['private', 'public', 'transient', 'protected'], 'A',
      '`private` limits access to the class itself. `protected` would also open it to subclasses (and, in Java, '
      'the package). `transient` is not an access modifier; it marks a field to skip during serialisation.'),
    Q('Static members', [('p7', 55)],
      'Which of the statements below is/are true?\n\n'
      'I. A static method belongs to the class rather than to an object of the class.  \n'
      'II. Static methods can be called without creating an object of the class.  \n'
      'III. A static method can access static data members and can change their values.',
      ['Only (I)', 'All (I), (II) and (III)', 'Only (II)', 'Only (III)'], 'B',
      'All three hold. A static method has no `this`, so it cannot touch instance members directly, but static '
      'data belongs to the class and a static method may read and write it.'),
    Q('Interfaces (Java)', [('p7', 46)],
      'Which one of the statements given in the options is **false**?',
      ['An interface that is declared within the body of a class or interface is known as a nested interface.',
       'A class declaration can be a member of an interface.',
       'A constant can be a member of an interface.',
       'If an interface is named in the implements clause of a class, then the class must implement all of the '
       'methods declared within the interface.'], 'D',
      'An **abstract** class can name an interface in its `implements` clause and leave some methods '
      'unimplemented; only a concrete class must implement all of them (and since Java 8, `default` methods need '
      'no implementation either). The first three are true: nested interfaces exist, an interface may declare a '
      'member class, and every interface field is implicitly `public static final`, i.e. a constant.'),
]

OS = [
    # ---- processes and scheduling ----
    Q('Processes', [('p7', 39)],
      'In which of the process states given in the options are process instructions executed?',
      ['Running state', 'Terminated state', 'Waiting state', 'Ready state'], 'A',
      'Only a process that holds the CPU executes instructions; that is the running state. Ready processes wait '
      'for the CPU, waiting (blocked) processes wait for an event such as I/O.'),
    Q('Processes', [('p7', 30)],
      'If a process has finished its execution, what is the state of that process?',
      ['Waiting', 'Ready', 'Terminated', 'Running'], 'C',
      'After its last instruction (or `exit()`), a process moves to the terminated state, where it stays until '
      'the parent collects its exit status.'),
    Q('Processes', [('p0', 39)],
      'Which section of the process memory layout is also called the **bss** segment?',
      ['Stack', 'Uninitialized data segment', 'Initialized data segment', 'Code segment'], 'B',
      'The bss (block started by symbol) holds globals and statics that are not explicitly initialised; the '
      'loader zero-fills it, so it takes no space in the executable file. Initialised globals go in the data '
      'segment.'),
    Q('Processes', [('p1', 33)],
      'During a context switch, which of the following information is stored for later use?\n\n'
      'I. Accounting information  \nII. I/O status information',
      ['Only (II)', 'Neither (I) nor (II)', 'Both (I) and (II)', 'Only (I)'], 'C',
      'Both live in the process control block (PCB), which is saved on a switch along with the registers, '
      'program counter, scheduling and memory-management information.'),
    Q('Processes', [('p3', 39)],
      'Let *st1* be the time to switch between user mode and kernel mode, and *st2* the time to switch between '
      'two user processes. Which is true?',
      ['Indeterminate', 'st1 > st2', 'st1 < st2', 'st1 = st2'], 'C',
      'A mode switch only changes the privilege level and stack, inside the same process. A process switch has '
      'to do a mode switch **and** save one PCB, restore another, change the address space and lose TLB and cache '
      'warmth, so it always costs more.'),
    Q('Scheduling', [('p1', 27)],
      'Which scheduler is also called the **job scheduler**?',
      ['Intermediate-term', 'Long-term', 'Short-term', 'Medium-term'], 'B',
      'The long-term scheduler picks jobs from the job pool and admits them to memory, controlling the degree of '
      'multiprogramming. The short-term one is the CPU scheduler; the medium-term one swaps processes out and in.'),
    Q('Scheduling', [('p4', 40)],
      'Which of the CPU scheduling algorithms given in the options suffers from the **convoy effect**?',
      ['Multilevel queue', 'Shortest remaining time first', 'Round robin', 'First come first serve'], 'D',
      'In FCFS one long CPU-bound job holds the CPU while short I/O-bound jobs pile up behind it like cars behind '
      'a truck, which lowers both CPU and device utilisation.'),
    Q('Scheduling', [('p2', 31)],
      'Round robin with time quantum 1. Five processes arrive at time 0 in the order A, B, C, D, E with burst '
      'times A = 4, B = 1, C = 8, D = 1, E = 2. What is the completion time of A?',
      ['11', '4', '10', '12'], 'A',
      'Each round gives every live process one unit.\n\n'
      '| Time | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 |\n|---|---|---|---|---|---|---|---|---|---|---|---|\n'
      '| Runs | A | **B** | C | **D** | E | A | C | **E** | A | C | **A** |\n\n'
      'B finishes at 2, D at 4, E at 8, A at **11**, and C runs alone afterwards to finish at 16.'),
    Q('Scheduling', [('p0', 30)],
      'What is the average waiting time of a process if the scheduling queue holds on average 34 processes and '
      '9 processes arrive every second?',
      ['3.7 units', '2.9 units', '9 units', '4 units'], 'A',
      "Little's law: *n = λ × W*, so *W = n / λ = 34 / 9 ≈ 3.78* seconds; the option is 3.7."),
    Q('Scheduling', [('p7', 22)],
      'Which of the statements given below is/are correct for CPU scheduling algorithms?\n\n'
      'I. The throughput of Shortest Process Next (SPN) is on the higher side compared to FCFS.  \n'
      'II. The overhead for round robin is lower as compared to SPN.  \n'
      'III. Starvation of processes is possible in FCFS.',
      ['Only (II) and (III)', 'Only (II)', 'Only (I) and (II)', 'Only (I) and (III)'], 'C',
      'I is true: running short jobs first finishes more jobs per unit time. II is true in the standard comparison '
      '(Stallings): RR has minimal decision overhead, while SPN must estimate and compare burst times, which can '
      'be costly. III is false: in FCFS every process eventually reaches the head of the queue, so none starves.',
      conf='medium', note='Statement II depends on the textbook comparison table; RR does pay for extra context '
      'switches, but its scheduling decision itself is the cheapest.'),
    Q('Scheduling', [('p5', 40)],
      'Which one of the given options is also called the **release time** of a CPU scheduling process?',
      ['Completion time', 'Response time', 'Release time', 'Start time'], 'A',
      'The time at which a process leaves the system (finishes and releases the CPU) is its completion time, also '
      'called exit time. Note that in real-time scheduling "release time" means the time a job becomes ready, '
      'which is none of these options.',
      conf='medium', note='The wording is unusual; completion (exit) time is the only option that is a synonym '
      'for the moment a process leaves.'),
    Q('Disk scheduling', [('p6', 34)],
      'A disk driver receives requests for cylinders in the order 67, 45, 22, 180, 112, 95, 77, 69, 66, 55, 10. '
      'C-SCAN is used, where each seek … (the rest of the sentence is cut off in the photo). The head is '
      'currently at cylinder 30. What is the total seek time?',
      ['558 ms', '1096 ms', '996 ms', '408 ms'], None,
      'The service order is clear: moving up from 30, the head serves 45, 55, 66, 67, 69, 77, 95, 112, 180, then '
      'jumps back and serves 10 and 22.\n\n'
      '- Counting only the cylinders actually crossed while serving: 30 → 180 = 150, wrap 180 → 10 = 170, '
      '10 → 22 = 12, total 332. At 3 ms per cylinder that is **996 ms**.\n'
      '- If the head goes to the last cylinder (199) and the return to 0 is counted: 169 + 199 + 22 = 390 cylinders.\n\n'
      'The time per cylinder and the disk size were in the cut-off part, so the answer cannot be fixed.',
      conf='flag', note='The seek time per cylinder and the disk size are missing from the photo.'),
    # ---- memory ----
    Q('Memory management', [('p1', 26)],
      'Which of the statements given below is/are true about **dynamic partitioning**?\n\n'
      'I. Partitions are of fixed length and their number is variable.  \n'
      'II. Holes are created in memory over time.  \n'
      'III. Partitions are not of the same length and they vary in number.',
      ['Only (I) and (II)', 'Only (I)', 'Only (III)', 'Only (II) and (III)'], 'D',
      'Dynamic (variable) partitioning carves exactly the size each process needs, so partitions differ in size '
      'and count (III). As processes leave, free gaps appear between allocated blocks: external fragmentation (II). '
      'Fixed-length partitions describe static partitioning.'),
    Q('Memory management', [('p5', 38)],
      'Which of the following statements about memory fragmentation is true?',
      ['Such issues only occur in heap memory.', 'Using malloc() instead of calloc() prevents these issues.',
       'These issues occur only in stack memory.',
       'They can be caused by repeated allocation and deallocation.'], 'D',
      'Fragmentation comes from allocating and freeing blocks of different sizes over time, which leaves '
      'unusable gaps. It is not limited to the heap (OS physical memory fragments too), and `malloc` vs `calloc` '
      'only differ in zero-filling.'),
    Q('Memory management', [('p7', None)],
      'Which of the given statements is/are **not** true regarding memory management?\n\n'
      'I. Memory management refers to management of primary memory.  \n'
      'II. Memory management refers to management of secondary memory.',
      ['Both (I) and (II)', 'Only (II)', 'Neither (I) nor (II)', 'Only (I)'], 'B',
      'In OS terms memory management is about main (primary) memory: allocation, protection, paging, swapping. '
      'Secondary storage is handled by file-system and disk management, so II is the false statement.',
      conf='medium', note='Some notes describe swapping as moving data between primary and secondary memory, but '
      'the subject being managed is still main memory.'),
    Q('Virtual memory', [('p3', 30)],
      'The working-set size of a process should be increased (to minimise page faults) when the page-fault rate is:',
      ['Constant', 'Low', 'High', 'Varying'], 'C',
      'Page-fault-frequency control: a high fault rate means the process has too few frames, so its working set '
      'is grown; a very low rate means frames can be taken away.'),
    Q('Inter-process communication', [('p5', 34)],
      'Consider the IPC models I) Message passing and II) Shared memory. Which model(s) use map-memory system calls '
      'to access memory?',
      ['Neither (I) nor (II)', 'Only (I)', 'Only (II)', 'Both (I) and (II)'], 'C',
      'Shared memory is set up with calls such as `shmget`/`shmat` or `mmap`, which map a common region into each '
      'address space; after that the processes use plain loads and stores. Message passing goes through '
      '`send`/`receive` system calls instead.'),
    Q('Inter-process communication', [('p7', None)],
      'Which of the following statements about sockets is/are true?\n\n'
      'I. Sockets do not create connections between machines or processes to facilitate communication over a network.  \n'
      'II. In a distributed application, sockets offer dependable, asynchronous communication between parts '
      'operating on various machines.',
      ['None', 'Only ii', 'Both i and ii', 'Only i'], 'B',
      'Statement I is false: a socket is exactly the endpoint through which a connection between two processes '
      '(possibly on different machines) is made. Statement II describes their use in distributed applications.',
      conf='medium', note='Statement II is loosely worded (sockets can be blocking or non-blocking; only TCP is '
      'reliable), but it is the intended true statement.'),
    # ---- synchronisation ----
    Q('Synchronisation', [('p4', 37)],
      'Which of the following is a case of the concurrency-control problem?',
      ['Block allocation', 'Bounded buffer', 'I/O interlock', 'Low page hit ratio'], 'B',
      'The bounded-buffer (producer-consumer) problem is a classic synchronisation problem: producers must wait '
      'when the buffer is full and consumers when it is empty, with mutual exclusion on the buffer.'),
    Q('Synchronisation', [('p4', 48)],
      'Which of the following are **hardware-based** solutions to the critical-section problem?\n\n'
      'I. test_and_set()  \nII. compare_and_swap()  \nIII. Peterson\'s solution',
      ['Only (I) and (II)', 'Only (I) and (III)', 'Only (I)', 'All (I), (II) and (III)'], 'A',
      '`test_and_set` and `compare_and_swap` are atomic machine instructions. Peterson\'s algorithm is a pure '
      'software solution that uses ordinary loads and stores (and in fact needs memory barriers on modern CPUs).'),
    Q('Synchronisation', [('p4', 43)],
      'The `test_and_set()` algorithm below will satisfy which of the critical-section requirements? '
      '(The options were not captured in the photo.)', [], None,
      'This is the bounded-waiting mutual exclusion algorithm with `test_and_set`, and it satisfies **all three** '
      'requirements:\n\n'
      '- **Mutual exclusion**: a process enters only when `key` becomes false (it won the lock) or when `waiting[i]` '
      'is set false by the leaving process, and only one of those can happen at a time.\n'
      '- **Progress**: a leaving process either hands over to a waiting process or releases the lock.\n'
      '- **Bounded waiting**: the leaving process scans `waiting[]` in cyclic order starting at *i + 1*, so any '
      'waiting process gets in within *n − 1* turns.',
      code='do {\n    waiting[i] = true;\n    key = true;\n    while (waiting[i] && key)\n'
           '        key = test_and_set(&lock);\n    waiting[i] = false;\n\n    /* critical section */\n\n'
           '    j = (i + 1) % n;\n    while ((j != i) && !waiting[j])\n        j = (j + 1) % n;\n'
           '    if (j == i)\n        lock = false;\n    else\n        waiting[j] = false;\n\n'
           '    /* remainder section */\n} while (true);',
      conf='medium', note='Only the question and code were photographed; pick the option that lists mutual '
      'exclusion, progress and bounded waiting.'),
    # ---- deadlock ----
    Q('Deadlock', [('p4', 49)],
      'Which of the following are methods for handling deadlocks?\n\n'
      'I. Use a protocol to prevent or avoid deadlocks.  \n'
      'II. Allow the system to enter a deadlocked state, detect it, and recover.  \n'
      'III. Ignore the problem and pretend that deadlocks never occur.',
      ['Only (I) and (III)', 'Only (I)', 'All (I), (II) and (III)', 'Only (I) and (II)'], 'C',
      'These are the three textbook strategies. The third (the "ostrich" approach) is what most general-purpose '
      'systems, including Linux and Windows, actually do.'),
    Q('Deadlock', [('p0', 36)],
      'In deadlock avoidance, a request for a resource that is currently available is granted:\n\n'
      'I. only if the allocation leaves the system in a safe state.  \n'
      'II. if the allocation leaves the system in a safe or an unsafe state.',
      ['Only (I)', 'Both (I) and (II)', 'Only (II)', 'Neither (I) nor (II)'], 'A',
      'Avoidance (e.g. the banker\'s algorithm) grants a request only if the resulting state is safe; otherwise the '
      'process waits even though the resource is free.'),
    Q('Deadlock', [('p6', 39)],
      'What will happen if a system does not employ either a deadlock-prevention or a deadlock-avoidance algorithm?',
      ['Nothing will happen.', 'Deadlock situation may not arise.', 'Deadlock situation arise.',
       'Deadlock situation may arise.'], 'D',
      'Without prevention or avoidance nothing rules a deadlock out, but it is not guaranteed either; it may '
      'arise, and the system then needs detection and recovery.'),
    Q('Deadlock', [('p7', 52)],
      'Which one of the given options is true if information such as "which resources a process will request" '
      'is given in advance?',
      ['The operating system cannot decide whether the process should not wait for each request.',
       'The operating system cannot decide whether the process should wait for each request.',
       'The operating system cannot decide whether the current request can be satisfied or must be delayed.',
       'The operating system can decide whether or not the process should wait for each request.'], 'D',
      'Knowing future requests in advance is exactly what deadlock avoidance needs: for each request the OS checks '
      'whether granting it keeps the system safe, and makes the process wait if it would not.'),
    Q('Operating-system basics', [('p6', 26)],
      'Which of the statement(s) given below is/are true about a Linux (kernel) distribution?\n\n'
      'I. It is mostly abbreviated as distro.  \nII. It consists of a software collection.  \n'
      'III. It consists of a package management system.',
      ['Only (III)', 'Only (I)', 'Only (II)', '(I), (II) and (III)'], 'D',
      'A distribution (distro) bundles the Linux kernel with a collection of software (GNU tools, libraries, '
      'desktop, etc.) and a package manager such as apt, dnf or pacman to install and update it.'),
]
