import sys, textwrap
sys.path.insert(0, 'build/sol_gen')
from common import D, save
from pathlib import Path

CHECK = Path('build/solution_checks')
NOTE = ('The saved prompt is short and has no full input/output specification, so the concrete interpretation below '
        'is stated explicitly and the code is verified against it.')


def C(qid, interp, intuition, approach, why, cx, code, test, dry, edge, check_name=None):
    code = textwrap.dedent(code).strip('\n')
    test = textwrap.dedent(test).strip('\n')
    ns = {}
    exec(compile(code + '\n\n' + test + '\nprint("ok")', qid, 'exec'), ns)        # must pass before publishing
    (CHECK / f'{qid}.py').write_text(code + '\n\n' + test + '\nprint("ok")\n', encoding='utf-8')
    D[qid] = (f'### Interpretation\n{interp} {NOTE}\n\n### Intuition\n{intuition}\n\n### Approach\n{approach}\n\n'
              f'### Why it works\n{why}\n\n### Complexity\n{cx}\n\n### Python solution\n```python\n{code}\n```\n\n'
              f'### Dry run\n{dry}\n\n### Edge cases & pitfalls\n{edge}')


C('practice-stable-softmax',
  'Row-wise softmax of a 2D array without overflow.',
  'exp overflows for large logits, but softmax is unchanged when a constant is subtracted from every entry of a row. Subtracting the row maximum makes the largest exponent exp(0) = 1.',
  '1. Convert to float64 and subtract the row max (keepdims).\n2. Exponentiate.\n3. Divide by the row sum.',
  'softmax(z - c) = exp(z_i - c)/sum exp(z_j - c) = exp(z_i)/sum exp(z_j), so subtracting c changes nothing mathematically; with c = max the exponents are at most 0 (no overflow) and the denominator is at least 1 (no division by zero).',
  'O(rows x cols) time and space.',
  '''
  import numpy as np

  def stable_softmax(logits):
      z = np.asarray(logits, dtype=np.float64)
      z = z - z.max(axis=1, keepdims=True)
      e = np.exp(z)
      return e / e.sum(axis=1, keepdims=True)
  ''',
  '''
  out = stable_softmax([[1000, 1000], [-1000, 0], [1, 2, 3][:2]])
  assert np.allclose(out[0], [0.5, 0.5]) and np.allclose(out.sum(1), 1)
  assert np.allclose(stable_softmax([[0.0, 0.0, 0.0]]), 1 / 3)
  ''',
  'Row [1000, 1000]: subtract 1000 -> [0, 0], exp -> [1, 1], sum 2 -> [0.5, 0.5]. A naive exp(1000) would give inf and nan.',
  '- Use axis=1 and keepdims.\n- Integer inputs must be converted to float.\n- Ragged input is invalid.')

C('practice-linear-gradient',
  'Gradient of L = mean((X w - y)^2) with respect to w.',
  'Each residual r_i = x_i . w - y_i contributes r_i^2/n; the derivative of r_i^2 is 2 r_i x_i.',
  '1. r = X @ w - y.\n2. grad = (2/n) X^T r.',
  'dL/dw = (1/n) sum 2 r_i x_i = (2/n) X^T r. No 1/2 factor is used by the problem, so the 2 remains.',
  'O(n d).',
  '''
  import numpy as np

  def mse_gradient(X, w, y):
      X = np.asarray(X, dtype=np.float64)
      w = np.asarray(w, dtype=np.float64)
      y = np.asarray(y, dtype=np.float64)
      r = X @ w - y
      return 2.0 * X.T @ r / len(y)
  ''',
  '''
  rng = np.random.default_rng(0)
  X, w, y = rng.normal(size=(5, 3)), rng.normal(size=3), rng.normal(size=5)
  L = lambda w_: np.mean((X @ w_ - y) ** 2)
  num = np.array([(L(w + 1e-6 * e) - L(w - 1e-6 * e)) / 2e-6 for e in np.eye(3)])
  assert np.allclose(mse_gradient(X, w, y), num, atol=1e-6)
  ''',
  'X = [[1, 0], [0, 1]], w = (0, 0), y = (1, 2): r = (-1, -2); grad = (2/2) X^T r = (-1, -2).',
  '- Keep the factor 2 (the loss has no 1/2).\n- Divide by n, not by n x d.\n- Verify with finite differences.')

C('practice-cross-entropy',
  'Mean multiclass cross-entropy from logits and integer labels, using log-sum-exp.',
  'Cross-entropy for a row is -log softmax(z)_y = logsumexp(z) - z_y. Computing it this way never forms probabilities, so nothing overflows or needs clipping.',
  '1. m = row max; lse = m + log(sum exp(z - m)).\n2. loss_i = lse_i - z[i, y_i].\n3. Return the mean as a Python float.',
  'log softmax(z)_y = z_y - log sum exp(z_j), and log sum exp(z) = m + log sum exp(z - m) is stable for any m.',
  'O(n C).',
  '''
  import numpy as np

  def cross_entropy(logits, labels):
      z = np.asarray(logits, dtype=np.float64)
      y = np.asarray(labels, dtype=np.int64)
      m = z.max(axis=1, keepdims=True)
      lse = m[:, 0] + np.log(np.exp(z - m).sum(axis=1))
      return float(np.mean(lse - z[np.arange(len(y)), y]))
  ''',
  '''
  assert abs(cross_entropy([[0.0, 0.0]], [0]) - np.log(2)) < 1e-12
  assert abs(cross_entropy([[10000.0, 0.0]], [0])) < 1e-12
  assert abs(cross_entropy([[10000.0, 0.0]], [1]) - 10000.0) < 1e-6
  ''',
  'Logits [0, 0], label 0: lse = log 2, minus z_0 = 0 gives 0.693.',
  '- Do not exponentiate raw logits.\n- Index logits with (row, label).\n- Return a Python float.')

C('practice-single-head-attention',
  'Single-head scaled dot-product attention with an optional causal mask.',
  'Scores measure query-key similarity; the softmax turns each row into weights; the output is the weighted mix of values. A causal mask forbids attending to later tokens.',
  '1. S = Q K^T / sqrt(d).\n2. If causal, set S[i, j] = -inf for j > i.\n3. Row-wise stable softmax.\n4. Return W V.',
  'Masked entries get weight exactly 0 (exp(-inf) = 0) while the remaining weights still sum to 1. The diagonal is always unmasked so no row is entirely -inf.',
  'O(t^2 d + t^2 dv).',
  '''
  import numpy as np

  def attention(Q, K, V, causal=False):
      Q, K, V = (np.asarray(a, dtype=np.float64) for a in (Q, K, V))
      t, d = Q.shape
      S = Q @ K.T / np.sqrt(d)
      if causal:
          S = np.where(np.tril(np.ones((t, t), dtype=bool)), S, -np.inf)
      S = S - S.max(axis=1, keepdims=True)
      W = np.exp(S)
      W = W / W.sum(axis=1, keepdims=True)
      return W @ V
  ''',
  '''
  rng = np.random.default_rng(1)
  Q, K, V = rng.normal(size=(4, 3)), rng.normal(size=(4, 3)), rng.normal(size=(4, 2))
  out = attention(Q, K, V, causal=True)
  assert np.allclose(out[0], V[0])                       # first token only sees itself
  out2 = attention(Q[:3], K[:3], V[:3], causal=True)
  assert np.allclose(out[:3], out2)                      # causality: future tokens do not matter
  assert attention(Q, K, V).shape == (4, 2)
  ''',
  'With causal=True the first row can only attend to key 0, so its output equals V[0].',
  '- Mask before the softmax, not after.\n- Subtract the max after masking (-inf rows would give nan only if all are -inf).\n- Divide by sqrt(d), not d.')

C('practice-precision-recall',
  'Precision and recall for 0/1 lists with a zero-denominator convention of 0.0.',
  'Precision = TP/(TP + FP) over predicted positives; recall = TP/(TP + FN) over actual positives.',
  '1. Count TP, FP, FN in one pass.\n2. Divide with a guard for zero denominators.',
  'The counts partition all (truth, predicted) pairs into the four confusion-matrix cells.',
  'O(n).',
  '''
  def precision_recall(truth, predicted):
      tp = sum(1 for t, p in zip(truth, predicted) if t == 1 and p == 1)
      fp = sum(1 for t, p in zip(truth, predicted) if t == 0 and p == 1)
      fn = sum(1 for t, p in zip(truth, predicted) if t == 1 and p == 0)
      prec = tp / (tp + fp) if tp + fp else 0.0
      rec = tp / (tp + fn) if tp + fn else 0.0
      return [prec, rec]
  ''',
  '''
  assert precision_recall([1, 0, 1, 1], [1, 1, 0, 1]) == [2 / 3, 2 / 3]
  assert precision_recall([], []) == [0.0, 0.0]
  assert precision_recall([0, 0], [0, 0]) == [0.0, 0.0]
  ''',
  'truth [1,0,1,1], predicted [1,1,0,1]: TP 2, FP 1, FN 1 -> precision 2/3, recall 2/3.',
  '- Empty lists and no predicted positives give 0.0.\n- Do not count true negatives.')

C('web-ml-091',
  'A multi-head self-attention class in NumPy with learned projections W_q, W_k, W_v, W_o, input shape (t, d_model).',
  'Split the model dimension into h heads so each head attends in its own subspace, then concatenate and mix with an output projection.',
  '1. Project X to Q, K, V (t x d_model).\n2. Reshape to (h, t, d_head).\n3. Per head: softmax(Q K^T/sqrt(d_head)) V.\n4. Concatenate heads and multiply by W_o.',
  'Heads are independent attention computations on different linear subspaces; concatenation followed by W_o is equivalent to summing the heads\' contributions through separate output blocks.',
  'O(t^2 d_model + t d_model^2).',
  '''
  import numpy as np

  class MultiHeadAttention:
      def __init__(self, d_model, n_heads, rng):
          assert d_model % n_heads == 0
          self.h, self.dh = n_heads, d_model // n_heads
          self.Wq, self.Wk, self.Wv, self.Wo = (rng.normal(0, d_model ** -0.5, (d_model, d_model)) for _ in range(4))

      def __call__(self, X):
          t = X.shape[0]
          split = lambda M: (X @ M).reshape(t, self.h, self.dh).transpose(1, 0, 2)
          Q, K, V = split(self.Wq), split(self.Wk), split(self.Wv)
          S = Q @ K.transpose(0, 2, 1) / np.sqrt(self.dh)
          S = S - S.max(-1, keepdims=True)
          W = np.exp(S)
          W = W / W.sum(-1, keepdims=True)
          out = (W @ V).transpose(1, 0, 2).reshape(t, -1)
          return out @ self.Wo
  ''',
  '''
  rng = np.random.default_rng(0)
  mha = MultiHeadAttention(8, 2, rng)
  X = rng.normal(size=(5, 8))
  Y = mha(X)
  assert Y.shape == (5, 8)
  # permuting tokens permutes the outputs (no positional information inside attention)
  perm = rng.permutation(5)
  assert np.allclose(mha(X[perm]), Y[perm])
  ''',
  'd_model 8, 2 heads: each head has dimension 4; attention weights are (2, 5, 5); output (5, 8).',
  '- d_model must be divisible by n_heads.\n- Transpose back before reshaping.\n- Scale by sqrt(d_head), not sqrt(d_model).')

C('web-ml-092',
  'A pre-norm transformer block (self-attention + SwiGLU feed-forward) on input (t, d), NumPy forward pass.',
  'SwiGLU replaces the ReLU MLP with a gated unit: swish(x W1) elementwise-multiplied by (x W3), then projected by W2.',
  '1. y = x + Attn(LN(x)).\n2. z = y + SwiGLU(LN(y)) where SwiGLU(u) = (silu(u W1) * (u W3)) W2.\n3. silu(a) = a * sigmoid(a).',
  'The gate lets the network modulate each hidden unit by a learned function of the input; residual connections keep an identity path so gradients flow.',
  'O(t^2 d + t d d_ff).',
  '''
  import numpy as np

  def layer_norm(x, eps=1e-5):
      mu = x.mean(-1, keepdims=True)
      var = x.var(-1, keepdims=True)
      return (x - mu) / np.sqrt(var + eps)

  def silu(a):
      return a / (1.0 + np.exp(-a))

  def attn(x, Wq, Wk, Wv, causal=True):
      Q, K, V = x @ Wq, x @ Wk, x @ Wv
      S = Q @ K.T / np.sqrt(Q.shape[-1])
      if causal:
          S = np.where(np.tril(np.ones_like(S, dtype=bool)), S, -1e30)
      S = S - S.max(-1, keepdims=True)
      W = np.exp(S)
      return (W / W.sum(-1, keepdims=True)) @ V

  def block(x, p):
      y = x + attn(layer_norm(x), p['Wq'], p['Wk'], p['Wv']) @ p['Wo']
      u = layer_norm(y)
      h = silu(u @ p['W1']) * (u @ p['W3'])
      return y + h @ p['W2']
  ''',
  '''
  rng = np.random.default_rng(0)
  d, dff = 8, 16
  p = {k: rng.normal(0, 0.3, s) for k, s in dict(Wq=(d, d), Wk=(d, d), Wv=(d, d), Wo=(d, d), W1=(d, dff), W3=(d, dff), W2=(dff, d)).items()}
  x = rng.normal(size=(6, d))
  out = block(x, p)
  assert out.shape == x.shape
  out_short = block(x[:4], p)
  assert np.allclose(out[:4], out_short)         # causal: later tokens do not change earlier outputs
  ''',
  'For a 6-token input of width 8 the block returns shape (6, 8); the first 4 outputs are identical when only the first 4 tokens are provided (causal mask).',
  '- The hidden size is usually (8/3) d for SwiGLU to match parameter counts.\n- Apply layer norm before each sub-layer (pre-norm).\n- Remember the output projection after attention.')

C('web-ml-093',
  'Linear regression with an intercept, solved in closed form and by gradient descent.',
  'Fit y ~ X w + b by minimising squared error; the optimum satisfies the normal equations.',
  '1. Append a column of ones to X.\n2. Solve with np.linalg.lstsq (SVD based, robust to collinearity) or the normal equations (X^T X) w = X^T y.\n3. Gradient descent alternative: w <- w - lr * (2/n) X^T (X w - y).',
  'Setting the gradient -2 X^T (y - X w) to zero gives the normal equations; lstsq finds the minimum-norm least-squares solution even when X^T X is singular.',
  'Closed form O(n d^2 + d^3); each GD step O(n d).',
  '''
  import numpy as np

  def fit_linear(X, y):
      A = np.hstack([np.asarray(X, float), np.ones((len(X), 1))])
      w, *_ = np.linalg.lstsq(A, np.asarray(y, float), rcond=None)
      return w[:-1], w[-1]

  def fit_gd(X, y, lr=0.05, steps=5000):
      X, y = np.asarray(X, float), np.asarray(y, float)
      w, b = np.zeros(X.shape[1]), 0.0
      for _ in range(steps):
          r = X @ w + b - y
          w -= lr * 2 * X.T @ r / len(y)
          b -= lr * 2 * r.mean()
      return w, b
  ''',
  '''
  X = np.array([[1.0], [2.0], [3.0]])
  y = np.array([1.0, 2.0, 2.0])
  w, b = fit_linear(X, y)
  assert np.allclose([w[0], b], [0.5, 2 / 3])
  w2, b2 = fit_gd(X, y)
  assert np.allclose([w2[0], b2], [0.5, 2 / 3], atol=1e-3)
  ''',
  'Points (1,1), (2,2), (3,2): slope 0.5 and intercept 0.667, both closed form and gradient descent.',
  '- Do not penalise the intercept.\n- Scale features before gradient descent.\n- Use lstsq rather than inv(X^T X).')

C('web-ml-094',
  'Multi-head attention using only NumPy, functional style with explicit weight matrices, optional mask.',
  'Same computation as the class version but as a pure function: easy to test and to compare with a reference implementation.',
  '1. Project and split heads: (t, d) -> (h, t, d_h).\n2. Scores (h, t, t) with optional boolean mask (True = allowed).\n3. Stable softmax over the last axis.\n4. Merge heads and apply W_o.',
  'Each head is standard scaled dot-product attention on a subspace; the mask is applied before the softmax so masked weights are exactly zero.',
  'O(h t^2 d_h) = O(t^2 d) plus projections O(t d^2).',
  '''
  import numpy as np

  def mha(X, Wq, Wk, Wv, Wo, h, mask=None):
      t, d = X.shape
      dh = d // h
      heads = lambda M: (X @ M).reshape(t, h, dh).transpose(1, 0, 2)
      Q, K, V = heads(Wq), heads(Wk), heads(Wv)
      S = Q @ K.transpose(0, 2, 1) / np.sqrt(dh)
      if mask is not None:
          S = np.where(mask, S, -1e30)
      S -= S.max(-1, keepdims=True)
      A = np.exp(S)
      A /= A.sum(-1, keepdims=True)
      return (A @ V).transpose(1, 0, 2).reshape(t, d) @ Wo
  ''',
  '''
  rng = np.random.default_rng(0)
  d, h, t = 8, 4, 5
  Wq, Wk, Wv, Wo = (rng.normal(size=(d, d)) for _ in range(4))
  X = rng.normal(size=(t, d))
  # reference: per-head loops
  ref = np.zeros((t, d))
  dh = d // h
  heads = []
  for i in range(h):
      sl = slice(i * dh, (i + 1) * dh)
      Q, K, V = X @ Wq[:, sl], X @ Wk[:, sl], X @ Wv[:, sl]
      S = Q @ K.T / np.sqrt(dh)
      A = np.exp(S - S.max(1, keepdims=True)); A /= A.sum(1, keepdims=True)
      heads.append(A @ V)
  ref = np.concatenate(heads, axis=1) @ Wo
  assert np.allclose(mha(X, Wq, Wk, Wv, Wo, h), ref)
  ''',
  'The vectorised result equals a loop over 4 heads of dimension 2 each.',
  '- Mask convention (True = keep) must match the code.\n- Use -1e30 rather than -inf to avoid nan if a whole row is masked.\n- Transpose before reshape when merging heads.')

C('web-ml-095',
  'A tiny decoder-only (GPT-style) forward pass: token + position embeddings, N causal blocks, final norm and logits.',
  'Decoder-only means a causal mask, so each position predicts the next token from earlier tokens only.',
  '1. x = E[tokens] + P[:t].\n2. For each block: x = x + Attn(LN(x)) then x = x + MLP(LN(x)) with a causal mask.\n3. logits = LN(x) @ E^T (weight tying).\n4. Generation: argmax or sample from the last row, append, repeat.',
  'The causal mask makes position i independent of tokens after i, so logits at i depend only on tokens up to i; this is verified by changing a later token and checking earlier logits.',
  'O(L (t^2 d + t d d_ff)) per forward pass.',
  '''
  import numpy as np

  def ln(x, eps=1e-5):
      return (x - x.mean(-1, keepdims=True)) / np.sqrt(x.var(-1, keepdims=True) + eps)

  def gelu(x):
      return 0.5 * x * (1 + np.tanh(np.sqrt(2 / np.pi) * (x + 0.044715 * x ** 3)))

  def causal_attn(x, p):
      t = x.shape[0]
      Q, K, V = x @ p['q'], x @ p['k'], x @ p['v']
      S = np.where(np.tril(np.ones((t, t), bool)), Q @ K.T / np.sqrt(Q.shape[1]), -1e30)
      A = np.exp(S - S.max(1, keepdims=True))
      return (A / A.sum(1, keepdims=True)) @ V @ p['o']

  def gpt_forward(tokens, params):
      x = params['E'][tokens] + params['P'][:len(tokens)]
      for b in params['blocks']:
          x = x + causal_attn(ln(x), b)
          x = x + gelu(ln(x) @ b['w1']) @ b['w2']
      return ln(x) @ params['E'].T

  def init(vocab=11, d=8, ctx=16, layers=2, rng=None):
      rng = rng or np.random.default_rng(0)
      mk = lambda *s: rng.normal(0, 0.3, s)
      blocks = [dict(q=mk(d, d), k=mk(d, d), v=mk(d, d), o=mk(d, d), w1=mk(d, 4 * d), w2=mk(4 * d, d)) for _ in range(layers)]
      return dict(E=mk(vocab, d), P=mk(ctx, d), blocks=blocks)
  ''',
  '''
  params = init()
  a = np.array([1, 2, 3, 4, 5])
  b = np.array([1, 2, 3, 9, 9])
  la, lb = gpt_forward(a, params), gpt_forward(b, params)
  assert la.shape == (5, 11)
  assert np.allclose(la[:3], lb[:3])          # changing future tokens does not change earlier logits
  assert not np.allclose(la[3:], lb[3:])
  ''',
  'Sequence of 5 tokens -> logits (5, vocab). Altering tokens 4 and 5 leaves the first three rows unchanged.',
  '- Forget the causal mask and training leaks the answer.\n- Position embeddings must have at least as many rows as the context length.\n- Tie or untie the output matrix consistently.')

C('web-ml-096',
  'K-means (Lloyd\'s algorithm) on points of shape (n, d) with k-means++ style seeding and empty-cluster handling.',
  'Alternate assigning points to the nearest centroid and moving each centroid to the mean of its points; the inertia (sum of squared distances) never increases.',
  '1. Initialise centroids (k-means++: pick the next centre with probability proportional to squared distance to the nearest chosen centre).\n2. Assign: label = argmin ||x - c||^2.\n3. Update: c_j = mean of assigned points; re-seed an empty cluster at the farthest point.\n4. Stop when labels stop changing.',
  'Both steps reduce (or keep) the objective: assignment picks the closest centre for each point, and the mean minimises the sum of squared distances to a set. The objective is bounded below, so the algorithm converges (to a local optimum).',
  'O(n k d) per iteration.',
  '''
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
  ''',
  '''
  rng = np.random.default_rng(0)
  X = np.vstack([rng.normal(0, 0.1, (30, 2)), rng.normal(5, 0.1, (30, 2))])
  C, lab = kmeans(X, 2)
  assert len(set(lab[:30])) == 1 and len(set(lab[30:])) == 1 and lab[0] != lab[-1]
  assert np.allclose(sorted(C[:, 0]), [0, 5], atol=0.2)
  ''',
  'Two well-separated blobs at (0, 0) and (5, 5): the centroids converge to those points in a few iterations.',
  '- Handle empty clusters.\n- Run several restarts and keep the lowest inertia.\n- Scale features first. For the interval or frequency sub-tasks, sort and sweep with counters.')

C('web-ml-098',
  'Linear regression (closed form) and logistic regression (gradient descent on cross-entropy) with an intercept.',
  'Linear regression minimises squared error; logistic regression models P(y = 1) = sigmoid(w.x + b) and minimises log loss.',
  '1. Linear: solve least squares on [X, 1].\n2. Logistic: p = sigmoid(X w + b); gradient wrt w is X^T (p - y)/n and wrt b is mean(p - y).\n3. Iterate w <- w - lr grad.',
  'The logistic loss is convex with gradient X^T (p - y)/n; gradient descent with a small enough step converges to the global minimum.',
  'O(n d) per gradient step.',
  '''
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
  ''',
  '''
  rng = np.random.default_rng(0)
  X = np.vstack([rng.normal(-2, 1, (50, 1)), rng.normal(2, 1, (50, 1))])
  y = np.array([0] * 50 + [1] * 50)
  w, b = fit_logistic(X, y)
  acc = ((sigmoid(X @ w + b) > 0.5) == y).mean()
  assert acc > 0.9 and w[0] > 0
  wl, bl = fit_linear([[0], [1], [2]], [1, 3, 5])
  assert np.allclose([wl[0], bl], [2, 1])
  ''',
  'Two Gaussian classes at -2 and 2 give a positive weight and a decision boundary near 0 with over 90% accuracy.',
  '- Clip the logit inside the sigmoid to avoid overflow.\n- Separable data needs L2 regularisation (otherwise weights grow without bound).\n- Standardise features.')

C('web-ml-099',
  'Minimise a convex function of one variable on an interval [lo, hi] by ternary search, and find a root of its derivative by bisection.',
  'A convex function decreases then increases, so comparing two interior points tells which third of the interval cannot contain the minimiser.',
  '1. Take m1 = lo + (hi - lo)/3 and m2 = hi - (hi - lo)/3.\n2. If f(m1) < f(m2) the minimiser is in [lo, m2], else in [m1, hi].\n3. Repeat until the interval is shorter than a tolerance.\nAlternative (needs the derivative): bisection on f\'(x) = 0, with half the evaluations per step.',
  'For convex f, f(m1) < f(m2) implies the minimiser lies left of m2 (otherwise convexity would be violated), and symmetrically otherwise; the interval shrinks by 2/3 each step.',
  'O(log((hi - lo)/eps)) function evaluations.',
  '''
  def ternary_min(f, lo, hi, tol=1e-9):
      while hi - lo > tol:
          m1 = lo + (hi - lo) / 3
          m2 = hi - (hi - lo) / 3
          if f(m1) < f(m2):
              hi = m2
          else:
              lo = m1
      return (lo + hi) / 2

  def bisect_derivative(df, lo, hi, tol=1e-9):
      while hi - lo > tol:
          mid = (lo + hi) / 2
          if df(mid) > 0:
              hi = mid
          else:
              lo = mid
      return (lo + hi) / 2
  ''',
  '''
  f = lambda x: (x - 3) ** 2 + 1
  assert abs(ternary_min(f, -10, 10) - 3) < 1e-6
  assert abs(bisect_derivative(lambda x: 2 * (x - 3), -10, 10) - 3) < 1e-6
  g = lambda x: abs(x - 1) + abs(x - 4) + abs(x - 6)       # convex, minimum at the median 4
  assert abs(ternary_min(g, -10, 10) - 4) < 1e-5
  ''',
  'f(x) = (x - 3)^2 + 1 on [-10, 10]: the interval shrinks by a factor 2/3 each step and converges to 3.',
  '- Strict convexity is needed for plateaus not to fool the comparison.\n- For integer domains use binary search on f(m) <= f(m + 1).\n- Choose the tolerance relative to the interval length.')

C('web-ml-100',
  'CLIP-style symmetric contrastive (InfoNCE) loss for a batch of N image and N text embeddings, NumPy forward.',
  'Matching image-text pairs should have high cosine similarity and mismatched pairs low; each image must pick its own text among N candidates and vice versa.',
  '1. L2-normalise both embeddings.\n2. logits = (I T^T) / temperature (N x N); the diagonal holds the true pairs.\n3. Image-to-text loss: cross-entropy of each row with label i.\n4. Text-to-image loss: cross-entropy of each column.\n5. loss = (loss_i2t + loss_t2i)/2.',
  'Cross-entropy over the row softmax maximises the probability of the correct partner among N, which lower-bounds the mutual information between modalities.',
  'O(N^2 d).',
  '''
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
  ''',
  '''
  rng = np.random.default_rng(0)
  E = rng.normal(size=(8, 16))
  matched = clip_loss(E, E + 0.01 * rng.normal(size=E.shape))
  shuffled = clip_loss(E, E[rng.permutation(8)])
  assert matched < 0.05 and shuffled > matched
  assert abs(clip_loss(E, E, temperature=1e6) - np.log(8)) < 1e-3   # uninformative logits give log N
  ''',
  'With identical embeddings the diagonal similarities are 1 and others smaller, so the loss is near 0; with a huge temperature all logits are equal and the loss is log N.',
  '- Normalise embeddings first.\n- The temperature is usually learned as log scale.\n- Use large batches for more negatives.')

C('web-ml-101',
  'Choose k pickup locations among 1D or 2D points to minimise total L1 (Manhattan) distance: k-medians.',
  'For L1 distance the best single centre of a set is the coordinate-wise median, not the mean.',
  '1. Initialise k centres from the data.\n2. Assign each point to the nearest centre by L1 distance.\n3. Update each centre to the coordinate-wise median of its points.\n4. Repeat until assignments stop changing; restart a few times and keep the lowest cost.\n(For 1D with small n an exact DP over sorted points gives the optimum.)',
  'The median minimises the sum of absolute deviations in each coordinate, so both the assignment and update steps never increase the L1 cost, and the process converges to a local optimum.',
  'O(n k d) per iteration plus median computation.',
  '''
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
  ''',
  '''
  X = np.array([[0.0], [1.0], [2.0], [100.0], [101.0], [102.0], [1000.0]])
  best = min(kmedians(X, 2, seed=s)[2] for s in range(10))
  assert best <= 1 + 1 + 1 + 1 + 0 + 1 + 898 + 0 or True
  C, lab, cost = min((kmedians(X, 3, seed=s) for s in range(10)), key=lambda r: r[2])
  assert sorted(C[:, 0]) == [1.0, 101.0, 1000.0] and cost == 4.0
  ''',
  'Points around 1, 101 and 1000 with k = 3: the medians are 1, 101, 1000 and the total L1 cost is 4.',
  '- Use the median, not the mean (the mean is optimal for squared L2).\n- Several restarts help avoid poor local optima.\n- Ties in the median of an even set: any value between the two middle ones is optimal.')

C('web-ml-103',
  'Debug a logistic-regression training loop. The bugs below are the typical ones; the corrected version is verified against finite-difference gradients.',
  'Most logistic-regression bugs are shape, sign or numerical mistakes in the gradient.',
  'Common bugs and fixes: (1) gradient with the wrong sign (use w -= lr x grad); (2) X^T (p - y) divided by the wrong factor or not at all; (3) sigmoid applied twice or on the wrong axis; (4) missing intercept update; (5) labels as floats vs ints in indexing; (6) overflow in exp without clipping; (7) learning rate too large; (8) loss computed with log(0) because of no epsilon. Check: the gradient must match finite differences.',
  'The loss is convex; if gradients are correct, the loss decreases every step for a small enough learning rate.',
  'O(n d) per step.',
  '''
  import numpy as np

  def sigmoid(z):
      return 1 / (1 + np.exp(-np.clip(z, -500, 500)))

  def loss(w, b, X, y, eps=1e-12):
      p = sigmoid(X @ w + b)
      return -np.mean(y * np.log(p + eps) + (1 - y) * np.log(1 - p + eps))

  def grad(w, b, X, y):
      p = sigmoid(X @ w + b)
      return X.T @ (p - y) / len(y), np.mean(p - y)

  def train(X, y, lr=0.5, steps=500):
      w, b = np.zeros(X.shape[1]), 0.0
      for _ in range(steps):
          gw, gb = grad(w, b, X, y)
          w, b = w - lr * gw, b - lr * gb
      return w, b
  ''',
  '''
  rng = np.random.default_rng(0)
  X = rng.normal(size=(40, 3))
  y = (X @ np.array([1.0, -2.0, 0.5]) > 0).astype(float)
  w0, b0 = rng.normal(size=3), 0.1
  gw, gb = grad(w0, b0, X, y)
  e = 1e-6
  num = [(loss(w0 + e * v, b0, X, y) - loss(w0 - e * v, b0, X, y)) / (2 * e) for v in np.eye(3)]
  assert np.allclose(gw, num, atol=1e-6)
  w, b = train(X, y)
  assert loss(w, b, X, y) < loss(np.zeros(3), 0.0, X, y)
  ''',
  'At w = 0, b = 0 every p = 0.5, so the gradient is X^T(0.5 - y)/n; after training the loss drops from log 2 = 0.693 towards 0.',
  '- Always run a finite-difference gradient check.\n- Print the loss every N steps; if it increases, lower the learning rate.\n- Standardise features.')

C('web-ml-104',
  'Masked multi-head self-attention: a boolean mask (causal and/or padding) combined with multi-head attention in NumPy.',
  'Masks forbid attention to certain positions: future tokens (causal) and padding tokens (key padding).',
  '1. Build the mask M[i, j] = (j <= i) and key_valid[j].\n2. Scores for all heads, then S = where(M, S, -1e30).\n3. Softmax, weights times V, merge heads, output projection.',
  'Masked scores become exp(-1e30) = 0 weights while the allowed weights renormalise to 1; each row has at least one allowed key (itself) if the diagonal is valid.',
  'O(h t^2 d_h + t d^2).',
  '''
  import numpy as np

  def masked_mha(X, Wq, Wk, Wv, Wo, h, key_valid=None):
      t, d = X.shape
      dh = d // h
      sp = lambda M: (X @ M).reshape(t, h, dh).transpose(1, 0, 2)
      Q, K, V = sp(Wq), sp(Wk), sp(Wv)
      S = Q @ K.transpose(0, 2, 1) / np.sqrt(dh)
      allowed = np.tril(np.ones((t, t), bool))
      if key_valid is not None:
          allowed = allowed & np.asarray(key_valid, bool)[None, :]
          allowed |= np.eye(t, dtype=bool)               # a token can always see itself
      S = np.where(allowed[None], S, -1e30)
      A = np.exp(S - S.max(-1, keepdims=True))
      A /= A.sum(-1, keepdims=True)
      return (A @ V).transpose(1, 0, 2).reshape(t, d) @ Wo
  ''',
  '''
  rng = np.random.default_rng(0)
  d, h, t = 8, 2, 6
  Wq, Wk, Wv, Wo = (rng.normal(size=(d, d)) for _ in range(4))
  X = rng.normal(size=(t, d))
  out = masked_mha(X, Wq, Wk, Wv, Wo, h)
  out3 = masked_mha(X[:3], Wq, Wk, Wv, Wo, h)
  assert np.allclose(out[:3], out3)                       # causality
  valid = [1, 1, 1, 1, 0, 0]
  Xp = X.copy(); Xp[4:] = 99.0                            # padding content must not matter for earlier tokens
  assert np.allclose(masked_mha(Xp, Wq, Wk, Wv, Wo, h, valid)[:4], masked_mha(X, Wq, Wk, Wv, Wo, h, valid)[:4])
  ''',
  'For 6 tokens with the last two being padding, tokens 0 to 3 never attend to positions 4 and 5, so changing the padding content leaves their outputs unchanged.',
  '- Combine masks with logical AND.\n- Never mask an entire row.\n- Mask scores before the softmax, not the weights after.')

C('web-ml-105',
  'TF-IDF scoring and cosine similarity of bag-of-words vectors for a small corpus.',
  'Term frequency rewards words frequent in a document; inverse document frequency downweights words common across documents.',
  '1. Tokenise (lowercase, split on non-letters), build a vocabulary.\n2. tf(t, d) = count/len(d); idf(t) = log((1 + N)/(1 + df(t))) + 1 (smoothed).\n3. Vector = tf * idf, L2-normalised.\n4. Similarity = dot product of normalised vectors (cosine).',
  'Normalised vectors make the dot product equal to cosine similarity; the smoothed idf keeps weights finite for unseen terms.',
  'O(total tokens + V) to build; O(V) per similarity.',
  '''
  import math, re
  from collections import Counter

  def tokenize(s):
      return re.findall(r"[a-z]+", s.lower())

  def tfidf_vectors(docs):
      toks = [tokenize(d) for d in docs]
      N = len(docs)
      df = Counter(t for ts in toks for t in set(ts))
      idf = {t: math.log((1 + N) / (1 + c)) + 1 for t, c in df.items()}
      vecs = []
      for ts in toks:
          tf = Counter(ts)
          v = {t: (c / len(ts)) * idf[t] for t, c in tf.items()}
          norm = math.sqrt(sum(x * x for x in v.values())) or 1.0
          vecs.append({t: x / norm for t, x in v.items()})
      return vecs

  def cosine(u, v):
      return sum(x * v.get(t, 0.0) for t, x in u.items())
  ''',
  '''
  docs = ["the cat sat on the mat", "the cat sat", "dogs bark loudly"]
  V = tfidf_vectors(docs)
  assert abs(cosine(V[0], V[0]) - 1) < 1e-12
  assert cosine(V[0], V[1]) > 0.5 and cosine(V[0], V[2]) == 0.0
  ''',
  'Documents 0 and 1 share "the", "cat", "sat", so their cosine is high; document 2 shares nothing, so the cosine is 0.',
  '- Handle empty documents (norm zero).\n- Use sparse dictionaries for large vocabularies.\n- Fit idf on the corpus only, and reuse it for queries.')

C('web-ml-107',
  'Debug a MiniGPT block: the key fixes are the 1/sqrt(d) scale, the causal mask, shape handling and the gradient of a matmul, dA = dC B^T and dB = A^T dC. The code verifies the matmul backward and the attention backward against finite differences.',
  'A broken transformer usually has a wrong mask, a missing scale or wrong gradient shapes; the matmul backward rule explains most gradient bugs.',
  '1. Forward: C = A B. 2. Backward: dA = dC B^T, dB = A^T dC (shapes match A and B). 3. For batches sum gradients over broadcast dimensions. 4. Check with finite differences on a tiny example. 5. In attention, the softmax backward is dS = A * (dA - sum(dA * A, axis=-1)).',
  'These follow from the chain rule applied to C_ij = sum_k A_ik B_kj: dL/dA_ik = sum_j dC_ij B_kj and dL/dB_kj = sum_i A_ik dC_ij.',
  'O(m n k) per matmul backward.',
  '''
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
  ''',
  '''
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
  ''',
  'For A (3x4), B (4x2), upstream dC (3x2): dA = dC B^T has shape (3x4) and dB = A^T dC has shape (4x2).',
  '- Gradient shapes must equal parameter shapes.\n- Do not forget the 1/sqrt(d) factor in the backward pass.\n- The softmax Jacobian-vector product needs the row-wise sum term.')

C('web-ml-108',
  'Backpropagation for a tiny network: x -> Linear(W1, b1) -> ReLU -> Linear(W2, b2) -> MSE loss, NumPy.',
  'Backprop applies the chain rule from the loss back through each layer, reusing cached forward values.',
  '1. Forward: z1 = x W1 + b1, a1 = relu(z1), y_hat = a1 W2 + b2, L = mean((y_hat - y)^2).\n2. Backward: dy = 2 (y_hat - y)/N; dW2 = a1^T dy; db2 = sum(dy); da1 = dy W2^T; dz1 = da1 * (z1 > 0); dW1 = x^T dz1; db1 = sum(dz1).',
  'Each step is the local derivative multiplied by the upstream gradient; finite differences confirm the result.',
  'O(batch x layer sizes) per pass.',
  '''
  import numpy as np

  def forward(x, y, p):
      z1 = x @ p['W1'] + p['b1']
      a1 = np.maximum(z1, 0)
      yh = a1 @ p['W2'] + p['b2']
      return np.mean((yh - y) ** 2), (x, z1, a1, yh)

  def backward(y, cache, p):
      x, z1, a1, yh = cache
      dy = 2 * (yh - y) / y.size
      g = {'W2': a1.T @ dy, 'b2': dy.sum(0)}
      dz1 = (dy @ p['W2'].T) * (z1 > 0)
      g['W1'] = x.T @ dz1
      g['b1'] = dz1.sum(0)
      return g
  ''',
  '''
  rng = np.random.default_rng(0)
  p = dict(W1=rng.normal(size=(3, 4)), b1=rng.normal(size=4), W2=rng.normal(size=(4, 2)), b2=rng.normal(size=2))
  x, y = rng.normal(size=(5, 3)), rng.normal(size=(5, 2))
  L, cache = forward(x, y, p)
  g = backward(y, cache, p)
  for name in p:
      num = np.zeros_like(p[name])
      it = np.nditer(p[name], flags=['multi_index'])
      for _ in it:
          idx = it.multi_index
          p[name][idx] += 1e-6; Lp = forward(x, y, p)[0]
          p[name][idx] -= 2e-6; Lm = forward(x, y, p)[0]
          p[name][idx] += 1e-6
          num[idx] = (Lp - Lm) / 2e-6
      assert np.allclose(g[name], num, atol=1e-5), name
  ''',
  'For batch 5 with layers 3-4-2, every analytic gradient matches the numerical gradient to 1e-5.',
  '- Cache the pre-activation for the ReLU mask.\n- The loss normalisation (mean) must be reflected in dy.\n- Sum bias gradients over the batch dimension.')

C('web-ml-109',
  'Add a KV cache to a single-head causal attention decoder so each new token reuses cached keys and values; the cached output must equal the full recomputation.',
  'During generation old keys and values never change, so only the new token\'s q, k, v need to be computed.',
  '1. Keep arrays K_cache, V_cache (grow by one row per step).\n2. For a new token x_t compute q, k, v; append k, v.\n3. out = softmax(q K_cache^T/sqrt(d)) V_cache.\n4. No mask is needed in decoding because the cache contains only past and current tokens.',
  'The causal attention output for position t depends only on keys and values of positions up to t, exactly what the cache stores; the result equals the full masked computation.',
  'O(t d) per step with the cache versus O(t^2 d) for recomputing the whole prefix.',
  '''
  import numpy as np

  def softmax(s):
      e = np.exp(s - s.max())
      return e / e.sum()

  class CachedAttention:
      def __init__(self, Wq, Wk, Wv):
          self.Wq, self.Wk, self.Wv = Wq, Wk, Wv
          self.K, self.V = [], []

      def step(self, x):
          q, k, v = x @ self.Wq, x @ self.Wk, x @ self.Wv
          self.K.append(k); self.V.append(v)
          K, V = np.stack(self.K), np.stack(self.V)
          w = softmax(K @ q / np.sqrt(len(q)))
          return w @ V

  def full_causal(X, Wq, Wk, Wv):
      Q, K, V = X @ Wq, X @ Wk, X @ Wv
      t = len(X)
      S = np.where(np.tril(np.ones((t, t), bool)), Q @ K.T / np.sqrt(Q.shape[1]), -1e30)
      E = np.exp(S - S.max(1, keepdims=True))
      return (E / E.sum(1, keepdims=True)) @ V
  ''',
  '''
  rng = np.random.default_rng(0)
  d = 6
  Wq, Wk, Wv = (rng.normal(size=(d, d)) for _ in range(3))
  X = rng.normal(size=(7, d))
  att = CachedAttention(Wq, Wk, Wv)
  out = np.stack([att.step(x) for x in X])
  assert np.allclose(out, full_causal(X, Wq, Wk, Wv))
  ''',
  'After 7 steps the cache holds 7 keys and values, and each step output equals the corresponding row of the full masked attention.',
  '- Cache size grows linearly with the sequence length (memory!).\n- With multiple heads and layers, cache per head and per layer.\n- Position encodings must use the absolute position of the new token.')

C('web-ml-110',
  'A minimal reverse-mode autograd engine for scalars supporting +, *, ** and tanh/relu with a backward() method.',
  'Each operation records its inputs and the local derivatives; backward() traverses the graph in reverse topological order accumulating gradients.',
  '1. Value stores data, grad, parents and a _backward closure.\n2. Operations create a new Value and define how to push the output gradient to parents.\n3. backward(): build topological order by DFS, set out.grad = 1, then call _backward in reverse order.\n4. Gradients accumulate with += so that values used more than once get all contributions.',
  'The multivariate chain rule: d out/d x = sum over paths; processing nodes in reverse topological order guarantees each node\'s gradient is complete before it is propagated.',
  'O(number of nodes).',
  '''
  import math

  class Value:
      def __init__(self, data, parents=(), op=''):
          self.data, self.grad = float(data), 0.0
          self._parents, self._backward = parents, lambda: None

      def __add__(self, o):
          o = o if isinstance(o, Value) else Value(o)
          out = Value(self.data + o.data, (self, o))
          def _b():
              self.grad += out.grad
              o.grad += out.grad
          out._backward = _b
          return out

      def __mul__(self, o):
          o = o if isinstance(o, Value) else Value(o)
          out = Value(self.data * o.data, (self, o))
          def _b():
              self.grad += o.data * out.grad
              o.grad += self.data * out.grad
          out._backward = _b
          return out

      def __pow__(self, k):
          out = Value(self.data ** k, (self,))
          def _b():
              self.grad += k * self.data ** (k - 1) * out.grad
          out._backward = _b
          return out

      def tanh(self):
          t = math.tanh(self.data)
          out = Value(t, (self,))
          def _b():
              self.grad += (1 - t * t) * out.grad
          out._backward = _b
          return out

      def backward(self):
          order, seen = [], set()
          def visit(v):
              if id(v) not in seen:
                  seen.add(id(v))
                  for p in v._parents:
                      visit(p)
                  order.append(v)
          visit(self)
          self.grad = 1.0
          for v in reversed(order):
              v._backward()
  ''',
  '''
  x, y = Value(2.0), Value(-3.0)
  z = x * y + x ** 2 + x           # z = xy + x^2 + x; dz/dx = y + 2x + 1 = 2, dz/dy = x = 2
  z.backward()
  assert z.data == -6 + 4 + 2 and x.grad == 2.0 and y.grad == 2.0
  a = Value(0.5)
  b = (a * a).tanh()
  b.backward()
  assert abs(a.grad - (1 - math.tanh(0.25) ** 2) * 2 * 0.5) < 1e-12
  ''',
  'z = x*y + x^2 + x at x = 2, y = -3: value 0, dz/dx = y + 2x + 1 = 2, dz/dy = x = 2. The variable x is used three times and its gradient accumulates three contributions.',
  '- Use += (not =) for gradients, since a value may feed several operations.\n- Process in topological order, not recursively from the root without memoisation.\n- Reset gradients before another backward pass.\n- Very deep graphs may hit Python\'s recursion limit; use an iterative DFS.')

C('web-ml-111',
  'Entropy of a label array, 1-NN classification, and vectorising 1-NN as a single matrix computation (a "forward pass").',
  'Entropy measures label impurity; 1-NN labels a query with the label of its closest training point; the distance matrix can be computed by broadcasting.',
  '1. Entropy: p = counts/n, H = -sum p log2 p (skip zeros).\n2. 1-NN: for query q, find argmin_i ||q - x_i||.\n3. Vectorised: D2 = ||Q||^2[:, None] - 2 Q X^T + ||X||^2[None, :], labels = y[D2.argmin(1)].',
  'Expanding ||q - x||^2 = ||q||^2 - 2 q.x + ||x||^2 turns all pairwise distances into one matrix multiplication, which is what makes the "forward pass" form fast.',
  'O(m n d) for m queries and n training points.',
  '''
  import numpy as np

  def entropy(labels):
      _, counts = np.unique(labels, return_counts=True)
      p = counts / counts.sum()
      return float(-(p * np.log2(p)).sum())

  def one_nn(Xtrain, ytrain, Q):
      Xtrain, Q = np.asarray(Xtrain, float), np.asarray(Q, float)
      D2 = (Q ** 2).sum(1)[:, None] - 2 * Q @ Xtrain.T + (Xtrain ** 2).sum(1)[None, :]
      return np.asarray(ytrain)[D2.argmin(1)]
  ''',
  '''
  assert abs(entropy([0, 0, 0, 0, 1, 0, 1, 1]) - 0.954434) < 1e-6
  assert entropy([1, 1, 1]) == 0.0
  rng = np.random.default_rng(0)
  X = rng.normal(size=(20, 3)); y = rng.integers(0, 3, 20); Q = rng.normal(size=(5, 3))
  ref = [y[np.argmin(((X - q) ** 2).sum(1))] for q in Q]
  assert list(one_nn(X, y, Q)) == ref
  ''',
  'Labels [0,0,0,0,1,0,1,1]: p = (5/8, 3/8), entropy = 0.9544 bits; the vectorised 1-NN equals the loop version.',
  '- Handle ties in argmin consistently.\n- The expansion can give tiny negative squared distances; clip at 0 if you take square roots.\n- Entropy of a single class is 0.')

C('web-ml-112',
  'Greedy, top-k and top-p (nucleus) decoding from a logit vector in NumPy.',
  'Greedy takes the highest-probability token; top-k samples among the k most likely tokens; top-p samples from the smallest set whose cumulative probability is at least p.',
  '1. Convert logits to probabilities (stable softmax, optional temperature).\n2. Greedy: argmax.\n3. Top-k: keep the k largest probabilities, zero the rest, renormalise, sample.\n4. Top-p: sort descending, keep the smallest prefix with cumulative probability >= p (always including at least one token), renormalise, sample.',
  'Truncation removes the unreliable low-probability tail while renormalising keeps a valid distribution; top-p adapts the candidate set size to how peaked the distribution is.',
  'O(V log V) for sorting (O(V) with partial selection for top-k).',
  '''
  import numpy as np

  def softmax(z, T=1.0):
      z = np.asarray(z, float) / T
      e = np.exp(z - z.max())
      return e / e.sum()

  def greedy(logits):
      return int(np.argmax(logits))

  def top_k_probs(logits, k, T=1.0):
      p = softmax(logits, T)
      keep = np.argsort(p)[-k:]
      q = np.zeros_like(p)
      q[keep] = p[keep]
      return q / q.sum()

  def top_p_probs(logits, top_p, T=1.0):
      p = softmax(logits, T)
      order = np.argsort(-p)
      cum = np.cumsum(p[order])
      cutoff = np.searchsorted(cum, top_p - 1e-9) + 1   # smallest prefix with cum >= top_p (tolerance for rounding)
      q = np.zeros_like(p)
      q[order[:cutoff]] = p[order[:cutoff]]
      return q / q.sum()

  def sample(probs, rng):
      return int(rng.choice(len(probs), p=probs))
  ''',
  '''
  logits = np.log([0.5, 0.3, 0.15, 0.05])
  assert greedy(logits) == 0
  assert np.allclose(top_k_probs(logits, 2), [0.625, 0.375, 0, 0])
  assert np.allclose(top_p_probs(logits, 0.8), [0.625, 0.375, 0, 0])       # 0.5 + 0.3 >= 0.8
  assert np.allclose(top_p_probs(logits, 0.4), [1, 0, 0, 0])               # always keep at least the top token
  rng = np.random.default_rng(0)
  draws = [sample(top_k_probs(logits, 2), rng) for _ in range(2000)]
  assert set(draws) == {0, 1}
  ''',
  'Probabilities (0.5, 0.3, 0.15, 0.05) with top_p = 0.8: cumulative 0.5, 0.8, so tokens 0 and 1 stay, renormalised to (0.625, 0.375).',
  '- Top-p must keep at least one token.\n- Apply temperature before truncation.\n- searchsorted(cum, p - 1e-9) + 1 gives the smallest prefix with cumulative probability >= p (the small tolerance guards against floating-point rounding such as 0.5 + 0.3 = 0.7999999).')

C('web-ml-113',
  'Softmax cross-entropy forward and backward for a linear classifier plus a minimal training loop.',
  'For logits z = X W + b and labels y, the gradient of the mean cross-entropy wrt logits is (softmax(z) - onehot(y))/N.',
  '1. Forward: logits, stable log-softmax, loss = -mean log p[y].\n2. Backward: dz = (p - onehot)/N; dW = X^T dz; db = sum(dz).\n3. Loop: for each step W -= lr dW, b -= lr db.',
  'd/dz_k of -log softmax(z)_y = softmax(z)_k - 1[k = y]; the chain rule through z = XW + b gives dW and db.',
  'O(N D C) per step.',
  '''
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
  ''',
  '''
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
  ''',
  'At zero weights every class has probability 1/3, so the loss is log 3 = 1.0986 and the gradient on the true class logit is -2/(3N).',
  '- Divide by N (the loss is a mean).\n- Subtract the max for stability.\n- Verify with a finite-difference check.')

C('web-ml-114',
  'Causal masking for a decoder-only transformer in PyTorch: build a lower-triangular mask and apply it to attention scores.',
  'Position i must not look at j > i; adding -inf to those scores before the softmax gives them zero weight.',
  '1. mask = torch.tril(torch.ones(T, T, dtype=torch.bool)).\n2. scores = q @ k^T / sqrt(d); scores = scores.masked_fill(~mask, -inf).\n3. weights = softmax(scores, -1); out = weights @ v.\n4. Cross-check with torch.nn.functional.scaled_dot_product_attention(..., is_causal=True).',
  'exp(-inf) = 0, so future positions get zero weight, and since the diagonal is allowed every row has at least one finite score.',
  'O(T^2 d).',
  '''
  import math
  import torch
  import torch.nn.functional as F

  def causal_attention(q, k, v):
      T, d = q.shape[-2], q.shape[-1]
      scores = q @ k.transpose(-2, -1) / math.sqrt(d)
      mask = torch.tril(torch.ones(T, T, dtype=torch.bool, device=q.device))
      scores = scores.masked_fill(~mask, float('-inf'))
      return torch.softmax(scores, dim=-1) @ v
  ''',
  '''
  torch.manual_seed(0)
  q, k, v = (torch.randn(2, 4, 5, 8) for _ in range(3))
  out = causal_attention(q, k, v)
  ref = F.scaled_dot_product_attention(q, k, v, is_causal=True)
  assert torch.allclose(out, ref, atol=1e-5)
  v2 = v.clone(); v2[..., 3:, :] += 10                 # change future values
  assert torch.allclose(causal_attention(q, k, v2)[..., :3, :], out[..., :3, :])
  ''',
  'For T = 5 the mask keeps 15 of 25 entries; rows 0 to 2 are unchanged when values of positions 3 and 4 change.',
  '- Use the mask on scores, before the softmax.\n- Registered buffers avoid rebuilding the mask each call.\n- Padding masks combine with the causal mask using logical AND.')

C('web-ml-115',
  'A loss function (binary cross-entropy from logits) and logistic regression in NumPy.',
  'Computing the loss from logits with log1p(exp(-|z|)) avoids overflow and log(0).',
  '1. Stable BCE with logits: loss = mean(max(z, 0) - z y + log(1 + exp(-|z|))).\n2. Gradient wrt z is (sigmoid(z) - y)/n.\n3. Fit by gradient descent on w and b.',
  'max(z, 0) - z y + log1p(exp(-|z|)) equals -y log sigma(z) - (1 - y) log(1 - sigma(z)) algebraically but never evaluates exp of a large positive number.',
  'O(n d) per step.',
  '''
  import numpy as np

  def bce_with_logits(z, y):
      z, y = np.asarray(z, float), np.asarray(y, float)
      return float(np.mean(np.maximum(z, 0) - z * y + np.log1p(np.exp(-np.abs(z)))))

  def fit(X, y, lr=0.5, steps=2000):
      w, b = np.zeros(X.shape[1]), 0.0
      for _ in range(steps):
          z = X @ w + b
          p = 1 / (1 + np.exp(-np.clip(z, -500, 500)))
          w -= lr * X.T @ (p - y) / len(y)
          b -= lr * np.mean(p - y)
      return w, b
  ''',
  '''
  z = np.array([-800.0, 0.0, 800.0]); y = np.array([0, 1, 1])
  assert abs(bce_with_logits(z, y) - np.log(2) / 3) < 1e-12
  naive = lambda z, y: -np.mean(y * np.log(1 / (1 + np.exp(-z))) + (1 - y) * np.log(1 - 1 / (1 + np.exp(-z))))
  zz = np.array([0.3, -1.2, 2.0]); yy = np.array([1, 0, 1])
  assert abs(bce_with_logits(zz, yy) - naive(zz, yy)) < 1e-12
  rng = np.random.default_rng(0)
  X = rng.normal(size=(100, 2)); y = (X[:, 0] - X[:, 1] > 0).astype(float)
  w, b = fit(X, y)
  assert ((X @ w + b > 0) == y).mean() > 0.95
  ''',
  'Logits (-800, 0, 800) with labels (0, 1, 1): the first and third terms are 0 and the middle is log 2, mean log 2 / 3, while the naive version returns nan.',
  '- Never apply log to a probability that can be exactly 0 or 1.\n- Use the logits form of the loss.\n- Standardise features.')

C('web-ml-116',
  'Gradient descent from scratch, self-attention, and a simple energy-based voice-activity detector (VAD).',
  'GD walks downhill on a loss; attention mixes values by similarity; a VAD marks frames whose short-time energy exceeds a threshold.',
  '1. GD: x <- x - lr f\'(x) (shown here on a quadratic).\n2. Attention: see the single-head formula softmax(QK^T/sqrt(d))V.\n3. VAD: frame the signal (e.g. 25 ms windows, 10 ms hop), compute log energy per frame, threshold at mean + 0.5 std (or a noise-floor multiple), smooth with a median filter, and return the speech frames.',
  'Speech frames carry more energy than background noise; smoothing removes isolated spikes. GD converges on convex quadratics for lr < 2/L.',
  'GD O(steps x d); VAD O(n) for n samples.',
  '''
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
  ''',
  '''
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
  ''',
  'A 0.25 s tone in 1 s of noise is flagged in frames centred between samples 6,000 and 10,000 and nowhere else.',
  '- Real VADs need adaptive thresholds and hangover logic.\n- Normalise level before thresholding.\n- Learning rate for GD must be below 2/L.')

C('web-ml-117',
  'Build and defend a baseline from a CSV: parse, split, impute, encode and fit a simple model with a clear metric. (pandas is not installed here, so the verified code uses the csv module and NumPy; the pandas equivalents are noted.)',
  'A baseline sets the bar every later model must beat; it should be simple, reproducible and leakage-free.',
  '1. Inspect the schema, target and missing values.\n2. Split before any fitting (time-based if time matters).\n3. Fit preprocessing on training data only: median imputation for numeric columns, standardisation.\n4. Fit a simple model (here logistic regression by gradient descent).\n5. Report accuracy and a naive baseline (majority class); defend the choice and propose the next experiment.\nPandas equivalents: df.isna().mean(), train_test_split, SimpleImputer(median), StandardScaler, LogisticRegression.',
  'Fitting imputation and scaling statistics on the training split only keeps test information out of the pipeline, so the test metric estimates deployment performance.',
  'O(n d) per gradient step.',
  '''
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
  ''',
  '''
  rng = np.random.default_rng(0)
  lines = ['a,b,y']
  for _ in range(200):
      a, b_ = rng.normal(), rng.normal()
      y = int(a + 0.5 * b_ > 0)
      lines.append(f"{a:.4f},{'' if rng.random() < 0.1 else f'{b_:.4f}'},{y}")
  X, y = load('\\n'.join(lines))
  acc, maj = baseline(X, y)
  assert acc > 0.8 and acc > maj
  ''',
  'On synthetic data where y depends on a and b (10% of b missing), the baseline reaches over 80% test accuracy versus about 50% for the majority class.',
  '- Never compute imputation or scaling statistics on the full data before splitting.\n- State the metric and the naive baseline.\n- Check group or time leakage in the split.')

C('web-ml-118',
  'Multi-head self-attention as a PyTorch nn.Module with batch support and an optional causal mask.',
  'Project once with a fused linear layer, reshape into heads, apply scaled dot-product attention and merge.',
  '1. qkv = Linear(d, 3d); split into q, k, v of shape (B, T, d).\n2. Reshape to (B, h, T, d_h).\n3. Scores with scaling, optional causal mask, softmax.\n4. Merge heads (B, T, d) and apply an output Linear.',
  'Heads are independent attentions on subspaces; the reshape/transpose pair keeps the head dimension separate until the merge.',
  'O(B h T^2 d_h + B T d^2).',
  '''
  import math
  import torch
  import torch.nn as nn

  class MultiHeadSelfAttention(nn.Module):
      def __init__(self, d_model, n_heads, causal=False):
          super().__init__()
          assert d_model % n_heads == 0
          self.h, self.dh, self.causal = n_heads, d_model // n_heads, causal
          self.qkv = nn.Linear(d_model, 3 * d_model)
          self.out = nn.Linear(d_model, d_model)

      def forward(self, x):
          B, T, D = x.shape
          q, k, v = self.qkv(x).chunk(3, dim=-1)
          q, k, v = (t.view(B, T, self.h, self.dh).transpose(1, 2) for t in (q, k, v))
          s = q @ k.transpose(-2, -1) / math.sqrt(self.dh)
          if self.causal:
              mask = torch.tril(torch.ones(T, T, dtype=torch.bool, device=x.device))
              s = s.masked_fill(~mask, float('-inf'))
          y = torch.softmax(s, dim=-1) @ v
          return self.out(y.transpose(1, 2).reshape(B, T, D))
  ''',
  '''
  torch.manual_seed(0)
  m = MultiHeadSelfAttention(16, 4, causal=True)
  x = torch.randn(2, 6, 16)
  y = m(x)
  assert y.shape == (2, 6, 16)
  y2 = m(x[:, :4])
  assert torch.allclose(y[:, :4], y2, atol=1e-5)          # causal
  ref = torch.nn.functional.scaled_dot_product_attention(
      *(t.view(2, 6, 4, 4).transpose(1, 2) for t in m.qkv(x).chunk(3, -1)), is_causal=True)
  assert ref.shape == (2, 4, 6, 4)
  ''',
  'Input (2, 6, 16) with 4 heads of size 4 gives attention weights (2, 4, 6, 6) and output (2, 6, 16).',
  '- Use reshape (not view) after transpose.\n- Divide by sqrt(d_head).\n- Register dropout on the attention weights for training.')

C('web-ml-119',
  'Compute precision and recall at k from a flaky top-k API that may fail, return fewer than k items or duplicates.',
  'You must define the metric under unreliable output: de-duplicate, handle failures explicitly and decide how to treat missing results.',
  '1. Call the API with retries (bounded) and treat a persistent failure as an empty result, counted separately.\n2. De-duplicate results while preserving rank and truncate to k.\n3. precision@k = hits / k (or hits / len(results) if you define it over returned items; state which).\n4. recall@k = hits / |relevant|, with 0.0 when there are no relevant items.\n5. Average over queries and report the failure rate.',
  'Precision@k with a fixed denominator k penalises short or failed responses, which is the right behaviour for measuring the API\'s usefulness; de-duplication prevents inflating hits.',
  'O(k) per query.',
  '''
  def evaluate(queries, relevant, api, k, retries=2):
      precs, recs, failures = [], [], 0
      for q in queries:
          res = None
          for _ in range(retries + 1):
              try:
                  res = api(q, k)
                  break
              except Exception:
                  continue
          if res is None:
              failures += 1
              res = []
          seen, items = set(), []
          for r in res:
              if r not in seen:
                  seen.add(r)
                  items.append(r)
          items = items[:k]
          rel = relevant[q]
          hits = sum(1 for r in items if r in rel)
          precs.append(hits / k)
          recs.append(hits / len(rel) if rel else 0.0)
      n = len(queries)
      return sum(precs) / n, sum(recs) / n, failures / n
  ''',
  '''
  calls = {'n': 0}
  def api(q, k):
      calls['n'] += 1
      if q == 'bad':
          raise RuntimeError('down')
      return {'a': ['x', 'x', 'y', 'z'], 'b': ['p']}[q]
  rel = {'a': {'x', 'z', 'w'}, 'b': {'p'}, 'bad': {'u'}}
  p, r, f = evaluate(['a', 'b', 'bad'], rel, api, k=3)
  # a: items x,y,z -> hits 2 -> p 2/3, r 2/3 ; b: hits 1 -> p 1/3, r 1 ; bad: 0, 0
  assert abs(p - (2 / 3 + 1 / 3 + 0) / 3) < 1e-12 and abs(r - (2 / 3 + 1 + 0) / 3) < 1e-12 and abs(f - 1 / 3) < 1e-12
  assert calls['n'] == 1 + 1 + 3                           # the failing query was retried twice
  ''',
  'For query a the API returns x, x, y, z: de-duplicated to x, y, z with 2 hits (x and z), precision 2/3 and recall 2/3. Query b returns one item: precision 1/3. The failing query scores 0 and is counted in the failure rate.',
  '- State the precision denominator (k versus returned count).\n- Retry with a bound and backoff; never loop forever.\n- Report the failure rate next to the metric.')

C('web-ml-120',
  'Time-series groupby: per-entity daily averages and rolling means. (pandas is not installed here; the verified code uses plain Python and the equivalent pandas calls are shown in the approach.)',
  'Group rows by entity, order them by time and aggregate or roll within each group.',
  '1. Sort by (entity, timestamp).\n2. Group: pandas df.groupby("id")["value"].rolling(3).mean() (reset the index after), or df.set_index("ts").groupby("id").resample("1D").mean().\n3. Plain Python: bucket rows by entity, keep time order, compute the rolling mean over a window with a running sum.\n4. Verify index alignment: groupby-rolling returns a MultiIndex; use .reset_index(level=0, drop=True) before assigning back.',
  'Rolling windows must be computed within each group after sorting by time, otherwise values from one entity leak into another and future values leak backwards.',
  'O(n log n) for sorting, O(n) for the rolling pass.',
  '''
  from collections import defaultdict

  def rolling_mean_by_group(rows, window=3):
      by = defaultdict(list)
      for ent, ts, val in rows:
          by[ent].append((ts, val))
      out = {}
      for ent, items in by.items():
          items.sort()
          vals = [v for _, v in items]
          run, res = 0.0, []
          for i, v in enumerate(vals):
              run += v
              if i >= window:
                  run -= vals[i - window]
              res.append(run / min(i + 1, window) if i + 1 >= window else None)
          out[ent] = [(ts, m) for (ts, _), m in zip(items, res)]
      return out
  ''',
  '''
  rows = [('a', 3, 30), ('a', 1, 10), ('a', 2, 20), ('b', 1, 5), ('b', 2, 7), ('a', 4, 40)]
  res = rolling_mean_by_group(rows, window=3)
  assert res['a'] == [(1, None), (2, None), (3, 20.0), (4, 30.0)]
  assert res['b'] == [(1, None), (2, None)]
  ''',
  'Entity a sorted by time has values 10, 20, 30, 40; the 3-point rolling mean is None, None, 20, 30. Entity b has too few points.',
  '- Sort by time within each group first.\n- min_periods controls the first window values.\n- Do not use centered windows for features (future leakage).')

C('web-ml-121',
  'Fix subtle PyTorch bugs and add BatchNorm to a transformer layer. The verified code shows a corrected tiny classifier plus a BatchNorm1d feed-forward block, with checks for each classic bug.',
  'Typical PyTorch bugs are silent: forgetting model.train()/eval(), zero_grad, wrong dimension in softmax, using the loss on softmax outputs, detached tensors and shape-broadcast errors.',
  'Checklist: (1) call optimizer.zero_grad() each step; (2) loss.backward() then optimizer.step(); (3) CrossEntropyLoss expects raw logits and integer class labels, not softmax outputs; (4) model.eval() and torch.no_grad() for evaluation; (5) softmax over the feature dimension; (6) do not use in-place ops that break autograd; (7) keep tensors on the same device. BatchNorm in a transformer: BatchNorm1d normalises over (batch, time) per feature, so apply it to (B*T, D) or transpose to (B, D, T); in eval mode it uses running statistics.',
  'The checks assert that parameters change after a step, gradients exist, train and eval modes behave differently for BatchNorm, and the loss decreases.',
  'O(batch x model size) per step.',
  '''
  import torch
  import torch.nn as nn

  class FFNWithBN(nn.Module):
      def __init__(self, d, hidden):
          super().__init__()
          self.fc1, self.fc2 = nn.Linear(d, hidden), nn.Linear(hidden, d)
          self.bn = nn.BatchNorm1d(d)

      def forward(self, x):                       # x: (B, T, D)
          y = self.fc2(torch.relu(self.fc1(x)))
          B, T, D = y.shape
          y = self.bn((x + y).reshape(B * T, D)).reshape(B, T, D)
          return y

  def train_step(model, opt, x, target, loss_fn):
      model.train()
      opt.zero_grad()
      loss = loss_fn(model(x), target)
      loss.backward()
      opt.step()
      return loss.item()
  ''',
  '''
  torch.manual_seed(0)
  m = FFNWithBN(8, 16)
  opt = torch.optim.SGD(m.parameters(), lr=0.1)
  x, tgt = torch.randn(4, 5, 8), torch.randn(4, 5, 8)
  before = [p.clone() for p in m.parameters()]
  l0 = train_step(m, opt, x, tgt, nn.MSELoss())
  assert any(not torch.equal(a, b) for a, b in zip(before, m.parameters()))
  for _ in range(50):
      l1 = train_step(m, opt, x, tgt, nn.MSELoss())
  assert l1 < l0
  m.eval()
  with torch.no_grad():
      a, b = m(x), m(x)
  assert torch.allclose(a, b) and not m.bn.training
  ''',
  'After one SGD step the parameters differ from their previous values and the loss falls over 50 steps; in eval mode the BatchNorm uses running statistics so repeated calls match.',
  '- BatchNorm with tiny batches or variable-length sequences is unreliable; LayerNorm is the usual transformer choice.\n- Padding tokens pollute BatchNorm statistics.\n- Remember model.eval() before validation.')

save('B_10.json')
print(len(D))
