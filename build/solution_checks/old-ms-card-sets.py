RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
SUITS = ['S', 'H', 'D', 'C']


def strongest_set(cards):
    by_rank = {}
    by_suit = {s: [] for s in SUITS}
    for c in cards:
        rank, suit = c[:-1], c[-1]
        by_rank.setdefault(rank, []).append(c)
        by_suit[suit].append(c)
    rk = lambda r: RANKS.index(r)
    ranks_desc = sorted(by_rank, key=rk, reverse=True)
    # 6. a triple and a pair
    for r in ranks_desc:
        if len(by_rank[r]) >= 3:
            for p in ranks_desc:
                if p != r and len(by_rank[p]) >= 2:
                    return 'a triple and a pair', by_rank[r][:3] + by_rank[p][:2]
    # 5. suit (five cards of one suit)
    for s in SUITS:
        if len(by_suit[s]) >= 5:
            top = sorted(by_suit[s], key=lambda c: rk(c[:-1]), reverse=True)[:5]
            return 'suit', top
    # 4. five in a row
    for hi in range(12, 3, -1):
        window = [RANKS[i] for i in range(hi - 4, hi + 1)]
        if all(r in by_rank for r in window):
            return 'five in a row', [by_rank[r][0] for r in window]
    # 3. triple, 2. pair
    for r in ranks_desc:
        if len(by_rank[r]) >= 3:
            return 'triple', by_rank[r][:3]
    for r in ranks_desc:
        if len(by_rank[r]) >= 2:
            return 'pair', by_rank[r][:2]
    return 'single card', [by_rank[ranks_desc[0]][0]]

# ---- tests
name, sel = strongest_set(["10D", "10H", "10C", "2S", "2H", "2D", "JH", "JC"])
assert name == 'a triple and a pair' and sorted(sel) == sorted(["10D", "10H", "10C", "JH", "JC"])
assert strongest_set(["2S", "5H", "KD"]) == ('single card', ['KD'])
assert strongest_set(["3S", "3H", "9D"])[0] == 'pair'
assert strongest_set(["5S", "6H", "7D", "8C", "9S"])[0] == 'five in a row'
assert strongest_set(["2S", "5S", "7S", "9S", "KS", "3H"])[0] == 'suit'
print('ok')
