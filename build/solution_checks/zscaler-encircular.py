def does_circle_exist(commands):
    out = []
    for cmd in commands:
        x = y = 0
        dx, dy = 0, 1                      # facing north
        for _ in range(4):                 # four repetitions return to the start iff the path is bounded
            for c in cmd:
                if c == 'G':
                    x, y = x + dx, y + dy
                elif c == 'L':
                    dx, dy = -dy, dx
                else:
                    dx, dy = dy, -dx
        out.append('YES' if (x, y) == (0, 0) else 'NO')
    return out

# ---- tests
import random
assert does_circle_exist(["G", "L", "RGRG"]) == ["NO", "YES", "YES"]
def brute(cmd):
    x = y = 0; dx, dy = 0, 1
    for _ in range(200):
        for c in cmd:
            if c == 'G': x, y = x + dx, y + dy
            elif c == 'L': dx, dy = -dy, dx
            else: dx, dy = dy, -dx
    return 'YES' if abs(x) + abs(y) < 5000 and max(abs(x), abs(y)) <= 4 * len(cmd) else 'NO'
for _ in range(500):
    cmd = ''.join(random.choice('GLR') for _ in range(random.randint(1, 8)))
    assert does_circle_exist([cmd]) == [brute(cmd)], cmd
print('ok')
