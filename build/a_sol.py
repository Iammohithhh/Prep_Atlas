"""Worker A helper: assemble a detailed coding solution from a verified check file."""
from pathlib import Path
CHK = Path(__file__).resolve().parent / 'solution_checks'


def code(key):
    return (CHK / f'{key}.py').read_text(encoding='utf-8').split('# ---- tests')[0].strip()


def sol(key, intuition, approach, why, complexity, dry, edge):
    ap = '\n'.join(f'{i}. {s}' for i, s in enumerate(approach, 1))
    eg = '\n'.join(f'- {s}' for s in edge)
    return (f'### Intuition\n{intuition}\n\n### Approach\n{ap}\n\n### Why it works\n{why}\n\n### Complexity\n{complexity}\n\n'
            f'### Python solution\n```python\n{code(key)}\n```\n\n### Dry run\n{dry}\n\n### Edge cases & pitfalls\n{eg}\n')
