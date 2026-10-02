"""Sigmoid (Mettl fresher assessment): five coding problems, CS fundamentals MCQs, two reasoning items."""


def S(body, wrong='', fast='', traps=''):
    out = '### Solution\n' + body.strip() + '\n'
    if wrong:
        out += '\n### Why the other options are wrong\n' + wrong.strip() + '\n'
    if fast:
        out += '\n### Faster method\n' + fast.strip() + '\n'
    if traps:
        out += '\n### Common traps\n' + traps.strip() + '\n'
    return out


def extend(add, merge, skip, alias):
    G = 'Sigmoid'

    def f(n):
        return f'IMG-20240914-WA00{n}.jpg'

    def g(s):
        return f'IMG_20240914_{s}.jpg'

    # ---------------- coding ----------------
    add('sigmoid-food-distribution', G, 'Count connected groups of people stuck after an earthquake',
        'People are stuck in different parts of a city and food is to be dropped by helicopter. A "part" is a maximal 4-directionally connected group of people. Given a 2-D array city, return the number of parts. People are denoted by 0 and the rest of the city is denoted by 1.',
        None,
        'Count the connected components of 0 cells under 4-direction adjacency. Scan the grid; each time an unvisited 0 is found, increment the answer and flood-fill (BFS or DFS) its component. O(N x M) time and O(N x M) space for the queue/visited marks.',
        section='dsa', topic='graphs', type='coding',
        sources=[f(32), f(33), f(35)],
        function_signature='foodDistribution(input1, input2, input3)',
        input_format='input1: number of rows N. input2: number of columns M. input3: N x M array, 0 = people, 1 = anything else.',
        output_format='An integer: the number of parts.',
        constraints='Bounds are not visible in the photographs.',
        examples=[{'input': 'input1 = 5, input2 = 5, input3 = [[0,1,1,1,1],[0,0,1,0,1],[1,0,1,0,1],[1,1,0,1,1],[0,1,1,0,1]]', 'output': '5'},
                  {'input': 'input1 = 3, input2 = 5, input3 = [[0,1,0,1,0],[0,1,0,1,0],[0,0,0,1,1]]', 'output': '2'}],
        leetcode={'name': 'Number of Islands', 'url': 'https://leetcode.com/problems/number-of-islands/', 'similarity': 'similar'},
        solution='''### Intuition
Groups of people that touch horizontally or vertically form one "part". Counting parts is exactly counting connected components of the 0 cells (this is the classic "number of islands" with 0 as land).

### Approach
1. Walk through every cell in row-major order.
2. When a cell with value 0 is found, it begins a new component: increase the counter.
3. Flood-fill the whole component with BFS, marking each reached 0 as visited (set it to 1 on a copy of the grid), moving in the four directions.
4. Continue scanning; already visited cells are skipped. The counter is the answer.

### Why it works
Each flood fill visits exactly the cells reachable from its start via 0 cells, i.e. one full component, and marks them so they are never counted again. Distinct components share no adjacent cells, so each triggers exactly one new fill.

### Complexity
O(N x M) time because every cell is pushed to the queue at most once; O(N x M) space in the worst case for the queue.

### Python solution
```python
from collections import deque

def foodDistribution(input1, input2, input3):
    n, m = input1, input2
    g = [row[:] for row in input3]      # copy so the input is not modified
    parts = 0
    for i in range(n):
        for j in range(m):
            if g[i][j] == 0:            # new, unvisited group of people
                parts += 1
                g[i][j] = 1             # mark visited
                q = deque([(i, j)])
                while q:
                    x, y = q.popleft()
                    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        a, b = x + dx, y + dy
                        if 0 <= a < n and 0 <= b < m and g[a][b] == 0:
                            g[a][b] = 1
                            q.append((a, b))
    return parts
```

### Dry run
Example 1 groups: {(0,0),(1,0),(1,1),(2,1)}, {(1,3),(2,3)}, {(3,2)}, {(4,0)}, {(4,3)}. The scan meets (0,0) first (count 1, fills its component), then (1,3) (count 2), (3,2) (3), (4,0) (4), (4,3) (5). Answer 5.

### Edge cases & pitfalls
- Diagonal neighbours do not connect; only four directions.
- Mark cells when they are pushed, not when popped, or the same cell can be queued many times.
- A grid of all 1s returns 0; an all-0 grid returns 1.
- Use an iterative fill; recursive DFS can overflow the stack on large grids.''')
    add('sigmoid-magical-gems', G, 'Maximum worth of magical gems split into groups',
        'A king has gems with integer values A[0..N-1]. In a group of gems, the total value of the group equals the number of gems in the group multiplied by the sum of the values of the gems in it. Distribute all gems into groups (the groups may be any subsets) so that the total value of all groups is maximum, and return that maximum.',
        None,
        'Sort the values in descending order. An exchange argument shows an optimal partition uses groups that are contiguous in this sorted order (a larger element never sits in a lower group than a smaller one). Then dp[i] = max over j<i of dp[j] + (i-j) x (prefix[i]-prefix[j]) on the sorted array. O(N^2) time, O(N) space; verified against brute force over all set partitions.',
        section='dsa', topic='dp', type='coding', hard=True,
        sources=[f(30), f(31), f(34), f(52), f(53), f(54), f(55), g('013528_064'), g('013528_129'), g('013528_447'), g('013541_326'), g('013541_699'), g('013542_053'), g('013547_924')],
        function_signature='magicalGems(input1, input2)',
        input_format='input1: N, the number of gems. input2: integer array A of gem values (may be negative).',
        output_format='An integer: the maximum total value.',
        constraints='Bounds are not visible in the photographs.',
        examples=[{'input': 'input1 = 4, input2 = [2, -7, 9, 9]', 'output': '53', 'explanation': 'Groups {2,9,9} -> 3 x 20 = 60 and {-7} -> -7, total 53.'},
                  {'input': 'input1 = 2, input2 = [2, 2]', 'output': '8', 'explanation': 'One group {2,2}: 2 x 4 = 8.'}],
        notes='The task is repeated across many captures of the same question; the examples in the photographs are consistent with groups being arbitrary subsets (the sample puts 2, 9, 9 together and -7 apart).',
        solution='''### Intuition
A group of size k and sum s is worth k x s, so putting several large positive values together multiplies their sum by the group size, while a negative value should be kept away unless it is dragged along cheaply. The groups are arbitrary subsets, so only the values matter, not the positions.

### Approach
1. Sort the values in descending order.
2. Claim: there is an optimal partition whose groups are contiguous blocks of the sorted array. Exchange argument: if a larger value x sits in a group of size p with sum S and a smaller value y sits in a group of size q with sum T where the group of x is "lower" in the ordering, swapping x and y changes the total by (q - p)(x - y) times a sign that is non-negative for a suitable orientation, so blocks never lose.
3. Let pre[i] be the sum of the first i sorted values. Define dp[i] = best total for the first i sorted values. dp[0] = 0.
4. Transition: dp[i] = max over j < i of dp[j] + (i - j) x (pre[i] - pre[j]); the last block is the sorted elements j..i-1.
5. The answer is dp[N].

### Why it works
Every partition can be rearranged without loss into contiguous blocks of the sorted order, and the DP tries every way to cut the sorted array into blocks, so it finds the best. The check script compares the DP to a brute force over all set partitions for 300 random arrays of size up to 7.

### Complexity
Sorting is O(N log N); the DP is O(N^2) time and O(N) space. If N is large the transition is a convex hull trick (dp[j] - j x pre[j] + ... lines), reducing it to O(N log N).

### Python solution
```python
def magicalGems(input1, input2):
    a = sorted(input2, reverse=True)
    n = len(a)
    pre = [0]
    for v in a:
        pre.append(pre[-1] + v)
    NEG = float('-inf')
    dp = [NEG] * (n + 1)
    dp[0] = 0
    for i in range(1, n + 1):
        for j in range(i):
            val = dp[j] + (i - j) * (pre[i] - pre[j])
            if val > dp[i]:
                dp[i] = val
    return dp[n]
```

### Dry run
Example 1: sorted = [9, 9, 2, -7], pre = [0, 9, 18, 20, 13].
dp[1] = 9, dp[2] = max(0 + 2 x 18, 9 + 9) = 36, dp[3] = max(3 x 20, 36 + 2) = 60 (one block of three), dp[4] = max(4 x 13 = 52, dp[3] + (-7) = 53, ...) = 53.

### Edge cases & pitfalls
- All values negative: every element is best alone, giving the sum of values.
- A single element: its value (1 x v).
- Large sums: use 64-bit integers in other languages (the product can reach N x N x max).
- Do not assume groups must be contiguous in the original order; the sample splits 2, 9, 9 away from -7 which sits between them.''')
    add('sigmoid-gift-box', G, 'Pack the most items with all type frequencies distinct',
        'Jack\'s gift shop has items, where items[i] denotes the type of the i-th gift (1 <= items[i] <= n). A customer wants a gift box with the maximum number of items such that the frequencies of each item type in the box are all different (if two items of type 5 are packed, no other type can also appear exactly twice). It is not necessary to use every type, nor all items of a type. Return the maximum number of items that can be packed.',
        None,
        'Count the frequency of each type and sort the counts in descending order. Greedily give each type min(count, previous taken - 1) items, stopping when this reaches 0. This makes the packed frequencies strictly decreasing and distinct while taking as many as possible. O(n log n) time, O(n) space; verified against brute force.',
        section='dsa', topic='greedy', type='coding',
        sources=[g('013528_070'), g('013528_109'), g('013528_509')],
        function_signature='maxItems(input1, input2)',
        input_format='input1: length of the array. input2: array of item types.',
        output_format='An integer: the maximum number of items that can be packed.',
        constraints='Bounds are not visible in the photographs.',
        examples=[{'input': 'input1 = 6, input2 = [4, 1, 6, 3, 6, 5]', 'output': '3', 'explanation': 'Pack 2 items of type 6 and 1 item of type 4.'},
                  {'input': 'input1 = 7, input2 = [3, 7, 1, 1, 3, 1, 7]', 'output': '6', 'explanation': 'Pack 3 of type 1, 2 of type 3 and 1 of type 7.'}],
        leetcode={'name': 'Minimum Deletions to Make Character Frequencies Unique', 'url': 'https://leetcode.com/problems/minimum-deletions-to-make-character-frequencies-unique/', 'similarity': 'similar'},
        solution='''### Intuition
Only the count of each type matters. We want distinct positive packed counts, each at most the available count of its type, with the largest possible total. This is the same idea as making character frequencies unique by deleting as little as possible.

### Approach
1. Count how many items of each type exist.
2. Sort these counts in descending order.
3. Keep `limit`, the largest value still allowed (initially infinity).
4. For each count c in order: take t = min(c, limit - 1). If t <= 0, stop (smaller counts cannot help). Otherwise add t to the answer and set limit = t.

### Why it works
Packed counts must be distinct positive integers, so if k types are used the packed counts are at most (a1, a1-1, a1-2, ...) when processed from the largest availability. Taking the largest count first and lowering each following count just enough to stay distinct never wastes capacity: if a type had to be lowered further, any other assignment would also be forced to give a smaller value to some type (exchange argument). The brute force check on 300 random cases confirms the greedy.

### Complexity
O(n log n) for counting and sorting, O(n) space.

### Python solution
```python
from collections import Counter

def maxItems(input1, input2):
    freq = sorted(Counter(input2).values(), reverse=True)
    total = 0
    limit = float('inf')          # largest count we may still use
    for f in freq:
        take = min(f, limit - 1)
        if take <= 0:
            break
        total += take
        limit = take
    return total
```

### Dry run
Example 2: counts are type 1 -> 3, type 3 -> 2, type 7 -> 2, sorted [3, 2, 2]. Take 3 (limit 3), then min(2, 2) = 2 (limit 2), then min(2, 1) = 1. Total 3 + 2 + 1 = 6.

### Edge cases & pitfalls
- Many types with equal counts: the answer is a triangular-like sum; the loop stops when `take` reaches 0.
- A single type: its entire count.
- Compare with the original array length, not with the number of types (types are values from 1 to n).''')
    add('sigmoid-illuminate-park', G, 'Minimum lamp power to light every bench in a park',
        'A park is a straight line of consecutive blocks. Array A gives the positions (blocks) of benches and array B gives the positions of lamp posts. Each lamp has an adjustable power p, meaning it illuminates every block within distance p on both sides, including its own; the initial power is 0 (only its own block). Find the minimum power that must be assigned so that all benches are lit. Return that integer.',
        None,
        'The needed power is the largest distance from any bench to its nearest lamp. Sort the lamp positions; for each bench binary-search the closest lamp and take the maximum of those distances. O((n + m) log m) time, O(1) extra space; verified against a brute-force search over powers.',
        section='dsa', topic='binary-search', type='coding',
        sources=[g('013541_212'), g('013541_832'), g('013542_071'), g('013548_276'), g('013548_354'), g('013548_435'), g('013548_658')],
        function_signature='minPower(input1, input2, input3, input4)',
        input_format='input1: number of benches. input2: number of lamp posts. input3: bench positions. input4: lamp positions.',
        output_format='An integer: the minimum power.',
        constraints='Bounds are not visible in the photographs.',
        examples=[{'input': 'input1 = 5, input2 = 3, input3 = [6, 7, 8, 9, 10], input4 = [6, 10, 8]', 'output': '1', 'explanation': 'Bench 7 and 9 are one block from a lamp.'},
                  {'input': 'input1 = 6, input2 = 4, input3 = [2, 7, 12, 17, 22, 27], input4 = [5, 10, 15, 20]', 'output': '7', 'explanation': 'Bench 27 is 7 blocks from the lamp at 20.'}],
        notes='The text calls the answer the "minimum power" and the samples show different lamps raised by different amounts, but the returned value (7 in example 2, where the raises are 3, 2, 2 and 7) is the largest raise, so the problem minimises the maximum power. The first sample lists 5 bench positions while saying 6 benches.',
        solution='''### Intuition
A bench is lit when some lamp has power at least its distance to that bench. To minimise the largest power required, each bench should use its nearest lamp, and the answer is the worst such distance.

### Approach
1. Sort the lamp positions.
2. For each bench at position b, binary-search the first lamp at or after b and compare it with the previous lamp. The distance to the nearest lamp is the minimum of the two gaps.
3. The answer is the maximum nearest distance over all benches (0 if there are no benches).

### Why it works
With a uniform power P every bench is lit iff its nearest lamp is within P. The smallest such P is the maximum nearest distance, and giving each lamp only the power it needs cannot reduce the maximum below that value because the farthest bench must still be reached by some lamp. Brute force over powers 0..200 agrees on 300 random cases.

### Complexity
O(m log m) to sort the lamps and O(n log m) for the queries; O(1) extra space.

### Python solution
```python
from bisect import bisect_left

def minPower(input1, input2, input3, input4):
    lamps = sorted(input4)
    ans = 0
    for b in input3:
        i = bisect_left(lamps, b)
        d = float('inf')
        if i < len(lamps):
            d = min(d, lamps[i] - b)      # nearest lamp on the right (or at b)
        if i > 0:
            d = min(d, b - lamps[i - 1])  # nearest lamp on the left
        ans = max(ans, d)
    return ans
```

### Dry run
Example 2: lamps [5, 10, 15, 20]. Distances: bench 2 -> 3, 7 -> 2, 12 -> 2, 17 -> 2, 22 -> 2, 27 -> 7. Maximum is 7.

### Edge cases & pitfalls
- A bench exactly at a lamp has distance 0 (initial power already lights it).
- Benches left of all lamps or right of all lamps use only one side.
- Duplicate lamp positions are harmless; empty bench list returns 0.
- If there are no lamps the problem is infeasible (not covered by the samples).''')
    add('sigmoid-king-george-rescue', G, 'Shortest path through a palace avoiding soldiers',
        'A palace grid contains 1 for the entrance, 2 for the prison cell, -1 for soldiers and 0 for other free cells. William can move in four directions and cannot step on soldiers. Given the grid, find the length of the shortest path (counting the entrance and the prison cell) from the entrance to the cell with 2. If no path exists, return -1. The palace has exactly one entrance and one prison; soldiers are not at either.',
        None,
        'Breadth-first search from the entrance over non-soldier cells; the first time the prison cell is reached, its distance (counted in cells) is the answer, else -1. O(N x M) time and space; verified against a Bellman-Ford style brute force.',
        section='dsa', topic='graphs', type='coding',
        sources=[g('013527_916'), g('013527_941'), g('013528_314')],
        function_signature='shortestRescue(input1, input2, input3)',
        input_format='input1: number of rows. input2: number of columns. input3: the 2-D palace array.',
        output_format='An integer: the length of the shortest path, or -1.',
        constraints='Bounds are not visible in the photographs.',
        examples=[{'input': 'input1 = 4, input2 = 4, input3 = [[1,-1,-1,-1],[0,0,0,0],[0,0,-1,0],[0,0,-1,2]]', 'output': '7'},
                  {'input': 'input1 = 5, input2 = 5, input3 = [[1,-1,-1,-1,-1],[0,-1,-1,-1,-1],[0,-1,0,0,0],[0,-1,0,-1,0],[0,0,0,-1,2]]', 'output': '13'}],
        notes='The entrance marker is hidden by the cursor in the statement photo; the examples show it is 1. In example 2 the second row is read as [0,-1,-1,-1,-1] from the diagram.',
        leetcode={'name': 'Shortest Path in Binary Matrix (4-direction variant)', 'url': 'https://leetcode.com/problems/shortest-path-in-binary-matrix/', 'similarity': 'similar'},
        solution='''### Intuition
Every move costs the same, so the shortest route in a grid with blocked cells is found by breadth-first search. The path length counts cells (the entrance and the prison cell included), so the entrance has length 1.

### Approach
1. Find the cell containing 1 (entrance).
2. Run BFS from it with `dist[entrance] = 1`, moving up, down, left and right to cells that are inside the grid, not -1 and not yet seen.
3. When a popped cell holds 2, return its distance.
4. If the queue empties without reaching 2, return -1.

### Why it works
BFS processes cells in nondecreasing order of distance, so the first time the prison is dequeued its recorded distance is minimal. Soldiers are never entered, so the path avoids them.

### Complexity
O(N x M) time and space since each cell is enqueued once.

### Python solution
```python
from collections import deque

def shortestRescue(input1, input2, input3):
    n, m, g = input1, input2, input3
    start = next((i, j) for i in range(n) for j in range(m) if g[i][j] == 1)
    dist = {start: 1}                       # count cells, entrance = 1
    q = deque([start])
    while q:
        x, y = q.popleft()
        if g[x][y] == 2:
            return dist[(x, y)]
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            a, b = x + dx, y + dy
            if 0 <= a < n and 0 <= b < m and g[a][b] != -1 and (a, b) not in dist:
                dist[(a, b)] = dist[(x, y)] + 1
                q.append((a, b))
    return -1
```

### Dry run
Example 1: from (0,0) go down to (1,0) (length 2), right along row 1 to (1,3) (length 5), down to (2,3) (6) and (3,3) (7) which is the prison. Answer 7.

### Edge cases & pitfalls
- Length counts cells, not moves, so adjacent entrance and prison give 2.
- If the prison is walled in by soldiers return -1.
- Mark cells as seen when enqueued to avoid duplicate work.
- Cells with value 1 and 2 are both walkable; only -1 blocks.''')
    merge('myntra-last-standing', G, [f(27), f(28), f(29), f(50), f(56), f(57), f(58), g('013541_522'), g('013541_622')])

    # ---------------- CS fundamentals ----------------
    add('sigmoid-max-heap-diagram', G, 'Identify the diagram that shows a max heap',
        'Choose the correct diagram from the given options that shows the Max Heap. Option 1: root 95 with children 63 and 52; 63 has children 35 and 15; 52 has children 45 and 25; 35 has children 10 and 4. Option 2: root 95 with children 45 and 63 (further levels not visible). Options 3 and 4: root 63 with children 45 and 95; 45 has children 52 and 35; 95 has children 15 and 10 (or 25 and 4), and 52 has children 25 and 4 (or 15 and 10).',
        'Root 95 with children 63 and 52 (the first diagram)',
        'A max heap must be a complete binary tree where every parent is at least as large as its children. In the first diagram every parent exceeds its children (95 > 63, 52; 63 > 35, 15; 52 > 45, 25; 35 > 10, 4) and levels fill left to right. The diagrams with root 63 are invalid because the child 95 is larger than the root.',
        section='cs', topic='general-cs', type='mcq', confidence='medium',
        sources=[f(17), f(18), f(19), f(20)],
        options=['Root 95; children 63, 52; then 35, 15, 45, 25; then 10, 4 under 35', 'Root 95; children 45 and 63', 'Root 63; children 45 and 95', 'Root 63; children 45 and 95 with a different arrangement below'],
        notes='The option diagrams were photographed in pieces and options 2 to 4 are summarised; only the first diagram satisfies the heap property.',
        solution=S('''A max heap needs two properties.
1. Shape: a complete binary tree (all levels full except possibly the last, filled left to right).
2. Order: every node is greater than or equal to both of its children.

Check the first diagram in level order: 95 | 63, 52 | 35, 15, 45, 25 | 10, 4. The shape is complete. Order: 95 > 63, 52; 63 > 35, 15; 52 > 45, 25; 35 > 10, 4. All hold.

The diagrams with 63 at the root have 95 as a child of 63, which breaks the order property. The second diagram shows root 95 with children 45 and 63 but the rest is cut off in the photo.

**Answer: the first diagram (root 95, children 63 and 52).**''',
                  wrong='Diagrams rooted at 63 fail the order property (95 is a child of 63). The second one is only partially visible.',
                  fast='Look at the root first: in a max heap it must be the largest value in the whole tree.',
                  traps='- Checking only parent-child pairs on one branch.\n- Forgetting that completeness is also required.'))
    add('sigmoid-java-tree-height', G, 'Output of a Java binary tree height program',
        'What will be the output of the following program?\n\n```java\nclass Node {\n    int key;\n    Node left = null, right = null;\n    Node(int key) { this.key = key; }\n}\nclass Main {\n    public static int height(Node root) {\n        if (root == null) { return 0; }\n        return 1 + Math.max(height(root.left), height(root.right));\n    }\n    public static void main(String[] args) {\n        Node root = null;\n        root = new Node(15);\n        root.left = new Node(10);\n        root.right = new Node(20);\n        root.left.left = new Node(8);\n        root.left.right = new Node(12);\n        root.right.left = new Node(16);\n        root.right.right = new Node(25);\n        System.out.print(height(root));\n    }\n}\n```',
        '3', 'The tree is perfect with 7 nodes: root 15, children 10 and 20, and four leaves. The height function counts nodes on the longest root-to-leaf path, which is 3.',
        section='cs', topic='java-output', type='mcq', sources=[f(23), f(24)], options=['2', '3', '4', '5'],
        solution=S('''height(null) = 0, height(leaf) = 1 + max(0, 0) = 1.
- Leaves 8, 12, 16, 25 each have height 1.
- Node 10 = 1 + max(1, 1) = 2; node 20 = 1 + max(1, 1) = 2.
- Root 15 = 1 + max(2, 2) = 3.
The program prints 3 (with print, no newline).

**Answer: 3**''', wrong='2 would be the height counted in edges; 4 and 5 count nonexistent levels.', fast='A perfect tree with 7 nodes has 3 levels.', traps='- Counting edges instead of nodes (that gives 2).'))
    add('sigmoid-java-bubble-sort-parity', G, 'Output of a bubble sort followed by printing i % 2',
        'What will be the output of the following program?\n\n```java\npublic class Main {\n    public static void main(String[] args) {\n        int arr[] = {11, 9, 10, 45, 22};\n        SomeFunction(arr);\n        for (int i : arr) {\n            System.out.println(i % 2);\n        }\n    }\n    static void SomeFunction(int arr[]) {\n        int n = arr.length;\n        for (int i = 0; i < n - 1; i++)\n            for (int j = 0; j < n - i - 1; j++)\n                if (arr[j] > arr[j + 1]) {\n                    int temp = arr[j];\n                    arr[j] = arr[j + 1];\n                    arr[j + 1] = temp;\n                }\n    }\n}\n```',
        '10101', 'SomeFunction is bubble sort (ascending), so arr becomes 9, 10, 11, 22, 45. The remainders mod 2 are 1, 0, 1, 0, 1, printed one per line (the options show them concatenated).',
        section='cs', topic='java-output', type='mcq', sources=[f(25), f(26), g('013535_531')],
        options=['10101', '9 10 11 22 45', '45 22 11 10 9', '00111'],
        solution=S('''1. The nested loops compare adjacent elements and swap when the left is larger: bubble sort in ascending order. The array is modified in place (arrays are passed by reference).
2. Sorted array: 9, 10, 11, 22, 45.
3. The loop prints i % 2: 9 -> 1, 10 -> 0, 11 -> 1, 22 -> 0, 45 -> 1.
4. Output is 1, 0, 1, 0, 1 on separate lines, i.e. the first option.

**Answer: 10101**''', wrong='The second and third options print the array itself, but the loop prints remainders. 00111 would be the remainders of a different order (e.g. 10, 22, 9, 11, 45).', fast='Sort mentally first, then take parity.', traps='- Printing the values instead of i % 2.\n- Missing that the original array (not a copy) is sorted.'))
    add('sigmoid-recursion-product', G, 'Output of a recursive product function Recur(6)',
        'What will be the output of the following program?\n\n```java\npublic class Main {\n    public static void main(String[] args) {\n        System.out.println(Recur(6));\n    }\n    public static int Recur(int num) {\n        if (num == 2) return 2;\n        if (num == 1) return 1;\n        return Recur(num - 1) * Recur(num - 2);\n    }\n}\n```',
        '32', 'Recur(1) = 1, Recur(2) = 2, Recur(3) = 2 x 1 = 2, Recur(4) = 2 x 2 = 4, Recur(5) = 4 x 2 = 8, Recur(6) = 8 x 4 = 32.',
        section='cs', topic='java-output', type='mcq', sources=[g('013534_813')], options=['16', '32', '30', '18'],
        solution=S('''Build values bottom up.
- Recur(1) = 1, Recur(2) = 2
- Recur(3) = Recur(2) x Recur(1) = 2
- Recur(4) = Recur(3) x Recur(2) = 4
- Recur(5) = Recur(4) x Recur(3) = 8
- Recur(6) = Recur(5) x Recur(4) = 32 (the exponents of 2 follow Fibonacci: 1, 1, 2, 3, 5)

**Answer: 32**''', wrong='16 and 18 and 30 come from wrong base values or adding instead of multiplying.', fast='Powers of two: exponents are Fibonacci numbers, 2^5 = 32.', traps='- Using addition like Fibonacci.'))
    add('sigmoid-java-hashtable-order', G, 'Iteration order of a Java Hashtable keySet',
        'What will be the output of the following program?\n\n```java\nimport java.util.*;\nclass Main {\n    public static void main(String[] args) {\n        Hashtable<Integer, Integer> hashtable = new Hashtable<>();\n        hashtable.put(1, 100);\n        hashtable.put(100, 1);\n        hashtable.put(5, 110);\n        hashtable.put(110, 5);\n        hashtable.put(9, 111);\n        hashtable.put(111, 9);\n        Iterator<Integer> itr = hashtable.keySet().iterator();\n        while (itr.hasNext()) {\n            System.out.println(hashtable.get(itr.next()));\n        }\n    }\n}\n```\nThe options list the printed values concatenated.',
        '111 110 9 1 100 5', 'Hashtable has 11 buckets, index = key mod 11, and its iterator walks buckets from the highest index to the lowest, newest entry first within a bucket. Keys map to: 9 -> 9, 5 -> 5, 1, 100 and 111 -> 1, 110 -> 0. Order: 9, 5, 111, 100, 1, 110, so the values printed are 111, 110, 9, 1, 100, 5.',
        section='cs', topic='java-output', type='mcq', sources=[g('013535_204')],
        options=['111 110 9 1 100 5', '111 110 100 9 5', '5 100 1 9 110 111', '100 1 110 5 111 9'],
        confidence='medium',
        notes='Options are read from a tilted photo; the correct order follows from the Hashtable implementation (default capacity 11, no rehash below 8 entries).',
        solution=S('''1. Default capacity is 11, load factor 0.75 (threshold 8), so 6 entries do not trigger a rehash.
2. Bucket index = key mod 11: 1 -> 1; 100 -> 1 (100 = 9 x 11 + 1); 5 -> 5; 110 -> 0; 9 -> 9; 111 -> 1.
3. New entries are inserted at the head of a bucket chain, so bucket 1 reads 111 -> 100 -> 1.
4. The keySet iterator (an Enumerator) goes from table index 10 down to 0, following each chain.
   Order of keys: 9 (bucket 9), 5 (bucket 5), 111, 100, 1 (bucket 1), 110 (bucket 0).
5. Values printed: get(9) = 111, get(5) = 110, get(111) = 9, get(100) = 1, get(1) = 100, get(110) = 5.

**Answer: 111 110 9 1 100 5**''', wrong='The other options assume HashMap-style ascending order or insertion order.', fast='Remember: Hashtable iterates from the last bucket to the first.', traps='- Assuming insertion order (Hashtable and HashMap do not preserve it).\n- Forgetting that chains put the newest entry first.'))
    add('sigmoid-insertion-sort-passes', G, 'Array state after five outer-loop iterations of insertion sort',
        'An array of 10 elements is passed through the insertion sort algorithm. What would be the resultant elements of the array obtained if the algorithm terminates exactly after five executions of the loop?\n\nGiven array: 28, 35, 12, 15, 27, 11, 9, 14, 8, 32. The sorting is in ascending order.',
        '11 12 15 27 28 35 9 14 8 32', 'Each outer iteration inserts the next element into the sorted prefix. After five iterations the first six elements (28, 35, 12, 15, 27, 11) are sorted as 11, 12, 15, 27, 28, 35 and the last four are untouched.',
        section='cs', topic='general-cs', type='mcq', sources=[g('013534_730')],
        options=['12 15 28 35 27 11 9 14 8 32', '12 15 27 28 35 11 9 14 8 32', '11 12 15 27 28 35 9 14 8 32', '9 11 12 15 27 28 35 14 8 32'],
        confidence='medium', notes='Counts one outer-loop execution as one insertion step starting from index 1, so five steps sort the first six elements.',
        solution=S('''Insertion sort treats the first element as a sorted prefix and inserts the elements at indices 1, 2, 3, ... in turn.
- After step 1 (insert 35): 28 35 12 15 27 11 9 14 8 32
- Step 2 (12): 12 28 35 15 27 11 ...
- Step 3 (15): 12 15 28 35 27 11 ...
- Step 4 (27): 12 15 27 28 35 11 ...
- Step 5 (11): 11 12 15 27 28 35 9 14 8 32
The remaining elements 9, 14, 8, 32 are untouched.

**Answer: 11 12 15 27 28 35 9 14 8 32**''', wrong='The first and second options stop after 2 and 4 steps; the fourth has already inserted 9 (a sixth step).', fast='After k steps the first k+1 elements are sorted and the rest unchanged.', traps='- Counting the first element as a step (that gives the 4-step result).'))
    add('sigmoid-hash-linear-probe-order', G, 'Possible insertion order for a linear-probing hash table',
        'Consider a hash table with hash function h(k) = k mod 10 that uses linear probing for collision resolution. Suppose the keys 26, 22, 24, 32, 33, 23 are inserted into the empty table in some order and the final state is: index 2: 22, index 3: 33, index 4: 24, index 5: 32, index 6: 26, index 7: 23. What is the correct order in which the values could have been inserted?',
        '26, 24, 22, 33, 32, 23', 'Simulate the order 26, 24, 22, 33, 32, 23: 26 goes to 6, 24 to 4, 22 to 2, 33 to 3, 32 collides at 2, 3, 4 and lands in 5, 23 collides at 3, 4, 5, 6 and lands in 7, which matches the table.',
        section='cs', topic='general-cs', type='mcq', confidence='medium', sources=[g('013534_731')],
        options=['22, 33, 32, 23, 26, 24', '32, 23, 22, 33, 26, 24', '26, 24, 22, 33, 32, 23', '22, 32, 26, 24, 23, 33'],
        notes='The photographed stem says "the length of the table is 15 (or 10) and ..."; a table of size 10 with hash mod 10 is assumed, which matches the final layout shown.',
        solution=S('''Test each order by simulating linear probing.
1. 22, 33, 32, 23, 26, 24: 22 -> 2, 33 -> 3, 32 -> 2 taken, 3 taken, so 4 (but the target layout has 24 at 4). Fails.
2. 32, 23, 22, 33, 26, 24: 32 goes to 2, but the table has 22 at 2. Fails.
3. 26, 24, 22, 33, 32, 23: 26 -> 6; 24 -> 4; 22 -> 2; 33 -> 3; 32 -> 2, 3, 4 taken, so 5; 23 -> 3, 4, 5, 6 taken, so 7. Matches the table.
4. 22, 32, 26, 24, 23, 33: 32 would go to 3 (2 taken), but the table has 33 at 3. Fails.

**Answer: 26, 24, 22, 33, 32, 23**''', wrong='See the failure points in 1, 2 and 4.', fast='Keys sitting away from their home slot (32 at 5, 23 at 7) must have been inserted after the keys that block them (22, 33, 24 and 26).', traps='- Forgetting that probing wraps over occupied slots one at a time.'))
    add('sigmoid-linked-list-remove-last', G, 'Missing step when removing the last node of a singly linked list',
        'You are working on a project involving a linked list data structure. The project requires you to implement a method to remove the last element of the linked list. You have implemented the method, but after running some tests, you notice it is not working as expected. The last element is not being removed from the list. After reviewing your code, you realize you missed a crucial step. What step did you forget to implement?',
        'Traverse to the second last element before removing the last element', 'In a singly linked list you can only remove the last node by changing the next pointer of the second last node to null. Without traversing to the second last element, the last node stays linked.',
        section='cs', topic='general-cs', type='mcq', sources=[g('013534_807')],
        options=['Traverse to the second last element before removing the last element', 'Traverse to the third last element before removing the last element', 'Traverse to the fourth last element before removing the last element', 'Traverse to the first element before removing the last element'],
        solution=S('''A singly linked list node knows only its successor. To delete the tail you must set `secondLast.next = null` (and update the tail pointer if one is kept). The second last node is found by walking until `node.next.next == null`.

**Answer: Traverse to the second last element before removing the last element.**''', wrong='The third or fourth last node is not adjacent to the tail, so its next pointer cannot detach the last node; the first element is the head, which is only right for a one-element list.', fast='To delete a node you always need its predecessor.', traps='- Moving the tail pointer without clearing the previous node\'s next field.'))
    add('sigmoid-binary-search-missing', G, 'Binary search for the first missing element in a sorted list',
        'A sorted list of ten numbers is given as A = [0, 1, 2, 3, 4, 5, 6, 8, 9, 10]. The requirement is to find the first missing element index; in this case 7 is the missing element. Select the correct binary search algorithm for the above requirement.',
        '1. Compare the middle value and middle index. 2. If both are same, the missing element is in the right side list. 3. If both are different, the missing element is in the left side array. 4. Repeat the step until the missing element is found. 5. Return the index of element.',
        'Before the missing value, A[i] == i; from the missing value onward, A[i] > i. Compare the middle value with its index: equal means the gap is on the right, different means the gap is at or to the left of the middle. Repeat to narrow down.',
        section='dsa', topic='binary-search', type='mcq', confidence='medium', sources=[g('013534_808')],
        options=['1. Divide the list in two equal parts. 2. Compare the index of each element. 3. Return the missing index of element.', '1. Divide the list in two equal parts. 2. If both are same, the missing element is in the right side list. 3. If both are different, the missing element is in the left side array. 4. Repeat the step until the missing element is found. 5. Return the index of element.', '1. Compare the middle value and middle index. 2. If both are same, the missing element is in the right side list. 3. If both are different, the missing element is in the left side array. 4. Find the missing element. 5. Return the index of element.', '1. Compare the middle value and middle index. 2. If both are same, the missing element is in the right side list. 3. If both are different, the missing element is in the left side array. 4. Repeat the step until the missing element is found. 5. Return the index of element.'],
        notes='The last two options differ only in step 4 ("Find the missing element" vs "Repeat the step until..."); binary search needs repetition.',
        solution=S('''Observation: for i before the missing value, A[i] = i. At and after the first missing value, A[i] = i + 1 (here), so A[i] > i.
1. Compare A[mid] with mid. If equal, all elements up to mid are in place, so the missing value is on the right.
2. If different, the missing value is at mid or on the left, so move left.
3. The search must repeat on the reduced range until the range has one element. Here A[7] = 8 != 7, so the first missing value is 7 at index 7.

The last option states these steps and includes the repeat step. The third option omits the repeat, so it is only one comparison, not a binary search.

**Answer: the last option (compare middle value and middle index, right if same, left if different, repeat, return the index).**''',
                  wrong='Options 1 and 2 split the list without comparing the middle value to its index (option 2 also never defines the comparison); option 3 does not repeat.',
                  fast='The loop invariant "A[i] == i on the left side" is the key; everything else follows.', traps='- Searching for the value instead of using value-index equality.'))
    add('sigmoid-bst-insertion-worst-case', G, 'Worst case of insertion in a binary search tree',
        'Given are two statements about the insertion operation in a binary search tree. Which of these is/are correct?\nA) The worst case happens when the given keys are sorted in ascending or descending order.\nB) The worst case happens when all the nodes except the leaf have one and only one child.',
        'Both A and B', 'Sorted keys make a skewed (linked-list) tree, and in a skewed tree every non-leaf node has exactly one child. Both describe the same worst case, where each insertion takes O(n).',
        section='cs', topic='general-cs', type='mcq', sources=[g('013535_347')], options=['Only A', 'Only B', 'Both A and B', 'Neither A nor B'],
        solution=S('''1. Inserting keys in ascending order always goes right, descending always goes left. The tree becomes a chain of height n, and each insertion walks the whole chain: O(n).
2. A chain is exactly a tree where every node except the leaf has one child, so statement B is the structural description of the same worst case. (A tree with one-child nodes in zig-zag order is also height n, so B is a valid worst-case shape.)
Both statements are correct.

**Answer: Both A and B**''', wrong='Only A or Only B each leave out a correct statement; Neither is false.', fast='Worst case for a BST = height n = skewed tree.', traps='- Thinking B is wrong because the chain does not go in one direction; any one-child-per-node shape has height n.'))
    add('sigmoid-tail-recursion-depth', G, 'Call-stack depth for a tail-recursive factorial with tail-call optimisation',
        'Assuming f(n) is a function that returns the factorial of a number n, if f(n) is implemented recursively and the compiler is capable of optimizing tail recursion, what would be the maximum depth of the call stack, at any given time, created by the call f(10)?',
        '1', 'With tail-call optimisation the compiler reuses the same stack frame for each recursive call, so the call stack depth stays at 1.',
        section='cs', topic='general-cs', type='mcq', confidence='medium', sources=[g('013534_617')], options=['10', '11', '1', '2'],
        notes='The question assumes the factorial is written in tail-recursive form (with an accumulator).',
        solution=S('''A tail call is a call that is the last action of the function, so its caller\'s frame is no longer needed. A compiler that optimises tail calls replaces the call by a jump and reuses the frame, turning the recursion into a loop. The depth therefore stays at one frame for f(10).
Without optimisation the depth would be 10 (or 11 with the base case call).

**Answer: 1**''', wrong='10 and 11 are the depths without optimisation; 2 would need an extra permanent frame.', fast='TCO means O(1) stack space.', traps='- Counting n frames out of habit.'))

    # ---------------- reasoning ----------------
    add('sigmoid-syllogism-giraffe', G, 'Syllogism: giraffes, short and dogs',
        'Two statements are given, followed by two conclusions. Assuming the statements to be true, decide which conclusion logically follows, disregarding commonly known facts.\n\nAll giraffe are short. All short are dogs.\nConclusion 1: Some giraffe are dogs.\nConclusion 2: Some dogs are short.',
        'Both conclusions follow', 'All giraffe are short and all short are dogs, so all giraffe are dogs, which implies some giraffe are dogs. "All short are dogs" also implies some dogs are short (the converse of an A statement gives an I statement when the class is non-empty).',
        section='aptitude', topic='logical', type='mcq', confidence='medium', sources=[f(36)],
        options=['Only conclusion 1 follows', 'Only conclusion 2 follows', 'Either 1 or 2 follows', 'Neither follows', 'Both conclusions follow'],
        notes='The answer options were not captured; they are the standard five.',
        solution=S('''1. Giraffe ⊂ Short ⊂ Dogs, so Giraffe ⊂ Dogs. "All giraffe are dogs" gives "Some giraffe are dogs": conclusion 1 follows.
2. "All short are dogs" gives "Some dogs are short" by conversion (the subset is non-empty): conclusion 2 follows.

**Answer: Both conclusions follow**''', wrong='Dropping either conclusion ignores a valid inference.', fast='Draw nested circles: giraffe inside short inside dogs.', traps='- Treating "some dogs are short" as unsupported because the statement says "all short are dogs" (the converse of an A statement is I).'))
    add('sigmoid-coding-sixteen', G, 'Digit coding: TEN and SIXTY to SIXTEEN',
        'In a certain coding system, \'TEN\' is coded as 256 and \'SIXTY\' is coded as 19827. How will you code \'SIXTEEN\'?',
        '1982556', 'From TEN = 256: T = 2, E = 5, N = 6. From SIXTY = 19827: S = 1, I = 9, X = 8, T = 2, Y = 7. So SIXTEEN = S I X T E E N = 1 9 8 2 5 5 6 = 1982556.',
        section='aptitude', topic='logical', type='numeric', confidence='medium', sources=[f(39)],
        notes='The answer options were not captured; the value is derived.',
        solution=S('''Match letters with digits position by position.
- TEN -> 2, 5, 6 gives T = 2, E = 5, N = 6.
- SIXTY -> 1, 9, 8, 2, 7 gives S = 1, I = 9, X = 8, T = 2 (consistent with TEN), Y = 7.
- SIXTEEN = S, I, X, T, E, E, N = 1, 9, 8, 2, 5, 5, 6.

**Answer: 1982556**''', fast='Write a letter-to-digit table and read off the word.', traps='- Forgetting that E repeats.'))
    add('sigmoid-coding-better', G, 'Digit coding: BAT, CAT, ARE to BETTER',
        'In a certain coding system, \'BAT\' is coded as 283 and \'CAT\' is coded as 383; \'ARE\' is coded as 801. How will you code \'BETTER\'?',
        '213310', 'BAT = 283 and CAT = 383 give B = 2, C = 3, A = 8, T = 3. ARE = 801 gives A = 8, R = 0, E = 1. BETTER = B E T T E R = 2 1 3 3 1 0 = 213310.',
        section='aptitude', topic='logical', type='numeric', confidence='medium', sources=[f(40)],
        notes='The answer options were not captured; the value is derived.',
        solution=S('''- BAT = 283: B = 2, A = 8, T = 3.
- CAT = 383: C = 3, A = 8, T = 3 (T is consistent).
- ARE = 801: A = 8, R = 0, E = 1.
- BETTER = B, E, T, T, E, R = 2, 1, 3, 3, 1, 0.

**Answer: 213310**''', fast='Compare words that differ in one letter (BAT and CAT) to read off letters quickly.', traps='- Taking T = 3 twice but E from the wrong word.'))

    skip(G, f(22), 'library caching problem, statement not captured')
