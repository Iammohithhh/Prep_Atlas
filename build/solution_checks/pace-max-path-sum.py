import random

def maxPathSum(board, p, q):
    n, m = len(board), len(board[0])
    def run(rows, start):
        dp = [None] * m
        dp[start] = rows[0][start]
        for r in rows[1:]:
            nd = [None] * m
            for j in range(m):
                best = None
                for k in (j - 1, j, j + 1):
                    if 0 <= k < m and dp[k] is not None and (best is None or dp[k] > best):
                        best = dp[k]
                if best is not None:
                    nd[j] = best + r[j]
            dp = nd
        return max(v for v in dp if v is not None)
    return max(run(board, p), run(board[::-1], q))

def brute(board, p, q):
    n, m = len(board), len(board[0])
    best = [-10**9]
    def dfs(rows, i, j, s):
        s += rows[i][j]
        if i == len(rows) - 1:
            best[0] = max(best[0], s); return
        for d in (-1, 0, 1):
            if 0 <= j + d < m: dfs(rows, i + 1, j + d, s)
    dfs(board, 0, p, 0); dfs(board[::-1], 0, q, 0)
    return best[0]

assert maxPathSum([[1,2,3],[4,5,6],[7,8,9]], 1, 0) == 17
for _ in range(300):
    n = random.randint(1, 5); m = random.randint(1, 4)
    b = [[random.randint(-5, 9) for _ in range(m)] for _ in range(n)]
    p, q = random.randrange(m), random.randrange(m)
    assert maxPathSum(b, p, q) == brute(b, p, q)
print('ok')
