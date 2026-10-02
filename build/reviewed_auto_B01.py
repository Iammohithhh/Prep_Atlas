"""ZS Associates (Mercer-Mettl cognitive test): critical thinking and verbal ability."""


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

    def wa(n):
        return f'IMG-20240805-WA00{n}.jpg'

    # ---------------- Critical thinking ----------------
    add('zs-ct-bureaucracy', Z, 'Inference from the bureaucratisation of the ruling process',
        'The greatest danger to democracy is the increasing bureaucratization of the ruling process. As bureaucracy takes control of virtually everything in governance, it becomes less accountable to both the ruling party and the legislature. There is a chance that democracy will become technocracy.\n\nWhich of the given statements can be inferred from the above information?',
        'The accountability to both the ruling party and the legislature is key to democracy.',
        'The passage links growing bureaucratic control to lost accountability and then to democracy turning into technocracy. That makes accountability to the elected bodies a condition for democracy, the only option that follows without adding new claims.',
        section='aptitude', topic='logical', type='mcq', confidence='medium', sources=[wa(52)],
        options=['Democracy may turn into autocracy if bureaucrats are not controlled.',
                 'Bureaucracy should be controlled to ensure its accountability to both the ruling party and the legislature.',
                 'Technocracy is not better than democracy.',
                 'The accountability to both the ruling party and the legislature is key to democracy.'],
        notes='The last option is cropped in the photo after "is key to de"; reconstructed as "democracy".',
        solution=S('''An inference must follow from the passage using only what it says.
1. Passage chain: more bureaucratisation -> bureaucracy becomes less accountable to the ruling party and legislature -> democracy may become technocracy.
2. So loss of accountability is what drives democracy towards technocracy. Reversing this, accountability to the elected bodies is what keeps a system democratic.
3. Option 4 states exactly this and adds no new fact.

**Answer: The accountability to both the ruling party and the legislature is key to democracy.**''',
                  wrong='''- "Democracy may turn into autocracy": the passage says technocracy, not autocracy.
- "Bureaucracy should be controlled...": a recommendation ("should"), not something stated or implied as fact.
- "Technocracy is not better than democracy": the passage never compares the two.''',
                  fast='Look for the option that restates the passage link (accountability and democracy) without a new word such as "autocracy", "should" or "better".',
                  traps='- Mixing up an inference with a recommendation.\n- Swapping one word (autocracy for technocracy).'))
    add('zs-ct-skill-obsolescence', Z, 'Reducing skill obsolescence in IT companies',
        'Most IT organizations face a unique dilemma. They find that with every trend in the industry and in the market, their workers\' knowledge and skills become obsolete. New skills and knowledge are needed every six months in order to keep up with the demands of the consumer and competition in the market.\n\nWhich of the following options would help companies reduce the threat they face from this particular obsolescence?',
        'Companies need to develop a training schedule that ensures frequent and necessary training for its employees.',
        'Skills go stale every six months, so the remedy must be frequent, needed training. A fixed two-year cycle is too slow, a bigger budget does not guarantee frequency, and a survey only diagnoses gaps without fixing them.',
        section='aptitude', topic='logical', type='mcq', confidence='medium', sources=[wa(53), wa(63)],
        options=['Companies need to develop a skills survey and administer this frequently to understand the skill gaps that prevail among employees.',
                 'Companies need to develop a training schedule that ensures frequent and necessary training for its employees.',
                 'Companies increase their training budget to allow for different training techniques.',
                 'Companies develop a training schedule that makes it compulsory for employees to be trained every 2 years.'],
        solution=S('''The problem is that skills expire about every six months. A good solution must act on employees\' skills at roughly that frequency.
1. Option 4: training every 2 years is four times slower than the obsolescence cycle, so skills would still lapse.
2. Option 3: more money or techniques says nothing about how often people are trained.
3. Option 1: a survey identifies gaps but is not itself training, so the threat remains.
4. Option 2: frequent and necessary training matches the six-month cycle and directly fixes the gap.

**Answer: Companies need to develop a training schedule that ensures frequent and necessary training for its employees.**''',
                  wrong='- Option 1 only diagnoses; option 3 changes budget not frequency; option 4 is too infrequent (2 years against 6 months).',
                  fast='Match the frequency in the stem (every six months) with the frequency in the option.',
                  traps='- Choosing the survey option because it sounds analytical; it does not remove the threat itself.'))
    alias('b05_zs_fractal-010', Z, ['IMG-20240805-WA0054.jpg', 'ZS  .pdf'])
    alias('b05_zs_fractal-012', Z, ['IMG-20240805-WA0055.jpg'])
    add('zs-ct-reality-shows', Z, 'Point of disagreement in a debate on reality shows',
        'Mr. A: The reality shows on television are affecting the moral fabric of our society. These shows present immoral behaviour as if it is the norm of society. People who watch these programs start believing that the immoral behaviour depicted in the programs is the norm of society.\n\nMr. B: The reality shows show what we wish to see. So the decline in our moral values is due to many other forces acting on society\'s moral fabric. Any kind of censorship against these programs would be an action against the fundamental right of speech and expression. We should let the viewers decide what they want to see.\n\nMr. A and Mr. B disagree about which of the given statements?',
        'The decline in moral values is due to reality shows.',
        'A blames reality shows for the moral decline; B says the decline is due to many other forces. They disagree on whether reality shows cause the decline. A never says censorship is required, and B alone says content follows viewer wishes.',
        section='aptitude', topic='logical', type='mcq', sources=[wa(56), P],
        options=['It is wrong not to let the viewers decide what they want to see.', 'Censorship is required to insulate the right values in the society.', 'The content of reality shows is guided by what viewers wish to see.', 'The decline in moral values is due to reality shows.'],
        solution=S('''Find the claim where one speaker affirms and the other denies.
1. Option 4: A says shows damage moral fabric and shape beliefs; B says the decline is due to many other forces. Direct conflict.
2. Option 1: only B states it; A does not say viewers should not decide.
3. Option 2: A never calls for censorship; B opposes it, but there is no A-side statement to disagree with.
4. Option 3: only B states it; A does not deny it.

**Answer: The decline in moral values is due to reality shows.**''',
                  wrong='Options 1 to 3 are each stated by only one speaker; the other speaker is silent, so there is no disagreement.',
                  fast='A disagreement needs both speakers to take opposite positions on the same claim, so check each option against both speakers.',
                  traps='- Picking the censorship option because B mentions it, even though A never advocates it.'))
    add('zs-ct-food-grains', Z, 'Assumption in the food-grain price argument',
        'One of the poll promises of the government in office was to control black marketing and hoarding of food grains. However, it seems that the government\'s initiative to control black marketing and hoarding failed in 2005. If the initiative had been successful, the price of food grains would not have gone up so much in 2005.\n\nWhich of the given is an assumption made in the above argument?',
        'A drop in the agricultural yield was not the reason for the rise in the price of food grains.',
        'The argument infers that the hoarding control failed because prices rose. This is valid only if no other cause, such as a poor harvest, pushed prices up. So the assumption is that a drop in yield was not the reason.',
        section='aptitude', topic='logical', type='mcq', sources=[wa(57), wa(58), wa(62)],
        options=['The supply of food grains dropped substantially in 2005.', 'A drop in the agricultural yield was not the reason for the rise in the price of food grains.', 'The price of food grains in the international market remained more or less stable.', 'Prices of vegetables and meat products were stable.'],
        solution=S('''1. Conclusion: the initiative failed. Evidence: grain prices rose a lot in 2005.
2. The gap: prices could have risen for other reasons (poor harvest, imports). The argument must assume those alternatives did not cause the rise.
3. Option 2 rules out the main alternative cause (lower yield). Negation test: if yield did drop, the price rise may not show the initiative failed, and the argument breaks.
4. Option 1 contradicts the argument; options 3 and 4 concern other markets and commodities.

**Answer: A drop in the agricultural yield was not the reason for the rise in the price of food grains.**''',
                  wrong='- Option 1 supplies an alternative cause, which weakens the argument.\n- Option 3 is about international prices, a weaker link than domestic supply.\n- Option 4 concerns other food items.',
                  fast='In cause-effect arguments the hidden assumption is usually "no other cause".',
                  traps='- Option 3 also looks like a "no other cause" statement, but option 2 targets the direct domestic supply cause.'))
    alias('b05_zs_fractal-015', Z, ['IMG-20240805-WA0059.jpg', 'IMG-20240805-WA0060.jpg'])
    add('zs-ct-education', Z, 'What cannot be inferred about mushrooming educational institutions',
        'Mushrooming of educational institutions has led to a downfall in the levels of quality. However, it has provided an avenue for many students to get a formal education.\n\nWhich of the following CANNOT be inferred from the information given?',
        'The lesser number of educational institutions will help in maintaining the quality of education.',
        'The passage links the growth in institutions to lower quality and to wider access. It says nothing about what would happen with fewer institutions, so that option cannot be inferred.',
        section='aptitude', topic='logical', type='mcq', sources=[wa(61)],
        options=['Not all educational institutions provide quality education.', 'The lesser number of educational institutions will help in maintaining the quality of education.', 'Educational institutions provide formal education.', 'Many students enrol for a formal education irrespective of the quality of the institution.'],
        notes='The last option is cropped in the photo; completed from context.',
        solution=S('''1. "Not all institutions provide quality education": quality has fallen, so some institutions are poor. Inferable.
2. "Educational institutions provide formal education": directly stated.
3. "Many students enrol irrespective of quality": the institutions gave an avenue to many students despite lower quality. Inferable.
4. "Fewer institutions will maintain quality": a counterfactual about a different situation. The passage does not say that reducing institutions restores quality.

**Answer: The lesser number of educational institutions will help in maintaining the quality of education.**''',
                  wrong='The other three follow directly from the two sentences.',
                  fast='In a CANNOT-be-inferred question, the answer is usually the option proposing a remedy or prediction not in the text.',
                  traps='- Treating a plausible remedy as an inference.'))
    add('zs-ct-uv-rays', Z, 'Conclusion best supported about ultraviolet exposure',
        'Prolonged exposure to ultraviolet rays increases the chances of developing skin cancer. Television screens, computer monitors, and water purifiers also emit ultraviolet rays.\n\nWhich of the given conclusions is best supported by the above statements?',
        'Certain devices in our day-to-day life can cause skin cancer.',
        'UV exposure raises skin-cancer risk and everyday devices emit UV, so such devices can contribute to skin cancer. The other options claim too much (primary cause, ozone thinning, a necessity).',
        section='aptitude', topic='logical', type='mcq', sources=[P],
        options=['Prolonged exposure to ultraviolet rays is the primary cause of skin cancer.', 'Television screens, computer monitors, and water purifiers result in the thinning of the Ozone layer.', 'Certain devices in our day-to-day life can cause skin cancer.', 'A person, suffering from skin cancer, must be exposed to ultraviolet rays from television screens, computer monitors, and water purifiers.'],
        solution=S('''1. Premise A: prolonged UV exposure increases the chance of skin cancer.
2. Premise B: TVs, monitors and water purifiers emit UV.
3. Combine: those devices can (with prolonged exposure) raise the chance of skin cancer, i.e. they can cause it.

**Answer: Certain devices in our day-to-day life can cause skin cancer.**''',
                  wrong='- "Primary cause": "increases the chances" does not mean primary.\n- Ozone thinning: not mentioned.\n- "Must be exposed": reverses the direction (cancer need not come from these devices).',
                  fast='Prefer the modest "can/may" conclusion over absolute words such as primary or must.',
                  traps='- Over-strong conclusions.'))
    add('zs-ct-writers-block', Z, 'Strengthening a statement about writer\'s block',
        'To overcome \'writer\'s block\', a writer needs to unwind and restart the entire thinking process so that the points that are stuck are released.\n\nWhich of the given options strengthens the statement above?',
        'Unwinding leads to fresh thoughts.',
        'The statement claims unwinding and restarting frees stuck points. Evidence that unwinding produces fresh thoughts supports why the method works.',
        section='aptitude', topic='logical', type='mcq', confidence='medium', sources=[P],
        options=['Every writer goes through a \'writer\'s block\'.', 'Unwinding leads to fresh thoughts.', 'New and fresh thoughts are required by all writers.', 'The thinking process needs to be restarted even if a writer doesn\'t face a block.'],
        notes='Read from a low-resolution page of a compiled PDF.',
        solution=S('''A strengthener supports the claim that unwinding fixes writer\'s block.
1. Option 1 says blocks are common; it does not show the remedy works.
2. Option 2 gives the mechanism: unwinding produces fresh thoughts, which would release stuck points.
3. Option 3 is about need, not about the method.
4. Option 4 extends the process to cases without a block, which is irrelevant to the claim.

**Answer: Unwinding leads to fresh thoughts.**''',
                  wrong='Options 1, 3 and 4 do not connect unwinding to relieving the block.',
                  fast='Choose the option that supplies the mechanism behind the stated remedy.',
                  traps='- Picking a statement that is merely related to writing.'))
    add('zs-ct-mobile-phones', Z, 'Assumption in the argument about mobile phones',
        'The current era is the era of communication and we are getting more and more dependent on mobile phones. However, there is an inherent problem in the use of mobile phones and hence they should be discontinued. According to a renowned psychiatrist, "Mobile phones will be a major cause of ailments in the times to come for a majority of the population."\n\nIf the above statements are true, then which of the following is an assumption made while making these statements?',
        'The disadvantages of using mobile phones outweigh their benefits.',
        'The argument jumps from "mobile phones cause ailments" to "they should be discontinued". That jump needs the unstated premise that the harms outweigh the benefits.',
        section='aptitude', topic='logical', type='mcq', confidence='medium', sources=[P],
        options=['Most people are spending significantly more hours on their mobile phones than on sleeping.', 'Mobile phone companies are recording increasingly higher revenues.', 'Stress is caused due to excessive use of mobile phones.', 'The disadvantages of using mobile phones outweigh their benefits.'],
        notes='Read from a low-resolution page of a compiled PDF.',
        solution=S('''1. Claim: phones have a problem (ailments), therefore discontinue them.
2. Discontinuing something useful is justified only if the cost exceeds the benefit. The passage even admits that people increasingly depend on phones.
3. So the necessary assumption is that disadvantages outweigh benefits (option 4).
4. Options 1 and 2 are unrelated statistics; option 3 names one specific ailment, but the conclusion needs the overall cost-benefit comparison.

**Answer: The disadvantages of using mobile phones outweigh their benefits.**''',
                  wrong='Options 1 to 3 give side facts and are not needed for "therefore discontinue".',
                  fast='When an argument jumps from "is harmful" to "should be stopped", the missing premise is "harm outweighs benefit".',
                  traps='- Picking an option that restates an effect of phone usage.'))
    alias('b05_zs_fractal-014', Z, ['ZS  .pdf'])
    alias('b05_zs_fractal-016', Z, ['ZS  .pdf'])
    add('zs-va-para-tea', Z, 'Sentence ordering: Sundays and tea tasting',
        'Arrange the following sentences in a logical order to construct a coherent paragraph:\n\n(A) finishing the chores left over on the weekdays and spending time with family and friends.\n(B) Sundays are meant for leisure, where one sets aside their worries,\n(C) Like any tea connoisseur, he believes that the true taste of tea can only be discovered with time.\n(D) One of the things that Paul loves to do during the weekend is discover the many different varieties of teas and lay out a tasting table.',
        'BADC',
        'B opens with the general idea (Sundays are for leisure). A continues the same sentence ("where one sets aside worries, finishing the chores..."). D then introduces Paul and his weekend habit. C adds a comment about him as a tea connoisseur, so the order is B A D C.',
        section='aptitude', topic='verbal', type='mcq', sources=[wa(64), wa(65), P],
        options=['ACBD', 'CADB', 'BADC', 'ABCD'],
        notes='Several other sentence-ordering items from the same test (healthcare, ocean warming, constructive dialogue) follow the same pattern: find the opener, chain the sentence fragments, use signal words.',
        solution=S('''1. B is a general statement and a sentence start ("Sundays are meant for leisure, where one sets aside their worries,").
2. A starts with a lowercase gerund and continues B\'s sentence: "...finishing the chores left over... and spending time with family and friends". So B then A is a fixed pair.
3. D introduces the specific person (Paul) and a weekend activity.
4. C ("Like any tea connoisseur, he...") refers to "he" and tea, so it must follow D.
Order: B A D C.

**Answer: BADC**''',
                  wrong='ACBD and ABCD start with A, a fragment that cannot begin a paragraph; CADB starts with "he" before Paul is introduced.',
                  fast='Find the sentence fragments that must pair (B then A), find the introduction (general before specific, name before pronoun) and test the options.',
                  traps='- Starting with a sentence that begins with a pronoun.'))
    add('zs-va-fill-climber', Z, 'Fill in the blank: the mountain climber\'s spirit',
        'Fill in the blank(s) with the correct word(s).\n\nThe mountain climber\'s ______ spirit drove him to attempt the most treacherous peaks.',
        'fearless', 'A spirit that drives someone to attempt treacherous peaks must be bold, so "fearless" fits. Critical, minimal and hostile do not describe what would make someone attempt dangerous climbs.',
        section='aptitude', topic='verbal', type='mcq', sources=[wa(66)], options=['critical', 'fearless', 'minimal', 'hostile'],
        solution=S('''The sentence says the spirit "drove him to attempt the most treacherous peaks". The adjective must show a bold, daring character.
- critical: faultfinding, does not fit.
- fearless: bold and daring, fits.
- minimal: too little, would not drive him.
- hostile: aggressive towards others, not relevant to climbing.

**Answer: fearless**''',
                  wrong='critical, minimal and hostile fail the cause-and-effect meaning.', fast='Predict the word first (bold, adventurous) and then look for it.', traps='- Choosing "hostile" because treacherous sounds negative.'))
    add('zs-va-error-litmus', Z, 'Identify the error: litmus test of the depth',
        'Identify the error in the following sentence:\n\nBeing a kind, gentle soul is like a litmus test of the depth to the personality.',
        'to the', 'The phrase "depth of the personality" needs "of", not "to". The other segments (Being a, soul is, test of the) are fine.',
        section='aptitude', topic='verbal', type='mcq', sources=[wa(67), P], options=['Being a', 'soul is', 'test of the', 'to the'],
        solution=S('''Break the sentence into the four segments offered.
1. "Being a kind, gentle soul" is a proper gerund phrase used as subject.
2. "soul is like a litmus test" agrees in number.
3. "test of the depth" is a correct collocation (a test of something).
4. "depth to the personality" is wrong: depth is of something, so it should be "depth of the personality".

**Answer: to the**''',
                  wrong='The other three segments are grammatically sound.', fast='Check prepositions first; they are the most common injected error.', traps='- Flagging "soul is" for agreement; the subject is "Being a kind, gentle soul", which is singular.'))
    add('zs-va-sentence-there', Z, 'Sentence correction: first went theirs',
        'Choose the option that correctly rephrases the underlined part of the sentence. Mark "No error" if there is none.\n\nDid you know about the accident when you first <u>went theirs</u>?',
        'went there', '"Theirs" is a possessive pronoun and cannot express a place. The adverb "there" is needed: "when you first went there".',
        section='aptitude', topic='verbal', type='mcq', sources=[wa(68), P], options=['go there', 'gone there?', 'went there?', 'went their.', 'No error'],
        solution=S('''1. The underlined "went theirs" has a place sense, so it requires the adverb "there".
2. The past tense "went" matches "when you first ...", so "go there" and "gone there" are tense errors.
3. "went their" uses the possessive determiner, still wrong.

**Answer: went there**''',
                  wrong='"go there" is the wrong tense; "gone there" is the wrong form (it needs "had gone"); "went their" confuses there and their.', fast='Spot the there/their/theirs confusion and keep the tense.', traps='- Choosing "No error" because the words look similar.'))
    add('zs-va-para-computers', Z, 'Sentence ordering: how computers store patterns',
        'Arrange the following sentences in a logical order to construct a coherent paragraph:\n\n(A) for example, they will occasionally reproduce the patterns and occasionally modify them in different ways. The guidelines that computers use to move, duplicate,\n(B) An "application" is what most people now refer to as an "app" and is a collection of algorithms that work together to assist us in doing a task (such as buying stocks or finding a date online).\n(C) and manipulate these data arrays are likewise kept inside the computer. A group of rules collectively is referred to as a "program" or "algorithm."\n(D) These patterns are moved about in different physical storage spaces carved onto electrical components by computers. When we edit a document or touch up a photo,',
        'BDAC',
        'B introduces applications as a collection of algorithms. D then explains patterns moving in storage when we edit a document, A continues with "for example, they will reproduce the patterns...", and its sentence ends with "move, duplicate," which C completes ("and manipulate these data arrays..."). So B D A C.',
        section='aptitude', topic='verbal', type='mcq', sources=[wa(69)], options=['BADC', 'BCDA', 'BACD', 'BDAC'],
        solution=S('''1. B is the only self-contained opening sentence.
2. D ends with "When we edit a document or touch up a photo," and A begins "for example, they will occasionally reproduce the patterns...", so D must be followed by A.
3. A ends with "The guidelines that computers use to move, duplicate," and C starts "and manipulate these data arrays", so A must be followed by C.
Order: B D A C.

**Answer: BDAC**''',
                  wrong='Other options split the D-A or A-C links.', fast='Mark the mid-sentence breaks (comma endings and lowercase openings) and chain them.', traps='- Putting A directly after B because of the words "for example".'))
    add('zs-va-sentence-frank', Z, 'Sentence correction: misplaced modifier about toys and books',
        'Choose the option that correctly rephrases the underlined part of the sentence. Mark "No error" if there is none.\n\n<u>Frank put all the toys and books into his dad\'s car, which he was going to donate to an orphanage.</u>',
        'Frank put all the toys and books, which he was going to donate to an orphanage, into his dad\'s car.',
        'In the original, "which he was going to donate" sits next to "car", making it seem the car was being donated. Moving the clause next to "toys and books" fixes the misplaced modifier.',
        section='aptitude', topic='verbal', type='mcq', sources=[wa(70)],
        options=['Frank putting all his toys and books into his dad\'s car, which he was donating to an orphanage.', 'Being donated to an orphanage, Frank put all his toys and books into his dad\'s car.', 'Frank had put all his toy and book into his dad\'s car, which he was donating to an orphanage.', 'Frank put all the toys and books, which he was going to donate to an orphanage, into his dad\'s car.', 'No error'],
        notes='Option wording is paraphrased from a photo taken at an angle.',
        solution=S('''1. The relative clause "which he was going to donate to an orphanage" should sit next to the thing being donated: the toys and books.
2. In the given sentence it follows "car", so it wrongly modifies the car.
3. The fourth option places the clause right after "toys and books" and keeps the sentence complete.
4. Option 1 is a fragment ("Frank putting"), option 2 has a dangling modifier ("Being donated ... Frank"), option 3 changes number and tense unnecessarily.

**Answer: Frank put all the toys and books, which he was going to donate to an orphanage, into his dad\'s car.**''',
                  wrong='See steps 3 and 4.', fast='Put a "which" clause immediately after the noun it describes.', traps='- Choosing "No error" because the sentence is understandable.'))
    add('zs-va-rearrange-dogs', Z, 'Rearranging phrases: dogs and their presence',
        'Rearrange the following phrases to form a complete sentence. Note: the phrase numbered 1 is fixed.\n\n1. Dogs have a\n(A) intimidating presence,\n(B) commanding both admiration\n(C) special and sometimes\n(D) and caution from people',
        'CABD', '"Dogs have a special and sometimes intimidating presence, commanding both admiration and caution from people." So C, A, B, D.',
        section='aptitude', topic='verbal', type='mcq', sources=[wa(71), P], options=['ACBD', 'CABD', 'CBAD', 'ABCD'],
        solution=S('''1. "Dogs have a" needs an adjective phrase: "special and sometimes" (C) leads into "intimidating presence," (A).
2. The participle phrase "commanding both admiration" (B) follows the comma and is completed by "and caution from people" (D).
3. Read aloud: Dogs have a special and sometimes intimidating presence, commanding both admiration and caution from people.

**Answer: CABD**''',
                  wrong='ACBD, CBAD and ABCD break either "special and sometimes + adjective" or "admiration ... and caution".', fast='Pair the obvious phrase links first: "both ... and" and "special and sometimes + adjective".', traps='- Ignoring the comma after "presence".'))
    add('zs-va-para-darkmatter', Z, 'Sentence ordering: dark matter',
        'Arrange the following sentences in a logical order to construct a coherent paragraph:\n\n(A) The cosmic galaxies belies the presence of a mysterious substance that defies detection by conventional means.\n(B) Even today, as astronomers peer into the cosmic abyss, they are confronted with the profound mysteries of the cosmos.\n(C) Exotic candidates such as axions form the basis of speculative theories seeking to unveil dark matter.\n(D) Moreover, gravitational lensing offers tantalizing glimpses into the unseen cosmic.\n(E) In theoretical astrophysics, where cosmic phenomena unfold, the nature of dark matter remains an elusive enigma.',
        'BEACD',
        'B states the general mystery of the cosmos, E narrows to dark matter being an enigma, A describes the hidden substance, C gives candidate explanations and D ("Moreover") adds a further line of evidence last.',
        section='aptitude', topic='verbal', type='mcq', sources=[P], options=['BCDEA', 'DCEAB', 'BEACD', 'EACDB'],
        solution=S('''1. B is the broad opener ("Even today ... profound mysteries of the cosmos").
2. E narrows to dark matter as an elusive enigma.
3. A explains the evidence for this mysterious substance.
4. C lists theoretical candidates (axions).
5. D begins with "Moreover", so it adds to earlier points and goes last.

**Answer: BEACD**''',
                  wrong='Options starting with D or E lack context; BCDEA puts "Moreover" before the idea it adds to.', fast='Use signal words: "Moreover" never opens a paragraph; general statements come before specifics.', traps='- Starting with A because it names galaxies.'))
    add('zs-va-sentence-nineteenth', Z, 'Sentence correction: nineteenth-century assimilation',
        'Choose the option that correctly rephrases the underlined part. Mark "No error" if there is none.\n\nDuring the nineteenth century, Americans <u>look to the eventual civilization and assimilation with Native Americans through a process of removal, reservation, and directing culture change.</u>',
        'looked to civilize and assimilate Native Americans through a process of removal, reservation, and directed culture change.',
        'A past-time phrase needs the past tense ("looked"), and "removal, reservation, and directed culture change" must be parallel. The verb phrase "to civilize and assimilate" is also cleaner than the noun forms with "with".',
        section='aptitude', topic='verbal', type='mcq', confidence='medium', sources=[P],
        options=['have looked at the eventual civilization and assimilation with Native Americans through a processing of removal, reservation, and directing culture change.', 'had had looked to the eventual civilization and assimilation with Native Americans through a process of removal, reservation, and directing culture change.', 'looked at eventual civilization and assimilation with Native Americans through a process of removal, reservation, and directed culture change.', 'looked to civilize and assimilate Native Americans through a process of removal, reservation, and directed culture change.', 'No error'],
        notes='The wording of the underlined original is partly illegible; the fourth option is clearly the correct one.',
        solution=S('''1. "During the nineteenth century" signals simple past: "looked".
2. "have looked" is present perfect and "had had looked" is malformed.
3. "civilization and assimilation with Native Americans" is awkward: assimilation is not "with". The verb form "to civilize and assimilate Native Americans" is direct.
4. The list "removal, reservation, and directed culture change" should be parallel: "directed" works as an adjective, "directing" does not.

**Answer: looked to civilize and assimilate Native Americans through a process of removal, reservation, and directed culture change.**''',
                  wrong='The other options keep a wrong tense, a malformed verb or the non-parallel "directing".', fast='Fix tense first, then parallelism.', traps='- Leaving "directing culture change" because it sounds natural.'))
    add('zs-va-fill-pain', Z, 'Fill in the blanks: the language of pain',
        'Fill in the blank(s) with the correct word(s).\n\nThe language of pain, stretching back to ______, conflated the ______ and the physical.',
        'antiquity, emotional', '"Stretching back to antiquity" is the idiom, and "conflated the emotional and the physical" is a natural pair of contrasting ideas about pain.',
        section='aptitude', topic='verbal', type='mcq', sources=[P], options=['ancient, psychological', 'antiquity, emotional', 'semantic, spiritual', 'historically, nature'],
        solution=S('''1. The first blank follows "stretching back to", which needs a noun: antiquity (not the adjective "ancient" or the adverb "historically").
2. The second blank pairs with "the physical" and should be its contrast: emotional.

**Answer: antiquity, emotional**''',
                  wrong='"ancient" and "historically" are not nouns; "semantic" and "nature" do not pair with "physical".', fast='Check parts of speech before meaning.', traps='- Choosing "ancient, psychological", which sounds fine but breaks the grammar of "back to ____".'))
    add('zs-detail-colour-background', Z, 'Attention to detail: background colour of a labelled figure',
        'What is the colour of the background of the following figure? (The figure is a blue square containing a hexagon whose label text reads GREEN.)',
        'Blue', 'The question asks for the background colour, not the word written in the figure. The background is blue even though the text says GREEN.',
        section='aptitude', topic='logical', type='mcq', sources=[P], options=['Green', 'Pentagon', 'Hexagon', 'Blue'],
        notes='Visual question, described in words. Sibling items in the same section ask for the text written in a figure (a green square with a pentagon labelled PINK; the answer is Pink) and count triangles or lines, which need the images.',
        solution=S('The word written inside the hexagon is GREEN, a distractor (the Stroop effect). The task asks for the colour of the background, which is blue.\n\n**Answer: Blue**',
                  wrong='Green is the printed word; Pentagon and Hexagon are shapes, not colours.', fast='Read the question stem, then answer only what is asked (colour, shape or text).', traps='- Answering with the word printed in the figure.'))
    skip(Z, 'LEELU.pdf', 'compilers lab report (LEX program), not an OA')
    skip(Z, '21.14.21_0a99fb5b.jpg', 'section selection screen')
    skip(Z, '2304101003_Aishwarya_Priyadarshini.pdf', 'resume')
    skip(Z, 'ShraddhaSingh_23EC193_Resume.pdf', 'resume')
