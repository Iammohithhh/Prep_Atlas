"""Amazon explanation checks against permutations, role indices and literal sets."""
from collections import Counter
from itertools import permutations, product
from math import prod
import random


def capable_winners(triples):
    rows=[sorted(t) for t in triples];low=[];middle=[]
    for i,(a,b,c) in enumerate(rows):
        low=sorted(low+[(a,i)],reverse=True)[:2]
        middle=sorted(middle+[(b,i)],reverse=True)[:2]
    return sum(b>next(v for v,j in low if j!=i) and c>next(v for v,j in middle if j!=i)
               for i,(a,b,c) in enumerate(rows))


def brute_winners(triples):
    def beats(a,b):
        return any(sum(x>y for x,y in zip(aa,bb))>=2 for aa in permutations(a) for bb in permutations(b))
    return sum(all(beats(a,b) for j,b in enumerate(triples) if i!=j) for i,a in enumerate(triples))


def largest_outlier(values):
    total=sum(values);counts=Counter(values);valid=[]
    for value in values:
        remainder=total-value
        if remainder%2==0 and counts[remainder//2]>int(value==remainder//2):valid.append(value)
    return max(valid) if valid else None


def brute_outlier(values):
    valid=[]
    for out in range(len(values)):
        for sum_index in range(len(values)):
            if out!=sum_index and values[sum_index]==sum(v for i,v in enumerate(values) if i not in (out,sum_index)):
                valid.append(values[out])
    return max(valid) if valid else None


def load_bound(parcels,extra):
    return max(max(parcels),(sum(parcels)+extra+len(parcels)-1)//len(parcels))


def compositions(total,parts):
    if parts==1:
        yield (total,)
    else:
        for first in range(total+1):
            for tail in compositions(total-first,parts-1):yield (first,)+tail


def brute_load(parcels,extra):
    return min(max(p+d for p,d in zip(parcels,allocation)) for allocation in compositions(extra,len(parcels)))


def wildcard_count(patterns):
    return sum(len({p[i] for p in patterns if p[i]!='?'})>1 for i in range(len(patterns[0])))


def literals(pattern):
    return {''.join(chars) for chars in product(*[('a','b') if c=='?' else (c,) for c in pattern])}


def brute_wildcards(patterns):
    options=[literals(p) for p in patterns];length=len(patterns[0]);best=length
    for chars in product('ab?',repeat=length):
        candidate=''.join(chars)
        if all(literals(candidate)&expanded for expanded in options):best=min(best,candidate.count('?'))
    return best


def divisible_pairs(values,x):
    seen=Counter();answer=0
    for value in values:
        r=value%x;answer+=seen[-r%x];seen[r]+=1
    return answer


if __name__=='__main__':
    rng=random.Random(1515);checks=0
    for _ in range(500):
        triples=[rng.sample(range(1,16),3) for _ in range(rng.randrange(2,8))]
        assert capable_winners(triples)==brute_winners(triples),triples;checks+=1
        values=[rng.randrange(-10,11) for _ in range(rng.randrange(3,10))]
        assert largest_outlier(values)==brute_outlier(values),values;checks+=1
        parcels=[rng.randrange(8) for _ in range(rng.randrange(1,5))];extra=rng.randrange(7)
        assert load_bound(parcels,extra)==brute_load(parcels,extra);checks+=1
        values=[rng.randrange(1,40) for _ in range(rng.randrange(1,25))];x=rng.randrange(1,15)
        assert divisible_pairs(values,x)==sum((values[i]+values[j])%x==0 for i in range(len(values)) for j in range(i));checks+=1
    for _ in range(250):
        length=rng.randrange(1,5)
        patterns=[''.join(rng.choice('ab?') for _ in range(length)) for _ in range(rng.randrange(1,6))]
        assert wildcard_count(patterns)==brute_wildcards(patterns),patterns;checks+=1
    assert capable_winners([(9,5,11),(4,12,3),(2,10,13)])==2
    assert capable_winners([(4,8,10),(2,5,12)])==2
    assert largest_outlier([2,2,4,2])==2
    assert largest_outlier([4,1,3,16,2,10])==16
    assert wildcard_count(['ha???rrank','?a?ke?bank'])==1
    print(f'Batch15: {checks} independent comparisons passed.')
