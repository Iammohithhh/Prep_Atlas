def are_almost_equivalent(s, t):
    out = []
    for a, b in zip(s, t):
        ok = len(a) == len(b)
        if ok:
            diff = [0] * 26
            for ch in a:
                diff[ord(ch) - 97] += 1
            for ch in b:
                diff[ord(ch) - 97] -= 1
            ok = all(abs(d) <= 3 for d in diff)
        out.append('YES' if ok else 'NO')
    return out

# ---- tests
assert are_almost_equivalent(["aabaab", "aaaaabb"], ["bbabbc", "abb"]) == ["YES", "NO"]
assert are_almost_equivalent(["aaa"], ["aab"]) == ["YES"]
assert are_almost_equivalent(["aaaa"], ["bbbb"]) == ["NO"]
assert are_almost_equivalent(["abc"], ["abcd"]) == ["NO"]
print('ok')
