def build_subsequences(s):
    n = len(s)
    out = []
    for mask in range(1, 1 << n):
        out.append(''.join(s[i] for i in range(n) if mask >> i & 1))
    out.sort()
    return out

# ---- tests
assert build_subsequences("ba") == ["a", "b", "ba"]
assert build_subsequences("xyz") == ["x", "xy", "xyz", "xz", "y", "yz", "z"]
print('ok')
