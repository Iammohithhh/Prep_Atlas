"""Independent small-instance checks for explanations in reviewed OA entries."""
from itertools import product, combinations
from functools import reduce
from operator import or_
import random
from collections import deque


def normalization(cost, days):
    lo, hi = min(cost), max(cost)
    left, right = lo, hi
    while left < right:
        mid = (left + right + 1) // 2
        if sum(max(0, mid-v) for v in cost) <= days: left = mid
        else: right = mid - 1
    lower = left
    left, right = lo, hi
    while left < right:
        mid = (left + right) // 2
        if sum(max(0, v-mid) for v in cost) <= days: right = mid
        else: left = mid + 1
    upper = left
    return upper-lower if upper > lower else int(sum(cost) % len(cost) != 0)


def simulate_normalization(cost, days):
    values = list(cost)
    for _ in range(days):
        if max(values)-min(values) <= 1: break
        small, large = values.index(min(values)), values.index(max(values))
        values[small] += 1
        values[large] -= 1
    return max(values)-min(values)


def move_count(moves, n, x, y):
    dp = [0]*(n+1); dp[x] = 1
    previous = {c:[0]*(n+1) for c in 'lr'}
    for c in moves:
        step = 1 if c == 'r' else -1
        extension = [dp[p-step] if 0 <= p-step <= n else 0 for p in range(n+1)]
        dp = [dp[p]+extension[p]-previous[c][p] for p in range(n+1)]
        previous[c] = extension
    return dp[y]


def brute_moves(moves, n, x, y):
    words = {''.join(c for i,c in enumerate(moves) if mask >> i & 1) for mask in range(1 << len(moves))}
    count = 0
    for word in words:
        p = x
        for c in word:
            p += 1 if c == 'r' else -1
            if not 0 <= p <= n: break
        else:
            count += p == y
    return count


def tile_count(tiles):
    a, b = tiles.count('RG'), tiles.count('GR')
    if a+b == 0: return max(tiles.count('RR'), tiles.count('GG'))
    return tiles.count('RR')+tiles.count('GG')+2*min(a,b)+int(a != b)


def brute_tiles(tiles):
    def visit(used, end):
        return max([used.bit_count()]+[visit(used | 1 << i,t[1]) for i,t in enumerate(tiles) if not used >> i & 1 and (end is None or t[0] == end)])
    return visit(0, None)


def parity_groups(rows):
    basis = {}
    for row in rows:
        mask = sum((v % 2) << i for i,v in enumerate(row))
        while mask:
            pivot = mask.bit_length()-1
            if pivot not in basis:
                basis[pivot] = mask; break
            mask ^= basis[pivot]
    return (1 << (len(rows)-len(basis))) - 1


def brute_groups(rows):
    return sum(all(sum(row[j] for i,row in enumerate(rows) if mask >> i & 1) % 2 == 0 for j in range(len(rows[0]))) for mask in range(1, 1 << len(rows)))


def digit_swaps(s, t):
    k = next((i for i in range(len(s)) if s[i] != t[i]), None)
    if k is None: return 0
    same = sum((s[i] > t[i]) == (s[k] > t[k]) for i in range(k+1,len(s)) if s[i] != t[i])
    different = sum((s[i] > t[i]) != (s[k] > t[k]) for i in range(k+1,len(s)) if s[i] != t[i])
    return min(same, 1+different)


def brute_swaps(s, t):
    results = []
    for mask in range(1 << len(s)):
        a = ''.join(t[i] if mask >> i & 1 else s[i] for i in range(len(s)))
        b = ''.join(s[i] if mask >> i & 1 else t[i] for i in range(len(s)))
        results.append((abs(int(a)-int(b)), mask.bit_count()))
    return min(results)[1]


def removal_or(values):
    n = len(values); full = reduce(or_,values,0)
    prefix = [0]
    for v in values: prefix.append(prefix[-1] | v)
    suffix = [0]*(n+1)
    for i in range(n-1,-1,-1): suffix[i] = suffix[i+1] | values[i]
    best = 0; right = 0
    for left in range(n):
        right = max(right, left)
        while right+1 <= n and (prefix[left] | suffix[right+1]) == full: right += 1
        best = max(best,right-left)
    return best


def brute_or(values):
    full = reduce(or_,values,0)
    return max(r-l for l in range(len(values)+1) for r in range(l,len(values)+1) if reduce(or_,values[:l]+values[r:],0) == full)


def return_path(forth):
    x = height = 0; low = high = 0
    for c in forth:
        if c == 'N': height += 1
        else: x += 1 if c == 'E' else -1
        low, high = min(low,x), max(high,x)
    def horizontal(delta): return ('E' if delta >= 0 else 'W') * abs(delta)
    candidates = [horizontal(column-x)+'S'*height+horizontal(-column) for column in (low-1,high+1)]
    return min(candidates, key=len)


def shortest_return(forth):
    vertices = {(0,0)}; x = y = 0
    for c in forth:
        x += int(c == 'E')-int(c == 'W'); y += int(c == 'N')
        if (x,y) in vertices: return None
        vertices.add((x,y))
    start = (x,y); forbidden = vertices - {start,(0,0)}
    queue = deque([(start,0)]); seen = {start}
    xmin, xmax = min(v[0] for v in vertices)-1, max(v[0] for v in vertices)+1
    while queue:
        (x,y),distance = queue.popleft()
        if (x,y) == (0,0): return distance
        for dx,dy in ((0,-1),(0,1),(-1,0),(1,0)):
            p = (x+dx,y+dy)
            if p not in seen and p not in forbidden and xmin <= p[0] <= xmax and 0 <= p[1] <= start[1]:
                seen.add(p); queue.append((p,distance+1))


def panel_gain(values):
    prefix = [0]
    for value in values: prefix.append(prefix[-1]+value)
    gain = 0
    for i,value in enumerate(values,1):
        for j in range(1,len(values)+1):
            delta = (j-i)*value + (prefix[i-1]-prefix[j-1] if j < i else -(prefix[j]-prefix[i]))
            gain = max(gain,delta)
    return sum(i*v for i,v in enumerate(values,1))+gain


def brute_panels(values):
    scores = []
    for i in range(len(values)):
        remaining = values[:i]+values[i+1:]
        for j in range(len(values)):
            result = remaining[:j]+[values[i]]+remaining[j:]
            scores.append(sum(k*v for k,v in enumerate(result,1)))
    return max(scores)


def elimination(size):
    head, step, left = 1, 1, True
    while size > 1:
        if left or size % 2: head += step
        size //= 2; step *= 2; left = not left
    return head


def brute_elimination(size):
    values = list(range(1,size+1)); left = True
    while len(values) > 1:
        values = values[1::2] if left else values[::-1][1::2][::-1]
        left = not left
    return values[0]


def any_tree_path(parent, values):
    children = [[] for _ in values]
    for node in range(1, len(values)):
        children[parent[node]].append(node)
    order = [0]
    for node in order:
        order.extend(children[node])
    down = [0] * len(values)
    best = max(values)
    for node in reversed(order):
        first = second = 0
        for child in children[node]:
            gain = down[child]
            if gain > first:
                first, second = gain, first
            elif gain > second:
                second = gain
        down[node] = values[node] + first
        best = max(best, values[node] + first + second)
    return best


def brute_tree_paths(parent, values):
    edges = [[] for _ in values]
    for node in range(1, len(values)):
        edges[node].append(parent[node])
        edges[parent[node]].append(node)
    sums = []
    for start in range(len(values)):
        pending = [(start, -1, values[start])]
        while pending:
            node, previous, total = pending.pop()
            sums.append(total)
            pending.extend((nxt, node, total + values[nxt]) for nxt in edges[node] if nxt != previous)
    return max(sums)


def alternating_partitions(values):
    mod = 10**9 + 7
    bucket = [[0, 0], [0, 0]]
    parity = 0
    even = odd = 0
    for value in values:
        parity ^= value & 1
        even = (bucket[parity][1] + (parity == 0)) % mod
        odd = (bucket[parity ^ 1][0] + (parity == 1)) % mod
        bucket[parity][0] = (bucket[parity][0] + even) % mod
        bucket[parity][1] = (bucket[parity][1] + odd) % mod
    return (even + odd) % mod


def brute_partitions(values):
    result = 0
    for mask in range(1 << (len(values)-1)):
        sums = []
        total = values[0]
        for i in range(1, len(values)):
            if mask & (1 << (i-1)):
                sums.append(total)
                total = 0
            total += values[i]
        sums.append(total)
        result += all(a % 2 != b % 2 for a, b in zip(sums, sums[1:]))
    return result


def cover_width(values, clusters):
    values = sorted(values)
    left, right = 0, values[-1] - values[0]
    while left < right:
        middle = (left + right) // 2
        used, end = 0, None
        for value in values:
            if end is None or value > end:
                used += 1
                end = value + middle
        if used <= clusters:
            right = middle
        else:
            left = middle + 1
    return left


def brute_cover_width(values, clusters):
    values = sorted(values)
    answer = values[-1] - values[0]
    for mask in range(1 << (len(values)-1)):
        if mask.bit_count()+1 > clusters:
            continue
        start, widths = 0, []
        for i in range(1, len(values)):
            if mask & (1 << (i-1)):
                widths.append(values[i-1] - values[start])
                start = i
        widths.append(values[-1] - values[start])
        answer = min(answer, max(widths))
    return answer


def downward_tree_path(parent, values):
    children = [[] for _ in parent]
    root = parent.index(-1)
    for node, p in enumerate(parent):
        if p >= 0: children[p].append(node)
    best_end = list(values)
    order = [root]
    for node in order:
        for child in children[node]:
            best_end[child] += max(0, best_end[node])
            order.append(child)
    return max(best_end)


def brute_downward_path(parent, values):
    sums = []
    for end in range(len(parent)):
        node, total = end, 0
        while node != -1:
            total += values[node]
            sums.append(total)
            node = parent[node]
    return max(sums)


def three_subsequence(target, source):
    dp = [1, 0, 0, 0]
    for char in source:
        for matched in range(3, 0, -1):
            if char == target[matched-1]: dp[matched] += dp[matched-1]
    return dp[3]


def brute_three_subsequence(target, source):
    return sum(''.join(source[i] for i in indices) == target
               for indices in combinations(range(len(source)), 3))


if __name__ == '__main__':
    rng = random.Random(317)
    checks = 0
    for size in range(1,6):
        for cost in product(range(1,5), repeat=size):
            for days in (0,1,2,5,12):
                assert normalization(cost,days) == simulate_normalization(cost,days), (cost, days)
                checks += 1
    for length in range(7):
        for chars in product('lr', repeat=length):
            moves = ''.join(chars)
            for n in range(1,4):
                for x in range(n+1):
                    for y in range(n+1):
                        assert move_count(moves,n,x,y) == brute_moves(moves,n,x,y), (moves,n,x,y)
                        checks += 1
    assert move_count('rrlrlr',6,1,4) == 3
    for size in range(1,6):
        for tiles in product(('RR','RG','GR','GG'), repeat=size):
            assert tile_count(tiles) == brute_tiles(tiles), tiles
            checks += 1
    for _ in range(400):
        rows = [[rng.randrange(10) for _ in range(5)] for _ in range(rng.randrange(1,9))]
        assert parity_groups(rows) == brute_groups(rows)
        size = rng.randrange(1,9)
        s, t = (''.join(str(rng.randrange(1 if i == 0 else 0,10)) for i in range(size)) for _ in range(2))
        assert digit_swaps(s,t) == brute_swaps(s,t), (s,t)
        values = [rng.randrange(16) for _ in range(size)]
        assert removal_or(values) == brute_or(values), values
        values = [rng.randrange(-10,11) for _ in range(size)]
        assert panel_gain(values) == brute_panels(values)
        checks += 4
    for length in range(2,9):
        for middle in product('NEW',repeat=length-2):
            forth = 'N'+''.join(middle)+'N'
            distance = shortest_return(forth)
            if distance is not None:
                assert len(return_path(forth)) == distance, forth
                checks += 1
    for size in range(1,301):
        assert elimination(size) == brute_elimination(size)
        checks += 1
    assert panel_gain([8,1,6,3,4]) == 78
    assert panel_gain([3,5,-9,10]) == 52
    assert elimination(12) == 6 and elimination(25) == 14
    for _ in range(400):
        size = rng.randrange(1, 12)
        parent = [-1] + [rng.randrange(i) for i in range(1, size)]
        values = [rng.randrange(-12, 13) for _ in range(size)]
        assert any_tree_path(parent, values) == brute_tree_paths(parent, values), (parent, values)
        checks += 1
    assert any_tree_path([-1,0,1,2,0], [-2,10,10,-3,10]) == 28
    assert any_tree_path([-1] + list(range(99999)), [-1]*100000) == -1
    for size in range(1, 9):
        for bits in product((1,2), repeat=size):
            assert alternating_partitions(bits) == brute_partitions(bits), bits
            checks += 1
    for _ in range(400):
        values = [rng.randrange(-20,21) for _ in range(rng.randrange(1,10))]
        clusters = rng.randrange(1,len(values)+1)
        assert cover_width(values,clusters) == brute_cover_width(values,clusters), (values,clusters)
        checks += 1
    assert alternating_partitions([1,2,3,3]) == 4
    assert alternating_partitions([1,1,1,1]) == 2
    assert cover_width([1,9,3,10,14],2) == 5  # Real radius 2.5; integer radius 3.
    for _ in range(400):
        size = rng.randrange(1, 15)
        parent = [-1] + [rng.randrange(i) for i in range(1, size)]
        values = [rng.randrange(-20,21) for _ in parent]
        permutation = list(range(size)); rng.shuffle(permutation)
        shuffled_parent, shuffled_values = [0]*size, [0]*size
        for old, new in enumerate(permutation):
            shuffled_parent[new] = -1 if parent[old] == -1 else permutation[parent[old]]
            shuffled_values[new] = values[old]
        assert downward_tree_path(shuffled_parent, shuffled_values) == brute_downward_path(shuffled_parent, shuffled_values)
        checks += 1
    assert downward_tree_path([-1,0,1,2,0],[-2,10,10,-3,10]) == 20
    assert downward_tree_path([-1] + list(range(99999)), [-1]*100000) == -1
    for target_tuple in product('AB', repeat=3):
        target = ''.join(target_tuple)
        for size in range(9):
            for source_tuple in product('AB', repeat=size):
                source = ''.join(source_tuple)
                assert three_subsequence(target, source) == brute_three_subsequence(target, source)
                checks += 1
    assert three_subsequence('ABC','ABCBABC') == 5
    assert three_subsequence('HRW','HERHRWS') == 3
    print(f'Reviewed algorithm explanations: {checks} independent comparisons passed.')
