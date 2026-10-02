MOD = 10**9 + 7


def get_infection_sequences_count(n, infected):
    pos = sorted(infected)
    counts = {}                                      # day -> how many houses get infected that day

    def add(d, c):
        counts[d] = counts.get(d, 0) + c

    for d in range(1, pos[0]):                       # left end gap: houses 1..pos[0]-1, infected one per day
        add(d, 1)
    for d in range(1, n - pos[-1] + 1):              # right end gap
        add(d, 1)
    for a, b in zip(pos, pos[1:]):                   # inner gaps are infected from both sides
        g = b - a - 1
        for d in range(1, (g + 1) // 2 + 1):
            add(d, 1 if (g % 2 == 1 and d == (g + 1) // 2) else 2)
    fact = [1] * (n + 1)
    for i in range(1, n + 1):
        fact[i] = fact[i - 1] * i % MOD
    ans = 1
    for c in counts.values():
        ans = ans * fact[c] % MOD
    return ans

# ---- tests
import random
assert get_infection_sequences_count(5, [1, 5]) == 2
assert get_infection_sequences_count(6, [3, 5]) == 6
from itertools import permutations
def brute(n, inf):
    infected = set(inf); days = []
    while len(infected) < n:
        new = set()
        for h in infected:
            for nb in (h - 1, h + 1):
                if 1 <= nb <= n and nb not in infected: new.add(nb)
        days.append(sorted(new)); infected |= new
    seqs = {()}
    for d in days:
        seqs = {s + p for s in seqs for p in permutations(d)}
    return len(seqs) % MOD
for _ in range(200):
    n = random.randint(2, 8); m = random.randint(1, n - 1)
    inf = random.sample(range(1, n + 1), m)
    assert get_infection_sequences_count(n, inf) == brute(n, inf), (n, inf)
get_infection_sequences_count(10**5, [1, 10**5])
print('ok')
