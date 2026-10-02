"""Worker A, module 02: Google (all 20 remaining files)."""
from a_sol import sol


def extend(add, alias):
    alias('b07_google_uber_li_ms-002', 'Google', ['IMG-20240804-WA0006.jpg', 'IMG-20240804-WA0010.jpg', 'IMG-20240804-WA0011.jpg', 'IMG-20240804-WA0012.jpg',
          'IMG-20240804-WA0021.jpg', 'IMG-20240804-WA0022.jpg', 'IMG-20240804-WA0034.jpg', 'IMG-20240804-WA0093.jpg'])
    alias('b07_google_uber_li_ms-004', 'Google', ['IMG-20240804-WA0023.jpg', 'IMG-20240804-WA0094.jpg', 'IMG-20240804-WA0095.jpg', 'IMG-20240804-WA0096.jpg', 'IMG-20240804-WA0097.jpg'])

    add('google-median-path', 'Google', 'Sum of medians over all odd-length root paths in a tree',
        'You are given a tree of $n$ nodes and $n-1$ edges, and an array $C$ of length $n$ where $C_i$ is the value of node $i$. Calculate the sum of the medians of every simple path of odd length starting from node 1 (the median of the node values on the path). 1-based indexing is used. The median is the middle number of the sorted list of values. A simple path has no repeated vertices.\n\nImplement `solve(n, C, edges)`.',
        None,
        'Every simple path from node 1 is a root-to-node path, and an odd length means an odd number of nodes (the path 1->1 counts). DFS from node 1 while keeping the path values in a Fenwick tree over compressed values; at odd depth, the median is the ((d+1)/2)-th smallest, found by Fenwick descent. O(n log n).',
        section='dsa', topic='trees', type='coding', hard=True,
        sources=['IMG-20240727-WA0027.jpg', 'IMG-20240727-WA0028.jpg', 'IMG-20240727-WA0029.jpg', 'IMG-20240727-WA0030.jpg', 'IMG-20240727-WA0031.jpg'],
        function_signature='int solve(int n, vector<int> C, vector<vector<int>> edges)',
        input_format='T test cases. Each: n; then n node values; then n-1 lines with an edge (u v).',
        output_format='For each test case, the sum of medians on its own line.',
        constraints='1 ≤ T < 10; 1 ≤ n ≤ 10⁵; 1 ≤ C_i ≤ 10⁹.',
        examples=[{'input': 'n = 6, C = [1, 2, 4, 3, 1, 5], edges = [(1,4),(4,2),(4,3),(4,5),(1,6)]', 'output': '7', 'explanation': 'Paths: [1] median 1; 1-4-2 values {1,3,2} median 2; 1-4-3 values {1,3,4} median 3; 1-4-5 values {1,3,1} median 1. Total 1+2+3+1 = 7.'},
                  {'input': 'n = 5, C = [7, 6, 9, 10, 1], edges = [(1,2),(2,3),(1,4),(2,5)]', 'output': '20', 'explanation': 'Paths [7], 7-6-9 (median 7), 7-6-1 (median 6): 7 + 7 + 6 = 20.'}],
        notes='The sample input of the form "2 / 5 / 7 6 9 10 1 / edges ... / 6 / 1 2 4 3 1 5 / edges" gives outputs 20 and 7. The tree of the worked example was read from a drawing: edges 1-4, 1-6, 4-2, 4-3, 4-5.',
        solution=sol('google-median-path',
            'In a tree, the simple paths starting at node 1 are exactly the root-to-node paths, one per node. We only need the nodes whose root path has an odd number of nodes, and for each the median of the values on that path.',
            ['Compress node values to ranks 1..m and keep a Fenwick tree of counts of the values on the current root path.', 'DFS from node 1 (iteratively, since depth can be 10⁵). On entering a node, add its value; on leaving, remove it.', 'When the depth d (number of nodes on the path) is odd, the median is the ((d+1)/2)-th smallest value. Find it with a binary descent over the Fenwick tree.', 'Add the median to the answer.'],
            'The Fenwick tree always holds exactly the multiset of values on the path from the root to the current node (insert on entry, delete on exit). The k-th smallest of that multiset is the median at odd d by definition. Each node is visited once, so every root path is covered.',
            'O(n log n) time (one update on entry and exit, one k-th query per odd node); O(n) space.',
            'Sample 2 (n=6): depth-1 node 1 -> median 1. Node 4 (depth 2) is skipped. Nodes 2, 3, 5 at depth 3: multiset {1,3,2}, {1,3,4}, {1,3,1} -> medians 2, 3, 1. Node 6 at depth 2 is skipped. Sum 7.',
            ['The path 1->1 (a single node) counts and has odd length.', 'Do not use recursion: a chain of 10⁵ nodes overflows the Python/C++ stack.', 'Values repeat; the Fenwick tree stores counts, so duplicates are fine.', 'The sum can reach 10⁵ · 10⁹, so use 64-bit.']))

    add('google-reckon-strings', 'Google', 'Count strings with no adjacent pair of related characters',
        'You are given an integer $N$ and $M$ pairs of distinct lowercase letters. A pair holds a relation between two letters, and the relation is transitive: if (u, v) and (v, w) are related then (u, w) is related too. Related characters cannot occur next to each other in the formed string. Count the strings of length $N$ over the 26 lowercase letters in which no two adjacent characters (that are different letters) hold a relation. Output the answer modulo $10^9+7$.',
        None,
        'Transitivity makes the relation "same connected component" of the pairs graph. Two adjacent different letters in one component are forbidden; equal letters are allowed. DP over letters: f[c] = strings ending in c. The next letter c can follow any letter outside its component, or c itself, so f_new[c] = total - compSum[comp(c)] + f[c].',
        section='dsa', topic='dp', type='coding',
        sources=['12.23.41_e05c7cb9.jpg', '12.23.44_201c5e27.jpg'],
        function_signature='int solve(int N, int M, vector<vector<char>> pairs)',
        input_format='N, M, then M pairs of characters.', output_format='The count modulo 10⁹+7.',
        constraints='Not visible (cropped).',
        examples=[{'input': 'N = 2, M = 3, pairs = [[a,b],[b,c],[c,d]]', 'output': '664', 'explanation': 'a,b,c,d are in one component, so the 12 ordered pairs of distinct letters among them are forbidden: 26·26 − 12 = 664 strings.'}],
        confidence='medium',
        notes='The final output of the sample is cropped in the screenshot; 664 follows from the visible explanation that exactly the 12 ordered pairs of distinct letters in {a,b,c,d} are forbidden. Constraints on N are not visible: the O(26·N) DP works for N up to about 10⁶-10⁷; for larger N use a 26×26 matrix power.',
        solution=sol('google-reckon-strings',
            'The statement hides a union-find problem: by transitivity, letters in the same connected component of the pairs graph are all mutually related, so two different letters of one component may never be adjacent. Letters not mentioned in any pair are free.',
            ['Union the letters of each pair (DSU of 26 nodes).', 'Let f[c] be the number of valid strings of the current length that end in letter c; initially f[c] = 1.', 'For each next position: total = sum f, and compSum[k] = sum of f over component k.', 'New f[c] = total - compSum[comp(c)] + f[c]: all letters outside c\'s component are allowed predecessors, plus c itself (equal letters are not a pair of distinct characters).', 'After N-1 steps the answer is sum f modulo 10⁹+7.'],
            'A string is valid iff every adjacent pair (x, y) satisfies x = y or comp(x) != comp(y). The DP counts strings by their last letter, so each valid string is counted exactly once, and the transition enumerates exactly the allowed predecessors of each letter.',
            'O(26·N + M) time, O(26) space. For huge N use fast exponentiation of the 26×26 transition matrix: O(26³ log N).',
            'N = 2 with the four related letters: after step 1, f = 1 for all letters, total = 26. For letter a, compSum = 4 so f_new[a] = 26 - 4 + 1 = 23; the same for b, c, d. The other 22 letters give 26 each. Total = 4·23 + 22·26 = 92 + 572 = 664 = 26·26 - 12.',
            ['A letter may follow itself even if it belongs to a non-trivial component ("aa" is allowed).', 'Mod arithmetic: use ((total - compSum + f) % MOD + MOD) % MOD in languages with negative remainders.', 'Pairs are distinct characters, so there are no self-pairs.', 'N = 1 gives 26.']))
