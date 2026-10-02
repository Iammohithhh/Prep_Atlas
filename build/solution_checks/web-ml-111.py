import numpy as np

def entropy(labels):
    _, counts = np.unique(labels, return_counts=True)
    p = counts / counts.sum()
    return float(-(p * np.log2(p)).sum())

def one_nn(Xtrain, ytrain, Q):
    Xtrain, Q = np.asarray(Xtrain, float), np.asarray(Q, float)
    D2 = (Q ** 2).sum(1)[:, None] - 2 * Q @ Xtrain.T + (Xtrain ** 2).sum(1)[None, :]
    return np.asarray(ytrain)[D2.argmin(1)]

assert abs(entropy([0, 0, 0, 0, 1, 0, 1, 1]) - 0.954434) < 1e-6
assert entropy([1, 1, 1]) == 0.0
rng = np.random.default_rng(0)
X = rng.normal(size=(20, 3)); y = rng.integers(0, 3, 20); Q = rng.normal(size=(5, 3))
ref = [y[np.argmin(((X - q) ** 2).sum(1))] for q in Q]
assert list(one_nn(X, y, Q)) == ref
print("ok")
