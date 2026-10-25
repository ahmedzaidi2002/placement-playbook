---
title: "9 · Low-level design case studies"
linkTitle: "9 LLD case studies"
weight: 9
math: true
---
## 9.1 How to approach an LLD round {#oop-9-1}

1. **Clarify requirements** (5 minutes): core features, actors, scale; agree what is out of scope.
2. **Identify entities** (nouns) and their **attributes**.
3. **Identify behaviours** (verbs) and which class owns each.
4. **Relationships:** is-a (inheritance), has-a (composition), uses (dependency); multiplicities.
5. **Apply patterns** where they fit (Strategy for interchangeable rules, Factory for creation, Observer for notifications, Singleton for a single system object).
6. **Write the key classes and one or two core methods**, then walk through a use case.
7. **Discuss extensions:** concurrency, new types, persistence.

## 9.2 Parking lot {#oop-9-2}

**Requirements:** multiple floors; spots of types small/compact/large; vehicles bike/car/truck; issue a ticket on entry; compute the fee on exit.

| Class | Holds / does |
|---|---|
| `ParkingLot` (Singleton) | list of `Floor`s; `park(vehicle)` → `Ticket`; `unpark(ticket)` → fee |
| `Floor` | list of `Spot`s; find a free spot of a type |
| `Spot` (abstract) → `SmallSpot`, `CompactSpot`, `LargeSpot` | id, type, occupied vehicle; `canFit(vehicle)` |
| `Vehicle` (abstract) → `Bike`, `Car`, `Truck` | number plate, size |
| `Ticket` | id, vehicle, spot, entry time |
| `FeeStrategy` (interface) → `HourlyFee`, `FlatFee` | `fee(ticket, exitTime)` — **Strategy** pattern |
| `SpotAssignmentStrategy` | nearest spot first, or spread evenly — **Strategy** |

**Flow:** a vehicle arrives → the lot asks floors for a free fitting spot (assignment strategy) → marks it occupied → issues a ticket. On exit → the fee strategy computes the amount → spot freed. **Concurrency:** two cars must not get the same spot: lock per floor, or an atomic "try occupy".

## 9.3 Library management {#oop-9-3}

| Class | Holds / does |
|---|---|
| `Library` | catalogue, members; search by title/author/subject |
| `Book` | ISBN, title, authors (the abstract work) |
| `BookItem` | one physical copy: barcode, status (available, loaned, reserved, lost) |
| `Member` → `Student`, `Faculty` | id, borrowed items, limit (different per type) |
| `Loan` | book item, member, issue date, due date; `fine()` |
| `Reservation` | queue of members waiting for a book (**Observer** to notify when available) |
| `FinePolicy` | per-day fine; can differ by member type (**Strategy**) |

Key design point: separate `Book` (one per title) from `BookItem` (one per copy).

## 9.4 Expense sharing (Splitwise) {#oop-9-4}

| Class | Holds / does |
|---|---|
| `User` | id, name |
| `Group` | members, expenses |
| `Expense` | payer, amount, list of `Split`s |
| `Split` (abstract) → `EqualSplit`, `ExactSplit`, `PercentSplit` | user, share; validation (exact shares sum to the amount, percentages to 100) |
| `BalanceSheet` | net balance between every pair of users |
| `SplitFactory` | creates the right `Split` type (**Factory**) |

**Flow:** adding an expense creates splits, validates them, and updates balances (`payer` is owed each share). **Simplify debts:** compute each user's net balance, then repeatedly match the largest creditor with the largest debtor; this needs at most $n - 1$ transactions.

## 9.5 Other common LLD questions {#oop-9-5}

Elevator system (State pattern for each car, a scheduler strategy), vending machine (State), BookMyShow (seat locking to prevent double booking), LRU cache (hash map + doubly linked list), rate limiter (token bucket), chess / tic-tac-toe (Board, Piece hierarchy, Player, move validation), logging framework (Singleton + Chain of Responsibility for levels).

<div class="nb nb-moral">

Requirements → entities → behaviours → relationships → patterns → key classes → walk-through. Strategy for swappable rules, Factory for creation, Observer for notifications, State for lifecycle, and always mention concurrency.

</div>
