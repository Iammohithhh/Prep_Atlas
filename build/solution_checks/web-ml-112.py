import numpy as np

def softmax(z, T=1.0):
    z = np.asarray(z, float) / T
    e = np.exp(z - z.max())
    return e / e.sum()

def greedy(logits):
    return int(np.argmax(logits))

def top_k_probs(logits, k, T=1.0):
    p = softmax(logits, T)
    keep = np.argsort(p)[-k:]
    q = np.zeros_like(p)
    q[keep] = p[keep]
    return q / q.sum()

def top_p_probs(logits, top_p, T=1.0):
    p = softmax(logits, T)
    order = np.argsort(-p)
    cum = np.cumsum(p[order])
    cutoff = np.searchsorted(cum, top_p - 1e-9) + 1   # smallest prefix with cum >= top_p (tolerance for rounding)
    q = np.zeros_like(p)
    q[order[:cutoff]] = p[order[:cutoff]]
    return q / q.sum()

def sample(probs, rng):
    return int(rng.choice(len(probs), p=probs))

logits = np.log([0.5, 0.3, 0.15, 0.05])
assert greedy(logits) == 0
assert np.allclose(top_k_probs(logits, 2), [0.625, 0.375, 0, 0])
assert np.allclose(top_p_probs(logits, 0.8), [0.625, 0.375, 0, 0])       # 0.5 + 0.3 >= 0.8
assert np.allclose(top_p_probs(logits, 0.4), [1, 0, 0, 0])               # always keep at least the top token
rng = np.random.default_rng(0)
draws = [sample(top_k_probs(logits, 2), rng) for _ in range(2000)]
assert set(draws) == {0, 1}
print("ok")
