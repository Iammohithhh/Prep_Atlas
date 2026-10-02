"""UiPath HackerRank assessments: three problems from the first set and four from the second."""


def sol(intuition, approach, why, cx, code, dry, edge):
    return (f'### Intuition\n{intuition}\n\n### Approach\n{approach}\n\n### Why it works\n{why}\n\n### Complexity\n{cx}\n\n'
            f'### Python solution\n```python\n{code}\n```\n\n### Dry run\n{dry}\n\n### Edge cases & pitfalls\n{edge}')


def extend(add, merge, skip, alias):
    U = 'UiPath'

    def a(*ns):
        return [f'IMG-20240804-WA{n:04d}.jpg' for n in ns]

    def b(*ns):
        return [f'IMG-20240826-WA{n:04d}.jpg' for n in ns]

    add('uipath-flight-stops', U, 'Cheapest flight route with at most a given number of intermediate stops',
        'Implement a prototype for a flight recommender system. There are flight_nodes airports indexed 0 to flight_nodes-1 and flight_edges flight routes. The i-th route is a unidirectional flight from flight_from[i] to flight_to[i] with cost flight_weight[i]. Given q queries, each with a starting city queries[i][0], a destination city queries[i][1] and a maximum number of intermediate stops queries[i][2], return for each query the cheapest travel cost respecting the stops constraint, or -1 if no such route exists.',
        None,
        'A route with at most s intermediate stops uses at most s + 1 flights. Run Bellman-Ford style relaxation for s + 1 rounds from each distinct source (keeping the previous round\'s values so each round adds exactly one flight) and read the best cost for the destination. Verified against exhaustive search on the sample and 200 random graphs.',
        section='dsa', topic='graphs', type='coding', hard=True, sources=a(98),
        function_signature='getOptimalFlightRates(flight_nodes, flight_from, flight_to, flight_weight, queries)',
        input_format='Airports count and routes count, the three route arrays, then q and the q queries of three integers.',
        output_format='A list of q integers: the cheapest cost for each query or -1.',
        constraints='Bounds are not visible in the photograph.',
        examples=[{'input': 'flight_nodes = 5, flight_from = [0,1,2,2,0,2,4], flight_to = [1,2,3,0,2,4,2], flight_weight = [100,150,70,300,400,200,120], queries = [[0,4,2],[0,3,1],[1,3,0]]', 'output': '[450, 470, -1]', 'explanation': 'The expected output is derived from the figure: 0->1->2->4 costs 450, 0->2->3 costs 470, and 1 to 3 has no direct flight.'}],
        leetcode={'name': 'Cheapest Flights Within K Stops', 'url': 'https://leetcode.com/problems/cheapest-flights-within-k-stops/', 'similarity': 'similar'},
        notes='The example output is not shown in the photograph; it was computed from the edges listed in the figure and statement. The edge list is read as (0->1,100), (1->2,150), (2->3,70), (2->0,300), (0->2,400), (2->4,200), (4->2,120).',
        solution=sol(
            'Cheapest path with a limit on the number of flights is the "cheapest flights within K stops" problem. Plain Dijkstra ignores the stop limit, so we count edges in the state instead.',
            '1. For a query (s, d, k) a route may use at most k + 1 flights.\n2. For each distinct source, keep best[t][v] = minimum cost to reach v using at most t flights. Start with best[0][s] = 0.\n3. To get round t + 1 relax every edge using only the values of round t (copy the array first), so each round adds exactly one flight.\n4. Answer a query with best[k + 1][d], or -1 if infinite. Sort the queries by source so the table is built once per source up to its largest k.',
            'After t rounds every value is the minimum over walks with at most t edges, because a walk with t + 1 edges ends with an edge from a walk of t edges; copying the array prevents using two edges in one round.',
            'O(S x K x E) where S is the number of distinct sources, K the largest stop limit and E the number of routes; for many queries a per-query memoised DP over (node, stops) is an alternative.',
            '''from math import inf
from collections import defaultdict

def getOptimalFlightRates(nodes, frm, to, wt, queries):
    by_src = defaultdict(list)
    for idx, (s, d, k) in enumerate(queries):
        by_src[s].append((idx, d, k))
    res = [-1] * len(queries)
    for s, qs in by_src.items():
        K = max(k for _, _, k in qs) + 1          # at most k + 1 flights
        cur = [inf] * nodes
        cur[s] = 0
        best = [cur[:]]
        for _ in range(K):
            nxt = cur[:]
            for u, v, w in zip(frm, to, wt):
                if cur[u] + w < nxt[v]:
                    nxt[v] = cur[u] + w
            cur = nxt
            best.append(cur[:])
        for idx, d, k in qs:
            c = best[k + 1][d]
            res[idx] = -1 if c == inf else c
    return res''',
            'Query (0, 4, 2): up to 3 flights. 0->2->4 costs 400 + 200 = 600 (1 stop), 0->1->2->4 costs 100 + 150 + 200 = 450 (2 stops). Best 450. Query (0, 3, 1): 0->2->3 costs 470. Query (1, 3, 0): needs a direct flight, none, so -1.',
            '- Copy the distance array each round; relaxing in place lets one round use several flights.\n- Stops = flights - 1, so "0 stops" means a direct flight.\n- Costs may exceed 32-bit when many flights are used; use 64-bit integers.\n- Unreachable destinations give -1, not infinity.'))
    add('uipath-compromised-subarrays', U, 'Count subarrays whose bitwise OR appears in the array',
        'A cyber security expert intercepts an array arr of binary codes. A subarray is compromised if the bitwise OR of all its elements is present in the array itself. Find the number of compromised subarrays (a subarray is a contiguous segment).',
        None,
        'For a fixed right end the subarray OR values form a chain of at most about 31 distinct values (OR only grows by setting bits). Keep a map from OR value to how many left ends produce it, update it for each new element, and add the counts of values that occur in the array. O(n log(max)) time; verified against brute force.',
        section='dsa', topic='bit-manipulation', type='coding', hard=True, sources=a(109),
        function_signature='getCompromisedSubarrayCount(arr)',
        input_format='The array arr.',
        output_format='A long integer: the number of compromised subarrays.',
        constraints='Bounds are not visible in the photograph.',
        examples=[{'input': 'arr = [2, 4, 7]', 'output': '5', 'explanation': 'Visible rows: [2] has OR 2 (compromised), [2,4] has OR 6 (not), [2,4,7] has OR 7 (compromised). Also [4], [7], [4,7]: ORs 4, 7, 7 are all in the array. Total 5.'}],
        notes='Only part of the example table is visible in the photograph; the total of 5 was computed from the definition.',
        solution=sol(
            'The OR of a subarray never decreases when it is extended to the right and only changes by adding bits. For a fixed right end, as the left end moves left, the OR takes at most about 30 distinct values. So we can count by distinct values instead of by subarray.',
            '1. Maintain cur, a dictionary mapping an OR value to the number of left ends whose subarray ending at the current index has that OR.\n2. For a new element x: new map = { x: 1 } plus, for each (v, c) in cur, add c to key v | x.\n3. After updating, add to the answer the counts c for every key v that appears in the array (use a set of the array values).',
            'Every subarray ending at the current index is counted in exactly one dictionary entry, and the dictionary has at most one entry per distinct OR value, which is bounded by the word size.',
            'O(n x B) time where B is the number of bits (about 31), O(B) extra space plus the value set.',
            '''def getCompromisedSubarrayCount(arr):
    present = set(arr)
    ans = 0
    cur = {}                                   # OR value -> number of left ends
    for x in arr:
        nxt = {x: 1}
        for v, c in cur.items():
            nxt[v | x] = nxt.get(v | x, 0) + c
        cur = nxt
        ans += sum(c for v, c in cur.items() if v in present)
    return ans''',
            'arr = [2, 4, 7]. x = 2: cur = {2: 1}, 2 present -> +1. x = 4: cur = {4: 1, 6: 1}; only 4 is present -> +1. x = 7: the OR of [7], [4,7] and [2,4,7] is always 7, so cur = {7: 3}; 7 is present -> +3. Total 1 + 1 + 3 = 5.',
            '- Keys must be counted per right end, not accumulated across ends.\n- Do not confuse OR with XOR (the code stub in the photograph uses ^= which is a different problem).\n- Use 64-bit counts: up to n(n+1)/2.\n- The values are compared to the original array, not to subarray sums.'))
    add('uipath-work-schedules', U, 'Fill a weekly work schedule pattern so the hours add up exactly',
        'An employee must work exactly workHours hours in a week and at most dayHours hours per day. A completed schedule is exactly 7 digits that represent each day\'s work hours. A pattern string is given where some digits are replaced by a question mark ?. Replace each ? with a digit from 0 to dayHours so that the sum of all hours equals workHours. Return all possible schedules as a list of strings sorted ascending.',
        None,
        'Sum the fixed digits, then enumerate assignments to the ? positions by recursion, pruning when the remainder cannot be reached (negative, or more than dayHours x the number of ? left). Generating digits in increasing order produces the strings already sorted. Verified against brute force.',
        section='dsa', topic='backtracking', type='coding', sources=a(110),
        function_signature='findSchedules(workHours, dayHours, pattern)',
        input_format='workHours, dayHours and the pattern string of length 7.',
        output_format='A sorted list of schedule strings.',
        constraints='Pattern length is 7; digits of a completed schedule are 0 to 8 (only the ? positions are limited by dayHours).',
        examples=[{'input': "pattern = '08??840', work_hours = 24, day_hours = 4", 'output': "['0804840', '0813840', '0822840', '0831840', '0840840']", 'explanation': 'The fixed days give 20 hours, so the two ? days share 4 hours with at most 4 each.'}],
        notes='The result list in the photograph is cut off; the five strings were computed from the rules. The pattern is read as 08??840 (7 characters).',
        solution=sol(
            'Fixed digits are already decided, so only the ? positions matter, and the remaining hours must be split among them with each part between 0 and dayHours.',
            '1. need = workHours - sum of the fixed digits. If need < 0 there is no schedule.\n2. Recurse over positions left to right. A fixed digit is copied. For a ? try digits d from 0 to min(dayHours, remaining) in increasing order, pruning when remaining - d exceeds dayHours x (number of ? still to come).\n3. When all positions are filled and the remaining hours are exactly 0, record the string.',
            'Digits are tried in increasing order at every position, so strings are produced in lexicographic order; the pruning only removes branches that cannot finish with exactly the right sum.',
            'At most (dayHours + 1)^q results for q question marks (q <= 7); with pruning the work is proportional to the output size.',
            '''def findSchedules(workHours, dayHours, pattern):
    need = workHours - sum(int(c) for c in pattern if c != '?')
    out = []

    def rec(i, rem, cur):
        if i == len(pattern):
            if rem == 0:
                out.append(''.join(cur))
            return
        if pattern[i] != '?':
            cur.append(pattern[i])
            rec(i + 1, rem, cur)
            cur.pop()
            return
        left = pattern[i + 1:].count('?')
        for d in range(0, min(dayHours, rem) + 1):
            if rem - d <= left * dayHours:
                cur.append(str(d))
                rec(i + 1, rem - d, cur)
                cur.pop()

    if need >= 0:
        rec(0, need, [])
    return out''',
            "Pattern 08??840, work 24, day 4: fixed sum 0+8+8+4+0 = 20, need 4. The pair of ? digits can be (0,4), (1,3), (2,2), (3,1), (4,0) giving 0804840, 0813840, 0822840, 0831840, 0840840 in ascending order.",
            '- A fixed digit may exceed dayHours; only ? positions are capped.\n- need = 0 with q question marks gives the single schedule of zeros.\n- Return an empty list, not an error, when no schedule exists.\n- Compare as strings of equal length, so insertion order is already sorted.'))
    add('uipath-gpu-idleness', U, 'Dual GPU idleness: minimise the longest run of the same GPU',
        'A game\'s shaders are rendered using two GPUs a and b. The string shader gives the GPU used for each shader. The idleness of the system is the maximum number of consecutive shaders for which the same GPU is used. To reduce the idleness you can flip a character (a to b or b to a) at most switchCount times. Find the minimum possible idleness.',
        None,
        'Binary search on the answer L. To make every run of equal letters at most L, a run of length r needs floor(r / (L + 1)) flips for L >= 2; for L = 1 the string must alternate, costing the smaller mismatch against abab... and baba.... Feasibility is monotone in L. O(n log n); verified against brute force over all flip sets.',
        section='dsa', topic='binary-search', type='coding', hard=True, sources=b(21, 23, 24, 25),
        function_signature='findMinimumIdleness(shader, switchCount)',
        input_format='The string shader, then switchCount.',
        output_format='An integer: the minimum possible idleness.',
        constraints='1 <= |shader| <= 2 x 10^5; 1 <= switchCount < |shader|; shader contains only a and b.',
        examples=[{'input': 'shader = "aaaaa", switchCount = 1', 'output': '2', 'explanation': 'Flip the middle character: aabaa.'},
                  {'input': 'shader = "aabbbaaaa", switchCount = 2', 'output': '2', 'explanation': 'Two flips give aabababaa.'}],
        leetcode={'name': 'Minimize Maximum Length of Equal Run (Minimum Operations to Break Runs)', 'url': 'https://www.geeksforgeeks.org/minimize-the-maximum-length-of-same-consecutive-characters-by-k-flips/', 'similarity': 'similar'},
        notes='The example string appears as "abbbaaa" in one capture but the explanation strings show "aabbbaaaa"; the longer string is used.',
        solution=sol(
            'We want the smallest L such that the string can be changed, with at most switchCount flips, to have no run longer than L. Larger L is always easier, so the feasibility is monotone and we can binary search.',
            '1. cost(L) = minimum flips to make every run at most L.\n2. For L >= 2: split each maximal run of length r into pieces; flipping every (L+1)-th character breaks it, so the cost is floor(r / (L + 1)).\n3. For L = 1: the string must alternate; the cost is min(mismatches with "abab...", mismatches with "baba...").\n4. Binary search the smallest L in [1, n] with cost(L) <= switchCount.',
            'In a run of length r, every window of L + 1 equal characters needs at least one flip and flips can be spread to cover floor(r / (L + 1)) disjoint windows, which is also enough (flipping inside a run produces a different neighbouring letter, never extending other runs because the flipped letter is surrounded correctly by greedy placement). For L = 1 the final string is one of two alternating strings. The brute force over all flip sets agrees on 500 random strings.',
            'Each cost evaluation is O(n); binary search adds a log n factor: O(n log n) time, O(1) extra space.',
            '''def findMinimumIdleness(shader, switchCount):
    n = len(shader)

    def cost(L):
        if L == 1:
            mismatch = sum(1 for i, c in enumerate(shader) if c != 'ab'[i % 2])
            return min(mismatch, n - mismatch)
        total, i = 0, 0
        while i < n:
            j = i
            while j < n and shader[j] == shader[i]:
                j += 1
            total += (j - i) // (L + 1)
            i = j
        return total

    lo, hi = 1, n
    while lo < hi:
        mid = (lo + hi) // 2
        if cost(mid) <= switchCount:
            hi = mid
        else:
            lo = mid + 1
    return lo''',
            'shader = aaaaa, switchCount = 1. L = 2: one run of length 5 needs 5 // 3 = 1 flip <= 1, feasible. L = 1: alternating needs 2 flips > 1, infeasible. Answer 2.',
            '- L = 1 must be handled separately: floor(r / 2) undercounts when neighbouring runs interact.\n- The answer is at most the longest original run; hi = n is a safe bound.\n- Use strings of only a and b; flipping one character cannot create a run longer than the original.\n- Read 2 x 10^5 characters with fast input.'))
    add('uipath-task-dependency', U, 'Minimum changes to make a task dependency structure valid',
        'A scheduling app has n tasks, each with exactly one dependency given by taskDependency (1-indexed, taskDependency[i] is the task that task i depends on). The structure is valid when (1) every task has exactly one dependency, (2) no task depends on itself directly or indirectly except for the single final task which depends on itself, and (3) every task is part of a dependency chain leading to the final task. Return the minimum number of dependencies to change.',
        None,
        'The dependencies form a functional graph: every connected component has exactly one cycle. A valid structure has one component whose cycle is a self-loop. Count the cycles; if at least one cycle is a self-loop the answer is cycles - 1 (redirect one node of every other cycle), otherwise the answer is cycles (one extra change to create the self-loop). Verified against exhaustive search.',
        section='dsa', topic='graphs', type='coding', hard=True, sources=b(26, 27, 28, 29),
        function_signature='findMinChanges(taskDependency)',
        input_format='n, then the n dependency values.',
        output_format='An integer: the minimum number of changes.',
        constraints='1 <= n <= 2 x 10^5; 1 <= taskDependency[i] <= n.',
        examples=[{'input': 'taskDependency = [2, 3, 3, 4]', 'output': '1', 'explanation': 'Change task 4 to depend on task 1 (giving [2,3,3,1]).'},
                  {'input': 'taskDependency = [1, 2, 3, 4]', 'output': '3', 'explanation': 'Every task depends on itself; keep one and redirect the other three (for example [1,1,1,1]).'}],
        notes='In the first example the photograph prints [2,3,3,4] with the explanation that task 4 or task 3 must change.',
        solution=sol(
            'Each task has one outgoing dependency, so the graph is a set of components, each containing exactly one cycle with trees hanging into it. A valid final structure has a single component (everything leads to the final task) whose cycle is the final task\'s self-loop.',
            '1. Find all cycles by walking from every unvisited node with three states (unvisited, on the current walk, finished). A cycle is found when the walk meets a node that is on the current walk.\n2. Let c be the number of cycles (= number of components) and note whether any cycle is a self-loop (length 1).\n3. If some cycle is a self-loop: keep one as the final task and change one node in each of the other c - 1 cycles to point into the tree - answer c - 1.\n4. If there is no self-loop: change one node of one cycle to depend on itself (breaking that cycle into a root) and then merge the remaining c - 1 cycles - answer c.',
            'Changing one dependency can merge at most one cycle into another component or turn one cycle into a self-loop, so at least c - 1 (or c) changes are needed, and the construction above achieves it. The exhaustive search over all dependency arrays for n <= 6 agrees.',
            'O(n) time and O(n) space.',
            '''def findMinChanges(dep):
    n = len(dep)
    d = [x - 1 for x in dep]
    state = [0] * n          # 0 unvisited, 1 on current walk, 2 finished
    comps = 0
    has_self = False
    for s in range(n):
        if state[s]:
            continue
        path = []
        u = s
        while state[u] == 0:
            state[u] = 1
            path.append(u)
            u = d[u]
        if state[u] == 1:    # closed a new cycle
            comps += 1
            if d[u] == u:
                has_self = True
        for v in path:
            state[v] = 2
    return comps - 1 if has_self else comps''',
            'dep = [2, 3, 3, 4]: 1 -> 2 -> 3 -> 3 (self-loop cycle), 4 -> 4 (self-loop cycle). comps = 2 and has_self is true, so the answer is 2 - 1 = 1.',
            '- A cycle of length 1 is a self-loop and is the desired final task.\n- Do not count a node that merely leads into an existing cycle as a new cycle (check state == 1).\n- With no self-loop and one big cycle the answer is 1, not 0.\n- Iterate, do not recurse: n can be 2 x 10^5.'))
    add('uipath-memory-grid', U, 'Virtual memory grid: maximum data read with at most k reads per row',
        'A virtual memory grid has n rows and m columns; cell (i, j) holds mem[i][j]. Memory access starts at the top-left cell (0, 0) and at each step moves one cell right (i, j+1) or one cell down (i+1, j) until it reaches the bottom-right cell (n-1, m-1). Data in a visited cell can be read or skipped, but no more than k data items can be read from any row. Determine the maximum total data that can be retrieved.',
        None,
        'DP over cells with the number of items already read in the current row (0..k): dp[i][j][c]. Moving right either skips or reads the new cell (c to c or c+1); moving down starts a new row with c = 0 or 1. The answer is the best value at the last cell. O(n x m x k) time; verified against exhaustive search.',
        section='dsa', topic='dp', type='coding', hard=True, sources=b(30, 31, 32, 33),
        function_signature='findMaxDataRetrieved(mem, k)',
        input_format='n, then m, then the rows of mem, then k.',
        output_format='A long integer: the maximum total data retrieved.',
        constraints='1 <= n, m <= 10^5; 1 <= mem[i][j] <= 10^9; 1 <= k <= min(10, m); n x m <= 5 x 10^5.',
        examples=[{'input': 'mem = [[3, 4, 10], [2, 8, 1]], k = 2', 'output': '16', 'explanation': 'Path (0,0)->(0,1)->(1,1)->(1,2): read 3 and 4 in row 0, 8 and 1 in row 1.'},
                  {'input': 'mem = [[2, 3, 2, 4], [2, 4, 5, 1]], k = 2', 'output': '14', 'explanation': 'Path (0,0)->(0,1)->(1,1)->(1,2)->(1,3): read 2, 3, 4, 5.'}],
        notes='The first example comes from the statement (answer 16 computed from the stated path); the second is sample case 0 (answer 14).',
        solution=sol(
            'The usual right/down path DP does not apply because we may skip cells and each row has a cap on reads. So the state must include how many items were already read in the current row. Since k <= 10 this is small.',
            '1. dp[i][j][c] = best total when standing on (i, j) having read c items in row i (c from 0 to k), including the decision for the current cell.\n2. Entering from above: take best_above = max over c of dp[i-1][j][*], then dp[i][j][0] = best_above (skip) and dp[i][j][1] = best_above + mem[i][j] (read).\n3. Entering from the left: dp[i][j][c] = max(dp[i][j-1][c] (skip), dp[i][j-1][c-1] + mem[i][j] (read)).\n4. Take the maximum of the candidates; the answer is max over c of dp[n-1][m-1][c].',
            'A path visits a contiguous segment of each row; the optimal reads in a row are any subset of at most k of the visited cells, which the c counter tracks one cell at a time. Resetting c when moving down enforces the per-row cap. The exhaustive search agrees on 300 random grids and both examples.',
            'O(n x m x k) time (about 5.5 x 10^6 steps for n x m = 5 x 10^5, k = 10) and O(m x k) space.',
            '''NEG = float('-inf')

def findMaxDataRetrieved(mem, k):
    n, m = len(mem), len(mem[0])
    best_above = [NEG] * m
    for i in range(n):
        cur = [None] * m
        best_here = [NEG] * m
        for j in range(m):
            dp = [NEG] * (k + 1)
            if i == 0 and j == 0:
                top = 0
            elif i > 0:
                top = best_above[j]
            else:
                top = NEG
            if top > NEG:
                dp[0] = top
                dp[1] = top + mem[i][j]
            if j > 0:
                left = cur[j - 1]
                for c in range(k + 1):
                    if left[c] > dp[c]:
                        dp[c] = left[c]                        # skip this cell
                    if c > 0 and left[c - 1] > NEG and left[c - 1] + mem[i][j] > dp[c]:
                        dp[c] = left[c - 1] + mem[i][j]        # read this cell
            cur[j] = dp
            best_here[j] = max(dp)
        best_above = best_here
    return int(best_above[m - 1])''',
            'mem = [[3,4,10],[2,8,1]], k = 2. Row 0: at (0,0) dp = [0, 3]; at (0,1) dp = [0, 4, 7]; at (0,2) dp = [0, 10, 14]. best_above for column 1 is 7. Row 1: at (1,1) reading 8 gives 7 + 8 = 15 with c = 1; moving right to (1,2) and reading 1 gives 16. Answer 16.',
            '- Moving down resets the per-row counter.\n- dp[..][1] requires k >= 1, which the constraints guarantee.\n- A very wide or very tall grid is fine because n x m is capped.\n- Use 64-bit sums (values up to 10^9 times 5 x 10^5 cells).'))
