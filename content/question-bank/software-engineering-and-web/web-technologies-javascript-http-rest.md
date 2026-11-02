---
title: "Web technologies (JavaScript, HTTP, REST)"
weight: 3
---

7 questions asked by MathWorks, Optum, Oracle. Try each one first, then open the toggle: it gives the answer, why it is right, and the idea behind it explained from scratch.

### 1 · Q30, appending to an element

*Asked by: MathWorks (Test Jul 2024)*

Given `<p id="test" name="hacker">Hello</p>`, which JavaScript snippets append
" Mr. Bob" after "Hello"? (select all)

- **(a)** document.getElementById("test").innerHTML += " Mr. Bob";
- **(b)** document.getElementsByName("hacker").innerHTML += " Mr. Bob";
- **(c)** document.getElementsById("test")[0].innerHTML += " Mr. Bob";
- **(d)** document.getElementsByName("hacker")[0].innerHTML += " Mr. Bob";

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) and (d)**

**Why.** `getElementById("test")` returns one element, so `.innerHTML += ...` works (a). `getElementsByName("hacker")` returns a collection, so you need `[0]` first (d); without it (b) sets a property on the collection, changing nothing. `getElementsById` (c) doesn't exist.

**Concept: single element vs collection.** getElementById and querySelector return one element; getElementsByName, getElementsByClassName and querySelectorAll return lists you must index or loop over.

{{< /details >}}

### 2 · Q31, window and document

*Asked by: MathWorks (Test Jul 2024)*

Which are true about the DOM objects `window` and `document`?

- **(a)** Both represent the same element and are only named differently across browsers
- **(b)** The window element can be used to affect and react to events related to browser behaviour
- **(c)** A document element can be used to affect and react to events related to browser behaviour
- **(d)** Both are singletons within a page (exactly one window and one document instance)

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) and (d)**

**Why.** `window` is the browser tab/frame: resize, scroll, location, timers (b). `document` is the loaded page (the DOM tree). They are different objects (a false), and each page has exactly one of each, frames aside (d).

**Concept: the browser object model.** window is the global object in browsers; `window.document` is the DOM. Page-content events (clicks on elements) go through the document; browser-level events (resize, load) through window.

{{< /details >}}

### 3 · Q32, objects in JavaScript

*Asked by: MathWorks (Test Jul 2024)*

Which of the following is considered an object in JavaScript?

- **(a)** function
- **(b)** true
- **(c)** 10
- **(d)** string

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (a) function**

**Why.** JavaScript functions are callable objects (they can have properties). `true`, `10` and string values are primitives; they are only wrapped in temporary objects when you call a method on them. (The candidate's extra tick on "string" is wrong.)

**Concept: primitives vs objects.** Primitives: number, string, boolean, null, undefined, symbol, bigint (immutable, compared by value). Everything else, including arrays and functions, is an object (compared by reference).

{{< /details >}}

### 4 · Q33, JSON data types

*Asked by: MathWorks (Test Jul 2024)*

Which are true about JSON data types?

- **(a)** JSON makes a distinction between integer and floating-point numbers
- **(b)** JSON allows for the null value
- **(c)** JSON does not allow for the null value
- **(d)** JSON allows for true, false and undefined values

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) only** (JSON allows null)

**Why.** JSON has a single number type (no int/float distinction), and `undefined` is not a JSON value. Its value types are string, number, boolean (true/false), null, object and array.

**Concept: JSON vs JavaScript.** JSON is a text format inspired by JS object syntax, but stricter: double-quoted keys and strings, no functions, no undefined, no comments, no trailing commas.

{{< /details >}}

### 5 · article view counts and categories in the Conduit app

*Asked by: Optum (Full-stack task 2025)*

You are given a working copy of *Conduit*, a Medium-like blogging site. It has an
Express.js back end using the Sequelize ORM and providing a REST API, and a React front
end. Users can sign up and log in, create, edit and delete markdown articles, comment,
follow other users, favourite articles, and filter articles by tag. The database is
seeded with 2 users and 7 articles. Implement four progressive features, each building on
the previous one.

1. **Tier 1, read-only API endpoint for article view count** (back end only).
    Add an integer `viewCount` attribute to the Article model, with default 0.
    Create an API route `/articles/:slug/viewed` that increments the counter when an
    article is viewed. Return `viewCount` with the article data.
2. **Tier 2, display the view count in the UI** (front end only). Every time an
    article is viewed, call the tier-1 API to increment the value by 1. Show a small icon
    and the `viewCount` value (for example "42 views") below the article title.
3. **Tier 3, article categories.** Implement article categories, separate from
    tags. Create a new Category model with attributes for name and description
    [cut off in the source].
4. Tier 4 is not visible in the photos.

Outline how you would implement tiers 1 to 3.

{{< details title="Answer and explanation" closed="true" >}}

**Answer (implementation outline).**

**Tier 1 (back end).**
- Add a migration with `viewCount INTEGER NOT NULL DEFAULT 0` on the articles table and declare it in the model.
- Add a route `/articles/:slug/viewed` with PUT or POST (it changes state, so not GET). Decide deliberately whether anonymous readers count (whether it sits behind the auth middleware).
- In the controller, find the article by slug (404 if missing), then increment atomically with `await article.increment("viewCount")`, which issues `UPDATE ... SET viewCount = viewCount + 1`, so concurrent views are not lost. Reload and return the article.
- Make sure the article serialiser includes `viewCount`.

**Tier 2 (front end).** In the article page, call the endpoint once per view in a `useEffect` keyed on the slug (guard with a ref, because React StrictMode runs effects twice in development). Store the returned count in state and show "{viewCount} views" with an icon under the title.

**Tier 3 (categories).** Add a `Category` model (id, unique name, description) with a migration; relate it with `Article.belongsTo(Category)` (one per article) or a join table (many); add `/categories` CRUD routes; accept and validate `categoryId` in article create/update; include the category in responses and support `?category=` filtering; add a category select in the editor and a filter on the home feed. Keep it separate from tags.

**Concept: atomic updates.** "Read count, add 1, save" loses updates when two requests interleave (both read 41, both write 42). Letting the database do `count = count + 1` in one statement makes it atomic. Also: use non-GET methods for anything that changes data, so caches and crawlers don't trigger it.

{{< /details >}}

### 6 · HTTP metadata

*Asked by: Oracle (HackerRank MCQ test)*

Which HTTP request method is used to retrieve the metadata associated with a resource's
state?

- **(a)** GET
- **(b)** PUT
- **(c)** HEAD
- **(d)** POST

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (c) HEAD**

**Why.** HEAD returns the same headers as GET (size, type, last-modified, ETag) without the body, so you learn about a resource without downloading it.

**Concept: HTTP methods.** GET read, HEAD headers only, POST create/process, PUT replace, PATCH partial update, DELETE remove, OPTIONS ask what is allowed (used in CORS preflight).

{{< /details >}}

### 7 · idempotency in REST

*Asked by: Oracle (HackerRank MCQ test)*

What does idempotency mean in REST API design?

- **(a)** The ability of an API to handle multiple requests in parallel
- **(b)** The property that a method can be called multiple times without different outcomes
- **(c)** The capability of an API to update data
- **(d)** The feature of an API that allows it to delete resources

{{< details title="Answer and explanation" closed="true" >}}

**Answer: (b) calling the method several times has the same effect as calling it once**

**Why.** GET, PUT, DELETE, HEAD and OPTIONS are idempotent: repeating `DELETE /items/5` leaves the same state. POST is not: repeating it can create two orders.

**Concept: why idempotency matters.** Networks fail and clients retry. Idempotent operations are safe to retry; for POST, APIs use idempotency keys so a retried request is recognised and not executed twice.

{{< /details >}}
