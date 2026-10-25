#!/usr/bin/env python3
"""Convert the Napkin-style LaTeX books (core subjects, projects) into Hugo pages.

    python tools/latex2hugo/convert.py            # all books
    python tools/latex2hugo/convert.py dsa os     # some books
    python tools/latex2hugo/convert.py --no-figs  # skip the TikZ -> SVG step

Every book is read from its LaTeX sources, never from the PDF. User macros are expanded
the way TeX would, listings are read from the same code/ files the PDF includes, and every
tikzpicture is compiled with the book's own preamble and turned into an SVG next to its page.
Output: content/<section>/<book>/_index.md plus one page bundle per chapter.
"""
import hashlib
import os
import re
import shutil
import subprocess
import sys
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.abspath(os.path.join(HERE, "..", ".."))
PREP = os.path.abspath(os.path.join(SITE, ".."))
NOTES = os.path.join(PREP, "notes-github")
LOCAL = os.path.join(NOTES, "latex")
# OS, DBMS, CN and COA were written by a cloud session and live only on this branch.
CLOUD_BRANCH = "origin/claude/dreamy-einstein-enzllk"
CLOUD = os.path.join(HERE, ".src", "latex")
CACHE = os.path.join(HERE, ".cache")
CONTENT = os.path.join(SITE, "content")
# the MTP and Transformer books live in the older notes folder (same template)
PROJECT_NOTES = os.path.join(PREP, "notes")

BOOKS = [
    dict(slug="dsa", root=LOCAL, wrapper="book-dsa.tex", short="DSA", weight=1),
    dict(slug="oop-cpp", root=LOCAL, wrapper="book-oops.tex", short="OOP in C++", weight=2,
         split="sections", chapter_file="chapters/08-oops-cpp.tex"),
    dict(slug="os", root=CLOUD, wrapper="book-os.tex", short="OS", weight=3),
    dict(slug="dbms", root=CLOUD, wrapper="book-dbms.tex", short="DBMS", weight=4),
    dict(slug="cn", root=CLOUD, wrapper="book-cn.tex", short="CN", weight=5),
    dict(slug="coa", root=CLOUD, wrapper="book-coa.tex", short="COA", weight=6),
    dict(slug="mtp", root=PROJECT_NOTES, wrapper="book-mtp.tex", short="MTP", weight=1,
         section="projects", split="sections", chapter_file="chapters/01-mtp.tex",
         appendix=["tex/backmatter/notation"], bib="references.bib"),
    dict(slug="transformer", root=PROJECT_NOTES, wrapper="book-transformer.tex",
         short="Transformer", weight=2, section="projects", split="sections",
         chapter_file="chapters/02-transformer-a3.tex",
         appendix=["tex/backmatter/notation"], bib="references.bib"),
]
SECTION_OF = {b["slug"]: b.get("section", "core") for b in BOOKS}
# Core books replaced by hand-written condensed pages; main() will not overwrite them.
CONDENSED = {"dsa", "oop-cpp", "os", "dbms", "cn", "coa"}

LOG = Counter()


def warn(msg):
    LOG[msg] += 1


# ----------------------------------------------------------------------------------------
# Low-level scanning
# ----------------------------------------------------------------------------------------

def read(path):
    with open(path, encoding="utf8", errors="replace") as f:
        return f.read().replace("\r\n", "\n")


LISTING_ENVS = {"cpp", "py", "sql", "sqlx", "cc", "verilog", "vhdl", "lstlisting", "verbatim"}
RAW_ENVS = LISTING_ENVS | {"tikzpicture"}


def strip_comments(s):
    """Drop TeX comments, keeping listing bodies verbatim. A comment also eats the newline
    and the next line's leading blanks, as in TeX."""
    out = []
    raw = None
    lines = s.split("\n")
    join = False
    for line in lines:
        if raw:
            out.append(line)
            if re.search(r"\\end\{%s\}" % re.escape(raw), line):
                raw = None
            continue
        if join:
            line = line.lstrip(" \t")
        m = re.search(r"\\begin\{(%s)\}" % "|".join(sorted(LISTING_ENVS)), line)
        idx = comment_index(line)
        if m and (idx is None or m.start() < idx) and not re.search(
                r"\\end\{%s\}" % m.group(1), line[m.end():]):
            raw = m.group(1)
            out_line = line
            if join and out:
                out[-1] += out_line
            else:
                out.append(out_line)
            join = False
            continue
        if idx is not None:
            piece = line[:idx]
            if join and out:
                out[-1] += piece
            else:
                out.append(piece)
            join = True
        else:
            if join and out:
                out[-1] += line
            else:
                out.append(line)
            join = False
    return "\n".join(out)


def comment_index(line):
    i = 0
    while True:
        i = line.find("%", i)
        if i < 0:
            return None
        k = i - 1
        n = 0
        while k >= 0 and line[k] == "\\":
            n += 1
            k -= 1
        if n % 2 == 0:
            return i
        i += 1


def read_group(s, i):
    """s[i] == '{'; return (content, index after the closing brace)."""
    assert s[i] == "{", (s[i:i + 40])
    depth = 0
    j = i
    while j < len(s):
        c = s[j]
        if c == "\\":
            j += 2
            continue
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return s[i + 1:j], j + 1
        j += 1
    warn("unbalanced group")
    return s[i + 1:], len(s)


def read_opt(s, i):
    """If s[i:] (after blanks) starts with [..], return (content, end) else (None, i)."""
    j = skip_ws(s, i, newlines=True)
    if j >= len(s) or s[j] != "[":
        return None, i
    depth = 0
    bdepth = 0
    k = j
    while k < len(s):
        c = s[k]
        if c == "\\":
            k += 2
            continue
        if c == "{":
            bdepth += 1
        elif c == "}":
            bdepth -= 1
        elif bdepth == 0 and c == "[":
            depth += 1
        elif bdepth == 0 and c == "]":
            depth -= 1
            if depth == 0:
                return s[j + 1:k], k + 1
        k += 1
    return None, i


def skip_ws(s, i, newlines=True):
    while i < len(s) and (s[i] in " \t" or (newlines and s[i] == "\n" and not blank_line_at(s, i))):
        i += 1
    return i


def blank_line_at(s, i):
    """True if s[i] is a newline that starts a blank line (a paragraph break)."""
    j = i + 1
    while j < len(s) and s[j] in " \t":
        j += 1
    return j < len(s) and s[j] == "\n"


def read_arg(s, i):
    """A mandatory argument: a braced group or a single token. Returns (text, end)."""
    j = skip_ws(s, i)
    if j >= len(s):
        return "", j
    if s[j] == "{":
        return read_group(s, j)
    if s[j] == "\\":
        m = re.match(r"\\([A-Za-z@]+|.)", s[j:])
        return m.group(0), j + len(m.group(0))
    return s[j], j + 1


def read_cmd(s, i):
    """s[i] == '\\'; return (name, end). A starred form keeps its name; is_starred() tells."""
    m = re.match(r"\\([A-Za-z@]+)\*?", s[i:])
    if m:
        return m.group(1), i + len(m.group(0))
    return s[i + 1:i + 2], i + 2


def is_starred(s, i, k):
    return s[k - 1] == "*" and re.match(r"\\[A-Za-z@]", s[i:i + 2]) is not None


def find_env_end(s, i, env):
    """i is just after \\begin{env}; return (body_start, body_end, after_end)."""
    depth = 1
    pat = re.compile(r"\\(begin|end)\{%s\}" % re.escape(env))
    for m in pat.finditer(s, i):
        if m.group(1) == "begin":
            depth += 1
        else:
            depth -= 1
            if depth == 0:
                return i, m.start(), m.end()
    warn("unterminated env " + env)
    return i, len(s), len(s)


def split_top(s, sep_re):
    """Split at matches of sep_re that are outside braces and nested environments."""
    parts = []
    depth = 0
    envdepth = 0
    last = 0
    i = 0
    rx = re.compile(sep_re)
    while i < len(s):
        c = s[i]
        if c == "\\":
            if s.startswith("\\begin{", i):
                envdepth += 1
            elif s.startswith("\\end{", i):
                envdepth -= 1
            if depth == 0 and envdepth == 0:
                m = rx.match(s, i)
                if m:
                    parts.append(s[last:i])
                    last = m.end()
                    i = m.end()
                    continue
            i += 2
            continue
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
        elif depth == 0 and envdepth == 0:
            m = rx.match(s, i)
            if m:
                parts.append(s[last:i])
                last = m.end()
                i = m.end()
                continue
        i += 1
    parts.append(s[last:])
    return parts


# ----------------------------------------------------------------------------------------
# Macro expansion (TeX-like, on the source text)
# ----------------------------------------------------------------------------------------

# Rendered by the converter itself, never expanded from their LaTeX definitions.
KEEP = {
    "vocab", "code", "src", "run", "prototype", "onechili", "twochili", "threechili",
    "hrulebar", "stub", "ojoin", "lojoin", "rojoin", "fojoin", "chili", "prechili",
    "listhack", "label", "Cref", "cref", "ref",
}


class Macros:
    def __init__(self):
        self.defs = {}          # name -> (nargs, default_or_None, body)
        self.envs = {}          # env -> (nargs, default, begin, end)
        self.styles = {}        # listings style -> dict of options
        self.lst_envs = {}      # listing env -> options string
        self.languages = {}     # listings language alias -> base

    def scan(self, s, remove=True, raw=None):
        """Record every definition in s; return s without them. raw, if given, collects the
        definition texts (pictures need the chapter's own macros when they are compiled)."""
        out = []
        i = 0
        pat = re.compile(r"\\(newcommand|renewcommand|providecommand|DeclareMathOperator|def|"
                         r"newenvironment|renewenvironment|lstdefinestyle|lstnewenvironment|"
                         r"lstdefinelanguage|newcounter|newcolumntype)\b(\*?)")
        while True:
            m = pat.search(s, i)
            if not m:
                out.append(s[i:])
                break
            out.append(s[i:m.start()])
            kind, star = m.group(1), m.group(2)
            j = m.end()
            try:
                j = self._one(s, j, kind, star)
            except Exception as e:  # noqa: BLE001
                warn("could not parse \\%s near %r (%s)" % (kind, s[m.start():m.start() + 60], e))
                j = m.end()
            if not remove:
                out.append(s[m.start():j])
            if raw is not None and kind not in ("newcounter",):
                raw.append(tex_redefinable(s[m.start():j]))
            i = j
        if raw is not None:
            for m in re.finditer(r"\\(tikzset|usetikzlibrary|pgfplotsset)\s*\{", "".join(out)):
                body, _ = read_group("".join(out), m.end() - 1)
                raw.append("\\%s{%s}" % (m.group(1), body))
        return "".join(out)

    def _one(self, s, j, kind, star):
        if kind in ("newcommand", "renewcommand", "providecommand"):
            j = skip_ws(s, j)
            if s[j] == "{":
                name, j = read_group(s, j)
            else:
                name, j = read_arg(s, j)
            name = name.strip().lstrip("\\")
            nargs, j2 = read_opt(s, j)
            nargs = int(nargs) if nargs else 0
            j = j2
            default, j2 = read_opt(s, j)
            if default is not None:
                j = j2
            body, j = read_arg(s, j)
            if not (kind == "providecommand" and name in self.defs):
                self.defs[name] = (nargs, default, body)
            return j
        if kind == "DeclareMathOperator":
            name, j = read_arg(s, j)
            body, j = read_arg(s, j)
            self.defs[name.strip().lstrip("\\")] = (
                0, None, "\\operatorname%s{%s}" % ("*" if star else "", body))
            return j
        if kind == "def":
            m = re.match(r"\s*\\([A-Za-z@]+)((?:#\d)*)", s[j:])
            name = m.group(1)
            if name == "expandafter":       # \def\expandafter\UrlBreaks...: not a macro we use
                return j
            nargs = len(m.group(2)) // 2
            j += m.end()
            body, j = read_group(s, skip_ws(s, j))
            self.defs[name] = (nargs, None, body)
            return j
        if kind in ("newenvironment", "renewenvironment"):
            name, j = read_arg(s, j)
            nargs, j2 = read_opt(s, j)
            nargs = int(nargs) if nargs else 0
            j = j2
            default, j2 = read_opt(s, j)
            if default is not None:
                j = j2
            begin, j = read_arg(s, j)
            end, j = read_arg(s, j)
            self.envs[name] = (nargs, default, begin, end)
            return j
        if kind == "lstdefinestyle":
            name, j = read_arg(s, j)
            body, j = read_arg(s, j)
            self.styles[name] = parse_keyvals(body)
            return j
        if kind == "lstnewenvironment":
            name, j = read_arg(s, j)
            nargs, j2 = read_opt(s, j)
            j = j2
            default, j2 = read_opt(s, j)
            if default is not None:
                j = j2
            begin, j = read_arg(s, j)
            end, j = read_arg(s, j)
            m = re.search(r"\\lstset\{(.*)\}", begin, re.S)
            self.lst_envs[name] = parse_keyvals(m.group(1)) if m else {}
            LISTING_ENVS.add(name)
            RAW_ENVS.add(name)
            return j
        if kind == "lstdefinelanguage":
            name, j = read_arg(s, j)
            _, j = read_opt(s, j)
            base, j = read_arg(s, j)
            body, j = read_arg(s, j)
            self.languages[name.strip()] = base.strip()
            return j
        if kind == "newcounter":
            _, j = read_arg(s, j)
            _, j2 = read_opt(s, j)
            return j2
        if kind == "newcolumntype":
            _, j = read_arg(s, j)
            _, j = read_arg(s, j)
            return j
        raise ValueError(kind)


def tex_redefinable(d):
    """\\newcommand{\\x}... -> \\providecommand{\\x}{}\\renewcommand{\\x}..., so that a
    definition can be repeated inside each picture's group without clashing."""
    m = re.match(r"\\newcommand\*?\s*\{?\\([A-Za-z@]+)\}?", d)
    if m:
        return "\\providecommand{\\%s}{}\\renew%s" % (m.group(1), d[4:])
    return d


def parse_keyvals(body):
    """listings options 'a=b, c={d,e}, f' -> dict."""
    out = {}
    for part in split_top(body, r","):
        part = part.strip()
        if not part:
            continue
        if "=" in part:
            k, v = part.split("=", 1)
            v = v.strip()
            if v.startswith("{") and v.endswith("}"):
                v = v[1:-1]
            out[k.strip()] = v
        else:
            out[part] = ""
    return out


class Expander:
    def __init__(self, macros, root):
        self.m = macros
        self.root = root

    def resolve(self, path):
        path = path.strip()
        for cand in (path, path + ".tex"):
            p = os.path.join(self.root, cand)
            if os.path.isfile(p):
                return p
        return None

    def expand(self, s, depth=0):
        if depth > 40:
            warn("macro recursion too deep")
            return s
        out = []
        i = 0
        n = len(s)
        while i < n:
            j = s.find("\\", i)
            if j < 0:
                out.append(s[i:])
                break
            out.append(s[i:j])
            name, k = read_cmd(s, j)
            if name == "begin":
                env, k2 = read_arg(s, k)
                if env in RAW_ENVS:
                    _, bend, after = find_env_end(s, k2, env)
                    out.append(s[j:after])
                    i = after
                    continue
                if env in self.m.envs and env not in BOX_KINDS:
                    nargs, default, begin, end = self.m.envs[env]
                    args, k3 = self._args(s, k2, nargs, default)
                    bstart, bend, after = find_env_end(s, k3, env)
                    body = s[bstart:bend]
                    out.append(self.expand(subst(begin, args) + body + subst(end, args), depth + 1))
                    i = after
                    continue
                out.append(s[j:k2])
                i = k2
                continue
            if name in ("input", "inputrows"):
                arg, k2 = read_arg(s, k)
                path = self.expand(arg, depth + 1)
                p = self.resolve(path)
                if p is None:
                    warn("missing input " + path)
                    i = k2
                    continue
                out.append(self.expand(strip_comments(self.m.scan(read(p))), depth + 1))
                i = k2
                continue
            if name == "csname" and s.startswith("@@input\\endcsname", skip_ws(s, k)):
                k2 = skip_ws(s, k) + len("@@input\\endcsname")
                m = re.match(r"\s*(\S+)", s[k2:])
                path = self.expand(m.group(1), depth + 1)
                p = self.resolve(path)
                if p:
                    out.append(self.expand(strip_comments(self.m.scan(read(p))), depth + 1))
                else:
                    warn("missing input " + path)
                i = k2 + m.end()
                continue
            if name == "IfFileExists":
                path, k2 = read_arg(s, k)
                yes, k3 = read_arg(s, k2)
                no, k4 = read_arg(s, k3)
                path = self.expand(path, depth + 1)
                hit = os.path.isfile(os.path.join(self.root, path.strip()))
                out.append(self.expand(yes if hit else no, depth + 1))
                i = k4
                continue
            if name == "ifdefined":
                m = re.match(r"\s*\\([A-Za-z@]+)", s[k:])
                test = m.group(1)
                yes, no, after = split_conditional(s, k + m.end())
                hit = test in self.m.defs or test in self.m.envs
                out.append(self.expand(yes if hit else no, depth + 1))
                i = after
                continue
            if name == "detokenize":
                arg, k2 = read_arg(s, k)
                out.append(self.expand(arg, depth + 1))
                i = k2
                continue
            if name in self.m.defs and name not in KEEP:
                nargs, default, body = self.m.defs[name]
                args, k2 = self._args(s, k, nargs, default)
                out.append(self.expand(subst(body, args), depth + 1))
                i = k2
                continue
            out.append(s[j:k])
            # \ttfamily\detokenize{crc}: keep the control word apart from expanded letters
            if k < n and s[k] == "\\" and re.match(r"\\[A-Za-z@]+$", s[j:k]):
                out.append(" ")
            i = k
        return "".join(out)

    def _args(self, s, k, nargs, default):
        args = []
        if nargs and default is not None:
            opt, k2 = read_opt(s, k)
            if opt is None:
                args.append(default)
            else:
                args.append(opt)
                k = k2
            nargs -= 1
        for _ in range(nargs):
            a, k = read_arg(s, k)
            args.append(a)
        return args, k


def subst(body, args):
    def rep(m):
        if m.group(0) == "##":
            return "#"
        idx = int(m.group(1)) - 1
        return args[idx] if idx < len(args) else ""
    return re.sub(r"##|#(\d)", rep, body)


# ----------------------------------------------------------------------------------------
# Numbering, labels and the page model
# ----------------------------------------------------------------------------------------

BOX_KINDS = {
    # env: (display name, counter, layout)  layout: block = title on its own line
    "theorem": ("Theorem", "thm", "block"),
    "lemma": ("Lemma", "thm", "block"),
    "proposition": ("Proposition", "thm", "block"),
    "corollary": ("Corollary", "thm", "block"),
    "example": ("Example", "thm", "block"),
    "definition": ("Definition", "thm", "runin"),
    "fact": ("Fact", "thm", "runin"),
    "claim": ("Claim", "thm", "runin"),
    "abuse": ("Abuse of Notation", "thm", "runin"),
    "remark": ("Remark", "thm", "runin"),
    "remark*": ("Remark", None, "runin"),
    "algo": ("Algorithm", "thm", "runin"),
    "ques": ("Question", "thm", "runin"),
    "exercise": ("Exercise", "thm", "runin"),
    "step": ("Step", "step", "runin"),
    "problem": ("Problem", "prob", "block"),
    "sproblem": ("Problem", "prob", "block"),
    "dproblem": ("Problem", "prob", "block"),
    "proof": ("Proof", None, "proof"),
    "moral": ("", None, "moral"),
}
CSS_KIND = {
    "lemma": "theorem", "proposition": "theorem", "corollary": "theorem",
    "fact": "definition", "claim": "definition", "abuse": "definition",
    "remark*": "remark", "algo": "remark", "step": "remark", "exercise": "ques",
    "sproblem": "problem", "dproblem": "problem",
}
PLURAL = {"Section": "Sections", "Chapter": "Chapters", "Theorem": "Theorems",
          "Problem": "Problems", "Definition": "Definitions", "Fact": "Facts",
          "Remark": "Remarks", "Example": "Examples", "Algorithm": "Algorithms",
          "Table": "Tables", "Figure": "Figures", "Lemma": "Lemmas",
          "Proposition": "Propositions", "Question": "Questions", "Claim": "Claims",
          "Corollary": "Corollaries", "Appendix": "Appendices"}


def anchor_of(label):
    return re.sub(r"[^A-Za-z0-9]+", "-", label).strip("-").lower()


class Book:
    def __init__(self, cfg):
        self.cfg = cfg
        self.slug = cfg["slug"]
        self.root = cfg["root"]
        self.split = cfg.get("split", "chapters")
        self.labels = {}   # label -> (kind, number, page_slug, anchor)
        self.figs = []     # (page_slug, index, tikz source)
        self.preamble = ""
        self.local_defs = []
        self.problem_style = "alpha"
        self.title = self.subtitle = self.about = ""
        self.pages = []    # dicts: slug, title, weight, part, src, number
        self.intro = ""
        self.bib = {}      # key -> entry fields plus "label" and "short"
        self.cited = set()


# ----------------------------------------------------------------------------------------
# Rendering LaTeX -> Markdown
# ----------------------------------------------------------------------------------------

TEXT_SYMBOLS = {
    "ldots": "…", "dots": "…", "textellipsis": "…", "S": "§", "textbackslash": "&#92;",
    "textasciitilde": "~", "textless": "&lt;", "textgreater": "&gt;", "textbar": "&#124;",
    "slash": "/", "quad": " ", "qquad": "  ", "enspace": " ", "thinspace": " ",
    "LaTeX": "LaTeX", "TeX": "TeX", "textendash": "–", "textemdash": "—", "dag": "†",
    "ddag": "‡", "copyright": "©", "textregistered": "®", "texttrademark": "™",
    "textdegree": "°", "times": "×", "checkmark": "✓", "textbullet": "•", "pounds": "£",
    "euro": "€", "textquotedbl": '"', "textquotesingle": "'", "_": "\\_", "&": "&amp;",
    "%": "%", "#": "\\#", "$": "&#36;", "{": "{", "}": "}", " ": " ", "\n": " ", "\t": " ",
    ",": " ", ";": " ",
    ":": " ", "!": "", "/": "", "-": "", "@": "", "\\": "<br>", "o": "ø",
    "i": "i", "ss": "ß", "textunderscore": "\\_", "lq": "‘", "rq": "’", "space": " ",
    "L": "Ł", "l": "ł", "O": "Ø", "aa": "å", "AA": "Å", "ae": "æ",
    "nobreakspace": " ", "textsection": "§", "P": "¶", "textasciicircum": "^",
    "arraybackslash": "", "tabularnewline": "<br>", "newline": "<br>", "linebreak": " ",
    "bullet": "•", "cdot": "·", "to": "→", "rightarrow": "→", "leftarrow": "←",
    "Rightarrow": "⇒", "ge": "≥", "le": "≤", "ne": "≠", "approx": "≈",
}
DROP0 = {
    "centering", "raggedright", "raggedleft", "footnotesize", "small", "scriptsize", "tiny",
    "normalsize", "large", "Large", "LARGE", "huge", "Huge", "leavevmode", "noindent",
    "indent", "smallskip", "medskip", "bigskip", "hfill", "vfill", "clearpage", "newpage",
    "cleardoublepage", "pagebreak", "nopagebreak", "ttfamily", "bfseries", "itshape",
    "rmfamily", "sffamily", "normalfont", "mdseries", "upshape", "relax", "protect",
    "nobreak", "allowbreak", "displaystyle", "strut", "break", "null", "empty",
    "frenchspacing", "sloppy", "fussy", "selectfont", "unskip", "ignorespaces", "par@",
    "toprule", "midrule", "bottomrule", "hline", "addlinespace", "listhack", "appendix",
    "maketitle", "tableofcontents", "mainmatter", "frontmatter", "backmatter",
    "prechili", "chili", "item@", "endcsname", "fi", "else", "hss", "vss",
    "makeatletter", "makeatother", "raggedbottom", "flushbottom", "printbibliography",
}
DROP1 = {
    "hspace", "vspace", "Needspace", "needspace", "color", "pagestyle", "thispagestyle",
    "enlargethispage", "stepcounter", "refstepcounter", "pageref", "usetikzlibrary",
    "tikzset", "pgfplotsset", "usepackage", "cmidrule", "cline", "rowcolor", "phantomsection",
    "addcontentsline@", "markboth@", "label@", "index", "nocite", "bibliographystyle",
    "vphantom", "phantom", "hphantom", "linewidth", "marginpar",
}
DROP2 = {"setlength", "setcounter", "addtocounter", "addtolength", "addcontentsline"}
WRAP1 = {
    "textbf": ("<strong>", "</strong>"), "textit": ("<em>", "</em>"), "emph": ("<em>", "</em>"),
    "textsl": ("<em>", "</em>"), "underline": ("<u>", "</u>"), "uline": ("<u>", "</u>"),
    "dashuline": ("<u>", "</u>"), "textsc": ("", ""), "textsf": ("", ""), "textrm": ("", ""),
    "textup": ("", ""), "textmd": ("", ""), "textnormal": ("", ""), "mbox": ("", ""),
    "hbox": ("", ""), "text": ("", ""), "fbox": ("", ""), "ensuremath": ("", ""),
    "textsuperscript": ("<sup>", "</sup>"), "textsubscript": ("<sub>", "</sub>"),
    "vocab": ("<strong>", "</strong>"), "strong": ("<strong>", "</strong>"),
    "mbox@": ("", ""), "makebox": ("", ""), "parbox@": ("", ""), "framebox": ("", ""),
}

MATH_ENVS = {"equation", "equation*", "align", "align*", "gather", "gather*", "multline",
             "multline*", "eqnarray", "eqnarray*", "displaymath", "flalign", "flalign*",
             "alignat", "alignat*"}
LIST_ENVS = {"itemize", "enumerate", "description", "compactitem", "compactenum"}
UNWRAP_ENVS = {"center", "flushleft", "flushright", "minipage", "table", "table*", "figure",
               "figure*", "small", "footnotesize", "scriptsize", "samepage", "adjustbox",
               "raggedright", "quote", "quotation", "spacing", "tcolorbox", "multicols",
               "wrapfigure", "subfigure", "sidewaystable", "landscape", "scope"}
TABLE_ENVS = {"tabular", "tabularx", "tabular*", "longtable", "tabulary", "array"}


class Page:
    def __init__(self, book, slug, number):
        self.book = book
        self.slug = slug
        self.number = number
        self.figs = 0
        self.defs = []      # the chapter's own definitions, for compiling its pictures
        self.assets = []    # (source file, name in the page bundle) from \\includegraphics


class Ctx:
    """Rendering state for one book; numbering state persists across pages."""

    def __init__(self, book, macros, collect):
        self.book = book
        self.m = macros
        self.collect = collect        # pass 1: only gather labels
        self.page = None
        self.chapter = 0
        self.section = 0
        self.subsection = 0
        self.counters = Counter()
        self.tables = 0
        self.figures = 0
        self.saved = {}               # enumerate counters saved with \setcounter{x}{\value{enumi}}
        self.last_anchor = None       # where a following \label attaches
        self.used_ids = set()
        self.in_table = False
        self.float_kind = None        # "Table" or "Figure" while inside that float
        self.heading_shift = 0        # sections-mode books: \section is the page title

    # ---- labels -------------------------------------------------------------------------
    def set_label(self, label, kind, number, anchor):
        if self.collect:
            self.book.labels[label] = (kind, number, self.page.slug, anchor)

    def new_id(self, base):
        base = anchor_of(base) or "x"
        cand = base
        n = 2
        while cand in self.used_ids:
            cand = "%s-%d" % (base, n)
            n += 1
        self.used_ids.add(cand)
        return cand

    # ---- numbers ------------------------------------------------------------------------
    def sec_number(self):
        return "%s.%d" % (self.chapter, self.section)

    def thm_number(self):
        self.counters["thm"] += 1
        return "%s.%d" % (self.sec_number(), self.counters["thm"])

    def prob_number(self):
        self.counters["prob"] += 1
        k = self.counters["prob"]
        if self.book.problem_style == "alpha":
            return "%s%s" % (self.chapter, alpha(k))
        return "%s.%d" % (self.chapter, k)


def alpha(k):
    s = ""
    while k:
        k, r = divmod(k - 1, 26)
        s = chr(65 + r) + s
    return s


def roman(k):
    vals = [(10, "x"), (9, "ix"), (5, "v"), (4, "iv"), (1, "i")]
    out = ""
    for v, r in vals:
        while k >= v:
            out += r
            k -= v
    return out


ALL_LABELS = {}   # book slug -> labels dict (for references across books)

# dvipsnames colours that carry meaning in the books (evidence levels in the MTP book)
CSS_COLORS = {"ForestGreen": "#009b55", "RoyalBlue": "#0071bc", "BurntOrange": "#f7921d",
              "red": "#d62728", "blue": "#1f5fbf", "MidnightBlue": "#006795",
              "RawSienna": "#974006", "purple": "#8c2b8c", "orange": "#e8740c"}


def split_conditional(s, i):
    """After \\ifdefined\\x: return (true branch, false branch, index after \\fi)."""
    depth = 1
    mid = None
    for m in re.compile(r"\\(if[A-Za-z]*|else|fi)(?![A-Za-z])").finditer(s, i):
        w = m.group(1)
        if w == "fi":
            depth -= 1
            if depth == 0:
                if mid is None:
                    return s[i:m.start()], "", m.end()
                return s[i:mid[0]], s[mid[1]:m.start()], m.end()
        elif w == "else":
            if depth == 1:
                mid = (m.start(), m.end())
        else:
            depth += 1
    warn("unterminated \\ifdefined")
    return s[i:], "", len(s)


class Renderer:
    def __init__(self, ctx):
        self.c = ctx

    # ================================ blocks ============================================
    def blocks(self, s):
        """Render a run of LaTeX as Markdown blocks separated by blank lines."""
        c = self.c
        out = []          # finished blocks
        para = []         # inline pieces of the current paragraph
        i = 0
        n = len(s)

        def flush():
            text = "".join(para)
            para.clear()
            text = tidy_inline(text)
            if text:
                out.append(escape_para_start(text))

        while i < n:
            ch = s[i]
            if ch == "\n" and blank_line_at(s, i):
                flush()
                i += 1
                continue
            if ch == "$" and s.startswith("$$", i):
                end = s.find("$$", i + 2)
                flush()
                out.append(self.display_math(s[i + 2:end]))
                i = end + 2
                continue
            if ch == "\\" and i + 1 < n and s[i + 1] == "[":
                end = find_display_end(s, i + 2)
                flush()
                out.append(self.display_math(s[i + 2:end]))
                i = end + 2
                continue
            if ch == "\\":
                name, k = read_cmd(s, i)
                starred = is_starred(s, i, k)
                base = name
                if base in ("chapter", "section", "subsection", "subsubsection"):
                    flush()
                    opt, k = read_opt(s, k)
                    title, k = read_arg(s, k)
                    out.append(self.heading(base, title, starred, s, k))
                    i = k
                    continue
                if base == "part":
                    flush()
                    _, k = read_opt(s, k)
                    _, k = read_arg(s, k)
                    i = k
                    continue
                if base == "paragraph":
                    flush()
                    title, k = read_arg(s, k)
                    para.append("<strong>%s</strong> " % self.inline(title).strip())
                    i = k
                    continue
                if base == "par":
                    flush()
                    i = k
                    continue
                if base == "begin":
                    env, k2 = read_arg(s, k)
                    bstart, bend, after = find_env_end(s, k2, env)
                    body = s[bstart:bend]
                    md = self.environment(env, body, para)
                    if md is None:          # inline environment, already appended to para
                        i = after
                        continue
                    flush()
                    if md:
                        out.append(md)
                    i = after
                    continue
                if base == "lstinputlisting":
                    flush()
                    opt, k = read_opt(s, k)
                    path, k = read_arg(s, k)
                    out.append(self.listing_file(opt or "", path))
                    i = k
                    continue
                if base == "caption":
                    flush()
                    _, k = read_opt(s, k)
                    text, k = read_arg(s, k)
                    out.append(self.caption(text))
                    i = k
                    continue
                if base == "hrulebar":
                    flush()
                    out.append("---")
                    i = k
                    continue
                if base == "label":
                    lab, k = read_arg(s, k)
                    self.attach_label(lab.strip())
                    i = k
                    continue
                if base == "prototype":
                    flush()
                    arg, k = read_arg(s, k)
                    out.append(html_wrap("nb-proto", "<em><span>Prototypical example for this "
                                         "section:</span> %s</em>" % self.inline(arg)))
                    i = k
                    continue
                if base == "stub":
                    flush()
                    arg, k = read_arg(s, k)
                    out.append(html_wrap("nb-stub", "<em>To write: %s</em>" % self.inline(arg)))
                    i = k
                    continue
                if base in ("item", "ii"):
                    warn("item outside a list")
                    i = k
                    continue
            # inline material: take one inline token
            piece, i = self.inline_token(s, i)
            para.append(piece)
        flush()
        return "\n\n".join(b for b in out if b.strip())

    def attach_label(self, lab):
        c = self.c
        tgt = c.last_anchor
        if tgt is None:
            warn("label with nothing to attach: " + lab)
            return
        kind, number, anchor = tgt
        c.set_label(lab, kind, number, anchor)

    def heading(self, cmd, title, starred, s, k):
        c = self.c
        level = {"chapter": 1, "section": 2, "subsection": 3, "subsubsection": 4}[cmd]
        level -= c.heading_shift
        if cmd == "chapter" or level <= 1:
            # the page title; counted when the page started
            c.last_anchor = ("Chapter", str(c.chapter), "")
            if c.heading_shift:
                c.last_anchor = ("Section", c.sec_number(), "")
            return ""
        text = self.inline(title).strip()
        if cmd == "section":
            if not starred:
                c.section += 1
                c.subsection = 0
                c.counters["thm"] = 0
                num = c.sec_number()
            else:
                num = None
            kind = "Section"
        elif cmd == "subsection":
            if not starred:
                c.subsection += 1
                num = "%s.%s" % (c.sec_number(), roman(c.subsection))
            else:
                num = None
            kind = "Section"
        else:
            num = None
            kind = "Section"
        # a \label right after the heading names it
        m = re.match(r"\s*\\label\{([^}]*)\}", s[k:])
        hid = c.new_id(m.group(1) if m else (("s" + num) if num else text))
        c.last_anchor = (kind, num or text, hid)
        label = ("%s " % num) if num else ""
        return "%s %s%s {#%s}" % ("#" * level, label, text, hid)

    # ---------------------------------------------------------------- environments ----
    def environment(self, env, body, para):
        c = self.c
        if env in BOX_KINDS:
            return self.box(env, body)
        if env in ("hint", "sol"):
            return self.details("Hint" if env == "hint" else "Solution", env, body)
        if env in LIST_ENVS:
            return self.lst(env, body)
        if env in TABLE_ENVS:
            return self.table(env, body)
        if env == "tikzpicture":
            return self.figure("\\begin{tikzpicture}" + body + "\\end{tikzpicture}")
        if env in LISTING_ENVS:
            opts = c.m.lst_envs.get(env, {})
            o, k = read_opt(body, 0)
            extra = {}
            if o is not None:
                extra = parse_keyvals(o)
                body = body[k:]
            opts = dict(opts, **extra)
            body = body.lstrip("\n").rstrip()
            body = dedent_listing(body)
            return code_fence(body, self.lang_of(opts, env), self.listing_title(opts), opts)
        if env in MATH_ENVS:
            inner = body
            if env.startswith("equation") or env == "displaymath":
                return self.display_math(inner)
            name = env if env.endswith("*") else env + "*"
            if name.startswith("eqnarray"):
                name = "align*"
            return self.display_math("\\begin{%s}%s\\end{%s}" % (name, inner, name))
        if env in UNWRAP_ENVS:
            if env in ("table", "table*", "figure", "figure*"):
                o, k = read_opt(body, 0)
                if o is not None:
                    body = body[k:]
            if env == "minipage":
                o, k = read_opt(body, 0)
                if o is not None:
                    body = body[k:]
                _, k = read_arg(body, 0)
                body = body[k:]
            if env in ("quote", "quotation"):
                inner = self.blocks(body)
                return "\n".join("> " + ln if ln else ">" for ln in inner.split("\n"))
            if env == "tcolorbox":
                o, k = read_opt(body, 0)
                if o is not None:
                    body = body[k:]
            if env.startswith(("table", "figure")):
                saved = c.float_kind
                c.float_kind = "Table" if env.startswith("table") else "Figure"
                md = self.blocks(body)
                c.float_kind = saved
                return md
            return self.blocks(body)
        if env == "axis":
            warn("axis outside tikzpicture")
            return ""
        warn("unknown environment " + env)
        return self.blocks(body)

    def box(self, env, body):
        c = self.c
        name, counter, layout = BOX_KINDS[env]
        title, k = read_opt(body, 0)
        if title is not None:
            body = body[k:]
        chili = ""
        m = re.search(r"\\(one|two|three)chili", body)
        if m:
            chili = " " + "🌶" * {"one": 1, "two": 2, "three": 3}[m.group(1)]
            body = re.sub(r"\\(one|two|three)chili", "", body)
        if counter == "thm":
            num = c.thm_number()
        elif counter == "prob":
            num = c.prob_number()
            if env == "sproblem":
                num += "★"
            elif env == "dproblem":
                num += "†"
        elif counter == "step":
            c.counters["step"] += 1
            num = str(c.counters["step"])
        else:
            num = None
        kindcss = CSS_KIND.get(env, env)
        hid = None
        if num:
            hid = c.new_id(name.lower() + "-" + num)
        saved_anchor = c.last_anchor
        c.last_anchor = (name, num, hid) if num else saved_anchor
        # a label at the very start of the body names the box
        lm = re.match(r"\s*\\label\{([^}]*)\}", body)
        if lm and num:
            c.set_label(lm.group(1).strip(), name, num, hid)
            body = body[lm.end():]
        inner = self.blocks(body)
        c.last_anchor = saved_anchor if not num else c.last_anchor
        head = ""
        ttl = self.inline(title).strip() if title else ""
        if layout == "moral":
            return '<div class="nb nb-moral">\n\n%s\n\n</div>' % inner
        if layout == "proof":
            label = "<em>%s.</em>" % (ttl or "Proof")
            inner = prefix_first_para(inner, label + " ")
            return '<div class="nb nb-proof">\n\n%s\n\n</div>' % inner
        label = "<strong>%s%s</strong>%s" % (name, (" " + num) if num else "", chili)
        if ttl:
            label += " (%s)" % ttl
        if layout == "block":
            # first paragraph of a block box is its title line (styled in custom.css)
            content = label + "\n\n" + inner
            kindcss += " nb-block"
        else:
            sep = " — " if kindcss in ("remark", "ques") else ". "
            content = prefix_first_para(inner, label + sep)
        idattr = ' id="%s"' % hid if hid else ""
        return '<div class="nb nb-%s"%s>\n\n%s\n\n</div>' % (kindcss, idattr, content)

    def details(self, summary, cls, body):
        inner = self.blocks(body)
        return ('<details class="nb-%s">\n<summary>%s</summary>\n\n%s\n\n</details>'
                % (cls, summary, inner))

    # ---------------------------------------------------------------- lists ----------
    def lst(self, env, body):
        c = self.c
        ordered = env in ("enumerate", "compactenum")
        desc = env == "description"
        _, k = read_opt(body, 0)        # enumitem options
        if _ is not None:
            body = body[k:]
        start = 1
        m = re.match(r"\s*\\setcounter\{enumi\}\{\\value\{([^}]*)\}\}", body)
        if m:
            start = c.saved.get(m.group(1), 0) + 1
            body = body[m.end():]
        m = re.match(r"\s*\\setcounter\{enumi\}\{(\d+)\}", body)
        if m:
            start = int(m.group(1)) + 1
            body = body[m.end():]
        tail_save = None
        m = re.search(r"\\setcounter\{([^}]*)\}\{\\value\{enumi\}\}\s*$", body)
        if m:
            tail_save = m.group(1)
            body = body[:m.start()]
        items = split_top(body, r"\\(?:item|ii)\b\*?")
        items = items[1:]  # text before the first \item
        lines = []
        num = start
        for it in items:
            label, k = (None, 0)
            if it.lstrip().startswith("["):
                label, k = read_opt(it, 0)
                it = it[k:]
            md = self.blocks(it)
            if ordered and label is None:
                marker = "%d. " % num
            else:
                marker = "- "
            if label is not None:
                md = prefix_first_para(md, "<strong>%s</strong> " % self.inline(label).strip())
            num += 1
            md_lines = md.split("\n") if md else [""]
            pad = " " * len(marker)
            lines.append(marker + md_lines[0])
            for ln in md_lines[1:]:
                lines.append((pad + ln) if ln.strip() else "")
        if tail_save:
            c.saved[tail_save] = num - 1
        if not items:
            warn("list without items")
        return "\n".join(lines)

    # ---------------------------------------------------------------- tables ---------
    def table(self, env, body):
        c = self.c
        if env == "tabularx" or env == "tabular*":
            _, k = read_arg(body, 0)       # width
            body = body[k:]
        o, k = read_opt(body, 0)
        if o is not None:
            body = body[k:]
        spec, k = read_arg(body, 0)
        body = body[k:]
        aligns = parse_colspec(spec)
        # drop rules, keep the position of the first \midrule
        body = re.sub(r"\\cmidrule(\([a-z]*\))?\{[^}]*\}", "", body)
        body = re.sub(r"\\(cline|rowcolor)\{[^}]*\}", "", body)
        body = re.sub(r"\\(addlinespace)(\[[^\]]*\])?", "", body)
        mid = body.find("\\midrule")
        if mid < 0:
            mid = None
        rows = []
        header_rows = 0
        for raw in split_top(body, r"\\\\(\[[^\]]*\])?|\\tabularnewline"):
            has_mid = "\\midrule" in raw or "\\hline" in raw
            raw_clean = re.sub(r"\\(toprule|midrule|bottomrule|hline)(\[[^\]]*\])?", "", raw)
            if has_mid and header_rows == 0 and rows and "\\midrule" in raw:
                header_rows = len(rows)
            if not raw_clean.strip():
                continue
            cells = split_top(raw_clean, r"&")
            row = []
            for cell in cells:
                mm = re.match(r"\s*\\multicolumn\{(\d+)\}", cell)
                span = 1
                if mm:
                    span = int(mm.group(1))
                    _, k1 = read_arg(cell, mm.end())   # spec
                    text, k2 = read_arg(cell, k1)
                    cell = text
                mr = re.match(r"\s*\\multirow\{[^}]*\}\{[^}]*\}", cell)
                if mr:
                    text, _ = read_arg(cell, mr.end())
                    cell = text
                c.in_table = True
                txt = self.blocks(cell)
                c.in_table = False
                txt = re.sub(r"\n\n+", "<br>", txt).replace("\n", " ").strip()
                row.append(txt)
                row.extend([""] * (span - 1))
            rows.append(row)
        if not rows:
            return ""
        if header_rows == 0:
            header_rows = 1
        ncol = max(len(r) for r in rows)
        rows = [r + [""] * (ncol - len(r)) for r in rows]
        while len(aligns) < ncol:
            aligns.append("l")
        head = rows[:header_rows]
        if len(head) > 1:
            merged = []
            for j in range(ncol):
                merged.append("<br>".join(h[j] for h in head if h[j]))
            head = [merged]
        lines = ["| " + " | ".join(head[0]) + " |",
                 "|" + "|".join({"l": ":--", "c": ":-:", "r": "--:"}[a] for a in aligns[:ncol]) + "|"]
        for r in rows[header_rows:]:
            lines.append("| " + " | ".join(r) + " |")
        return "\n".join(lines)

    def caption(self, text):
        c = self.c
        kind = c.float_kind or "Table"
        c.counters[kind] += 1
        num = "%s.%d" % (c.chapter, c.counters[kind])
        hid = c.new_id(kind.lower() + "-" + num)
        c.last_anchor = (kind, num, hid)
        inner = self.inline(text).strip()
        return html_wrap("nb-caption", "<strong>%s %s.</strong> %s" % (kind, num, inner), hid)

    # ---------------------------------------------------------------- figures --------
    def figure(self, tikz):
        c = self.c
        c.page.figs += 1
        idx = c.page.figs
        if not c.collect:
            c.book.figs.append((c.page.slug, idx, tikz, "\n".join(c.page.defs)))
        return '<figure class="nb-fig"><img src="fig-%d.svg" alt="Figure %d" loading="lazy"></figure>' % (idx, idx)

    # ---------------------------------------------------------------- code -----------
    def lang_of(self, opts, env=None):
        style = opts.get("style")
        lang = opts.get("language")
        seen = set()
        while style and style not in seen:
            seen.add(style)
            so = self.c.m.styles.get(style, {})
            if not lang and so.get("language"):
                lang = so["language"]
            style = so.get("style")
        if not lang and opts.get("style") in ("codeout", "dsaout", "cppout"):
            return "text"
        if not lang and env in ("cpp",):
            return "cpp"
        if not lang and env in ("py",):
            return "python"
        lang = (lang or "").strip()
        lang = self.c.m.languages.get(lang, lang)
        lang = re.sub(r"^\[[^\]]*\]", "", lang)
        table = {"c++": "cpp", "c": "c", "python": "python", "sql": "sql", "bash": "bash",
                 "verilog": "verilog", "vhdl": "vhdl", "java": "java", "": "text",
                 "sh": "bash", "make": "make", "haskell": "haskell"}
        return table.get(lang.lower(), lang.lower() or "text")

    def merged_opts(self, opts):
        style = opts.get("style")
        merged = {}
        chain = []
        seen = set()
        while style and style not in seen:
            seen.add(style)
            so = self.c.m.styles.get(style, {})
            chain.append(so)
            style = so.get("style")
        for so in reversed(chain):
            merged.update(so)
        merged.update(opts)
        return merged

    def listing_title(self, opts):
        t = opts.get("title")
        if not t:
            return None
        txt = self.inline(t)
        txt = re.sub(r"<[^>]+>", "", txt)
        txt = txt.replace("`", "").replace("&#92;", "\\").replace("\\_", "_").replace("&amp;", "&")
        return re.sub(r"\s+", " ", txt).strip()

    def listing_file(self, optstr, path):
        c = self.c
        opts = self.merged_opts(parse_keyvals(optstr))
        full = os.path.join(c.book.root, path.strip())
        if not os.path.isfile(full):
            warn("missing listing " + path)
            return ""
        text = read(full)
        lines = text.split("\n")
        if lines and lines[-1] == "":
            lines = lines[:-1]
        first = int(opts.get("firstline", 1))
        last = int(opts.get("lastline", len(lines)))
        body = "\n".join(lines[first - 1:last])
        lang = self.lang_of(opts)
        if path.endswith(".out") or path.endswith(".warn"):
            lang = "text"
        # line numbers only where the book shows a listing's real line numbers
        explicit = parse_keyvals(optstr)
        start = None
        if "firstnumber" in explicit:
            try:
                start = int(explicit["firstnumber"])
            except ValueError:
                start = first
        return code_fence(body, lang, self.listing_title(opts), opts, start)

    # ---------------------------------------------------------------- math -----------
    def display_math(self, m):
        m = self.fix_math(m).strip()
        if not m:
            return ""
        return "$$\n%s\n$$" % m

    def fix_math(self, m):
        c = self.c
        # labels inside equations
        def lab(mm):
            if c.collect:
                warn("equation label ignored")
            return ""
        m = re.sub(r"\\label\{[^}]*\}", lab, m)
        m = re.sub(r"\\(nonumber|notag)\b", "", m)
        m = re.sub(r"\\code\{", r"\\texttt{", m)
        m = re.sub(r"\\vocab\{", r"\\textbf{", m)
        # outer joins: the books draw two short rules beside \bowtie; KaTeX has no ⟕ glyph
        oj = r"\rule[-0.1ex]{0.3em}{0.06em}\llap{\rule[1.05ex]{0.3em}{0.06em}}"
        m = m.replace("\\lojoin", "\\mathbin{%s\\mkern-4mu\\bowtie}" % oj)
        m = m.replace("\\rojoin", "\\mathbin{\\bowtie\\mkern-4mu%s}" % oj)
        m = m.replace("\\fojoin", "\\mathbin{%s\\mkern-4mu\\bowtie\\mkern-4mu%s}" % (oj, oj))
        m = m.replace("\\ojoin", oj)
        # mathtools' small matrices, which KaTeX lacks
        for env, (l, r) in {"psmallmatrix": ("(", ")"), "bsmallmatrix": ("[", "]"),
                            "vsmallmatrix": ("|", "|"), "Bsmallmatrix": ("\\{", "\\}")}.items():
            m = m.replace("\\begin{%s}" % env, "\\left%s\\begin{smallmatrix}" % l)
            m = m.replace("\\end{%s}" % env, "\\end{smallmatrix}\\right%s" % r)
        # a literal \$ would end Hugo's $...$ passthrough early
        m = m.replace("\\$", "\\text{\\textdollar}")
        m = re.sub(r"\\intertext\{", r"\\text{", m)
        m = re.sub(r"\\(Cref|cref|ref)\{([^}]*)\}", lambda mm: "\\text{%s}" % strip_tags(self.ref(mm.group(1), mm.group(2))), m)
        m = re.sub(r"\\(texttt|textrm|text|mathrm)\{\\detokenize\{([^}]*)\}\}", r"\\\1{\2}", m)
        m = m.replace("\\dashuline", "\\underline").replace("\\textbackslash", "\\backslash ")
        m = re.sub(r"\\(scriptsize|footnotesize|small|tiny|normalsize)\b", "", m)
        if c.in_table:
            m = m.replace("\\|", "\\Vert ").replace("|", "\\vert ")
        return m

    # ================================ inline ============================================
    def inline(self, s):
        out = []
        i = 0
        while i < len(s):
            piece, i = self.inline_token(s, i)
            out.append(piece)
        return tidy_inline("".join(out))

    def inline_token(self, s, i):
        c = self.c
        ch = s[i]
        if ch == "$":
            if s.startswith("$$", i):
                end = s.find("$$", i + 2)
                return "$" + self.fix_math(s[i + 2:end]) + "$", end + 2
            end = find_math_end(s, i + 1)
            return "$" + one_line(self.fix_math(s[i + 1:end])) + "$", end + 1
        if ch == "\\" and s.startswith("\\(", i):
            end = s.find("\\)", i + 2)
            return "$" + one_line(self.fix_math(s[i + 2:end])) + "$", end + 2
        if ch == "{":
            body, k = read_group(s, i)
            return self.inline(body), k
        if ch == "}":
            return "", i + 1
        if ch == "~":
            return " ", i + 1
        if ch == "&":
            return "&amp;", i + 1
        if ch == "<":
            return "&lt;", i + 1
        if ch == ">":
            return "&gt;", i + 1
        if ch == "*":
            return "\\*", i + 1
        if ch == "_":
            return "\\_", i + 1
        if ch == "#":
            return "\\#", i + 1
        if ch == "|":
            return ("\\|" if c.in_table else "|"), i + 1
        if ch == "`":
            if s.startswith("``", i):
                return "“", i + 2
            return "‘", i + 1
        if ch == "'":
            if s.startswith("''", i):
                return "”", i + 2
            return "’", i + 1
        if ch == "-":
            if s.startswith("---", i):
                return "—", i + 3
            if s.startswith("--", i):
                return "–", i + 2
            return "-", i + 1
        if ch == "\n":
            return " ", i + 1
        if ch == "\t":
            return " ", i + 1
        if ch != "\\":
            j = i
            while j < len(s) and s[j] not in "$\\{}~&<>*_#|`'-\n\t":
                j += 1
            if j == i:
                j = i + 1
            return s[i:j], j
        # ---- commands
        name, k = read_cmd(s, i)
        if name in ("code", "texttt", "lstinline", "path", "verb"):
            if name == "lstinline" or name == "verb":
                o, k2 = read_opt(s, k)
                if o is not None:
                    k = k2
                if k < len(s) and s[k] != "{":
                    d = s[k]
                    e = s.find(d, k + 1)
                    return code_span(s[k + 1:e]), e + 1
            arg, k = read_arg(s, k)
            return self.code_inline(arg), k
        if name in WRAP1:
            arg, k = read_arg(s, k)
            a, b = WRAP1[name]
            if name in ("mbox", "makebox", "framebox"):
                _, k2 = read_opt(s, k)
            inner = self.inline(arg)
            return a + inner + b, k
        if name in ("Cref", "cref", "ref", "autoref", "eqref", "Autoref", "nameref"):
            arg, k = read_arg(s, k)
            return self.ref(name, arg), k
        if name == "label":
            arg, k = read_arg(s, k)
            self.attach_label(arg.strip())
            return "", k
        if name == "href":
            url, k = read_arg(s, k)
            text, k = read_arg(s, k)
            return "[%s](%s)" % (self.inline(text), url.strip()), k
        if name == "url":
            url, k = read_arg(s, k)
            return "<%s>" % url.strip(), k
        if name in ("cite", "textcite", "parencite", "citep", "citet"):
            _, k = read_opt(s, k)
            _, k = read_opt(s, k)
            arg, k = read_arg(s, k)
            return self.cite(name, arg), k
        if name == "includegraphics":
            _, k = read_opt(s, k)
            path, k = read_arg(s, k)
            return self.image(path.strip()), k
        if name == "cite@":
            _, k = read_opt(s, k)
            arg, k = read_arg(s, k)
            return "[%s]" % arg.strip(), k
        if name == "footnote":
            arg, k = read_arg(s, k)
            return " (%s)" % self.inline(arg).strip(), k
        if name == "texorpdfstring":
            a, k = read_arg(s, k)
            _, k = read_arg(s, k)
            return self.inline(a), k
        if name == "textcolor":
            col, k = read_arg(s, k)
            arg, k = read_arg(s, k)
            css = CSS_COLORS.get(col.strip())
            inner = self.inline(arg)
            return ('<span style="color:%s">%s</span>' % (css, inner)) if css else inner, k
        if name in ("textcolor", "colorbox"):
            _, k = read_arg(s, k)
            arg, k = read_arg(s, k)
            return self.inline(arg), k
        if name in ("resizebox", "scalebox", "raisebox", "rotatebox", "adjustbox"):
            nskip = {"resizebox": 2, "scalebox": 1, "raisebox": 1, "rotatebox": 1, "adjustbox": 1}[name]
            for _ in range(nskip):
                _, k = read_opt(s, k)
                _, k = read_arg(s, k)
            arg, k = read_arg(s, k)
            if "\\begin{tikzpicture}" in arg:
                return self.figure(arg[arg.find("\\begin{tikzpicture}"):]), k
            return self.inline(arg), k
        if name == "parbox":
            _, k = read_opt(s, k)
            _, k = read_arg(s, k)
            arg, k = read_arg(s, k)
            return self.inline(arg), k
        if name in ("onechili", "twochili", "threechili"):
            return " " + "🌶" * {"onechili": 1, "twochili": 2, "threechili": 3}[name], k
        if name == "rule":
            _, k = read_opt(s, k)
            _, k = read_arg(s, k)
            _, k = read_arg(s, k)
            return "", k
        if name == "src" or name == "run":
            arg, k = read_arg(s, k)
            return code_span(arg), k
        if name in ("item", "ii"):
            warn("stray item")
            return "", k
        if name == "\\":
            if k < len(s) and s[k] == "*":
                k += 1
            o, k2 = read_opt(s, k)
            if o is not None:
                k = k2
            return "<br>", k
        if name in TEXT_SYMBOLS:
            return TEXT_SYMBOLS[name], k
        if name in DROP0:
            return "", k
        if name in DROP1:
            _, k2 = read_opt(s, k)
            _, k = read_arg(s, k2)
            return "", k
        if name in DROP2:
            _, k = read_arg(s, k)
            _, k = read_arg(s, k)
            return "", k
        if name == "multicolumn":
            _, k = read_arg(s, k)
            _, k = read_arg(s, k)
            arg, k = read_arg(s, k)
            return self.inline(arg), k
        if name == "lstinputlisting":
            opt, k = read_opt(s, k)
            path, k = read_arg(s, k)
            return "\n\n" + self.listing_file(opt or "", path) + "\n\n", k
        if name == "begin":
            env, k2 = read_arg(s, k)
            bstart, bend, after = find_env_end(s, k2, env)
            if env == "tikzpicture":
                return self.figure(s[i:after]), after
            md = self.environment(env, s[bstart:bend], None)
            return (md or ""), after
        if name in ("ifnum", "ifdim", "ifx"):
            warn("conditional \\" + name)
            return "", k
        if name == "hyperref":
            _, k = read_opt(s, k)
            arg, k = read_arg(s, k)
            return self.inline(arg), k
        if name == "accent" or name in ("'", "`", "^", "\"", "~", "=", ".", "u", "v", "H", "c", "d", "b", "r", "t"):
            arg, k = read_arg(s, k)
            return accent(name, arg), k
        warn("unknown command \\" + name)
        return "", k

    def cite(self, name, arg):
        """biblatex alphabetic style: \\cite -> [Vas+17], \\textcite -> Vaswani et al. [Vas+17];
        the label links to the book's references page."""
        c = self.c
        out = []
        for key in [x.strip() for x in arg.split(",") if x.strip()]:
            e = c.book.bib.get(key)
            if e is None:
                warn("unknown citation " + key)
                out.append("[%s]" % key)
                continue
            c.book.cited.add(key)
            # brackets as entities: Hugo would read \[...\] as display math
            link = "[&#91;%s&#93;](%s)" % (e["label"], self.href(c.book.slug, "references", ref_anchor(key)))
            out.append(("%s %s" % (e["short"], link)) if name in ("textcite", "citet") else link)
        return join_and(out) if name in ("textcite", "citet") else ", ".join(out)

    def image(self, path):
        c = self.c
        full = None
        for ext in ("", ".png", ".jpg", ".jpeg", ".svg"):
            cand = os.path.join(c.book.root, path + ext)
            if os.path.isfile(cand):
                full = cand
                break
        if full is None:
            warn("missing image " + path)
            return ""
        name = os.path.basename(full)
        if not c.collect:
            c.page.assets.append((full, name))
        return ('<figure class="nb-fig nb-img"><img src="%s" alt="%s" loading="lazy"></figure>'
                % (name, os.path.splitext(name)[0].replace("_", " ")))

    def code_inline(self, arg):
        # \code may hold math or formatting; plain text becomes a code span
        if "$" in arg or "\\textit" in arg or "\\emph" in arg or "\\textbf" in arg or "\\vocab" in arg:
            inner = self.inline(arg)
            return "<code>%s</code>" % inner
        t = unescape_tt(arg)
        if self.c.in_table:
            t = t.replace("|", "\\|")
        return code_span(t)

    def ref(self, name, arg):
        c = self.c
        labs = [x.strip() for x in arg.split(",") if x.strip()]
        # the PDF's hint and solution appendices are drop-downs under each problem here
        if labs == ["app:hints"]:
            return "the <em>Hint</em> drop-down under each problem"
        if labs == ["app:sol"]:
            return "the <em>Solution</em> drop-down under each problem"
        found = []
        for lab in labs:
            info = c.book.labels.get(lab)
            book = c.book.slug
            if info is None:
                for slug, table in ALL_LABELS.items():
                    if lab in table:
                        info = table[lab]
                        book = slug
                        break
            if info is None:
                if not c.collect:
                    warn("undefined reference " + lab)
                found.append(("?", "??", "#"))
                continue
            kind, number, page, anchor = info
            found.append((kind, number, self.href(book, page, anchor)))
        if name in ("ref", "eqref"):
            return ", ".join("[%s](%s)" % (num, url) for _, num, url in found)
        kinds = {k for k, _, _ in found}
        def nm(kind, plural=False):
            w = PLURAL.get(kind, kind + "s") if plural else kind
            return w.lower() if name == "cref" else w
        if len(found) == 1:
            kind, num, url = found[0]
            return "[%s %s](%s)" % (nm(kind), num, url)
        if len(kinds) == 1:
            kind = found[0][0]
            nums = ["[%s](%s)" % (num, url) for _, num, url in found]
            return "%s %s" % (nm(kind, True), join_and(nums))
        return join_and(["[%s %s](%s)" % (nm(k), num, url) for k, num, url in found])

    def href(self, book, page, anchor):
        c = self.c
        frag = ("#" + anchor) if anchor else ""
        here = c.page.slug
        if book == c.book.slug and page == here:
            return frag or "#"
        up = "" if here == "" else "../"      # "" is the book's _index page
        if book == c.book.slug:
            return "%s%s/%s" % (up, page, frag)
        if SECTION_OF.get(book) == SECTION_OF.get(c.book.slug):
            return "%s../%s/%s/%s" % (up, book, page, frag)
        return "%s../../%s/%s/%s/%s" % (up, SECTION_OF.get(book), book, page, frag)


def one_line(m):
    return re.sub(r"\s*\n\s*", " ", m).strip()


def join_and(xs):
    if len(xs) <= 1:
        return "".join(xs)
    return ", ".join(xs[:-1]) + " and " + xs[-1]


def accent(cmd, arg):
    table = {("'", "e"): "é", ("`", "e"): "è", ("'", "a"): "á", ('"', "o"): "ö",
             ('"', "u"): "ü", ('"', "a"): "ä", ("^", "o"): "ô", ("~", "n"): "ñ",
             ("c", "c"): "ç", ("'", "o"): "ó", ("'", "i"): "í", ("'", "\\i"): "í",
             ("v", "s"): "š", ("v", "c"): "č", ("'", "E"): "É", ("H", "o"): "ő"}
    return table.get((cmd, arg.strip()), arg)


def find_math_end(s, i):
    while i < len(s):
        if s[i] == "\\":
            i += 2
            continue
        if s[i] == "$":
            return i
        i += 1
    warn("unterminated math")
    return len(s)


def find_display_end(s, i):
    j = s.find("\\]", i)
    return j if j >= 0 else len(s)


def unescape_tt(t):
    t = re.sub(r"\\textbackslash(\{\})?\s?", "\\\\", t)
    t = re.sub(r"\\textasciitilde(\{\})?", "~", t)
    t = re.sub(r"\\textasciicircum(\{\})?", "^", t)
    t = re.sub(r"\\textless(\{\})?", "<", t)
    t = re.sub(r"\\textgreater(\{\})?", ">", t)
    t = re.sub(r"\\textbar(\{\})?", "|", t)
    t = re.sub(r"\\textquotesingle(\{\})?", "'", t)
    t = re.sub(r"\\textquotedbl(\{\})?", '"', t)
    t = re.sub(r"\\(ldots|dots)(\{\})?", "...", t)
    t = re.sub(r"\\([_&%#${}])", r"\1", t)
    t = re.sub(r"\\\^\{\}", "^", t)
    t = re.sub(r"\\~\{\}", "~", t)
    t = t.replace("\\,", " ").replace("\\ ", " ").replace("~", " ") if False else t
    t = re.sub(r"\\(allowbreak|linebreak|hspace\{[^}]*\}|-)", "", t)
    t = re.sub(r"\{\}", "", t)
    t = re.sub(r"\\detokenize\{([^}]*)\}", r"\1", t)
    t = re.sub(r"\\(footnotesize|small|scriptsize|ttfamily)\s*", "", t)
    t = re.sub(r"\\textbf\{([^}]*)\}", r"\1", t)
    t = re.sub(r"\\code\{([^}]*)\}", r"\1", t)
    t = re.sub(r"\\texttt\{([^}]*)\}", r"\1", t)
    t = t.replace("\\\\", "\x00").replace("\\,", " ").replace("\\ ", " ").replace("\x00", "\\")
    t = re.sub(r"\s+", " ", t)
    return t


def code_span(t):
    t = t.replace("\n", " ")
    ticks = 1
    while "`" * ticks in t:
        ticks += 1
    fence = "`" * ticks
    pad = " " if t.startswith("`") or t.endswith("`") or (t.startswith(" ") and t.strip()) else ""
    return "%s%s%s%s%s" % (fence, pad, t, pad, fence)


def strip_tags(t):
    t = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", t)
    return re.sub(r"<[^>]+>", "", t)


def tidy_inline(t):
    t = re.sub(r"[ \t]+", " ", t)
    t = re.sub(r" ?<br> ?", "<br>", t)
    t = re.sub(r"^(<br>)+|(<br>)+$", "", t.strip())
    return t.strip()


def escape_para_start(t):
    if re.match(r"\d+[.)] ", t):
        t = re.sub(r"^(\d+)([.)])", r"\1\\\2", t)
    elif re.match(r"[-+>] ", t) or t.startswith("="):
        t = "\\" + t
    return t


def html_wrap(cls, md, hid=None):
    """A div around Markdown; the blank lines make goldmark parse the inside as Markdown
    (math, links and code spans inside a raw HTML line would stay literal)."""
    idattr = ' id="%s"' % hid if hid else ""
    return '<div class="%s"%s>\n\n%s\n\n</div>' % (cls, idattr, md)


def prefix_first_para(md, prefix):
    if not md:
        return prefix.strip()
    first = md.split("\n", 1)[0]
    if re.match(r"(\$\$|```|<figure|<div|<details|<p |\||- |\d+\. |#|>|---)", first):
        return prefix.strip() + "\n\n" + md
    return prefix + md


def parse_colspec(spec):
    out = []
    i = 0
    spec = re.sub(r"\*\{(\d+)\}\{([^}]*)\}", lambda m: m.group(2) * int(m.group(1)), spec)
    while i < len(spec):
        ch = spec[i]
        if ch in "@!><":
            j = spec.find("{", i)
            _, k = read_group(spec, j)
            i = k
            continue
        if ch in "pmb" and i + 1 < len(spec) and spec[i + 1] == "{":
            _, k = read_group(spec, i + 1)
            out.append("l")
            i = k
            continue
        if ch in "lLXpY":
            out.append("l")
        elif ch in "cC":
            out.append("c")
        elif ch in "rR":
            out.append("r")
        elif ch == "S":
            out.append("r")
        i += 1
    return out


def dedent_listing(body):
    lines = body.split("\n")
    ind = None
    for ln in lines:
        if ln.strip():
            lead = len(ln) - len(ln.lstrip("\t "))
            ind = lead if ind is None else min(ind, lead)
    if ind:
        lines = [ln[ind:] if len(ln) >= ind else ln.lstrip() for ln in lines]
    return "\n".join(lines)


def code_fence(body, lang, title, opts, start=None):
    fence = "```"
    while fence in body:
        fence += "`"
    attrs = []
    if title:
        attrs.append('filename="%s"' % title.replace('"', "'"))
    if start is not None:
        attrs.append("linenos=table")
        attrs.append("linenostart=%d" % start)
    attr = (" {%s}" % ",".join(attrs)) if attrs else ""
    body = body.expandtabs(4)
    return "%s%s%s\n%s\n%s" % (fence, lang, attr, body.rstrip("\n"), fence)


# ----------------------------------------------------------------------------------------
# Book assembly
# ----------------------------------------------------------------------------------------

def load_book(cfg):
    book = Book(cfg)
    root = book.root
    wrapper = strip_comments(read(os.path.join(root, cfg["wrapper"])))
    pre, _, docbody = wrapper.partition("\\begin{document}")
    book.preamble = pre
    macros = Macros()
    # the shared preamble's own definitions (theorem setup is handled natively)
    macros.scan(strip_comments(read(os.path.join(root, "tex", "preamble.tex"))))
    macros.scan(strip_comments(read(os.path.join(root, "tex", "macros.tex"))))
    for inp in re.findall(r"\\input\{([^}]*)\}", pre):
        if inp in ("tex/preamble", "tex/macros"):
            continue
        p = os.path.join(root, inp if inp.endswith(".tex") else inp + ".tex")
        macros.scan(strip_comments(read(p)))
    pre_local = re.sub(r"\\input\{[^}]*\}", "", pre)
    macros.scan(pre_local)
    if re.search(r"\\renewcommand\{\\theproblem\}\{\\thechapter\.\\arabic\{problem\}\}", pre):
        book.problem_style = "arabic"
    m = re.search(r"\\title\{(.*?)\}\n", pre)
    book.title = m.group(1) if m else cfg["slug"]
    m = re.search(r"\\subtitle\{(.*?)\}\n", pre)
    book.subtitle = m.group(1) if m else ""
    if "bookabout" in macros.defs:
        book.about = macros.defs["bookabout"][2]
    # chapters in order, with parts
    units = []
    part = None
    for m in re.finditer(r"\\part\{([^}]*)\}|\\input\{([^}]*)\}|\\appendix", docbody):
        if m.group(0) == "\\appendix":
            break
        if m.group(1) is not None:
            part = m.group(1)
            continue
        inp = m.group(2)
        if inp.startswith("tex/"):
            continue
        units.append((part, inp))
    book.units = units
    book.macros = macros
    bib = os.path.join(root, cfg.get("bib", "references.bib"))
    if os.path.isfile(bib):
        book.bib = parse_bib(read(bib))
    return book


def parse_bib(text):
    """A small BibTeX reader: @type{key, field = {value} | "value" | number, ...}."""
    entries = {}
    for m in re.finditer(r"@(\w+)\s*\{\s*([^,\s]+)\s*,", text):
        start = m.end()
        depth = 1
        j = start
        while j < len(text) and depth:
            if text[j] == "{":
                depth += 1
            elif text[j] == "}":
                depth -= 1
            j += 1
        body = text[start:j - 1]
        e = {"type": m.group(1).lower()}
        for part in split_top(body, r","):
            if "=" not in part:
                continue
            k, v = part.split("=", 1)
            v = v.strip()
            if v.startswith("{") and v.endswith("}") or v.startswith('"') and v.endswith('"'):
                v = v[1:-1]
            e[k.strip().lower()] = re.sub(r"\s+", " ", v).strip()
        entries[m.group(2)] = e
    labels = Counter()
    for key, e in entries.items():
        last = [bib_lastname(a) for a in re.split(r"\s+and\s+", e.get("author", e.get("editor", "Anon")))]
        yy = e.get("year", "")[-2:]
        if len(last) == 1:
            lab = last[0][:3]
        elif len(last) <= 3:
            lab = "".join(x[:1] for x in last)
        else:
            lab = last[0][:3] + "+"
        e["label"] = lab + yy
        labels[e["label"]] += 1
        if len(last) == 1:
            e["short"] = last[0]
        elif len(last) == 2:
            e["short"] = "%s and %s" % tuple(last)
        else:
            e["short"] = last[0] + " et al."
    seen = Counter()
    for key in sorted(entries):
        e = entries[key]
        if labels[e["label"]] > 1:          # Smi20a, Smi20b
            seen[e["label"]] += 1
            e["label"] += "abcdefghij"[seen[e["label"]] - 1]
    return entries


def bib_lastname(name):
    name = name.strip()
    if "," in name:
        last = name.split(",")[0]
    else:
        parts = split_top(name, r"\s+")
        last = parts[-1] if parts else name
    return re.sub(r"[{}\\]", "", last).strip()


def chapter_slug(path):
    base = os.path.basename(path)
    base = re.sub(r"\.tex$", "", base)
    return base


def render_book(book, collect):
    cfg = book.cfg
    macros = book.macros
    ctx = Ctx(book, macros, collect)
    exp = Expander(macros, book.root)
    r = Renderer(ctx)
    pages = []
    book_defs = []
    if book.split == "sections":
        # one LaTeX chapter whose \input files become the pages
        chap_src = strip_comments(read(os.path.join(book.root, cfg["chapter_file"])))
        chap_src = macros.scan(chap_src, raw=book_defs)
        m = re.search(r"\\chapter\{([^}]*)\}", chap_src)
        ctx.chapter = 1
        ctx.heading_shift = 1
        intro_src = chap_src[m.end():]
        inputs = re.findall(r"\\input\{([^}]*)\}", intro_src)
        intro_src = re.sub(r"\\input\{[^}]*\}", "", intro_src)
        intro_src = re.sub(r"^\s*\\label\{[^}]*\}", "", intro_src)
        ctx.page = Page(book, "", 0)
        book.intro = r.blocks(exp.expand(intro_src))
        # the chapter's opening paragraph repeats the book's own blurb; keep the rest
        if book.about and book.intro.startswith("This chapter "):
            book.intro = book.intro.split("\n\n", 1)[-1]
        units = [(None, p) for p in inputs]
    else:
        units = book.units
    for n, (part, inp) in enumerate(units, 1):
        path = os.path.join(book.root, inp if inp.endswith(".tex") else inp + ".tex")
        src = strip_comments(read(path))
        slug = chapter_slug(inp)
        page = Page(book, slug, n)
        # definitions stay in force for the rest of the book, as in TeX
        src = macros.scan(src, raw=book_defs)
        page.defs = list(book_defs)
        ctx.page = page
        ctx.used_ids = set()
        if book.split == "sections":
            m = re.search(r"\\section\*?\{", src)
            title, k = read_group(src, m.end() - 1)
            ctx.section = n
            ctx.subsection = 0
            ctx.counters["thm"] = 0
            number = "%d.%d" % (ctx.chapter, n)
            body_src = src[k:]
            ctx.last_anchor = ("Section", number, "")
        else:
            m = re.search(r"\\chapter\*?\{", src)
            title, k = read_group(src, m.end() - 1)
            ctx.chapter += 1
            ctx.section = 0
            ctx.subsection = 0
            ctx.counters = Counter()
            ctx.tables = ctx.figures = 0
            number = str(ctx.chapter)
            body_src = src[k:]
            ctx.last_anchor = ("Chapter", number, "")
            ctx.counters["prob"] = 0
        body_src = exp.expand(body_src)
        md = r.blocks(body_src)
        title_md = r.inline(exp.expand(title))
        pages.append(dict(slug=slug, title=title_md, number=number, part=part, body=md,
                          weight=n, figs=page.figs, assets=page.assets))
    # appendices (the notation glossary): chapter-style pages lettered A, B, ...
    for n, inp in enumerate(cfg.get("appendix", []), 1):
        src = macros.scan(strip_comments(read(os.path.join(book.root, inp + ".tex"))), raw=book_defs)
        m = re.search(r"\\chapter\*?\{", src)
        title, k = read_group(src, m.end() - 1)
        letter = alpha(n)
        page = Page(book, chapter_slug(inp), 900 + n)
        page.defs = list(book_defs)
        ctx.page = page
        ctx.used_ids = set()
        ctx.chapter, ctx.section, ctx.subsection, ctx.heading_shift = letter, 0, 0, 0
        ctx.counters = Counter()
        ctx.last_anchor = ("Appendix", letter, "")
        md = r.blocks(exp.expand(src[k:]))
        pages.append(dict(slug=page.slug, title=r.inline(exp.expand(title)), number=letter,
                          part=None, body=md, weight=900 + n, figs=page.figs,
                          assets=page.assets))
    if book.cited and not collect:
        pages.append(dict(slug="references", title="References", number="", part=None,
                          body=references_md(book, r), weight=999, figs=0, assets=[]))
    return pages


def ref_anchor(key):
    """ref:vaswani2017 -> ref-vaswani2017 (the bib keys already carry a ref: prefix)."""
    return anchor_of("ref-" + re.sub(r"^ref:", "", key))


def references_md(book, r):
    """The bibliography, in label order, with an anchor per entry for the citation links."""
    lines = []
    for key in sorted(book.cited, key=lambda k: book.bib[k]["label"].lower()):
        e = book.bib[key]
        authors = [r.inline(a) for a in re.split(r"\s+and\s+", e.get("author", ""))]
        title = r.inline(e.get("title", key))
        bits = [", ".join(authors) + "." if authors else "",
                "<em>%s</em>%s" % (title, "" if title.endswith(("?", "!", ".")) else ".")]
        venue = e.get("booktitle") or e.get("journal") or e.get("howpublished") or e.get("publisher")
        if venue:
            bits.append(r.inline(venue) + ",")
        if e.get("volume"):
            bits.append("vol. %s," % e["volume"])
        if e.get("pages"):
            bits.append("pp. %s," % r.inline(e["pages"]))
        bits.append(e.get("year", "") + ".")
        if e.get("doi"):
            bits.append("doi: [%s](https://doi.org/%s)" % (e["doi"], e["doi"]))
        elif e.get("url"):
            bits.append("<%s>" % e["url"])
        text = " ".join(b for b in bits if b).replace(",.", ".")
        lines.append('- <a id="%s"></a><strong>[%s]</strong> %s'
                     % (ref_anchor(key), e["label"], text))
    return "\n".join(lines)


# ----------------------------------------------------------------------------------------
# Figures
# ----------------------------------------------------------------------------------------

def compile_figures(book):
    if not book.figs:
        return {}
    cache = os.path.join(CACHE, book.slug)
    os.makedirs(cache, exist_ok=True)
    pre = book.preamble
    results = {}
    todo = []
    for slug, idx, tikz, defs in book.figs:
        h = hashlib.sha1((pre + defs + tikz).encode("utf8")).hexdigest()[:16]
        svg = os.path.join(cache, h + ".svg")
        results[(slug, idx)] = svg
        if not os.path.isfile(svg):
            todo.append((h, tikz, defs))
    if not todo:
        return results
    seen = set()
    todo = [t for t in todo if not (t[0] in seen or seen.add(t[0]))]
    # TikZ libraries must load globally (keys defined inside a group would be lost)
    libs = sorted({m for _, _, d in todo for m in re.findall(r"\\usetikzlibrary\{[^}]*\}", d)})
    todo = [(h, t, re.sub(r"\\usetikzlibrary\{[^}]*\}", "", d)) for h, t, d in todo]
    doc = ["\\def\\pgfsysdriver{pgfsys-dvisvgm.def}", pre, "\n".join(libs),
           "\\usepackage[active,tightpage]{preview}",
           "\\PreviewEnvironment{tikzpicture}",
           "\\setlength\\PreviewBorder{3pt}",
           "\\begin{document}"]
    # each picture in its own group, after its chapter's definitions (local to the group)
    for h, tikz, defs in todo:
        doc.append("\\begingroup\n%s\n%s\\endgroup\n\n" % (defs, tikz))
    doc.append("\\end{document}\n")
    tex = os.path.join(cache, "figs.tex")
    with open(tex, "w", encoding="utf8") as f:
        f.write("\n".join(doc))
    print("  compiling %d figures for %s" % (len(todo), book.slug))
    cmd = ["latex", "-interaction=nonstopmode", "-halt-on-error",
           "-output-directory=" + cache, tex]
    # stdin closed: a LaTeX error prompt then ends the run instead of waiting for input
    try:
        p = subprocess.run(cmd, cwd=book.root, capture_output=True, text=True, encoding="utf8",
                           errors="replace", timeout=300, stdin=subprocess.DEVNULL)
    except subprocess.TimeoutExpired:
        warn("LaTeX timed out on the figures of " + book.slug)
        return results
    dvi = os.path.join(cache, "figs.dvi")
    if p.returncode != 0 or not os.path.isfile(dvi):
        log = p.stdout[-3000:]
        print("  LaTeX failed for %s figures:\n%s" % (book.slug, log))
        warn("figure compile failed for " + book.slug)
        return results
    for f in os.listdir(cache):
        if f.startswith("page-") and f.endswith(".svg"):
            os.remove(os.path.join(cache, f))
    p = subprocess.run(["dvisvgm", "--no-fonts", "--exact-bbox", "--page=1-",
                        "--output=" + os.path.join(cache, "page-%p.svg"), dvi],
                       capture_output=True, text=True, encoding="utf8", errors="replace")
    pages = sorted(f for f in os.listdir(cache) if f.startswith("page-") and f.endswith(".svg"))
    # LaTeX may ship one "temporary extra page" at the very end; the pictures come first
    if len(pages) < len(todo):
        print("  dvisvgm produced %d pages for %d figures" % (len(pages), len(todo)))
        print(p.stderr[-2000:])
        warn("figure count mismatch for " + book.slug)
    pages.sort(key=lambda f: int(re.search(r"(\d+)", f).group(1)))
    for (h, _, _), f in zip(todo, pages):
        shutil.move(os.path.join(cache, f), os.path.join(cache, h + ".svg"))
    return results


# ----------------------------------------------------------------------------------------
# Writing the Hugo pages
# ----------------------------------------------------------------------------------------

def yaml_str(s):
    return '"%s"' % s.replace("\\", "\\\\").replace('"', '\\"')


MATH_TEXT = {"Theta": "Θ", "Omega": "Ω", "le": "≤", "ge": "≥", "times": "×", "to": "→",
             "log": "log", "lg": "lg", "ln": "ln", "cdot": "·", "ldots": "…", "dots": "…",
             "infty": "∞", "alpha": "α", "beta": "β", "lambda": "λ", "pi": "π", "neq": "≠",
             "ne": "≠", "bowtie": "⋈", "sigma": "σ", "rightarrow": "→"}


def plain_title(md):
    """Front-matter titles are plain text (sidebar, browser tab): math becomes text."""
    t = strip_tags(md)
    t = re.sub(r"`([^`]*)`", r"\1", t)

    def math(m):
        x = m.group(1)
        x = re.sub(r"\\([A-Za-z]+)", lambda mm: MATH_TEXT.get(mm.group(1), ""), x)
        x = x.replace("{", "").replace("}", "").replace("^", "").replace("\\,", " ")
        return x.strip()
    t = re.sub(r"\$([^$]*)\$", math, t)
    return t.replace("\\_", "_").replace("\\*", "*").replace("&amp;", "&")


def write_book(book, pages, figs):
    cfg = book.cfg
    bdir = os.path.join(CONTENT, SECTION_OF[book.slug], book.slug)
    os.makedirs(bdir, exist_ok=True)
    written = set()
    macros = book.macros
    ctx = Ctx(book, macros, False)
    ctx.page = Page(book, "", 0)
    r = Renderer(ctx)
    exp = Expander(macros, book.root)
    about = r.inline(exp.expand(book.about)) if book.about else ""
    lines = ["---", "title: %s" % yaml_str(plain_title(r.inline(book.title))),
             "weight: %d" % cfg["weight"],
             "sidebar:", "  open: false", "---", ""]
    if about:
        lines += [about, ""]
    if book.intro:
        lines += [book.intro, ""]
    lines += ["## Contents", ""]
    part = None
    for p in pages:
        if p["part"] and p["part"] != part:
            part = p["part"]
            lines += ["", "**Part: %s**" % part, ""]
        lines.append("- [%s](%s/)" % (numbered(p["number"], p["title"], " · "), p["slug"]))
    lines.append("")
    put(os.path.join(bdir, "_index.md"), "\n".join(lines), written)
    for p in pages:
        pdir = os.path.join(bdir, p["slug"])
        os.makedirs(pdir, exist_ok=True)
        fm = ["---", "title: %s" % yaml_str(numbered(p["number"], plain_title(p["title"]), " · ")),
              "linkTitle: %s" % yaml_str(numbered(p["number"], plain_title(p["title"]), " ")),
              "weight: %d" % p["weight"], "math: true", "---", ""]
        put(os.path.join(pdir, "index.md"), "\n".join(fm) + p["body"].rstrip() + "\n", written)
        for idx in range(1, p["figs"] + 1):
            svg = figs.get((p["slug"], idx))
            dst = os.path.join(pdir, "fig-%d.svg" % idx)
            if svg and os.path.isfile(svg):
                put(dst, read(svg), written)
            elif os.path.isfile(dst):
                written.add(os.path.normcase(dst))      # --no-figs keeps the last SVGs
            else:
                warn("figure missing: %s/%s fig %d" % (book.slug, p["slug"], idx))
        for src, name in p.get("assets", []):
            dst = os.path.join(pdir, name)
            written.add(os.path.normcase(dst))
            if not (os.path.isfile(dst) and os.path.getsize(dst) == os.path.getsize(src)):
                shutil.copyfile(src, dst)
    # remove pages and pictures that no longer exist in the book
    for dirpath, _, files in os.walk(bdir):
        for f in files:
            full = os.path.join(dirpath, f)
            if os.path.normcase(full) not in written:
                os.remove(full)


def put(path, text, written):
    """Write only when the content changed (a running `hugo server` holds files briefly)."""
    written.add(os.path.normcase(path))
    if os.path.isfile(path) and read(path) == text.replace("\r\n", "\n"):
        return
    for attempt in range(20):
        try:
            with open(path, "w", encoding="utf8", newline="\n") as f:
                f.write(text)
            return
        except PermissionError:
            import time
            time.sleep(0.25)
    raise PermissionError(path)


def numbered(number, title, sep):
    return ("%s%s%s" % (number, sep, title)) if number else title


def fetch_cloud_sources():
    """Extract the cloud branch's latex/ folder (read-only; the notes checkout is untouched)."""
    dst = os.path.join(HERE, ".src")
    if os.path.isdir(os.path.join(dst, "latex")):
        return
    os.makedirs(dst, exist_ok=True)
    git = subprocess.run(["git", "-C", NOTES, "archive", CLOUD_BRANCH, "latex"],
                         capture_output=True, check=True)
    subprocess.run(["tar", "-x", "-C", dst], input=git.stdout, check=True)


def main(argv):
    want = [a for a in argv if not a.startswith("--")]
    figs_on = "--no-figs" not in argv
    fetch_cloud_sources()
    loaded = []
    for cfg in BOOKS:
        b = load_book(cfg)
        loaded.append(b)
    # pass 1: labels of every book, so references across books resolve
    for b in loaded:
        render_book(b, collect=True)
        ALL_LABELS[b.slug] = b.labels
    for b in loaded:
        if want and b.slug not in want:
            continue
        # content/core/<book>/ now holds hand-written condensed pages (2026-10-24);
        # the generated full versions are kept in tools/latex2hugo/full-version/.
        if b.slug in CONDENSED and "--overwrite-condensed" not in argv:
            print("book", b.slug, "skipped: hand-written condensed version in content/core")
            continue
        print("book", b.slug)
        b.figs = []
        pages = render_book(b, collect=False)
        figs = compile_figures(b) if figs_on else {}
        write_book(b, pages, figs)
        print("  %d pages, %d figures" % (len(pages), len(b.figs)))
    if LOG:
        print("\nwarnings:")
        for msg, n in sorted(LOG.items(), key=lambda x: -x[1]):
            print("  %4d  %s" % (n, msg))


if __name__ == "__main__":
    main(sys.argv[1:])
