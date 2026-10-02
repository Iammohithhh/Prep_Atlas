import numpy as np

def stable_softmax(logits):
    z = np.asarray(logits, dtype=np.float64)
    z = z - z.max(axis=1, keepdims=True)
    e = np.exp(z)
    return e / e.sum(axis=1, keepdims=True)

out = stable_softmax([[1000, 1000], [-1000, 0], [1, 2, 3][:2]])
assert np.allclose(out[0], [0.5, 0.5]) and np.allclose(out.sum(1), 1)
assert np.allclose(stable_softmax([[0.0, 0.0, 0.0]]), 1 / 3)
print("ok")
