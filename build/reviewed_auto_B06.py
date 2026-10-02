"""Axtria (HirePro analyst assessment): data structures, MS Office, reasoning, quant and verbal."""


def extend(add, merge, skip, alias):
    A = 'Axtria'

    def f(*ts):
        return [f'IMG_20240914_{t}_HDR_AE.jpg' for t in ts]

    def Q(key, title, stmt, options, ans, explain, steps, srcs, topic, section='aptitude', wrong='', fast='', traps='', **kw):
        sol = '### Solution\n' + steps.strip() + f'\n\n**Answer: {ans}**\n'
        if wrong:
            sol += '\n### Why the other options are wrong\n' + wrong.strip() + '\n'
        if fast:
            sol += '\n### Faster method\n' + fast.strip() + '\n'
        if traps:
            sol += '\n### Common traps\n' + traps.strip() + '\n'
        add(key, A, title, stmt, ans, explain, section=section, topic=topic, type='mcq', options=options,
            sources=srcs, solution=sol, **kw)

    Q('axtria-mid-square-hash', 'Hash key of 4352 using the mid-square method',
      'What will be the hash key for 4352 if the mid-square hashing technique is used?', ['2534', '1804', '2025', '9399'], '9399',
      'Square the key: 4352^2 = 18,939,904. Take the middle four digits of the 8-digit square: 9399.',
      '4352^2 = 18,939,904 (8 digits: 1 8 9 3 9 9 0 4). Mid-square hashing extracts the middle digits; the middle four are 9399.',
      f('162123376'), 'cs', section='cs', wrong='The other options are not middle digits of 18939904.', fast='Square, then drop equal numbers of digits from both ends.',
      confidence='medium', notes='The number of middle digits to extract (four) is assumed from the option lengths.')
    Q('axtria-excel-extract-filter', 'Excel feature to extract required data from a large pool',
      'Which one of the given functions is used to extract the required data from a large pool of data?', ['Count if', 'Sorting', 'Filter', 'Pivot table'], 'Filter',
      'Filter shows only the rows that meet chosen criteria, which is how required data is extracted from a large data set. Sorting only reorders, COUNTIF counts and a pivot table summarises.',
      'Filtering hides rows that do not meet the criteria, leaving the required records. COUNTIF returns a count, sorting changes order only and a pivot table aggregates rather than extracts rows.',
      f('162245844'), 'general-cs', section='cs', confidence='medium', notes='The stem is cropped after "from a large pool"; the filter answer is the standard one.')
    Q('axtria-max-heap-insert-50', 'Max heap built from 3 5 8 88 6 45 and then inserting 50',
      'Construct a max heap from the values 3, 5, 8, 88, 6, 45 (inserting them in the given order). Which statement is true when 50 is inserted into the resultant heap?',
      ['Height of heap is 3 (if root is at height 0)', '3, 8, 5 and 45 will be the leaf nodes.', 'Sibling of 8 is 50.', '88, 8, 5 and 50 are internal nodes.'], 'Sibling of 8 is 50.',
      'Inserting one by one gives [88, 8, 45, 3, 6, 5]. Adding 50 at the end and sifting up past 45 gives [88, 8, 50, 3, 6, 5, 45], so 8 and 50 are the two children of 88.',
      '''Insert one at a time with sift-up: 3 -> [3]; 5 -> [5,3]; 8 -> [8,3,5]; 88 -> [88,8,5,3]; 6 -> [88,8,5,3,6]; 45 -> [88,8,45,3,6,5].
Insert 50 at index 6 (child of index 2 = 45): 50 > 45 so swap: [88, 8, 50, 3, 6, 5, 45]. 50 < 88 stops.
Tree: root 88; children 8 and 50; 8 has 3, 6; 50 has 5, 45.
- Height is 2 (7 nodes), not 3.
- 8 is internal, so "3, 8, 5, 45 are leaves" is false.
- 8 and 50 are siblings: true.
- 5 is a leaf, so "88, 8, 5, 50 are internal" is false.''',
      f('162253897'), 'general-cs', section='cs', confidence='medium', notes='Assumes the heap is built by repeated insertion; a bottom-up heapify would give a different layout.',
      wrong='See the node-by-node checks above.', traps='- Using bottom-up heapify instead of insertion changes the shape.')
    Q('axtria-excel-subtract', 'Excel formula for the difference of cells A3 and A4',
      'If a user wants to calculate the difference between the cells A3 and A4, which of the below formulas should be used?', ['A3-A4', 'SUBTRACT(A3-A4)', 'STRACT(A3-A4)', 'SUB(A3-A4)'], 'A3-A4',
      'Excel has no SUBTRACT or SUB function; subtraction uses the minus operator (=A3-A4).', 'Excel subtracts with the - operator. SUBTRACT, STRACT and SUB are not Excel functions.',
      f('162312954'), 'general-cs', section='cs', notes='The stem is cropped after "which of the below formulas".')
    Q('axtria-circular-list-empty', 'Condition for an empty circular linked list with a tail pointer',
      'Consider a circular linked list L (nodes 3, 7, 45, 90, with head pointing to node 3 and the last node pointing back). Which option is used to indicate L is empty, if current is a pointer to the last node?',
      ['current == NULL', 'head == NULL', 'head == current == NULL', 'current == head'], 'current == NULL',
      'When the list is addressed through a pointer to its last node, an empty list is signalled by that pointer being NULL.',
      'In a circular list the last node points to the first, so keeping only a pointer to the last node is enough to reach both ends. The list is empty exactly when this pointer is NULL. current == head is true for a single node, not an empty list.',
      f('162325628'), 'general-cs', section='cs', confidence='medium', notes='The tail of the stem is cropped in the photo.',
      wrong='head == NULL is meaningful only if head is the pointer being kept; current == head holds for a one-node list.')
    Q('axtria-graph-true-statement', 'True statement about graphs',
      'Identify the TRUE statement about the graph.', ['Queue is used with an Adjacency List to represent a graph.', 'In a complete graph, the degree of each vertex is n-1.', 'In a regular graph, only the in-degree of each vertex should be the same.', 'None of the options given'],
      'In a complete graph, the degree of each vertex is n-1.',
      'Each vertex of a complete graph on n vertices is joined to the other n-1.',
      'In a complete graph every pair of vertices is adjacent, so each vertex has degree n-1. A queue is used for BFS, not to represent a graph; a regular graph needs every vertex to have the same degree (both in and out for directed graphs).',
      f('162335061'), 'general-cs', section='cs', wrong='Option 1 confuses representation with BFS; option 3 requires only in-degree equality, which is not the definition.')
    Q('axtria-unit-matrix-algorithm', 'What does the pseudocode compute on a square matrix',
      'Find(mat, size): flag = 1; for i = 0..size-1, for j = 0..size-1: if i = j and mat[i][j] != 1 then flag = 0, break; if i != j and mat[i][j] != 0 then flag = 0, break. After the loops, if flag = 1 write("Output"). What does the algorithm do?',
      ['Finds whether the given matrix is a unit matrix or not.', 'Finds whether the given matrix is a zero matrix or not.', 'Finds whether the given matrix is a scalar matrix or not.', 'Finds whether the given matrix is a singular matrix or not'], 'Finds whether the given matrix is a unit matrix or not.',
      'It requires all diagonal entries to be 1 and all off-diagonal entries to be 0, which defines the identity (unit) matrix.',
      'The flag is cleared if a diagonal entry is not 1 or an off-diagonal entry is not 0. "Output" is written only if every diagonal entry is 1 and every other entry is 0: the identity matrix. A scalar matrix would allow any equal diagonal value; a zero matrix needs all zeros.',
      f('162439435', '162447923'), 'general-cs', section='cs', wrong='Scalar allows other diagonal values, zero needs all zeros, singular is about the determinant.',
      traps='- The break only exits the inner loop, but flag stays 0.')
    Q('axtria-relation-expression', 'Blood relation from a coded expression M % N & O $ P & Q @ S',
      'X % Y means X is the daughter of Y; X @ Y means X is the son of Y; X $ Y means X is the mother of Y; X & Y means X is the brother of Y. How is N related to Q in the expression M % N & O $ P & Q @ S?',
      ['Father', 'Brother-in-law', 'Uncle', 'Grandfather'], 'Uncle',
      'N is the brother of O, O is the mother of P, and P is the brother of Q, so Q is also O\'s child. N is therefore Q\'s maternal uncle.',
      '''Read the chain: M % N means M is the daughter of N; N & O means N is the brother of O; O $ P means O is the mother of P; P & Q means P is the brother of Q; Q @ S means Q is the son of S.
Q and P are siblings, so O is also Q\'s mother. N is O\'s brother, so N is Q\'s maternal uncle.''',
      f('163156481'), 'logical', confidence='medium', notes='The expression is read from a photograph; the symbols follow the given definitions.',
      wrong='Father and grandfather would need N to be in the parent line; brother-in-law would need a marriage link.')
    Q('axtria-circle-radius', 'Radius of a circular field from its circumference',
      'The circumference of a circular field is 25 pi cm. What will be the radius of the field?', ['10 cm', '22.5 cm', '12.5 cm', '12 cm'], '12.5 cm',
      'C = 2 pi r = 25 pi, so r = 12.5 cm.', '2 pi r = 25 pi gives r = 25/2 = 12.5 cm.', f('163337966'), 'quant', confidence='medium',
      notes='The end of the stem is cropped; it asks for the radius.')
    Q('axtria-partnership-capital', 'Y\'s capital when he joins X after 7 months',
      'X started a business with Rs. 6500 and after 7 months, Y joined the business with some amount. After a year the profit was divided in the ratio 4 : 3. What is Y\'s contribution in the capital?',
      ['Rs. 20,800', 'Rs. 17,300', 'Rs. 11,700', 'Rs. 14,600'], 'Rs. 11,700',
      'X invests 6500 for 12 months and Y invests c for 5 months: 6500 x 12 : 5c = 4 : 3, so c = 78000 x 3 / 20 = 11,700.',
      'Profit shares are proportional to capital x time. X: 6500 x 12 = 78000. Y: c x 5. Ratio 78000 : 5c = 4 : 3, so 5c = 78000 x 3/4 = 58500 and c = 11,700.',
      f('163708141', '163825313'), 'quant', confidence='medium', notes='The middle of the stem is cropped; it is read as "after a year the profit was divided in the ratio 4:3".',
      wrong='The other options give a different ratio of capital-months.')
    Q('axtria-stocks-investment', 'Amount invested in the second stock',
      'Ben invests a total of Rs. 5000 in two different stocks, the first stock quoted at Rs. 154 gets a dividend of 7% and the second stock is quoted at Rs. 99 gets a dividend of 11%. If his total annual income is Rs. 375, find the amount he invested in the second stock which gives an 11% dividend.',
      ['Rs. 3000', 'Rs. 2000', 'Rs. 2250', 'Rs. 3500'], 'Rs. 2250',
      'Income per rupee: 7/154 = 1/22 and 11/99 = 1/9. With x in the first: x/22 + (5000 - x)/9 = 375, so x = 2750 and the second is 2250.',
      'Dividend is on face value, so income per rupee invested = dividend% / quoted price: 7/154 = 1/22; 11/99 = 1/9.\nx/22 + (5000 - x)/9 = 375 -> 9x + 22(5000 - x) = 74250 -> 110000 - 13x = 74250 -> x = 2750.\nSecond stock = 5000 - 2750 = 2250.',
      f('171812520'), 'quant', confidence='medium', notes='The front of the stem is cropped; it reads "Ben invests ... find the amount he invested in the second stock".')
    Q('axtria-guns-train-speed', 'Speed of a train from the interval between two gunshots',
      'Two guns are fired from the same place at an interval of 26 minutes but a person in a train approaching the place hears the second shot 24 min after he heard the first shot. Find the speed of the train, if sound travels at 330 m/s.',
      ['27.5 m/s', '25 m/s', '22.8 m/s', '12.5 m/s'], '27.5 m/s',
      'Let v be the train speed. The second shot is heard 26 - 26v/(330 + v) minutes after the first, so 26v/(330 + v) = 2 and v = 27.5 m/s.',
      '''Let the first sound reach the train at time t1 = D/(330 + v). The second shot is fired 26 min later when the train is 26v closer, so it is heard at 26 + (D - 26v)/(330 + v).
Gap between hearings = 26 - 26v/(330 + v) = 24 (minutes), so 26v/(330 + v) = 2.
26v = 660 + 2v -> 24v = 660 -> v = 27.5 m/s.''', f('171908427'), 'quant', confidence='medium',
      notes='The end of the stem is cropped; it is read as the train approaching the place.', fast='Relative closing: 26v = 2(330 + v).',
      traps='- Using v x 26 = 330 x 2, which ignores the train\'s own motion during the sound travel and gives 25.4.')
    Q('axtria-gp-sixth-term', 'Sixth term of a GP from its eighth and ninth terms',
      'The ninth term of the Geometric progression is 81 and the eighth term is 27. Find the 6th term of the GP.', ['3', '9', '1/3', '1/9'], '3',
      'The common ratio is 81/27 = 3. The sixth term is the eighth divided by 3^2: 27/9 = 3.', 'r = a9 / a8 = 3. a6 = a8 / r^2 = 27 / 9 = 3.',
      f('172016874', '172019610'), 'quant', wrong='9 would be the 7th term; 1/3 and 1/9 would need ratios below 1.')
    Q('axtria-escape-letter-pairs', 'Letter pairs in ESCAPE with as many letters between them as in the alphabet',
      'How many pairs of letters are there in the word \'ESCAPE\' which has as many letters between them (from both sides) in the word as there are between them in the alphabets from A to Z?',
      ['3', '1', '0', '2'], '2',
      'E and C have one letter between them in the word (S) and one in the alphabet (D); S and P have two letters between them in the word (C, A) and two in the alphabet (Q, R). No other pair matches.',
      'List each pair with the number of letters between them in the word and in the alphabet. E(1)-C(3): 1 and 1 (D). S(2)-P(5): 2 (C, A) and 2 (Q, R). All other pairs differ, for example C-A has 0 in the word and 1 in the alphabet, E-S has 1 against 13.',
      f('172042572'), 'logical', confidence='medium', notes='The end of the stem ("from both the sides") is cropped.')
    Q('axtria-average-speed', 'Average speed for a round trip at 50 km/h and 75 km/h',
      'Haritha travelled from Pune to Kolkata at a speed of 50 km/hr and returned to Pune at a speed of 75 km/hr. Find the average speed of Haritha.',
      ['58 km/hr', '50 km/hr', '60 km/hr', '55 km/hr'], '60 km/hr',
      'For equal distances the average speed is the harmonic mean: 2 x 50 x 75 / (50 + 75) = 60 km/h.', 'Distance d each way. Time = d/50 + d/75 = 5d/150 = d/30. Total distance 2d, so average speed = 2d / (d/30) = 60 km/h.',
      f('172127153'), 'quant', fast='2ab/(a + b).', traps='- Taking the arithmetic mean 62.5.', wrong='58 and 55 are not the harmonic mean.')
    Q('axtria-locker-code-trials', 'Maximum trials to open a locker whose code is an odd number between 50 and 450 using digits 0 to 5',
      'If a thief wants to rob a jewelry shop, whose locker code information is an odd number between 50 and 450 and the digits are from the set 0 to 5 (repetition allowed), how many maximum trials does he have to take to unlock the locker?',
      ['68', '70', '75', '72'], '72',
      'Count odd numbers from 51 to 449 with all digits in 0-5. Two-digit: 51, 53, 55 (3). Hundreds 1 to 3: 3 x 6 x 3 = 54. Hundreds 4: tens 0 to 4 and odd units: 5 x 3 = 15. Total 72.',
      '''Digits allowed: 0 to 5, units digit odd: 1, 3, 5.
- 51 to 99 with digits 0-5: tens digit 5 gives 51, 53, 55 -> 3.
- 100 to 399: hundreds 1, 2, 3 (3 choices), tens any of 6, units 3 choices -> 54.
- 400 to 449: hundreds 4, tens 0 to 4 (5 choices, since 45x is above 450 for odd x), units 3 choices -> 15.
Total = 3 + 54 + 15 = 72.''', f('172149928'), 'quant', confidence='medium', notes='The stem is partly cropped on the right; the range and digit-repetition assumption are inferred and reproduce an offered option.')
    Q('axtria-sentence-over-his', 'Sentence correction: sovereign above his own person',
      'Identify if the underlined part in the sentence is incorrect. If yes, choose the option which makes the sentence grammatically correct. If no, choose the option that is the same as the underlined part.\n\nIn a purely free society, each individual is sovereign above his own person and property.',
      ['above his', 'under him', 'over his', 'within is'], 'over his',
      'One is "sovereign over" something. "Above" is the wrong preposition here.', 'The collocation is "sovereign over". "Under him" reverses the meaning and "within is" is ungrammatical.',
      f('172054294'), 'verbal', wrong='"above his" is the original wrong preposition.')
    Q('axtria-para-hurricane', 'Sentence ordering: the 1947 hurricane seeding flight',
      'Choose the most logical order of the given sentences to construct a coherent paragraph.\nA. The airplane circled for a while, then turned for home.\nB. Two days earlier, a hurricane had wreaked havoc in Miami, but had since been treading water 350 miles to the east.\nC. For reasons as obscure as they were controversial, the hurricane followed [the plane back].\nD. On the morning of October 13, 1947, a Boeing B-17 loaded with 180 pounds of crushed dry ice took off from MacDill Field.\nE. The U.S. Air Force B-17 rendezvoused with the storm and climbed 500 feet above its dark upper clouds, where the crew dropped a thousand white pebbles of dry ice (frozen carbon dioxide).',
      ['DABEC', 'DEBCA', 'DEACB', 'DBEAC'], 'DBEAC',
      'D opens with the flight, B gives the hurricane background, E describes the seeding, A the return, and C the hurricane following.',
      'D introduces the flight. B explains which storm (two days earlier, treading water). E says the B-17 met the storm and dropped dry ice. A: the plane circled, then went home. C: the hurricane then followed. DBEAC.',
      f('171934248', '171941555'), 'verbal', confidence='medium', notes='Some sentence endings are cropped in the photographs.')
    Q('axtria-one-word-rapturous', 'One-word substitution: a face filled with pleasure and excitement',
      'Choose the option that can be substituted for the given sentence/phrase: A face filled with pleasure and excitement.',
      ['Everyouth face', 'Rapturous face', 'Cosmic face', 'Ironic face'], 'Rapturous face',
      '"Rapturous" means expressing great pleasure or enthusiasm.', 'Rapturous means full of intense joy and excitement. Cosmic relates to the universe and ironic to irony; "everyouth" is not a word.',
      f('172134534'), 'verbal', confidence='medium', notes='Option 1 is hard to read in the photograph.')
    for s, why in [('163851989', 'stem cropped (rectangle wire stretched)'), ('171759894', 'stem cropped (college subjects)'),
                   ('171827528', 'stem cropped (blood relation)'), ('171848368', 'blurry code-language item'),
                   ('171853423', 'blurry code-language item'), ('172020275', 'blurry unreadable'), ('172210357', 'unreadable stem'),
                   ('162807686', 'height/class puzzle with cropped option list')]:
        skip(A, f'IMG_20240914_{s}_HDR_AE.jpg', why)
    skip(A, 'IMG_20240914_171836154_BURST000_COVER.jpg', 'stem cropped (partnership profit share)')
    skip(A, 'IMG_20240914_171836154_BURST001.jpg', 'stem cropped (partnership profit share)')
