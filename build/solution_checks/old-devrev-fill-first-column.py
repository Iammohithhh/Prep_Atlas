from functools import lru_cache


def solution(field):
    rows, cols = len(field), len(field[0])
    start = tuple(tuple(c == '#' for c in row) for row in field)

    def throw(state, r):
        """Return the new state after throwing a block into row r, or None if the row's first cell is taken."""
        if state[r][0]:
            return None
        c = 0
        while c + 1 < cols and not state[r][c + 1]:
            c += 1
        rr = r
        while rr + 1 < rows and not state[rr + 1][c]:
            rr += 1
        grid = [list(row) for row in state]
        grid[rr][c] = True
        return tuple(tuple(row) for row in grid)

    def done(state):
        return all(state[r][0] for r in range(rows))

    @lru_cache(None)
    def lo(state):
        if done(state):
            return 0
        best = 10**9
        for r in range(rows):
            nxt = throw(state, r)
            if nxt is not None:
                best = min(best, 1 + lo(nxt))
        return best

    @lru_cache(None)
    def hi(state):
        if done(state):
            return 0
        best = -10**9
        for r in range(rows):
            nxt = throw(state, r)
            if nxt is not None:
                best = max(best, 1 + hi(nxt))
        return best

    return [lo(start), hi(start)]

# ---- tests
assert solution([list(".##"), list("#.."), list("...")]) == [4, 4]
assert solution([list(".##"), list("..#"), list("...")]) == [3, 6]
print('ok')
