import numpy as np

def forward(x, y, p):
    z1 = x @ p['W1'] + p['b1']
    a1 = np.maximum(z1, 0)
    yh = a1 @ p['W2'] + p['b2']
    return np.mean((yh - y) ** 2), (x, z1, a1, yh)

def backward(y, cache, p):
    x, z1, a1, yh = cache
    dy = 2 * (yh - y) / y.size
    g = {'W2': a1.T @ dy, 'b2': dy.sum(0)}
    dz1 = (dy @ p['W2'].T) * (z1 > 0)
    g['W1'] = x.T @ dz1
    g['b1'] = dz1.sum(0)
    return g

rng = np.random.default_rng(0)
p = dict(W1=rng.normal(size=(3, 4)), b1=rng.normal(size=4), W2=rng.normal(size=(4, 2)), b2=rng.normal(size=2))
x, y = rng.normal(size=(5, 3)), rng.normal(size=(5, 2))
L, cache = forward(x, y, p)
g = backward(y, cache, p)
for name in p:
    num = np.zeros_like(p[name])
    it = np.nditer(p[name], flags=['multi_index'])
    for _ in it:
        idx = it.multi_index
        p[name][idx] += 1e-6; Lp = forward(x, y, p)[0]
        p[name][idx] -= 2e-6; Lm = forward(x, y, p)[0]
        p[name][idx] += 1e-6
        num[idx] = (Lp - Lm) / 2e-6
    assert np.allclose(g[name], num, atol=1e-5), name
print("ok")
