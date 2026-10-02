def closest_color(bits):
    pure = {'Black': (0, 0, 0), 'White': (255, 255, 255), 'Red': (255, 0, 0), 'Green': (0, 255, 0), 'Blue': (0, 0, 255)}
    r, g, b = int(bits[0:8], 2), int(bits[8:16], 2), int(bits[16:24], 2)
    dist = {name: abs(r - x) + abs(g - y) + abs(b - z) for name, (x, y, z) in pure.items()}
    best = min(dist.values())
    winners = [name for name, d in dist.items() if d == best]
    return winners[0] if len(winners) == 1 else 'Ambiguous'

# ---- tests
assert closest_color('000000000000000000000000') == 'Black'
assert closest_color('111111111111111111111111') == 'White'
assert closest_color('111111110000000000000000') == 'Red'
# 010111011010010110000011 = (93, 165, 131): distances Black 389, White 307, Red 369, Green 227 (Manhattan), Blue 349 -> Green
assert closest_color('010111011010010110000011') == 'Green'
assert closest_color('100000000000000000000000') == 'Red'     # (128,0,0): 127 to Red, 128 to Black
print('ok')
