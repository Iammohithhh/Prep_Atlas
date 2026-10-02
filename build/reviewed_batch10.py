"""Oracle final photo continuations; diagrams represented by their data."""


def extend(add, merge, skip):
    groups={
        'oracle-nested-uri':['0062','0063'], 'oracle-bgp-layer':['0064'], 'oracle-tcp-order':['0065'],
        'oracle-past-perfect':['0070'], 'oracle-three-ants':['0071'], 'oracle-clock-overlap':['0072'],
        'oracle-two-eggs':['0073'], 'oracle-nine-coins':['0074'], 'oracle-cyclical-sequence':['0080'],
        'oracle-previous-year-day':['0081'], 'oracle-weaned-off':['0085','0086','0087'],
    }
    for key, suffixes in groups.items():
        merge(key,'Oracle',['IMG-20240915-WA'+s+'.jpg' for s in suffixes])
    add('oracle-power-mod','Oracle','Remainder of 2000 to the power 1000 modulo 13',
        'What is the remainder when 2000¹⁰⁰⁰ is divided by 13?', '3',
        '2000≡−2 (mod 13). Since 2¹²≡1 (mod 13) and 1000≡4 (mod 12), (−2)¹⁰⁰⁰≡2⁴≡16≡3 (mod 13). Repeated modular squaring also computes this without constructing the large power.',
        options=['3','4','8','11'], sources=['IMG-20240913-WA0006.jpg','IMG-20240915-WA0075.jpg'], notes='The exponent is clearly raised in the repeated photo’s body text; the source heading loses the superscript formatting.')
    add('oracle-phone-customers','Oracle','Recover July phone customers from August additions',
        'Only Hington and Euphore phones are included. Counts and additions are in millions.\n\n| Month | Hington total | Euphore total | Hington additions | Euphore v1 additions | Euphore v2 additions |\n|---|---:|---:|---:|---:|---:|\n| Aug 2012 | 46.18 | 47.28 | 0.36 | 1.24 | 0.60 |\n| Sep 2012 | 47.34 | 48.91 | 1.16 | 1.08 | 0.80 |\n| Oct 2012 | 49.32 | 49.27 | 1.98 | 0.84 | 0.48 |\n\nAssuming August additions are net new users and each person is counted once, what is the combined total for July 2012?', 'None of these',
        'Subtract the August additions from the August total: 46.18+47.28−0.36−1.24−0.60=91.26 million. None of the listed numeric choices matches. July can be derived from the August row under the stated net-addition assumption. Later Euphore totals do not reconcile with later additions, so they cannot establish consistent month-to-month growth without additional churn information.',
        topic='data-interpretation', options=['91.21 million','6.87 million','98.23 million','None of these'], sources=['IMG-20240913-WA0004.jpg','IMG-20240913-WA0007.jpg','IMG-20240913-WA0008.jpg','IMG-20240913-WA0010.jpg']+[f'IMG-20240915-WA00{i}.jpg' for i in range(76,80)], notes='The chart is transcribed as a table. User overlap/churn is not specified in the source; the standard exercise assumptions are made explicit.')
    add('oracle-pollution-ranks','Oracle','Cities whose ranking changes at most once',
        'Rank seven cities by ascending pollution index separately in 2006, 2007 and 2008, with the least polluted ranked first. How many cities change rank at most once across the two year-to-year transitions?\n\n| City | 2006 | 2007 | 2008 |\n|---|---:|---:|---:|\n| A | 13 | 21 | 24 |\n| B | 15 | 17 | 11 |\n| C | 34 | 35 | 29 |\n| D | 56 | 57 | 56 |\n| E | 57 | 45 | 45 |\n| F | 12 | 12 | 13 |\n| G | 11 | 15 | 17 |', '4',
        'Ascending orders are G,F,A,B,C,D,E in 2006; F,G,B,A,C,E,D in 2007; and B,F,G,A,C,E,D in 2008. Rank sequences: A=(3,4,4), B=(4,3,1), C=(5,5,5), D=(6,7,7), E=(7,6,6), F=(2,1,2), G=(1,2,3). A,C,D,E change at most once, so there are four. The source chart also includes 2009/2010, but the question’s requested interval ends in 2008.',
        topic='data-interpretation', options=['1','2','3','4'], sources=['IMG-20240913-WA0001.jpg','IMG-20240913-WA0002.jpg','IMG-20240915-WA0089.jpg','IMG-20240915-WA0090.jpg'])
    add('oracle-count-subsequence','Oracle','Count appearances of a three-letter subsequence',
        'Given uppercase strings s1 and s2, where s1 has exactly three characters, count how many index triples i<j<k in s2 spell s1. Different position triples count separately, even if they produce the same text. Return the count.', None,
        'Maintain counts of matched prefixes of lengths 1,2,3. For each character c, first add count2 to count3 if c=s1[2], then add count1 to count2 if c=s1[1], then increment count1 if c=s1[0]. Updating in descending order prevents reusing one position twice when s1 contains repeated letters. Equivalently initialise dp[0]=1 and update dp[3…1] backwards. O(len(s2)) time and O(1) space because the target length is fixed. The source requests a long integer, with no modulus; use Python integers or a sufficiently wide type.',
        section='dsa', topic='dp', type='coding', function_signature='getSubsequenceCount(s1, s2)', sources=['WhatsApp Image 2024-08-03 at 16.28.18_61a277d0.jpg','WhatsApp Image 2024-08-03 at 16.28.20_e7198c4c.jpg','WhatsApp Image 2024-08-03 at 16.28.28_438affba.jpg'], constraints='len(s1)=3; s1 and s2 contain uppercase English letters. The photographed exponent in s2’s upper bound is unclear.',
        examples=[{'input':'s1 = "ABC", s2 = "ABCBABC"','output':'5'},{'input':'s1 = "HRW", s2 = "HERHRWS"','output':'3'}])
    add('oracle-ongoing-tense','Oracle','Tense for an ongoing condition over three years',
        'Improve the verb phrase: “My father is suffering from diabetes for the past three years.”', None,
        'For a condition that began in the past and continues now, “has been suffering” is the expected present-perfect-continuous replacement. “Has suffered” is also grammatical for a state continuing over that period, though it shifts emphasis. Thus the source options do not make only one form grammatically possible. “Is suffer” is ungrammatical and leaving the original tense does not express the duration correctly.',
        topic='verbal', type='subjective', sources=['IMG-20240915-WA0066.jpg','IMG-20240915-WA0069.jpg'], notes='The source’s has been suffering and has suffered options can both fit. Its unrelated number-wheel image is omitted from this language prompt.')
    for s, reason in [('0067','sentence question contains unrelated number wheel'),('0068','its/it’s and will/shall alternatives need closer grammar review'),('0082','historical reading passage has ambiguous brevity inference'),('0083','reading inference has two plausible brevity benefits'),('0084','reading inference has two plausible brevity benefits'),('0088','animal survival model is unclear')]:
        skip('Oracle','IMG-20240915-WA'+s+'.jpg',reason)
    skip('Oracle','WhatsApp Image 2024-08-23 at 14.48.06_5038b95d.jpg','NoSQL classification needs full verification')
