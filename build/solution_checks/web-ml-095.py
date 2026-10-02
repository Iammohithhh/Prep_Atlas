import numpy as np

def ln(x, eps=1e-5):
    return (x - x.mean(-1, keepdims=True)) / np.sqrt(x.var(-1, keepdims=True) + eps)

def gelu(x):
    return 0.5 * x * (1 + np.tanh(np.sqrt(2 / np.pi) * (x + 0.044715 * x ** 3)))

def causal_attn(x, p):
    t = x.shape[0]
    Q, K, V = x @ p['q'], x @ p['k'], x @ p['v']
    S = np.where(np.tril(np.ones((t, t), bool)), Q @ K.T / np.sqrt(Q.shape[1]), -1e30)
    A = np.exp(S - S.max(1, keepdims=True))
    return (A / A.sum(1, keepdims=True)) @ V @ p['o']

def gpt_forward(tokens, params):
    x = params['E'][tokens] + params['P'][:len(tokens)]
    for b in params['blocks']:
        x = x + causal_attn(ln(x), b)
        x = x + gelu(ln(x) @ b['w1']) @ b['w2']
    return ln(x) @ params['E'].T

def init(vocab=11, d=8, ctx=16, layers=2, rng=None):
    rng = rng or np.random.default_rng(0)
    mk = lambda *s: rng.normal(0, 0.3, s)
    blocks = [dict(q=mk(d, d), k=mk(d, d), v=mk(d, d), o=mk(d, d), w1=mk(d, 4 * d), w2=mk(4 * d, d)) for _ in range(layers)]
    return dict(E=mk(vocab, d), P=mk(ctx, d), blocks=blocks)

params = init()
a = np.array([1, 2, 3, 4, 5])
b = np.array([1, 2, 3, 9, 9])
la, lb = gpt_forward(a, params), gpt_forward(b, params)
assert la.shape == (5, 11)
assert np.allclose(la[:3], lb[:3])          # changing future tokens does not change earlier logits
assert not np.allclose(la[3:], lb[3:])
print("ok")
