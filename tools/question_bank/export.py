"""Export every non-coding company question to questions.json for the subject-wise Question Bank.

    python tools/question_bank/export.py

Sources
  * company-questions/catalogue/*.yaml (the 883-question company DB), grouped into
    subject -> topic with the same rules as company-questions/tools/build_md.py;
  * tools/qualcomm_core/data_*.py (156 core-subject questions from the eight Qualcomm papers);
  * content/companies/qualcomm/0[2-4]-*.md (the 60-question Qualcomm assessment).

questions.json is committed, so build.py runs without the company-questions folder.
Topics for the Qualcomm questions are set in extras_topics.py.
"""
import json
import os
import re
import sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
BOOK = os.path.abspath(os.path.join(ROOT, '..', 'company-questions'))
OUT = os.path.join(HERE, 'questions.json')

sys.path.insert(0, os.path.join(BOOK, 'tools'))
sys.path.insert(0, os.path.join(ROOT, 'tools', 'qualcomm_core'))
sys.path.insert(0, HERE)
import build_md as B  # noqa: E402
import extras_topics as X  # noqa: E402


MARK = '\x00'


def md(s):
    """build_md.md, but a LaTeX \\$ (a literal dollar) stays escaped as \\$ in the Markdown, so
    Hugo's math passthrough does not pair currency signs as $...$ (inside inline code it is
    a plain $)."""
    out = B.md(str(s).replace('\\$', MARK) if s is not None else s)
    parts = re.split(r'(`[^`\n]*`)', out)
    return ''.join(p.replace(MARK, '$') if p.startswith('`') else p.replace(MARK, '\\$')
                   for p in parts)


def one_line(s):
    return re.sub(r'\s+', ' ', md(s)).strip()


def catalogue():
    byid = B.load()
    dups = defaultdict(list)
    for q in byid.values():
        if q.get('dup_of'):
            dups[q['dup_of']].append(q)
    out = []
    for q in byid.values():
        if q.get('dup_of') or q['subject'] == 'Coding problems':
            continue
        ts = B.topics_of(q)
        code = B.read_code(q)
        out.append({
            'id': q['id'],
            'subject': q['subject'],
            'topic': ts[0],
            'also': ts[1:],
            'title': one_line(q.get('title') or ''),
            'asked': B.asked_by(q, dups[q['id']]),
            'companies': sorted({r['_co'] for r in [q] + dups[q['id']]}),
            'stem': md(q.get('stem')),
            'code': code[0] if code else '',
            'lang': code[1] if code else '',
            'options': [one_line(o) for o in q.get('options') or []],
            'letters': 'abcdefgh',
            'answer': md(q.get('answer')),
            'fig': '',
        })
    return out


def qualcomm_core():
    import qdef
    from data_os_oop import OOP, OS
    from data_arch import ARCH
    from data_dig import DIG
    out = []
    for key, rows in (('oop', OOP), ('os', OS), ('arch', ARCH), ('dig', DIG)):
        for i, q in enumerate(rows, 1):
            qid = f'qcc-{key}-{i:02d}'
            subj, topic = X.CORE[key](q.topic)
            asked = ' · '.join(f"Qualcomm ({qdef.PAPERS[p]}{', Q%d' % n if n else ''})" for p, n in q.src)
            stem = q.text + ('\n\n' + q.table if q.table else '')
            if q.conf == 'flag':
                ans = '**No reliable pick.** ' + q.note + '\n\n' + q.expl
            else:
                ans = f'**{q.ans}.** ' + q.expl
                if q.conf == 'medium' and q.note:
                    ans += '\n\n*Less certain:* ' + q.note
            out.append({
                'id': qid, 'subject': subj, 'topic': topic, 'also': [], 'title': q.topic,
                'asked': asked, 'companies': ['Qualcomm'], 'stem': stem, 'code': q.code,
                'lang': 'c' if q.code else '', 'options': list(q.opts), 'letters': 'ABCD',
                'answer': ans, 'fig': f'/companies/qualcomm/core/{q.fig}.svg' if q.fig else '',
            })
    return out


def qualcomm_60():
    out = []
    pages = ['02-aptitude.md', '03-programming-basics.md', '04-computer-science.md']
    for page in pages:
        with open(os.path.join(ROOT, 'content', 'companies', 'qualcomm', page), encoding='utf8') as fh:
            text = fh.read()
        for m in re.finditer(r'^### Q(\d+) · (.*?)\n(.*?)(?=^### Q\d+ · |\Z)', text, re.S | re.M):
            n, section, body = int(m.group(1)), m.group(2).strip(), m.group(3)
            stem, _, rest = body.partition('**Options**')
            opts_part, _, ans_part = rest.partition('{{< details')
            opts = re.findall(r'^- \*\*[A-E]\.\*\* (.*)$', opts_part, re.M)
            ans = ans_part.split('>}}', 1)[1].rsplit('{{< /details >}}', 1)[0].strip()
            subj, topic = X.Q60[n]
            out.append({
                'id': f'qc60-{n:02d}', 'subject': subj, 'topic': topic, 'also': [],
                'title': section, 'asked': 'Qualcomm (60-question online assessment)',
                'companies': ['Qualcomm'], 'stem': stem.strip(), 'code': '', 'lang': '',
                'options': opts, 'letters': 'ABCDE', 'answer': ans, 'fig': '',
            })
    if len(out) != 60:
        sys.exit(f'export: expected 60 Qualcomm assessment questions, parsed {len(out)}')
    return out


def main():
    qs = catalogue() + qualcomm_core() + qualcomm_60()
    with open(OUT, 'w', encoding='utf8', newline='\n') as fh:
        json.dump(qs, fh, ensure_ascii=False, indent=1)
    by = defaultdict(int)
    for q in qs:
        by[(q['subject'], q['topic'])] += 1
    print(f'wrote {OUT}: {len(qs)} questions')
    for (s, t), n in sorted(by.items()):
        print(f'{n:4d}  {s} / {t}')


if __name__ == '__main__':
    main()
