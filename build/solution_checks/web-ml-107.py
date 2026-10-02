import numpy as np

def matmul_backward(A, B, dC):
    return dC @ B.T, A.T @ dC

def softmax(S):
    S = S - S.max(-1, keepdims=True)
    E = np.exp(S)
    return E / E.sum(-1, keepdims=True)

def attn_forward(Q, K, V):
    A = softmax(Q @ K.T / np.sqrt(Q.shape[1]))
    return A, A @ V

def attn_backward(Q, K, V, dOut):
    A, _ = attn_forward(Q, K, V)
    dA = dOut @ V.T
    dV = A.T @ dOut
    dS = A * (dA - (dA * A).sum(-1, keepdims=True))
    dS = dS / np.sqrt(Q.shape[1])
    return dS @ K, dS.T @ Q, dV

rng = np.random.default_rng(0)
A, B = rng.normal(size=(3, 4)), rng.normal(size=(4, 2))
dC = rng.normal(size=(3, 2))
dA, dB = matmul_backward(A, B, dC)
f = lambda A_: np.sum((A_ @ B) * dC)
num = np.zeros_like(A)
for i in range(3):
    for j in range(4):
        E = np.zeros_like(A); E[i, j] = 1e-6
        num[i, j] = (f(A + E) - f(A - E)) / 2e-6
assert np.allclose(dA, num, atol=1e-6)
Q, K, V = rng.normal(size=(4, 3)), rng.normal(size=(4, 3)), rng.normal(size=(4, 2))
dOut = rng.normal(size=(4, 2))
dQ, dK, dV = attn_backward(Q, K, V, dOut)
loss = lambda Q_: np.sum(attn_forward(Q_, K, V)[1] * dOut)
numQ = np.zeros_like(Q)
for i in range(4):
    for j in range(3):
        E = np.zeros_like(Q); E[i, j] = 1e-6
        numQ[i, j] = (loss(Q + E) - loss(Q - E)) / 2e-6
assert np.allclose(dQ, numQ, atol=1e-5)
print("ok")
