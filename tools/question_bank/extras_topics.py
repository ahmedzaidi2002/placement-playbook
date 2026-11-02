"""Subject and topic for the Qualcomm questions that are not in the company DB.

Topic names match company-questions/tools/topics_*.py so every question of a topic lands on
one page.
"""
QA = 'Quantitative aptitude'
LR = 'Logical reasoning'
C = 'C programming'
CPP = 'C++ and object-oriented programming'
DSA = 'Data structures and algorithms'
OS = 'Operating systems'
ARCH = 'Computer architecture and digital logic'
EMB = 'Embedded systems and electronics'

T_NUM = 'Number systems and computer arithmetic'
T_COMB = 'Combinational logic (gates, K-map, adders, MUX)'
T_SEQ = 'Sequential logic (flip-flops, counters, FSM)'
T_ISA = 'Instruction set, addressing modes and CPU design'
T_PIPE = 'Pipelining and hazards'
T_CACHE = 'Cache and memory hierarchy'
T_MISC = 'Computer architecture and miscellaneous'

# 60-question assessment: question number -> (subject, topic)
Q60 = {
    1: (QA, 'Geometry and mensuration'),
    2: (QA, 'Geometry and mensuration'),
    3: (QA, 'Ages'),
    4: (QA, 'Percentages'),
    5: (LR, 'Series and pattern completion'),
    6: (QA, 'Permutations and combinations'),
    7: (QA, 'Ratio, proportion, mixtures and partnership'),
    8: (LR, 'Seating, row and floor arrangements'),
    9: (LR, 'Seating, row and floor arrangements'),
    10: (LR, 'Seating, row and floor arrangements'),
    11: (LR, 'Seating, row and floor arrangements'),
    12: (LR, 'Seating, row and floor arrangements'),
    13: (LR, 'Series and pattern completion'),
    14: (QA, 'Data interpretation (tables, charts)'),
    15: (QA, 'Data interpretation (tables, charts)'),
    16: (QA, 'Data interpretation (tables, charts)'),
    17: (QA, 'Data interpretation (tables, charts)'),
    18: (QA, 'Time, speed and distance'),
    19: (QA, 'Probability'),
    20: (LR, 'Mathematical operations and input-output rules'),
    21: (ARCH, T_NUM),
    22: (OS, 'Memory management and paging'),
    23: (ARCH, T_COMB),
    24: (C, 'Functions, recursion, scope and storage classes'),
    25: (C, 'General output prediction and compile errors'),
    26: (DSA, 'Sorting and searching'),
    27: (C, 'General output prediction and compile errors'),
    28: (OS, 'CPU scheduling'),
    29: (DSA, 'Linked lists, stacks and queues'),
    30: (ARCH, T_NUM),
    31: (DSA, 'Sorting and searching'),
    32: (OS, 'Processes, threads and IPC'),
    33: (ARCH, T_SEQ),
    34: (ARCH, T_ISA),
    35: (C, 'General output prediction and compile errors'),
    36: (DSA, 'Linked lists, stacks and queues'),
    37: (C, 'General output prediction and compile errors'),
    38: (C, 'General output prediction and compile errors'),
    39: (C, 'General output prediction and compile errors'),
    40: (C, 'printf/scanf and I/O'),
    41: (ARCH, T_PIPE),
    42: (DSA, 'Arrays, strings and output prediction'),
    43: (C, 'General output prediction and compile errors'),
    44: (CPP, 'OOP concepts and miscellaneous'),
    45: (C, 'General output prediction and compile errors'),
    46: (ARCH, T_COMB),
    47: (C, 'Arrays and 2-D arrays'),
    48: (CPP, 'OOP concepts and miscellaneous'),
    49: (C, 'General output prediction and compile errors'),
    50: (ARCH, T_NUM),
    51: (DSA, 'Arrays, strings and output prediction'),
    52: (DSA, 'Complexity and recurrences'),
    53: (C, 'Pointers and pointer arithmetic'),
    54: (C, 'General output prediction and compile errors'),
    55: (OS, 'Deadlocks'),
    56: (C, 'General output prediction and compile errors'),
    57: (DSA, 'Linked lists, stacks and queues'),
    58: (OS, 'CPU scheduling'),
    59: (CPP, 'Inheritance, virtual functions and polymorphism'),
    60: (OS, 'Memory management and paging'),
}

_OOP = {
    'Constructors': 'Constructors, destructors and copy semantics',
    'Inheritance': 'Inheritance, virtual functions and polymorphism',
    'Access control': 'Classes, access, static and friend',
    'Static members': 'Classes, access, static and friend',
    'Interfaces (Java)': 'Inheritance, virtual functions and polymorphism',
}
_OS = {
    'Processes': 'Processes, threads and IPC',
    'Scheduling': 'CPU scheduling',
    'Disk scheduling': 'File systems and disk scheduling',
    'Memory management': 'Memory management and paging',
    'Virtual memory': 'Memory management and paging',
    'Inter-process communication': 'Processes, threads and IPC',
    'Synchronisation': 'Synchronization (semaphores, mutex, monitors)',
    'Deadlock': 'Deadlocks',
    'Operating-system basics': 'System calls, kernel and general OS',
}
_ARCH = {
    'Number systems': T_NUM,
    'Boolean algebra and gates': T_COMB,
    'Digital design flow': T_MISC,
    'Registers and instruction sets': T_ISA,
    'Pipelining': T_PIPE,
    'Performance': T_PIPE,
    'Parallel organisation': T_MISC,
    'Memory hierarchy': T_CACHE,
    'Caches': T_CACHE,
    'Memory organisation': T_CACHE,
    'Buses and I/O': T_ISA,
    'Flip-flops (CA section)': T_SEQ,
}
_DIG = {
    'Codes and number systems': (ARCH, T_NUM),
    'Boolean algebra': (ARCH, T_COMB),
    'Gates and combinational circuits': (ARCH, T_COMB),
    'Multiplexers and decoders': (ARCH, T_COMB),
    'Arithmetic circuits': (ARCH, T_COMB),
    'Programmable logic': (ARCH, T_COMB),
    'Latches and flip-flops': (ARCH, T_SEQ),
    'Registers and sequential design': (ARCH, T_SEQ),
    'Counters': (ARCH, T_SEQ),
    'Timing': (ARCH, T_SEQ),
    'Logic families': (EMB, 'Analog devices and op-amps'),
    'MOS circuits': (EMB, 'Analog devices and op-amps'),
    'Data converters': (EMB, 'Microcontrollers, interrupts, ADC and timers'),
    'Circuits and signals': (EMB, 'Circuit analysis (Kirchhoff, RC/RLC, two-port)'),
    'Memory devices': (ARCH, T_CACHE),
    'Control unit': (ARCH, T_ISA),
    'Testing': (ARCH, T_MISC),
}

CORE = {
    'oop': lambda t: (CPP, _OOP[t]),
    'os': lambda t: (OS, _OS[t]),
    'arch': lambda t: (ARCH, _ARCH[t]),
    'dig': lambda t: _DIG[t],
}
