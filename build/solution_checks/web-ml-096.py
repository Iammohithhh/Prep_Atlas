import numpy as np

def kmeans(X, k, iters=100, seed=0):
    X = np.asarray(X, float)
    rng = np.random.default_rng(seed)
    C = [X[rng.integers(len(X))]]
    for _ in range(k - 1):
        d2 = np.min([((X - c) ** 2).sum(1) for c in C], axis=0)
        C.append(X[rng.choice(len(X), p=d2 / d2.sum())] if d2.sum() > 0 else X[rng.integers(len(X))])
    C = np.array(C)
    labels = None
    for _ in range(iters):
        d2 = ((X[:, None, :] - C[None]) ** 2).sum(-1)
        new = d2.argmin(1)
        if labels is not None and np.array_equal(new, labels):
            break
        labels = new
        for j in range(k):
            pts = X[labels == j]
            C[j] = pts.mean(0) if len(pts) else X[d2.min(1).argmax()]
    return C, labels

rng = np.random.default_rng(0)
X = np.vstack([rng.normal(0, 0.1, (30, 2)), rng.normal(5, 0.1, (30, 2))])
C, lab = kmeans(X, 2)
assert len(set(lab[:30])) == 1 and len(set(lab[30:])) == 1 and lab[0] != lab[-1]
assert np.allclose(sorted(C[:, 0]), [0, 5], atol=0.2)
print("ok")
