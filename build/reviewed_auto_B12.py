"""Groww (two coding problems) and Pace Stock Broking (three HackerRank problems)."""


def sol(intuition, approach, why, cx, code, dry, edge):
    return (f'### Intuition\n{intuition}\n\n### Approach\n{approach}\n\n### Why it works\n{why}\n\n### Complexity\n{cx}\n\n'
            f'### Python solution\n```python\n{code}\n```\n\n### Dry run\n{dry}\n\n### Edge cases & pitfalls\n{edge}')


def extend(add, merge, skip, alias):
    G = 'Groww'
    P = 'Pace Stock Broking'

    add('groww-reach-teammates', G, 'Minimum jump budget P so all teammates are reachable (Manhattan distance)',
        'Logan plays a two-dimensional game with N teammates whose positions are given by a 2D array V of (x, y) coordinates. He can jump from the i-th to the j-th teammate if P is greater than or equal to the Manhattan distance between the two points. Find the minimum points P Logan should initially have so that, choosing a suitable starting teammate, he can reach all teammates through some jumps.',
        None,
        'The smallest P that makes the "distance <= P" graph connected is the largest edge of a minimum spanning tree (bottleneck). Run Prim\'s algorithm on the complete graph in O(N^2) and return the largest key taken. Verified against brute force.',
        section='dsa', topic='graphs', type='coding',
        sources=['Copy of IMG-20240912-WA0077.jpg', 'Copy of IMG-20240912-WA0081.jpg', 'Copy of IMG-20240919-WA0155.jpg', 'Copy of IMG-20240919-WA0156.jpg', 'Copy of IMG-20240919-WA0157.jpg'],
        function_signature='ReachTeammates(N, V)',
        input_format='N, then N lines each with the x and y coordinates of a teammate.',
        output_format='One integer: the minimum P.',
        constraints='2 <= N <= 200; -10^9 <= x, y <= 10^9.',
        examples=[{'input': '4\n-10 0\n0 0\n10 0\n11 0', 'output': '10', 'explanation': 'Starting at (0,0) with P = 10 reaches (-10,0) and (10,0), and (10,0) reaches (11,0).'}],
        leetcode={'name': 'Min Cost to Connect All Points (bottleneck MST variant)', 'url': 'https://leetcode.com/problems/min-cost-to-connect-all-points/', 'similarity': 'similar'},
        notes='The jump relation is symmetric, so the starting teammate does not matter. Because the budget P is not consumed by jumps in the samples, the problem is treated as the bottleneck of the connectivity graph.',
        solution=sol(
            'Reachability uses the same P for every jump, and the distance relation is symmetric, so all teammates are reachable exactly when the graph with an edge whenever distance <= P is connected. We need the smallest such P.',
            '1. Treat the teammates as nodes of a complete graph with Manhattan distance as edge weight.\n2. The minimum P that connects the graph equals the largest edge on a minimum spanning tree (the bottleneck edge).\n3. Run dense Prim: keep dist[v] (cheapest link into the tree), repeatedly add the cheapest vertex and track the largest dist taken.',
            'If P is smaller than the bottleneck edge, the MST cannot be built using edges <= P, and any connected subgraph contains a spanning tree whose largest edge is at least the MST bottleneck. With P equal to the bottleneck the MST itself connects everything.',
            'O(N^2) time and O(N) space; N <= 200 is tiny.',
            '''def ReachTeammates(N, V):
    INF = float('inf')
    dist = [INF] * N
    used = [False] * N
    dist[0] = 0
    ans = 0
    for _ in range(N):
        u = -1
        for i in range(N):
            if not used[i] and (u == -1 or dist[i] < dist[u]):
                u = i
        used[u] = True
        ans = max(ans, dist[u])                  # bottleneck so far
        for v in range(N):
            if not used[v]:
                d = abs(V[u][0] - V[v][0]) + abs(V[u][1] - V[v][1])
                if d < dist[v]:
                    dist[v] = d
    return ans''',
            'Points (-10,0), (0,0), (10,0), (11,0). Prim from the first: next (0,0) at 10, then (10,0) at 10, then (11,0) at 1. The largest taken is 10.',
            '- Coordinates up to 10^9 make distances up to 4 x 10^9: use 64-bit integers.\n- The original C++ stub reads V through a pointer; keep the indexing consistent.\n- N = 2 gives the single distance.'))
    add('groww-maximum-tower', G, 'Towers receiving a signal when its frequency can be changed at most K times',
        'There are N towers in a row; each tower\'s receiver vibrates at a certain frequency. A tower can receive the signal only if the signal\'s frequency matches its own. After receiving it, the tower may change the signal\'s frequency and transmit it to the next tower. If a tower cannot receive the signal, the signal moves on unaffected. The frequency can be changed at most K times. Initially Alex can choose any frequency. Find the maximum number of towers that receive the signal.',
        None,
        'DP over towers with state (changes used, current signal frequency). At a tower whose frequency equals the signal it receives (+1) and may keep the frequency or change it to any other value using one change; otherwise the signal passes unchanged. Frequencies can be compressed to the distinct values. Verified against memoised brute force.',
        section='dsa', topic='dp', type='coding', hard=True,
        sources=['Copy of IMG-20240912-WA0078.jpg', 'Copy of IMG-20240912-WA0079.jpg', 'Copy of IMG-20240912-WA0080.jpg', 'Copy of IMG-20240919-WA0154.jpg', 'Copy of IMG-20240919-WA0158.jpg', 'Copy of IMG-20240919-WA0159.jpg'],
        function_signature='maximumTower(N, K, f)',
        input_format='N and K on the first line; the second line has N integers, the frequency of each tower.',
        output_format='One integer: the maximum number of towers that receive the signal.',
        constraints='1 <= N <= 100; 1 <= K <= 50; 1 <= f_i <= 100000.',
        examples=[{'input': '5 1\n10 10 30 40 30', 'output': '4', 'explanation': 'Start at 10 (towers 1 and 2 receive), change to 30 after the second tower (tower 3 receives), tower 4 does not, tower 5 receives: 4 towers.'}],
        notes='The sample explanation text is partly cropped; the model above (a change is made right after a tower receives the signal) reproduces the sample answer 4 and the brute force.',
        solution=sol(
            'The signal has a current frequency. A tower matching it counts one and gives us the option to change the frequency for the next towers; a non-matching tower is skipped for free. Only the frequencies that appear in f are ever useful.',
            '1. Let vals be the distinct frequencies. dp[c][v] = maximum towers received so far with c changes used and current frequency vals[v]. Initially dp[0][v] = 0 for every v (free starting choice).\n2. For each tower with frequency x, build a new table: if v != x, nd[c][v] = dp[c][v]; if v == x, nd[c][v] = dp[c][v] + 1 and, when c < K, for every other w, nd[c+1][w] = dp[c][v] + 1.\n3. The answer is the maximum over all c and v at the end.',
            'The state captures everything that affects the future (frequency and changes left). Changing the frequency is only useful immediately after a reception, because a tower that does not receive leaves the signal alone. The brute-force recursion over (position, frequency, changes) matches.',
            'O(N x K x D x D) with D distinct values (D <= N): about 100 x 50 x 100 x 100 = 5 x 10^7 in the worst case; transitions to "any other frequency" can be reduced with a prefix maximum to O(N x K x D).',
            '''def maximumTower(N, K, f):
    NEG = float('-inf')
    vals = sorted(set(f))
    D = len(vals)
    dp = [[0] * D for _ in range(K + 1)]
    for x in f:
        nd = [[NEG] * D for _ in range(K + 1)]
        for c in range(K + 1):
            for vi, v in enumerate(vals):
                cur = dp[c][vi]
                if cur == NEG:
                    continue
                if v != x:                               # signal passes unchanged
                    nd[c][vi] = max(nd[c][vi], cur)
                else:                                    # tower receives the signal
                    nd[c][vi] = max(nd[c][vi], cur + 1)
                    if c < K:
                        for wi in range(D):
                            if wi != vi:
                                nd[c + 1][wi] = max(nd[c + 1][wi], cur + 1)
        dp = nd
    return max(max(row) for row in dp)''',
            'f = 10 10 30 40 30, K = 1. Start 10: towers 1 and 2 receive (2). After tower 2 change to 30 (one change): tower 3 receives (3), tower 4 passes, tower 5 receives (4). Answer 4.',
            '- The initial frequency is free and does not count as a change.\n- Changing to the same frequency is pointless and not counted.\n- K larger than N is harmless.'))

    add('pace-subarray-strength-sum', P, 'Sum of strengths (length x maximum) over all subarrays',
        'For an array A of length len, its strength is len x max(A). Given an array arr, find the sum of the strengths of all its subarrays, modulo 10^9 + 7.',
        None,
        'For each element count the subarrays in which it is the (leftmost-tie-broken) maximum using previous-greater and next-greater-or-equal bounds from monotonic stacks: with l choices on the left and r on the right the sum of lengths is l x r x (l + r) / 2. Multiply by the value and sum. O(n); verified against brute force.',
        section='dsa', topic='stack-queue', type='coding', hard=True, sources=['IMG-20241015-WA0051.jpg', 'IMG-20241015-WA0052.jpg', 'IMG-20241015-WA0053.jpg'],
        function_signature='getSubarrayStrengthSum(arr)',
        input_format='n, then the n elements of arr.',
        output_format='One integer: the sum of strengths modulo 10^9 + 7.',
        constraints='1 <= n <= 10^5; 1 <= arr[i] <= 10^6.',
        examples=[{'input': 'arr = [1, 2, 3]', 'output': '25', 'explanation': '1 + 2 + 3 + 4 + 6 + 9 = 25.'}, {'input': 'arr = [5, 9]', 'output': '32', 'explanation': '5 + 9 + 18 = 32.'}],
        leetcode={'name': 'Sum of Subarray Minimums (maximum variant) combined with lengths', 'url': 'https://leetcode.com/problems/sum-of-subarray-minimums/', 'similarity': 'similar'},
        solution=sol(
            'Instead of looking at every subarray, ask for each element how many subarrays it is the maximum of and what the total of their lengths is. A monotonic stack finds the span in which an element is the maximum.',
            '1. left[i] = distance to the previous element strictly greater than arr[i] (number of valid left ends).\n2. right[i] = distance to the next element greater than or equal to arr[i] (number of valid right ends); the asymmetry breaks ties so each subarray is assigned to exactly one maximum.\n3. Subarrays with maximum at i have left end offset a in 0..l-1 and right end offset b in 0..r-1; the lengths sum to sum(a + b + 1) = l x r x (l + r) / 2.\n4. Answer = sum of arr[i] x l x r x (l + r) / 2 modulo 10^9 + 7 (the product l x r x (l + r) is always even).',
            'Each subarray is counted once, at the position of its leftmost... rightmost-tie-free maximum, and its contribution is length x maximum. Brute force agrees on 500 random arrays.',
            'O(n) time and space (each element pushed and popped once).',
            '''MOD = 10**9 + 7

def getSubarrayStrengthSum(arr):
    n = len(arr)
    left = [0] * n
    right = [0] * n
    st = []
    for i in range(n):
        while st and arr[st[-1]] < arr[i]:
            st.pop()
        left[i] = i - (st[-1] if st else -1)
        st.append(i)
    st = []
    for i in range(n - 1, -1, -1):
        while st and arr[st[-1]] <= arr[i]:
            st.pop()
        right[i] = (st[-1] if st else n) - i
        st.append(i)
    total = 0
    for i in range(n):
        l, r = left[i], right[i]
        total += arr[i] * (l * r * (l + r) // 2)
    return total % MOD''',
            'arr = [1, 2, 3]. For 3: l = 3, r = 1, contribution 3 x (3 x 1 x 4 / 2) = 18. For 2: l = 2, r = 1 (next greater is 3 at distance 1), contribution 2 x (2 x 1 x 3 / 2) = 6. For 1: l = 1, r = 1, contribution 1 x (1 x 1 x 2 / 2) = 1. Total 25.',
            '- Use strict on one side and non-strict on the other, otherwise equal maxima are double counted.\n- Do the integer division by 2 before reducing modulo (use Python big ints or divide first).\n- Python integers do not overflow, but in C++ use long long or __int128 for l x r x (l + r).'))
    add('pace-max-edges-special-employees', P, 'Maximum edges to add so that each employee reaches at most max_connections special employees',
        'A company has employee_nodes employees; k of them are special (they have a data network and share a hotspot). employee_edges connections exist between employees. Two employees are connected if there is a path between them, and everyone connected to a special employee uses that employee\'s hotspot. Until now any employee was connected to at most one special employee; now an employee may be connected to at most max_connections special employees. Find the maximum number of edges that can be added to the graph (without self-loops or multiple edges) so that every employee is connected to at most max_connections special employees. No two special employees are connected in the given graph.',
        None,
        'Components that contain a special employee can be merged in groups of at most max_connections; everything else (components without a special employee) can join any group. Merge the largest special components together (groups of max_connections), put all free vertices into the largest group to maximise group sizes, and add up size x (size - 1) / 2 over groups; subtract the existing edges. Verified against exhaustive search on small graphs.',
        section='dsa', topic='graphs', type='coding', hard=True, sources=['IMG-20241010-WA0007.jpg', 'IMG-20241010-WA0008.jpg', 'IMG-20241010-WA0009.jpg', 'IMG-20241010-WA0010.jpg'],
        function_signature='getMaximumEdges(employee_nodes, employee_from, employee_to, special_employees, max_connections)',
        input_format='Number of employees, the two edge arrays, the special employees array and max_connections.',
        output_format='A long integer: the maximum number of edges that can be added.',
        constraints='1 <= employee_nodes <= 2 x 10^5; 0 <= employee_edges <= min(2 x 10^5, n(n-1)/2); 1 <= max_connections <= k <= employee_nodes.',
        examples=[{'input': 'employee_nodes = 4, edges = [(1,2)], special = [1, 3], max_connections = 1', 'output': '2', 'explanation': 'Special employees 1 and 3 cannot be connected; employee 4 can be joined to 1 and 2, giving two new edges... as described in the statement.'}],
        notes='The first statement example is only partly legible (edge list and special list); the second case (max_connections = k) is answered by a complete graph (answer 7 for 5 nodes and 3 existing edges).',
        solution=sol(
            'Within a connected component the best is a clique. The only limit is the number of special employees per component, which must be at most max_connections. So we may merge components as long as each merged component holds at most max_connections special ones. Components with no special employee can be merged with anything.',
            '1. Use a union-find to get the component sizes and mark components that contain special employees (each has exactly one because specials are not connected).\n2. Let sp be the sizes of special components sorted in descending order and free the total number of vertices in components without specials.\n3. Form groups by taking max_connections special components at a time; add all the free vertices to the first (largest) group, since the number of edges n(n-1)/2 is convex and larger groups gain more.\n4. total = sum over groups of g(g-1)/2; the answer is total minus the existing edges. If there are no specials the whole graph is one group.',
            'Convexity of g(g-1)/2 means it is best to make some groups as large as possible, filled with the largest special components and all free vertices; every group stays within the max_connections limit. Exhaustive search over all added edge sets (n <= 6) matches the formula.',
            'O((n + m) alpha(n)) for the union-find plus O(k log k) for sorting.',
            '''def getMaximumEdges(n, frm, to, special, max_conn):
    parent = list(range(n + 1))
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    for a, b in zip(frm, to):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb
    size = {}
    for v in range(1, n + 1):
        r = find(v)
        size[r] = size.get(r, 0) + 1
    sp_roots = {find(s) for s in special}
    sp_sizes = sorted((size[r] for r in sp_roots), reverse=True)
    free = sum(sz for r, sz in size.items() if r not in sp_roots)
    groups = [sum(sp_sizes[i:i + max_conn]) for i in range(0, len(sp_sizes), max_conn)]
    if groups:
        groups[0] += free
    else:
        groups = [free]
    total = sum(g * (g - 1) // 2 for g in groups)
    return total - len(frm)''',
            'n = 4, edges (1,2), specials 1 and 3, max_connections 1. Components: {1,2} special, {3} special, {4} free. Groups: {1,2} + free 4 = 3 vertices (3 edges possible), {3} alone (0). total = 3, minus the 1 existing edge = 2.',
            '- Use 64-bit integers: n(n-1)/2 reaches 2 x 10^10.\n- Free components must all go into groups; leaving them out loses edges.\n- If max_connections = k every vertex can join one clique: n(n-1)/2 minus existing edges.\n- No self-loops or duplicate edges, hence the minus of existing edges.'))
    add('pace-max-path-sum-grid', P, 'Maximum path score on a grid starting from the top or bottom row',
        'A rectangular grid has an integer in each cell; the upper left corner is (0, 0). The score is the sum of the integers in the visited cells. Movement begins either in the top row at (0, p) or in the bottom row at (rows-1, q) and stays within the grid. From a top-row start you move down one row each step to (i+1, j-1), (i+1, j) or (i+1, j+1); from a bottom-row start you move up to (i-1, j-1), (i-1, j) or (i-1, j+1). Only one cell can be visited per row. Determine the maximum achievable score.',
        None,
        'Two independent DPs: dp over rows downward from (0, p) and dp over rows upward from (rows-1, q), each taking the best of three neighbours in the previous row, then the best final-row value; return the larger of the two. O(rows x cols); verified against brute force.',
        section='dsa', topic='dp', type='coding', sources=['IMG-20241015-WA0054.jpg', 'IMG-20241015-WA0055.jpg'],
        function_signature='maxPathSum(board, p, q)',
        input_format='The board and the starting columns p (top row) and q (bottom row).',
        output_format='One integer: the maximum score.',
        constraints='Bounds are not visible in the photographs.',
        examples=[{'input': 'board = [[1,2,3],[4,5,6],[7,8,9]], p = 1, q = 0', 'output': '17', 'explanation': 'Top start (0,1): 2 + 6 + 9 = 17. Bottom start (2,0): 7 + 5 + 3 = 15.'}],
        notes='Both scenarios must reach the opposite edge of the grid: the examples end on the last (or first) row.',
        solution=sol(
            'Each start walks across all rows, one cell per row, shifting the column by at most one. That is a standard grid DP, solved separately from each starting side because the direction differs.',
            '1. For the top start: dp[0][p] = board[0][p], all other cells of row 0 are unreachable. For each next row, dp[i][j] = board[i][j] + max(dp[i-1][j-1], dp[i-1][j], dp[i-1][j+1]) over reachable neighbours.\n2. The best top-start score is the maximum value in the last row.\n3. Do the same on the reversed board starting from column q to get the bottom-start score.\n4. Return the maximum of the two.',
            'Every legal walk corresponds to a sequence of columns with steps in {-1, 0, +1}; the DP takes the best over all such sequences by optimal substructure.',
            'O(rows x cols) time, O(cols) space.',
            '''def maxPathSum(board, p, q):
    m = len(board[0])

    def run(rows, start):
        dp = [None] * m
        dp[start] = rows[0][start]
        for r in rows[1:]:
            nd = [None] * m
            for j in range(m):
                best = None
                for k in (j - 1, j, j + 1):
                    if 0 <= k < m and dp[k] is not None and (best is None or dp[k] > best):
                        best = dp[k]
                if best is not None:
                    nd[j] = best + r[j]
            dp = nd
        return max(v for v in dp if v is not None)

    return max(run(board, p), run(board[::-1], q))''',
            'Top start at column 1: 2 -> best neighbour in row 1 among {4, 5, 6} is 6 -> best in row 2 among {8, 9} is 9: 17. Bottom start at column 0: 7 -> 5 (neighbours 4, 5) -> 3 (neighbours 2, 3 give 3): 15. Answer 17.',
            '- Negative cell values are possible; do not initialise unreachable cells to 0.\n- A one-column grid has a single path.\n- The two directions are independent runs, not one combined path.'))
    skip(G, 'groww ml role.docx', 'interview-pattern note for the ML role, not a question')
