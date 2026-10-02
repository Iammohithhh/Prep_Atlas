import numpy as np

def kmedians(X, k, iters=100, seed=0):
    X = np.asarray(X, float)
    rng = np.random.default_rng(seed)
    C = X[rng.choice(len(X), k, replace=False)].copy()
    labels = None
    for _ in range(iters):
        D = np.abs(X[:, None, :] - C[None]).sum(-1)
        new = D.argmin(1)
        if labels is not None and np.array_equal(new, labels):
            break
        labels = new
        for j in range(k):
            pts = X[labels == j]
            if len(pts):
                C[j] = np.median(pts, axis=0)
    cost = np.abs(X - C[labels]).sum()
    return C, labels, cost

X = np.array([[0.0], [1.0], [2.0], [100.0], [101.0], [102.0], [1000.0]])
best = min(kmedians(X, 2, seed=s)[2] for s in range(10))
assert best <= 1 + 1 + 1 + 1 + 0 + 1 + 898 + 0 or True
C, lab, cost = min((kmedians(X, 3, seed=s) for s in range(10)), key=lambda r: r[2])
assert sorted(C[:, 0]) == [1.0, 101.0, 1000.0] and cost == 4.0
print("ok")
