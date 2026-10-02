def first_k_primes(n_sum, k, limit=100000):
    sieve = bytearray([1]) * limit
    sieve[0] = sieve[1] = 0
    for i in range(2, int(limit ** 0.5) + 1):
        if sieve[i]:
            sieve[i * i::i] = bytearray(len(sieve[i * i::i]))
    out = []
    for p in range(2, limit):
        if sieve[p] and sum(map(int, str(p))) == n_sum:
            out.append(p)
            if len(out) == k:
                break
    return out if out else [-1]

# ---- tests
assert first_k_primes(10, 5) == [19, 37, 73, 109, 127]
assert first_k_primes(12, 4) == [-1]
assert first_k_primes(2, 3) == [2, 11, 101]
print('ok')
