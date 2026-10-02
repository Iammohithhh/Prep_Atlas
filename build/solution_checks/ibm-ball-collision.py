def find_remaining_balls(direction, strength):
    stack = []                         # indices of right-moving balls that are still alive
    left_survivors = []                # left-moving balls that got past every right-moving ball
    for i, d in enumerate(direction):
        if d == 1:
            stack.append(i)
            continue
        alive = True
        while stack:
            top = stack[-1]
            if strength[top] > strength[i]:
                alive = False
                break
            if strength[top] == strength[i]:
                stack.pop()
                alive = False
                break
            stack.pop()                # the right-moving ball is weaker and is destroyed
        if alive:
            left_survivors.append(i)
    return sorted(left_survivors + stack)

# ---- tests
import random
assert find_remaining_balls([1, -1], [2, 1]) == [0]
assert find_remaining_balls([1, -1, 1], [5, 3, 1]) == [0, 2]
assert find_remaining_balls([1, 1], [3, 4]) == [0, 1]
def brute(direction, strength):
    balls = [[i, direction[i], strength[i]] for i in range(len(direction))]
    changed = True
    while changed:
        changed = False
        for j in range(len(balls) - 1):
            a, b = balls[j], balls[j + 1]
            if a[1] == 1 and b[1] == -1:      # adjacent right-mover and left-mover collide
                if a[2] > b[2]: del balls[j + 1]
                elif a[2] < b[2]: del balls[j]
                else: del balls[j:j + 2]
                changed = True
                break
    return sorted(b[0] for b in balls)
for _ in range(500):
    n = random.randint(1, 9)
    d = [random.choice([1, -1]) for _ in range(n)]; s = [random.randint(1, 5) for _ in range(n)]
    assert find_remaining_balls(d, s) == brute(d, s), (d, s)
print('ok')
