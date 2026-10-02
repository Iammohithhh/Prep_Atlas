import numpy as np

def fit_linear(X, y):
    A = np.hstack([np.asarray(X, float), np.ones((len(X), 1))])
    w, *_ = np.linalg.lstsq(A, np.asarray(y, float), rcond=None)
    return w[:-1], w[-1]

def fit_gd(X, y, lr=0.05, steps=5000):
    X, y = np.asarray(X, float), np.asarray(y, float)
    w, b = np.zeros(X.shape[1]), 0.0
    for _ in range(steps):
        r = X @ w + b - y
        w -= lr * 2 * X.T @ r / len(y)
        b -= lr * 2 * r.mean()
    return w, b

X = np.array([[1.0], [2.0], [3.0]])
y = np.array([1.0, 2.0, 2.0])
w, b = fit_linear(X, y)
assert np.allclose([w[0], b], [0.5, 2 / 3])
w2, b2 = fit_gd(X, y)
assert np.allclose([w2[0], b2], [0.5, 2 / 3], atol=1e-3)
print("ok")
