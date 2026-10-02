import random

def ReachTeammates(N, V):
    # minimum P such that the graph (edge if Manhattan distance <= P) is connected
    INF = float('inf')
    dist = [INF] * N
    used = [False] * N
    dist[0] = 0
    ans = 0
    for _ in range(N):
        u = -1
        for i in range(N):
            if not used[i] and (u == -1 or dist[i] < dist[u]):
                u = i
        used[u] = True
        ans = max(ans, dist[u])
        for v in range(N):
            if not used[v]:
                d = abs(V[u][0] - V[v][0]) + abs(V[u][1] - V[v][1])
                if d < dist[v]:
                    dist[v] = d
    return ans

def brute(N, V):
    cand = sorted({abs(V[i][0] - V[j][0]) + abs(V[i][1] - V[j][1]) for i in range(N) for j in range(N)})
    for P in cand:
        seen = {0}
        st = [0]
        while st:
            u = st.pop()
            for v in range(N):
                if v not in seen and abs(V[u][0] - V[v][0]) + abs(V[u][1] - V[v][1]) <= P:
                    seen.add(v)
                    st.append(v)
        if len(seen) == N:
            return P

assert ReachTeammates(4, [[-10, 0], [0, 0], [10, 0], [11, 0]]) == 10
for _ in range(300):
    n = random.randint(2, 7)
    V = [[random.randint(-20, 20), random.randint(-20, 20)] for _ in range(n)]
    assert ReachTeammates(n, V) == brute(n, V)
print('ok')
