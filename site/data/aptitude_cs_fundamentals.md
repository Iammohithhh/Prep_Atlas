# Aptitude & CS Fundamentals — Web Research (collected 2026-10-01)

Partial report — the search was stopped early on request. The question list is mostly topic-level, not full worded problems.

Source caveats:
- LeetCode Discuss, naukri code360 and Glassdoor block direct fetches (403). Details from them come only from search-engine snippets.
- placementpreparation.io, placementpapers.app, papersadda and faceprep are aggregator pages and less reliable.
- GeeksforGeeks and jointaro pages are first-hand accounts.

---

## OA patterns by company

| Company | Sections | # Qs / Time | Platform | Negative marking | Source (date) |
|---|---|---|---|---|---|
| **Goldman Sachs** (aptitude round) | Numerical computation (probability, P&C, arithmetic), numerical reasoning (DI, series), logical reasoning (sequences, coding-decoding, logic gates), abstract reasoning (figure series), diagrammatic reasoning, verbal (RC, sentence correction) | 66 MCQs / 90 min. Older variant: 70 Qs / 120 min over 7 sections, including two 5-question comprehensions. | HackerRank | Yes, +5 / −2. Cutoff about 50 correct (~75%). | [placementpreparation.io](https://www.placementpreparation.io/goldman-sachs/syllabus-and-test-pattern/) (aggregator, 2025–26); [code360 off-campus Mar 2025](https://www.naukri.com/code360/interview-experiences/goldman-sachs/goldman-sachs-interview-experience-by-shubham-namasudra-off-campus-mar-2025) (snippet) |
| **Goldman Sachs** (technical round) | 2–3 coding + about 10 MCQs (DSA, OOP, quant, output prediction, DBMS). One variant: 3 coding + 5 DSA MCQ + 2 OOP MCQ + 3 quant MCQ + 1 behavioural. | 60–120 min | HackerRank | On MCQs only | Same sources (2025) |
| **DE Shaw** | 1 DP coding + technical MCQs (DSA, SQL, OS, C++ OOP) + aptitude MCQs + systems MCQs | 45 min in one report. Another: 3 coding + 20 MCQs (7 CS + 13 aptitude) in 1h20m, with about 30 min for 15 hard aptitude MCQs. | HackerRank | Not stated | [GFG DE Shaw process](https://geeksforgeeks.org/de-shaw-recruitment-process); [LeetCode May 2025](https://leetcode.com/discuss/post/6637806/); [jointaro Jul 2025 intern](https://www.jointaro.com/interviews/companies/de-shaw/experiences/software-engineerinternship-hyderabad-july-1-2025-no-offer-positive-176d46d3/) (only 3 coding Qs, no MCQs; format varies by role) |
| **Oracle** (Server Technology, on-campus FTE) | 4 separately timed sections: SE aptitude (easy, speed), contextual communication, coding skills (MCQs on trees and flowcharts), CS knowledge | 95–100 min. Second coding round: 2 Qs in 1 hr (recursion problem, word ladder). | — | — | [GFG, 11 Jul 2025](https://geeksforgeeks.org/oracle-on-campus-fte-server-technology) |
| **Oracle** (other 2024–25) | 1–2 coding + ~15 aptitude + ~15 technical MCQs (OOP, DBMS, OS, CN, SQL) | ~90 min | — | — | [jointaro](https://www.jointaro.com/interviews/companies/oracle/work-experiences/applications-developer-hyderabad-september-11-2025-2-df74a539/); [papersadda 2026](https://papersadda.com/article/oracle-online-assessment-2026/) (aggregator) |
| **SAP Labs** | ~25 aptitude MCQs (quant, verbal, logical, DI) + technical MCQs (OS scheduling, normalisation, OOP) + 2–3 implementation-level coding incl. SQL (JOIN / GROUP BY / HAVING) | ~1 hr for MCQs. One drive: ~400 test-takers → 29 shortlisted → 6 offers. | — | — | [GFG SAP Associate Developer](https://www.geeksforgeeks.org/?p=532286); [LeetCode on-campus](https://leetcode.com/discuss/interview-experience/6174996) (snippets) |
| **ZS Associates** | 6 timed sections: quant, logical (25 Qs in 5 min), analytical (directions, blood relations, positioning), verbal, DI, role-specific | 59 Qs / 52 min (older: 60 / 60) | Mettl | No (older report) | [placementpreparation.io](https://www.placementpreparation.io/zs-associates/recruitment-process/) (2025); [code360 Apr 2025](https://www.naukri.com/code360/interview-experiences/zs-associates-india-pvt-ltd/interview-experience-on-campus-apr-2025-2-9878) |
| **Axtria** | Technical (Java, Python, SQL, OOP, cloud, git, output-of-program), logical, data sufficiency, DI (incl. donut charts), quant | 70 Qs / 90 min, ~60% to advance | — | — | [GFG Axtria](https://www.geeksforgeeks.org/?p=1186549) (~2024) |
| **Fractal Analytics** | Data analysis, reasoning, quant, verbal (some add basic coding) | 70 Qs / 75 min | — | — | [GFG Fractal](https://www.geeksforgeeks.org/?p=581612) (mixed dates) |
| **Qualcomm** | Aptitude (TSD, DI, ratio, P&C, mixtures), C programming (output/error, bitwise), technical (OS, CN, DBMS, sorting, OOP) | Sectional cutoffs | — | Yes, +1 / −0.25 | [GFG, 23 Jul 2025](https://www.geeksforgeeks.org/interview-experiences/qualcomm-interview-experience-on-campus-3/) |
| **Texas Instruments** | Aptitude (20) + analog (20) + digital (20), MCQ / fill-in | 30 min/section (or 30/45/45) | — | Per-section cutoff | [Glassdoor](https://www.glassdoor.sg/Interview/Texas-Instruments-Interview-E651-RVW99485368.htm) (2025, snippet) |
| **Cadence** | SW: 20 C++/Java MCQs + 2 medium coding (2023). HW: aptitude, digital, STA, Python, Verilog. | — | — | Implied | [GFG Aug 2023](https://www.geeksforgeeks.org/?p=1049253) |
| **Deutsche Bank** | 2 medium coding + 10 MCQs (DSA, DBMS, OS, CN, OOP) | ~90 min | — | — | [GFG](https://www.geeksforgeeks.org/?p=1167692) (2023–24) |
| **Mastercard** | C language + core CS (Nov 2025); another drive 2 DSA Qs (Aug 2025) | — | — | — | [Glassdoor](https://clear.glassdoor.nl/Interview/Mastercard-Interview-E3677-RVW99695760.htm) |
| **Trilogy Innovations** | 4 medium-hard coding → CCAT → proctored PCCAT | CCAT/PCCAT ~15 min each | Criteria Corp | — | [Glassdoor](https://fr.glassdoor.ca/Entretien/Trilogy-Innovations-Entretien-E6356019-RVW100098864.htm) (2025) |
| **Visa** | 4 coding (3 easy-medium, 1 hard), no aptitude | 70 min | CodeSignal | — | [jointaro May 2025](https://www.jointaro.com/interviews/companies/visa/experiences/software-engineer-bengaluru-may-8-2025-no-offer-neutral-dc30770b/); [LeetCode](https://leetcode.com/discuss/interview-experience/7307977) |
| **PayPal** | Quant (15–20), verbal (10–15), logical (10–15), 2–3 coding; Nov 2025: only 2 coding | — | HackerRank | — | [faceprep](https://faceprep.in/article/paypal-interview-process-a-comprehensive-guide-for-2025/) (aggregator) |
| **Amazon** (SDE intern) | Coding + work simulation + work-style (~50 sliders, Leadership Principles). No aptitude. | — | Amazon | — | [GFG](https://www.geeksforgeeks.org/?p=1203014); [1point3acres](https://www.1point3acres.com/interview/thread/1103188) (2025) |
| **Microsoft** (intern 2025) | 2 DSA problems, no MCQs | 75 min | — | — | [GFG](https://www.geeksforgeeks.org/interview-experiences/microsoft-internship-oa-interview-experience-2025/) |
| **BNY Mellon** | DSA on HackerRank, moderate-hard; aptitude in HR round | — | HackerRank | — | [Glassdoor](https://www.glassdoor.co.in/Interview/BNY-Interview-E78-RVW98623513.htm) (2025) |
| **Samsung SRIB** | 3 coding in 70 min, no STL (2021–22 reports only) | 70 min | CoCubes | — | GFG (older) |

**Not covered:** IBM, HP, UBS, Sigmoid, ProcDNA, MAQ Software, Pace Stock Broking, Turing.

---

## Questions (topic-level)

### Quantitative aptitude
1. TSD and ratio/proportion word problems (time-consuming) — Qualcomm — Easy-Medium — [GFG Jul 2025](https://www.geeksforgeeks.org/interview-experiences/qualcomm-interview-experience-on-campus-3/)
2. Permutation and mixture problems — Qualcomm — Easy-Medium — GFG 2025
3. Multi-step mixes of TSD, profit-loss, time-work, ratios, number systems, P&C — DE Shaw — Hard — [GFG](https://geeksforgeeks.org/de-shaw-recruitment-process)
4. Probability, P&C, fast arithmetic — Goldman Sachs — Easy-Medium (time-pressured) — placementpreparation.io 2025
5. Number systems, percentages/ratios — SAP Labs — Easy-Medium — snippet 2025
6. Probability and P&C MCQs, ~30 min for 15 Qs, very difficult — DE Shaw — Hard — LeetCode snippets 2022–24

### Logical reasoning
1. 25 pattern-recognition Qs in 5 min — ZS Associates — Easy-Medium (speed)
2. Direction sense, blood relations, arrangements — ZS Associates — Easy-Medium
3. Abstract figure series, diagrammatic/flowchart reasoning — Goldman Sachs — Easy-Medium
4. Logic-gate reasoning — Goldman Sachs — Easy-Medium
5. Data sufficiency — Axtria — Easy-Medium — [GFG](https://www.geeksforgeeks.org/?p=1186549)
6. Blood relations in a 20-MCQ/30-min test — General (Accolite) — Easy-Medium — [GFG](https://www.geeksforgeeks.org/interview-experiences/accolite-interview-experience-set-3-on-campus/)

### Verbal
1. RC passages + sentence correction — Goldman Sachs — Easy-Medium
2. "Contextual communication" section — Oracle Server Tech — Easy-Medium — [GFG Jul 2025](https://geeksforgeeks.org/oracle-on-campus-fte-server-technology)
3. Verbal analogies — SAP Labs — Easy-Medium

### Data interpretation
1. DI from bar, line, donut charts — Axtria — Easy-Medium to Hard
2. DI in aptitude section — Qualcomm — Easy-Medium
3. Numerical reasoning from graphs/tables + number series — Goldman Sachs — Easy-Medium
4. Standalone DI section — ZS Associates — Easy-Medium

### CS fundamentals
1. C output prediction / error finding with bitwise ops — Qualcomm — Easy-Medium
2. Quicksort/mergesort behaviour and complexity MCQs — Qualcomm — Easy-Medium
3. Tree operations and flowchart tracing MCQs — Oracle Server Tech — Easy-Medium
4. OS scheduling, normalisation, OOP MCQs — SAP Labs — Easy-Medium
5. SQL JOIN / GROUP BY / HAVING — SAP Labs — Easy-Medium
6. Program output + Git, cloud, SQL MCQs — Axtria — Easy-Medium
7. C-language core MCQs — Mastercard — Easy-Medium (Nov 2025)
8. DBMS, OS, CN, OOP MCQs — Deutsche Bank — Easy-Medium
9. SQL, OS, C++ OOP, DS + systems MCQs — DE Shaw — Hard
10. C++/Java fundamentals MCQs — Cadence — Easy-Medium (2023)
11. Digital electronics + some architecture and C — Texas Instruments — Easy-Medium
12. Heap MCQs incl. expected values and running times — Adobe — Hard — [GFG](https://www.geeksforgeeks.org/interview-experiences/adobe-interview-set-13-campus-internship/) (older)

### Quant-firm style
1. Expected-value/probability MCQs tied to heaps — Adobe — Hard (older)
2. Simple probability in short MCQ test — General (Accolite) — Easy-Medium (older)
3. CCAT speed cognitive test (math, verbal, spatial in 15 min) — Trilogy — Hard (speed)

**Coverage:** verbal, DI and quant-firm are very thin; logical and quant are topic-level only; CS fundamentals is best covered.

---

## Good resources (free)
1. [IndiaBix](https://www.indiabix.com) — topic-wise quant, logical, verbal, DI with solutions
2. [GFG Aptitude](https://www.geeksforgeeks.org/aptitude-questions-and-answers/) — theory + practice
3. [GFG 90 Most Asked Aptitude & Reasoning](https://www.geeksforgeeks.org/interview-experiences/90-most-asked-aptitude-and-reasoning-questions-in-interviews/) — quick revision
4. [GFG Puzzles](https://www.geeksforgeeks.org/puzzles/) — classic brainteasers (DE Shaw, GS, Adobe)
5. [Brainstellar](https://brainstellar.com) — graded probability/EV/logic puzzles
6. [TraderMath brainteasers](https://www.tradermath.org/brainteasers) — quant brainteasers + mental math
7. [QuantVault](https://quantvault.org/probability-interview-questions.html) — probability/EV with solutions
8. [LeetCode Top SQL 50](https://leetcode.com/studyplan/top-sql-50/) — SQL practice
9. [GFG interview experiences](https://www.geeksforgeeks.org/interview-experiences/) — first-hand OA reports
10. [GFG Last Minute Notes](https://www.geeksforgeeks.org/last-minute-notes-lmns/) — OS, DBMS, CN revision
11. Gate Smashers / Neso Academy (YouTube) — OS, DBMS, CN, digital electronics
12. [Sanfoundry](https://www.sanfoundry.com) — C/C++/Java output-prediction MCQs
13. [Criteria Corp CCAT prep](https://www.criteriacorp.com/candidates/ccat-prep) — for Trilogy
14. [Jointaro](https://www.jointaro.com/interviews/companies/oracle/) / 1point3acres — recent dated OA reports

---

# Addendum (late helper reports)

"Int" = asked in an interview round, not the OA.

## Additional OA patterns
- **Deutsche Bank** (TDI intern, Jul 2025): 10 CS MCQs (OOP/DBMS/OS/CN/SQL, 4 marks each) + 2 coding (one LC-hard). No negative marking. [LeetCode](https://leetcode.com/discuss/interview-experience/6999473)
- **Goldman Sachs** Engineering Analyst: 15 CS MCQs / 30 min, 2 DSA / 40 min, 2 subjective / 15 min, HackerRank. [papersadda Aug 2025](https://papersadda.com/article/goldman-sachs-analyst-campus-2025-10hour-marathon-selected/) (aggregator). Aptitude round 70 Qs / 120 min, +5/−2: [GFG](https://geeksforgeeks.org/goldman-sachs-interview-experience-for-internship-off-campus)
- **DE Shaw** MTS (Jan 2025): 3 DSA, 10 math/probability MCQs (combinatorics, Bayes, geometric probability, expectation, binomial/Poisson), 10 CS MCQs. [papersadda](https://papersadda.com/article/de-shaw-mts-india-jan-2025-quant-dsa-selected/) (orig. leetcode post 6754544). Systems Engineer intern: 45 min, 17/109 shortlisted. [GFG Jul 2024](https://geeksforgeeks.org/de-shaw-group-interview-experience-systems-engineer-intern)
- **Arcesium**: 15 tech + 15 aptitude MCQs + 2 coding, HackerRank; one-way navigation, negative marking on MCQs. [GFG Jul 2025](https://geeksforgeeks.org/arcesium-interview-experience-for-software-engineer)
- **Qualcomm** intern: 3 × 20 Qs, 30 min each; programming covers C output, bits, malloc, trees, OS; +1/−0.25. [GFG Jul 2025](https://geeksforgeeks.org/qualcomm-internship-interview-experience-on-campus)
- **Adobe** intern: 30 MCQs (aptitude, DSA, OOP, OS, CN) + 2 coding. [GFG Jul 2025](https://www.geeksforgeeks.org/?p=1099039)
- **Amazon** SDE intern (India): 2 coding + 10 CS MCQs, HackerRank. [LeetCode](https://leetcode.com/discuss/post/8415292/)
- **Nutanix** MTS-1: 2 coding + SQL, Linux, DSA MCQs, HackerRank. [LeetCode Jul 2025](https://leetcode.com/discuss/interview-experience/6951560)
- **UBS**: 2 DSA + 10 aptitude + 5 CS MCQs / 90 min ([GFG Oct 2023](https://www.geeksforgeeks.org/?p=1092776)); other reports: 39 MCQs + 1 coding (2025), or 50 MCQs + 1 coding ([interview-insights](https://interview-insights.onrender.com/articles/ubs-on-campus-interview-experience))
- **IBM**: 25 CS MCQs + 3 DSA, HackerRank (Glassdoor snippet, 2025)
- **Intuit** (New Delhi campus): normalisation, SQL 2nd-highest GPA, monotonic stack. [Glassdoor Aug 2025](https://www.glassdoor.com.au/Interview/Intuit-Interview-E2293-RVW99414191.htm)
- **ZS Associates** (first-hand, Mettl, 6 timed sections, no switching): Logical 25 Qs / 5 min; Analytical 8 / 15 min; Unstructured problem solving 2 case studies / 15 min (hard); Numerical 8 / 15 min; Critical thinking + verbal (error spotting, sentence order, verb forms, synonyms). [GFG Oct 2024](https://www.geeksforgeeks.org/?p=1050607). DAA variant with attention-to-detail and guesstimates: [GFG Aug 2024](https://geeksforgeeks.org/zs-associates-interview-experience-daa-on-campus)
- **Axtria**: 70 Qs / 90 min on HirePro. [GFG](https://geeksforgeeks.org/axtria-interview-experience-off-campus)
- **Tiger Analytics**: ~20 aptitude (40 min), ~10 CS (10 min), 2 coding on iMocha. [GFG ~Dec 2024](https://www.geeksforgeeks.org/?p=1118860)
- **American Express** analytics (IITK): aptitude, case study, ML MCQs. [IITK SPO Jul 2024](https://spo.iitk.ac.in/insights/2024-intern-snehal-shridhar-kane-american-express)
- **Mu Sigma**: muAPT 28 Qs + 5 GK / 45 min, adaptive, no negative marking. [prepinsta](https://prepinsta.com/mu-sigma/) (aggregator)
- **Sigmoid**: 15 reasoning MCQs + DSA problems (2025). [Substack](https://athenasquare.substack.com/p/sigmoid-interview-experience)
- **MAQ Software**: 28 CS MCQs + 2 coding (code360/Glassdoor snippets)
- **ProcDNA**: aptitude, then case study (7 Qs, Python/SQL) (Glassdoor snippet)
- **Turing** Data Analyst (on-campus): 18 aptitude MCQs (LR, quant, DI) / 60 min, then Python challenge + RLHF task. [GFG Dec 2024](https://geeksforgeeks.org/turing-interview-experience-for-data-analyst-on-campus)
- **Quant firms:**
  - Optiver: games test incl. "80 in 8" mental math. [IITK SPO](https://spo.iitk.ac.in/insights/2024-intern-aniruddh-pramod-optiverquant-role)
  - WorldQuant: 50 probability/stats Qs / 3 h. [IITK SPO](https://spo.iitk.ac.in/insights/2024-placement-hitesh-anand-world-quant)
  - Tower Research: coding, probability, puzzles, hardware. [IITK SPO](https://spo.iitk.ac.in/insights/2024-intern-talin-gupta-tower-research-capital)
  - AlphaGrep: puzzle rounds + ~8–9 probability Qs. [IITK SPO](https://spo.iitk.ac.in/insights/2024-intern-mihir-r-deshpande-alphagrep-securities-private-limited)
  - Graviton, Quadeye, NK Securities: aggregator-only patterns.
- **Pace Stock Broking**: no data anywhere.

## Additional questions

### Quant-firm style
1. Quadratic with b, c ~ U[-1,1]: P(real roots) — Goldman Sachs — Hard — GfG snippet (~2021)
2. HHT vs HTH race: P(HHT first) — GS — Hard — pre-2024
3. Two people arrive at random times: P(meet) — GS — Easy-Medium
4. Expected double sixes rolling two dice — GS — Easy-Medium — code360 snippet
5. Rod broken into 3: P(triangle) — GS; also Tiger Analytics (Int) — Hard — IIT Bhubaneswar PDF 2024
6. Cow tethered to a pole, rope length / area — GS — Easy-Medium
7. m×m grid of coins, every row and column even — WorldQuant (Int) — Hard — IITK Aug 2024
8. 100^99 vs 99^100 — WorldQuant (Int) — Easy-Medium
9. "80 in 8" mental math — Optiver OA — Easy-Medium
10. Two players draw cards and guess the other's: maximise min success probability — NK Securities (Int) — Hard — aggregator
11. Two-state Markov weather chain: long-run P(sun) — Tiger (Int) — Hard — IIT Bhubaneswar 2024
12. Two dice: P(sum > 10) — Tiger (Int) — Easy-Medium
13. Trailing zeros of N! — Tiger (Int) — Easy-Medium
14. Ants on triangle corners: P(no collision) — Axtria OA — Easy-Medium
15. P(at least one head in 2 tosses) — GS — Easy-Medium — [GFG](https://www.geeksforgeeks.org/?p=1044277)
16. Normal distribution properties — AlphaGrep (Int) — Easy-Medium
17. Take 1–3 marbles, last wins (multiples of 4 lose) — General — Easy-Medium — aggregator

DE Shaw MCQ topics: Bayes, geometric probability, expectation, binomial/Poisson (Jan 2025, aggregator).

### CS fundamentals
1. SQL 2nd-highest GPA — Intuit OA — Easy-Medium
2. Normalisation — Intuit OA — Easy-Medium
3. C bit-manipulation and output (~70% of programming section) — Qualcomm OA — Hard
4. malloc and error-finding MCQs — Qualcomm OA — Easy-Medium
5. Flowchart: fill in the missing box — Oracle OA — Easy-Medium
6. AVL/BST insert-delete traversal, red-black tree MCQs — Oracle OA — Hard — leetcode 814592 (older)
7. Function-pointer output in C — Texas Instruments OA — Hard
8. Diamond inheritance (which print() runs; virtual inheritance) — DE Shaw (Int) — Hard — LeetCode 6637806, Apr 2025
9. Stack vs heap object allocation — DE Shaw (Int) — Easy-Medium
10. Deadlock conditions; write a mutex deadlock — DE Shaw (Int) — Hard
11. vtable and vptr — Arcesium (Int) — Hard
12. Can a static method be overridden? — Media.net (Int) — Hard — LeetCode 7088818, Aug 2025
13. Referential integrity — Media.net (Int) — Easy-Medium
14. TCP vs UDP — Media.net (Int) — Easy-Medium
15. Union vs struct sizeof — Qualcomm (Int) — Easy-Medium
16. Swap even and odd bits — Qualcomm (Int) — Easy-Medium
17. Detect integer overflow — Qualcomm (Int) — Easy-Medium
18. Meaning of volatile — Texas Instruments (Int) — Easy-Medium
19. Highest salary per department — UBS (Int) — Easy-Medium
20. fork() in a loop: count processes; LRU page-fault count — General — Easy-Medium — GfG/GATE

### General practice items (from ZS / Mu Sigma prep pages — not reported as actually asked)
Sources: prepinsta.com/zs-associates-paper/, faceprep ZS and Mu Sigma papers, prepinsta.com/mu-sigma/logical-reasoning-questions/
- **Quant (~19):** train speed ratio from meeting point; sugar mixture to target cost; greatest 6-digit multiple of 12; successive percentage expenses; two workers with rest days; clock gaining time; markup after discount; committee selection with constraint; coloured-ball selection; ages at equal intervals; average speed at 60/40 km/h (48); train crossing a bridge; P(both balls red); income/savings ratio; pentagon angle; boys-to-girls percentage; cars meeting 110 km into a 200 km gap; work done in 12 days; boats in stream + simple interest.
- **LR (~20):** wrong term in series; blood relations; linear and circular seating; ordering; APPLE→BQQMF coding; series 2, 6, 12, 20, 30; syllogisms; flowchart box value; statement and conclusion; letter series RQP, ONM, LKJ.
- **DI (15):** state-qualifier table (5 Qs); branch sales over years (5); budget pie chart; quarterly profit margin; IT-company market-share table (3).

**Coverage now:** Quant, LR, DI each >12 (mostly general practice). CS ~20 company-tagged (OA + Int). Quant-firm ~17. Verbal still thin (one concrete item).

## How to get more
- LeetCode Discuss post text: POST https://leetcode.com/graphql with `ugcArticleDiscussionArticle(topicId:"<id>"){title content createdAt}` (see `leetcode_index/lc.py`).
- [IIT Kanpur SPO Insights](https://spo.iitk.ac.in/insights) has 2025–26 intern write-ups (Graviton, Quadeye, Tower, GS Quant, DE Shaw TD, Squarepoint, WorldQuant, AlphaGrep, Optiver; also EXL, Fractal, Amex). Several were downloaded to this session's tool-results folder but not parsed.
