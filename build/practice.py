"""Original, fully specified exercises based on archive/research patterns.

These are labelled practice adaptations, never transcribed company questions.
Reference solutions stay in build/; public cases offer feedback, not a secure judge.
"""
import itertools
import math
import random


def make_practice():
    questions = []
    references = {}
    rng = random.Random(721)

    def add(key, title, section, topic, statement, signature, explanation, cases, ref, *, hard=False, numpy=False, floating=False, example=None):
        function = signature.split('(')[0].replace('def ', '')
        q = dict(id='practice-'+key, company='General', also_asked_by=[], origin='practice', section=section,
                 subsection=topic, topics=[topic], pattern=key, difficulty='hard' if hard else 'easy-medium',
                 type='coding', title=title, statement=statement, function_signature=signature,
                 starter=('# import numpy as np\n\n' if numpy else '') + signature + ':\n    # Implement this function.\n    pass\n',
                 explanation=explanation, checker={'function':function,'cases':cases, 'numpy':numpy,'float':floating},
                 examples=([example] if example else []), sources=[])
        questions.append(q)
        references[q['id']] = ref

    hist_cases = [{'args':[a],'expected':max([0]+[min(a[i:j])*(j-i) for i in range(len(a)) for j in range(i+1,len(a)+1)])} for a in [[],[0],[2,1,5,6,2,3],[2,2,2],[6,5,4,3,2,1]]+[[rng.randrange(8) for _ in range(rng.randrange(1,10))] for _ in range(35)]]
    add('histogram','Largest rectangle in a histogram','dsa','stack-queue',
        'Given a list `heights` of nonnegative integers, each representing a histogram bar of width 1, return the largest rectangular area under the histogram. An empty list has area 0.\n\nPractice constraints: `0 ≤ len(heights) ≤ 100,000`, `0 ≤ heights[i] ≤ 10⁹`. Return an integer.',
        'def largest_rectangle(heights)',
        'Maintain an increasing stack of bar indices. When the next height is smaller, pop each taller bar and compute its area using the previous stack element as its left boundary. A sentinel height 0 flushes the stack. Each index is pushed and popped once: O(n) time, O(n) space.', hist_cases,
        'def largest_rectangle(heights):\n    stack = []\n    best = 0\n    for i, h in enumerate(heights + [0]):\n        while stack and heights[stack[-1]] > h:\n            top = stack.pop()\n            width = i - (stack[-1] if stack else -1) - 1\n            best = max(best, heights[top] * width)\n        stack.append(i)\n    return best\n', hard=True,
        example={'input':'heights = [2, 1, 5, 6, 2, 3]','output':'10','explanation':'The bars of heights 5 and 6 form a rectangle of height 5 and width 2.'})

    def cover_ref(a):
        required=len(set(a)); counts={}; left=0;best=len(a)
        for right,v in enumerate(a):
            counts[v]=counts.get(v,0)+1
            while len(counts)==required and left<=right:
                best=min(best,right-left+1);counts[a[left]]-=1
                if counts[a[left]]==0:del counts[a[left]]
                left+=1
        return best if a else 0
    cover_arrays=[[],[1],[1,2,1,3,2],[4,4,4],[1,2,3,4]]+[[rng.randrange(4) for _ in range(rng.randrange(12))] for _ in range(25)]
    add('distinct-window','Shortest window containing every distinct value','dsa','sliding-window',
        'Return the length of the shortest contiguous subarray that contains every distinct value present anywhere in `values`. Return 0 for an empty list.\n\nPractice constraints: at most 100,000 integers; values may be negative.',
        'def shortest_cover(values)','Use a frequency map and a sliding window. Expand right until all required values are present, then shrink left while preserving coverage. O(n) time and O(k) space for k distinct values.',
        [{'args':[a],'expected':min([len(a)]+[j-i for i in range(len(a)) for j in range(i+1,len(a)+1) if set(a[i:j])==set(a)]) if a else 0} for a in cover_arrays],
        'def shortest_cover(values):\n    required = len(set(values))\n    counts = {}\n    left = 0\n    best = len(values)\n    for right, value in enumerate(values):\n        counts[value] = counts.get(value, 0) + 1\n        while len(counts) == required and left <= right:\n            best = min(best, right - left + 1)\n            counts[values[left]] -= 1\n            if counts[values[left]] == 0: del counts[values[left]]\n            left += 1\n    return best if values else 0\n',
        example={'input':'values = [1, 2, 1, 3, 2]','output':'3','explanation':'The window [2, 1, 3] covers {1, 2, 3}.'})

    arrays=[[5,1,3,2,9],[1],[-4,-3,-5],[2,2,2,2]]+[[rng.randrange(-10,11) for _ in range(rng.randrange(1,12))] for _ in range(25)]
    cases=[]
    for a in arrays:
        k=rng.randrange(1,len(a)+1)
        cases.append({'args':[a,k],'expected':[sorted(a[:i],reverse=True)[k-1] for i in range(k,len(a)+1)]})
    add('prefix-kth','Kth largest value in every eligible prefix','dsa','heap',
        'Given a nonempty integer list `values` and `1 ≤ k ≤ len(values)`, return a list of the kth largest values of each prefix of lengths k, k+1, …, n. Count equal values separately.\n\nPractice constraints: n ≤ 100,000. Values may be negative.',
        'def prefix_kth(values, k)','Maintain a min-heap containing the largest k values seen so far. After each prefix of length at least k, the heap root is the kth largest. O(n log k) time and O(k) space.',cases,
        'def prefix_kth(values, k):\n    import heapq\n    heap=[]\n    out=[]\n    for v in values:\n        heapq.heappush(heap,v)\n        if len(heap)>k:heapq.heappop(heap)\n        if len(heap)==k:out.append(heap[0])\n    return out\n',
        example={'input':'values = [5, 1, 3, 2, 9], k = 2','output':'[1, 3, 3, 5]'})

    add('rod-cutting','Maximum revenue from cutting a rod','dsa','dp',
        'A rod has length `n`. `prices[i-1]` is the selling price of a piece of length i, for i from 1 to n. Cuts are free and the entire rod must be sold. Return the maximum revenue.\n\nPractice constraints: 0 ≤ n ≤ 2,000; `len(prices) == n`; prices are nonnegative integers.',
        'def rod_revenue(n, prices)','Let dp[length] be the best revenue for that length. Try each first piece: dp[length] = max(prices[piece-1] + dp[length-piece]). O(n²) time, O(n) space.',
        [{'args':[0,[]],'expected':0},{'args':[4,[2,4,7,7]],'expected':9},{'args':[1,[3]],'expected':3},{'args':[5,[1,5,8,9,10]],'expected':13},{'args':[4,[0,0,0,0]],'expected':0}],
        'def rod_revenue(n, prices):\n    dp=[0]*(n+1)\n    for length in range(1,n+1):\n        dp[length]=max(prices[p-1]+dp[length-p] for p in range(1,length+1))\n    return dp[n]\n',
        example={'input':'n = 4, prices = [2, 4, 7, 7]','output':'9','explanation':'Use pieces of lengths 1 and 3: 2 + 7 = 9.'})

    def interval_union(a):
        points=sorted({v for pair in a for v in pair})
        return sum(y-x for x,y in zip(points,points[1:]) if any(l<=x and y<=r for l,r in a))
    intervals=[[],[[1,3]],[[1,3],[2,6],[8,10]],[[0,1],[1,2]],[[2,2]],[[1,9],[3,5]]]
    intervals += [[sorted([rng.randrange(-8,9),rng.randrange(-8,9)]) for _ in range(rng.randrange(8))] for _ in range(25)]
    add('interval-union','Total length covered by intervals','dsa','sorting',
        'Given intervals `[start, end]` on the number line, return their total covered length. Overlaps count once. Endpoints do not contribute extra units. All intervals satisfy start ≤ end. An empty list covers length 0.\n\nPractice constraints: at most 100,000 intervals; integer endpoints.',
        'def covered_length(intervals)','Sort by start. Merge each overlapping or touching interval into the current segment, accumulating finished lengths. O(n log n) time, O(n) extra space if sorting a copy.',
        [{'args':[a],'expected':interval_union(a)} for a in intervals],
        'def covered_length(intervals):\n    if not intervals:return 0\n    ordered=sorted(intervals)\n    start,end=ordered[0]\n    total=0\n    for a,b in ordered[1:]:\n        if a>end:total+=end-start;start,end=a,b\n        else:end=max(end,b)\n    return total+end-start\n',
        example={'input':'intervals = [[1, 3], [2, 6], [8, 10]]','output':'7','explanation':'[1, 6] contributes 5 and [8, 10] contributes 2.'})

    pair_arrays=[[1,2,3,4,5],[],[0,0,0],[-1,1,2,-2]]+[[rng.randrange(-9,10) for _ in range(rng.randrange(14))] for _ in range(25)]
    cases=[]
    for a in pair_arrays:
        mod=rng.randrange(1,9)
        cases.append({'args':[a,mod],'expected':sum((a[i]+a[j])%mod==0 for i in range(len(a)) for j in range(i+1,len(a)))})
    add('divisible-pairs','Count pairs whose sum is divisible by k','dsa','hashing',
        'Return the number of index pairs i < j such that `(values[i] + values[j]) % k == 0`. Equal values at different indices form different pairs.\n\nPractice constraints: 1 ≤ k ≤ 10⁹; n ≤ 100,000; negative values are allowed.',
        'def divisible_pairs(values, k)','For remainder r, previously seen elements of remainder (-r) mod k form valid pairs. Query the frequency before incrementing it to avoid pairing an index with itself. O(n) expected time, O(min(n,k)) space.',cases,
        'def divisible_pairs(values, k):\n    counts={}\n    result=0\n    for value in values:\n        r=value%k\n        result+=counts.get((-r)%k,0)\n        counts[r]=counts.get(r,0)+1\n    return result\n')

    graph_cases=[{'args':[3,[[0,1],[1,2]],0,2],'expected':2},{'args':[3,[[0,1]],0,2],'expected':-1},{'args':[1,[],0,0],'expected':0},{'args':[4,[[0,1],[1,2],[0,2],[2,3]],0,3],'expected':2}]
    add('graph-shortest','Shortest path in an unweighted graph','dsa','graphs',
        'Given n vertices numbered 0 to n−1 and a list of undirected edges, return the fewest edges on a path from source to target. Return −1 if unreachable. Source equal to target requires 0 edges. Duplicate edges and self-loops are allowed.\n\nPractice constraints: 1 ≤ n ≤ 100,000; at most 200,000 edges.',
        'def shortest_path(n, edges, source, target)','Build adjacency lists and run BFS from source. A vertex’s first visit gives its shortest distance. O(n + m) time and O(n + m) space.',graph_cases,
        'def shortest_path(n, edges, source, target):\n    from collections import deque\n    adj=[[] for _ in range(n)]\n    for a,b in edges:adj[a].append(b);adj[b].append(a)\n    distance=[-1]*n\n    distance[source]=0\n    todo=deque([source])\n    while todo:\n        v=todo.popleft()\n        if v==target:return distance[v]\n        for u in adj[v]:\n            if distance[u]<0:distance[u]=distance[v]+1;todo.append(u)\n    return -1\n')

    add('bipartite','Can a graph be split into two teams?','dsa','graphs',
        'Given n vertices and undirected edges, return True if every edge can connect vertices in different teams. Disconnected components must all satisfy this rule. A self-loop makes the graph invalid.\n\nPractice constraints: 0 ≤ n ≤ 100,000; at most 200,000 edges.',
        'def is_bipartite(n, edges)','Run BFS/DFS in each component, assigning opposite colors across every edge. A same-color edge is a contradiction. O(n + m) time and space.',
        [{'args':[0,[]],'expected':True},{'args':[3,[[0,1],[1,2],[2,0]]],'expected':False},{'args':[4,[[0,1],[1,2],[2,3],[3,0]]],'expected':True},{'args':[5,[[0,1],[2,3]]],'expected':True},{'args':[1,[[0,0]]],'expected':False}],
        'def is_bipartite(n, edges):\n    adj=[[] for _ in range(n)]\n    for a,b in edges:adj[a].append(b);adj[b].append(a)\n    color=[-1]*n\n    for root in range(n):\n        if color[root]>=0:continue\n        color[root]=0\n        stack=[root]\n        while stack:\n            v=stack.pop()\n            for u in adj[v]:\n                if color[u]<0:color[u]=1-color[v];stack.append(u)\n                elif color[u]==color[v]:return False\n    return True\n')

    add('min-coins','Minimum coins for an exact amount','dsa','dp',
        'Given positive integer denominations and a nonnegative amount, return the fewest coins needed to reach that amount exactly. You have unlimited coins of each denomination. Return −1 when impossible. Amount 0 requires 0 coins.\n\nPractice constraints: amount ≤ 10,000; at most 100 denominations.',
        'def min_coins(coins, amount)','Use dp[0]=0 and set dp[a]=min(dp[a-c]+1) over usable denominations. Unreachable states remain infinite. O(amount × number of denominations) time, O(amount) space.',
        [{'args':[[1,2,5],11],'expected':3},{'args':[[2],3],'expected':-1},{'args':[[],0],'expected':0},{'args':[[],5],'expected':-1},{'args':[[2,3],7],'expected':3},{'args':[[1],7],'expected':7}],
        'def min_coins(coins, amount):\n    dp=[0]+[amount+1]*amount\n    for a in range(1,amount+1):\n        for c in coins:\n            if c<=a:dp[a]=min(dp[a],dp[a-c]+1)\n    return dp[amount] if dp[amount]<=amount else -1\n')

    add('one-delete-palindrome','Palindrome after at most one deletion','dsa','two-pointers',
        'Given a string s, return True if deleting at most one character makes it a palindrome. The comparison is case-sensitive; all characters count. The empty string is a palindrome.\n\nPractice constraint: length ≤ 100,000.',
        'def valid_palindrome(s)','Advance two pointers while characters match. At the first mismatch, test the two possible deletions. Checking the remaining intervals takes O(n) time and O(1) extra space when implemented with indices.',
        [{'args':[s],'expected':s==s[::-1] or any((s[:i]+s[i+1:])==(s[:i]+s[i+1:])[::-1] for i in range(len(s)))} for s in ['', 'a','abca','abc','racecar','deeee','ab','abcdef','Aa','abccdba']],
        'def valid_palindrome(s):\n    def check(l,r):\n        while l<r:\n            if s[l]!=s[r]:return False\n            l+=1;r-=1\n        return True\n    l,r=0,len(s)-1\n    while l<r:\n        if s[l]!=s[r]:return check(l+1,r) or check(l,r-1)\n        l+=1;r-=1\n    return True\n')

    add('stable-softmax','Numerically stable row-wise softmax','ml','ml-coding',
        'Implement `stable_softmax(logits)` using NumPy. Accept a nonempty 2D numeric array-like input and return a NumPy array of the same shape, with softmax applied independently to each row. Handle large positive and negative finite logits without overflow.\n\nUse float64 for computation. Practice constraints: 1 ≤ rows, columns ≤ 100.',
        'def stable_softmax(logits)','For each row subtract its maximum before exponentiation, then divide by the row sum. This leaves the probabilities unchanged while preventing exponential overflow. Preserve the column axis using keepdims=True. O(rows × columns) time and output space.',
        [{'args':[[[0,0]]],'expected':[[.5,.5]]},{'args':[[[1000,1000],[-1000,-1000]]],'expected':[[.5,.5],[.5,.5]]},{'args':[[[1,2,3]]],'expected':[[.0900305732,.2447284711,.6652409558]]},{'args':[[[10],[-8]]],'expected':[[1],[1]]}],
        'def stable_softmax(logits):\n    import numpy as np\n    x=np.asarray(logits,dtype=np.float64)\n    e=np.exp(x-x.max(axis=1,keepdims=True))\n    return e/e.sum(axis=1,keepdims=True)\n', numpy=True,
        example={'input':'logits = [[1000, 1000], [1, 2, 3]] is invalid (ragged).\nValid: logits = [[1000, 1000]]','output':'[[0.5, 0.5]]'})

    add('linear-gradient','Gradient of mean squared error','ml','ml-coding',
        'Implement the gradient with respect to w for loss `L = mean((X @ w − y)²)`. Inputs are array-like: X has shape (n, d), w has shape (d,), and y has shape (n,), with n ≥ 1. Return a 1D NumPy array of shape (d,). Use float64.\n\nThe loss includes no factor of 1/2 and no regularisation.',
        'def mse_gradient(X, w, y)','The derivative is (2/n) Xᵀ(Xw−y). Check dimensions carefully; a column-shaped target may accidentally broadcast into an n×n matrix. O(nd) time and O(n+d) additional space.',
        [{'args':[[[1],[2]],[0],[1,2]],'expected':[-5]},{'args':[[[1,0],[0,1]],[2,3],[2,3]],'expected':[0,0]},{'args':[[[1,2]],[1,1],[0]],'expected':[6,12]}],
        'def mse_gradient(X, w, y):\n    import numpy as np\n    X=np.asarray(X,dtype=np.float64)\n    w=np.asarray(w,dtype=np.float64)\n    y=np.asarray(y,dtype=np.float64)\n    return 2/X.shape[0]*X.T@(X@w-y)\n', numpy=True)

    add('cross-entropy','Cross-entropy from logits','ml','ml-coding',
        'Given a nonempty 2D logits array and a 1D list of integer class labels, return the mean multiclass cross-entropy as a Python float. Each label is between 0 and number_of_classes−1. Use the log-sum-exp trick; do not clip probabilities.\n\nPractice constraints: finite logits with absolute value ≤ 10,000.',
        'def cross_entropy(logits, labels)','Subtract the row maximum. Compute log-normaliser = log(sum(exp(shifted))) and subtract the shifted true-class logit. Average across examples. O(nc) time and space; this avoids log(0) from underflow.',
        [{'args':[[[0,0]],[0]],'expected':math.log(2)},{'args':[[[1000,-1000]],[1]],'expected':2000},{'args':[[[0,0,0],[0,0,0]],[0,2]],'expected':math.log(3)},{'args':[[[5]],[0]],'expected':0}],
        'def cross_entropy(logits, labels):\n    import numpy as np\n    x=np.asarray(logits,dtype=np.float64)\n    labels=np.asarray(labels,dtype=int)\n    z=x-x.max(axis=1,keepdims=True)\n    return float(np.mean(np.log(np.exp(z).sum(axis=1))-z[np.arange(len(z)),labels]))\n', floating=True)

    add('single-head-attention','Scaled dot-product attention with a causal mask','ml','ml-coding',
        'Implement one attention head in NumPy. Q and K have shape (t, d); V has shape (t, dv); t, d and dv are positive. Return `softmax(Q @ K.T / sqrt(d)) @ V`. If `causal=True`, token i may attend only to keys j ≤ i. Apply a numerically stable softmax after masking. Return a NumPy array of shape (t, dv), float64.\n\nNo batching, dropout or projection matrices are required.',
        'def attention(Q, K, V, causal=False)','Compute scaled scores, replace disallowed entries above the diagonal with −∞, then subtract each row maximum and normalise exponentials. Multiply the probabilities by V. O(t²d + t²dv) time and O(t²) score memory.',
        [{'args':[[[0],[0]],[[0],[0]],[[2],[4]],False],'expected':[[3],[3]]},{'args':[[[0],[0]],[[0],[0]],[[2],[4]],True],'expected':[[2],[3]]},{'args':[[[1,2]],[[3,4]],[[7,8]],True],'expected':[[7,8]]}],
        'def attention(Q, K, V, causal=False):\n    import numpy as np\n    Q,K,V=[np.asarray(a,dtype=np.float64) for a in (Q,K,V)]\n    scores=Q@K.T/np.sqrt(Q.shape[1])\n    if causal:scores[np.triu_indices(len(Q),1)]=-np.inf\n    p=np.exp(scores-scores.max(axis=1,keepdims=True))\n    p/=p.sum(axis=1,keepdims=True)\n    return p@V\n', numpy=True,hard=True)

    add('precision-recall','Compute precision and recall for binary predictions','ml','ml-coding',
        'Given equal-length lists `truth` and `predicted` containing only 0 or 1, return `[precision, recall]` for positive class 1. Define a metric as 0.0 when its denominator is zero. Empty lists return `[0.0, 0.0]`.',
        'def precision_recall(truth, predicted)','Count true positives, false positives and false negatives. Precision = TP/(TP+FP); recall = TP/(TP+FN). State your convention for empty denominators. O(n) time, O(1) extra space.',
        [{'args':[[1,0,1,0],[1,1,0,0]],'expected':[.5,.5]},{'args':[[],[]],'expected':[0,0]},{'args':[[1,1],[0,0]],'expected':[0,0]},{'args':[[0,0],[1,1]],'expected':[0,0]},{'args':[[1,0,1],[1,0,1]],'expected':[1,1]}],
        'def precision_recall(truth, predicted):\n    tp=sum(a==1 and b==1 for a,b in zip(truth,predicted))\n    positives=sum(predicted)\n    actual=sum(truth)\n    return [tp/positives if positives else 0.,tp/actual if actual else 0.]\n',numpy=True)
    return questions, references


def verify():
    import numpy as np
    questions, references=make_practice()
    count=0
    for q in questions:
        ns={};exec(references[q['id']],ns)
        for case in q['checker']['cases']:
            got=ns[q['checker']['function']](*case['args']);expected=case['expected']
            if q['checker']['numpy']:equal=np.shape(got)==np.shape(expected) and np.allclose(got,expected,rtol=1e-5,atol=1e-7)
            elif q['checker']['float']:equal=math.isclose(got,expected,rel_tol=1e-6,abs_tol=1e-8)
            else:equal=got==expected
            assert equal,(q['id'],case,got)
            count+=1
    print(f'{len(questions)} reference solutions passed {count} cases (including brute-force comparisons).')


if __name__=='__main__':verify()
