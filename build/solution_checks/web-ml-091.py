import numpy as np

class MultiHeadAttention:
    def __init__(self, d_model, n_heads, rng):
        assert d_model % n_heads == 0
        self.h, self.dh = n_heads, d_model // n_heads
        self.Wq, self.Wk, self.Wv, self.Wo = (rng.normal(0, d_model ** -0.5, (d_model, d_model)) for _ in range(4))

    def __call__(self, X):
        t = X.shape[0]
        split = lambda M: (X @ M).reshape(t, self.h, self.dh).transpose(1, 0, 2)
        Q, K, V = split(self.Wq), split(self.Wk), split(self.Wv)
        S = Q @ K.transpose(0, 2, 1) / np.sqrt(self.dh)
        S = S - S.max(-1, keepdims=True)
        W = np.exp(S)
        W = W / W.sum(-1, keepdims=True)
        out = (W @ V).transpose(1, 0, 2).reshape(t, -1)
        return out @ self.Wo

rng = np.random.default_rng(0)
mha = MultiHeadAttention(8, 2, rng)
X = rng.normal(size=(5, 8))
Y = mha(X)
assert Y.shape == (5, 8)
# permuting tokens permutes the outputs (no positional information inside attention)
perm = rng.permutation(5)
assert np.allclose(mha(X[perm]), Y[perm])
print("ok")
