"""Print the questions of one subject (optionally one topic) with their short catalogue answers.

    python tools/question_bank/dump.py "Quantitative aptitude" ["Probability"] [--missing]

Used while writing explain/ blocks; --missing skips questions that already have one.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build  # noqa: E402

args = [a for a in sys.argv[1:] if not a.startswith('--')]
subj, topic = args[0], (args[1] if len(args) > 1 else None)
ex = build.load_explanations() if '--missing' in sys.argv else {}
sys.stdout.reconfigure(encoding='utf8')
for q in sorted(build.load_questions(), key=lambda q: (q['topic'], q['companies'][0], q['id'])):
    if q['subject'] != subj or (topic and q['topic'] != topic) or q['id'] in ex:
        continue
    print(f"=== {q['id']}  [{q['topic']}]  {q['title']}  <{q['asked']}>")
    print(q['stem'])
    if q['fig']:
        print('[figure', q['fig'] + ']')
    if q['code']:
        print('```\n' + q['code'] + '\n```')
    for i, o in enumerate(q['options']):
        print(f"  ({q['letters'][i].lower()}) {o}")
    print('ANS:', q['answer'])
    print()
