"""Deutsche Bank online assessments: five coding problems (HackerRank-style) and the October OA document."""


def sol(intuition, approach, why, cx, code, dry, edge):
    return (f'### Intuition\n{intuition}\n\n### Approach\n{approach}\n\n### Why it works\n{why}\n\n### Complexity\n{cx}\n\n'
            f'### Python solution\n```python\n{code}\n```\n\n### Dry run\n{dry}\n\n### Edge cases & pitfalls\n{edge}')


def extend(add, merge, skip, alias):
    D = 'Deutsche Bank'

    def w(*ns):
        return [f'IMG-20240907-WA{n:04d}.jpg' for n in ns]

    add('db-black-white-tree-beauty', D, 'Black and white tree: beauty of every vertex',
        'Given a tree with N vertices labelled 1 to N, rooted at vertex 1, with N-1 undirected edges. Each vertex i is coloured white (0) or black (1). The beauty of a vertex i is the number of paths in its subtree that have end vertices of opposite colours. Find the beauty of all N vertices. (The subtree of i is the connected subgraph of all descendants of i including i.)',
        None,
        'A path with end vertices of different colours is a pair (white vertex, black vertex) in the subtree, and in a tree each pair defines exactly one path. So beauty(v) = whites in subtree x blacks in subtree. Compute subtree colour counts bottom-up with an iterative DFS. O(N).',
        section='dsa', topic='trees', type='coding', sources=w(113, 114, 115),
        function_signature='solve(N, Color, Edges)',
        input_format='N; then the string Color of length N of 0/1 characters; then N-1 lines with the two endpoints of each edge.',
        output_format='N space-separated integers: the beauty of vertices 1 to N.',
        constraints='1 <= N <= 10^5; Color[i] in {0, 1}; 1 <= a_i, b_i <= N.',
        examples=[{'input': '5\n11110\n3 1\n4 3\n5 3\n2 4', 'output': '4 0 3 0 0', 'explanation': 'Vertex 5 is the only white vertex. Vertex 1 sees 4 black vertices, vertex 3 sees 3 (1 is outside its subtree).'}],
        solution=sol(
            'Between any two vertices of a tree there is exactly one simple path, so counting paths with opposite-coloured ends is the same as counting pairs (white vertex, black vertex) inside the subtree.',
            '1. Build the adjacency list and run an iterative DFS from vertex 1 to get a parent array and a visiting order.\n2. Process vertices in reverse order (children before parents). For each vertex, start its counts with its own colour and add the counts of its children by adding the vertex counts into its parent.\n3. beauty(v) = white[v] x black[v].',
            'Each unordered pair of vertices in the subtree of v corresponds to exactly one path inside the subtree, and the pair has opposite colours exactly when one is white and the other black, giving white x black pairs.',
            'O(N) time and O(N) space.',
            '''def solve(N, color, edges):
    adj = [[] for _ in range(N + 1)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    parent = [0] * (N + 1)
    parent[1] = -1
    order, stack = [], [1]
    while stack:                                   # iterative DFS from the root
        u = stack.pop()
        order.append(u)
        for v in adj[u]:
            if v != parent[u]:
                parent[v] = u
                stack.append(v)
    white = [0] * (N + 1)
    black = [0] * (N + 1)
    for u in reversed(order):                      # children before parents
        if color[u - 1] == '0':
            white[u] += 1
        else:
            black[u] += 1
        if parent[u] > 0:
            white[parent[u]] += white[u]
            black[parent[u]] += black[u]
    return [white[u] * black[u] for u in range(1, N + 1)]''',
            'Colours "11110": only vertex 5 is white. Subtree of 1 is the whole tree: 1 white, 4 black, beauty 4. Subtree of 3 is {3, 4, 5, 2}: 1 white, 3 black, beauty 3. Subtrees of 2, 4, 5 contain no mixed colours that form a pair: 4 holds {4, 2} both black -> 0, vertex 5 alone -> 0, vertex 2 alone -> 0. Output 4 0 3 0 0.',
            '- Beauty counts unordered pairs; do not double it.\n- N = 10^5 can create a path-like tree: use an iterative DFS, not recursion.\n- The answer can reach about N^2 / 4 = 2.5 x 10^9, so use 64-bit integers.\n- The tree is rooted at 1 even though the edges are undirected.'))
    add('db-window-rightmost-most-prime-factors', D, 'Minimum over windows of the rightmost number with the most distinct prime factors',
        'For a given integer x and an array a of size n, for each window of x consecutive elements define fun(window) as the rightmost number in the window with the highest number of distinct prime factors. If m_i = fun(a_i, a_{i+1}, ..., a_{i+x-1}) for each valid i, compute min(m_i) over all windows.',
        None,
        'Sieve the number of distinct prime factors omega up to max(a). Slide a monotonic deque that keeps indices with strictly decreasing omega (popping when omega is <=, so the rightmost wins ties); the front is the window answer. Track the minimum. O(max log log max + n); verified against brute force.',
        section='dsa', topic='sliding-window', type='coding', sources=w(116, 118, 119, 120, 121, 122),
        function_signature='solve(x, n, a)',
        input_format='First line: x and n. Second line: n integers a_1..a_n.',
        output_format='One integer: the value of the expression.',
        constraints='1 <= n <= 10^6; 1 <= x <= n; 0 <= a_i <= 10^6.',
        examples=[{'input': '3 5\n2 4 6 10 5', 'output': '6', 'explanation': 'm_1 = fun(2,4,6) = 6, m_2 = fun(4,6,10) = 10, m_3 = fun(6,10,5) = 10; the minimum is 6.'}],
        notes='The sample is fully visible; a_i = 0 is treated as having 0 prime factors (an assumption since the statement does not define it).',
        solution=sol(
            'It is a sliding-window maximum, but the key is the number of distinct prime factors, and ties go to the rightmost element. A monotonic deque gives each window\'s answer in amortised O(1).',
            '1. Build omega[v] (number of distinct primes dividing v) with a sieve up to the largest value: for each prime p, add 1 to omega of all its multiples.\n2. Keep a deque of indices whose omega values are strictly decreasing from front to back. For a new index i, pop from the back while omega[a[back]] <= omega[a[i]] (<= so a later equal element replaces an earlier one), then push i.\n3. Drop the front if it left the window (index <= i - x).\n4. Once i >= x - 1 the front is the answer for the window: a[front]. Keep the minimum of these values.',
            'The deque front is always the element with the maximum omega in the window and, among equal omega, the rightmost one because equal earlier elements were popped. The brute force confirms the rule on 300 random arrays.',
            'O(M log log M + n) time with M = max(a); O(M + n) space.',
            '''from collections import deque

def solve(x, n, a):
    top = max(a) if a else 0
    omega = [0] * (top + 1)
    for p in range(2, top + 1):
        if omega[p] == 0:                          # p is prime
            for m in range(p, top + 1, p):
                omega[m] += 1
    dq = deque()
    best = None
    for i in range(n):
        while dq and omega[a[dq[-1]]] <= omega[a[i]]:
            dq.pop()
        dq.append(i)
        if dq[0] <= i - x:
            dq.popleft()
        if i >= x - 1:
            v = a[dq[0]]
            best = v if best is None else min(best, v)
    return best''',
            'a = 2 4 6 10 5, x = 3. omega: 2->1, 4->1, 6->2, 10->2, 5->1. Window [2,4,6] -> 6; window [4,6,10] -> omega tie between 6 and 10, rightmost is 10; window [6,10,5] -> 10. Minimum of 6, 10, 10 is 6.',
            '- Ties go to the rightmost element: pop with <=, not <.\n- A value of 1 (and 0) has 0 distinct prime factors.\n- n up to 10^6 needs fast input; the sieve is run once.\n- If x = 1 each element is its own window and the answer is min(a).'))
    add('db-min-required-k-debugging', D, 'Debugging: minimum K non-adjacent elements of B so that the OR-sum reaches M',
        'You are given two arrays A and B of size N of non-negative integers. You have to select K numbers from B (no two adjacent elements of B may be chosen). For each chosen number, take its bitwise OR with every element of A and add all those results to a sum. Find the minimum K such that the sum is greater than or equal to M, or print -1 if it is impossible. (The original task supplies buggy code that must be fixed so that all test cases pass.)',
        None,
        'Each B[i] has a fixed value val[i] = sum over a of (a OR B[i]). The task becomes: choose the fewest non-adjacent indices whose values sum to at least M. A DP dp[i][k] = best total using k non-adjacent items among the first i, then the smallest k with dp >= M. val is computed in O(N x 30) from bit counts of A. Verified against brute force.',
        section='dsa', topic='dp', type='coding', hard=True, sources=w(117, 123, 124, 127),
        function_signature='MinReq(N, A, B, M)',
        input_format='T test cases. Each: N, then M (partly cropped), then arrays A and B.',
        output_format='For each test case print the minimum K (or -1), one per line.',
        constraints='1 <= T <= 10; 1 <= N <= 10^3 (as printed); 0 <= A_i, B_i <= 10^9; 0 <= M <= 10^18.',
        examples=[{'input': 'A = [1,2,3,4,5], B = [2,2,2,2,2], M = 40', 'output': '2', 'explanation': 'One chosen 2 gives 3+2+3+6+7 = 21; two chosen 2s give 42 >= 40.'}],
        notes='The buggy starter code and the exact input order of the samples are not fully visible; the statement and worked example were used. M = 0 needs K = 0.',
        solution=sol(
            'Each element of B contributes a fixed amount to the sum, independent of the other choices: val[j] = sum over i of (A[i] OR B[j]). The adjacency rule then turns the question into picking non-adjacent items with the fewest items reaching a target sum.',
            '1. Count how many elements of A have each bit set: cnt[b].\n2. a OR b = a + b - (a AND b), so val[j] = sumA + N x B[j] - sum over set bits t of B[j] of cnt[t] x 2^t.\n3. DP over positions: dp[i][k] = maximum sum using exactly k chosen items among the first i with no two adjacent; dp[i][k] = max(dp[i-1][k], dp[i-2][k-1] + val[i]).\n4. The answer is the smallest k with dp[N][k] >= M (k = 0 if M = 0), else -1.',
            'Values are positive and independent, so for a fixed k the best choice maximises the total; the first k whose maximum reaches M is the minimum number of picks. Brute force over all non-adjacent subsets agrees on 300 random cases and the worked example.',
            'O(N x 30) to compute the values and O(N x N/2) for the DP (at most about 5 x 10^5 steps for N = 10^3).',
            '''def MinReq(N, A, B, M):
    if M == 0:
        return 0
    sumA = sum(A)
    cnt = [sum(1 for a in A if a >> b & 1) for b in range(31)]
    val = []
    for b in B:
        and_sum = sum((1 << bit) * cnt[bit] for bit in range(31) if b >> bit & 1)
        val.append(sumA + N * b - and_sum)         # sum of (a | b) over all a in A
    NEG = float('-inf')
    maxK = (N + 1) // 2
    dp2 = [0] + [NEG] * maxK                       # dp[i-2]
    dp1 = [0] + [NEG] * maxK                       # dp[i-1]
    for i in range(1, N + 1):
        cur = dp1[:]
        for k in range(1, maxK + 1):
            if dp2[k - 1] > NEG:
                cur[k] = max(cur[k], dp2[k - 1] + val[i - 1])
        dp2, dp1 = dp1, cur
    for k in range(maxK + 1):
        if dp1[k] >= M:
            return k
    return -1''',
            'A = [1,2,3,4,5], B = [2,2,2,2,2]. Each val = (1|2)+(2|2)+(3|2)+(4|2)+(5|2) = 3+2+3+6+7 = 21. Non-adjacent picks: k = 1 -> 21, k = 2 -> 42, k = 3 -> 63. First k with sum >= 40 is 2.',
            '- Use 64-bit integers: val can reach about 10^3 x 2 x 10^9 and sums up to 10^12 (M up to 10^18).\n- The maximum number of non-adjacent items is ceil(N / 2).\n- M = 0 gives 0 without choosing anything.\n- Do not sort B: positions matter because of the adjacency rule.'))
    add('db-lexicographically-smallest-by-weight', D, 'Lexicographically smallest string using swaps between equal-weight positions',
        'You are given a string s and an integer array arr where arr[i] is the weight of the character at index i (1-based). You may swap two characters of the string if they have the same weight (arr[i] = arr[j]) any number of times. Return the lexicographically smallest string that can be formed.',
        None,
        'Positions with the same weight can be permuted arbitrarily (any two can swap directly). Group the positions by weight, sort the group\'s characters and write them back into that group\'s positions in increasing index order. O(N log N); verified against exhaustive swapping.',
        section='dsa', topic='sorting', type='coding', sources=['Deutsche Bank OA 14th October.pdf'],
        function_signature='smallest(s, arr)',
        input_format='A string s of length N and an integer array arr of length N.',
        output_format='The lexicographically smallest string.',
        constraints='1 <= N <= 2000; 1 <= arr[i] <= 10^4; s has lowercase letters only.',
        examples=[{'input': 's = "xvrb", arr = [2, 1, 2, 2]', 'output': 'bvrx', 'explanation': 'x, r, b share weight 2 and are sorted into positions 1, 3, 4; v stays.'}],
        solution=sol(
            'Because any two equal-weight positions can swap directly, every weight class is fully connected: any permutation of its characters is reachable. Classes never interact.',
            '1. Map each weight to the list of indices that have it.\n2. For each weight, collect the characters at those indices, sort them, and place them back in increasing index order.\n3. Join the result.',
            'Within a class the smallest possible assignment gives the smallest character to the earliest index; since classes do not exchange characters, minimising each class independently minimises the whole string lexicographically.',
            'O(N log N) time, O(N) space.',
            '''from collections import defaultdict

def smallest(s, arr):
    pos = defaultdict(list)
    for i, w in enumerate(arr):
        pos[w].append(i)
    res = list(s)
    for idx in pos.values():
        for i, ch in zip(idx, sorted(s[i] for i in idx)):
            res[i] = ch
    return ''.join(res)''',
            's = xvrb, weights 2 1 2 2. Weight 2 has indices 0, 2, 3 with letters x, r, b -> sorted b, r, x placed at 0, 2, 3. Weight 1 keeps v at index 1. Result b v r x.',
            '- Indices are 1-based in the statement, 0-based in code.\n- A weight that occurs once leaves its character unchanged.\n- Do not sort the whole string; only within each weight class.'))
    add('db-minimum-price-stones', D, 'Minimum price to collect all N types of stones with cyclic type shifts',
        'There are N stones in a line. The cost and type of the i-th stone are a_i units and i respectively. You start with no stones and want to collect all N types. You can perform an operation that changes the type of every stone from i to i+1 (type N becomes 1); each operation costs x units. Find the minimum total price to collect all N types of stones.',
        None,
        'After k operations the stone at index j has type j + k (mod N). So type t can be bought at any of the k+1 indices t, t-1, ..., t-k. For each k the cost is k x x + sum over types of the minimum price among those k+1 indices. Keep a running minimum array while k grows. O(N^2).',
        section='dsa', topic='greedy', type='coding', sources=['Deutsche Bank OA 14th October.pdf'],
        function_signature='minPrice(N, x, a)',
        input_format='First line: N and x. Second line: N prices.',
        output_format='A single integer: the minimum price.',
        constraints='1 < N <= 2000; 0 < x <= 10^9; 1 <= a[i] <= 10^9.',
        examples=[{'input': '3 5\n50 1 50', 'output': '13', 'explanation': 'Buy the cheap stone (1) three times with two shifts (5 each): 1 + 5 + 1 + 5 + 1 = 13.'}],
        leetcode={'name': 'Collecting Chocolates', 'url': 'https://leetcode.com/problems/collecting-chocolates/', 'similarity': 'same'},
        solution=sol(
            'Operations shift every type by one position together. After k shifts, the cheapest way to own type t is the cheapest of the prices at the k + 1 positions that held type t at some moment (positions t, t-1, ..., t-k, taken cyclically). More shifts cost more but lower the per-type minimum.',
            '1. Let cur[t] be the cheapest price known for type t, initially a[t] (k = 0).\n2. For k = 0..N-1: if k > 0, update cur[t] = min(cur[t], a[(t - k) % N]) for every t. Total(k) = k x x + sum(cur).\n3. The answer is the minimum Total(k) over k. Shifting N or more times is never useful because all positions have already been seen.',
            'For a fixed number k of shifts, buying a type is possible at exactly the positions seen in the k + 1 states; choosing the cheapest for each type independently is optimal because purchases do not interact.',
            'O(N^2) time (N <= 2000 gives 4 x 10^6 steps), O(N) space.',
            '''def minPrice(N, x, a):
    cur = a[:]                                     # cheapest price seen for each type
    best = sum(cur)                                # k = 0
    for k in range(1, N):
        for t in range(N):
            cand = a[(t - k) % N]
            if cand < cur[t]:
                cur[t] = cand
        best = min(best, k * x + sum(cur))
    return best''',
            'a = 50 1 50, x = 5. k = 0: 101. k = 1: cur becomes [50, 1, 1]... updating with a[t-1]: t=0 -> a[2] = 50 (stays 50), t=1 -> a[0] = 50 (stays 1), t=2 -> a[1] = 1 -> 1; total 5 + 52 = 57. k = 2: t=0 -> a[1] = 1; total 10 + 3 = 13. Best 13.',
            '- x can be 10^9 and prices 10^9, so totals reach about 2000 x 10^9 x 2: use 64-bit integers.\n- Do not run more than N - 1 shifts.\n- The recomputation sum(cur) inside the loop is O(N), keeping the whole thing O(N^2).'))
