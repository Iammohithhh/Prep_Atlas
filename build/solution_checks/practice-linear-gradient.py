import numpy as np

def mse_gradient(X, w, y):
    X = np.asarray(X, dtype=np.float64)
    w = np.asarray(w, dtype=np.float64)
    y = np.asarray(y, dtype=np.float64)
    r = X @ w - y
    return 2.0 * X.T @ r / len(y)

rng = np.random.default_rng(0)
X, w, y = rng.normal(size=(5, 3)), rng.normal(size=3), rng.normal(size=5)
L = lambda w_: np.mean((X @ w_ - y) ** 2)
num = np.array([(L(w + 1e-6 * e) - L(w - 1e-6 * e)) / 2e-6 for e in np.eye(3)])
assert np.allclose(mse_gradient(X, w, y), num, atol=1e-6)
print("ok")
