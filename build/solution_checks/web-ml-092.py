import numpy as np

def layer_norm(x, eps=1e-5):
    mu = x.mean(-1, keepdims=True)
    var = x.var(-1, keepdims=True)
    return (x - mu) / np.sqrt(var + eps)

def silu(a):
    return a / (1.0 + np.exp(-a))

def attn(x, Wq, Wk, Wv, causal=True):
    Q, K, V = x @ Wq, x @ Wk, x @ Wv
    S = Q @ K.T / np.sqrt(Q.shape[-1])
    if causal:
        S = np.where(np.tril(np.ones_like(S, dtype=bool)), S, -1e30)
    S = S - S.max(-1, keepdims=True)
    W = np.exp(S)
    return (W / W.sum(-1, keepdims=True)) @ V

def block(x, p):
    y = x + attn(layer_norm(x), p['Wq'], p['Wk'], p['Wv']) @ p['Wo']
    u = layer_norm(y)
    h = silu(u @ p['W1']) * (u @ p['W3'])
    return y + h @ p['W2']

rng = np.random.default_rng(0)
d, dff = 8, 16
p = {k: rng.normal(0, 0.3, s) for k, s in dict(Wq=(d, d), Wk=(d, d), Wv=(d, d), Wo=(d, d), W1=(d, dff), W3=(d, dff), W2=(dff, d)).items()}
x = rng.normal(size=(6, d))
out = block(x, p)
assert out.shape == x.shape
out_short = block(x[:4], p)
assert np.allclose(out[:4], out_short)         # causal: later tokens do not change earlier outputs
print("ok")
