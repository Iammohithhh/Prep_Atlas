"""Independent small-instance checks for the latest archive algorithm explanations."""
from collections import Counter, deque
from itertools import combinations
from heapq import heappush, heappop
from math import isqrt
import random


def cluster_quality(speed, reliability, k):
    heap, total, best = [], 0, 0
    for r, s in sorted(zip(reliability,speed), reverse=True):
        heappush(heap,s); total += s
        if len(heap)>k: total -= heappop(heap)
        best=max(best,total*r)
    return best


def brute_cluster(speed,reliability,k):
    return max(sum(speed[i] for i in ids)*min(reliability[i] for i in ids)
               for size in range(1,k+1) for ids in combinations(range(len(speed)),size))


def prune_tree(parent,weights,limits):
    children=[[] for _ in parent]
    for node in range(1,len(parent)): children[parent[node]].append(node)
    stack=[(0,0,False)]; removed=0
    while stack:
        node,d,bad=stack.pop()
        bad=bad or d>limits[node]
        removed+=bad
        stack.extend((c,max(0,d+weights[c]),bad) for c in children[node])
    return removed


def brute_prune(parent,weights,limits):
    n=len(parent); best=n
    for mask in range(1<<n):
        if not mask&1: continue
        kept={i for i in range(n) if mask>>i&1}
        if any(parent[i] not in kept for i in kept if i): continue
        valid=True
        for end in kept:
            node,total=end,0
            while node:
                total+=weights[node]; node=parent[node]
                if total>limits[end]: valid=False
        if valid: best=min(best,n-len(kept))
    return best


def minimax_path(values,edges,start,end):
    adj=[[] for _ in values]
    for a,b in edges:adj[a].append(b);adj[b].append(a)
    dist=[float('inf')]*len(values);dist[start]=0;heap=[(0,start)]
    while heap:
        cost,node=heappop(heap)
        if cost!=dist[node]:continue
        for nxt in adj[node]:
            candidate=max(cost,abs(values[node]-values[nxt]))
            if candidate<dist[nxt]:dist[nxt]=candidate;heappush(heap,(candidate,nxt))
    return dist[end]


def brute_minimax(values,edges,start,end):
    adj=[[] for _ in values]
    for a,b in edges:adj[a].append(b);adj[b].append(a)
    best=float('inf');stack=[(start,{start},0)]
    while stack:
        node,seen,cost=stack.pop()
        if node==end:best=min(best,cost);continue
        for nxt in adj[node]:
            if nxt not in seen:stack.append((nxt,seen|{nxt},max(cost,abs(values[node]-values[nxt]))))
    return best


def nice_pairs(parent,labels):
    masks=[0]*len(parent);frequencies=Counter();answer=0
    for node in range(len(parent)):
        if node:masks[node]=masks[parent[node]]^(1<<labels[node])
        mask=masks[node]
        answer+=frequencies[mask]+sum(frequencies[mask^(1<<bit)] for bit in range(26))
        frequencies[mask]+=1
    return answer


def brute_nice_pairs(parent,labels):
    adj=[[] for _ in parent]
    for node in range(1,len(parent)):
        adj[node].append((parent[node],labels[node]));adj[parent[node]].append((node,labels[node]))
    answer=0
    for start in range(len(parent)):
        stack=[(start,-1,[])]
        while stack:
            node,prev,path=stack.pop()
            if node>start and sum(count%2 for count in Counter(path).values())<=1:answer+=1
            stack.extend((nxt,node,path+[char]) for nxt,char in adj[node] if nxt!=prev)
    return answer


def min_square(points,k):
    xs=sorted(set(x for x,y in points));best=float('inf')
    for left in xs:
        for right in xs:
            if right<left:continue
            ys=sorted(y for x,y in points if left<=x<=right)
            for i in range(len(ys)-k+1):best=min(best,(max(right-left,ys[i+k-1]-ys[i])+2)**2)
    return best


def brute_square(points,k):
    return min((max(max(x for x,y in subset)-min(x for x,y in subset),
                    max(y for x,y in subset)-min(y for x,y in subset))+2)**2
               for subset in combinations(points,k))


def power_sums(bound):
    powers={0}
    if bound>=1:powers.add(1)
    for base in range(2,isqrt(bound)+1):
        number=base*base
        while number<=bound:powers.add(number);number*=base
    return {a+b for a in powers for b in powers if a+b<=bound}


def brute_power_sums(bound):
    # Enumerate bases/exponents directly, rather than generating by multiplication.
    terms={base**exponent for base in range(bound+1) for exponent in range(2,max(3,bound.bit_length()+1)) if base**exponent<=bound}
    return {a+b for a in terms for b in terms if a+b<=bound}


def distinct_digit_mask(number):
    seen=0
    while number:
        number,digit=divmod(number,10)
        if seen&(1<<digit):return False
        seen|=1<<digit
    return True


def grid_jumps(grid):
    n,m=len(grid),len(grid[0]);directions=[(-1,0),(1,0),(0,-1),(0,1)]
    start=next((r,c) for r in range(n) for c in range(m) if grid[r][c]=='S')
    queue=deque([(*start,-1,0)]);seen={(*start,-1)}
    while queue:
        row,col,forced,distance=queue.popleft()
        if grid[row][col]=='E' and forced==-1:return distance
        for direction in (range(4) if forced==-1 else [forced]):
            dr,dc=directions[direction];length=1
            while 0<=row+dr*length<n and 0<=col+dc*length<m:
                r,c=row+dr*length,col+dc*length
                if grid[r][c]!='#':
                    state=(r,c,-1 if length==1 else direction)
                    if state not in seen:seen.add(state);queue.append((*state,distance+1))
                length+=1
    return -1


if __name__=='__main__':
    rng=random.Random(129);checks=0
    for _ in range(500):
        n=rng.randrange(1,9);k=rng.randrange(1,n+1)
        speed=[rng.randrange(1,20) for _ in range(n)];reliability=[rng.randrange(1,20) for _ in range(n)]
        assert cluster_quality(speed,reliability,k)==brute_cluster(speed,reliability,k)
        parent=[-1]+[rng.randrange(i) for i in range(1,n)]
        weights=[0]+[rng.randrange(-10,11) for _ in range(1,n)];limits=[rng.randrange(1,15) for _ in range(n)]
        assert prune_tree(parent,weights,limits)==brute_prune(parent,weights,limits)
        values=[rng.randrange(20) for _ in range(n)]
        edges=[(i,j) for i in range(n) for j in range(i) if rng.randrange(3)==0]
        assert minimax_path(values,edges,0,n-1)==brute_minimax(values,edges,0,n-1)
        labels=[rng.randrange(26) for _ in range(n)]
        assert nice_pairs(parent,labels)==brute_nice_pairs(parent,labels)
        points=[(rng.randrange(-4,5),rng.randrange(-4,5)) for _ in range(n)]
        assert min_square(points,k)==brute_square(points,k)
        checks+=5
    for bound in range(101):
        assert power_sums(bound)==brute_power_sums(bound);checks+=1
    assert power_sums(25)&set(range(20,26))=={20,24,25}
    assert cluster_quality([4,3,15,5,6],[7,6,1,2,8],3)==78
    assert cluster_quality([12,112,100,13,55],[31,4,100,55,50],3)==10000
    for number in range(1,10001):
        assert distinct_digit_mask(number)==(len(str(number))==len(set(str(number))));checks+=1
    assert sum(distinct_digit_mask(i) for i in range(80,121))==27
    assert grid_jumps(['S****#','**#***','*****#','*#*#**','#****E'])==5
    assert grid_jumps(['S#*E'])==2  # Jump across #, then finish with length one.
    assert grid_jumps(['S#E'])==-1  # A long final jump alone does not finish.
    assert grid_jumps(['S***E'])==2
    assert grid_jumps(['SE'])==1
    assert min_square([(1,1),(1,2),(2,1)],3)==9
    print(f'Batch12: {checks} independent comparisons and targeted grid examples passed.')
