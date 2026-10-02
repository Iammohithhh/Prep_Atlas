import numpy as np

def forward_backward(X, y, W, b):
    z = X @ W + b
    z = z - z.max(1, keepdims=True)
    p = np.exp(z)
    p /= p.sum(1, keepdims=True)
    n = len(y)
    loss = -np.mean(np.log(p[np.arange(n), y]))
    dz = p.copy()
    dz[np.arange(n), y] -= 1
    dz /= n
    return loss, X.T @ dz, dz.sum(0)

def train(X, y, C, lr=0.5, steps=300):
    W, b = np.zeros((X.shape[1], C)), np.zeros(C)
    losses = []
    for _ in range(steps):
        loss, dW, db = forward_backward(X, y, W, b)
        W -= lr * dW
        b -= lr * db
        losses.append(loss)
    return W, b, losses

rng = np.random.default_rng(0)
X = rng.normal(size=(6, 4)); y = rng.integers(0, 3, 6)
W, b = rng.normal(size=(4, 3)), rng.normal(size=3)
loss, dW, db = forward_backward(X, y, W, b)
num = np.zeros_like(W)
for i in range(4):
    for j in range(3):
        E = np.zeros_like(W); E[i, j] = 1e-6
        num[i, j] = (forward_backward(X, y, W + E, b)[0] - forward_backward(X, y, W - E, b)[0]) / 2e-6
assert np.allclose(dW, num, atol=1e-6)
X2 = rng.normal(size=(60, 2)); y2 = (X2[:, 0] > 0).astype(int) + (X2[:, 1] > 0)
_, _, losses = train(X2, y2, 3)
assert losses[-1] < losses[0] * 0.6
print("ok")
