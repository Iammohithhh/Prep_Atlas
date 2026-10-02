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

f = lambda x: (x - 3) ** 2 + 1
assert abs(ternary_min(f, -10, 10) - 3) < 1e-6
assert abs(bisect_derivative(lambda x: 2 * (x - 3), -10, 10) - 3) < 1e-6
g = lambda x: abs(x - 1) + abs(x - 4) + abs(x - 6)       # convex, minimum at the median 4
assert abs(ternary_min(g, -10, 10) - 4) < 1e-5
print("ok")
