"""ZS Associates: numerical ability, analytical reasoning, estimation, Hungry Kya case study, SQL."""


def S(body, wrong='', fast='', traps=''):
    out = '### Solution\n' + body.strip() + '\n'
    if wrong:
        out += '\n### Why the other options are wrong\n' + wrong.strip() + '\n'
    if fast:
        out += '\n### Faster method\n' + fast.strip() + '\n'
    if traps:
        out += '\n### Common traps\n' + traps.strip() + '\n'
    return out


def extend(add, merge, skip, alias):
    Z = 'ZS Associates'
    P = 'ZS  .pdf'

    # ---------------- Quant ----------------
    add('zs-quant-trader-profit', Z, 'Profit percentage when buying 20 for $15 and selling 16 for $15',
        'A trader bought some items at a rate of 20 items for $15 and later sold them at a rate of 16 items for $15. Find the profit percentage for the trader.',
        '25%', 'Cost per item is 15/20 = $0.75 and selling price per item is 15/16 = $0.9375. Profit = 0.1875, so profit percent = 0.1875/0.75 = 25%.',
        section='aptitude', topic='quant', type='mcq', sources=['20.48.59_85613b4a.jpg', P], options=['12.5%', '16%', '20%', '25%'],
        solution=S('''Cost per item = 15/20 = 0.75. Selling price per item = 15/16 = 0.9375.
Profit = 0.9375 - 0.75 = 0.1875.
Profit % = 0.1875 / 0.75 x 100 = 25%.

**Answer: 25%**''', wrong='12.5% and 16% come from dividing by the wrong base; 20% is the profit on selling price (4/20 items extra).',
                  fast='Pick 80 items: cost = 4 x 15 = $60; sold at 5 x 15 = $75. Profit = 15/60 = 25%.',
                  traps='- Using selling price as the base (gives 20%).'))
    add('zs-quant-pets-venn', Z, 'People owning all three breeds (three-set Venn)',
        'In a community of 52 members, each person has at least one pet among Dobermans, Spitzes, or Terriers. Among the members, 24 own Dobermans, 24 own Spitzes, and 35 own Terriers. No person owns more than one pet of the same breed. Additionally, there are 13 individuals who own pets of exactly two different breeds. How many people own pets of all three breeds?',
        '9', 'Let a own exactly one breed, 13 own exactly two and t own all three. People: a + 13 + t = 52. Pets: a + 26 + 3t = 83. Subtracting gives 13 + 2t = 31, so t = 9.',
        section='aptitude', topic='quant', type='mcq', sources=['20.49.54_820dfdb7.jpg', P], options=['5', '9', '13', '18'],
        solution=S('''Let a = exactly one breed, b = exactly two (13), t = all three.
1. Members: a + b + t = 52.
2. Pet count (one pet per breed owned): a + 2b + 3t = 24 + 24 + 35 = 83.
3. Subtract: b + 2t = 31, so 13 + 2t = 31, giving t = 9. (Then a = 52 - 13 - 9 = 30; check 30 + 26 + 27 = 83.)

**Answer: 9**''', wrong='5, 13 and 18 fail the pet-count equation a + 2b + 3t = 83.',
                  fast='Total pets minus total people = b + 2t = 83 - 52 = 31.',
                  traps='- Using the "exactly two" count as the total of pairwise overlaps (it excludes the triple overlap).'))
    add('zs-quant-paint-ratio', Z, 'Colour ratio in the lower half of a painting',
        'The ratio of the quantities of black, white, and blue colours used in a round canvas painting is 4 : 3 : 2 respectively. If, in the upper half of the painting, black, white, and blue colours are in the ratio 2 : 3 : 1 respectively, then what is the ratio of black, white, and blue in the lower half of the painting? (Assume equal paint in both halves.)',
        '10 : 3 : 5', 'The total ratio sum is 9, so each half has 4.5 parts. Upper half: 4.5 x (2, 3, 1)/6 = (1.5, 2.25, 0.75). Lower half = (4 - 1.5, 3 - 2.25, 2 - 0.75) = (2.5, 0.75, 1.25), which scales to 10 : 3 : 5.',
        section='aptitude', topic='quant', type='mcq', sources=['20.50.40_e801c22f.jpg'], options=['10 : 3 : 5', '8 : 7 : 4', '5 : 9 : 4', '2 : 2 : 3'],
        notes='The ratio 4:3:2 was read from the photo; equal quantities in both halves is the assumption that makes one option fit.',
        solution=S('''1. Total quantity = 4 + 3 + 2 = 9 parts; assume each half uses 4.5 parts.
2. Upper half ratio 2:3:1 has sum 6, so the scale factor is 4.5/6 = 0.75: black 1.5, white 2.25, blue 0.75.
3. Lower half = total minus upper: black 2.5, white 0.75, blue 1.25.
4. Multiply by 4: 10 : 3 : 5.

**Answer: 10 : 3 : 5**''', wrong='Check each other option against "upper + lower = 4:3:2 with equal halves"; none works.',
                  fast='Use total = 18 parts (8, 6, 4), so 9 per half. Upper half 2:3:1 scaled to 9 is 3, 4.5, 1.5, so lower = 5, 1.5, 2.5 = 10 : 3 : 5.',
                  traps='- Forgetting each half holds equal paint.'))
    add('zs-quant-combinations-ab', Z, 'Choosing 3 of 6 people with A and B not together',
        'In how many ways can 3 people be chosen from 6 people, A, B, C, D, E and F, so that both A and B are not selected together?',
        '16', 'Total ways C(6,3) = 20. Ways with both A and B selected: choose the third from the remaining 4, giving 4. So 20 - 4 = 16.',
        section='aptitude', topic='quant', type='mcq', sources=['20.50.47_8f841b07.jpg'], options=['12', '16', '18', '19'],
        solution=S('''Total selections = C(6,3) = 20.
Selections containing both A and B: pick the third person from C, D, E, F = 4 ways.
Required = 20 - 4 = 16.

**Answer: 16**''', wrong='12 subtracts too much; 18 and 19 subtract too little.',
                  fast='Complement counting: total minus the "bad" cases.',
                  traps='- Subtracting 2 (the A-only and B-only cases) instead of the "both" count.'))
    add('zs-quant-pqr-marks', Z, 'Percent by which P\'s marks exceed R\'s',
        'Three students, P, Q, and R appeared at an examination. P\'s marks are 50% of the sum of the marks of P, Q and R. R\'s marks are 60% less than the combined marks of Q and P. Find by what percent P\'s marks are more than R\'s marks.',
        '75%', 'P = 0.5(P+Q+R) gives P = Q + R. R = 0.4(P+Q). Substituting Q = P - R: R = 0.4(2P - R), so 1.4R = 0.8P and R = 4P/7. Then (P - R)/R = (3/7)/(4/7) = 75%.',
        section='aptitude', topic='quant', type='mcq', sources=['20.50.58_87fcd242.jpg', P], options=['50%', '75%', '25%', "Can't be determined"],
        solution=S('''1. P = 50% of (P+Q+R) means P = Q + R, so Q = P - R.
2. R is 60% less than (Q+P): R = 0.4(Q+P) = 0.4(2P - R) => R = 0.8P - 0.4R => 1.4R = 0.8P => R = 4P/7.
3. Q = 3P/7 (check: Q + R = P).
4. P exceeds R by (P - R)/R = (3P/7)/(4P/7) = 3/4 = 75%.

**Answer: 75%**''', wrong='50% and 25% come from using P as the base; "cannot be determined" fails because the ratio is fixed.',
                  fast='Let P = 7, then Q = 3, R = 4. (7 - 4)/4 = 75%.',
                  traps='- Computing the difference as a percent of P instead of R.'))
    add('zs-quant-three-numbers', Z, 'Three numbers in doubling progression with average of last two',
        'Three numbers are given, the first number is half the second, and the second number is half the third. If the average of the second and third numbers is 93, determine the value of the first number.',
        '31', 'Let the numbers be x, 2x, 4x. The average of 2x and 4x is 3x = 93, so x = 31.',
        section='aptitude', topic='quant', type='mcq', sources=['hhh.jpg', P], options=['25', '31', '27', '33'],
        solution=S('Let the first number be x; the others are 2x and 4x. (2x + 4x)/2 = 3x = 93, so x = 31.\n\n**Answer: 31**',
                  wrong='Other options do not give 3x = 93.', fast='The average of the last two is 3 times the first number, so first = 93/3.', traps='- Taking the first number as half of 93.'))
    add('zs-quant-couples-seating', Z, 'Seating 3 couples adjacently in a row',
        'In how many ways can 3 couples be seated on 6 chairs lying in a row, such that every husband and wife are seated adjacent to each other?',
        '48', 'Treat each couple as a block: 3! arrangements of blocks, and each couple can swap seats in 2 ways, so 3! x 2^3 = 48.',
        section='aptitude', topic='quant', type='mcq', sources=[P], options=['12', '24', '48', '120'],
        solution=S('3 couples become 3 blocks arranged in 3! = 6 ways. Inside each block the two partners can be ordered in 2 ways, giving 2 x 2 x 2 = 8.\nTotal = 6 x 8 = 48.\n\n**Answer: 48**',
                  wrong='12 and 24 ignore the internal swaps; 120 = 5! is arbitrary.', fast='n! x 2^n with n = 3.', traps='- Forgetting the internal swap factor 2^3.'))
    add('zs-quant-chocolate-sp', Z, 'Selling price per chocolate for 25 percent profit after a loss',
        'A shopkeeper sells 5 chocolates for $4 and incurs a loss of $2 in the transaction. At what price should he sell each chocolate to make a profit of 25%?',
        '$1.5', 'Cost of 5 chocolates = 4 + 2 = $6, so cost per chocolate = $1.2. For 25% profit, SP = 1.25 x 1.2 = $1.5.',
        section='aptitude', topic='quant', type='mcq', sources=[P], options=['$1.2', '$1.5', '$2', '$2.5'],
        solution=S('The sale price of 5 chocolates is $4 with a $2 loss, so their cost price is $6, i.e. $1.2 each.\nFor 25% profit: 1.2 x 1.25 = $1.5.\n\n**Answer: $1.5**',
                  wrong='$1.2 is the cost price; $2 and $2.5 are too high.', fast='CP = SP + loss; then multiply by 1.25.', traps='- Using $4/5 = $0.8 as the cost price.'))
    add('zs-quant-commission', Z, 'Commission as a percent of basic pay',
        'A man\'s salary comprises basic pay (fixed) and commission. In a particular month, he got 20% less commission than in the previous month, and as a result, his total salary was reduced by 5%. The commission he received last month was what percent of the basic pay?',
        '33.33%', 'Let basic = B and last month commission = C. The 20% drop in commission (0.2C) equals 5% of the previous total: 0.2C = 0.05(B + C), so 0.15C = 0.05B and C = B/3.',
        section='aptitude', topic='quant', type='mcq', sources=[P], options=['16.66%', '33.33%', '50%', '100%'],
        solution=S('The fall in salary equals the fall in commission: 0.2C = 0.05(B + C).\n0.2C - 0.05C = 0.05B -> 0.15C = 0.05B -> C = B/3 = 33.33% of B.\n\n**Answer: 33.33%**',
                  wrong='Other values do not satisfy 0.2C = 0.05(B + C).', fast='20% of C is 5% of (B + C), so C : (B + C) = 1 : 4, hence C : B = 1 : 3.', traps='- Using this month\'s total as the base for the 5% reduction.'))
    add('zs-quant-proportion-add', Z, 'Number to add to 5, 17, 41, 89 to make them proportional',
        'What number should be added to each of the numbers 5, 17, 41, and 89 so that they are in proportion?',
        '7', 'For proportion (5+x) : (17+x) = (41+x) : (89+x): (5+x)(89+x) = (17+x)(41+x). Expanding: 445 + 94x = 697 + 58x, so 36x = 252 and x = 7. Check: 12:24 = 48:96.',
        section='aptitude', topic='quant', type='mcq', sources=[P], options=['3', '5', '7', '8'],
        solution=S('Condition: (5+x)/(17+x) = (41+x)/(89+x).\nCross multiply: 445 + 94x + x^2 = 697 + 58x + x^2 -> 36x = 252 -> x = 7.\nCheck: 12, 24, 48, 96 are in ratio 1:2:4:8, so 12:24 = 48:96.\n\n**Answer: 7**',
                  wrong='x = 3 gives 8:20 vs 44:92; x = 5 gives 10:22 vs 46:94; x = 8 gives 13:25 vs 49:97; none are equal.', fast='Plug the options: 7 gives 12, 24, 48, 96.', traps='- Forgetting that the x^2 terms cancel.'))
    add('zs-quant-salary-ratio', Z, 'Ratio of salaries in March after percentage changes',
        'In a particular year, the salaries of employees P and Q in January were in the ratio of 3 : 2, respectively. P\'s salary ratio for January and February was 4 : 5, while Q\'s salary ratio for January and February was 2 : 3. In March, P\'s salary decreased by 20% and Q\'s salary decreased by 25% from their respective previous month\'s salary. What is the ratio of the salaries of P and Q in March, respectively?',
        '4 : 3', 'Take January salaries P = 12, Q = 8. February: P = 15, Q = 12. March: P = 12, Q = 9. Ratio 12 : 9 = 4 : 3.',
        section='aptitude', topic='quant', type='mcq', sources=[P], options=['7 : 4', '7 : 5', '8 : 7', '4 : 3'],
        solution=S('January: P = 12, Q = 8 (3 : 2 scaled by 4).\nFebruary: P = 12 x 5/4 = 15, Q = 8 x 3/2 = 12.\nMarch: P = 15 x 0.8 = 12, Q = 12 x 0.75 = 9.\nRatio = 12 : 9 = 4 : 3.\n\n**Answer: 4 : 3**',
                  wrong='The other ratios come from applying the decreases to the wrong month.', fast='Use P = 12, Q = 8 so every step stays an integer.', traps='- Applying the percentage decreases to January salaries.'))
    add('zs-quant-fest-sets', Z, 'Percentage of students in the dance competition',
        'In a college fest, 40% of the students participated in the painting competition, and 20% of those who participated in the painting competition also participated in the dance competition. If 40% of the students participated in neither the dance nor the painting competition, what is the percentage of students who participated in the dance competition?',
        '28%', 'Painting 40%, both = 20% of 40 = 8%, neither = 40% so union = 60%. Dance = union - painting + both = 60 - 40 + 8 = 28%.',
        section='aptitude', topic='quant', type='mcq', sources=[P], options=['20%', '28%', '32%', '40%'],
        solution=S('Union = 100 - 40 = 60%.\nBoth = 0.2 x 40 = 8%.\nUnion = Painting + Dance - Both -> 60 = 40 + D - 8 -> D = 28%.\n\n**Answer: 28%**',
                  wrong='20%, 32% and 40% do not satisfy the union equation.', fast='Dance = 60 - 40 + 8.', traps='- Forgetting to add back the overlap.'))
    add('zs-quant-judge-arrangements', Z, 'Arrangements of JUDGE with all consonants not together',
        'In how many ways can the letters of the word JUDGE be arranged so that all consonants are not together?',
        '84', 'The word has 5 distinct letters (120 arrangements). Consonants J, D, G; vowels U, E. Arrangements with all three consonants together = 3! x 3! = 36. So 120 - 36 = 84.',
        section='aptitude', topic='quant', type='mcq', sources=[P], options=['65', '72', '84', '114'],
        solution=S('Total arrangements = 5! = 120.\nConsonants J, D, G together: treat them as one block, so 3 units (block, U, E) are arranged in 3! = 6 ways; inside the block 3! = 6 ways. 6 x 6 = 36.\nRequired = 120 - 36 = 84.\n\n**Answer: 84**',
                  wrong='72 would be 120 - 48; 65 and 114 do not come from any valid count.', fast='Complement: total minus "together".', traps='- Reading "not together" as "no two consonants adjacent" (that would give 12).'))

    # ---------------- Logical / reasoning ----------------
    add('zs-lr-direction-journey', Z, 'Starting direction from turns',
        'Mr. X travelled a certain distance straight ahead from station A. He then turned left and travelled some more distance to reach station B. Finally, he turned to his right from station B and travelled some more distance. If he was finally facing South, in which direction did he start the journey?',
        'South', 'A left turn and then a right turn cancel each other, so the final facing direction equals the starting direction. He finally faces South, so he started facing South.',
        section='aptitude', topic='logical', type='mcq', sources=[P], options=['South-West', 'North', 'South', 'North-East'],
        solution=S('Starting direction = d. After turning left he faces d rotated 90 degrees anticlockwise; turning right then rotates 90 degrees clockwise, back to d. Final direction = d = South.\n\n**Answer: South**',
                  wrong='Any other start would end in a different final direction.', fast='Left followed by right means no net turn.', traps='- Thinking the two turns point you in a new direction.'))
    alias('b05_zs_fractal-008', Z, ['ZS  .pdf'])
    alias('b05_zs_fractal-003', Z, ['ZS  .pdf'])
    add('zs-lr-rank-position', Z, 'Position of R between two interchanged ranks',
        'In a class test ranking, each student secured a unique position. \'P\' holds the 27th position from the top, while \'Q\' holds the 24th position from the bottom. If they interchange their positions, \'P\' will then occupy the 13th position from the top. If \'R\' is positioned exactly between \'P\' and \'Q\', what will be R\'s position from the top?',
        '20th', 'After the interchange P takes Q\'s old place, so Q was 13th from the top. P was 27th. R is exactly midway: (13 + 27)/2 = 20th from the top.',
        section='aptitude', topic='logical', type='mcq', sources=[P], options=['20th', '15th', '23rd', '19th'],
        solution=S('Q originally = 13th from the top (that is the seat P gets). P originally = 27th. The middle of 13 and 27 is (13 + 27)/2 = 20, with 6 students between 13 and 20 and 6 between 20 and 27. (Total students = 13 + 23 = 36.)\n\n**Answer: 20th**',
                  wrong='15th, 23rd and 19th are not midway between 13 and 27.', fast='Midpoint formula.', traps='- Using the interchanged positions for R.'))
    add('zs-lr-bags-weights', Z, 'Weights of bags: truth of the third statement',
        'There are four bags, A, B, C, and D, with different weights loaded onto a wagon. It is known that:\nI. Bag B is heavier than bag D but not the heaviest.\nII. Bag C is heavier than bag D but lighter than bag A.\nIII. Only one bag is heavier than bag B.\n\nIf the first two statements are true, what can be said about the third statement?',
        'Uncertain', 'From I and II: A > C > D and B > D, B not heaviest. B could be between A and C (A > B > C > D, only A heavier: III true) or between C and D (A > C > B > D, two bags heavier: III false). So it is uncertain.',
        section='aptitude', topic='logical', type='mcq', sources=[P], options=['True', 'False', 'Uncertain'],
        solution=S('Known: A > C > D, B > D, and B is not the heaviest.\nCase 1: A > B > C > D. Only A is heavier than B: III true.\nCase 2: A > C > B > D. A and C are heavier than B: III false.\nBoth cases fit statements I and II, so the third statement is uncertain.\n\n**Answer: Uncertain**',
                  wrong='"True" and "False" each fail in one valid arrangement.', fast='Enumerate where the unconstrained bag can sit.', traps='- Assuming B is directly below A.'))
    add('zs-lr-seating-six', Z, 'Six girls seated in a row: who sits at the ends',
        'Six girls Jasmine, Kara, Linda, Megan, Nora, and Oliver are sitting in a row facing North, but not necessarily in the same order.\n- Kara is sitting third to the right of Linda.\n- The number of people to the left of Kara is the same as the number of people to the right of Linda.\n- Megan and Nora are sitting adjacent to each other.\n\nWho among the given pairs is sitting at the end of the row?',
        'Oliver and Jasmine', 'Number seats 1 to 6 from left to right. If Linda is at L, Kara is at L + 3, and K - 1 = 6 - L gives L = 2, K = 5. Megan and Nora must be adjacent in the remaining seats {1, 3, 4, 6}, so they take 3 and 4. Jasmine and Oliver take the ends 1 and 6.',
        section='aptitude', topic='logical', type='mcq', sources=[P], options=['Kara and Linda', 'Oliver and Jasmine', 'Linda and Jasmine', 'Kara and Oliver'],
        solution=S('''1. Facing North, right means a higher seat number. Kara = Linda + 3.
2. People to Kara\'s left = K - 1; people to Linda\'s right = 6 - L. Equal: L + 2 = 6 - L -> L = 2, K = 5.
3. Free seats: 1, 3, 4, 6. Megan and Nora need adjacent seats: only 3 and 4.
4. Jasmine and Oliver fill 1 and 6, the two ends.

**Answer: Oliver and Jasmine**''', wrong='Linda (seat 2) and Kara (seat 5) are not at the ends.', fast='The equation from the two counts gives Linda and Kara; adjacency pushes the others to the ends.', traps='- Reading "right" as the viewer\'s right instead of the girls\' right.'))
    add('zs-lr-car-colour', Z, 'Who owns the Audi among three friends',
        'Three friends, Jassi, Kane, and Roman, have three different cars, namely Audi, Ferrari, and Mercedes, of three different colours Red, White, and Yellow, not necessarily in the same order.\n- Jassi has a red colour car which is not an Audi.\n- Kane has a Mercedes which is not yellow.\n\nWho among them has the Audi?',
        'Roman', 'Kane has the Mercedes. Jassi\'s car is not an Audi and not the Mercedes, so it is the Ferrari. The Audi is left for Roman.',
        section='aptitude', topic='logical', type='mcq', sources=[P], options=['Jassi', 'Kane', 'Roman', 'Either Jassi or Kane'],
        solution=S('Kane has the Mercedes. Jassi has neither the Audi nor the Mercedes (taken), so the Ferrari (red). Roman gets the Audi. (Colours: Jassi red, Kane not yellow so white, Roman yellow.)\n\n**Answer: Roman**',
                  wrong='Jassi is excluded by the clue and Kane has the Mercedes.', fast='Eliminate by cars first; colours are not needed.', traps='- Spending time on colours, which do not affect the answer.'))

    # ---------------- Estimation / case ----------------
    add('zs-est-dubai-mall', Z, 'Estimate the daily footfall of the Dubai Mall',
        'You are shown a set of statements. Use the data in these statements to find the answer to the question. Not all the data may be relevant. Round decimal answers to the next whole number.\n\nRelevant statements: 8) In 2008 the total footfall was 32 million in a year, and since then the number of visitors increased by 20%, then 24%, then 28%, then 23% and 25% in the following years. 14) The days of 2013 are used for calculation (365 days). 15) Footfalls include visitors and workers. 16) The mall is open 24 hours a day. (Other statements cover shops, workers, parking, revenue and hours.)\n\nHow many people footfall into Dubai Mall in a day?',
        '256736',
        'Footfall in 2013 = 32 million x 1.20 x 1.24 x 1.28 x 1.23 x 1.25 = 93,708,288. Dividing by 365 days gives 256,735.7, which rounds up to 256,736 per day. The worker, parking and revenue statements are distractors because footfall already includes workers.',
        section='aptitude', topic='data-interpretation', type='numeric', confidence='medium',
        sources=['20.39.23_17e0af9b.jpg', '20.39.36_5300d67b.jpg'],
        notes='Interpretation: statement 15 says footfalls include visitors and workers, so no extra worker count is added. If the intended answer adds workers separately the number would differ.',
        solution=S('''1. 2009: 32 x 1.20 = 38.4 million.
2. 2010: 38.4 x 1.24 = 47.616 million.
3. 2011: 47.616 x 1.28 = 60.948 million.
4. 2012: 60.948 x 1.23 = 74.966 million.
5. 2013: 74.966 x 1.25 = 93.708 million (93,708,288).
6. Per day: 93,708,288 / 365 = 256,735.7, rounded up to the next whole number = 256,736.

**Answer: 256,736 people per day**''', fast='Multiply the growth factors first: 1.2 x 1.24 x 1.28 x 1.23 x 1.25 = 2.928384, then 32M x 2.928384 / 365.',
                  traps='- Starting the growth in 2008 instead of 2009 (the first increase gives 2009).\n- Adding workers on top of the footfall, although statement 15 says they are included.\n- Using 366 or 360 days.'))
    add('zs-est-ipod-songs', Z, 'Songs stored on iPods in India (million)',
        'Use the given statements to answer. Round decimal answers to the next whole number.\n\nRelevant statements: 2) The average song length is 4 minutes 20 seconds. 10) A total of 488,600,000 hours of music is stored in iPods in India. (The statements about population, market share, prices, sizes and storage are distractors.)\n\nHow many songs in total are stored in iPods in India? (in million)',
        '6766', 'Convert hours to minutes: 488,600,000 x 60 = 29,316,000,000 minutes. One song is 4 min 20 s = 13/3 minutes. Songs = 29,316,000,000 x 3/13 = 6,765.2 million, rounded up to 6,766 million.',
        section='aptitude', topic='data-interpretation', type='numeric', confidence='medium', sources=['20.39.49_5f47ee75.jpg'],
        notes='Rounding: 6,765.23 million is rounded up to the next whole number per the instruction.',
        solution=S('''1. 488,600,000 hours = 488,600,000 x 60 = 29,316,000,000 minutes.
2. Song length = 4 min 20 s = 260 s = 13/3 min.
3. Number of songs = 29,316,000,000 / (13/3) = 29,316,000,000 x 3 / 13 = 6,765,230,769.
4. In millions: 6,765.23, rounded up = 6,766.

**Answer: 6,766 million songs**''', fast='Work in seconds: hours x 3600 / 260 = 488.6M x 13.846 = 6,765M.', traps='- Using the file size (8 MB) and the iPod capacity statements; they are distractors.'))
    add('zs-est-movie-halls', Z, 'Estimate the number of movie halls in Delhi',
        'Use the statements to find the number of movie halls in Delhi (round up to the next whole number).\n\n1) Delhi population is 22 million. 2) Total average monthly revenue is Rs 1.2 billion. 3) Average ticket price is Rs 200. 4) 10 movies run on any day. 5) About 30% of the population is below 14 years. 6) About 5% is above 60 years. 7) 5% of children below 14 and 5% of people above 60 go for an average of one movie per month. 8) 20% of the population in the 14-60 age group go for an average of 2 movies per month. 9) 80% of the halls are multiplexes (4 screens) and 20% are single-screen halls. 10) Average optimum capacity per screen is 300. 11) Monday to Friday average occupancy is 40% and on Saturday-Sunday 70%. 12) There are on average 4 shows per screen per day.',
        '103', 'Monthly tickets: children 22M x 0.30 x 0.05 = 0.33M, seniors 22M x 0.05 x 0.05 = 0.055M, adults (65%) 14.3M x 0.20 x 2 = 5.72M, total 6.105M. Average screens per hall = 0.8 x 4 + 0.2 x 1 = 3.4. Weekly average occupancy = (5 x 0.4 + 2 x 0.7)/7 = 0.4857. Tickets per screen per month = 4 x 300 x 0.4857 x 30 = 17,486. Per hall = 3.4 x 17,486 = 59,451. Halls = 6.105M / 59,451 = 102.7, so 103.',
        section='aptitude', topic='data-interpretation', type='numeric', confidence='low', hard=True,
        sources=['20.30.37_f00850f9.jpg'],
        notes='Estimation question; another route (revenue Rs 1.2 billion / Rs 200 = 6 million tickets) gives about 101 halls. The 103 figure follows the demographic statements 5 to 8. A month is taken as 30 days.',
        solution=S('''Match demand (tickets per month) with the supply per hall.

**Demand**
1. Children below 14: 22M x 30% = 6.6M; 5% watch 1 film -> 0.33M.
2. Above 60: 22M x 5% = 1.1M; 5% watch 1 film -> 0.055M.
3. Ages 14-60: 65% = 14.3M; 20% watch 2 films -> 14.3M x 0.2 x 2 = 5.72M.
4. Total tickets per month = 6.105M.

**Supply per hall**
5. Average screens per hall = 0.8 x 4 + 0.2 x 1 = 3.4.
6. Average occupancy = (5 x 40% + 2 x 70%)/7 = 48.57%.
7. Tickets per screen per month = 4 shows x 300 seats x 0.4857 x 30 days = 17,486.
8. Per hall = 3.4 x 17,486 = 59,451.

**Answer:** 6,105,000 / 59,451 = 102.7, rounded up to **103 halls**.''', fast='Compute total demand once, then one blended hall capacity, and divide.',
                  traps='- Using 4 screens for every hall.\n- Using 40% occupancy for all days.\n- Treating "Rs 1.2 billion per hall" literally; the revenue is for Delhi as a whole (6.105M x Rs 200 = Rs 1.22 billion, consistent with the demand).'))
    add('zs-est-igi-t3', Z, 'Estimate daytime passengers through T3 of IGI Airport',
        'Use the statements to estimate the number of people who fly in and out of T3 of Indira Gandhi International Airport, New Delhi during day time (7 am to 8 pm). Round to the next whole number.\n\nRelevant statements: peak traffic is 7-10 am and 3-8 pm; an average plane is at 100% capacity only at peak, and at 50% off-peak and 75% mid-peak; a plane lands or takes off every 5 minutes at peak, every 10 minutes at mid-peak and every 15 minutes off-peak; an aircraft carries 200 passengers at full capacity; 10 am to 3 pm is mid-peak; 8 pm to 11 pm is mild traffic. (The remaining statements on area, runway, counters and ranking are distractors.)',
        '23700', 'Peak hours 7-10 am and 3-8 pm total 8 hours: 12 flights per hour x 8 = 96 flights at 200 passengers = 19,200. Mid-peak 10 am-3 pm is 5 hours: 6 flights per hour x 5 = 30 flights at 150 passengers = 4,500. Total = 23,700.',
        section='aptitude', topic='data-interpretation', type='numeric', confidence='medium', sources=['20.30.37_c0a2b7f6.jpg'],
        solution=S('''Daytime 7 am to 8 pm = 13 hours = peak 8 h (7-10 and 3-8) + mid-peak 5 h (10-3). Off-peak does not occur in this window.
1. Peak: a flight every 5 min = 12 per hour. 12 x 8 = 96 flights, each full: 96 x 200 = 19,200.
2. Mid-peak: a flight every 10 min = 6 per hour. 6 x 5 = 30 flights at 75%: 30 x 150 = 4,500.
3. Total = 19,200 + 4,500 = 23,700.

**Answer: 23,700 people**''', fast='Flights x capacity: (96 x 200) + (30 x 150).',
                  traps='- Counting off-peak hours (8 pm to 11 pm is outside 7 am to 8 pm).\n- Doubling for "in and out"; every landing or take-off is a separate flight event already counted by the frequency.'))
    add('zs-est-audi-delhi', Z, 'Estimate the number of Audi cars in Delhi',
        'Use the statements to find how many Audi cars there are in Delhi (round up to the next whole number). Key statements: 1) The total population of Delhi is 22.7 million. 2) There are 458,500 Audi cars in India. 6) Delhi, Mumbai, Hyderabad and Bangalore account for 72% of the total Audi cars. 14) Delhi accounts for 8/18 of Audi cars in these 4 metropolitan cities. (Statements about showrooms, rentals, income, households and yearly sales are distractors.)',
        '146720', 'Audi cars in the four metros = 72% of 458,500 = 330,120. Delhi\'s share is 8/18 of that = 330,120 x 8/18 = 146,720.',
        section='aptitude', topic='data-interpretation', type='numeric', confidence='medium', sources=[P],
        notes='Read from a compiled PDF page; other statements (showroom sales, rentals) give alternative routes but this uses the direct share chain.',
        solution=S('''1. Audi cars in the 4 metros = 0.72 x 458,500 = 330,120.
2. Delhi\'s share of the 4 metros = 8/18: 330,120 x 8/18 = 146,720.

**Answer: 146,720**''', fast='72% x 8/18 = 32%; 32% of 458,500 = 146,720.', traps='- Using the showroom sales (6,700 per showroom growing 12% a year) data, which gives a different number.\n- Applying 8/18 to the national total.'))
    add('zs-case-hungry-kya-kitchens', Z, 'Hungry Kya!: profit of the most profitable circle',
        'Hungry Kya! plans to launch a cloud kitchen service in the eastern metropolitan Pianchi. Pianchi is divided into 6 circles, each with roughly equal population. Outlets are expected to receive 180K orders per month across Pianchi at an Average Order Value (AOV) of INR 500 (assume equal distribution of orders and revenue across circles). Field research shows Hungry Kya! will have to set up 5 kitchens in Circle 1 to support the demand (assume each kitchen covers an equal area irrespective of circle/density). Average monthly cost per kitchen: INR 1,000,000.\n\nPopulation density (per sq. mile): Circle 1: 300, Circle 2: 200, Circle 3: 150, Circle 4: 75, Circle 5: 250, Circle 6: 100.\n\nQuestion 1.2: What is the estimated maximum profit that Hungry Kya! can achieve from its most profitable region, considering they launch in select regions?',
        'INR 10,000,000 per month (Circle 1)',
        'Revenue per circle = 180,000 x 500 / 6 = INR 15,000,000 per month. With equal population, area is proportional to 1/density, and one kitchen covers the area of Circle 1 divided by 5, so kitchens needed = 1500/density: C1 5, C2 7.5, C3 10, C4 20, C5 6, C6 15. Profit = 15M - kitchens x 1M: C1 10M, C2 7.5M, C3 5M, C4 -5M, C5 9M, C6 0. The most profitable circle is Circle 1 with INR 10 million.',
        section='aptitude', topic='data-interpretation', type='numeric', confidence='medium', hard=True,
        sources=['19.09.06.jpeg', '19.09.11.jpeg', '19.09.13.jpeg'],
        notes='The answer options were cropped out of all photos. The first screenshot (Part 1(a)) belongs to a sibling question on which circles to launch in; its question text was not captured. The result above is derived from the data.',
        solution=S('''**Step 1: revenue per circle.** Total orders 180,000 x INR 500 = INR 90,000,000 per month; equal across 6 circles = INR 15,000,000 each.

**Step 2: kitchens needed per circle.** Populations are equal, so area is proportional to 1/density. A kitchen covers a fixed area, so kitchens needed is proportional to 1/density. Circle 1 needs 5 kitchens at density 300, so kitchens = 5 x 300 / density = 1500/density.

| Circle | Density | Kitchens | Cost (INR M) | Profit (INR M) |
|---|---|---|---|---|
| 1 | 300 | 5 | 5 | 10 |
| 2 | 200 | 7.5 | 7.5 | 7.5 |
| 3 | 150 | 10 | 10 | 5 |
| 4 | 75 | 20 | 20 | -5 |
| 5 | 250 | 6 | 6 | 9 |
| 6 | 100 | 15 | 15 | 0 |

**Step 3.** Launching only in profitable circles (1, 2, 3, 5) avoids the loss in Circle 4 and the break-even in Circle 6. The best single circle is Circle 1 with **INR 10,000,000 per month**.''',
                  fast='Kitchens = 1500/density; profit = 15 - kitchens (in INR million).',
                  traps='- Forgetting that denser circles need fewer kitchens (the area per kitchen is fixed).\n- Dividing the revenue by circle area; revenue is equal per circle.'))
    add('zs-case-hungry-kya-segment', Z, 'Hungry Kya!: customer segment to prioritise for sales potential',
        'Hungry Kya! customer segments (share of orders per month, AOV in INR): PG/Hostel Dwellers 16%, 150-300; Young Married Couples 20%, 200-400; Working Wives 27%, 400-800; Students 12%, 150-200; Hardcore Foodies 25%, 500-1000. Time spent with major media (minutes per day) is also given per segment as a stacked bar chart.\n\nQuestion 2.3: Based on your strategy in Part 2(a), which of the given customer segments should be given the highest priority considering their sales potential? (Use the data given above.)',
        'Hardcore Foodies',
        'Sales potential is order share multiplied by AOV. Using AOV mid-points: PG 16% x 225 = 36, Young couples 20% x 300 = 60, Working wives 27% x 600 = 162, Students 12% x 175 = 21, Hardcore foodies 25% x 750 = 187.5. Hardcore Foodies is the highest.',
        section='aptitude', topic='data-interpretation', type='mcq', confidence='low',
        sources=['19.09.08.jpeg', '19.09.16.jpeg', '19.09.19.jpeg'],
        options=['PG/Hostel Dwellers', 'Young Married Couples', 'Working Wives', 'Students', 'Hardcore Foodies'],
        notes='Answer options were cropped; the choice list is inferred from the segments. Question 2.1 (maximum revenue from advertisements) shares the same chart but the ad-rate data it needs is not visible. If the Part 2(a) strategy weights media time as well, Working Wives could rank differently.',
        solution=S('''Sales potential = share of monthly orders x average order value.

| Segment | Share | AOV mid-point | Share x AOV |
|---|---|---|---|
| PG/Hostel | 16% | 225 | 36 |
| Young Married Couples | 20% | 300 | 60 |
| Working Wives | 27% | 600 | 162 |
| Students | 12% | 175 | 21 |
| Hardcore Foodies | 25% | 750 | 187.5 |

Hardcore Foodies has the highest value, with Working Wives close behind.

**Answer: Hardcore Foodies**''', wrong='Other segments have lower share x AOV; Working Wives is the nearest alternative.', fast='Compare share x top-of-range AOV: 25 x 1000 against 27 x 800.', traps='- Ranking only by share of orders (Working Wives 27%) and ignoring AOV.'))
    add('zs-case-promo-budget', Z, 'Hungry Kya!: best expected return from splitting the marketing budget',
        'In advance of launching the new service, Hungry Kya! wants to streamline its annual marketing budget (INR 100 lakhs) to achieve more impact and sales growth from the same amount of money spent. A line chart shows expected returns (in MN) for Social Media, Online, TV, Print and Telemarketing against the percentage of the annual advertising budget spent on each channel.\n\nQuestion 3: What is the maximum expected return from the best allocation of the budget across channels?',
        'INR 16,00,00,000', 'Read each channel curve at 10% steps and choose the split of 100% that maximises the sum. Approximate reading: Social Media 30% -> 70, Online 10% -> 20, TV 50% -> 60, Print 10% -> 10, Telemarketing 0%. Total about 160 MN = INR 16 crore.',
        section='aptitude', topic='data-interpretation', type='mcq', confidence='low',
        sources=['19.09.14.jpeg'], options=['INR 16,50,00,000', 'INR 16,00,00,000', 'INR 15,50,00,000', 'INR 15,00,00,000'],
        notes='The exact question line was not visible in the photo; it is inferred from the options and chart title. Curve values were read by eye, so the answer could be off by one option.',
        solution=S('''Approach: a knapsack-style allocation. Split 100% of the budget in 10% steps among channels so that the sum of expected returns is maximal.
1. Read the chart (approximate, MN): Social Media 10% -> 5, 20% -> 50, 30% -> 70, 40%+ -> 80; Online 10% -> 20, 70% -> 75; TV 10% -> 15, 50% -> 60; Print 10% -> 10, 60% -> 65, 70% -> 70; Telemarketing low everywhere.
2. Dynamic programming over channels gives the best total with Social 30%, Online 10%, TV 50%, Print 10%: 70 + 20 + 60 + 10 = 160 MN.
3. 160 MN = INR 16,00,00,000.

**Answer: INR 16,00,00,000** (confidence low because the curve values are read by eye).''',
                  wrong='INR 16.5 crore would need chart readings about 5 MN higher; 15.5 and 15 crore are below the best split found.',
                  fast='Social Media saturates at about 40%, so put only as much there as the steep part needs, then give the rest to the next best curves.',
                  traps='- Putting everything on the single best channel.\n- Ignoring diminishing or even falling returns (TV and Online drop after their peak).'))
    add('zs-case-factors-focus', Z, 'Hungry Kya!: which service factors need focus compared with the competitor',
        'A survey asked customers to rate features of Hungry Kya! (n = 300) and a competitor (n = 350) on a scale of 1 to 5 (5 is best). For Hungry Kya!: surge pricing 80% gave 5; time to delivery 30% gave 5; cuisine variety 80% gave 5; missing orders 20% gave 5; discounts 90% gave 1; ease of ordering 95% gave 5; restaurant ratings 90% gave 5. For the competitor: surge pricing 79% gave 5; time to delivery 50% gave 5; cuisine variety 78% gave 5; missing orders 50% gave 5; discounts 90% gave 5; ease of ordering 95% gave 5; restaurant ratings 50% gave 5.\n\nQuestion 3: Which factors does Hungry Kya! need to focus on?',
        'Discounts, time to delivery and missing orders',
        'Compare the share of top ratings: Hungry Kya! lags the competitor on discounts (90% rate it 1 against 90% rating it 5), on time to delivery (30% against 50% top rating) and on missing orders (20% against 50%). Surge pricing, cuisine variety and ease of ordering are on par, and restaurant ratings are better.',
        section='aptitude', topic='data-interpretation', type='subjective', confidence='medium',
        sources=['19.09.25.jpeg', '19.09.27.jpeg'],
        notes='Percentages were read from stacked bar charts in angled photos; the options of the original question were not visible, so this is recorded as an open question.',
        solution='''### Approach
Compare each feature across the two bar charts and find where Hungry Kya! is clearly worse.

### Comparison (share giving the top rating of 5 unless stated)
| Feature | Hungry Kya! | Competitor | Verdict |
|---|---|---|---|
| Surge pricing | 80% | 79% | on par |
| Time to delivery | 30% | 50% | behind |
| Cuisine variety | 80% | 78% | on par |
| Missing orders | 20% | 50% | behind |
| Discounts | 90% rate it 1 (poor) | 90% rate it 5 | far behind |
| Ease of ordering | 95% | 95% | on par |
| Restaurant ratings | 90% | 50% | ahead |

### Recommendation
Focus on **discounts** (largest gap), **time to delivery** and **missing orders** (operational reliability). Keep investing lightly where it already equals or beats the competitor, and use the restaurant-ratings advantage in marketing.

### Likely follow-ups
- **Which one first?** Discounts, because it is the biggest satisfaction gap and the cheapest lever to pull.
- **How would you measure improvement?** Re-run the same survey and track top-rating share and repeat-order rate for each feature.
- **Why not surge pricing?** Ratings there are already equal to the competitor.''')
    add('zs-sql-luxury-trains', Z, 'SQL: names of trains whose description is LUXURY',
        'Write an SQL query (MySQL 8.0) to display the train names whose description is LUXURY. Your output should contain one column: Train_Name. (The database schema was shown only inside the test tool, so the table and column names below are assumed.)',
        "SELECT t.train_name AS Train_Name FROM train t JOIN train_type tt ON t.type_code = tt.type_code WHERE tt.type_description = 'LUXURY';",
        'Join the train table to the train-type table on the type code and filter on the description. The schema was not visible, so the names are assumed.',
        section='cs', topic='sql', type='sql', confidence='low', sources=['19.09.21.jpeg'],
        notes='The schema was only available in the test tool. Table and column names (train, train_type, train_name, type_code, type_description) are assumptions.',
        solution='''### Intuition
The luxury label lives in a lookup table of train types, while train names live in the train table, so we need a join.

### Approach
1. Join `train` with `train_type` on the type code.
2. Keep the rows whose description equals LUXURY.
3. Select only the train name and alias it as `Train_Name`.

### Why it works
An inner join keeps only trains with a known type; the equality filter selects those typed as LUXURY.

### Complexity
O(n + m) with hash joins, or O(n log m) with an index on `type_code`.

### SQL solution
```sql
SELECT t.train_name AS Train_Name
FROM train t
JOIN train_type tt ON t.type_code = tt.type_code
WHERE tt.type_description = 'LUXURY';
```

### Dry run
If train_type has (LUX, LUXURY) and train has (Maharajas Express, LUX), (Local Fast, PSNG), the join gives one row for Maharajas Express which passes the filter.

### Edge cases & pitfalls
- Case or trailing spaces in the description: use `UPPER(TRIM(...))` if the data are messy.
- If the description is stored on the train table itself, no join is needed.
- Use the exact output column name required.''')
    add('zs-sql-express-passenger', Z, 'SQL: express and passenger trains with start and destination codes',
        'Write a MySQL query to find the train name, type description, code of the starting station and code of the destination station (for example NDLS for New Delhi) of all express and passenger trains. The output should contain 4 columns in this order: train_name, type_description, train_from, train_to. Hint: train types are abbreviated; Express is stored as "EXP" and Passenger as "PSNG". (The schema was not visible in the photo; names below are assumed.)',
        "SELECT t.train_name, tt.type_description, t.train_from, t.train_to FROM train t JOIN train_type tt ON t.type_code = tt.type_code WHERE t.type_code IN ('EXP', 'PSNG');",
        'Join trains with their type and keep types EXP and PSNG with IN. Output the four requested columns in order. Station codes are assumed to be stored directly on the train table.',
        section='cs', topic='sql', type='sql', confidence='low', sources=['19.09.24.jpeg'],
        notes='Schema not visible; table and column names are assumed. If station codes are in a separate stations table, two extra joins on from/to ids are needed.',
        solution='''### Intuition
We need train attributes plus the textual type description, filtered to two codes.

### Approach
1. Join `train` to `train_type` on the type code.
2. Filter `type_code IN ('EXP', 'PSNG')`.
3. Select the columns in the order given: name, description, from-code, to-code.

### Why it works
The join attaches the description to each train and the `IN` filter keeps only the requested categories.

### Complexity
O(n + m) with a hash join (or an indexed join).

### SQL solution
```sql
SELECT t.train_name,
       tt.type_description,
       t.train_from,
       t.train_to
FROM train t
JOIN train_type tt ON t.type_code = tt.type_code
WHERE t.type_code IN ('EXP', 'PSNG');
```

### Dry run
Rows (Rajdhani, EXP, NDLS, BCT), (Local, PSNG, ...), (Luxury Special, LUX, ...) give two output rows: the LUX train is filtered out.

### Edge cases & pitfalls
- If station codes live in a `station` table, join it twice with aliases (one for from, one for to).
- Column order matters when the checker compares output.
- Do not use `LIKE '%EXP%'`, which could also match other codes.''')
