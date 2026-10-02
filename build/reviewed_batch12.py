"""Visually reviewed BNY Mellon, Zepto, ThoughtSpot and Visa screenshots."""


def extend(add, skip):
    add('bny-cluster-quality', 'BNY Mellon', 'Maximum quality of a machine cluster',
        'Each machine has a positive integer speed and reliability. Select a nonempty cluster containing at most maxMachines machines. Its quality is the sum of selected speeds multiplied by the minimum selected reliability. Return the maximum possible quality, without applying a modulus.', None,
        'Sort machines by decreasing reliability. Maintain a min-heap of at most maxMachines speeds and their sum. Insert the current speed, discarding the smallest if the heap is too large, and consider speed_sum×current_reliability. At an optimal cluster’s minimum reliability, all its machines have become eligible; retaining the largest eligible speeds maximises the sum for that threshold. Evaluate all thresholds, not only clusters of exactly maxMachines machines: fewer machines can be better. O(n log n+n log k) time and O(n+k) space with the sorted list. Products can exceed a 32-bit integer; use Python integers or a wide type. [LeetCode 1383](https://leetcode.com/problems/maximum-performance-of-a-team/) uses the same optimisation but requires a modulus, which this source does not.',
        section='dsa', topic='heap', type='coding', hard=True,
        sources=[f'IMG-20240820-WA0{i}.jpg' for i in range(103,106)],
        function_signature='maxClusterQuality(speed, reliability, maxMachines)',
        constraints='1 ≤ n ≤ 10⁵; 1 ≤ speed[i], reliability[i] ≤ 10⁵; 1 ≤ maxMachines ≤ n.',
        examples=[{'input':'speed = [4,3,15,5,6]\nreliability = [7,6,1,2,8]\nmaxMachines = 3','output':'78'}, {'input':'speed = [12,112,100,13,55]\nreliability = [31,4,100,55,50]\nmaxMachines = 3','output':'10000','explanation':'The third machine alone is optimal.'}],
        leetcode={'name':'Maximum Performance of a Team','url':'https://leetcode.com/problems/maximum-performance-of-a-team/','similarity':'similar'})

    add('bny-tree-pruning', 'BNY Mellon', 'Remove leaves to eliminate ancestor-distance violations',
        'A weighted undirected tree is rooted at node 1. Each node y has a positive limit arr[y]. The remaining tree must have no ancestor x and descendant y for which the sum of edge weights on x→y exceeds arr[y]. Repeatedly remove a current leaf, keeping the root. Return the minimum total number of removed nodes; each deletion is one leaf-removal operation. Edge weights may be negative.', None,
        'For each node y, compute the largest ancestor-to-y path sum, including the zero-length path. Starting with d[root]=0, an edge of weight w from x to y gives d[y]=max(0,d[x]+w). If d[y]>arr[y], y must be removed; to delete it as a leaf, every descendant must be removed first, so remove its whole subtree. Otherwise continue to its children. Count all nodes beneath the first violating ancestor. An iterative DFS carrying distance and a removed flag handles deep trees in O(n) time and O(n) space. With negative weights, root distance alone is insufficient: the largest suffix can begin at a later ancestor. Equality is permitted by the stated “no arr[y]<distance” condition. [Codeforces 682C](https://codeforces.com/problemset/problem/682/C) has the same pruning pattern.',
        section='dsa', topic='trees', type='coding', hard=True,
        sources=[f'IMG-20240820-WA0{i}.jpg' for i in range(106,109)],
        function_signature='getMinLeavesToRemove(tree_nodes, tree_from, tree_to, tree_weight, arr)',
        constraints='1 ≤ tree_nodes ≤ 10⁵; tree_edges=tree_nodes−1; connected tree; arr values are positive. Exact weight bounds are blurred in the source.',
        examples=[{'input':'tree_nodes = 5\ntree_from = [1,1,3,3]\ntree_to = [2,3,4,5]\ntree_weight = [8,5,2,7]\narr = [12,2,27,11,1]','output':'2','explanation':'Remove leaves 2 and 5.'}],
        notes='The source’s existential “a pair” phrasing conflicts with its “no instance” condition and worked example. The cleaned prompt uses the universal no-violation interpretation supported by the example; its explanation uses > comparisons even though the condition allows equality.')

    add('zepto-minimax-path', 'Zepto', 'Minimise the largest adjacent-value jump along a path',
        'An undirected graph has N nodes, M edges and an integer value A[i] at each node. A path’s value is the maximum absolute difference |A[u]−A[v]| across its edges. Given start S and end E, return the minimum possible path value.', None,
        'Treat each edge (u,v) as having weight |A[u]−A[v]|. Use Dijkstra’s algorithm with bottleneck distance: initialise dist[S]=0 and relax an edge with candidate=max(dist[u],edge_weight), taking the smaller candidate at v. Pop the smallest candidate from a min-heap and discard stale entries; the first settled destination gives the optimum. Alternatively sort edges by weight and union endpoints until S and E are connected. Heap Dijkstra is O((N+M) log(N+M)) time with lazy heap entries and O(N+M) space. A sum-of-weights shortest path optimises a different objective.',
        section='dsa', topic='graphs', type='coding', hard=True,
        sources=[f'IMG-20240804-WA0{i}.jpg' for i in range(120,123)],
        function_signature='pathValue(N, M, S, E, edge, A)',
        constraints='1 ≤ N ≤ 10⁵; N−1 ≤ M ≤ 10⁶; 1 ≤ A[i] ≤ 10⁶. The photos do not specify the unreachable-case return value or the zero-edge S=E case.',
        examples=[{'input':'N = 5, M = 7, S = 2, E = 5\nedge = [(1,2),(2,3),(3,4),(4,5),(1,3),(1,4),(1,5)]\nA = [20,23,21,45,21]','output':'2','explanation':'The path 2→3→1→5 has differences 2,1,1.'}],
        notes='Do not infer connectivity merely from M≥N−1. Clarify missing endpoint/failure conventions before attaching a judge.')
    for i in (123,124):
        skip('Zepto',f'IMG-20240804-WA0{i}.jpg','Coin problem has function/constraints and examples but lacks its main statement, coin values, selection rule and counting modulus. Do not infer rules from two sample subsets.')

    add('thoughtspot-palindrome-pairs', 'ThoughtSpot', 'Tree paths whose edge labels can form a palindrome',
        'A tree has g_nodes vertices numbered 1 through g_nodes. Each edge has a label in 1…26 representing A…Z. Count unordered pairs of distinct vertices whose unique path has edge characters that can be rearranged into a palindrome.', None,
        'Assign each node a 26-bit root-path parity mask: toggle the bit of each traversed edge label. The XOR of two node masks gives odd/even edge-label counts on their connecting path. Rearrangement into a palindrome is possible exactly when this XOR has zero or one set bit. Process masks one at a time: add the stored frequency of the same mask and of each of its 26 single-bit neighbours, then increment this mask’s frequency. This counts each unordered distinct pair once and excludes self-pairs. Iterative traversal avoids depth limits. O(26n) time and O(n) space. Use a wide count because n(n−1)/2 can exceed signed 32-bit range.',
        section='dsa', topic='bit-manipulation', type='coding', hard=True,
        sources=['IMG-20241105-WA0001.jpg','IMG-20241105-WA0004.jpg'],
        function_signature='numNicePairs(g_nodes, g_from, g_to, g_weight)',
        constraints='1 ≤ g_nodes ≤ 10⁵; g_edges=g_nodes−1; 1 ≤ edge labels ≤ 26; the reported tree diameter is less than 1000.',
        examples=[{'input':'g_nodes = 5\ng_from = [1,2,3,3]\ng_to = [2,3,4,5]\ng_weight = [2,1,1,1]','output':'9'}])
    add('thoughtspot-distinct-digits', 'ThoughtSpot', 'Count numbers without repeated digits in inclusive ranges',
        'For each inclusive integer range [n,m], print the number of integers whose usual decimal representation has no repeated digit. Ranges may contain up to one million, and there may be up to 100,000 queries.', None,
        'Precompute a prefix count through the largest queried endpoint B. Check each integer with a ten-bit digit mask; a previously set bit means a repeated digit. Leading zeros are not part of the usual representation. Set prefix[x]=prefix[x−1]+valid(x), then answer [n,m] as prefix[m]−prefix[n−1]. O(B log B+q) time and O(B) space. Alternatively digit DP answers counts up to each bound without enumerating B, useful for larger domains.',
        section='dsa', topic='preprocessing', type='coding',
        sources=['IMG-20241105-WA0002.jpg','IMG-20241105-WA0005.jpg'],
        function_signature='countNumbers(arr)', constraints='1 ≤ q ≤ 10⁵; 1 ≤ n ≤ m ≤ 10⁶.',
        examples=[{'input':'arr = [[80,120]]','output':'27','explanation':'There are 41 integers in the range; 14 repeat a digit.'}])
    add('thoughtspot-power-sums', 'ThoughtSpot', 'Count distinct sums of two integer powers',
        'Count integers x in the inclusive range [l,r] that can be written as a^p+b^q, where a,b are nonnegative integers and p,q are integers greater than 1. Count x once even when it has multiple representations.', None,
        'Generate a set P of all power values at most r. Include 0 and, if r≥1, 1. For each base from 2 through floor(sqrt(r)), repeatedly multiply starting at its square while the value is ≤r. Deduplicate before pairing. Sort P and enumerate unordered pairs of power values, allowing the same value twice; mark each sum ≤r in a byte array and stop a row when sums exceed r. Count marked entries in [l,r]. If t=|P|, this straightforward method takes O(r+t²+sqrt(r) log r) time and O(r+t) space. Deduplicating sums is essential: the problem counts integers, not base/exponent tuples. For r=0, 0=0²+0² is valid.',
        section='dsa', topic='math', type='coding', hard=True,
        sources=['IMG-20241105-WA0003.jpg'],function_signature='countPowerNumbers(l, r)',
        constraints='0 ≤ l ≤ r ≤ 5×10⁶.', examples=[{'input':'l = 20, r = 25','output':'3','explanation':'20=2²+4², 24=2³+4² and 25=3²+4².'}])
    add('thoughtspot-directional-jumps', 'ThoughtSpot', 'Minimum grid jumps with a forced next direction',
        'A grid uses * for empty cells, # for blocked cells, S for the start and E for the destination. Jump any positive integer distance horizontally or vertically; intermediate blocked cells may be crossed but the landing cell must be traversable. After a jump of length greater than one, the next jump must use the same direction. A length-one jump frees the direction for the following jump. The final jump must have length one. Return the minimum number of jumps from S to E, or −1 if impossible.', None,
        'Run BFS over (row,column,direction_state). State FREE permits four directions; after a long jump the state forces its direction until a length-one jump resets it to FREE. Each legal jump is one edge regardless of length. Enumerate positive lengths up to the grid boundary and skip blocked landing cells without stopping the ray. Accept the destination only in FREE state, ensuring the final jump had length one; reaching E after a long jump does not finish the route. Five states per cell use O(nm) space. Direct ray enumeration costs O(nm(n+m)) time. For larger grids, maintain unvisited forced-state landing positions in ordered row/column sets and remove a destination after first discovery, while handling length-one moves separately; this avoids repeatedly scanning the same long-jump targets. The source omits grid-size bounds, so select the implementation after clarifying them.',
        section='dsa', topic='graphs', type='coding', hard=True,
        sources=['WhatsApp Image 2024-11-05 at 02.30.10_ea0f0e3b.jpg'],
        constraints='Exactly one S and one E; full dimension bounds and the original function signature are not shown.',
        examples=[{'input':'grid = ["S****#","**#***","*****#","*#*#**","#****E"]','output':'5','explanation':'(0,0)→(0,3)→(0,4)→(3,4)→(4,4)→(4,5).'}])

    add('visa-enclosing-square', 'Visa', 'Smallest integer-coordinate square strictly containing k points',
        'Given integer point coordinates x[i],y[i], find the minimum area of an axis-aligned square with integer-coordinate vertices that contains at least k points strictly inside. Points on a square’s boundary do not count.', None,
        'Enumerate the leftmost and rightmost point x-coordinates of a candidate subset. Collect y-coordinates of all points in that inclusive x-band and sort them. For every window of k consecutive y-values, let span_y be its last minus first value and span_x the x-band width. These k points fit strictly inside an integer-vertex square of side max(span_x,span_y)+2: integer boundaries must lie at least one unit beyond each extreme. Minimise the squared side over all bands and windows. Considering the actual x-extremes of an optimal k-point subset ensures it is represented. O(n³ log n) time and O(n) extra space with n≤100. The +2 is essential; even a single point needs side 2 and area 4. Use wide arithmetic for coordinates near ±10⁹.',
        section='dsa', topic='geometry', type='coding', hard=True,
        sources=[f'IMG-20240831-WA00{i}.jpg' for i in range(55,58)],
        function_signature='minArea(x, y, k)',constraints='2 ≤ n ≤ 100; −10⁹ ≤ x[i],y[i] ≤ 10⁹; 1 ≤ k ≤ n.',
        examples=[{'input':'x = [1,1,2]\ny = [1,2,1]\nk = 3','output':'9','explanation':'The square from (0,0) to (3,3) contains all points strictly inside.'}],
        notes='The source says integer coordinates and its side-3 example supports integer square vertices; permitting arbitrary real vertices would yield a different infimum.')
