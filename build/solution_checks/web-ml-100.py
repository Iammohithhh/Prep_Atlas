import numpy as np

def clip_loss(img, txt, temperature=0.07):
    I = img / np.linalg.norm(img, axis=1, keepdims=True)
    T = txt / np.linalg.norm(txt, axis=1, keepdims=True)
    logits = I @ T.T / temperature
    def ce(z):
        z = z - z.max(1, keepdims=True)
        logp = z - np.log(np.exp(z).sum(1, keepdims=True))
        return -np.mean(np.diag(logp))
    return (ce(logits) + ce(logits.T)) / 2

rng = np.random.default_rng(0)
E = rng.normal(size=(8, 16))
matched = clip_loss(E, E + 0.01 * rng.normal(size=E.shape))
shuffled = clip_loss(E, E[rng.permutation(8)])
assert matched < 0.05 and shuffled > matched
assert abs(clip_loss(E, E, temperature=1e6) - np.log(8)) < 1e-3   # uninformative logits give log N
print("ok")
