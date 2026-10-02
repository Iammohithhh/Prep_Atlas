import numpy as np

def gradient_descent(grad, x0, lr=0.1, steps=200):
    x = np.asarray(x0, float)
    for _ in range(steps):
        x = x - lr * grad(x)
    return x

def simple_vad(signal, frame=400, hop=160, k=0.5, smooth=5):
    sig = np.asarray(signal, float)
    n = 1 + max(0, (len(sig) - frame) // hop)
    e = np.array([np.log(np.sum(sig[i * hop:i * hop + frame] ** 2) + 1e-10) for i in range(n)])
    speech = e > e.mean() + k * e.std()
    pad = smooth // 2
    padded = np.pad(speech.astype(int), pad, mode='edge')
    return (np.array([np.median(padded[i:i + smooth]) for i in range(n)]) > 0.5)

x = gradient_descent(lambda x: 2 * (x - np.array([3.0, -1.0])), [0.0, 0.0])
assert np.allclose(x, [3, -1], atol=1e-6)
rng = np.random.default_rng(0)
sr = 16000
sig = 0.01 * rng.normal(size=sr)                       # 1 s of low noise
t = np.arange(4000) / sr
sig[6000:10000] += 0.5 * np.sin(2 * np.pi * 300 * t)    # 0.25 s tone as "speech"
mask = simple_vad(sig)
frames = np.arange(len(mask)) * 160 + 200               # frame centres
inside = mask[(frames > 6200) & (frames < 9800)].mean()
outside = mask[(frames < 5500) | (frames > 10500)].mean()
assert inside > 0.95 and outside < 0.05
print("ok")
