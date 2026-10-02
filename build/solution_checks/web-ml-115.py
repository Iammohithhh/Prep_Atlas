import numpy as np

def bce_with_logits(z, y):
    z, y = np.asarray(z, float), np.asarray(y, float)
    return float(np.mean(np.maximum(z, 0) - z * y + np.log1p(np.exp(-np.abs(z)))))

def fit(X, y, lr=0.5, steps=2000):
    w, b = np.zeros(X.shape[1]), 0.0
    for _ in range(steps):
        z = X @ w + b
        p = 1 / (1 + np.exp(-np.clip(z, -500, 500)))
        w -= lr * X.T @ (p - y) / len(y)
        b -= lr * np.mean(p - y)
    return w, b

z = np.array([-800.0, 0.0, 800.0]); y = np.array([0, 1, 1])
assert abs(bce_with_logits(z, y) - np.log(2) / 3) < 1e-12
naive = lambda z, y: -np.mean(y * np.log(1 / (1 + np.exp(-z))) + (1 - y) * np.log(1 - 1 / (1 + np.exp(-z))))
zz = np.array([0.3, -1.2, 2.0]); yy = np.array([1, 0, 1])
assert abs(bce_with_logits(zz, yy) - naive(zz, yy)) < 1e-12
rng = np.random.default_rng(0)
X = rng.normal(size=(100, 2)); y = (X[:, 0] - X[:, 1] > 0).astype(float)
w, b = fit(X, y)
assert ((X @ w + b > 0) == y).mean() > 0.95
print("ok")
