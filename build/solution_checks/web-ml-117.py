import csv, io
import numpy as np

def load(text):
    rows = list(csv.DictReader(io.StringIO(text)))
    cols = [c for c in rows[0] if c != 'y']
    X = np.array([[float(r[c]) if r[c] != '' else np.nan for c in cols] for r in rows])
    y = np.array([float(r['y']) for r in rows])
    return X, y

def baseline(X, y, train_frac=0.7, lr=0.5, steps=1500):
    n = int(len(y) * train_frac)                       # time-ordered split
    Xtr, Xte, ytr, yte = X[:n], X[n:], y[:n], y[n:]
    med = np.nanmedian(Xtr, axis=0)
    fill = lambda A: np.where(np.isnan(A), med, A)
    Xtr, Xte = fill(Xtr), fill(Xte)
    mu, sd = Xtr.mean(0), Xtr.std(0) + 1e-9
    Xtr, Xte = (Xtr - mu) / sd, (Xte - mu) / sd
    w, b = np.zeros(X.shape[1]), 0.0
    for _ in range(steps):
        p = 1 / (1 + np.exp(-(Xtr @ w + b)))
        w -= lr * Xtr.T @ (p - ytr) / n
        b -= lr * np.mean(p - ytr)
    acc = ((Xte @ w + b > 0) == yte).mean()
    majority = max(yte.mean(), 1 - yte.mean())
    return acc, majority

rng = np.random.default_rng(0)
lines = ['a,b,y']
for _ in range(200):
    a, b_ = rng.normal(), rng.normal()
    y = int(a + 0.5 * b_ > 0)
    lines.append(f"{a:.4f},{'' if rng.random() < 0.1 else f'{b_:.4f}'},{y}")
X, y = load('\n'.join(lines))
acc, maj = baseline(X, y)
assert acc > 0.8 and acc > maj
print("ok")
