import numpy as np

def sigmoid(z):
    return 1 / (1 + np.exp(-np.clip(z, -500, 500)))

def fit_logistic(X, y, lr=0.5, steps=3000, l2=0.0):
    X, y = np.asarray(X, float), np.asarray(y, float)
    w, b = np.zeros(X.shape[1]), 0.0
    for _ in range(steps):
        p = sigmoid(X @ w + b)
        w -= lr * (X.T @ (p - y) / len(y) + l2 * w)
        b -= lr * (p - y).mean()
    return w, b

def fit_linear(X, y):
    A = np.hstack([np.asarray(X, float), np.ones((len(X), 1))])
    sol = np.linalg.lstsq(A, np.asarray(y, float), rcond=None)[0]
    return sol[:-1], sol[-1]

rng = np.random.default_rng(0)
X = np.vstack([rng.normal(-2, 1, (50, 1)), rng.normal(2, 1, (50, 1))])
y = np.array([0] * 50 + [1] * 50)
w, b = fit_logistic(X, y)
acc = ((sigmoid(X @ w + b) > 0.5) == y).mean()
assert acc > 0.9 and w[0] > 0
wl, bl = fit_linear([[0], [1], [2]], [1, 3, 5])
assert np.allclose([wl[0], bl], [2, 1])
print("ok")
