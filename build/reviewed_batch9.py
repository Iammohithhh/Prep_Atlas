"""Oracle partition DP, minimax clustering caveat, and repeated MCQs."""


def extend(add, merge, skip):
    add('oracle-alternating-partitions','Oracle','Count partitions with alternating odd/even segment sums',
        'Partition a positive integer array into one or more nonempty contiguous segments covering every element exactly once. Adjacent segment sums must have opposite parity. Count the different valid partitions modulo 10⁹+7. A one-segment partition is always valid.', None,
        'Let P[i] be the parity of the prefix ending at i, with P[0]=0. For a previous cut j, the last segment parity is P[i] XOR P[j]. Maintain four sums B[prefix parity][previous last-segment parity] over already processed nonempty prefixes. For current parity t, ways ending even are B[t][1] plus 1 if t=0; ways ending odd are B[t XOR 1][0] plus 1 if t=1. The added 1 represents taking the whole prefix as a single segment. Compute both values before inserting them into B[t], so no zero-length segment is counted. Sum the two values at the final index, reducing all accumulators modulo 10⁹+7. O(n) time and O(1) extra space.',
        section='dsa', topic='dp', type='coding', sources=[f'IMG-20240914-WA00{i}.jpg' for i in range(65,69)], function_signature='findNumberOfPartitions(arr)', constraints='1 ≤ n ≤ 2×10⁵; 1 ≤ arr[i] ≤ 10⁹.',
        examples=[{'input':'arr = [1,2,3,3]','output':'4'},{'input':'arr = [1,1,1,1]','output':'2','explanation':'Either one segment, or segments [1], [1,1], [1].'}])
    add('oracle-minimax-clusters','Oracle','Minimise maximum distance to k one-dimensional centres',
        'Given n integer locations on a line, place k cluster centres to minimise the maximum distance from any point to its nearest centre. Distance is |x−y|. The source calls this K-Means Clustering, says centres may be placed anywhere, and requests an integer return value.', None,
        'The objective is one-dimensional minimax k-centre, not ordinary k-means (which minimises squared-distance sum). Sort the points and binary-search a coverage width D. Greedily start each interval at the leftmost uncovered point and include every point at most D farther right; D is feasible when at most k intervals suffice. This placement covers as far right as any feasible interval containing that leftmost point. With unrestricted real centres, a span D can be covered at its midpoint with radius D/2. The minimum feasible D is an integer for integer input. The sample locations [1,9,3,10,14], k=2 have optimal real radius 2.5, yet the source returns 3; its integer outputs fit ceiling the radius or requiring integer centres. Clarify that policy before implementing a judge. The integer-radius variant tests width 2R and returns the smallest feasible R. O(n log n+n log W) time and O(n) sorted-copy space, where W is the coordinate range.',
        section='dsa', topic='binary-search', type='coding', sources=[f'IMG-20240915-WA00{i}.jpg' for i in range(33,41)], function_signature='getMaximumDistance(location, k)', constraints='1 ≤ n ≤ 10⁵; 1 ≤ k ≤ n; 1 ≤ location[i] ≤ 10⁹.',
        examples=[{'input':'location = [1,9,3,10,14], k = 2','output':'3 (source integer result)','explanation':'Centres 2 and 11.5 achieve a real radius of 2.5; the source instead shows centres 3 and 12.'},{'input':'location = [5,3,8], k = 3','output':'0'}], notes='Centre-coordinate/rounding semantics are inconsistent between the continuous wording and integer samples. No practice checker is attached.')
    groups={
        'oracle-virtual-address':['0041'], 'oracle-semaphore-race':['0042','0043'],
        'oracle-kernel-mode':['0044'], 'oracle-priority-heap':['0045'], 'oracle-memoization':['0046'],
        'oracle-marathon-vector':['0047'], 'oracle-pointer-output':['0048','0049','0050'],
        'oracle-acid-not':['0053'], 'oracle-sql-default':['0054'], 'oracle-truncate-ddl':['0055'],
        'oracle-load-balancer':['0056','0057'], 'oracle-cap':['0058'], 'oracle-zombie':['0059'],
        'oracle-create-method':['0060'], 'oracle-server-error':['0061'],
    }
    for key, suffixes in groups.items():
        merge(key,'Oracle',['IMG-20240915-WA'+s+'.jpg' for s in suffixes])
    skip('Oracle','IMG-20240915-WA0051.jpg','named cloud services need current source verification')
    skip('Oracle','IMG-20240915-WA0052.jpg','historical software version needs dated verification')
