def secret_recipe(n, m, queries):
    # I_i = s_i * t + b_i with I_1 = t: s_1 = 1, b_1 = 0, s_{i+1} = -s_i, b_{i+1} = M_i - b_i
    b = [0] * (n + 1)
    for i in range(1, n):
        b[i + 1] = m[i - 1] - b[i]
    out = []
    for u, v in queries:
        if (u - v) % 2 == 0:                          # same parity: the free variable does not cancel
            out.append(-1)
        else:
            out.append(b[u] + b[v])
    return out

# ---- tests
import random
assert secret_recipe(4, [1, 2, 3], [(1, 2), (1, 3), (1, 4)]) == [1, -1, 2]
for _ in range(300):
    n = random.randint(2, 8); I = [random.randint(1, 9) for _ in range(n)]
    M = [I[i] + I[i + 1] for i in range(n - 1)]
    t = random.randint(-5, 5)
    I2 = [I[i] + (t if i % 2 == 0 else -t) for i in range(n)]       # another solution of the same equations
    assert [I2[i] + I2[i + 1] for i in range(n - 1)] == M
    for u in range(1, n + 1):
        for v in range(1, n + 1):
            ans = secret_recipe(n, M, [(u, v)])[0]
            if (u - v) % 2:
                assert ans == I[u - 1] + I[v - 1] == I2[u - 1] + I2[v - 1]
            else:
                assert ans == -1 and I[u - 1] + I[v - 1] != I2[u - 1] + I2[v - 1] or t == 0
print('ok')
