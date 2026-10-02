class TopSolvers:
    """Leaderboard of the K best users when solved counts only grow."""

    def __init__(self, k=10):
        self.k = k
        self.count = {}                       # every user -> solved count
        self.top = {}                         # at most k users that are currently on the board

    def update(self, user, solved):
        self.count[user] = solved
        if user in self.top or len(self.top) < self.k:
            self.top[user] = solved
            return
        worst = max(self.top, key=lambda u: (-self.top[u], u))      # lowest count, then largest name
        if (-solved, user) < (-self.top[worst], worst):
            del self.top[worst]
            self.top[user] = solved

    def top_list(self):
        return sorted(self.top.items(), key=lambda kv: (-kv[1], kv[0]))

# ---- tests
import random
def brute(counts, k):
    return sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))[:k]
for _ in range(300):
    k = random.randint(1, 4)
    board = TopSolvers(k)
    counts = {}
    for _ in range(40):
        u = random.choice('abcdefgh')
        counts[u] = counts.get(u, 0) + random.randint(1, 3)      # solved counts never decrease
        board.update(u, counts[u])
        assert board.top_list() == brute(counts, k)
print('ok')
