@@ exl-dax
**Answer: (c) option 3, `SUMMARIZE(...)`**

**Why.** `SUMMARIZE(table, groupBy columns..., "Name", expression)` groups by the listed columns and adds named aggregate columns: exactly "unique category/subcategory pairs with total sales". `DATATABLE` builds a table from literal values; option 2 passes a bare column where a name/expression pair is needed; `SELECTCOLUMNS` keeps every row instead of grouping.

**Concept: DAX table functions.** DAX (Power BI's formula language) has functions that return tables. SUMMARIZE / SUMMARIZECOLUMNS ≈ SQL's GROUP BY with aggregates; SELECTCOLUMNS ≈ SELECT without grouping; FILTER ≈ WHERE.

@@ exl-powerbi-qa
**Answer: (b) Import**

**Why.** Q&A (natural-language questions in reports) is fully supported on imported data. Live and DirectQuery sources have restrictions, paginated Reporting Services reports have no Q&A, and Q&A is not supported with object-level security.

**Concept: Power BI storage modes.** Import: data copied into Power BI's in-memory engine (fastest, all features). DirectQuery: queries sent to the source each time (always fresh, fewer features). Composite: a mix.

@@ exl-r-installer
**Answer: (c) Rtools**

**Why.** Rtools is the Windows toolchain (compilers, make) needed to build R packages from source. "base" installs R itself; "contrib" holds prebuilt binary packages.

**Concept: building from source.** Packages with C/C++/Fortran code must be compiled; Windows lacks a compiler by default, so R provides Rtools.

@@ exl-solver-integer
**Answer: (a) Relation code 4**

**Why.** SolverAdd's relation codes: 1 is ≤, 2 is =, 3 is ≥, 4 is integer, 5 is binary, 6 is all-different. Code 4 forces the cells to integers.

**Concept: integer constraints in optimisation.** Requiring integer values turns a linear program into an integer program, which Solver handles by branch and bound (slower but exact).

@@ exl-solver-optional
**Answer: (c) FormulaText**

**Why.** `SolverAdd(CellRef, Relation, FormulaText)`: CellRef and Relation are required; FormulaText (the right-hand side) is omitted for the relations int (4), bin (5) and dif (6), which need no value.

**Concept: constraint = left side, relation, right side.** "A1 <= 10" needs all three; "A1 is integer" needs only the cell and the relation.

@@ exl-vlookup
**Answer: (d) range_lookup**

**Why.** The fourth argument decides the match type: FALSE (or 0) means exact match; TRUE (the default) means approximate match on a sorted first column. For IDs you want exact match.

**Concept: VLOOKUP's arguments.** `VLOOKUP(lookup_value, table_array, col_index_num, range_lookup)`: what to find, where (search happens in the first column), which column to return, and exact vs approximate. Forgetting FALSE is a classic bug.

@@ fk-accessibility
**Answer: (d) ensuring readability for colour-blind people**

**Why.** About 1 in 12 men has some colour-vision deficiency. Choose palettes they can tell apart and add redundant cues (labels, patterns, shapes) instead of relying on colour alone.

**Concept: accessible charts.** Good contrast, direct labels, not encoding meaning only in red vs green, and readable font sizes.

@@ fk-comparison
**Answer: (b) pie chart**

**Why.** A pie chart shows parts of one whole; people compare angles poorly, especially across many slices or several pies. Bar and column charts (lengths on a common baseline) are the standard for comparison.

**Concept: chart choice.** Comparison: bar/column. Trend over time: line. Part of a whole: pie (few slices) or stacked bar. Relationship between two variables: scatter. Distribution: histogram or box plot.

@@ fk-email
**Answer: (a) `=CONCAT(LEFT(A2,FIND(".",A2)-1),MID(A2,FIND(".",A2),2),"@example.com")`**

**Why.** `FIND(".", A2)` gives the dot's position. `LEFT(A2, pos − 1)` takes the first name ("ravinder"). `MID(A2, pos, 2)` takes the dot and the next letter (".d"). Then the domain is appended. Option (d) has the same idea, but its second FIND looks for a space, which doesn't occur; (b) and (c) misuse functions (EXTRACT doesn't exist).

**Concept: text functions.** LEFT(text, n), RIGHT(text, n), MID(text, start, n), FIND(what, text) for positions, and & or CONCAT to join.

@@ fk-gauge
**Answer: (d) to show a percentage or value within a range**

**Why.** A gauge (speedometer) shows one value against a scale or target, e.g. 72% of a sales goal.

**Concept: single-value visuals.** Gauges, KPI cards and bullet charts show one number in context; they are not for comparing categories or showing trends.

@@ fk-illustrations
**Answer: (c) Insert tab**

**Why.** Pictures, shapes, icons, SmartArt and charts are all inserted from the Insert tab's Illustrations group.

**Concept: ribbon layout.** Home: formatting and clipboard. Insert: objects and charts. Page Layout: printing setup. Formulas: function library. Data: sorting, filters, imports.

@@ fk-paste
**Answer: (d) Ctrl+V**

**Why.** Ctrl+C copies, Ctrl+X cuts, Ctrl+V pastes. (Ctrl+W closes the window, Ctrl+P prints.)

**Concept: universal shortcuts.** These work in almost every Windows program.

@@ fk-pivot-chart
**Answer: (a) Insert → Column Chart → Stacked Column**

**Why.** The picture has vertical bars, i.e. a column chart. With a single series ("Total"), a stacked column looks the same as a clustered one. Bar charts are horizontal; area and scatter charts don't match.

**Concept: column vs bar.** In Excel, "column" = vertical bars, "bar" = horizontal bars.

@@ fk-subtotal
**Answer: (b) `=SUBTOTAL(9, A1:A5)`**

**Why.** In SUBTOTAL, function number 9 means SUM (10 is VAR). `A1:A5` is the range; `A1,A5` would sum only those two cells.

**Concept: SUBTOTAL.** `SUBTOTAL(function_num, range)`: 1 AVERAGE, 2 COUNT, 9 SUM, etc. It ignores other SUBTOTAL results in the range (no double counting) and, with codes 101–111, also ignores hidden rows.

@@ fk-tab-color
**Answer: (a) Tab Color**

**Why.** Right-click the sheet tab → Tab Color → pick a colour.

**Concept: sheet-level options** (rename, move/copy, tab colour, protect) live on the sheet tab's right-click menu.

@@ fk-undo
**Answer: (c) Ctrl+Z**

**Why.** Ctrl+Z undoes; Ctrl+Y redoes; Ctrl+X cuts; Ctrl+W closes the workbook.

**Concept: undo/redo shortcuts** are the same across Office and most editors.

@@ fk-vlookup
**Answer: (a) `VLookup("ABC-121C", A2:G12, {4,7}, 0)`**

**Why.** The lookup range must start at the ID column (A), because VLOOKUP searches the first column. An array constant {4, 7} as col_index_num returns both column 4 (customer) and column 7 (sales); in Excel 365 the result spills into two cells. (b) and (c) pass five arguments; (d) starts the range at B, where the ID is not.

**Concept: column numbers are relative to the range.** Column 4 of A2:G12 is D. Modern alternative: `XLOOKUP`, which can look left and return several columns.

@@ epam-q7
**Answer: E = 16** (presumably the cut-off fourth option)

**Why.** For a control-flow graph, cyclomatic complexity also equals (decision points + 1): M = 4 + 1 = 5. Then from M = E − V + 2C: E = M + V − 2C = 5 + 13 − 2 = 16. None of the visible 14, 9, 10 satisfies both formulas.

**Concept: cyclomatic complexity.** McCabe's measure of how many independent paths a program has. M = E − N + 2P (edges, nodes, connected components) = decisions + 1. It equals the minimum number of test cases for full branch coverage; above about 10, functions are considered hard to test.

@@ fj-kgp-se1
**Answer: (c) Mediator**

**Why.** The Gang of Four defines Mediator as "an object that encapsulates how a set of objects interact": objects talk to the mediator instead of to each other (like an air-traffic control tower). Observer (ticked in the screenshot) is one-to-many notification, not an object that owns the interaction logic.

**Concept: Mediator vs Observer.** Mediator centralises complex many-to-many communication. Observer lets many listeners subscribe to one subject's changes. Both reduce coupling, in different shapes.

@@ fj-kgp-se2
**Answer: (b) Singleton**

**Why.** A private constructor plus a static accessor that creates the single instance on first use guarantees exactly one instance with global access.

**Concept: Singleton caveats.** Useful for shared resources (config, logger), but it is global state: hard to test and must be made thread-safe (e.g. a function-local static in C++11, which is initialised safely).

@@ fj-kgp-se3
**Answer: (b) combining changes from one branch into another**

**Why.** For example, `git merge feature` while on `main` brings the feature branch's commits into main. If both changed the same lines, you get a merge conflict to resolve.

**Concept: branching workflow.** Create a branch per feature, commit there, then merge (or rebase) back. Merge keeps history as it happened (with a merge commit); rebase rewrites it into a straight line.

@@ fj-kgp-se4
**Answer: (d) Mutable State Principle** (it does not exist)

**Why.** SOLID = Single responsibility, Open–closed, Liskov substitution, Interface segregation, Dependency inversion. (Option (c) is also misnamed: the D is Dependency **Inversion**; dependency injection is a technique for applying it.)

**Concept: dependency inversion.** High-level modules should depend on abstractions (interfaces), not on concrete low-level classes. Dependency injection (passing dependencies in from outside) is how you achieve that.

@@ fj-kgp-se5
**Answer: (c) the number of linearly independent paths through the control flow**

**Why.** McCabe's metric M = E − N + 2P on the control-flow graph; for one function it equals decision points + 1.

**Concept: why it matters.** Higher M = more paths = more tests needed and higher bug risk. Refactor functions with high M into smaller ones.

@@ mw-nitd-22
**Answer: (c) to analyse and detect logical errors**

**Why.** A debugger (gdb, Visual Studio) lets you pause the running program, step through it and inspect variables to find where the logic goes wrong. Syntax errors are reported by the compiler, which also builds the executable. (The candidate's (a) is wrong.)

**Concept: debugging tools.** Breakpoints (stop at a line), stepping (over/into/out), watches (track variables), call stack (how you got here). Compile with `-g` to keep debug information.

@@ exl-dynamics-popup
**Answer: (a) allow pop-ups from `*.businesscentral.dynamics.com`**

**Why.** A pop-up blocker is fixed by allowing pop-ups from the application's own domain; Business Central sandboxes are served from that domain. Network exceptions and certificates have nothing to do with pop-up blocking.

**Concept: match the fix to the layer.** Pop-ups are a browser setting (per site); certificates are about trust/encryption; firewall rules are about network access.

@@ or-cap
**Answer: (b) the trade-offs between consistency, availability and partition tolerance**

**Why.** In a distributed store, network partitions will happen. During one, the system must choose: refuse some requests to stay consistent (CP), or answer everything but possibly with stale data (AP).

**Concept: CAP theorem.** Consistency: every read sees the latest write. Availability: every request gets a response. Partition tolerance: the system keeps working despite lost messages between nodes. Since P is unavoidable, the real choice is C vs A during partitions.

@@ mw-web-30
**Answer: (a) and (d)**

**Why.** `getElementById("test")` returns one element, so `.innerHTML += ...` works (a). `getElementsByName("hacker")` returns a collection, so you need `[0]` first (d); without it (b) sets a property on the collection, changing nothing. `getElementsById` (c) doesn't exist.

**Concept: single element vs collection.** getElementById and querySelector return one element; getElementsByName, getElementsByClassName and querySelectorAll return lists you must index or loop over.

@@ mw-web-31
**Answer: (b) and (d)**

**Why.** `window` is the browser tab/frame: resize, scroll, location, timers (b). `document` is the loaded page (the DOM tree). They are different objects (a false), and each page has exactly one of each, frames aside (d).

**Concept: the browser object model.** window is the global object in browsers; `window.document` is the DOM. Page-content events (clicks on elements) go through the document; browser-level events (resize, load) through window.

@@ mw-web-32
**Answer: (a) function**

**Why.** JavaScript functions are callable objects (they can have properties). `true`, `10` and string values are primitives; they are only wrapped in temporary objects when you call a method on them. (The candidate's extra tick on "string" is wrong.)

**Concept: primitives vs objects.** Primitives: number, string, boolean, null, undefined, symbol, bigint (immutable, compared by value). Everything else, including arrays and functions, is an object (compared by reference).

@@ mw-web-33
**Answer: (b) only** (JSON allows null)

**Why.** JSON has a single number type (no int/float distinction), and `undefined` is not a JSON value. Its value types are string, number, boolean (true/false), null, object and array.

**Concept: JSON vs JavaScript.** JSON is a text format inspired by JS object syntax, but stricter: double-quoted keys and strings, no functions, no undefined, no comments, no trailing commas.

@@ optum-conduit
**Answer (implementation outline).**

**Tier 1 (back end).**
- Add a migration with `viewCount INTEGER NOT NULL DEFAULT 0` on the articles table and declare it in the model.
- Add a route `/articles/:slug/viewed` with PUT or POST (it changes state, so not GET). Decide deliberately whether anonymous readers count (whether it sits behind the auth middleware).
- In the controller, find the article by slug (404 if missing), then increment atomically with `await article.increment("viewCount")`, which issues `UPDATE ... SET viewCount = viewCount + 1`, so concurrent views are not lost. Reload and return the article.
- Make sure the article serialiser includes `viewCount`.

**Tier 2 (front end).** In the article page, call the endpoint once per view in a `useEffect` keyed on the slug (guard with a ref, because React StrictMode runs effects twice in development). Store the returned count in state and show "{viewCount} views" with an icon under the title.

**Tier 3 (categories).** Add a `Category` model (id, unique name, description) with a migration; relate it with `Article.belongsTo(Category)` (one per article) or a join table (many); add `/categories` CRUD routes; accept and validate `categoryId` in article create/update; include the category in responses and support `?category=` filtering; add a category select in the editor and a filter on the home feed. Keep it separate from tags.

**Concept: atomic updates.** "Read count, add 1, save" loses updates when two requests interleave (both read 41, both write 42). Letting the database do `count = count + 1` in one statement makes it atomic. Also: use non-GET methods for anything that changes data, so caches and crawlers don't trigger it.

@@ or-head
**Answer: (c) HEAD**

**Why.** HEAD returns the same headers as GET (size, type, last-modified, ETag) without the body, so you learn about a resource without downloading it.

**Concept: HTTP methods.** GET read, HEAD headers only, POST create/process, PUT replace, PATCH partial update, DELETE remove, OPTIONS ask what is allowed (used in CORS preflight).

@@ or-idempotent
**Answer: (b) calling the method several times has the same effect as calling it once**

**Why.** GET, PUT, DELETE, HEAD and OPTIONS are idempotent: repeating `DELETE /items/5` leaves the same state. POST is not: repeating it can create two orders.

**Concept: why idempotency matters.** Networks fail and clients retry. Idempotent operations are safe to retry; for POST, APIs use idempotency keys so a retried request is recognised and not executed twice.
