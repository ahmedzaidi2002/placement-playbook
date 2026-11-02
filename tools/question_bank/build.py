"""Build the subject-wise pages of the Question Bank from questions.json + explain/*.md.

    python tools/question_bank/build.py

Writes content/question-bank/<subject>/_index.md and one page per topic. Each question shows
who asked it, the statement, code and options, then a closed toggle with the explained answer.

Explanations live in explain/<subject-slug>/<topic-slug>.md as blocks:

    @@ question-id
    **Answer: (b) 57.**
    ...

A question with no block falls back to the short catalogue answer and is counted as missing.
"""
import glob
import json
import os
import re
import sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
OUT = os.path.join(ROOT, 'content', 'question-bank')
EXPLAIN = os.path.join(HERE, 'explain')
CARDS_START, CARDS_END = '<!-- subject-cards:start -->', '<!-- subject-cards:end -->'
SAFE_TAGS = 'code|u|br|sub|sup|b|i|em|strong|figure|img|details|summary|div|span|table|tr|td|th'

SUBJECTS = [
    ('Quantitative aptitude', 'calculator'),
    ('Logical reasoning', 'puzzle'),
    ('Verbal ability', 'book-open'),
    ('Mathematics', 'variable'),
    ('C programming', 'code'),
    ('C++ and object-oriented programming', 'cube'),
    ('Java', 'code'),
    ('Python', 'code'),
    ('Data structures and algorithms', 'share'),
    ('Operating systems', 'terminal'),
    ('DBMS and SQL', 'database'),
    ('Computer networks', 'globe-alt'),
    ('Computer architecture and digital logic', 'chip'),
    ('Embedded systems and electronics', 'light-bulb'),
    ('Machine learning', 'sparkles'),
    ('Software engineering and web', 'server'),
    ('Interview questions', 'chat'),
    ('Other', 'cog'),
]

# Qualcomm-only question -> the company-DB question it repeats (shown once, both sources listed)
MERGE = {
    'qcc-oop-01': 'qc-n-ctor',
    'qcc-os-10': 'qc-n-sched',
    'qcc-os-11': 'qc25-release',
    'qcc-os-20': 'qc-n-hwcs',
    'qcc-arch-27': 'qc-n-mov',
    'qcc-arch-37': 'qc-n-cpi',
}


def slug(s):
    return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')


def yaml_str(s):
    return '"' + s.replace('\\', '\\\\').replace('"', '\\"') + '"'


def load_explanations():
    ex = {}
    for f in glob.glob(os.path.join(EXPLAIN, '**', '*.md'), recursive=True):
        with open(f, encoding='utf8') as fh:
            text = fh.read()
        for m in re.finditer(r'^@@ (\S+)[ \t]*\n(.*?)(?=^@@ |\Z)', text, re.S | re.M):
            qid = m.group(1)
            if qid in ex:
                sys.exit(f'build: {qid} explained twice ({f})')
            ex[qid] = m.group(2).strip()
    return ex


def load_questions():
    with open(os.path.join(HERE, 'questions.json'), encoding='utf8') as fh:
        qs = json.load(fh)
    byid = {q['id']: q for q in qs}
    for extra, keep in MERGE.items():
        byid[keep]['asked'] += '; ' + byid[extra]['asked']
        del byid[extra]
    return list(byid.values())


def _dollar_code(m):
    inner = m.group(1).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    for ch, ent in (('$', '&#36;'), ('*', '&#42;'), ('_', '&#95;'), ('\\', '&#92;')):
        inner = inner.replace(ch, ent)
    return '<code>' + inner + '</code>'


def fix_md(text, plain_dollars=False):
    """Make Markdown safe for Hugo's math passthrough, outside fenced code.

    Inline code holding `$` (the binary-code puzzles) would be read as math, so it becomes
    <code> with entities; the book's own LaTeX macros become plain KaTeX or text. With
    plain_dollars (the explain/ blocks, which write maths in Unicode, never $...$) every
    other $ is a currency sign and is escaped.
    """
    parts = re.split(r'(^```.*?^```)', text, flags=re.S | re.M)
    for i in range(0, len(parts), 2):
        t = parts[i]
        t = re.sub(r'\$\(\\code\{(.*?)\}\)\^\{\\code\{(.*?)\}\}\$',
                   lambda m: '(`%s`) to the power (`%s`)' % (m.group(1).replace('\\$', '$'),
                                                           m.group(2).replace('\\$', '$')), t)
        t = re.sub(r'\\abs\{([^{}]*)\}', r'|\1|', t)
        t = t.replace('\\textbackslash ', '\\').replace('\\textbackslash{}', '\\')
        t = re.sub(r'`([^`\n]*\$[^`\n]*)`', _dollar_code, t)
        if plain_dollars:
            t = re.sub(r'(?<!\\)\$', r'\\$', t)
        # C++ text such as `class <template T>` outside backticks would open a raw HTML
        # element (Goldmark runs with unsafe HTML), so only known tags stay live
        spans = re.split(r'(`[^`\n]*`)', t)
        t = ''.join(s if s.startswith('`') else re.sub(r'<(?!/?(?:%s)\b)(?=/?[A-Za-z])' % SAFE_TAGS, '&lt;', s)
                    for s in spans)
        parts[i] = t
    return ''.join(parts)


def render(q, n, ex):
    head = f'### {n} · {q["title"]}' if q['title'] else f'### {n}'
    out = [head, '', f'*Asked by: {q["asked"]}*', '', fix_md(q['stem']), '']
    if q['fig']:
        out += [f'<figure class="nb-fig"><img src="{q["fig"]}" alt="Figure for question {n}" loading="lazy"></figure>', '']
    if q['code']:
        out += ['```' + (q['lang'] or 'c'), q['code'], '```', '']
    if q['options']:
        out += [f'- **({q["letters"][i].lower()})** {fix_md(o)}' for i, o in enumerate(q['options'])]
        out.append('')
    body = ex.get(q['id'])
    body = fix_md(body, plain_dollars=True) if body is not None else fix_md('**Answer.** ' + q['answer'])
    out += ['{{< details title="Answer and explanation" closed="true" >}}', '', body, '', '{{< /details >}}', '']
    return '\n'.join(out)


def main():
    qs = load_questions()
    ex = load_explanations()
    unknown = set(ex) - {q['id'] for q in qs}
    if unknown:
        sys.exit(f'build: explanations for unknown ids: {sorted(unknown)}')
    tree = defaultdict(lambda: defaultdict(list))
    for q in qs:
        tree[q['subject']][q['topic']].append(q)

    total_missing = 0
    cards = []
    for w, (subj, icon) in enumerate(SUBJECTS, 1):
        topics = tree.get(subj)
        if not topics:
            continue
        sdir = os.path.join(OUT, slug(subj))
        os.makedirs(sdir, exist_ok=True)
        for old in glob.glob(os.path.join(sdir, '*.md')):
            os.remove(old)
        order = sorted(topics, key=lambda t: (-len(topics[t]), t))
        n_subj = sum(len(v) for v in topics.values())
        rows = []
        for tw, t in enumerate(order, 1):
            items = sorted(topics[t], key=lambda q: (q['companies'][0], q['id']))
            companies = sorted({c for q in items for c in q['companies']})
            missing = sum(1 for q in items if q['id'] not in ex)
            total_missing += missing
            page = [
                '---', f'title: {yaml_str(t)}', f'weight: {tw}', '---', '',
                f'{len(items)} question{"s" if len(items) != 1 else ""} asked by '
                f'{", ".join(companies)}. Try each one first, then open the toggle: it gives the answer, '
                'why it is right, and the idea behind it explained from scratch.', '',
            ]
            page += [render(q, i, ex) for i, q in enumerate(items, 1)]
            with open(os.path.join(sdir, slug(t) + '.md'), 'w', encoding='utf8', newline='\n') as fh:
                fh.write('\n'.join(page))
            rows.append(f'| [{t}]({slug(t)}) | {len(items)} | {", ".join(companies)} |')
            if missing:
                print(f'  {missing:3d} without explanation: {subj} / {t}')
        index = [
            '---', f'title: {yaml_str(subj)}', f'weight: {w}', '---', '',
            f'{n_subj} questions from company tests, grouped by topic. Every answer explains the reasoning '
            'and the concept it uses.', '',
            '| Topic | Questions | Asked by |', '|---|---|---|', *rows, '',
        ]
        with open(os.path.join(sdir, '_index.md'), 'w', encoding='utf8', newline='\n') as fh:
            fh.write('\n'.join(index))
        cards.append((subj, icon, n_subj))

    block = ['{{< cards >}}']
    block += [f'  {{{{< card link="/question-bank/{slug(s)}/" title={yaml_str(s)} subtitle="{n} questions" '
              f'icon="{icon}" >}}}}' for s, icon, n in cards]
    block.append('{{< /cards >}}')
    index = os.path.join(OUT, '_index.md')
    with open(index, encoding='utf8') as fh:
        text = fh.read()
    a, b = text.index(CARDS_START) + len(CARDS_START), text.index(CARDS_END)
    with open(index, 'w', encoding='utf8', newline='\n') as fh:
        fh.write(text[:a] + '\n' + '\n'.join(block) + '\n' + text[b:])
    print(f'{len(qs)} questions, {len(qs) - total_missing} explained, {total_missing} missing')


if __name__ == '__main__':
    main()
