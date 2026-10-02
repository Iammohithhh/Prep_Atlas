import numpy as np

def masked_mha(X, Wq, Wk, Wv, Wo, h, key_valid=None):
    t, d = X.shape
    dh = d // h
    sp = lambda M: (X @ M).reshape(t, h, dh).transpose(1, 0, 2)
    Q, K, V = sp(Wq), sp(Wk), sp(Wv)
    S = Q @ K.transpose(0, 2, 1) / np.sqrt(dh)
    allowed = np.tril(np.ones((t, t), bool))
    if key_valid is not None:
        allowed = allowed & np.asarray(key_valid, bool)[None, :]
        allowed |= np.eye(t, dtype=bool)               # a token can always see itself
    S = np.where(allowed[None], S, -1e30)
    A = np.exp(S - S.max(-1, keepdims=True))
    A /= A.sum(-1, keepdims=True)
    return (A @ V).transpose(1, 0, 2).reshape(t, d) @ Wo

rng = np.random.default_rng(0)
d, h, t = 8, 2, 6
Wq, Wk, Wv, Wo = (rng.normal(size=(d, d)) for _ in range(4))
X = rng.normal(size=(t, d))
out = masked_mha(X, Wq, Wk, Wv, Wo, h)
out3 = masked_mha(X[:3], Wq, Wk, Wv, Wo, h)
assert np.allclose(out[:3], out3)                       # causality
valid = [1, 1, 1, 1, 0, 0]
Xp = X.copy(); Xp[4:] = 99.0                            # padding content must not matter for earlier tokens
assert np.allclose(masked_mha(Xp, Wq, Wk, Wv, Wo, h, valid)[:4], masked_mha(X, Wq, Wk, Wv, Wo, h, valid)[:4])
print("ok")
