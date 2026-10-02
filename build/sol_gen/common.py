import json, sys
from pathlib import Path

D = {}


def T(definition, intuition='', math='', example='', tradeoffs='', followups=()):
    out = '### Definition\n' + definition.strip() + '\n'
    if intuition:
        out += '\n### Intuition\n' + intuition.strip() + '\n'
    if math:
        out += '\n### The math\n' + math.strip() + '\n'
    if example:
        out += '\n### Concrete example\n' + example.strip() + '\n'
    if tradeoffs:
        out += '\n### Trade-offs and when to use what\n' + tradeoffs.strip() + '\n'
    if followups:
        out += '\n### Likely follow-ups\n' + '\n'.join(f'- **{q}** {a}' for q, a in followups) + '\n'
    return out


def S(body, wrong='', fast='', traps=''):
    out = '### Solution\n' + body.strip() + '\n'
    if wrong:
        out += '\n### Why the other options are wrong\n' + wrong.strip() + '\n'
    if fast:
        out += '\n### Faster method\n' + fast.strip() + '\n'
    if traps:
        out += '\n### Common traps\n' + traps.strip() + '\n'
    return out



def save(name):
    Path('build/solutions/'+name).write_text(json.dumps(D, indent=1, ensure_ascii=False), encoding='utf-8')
    print(name, len(D))
