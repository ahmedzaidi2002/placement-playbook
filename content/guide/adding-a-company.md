---
title: Adding a company
weight: 1
---

Create a folder under `content/companies/` and copy this layout:

{{< filetree/container >}}
  {{< filetree/folder name="content/companies/<company>" >}}
    {{< filetree/file name="_index.md" >}}
    {{< filetree/file name="01-<round-one>.md" >}}
    {{< filetree/file name="02-<round-two>.md" >}}
    {{< filetree/file name="questions-asked.md" >}}
    {{< filetree/file name="preparation.md" >}}
    {{< filetree/file name="source-account.md" >}}
  {{< /filetree/folder >}}
{{< /filetree/container >}}

Every page needs a `title` and a `weight` (sidebar order). Then add a card for the company in
`content/companies/_index.md` and, if you want it on the landing page, a feature card in
`content/_index.md`.

The overview page should open with an **at a glance** table and a Mermaid flow of the rounds,
exactly as the [Goldman Sachs overview](/companies/goldman-sachs) does. Run the site with:

```bash
hugo server
```
