"""Fractal (GMAT-style online assessment): reading/critical reasoning, data interpretation, data sufficiency, quant."""


def S(body, wrong='', fast='', traps=''):
    out = '### Solution\n' + body.strip() + '\n'
    if wrong:
        out += '\n### Why the other options are wrong\n' + wrong.strip() + '\n'
    if fast:
        out += '\n### Faster method\n' + fast.strip() + '\n'
    if traps:
        out += '\n### Common traps\n' + traps.strip() + '\n'
    return out


DS = ['Statement (1) ALONE is sufficient, but statement (2) alone is not sufficient.',
      'Statement (2) ALONE is sufficient, but statement (1) alone is not sufficient.',
      'BOTH statements TOGETHER are sufficient, but NEITHER statement ALONE is sufficient.',
      'EACH statement ALONE is sufficient.',
      'Statements (1) and (2) TOGETHER are not sufficient.']


def extend(add, merge, skip, alias):
    F = 'Fractal'

    # ---------- Reading and critical reasoning ----------
    add('fractal-ipr-structure', F, 'Organisation of a passage on intellectual property rights',
        'The passage explains that globalisation has raised the importance of intellectual property rights (IPRs); that firms with significant IPRs hold considerable power, especially in technology; that economists say the social benefits (innovation and creativity) outweigh monopolistic consequences while critics say IPRs stifle innovation and let firms limit competition and raise prices; and that the digital age is pushing the boundaries of traditional IPR frameworks, prompting regulators to balance rewarding innovation against the risks of monopolies.\n\nWhich of the following best describes the author\'s organization of the passage?',
        'The author discusses the importance of Intellectual Property Rights, outlines its positive and negative consequences, and finally discusses the role of regulatory bodies',
        'The passage opens with why IPRs matter, then gives the pro and con arguments, and closes with the regulators\' balancing role. Only the first option follows that order.',
        section='aptitude', topic='verbal', type='mcq', sources=['20240908_111150.jpg', '20240908_111156.jpg', 'WA0132.jpeg'],
        options=['The author discusses the importance of Intellectual Property Rights, outlines its positive and negative consequences, and finally discusses the role of regulatory bodies',
                 'The author critiques Intellectual Property Rights before defending its importance in the modern economy',
                 'The author provides a brief introduction of Intellectual Property Rights, discusses its history and evolution, and wraps up with its future prospects',
                 'The author maintains a neutral stance, providing equal arguments for and against Intellectual Property Rights'],
        notes='The passage was photographed in two parts; the summary above paraphrases it.',
        solution=S('''Map each paragraph block to its function.
1. Opening: globalisation raises the significance of IPRs and why firms guard them (importance).
2. Middle: economists (benefits) versus critics (stifled innovation, high prices) -> positive and negative consequences.
3. Close: the digital age strains old frameworks and regulators must balance reward and monopoly risk -> regulators\' role.
This is exactly option A.

**Answer: A**''',
                  wrong='- B: the author never critiques first and then defends.\n- C: there is no history or evolution section.\n- D: the author does not take a neutral "equal arguments" stance; the passage also covers regulators.',
                  fast='Write a three-word skeleton of the passage (importance, pros/cons, regulation) and match it to the options.',
                  traps='- Choosing the "neutral stance" option because both sides appear; structure questions ask about order, not tone.'))
    add('fractal-modern-marketing-structure', F, 'Logical structure of a passage on modern marketing',
        'The passage says that integrating traditional marketing with digital media has created "modern marketing": technology is used for data collection, audience targeting and analytics, giving higher return on investment. It then explains how HR roles are changing from hiring and firing to strategic decision-making, how regulators grapple with digital technology, and concludes that modern marketing is "a montage of technological changes reinforcing traditional business domains".\n\nWhat is the logical structure of the passage?',
        'Introduction of a concept followed by elaborations, examples and implications',
        'The first sentence introduces the concept; the rest elaborate its use, then its effects on HR and regulation, ending with a summary line. There is no opposing view or narrative.',
        section='aptitude', topic='verbal', type='mcq', sources=['WA0124.jpeg', 'WA0126.jpeg', 'WA0128.jpeg'],
        options=['Presentation of a concept followed by contrary ideas', 'Presentation of an idea followed by critique and conclusion', 'Introduction of a concept followed by elaborations, examples and implications', 'Narration of an event from start to finish', 'Discussion of two opposing concepts'],
        solution=S('''1. Para opens by defining "modern marketing" (concept introduced).
2. It then elaborates technology uses, impact on HR and on regulation (elaborations and implications).
3. It closes with a one-line synthesis. Nothing is critiqued, no contrary view is given, and it is not a story.

**Answer: Introduction of a concept followed by elaborations, examples and implications**''',
                  wrong='A, B and E need an opposing view or critique, which the passage lacks; D needs a sequence of events.',
                  fast='Look for words such as "however" or "critics". None appear, so eliminate options needing opposition.', traps='- Reading "traditional vs digital" as two opposing concepts; the passage says they reinforce each other.'))
    add('fractal-flexible-hours', F, 'Completion of an argument on flexible work hours for designers',
        'A design agency is contemplating flexible work hours for its graphic designers within a time window from 8 a.m. to 8 p.m.\n\nThis policy could likely undermine project completion if the designers\' responsibilities involve them needing to ______.',
        'seek frequent input and feedback from their colleagues',
        'Flexible, non-overlapping hours hurt tasks that depend on real-time collaboration. Frequent input from colleagues is the only option that depends on others being present at the same time.',
        section='aptitude', topic='logical', type='mcq', confidence='medium', sources=['WA0134.jpeg', 'WA0136.jpeg'],
        options=['seek frequent input and feedback from their colleagues', 'use specialized design software', 'adhere to the established design principles', 'ensure their designs meet client expectations', 'deliver projects within tight deadlines'],
        notes='The full wording of the stem was cropped at the right; the completion above is as captured.',
        solution=S('''Flexible hours let each person choose when to work in a 12-hour window, so overlap with colleagues shrinks.
- Software use, design principles and client expectations can be handled alone at any hour.
- Tight deadlines are affected by total hours, not by the time of day.
- Frequent colleague feedback needs others to be available at the same time, so it is the responsibility that flexible timing can undermine.

**Answer: seek frequent input and feedback from their colleagues**''', wrong='The other four are individual tasks that do not depend on when others are working.', fast='Find the option that needs other people at the same moment.', traps='- Picking "tight deadlines"; flexibility does not remove hours.'))
    add('fractal-telecare-training', F, 'Best plan to prepare healthcare staff for telecare',
        'Given the rapid growth of telecare in healthcare, traditional roles within the sector are transforming substantially. Within the next five years, healthcare professionals will require new skills to adapt effectively to these technologies.\n\nWhich of the following plans, if feasible, would enable a healthcare organization to prepare most effectively for this impending change?',
        'The organization commits to providing continuous necessary training to meet the evolving demand of its employees in the rapidly changing telecare-integrated healthcare field.',
        'The need is new skills within five years, so the best plan is ongoing, needed training. Surveys only observe, an awareness programme informs without training, and training six years in is too late.',
        section='aptitude', topic='logical', type='mcq', sources=['WA0144.jpeg', 'WA0146.jpeg'],
        options=['The organization commits to providing continuous necessary training to meet the evolving demand of its employees in the rapidly changing telecare-integrated healthcare field.', 'The organization contemplates conducting periodic surveys to understand the impacts of telecare integration on its employees role.', 'Before telecare implementation, the organization intends to conduct an educational program to inform staff of the likely repercussions.', 'The organization proposes offering specific telecare training to select employees six years into service.'],
        solution=S('''Requirement: staff need new skills before about five years pass.
- A: continuous, necessary training builds the skills in time and keeps up with change.
- B: surveys measure the impact but do not build skills.
- C: an educational programme informs staff about repercussions, which is awareness and not skill building, and only happens once.
- D: only select employees and after six years, past the five-year window.

**Answer: A**''', wrong='See steps B, C and D above.', fast='Check each plan for who is trained, what is taught and when.', traps='- Option C sounds proactive, but informing is not training.'))
    add('fractal-main-point-economics', F, 'Main point of a passage on economics, marketing and HR in business success',
        'The passage argues that a deep understanding of economic fundamentals (supply and demand, GDP, inflation, interest rates) is said to matter more than academic qualifications for entrepreneurs; marketing experts counter that understanding customer needs underpins strategy; HR researchers say success depends on the people who create, manage and sell the product; studies concluded that the three fields hold equitable significance, yet in practice undue importance is given to one field depending on the business environment.\n\nWhich among the following best articulates the main point of the passage?',
        'The debate among different fields on their importance in running a successful business',
        'The passage presents economists, marketers and HR researchers each claiming primacy, then notes the studies find equal importance. Its main point is the debate among fields about importance, not any single field.',
        section='aptitude', topic='verbal', type='mcq', confidence='medium', sources=['WA0148.jpeg', 'WA0150.jpeg'],
        options=['The significance of human resources in a business', 'The role of the marketing in business success', 'The debate among different fields on their importance in running a successful business', 'The changing emphasis in the business world depending on the requirements of the business environment', 'The importance of economics in business'],
        notes='Options B and D wording is partly cropped; reconstructed from context.',
        solution=S('''The main point must cover the whole passage.
1. Options A, B and E each describe only one field, so they are too narrow.
2. Option D (changing emphasis) is only the last sentence and is a detail about practice.
3. Option C covers all three fields claiming importance and the conclusion that they are equally significant.

**Answer: The debate among different fields on their importance in running a successful business**''', wrong='A, B, E are too narrow; D covers only the final sentence.', fast='Main-point options that name one subject are usually traps when the passage lists several.', traps='- Choosing the first field mentioned (economics).'))
    add('fractal-ai-developer-flaw', F, 'Flaw in the data analyst\'s argument about the DeepThought model',
        'AI Developer: The AI model DeepThought has shown promise in predictive analytics. However, the long-term impacts on data integrity are still unknown, and for that reason, I am not advocating for its wide use currently.\n\nData Analyst: Your viewpoint opposes your usual actions. You implement models that you know can potentially lead to data issues, so surely concern about impacts isn\'t why you won\'t endorse DeepThought.\n\nThe data analyst\'s argument is flawed because it fails to consider that ______.',
        'known risks can be compared to known benefits, but unknown risks cannot',
        'The developer accepts models with known, weighable risks but hesitates over DeepThought whose risk is unknown. The analyst treats these as the same, ignoring that unknown risks cannot be weighed against benefits.',
        section='aptitude', topic='logical', type='mcq', confidence='medium', sources=['WA0152.jpeg', 'WA0154.jpeg'],
        options=['the impacts of an AI model on data integrity can sometimes take time to manifest', 'the AI developer could be uncertain that DeepThought has been conclusively proven to be beneficial', 'if left unchecked, widespread use of a defective AI model could lead to serious data integrity concerns', 'known risks can be compared to known benefits, but unknown risks cannot', 'the data impacts of DeepThought might differ from other AI models'],
        notes='Option E text is partly cropped in the photo.',
        solution=S('''1. Developer\'s reason: the long-term impacts are unknown.
2. Analyst\'s attack: you use other models with known potential problems, so your stated reason must be false.
3. The gap: for other models the risks are known and can be balanced against benefits; for DeepThought the risk is unknown and cannot be balanced. That explains consistent behaviour, which option D states.

**Answer: known risks can be compared to known benefits, but unknown risks cannot**''', wrong='A, C and E add facts about impacts but do not explain why the developer\'s behaviour is consistent; B concerns benefit, not risk.', fast='Look for the distinction between the two situations the analyst treated as the same (known vs unknown).', traps='- Choosing C, which supports the developer\'s caution but does not expose the analyst\'s flaw.'))
    add('fractal-social-media-conclusion', F, 'Logical conclusion from a passage on digital marketing and social media',
        'The passage says social media has disrupted traditional marketing models, broadened consumer touchpoints, lowered entry barriers for small businesses (causing saturation and intense competition), and created a need for new skills among groups with differential technology acceptance rates. Despite this, many enterprises remain reluctant to embrace the medium fully and supplement traditional marketing with digital channels, causing inconsistent brand messages; some theorists blame reluctance to abandon successful frameworks, others see it as a response to demographic groups with different technology acceptance.\n\nWhat might be a logical conclusion that could be drawn from the passage?',
        'Digital marketing strategies should cater to multiple demographic groups.',
        'The passage links the blended approach to demographic groups accepting technology at different rates. A conclusion that follows is that digital strategies should serve several demographic groups. The other options go beyond the text (disregard traditional methods, small business advantage, forced adoption).',
        section='aptitude', topic='logical', type='mcq', confidence='medium', sources=['WA0162.jpeg', 'WA0164.jpeg'],
        options=['Businesses should disregard traditional marketing methods.', 'Digital marketing strategies should cater to multiple demographic groups.', 'Brand messages are always consistent across channels.', 'Small businesses have an advantage in the digital era.', 'Increased market saturation will force businesses to embrace digital marketing.'],
        notes='Option C wording is not visible in the photo (only its place between B and D is); it is reconstructed.',
        solution=S('''1. The passage gives two explanations for the hybrid approach; one is demographic groups with different technology acceptance.
2. A conclusion supported by that explanation: strategies should address several groups.
3. A and D and E are stronger claims not backed by the text (the passage says entry barriers fell and saturation grew, which is not an advantage; enterprises remain reluctant, so "forced" is unsupported).

**Answer: Digital marketing strategies should cater to multiple demographic groups.**''', wrong='A is contradicted (firms still use traditional methods); D and E overreach; C contradicts "inconsistent brand messages".', fast='Choose the conclusion that restates one of the passage\'s own explanations, not a new claim.', traps='- Selecting the option about saturation because it is mentioned in the text.'))

    # ---------- Data interpretation ----------
    add('fractal-di-airline-growth', F, 'Airline B quarter with the biggest percentage increase',
        'A bar chart gives the number of passengers (in millions) carried by two airlines in four quarters of 2020. Airline A: Q1 15, Q2 12, Q3 18, Q4 20. Airline B: Q1 14, Q2 16, Q3 17, Q4 21.\n\nWhich quarter did Airline B see the biggest percentage increase in passengers from the previous quarter?',
        'Q4', 'Airline B growth: Q2 = (16-14)/14 = 14.3%, Q3 = (17-16)/16 = 6.25%, Q4 = (21-17)/17 = 23.5%. The biggest is Q4.',
        section='aptitude', topic='data-interpretation', type='mcq', sources=['WA0059.jpeg', 'WA0061.jpeg'],
        options=["Can't determine from data given", 'Q1', 'Q4', 'Q2', 'Q3'],
        solution=S('''Percentage increase = (current - previous)/previous.
- Q2: (16-14)/14 = 14.29%
- Q3: (17-16)/16 = 6.25%
- Q4: (21-17)/17 = 23.53%
Q1 has no previous quarter in the data.

**Answer: Q4**''', wrong='Q2 14.3% and Q3 6.25% are lower; Q1 cannot be computed; the data are sufficient.', fast='Q4 has the largest absolute rise (4) on a modest base (17), so it is the largest percentage too.', traps='- Using the absolute change alone (Q2 is +2, Q4 is +4, but check the base).'))
    add('fractal-di-courier-growth', F, 'Courier company with the highest year-on-year revenue growth',
        'Annual revenue (in millions USD), 2016 to 2020. Xeon Express: 500, 550, 600, 620, 650. Paragon Couriers: 450, 520, 560, 590, 610.\n\nWhich company had the highest year-on-year revenue growth rate in any year?',
        'Paragon Couriers', 'Paragon grew 11.1% (450 to 520) in 2017, higher than any Xeon year (best 10%, 500 to 550). Other Paragon years: 7.7%, 5.4%, 3.4%; Xeon: 9.1%, 3.3%, 4.8%.',
        section='aptitude', topic='data-interpretation', type='mcq', sources=['WA0063.jpeg', 'WA0065.jpeg'],
        options=['Paragon Couriers', 'Both had the same highest growth rate', 'Xeon Express', 'Data insufficient', 'None of the above'],
        solution=S('''Compute each year-on-year growth.
Xeon: 550/500 = 10.0%, 600/550 = 9.09%, 620/600 = 3.33%, 650/620 = 4.84%.
Paragon: 520/450 = 11.11%, 560/520 = 7.69%, 590/560 = 5.36%, 610/590 = 3.39%.
Highest overall = Paragon in 2017 (11.11%).

**Answer: Paragon Couriers**''', wrong='Xeon\'s best growth is 10%; the rates differ; the data are sufficient.', fast='Only the first year pair can reach 10% or more: 50/450 against 50/500.', traps='- Comparing absolute growth (Xeon grows by 50 in 2017 too).'))
    add('fractal-di-ecommerce-margin-swap', F, 'Highest profit after swapping profit margins of two websites',
        'Six e-commerce websites, year 2020 (annual revenue in million $, profit margin %): ShopNow 380, 30; BayZ 520, 45; ClickBuy 210, 18; CartJoy 460, 40; RapidShop 290, 22; SwiftPurchase 550, 50. (Sales volume, growth and age group columns are also shown.)\n\nIf the profit margins of BayZ and ClickBuy are interchanged, which website will have the highest profit?',
        'SwiftPurchase', 'After swapping, BayZ = 520 x 18% = 93.6 and ClickBuy = 210 x 45% = 94.5. The rest: ShopNow 114, CartJoy 184, RapidShop 63.8, SwiftPurchase 550 x 50% = 275. The highest is SwiftPurchase.',
        section='aptitude', topic='data-interpretation', type='mcq', sources=['WA0067.jpeg', 'WA0069.jpeg', 'WA0071.jpeg', 'WA0073.jpeg'],
        options=['CartJoy', 'ShopNow', 'BayZ', 'SwiftPurchase', 'ClickBuy'],
        solution=S('''Profit = revenue x margin.
- ShopNow 380 x 0.30 = 114
- BayZ (now 18%) 520 x 0.18 = 93.6
- ClickBuy (now 45%) 210 x 0.45 = 94.5
- CartJoy 460 x 0.40 = 184
- RapidShop 290 x 0.22 = 63.8
- SwiftPurchase 550 x 0.50 = 275
SwiftPurchase is highest (it was already highest before the swap; the swap moved BayZ from 234 to 93.6).

**Answer: SwiftPurchase**''', wrong='BayZ and ClickBuy drop to about 94; CartJoy 184 and ShopNow 114 are lower than 275.', fast='SwiftPurchase has the largest revenue and the largest margin, so only an unaffected comparison is needed.', traps='- Assuming the swap changes the top website (it only changes BayZ and ClickBuy).'))
    add('fractal-di-profit-percentage', F, 'Year with the highest profit percentage',
        'Operating costs and profits of XYZ company ($ million). 2016: costs 140, profit 70. 2017: 150, 85. 2018: 160, 90. 2019: 180, 100. 2020: 200, 120.\n\nIn what year was the profit percentage highest?',
        '2020', 'Profit as a percentage of cost: 2016 50%, 2017 56.7%, 2018 56.25%, 2019 55.6%, 2020 60%. (Against total revenue the order is the same: 33.3, 36.2, 36.0, 35.7, 37.5.)',
        section='aptitude', topic='data-interpretation', type='mcq', sources=['WA0080.jpeg', 'WA0082.jpeg'],
        options=['2018', '2016', '2020', '2017', '2019'],
        solution=S('''Profit % = profit / operating cost.
2016: 70/140 = 50%; 2017: 85/150 = 56.67%; 2018: 90/160 = 56.25%; 2019: 100/180 = 55.56%; 2020: 120/200 = 60%.
2020 is highest. The conclusion is the same if profit is taken as a share of revenue (cost + profit).

**Answer: 2020**''', wrong='All other years are below 57%.', fast='Profit/cost: 120/200 = 0.6 is the only ratio above 0.57.', traps='- Picking the year with the largest profit in absolute terms without checking the ratio (2020 is also largest here).'))
    add('fractal-di-expense-growth', F, 'Year with the highest percentage increase in expenses',
        'A retail store\'s annual revenue and expenses ($ thousand), 2017 to 2021. Expenses: 2017 600, 2018 700, 2019 800, 2020 570, 2021 710.\n\nIn which year did the expenses increase by the highest percentage compared to the previous year?',
        '2021', 'Expense changes: 2018 +16.7%, 2019 +14.3%, 2020 -28.75% (a decrease), 2021 +24.6% (570 to 710). The highest increase is in 2021.',
        section='aptitude', topic='data-interpretation', type='mcq', sources=['WA0084.jpeg', 'WA0086.jpeg'],
        options=['2018', 'There was no increase in expenses in any year', '2019', '2021', '2020'],
        notes='The expense for 2020 and 2021 (570 and 710) was read from a slightly blurry photo.',
        solution=S('''Percentage change = (current - previous)/previous.
- 2018: 100/600 = 16.67%
- 2019: 100/700 = 14.29%
- 2020: (570-800)/800 = -28.75% (decrease)
- 2021: 140/570 = 24.56%

**Answer: 2021**''', wrong='2018 and 2019 are lower; 2020 is a decrease.', fast='The 2021 jump is 140 on a base of 570, a much smaller base than in 2018 or 2019.', traps='- Comparing absolute increases (2021 is also the largest absolute here, but use the base).'))
    add('fractal-di-quarterly-margin', F, 'Quarter with the highest profit margin',
        'Quarterly revenue and profit of XYZ Limited for 2021 ($). Q1 revenue 50,000, profit 20,000; Q2 revenue 60,000, profit 25,000; Q3 revenue 75,000, profit 30,000; Q4 profit 40,000 (revenue about 80,000).\n\nWhich quarter had the highest profit margin?',
        'Q4', 'Margins: Q1 40%, Q2 41.7%, Q3 40%, Q4 40,000/80,000 = 50%. Even if Q4 revenue were somewhat lower, the margin stays well above the others.',
        section='aptitude', topic='data-interpretation', type='mcq', confidence='medium', sources=['WA0090.jpeg', 'WA0092.jpeg'],
        options=['Q2', 'Q3', 'Profit margin is the same in all quarters', 'Q1', 'Q4'],
        notes='The Q4 revenue label is hidden in the photo (about 80,000). Option C is partly cropped.',
        solution=S('''Margin = profit/revenue.
Q1: 20/50 = 40%. Q2: 25/60 = 41.67%. Q3: 30/75 = 40%. Q4: 40/80 = 50% (revenue about 80,000).
Q4 is highest.

**Answer: Q4**''', wrong='Q1, Q2 and Q3 lie between 40% and 41.7%.', fast='Q4 profit doubles Q1\'s while revenue grows by far less than double.', traps='- Comparing profit amounts instead of margins.'))
    add('fractal-ds-college-grads', F, 'Data sufficiency: college graduates in a sample of 120',
        'In a random sample of 120 adults, how many are college graduates?\n\n(1) In the sample, the number of adults who are not college graduates is 3 times the number who are college graduates.\n(2) In the sample, the number of adults who are not college graduates is 90 more than the number who are college graduates.',
        'EACH statement ALONE is sufficient.', 'Let g be graduates, so non-graduates are 120 - g. (1): 120 - g = 3g gives g = 30. (2): 120 - g = g + 90 gives g = 15. Each gives a unique value.',
        section='aptitude', topic='quant', type='mcq', sources=['WA0075.jpeg', 'WA0077.jpeg'], options=DS,
        solution=S('''Let g = college graduates; non-graduates = 120 - g.
(1) 120 - g = 3g -> g = 30. Sufficient.
(2) 120 - g = g + 90 -> 2g = 30 -> g = 15. Sufficient.
(The two statements give different values, which is allowed to happen only because the problem is invented; each alone answers the question.)

**Answer: EACH statement ALONE is sufficient.**''', wrong='Each statement alone fixes g, so A, B, C and E are false.', fast='Both are linear equations in one unknown, so each is sufficient.', traps='- Combining the statements even though each already works.'))
    add('fractal-ds-median-n', F, 'Data sufficiency: value of n in a five-number list',
        'n, 10, 8, 6, 12\n\nWhat is the value of n in the list above?\n\n(1) n > 12\n(2) The median of the numbers in the list is 9.',
        'Statement (2) ALONE is sufficient, but statement (1) alone is not sufficient.', 'The sorted known values are 6, 8, 10, 12. For a median of 9 with five numbers, the middle value must be n itself, between 8 and 10, so n = 9 (if n were elsewhere the median would be 8 or 10). Statement (1) gives only n > 12.',
        section='aptitude', topic='quant', type='mcq', confidence='medium', sources=['WA0088.jpeg'], options=DS,
        notes='The answer option screen for this item was not photographed; the standard option wording is used.',
        solution=S('''(1) n > 12 allows infinitely many values: insufficient.
(2) Five numbers, the median is the third value. With known 6, 8, 10, 12:
- n <= 8: sorted n,6/8,... median is 8.
- 8 < n < 10: sorted 6, 8, n, 10, 12, median n.
- n >= 10: median is 10.
A median of 9 therefore forces n = 9. Sufficient.

**Answer: Statement (2) ALONE is sufficient, but statement (1) alone is not sufficient.**''', wrong='(1) alone gives a range; the other combinations are unnecessary or wrong.', fast='With an odd count, the median equals one of the values; since 9 is not in the list, it must be n.', traps='- Averaging 8 and 10 as if the count were even.'))
    add('fractal-ds-j-over-k', F, 'Data sufficiency: is j/k greater than 1',
        'If j and k are positive, is j/k greater than 1?\n\n(1) j < k\n(2) jk > 1',
        'Statement (1) ALONE is sufficient, but statement (2) alone is not sufficient.', 'For positive numbers, j < k means j/k < 1, so the answer to the question is a definite no. Statement (2) allows j = 4, k = 1 (ratio above 1) and j = 1, k = 4 (below 1).',
        section='aptitude', topic='quant', type='mcq', sources=['WA0116.jpeg', 'WA0118.jpeg'], options=DS,
        solution=S('''(1) j < k with k > 0: dividing by k gives j/k < 1. The answer is a definite "No", so sufficient.
(2) jk > 1: j = 4, k = 1 gives ratio 4 (yes); j = 1, k = 4 gives ratio 0.25 (no). Insufficient.

**Answer: Statement (1) ALONE is sufficient, but statement (2) alone is not sufficient.**''', wrong='(2) gives both yes and no; no need to combine.', fast='In data sufficiency a definite "No" is sufficient too.', traps='- Thinking (1) is insufficient because it does not give "greater than 1".'))
    add('fractal-ds-pat-earnings', F, 'Data sufficiency: Pat\'s earnings from his savings',
        'If Pat saved $1190 of his earnings last month, how much did Pat earn last month?\n\n(1) Pat spent 1/4 of his earnings last month for living expenses and saved 1/6 of the remainder.\n(2) Of his earnings last month, Pat paid the same amount in taxes as he saved.',
        'Statement (1) ALONE is sufficient, but statement (2) alone is not sufficient.', 'Statement (1): remainder after living expenses = 3E/4, saved = (1/6)(3E/4) = E/8 = 1190, so E = 9520. Statement (2) only says taxes equal savings, which leaves E unknown.',
        section='aptitude', topic='quant', type='mcq', sources=['WA0120.jpeg', 'WA0122.jpeg'], options=DS,
        solution=S('''(1) Savings = (1/6) x (3/4)E = E/8. Given 1190 = E/8, E = 9520. Sufficient.
(2) Taxes = savings = 1190, but no other expense or fraction is known, so E cannot be found. Insufficient.

**Answer: Statement (1) ALONE is sufficient, but statement (2) alone is not sufficient.**''', wrong='(2) is not enough alone, and since (1) works alone, the combination options are wrong.', fast='Savings fraction of earnings is 3/4 x 1/6 = 1/8.', traps='- Using 1/6 of E instead of 1/6 of the remainder.'))

    # ---------- Quant ----------
    add('fractal-decimal-7-11', F, '21st digit after the decimal point of 7/11',
        'What is the 21st digit to the right of the decimal point in the decimal form of 7/11?',
        '6', '7/11 = 0.636363..., repeating "63". Odd-numbered places hold 6 and even-numbered places hold 3. The 21st place is odd, so the digit is 6.',
        section='aptitude', topic='quant', type='mcq', sources=['WA0098.jpeg', 'WA0100.jpeg'], options=['7', '5', '6', '3', '1'],
        solution=S('7/11 = 0.636363... The block "63" has length 2. Position 21 = 2 x 10 + 1, so it is the first digit of the 11th block: 6.\n\n**Answer: 6**',
                  wrong='7, 5, 3 and 1 are not 6; 3 would be the 20th digit.', fast='Odd position gives the first digit of the block (6), even gives the second (3).', traps='- Counting the digit before the decimal point.'))
    add('fractal-grades-fractions', F, 'Students in a course from grade fractions',
        'Of the final grades received by the students in a certain math course, 1/5 are A\'s, 1/4 are B\'s, 1/2 are C\'s, and the remaining 145 grades are D\'s. What is the number of students in the course?',
        '2900', 'A + B + C = 1/5 + 1/4 + 1/2 = 0.95, so D = 5% of the students. 145/0.05 = 2900.',
        section='aptitude', topic='quant', type='numeric', confidence='medium', sources=['WA0102.jpeg'],
        notes='The answer options are cropped in the photo; the value is computed.',
        solution=S('1/5 + 1/4 + 1/2 = 4/20 + 5/20 + 10/20 = 19/20. D\'s are 1/20 of the class = 145, so the class has 145 x 20 = 2900 students.\n\n**Answer: 2900**',
                  fast='Common denominator 20: A 4, B 5, C 10, D 1 out of 20.', traps='- Forgetting that the fractions must add to 1 with the D grades.'))
    add('fractal-arithmetic-saving', F, 'Total saved over 52 weeks with weekly increase',
        'In the first week of the year, Nancy saved $27. In each of the next 51 weeks, she saved $27 more than she had saved in the previous week. What was the total amount that Nancy saved during the 52 weeks?',
        '37206', 'Week k savings = 27k. Total = 27 x (1 + 2 + ... + 52) = 27 x 52 x 53 / 2 = 27 x 1378 = 37,206.',
        section='aptitude', topic='quant', type='numeric', confidence='medium', sources=['WA0104.jpeg'],
        notes='The answer options are cropped in the photo; the value is computed.',
        solution=S('Savings form an arithmetic progression 27, 54, ..., 27 x 52. Sum = 27 x (52 x 53 / 2) = 27 x 1378 = 37,206.\n\n**Answer: $37,206**',
                  fast='Sum = n/2 x (first + last) = 26 x (27 + 1404) = 26 x 1431 = 37,206.', traps='- Using 51 weeks of increase on top of a 27 base, i.e. 27 x 51 x 52 / 2.'))
    add('fractal-machines-rate', F, 'Bottles produced by 9 machines in 5 minutes',
        'Running at the same constant rate, 3 identical machines can produce a total of 90 bottles per minute. At this rate, how many bottles could 9 such machines produce in 5 minutes?',
        '1350', 'One machine makes 30 bottles per minute. Nine machines make 270 per minute, and in 5 minutes 1350.',
        section='aptitude', topic='quant', type='numeric', confidence='medium', sources=['WA0106.jpeg'],
        notes='The answer options were not captured; the value is computed.',
        solution=S('Rate per machine = 90/3 = 30 per minute. Nine machines: 270 per minute. In 5 minutes: 1350.\n\n**Answer: 1350**', fast='Machines x3 and time x5/1 means 90 x 3 x 5 = 1350.', traps='- Forgetting to multiply by the time.'))
    add('fractal-ratio-soap', F, 'Altered soap-alcohol-water solution',
        'The ratio, by volume, of soap to alcohol to water in a certain solution is 2:70:140. The solution will be altered so that the ratio of soap to alcohol is magnified two times while the ratio of soap to water is made half. If the altered solution will contain 210 cubic centimeters of alcohol, how many cubic centimeters of water will it contain?',
        '1680', 'Original soap:alcohol = 1:35, soap:water = 1:70. Doubling the first ratio gives soap/alcohol = 2/35, halving the second gives soap/water = 1/140. For alcohol 210, soap = 210 x 2/35 = 12, and water = 12 x 140 = 1680.',
        section='aptitude', topic='quant', type='mcq', sources=['WA0108.jpeg', 'WA0110.jpeg'], options=['1200', '1260', '1400', '1680', '1650'],
        notes='Options A and B were cropped; the others read 1400, 1680 and 1650.',
        solution=S('''1. Original: soap/alcohol = 2/70 = 1/35; soap/water = 2/140 = 1/70.
2. Altered: soap/alcohol = 2 x 1/35 = 2/35; soap/water = (1/2) x 1/70 = 1/140.
3. Alcohol = 210 -> soap = 210 x 2/35 = 12.
4. Water = soap x 140 = 12 x 140 = 1680.

**Answer: 1680**''', wrong='1400 and 1650 do not satisfy soap/water = 1/140 with soap = 12.', fast='New ratio soap:alcohol:water = 2:35:280, so water = 210 x 280/35 = 1680.', traps='- Halving the water quantity instead of halving the soap-to-water ratio.'))
    add('fractal-pumps-two', F, 'Two pumps filling a pool, first started alone',
        'Two pumps, each working alone, can fill an empty pool in 28 hours and 42 hours, respectively. The first pump initially started alone for h hours; after which the second pump was also started. If it took a total of 25 hours for the pool to be filled completely by both pumps, what is the value of h?',
        '20.5', 'Rates are 1/28 and 1/42, combined 5/84. Work: h/28 + (25 - h)(5/84) = 1, i.e. 3h + 125 - 5h = 84, so h = 20.5.',
        section='aptitude', topic='quant', type='mcq', sources=['WA0112.jpeg'], options=['20.5', '25.5', '27.5', '20.9', '16.5'],
        solution=S('''1. Combined rate = 1/28 + 1/42 = 3/84 + 2/84 = 5/84 per hour.
2. First pump alone for h hours: h/28 = 3h/84.
3. Both for 25 - h hours: 5(25 - h)/84.
4. 3h + 125 - 5h = 84 -> 2h = 41 -> h = 20.5.

**Answer: 20.5**''', wrong='Other values do not satisfy 3h + 5(25 - h) = 84.', fast='Plug h = 20.5: 61.5/84 + 22.5/84 = 84/84.', traps='- Treating 25 hours as the time of both pumps together.'))
    add('fractal-overtime-pay', F, 'Total weekly remuneration with overtime rate',
        'A clothing retailer employs 250 salespeople. Each of them is paid $9 per hour for the first 38 hours worked during a week and 1 1/4 times that rate for hours worked in excess of 38 hours. What was the total remuneration of the salespeople for a week in which 20 percent of them worked 30 hours, 50 percent worked 38 hours, and the rest worked 45 hours?',
        '87806', 'Overtime rate = 1.25 x 9 = $11.25. 50 people x 30 h = 50 x 270 = 13,500. 125 people x 38 h = 125 x 342 = 42,750. 75 people x (342 + 7 x 11.25 = 420.75) = 31,556.25. Total = 87,806.25, closest option 87,806.',
        section='aptitude', topic='quant', type='mcq', confidence='medium', sources=['WA0114.jpeg'], options=['87506', '87956', '88506', '87806', '88106'],
        notes='The overtime multiplier is partly illegible ("1 ? times"); 1.25 reproduces option D (87,806). With 1.5 no option matches.',
        solution=S('''1. Groups: 20% = 50 people at 30 h; 50% = 125 at 38 h; 30% = 75 at 45 h.
2. Overtime rate = 1.25 x 9 = 11.25.
3. 30 h: 30 x 9 = 270 -> 50 x 270 = 13,500.
4. 38 h: 38 x 9 = 342 -> 125 x 342 = 42,750.
5. 45 h: 342 + 7 x 11.25 = 420.75 -> 75 x 420.75 = 31,556.25.
6. Total = 13,500 + 42,750 + 31,556.25 = 87,806.25 which matches option D.

**Answer: 87806**''', wrong='Other totals differ by multiples of about 50 and come from wrong overtime rates.', fast='Only the 75 people with overtime need the extra: base 250 x 9 x 38 less the short hours, etc.', traps='- Applying the overtime rate to all hours above 30 instead of above 38.'))
    add('fractal-book-depot', F, 'Fraction of books sorted by the day crew',
        'In a book depot, each worker on the night shift sorted 3/7 as many books as each worker on the day shift. If the night crew is 2/3 the size of the day crew, what fraction of all books sorted by both crews was sorted by the day crew?',
        '7/9', 'Let the day crew have D workers each sorting b books: day total Db. Night: (2D/3) x (3b/7) = 2Db/7. Day fraction = Db / (Db + 2Db/7) = 1 / (9/7) = 7/9.',
        section='aptitude', topic='quant', type='mcq', sources=['WA0051.jpeg', 'WA0053.jpeg'], options=['7/9', '5/9', '2/3', '3/4', '3/7'],
        solution=S('''1. Day: D workers x b books = Db.
2. Night: (2/3)D workers x (3/7)b books = (6/21)Db = (2/7)Db.
3. Total = Db(1 + 2/7) = (9/7)Db.
4. Day share = Db / ((9/7)Db) = 7/9.

**Answer: 7/9**''', wrong='5/9 and 3/7 come from using only one of the two ratios; 2/3 and 3/4 are not 1/(1 + 2/7).',
                  fast='Take D = 3, b = 7: day = 21, night = 2 x 3 = 6. Day share = 21/27 = 7/9.', traps='- Using 3/7 and 2/3 separately instead of multiplying them for the night total.'))
    merge('prime-factors', F, ['WA0096.jpeg'])
    skip(F, 'WA0094.jpeg', 'revenue/profit line chart values unreadable')
    skip(F, 'WA0138.jpeg', 'question stem cropped')
    skip(F, 'WA0140.jpeg', 'question stem cropped')
    skip(F, 'WA0142.jpeg', 'options of cropped question')
    skip(F, 'WA0156.jpeg', 'question stem not captured')
    skip(F, 'WA0158.jpeg', 'blurry options of uncaptured question')
    skip(F, 'WA0160.jpeg', 'options of uncaptured question')
    skip(F, 'WA0166.jpeg', 'question stem and options not captured')
    skip(F, 'passport_size_photo_Aniruddha_Tathe.jpg', 'personal photo')
    skip(F, 'ssc-cgl-13th-sep-shift-1_copy.pdf', 'government exam paper, not an OA')
