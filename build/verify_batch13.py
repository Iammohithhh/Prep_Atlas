"""Check swap-cost greedy against whole multiset-state shortest paths."""
from collections import Counter
from heapq import heappop, heappush
from itertools import product, permutations
from math import prod
import random


def swap_cost(a,b):
    ca,cb=Counter(a),Counter(b);extra_a=[];extra_b=[]
    for height in ca.keys()|cb.keys():
        difference=ca[height]-cb[height]
        if difference%2:return -1
        if difference>0:extra_a.extend([height]*(difference//2))
        else:extra_b.extend([height]*(-difference//2))
    minimum=min(a+b)
    return sum(min(x,y,2*minimum) for x,y in zip(sorted(extra_a),sorted(extra_b,reverse=True)))


def brute_swap_cost(a,b):
    initial=(tuple(sorted(a)),tuple(sorted(b)))
    heap=[(0,initial)];distances={initial:0}
    while heap:
        cost,(left,right)=heappop(heap)
        if cost!=distances[(left,right)]:continue
        if left==right:return cost
        for x in set(left):
            for y in set(right):
                if x==y:continue
                new_left=list(left);new_right=list(right)
                new_left.remove(x);new_left.append(y)
                new_right.remove(y);new_right.append(x)
                state=(tuple(sorted(new_left)),tuple(sorted(new_right)))
                candidate=cost+min(x,y)
                if candidate<distances.get(state,float('inf')):
                    distances[state]=candidate;heappush(heap,(candidate,state))
    return -1


def parity(m,strings):
    if m==0:return len(strings)%2
    return sum(all(ord(c)%2 for c in s) for s in strings)%2


def positive_meetings(values):
    total=count=0
    for value in sorted(values,reverse=True):
        total+=value
        if total<=0:break
        count+=1
    return count


def brute_meetings(values):
    best=0
    for order in set(permutations(values)):
        total=count=0
        for value in order:
            total+=value
            if total<=0:break
            count+=1
        best=max(best,count)
    return best


def festival_cost(population,x,y):
    def median(values):
        accumulated=0
        for value,weight in sorted(zip(values,population)):
            accumulated+=weight
            if 2*accumulated>=sum(population):return value
    a,b=median(x),median(y)
    return sum(p*(abs(px-a)+abs(py-b)) for p,px,py in zip(population,x,y))


def brute_festival(population,x,y):
    return min(sum(p*(abs(px-a)+abs(py-b)) for p,px,py in zip(population,x,y))
               for a in range(min(x),max(x)+1) for b in range(min(y),max(y)+1))


if __name__=='__main__':
    checks=0;rng=random.Random(1313)
    arrays=list(product(range(1,5),repeat=2))
    for a in arrays:
        for b in arrays:
            assert swap_cost(list(a),list(b))==brute_swap_cost(a,b),(a,b)
            checks+=1
    for _ in range(600):
        n=rng.randrange(1,6)
        a=[rng.randrange(1,10) for _ in range(n)];b=[rng.randrange(1,10) for _ in range(n)]
        assert swap_cost(a,b)==brute_swap_cost(a,b),(a,b)
        checks+=1
    for _ in range(1000):
        strings=[''.join(rng.choice('abcdefxyz') for _ in range(rng.randrange(1,7))) for _ in range(rng.randrange(1,10))]
        m=rng.randrange(9)
        assert parity(m,strings)==sum(prod(ord(c)**m for c in s) for s in strings)%2
        checks+=1
    assert swap_cost([4,2,2,2],[1,4,1,2])==1
    assert swap_cost([1,10,10],[1,20,20])==2  # The global-minimum detour.
    for _ in range(200):
        values=[rng.randrange(-6,7) for _ in range(rng.randrange(1,8))]
        assert positive_meetings(values)==brute_meetings(values);checks+=1
    for _ in range(500):
        n=rng.randrange(1,9)
        population=[rng.randrange(1,10) for _ in range(n)]
        x=[rng.randrange(-4,5) for _ in range(n)];y=[rng.randrange(-4,5) for _ in range(n)]
        assert festival_cost(population,x,y)==brute_festival(population,x,y);checks+=1
    print(f'Batches13–14: {checks} independent comparisons passed.')
