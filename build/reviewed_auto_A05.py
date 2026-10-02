"""Worker A, module 05: PayPal (all 26 files)."""
from a_sol import sol


def extend(add):
    add('paypal-lex-smallest-string', 'PayPal', 'Lexicographically smallest input string for a fixed-length data generation tool',
        'A data scientist trains a language model that needs a specific set of characters, some of which are missing from the dataset; the missing characters are given as a string `dataToBeGenerated`. A tool can generate multiple copies of a given string. It can only generate strings of a fixed length $n$ and accepts one input string to generate the missing data. Each generated string incurs a cost, so more copies cost more. Find the lexicographically smallest input string (of length $n$) that, when fed into the tool, produces datasets containing all the required characters while minimising the total cost (the number of copies). If it is not possible, return "-1" as a string.\n\nExample: n = 2, dataToBeGenerated = "aavvavv": the character a appears 3 times and v appears 4 times. There are two distinct characters and the input string must have length 2, so it can only be "av" or "va"; four copies are required in either case, and the answer is "av" (lexicographically smaller).',
        '"av" for n = 2, dataToBeGenerated = "aavvavv"; "aab" for n = 3, "aabaabba"',
        'With k copies of a string s whose letter counts are m_c, we get k·m_c of each letter, so we need m_c >= ceil(need_c / k). The total of these minimal counts must fit in n slots. The cost k is minimal when sum of ceil(need_c / k) <= n first holds, found by binary search (the sum is non-increasing in k). Fill the remaining slots with the smallest letter a and sort the letters ascending.',
        section='dsa', topic='strings', type='coding',
        sources=['IMG-20240919-WA0002.jpg', 'IMG-20240919-WA0005.jpg', 'IMG-20240919-WA0006.jpg', 'IMG-20240919-WA0008.jpg', 'IMG-20240919-WA0010.jpg', 'IMG-20240919-WA0011.jpg',
                 'IMG-20240919-WA0012.jpg', 'IMG-20240919-WA0013.jpg', 'IMG-20240919-WA0014.jpg', 'IMG-20240919-WA0015.jpg', 'IMG-20240919-WA0016.jpg', 'IMG-20240919-WA0017.jpg',
                 'IMG-20240919-WA0018.jpg', 'IMG-20240919-WA0019.jpg', 'IMG-20240919-WA0020.jpg', 'IMG-20240919-WA0021.jpg', 'IMG-20240919-WA0022.jpg', 'IMG-20240919-WA0023.jpg',
                 'IMG-20240919-WA0024.jpg', 'IMG-20240919-WA0025.jpg', 'IMG-20240919-WA0026.jpg'],
        function_signature='string getLexSmallestString(int n, string dataToBeGenerated)',
        input_format='n; then the string dataToBeGenerated.', output_format='The lexicographically smallest string of length n, or "-1".',
        constraints='1 ≤ n ≤ 2·10⁵; dataToBeGenerated contains lowercase letters (its length bound is not visible).',
        examples=[{'input': 'n = 2, dataToBeGenerated = "aavvavv"', 'output': 'av', 'explanation': 'a needs 3 copies and v needs 4 copies; with "av" 4 copies cover both.'},
                  {'input': 'n = 3, dataToBeGenerated = "aabaabba"', 'output': 'aab', 'explanation': 'a appears 5 times and b 3 times. "aab" needs 3 copies; "abb" would need 5.'},
                  {'input': 'n = 4, dataToBeGenerated = "abacbca"', 'output': 'aabc', 'explanation': 'a:3, b:2, c:2. Two copies of "aabc" provide 4 a, 2 b, 2 c.'}],
        confidence='medium',
        notes='The expected output of the first custom sample is not visible; "aabc" follows from the rules. The statement describes the tool as producing "multiple copies of a string", interpreted as k independent copies whose letters are pooled.',
        solution=sol('paypal-lex-smallest-string',
            'If the input string s has m_c copies of letter c, then k copies of s supply k·m_c copies of c. So a letter that must appear need_c times requires m_c >= ceil(need_c / k). The string has only n positions, so the demands must fit: sum over letters of ceil(need_c / k) <= n. We want the smallest k (cost), and then the smallest string.',
            ['Count the letters of dataToBeGenerated. If the number of distinct letters exceeds n, return "-1" (even k = max count would need more than n slots).', 'The function f(k) = sum ceil(need_c / k) is non-increasing in k. Binary search the smallest k in [1, max need] with f(k) <= n.', 'For that k put ceil(need_c / k) copies of each required letter into the string; the n - f(k) spare positions can hold any letter.', 'To be lexicographically smallest, fill the spare positions with "a" and sort the whole multiset ascending.'],
            'Feasibility of a count vector m is exactly m_c >= ceil(need_c / k) for all required c, and the cost of m is max_c ceil(need_c / m_c). The minimal feasible k is the smallest one with f(k) <= n. For that k, every valid string contains at least the demanded counts; among strings with a given multiset the sorted arrangement is the lexicographically smallest, and replacing any spare position by "a" can only decrease the sorted string. A brute-force search over all strings of length n ≤ 5 on a 4-letter alphabet agrees on 300 random inputs.',
            'O(L + 26 log L) to count the letters and binary search (L = |dataToBeGenerated|), then O(n) to build the string; O(n) space.',
            'n=3, data = "aabaabba": need a=5, b=3. f(1) = 8 > 3; f(2) = 3 + 2 = 5 > 3; f(3) = 2 + 1 = 3 <= 3. So k = 3, string letters a, a, b → "aab".',
            ['More distinct letters than n is impossible: return the string "-1".', 'Spare positions get "a", not necessarily a required letter.', 'Do not minimise the string first: the cost k is minimised before lexicographic order.', 'Use ceiling division; floor undercounts the copies.']))

    add('paypal-bandwidth-calculation', 'PayPal', 'Total bandwidth for concurrent HD streams',
        'A video streaming service provides movies in HD quality, each stream consuming a bandwidth of 4 Mbps. If the service has 10,000 concurrent users streaming video, what is the total bandwidth required for the service to function smoothly?',
        '40 Gbps',
        '10,000 streams × 4 Mbps = 40,000 Mbps = 40 Gbps.',
        options=['4 Gbps', '40 Gbps', '400 Gbps', '400 Mbps'],
        section='cs', topic='networks', type='mcq', confidence='medium',
        sources=['IMG-20240919-WA0000.jpg'],
        notes='The statement is partly cut at the edge of the photo; the user count 10,000 and the rate 4 Mbps were read from the visible text.',
        solution='### Solution\nEach stream needs 4 Mbps and there are 10,000 concurrent streams, so the total is\n\n10,000 × 4 Mbps = 40,000 Mbps.\n\nConvert to gigabits: 1 Gbps = 1,000 Mbps (decimal units are used for network rates), so 40,000 Mbps = 40 Gbps.\n\n**Answer: 40 Gbps**\n\n### Why the other options are wrong\n- 4 Gbps: this would be only 1,000 users at 4 Mbps.\n- 400 Gbps: ten times too large (a slip of one decimal place).\n- 400 Mbps: that supports only 100 streams.\n\n### Faster method\n10⁴ × 4 = 4 × 10⁴ Mbps; dividing by 10³ gives 4 × 10 = 40 Gbps. Count the powers of ten: Mbps -> Gbps is ÷10³.\n\n### Common traps\n- Using 1024 instead of 1000 for the unit conversion (network rates are decimal).\n- Confusing Mbps (megabits) with MBps (megabytes).\n- Forgetting the extra zero from 10,000 users.\n')

    add('paypal-lru-cache', 'PayPal', 'Final contents of a 3-item LRU cache',
        'Consider a caching system that uses the LRU (Least Recently Used) cache replacement policy. The cache size is limited to 3 items. The following sequence of items is accessed: A, B, C, A, D, E. After these accesses, which items are in the cache?',
        'A, D, E',
        'Track recency. A, B, C fill the cache. Accessing A is a hit and makes A the most recent. D evicts the least recently used item B. E evicts the least recently used item, C. The cache holds A, D, E.',
        options=['A, C, E', 'A, D, E', 'B, D, E', 'C, D, E'],
        section='cs', topic='general-cs', type='mcq',
        sources=['IMG-20240919-WA0003.jpg'],
        solution='### Solution\nKeep the cache as an ordered list from least to most recently used.\n\n| Access | Hit/miss | Cache (LRU -> MRU) |\n|---|---|---|\n| A | miss | A |\n| B | miss | A, B |\n| C | miss | A, B, C |\n| A | hit, A becomes most recent | B, C, A |\n| D | miss, full: evict LRU = B | C, A, D |\n| E | miss, full: evict LRU = C | A, D, E |\n\n**Answer: A, D, E**\n\n### Why the other options are wrong\n- A, C, E: C was evicted by E, since C was least recently used at that moment.\n- B, D, E: B was evicted by D; the earlier hit on A refreshed A.\n- C, D, E: would be right for FIFO-like behaviour only if A had not been refreshed; A is kept because it was used again.\n\n### Faster method\nThe cache after the last access holds the 3 most recently used distinct items. Reading the sequence from the end: E, D, A (then B/C would be older). So {A, D, E}.\n\n### Common traps\n- Treating the policy as FIFO: that would evict A (first in) when D arrives.\n- Forgetting that a hit updates recency.\n')

    add('paypal-o1-tasks', 'PayPal', 'Which tasks take constant time? (select all that apply)',
        'An example of an O(1) task is... (pick one or more options)',
        'Printing a character to screen; Incrementing a variable',
        'Printing a single character and incrementing a variable take a fixed number of steps, O(1). Inserting into a binary search tree costs O(h) (O(log n) balanced, O(n) worst), and adding at the beginning of an array shifts all n elements, O(n).',
        options=['Printing a character to screen', 'Incrementing a variable', 'Inserting a node in non-empty binary search tree', 'Adding element at the beginning of non-empty array'],
        section='cs', topic='general-cs', type='mcq', confidence='medium',
        sources=['IMG-20240919-WA0004.jpg'],
        notes='Multiple-select question: the correct options are the first two. The screenshot does not show the official answer.',
        solution='### Solution\nA task is O(1) if its cost does not depend on the input size.\n\n- Printing a character to the screen: one fixed operation. O(1). Correct.\n- Incrementing a variable: one arithmetic operation. O(1). Correct.\n- Inserting a node in a non-empty BST: walk down from the root to a leaf, O(height): O(log n) for a balanced tree and O(n) for a skewed one. Not O(1).\n- Adding an element at the beginning of a non-empty array: all existing elements shift one place, O(n). Not O(1).\n\n**Answer: Printing a character to screen; Incrementing a variable**\n\n### Why the other options are wrong\n- BST insertion depends on the height of the tree.\n- Insertion at the front of an array moves n elements (it would be O(1) only for a linked list or a deque).\n\n### Faster method\nAsk "does the work grow with n?". Only the first two do not.\n\n### Common traps\n- Treating "insert" as O(1) because the final pointer assignment is O(1), ignoring the search/shift.\n- Confusing array front insertion with linked-list head insertion.\n')

    add('paypal-log-loop-complexity', 'PayPal', 'Time complexity of a doubling loop',
        'What is the complexity of the following code snippet?\n\n```c\nint a = 1;\nwhile (a < n) {\n    a = a * 2;\n}\n```',
        'O(log2 N)',
        'a takes the values 1, 2, 4, 8, ... and the loop stops once a >= n, which needs about log2(n) doublings, so the loop runs O(log n) times.',
        options=['O(n)', 'O(1)', 'O(log2 N)', 'O(2^n)'],
        section='cs', topic='general-cs', type='mcq',
        sources=['IMG-20240919-WA0007.jpg'],
        solution='### Solution\nTrace a: after the i-th iteration a = 2^i. The loop continues while a < n, i.e. 2^i < n, so it stops at the first i with 2^i >= n, namely i = ceil(log2 n). Each iteration does O(1) work, so the total is O(log2 n).\n\nExample: n = 100 gives a = 1, 2, 4, 8, 16, 32, 64, 128: 7 iterations = ceil(log2 100).\n\n**Answer: O(log2 N)**\n\n### Why the other options are wrong\n- O(n): would need a to grow by a constant (a = a + 1).\n- O(1): the number of iterations grows with n.\n- O(2^n): the exponent is on the number of iterations in the wrong direction; here the value of a is exponential in the iteration count, not the other way round.\n\n### Faster method\nWhenever the loop variable is multiplied (or divided) by a constant each step, the iteration count is logarithmic.\n\n### Common traps\n- Confusing a *= 2 with a += 2 (the latter is O(n)).\n- Counting a in the exponent: the number of iterations is log n, not 2^n.\n')

    add('paypal-level-order-queue', 'PayPal', 'Data structure for level-order traversal',
        'A level-order traversal in a binary tree requires which data structure?',
        'Queue',
        'Level-order (breadth-first) traversal visits nodes level by level in first-in-first-out order: enqueue the root, then repeatedly dequeue a node, visit it and enqueue its children. A stack would give depth-first order.',
        options=['Stack', 'Doubly Linked List', 'Queue', 'Circular Linked List'],
        section='dsa', topic='trees', type='mcq',
        sources=['IMG-20240919-WA0009.jpg'],
        solution='### Solution\nLevel-order traversal visits all nodes at depth 0, then depth 1, then depth 2, and so on. Children are discovered while processing their parents and must be processed in the same order they were discovered: first discovered, first processed. That is FIFO, i.e. a queue.\n\nAlgorithm: enqueue(root); while the queue is not empty: node = dequeue(); visit(node); enqueue its left child, then its right child.\n\nOn a tree with root 1, children 2 and 3: queue [1] -> visit 1, queue [2, 3] -> visit 2, queue [3, (children of 2)] -> ... which yields 1, 2, 3, ...\n\n**Answer: Queue**\n\n### Why the other options are wrong\n- Stack: LIFO gives depth-first traversals (pre/in/post-order).\n- Doubly linked list and circular linked list: these are underlying storage structures, not the abstract access discipline needed; a queue can be built on them but the requirement is FIFO.\n\n### Faster method\nBFS = queue, DFS = stack (or recursion).\n\n### Common traps\n- Choosing a stack because tree traversals are usually recursive: only the depth-first ones are.\n')
