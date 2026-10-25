---
title: "9 · File systems"
linkTitle: "9 File systems"
weight: 9
math: true
---
## 9.1 Files, inodes and directories {#os-9-1}

<div class="nb nb-definition">

<strong>Definition</strong> — A **file** is a named, persistent sequence of bytes. In UNIX, everything about a file except its name (type, size, owner, permissions, timestamps, link count, pointers to its data blocks) is stored in an **inode**. A **directory** is a special file that maps names to inode numbers.

</div>

- **Access methods:** sequential (read the next part), direct/random (read block $n$), indexed (an index maps keys to blocks).
- **Directory structures:** single-level → two-level (per user) → **tree** (subdirectories, absolute/relative paths) → acyclic graph (shared files via links) → general graph (cycles allowed; hard to traverse, so UNIX forbids hard links to directories).

## 9.2 Block allocation methods {#os-9-2}

| Method | How | Good | Bad |
|---|---|---|---|
| **Contiguous** | file = (start block, length) | fast sequential and random access | external fragmentation; hard to grow |
| **Linked** | each block points to the next | no fragmentation; easy to grow | random access to block $i$ needs $i$ reads; a broken pointer loses the rest |
| **FAT** | the "next" pointers kept in one table (File Allocation Table) in memory | random access by following the cached table | the table must be cached; large for big disks |
| **Indexed** | an index block lists all the file's blocks | fast random access, no external fragmentation | overhead of index blocks |

## 9.3 The UNIX inode and maximum file size {#os-9-3}

An inode holds some **direct** pointers to data blocks, then one **single indirect** pointer (to a block full of pointers), one **double indirect** and one **triple indirect**.

<div class="nb nb-theorem nb-block">

<strong>Maximum file size</strong>

Block size $B$, pointer size $p$, so $k = B/p$ pointers fit in one block. With $d$ direct pointers:

$$\text{max size} = \left(d + k + k^2 + k^3\right) \times B.$$

</div>

<div class="nb nb-example">

<strong>Example</strong> (Max file size)

4 KB blocks, 4-byte pointers → $k = 1024$. 12 direct pointers:

- direct: $12 \times 4$ KB = **48 KB**
- single indirect: $1024 \times 4$ KB = **4 MB**
- double indirect: $1024^2 \times 4$ KB = **4 GB**
- triple indirect: $1024^3 \times 4$ KB = **4 TB**

Total ≈ **4 TB**. Reading a byte at offset 100 KB needs 2 disk reads (the single-indirect block, then the data block).

</div>

## 9.4 Free-space management {#os-9-4}

- **Bitmap:** one bit per block. Compact; easy to find contiguous free runs. A 1 TB disk with 4 KB blocks has $2^{28}$ blocks → a bitmap of $2^{28}$ bits = **32 MB**.
- **Linked list** of free blocks; **grouping** (a free block stores addresses of $n$ free blocks); **counting** (store "start, count" pairs).

## 9.5 Hard links and symbolic links {#os-9-5}

| | Hard link | Symbolic (soft) link |
|---|---|---|
| What it is | another directory entry for the **same inode** | a small file containing a **path** |
| Delete the original | still works (data freed only when link count reaches 0) | **dangles** (broken) |
| Across file systems | no | yes |
| To directories | no | yes |

## 9.6 Open files and caching {#os-9-6}

- A **file descriptor** (an integer) indexes the process's open-file table → the system-wide **open file description** (holds the current **offset**) → the in-memory inode. After `fork` or `dup`, two descriptors share one description, so they share the offset.
- `write` only copies into the kernel's **page cache** and returns; the data reaches the disk later. A crash before that loses it. **`fsync`** forces it to disk.
- The **VFS** (virtual file system) layer gives every file system (ext4, NTFS, NFS, `/proc`) the same interface: "everything is a file".

## 9.7 Crash consistency {#os-9-7}

- **fsck:** scan the whole disk after a crash and repair. Slow on big disks.
- **Journaling** (write-ahead logging): write the intended changes to a journal first, then apply them; after a crash, replay committed entries. Used by ext4, NTFS.
- **Copy-on-write file systems** (ZFS, Btrfs): never overwrite in place; write new blocks, then switch one pointer atomically.

<div class="nb nb-moral">

A file is an inode; names are directory entries pointing to it. Max file size = (direct + k + k² + k³) × block size. `write` reaches the cache; `fsync` reaches the disk; a journal keeps the metadata consistent.

</div>
