#!/usr/bin/env python3
"""Look for LaTeX that leaked into the generated Markdown (outside math and code).

    python tools/latex2hugo/check.py
"""
import collections
import glob
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
CONTENT = os.path.join(HERE, "..", "..", "content")
SECTIONS = ("core", "projects")

hits = collections.Counter()
examples = {}
paths = [p for sec in SECTIONS
         for p in glob.glob(os.path.join(CONTENT, sec, "**", "*.md"), recursive=True)]
for path in paths:
    text = open(path, encoding="utf8").read()
    text = re.sub(r"(?ms)^(`{3,}).*?^\1\s*$", "", text)       # fenced code
    text = re.sub(r"(?s)\$\$.*?\$\$", "", text)                 # display math
    text = re.sub(r"(`+).+?\1", "", text)                        # code spans
    text = re.sub(r"(?<!\\)\$.+?(?<!\\)\$", "", text)            # inline math
    text = re.sub(r"\{#[^}]*\}", "", text)                       # heading ids
    text = re.sub(r"\{\{<.*?>\}\}", "", text)                    # shortcodes
    for m in re.finditer(r"\\[A-Za-z]{2,}|\{\{|[{}]", text):
        key = m.group(0)
        hits[key] += 1
        if key not in examples:
            line = text[:m.start()].count("\n") + 1
            ctx = text[max(0, m.start() - 60):m.end() + 60].replace("\n", " ")
            examples[key] = "%s:%d  ...%s..." % (os.path.relpath(path, CONTENT), line, ctx)
for key, n in hits.most_common():
    print("%5d  %-12s %s" % (n, key, examples[key]))
