"""Oracle repeats and a further group of independently solved prompts."""


def extend(add, merge, skip):
    repeats = {
        'oracle-23tree':['0090'], 'oracle-sparse-matrix':['0091'], 'oracle-arp':['0092'],
        'oracle-ring':['0093'], 'oracle-idempotent':['0095','0097'],
        'oracle-having':['0098'], 'oracle-hosts':['0099'], 'oracle-nosql-choice':['0100'],
        'oracle-cap':['0101'], 'oracle-c-macro':['0108'], 'reverse-array':['0107'],
    }
    for key, suffixes in repeats.items():
        merge(key, 'Oracle', ['IMG-20240823-WA'+s+'.jpg' for s in suffixes])
    add('oracle-head', 'Oracle', 'HTTP method for resource metadata without a response body',
        'Which HTTP request method retrieves response metadata for a resource without transferring the representation body?', 'HEAD',
        'HEAD has GET-like semantics but the server does not send response content. It is useful for inspecting headers such as content type or validators. POST is not the method for metadata retrieval; the candidate’s marked option in one screenshot is not a verified key.',
        section='cs', topic='networks', options=['GET','PUT','HEAD','POST'], sources=['IMG-20240823-WA0094.jpg','IMG-20240823-WA0096.jpg'])
    add('oracle-acid-not', 'Oracle', 'Which is not an ACID property?',
        'Which listed choice is not an ACID transaction property?', 'Dependency',
        'ACID stands for Atomicity, Consistency, Isolation and Durability. Dependency can describe relationships between data or operations, but is not one of these four guarantees.',
        section='cs', topic='dbms', options=['Atomicity','Consistency','Isolation','Dependency'], sources=['IMG-20240823-WA0102.jpg'])
    add('oracle-nine-coins', 'Oracle', 'Find a known-lighter coin among nine',
        'There are nine visually identical coins. Exactly one is lighter than the others. What is the minimum number of balance-scale weighings needed in the worst case to find it?', '2',
        'Divide the coins into groups of three and weigh two groups. If balanced, the lighter coin is in the unweighed group; otherwise it is in the lighter group. From those three, weigh one against another: the lighter coin is identified either by imbalance or as the third coin if balanced. One weighing has only three outcomes, insufficient to distinguish nine candidates, so two is optimal.',
        topic='logical', options=['2','3','4','5'], sources=['IMG-20240913-WA0005.jpg'])
    add('oracle-two-eggs', 'Oracle', 'Minimum worst-case drops for two eggs and 100 floors',
        'A building has 100 floors. An egg breaks when dropped from floor N or above and survives below N. With two eggs, what minimum worst-case number of drops determines the threshold?', '14',
        'With d drops and two eggs, the largest searchable floor count is 1+2+…+d=d(d+1)/2. Drop the first egg at floors 14,27,39,…, decreasing the interval by one each time. If it breaks, use the second egg to search the previous interval linearly within the remaining budget. Thirteen drops cover at most 91 floors; fourteen cover 105, enough for 100. The count is a worst-case guarantee.',
        topic='logical', options=['12','14','17','20'], sources=['IMG-20240913-WA0009.jpg'])
    add('oracle-clock-overlap', 'Oracle', 'Daily overlaps of clock hands',
        'The hour and minute hands of a regular clock coincide at midnight. How many times do they coincide in a 24-hour day, counting its starting midnight and excluding the next day’s starting midnight?', '22',
        'The minute hand gains on the hour hand at 6−0.5=5.5 degrees per minute. Consecutive coincidences are 360/5.5=720/11 minutes apart. There are eleven per twelve-hour half-open interval and twenty-two per day. Counting both midnight endpoints would count the shared boundary twice.',
        options=['24','23','22','21'], sources=['IMG-20240913-WA0011.jpg'], notes='The standard day-boundary convention is stated explicitly.')
    add('oracle-three-ants', 'Oracle', 'Probability three ants do not collide',
        'Three ants start at the vertices of an equilateral triangle. Independently, each chooses clockwise or counterclockwise with equal probability and moves along its edges at the same speed. What is the probability that no ants collide?', '0.25',
        'There are 2³=8 equally likely direction assignments. Collision is avoided only when all three go clockwise or all three go counterclockwise, giving 2/8=1/4. Mixed directions cause at least one pair to approach along the same edge.',
        topic='probability', options=['0.2','0.25','0.33','0.5'], sources=['IMG-20240913-WA0012.jpg'], notes='Independent fair direction choices and equal speed make the usual puzzle assumptions explicit.')
    add('oracle-cyclical-sequence', 'Oracle', 'Recover the first two terms of a multiplicative sequence',
        'A sequence has 100 real elements. Every element except the first and last equals the product of its two neighbours. The product of the first 50 elements is 27, and the product of all 100 is also 27. Find the sum of the first two elements.', '12',
        'All elements are nonzero because their total product is 27. Writing the first two as a,b, the recurrence gives the repeating six-term cycle a,b,b/a,1/a,1/b,a/b, whose product is 1. Fifty terms comprise eight cycles followed by a,b, so ab=27. A hundred terms comprise sixteen cycles followed by a,b,b/a,1/a, so b²/a=27. Substituting a=27/b gives b³=729, hence b=9, a=3 and a+b=12.',
        options=['6','7','10','12'], sources=['IMG-20240913-WA0004.jpg','IMG-20240913-WA0013.jpg'])
    for s, reason in [('0103','historical software-version question needs dated verification'), ('0105','NoSQL store classification needs full review'), ('0106','partition syntax and database dialect need verification')]:
        skip('Oracle','IMG-20240823-WA'+s+'.jpg',reason)
    for s, reason in [('0003','reading passage without its question')]:
        skip('Oracle','IMG-20240913-WA'+s+'.jpg',reason)
