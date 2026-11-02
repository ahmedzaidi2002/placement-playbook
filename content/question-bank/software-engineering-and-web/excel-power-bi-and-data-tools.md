---
title: "Excel, Power BI and data tools"
weight: 1
---

17 questions asked by EXL, Flipkart. Try each one first, then open the toggle: it gives the answer, why it is right, and the idea behind it explained from scratch.

### 1 · DAX table of category combinations with sales

*Asked by: EXL (HackerEarth test, 2025)*

Rob wants to create a table with the unique combinations of category and subcategory and
their aggregated sales. Which DAX expression should he use?

1. `DATATABLE(sales, product[Category], product[Subcategory], "Sales Total", SUM(sales[Sales Amount]))`
2. `SUMMARIZECOLUMNS(product[Category], product[Subcategory], sales[Sales Amount])`
3. `SUMMARIZE(sales, product[Category], product[Subcategory], "Sales Total", SUM(sales[Sales Amount]))`
4. `SELECTCOLUMNS(sales, product[Category], product[Subcategory], sales[Sales Amount])`

- **(a)** 1
- **(b)** 2
- **(c)** 3
- **(d)** 4

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) option 3, `SUMMARIZE(...)`**

**Why.** `SUMMARIZE(table, groupBy columns..., "Name", expression)` groups by the listed columns and adds named aggregate columns: exactly "unique category/subcategory pairs with total sales". `DATATABLE` builds a table from literal values; option 2 passes a bare column where a name/expression pair is needed; `SELECTCOLUMNS` keeps every row instead of grouping.

**Concept: DAX table functions.** DAX (Power BI's formula language) has functions that return tables. SUMMARIZE / SUMMARIZECOLUMNS ≈ SQL's GROUP BY with aggregates; SELECTCOLUMNS ≈ SELECT without grouping; FILTER ≈ WHERE.

{{< /details >}}

### 2 · Power BI Q&A and the data model

*Asked by: EXL (HackerEarth test, 2025)*

Bob, new to Power BI, works in the marketing division of a sports-apparel company; his
model has a sales fact table and several dimension tables. The head of marketing wants
self-service analytics through Q&A in the reports. Which configuration allows Q&A to work
in his data model?

- **(a)** Object-level security with any type of data source
- **(b)** Import
- **(c)** Composite models
- **(d)** Reporting Services

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) Import**

**Why.** Q&A (natural-language questions in reports) is fully supported on imported data. Live and DirectQuery sources have restrictions, paginated Reporting Services reports have no Q&A, and Q&A is not supported with object-level security.

**Concept: Power BI storage modes.** Import: data copied into Power BI's in-memory engine (fastest, all features). DirectQuery: queries sent to the source each time (always fresh, fewer features). Composite: a mix.

{{< /details >}}

### 3 · tools to build R packages

*Asked by: EXL (HackerEarth test, 2025)*

Which of the following installers includes tools to build R packages?

- **(a)** Contrib
- **(b)** Base
- **(c)** Rtools
- **(d)** None of these

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) Rtools**

**Why.** Rtools is the Windows toolchain (compilers, make) needed to build R packages from source. "base" installs R itself; "contrib" holds prebuilt binary packages.

**Concept: building from source.** Packages with C/C++/Fortran code must be compiled; Windows lacks a compiler by default, so R provides Rtools.

{{< /details >}}

### 4 · forcing integer cells with SolverAdd

*Asked by: EXL (HackerEarth test, 2025)*

Mary uses Excel macros to optimise a pricing strategy, calling `SolverAdd` to set
constraints. How can she ensure that the final values of the cells referenced by
`CellRef` are integers?

- **(a)** By setting the Relation code to 4
- **(b)** By setting the Relation code to 5
- **(c)** By not specifying the FormulaText parameter
- **(d)** By selecting the Solver option from the Developer tab

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) Relation code 4**

**Why.** SolverAdd's relation codes: 1 is ≤, 2 is =, 3 is ≥, 4 is integer, 5 is binary, 6 is all-different. Code 4 forces the cells to integers.

**Concept: integer constraints in optimisation.** Requiring integer values turns a linear program into an integer program, which Solver handles by branch and bound (slower but exact).

{{< /details >}}

### 5 · optional parameter of SolverAdd

*Asked by: EXL (HackerEarth test, 2025)*

Mike uses Excel macros to find optimal distribution routes. He calls the `SolverAdd`
function to add constraints to his model. Which parameter of `SolverAdd` is optional?

- **(a)** CellRef
- **(b)** Relation
- **(c)** FormulaText
- **(d)** None of these

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) FormulaText**

**Why.** `SolverAdd(CellRef, Relation, FormulaText)`: CellRef and Relation are required; FormulaText (the right-hand side) is omitted for the relations int (4), bin (5) and dif (6), which need no value.

**Concept: constraint = left side, relation, right side.** "A1 <= 10" needs all three; "A1 is integer" needs only the cell and the relation.

{{< /details >}}

### 6 · exact match in VLOOKUP

*Asked by: EXL (HackerEarth test, 2025)*

Mary uses `VLOOKUP` to find the sales representative for each transaction ID. To
ensure accuracy she must state whether an exact or an approximate match is used. Which
parameter of `VLOOKUP` decides this?

- **(a)** lookup_value
- **(b)** table_array
- **(c)** col_index_num
- **(d)** range_lookup

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) range_lookup**

**Why.** The fourth argument decides the match type: FALSE (or 0) means exact match; TRUE (the default) means approximate match on a sorted first column. For IDs you want exact match.

**Concept: VLOOKUP's arguments.** `VLOOKUP(lookup_value, table_array, col_index_num, range_lookup)`: what to find, where (search happens in the first column), which column to return, and exact vs approximate. Forgetting FALSE is a classic bug.

{{< /details >}}

### 7 · accessible visualisation

*Asked by: Flipkart (Neev 2025)*

When designing a data visualisation for a broad audience, what is a key consideration for
ensuring accessibility? (The first option is hidden.)

- **(a)** Using many bright colours
- **(b)** Incorporating interactive features
- **(c)** Including complex statistical analyses
- **(d)** Ensuring readability for color-blind individuals

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) ensuring readability for colour-blind people**

**Why.** About 1 in 12 men has some colour-vision deficiency. Choose palettes they can tell apart and add redundant cues (labels, patterns, shapes) instead of relying on colour alone.

**Concept: accessible charts.** Good contrast, direct labels, not encoding meaning only in red vs green, and readable font sizes.

{{< /details >}}

### 8 · chart unsuitable for comparison

*Asked by: Flipkart (Neev 2025)*

Which type of visualisation is not appropriate if you need to create a comparison chart?

- **(a)** Bar Graph
- **(b)** Pie Chart
- **(c)** Column Chart
- **(d)** Area Chart

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) pie chart**

**Why.** A pie chart shows parts of one whole; people compare angles poorly, especially across many slices or several pies. Bar and column charts (lengths on a common baseline) are the standard for comparison.

**Concept: chart choice.** Comparison: bar/column. Trend over time: line. Part of a whole: pie (few slices) or stacked bar. Relationship between two variables: scatter. Distribution: histogram or box plot.

{{< /details >}}

### 9 · building short e-mail IDs

*Asked by: Flipkart (Neev 2025)*

Column A has e-mails like `ravinder.dasgupta@example.com`; the result should be
`ravinder.d@example.com`. Which formula creates it?

- **(a)** =CONCAT(LEFT(A2,FIND(".",A2)-1),MID(A2,FIND(".",A2),2),"@example.com")
- **(b)** =CONCAT(LEFT(A2,MID(".",A2)-1),FIND(A2,MID(".",A2),2),"@example.com")
- **(c)** =MID(A2,EXTRACT(".",A2)-1)&LEFT(A2,EXTRACT(".",A2),2)&"@example.com"
- **(d)** =LEFT(A2,FIND(".",A2)-1)&MID(A2,FIND(" ",A2),2)&"@example.com"

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) `=CONCAT(LEFT(A2,FIND(".",A2)-1),MID(A2,FIND(".",A2),2),"@example.com")`**

**Why.** `FIND(".", A2)` gives the dot's position. `LEFT(A2, pos − 1)` takes the first name ("ravinder"). `MID(A2, pos, 2)` takes the dot and the next letter (".d"). Then the domain is appended. Option (d) has the same idea, but its second FIND looks for a space, which doesn't occur; (b) and (c) misuse functions (EXTRACT doesn't exist).

**Concept: text functions.** LEFT(text, n), RIGHT(text, n), MID(text, start, n), FIND(what, text) for positions, and & or CONCAT to join.

{{< /details >}}

### 10 · purpose of a gauge chart

*Asked by: Flipkart (Neev 2025)*

The primary purpose of a gauge chart is to:

- **(a)** compare multiple categories of data
- **(b)** show the composition of a whole
- **(c)** display data trends over time
- **(d)** show a percentage or value within a range.

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) to show a percentage or value within a range**

**Why.** A gauge (speedometer) shows one value against a scale or target, e.g. 72% of a sales goal.

**Concept: single-value visuals.** Gauges, KPI cards and bullet charts show one number in context; they are not for comparing categories or showing trends.

{{< /details >}}

### 11 · where the Illustrations group is

*Asked by: Flipkart (Neev 2025)*

In which tab of the Excel ribbon is the Illustrations feature (pictures, shapes, icons)?

- **(a)** Home tab
- **(b)** Page Layout tab
- **(c)** Insert tab
- **(d)** Formulas tab

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) Insert tab**

**Why.** Pictures, shapes, icons, SmartArt and charts are all inserted from the Insert tab's Illustrations group.

**Concept: ribbon layout.** Home: formatting and clipboard. Insert: objects and charts. Page Layout: printing setup. Formulas: function library. Data: sorting, filters, imports.

{{< /details >}}

### 12 · Excel paste shortcut

*Asked by: Flipkart (Neev 2025)*

The keyboard shortcut for pasting the selection in Excel is:

- **(a)** Ctrl+W
- **(b)** Ctrl+P
- **(c)** Ctrl+C
- **(d)** Ctrl+V

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (d) Ctrl+V**

**Why.** Ctrl+C copies, Ctrl+X cuts, Ctrl+V pastes. (Ctrl+W closes the window, Ctrl+P prints.)

**Concept: universal shortcuts.** These work in almost every Windows program.

{{< /details >}}

### 13 · chart from a pivot table

*Asked by: Flipkart (Neev 2025)*

A pivot table sums amounts by status (Completed, Failed, Abandoned; grand total 10400). The
user wants a column chart with one bar per status (series "Total"). What are the steps?

- **(a)** Select the table -> Insert Menu -> select Column Chart option -> select "Stacked Column" from dropdown.
- **(b)** Select the table -> Insert Menu -> select Area Chart option -> select "Stacked Area" from dropdown.
- **(c)** Select the table -> Insert Menu -> select Bar Chart option -> select "Stacked Bar" from dropdown.
- **(d)** Select the table -> Insert Menu -> select Scatter Chart option -> select "Scatter Column Chart" from dropdown.

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) Insert → Column Chart → Stacked Column**

**Why.** The picture has vertical bars, i.e. a column chart. With a single series ("Total"), a stacked column looks the same as a clustered one. Bar charts are horizontal; area and scatter charts don't match.

**Concept: column vs bar.** In Excel, "column" = vertical bars, "bar" = horizontal bars.

{{< /details >}}

### 14 · SUBTOTAL for a total

*Asked by: Flipkart (Neev 2025)*

A1:A5 holds 10, 20, 30, 40, 50 (total 150). Which SUBTOTAL formula computes the total?

- **(a)** =SUBTOTAL(10, A1:A5)
- **(b)** =SUBTOTAL(9, A1:A5)
- **(c)** =SUBTOTAL(10, A1,A5)
- **(d)** =SUBTOTAL(9, A1,A5)

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) `=SUBTOTAL(9, A1:A5)`**

**Why.** In SUBTOTAL, function number 9 means SUM (10 is VAR). `A1:A5` is the range; `A1,A5` would sum only those two cells.

**Concept: SUBTOTAL.** `SUBTOTAL(function_num, range)`: 1 AVERAGE, 2 COUNT, 9 SUM, etc. It ignores other SUBTOTAL results in the range (no double counting) and, with codes 101–111, also ignores hidden rows.

{{< /details >}}

### 15 · colouring a worksheet tab

*Asked by: Flipkart (Neev 2025)*

To change a worksheet tab's colour, right-click the desired worksheet, hover over
_____, and choose a colour from the menu.

- **(a)** Tab Color
- **(b)** Fill
- **(c)** Cell Color
- **(d)** Background Color

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) Tab Color**

**Why.** Right-click the sheet tab → Tab Color → pick a colour.

**Concept: sheet-level options** (rename, move/copy, tab colour, protect) live on the sheet tab's right-click menu.

{{< /details >}}

### 16 · Excel undo shortcut

*Asked by: Flipkart (Neev 2025)*

The keyboard shortcut to undo a recent action in Microsoft Excel is:

- **(a)** Ctrl+X
- **(b)** Ctrl+Y
- **(c)** Ctrl+Z
- **(d)** Ctrl+W

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) Ctrl+Z**

**Why.** Ctrl+Z undoes; Ctrl+Y redoes; Ctrl+X cuts; Ctrl+W closes the workbook.

**Concept: undo/redo shortcuts** are the same across Office and most editors.

{{< /details >}}

### 17 · VLOOKUP returning two columns

*Asked by: Flipkart (Neev 2025)*

A sheet A1:G12 lists transactions: column A the transaction ID (ABC-...), D the customer,
G the sales. Which function extracts the customer and sales values for transaction
ABC-121C?

- **(a)** VLookup("ABC-121C",A2:G12,{4,7},0)
- **(b)** VLookup("ABC-121C",B2:G12,3,6,0)
- **(c)** VLookup("ABC-121C",A2:G12,4,7,0)
- **(d)** VLookup("ABC-121C",B2:G12,{3,6},0)

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) `VLookup("ABC-121C", A2:G12, {4,7}, 0)`**

**Why.** The lookup range must start at the ID column (A), because VLOOKUP searches the first column. An array constant {4, 7} as col_index_num returns both column 4 (customer) and column 7 (sales); in Excel 365 the result spills into two cells. (b) and (c) pass five arguments; (d) starts the range at B, where the ID is not.

**Concept: column numbers are relative to the range.** Column 4 of A2:G12 is D. Modern alternative: `XLOOKUP`, which can look left and return several columns.

{{< /details >}}
