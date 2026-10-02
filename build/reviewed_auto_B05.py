"""ProcDNA (AON-style cognitive test): analytical reasoning, quantitative aptitude, data interpretation."""


def extend(add, merge, skip, alias):
    P = 'ProcDNA'

    def w(*ns):
        return [f'IMG-20240820-WA{n:04d}.' + ('jpeg' if n <= 77 else 'jpg') for n in ns]

    def Q(key, title, stmt, options, ans, explain, steps, srcs, topic='quant', wrong='', fast='', traps='',
          typ=None, **kw):
        sol = '### Solution\n' + steps.strip() + f'\n\n**Answer: {ans}**\n'
        if wrong:
            sol += '\n### Why the other options are wrong\n' + wrong.strip() + '\n'
        if fast:
            sol += '\n### Faster method\n' + fast.strip() + '\n'
        if traps:
            sol += '\n### Common traps\n' + traps.strip() + '\n'
        add(key, P, title, stmt, ans, explain, section='aptitude', topic=topic,
            type=typ or ('mcq' if options else 'numeric'), options=options, sources=w(*srcs), solution=sol, **kw)

    DS4 = ['Statements I and II together are not sufficient to answer the question asked and additional data to the problem is needed',
           'Each statement alone is sufficient to answer the question',
           'Both statements I and II together are sufficient to answer the question asked but neither statement alone is sufficient',
           'Only one of the statements, alone, is sufficient to answer the question but the other statement is not']

    # ---------------- Analytical reasoning ----------------
    Q('procdna-series-x3-plus1', 'Missing term in 7, 21, 22, 66, 67, ?, 202, 606',
      'Find the missing term in the series: 7, 21, 22, 66, 67, ?, 202, 606',
      ['198', '201', '68', '176'], '201',
      'The operations alternate between multiply by 3 and add 1: 7, 21, 22, 66, 67, then 67 x 3 = 201, 202, 606.',
      '''Look at consecutive ratios and differences: 7 -> 21 (x3), 21 -> 22 (+1), 22 -> 66 (x3), 66 -> 67 (+1), 67 -> ? (x3) = 201, 201 -> 202 (+1), 202 -> 606 (x3). The pattern repeats, so the missing term is 201.''',
      [11], topic='logical', wrong='198 and 176 break the +1 / x3 alternation; 68 is 67 + 1 but the next step must be x3.',
      fast='Check the final pair: 202 x 3 = 606 confirms that ? + 1 = 202, so ? = 201.', traps='- Applying +1 twice in a row.')
    Q('procdna-syllogism-cockroach', 'Syllogism: cockroaches, tadpoles, donkeys, bears and sharks',
      'Statements: I. All cockroaches are tadpoles. II. All tadpoles are donkeys. III. Some donkeys are bears. IV. Some donkeys are sharks.\nConclusions: I. Some bears are sharks. II. No cockroach is a bear.\nAssume the statements are true even if they contradict commonly known facts.',
      ['Neither conclusion I nor conclusion II follows', 'Both conclusion I and conclusion II follow', 'Only conclusion I follows', 'Only conclusion II follows'],
      'Neither conclusion I nor conclusion II follows',
      'Two "some" statements sharing a middle term (donkeys) give no relation between bears and sharks. Cockroaches are donkeys, but the bears may or may not include them, so "no cockroach is a bear" is not forced.',
      '''Draw cockroach inside tadpole inside donkey. Bears and sharks overlap donkeys partially, in unknown places.
- Conclusion I: "some bears are sharks" needs the two overlaps to meet, which is not given.
- Conclusion II: "no cockroach is a bear" would need the bears to avoid the cockroach region; the bears might overlap it.
Neither is certain.''',
      [11, 13], topic='logical', wrong='Any option claiming a conclusion follows relies on an unstated overlap.',
      fast='Two particular ("some") premises never yield a definite conclusion.', traps='- Assuming the "some" groups are the same donkeys.')
    Q('procdna-ds-average-pocket-money', 'Data sufficiency: average pocket money of a kid',
      'Question: What is the average pocket money of a kid in the class?\nI. The sum of the pocket money of all the kids is $8,100.\nII. Lisa had $65, a value above the average.',
      DS4, DS4[0],
      'The average needs the sum and the number of kids. I gives only the sum; II gives an inequality on Lisa\'s share, not the count.',
      '''Average = total / number of kids. I gives the total but not the count. II says only that the average is below $65 (a bound, not a number). Together we still do not know the number of kids: at most 8100/65 > 124.6 means more than 124 kids, but not exactly how many.''',
      [13, 122, 125], topic='logical', wrong='No statement or pair provides the number of kids.', fast='Ask: what quantity is missing? The count of kids.', traps='- Reading "above the average" as an exact value.')
    Q('procdna-odd-one-turnip', 'Odd one out: Turnip, Potato, Carrot, Banana',
      'Mark the odd one out from the given options.', ['Turnip', 'Potato', 'Carrot', 'Banana'], 'Banana',
      'Turnip, potato and carrot are root vegetables; banana is a fruit.',
      'Classify by category: turnip, potato and carrot are all root vegetables (underground edible parts), banana is a fruit.',
      [15, 17], topic='logical', wrong='The other three share the root-vegetable property.', fast='Find the category that three items share.')
    Q('procdna-ds-chem-physics', 'Data sufficiency: students taking Chemistry but not Physics',
      'Question: 50 students are taking at least one course out of Chemistry and Physics. How many of the 50 students are taking Chemistry but not Physics?\nI. 16 students are taking Chemistry and Physics.\nII. The number of students taking Physics but not Chemistry is the same as the number taking Chemistry but not Physics.',
      DS4, DS4[2],
      'Let x be Chemistry-only and Physics-only (equal by II). With both = 16 (I): 2x + 16 = 50, so x = 17. Neither statement alone fixes x.',
      '''Venn diagram: Chemistry-only c, Physics-only p, both b, with c + p + b = 50.
- I alone: b = 16 gives c + p = 34 but not c.
- II alone: c = p gives 2c + b = 50, but b unknown.
- Together: 2c + 16 = 50, so c = 17.

Both together are sufficient.''', [17, 19, 142], wrong='Each statement alone leaves one free variable.',
      fast='Two unknown quantities need two equations.', traps='- Forgetting that "at least one course" means nobody is outside the union.')
    Q('procdna-ds-travel-time', 'Data sufficiency: time from A to B given round trip of 4 hours',
      'Question: How long will it take to travel from A to B if it takes 4 hours to travel from A to B and back to A?\nI. It takes 25% more time to travel from A to B than it does to travel from B to A.\nII. C is midway between A and B and it takes 2 hours to travel from A to C and back to A.',
      DS4, DS4[3],
      'I gives t(AB) = 1.25 t(BA) and t(AB) + t(BA) = 4, so t(AB) = 20/9 hours. II is consistent with equal times (2 h from A to B) but also with unequal ones, so it does not fix t(AB).',
      '''I: let t(BA) = x, then t(AB) = 1.25x and 2.25x = 4, so x = 16/9 h and t(AB) = 20/9 h = 2 h 13 min 20 s. Sufficient.
II: A to C and back is 2 hours, but with different speeds uphill/downhill the whole A to B leg is not determined (e.g. A->B could be 2 h or 2.2 h while A->C->A stays 2 h). Not sufficient.''',
      [17, 19, 21, 140, 141], wrong='II alone does not determine t(AB); the other options ignore that I works alone.',
      fast='I creates a ratio plus a sum: sufficient. II gives only a half-distance round trip.', traps='- Assuming equal speeds both ways in II.')
    Q('procdna-shadow-direction', 'Direction of a pole\'s shadow after a turning path',
      'Ray started from his house which is facing East, took left and walked for 12 minutes. He then took right and walked for 6 minutes, then took right again and walked for 20 meters, then again took right where he saw a rectangular pole as shown in the figure (a compass with the pole on the left whose shadow falls on its right, towards the direction marked North). What is the direction of his shadow? (Taking left or right means turning 90 degrees.)',
      ['On his right', 'On his left', 'On his back', 'In front of Ray'], 'On his right',
      'Ray faces East, turns left (North), right (East), right (South), right (West), so he faces West at the pole. The figure shows the shadow pointing to North, which is on his right when facing West.',
      '''Headings: East -> left = North -> right = East -> right = South -> right = West. He is facing West.
In the figure the pole\'s shadow lies in the direction labelled North. Facing West, North is on the right-hand side.''',
      [19, 21, 23, 131], topic='logical', confidence='low',
      notes='The figure was small; the reading that the shadow falls toward North is an interpretation.',
      wrong='Left would need the shadow to point South; back would need East; front would need West.', traps='- Forgetting that the final turn also changes his heading.')
    Q('procdna-series-cubes-times-two', 'Missing term in 2, 16, ?, 128, 250, 432',
      'Find the missing term in the series: 2, 16, ?, 128, 250, 432', ['32', '48', '54', '96'], '54',
      'The terms are 2n^3: 2, 16, 54, 128, 250, 432.', '2 x 1^3 = 2, 2 x 2^3 = 16, 2 x 3^3 = 54, 2 x 4^3 = 128, 2 x 5^3 = 250, 2 x 6^3 = 432.',
      [21, 23, 25, 122], topic='logical', wrong='32, 48 and 96 are not 2 x 27.', fast='Test the last term: 432 / 2 = 216 = 6^3.')
    Q('procdna-support-math-paragraph', 'Statement that best supports a paragraph about mathematics',
      'Select the statement that best develops or supports the paragraph: "Mathematics allows us to expand our consciousness. Mathematics tells us about economic trends, patterns of disease and the growth of populations. Math is good at exposing the truth, but it can also perpetuate misunderstandings and untruths. Figures have the power to mislead people."',
      ['The study of mathematics can be both beneficial and confusing.', 'The study of mathematics is more important than other disciplines.', 'The power of numbers is that they cannot lie.', 'The study of mathematics is dangerous.'],
      'The study of mathematics can be both beneficial and confusing.',
      'The paragraph gives both benefits (expanding consciousness, exposing truth) and risks (misunderstandings, misleading figures), so "beneficial and confusing" matches it.',
      'The two sides of the paragraph are the useful side (insights into trends) and the misleading side. Only the first option states both. "More important than other disciplines" is never claimed; "cannot lie" contradicts the paragraph; "dangerous" ignores the benefits.',
      [23, 25, 27, 126], topic='verbal')
    Q('procdna-argument-against-consensus', 'Argument against assimilating many views before critical decisions',
      'The progress of a society can be achieved through several factors. Each factor has a different impact, positive or negative. It may be difficult sometimes to assess the precise impact of a certain factor because it may be a combination of many factors that bring progress. Hence, it is important to assimilate as many views as possible while taking critical decisions that impact social progress.\n\nFrom the given options choose the argument which is against the view expressed above.',
      ['Whenever a single person took a decision he committed many mistakes; all human beings are liable to err.',
       'Favouritism plays its part in decision-making and once a decision is taken it is too late to reverse; it is advantageous to try for consensus before deciding.',
       'An individual is unable to consider all aspects of a problem on his own; two heads are better than one, and when many people express views the result is wholesome.',
       'Many times the situation warrants a prompt and speedy decision; where an individual has final authority he can decide without waiting for others, because time makes all the difference.'],
      'Many times the situation warrants a prompt and speedy decision; where an individual has final authority he can decide without waiting for others, because time makes all the difference.',
      'The view favours gathering many opinions. Only the last option argues that decisions should not wait for others.',
      'Options 1, 2 and 3 all support consulting many people (individuals err, consensus helps, many heads are better). Option 4 is the only one that argues against waiting for the views of others, so it opposes the stated view.',
      [25, 27, 29], topic='verbal', wrong='Options 1 to 3 agree with the view.', fast='Look for the option that rejects consultation.', traps='- Picking option 1, which sounds negative but argues for consultation.')
    Q('procdna-code-lament-letters', 'Coding: LAMENT = 12 and SOFTENS = 14 so SCAM = ?',
      'If in a certain code language "LAMENT" equals 12 and "SOFTENS" equals 14, then what is the value of "SCAM"?',
      ['18', '12', '6', '8'], '8', 'Each word equals twice its number of letters: LAMENT (6) -> 12, SOFTENS (7) -> 14, so SCAM (4) -> 8.',
      'LAMENT has 6 letters and is 12; SOFTENS has 7 letters and is 14; the value is 2 x (number of letters). SCAM has 4 letters, so 8.',
      [29, 31], topic='logical', wrong='18, 12 and 6 do not equal 2 x 4.', fast='Compare number of letters with the value.')
    Q('procdna-syllogism-crabs', 'Syllogism: no horses are molluscs and all crabs are horses',
      'Statements: I. No horses are molluscs. II. All crabs are horses. Which conclusion follows?',
      ['All molluscs are crabs', 'Some horses are not crabs', 'None follow', 'No crabs are molluscs'], 'No crabs are molluscs',
      'Crabs lie inside horses, and horses have no overlap with molluscs, so crabs have none either.',
      'All crabs are horses, so crabs are a subset of horses. No horse is a mollusc, so no crab is a mollusc. "Some horses are not crabs" cannot be inferred (all horses could be crabs).',
      [31, 33], topic='logical', wrong='"All molluscs are crabs" contradicts statement I; "Some horses are not crabs" is possible but not certain.',
      fast='A-statement followed by an E-statement gives an E conclusion.')
    Q('procdna-seating-eight-heights-q1', 'Eight friends by height: taller than Oliver and from the same city',
      'Eight friends Oliver, John, Ethan, Oscar, Bruce, Jonathan, Harry and Kevin are of different heights and stand in a row facing North in decreasing order of height from left to right (shortest at the extreme right). Three are from Mumbai, three from Paris and the rest from New York.\nI. Kevin, the 2nd tallest, is not from Mumbai and Harry, the 4th tallest, is from Paris.\nII. Oscar is from Paris but Jonathan is not from New York.\nIII. Oliver is taller than John but shorter than Harry, while Bruce is shorter than Kevin.\nIV. Jonathan is shorter than John but taller than Ethan.\nV. Neither the shortest nor the second shortest friend is from Mumbai.\n\nWho among the following is taller than Oliver and is also from the same city as him?',
      ['Oscar', 'Jonathan', 'John', 'Bruce'], 'Bruce',
      'The order is Oscar, Kevin, Bruce, Harry, Oliver, John, Jonathan, Ethan. Cities: Paris - Oscar, Harry, Jonathan; Mumbai - Bruce, Oliver, John; New York - Kevin, Ethan. Bruce is from Mumbai like Oliver and taller than him.',
      '''1. Kevin is 2nd and Harry 4th. Oliver < Harry, John < Oliver, Jonathan < John, Ethan < Jonathan, so positions 5 to 8 are Oliver, John, Jonathan, Ethan.
2. Oscar and Bruce take positions 1 and 3; Bruce is shorter than Kevin, so Bruce is 3rd and Oscar is 1st.
3. Cities: Harry, Oscar are Paris. Shortest (Ethan) and second shortest (Jonathan) are not Mumbai; Jonathan is not New York, so Jonathan is Paris (third Paris person). Ethan is then New York; Kevin (not Mumbai, Paris full) is New York. The remaining three, Bruce, Oliver and John, are from Mumbai.
4. Taller than Oliver and Mumbai: Bruce (position 3). John is shorter.

A computer search of all 40,320 orderings confirms this is the only arrangement.''',
      [33, 35, 37, 137, 138], topic='puzzles', hard=True,
      wrong='Oscar is from Paris; Jonathan is from Paris and shorter; John is from Mumbai but shorter than Oliver.')
    Q('procdna-seating-eight-heights-q2', 'Eight friends by height: Mumbai or Paris person with an odd number on the left',
      'Using the same arrangement of eight friends by height (Oscar, Kevin, Bruce, Harry, Oliver, John, Jonathan, Ethan from left to right; Paris: Oscar, Harry, Jonathan; Mumbai: Bruce, Oliver, John; New York: Kevin, Ethan), who among the following belonging to either Mumbai or Paris has an odd number of persons standing on their left?',
      ['Ethan', 'Harry', 'Oliver', 'Kevin'], 'Harry',
      'An odd number of people on the left means an even position: 2 Kevin, 4 Harry, 6 John, 8 Ethan. Of the options, Harry (Paris) is from Mumbai or Paris; Kevin and Ethan are from New York.',
      'Positions with an odd number on the left are 2, 4, 6 and 8: Kevin (NY), Harry (Paris), John (Mumbai), Ethan (NY). Among the options only Harry qualifies.',
      [35, 37, 138, 139], topic='puzzles', wrong='Ethan and Kevin are from New York; Oliver stands 5th with four people on the left (even).')
    Q('procdna-seating-eight-heights-q3', 'Eight friends by height: two friends from the same city standing adjacent',
      'In the same arrangement (Oscar, Kevin, Bruce, Harry, Oliver, John, Jonathan, Ethan; Paris: Oscar, Harry, Jonathan; Mumbai: Bruce, Oliver, John; New York: Kevin, Ethan), which two friends from the same city are adjacent to each other?',
      ['Oliver & Harry', 'Oscar & Kevin', 'Oliver & John', 'Jonathan & Ethan'], 'Oliver & John',
      'Oliver (5th) and John (6th) stand next to each other and are both from Mumbai.',
      'Adjacent pairs: Oscar-Kevin (Paris, NY), Kevin-Bruce, Bruce-Harry (Mumbai, Paris), Harry-Oliver (Paris, Mumbai), Oliver-John (both Mumbai), John-Jonathan, Jonathan-Ethan (Paris, NY). Only Oliver and John share a city.',
      [37, 139, 140], topic='puzzles', wrong='Each of the other pairs is from two different cities.')
    Q('procdna-flowchart-empty-file', 'Flowchart behaviour on an empty file',
      'A flowchart prints "Name" and "Total", sets ctr = 0, reads Name and Amount, then tests End Of File. If End Of File is true it prints "Number of records read" with ctr and stops; otherwise it sets Namebreak = "No", Old Name = Name, Total = 0, prints Name and processes the group (more steps not visible). How will the flowchart handle a scenario where the file is empty?',
      ['The flow chart will throw an error', 'There will be no error and it will not print anything', 'This will get into an infinite loop', 'There will be no error and it prints "Number of records read" as zero'],
      'There will be no error and it prints "Number of records read" as zero',
      'On an empty file the first read hits End Of File immediately, so the flow goes straight to "Print Number of records read ctr" with ctr = 0 and then stops.',
      'The header line is printed first, then ctr = 0, then the first read finds nothing and the End Of File decision is true. The true branch prints the record count (still 0) and stops. No error and no loop occur.',
      [56, 58], topic='logical', confidence='medium',
      notes='Only the upper half of the flowchart is visible in the photographs.',
      wrong='Nothing is printed only if the stop did not print the count; the loop is never entered.', traps='- Forgetting that the header is printed before the first read.')
    Q('procdna-presentation-order', 'Six presentations: number of possible schedules',
      'Six persons Jacob, William, Liam, Alexander, Ethan and Andrew give presentations, not necessarily in this order.\nI. Andrew delivers either at the start or at the end.\nII. Jacob delivers immediately after Ethan.\nIII. There are exactly three presentations between William and Liam.\nIV. Alexander is the second person to deliver.\n\nHow many different possible scheduling combinations are possible?',
      ['1', '4', '3', '2'], '2',
      'Alexander is 2nd, so William and Liam must be 1st and 5th (three between them). Andrew must then be 6th, leaving Ethan 3rd and Jacob 4th. William and Liam can swap, giving 2 schedules.',
      '''Positions 1 to 6. Alexander = 2. The pairs of positions with exactly three people between are (1,5) and (2,6); position 2 is taken, so William and Liam use 1 and 5 in either order.
Andrew must be first or last; 1 is taken, so Andrew is 6. Jacob follows Ethan directly in the free positions 3 and 4: Ethan 3, Jacob 4.
Two schedules: William, Alexander, Ethan, Jacob, Liam, Andrew and Liam, Alexander, Ethan, Jacob, William, Andrew. A brute-force search over all 720 orders gives the same two.''',
      [58, 60], topic='puzzles', hard=True, wrong='1, 3 and 4 miscount the swap of William and Liam.')
    Q('procdna-presentation-after-william', 'Six presentations: who delivers immediately after William',
      'In the schedule problem where Andrew presents first or last, Jacob follows Ethan, exactly three presentations lie between William and Liam, and Alexander is second: who delivers his presentation immediately after William?',
      ['Jacob', 'Alexander', 'Andrew', 'Either Alexander or Andrew'], 'Either Alexander or Andrew',
      'In the two valid schedules, William is either 1st (followed by Alexander) or 5th (followed by Andrew).',
      'Schedule 1: William, Alexander, Ethan, Jacob, Liam, Andrew -> after William comes Alexander. Schedule 2: Liam, Alexander, Ethan, Jacob, William, Andrew -> after William comes Andrew. Both schedules are valid, so the answer is "either".',
      [60], topic='puzzles', wrong='Jacob never directly follows William; a single name would be wrong in one schedule.')

    # ---------------- Quantitative ----------------
    Q('procdna-probability-screening', 'Probability that a box with 3 defective articles passes the sampling test',
      'Out of a set of 15 articles, 3 are chosen at random. If any one of them is found to be defective, then the whole set is put under 100% screening. If no item is found to be defective, it is sent for sale. Find the probability that a box containing 3 defective articles will be sent for the sale.',
      ['52/91', '9/91', '44/91', '88/91'], '44/91',
      'The box is sold only when all 3 chosen items are good: C(12,3)/C(15,3) = 220/455 = 44/91.',
      'There are 12 good articles. P(all three chosen good) = C(12,3)/C(15,3) = 220/455 = 44/91.',
      [62], wrong='52/91 and 9/91 do not equal 220/455; 88/91 is 2 x 44/91.', fast='(12/15)(11/14)(10/13) = 1320/2730 = 44/91.')
    Q('procdna-power-expression', 'Value of a ratio of powers of 6, 8, 2 and 3',
      'The value of [(6^4)^2 x (8^5)^2 x (2^2)^3 x (3^2)^2] / [(6^2)^3 x (8^3)^4 x (3^3)^2] is:',
      ['4', '2', 'None of the mentioned options', '1/4'], '4',
      'Powers: numerator 6^8 x 8^10 x 2^6 x 3^4, denominator 6^6 x 8^12 x 3^6. The ratio is 6^2 x 8^-2 x 2^6 x 3^-2 = 36 x 64 / (64 x 9) = 4.',
      'Numerator: (6^4)^2 = 6^8, (8^5)^2 = 8^10, (2^2)^3 = 2^6, (3^2)^2 = 3^4. Denominator: (6^2)^3 = 6^6, (8^3)^4 = 8^12, (3^3)^2 = 3^6.\nRatio = 6^(8-6) x 8^(10-12) x 2^6 x 3^(4-6) = 36 / 64 x 64 / 9 = 4.',
      [62, 156], wrong='The other options come from sign errors in the exponents.', fast='Cancel like bases first: 6^2 / 3^2 = 4 and 2^6 / 8^2 = 1.')
    Q('procdna-ap-maximum-sum', 'Maximum possible sum of the A.P. 40, 36, 32, ...',
      'The maximum possible sum of the A.P. series 40, 36, 32, ... is:', ['225', '320', '220', '232'], '220',
      'The terms are 40, 36, ..., 4, 0 (11 terms), after which they turn negative. Sum = 11/2 x (40 + 0) = 220.',
      'Terms are positive until 40 - 4(n-1) = 0, i.e. n = 11 (the 11th term is 0). The maximum sum is S = 11 x (40 + 0)/2 = 220; adding negative terms only reduces it.',
      [62], wrong='225 and 232 would need positive terms beyond zero; 320 is the sum of 40 terms without stopping.', traps='- Continuing the series into negative terms.')
    Q('procdna-polynomial-divisible', 'Value of a for divisibility by x^2 + 1',
      'What is the value of a when 3x^4 + 4x^3 + 5x^2 + 4x + a is divisible by x^2 + 1?', ['1', '0.5', '0', '2'], '2',
      'Dividing gives (x^2 + 1)(3x^2 + 4x + 2) = 3x^4 + 4x^3 + 5x^2 + 4x + 2, so a = 2.',
      'Divide: 3x^4 + 4x^3 + 5x^2 + 4x + a = (x^2 + 1)(3x^2 + 4x + 2) + (a - 2). For divisibility the remainder a - 2 must be 0, so a = 2.\nCheck with x = i: 3 - 4i - 5 + 4i + a = a - 2 = 0.',
      [64, 155], wrong='Any other value leaves a nonzero remainder a - 2.', fast='Substitute x^2 = -1: 3 - 5 + a + (4x^3 + 4x = 4x(x^2 + 1) = 0) = a - 2.')
    Q('procdna-right-triangle-angle', 'Angle PRQ in a right triangle with hypotenuse twice a leg',
      'In triangle PQR, angle QPR is a right angle and QR is twice the length of PQ. The measure of angle PRQ is:', ['75 degrees', '60 degrees', '45 degrees', '30 degrees'], '30 degrees',
      'QR is the hypotenuse and PQ = QR/2, so sin(PRQ) = PQ/QR = 1/2 and angle PRQ = 30 degrees.',
      'Angle P = 90 degrees, so QR is the hypotenuse. The side opposite angle R is PQ, so sin R = PQ / QR = 1/2, giving R = 30 degrees.',
      [64, 158, 159], wrong='60 degrees is angle Q; 45 and 75 degrees need other side ratios.')
    Q('procdna-bus-speed-calculus', 'Speed of a bus from a given velocity law and acceleration',
      'A bus begins moving at time t = 0 and 3 seconds after the beginning attains an acceleration of 2 m/s^2. Find the speed of the bus 6 seconds after the beginning if the speed varies according to v(t) = t^2 + 2kt + 4 (m/s), where k is a constant. The object moves along a straight line.',
      ['25 m/s', '12 m/s', "Can't be determined", '16 m/s'], '16 m/s',
      'Acceleration is dv/dt = 2t + 2k. At t = 3 it is 6 + 2k = 2, so k = -2. Then v(6) = 36 - 24 + 4 = 16 m/s.',
      'a(t) = dv/dt = 2t + 2k. a(3) = 6 + 2k = 2 gives k = -2. v(t) = t^2 - 4t + 4 = (t - 2)^2, so v(6) = 16 m/s.',
      [64], wrong='25 would be v(7); 12 and "cannot be determined" ignore that k is fixed by the acceleration data.', fast='v = (t - 2)^2, so v(6) = 4^2.')
    Q('procdna-cylinder-increase', 'Cylinder: x added to radius or height gives the same volume increase',
      'Consider a cylinder with a diameter of its base as 20 cm and height 4 cm. If x cm is added to either the radius or the height to get the same increase in the volume of the cylinder, then the value of x is:',
      ['16', '5', '25', '4'], '5',
      'With r = 10 and h = 4: pi[(10 + x)^2 x 4 - 400] = pi[100 x (4 + x) - 400], which simplifies to 4x^2 = 20x, so x = 5.',
      '''Increase from the radius: pi x 4 x [(10 + x)^2 - 100] = pi x 4 x (20x + x^2).
Increase from the height: pi x 100 x x.
Equate: 4(20x + x^2) = 100x, so 4x^2 - 20x = 0 and x = 5 (x = 0 is trivial).''',
      [66, 155], wrong='16, 25 and 4 do not satisfy 4x^2 = 20x.', fast='Test x = 5: 4(100 + 25) = 500 = 100 x 5.')
    Q('procdna-trailing-zeros-963', 'Number of trailing zeros in 963 factorial',
      'Find the number of zeroes in 963!. (Printed options: 223, 237, 246, 251.)', None, '238',
      'Count factors of 5: floor(963/5) = 192, floor(963/25) = 38, floor(963/125) = 7, floor(963/625) = 1. Total 238.',
      'Trailing zeros = number of factors of 5 (2s are plentiful): 192 + 38 + 7 + 1 = 238.\nNone of the printed options (223, 237, 246, 251) equals 238, so the exam item or the option list is likely misprinted; the closest is 237.',
      [66, 147], typ='numeric', confidence='medium',
      notes='The correct value 238 is not among the printed options, so the original item has a discrepancy.',
      fast='Divide repeatedly by 5 and add the quotients.', traps='- Stopping after the first division (192).')
    Q('procdna-trailing-zeros-product', 'Number of zeroes at the end of a product',
      'Find the number of zeroes in the result of 5 x 15 x 22 x 11 x 44 x 135 x 20 x 42 x 95.', ['2', '3', '4', '5'], '5',
      'Factors of 5: 5, 15, 135, 20 and 95 give five 5s. Factors of 2: 22, 44 (two), 20 (two) and 42 give six 2s. Zeros = min(5, 6) = 5.',
      'Count the primes 2 and 5. 5s: 5 (1), 15 (1), 135 (1), 20 (1), 95 (1) = 5. 2s: 22 (1), 44 (2), 20 (2), 42 (1) = 6. Each trailing zero needs one 2 and one 5, so there are min(5, 6) = 5 zeros.',
      [66], wrong='Smaller counts forget some multiples of 5; 5 is the min of the two prime counts.', traps='- Counting only numbers ending in 0 or 5 (the 5s appear in 135 and 95 as well).')
    Q('procdna-fixed-variable-income', 'Total income of A from ratios of total and fixed income',
      'The total incomes of A and B are in the ratio 2 : 3 when each of them has earned a variable of $300. Determine A\'s total income if the ratio of their fixed incomes is 1 : 2.',
      ['$400', '$600', '$300', '$350'], '$600',
      'Let fixed incomes be a and 2a: (a + 300)/(2a + 300) = 2/3, so 3a + 900 = 4a + 600, a = 300. A\'s total is 300 + 300 = 600.',
      '(a + 300) : (2a + 300) = 2 : 3 gives 3a + 900 = 4a + 600, so a = 300. A\'s total income = fixed 300 + variable 300 = $600.',
      [66, 68, 160], wrong='$300 is only A\'s fixed income; $400 and $350 do not satisfy the ratio.', fast='Test $600: A = 600, B = 900, ratio 2:3.')
    Q('procdna-work-delay-workers', 'Delay if no additional workers had been employed',
      'Matt wants to build his dream house in 70 days. He employed 40 workers in the beginning and 50 more workers after 34 days to complete the work. Find the delay (in days) if no additional workers would have been employed.',
      ['45', '30', '40', '39'], '45',
      'Total work = 40 x 34 + 90 x 36 = 4600 worker-days. With only 40 workers it takes 115 days, a delay of 45 days.',
      'The house was finished on time with 40 workers for 34 days and 90 workers for the remaining 36 days: 1360 + 3240 = 4600 worker-days. With 40 workers alone: 4600 / 40 = 115 days. Delay = 115 - 70 = 45 days.',
      [68, 148], wrong='30, 39 and 40 come from using 50 workers instead of 90 after day 34.', traps='- Using 50 instead of 40 + 50 = 90 workers after day 34.')
    Q('procdna-emergency-fund', 'Amount spent on emergency funds',
      'Monty\'s monthly income is $4000. He spends 36% of his income on rent, 25% on food, 30% on investment and the rest on emergency funds. What is the amount (in $) that he spends on emergency funds?',
      ['299', '499', '450', '360'], '360',
      '100 - 36 - 25 - 30 = 9 percent of 4000 = 360.', 'Remaining percentage = 100 - (36 + 25 + 30) = 9%. 9% of 4000 = 360.', [68, 149],
      wrong='450 is 11.25%, 499 and 299 are not 9%.')
    Q('procdna-custom-operations-1', 'Custom operations: (6#2)@(51?43)',
      'Read the information given below. x#y = (x^3 - y^3), x?y = (x - y), x@y = x / y. Determine the value of [(6#2) @ (51?43)].',
      ['26', '52', '13', 'None of the mentioned options'], '26',
      '6#2 = 216 - 8 = 208, 51?43 = 8, and 208 @ 8 = 208 / 8 = 26.', '6#2 = 6^3 - 2^3 = 208. 51?43 = 51 - 43 = 8. 208 @ 8 = 208 / 8 = 26.', [71],
      wrong='52 and 13 are 208/4 and 208/16.', fast='Evaluate the brackets first.',
      notes='The other version of the paper uses different operators for a similar item (see the next question).')
    Q('procdna-custom-operations-2', 'Custom operations: (52$2)&(24?16)',
      'Read the information given below. x?y = (x + y)/2, x&y = (x^2 - y^2), x$y = (x - y)/2. Determine the value of [(52$2) & (24?16)].',
      ['None of the mentioned options', '25', '125', '225'], '225',
      '52$2 = 25, 24?16 = 20, and 25 & 20 = 625 - 400 = 225.', '52$2 = (52 - 2)/2 = 25. 24?16 = (24 + 16)/2 = 20. 25 & 20 = 25^2 - 20^2 = 625 - 400 = 225.', [157],
      wrong='25 and 125 are intermediate values; the result is 225.', fast='25^2 - 20^2 = (25 - 20)(25 + 20) = 5 x 45.')
    Q('procdna-fgh-function-product', 'Product of F, G and H for a = 2, b = -3',
      'F(a, b) = |a - b|, G(a, b) = -F(a, b), H(a, b) = |a + b|. If a = 2 and b = -3, what is the value of F.G.H?', ['-36', '-25', '25', '36'], '-25',
      'F = |2 + 3| = 5, G = -5, H = |2 - 3| = 1, so F x G x H = -25.', 'F(2, -3) = |2 - (-3)| = 5. G = -5. H = |2 + (-3)| = 1. Product = 5 x (-5) x 1 = -25.', [71, 158],
      wrong='36 is (a - b)^2 + ... not applicable; positive 25 forgets the sign of G.', traps='- Forgetting the negative sign in G.')
    Q('procdna-train-passing-building', 'Time for an 80 m train at 54 km/h to pass a building',
      'A 80 m long train is running at a speed of 54 kmph and passes a building. What is the time taken by the train to pass by the building?',
      ['5.3 seconds', '8 seconds', '9 seconds', '4.5 seconds'], '5.3 seconds',
      '54 km/h = 15 m/s, and the train must cover its own length: 80 / 15 = 5.33 s.', 'Speed = 54 x 5/18 = 15 m/s. The distance to pass a building is the train length: 80 m. Time = 80 / 15 = 5.33 s, i.e. 5.3 s.', [73, 156],
      wrong='8 s would be 120 m; 9 s would be 135 m; 4.5 s would be 67.5 m.', fast='54 kmph = 15 m/s; 80/15.')
    Q('procdna-bar-percent-change', 'Overall percentage change of infrastructure expenditure of five countries',
      'A bar chart gives infrastructure expenditure (million $) of five countries. 2013-2014: US 830, France 750, Scotland 750, UK 1075, India 720. 2012-2013: US 1100, France 900, Scotland 720, UK 1150, India 965.\n\nCalculate the percentage change in the overall infrastructure expenditure of the five countries together between 2012-2013 and 2013-2014.',
      ['10.89 %', '14.68 %', '21.99 %', '27.01 %'], '14.68 %',
      '2012-13 total = 4835 and 2013-14 total = 4125. Change = (4125 - 4835)/4835 = -14.68%, a decrease of 14.68%.',
      '2012-2013 total: 1100 + 900 + 720 + 1150 + 965 = 4835. 2013-2014 total: 830 + 750 + 750 + 1075 + 720 = 4125. Change = -710 / 4835 = -14.68%.',
      [73, 75, 149, 150], topic='data-interpretation', confidence='medium',
      notes='The chart labels in the photograph are slightly blurry; the figures are consistent with the offered answer.',
      wrong='The other options do not equal 710/4835.', traps='- Using 2013-14 as the base (gives 17.2%).')
    Q('procdna-bar-highest-difference', 'Country with the highest percentage difference in infrastructure expenditure',
      'Using the infrastructure expenditure data (2013-14 against 2012-13: US 830 vs 1100, France 750 vs 900, Scotland 750 vs 720, UK 1075 vs 1150, India 720 vs 965), specify the country which shows the highest percentage difference in infrastructure expenditure between the two years.',
      ['US', 'Scotland', 'India', 'UK'], 'India',
      'Percentage change from 2012-13: US -24.55%, Scotland +4.17%, India -25.39%, UK -6.52% (France -16.67%). India has the largest magnitude.',
      'Percent difference relative to 2012-13: US 270/1100 = 24.55%; Scotland 30/720 = 4.17%; India 245/965 = 25.39%; UK 75/1150 = 6.52%. India is highest. (Relative to 2013-14 the order would change: US 32.5%, India 34.0%, still India.)',
      [75], topic='data-interpretation', confidence='medium', wrong='US is close but smaller; Scotland and UK change little.')
    Q('procdna-jewellers-ruby-share', 'Ruby sales as a percentage of total precious stone sales',
      'XYZ jewellers recorded sales (kg) of five stones (Topaz, Emerald, Ruby, Opal, Bezel) for 1995-96 to 1999-2000 (bar chart). Reading the chart: 1995-96: 200, 300, 200, 200, 100; 1996-97: 150, 250, 50, 200, 100; 1997-98: 400, 400, 200, 200, 200; 1998-99: 300, 400, 200, 200, 100; 1999-2000: 200, 150, 150, 100, 150.\n\nWhat are the total sales of Ruby as a percentage of the total sales of precious stones for the given period?',
      ['19.23%', '23.15%', '17.3%', '15.53%'], '15.53%',
      'Ruby total = 200 + 50 + 200 + 200 + 150 = 800 kg out of about 5100-5150 kg total, about 15.5-15.7%, matching 15.53%.',
      'Ruby: 200 + 50 + 200 + 200 + 150 = 800. Totals by year: 1000, 750, 1400, 1200, 750 = 5100. 800 / 5100 = 15.69%. The nearest option is 15.53% (a total of about 5150 would give it exactly; one bar was likely read about 50 kg off).',
      [75, 77, 152, 153, 154], topic='data-interpretation', confidence='medium',
      notes='Bar heights were read by eye from the photograph, so the result is approximate.',
      wrong='19.23%, 23.15% and 17.3% need a Ruby total outside the 800 kg read from the chart.')
    Q('procdna-jewellers-emerald-opal', 'Average annual Emerald sales compared with Opal sales in 1998-99',
      'From the same jewellers chart, by what percent are the average annual sales of Emerald for the given period more than the sales of Opal in 1998-99? (Emerald: 300, 250, 400, 400, 150 kg; Opal in 1998-99: 200 kg.)',
      ['50%', '25%', '40%', '120%'], '50%',
      'Average Emerald = (300 + 250 + 400 + 400 + 150)/5 = 300 kg; Opal 1998-99 = 200 kg; (300 - 200)/200 = 50%.',
      'Emerald total = 1500, average 300. Opal 1998-99 = 200. Percentage more = (300 - 200)/200 x 100 = 50%.', [77, 153, 154], topic='data-interpretation',
      wrong='The other options use wrong bases or totals.', confidence='medium')
    Q('procdna-trailing-zeros-937', 'Number of zeros at the end of 937 factorial',
      'Determine the number of zeros at the end of 937!.', ['224', '230', '232', '228'], '232',
      'Count factors of 5: 187 + 37 + 7 + 1 = 232.', 'floor(937/5) = 187, floor(937/25) = 37, floor(937/125) = 7, floor(937/625) = 1. Sum = 232.', [77],
      wrong='Other options miss one of the higher powers of 5.', fast='Keep dividing by 5.')
    Q('procdna-trailing-zeros-3000', 'Number of zeros at the end of 3000 factorial',
      'Determine the number of zeros at the end of 3000!.', ['748', '784', '726', '762'], '748',
      'Count factors of 5: 600 + 120 + 24 + 4 = 748.', 'floor(3000/5) = 600, floor(3000/25) = 120, floor(3000/125) = 24, floor(3000/625) = 4, floor(3000/3125) = 0. Sum = 748.', [160],
      wrong='784, 726 and 762 do not equal the sum of the quotients.')
    Q('procdna-syllogism-boots', 'Syllogism: boots, jugs, plastics, cars and vehicles',
      'Statements: I. Some boots are jugs. II. All jugs are plastics. III. Some plastics are cars. IV. All cars are vehicles.\nConclusions: I. Some plastics are boots. II. Some plastics are cars. III. Some vehicles are plastics.',
      ['Only conclusion I follows', 'Only conclusion II follows', 'Only conclusions I and II follow', 'All follow'], 'All follow',
      'I follows from I and II (some boots are jugs, all jugs are plastics). II repeats statement III. III follows from III and IV.',
      '1. Some boots are jugs and all jugs are plastics, so some boots are plastics, and by conversion some plastics are boots (conclusion I).\n2. Conclusion II is statement III itself.\n3. Some plastics are cars and all cars are vehicles, so those plastics are vehicles: some vehicles are plastics (conclusion III).',
      [121, 122], topic='logical', confidence='medium', notes='The options were partly cropped; the last option reads "All follow".',
      wrong='Each other option omits a valid conclusion.')
    Q('procdna-support-business-email', 'Statement supporting a paragraph about planning a business email',
      'Select the statement that best develops or supports the paragraph: "Before you begin to compose a business email, sit down and think about your purpose for writing the email. ... gather the information before you begin writing. Always keep your objective in mind."',
      ['While some people plan ahead when they are writing a business email, others do not.', 'For many different kinds of writing tasks, planning is an important first step.', 'Brainstorming and writing take approximately equal amounts of time.', 'Business emails are frequently complaint emails.'],
      'For many different kinds of writing tasks, planning is an important first step.',
      'The paragraph advises planning before writing; the statement that planning is an important first step supports and generalises it.',
      'The paragraph\'s point is: plan before you write. Option 2 states that planning is an important first step, which supports it. Option 1 mentions people who do not plan (undermines the advice), option 3 is about time split, option 4 is unrelated.',
      [127], topic='verbal', confidence='medium', notes='The paragraph is partly cropped in the photograph.')
    Q('procdna-series-letters-aby', 'Missing term in ABY, CDW, EFU, GHS, ?',
      'Find the missing term in the series: ABY, CDW, EFU, GHS, ?', ['IJQ', 'IKP', 'IJK', 'IJR'], 'IJQ',
      'The first two letters run through consecutive alphabet pairs (AB, CD, EF, GH, IJ) and the third letter goes backwards in steps of two (Y, W, U, S, Q).',
      'First letters: A, C, E, G, I. Second letters: B, D, F, H, J. Third letters: Y, W, U, S, Q (each minus 2). The next term is I, J, Q.',
      [145], topic='logical', wrong='IKP, IJK and IJR break one of the three progressions.')
    Q('procdna-odd-one-calculus', 'Odd one out: Calculus, Perimeter, Volume, Area',
      'Mark the odd one out from the given options.', ['Calculus', 'Perimeter', 'Volume', 'Area'], 'Calculus',
      'Perimeter, volume and area are measures; calculus is a branch of mathematics.', 'Perimeter, volume and area are quantities that can be measured. Calculus is a field of study, not a measurement.', [145], topic='logical')
    Q('procdna-syllogism-naggers', 'Syllogism: all children are naggers, some children are whiners',
      'Statements: I. All children are naggers. II. Some children are whiners. Which conclusion follows?',
      ['None follow', 'All naggers are whiners', 'No naggers are whiners', 'Some naggers are whiners'], 'Some naggers are whiners',
      'The children who are whiners are also naggers, so some naggers are whiners.', 'Take the children who are whiners (statement II). By statement I they are naggers, so there is at least one person who is both a nagger and a whiner.',
      [144], topic='logical', wrong='"All" and "No" claims are too strong; "None follow" ignores the valid conclusion.')
    Q('procdna-ap-72-terms', 'Number of terms of an A.P. with sum 72',
      'The sum of a series in A.P. is 72, the first term is 17 and the common difference is -2. What is the number of terms in the series?',
      ['6 or 13', '8 or 12', '6 or 12', 'None of the mentioned options'], '6 or 12',
      'S_n = n/2 [34 + (n - 1)(-2)] = n(18 - n) = 72, so n^2 - 18n + 72 = 0 and n = 6 or 12.',
      'S_n = n/2 [2 x 17 + (n - 1)(-2)] = n(18 - n). Set it to 72: n^2 - 18n + 72 = 0, giving (n - 6)(n - 12) = 0. Both are valid because the series goes negative after the 9th term and cancels.',
      [146], wrong='6 or 13 and 8 or 12 do not satisfy the quadratic.', traps='- Giving only one root.')
    Q('procdna-remainder-sum-of-powers', 'Remainder of 43^101 + 23^101 divided by 66',
      'Determine the remainder when (43^101 + 23^101) is divided by 66.', ['0', '2', '5', '(fourth option not visible)'], '0',
      'For odd n, a^n + b^n is divisible by a + b. Here 43 + 23 = 66, so the remainder is 0.', 'Since 101 is odd, x^101 + y^101 is divisible by x + y. 43 + 23 = 66, so the remainder is 0.',
      [147], notes='The fourth option was not visible.', fast='Use the a^n + b^n rule for odd n.')
    Q('procdna-trains-head-on', 'Time to avert a head-on collision between two trains',
      'Ohio Express starts from Ohio at 6:30 a.m. and travels at 50 kmph towards Toronto situated 100 km away. At 7:00 a.m., Vancouver-Ohio Express leaves Toronto towards Ohio and travels at 40 kmph. At 7:30 a.m., Mr. Sundar, the traffic inspector at Toronto, realizes that both the trains are running on the same track. How much time does he have to avert a head-on collision between the two trains?',
      ['20 minutes', '15 minutes', '25 minutes', '30 minutes'], '20 minutes',
      'By 7:30 the first train has gone 50 km and the second 20 km, leaving 30 km. Closing speed 90 km/h, so 30/90 h = 20 minutes.',
      'At 7:30 a.m.: train 1 travelled 1 h x 50 = 50 km; train 2 travelled 0.5 h x 40 = 20 km. Gap = 100 - 50 - 20 = 30 km. Relative speed = 50 + 40 = 90 km/h. Time = 30/90 h = 1/3 h = 20 minutes.',
      [148], wrong='15, 25 and 30 minutes come from wrong gap or speed sums.', traps='- Forgetting that train 2 started 30 minutes after train 1.')
    Q('procdna-random-bags-chocolates', 'Probability of exactly 3 chocolates in the first of 3 bags',
      'Amanda keeps 8 identical chocolates in 3 similar bags at random. What is the probability that she kept exactly 3 chocolates in the first bag?',
      ['0.2731', '0.3256', '0.1924', '0.3443'], '0.2731',
      'Each chocolate independently goes to the first bag with probability 1/3: P = C(8,3)(1/3)^3(2/3)^5 = 56 x 32 / 6561 = 0.2731.',
      'Treat each of the 8 chocolates as placed independently and uniformly in one of 3 bags (the intended model, since it matches an option). Exactly 3 in the first bag: C(8,3) x (1/3)^3 x (2/3)^5 = 56 x 32 / 6561 = 0.2731.',
      [159], confidence='medium',
      notes='If the bags were filled uniformly over compositions of 8 into 3 parts (45 equally likely), the probability would be 6/45 = 0.133, which is not an option, so the independent-placement model is the intended one.',
      wrong='The other options do not match the binomial value.')
    skip(P, w(41)[0], 'Latin-square figure item (image only)')
    skip(P, w(53)[0], 'Latin-square figure item (image only)')
    skip(P, w(143)[0], 'figure-sequence item (image only)')
    skip(P, w(133)[0], 'figure-set item (image only)')
    skip(P, w(135)[0], 'letter-coding item with cropped stem and Latin-square figure')
    skip(P, w(132)[0], 'letter-coding item with garbled stem')
    skip(P, w(151)[0], 'bar-chart follow-up questions, text unreadable')
