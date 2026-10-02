"""Worker A: print unsolved dsa/cs questions: a_todo.py start end"""
import json, sys, glob
d = json.load(open('site/data/questions.json', encoding='utf-8'))['questions']
have = set()
for p in glob.glob('build/solutions/*.json'): have |= set(json.load(open(p, encoding='utf-8')))
todo = [q for q in d if q['section'] in ('dsa', 'cs') and not q.get('solution') and q['id'] not in have]
todo.sort(key=lambda q: (q['section'], q['type'] != 'coding', q['id']))
s, e = int(sys.argv[1]), int(sys.argv[2])
for i, q in enumerate(todo[s:e], s):
    print(f"[{i}] {q['id']} | {q['section']}/{q['type']} | {q['title']}")
    print('  ST:', q['statement'][:1100].replace('\n', ' '))
    for k in ('function_signature', 'constraints'):
        if q.get(k): print(f'  {k}:', str(q[k])[:200])
    if q.get('examples'): print('  EX:', json.dumps(q['examples'][:2], ensure_ascii=False)[:500])
    if q.get('options'): print('  OPT:', q['options'])
    if q.get('answer') is not None: print('  ANS:', str(q['answer'])[:200])
    print('  EXPL:', (q.get('explanation') or '')[:500].replace('\n', ' '))
    print()
