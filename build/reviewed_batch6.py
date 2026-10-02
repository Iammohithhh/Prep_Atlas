"""Oracle aptitude continuations and a maximum-path tree variant."""


def extend(add, merge, skip):
    add('oracle-hiker', 'Oracle', 'Distance from the starting point after three left turns',
        'A hiker walks 50 m north, turns left and walks 30 m, turns left and walks 50 m, then turns left and walks 50 m. How far is the hiker from the starting point?', 'None of the above',
        'The north and south legs cancel. The westward 30 m and eastward 50 m leave a displacement of 20 m east, so the distance is 20 m. This is absent from the listed numeric choices.',
        topic='logical', options=['25 m', '50 m', '35 m', 'None of the above'], sources=['IMG-20240823-WA0059.jpg'])
    add('oracle-digital-root', 'Oracle', 'Repeated digit sum of 25 factorial',
        'Repeatedly sum the decimal digits of 25! until one digit remains. What is that digit?', '9',
        '25! includes enough factors of 3 to be divisible by 9. A positive integer divisible by 9 has digital root 9, since every digit-sum step preserves the residue modulo 9. There is no need to expand the factorial.',
        options=['6', '7', '8', '9'], sources=['IMG-20240823-WA0060.jpg', 'IMG-20240823-WA0062.jpg'])
    add('oracle-expected-vegetarians', 'Oracle', 'Expected number of vegetarians in a two-person sample',
        'Of 50 people, 20 are vegetarian. Two people are selected uniformly at random without replacement. What is the expected number of vegetarians selected?', '196/245',
        'Each of the two selected positions has probability 20/50 of being vegetarian. By linearity of expectation, the expected count is 2×20/50=4/5=196/245. Independence is not required, so sampling without replacement does not change this expectation.',
        topic='probability', options=['197/245', '198/245', '196/245', '191/245'], sources=['IMG-20240823-WA0061.jpg', 'IMG-20240823-WA0063.jpg', 'IMG-20240823-WA0066.jpg'])
    add('oracle-father-age', 'Oracle', 'Father and son ages at a vacation',
        'A man spent one-third of his life up to the vacation as a bachelor. His son was born ten years after his marriage. At the vacation, the father was twice as old as his son. How old was the father?', '60',
        'Let the father’s vacation age be F. He married at F/3, so the son was born when the father was F/3+10. The son’s age at the vacation is F−(F/3+10)=2F/3−10. Since F=2(2F/3−10), F=60. He married at 20, had his son at 30, and their vacation ages were 60 and 30.',
        options=['50', '60', '70', '80'], sources=['IMG-20240823-WA0065.jpg'])
    add('oracle-past-perfect', 'Oracle', 'Correct tense for a loss before a past visit',
        'Find the erroneous part: “I regret that I wasn’t aware that you have lost your job when you visited me last week.”', 'Have lost your',
        'The job loss precedes the past visit and the speaker’s past lack of awareness. Use “had lost your job” to mark that earlier past event. “I regret” can remain present because the regret is expressed now.',
        topic='verbal', options=['I wasn’t aware', 'Have lost your', 'When you visited me', 'None of the options'], sources=['IMG-20240823-WA0064.jpg', 'IMG-20240823-WA0067.jpg', 'IMG-20240823-WA0068.jpg'])
    add('oracle-real-set', 'Oracle', 'Cardinality of a real-valued rational-inequality solution set',
        'S contains all positive real x satisfying (x²+5x+4)/(x²−7x+12) ≤ 0, with x≠3,4. What is the cardinality of S? The source choices are 0, 1, 2 and 3.', None,
        'Factor the numerator as (x+1)(x+4), which is positive for x>0. The denominator (x−3)(x−4) is negative precisely when 3<x<4. The numerator never vanishes in the positive domain. Hence S=(3,4), an uncountably infinite set, and none of the listed finite counts is correct. If the setter had meant positive integers, there would be no solutions, but that is a different domain.',
        topic='quant', type='subjective', sources=['IMG-20240823-WA0058.jpg', 'IMG-20240823-WA0071.jpg'], notes='Both screenshots explicitly say real positive values. The finite MCQ choices do not match that domain.')
    add('oracle-any-tree-path', 'Oracle', 'Maximum value sum along any nonempty tree path',
        'A tree rooted at node 0 is given by parent and values arrays. parent[i] identifies the parent of i and parent[0]=−1. Return the maximum sum of node values along any nonempty simple path. The path can start and finish anywhere and need not pass through the root. The tree is not restricted to two children per node.', None,
        'Process nodes in postorder. For each node, keep the largest downward sum beginning there: its value plus the largest positive child gain, or its value alone. A path whose highest node is this node can use at most two child branches, so update the global answer with the node value plus its two largest positive child gains. Initialise the answer to a node value rather than zero to handle all-negative input. Build an explicit traversal order and process it backwards to avoid Python recursion depth on a 100,000-node chain. O(n) time and O(n) space.',
        section='dsa', topic='trees', type='coding', hard=True, sources=[f'IMG-20240823-WA00{i}.jpg' for i in range(72, 76)], function_signature='bestSumAnyTreePath(parent, values)', constraints='1 ≤ n ≤ 10⁵; parent[0]=−1. Full value bounds are unclear in the angled screenshot.',
        examples=[{'input':'parent = [-1,0,1,2,0]\nvalues = [-2,10,10,-3,10]', 'output':'28', 'explanation':'Path 2→1→0→4 sums to 10+10−2+10.'}])
    add('oracle-reading-method', 'Oracle', 'Infer an alleged methodological failure from a passage',
        'Passage summary: Ancient political writers seriously and systematically organised data about political life and sought rules explaining how regimes arise and disappear. Their alleged failure lay in the way they pursued this study, rather than a lack of effort; later thinkers criticised their methodological naivety.\n\nAccording to the passage, what were the ancient writers allegedly unsuccessful at?', 'Establishing a methodology for the study of political science',
        'The criticism targets their method of inquiry. The passage explicitly acknowledges serious, systematic effort, ruling out insufficient effort and failure to study data systematically. It does not attribute the failure to a particular misunderstanding of how laws arise. The methodology choice best captures the stated criticism.',
        topic='verbal', options=['Establishing a methodology for the study of political science', 'Putting enough effort into establishing the discipline', 'Understanding how rules and laws came into being and passed away', 'Studying political data systematically'], sources=['IMG-20240823-WA0051.jpg', 'IMG-20240823-WA0052.jpg'], notes='The relevant portion of the long passage is paraphrased; answer choices are shortened without changing their distinction.')
    add('oracle-reading-louis', 'Oracle', 'Assess a passage about an enlightened absolutist',
        'Passage summary: War and royal extravagance depleted France’s treasury. The king’s proposed reforms increased spending, requiring additional taxes. Poor harvests raised bread prices, and taxes and royal excesses increased resentment. The passage says Louis XVI failed to establish himself as an enlightened absolutist.\n\nThe source asks which explains that failure, offering rising bread costs, citizens rejecting proposed ideals, nobles obstructing the king’s ideas, and the burden of taxes on citizens.', None,
        'The tax-burden option has the strongest direct support in the supplied text: increased expenditure necessitated additional taxes, followed by resentment. Bread costs also contributed to unrest, but the passage does not establish a single exclusive cause of the broad political failure. Neither citizens rejecting ideals nor nobles blocking their implementation is explicitly stated. Assess the answer from the given passage.',
        topic='verbal', type='subjective', sources=['IMG-20240730-WA0093.jpg', 'IMG-20240823-WA0054.jpg'], notes='The later screenshot supplies the previously missing choices. The cause-and-effect wording remains broad, so no answer is auto-graded.')
    for key, suffix in [('oracle-only-cricket','0076'), ('oracle-exam-idiom','0079'), ('oracle-hiring-idiom','0080'), ('oracle-autonomy','0081'), ('oracle-standing-order','0084'), ('oracle-favorite-color','0085'), ('oracle-painted-cube','0087'), ('oracle-five-ingredients','0089')]:
        merge(key, 'Oracle', ['IMG-20240823-WA'+suffix+'.jpg'])
    for suffix, reason in [('0069','diagram needs vector transcription'), ('0070','diagram needs vector transcription'), ('0077','chart question missing'), ('0078','division operands unclear in angled photograph'), ('0082','diagram needs vector transcription'), ('0083','diagram needs vector transcription'), ('0086','graph path condition needs transcription'), ('0088','graph path condition needs transcription')]:
        skip('Oracle', 'IMG-20240823-WA'+suffix+'.jpg', reason)
