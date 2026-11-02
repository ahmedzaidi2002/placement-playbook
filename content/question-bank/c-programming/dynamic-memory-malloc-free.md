---
title: "Dynamic memory (malloc, free)"
weight: 6
---

5 questions asked by MathWorks, NVIDIA. Try each one first, then open the toggle: it gives the answer, why it is right, and the idea behind it explained from scratch.

### 1 · Q9, the malloc free list

*Asked by: MathWorks (IISc 2024)*

Which is true? (1) When `malloc` allocates a block it allocates extra bytes to hold an
integer containing the size of the block. (2) The list of free blocks is a doubly linked
list.

- **(a)** Both
- **(b)** Neither
- **(c)** Only 1
- **(d)** Only 2

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) only 1**

**Why.** (1) Allocators store a small header with each block's size; that is how `free(p)` knows how much to release. (2) The free list's structure depends on the allocator: the classic K&R allocator uses a singly linked circular list, so "doubly linked" is not true in general.

**Concept: how malloc works.** The heap is a pool of memory. `malloc` finds a free chunk big enough, records its size in a hidden header just before the returned pointer, and gives you the address after the header. `free` reads that header and puts the chunk back on a free list.

{{< /details >}}

### 2 · Q24, dangling pointers

*Asked by: MathWorks (IIT Bombay 2024)*

A dangling pointer arises when:

- **(a)** a local variable is static
- **(b)** a pointer is uninitialised
- **(c)** a pointer points to nothing
- **(d)** the memory it points to is freed

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) the memory it points to is freed**

**Why.** After `free(p)` (or after a local variable's function returns), p still holds the old address, but that memory no longer belongs to you: p is dangling. An uninitialised pointer is called a "wild" pointer.

**Concept: dangling pointers.** Using one is undefined behaviour (may crash or corrupt data). Set pointers to NULL after freeing and never return the address of a local variable.

{{< /details >}}

### 3 · Q19, malloc versus calloc

*Asked by: MathWorks (NIT Durgapur 2024); MathWorks (IIIT Delhi 2024); MathWorks (Recalled list); MathWorks (IIITDM Kancheepuram 2025)*

With respect to the differences between `malloc` and `calloc`, which are true?

- **(a)** calloc initialises the allocated memory with 0 while malloc leaves garbage
- **(b)** calloc always allocates contiguous memory but malloc may not
- **(c)** calloc takes the number and size of elements as arguments while malloc takes the number of bytes
- **(d)** calloc may not allocate contiguous memory but malloc always does

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) and (c)**

**Why.** `calloc(n, size)` allocates n × size bytes and fills them with zeros; `malloc(bytes)` takes one size and leaves the contents uninitialised. Both return a single contiguous block, so (b) and (d) are false.

**Concept: malloc vs calloc.** Same kind of heap block; the differences are the argument form and zero-initialisation. Use calloc when you need zeroed memory (e.g. counters).

{{< /details >}}

### 4 · Q3, return type of malloc

*Asked by: MathWorks (IIITDM Kancheepuram 2025)*

The return type of `malloc` is _____.

- **(a)** int*
- **(b)** void*
- **(c)** int
- **(d)** void

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) `void*`**

**Why.** `malloc` doesn't know what you will store, so it returns a generic pointer. C converts `void*` to any object pointer automatically; C++ requires a cast.

**Concept: `void*`.** A pointer with no type information. You cannot dereference it directly; you assign it to a typed pointer first.

{{< /details >}}

### 5 · Q13, calloc

*Asked by: NVIDIA (SSE NCG, Nov 2024)*

How many arguments does the function `calloc()` take?

- **(a)** 1
- **(b)** 2
- **(c)** 3
- **(d)** None of the above

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) 2**

**Why.** `calloc(count, size)` takes the number of elements and the size of each, allocates count × size bytes and zeroes them. `malloc` takes one argument.

**Concept: same as above.** Remember the signatures: `malloc(size)`, `calloc(count, size)`, `realloc(ptr, new_size)`, `free(ptr)`.

{{< /details >}}
