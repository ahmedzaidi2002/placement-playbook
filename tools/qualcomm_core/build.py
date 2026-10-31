"""Build the "Core subjects" tabs on content/companies/qualcomm/_index.md.

    python tools/qualcomm_core/build.py

Writes every figure to static/companies/qualcomm/core/<name>.svg and replaces the block
between the core-tabs markers in the Qualcomm index page. Questions live in data_*.py,
figures in figures.py. Tab content goes through Hextra's markdownify, which renders with
the home page as context, so figures use root-relative paths and the answer toggles are
plain <details> elements with Hextra's classes rather than the details shortcode.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))

import figures  # noqa: E402
from qdef import PAPERS  # noqa: E402
from data_os_oop import OOP, OS  # noqa: E402
from data_arch import ARCH  # noqa: E402
from data_dig import DIG  # noqa: E402

FIG_DIR = os.path.join(ROOT, 'static', 'companies', 'qualcomm', 'core')
FIG_URL = '/companies/qualcomm/core'
INDEX = os.path.join(ROOT, 'content', 'companies', 'qualcomm', '_index.md')
START, END = '<!-- core-tabs:start -->', '<!-- core-tabs:end -->'

TABS = [
    ('OOPS', 'O', 'cube', OOP,
     'Only five OOPS questions appear across the eight papers; the section was small in every sitting. '
     'Q50–Q54 of the [60-question set](/companies/qualcomm/04-computer-science/) and the '
     '[OOP in C++ book](/core/oop-cpp/) cover the rest of the ground.'),
    ('Operating systems', 'S', 'terminal', OS,
     'Process states, scheduling arithmetic, memory, synchronisation and deadlock. Most items are one-line '
     'concept checks; the arithmetic ones (round robin, Little\'s law, C-SCAN) are worked in full.'),
    ('Digital circuits', 'D', 'chip', DIG,
     'The largest section: Boolean algebra, combinational and sequential circuits, counters, timing, logic '
     'families and data converters. Every circuit figure is redrawn from the exam photos.'),
    ('Computer architecture', 'A', 'server', ARCH,
     'Number representation, x86 and 8085 registers and instructions, pipelining, performance, memory and buses. '
     'Some papers label this section "Computer Architecture 2" or "CA".'),
]

DETAILS_OPEN = ('<details class="hx:last-of-type:mb-0 hx:rounded-lg hx:bg-neutral-50 hx:dark:bg-neutral-800 hx:p-2 '
                'hx:mt-4 hx:group">\n<summary class="hx:flex hx:items-center hx:cursor-pointer hx:select-none '
                'hx:list-none hx:p-1 hx:rounded-sm hx:transition-colors hx:hover:bg-gray-100 '
                'hx:dark:hover:bg-neutral-800 hx:before:mr-1 hx:before:inline-block hx:before:transition-transform '
                'hx:before:content-[\'\'] hx:dark:before:invert hx:rtl:before:rotate-180 '
                'hx:group-open:before:rotate-90"><strong class="hx:text-lg">Show answer and explanation</strong>'
                '</summary>\n<div class="hx:p-2 hx:overflow-hidden">')
DETAILS_CLOSE = '</div>\n</details>'


def sources(q):
    parts = []
    for p, n in q.src:
        parts.append(f'{PAPERS[p]}, Q{n}' if n else PAPERS[p])
    return ' · '.join(parts)


def render(q, label):
    out = [f'#### {label} · {q.topic}', '', f'*Asked in: {sources(q)}*', '', q.text, '']
    if q.fig:
        out += [f'<figure class="nb-fig"><img src="{FIG_URL}/{q.fig}.svg" alt="Figure for {label}" '
                f'loading="lazy"></figure>', '']
    if q.table:
        out += [q.table, '']
    if q.code:
        out += ['```c', q.code, '```', '']
    if q.opts:
        out += ['**Options**', '']
        out += [f'- **{"ABCD"[i]}.** {o}' for i, o in enumerate(q.opts)]
        out.append('')
    out += [DETAILS_OPEN, '']
    if q.conf == 'flag':
        head = '**No reliable pick.**'
        if q.note:
            head += ' ' + q.note
    else:
        if q.ans:
            i = 'ABCD'.index(q.ans)
            head = f'**Answer: {q.ans}.** {q.opts[i]}'
        else:
            head = '**Answer** (options not captured):'
    out += [head, '', q.expl, '']
    if q.conf == 'medium' and q.note:
        out += [f'*Medium confidence.* {q.note}', '']
    out += [DETAILS_CLOSE, '']
    return out


def tab_body(prefix, intro, qs):
    lines = [intro, '']
    flagged = [f'{prefix}{i + 1}' for i, q in enumerate(qs) if q.conf == 'flag']
    medium = [f'{prefix}{i + 1}' for i, q in enumerate(qs) if q.conf == 'medium']
    lines += [f'**{len(qs)} questions.** Medium confidence: {", ".join(medium) or "none"}. '
              f'Flagged (no reliable pick): {", ".join(flagged) or "none"}.', '']
    topic = None
    for i, q in enumerate(qs):
        if q.topic != topic:
            topic = q.topic
            lines += [f'### {topic}', '']
        lines += render(q, f'{prefix}{i + 1}')
    return lines


def block():
    total = sum(len(t[3]) for t in TABS)
    papers = ', '.join(PAPERS.values())
    lines = [START, '', '## Core subjects from campus papers', '',
             f'{total} more questions from eight Qualcomm online tests ({papers}), limited to the four core '
             'sections: OOPS, operating systems, digital circuits and computer architecture. They were transcribed '
             'from photos of the HirePro screen, solved here, and every circuit was redrawn. A question asked in '
             'two papers is listed once with both sources.', '',
             '| Tab | Questions | Medium | Flagged |', '|---|:-:|:-:|:-:|']
    for name, prefix, icon, qs, intro in TABS:
        lines.append(f'| {name} | {len(qs)} | {sum(q.conf == "medium" for q in qs)} | '
                     f'{sum(q.conf == "flag" for q in qs)} |')
    lines += ['', '*Medium* means the answer is sound but rests on reading a blurred photo or an ambiguous '
              'question; the toggle says why. *Flagged* means no option is right as printed, or the photo cut off '
              'data the answer needs; the toggle shows the working instead of a pick.', '',
              '{{< tabs >}}', '']
    for k, (name, prefix, icon, qs, intro) in enumerate(TABS):
        sel = ' selected=true' if k == 0 else ''
        lines += [f'{{{{< tab name="{name}" icon="{icon}"{sel} >}}}}', '']
        lines += tab_body(prefix, intro, qs)
        lines += ['{{< /tab >}}', '']
    lines += ['{{< /tabs >}}', '', END]
    return '\n'.join(lines)


def main():
    os.makedirs(FIG_DIR, exist_ok=True)
    used = {q.fig for t in TABS for q in t[3] if q.fig}
    missing = used - set(figures.ALL)
    assert not missing, f'unknown figures: {missing}'
    for name in sorted(used):
        with open(os.path.join(FIG_DIR, name + '.svg'), 'w', encoding='utf-8', newline='\n') as f:
            f.write(figures.ALL[name]())
    for t in TABS:
        for q in t[3]:
            assert q.conf in ('high', 'medium', 'flag'), q.text[:40]
            assert q.conf == 'flag' or q.ans or not q.opts, q.text[:40]
            assert not q.opts or len(q.opts) == 4, q.text[:40]
    with open(INDEX, encoding='utf-8') as f:
        page = f.read()
    new = block()
    if START in page:
        a = page.index(START)
        b = page.index(END) + len(END)
        page = page[:a] + new + page[b:]
    else:
        page = page.rstrip('\n') + '\n\n' + new + '\n'
    with open(INDEX, 'w', encoding='utf-8', newline='\n') as f:
        f.write(page)
    print(f'{sum(len(t[3]) for t in TABS)} questions, {len(used)} figures -> {INDEX}')


if __name__ == '__main__':
    main()
