import numpy as np

def cross_entropy(logits, labels):
    z = np.asarray(logits, dtype=np.float64)
    y = np.asarray(labels, dtype=np.int64)
    m = z.max(axis=1, keepdims=True)
    lse = m[:, 0] + np.log(np.exp(z - m).sum(axis=1))
    return float(np.mean(lse - z[np.arange(len(y)), y]))

assert abs(cross_entropy([[0.0, 0.0]], [0]) - np.log(2)) < 1e-12
assert abs(cross_entropy([[10000.0, 0.0]], [0])) < 1e-12
assert abs(cross_entropy([[10000.0, 0.0]], [1]) - 10000.0) < 1e-6
print("ok")
