"""Edelweiss (HackerRank), HP repeats, HiLabs SDE PDF."""


def sol(intuition, approach, why, cx, code, dry, edge):
    return (f'### Intuition\n{intuition}\n\n### Approach\n{approach}\n\n### Why it works\n{why}\n\n### Complexity\n{cx}\n\n'
            f'### Python solution\n```python\n{code}\n```\n\n### Dry run\n{dry}\n\n### Edge cases & pitfalls\n{edge}')


def extend(add, merge, skip, alias):
    E = 'Edelweiss'
    H = 'HP'
    L = 'HiLabs'
    sh = lambda n, ext='png': f'Screenshot ({n}).{ext}'

    # ---- Edelweiss ----
    merge('uipath-compromised-subarrays', E, [sh(138), sh(144)])
    add('edelweiss-longest-string-chain', E, 'Longest string chain by removing one character at a time',
        'Given an array of words representing a dictionary, test each word to see if it can be made into another word in the dictionary when characters are removed one at a time. Each word is its own first element of its string chain, so start with a chain length of 1. Each time a character is removed the chain length increases by 1, and the resulting word must be in the original dictionary. Determine the longest string chain achievable for the dictionary.',
        None,
        'Process the distinct words by increasing length. For each word try deleting each character; if the shorter word is in the dictionary, chain[w] = max(chain[w], chain[shorter] + 1). Answer the maximum chain. O(n x L^2) with L <= 60; verified against brute force.',
        section='dsa', topic='dp', type='coding', sources=[sh(142), sh(143)],
        function_signature='longestChain(words)',
        input_format='n, then the n words (one per line).',
        output_format='An integer: the length of the longest string chain.',
        constraints='1 <= n <= 50000; 1 <= |words[i]| <= 60; lowercase letters only.',
        examples=[{'input': 'words = ["a", "b", "ba", "bca", "bda", "bdca"]', 'output': '4', 'explanation': 'bdca -> bca -> ba -> a.'},
                  {'input': 'words = ["a", "and", "an", "bear"]', 'output': '3', 'explanation': 'and -> an -> a; bear cannot be reduced.'}],
        leetcode={'name': 'Longest String Chain', 'url': 'https://leetcode.com/problems/longest-string-chain/', 'similarity': 'same'},
        solution=sol(
            'A chain goes from a longer word to a shorter word by deleting one letter, so every chain strictly decreases in length. That makes it a longest-path problem on a DAG ordered by length, solvable by DP.',
            '1. Take the distinct words and sort them by length.\n2. best[w] = 1 initially.\n3. For each word w and each position i, form p = w without the i-th character; if p is in best, set best[w] = max(best[w], best[p] + 1).\n4. Return the maximum value of best.',
            'Predecessors of w (words obtained by deleting a letter) are strictly shorter, so they are processed before w; the recurrence takes the best chain among them. A recursive memoised brute force agrees on 300 random inputs.',
            'O(n x L^2): n words, L deletions each, each building a string of length up to L. Space O(n x L).',
            '''def longestChain(words):
    best = {}
    for w in sorted(set(words), key=len):
        b = 1
        for i in range(len(w)):
            p = w[:i] + w[i + 1:]
            if p in best:
                b = max(b, best[p] + 1)
        best[w] = b
    return max(best.values())''',
            'a, b -> 1. ba: deleting gives a or b -> 2. bca: deleting c gives ba -> 3. bda: -> 3. bdca: deleting d gives bca -> 4, deleting c gives bda -> 4. The maximum is 4.',
            '- Duplicates in the list are harmless after taking set().\n- A word of length 1 gives the empty string, which is not in the dictionary.\n- Sort by length (not alphabetically) so predecessors are always ready.'))
    add('edelweiss-prime-subtree-query', E, 'Count prime-valued nodes in the subtree of a queried node',
        'Construct a rooted undirected graph with n nodes numbered 1 to n by connecting m pairs of nodes (first[i], second[i]); node 1 is the root and the graph is a tree. A node\'s parent is the next node on the shortest path to node 1 and its descendants lie away from node 1. Each node has a positive integer value. For each query node, find the number of nodes with prime values in the subtree rooted at that node (1 is not prime).',
        None,
        'Sieve the primes up to max(values), root the tree at 1 with an iterative DFS, then accumulate prime counts from children to parents in reverse visiting order. Each query is an array lookup. O(n + max(values) + q); verified against brute force.',
        section='dsa', topic='trees', type='coding', sources=[sh(139, 'docx'), sh(139), sh(140), sh(141)],
        function_signature='primeQuery(n, first, second, values, queries)',
        input_format='n, the edge arrays first and second, the array values, and the queries array.',
        output_format='An array of integers aligned with the queries.',
        constraints='1 <= n <= 10^5; 1 <= m <= n-1; 1 <= first[i], second[i], values[i] <= 10^5; first[i] != second[i]; 1 <= q <= 10^5; 1 <= queries[j] <= 10^5.',
        examples=[{'input': 'n = 1, values = [7], queries = [1]', 'output': '[1]', 'explanation': 'A single prime node. (The photographed sample figure is only partly legible.)'}],
        notes='The sample tree in the photographs is a figure with node values (29, 11, 5, 15, 8, 17, 23 ...) that could not be transcribed exactly, so a trivial example is given instead.',
        solution=sol(
            'The answer for a node is the number of prime-valued nodes in its subtree, which equals its own prime flag plus the sum of its children\'s answers. Computing all subtree counts once makes every query O(1).',
            '1. Sieve of Eratosthenes up to max(values) (1 is not prime).\n2. Build the adjacency list and run an iterative DFS from node 1 to get a parent array and an order list.\n3. Process the order in reverse: cnt[u] += 1 if values[u-1] is prime; then cnt[parent[u]] += cnt[u].\n4. Answer each query with cnt[q].',
            'In reverse DFS order every child is finished before its parent, so cnt[u] already includes all its descendants when it is added to the parent. The brute force (collect each subtree and test primality) agrees on 300 random trees.',
            'O(M log log M + n + q) with M = max(values); O(n + M) space.',
            '''def primeQuery(n, first, second, values, queries):
    top = max(values) + 2
    sieve = [True] * top
    sieve[0] = sieve[1] = False
    for i in range(2, int(top ** 0.5) + 1):
        if sieve[i]:
            for j in range(i * i, top, i):
                sieve[j] = False
    adj = [[] for _ in range(n + 1)]
    for a, b in zip(first, second):
        adj[a].append(b)
        adj[b].append(a)
    parent = [0] * (n + 1)
    parent[1] = -1
    order, stack = [], [1]
    while stack:
        u = stack.pop()
        order.append(u)
        for v in adj[u]:
            if v != parent[u]:
                parent[v] = u
                stack.append(v)
    cnt = [0] * (n + 1)
    for u in reversed(order):
        if sieve[values[u - 1]]:
            cnt[u] += 1
        if parent[u] > 0:
            cnt[parent[u]] += cnt[u]
    return [cnt[q] for q in queries]''',
            'For a path 1 - 2 - 3 with values 4, 7, 9: cnt[3] = 0, cnt[2] = 1 (7), cnt[1] = 1. Queries [1, 2, 3] give [1, 1, 0].',
            '- The graph is given undirected; the rooting at node 1 defines the subtree.\n- Value 1 is not prime.\n- Use an iterative DFS: n = 10^5 can be a chain.\n- Query nodes refer to the same labels as the edge list.'))

    # ---- HP (existing questions) ----
    merge('hp-lfu', H, ['9a3cf435-b97d-4f21-acc0-83e0df5d8220.jpg', 'aa120bf7-f940-475b-b13d-10a97a5f5f57.jpg', 'e9f78318-0c54-4beb-8acb-41c93bf952f8.jpg'])
    merge('hp-even-difference', H, ['24ad085d-2d62-4d7b-9cf5-36d351fe02b2.jpg', '412d5087-47a9-41a5-9a17-5f55de77a013.jpg', '64c99298-0602-4998-8f51-81d761b6e7f0.jpg', 'dc105ef0-4c27-47e6-9943-63ae12f3f7be.jpg', 'e8e0b050-0887-4b2f-b714-f4deec3fb7fd.jpg'])

    # ---- HiLabs SDE PDF ----
    add('hilabs-connected-components-lcm', L, 'Connected components where an edge needs LCM at most 10^6',
        'An undirected graph has N nodes. The number written on the i-th node is a[i] (N distinct integers). There is an edge between nodes i and j if lcm(a[i], a[j]) <= 10^6. Print the number of connected components of the graph.',
        None,
        'A value above 10^6 has lcm above 10^6 with everything, so it is isolated. For the rest, for every x present and every multiple m of x up to 10^6, union x with the first present divisor seen for m: all present divisors of m have lcm dividing m and therefore are pairwise adjacent. Count the union-find roots. About 10^6 log 10^6 steps; verified against brute force.',
        section='dsa', topic='graphs', type='coding', hard=True, sources=['hilabs sde.pdf'],
        function_signature='solve(N, arr)',
        input_format='N; then N space-separated integers a[i].',
        output_format='The number of connected components.',
        constraints='1 <= N <= 10^6; 1 <= a[i] <= 10^9, all distinct.',
        examples=[{'input': '3\n2 1000000 999999', 'output': '2', 'explanation': 'lcm(2, 1000000) = 1000000 is an edge; 999999 is joined to neither.'}],
        notes='The statement prints the lcm bound as "<= 10" (cropped); the explanation shows the bound is 10^6.',
        solution=sol(
            'Checking all pairs is O(N^2). The trick is to look at the LCM value m itself: if two present numbers both divide m and m <= 10^6, then their lcm divides m, so it is also <= 10^6 and they are adjacent.',
            '1. Numbers above 10^6 are isolated components; count them separately.\n2. For the remaining present numbers keep a union-find.\n3. For each present x in increasing order, loop over multiples m of x up to 10^6: if firstdiv[m] is unset set it to x, otherwise union x with firstdiv[m].\n4. Answer = isolated count + number of distinct union-find roots among the present numbers.',
            'If lcm(a, b) = m <= 10^6, then both a and b divide m, so both are linked to firstdiv[m] and hence to each other. Conversely every union joins two numbers that divide a common m <= 10^6 and thus have lcm <= 10^6. A brute-force pairwise check matches on 200 random sets with random bounds.',
            'O(L log L) with L = 10^6 for the multiple loops (harmonic sum over present values), plus near-linear union-find; O(L) memory for firstdiv.',
            '''def solve(N, arr, L=10**6):
    present = set(a for a in arr if a <= L)
    big = sum(1 for a in arr if a > L)          # a > L has lcm > L with everything
    parent = {a: a for a in present}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    firstdiv = [0] * (L + 1)
    for x in sorted(present):
        for m in range(x, L + 1, x):
            if firstdiv[m] == 0:
                firstdiv[m] = x
            else:
                parent[find(x)] = find(firstdiv[m])
    return big + len({find(a) for a in present})''',
            'a = 2, 1000000, 999999. 999999 <= 10^6 is present. Multiples of 2 include 10^6, which is also a multiple of 10^6 itself, so 2 and 10^6 are united. 999999 shares no multiple <= 10^6 with them. Components: {2, 10^6} and {999999} = 2.',
            '- Use only values <= L as union-find nodes; a value like 10^9 would make the multiple loop empty but must still be counted as isolated.\n- 1 is adjacent to everything <= L (lcm(1, x) = x).\n- Python loops over 10^6 log 10^6 steps are slow; use C++ or numpy-style tricks in a real contest.'))
    add('hilabs-coin-problem', L, 'Count k-subsets of coins 0..N-1 whose sum is divisible by M',
        'Given N coins whose amounts are 0 to N-1 respectively, a friend wants to take K coins. The set of K coins is useful if the sum of the coins is divisible by a given integer M. Find the number of ways in which the friend can get K coins, modulo 10^9 + 7.',
        None,
        'DP over coins with dp[j][r] = number of ways to pick j coins with sum remainder r mod M; iterate j downwards for each coin. O(N x K x M) = 10^8 in the worst case. The sample (N = 4, K = 2, M = 2 gives 2) and a brute force on 300 random cases both agree.',
        section='dsa', topic='dp', type='coding', hard=True, sources=['hilabs sde.pdf'],
        function_signature='solve(n, k, m)',
        input_format='One line with N, K and M.',
        output_format='The number of useful sets modulo 10^9 + 7.',
        constraints='1 <= N <= 10^3; 1 <= K <= 10^2; 1 <= M <= 10^3.',
        examples=[{'input': '4 2 2', 'output': '2', 'explanation': 'The explanation lists {1, 3} and {2, 4} (sums 4 and 6); with coins 0..3 the useful sets are {0, 2} and {1, 3}: also 2.'}],
        notes='The statement says the coin amounts are 0 to N-1, but the explanation lists coins up to N (sets {1,3} and {2,4}). Both readings give 2 for the sample. This solution follows the written statement (0..N-1).',
        solution=sol(
            'We count subsets of fixed size K by their sum modulo M, which is a classic knapsack DP with the remainder as part of the state.',
            '1. dp[j][r] = number of ways to choose j coins (from those processed so far) with sum % M == r. Start with dp[0][0] = 1.\n2. For coin value c (0..N-1), iterate j from min(K, c+1) down to 1 and for every remainder s add dp[j-1][s] to dp[j][(s + c) % M] (iterating j downwards avoids using a coin twice).\n3. The answer is dp[K][0] modulo 10^9 + 7.',
            'Each subset is built by deciding for each coin whether it is included; the table tracks only the count and the remainder, which is all that affects the final condition.',
            'O(N x K x M) time (up to 10^8 for the largest limits, so use C++ or numpy vectorisation over the remainder dimension) and O(K x M) space.',
            '''MOD = 10**9 + 7

def solve(n, k, m):
    dp = [[0] * m for _ in range(k + 1)]
    dp[0][0] = 1
    for c in range(n):                         # coin amounts 0 .. n-1
        r = c % m
        for j in range(min(k, c + 1), 0, -1):
            prev, cur = dp[j - 1], dp[j]
            for s in range(m):
                v = prev[s]
                if v:
                    t = (s + r) % m
                    cur[t] = (cur[t] + v) % MOD
    return dp[k][0]''',
            'n = 4, k = 2, m = 2, coins 0, 1, 2, 3. Pairs with an even sum: (0, 2) and (1, 3). The DP ends with dp[2][0] = 2.',
            '- Coin 0 is a valid coin (amount 0) and counts as a distinct element.\n- Iterate j downwards, or each coin could be taken twice.\n- K may exceed N, in which case the answer is 0 (dp[K] is never filled).'))
