import numpy as np

def mha(X, Wq, Wk, Wv, Wo, h, mask=None):
    t, d = X.shape
    dh = d // h
    heads = lambda M: (X @ M).reshape(t, h, dh).transpose(1, 0, 2)
    Q, K, V = heads(Wq), heads(Wk), heads(Wv)
    S = Q @ K.transpose(0, 2, 1) / np.sqrt(dh)
    if mask is not None:
        S = np.where(mask, S, -1e30)
    S -= S.max(-1, keepdims=True)
    A = np.exp(S)
    A /= A.sum(-1, keepdims=True)
    return (A @ V).transpose(1, 0, 2).reshape(t, d) @ Wo

rng = np.random.default_rng(0)
d, h, t = 8, 4, 5
Wq, Wk, Wv, Wo = (rng.normal(size=(d, d)) for _ in range(4))
X = rng.normal(size=(t, d))
# reference: per-head loops
ref = np.zeros((t, d))
dh = d // h
heads = []
for i in range(h):
    sl = slice(i * dh, (i + 1) * dh)
    Q, K, V = X @ Wq[:, sl], X @ Wk[:, sl], X @ Wv[:, sl]
    S = Q @ K.T / np.sqrt(dh)
    A = np.exp(S - S.max(1, keepdims=True)); A /= A.sum(1, keepdims=True)
    heads.append(A @ V)
ref = np.concatenate(heads, axis=1) @ Wo
assert np.allclose(mha(X, Wq, Wk, Wv, Wo, h), ref)
print("ok")
