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

docs = ["the cat sat on the mat", "the cat sat", "dogs bark loudly"]
V = tfidf_vectors(docs)
assert abs(cosine(V[0], V[0]) - 1) < 1e-12
assert cosine(V[0], V[1]) > 0.5 and cosine(V[0], V[2]) == 0.0
print("ok")
