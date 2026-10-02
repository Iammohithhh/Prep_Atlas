"""MAQ Software: two coding problems plus reasoning, quant and CS MCQs."""


def extend(add, merge, skip, alias):
    M = 'MAQ Software'

    def w(*ns):
        return [f'IMG-20240921-WA0{n}.jpg' for n in ns]

    def Q(key, title, stmt, options, ans, explain, steps, srcs, topic, section='aptitude', wrong='', fast='', traps='', **kw):
        sol = '### Solution\n' + steps.strip() + f'\n\n**Answer: {ans}**\n'
        if wrong:
            sol += '\n### Why the other options are wrong\n' + wrong.strip() + '\n'
        if fast:
            sol += '\n### Faster method\n' + fast.strip() + '\n'
        if traps:
            sol += '\n### Common traps\n' + traps.strip() + '\n'
        add(key, M, title, stmt, ans, explain, section=section, topic=topic, type='mcq', options=options,
            sources=srcs, solution=sol, **kw)

    add('maq-christmas-celebration', M, 'Christmas gifts: pair chocolate boxes whose total is divisible by x',
        'You are a teacher with n boxes of chocolates and x students. Each gift consists of exactly two boxes, and the total number of chocolates in a gift must be divisible by x so it can be shared evenly. Each box can be used in at most one gift and not partially. Find the maximum number of chocolate boxes that can be given as gifts.',
        None,
        'Only remainders mod x matter. Boxes with remainder 0 pair among themselves, remainders r and x-r pair with each other, and when x is even the remainder x/2 pairs with itself. Count pairs with a frequency table and return twice the number of pairs. O(n + x) per test, O(x) space; verified against brute force.',
        section='dsa', topic='hashing', type='coding', sources=w(155),
        function_signature='maxBoxes(n, x, a)',
        input_format='T test cases. Each has n and x, then n integers a_i (the chocolates in each box).',
        output_format='For each test case print one integer: the maximum number of boxes given as gifts.',
        constraints='1 <= T <= 10; 1 <= n, x <= 10^5; 1 <= a_i <= 10^9.',
        examples=[{'input': '1\n5 4\n10 7 6 5 1', 'output': '4', 'explanation': 'Gifts (10, 6) and (7, 5) (or (7, 1)) use four boxes.'}],
        leetcode={'name': 'Check If Array Pairs Are Divisible by k', 'url': 'https://leetcode.com/problems/check-if-array-pairs-are-divisible-by-k/', 'similarity': 'similar'},
        solution='''### Intuition
A pair of boxes works when (a + b) % x == 0, which depends only on the remainders. Remainder r needs a partner with remainder (x - r) % x, so this is a matching problem between remainder classes rather than between individual boxes.

### Approach
1. Count how many boxes have each remainder r = a % x.
2. Remainder 0: those boxes pair with each other, giving cnt[0] // 2 pairs.
3. For r from 1 to x // 2: if 2r == x the class pairs with itself, giving cnt[r] // 2 pairs; otherwise it pairs with class x - r, giving min(cnt[r], cnt[x - r]) pairs.
4. The answer is 2 x (total pairs).

### Why it works
The classes interact only in these pairs, so the matching decomposes into independent sub-problems, each solved optimally by taking the maximum possible pairs (min of the two sizes or half of the size).

### Complexity
O(n + x) time per test case and O(min(n, x)) space with a hash map.

### Python solution
```python
from collections import Counter

def maxBoxes(n, x, a):
    cnt = Counter(v % x for v in a)
    pairs = cnt[0] // 2                  # remainder 0 pairs with itself
    for r in range(1, x // 2 + 1):
        if 2 * r == x:                   # r equals x - r
            pairs += cnt[r] // 2
        else:
            pairs += min(cnt[r], cnt[x - r])
    return 2 * pairs
```

### Dry run
x = 4, boxes 10, 7, 6, 5, 1 have remainders 2, 3, 2, 1, 1. cnt[0] = 0 (0 pairs); r = 1: min(cnt[1] = 2, cnt[3] = 1) = 1; r = 2: 2r = 4 so cnt[2] // 2 = 1. Pairs = 2, answer 4.

### Edge cases & pitfalls
- x = 1: every pair works, answer is n rounded down to even.
- When x is even, do not count r = x/2 twice.
- Large x (10^5) is fine with a dictionary; avoid allocating when only n values exist if x is huge.
- Read all test cases fast (sys.stdin).''')
    add('maq-largest-palindrome', M, 'Largest lexicographically smallest palindrome from the characters of a string',
        'Hari is given a string S of lowercase letters. He has to find the largest palindrome that can be formed using the characters of S (each character used at most as many times as it appears). If several such palindromes exist, he must output the lexicographically smallest one.',
        None,
        'Count letters. Use floor(count/2) pairs of every letter to build the left half in ascending order; the middle character (if any letter has an odd count) is the smallest letter with an odd count; the right half is the reverse of the left. O(|S| + 26) per test; verified against brute force.',
        section='dsa', topic='strings', type='coding', sources=w(156, 157),
        function_signature='solve(s)',
        input_format='T, then T lines each with a lowercase string S.',
        output_format='For each test case print the largest (lexicographically smallest) palindrome.',
        constraints='1 <= T <= 100; 1 <= |S| <= 10^5.',
        examples=[{'input': '3\nadskassda\ntalent\ndecrypt', 'output': 'adsasda\ntat\nc'}],
        leetcode={'name': 'Longest Palindrome', 'url': 'https://leetcode.com/problems/longest-palindrome/', 'similarity': 'similar'},
        solution='''### Intuition
The longest palindrome uses every pair of equal letters, plus at most one unpaired letter in the centre. Lexicographic minimality then only depends on the order of the left half and on which letter is placed in the centre.

### Approach
1. Count letter frequencies.
2. Build the left half by writing each letter in alphabetical order floor(count / 2) times.
3. The centre is the smallest letter whose count is odd (empty if none).
4. Return left + centre + reverse(left).

### Why it works
Maximum length: every pair contributes 2 characters and one centre can add 1, which cannot be improved. For minimality, the left half is the lexicographically smallest arrangement of the multiset of pairs (sorted); the right half is forced by symmetry. Different centre choices change the character at position len(left), so the smallest odd letter wins. Brute force over all sub-multisets agrees on 100 random strings.

### Complexity
O(|S| + 26) time and O(|S|) space for the output.

### Python solution
```python
from collections import Counter

def solve(s):
    c = Counter(s)
    half = ''.join(ch * (c[ch] // 2) for ch in sorted(c))
    odd = [ch for ch in sorted(c) if c[ch] % 2]
    mid = odd[0] if odd else ''
    return half + mid + half[::-1]
```

### Dry run
"adskassda": a3 d2 s3 k1. half = "a" + "d" + "s" = "ads"; odd letters a, k, s so mid = "a"; result "ads" + "a" + "sda" = "adsasda".

### Edge cases & pitfalls
- All letters distinct: the answer is the single smallest letter.
- Do not use an even-count letter as the centre; it is already consumed by pairs.
- Build strings with join, not repeated concatenation, for 10^5 length.''')

    Q('maq-family-females', 'Number of females at a family party',
      'A party consists of grandmother, father, mother, four sons and their wives and one son and two daughters to each of the sons. How many females are there in all?',
      ['24', '18', '14', '16'], '14',
      'Females: grandmother 1, mother 1, four daughters-in-law 4, and 2 daughters for each of 4 sons = 8. Total 14.',
      'Count only the females. Grandmother (1) + mother (1) + 4 wives (4) + 4 sons x 2 daughters (8) = 14. The grandsons are males and are not counted.',
      w(129), 'logical', wrong='24 and 18 include the grandsons or the males; 16 forgets one of the groups.', traps='- Counting the sons\' sons.')
    Q('maq-kilogram-quintal', 'Analogy: Kilogram : Quintal :: Paisa : ?',
      'Kilogram is related to Quintal in the same way as Paisa is related to ...', ['Coin', 'Money', 'Rupee', 'Wealth'], 'Rupee',
      'A kilogram is a smaller unit that makes up a quintal (100 kg), just as a paisa is a smaller unit of a rupee.', 'Kilogram is a smaller unit and a quintal the larger unit that contains it. Paisa is the smaller unit and rupee the larger unit.',
      w(130), 'verbal', confidence='medium', notes='The correct option text is read from OCR; the layout of options is partly cropped.')
    Q('maq-direction-kate-denise', 'Direction of Kate from Denise',
      'Kate lives 55 km northeast to Mark while Robert lives 35 km southeast to him. Denise lives 55 km southeast to Robert. In which direction does Kate live with respect to Denise?',
      ['Northeast', 'Southwest', 'Northwest', 'Southeast'], 'Northwest',
      'Denise is 35 + 55 = 90 km southeast of Mark along the same line, while Kate is 55 km northeast of Mark. From Denise, Kate lies north-west.',
      'Put Mark at the origin. Kate is at 55 NE; Robert at 35 SE; Denise is another 55 SE of Robert, so Denise is at 90 SE. The vector from Denise to Kate is 55 NE - 90 SE = (-35, 145) in (east, north) units: mostly north and a little west, i.e. the north-west quadrant. Among the options this is Northwest.',
      w(133), 'logical', confidence='medium', notes='With exact axes the bearing is about 14 degrees west of north; the nearest offered direction is Northwest.')
    Q('maq-pets-least', 'Who has the least number of pets',
      'Lisa, Bob, and Ben have cats. Mike has a dog and a guinea pig. Bob also has a rabbit. Mike just bought a bird for Ben. Paul has a dog and some goldfish. Who has the least number of pets?',
      ['Lisa', 'Paul', 'Ben', 'Bob'], 'Lisa',
      'Lisa has only a cat (1). Bob has a cat and a rabbit (2), Ben a cat and a bird (2), and Paul a dog and goldfish (at least 2).', 'Count each person: Lisa 1; Bob 2; Ben 2 (cat + bird from Mike); Paul 2 or more. The least is Lisa. Mike\'s bird goes to Ben, not Mike.',
      w(134), 'logical', traps='- Giving the bird to Mike instead of Ben.')
    Q('maq-mirror-clock-930', 'Actual time when the mirror shows 9:30',
      'Looking into a mirror, the clock shows 9:30 as the time. The actual time is', ['4:30', '9:00', '3:30', '2:30'], '2:30',
      'Actual time = 12:00 - mirror time = 2:30.', 'For a mirror image of a clock the actual time is 11:60 minus the shown time: 11:60 - 9:30 = 2:30.',
      w(138), 'logical', fast='Subtract the shown time from 12:00.', wrong='4:30 and 3:30 come from subtracting from other hours.')
    Q('maq-code-moon-noon', 'Letter coding: MOON = LMLI so NOON = ?',
      'If the code for MOON is LMLI in a certain language, then what is the code for NOON?', ['MJVL', 'KJVL', 'MMLI', 'MLVN'], 'MMLI',
      'Shifts per position are -1, -2, -3, -5: M-1 = L, O-2 = M, O-3 = L, N-5 = I. NOON gives N-1 = M, O-2 = M, O-3 = L, N-5 = I = MMLI.',
      'Compare MOON with LMLI position by position: M->L (-1), O->M (-2), O->L (-3), N->I (-5). Apply the same shifts to NOON: N->M, O->M, O->L, N->I, giving MMLI.',
      w(140), 'logical', confidence='medium', notes='The shift pattern -1, -2, -3, -5 is inferred from the single example, but it reproduces an offered option.')
    Q('maq-dictionary-in-words', 'Dictionary order: Inhabit, Ingenious, Inherit, Influence, Infatuation',
      'Arrange the words as per order in the dictionary: 1. Inhabit 2. Ingenious 3. Inherit 4. Influence 5. Infatuation',
      ['4, 5, 2, 1, 3', '1, 2, 3, 4, 5', '5, 4, 2, 1, 3', '5, 4, 1, 2, 3'], '5, 4, 2, 1, 3',
      'Compare the letters after "In": f-a (Infatuation), f-l (Influence), g (Ingenious), h-a (Inhabit), h-e (Inherit).', 'All words start with "In". Next letters: f, f, g, h, h. Between the two f-words: "Infa" < "Infl". Between the two h-words: "Inha" < "Inhe". Order: Infatuation (5), Influence (4), Ingenious (2), Inhabit (1), Inherit (3).',
      w(146), 'verbal')
    Q('maq-dictionary-dis', 'Dictionary order of Dis- words',
      'Arrange the following words as they appear in the dictionary: 1. Dissipate 2. Dissuade 3. Disseminate 4. Distract 5. Dissociate 6. Disect',
      ['3, 6, 1, 2, 5, 4', '6, 3, 1, 5, 2, 4', '4, 6, 3, 1, 5, 2', '1, 6, 3, 2, 4, 5'], '6, 3, 1, 5, 2, 4',
      'Sorted: Disect, Disseminate, Dissipate, Dissociate, Dissuade, Distract.', 'After "Dis": e (Disect) < s-s-e (Disseminate) < s-s-i (Dissipate) < s-s-o (Dissociate) < s-s-u (Dissuade) < t (Distract). That is 6, 3, 1, 5, 2, 4.',
      w(166), 'verbal')
    Q('maq-sequence-book-words', 'Most appropriate sequence: Book, Chapter, Paragraph, Sentence, Words, Letter',
      'Choose the most appropriate sequence (largest to smallest): 1. Sentence 2. Chapter 3. Letter 4. Book 5. Words 6. Paragraph',
      ['4, 6, 2, 5, 1, 3', '4, 6, 1, 2, 3, 5', '4, 2, 1, 6, 5, 3', '4, 2, 6, 1, 5, 3'], '4, 2, 6, 1, 5, 3',
      'A book contains chapters, chapters contain paragraphs, paragraphs contain sentences, sentences contain words, words contain letters.', 'Order of containment: Book (4) > Chapter (2) > Paragraph (6) > Sentence (1) > Words (5) > Letter (3).',
      w(159), 'logical', confidence='medium', notes='The option wording is read from OCR.')
    Q('maq-birders-only-one', 'Birders who wanted to see only one bird',
      'Out of the 75 birders, 15 wanted to see only sunbird, 10 wanted to see only flycatcher, 12 wanted to see both sunbird and nuthatch, 15 wanted to see only bee-eater, 13 wanted to see both sunbird and bee-eater, 5 wanted to see both flycatcher and nuthatch and the remaining wanted to see only nuthatch. How many birders wanted to see only one bird?',
      ['40', '50', '30', '45'], '45',
      'Birders accounted for: 15 + 10 + 12 + 15 + 13 + 5 = 70, so only-nuthatch = 5. Only one bird: 15 + 10 + 15 + 5 = 45.', 'Sum the listed groups: 15 + 10 + 12 + 15 + 13 + 5 = 70. The remaining 75 - 70 = 5 want only nuthatch. Those who want just one bird are the "only" groups: sunbird 15, flycatcher 10, bee-eater 15, nuthatch 5 = 45.',
      w(169), 'quant', wrong='40, 50 and 30 miscount the "only nuthatch" group or include the combined groups.')
    Q('maq-bench-seating-c', 'Seven students on three benches: who sits with C',
      'In a class there are seven students (boys and girls) A, B, C, D, E, F and G. They sit on three benches I, II and III such that at least two students sit on each bench and at least one girl on each bench. C, who is a girl, does not sit with A, E and D. F, the boy, sits with only B. A sits on bench I with his best friends. G sits on bench III. E is the brother of C. Who sits with C?',
      ['E', 'G', 'B', 'D'], 'G',
      'F and B alone form a bench of two, which cannot be bench I (A) or III (G), so it is bench II. C cannot sit with A, E or D, so C is on bench III with G. A, E and D take bench I.',
      '''1. F sits with only B: they form a two-person bench. A is on bench I and G on bench III, so F and B are on bench II.
2. C must avoid A, E and D. The only bench left without them is bench III, with G.
3. A, D and E share bench I. Each bench has at least a girl: C on III, and the others fit.''',
      w(165), 'puzzles')
    Q('maq-trade-deficit-net', 'Net total of a cumulative trade deficit/surplus chart',
      'Cumulative Trade Deficit/Surplus of Countries for 2006-2007 (all figures in Yen). The total of the first three deficit countries = 3594.3, of the next five deficit countries = 2588.5, and of the last five deficit countries = 334.2 (from the chart). Surplus countries: Sri Lanka 305.7, UAE 427.7, USA 462, UK 665. The net total deficit/surplus is equal to?',
      ['None of these', '4656.6 surplus', '4656.6 deficit', '3836.5 deficit'], '4656.6 deficit',
      'Total deficit = 3594.3 + 2588.5 + 334.2 = 6517.0. Total surplus = 305.7 + 427.7 + 462 + 665 = 1860.4. Net = 6517.0 - 1860.4 = 4656.6 deficit.', 'Add the deficits and the surpluses separately and subtract: 6517.0 - 1860.4 = 4656.6, a net deficit.',
      w(167), 'data-interpretation', confidence='low',
      notes='The last-five-deficit total was cut off in the stem; 334.2 is back-computed from the offered answer and the chart labels (one label could not be read reliably).')
    Q('maq-cpp-encapsulation', 'C++ class Talent: encapsulation',
      'In C++, which of these describes the following class: class Talent { private: double temp; double tempF(double); public: Talent(); ~Talent(); setTemp(double); double getTemp(); double getTempF(); };',
      ['It is not a true encapsulation.', 'It is a true interface', 'It is a true encapsulation.', 'None'], 'It is a true encapsulation.',
      'Data (temp) and the helper tempF are private and only reachable through public methods, bundling data with behaviour: encapsulation.', 'Encapsulation means hiding data and exposing a controlled public interface. The data member and helper are private; the public methods set and get values. An interface (pure abstract class) would have only pure virtual functions.',
      w(170), 'oop', section='cs', confidence='medium', wrong='It is not an interface because it has data members and implementations.')
    skip(M, w(136)[0], 'mirror-image clock item with unclear premise')
    skip(M, w(158)[0], 'options only, no stem')
    skip(M, w(160)[0], 'figure item (mirror image), image only')
    skip(M, w(161)[0], 'figure item (water image), image only')
    skip(M, w(162)[0], 'Venn-diagram figure item, image only')
    skip(M, w(163)[0], 'seating around a square table, ambiguous adjacency definition')
    Q('maq-marbles-pigeonhole', 'Marbles in the dark: draws to guarantee two of one colour',
      'Alice has a box that contains 12 marbles, consisting of 4 green, 4 yellow and 4 blue ones. If Alice was in a dark room and had to pick them at random, how many marbles must she take out so as to pick out at least 2 of one color?',
      ['8', '3', '4', '9'], '4',
      'Worst case: one marble of each of the three colours (3), so the 4th marble must repeat a colour.', 'Pigeonhole principle: with 3 colours, 3 marbles can all be different, but a 4th must match one of them, giving 2 of the same colour.',
      w(164), 'quant', wrong='3 does not guarantee a pair; 8 and 9 are far more than needed.', traps='- Using the count of marbles instead of the number of colours.')
    skip(M, w(168)[0], 'dot-placement figure item, image only')
    skip(M, w(171)[0], 'thread handling question, ambiguous options')
