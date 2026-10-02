def solution(chain, elements):
    need = {e: 0 for e in elements}                 # occurrences inside the current window
    required = len(need)
    covered = 0
    best = (len(chain) + 1, 0, 0)
    left = 0
    for right, x in enumerate(chain):
        if x in need:
            need[x] += 1
            if need[x] == 1:
                covered += 1
        while covered == required:
            if right - left + 1 < best[0]:
                best = (right - left + 1, left, right)
            y = chain[left]
            if y in need:
                need[y] -= 1
                if need[y] == 0:
                    covered -= 1
            left += 1
    if best[0] > len(chain):
        return []
    return chain[best[1]:best[2] + 1]

# ---- tests
import random
assert solution(["O", "C", "Ra", "Li", "Na"], ["Li", "C"]) == ["C", "Ra", "Li"]
assert solution(["a", "b"], ["z"]) == []
def brute(ch, el):
    best = None
    for i in range(len(ch)):
        for j in range(i, len(ch)):
            if set(el) <= set(ch[i:j + 1]) and (best is None or j - i < len(best) - 1): best = ch[i:j + 1]
    return best or []
for _ in range(400):
    ch = [random.choice('abcd') for _ in range(random.randint(1, 10))]
    el = random.sample('abcde', random.randint(1, 3))
    assert solution(ch, el) == brute(ch, el), (ch, el)
print('ok')
