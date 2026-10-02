import numpy as np

def sigmoid(z):
    return 1 / (1 + np.exp(-np.clip(z, -500, 500)))

def loss(w, b, X, y, eps=1e-12):
    p = sigmoid(X @ w + b)
    return -np.mean(y * np.log(p + eps) + (1 - y) * np.log(1 - p + eps))

def grad(w, b, X, y):
    p = sigmoid(X @ w + b)
    return X.T @ (p - y) / len(y), np.mean(p - y)

def train(X, y, lr=0.5, steps=500):
    w, b = np.zeros(X.shape[1]), 0.0
    for _ in range(steps):
        gw, gb = grad(w, b, X, y)
        w, b = w - lr * gw, b - lr * gb
    return w, b

rng = np.random.default_rng(0)
X = rng.normal(size=(40, 3))
y = (X @ np.array([1.0, -2.0, 0.5]) > 0).astype(float)
w0, b0 = rng.normal(size=3), 0.1
gw, gb = grad(w0, b0, X, y)
e = 1e-6
num = [(loss(w0 + e * v, b0, X, y) - loss(w0 - e * v, b0, X, y)) / (2 * e) for v in np.eye(3)]
assert np.allclose(gw, num, atol=1e-6)
w, b = train(X, y)
assert loss(w, b, X, y) < loss(np.zeros(3), 0.0, X, y)
print("ok")
