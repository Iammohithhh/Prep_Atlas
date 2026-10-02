import numpy as np

def softmax(s):
    e = np.exp(s - s.max())
    return e / e.sum()

class CachedAttention:
    def __init__(self, Wq, Wk, Wv):
        self.Wq, self.Wk, self.Wv = Wq, Wk, Wv
        self.K, self.V = [], []

    def step(self, x):
        q, k, v = x @ self.Wq, x @ self.Wk, x @ self.Wv
        self.K.append(k); self.V.append(v)
        K, V = np.stack(self.K), np.stack(self.V)
        w = softmax(K @ q / np.sqrt(len(q)))
        return w @ V

def full_causal(X, Wq, Wk, Wv):
    Q, K, V = X @ Wq, X @ Wk, X @ Wv
    t = len(X)
    S = np.where(np.tril(np.ones((t, t), bool)), Q @ K.T / np.sqrt(Q.shape[1]), -1e30)
    E = np.exp(S - S.max(1, keepdims=True))
    return (E / E.sum(1, keepdims=True)) @ V

rng = np.random.default_rng(0)
d = 6
Wq, Wk, Wv = (rng.normal(size=(d, d)) for _ in range(3))
X = rng.normal(size=(7, d))
att = CachedAttention(Wq, Wk, Wv)
out = np.stack([att.step(x) for x in X])
assert np.allclose(out, full_causal(X, Wq, Wk, Wv))
print("ok")
