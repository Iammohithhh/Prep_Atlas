"""SAP Labs (SHL/AMCAT coding assessment): four coding problems."""


def extend(add, merge, skip, alias):
    S = 'SAP Labs'

    add('sap-flip-bits', S, 'Minimum bits to flip to convert message P to message Q',
        'An agent sends a secret message to headquarters. One soft copy is sent to the agency\'s computer (P) and one hard copy by fax to Roger (Q). During transmission some bits of P get distorted. Roger compares the binary values and checks how many bits must be flipped to convert message P into message Q. Write an algorithm to find the minimum number of bits that must be flipped to convert P to Q.',
        None,
        'The bits that differ are the 1-bits of P xor Q, so the answer is the popcount of the XOR. For negative inputs use a fixed 32-bit two\'s complement view. O(1) time and space; checked on the sample and negative cases.',
        section='dsa', topic='bit-manipulation', type='coding', sources=['Copy of IMG-20240825-WA0006.jpeg', '20240825_100411.jpg'],
        function_signature='flippedBits(num1, num2)',
        input_format='Line 1: integer num1 (message P). Line 2: integer num2 (message Q).',
        output_format='One integer: the minimum number of bit flips.',
        constraints='-10^4 <= num1, num2 <= 10^9.',
        examples=[{'input': '7\n10', 'output': '3', 'explanation': 'P = 00000111, Q = 00001010 differ in 3 bit positions.'}],
        leetcode={'name': 'Minimum Bit Flips to Convert Number', 'url': 'https://leetcode.com/problems/minimum-bit-flips-to-convert-number/', 'similarity': 'same'},
        notes='The constraint line is printed as -10^4 <= num1, num2 <= 10^9; the lower bound suggests negatives may appear, which the 32-bit mask handles.',
        solution='''### Intuition
Flipping a bit changes exactly one position. To turn P into Q we must flip exactly the positions where P and Q differ, and flipping any other position only makes things worse. So the answer is the number of differing positions.

### Approach
1. Compute d = num1 XOR num2; a bit of d is 1 exactly where the two numbers differ.
2. Mask d to 32 bits (so negative numbers use their two's complement form).
3. Count the 1-bits.

### Why it works
XOR is 1 iff the two bits differ, so popcount(P xor Q) is the Hamming distance between the two bit patterns, and each flip fixes at most one differing position.

### Complexity
O(1) time (at most 32 bits) and O(1) space.

### Python solution
```python
def flippedBits(num1, num2):
    return bin((num1 ^ num2) & 0xFFFFFFFF).count('1')
```

### Dry run
7 = 0b0111 and 10 = 0b1010. XOR = 0b1101, which has three 1-bits. Answer 3.

### Edge cases & pitfalls
- Equal numbers give 0.
- Negative numbers: mask to 32 bits, otherwise Python's unbounded ints give a wrong count.
- Use an unsigned type or __builtin_popcount in C++.''')
    add('sap-evens-before-odds', S, 'Arrange a list so that all odd numbers come after the even numbers',
        'In an online game a list of N numbers is given. The player must arrange the numbers so that all the odd numbers of the list come after the even numbers. The relative order of the odd numbers and the relative order of the even numbers in the output must be the same as in the input.',
        None,
        'This is a stable partition: output all even numbers in input order, then all odd numbers in input order. One pass each (or one pass with two lists). O(N) time and space.',
        section='dsa', topic='two-pointers', type='coding', sources=['20240825_100753.jpg', 'Copy of IMG-20240825-WA0008.jpeg', 'Copy of IMG_20240825_100313_734.jpg', 'Copy of IMG_20240825_100331_871.jpg'],
        function_signature='arrange(a)',
        input_format='Line 1: N. Line 2: N space-separated integers.',
        output_format='N space-separated integers with all evens before all odds, order preserved within each group.',
        constraints='Bounds are not visible in the photographs.',
        examples=[{'input': '8\n10 98 3 33 12 22 21 11', 'output': '10 98 12 22 3 33 21 11'}],
        notes='The starter code in the photographs uses a swap-based two-pointer partition, which is not stable; the stability note in the statement requires a stable method.',
        solution='''### Intuition
The note on relative order rules out the usual swap-based partition (which scrambles order). We need a stable partition: keep the evens in their original order, then keep the odds in their original order.

### Approach
1. Walk the list once and collect the even numbers into one list and the odd numbers into another.
2. Output the even list followed by the odd list.

### Why it works
Each list keeps the input order of its elements, and concatenating them puts every even before every odd.

### Complexity
O(N) time and O(N) extra space. A stable in-place version exists with O(N log N) time (divide and conquer) but is not needed here.

### Python solution
```python
def arrange(a):
    evens = [v for v in a if v % 2 == 0]
    odds = [v for v in a if v % 2 != 0]   # v % 2 != 0 also works for negatives
    return evens + odds

if __name__ == '__main__':
    n = int(input())
    print(*arrange(list(map(int, input().split()))))
```

### Dry run
Input 10 98 3 33 12 22 21 11: evens 10, 98, 12, 22; odds 3, 33, 21, 11. Output 10 98 12 22 3 33 21 11.

### Edge cases & pitfalls
- Use v % 2 != 0 rather than == 1: in C++ and Java -3 % 2 == -1.
- N = 0 or all-even / all-odd lists work without changes.
- Do not use std::partition (not stable); use stable_partition in C++.''')
    add('sap-pizza-first-meat-order', S, 'First meat pizza order in each window of K displayed orders',
        'A pizza shop serves vegan pizza (positive order numbers) and meat pizza (negative order numbers). The shop displays K out of N orders at a time; when an order is delivered it is removed from the front of the display and the next order is added at the end. For each display (each window of K consecutive orders) report the first meat pizza order number shown, or 0 if no meat pizza order is on the screen.',
        None,
        'For every window of size K output the first negative number in it, or 0. Keep a deque of indices of negative numbers: push when a negative arrives, drop indices that left the window, and read the front. O(N) time, O(K) space; verified against brute force.',
        section='dsa', topic='sliding-window', type='coding', sources=['IMG-20240915-WA0013.jpg', 'IMG-20240915-WA0014.jpg', 'IMG-20240915-WA0015.jpg', 'IMG-20240915-WA0016.jpg'],
        function_signature='orderPizza(orderPlaced, size)',
        input_format='Line 1: N (orderPlaced_size). Line 2: N space-separated integers. Last line: K (size).',
        output_format='Space-separated integers: for each of the N - K + 1 windows, the first meat pizza order (negative) or 0.',
        constraints='0 <= orderPlaced_size <= 10^6; 0 <= size <= orderPlaced_size; -10^9 <= order numbers <= 10^9.',
        examples=[{'input': '6\n-11 -2 19 37 64 -18\n3', 'output': '-11 -2 0 -18', 'explanation': 'Windows [-11,-2,19], [-2,19,37], [19,37,64], [37,64,-18].'}],
        leetcode={'name': 'First Negative Integer in Every Window of Size K', 'url': 'https://www.geeksforgeeks.org/first-negative-integer-every-window-size-k/', 'similarity': 'same'},
        notes='An order number of 0 is neither vegan nor meat; it is treated as non-meat. K = 0 is outside the useful range; return an empty list.',
        solution='''### Intuition
For every window we only care about the earliest negative value. As the window slides, a negative leaves from the front and a new element enters at the back, so a queue of the negative elements' indices gives the earliest one at its front.

### Approach
1. Keep a deque of indices of negative numbers seen so far.
2. For each index i: if orders[i] < 0 push i.
3. When i >= K - 1 a full window ends at i: pop indices from the front while they are <= i - K (they left the window); the answer for the window is orders[front] if the deque is non-empty, else 0.

### Why it works
Indices in the deque are in increasing order, so the front is the earliest negative still possibly inside the window; stale indices are removed before reading, so the front is always inside [i-K+1, i].

### Complexity
Each index is pushed and popped at most once: O(N) time, O(K) space (at most K indices are alive after pruning).

### Python solution
```python
from collections import deque

def orderPizza(orders, k):
    res = []
    dq = deque()                       # indices of negative numbers
    for i, v in enumerate(orders):
        if v < 0:
            dq.append(i)
        if i >= k - 1:
            while dq and dq[0] <= i - k:   # left the window
                dq.popleft()
            res.append(orders[dq[0]] if dq else 0)
    return res
```

### Dry run
orders = [-11, -2, 19, 37, 64, -18], K = 3. i=0: dq=[0]. i=1: dq=[0,1]. i=2: window ends; front 0 -> -11. i=3: dq front 0 <= 0 removed, front 1 -> -2. i=4: front 1 <= 1 removed, dq empty -> 0. i=5: push 5, front 5 -> -18. Output -11 -2 0 -18.

### Edge cases & pitfalls
- K greater than N gives no windows; K = N gives one.
- The stub prints the result with a separator pattern assuming a non-empty list; guard for an empty result.
- Use 64-bit-safe reads for 10^6 numbers (fast input).''')
    add('sap-min-rotations-common-prefix', S, 'Minimum rotations of the second string for the longest common prefix',
        'Peter has two strings of the same length. The first string is fixed and the second is rotatable. In a left rotation the first character is removed and added to the end; in a right rotation the last character is removed and added to the start. Peter wants the longest common prefix of both strings. Find the minimum number of rotations required to obtain the longest common prefix. If no prefix is common, output -1.',
        None,
        'Rotating left by k equals rotating right by n-k, so the cost of shift k is min(k, n-k). Build first + separator + second + second and run the Z-function: z at position n+1+k is the common prefix length for left shift k. Take the longest prefix and, among ties, the cheapest shift. O(n) time and space; verified against brute force.',
        section='dsa', topic='strings', type='coding', hard=True, sources=['65bc4e2a89ac8_59465bc4e2a2c01e.jpg', '65bc4e2b285ba_59465bc4e2ac9dc0.jpg', '65bc4e2bc2e43_59565bc4e2b74de9.jpg'],
        function_signature='minRotations(firstString, secondString)',
        input_format='Line 1: firstString. Line 2: secondString (same length).',
        output_format='One integer: the minimum number of rotations, or -1 if no prefix is common.',
        constraints='0 < len (the length of both strings). Alphanumeric characters (a-z, A-Z, 0-9), comparisons are case sensitive.',
        examples=[{'input': 'a2abccc\nbddda2a', 'output': '3', 'explanation': 'The longest common prefix a2ab is reached after 3 right rotations.'}],
        notes='The sample output is read from the explanation (3 right rotations); the printed output line was partly hidden. If several rotations give the same longest prefix, the cheaper of left and right is taken.',
        solution='''### Intuition
Only the n possible rotations matter, and rotating left by k is the same as rotating right by n - k. For each rotation we want the length of its common prefix with the first string. Computing these naively costs O(n^2); the Z-function gives all of them at once.

### Approach
1. Let n = len(first). Build t = first + '#' + second + second ('#' cannot appear in the strings).
2. Compute the Z-array of t. For a left shift k (0 <= k < n), z[n + 1 + k] is the length of the common prefix between first and the rotated second (capped at n).
3. Track the best prefix length; among shifts with the same best length choose the smallest cost min(k, n - k).
4. If the best length is 0 return -1, otherwise return the cost.

### Why it works
The second doubled string contains every rotation of second as a window of length n, so Z at the window start is exactly the prefix match with first. Rotating left k times or right n - k times produce the same string, so the cost is the smaller of the two.

### Complexity
O(n) time and space for the Z-function. A brute-force comparison on 500 random small cases passes.

### Python solution
```python
def z_function(s):
    n = len(s)
    z = [0] * n
    l = r = 0
    for i in range(1, n):
        if i < r:
            z[i] = min(r - i, z[i - l])
        while i + z[i] < n and s[z[i]] == s[i + z[i]]:
            z[i] += 1
        if i + z[i] > r:
            l, r = i, i + z[i]
    return z

def minRotations(first, second):
    n = len(first)
    t = first + '\\x00' + second + second
    z = z_function(t)
    best, bestcost = 0, 0
    for k in range(n):                       # k left rotations
        lcp = min(z[n + 1 + k], n)
        cost = min(k, n - k)                 # or n - k right rotations
        if lcp > best or (lcp == best and lcp > 0 and cost < bestcost):
            best, bestcost = lcp, cost
    return bestcost if best > 0 else -1
```

### Dry run
first = a2abccc, second = bddda2a. Rotating second left by 4 (equivalently right by 3) gives a2abddd whose common prefix with first is a2ab (length 4), the longest. cost = min(4, 7 - 4) = 3. No other shift reaches length 4, so the answer is 3.

### Edge cases & pitfalls
- No character of second matches first[0] -> -1.
- Shift 0 (no rotation) is allowed and costs 0 when it already gives the longest prefix.
- Use a separator not in the alphabet so Z values cannot spill past n.
- Strings are case-sensitive.''')
    skip(S, 'AAO Generalist notification 2025-Final_copy.pdf', 'LIC recruitment notification, not an OA')
    skip(S, 'Instruction for Candidates F.Y. B.Tech ACAP -2025-26_copy.pdf', 'exam instructions document')
    skip(S, '20240825_100411.docx', 'duplicate of the bit-flip problem screenshot as a document')
    skip(S, 'IMG_20240913_132940.jpg', 'chat message with a cropped one-line problem start (flowers)')
