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

D['b05_zs_fractal-001'] = S('''Sizes are 7, 8, 9, 10.
1. Perfect squares: only 9. So David has size 9 and brand Pima or Fola.
2. Primes: only 7. Shane has size 7 and brand Nikiy.
3. The only perfect cube is 8, so the size-8 shoe is Fola.
4. David (size 9) is not Fola (Fola is size 8), so David is Pima.
5. John is not Fola, so the size-8 Fola owner is Max; John gets size 10 and the last brand, Avidas.
Result: David-9-Pima, Max-8-Fola, John-10-Avidas, Shane-7-Nikiy.

**Answer: John-10-Avidas**''',
 wrong='- David-7-Pima: David\'s size must be the square 9, and 7 is Shane\'s.\n- Max-9-Fola: the cube size 8 is the Fola shoe, and 9 is David\'s.\n- Shane-7-Avidas: Shane bought from Nikiy.',
 fast='List which sizes are square, prime and cube: they are 9, 7 and 8, which fixes three people at once.', traps='- Treating 1 or 4 as sizes; only 7 to 10 exist.')

D['b05_zs_fractal-002'] = S('''Seats 1 to 6 from the left (facing North, left is the girl's left, but we only need consistent numbering).
1. Three girls between Rachel and Sara means their seats differ by 4: (1,5) or (2,6) in either order.
2. Tara is immediately right of Sara and not at an end. With Sara at 1: Tara 2, Rachel 5. With Sara at 2: Tara 3, Rachel 6. (Sara at 5 or 6 would put Tara at 6 or beyond; Sara at 6 is impossible and Tara at 6 is an end.)
3. Case Sara 1, Tara 2, Rachel 5: free seats are 3, 4, 6. Seat 3 is next to Tara, 4 and 6 are next to Rachel, so Olivia cannot sit anywhere. Rejected.
4. Case Sara 2, Tara 3, Rachel 6: free seats 1, 4, 5. Olivia cannot take 4 (next to Tara) or 5 (next to Rachel), so Olivia sits at seat 1.

**Answer: Olivia**''',
 wrong='Rachel is at the right end (seat 6), Tara is at seat 3 and Nia would need seat 4 or 5, not seat 1.', fast='Write the position difference 4 first; only two placements exist.', traps='- Forgetting the "not at either end" clue for Tara, which removes other cases.')

D['b05_zs_fractal-004'] = S('''Build the partial order from statements I-III.
- P > Q, so P is not the shortest. P is also not the tallest.
- S > R, so S is not the shortest.
- T < U, so U is not the shortest; T is taller than at least three people, so T is not the shortest.
So P, S, T and U are all not the shortest, and the shortest person is one of Q or R. Statement IV is therefore true.

**Answer: True**''',
 wrong='"False" and "Uncertain" fail because the first three statements already exclude four of the six people.', fast='Cross out everyone who is taller than someone: only Q and R remain.', traps='- Worrying about the exact full ordering, which is not needed.')

D['b05_zs_fractal-005'] = S('''Alex is 10th from the top. Alex is eight positions higher than Ben, so Ben is 10 + 8 = 18th from the top.
Ben is also 18th from the bottom. Total = rank from top + rank from bottom - 1 = 18 + 18 - 1 = 35.

**Answer: 35**''',
 wrong='36 forgets to subtract 1 (Ben is counted twice); 20 uses 10 + 10.', fast='Same person from both ends: total = a + b - 1.', traps='- Using Alex\'s numbers for the total instead of Ben\'s.')

D['b05_zs_fractal-006'] = S('''Legs alternate: 10 N, 20 S, 30 N, 40 S, 50 N, 60 S (the last turn covers 60 m, and the pattern increases by 10 each time).
North total = 10 + 30 + 50 = 90; South total = 20 + 40 + 60 = 120. Net = 30 m South, and she faces South.
Her right while facing South is West, so she walks 30 m West.
Final displacement: 30 m South and 30 m West, so distance = sqrt(30^2 + 30^2) = 30 sqrt(2) m.

**Answer: 30 sqrt(2) m**''',
 wrong='20 + 20 sqrt(2) and 20 sqrt(5) come from wrong net displacements; 40 m ignores the sideways leg.', fast='Net = (10 - 20) + (30 - 40) + (50 - 60) = -30, then a 30 m sidestep gives a 45-degree diagonal.', traps='- Taking right as East when facing South.')

D['b05_zs_fractal-007'] = S('''Phrases: (1) you can win -> joe nee sop; (2) can you do -> sop nee tee; (3) do you play -> nee sow tee.
- "you" is in all three; the common code word is nee, so you = nee.
- Phrases 1 and 2 share "can" and "you": common codes are nee and sop, so can = sop.
- Then win = joe (rest of phrase 1).
- Phrases 2 and 3 share "do": the remaining common code is tee, so do = tee, and play = sow.
"play can win" = sow sop joe, i.e. the code set {sop, sow, joe}. The option listed as "sop sow joe" contains exactly these three codes.

**Answer: sop sow joe**''',
 wrong='"sop tee joe" contains tee (do); "nee tee sow" contains nee (you); "joe tee sow" contains tee.', fast='Find the word common to all phrases first (you = nee), then the pair-wise commons.', traps='- The question asks for the set of codes, and the options are written in a different order from the phrase.')

D['b05_zs_fractal-009'] = S('''The passage says: determination can ensure success, and enhancing determination using self-control is the first step towards success. So self-control is a contributing step towards success: "self-control is a factor that can lead to success".''',
 wrong='- "Only one step": the passage says "the first step", not the only step.\n- "Anyone successful would surely have greater self-control": too strong ("surely"), a reverse inference.\n- "Only with determination": the passage says determination can ensure success, not that nothing else can.',
 fast='Prefer the weakest modal option ("can lead to") over absolute words (surely, only, always).', traps='- Reversing a necessary-and-sufficient reading of "first step".')

D['b05_zs_fractal-011'] = S('''The advertiser reasons: more protein in two spoons than a bowl of pulses, therefore the drink can replace pulses. The hidden assumption is that protein is the only reason one needs pulses.
Weaken it by showing pulses provide something the drink does not: "Pulses provide important nutrients other than protein as well".''',
 wrong='- "Only a few people depend on pulses for protein" and "protein requirement varies" do not touch replacement.\n- "A bowl of pulses may not be sufficient for everyone" says pulses lack protein, which supports the drink.',
 fast='Attack the assumption: protein is the only function of pulses.', traps='- Picking an option about protein quantity instead of non-protein value.')

D['b05_zs_fractal-013'] = S('''Argument: many applied (premise), therefore such skilled workers were getting jobs (conclusion). To weaken, show that applying did not translate into getting jobs: only a very small percentage obtained suitable positions.
The other options are about hiring preferences in the USA, Indian demand for exposure (which supports the conclusion) or the need to reskill (which does not stop them being hired).''',
 wrong='US hiring practices and re-skilling needs do not contradict "they were getting jobs"; Indian demand for foreign exposure strengthens the claim.', fast='Look for the option that breaks the step from "applied" to "got".', traps='- Choosing an option that is merely about the topic (IT workers) and not the logic gap.')

D['b11_small-006'] = S('''From the net, the opposite pairs are: 4-dot and 5-dot (first and third squares of the column), black and hatched (second and fourth), and blank and circles.
1. A box can never show two opposite faces together. Option 2 shows hatched and black together, and option 3 shows circles and blank together, so both are impossible.
2. Fold with the 5-dot face in front: top = black, bottom = hatched, left = blank, right = circles, back = 4-dot.
3. Option 1 (top hatched, front 4-dot) forces the right face to be circles, but option 1 shows blank on the right, so it fails.
4. Rotating the folded box 180 degrees about the vertical axis gives front = 4-dot, top = black, right = blank, which is option 4.

**Answer: Only (4)**''',
 wrong='Options 2 and 3 show opposite faces together; option 1 has the wrong face on the right for its top and front.', fast='List the three opposite pairs, eliminate boxes showing a pair, then test the rest by one fold.', traps='- Forgetting that a rotation of the whole box can also match a pattern.')
D['b11_small-006'] += '\nNote: this is a figure-based question; the working above uses the textual description of the net.\n'

D['curated-local-prime-factors'] = S('''52,500 = 52,5 x 100 = 525 x 100 = (3 x 5^2 x 7) x (2^2 x 5^2) = 2^2 x 3 x 5^4 x 7.
The distinct primes are 2, 3, 5, 7: four primes, all below 175.

**Answer: 4**''', fast='Strip factors: 52500 / 100 = 525 = 3 x 175 = 3 x 5^2 x 7.', traps='- Counting prime powers (2^2, 5^4) instead of distinct primes.')

D['curated-local-garden-perimeter'] = S('''Width w, length 5w. Perimeter 2(w + 5w) = 12w = 2160, so w = 180 and length = 5 x 180 = 900.

**Answer: 900**''', wrong='850, 750, 800 and 1000 do not satisfy 12w = 2160 with length 5w.', fast='Length is 5/12 of the perimeter... half the perimeter is 1080 = 6w, so the length is 1080 x 5/6 = 900.', traps='- Using the perimeter as 6w instead of 12w.')

D['curated-local-labelled-die'] = S('''Faces: x on 3, y on 2, z on 1. P(x) = 1/2, P(y) = 1/3, P(z) = 1/6.
P(same label on two independent rolls) = (1/2)^2 + (1/3)^2 + (1/6)^2 = 9/36 + 4/36 + 1/36 = 14/36 = 7/18.

**Answer: 7/18**''', wrong='1/6, 13/36 and 11/18 come from adding the probabilities rather than their squares or arithmetic slips.', fast='Sum of squares of the three label probabilities.', traps='- Computing P(x) + P(y) + P(z) = 1.')

D['curated-local-digit-sum-chain'] = S('''Let a = f(k), b = f(a), c = f(b). We need f(c) = 1 with k > a > b > c > 1.
- c > 1 and f(c) = 1: the smallest such c is 10 (digit sum 1).
- b > c with f(b) = c = 10: the smallest number with digit sum 10 above 10 is 19.
- a > b with f(a) = b = 19: the smallest number with digit sum 19 above 19 is 199.
- k > a with f(k) = a = 199: k must have digit sum 199, which needs at least ceil(199/9) = 23 digits (22 digits give at most 198).
A 23-digit number with digit sum 199 exists (for example 22 nines and a 1), and it is larger than 199.

**Answer: 23**''', wrong='21 and 22 digits give a maximum digit sum of 189 and 198, which is below 199; 24 is not minimal.', fast='Work backwards: 1 -> 10 -> 19 -> 199, then 199/9 rounded up.', traps='- Starting from c = 1 (not allowed since c > 1).')

D['curated-local-consecutive-hh'] = S('''Eight tosses give 7 adjacent pairs. Each pair is HH with probability 1/2 x 1/2 = 1/4. Linearity of expectation: E = 7 x 1/4 = 7/4. Overlapping pairs are dependent, but linearity does not need independence.

**Answer: 7/4**''', wrong='2 and 9/4 and 5/2 are not 7/4; 2 comes from 8 x 1/4 (counting 8 pairs).', fast='(n - 1)/4.', traps='- Counting 8 pairs, or trying to subtract for HHH overlaps.')

D['curated-local-conditional-reroll'] = S('''Cases by first roll:
- 6 (probability 1/6): sum >= 6 already.
- 4 or 5: no re-roll and the sum is below 6, so they fail.
- 1, 2, 3: re-roll; need the second roll >= 5, >= 4, >= 3 respectively: 2, 3 and 4 outcomes out of 6.
P = 1/6 + (1/6)(2/6 + 3/6 + 4/6) = 1/6 + (1/6)(9/6) = 1/6 + 1/4 = 5/12.

**Answer: 5/12**''', wrong='10/21 would result from re-rolling after every first result; 2/3 and 1/8 do not match the case probabilities.', fast='Use P = sum over first roll of P(first) x P(success).', traps='- Re-rolling after 4 and 5 (the rule re-rolls only after 1, 2 or 3).')

D['curated-local-cube-divisor-count'] = S('''If N = p1^e1 ... pk^ek is a perfect cube, every ei = 3 ai, so the divisor count is the product of (3 ai + 1) factors, each equal to 1 modulo 3, hence the count is 1 modulo 3.
- 22 = 3 x 7 + 1: achievable with a single prime p^21 (21 = 3 x 7).
- 37 = 3 x 12 + 1: achievable with p^36.
- 53 = 3 x 17 + 2: not 1 mod 3, impossible.
- 66 = 3 x 22: not 1 mod 3, impossible.
So only A and B could be perfect cubes.

**Answer: A & B**''', wrong='53 and 66 fail the 1 mod 3 condition, so any option containing C or D is wrong.', fast='Check divisor count mod 3: only counts that are 1 mod 3 can belong to cubes.', traps='- Forgetting that a prime power p^(3a) has 3a + 1 divisors.')

D['curated-local-five-digit-multiple'] = S('''Divisible by 15 means divisible by 5 and 3.
1. Divisible by 5: the last digit is 5 (0 is not available).
2. The five digits are chosen from {2,3,4,5,6,7} with sum 27 - omitted digit. For divisibility by 3 the sum must be a multiple of 3, so the omitted digit is 3 or 6 (it cannot be 5).
3. For each choice, the remaining four digits fill the first four places in 4! = 24 ways.
Total = 2 x 24 = 48.

**Answer: 48**''', wrong='36 and 60 and 96 come from counting only one omitted digit or allowing other last digits.', fast='Omitted digit must be congruent to 27 mod 3, i.e. 3 or 6; then 2 x 4!.', traps='- Letting 5 be omitted (then no digit ends in 5).')

D['curated-local-printed-digits'] = S('''Count digits 3 and 5 in 1,000 to 9,999 and 10,000.
- Thousands place: digit 3 appears in 3,000 to 3,999 = 1,000 numbers; same for 5.
- Each other place (hundreds, tens, units): of the 9,000 numbers, the digit appears in 1/10 of them = 900 times.
For one digit: 1,000 + 3 x 900 = 3,700. For both: 7,400. The number 10,000 contains neither digit.

**Answer: 7400**''', wrong='7960, 7680 and 7560 add or omit blocks of 900.', fast='3,700 per digit x 2.', traps='- Counting 900 for the thousands place (only 1,000 numbers have 3 there).')

D['curated-local-coffee-tea-overlap'] = S('''Everyone likes at least one drink, so coffee + tea - both = 100%. Both = 63 + 76 - 100 = 39%.

**Answer: 39**''', fast='Sum minus 100.', traps='- Forgetting the "everyone likes one" condition (otherwise only a range is determined).')

D['curated-local-binomial-digit-product'] = S('''Two-digit strings 00 to 99 with digit product 18: 29, 92, 36, 63. So p = 4/100 = 1/25 per selection.
Four independent selections: X ~ Binomial(4, 1/25). P(X >= 2) = 1 - P(0) - P(1).
P(0) = (24/25)^4 = 331776/390625; P(1) = 4 x (1/25) x (24/25)^3 = 55296/390625.
P(X >= 2) = (390625 - 331776 - 55296)/390625 = 3553/390625.

**Answer: 3553/390625**''', wrong='601/390625 is P(X >= 3)-like; options with denominator 380625 are not powers of 25.', fast='Compute 1 - (24/25)^3 (24/25 + 4/25).', traps='- Treating the product 18 as including pairs like 18 (product 8) or 09 (0).')

D['curated-local-ant-on-cube'] = S('''Let E_d be the expected steps to reach the opposite corner from a vertex at distance d (in edges) from it. E_0 = 0.
- From distance 3: all three edges lead to distance 2: E_3 = 1 + E_2.
- From distance 2: 2 edges go to distance 1, 1 edge goes back to distance 3: E_2 = 1 + (2/3)E_1 + (1/3)E_3.
- From distance 1: 1 edge reaches the target, 2 edges go to distance 2: E_1 = 1 + (2/3)E_2.
Simplify: E_2 = 1 + (2/3)E_1 + (1/3)(1 + E_2) gives (2/3)E_2 = 4/3 + (2/3)E_1, so E_2 = E_1 + 2. Then E_1 = 1 + (2/3)(E_1 + 2) gives E_1/3 = 7/3, so E_1 = 7, E_2 = 9 and E_3 = 10.

**Answer: 10**''', wrong='7 and 9 are E_1 and E_2; 8 is not an expected value of any state.', fast='Known result: expected hitting time of the antipode on a 3-cube is 10.', traps='- Forgetting the step that moves backwards from distance 2.')

D['curated-local-uniform-ratio'] = S('''(p, q) is uniform on the unit square. The condition 1 < p/q < 2 means q < p < 2q (and p < 1).
Area = integral from q = 0 to 1/2 of (2q - q) dq + integral from q = 1/2 to 1 of (1 - q) dq = [q^2/2] from 0 to 1/2 + [q - q^2/2] from 1/2 to 1 = 1/8 + 1/8 = 1/4.

**Answer: 1/4**''', wrong='1/2, 1/8 and 3/8 correspond to other regions (for instance only one of the two integrals, or P(p/q < 2)).', fast='P(p/q > 1) = 1/2 and P(p/q > 2) = 1/4, so the difference is 1/4.', traps='- Forgetting that p < 1 caps the upper limit when q > 1/2.')

D['curated-local-lotus-doubling'] = S('''Covered area after d days = 25 x 2^d square feet.
- d = 7: 25 x 128 = 3,200 < 5,300.
- d = 8: 25 x 256 = 6,400 >= 5,300.
The pond is fully covered on day 8 (the area cannot exceed the pond, so it is exactly covered then).

**Answer: 8 days**''', wrong='6 and 7 days give 1,600 and 3,200 square feet; 9 days is later than necessary.', fast='5300/25 = 212, and 2^8 = 256 is the first power of 2 above 212.', traps='- Using doubling of the number of days rather than area.')

D['curated-local-oracle-five-ingredients'] = S('''Facts: apricots and eggs are used (statement 4).
- Statement 2: apricots used implies bacon and cake used.
- Statement 3 (contrapositive): apricots used implies donuts used.
So the chosen ingredients include apricots, eggs, bacon, cake and donuts: that is five distinct ingredients, filling the quota of exactly five. All five are known.

**Answer: 5**''', wrong='2, 3 and 4 count only the givens or part of the chain.', fast='Apricots forces bacon, cake and donuts; add eggs; count 5.', traps='- Forgetting the contrapositive of statement 3.')

D['curated-local-oracle-painted-cube'] = S('''A 10 x 10 x 10 cube has 1,000 unit cubes. A small cube shows three painted faces only if it touches three outer faces, i.e. it is at a corner of the big cube. A cube has 8 corners.

**Answer: 8**''', wrong='10 and 100 and 64 correspond to edge-count, face-count or inner counts: 12 x 8 = 96 two-face cubes, 6 x 64 = 384 one-face cubes, 8^3 = 512 unpainted.', fast='Three-face cubes are always the 8 corners.', traps='- Confusing with the number of edge cubes.')

D['curated-local-oracle-favorite-color'] = S('''Facts: Matthew: badminton, Russia. Peter and Sebastian: China/UK and yellow/green. Albert: football, not yellow, not UK.
1. Jack is from neither India nor China and not Russia (Matthew), nor the UK (Peter or Sebastian), so Jack is from South Korea; Jack likes red.
2. Albert is not from the UK; the remaining country for him is India. The Indian likes brown, so Albert likes brown.
3. Colors used: red (Jack), brown (Albert), yellow and green (Peter, Sebastian). The leftover color black belongs to Matthew.

**Answer: Matthew**''', wrong='Albert likes brown, Peter and Sebastian like yellow or green.', fast='Eliminate colours: red, brown, yellow, green are taken, leaving black for Matthew.', traps='- Forgetting that Jack cannot be from the UK because the UK and China belong to Peter and Sebastian.')

D['curated-local-oracle-standing-order'] = S('''Positions 1 to 5 from the left. Tyson = 1 (clue 3), Richard = 4 (second from right).
- Peter is right of both Quinn and Tyson and next to Richard (clue 6), so Peter is 3 or 5.
- Peter and Quinn are adjacent (clue 1). If Peter = 5, Quinn must be 4, but Richard is 4. So Peter = 3 and Quinn = 2 (left of Peter).
- Steve is next to Richard and the remaining seat is 5: Steve = 5, which is also not next to Tyson.
Order: Tyson, Quinn, Peter, Richard, Steve. The middle is Peter.

**Answer: Peter**''', wrong='Richard is 4th, Steve 5th, Quinn 2nd.', fast='Fix Tyson and Richard first; clue 5 then forces Peter to the centre.', traps='- Treating "next to" as ordered (left of) rather than just adjacent.')

D['curated-local-oracle-autonomy'] = S('''Autonomy means the right or condition of self-government. Of the options, it is the only word associated with self-governing. Autocracy is rule by a single person, anarchy is the absence of government, and ethnology is the study of peoples.

**Answer: Autonomy**''', wrong='Autocracy: absolute rule by one person. Anarchy: no governing authority. Ethnology: study of cultures.', fast='Auto = self, nomos = law, so self-law.', traps='- Picking "autocracy" because of the shared prefix auto-.')

D['curated-local-oracle-hiring-idiom'] = S('''The sentence warns against hiring someone who seems dangerous or deceptive. "A wolf in sheep\'s clothing" means someone harmful who looks harmless. "A fish out of water" means uncomfortable in a new setting, "the black sheep of the family" means a disreputable member, and "the apple of my eye" means a cherished person (a compliment, wrong here).

**Answer: a wolf in sheep\'s clothing**''', fast='Eliminate the compliment ("apple of my eye") first.', traps='- "Fish out of water" fits the discomfort reading but not a reason to refuse a hire.')

out = Path(sys.argv[1] if len(sys.argv) > 1 else 'build/solutions/B_02.json')
out.write_text(json.dumps(D, indent=1, ensure_ascii=False), encoding='utf-8')
print(len(D))
