import numpy as np

def attention(Q, K, V, causal=False):
    Q, K, V = (np.asarray(a, dtype=np.float64) for a in (Q, K, V))
    t, d = Q.shape
    S = Q @ K.T / np.sqrt(d)
    if causal:
        S = np.where(np.tril(np.ones((t, t), dtype=bool)), S, -np.inf)
    S = S - S.max(axis=1, keepdims=True)
    W = np.exp(S)
    W = W / W.sum(axis=1, keepdims=True)
    return W @ V

rng = np.random.default_rng(1)
Q, K, V = rng.normal(size=(4, 3)), rng.normal(size=(4, 3)), rng.normal(size=(4, 2))
out = attention(Q, K, V, causal=True)
assert np.allclose(out[0], V[0])                       # first token only sees itself
out2 = attention(Q[:3], K[:3], V[:3], causal=True)
assert np.allclose(out[:3], out2)                      # causality: future tokens do not matter
assert attention(Q, K, V).shape == (4, 2)
print("ok")
