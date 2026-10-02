import json, sys
from pathlib import Path


def S(body, wrong='', fast='', traps=''):
    out = '### Solution\n' + body.strip() + '\n'
    if wrong:
        out += '\n### Why the other options are wrong\n' + wrong.strip() + '\n'
    if fast:
        out += '\n### Faster method\n' + fast.strip() + '\n'
    if traps:
        out += '\n### Common traps\n' + traps.strip() + '\n'
    return out


D = {}

D['curated-local-oracle-exam-idiom'] = S('''The sentence needs an idiom meaning "start well and quickly" after months of preparation.
- Hit the ground running: begin something energetically and effectively from the start. Fits.
- Have a field day: enjoy an opportunity greatly. Does not describe performing well.
- Be a dark horse: an unexpected winner. Possible but about surprise, not preparation.
- Have a lot on my plate: have many tasks. Contradicts "hoping to".
The best fit is "hit the ground running".

**Answer: hit the ground running**''',
 fast='Match the idiom to the meaning the context needs: effective start after preparation.',
 traps='- "Dark horse" sounds exam-related but means an unexpected contender, not a well-prepared candidate.\n- The printed options do not include "ace the exam", so choose the closest, not a perfect fit.')

D['curated-local-oracle-sports-ambiguity'] = '''### Solution
The statement is ambiguous, so first identify the readings.

1. Reading A (inclusive totals): 50 like football, 40 like hockey, and the others ("the rest") like both. Then at least one game is liked by 100 - (number who like neither). The wording says "the rest like both", but 100 - 50 - 40 = 10 would be the rest, and 50 + 40 - 10 = 80 liking at least one would leave 20 who like neither, contradicting "the rest like both".
2. Reading B (exclusive categories): 50 like only football, 40 like only hockey, and the remaining 10 like both. Then everyone likes at least one game: 50 + 40 + 10 = 100.
3. Union counting: with 10 who like both, football = 60 and hockey = 50, so the union is 60 + 50 - 10 = 100. None of the listed options (40, 90, 80, 20) is 100.
4. The option 80 results from the mixed reading above (50 + 40 - 10), which is internally inconsistent.

**Conclusion:** the question is flawed; the consistent exclusive reading gives 100, which is not offered, and the listed key 80 relies on the inconsistent reading. If forced to choose, 80 is the value produced by the usual inclusion-exclusion with overlap 10.

### Common traps
- Applying inclusion-exclusion while also assuming "the rest like both" refers to a third group.
- Always check that the answer options cover the consistent reading before guessing.
'''

D['curated-local-oracle-only-cricket'] = S('''Union = 100 - 12 = 88%. Both = football + cricket - union = 60 + 40 - 88 = 12%. Only cricket = cricket - both = 40 - 12 = 28%.

**Answer: 28**''', wrong='14 and 42 and 56 come from using the wrong overlap (e.g. subtracting 26 or 0).', fast='Only cricket = union - football = 88 - 60 = 28.', traps='- Forgetting that "neither" must be removed first.')

D['curated-local-oracle-spawned-antonym'] = S('''"Spawned" means gave rise to, produced. Its opposites would mean to suppress or stop. Fostered (encouraged), begat (produced) and generated (created) are all synonyms in this context. Squelched means crushed or suppressed, so it is the farthest in meaning.

**Answer: squelched**''', wrong='Fostered, begat and generated are close to spawned.', fast='Look for the only word with the opposite direction (stop vs create).', traps='- Reading "farthest" as "closest" and picking a synonym.')

D['curated-local-oracle-weekday'] = S('''62 = 7 x 8 + 6, so 62 days is 8 whole weeks plus 6 days. Six days after Monday: Tue, Wed, Thu, Fri, Sat, Sun. The answer is Sunday.

**Answer: Sunday**''', wrong='Monday would be 56 or 63 days later; Saturday is 5 days later; Wednesday is 2 days later.', fast='62 mod 7 = 6, and +6 equals -1, so the day before Monday.', traps='- Counting 62 mod 7 as 5.')

D['curated-local-oracle-remainder'] = S('''92 x 21 = 1,932 and 1,992 - 1,932 = 60. Since 0 <= 60 < 92, the remainder is 60, which is not among 0, 1, 40.

**Answer: None of the above**''', fast='1992 = 2000 - 8; 2000 mod 92 = 68, 68 - 8 = 60.', traps='- Choosing 40 from a wrong multiple.')

D['curated-local-oracle-work-rates'] = S('''Rates in jobs per day: a + b = 1/10, b + c = 1/5, c + d = 1/4, a = 1/40.
- b = 1/10 - 1/40 = 3/40.
- c = 1/5 - 3/40 = 8/40 - 3/40 = 5/40.
- d = 1/4 - 5/40 = 10/40 - 5/40 = 5/40.
So c = d = 1/8 per day: C and D work at the same rate (each alone takes 8 days). A is 1/40 and B is 3/40, so no other pair is equal.

**Answer: C and D**''', wrong='A and B (1/40 vs 3/40), B and D (3/40 vs 5/40) and A and D (1/40 vs 5/40) differ.', fast='Use a denominator of 40: a + b = 4, b + c = 8, c + d = 10, a = 1, so b = 3, c = 5, d = 5.', traps='- Treating the days as additive rather than the rates.')

D['curated-local-oracle-semicircle-angles'] = S('''Let the arcs AC and CE (on the semicircle containing B and D) measure u and v, with u + v = 180 degrees since AE is a diameter.
- B lies on arc AC, so angle ABC is an inscribed angle that intercepts the other arc AC (the one not containing B), of measure 360 - u. Hence angle ABC = (360 - u)/2.
- Likewise angle CDE = (360 - v)/2.
- Sum = (720 - (u + v))/2 = (720 - 180)/2 = 270 degrees.
Check with equal spacing: A, B, C, D, E divide the semicircle into four 45-degree arcs; u = v = 90, and each angle is 135 degrees, so the sum is 270.
The sum 270 degrees is not among the listed options (135, 180, 225, 315, 90): the question is mis-keyed.

**Answer: 270 degrees (not offered in the options)**''', fast='Test the equally spaced case: both angles are 135 degrees, so the sum is 270.', traps='- Using the angle in a semicircle (90 degrees) for the wrong triangle.')

D['curated-local-oracle-hiker'] = S('''Take north as +y and east as +x.
- 50 m north: (0, 50).
- Turn left (west), 30 m: (-30, 50).
- Turn left (south), 50 m: (-30, 0).
- Turn left (east), 50 m: (20, 0).
Distance from the start = 20 m, which is not among 25, 50, 35.

**Answer: None of the above (20 m)**''', fast='North and south cancel; east 50 minus west 30 leaves 20.', traps='- Mixing the turn direction (left from north is west).')

D['curated-local-oracle-digital-root'] = S('''25! contains the factors 3, 6, 9, 12, ... so it is divisible by 9. Repeated digit sums preserve the residue modulo 9. A positive multiple of 9 has residue 0 mod 9, hence its digital root is 9.

**Answer: 9**''', wrong='6, 7 and 8 would need a nonzero residue modulo 9.', fast='n! for n >= 6 is divisible by 9, so its digital root is 9.', traps='- Computing the huge factorial instead of using mod 9.')

D['curated-local-oracle-expected-vegetarians'] = S('''Let X be the number of vegetarians among the two selected. For each selected position, the chance of a vegetarian is 20/50 = 2/5. By linearity of expectation E[X] = 2 x 2/5 = 4/5 (without replacement does not change the expectation).
The options are written over 245: 4/5 = 196/245.

**Answer: 196/245**''', wrong='197/245, 198/245 and 191/245 are not equal to 4/5.', fast='Expectation = n x (K/N) = 2 x 20/50.', traps='- Computing the hypergeometric pieces and making an arithmetic slip; linearity is quicker.')

D['curated-local-oracle-father-age'] = S('''Let the father\'s age at the vacation be F.
- He was a bachelor for the first F/3 years, so he married at age F/3.
- The son was born 10 years after marriage, when the father was F/3 + 10.
- The son\'s age at the vacation is F - (F/3 + 10) = 2F/3 - 10.
- The father is twice the son: F = 2(2F/3 - 10) = 4F/3 - 20, so F/3 = 20 and F = 60.
Check: he married at 20, the son was born at 30, so the son is 30 and the father 60.

**Answer: 60**''', wrong='50, 70 and 80 do not satisfy F = 2(2F/3 - 10).', fast='Plug in the options: F = 60 gives son 30 = 60/2.', traps='- Interpreting the one-third as the time since marriage.')

D['curated-local-oracle-past-perfect'] = S('''The sentence: "I regret that I wasn\'t aware that you have lost your job when you visited me last week."
The loss of the job happened before the visit and before the speaker\'s lack of awareness (both in the past), so the earlier event needs the past perfect: "you had lost your job". The faulty segment is "have lost your".
"I wasn\'t aware" (past) and "when you visited me" (simple past) are fine; "I regret" can stay present because the regret is felt now.

**Answer: Have lost your**''', wrong='"I wasn\'t aware" and "When you visited me" are correct past forms.', fast='Look for two past events; the earlier one takes had + past participle.', traps='- Marking "I regret" as an error because the rest is past tense.')

D['curated-local-oracle-real-set'] = '''### Solution
Solve (x^2 + 5x + 4)/(x^2 - 7x + 12) <= 0 for positive real x with x not equal to 3 or 4.
1. Factor: numerator = (x + 1)(x + 4); denominator = (x - 3)(x - 4).
2. For x > 0 the numerator is always positive.
3. So the fraction is <= 0 exactly when the denominator is negative: 3 < x < 4.
4. The numerator never vanishes for positive x, so equality (zero) never occurs.
5. Therefore S = (3, 4), an interval containing infinitely many (uncountably many) reals.

None of the listed finite cardinalities (0, 1, 2, 3) is correct. If x were required to be a positive integer, there would be no integer in (3, 4) and the cardinality would be 0, which is probably the intended answer.

**Answer: S is infinite; if integers were intended, 0.**

### Common traps
- Forgetting that the numerator is positive for positive x, which removes any sign change at the numerator roots.
- Forgetting the excluded points x = 3 and x = 4.
'''

D['curated-local-oracle-reading-method'] = S('''The passage says the ancient writers made a serious, systematic effort and sought rules about how regimes begin and end; the criticism concerns their methodological naivety.
- "Establishing a methodology for the study of political science": matches the criticism of their method.
- "Putting enough effort": the passage says effort was not lacking.
- "Understanding how rules and laws came into being and passed away": this is what they tried to do; the failure is about method rather than the aim.
- "Studying political data systematically": the passage says they did organise data systematically.

**Answer: Establishing a methodology for the study of political science**''', fast='Look for the sentence that states what the later thinkers criticised: their method.', traps='- Picking the goal they pursued rather than what they failed at.')

D['curated-local-oracle-reading-louis'] = '''### Solution
The passage chain: war and royal extravagance drained the treasury; the proposed reforms increased spending; therefore additional taxes were needed; poor harvests raised bread prices; the taxes and royal excesses increased resentment; Louis XVI failed to establish himself as an enlightened absolutist.

Compare the options:
- Rising bread costs: mentioned as a contributing hardship but not as the stated explanation of the failure of enlightened absolutism.
- Citizens rejecting the proposed ideals: not supported; people resented the cost, not the ideals.
- Nobles obstructing the king\'s ideas: not mentioned.
- The burden of taxes on citizens: stated directly as the consequence of the reforms and the cause of resentment.

**Answer: the burden of taxes on citizens**

### Common traps
- Choosing bread costs because it is vivid; the passage ties the failure to the reform-driven taxes.
- Importing outside history (nobles) that the passage does not state.
'''

D['curated-local-oracle-nine-coins'] = S('''Each weighing has three outcomes (left lighter, right lighter, balance), so k weighings distinguish at most 3^k coins. Since 3^2 = 9, two weighings are enough and one weighing (3 outcomes) cannot separate nine coins.
Strategy: weigh 3 coins against 3 coins. The lighter side (or the unweighed three if balanced) contains the odd coin. Then weigh one of those three against another: the lighter one is the fake, or, if they balance, the third.

**Answer: 2**''', wrong='3, 4 and 5 are not minimal; one weighing cannot find the coin among nine.', fast='3^k >= 9 gives k = 2.', traps='- Splitting into 4 and 5 rather than into thirds.')

D['curated-local-oracle-two-eggs'] = S('''With d drops and two eggs the number of floors that can be covered is d + (d - 1) + ... + 1 = d(d + 1)/2.
- d = 13: 91 floors, not enough for 100.
- d = 14: 105 floors, enough.
Strategy: drop the first egg from floors 14, 27, 39, ..., reducing the step by one each time; if it breaks, use the second egg linearly in the last interval.

**Answer: 14**''', wrong='12 drops cover 78 floors and 13 cover 91; 17 and 20 are far more than necessary.', fast='Solve d(d+1)/2 >= 100.', traps='- Using binary search (it breaks eggs too quickly with only two eggs).')

D['curated-local-oracle-clock-overlap'] = S('''Relative speed of the minute hand over the hour hand is 6 - 0.5 = 5.5 degrees per minute. They coincide every 360/5.5 = 720/11 minutes. In 12 hours (720 minutes) there are 11 coincidences (at times k x 720/11 for k = 0..10 when excluding the end). In 24 hours counting the starting midnight and excluding the next one, there are 22.

**Answer: 22**''', wrong='24 assumes one per hour; 23 and 21 miscount the endpoints.', fast='11 per half-day x 2.', traps='- Counting both midnights or counting 12 per half day.')

D['curated-local-oracle-three-ants'] = S('''Each ant picks a direction independently: 2^3 = 8 equally likely outcomes. A collision is avoided only if all ants move in the same direction (all clockwise or all counterclockwise): 2 outcomes. Any mixed assignment has two neighbours heading towards each other along an edge.
P = 2/8 = 0.25.

**Answer: 0.25**''', wrong='0.2, 0.33 and 0.5 are not 2/8.', fast='P = 2 / 2^n for an n-gon.', traps='- Counting only one of the two uniform directions.')

D['curated-local-oracle-cyclical-sequence'] = S('''Let the first two elements be a and b. For 2 <= i <= 99, x_i = x_{i-1} x_{i+1}, so x_{i+1} = x_i / x_{i-1}. The sequence is a, b, b/a, 1/a, 1/b, a/b, a, b, ... with period 6, and the product of a full period is 1. All terms are nonzero because the total product is 27.
- First 50 terms = 8 full periods (48 terms) plus a, b, so ab = 27.
- First 100 terms = 16 full periods (96 terms) plus a, b, b/a, 1/a, whose product is b^2/a x ... = (a)(b)(b/a)(1/a) = b^2/a = 27.
- With a = 27/b: b^3/27 = 27, so b^3 = 729 and b = 9, a = 3.
Sum of the first two elements = 3 + 9 = 12.

**Answer: 12**''', wrong='6, 7 and 10 do not satisfy ab = 27 and b^2/a = 27.', fast='The period is 6 with product 1; match the remainders 2 and 4.', traps='- Using x_{i+1} = x_i x_{i-1} instead of the quotient.')

D['curated-local-oracle-previous-year-day'] = S('''From 8 December 2006 to 8 December 2007 is 365 days (2007 is not a leap year; the extra day of 2008 is irrelevant). 365 = 7 x 52 + 1, so the weekday advances by 1. Therefore 8 December 2006 was one day before Saturday: Friday.

**Answer: Friday**''', wrong='Sunday, Tuesday and Thursday would need a shift of 1, 3 or 2 days in the other direction.', fast='Non-leap year: the same date moves one weekday later.', traps='- Counting 366 days (the leap day is Feb 29 2008, not in this interval).')

D['curated-local-oracle-weaned-off'] = S('''"Weaned off" means gradually made to stop depending on something. Check each sentence:
- Take seal pups off their mothers\' milk: weaning, a reduction of dependence.
- Dissuade patients from taking alcohol: reducing a habit.
- Curtail children\'s interest in TV and video games: reducing a habit.
- Encourage people to eat fruits and vegetables: promotes a behaviour rather than weaning someone from something.
The odd one out is the encouragement sentence.

**Answer: Encourage people to eat fruits and vegetables**''', fast='The question asks for the sentence that does NOT involve reducing a dependence.', traps='- Picking an option because it is unrelated in topic rather than in idea.')

D['curated-local-oracle-power-mod'] = S('''2000 = 13 x 153 + 11, so 2000 is congruent to 11, i.e. -2 (mod 13).
2000^1000 is congruent to (-2)^1000 = 2^1000 (even exponent). By Fermat, 2^12 is congruent to 1 (mod 13). 1000 = 12 x 83 + 4, so 2^1000 is congruent to 2^4 = 16, which is 3 (mod 13).

**Answer: 3**''', wrong='4, 8 and 11 are other residues of small powers of 2 mod 13.', fast='Reduce the base to -2 and the exponent modulo 12.', traps='- Forgetting that the sign disappears for an even exponent.')

D['curated-local-oracle-phone-customers'] = S('''For July 2012, subtract the August net additions from the August totals (the stated assumption).
- Hington: 46.18 - 0.36 = 45.82.
- Euphore: 47.28 - (1.24 + 0.60) = 45.44.
Combined July total = 45.82 + 45.44 = 91.26 million.
This is not any of 91.21, 6.87, 98.23, so the answer is "None of these".

**Answer: None of these**''', wrong='91.21 is off by 0.05; 6.87 is the combined additions of a different set; 98.23 does not match.', fast='Combined August total 93.46 minus total additions 2.20 = 91.26.', traps='- Forgetting that Euphore has two additions columns (v1 and v2).')

D['curated-local-oracle-pollution-ranks'] = S('''Rank cities from the least polluted (rank 1) in each year.
- 2006: G(11), F(12), A(13), B(15), C(34), D(56), E(57) -> ranks G1 F2 A3 B4 C5 D6 E7.
- 2007: F(12), G(15), B(17), A(21), C(35), E(45), D(57) -> F1 G2 B3 A4 C5 E6 D7.
- 2008: B(11), F(13), G(17), A(24), C(29), E(45), D(56) -> B1 F2 G3 A4 C5 E6 D7.
Rank sequences: A (3,4,4) changes once; B (4,3,1) twice; C (5,5,5) zero; D (6,7,7) once; E (7,6,6) once; F (2,1,2) twice; G (1,2,3) twice.
Changing at most once: A, C, D, E = 4 cities.

**Answer: 4**''', wrong='1, 2 and 3 undercount: cities A, C, D and E all qualify.', fast='Write the three rank lists and count the transitions per city.', traps='- Counting a change in value rather than in rank.')

D['curated-local-oracle-ongoing-tense'] = '''### Solution
The action (suffering from diabetes) began three years ago and continues now. English uses the present perfect (continuous) with "for" plus a duration:
- Correct: "My father has been suffering from diabetes for the past three years."
- "Has suffered" is also grammatical but suggests a completed or summarised experience and loses the ongoing sense.
- "Is suffering ... for" is wrong because the simple present continuous does not combine with "for the past three years".
- "Is suffer" is ungrammatical.

**Answer: has been suffering**

### Common traps
- Using the present continuous with a duration phrase starting in the past.
- Choosing "has suffered" without the ongoing meaning.
'''

D['curated-local-oracle-animal-model'] = '''### Solution
The question asks how many families have two hens and four cows. The supplied data are: 729 farmers, six animals each (cows or hens), hen survival 1/3 and cow survival 2/3. These data give survival probabilities, not the initial composition of any family.

- To count families with exactly two hens, we would need the distribution of the number of hens per family before the flood (for instance each animal being a hen with some probability).
- Survival probabilities say nothing about how many animals of each species a family started with, nor about independence of animals or an observed number of survivors.
- If one assumed a model where each of the six animals is independently a hen with probability 1/3, the expected number of such families would be 729 x C(6,2) x (1/3)^2 x (2/3)^4 = 729 x 15 x 16/729 = 240, but this assumption is not given in the problem.

**Answer: No, the information supplied does not determine the count (240 only under the extra assumed binomial model).**

### Common traps
- Treating survival probabilities as if they were composition probabilities.
- Always check which quantities the question actually supplies before computing.
'''

out = Path(sys.argv[1] if len(sys.argv) > 1 else 'build/solutions/B_03.json')
out.write_text(json.dumps(D, indent=1, ensure_ascii=False), encoding='utf-8')
print(len(D))
