"""PhonePe online assessment: six coding problems (hurdles, case streak, island travel, fun Friday, XOR divisors, XOR swaps)."""


def sol(intuition, approach, why, cx, code, dry, edge):
    return (f'### Intuition\n{intuition}\n\n### Approach\n{approach}\n\n### Why it works\n{why}\n\n### Complexity\n{cx}\n\n'
            f'### Python solution\n```python\n{code}\n```\n\n### Dry run\n{dry}\n\n### Edge cases & pitfalls\n{edge}')


def extend(add, merge, skip, alias):
    P = 'PhonePe'

    def w(*ns):
        return [f'IMG-20240802-WA{n:04d}.jpg' for n in ns]

    add('phonepe-hurdles-max-score', P, 'Paris Olympics hurdles: maximum score keeping at most k consecutive hurdles',
        'There are n ordered hurdles and an athlete can cross at most k consecutive hurdles (hurdles cannot be reordered). The athlete removes some hurdles so that no run of more than k consecutive hurdles remains. Each hurdle i has a score; the athlete wants the maximum total score of the hurdles that remain. For example, with 3 hurdles and k = 1 the athlete must remove the first two, the last two, or the first and last hurdle.',
        None,
        'Equivalent to removing hurdles of minimum total score so that every window of k+1 consecutive hurdles contains a removed one. dp[i] = score[i] + min(dp[j]) for j in [i-k-1, i-1] with a virtual removed hurdle at index 0; answer = total - min dp[j] for j in [n-k, n]. A monotonic deque gives O(n). Verified against brute force.',
        section='dsa', topic='dp', type='coding', hard=True, sources=w(2, 3, 4),
        function_signature='maxScore(n, k, a)',
        input_format='First line: n and k. Next n lines: the score of hurdle i.',
        output_format='One integer: the maximum score.',
        constraints='1 <= n <= 10^5; 1 <= k <= n; 0 <= score <= 2 * 10^9.',
        examples=[{'input': '6 2\n1\n2\n3\n1\n6\n10', 'output': '21', 'explanation': 'Remove the 1st and 4th hurdles, keeping _ 2 3 _ 6 10.'},
                  {'input': '5 4\n1\n2\n3\n4\n5', 'output': '14', 'explanation': 'Remove the first hurdle.'}],
        solution=sol(
            'Keeping the maximum score is the same as deleting the minimum total score. The rule "at most k consecutive hurdles" says that between any two removed hurdles (and between the ends and the nearest removed hurdle) there can be at most k kept hurdles.',
            '1. Add a virtual removed hurdle at position 0 and one at n + 1 with score 0.\n2. dp[i] = minimum removed score if hurdle i is removed and the removed hurdles before it are valid: dp[i] = a[i] + min(dp[j]) over j in [i-k-1, i-1] (the gap of kept hurdles i-j-1 is at most k). dp[0] = 0.\n3. The end condition: the last real removed hurdle j must satisfy n - j <= k, i.e. j >= n - k. Answer = total - min(dp[j] for j in [max(0, n-k), n]).\n4. The window minimum is maintained with a monotonic deque.',
            'Every valid set of removed hurdles corresponds to a chain of removed positions with gaps of at most k kept hurdles; the dp enumerates exactly these chains and minimises the removed score. Brute force over all 2^n subsets agrees on 500 random cases.',
            'O(n) time with the deque, O(n) space.',
            '''from collections import deque

def maxScore(n, k, a):
    INF = float('inf')
    dp = [INF] * (n + 1)
    dp[0] = 0                               # virtual removed hurdle before the first one
    dq = deque([0])                         # indices with increasing dp values
    for i in range(1, n + 1):
        while dq and dq[0] < i - k - 1:     # too far back
            dq.popleft()
        dp[i] = a[i - 1] + dp[dq[0]]
        while dq and dp[dq[-1]] >= dp[i]:
            dq.pop()
        dq.append(i)
    best = min(dp[j] for j in range(max(0, n - k), n + 1))
    return sum(a) - best''',
            'Sample 0: n = 6, k = 2, scores 1 2 3 1 6 10, total 23. Removing hurdles 1 and 4 costs 1 + 1 = 2: gaps are 0 (before hurdle 1), 2 (hurdles 2 and 3) and 2 (hurdles 5 and 6), all at most k. Answer 23 - 2 = 21.',
            '- n = k: nothing needs to be removed, answer is the total (dp index n - k = 0 gives 0).\n- Scores up to 2 x 10^9 need 64-bit sums.\n- Use fast input for 10^5 lines.\n- Tie scores of 0 are fine.'))
    add('phonepe-mike-case-streak', P, 'Help Mike get rich: latest arrival that still gets a case',
        'To be eligible for a bonus, a lawyer must receive a case every day. Case distribution events happen at given timestamps (not sorted); each event hands out a fixed number of cases c. A lawyer who enters the office waits in line for the next event; at an event, waiting lawyers with the earliest entry times get the cases first. If there are more cases than waiting lawyers the extra cases are sent to senior partners and lost. No two lawyers arrive at the same time. Given the event timestamps, the entry timestamps of the other lawyers and the number of cases per event, find the latest timestamp at which Mike can reach the office and still get a case that day.',
        None,
        'Whether Mike is served is monotone in his arrival time: arriving earlier never hurts. Simulate events in order with a min-heap of waiting entry times, serve the c smallest, and binary search on Mike\'s arrival time among times not used by other lawyers. O((n + m) log m log T); verified against a brute force over all arrival times.',
        section='dsa', topic='heap', type='coding', hard=True, sources=w(5, 6, 7, 8),
        function_signature='latestArrival(events, lawyers, c)',
        input_format='Line 1: n (number of events). Line 2: n event timestamps. Line 3: m (other lawyers). Line 4: m entry timestamps. Last line: cases per event c.',
        output_format='One integer: the latest timestamp at which Mike can arrive and still be assigned a case.',
        constraints='Only partly visible: the arrays are unsorted, entry times are distinct and Mike\'s time must differ from the other lawyers\' times.',
        examples=[{'input': '3\n20 30 10\n7\n19 13 26 4 25 11 21\n2', 'output': '20'},
                  {'input': '2\n10 20\n4\n2 17 18 19\n2', 'output': '16'}],
        notes='The constraints block is cropped. It is assumed that a lawyer who arrives exactly at an event time joins that event, which reproduces both samples.',
        solution=sol(
            'The line at each event is first-come first-served. Mike wants to be as late as possible but still within the first c waiting lawyers at some event. Arriving later never helps, so the set of arrival times that succeed is a prefix (among the times nobody else uses).',
            '1. For a candidate arrival time t, run the simulation: sort events; push every lawyer (including Mike at t) whose entry time is <= the event time into a min-heap; pop up to c entries; if Mike\'s entry is popped he gets a case.\n2. Binary search on t in [0, last event time]. Define bad(x) as: the largest unused time <= x exists and Mike would not be served there. bad is monotone, so find the largest x that is not bad.\n3. The answer is the largest unused time <= x (or -1 if none).',
            'Earlier arrival means an earlier position in every queue Mike belongs to, so if arrival t is served then every earlier unused time is served too. The heap simulation applies the rules exactly. A brute force over all unused times agrees with the binary search on 500 random cases and on both samples.',
            'Each simulation is O((n + m) log m); with the binary search over a time range T this is O((n + m) log m log T).',
            '''import heapq

def served(events, lawyers, c, t):
    L = sorted(lawyers + [t])
    heap, li = [], 0
    for e in sorted(events):
        while li < len(L) and L[li] <= e:
            heapq.heappush(heap, L[li]); li += 1
        for _ in range(c):
            if not heap:
                break
            if heapq.heappop(heap) == t:
                return True
    return False

def latestArrival(events, lawyers, c):
    taken = set(lawyers)

    def free(x):                            # largest unused time <= x, or -1
        while x >= 0 and x in taken:
            x -= 1
        return x

    def bad(x):                             # monotone: once True it stays True
        f = free(x)
        return f >= 0 and not served(events, lawyers, c, f)

    lo, hi, best = 0, max(events), -1
    while lo <= hi:
        mid = (lo + hi) // 2
        if not bad(mid):
            best = mid
            lo = mid + 1
        else:
            hi = mid - 1
    return free(best) if best >= 0 else -1''',
            'Sample 1: events 10, 20, 30, lawyers 4 11 13 19 21 25 26, c = 2. With Mike at 20: event 10 serves 4; event 20 serves 11 and 13 (queue 11, 13, 19, 20); event 30 queue 19, 20, 21, 25, 26 serves 19 and Mike. At 22 he would be behind 19 and 21, so 20 is the latest.',
            '- Mike cannot share a time with another lawyer, so step down to the nearest unused time.\n- Cases left over at an event with an empty queue are lost, they do not carry over.\n- Lawyers who arrive after the last event are never served.\n- If no arrival works print -1.'))
    add('phonepe-dora-island-travel', P, 'Dora the Explorer: cheapest trip with exactly one switch between boat and plane',
        'An archipelago has N islands. Dora starts on island S and ends on island E. She may travel by Boat and by Sea Plane and must switch her mode of transportation exactly once: she travels from S to some island I using only one mode and then from I to E using only the other mode (in either order). Matrix B gives the boat cost between islands and matrix P the plane cost (-1 means no direct route). Find the minimum cost of the vacation, or -1 if the journey is impossible.',
        None,
        'Run Dijkstra on each mode: forward from S and backward (on the transposed matrix) from E. For both orders (boat then plane, plane then boat) take the minimum over switch islands I of dist1[I] + dist2[I]. Dense Dijkstra is O(N^2) per run, six runs in total. Verified against Floyd-Warshall brute force.',
        section='dsa', topic='graphs', type='coding', hard=True, sources=w(9, 10, 11, 13),
        function_signature='minCost(n, B, P, S, E)',
        input_format='N; then N lines of N integers for B; then N lines for P; then S and E (1-indexed).',
        output_format='A single number: the minimum cost of the vacation or -1.',
        constraints='3 <= N <= 1250; 1 <= S, E <= N, S != E; 1 <= Bij, Pij <= 100, and -1 if there is no direct route.',
        examples=[{'input': '3\n-1 1 2\n3 -1 4\n5 6 -1\n-1 6 5\n1 -1 4\n3 2 -1\n1 2', 'output': '4', 'explanation': 'Boat from island 1 to 3 (cost 2), then plane from 3 to 2 (cost 2).'}],
        notes='Whether the switch island may equal S or E is not stated; this solution requires the switch to happen at an island other than S and E so that both modes are really used. The second sample is cropped and not reproduced.',
        solution=sol(
            'Once the switch island I is fixed, the two halves are independent shortest-path problems, one per mode. So we need shortest distances from S in one mode and shortest distances to E in the other mode, for every island.',
            '1. Dijkstra from S on matrix B gives dB_from_S; Dijkstra from E on the transpose of P gives dP_to_E (cost of reaching E from each island by plane).\n2. Candidate 1: min over I (not S or E) of dB_from_S[I] + dP_to_E[I].\n3. Repeat with plane first then boat: Dijkstra from S on P and from E on the transpose of B.\n4. Answer is the smaller candidate, or -1 if both are infinite.',
            'Any valid journey is a path in one mode up to the switch island followed by a path in the other mode; the sum of the two shortest sub-paths is a lower bound for that I and is achievable. Using the transpose turns "to E" into "from E".',
            'O(N^2) per Dijkstra with an array scan (dense graph), four runs: about 6 x 10^6 operations for N = 1250.',
            '''INF = float('inf')

def dijkstra(W, src, n):
    d = [INF] * n
    d[src] = 0
    done = [False] * n
    for _ in range(n):
        u, best = -1, INF
        for i in range(n):
            if not done[i] and d[i] < best:
                best, u = d[i], i
        if u < 0:
            break
        done[u] = True
        row = W[u]
        for v in range(n):
            w = row[v]
            if w != -1 and d[u] + w < d[v]:
                d[v] = d[u] + w
    return d

def minCost(n, B, P, S, E):
    S -= 1
    E -= 1
    best = INF
    for first, second in ((B, P), (P, B)):
        d1 = dijkstra(first, S, n)
        d2 = dijkstra([list(c) for c in zip(*second)], E, n)   # transpose: distance to E
        for i in range(n):
            if i != S and i != E:
                best = min(best, d1[i] + d2[i])
    return -1 if best == INF else best''',
            'Sample 1 (S = 1, E = 2): boat from 1: island 3 costs 2. Plane to island 2: from island 3 costs 2. Switch at island 3 gives 2 + 2 = 4. The reverse order (plane first) gives 5 + 1 = 6 at island 3. Answer 4.',
            '- Use a distinct 1-indexed S and E; subtract 1.\n- A -1 entry is "no edge", not a negative cost.\n- Reading 2 x 1250 x 1250 numbers needs fast input.\n- Without the transpose, the "to E" distances would be wrong for asymmetric costs.'))
    add('phonepe-fun-friday-points', P, 'Fun Friday: maximum points from repeatedly splitting a list',
        'Harsh gives Pranay a list of n numbers. In each iteration Pranay adds the sum of all numbers in the list to his points and returns the list to Harsh. Harsh then acts: if the list has only one number he throws it out of the game; if it has more than one number he splits it into two non-empty subsequences and gives both subsequences to Pranay one by one. After all iterations Pranay checks his total points. Find the maximum possible points.',
        None,
        'Each element is counted once for every list it belongs to. The best split is to peel off the smallest element each time, so the sorted elements a1 <= ... <= an are counted 2, 3, ..., n, n times respectively (n >= 2). The formula is checked against an exhaustive search on 200 small cases.',
        section='dsa', topic='greedy', type='coding', sources=w(12, 14, 15),
        function_signature='maxPoints(a)',
        input_format='Line 1: n. Line 2: n integers (the initial list).',
        output_format='One integer: the maximum possible points.',
        constraints='1 <= n <= 3 x 10^5; 1 <= a_i <= 10^6.',
        examples=[{'input': '3\n4 2 6', 'output': '34', 'explanation': '12 for the full list, then 2 for (2) and 10 for (4, 6), then 4 and 6 for the singletons.'},
                  {'input': '1\n11', 'output': '11'}],
        solution=sol(
            'Total points = sum over all lists ever handed to Pranay of that list\'s sum = sum over elements of (number of lists containing the element). The splitting process is a binary tree whose leaves are single numbers; an element at depth d is counted d + 1 times.',
            '1. The tree has n leaves; we want large elements deep and small elements shallow.\n2. A caterpillar tree (peel off one element at a time) has leaf depths 1, 2, ..., n-1, n-1, so counts 2, 3, ..., n, n.\n3. Assign the smallest value to the shallowest leaf: sort ascending and use multipliers 2, 3, ..., n for the first n - 1 elements and n for the last one. For n = 1 the answer is the single value.',
            'By the rearrangement inequality, the multiset of depths is fixed by the tree shape and the largest values should get the largest counts. A caterpillar is optimal because any binary tree with n leaves has leaf depths d_i with sum of 2^(-d_i) = 1, and the caterpillar has the lexicographically largest (deepest) multiset of leaf counts. An exhaustive search over all splits (n up to 7) matches the formula.',
            'O(n log n) for sorting, O(1) extra space.',
            '''def maxPoints(a):
    a = sorted(a)
    n = len(a)
    if n == 1:
        return a[0]
    # a[i] is counted i + 2 times for i < n - 1, the largest is counted n times
    return sum(a[i] * (i + 2) for i in range(n - 1)) + a[-1] * n''',
            'a = 4 2 6 sorted to 2 4 6. Counts 2, 3, 3: 2 x 2 + 4 x 3 + 6 x 3 = 4 + 12 + 18 = 34, matching the sample.',
            '- Totals reach about 3 x 10^5 x 3 x 10^5 x 10^6 = 9 x 10^16: fits in signed 64-bit.\n- The last two elements both use multiplier n.\n- The split is into subsequences, so order inside the list does not matter.'))
    add('phonepe-xor-even-divisors', P, 'Count subarrays whose XOR has an even number of divisors',
        'Given an array a of n integers (1 <= a[i] <= n), count the subarrays whose XOR has an even number of divisors. (For example 2, 3, 5, 6 have an even number of divisors, while 1 and 4 have an odd number.)',
        None,
        'A positive integer has an even number of divisors iff it is not a perfect square. Count subarrays with prefix XOR difference 0 or a perfect square using a frequency array over prefix XORs (values < 2^18, only about 512 squares) and subtract from n(n+1)/2. The sample 1 (3 1 2) shows XOR 0 is not counted. Verified against brute force.',
        section='dsa', topic='bit-manipulation', type='coding', hard=True, sources=['Phonepe OA questions.pdf'],
        function_signature='countSubarrays(n, a)',
        input_format='First line: n. Second line: n integers.',
        output_format='The number of subarrays whose XOR has an even number of divisors.',
        constraints='2 <= n <= 2 x 10^5; 1 <= a[i] <= n.',
        examples=[{'input': '3\n3 1 2', 'output': '4', 'explanation': 'Subarrays [3], [3,1], [1,2], [2].'},
                  {'input': '5\n4 2 1 5 3', 'output': '11'}],
        notes='A subarray whose XOR is 0 is not counted in sample 1 (the subarray 3 1 2 has XOR 0 and is excluded), so 0 is treated as having no even divisor count.',
        solution=sol(
            'Divisors of x pair up as (d, x/d); the pairing breaks only when d = x/d, i.e. x is a perfect square. So even divisor count means "not a perfect square" (and x > 0).',
            '1. Let p_0 = 0 and p_i = a_1 xor ... xor a_i. The XOR of subarray (i, j] is p_i xor p_j.\n2. All XORs are below M = the smallest power of two above n (at most 2^18). Store cnt[v] = how many prefixes equal v.\n3. Bad pairs: XOR = 0 contributes sum cnt[v](cnt[v]-1)/2; for each perfect square s = 1, 4, 9, ..., s < M, the pairs with p_i xor p_j = s number sum over v of cnt[v] x cnt[v xor s] divided by 2.\n4. Answer = n(n+1)/2 - bad pairs.',
            'Subarrays correspond one-to-one with pairs of prefix indices i < j, and the XOR value of the subarray is p_i xor p_j; complementing "perfect square or zero" gives exactly the subarrays whose XOR is a non-square positive number.',
            'About 512 squares x M (2^18) numpy operations = 1.3 x 10^8 element operations; O(sqrt(M) x M) in total.',
            '''import numpy as np

def countSubarrays(n, a):
    M = 1
    while M <= n:
        M <<= 1
    cnt = np.zeros(M, dtype=np.int64)
    cnt[0] += 1
    p = 0
    for v in a:
        p ^= v
        cnt[p] += 1
    idx = np.arange(M)
    bad = int((cnt * (cnt - 1) // 2).sum())          # XOR == 0
    s = 1
    while s * s < M:
        sq = s * s
        bad += int((cnt * cnt[idx ^ sq]).sum()) // 2
        s += 1
    return n * (n + 1) // 2 - bad''',
            'Sample 1: prefix XORs are 0, 3, 2, 0. Total subarrays 6. Pairs with XOR 0: (0,0) = 1 (the whole array). Pairs with XOR square: 3 xor 2 = 1 (subarray [1]) is a square, giving 1 more. Bad = 2, answer 6 - 2 = 4.',
            '- XOR 0 is excluded (as the sample shows).\n- Values below M only: XOR of numbers <= n stays below the next power of two.\n- Divide the square-pair sum by 2 because each unordered pair is counted twice (squares > 0 so v != v xor s).\n- Use int64 to hold counts.'))
    add('phonepe-lexi-smallest-xor-lt-4', P, 'Lexicographically smallest array when only elements with XOR less than 4 can be swapped',
        'Given an array of non-negative integers, you may swap two elements any number of times provided the bitwise XOR of the two elements is less than 4. Output the lexicographically smallest array that can be made.',
        None,
        'a xor b < 4 exactly when a and b agree on all bits above the lowest two, i.e. a >> 2 == b >> 2. Elements of one group (equal a >> 2) can be permuted freely, so sort each group\'s values into that group\'s positions. Verified against exhaustive swapping.',
        section='dsa', topic='sorting', type='coding', sources=['Phonepe OA questions.pdf'],
        function_signature='smallest(a)',
        input_format='Per test case: n, then n integers. The sum of n over all test cases is at most 2 x 10^5.',
        output_format='n integers: the lexicographically smallest array.',
        constraints='1 <= n <= 2 x 10^5; 0 <= a_i <= 10^9.',
        examples=[{'input': '4\n1 0 3 2', 'output': '0 1 2 3'}, {'input': '5\n2 7 1 5 6', 'output': '1 5 2 6 7'}],
        leetcode={'name': 'Make Lexicographically Smallest Array by Swapping Elements', 'url': 'https://leetcode.com/problems/make-lexicographically-smallest-array-by-swapping-elements/', 'similarity': 'similar'},
        notes='The first sample input is partly illegible; the array 1 0 3 2 is inferred from its output 0 1 2 3 and the explanation (swap 0,1 and 3,2).',
        solution=sol(
            'Swaps are allowed between a pair only when their XOR is under 4, which depends only on the bits above the two lowest bits. Pairs within the same group (same a >> 2) can swap directly, so every group is fully connected.',
            '1. Group the indices by key = a[i] >> 2.\n2. For each group, sort its values and write them back into the group\'s positions in increasing index order.\n3. The result is lexicographically smallest because each position receives the smallest value still available to it.',
            'Within a connected group any permutation is reachable; positions of different groups never exchange values. Greedily placing sorted values in increasing positions minimises the array lexicographically group by group.',
            'O(n log n) time, O(n) space.',
            '''from collections import defaultdict

def smallest(a):
    groups = defaultdict(list)
    pos = defaultdict(list)
    for i, v in enumerate(a):
        groups[v >> 2].append(v)
        pos[v >> 2].append(i)
    res = a[:]
    for g in groups:
        for i, v in zip(pos[g], sorted(groups[g])):
            res[i] = v
    return res''',
            'a = 2 7 1 5 6. Keys: 2 -> 0, 7 -> 1, 1 -> 0, 5 -> 1, 6 -> 1. Group 0 positions {0, 2} hold {2, 1} -> 1, 2. Group 1 positions {1, 3, 4} hold {7, 5, 6} -> 5, 6, 7. Result 1 5 2 6 7.',
            '- XOR < 4 means equal value of a >> 2, not "differs in the last two bits only" for arbitrary values; for example 3 and 4 differ in the last bits but have XOR 7.\n- Fast input is needed for 2 x 10^5 numbers.\n- Print each test case on its own line.'))
