# DSA OA Questions — Web Research (collected 2026-10-01)

Partial report — stopped early on request. About 40 question entries; most companies have no question-level data yet.

Why thin: WebFetch gets 403 on leetcode.com/discuss. LeetCode's public GraphQL endpoint does return post bodies; ~1,500 recent discuss posts (2024-09 onward) were indexed by title only. See `leetcode_index/` in this folder (`lc.py` with `search(keyword)` / `fetch(topicId)`, and `index.json`).

Key: **[T]** = title only (body not read). **[U]** = uncertain date or source.

---

## Trends
1. **Samsung SRIB SWC test:** usually 1 problem in 3 hours; C, C++ or Java only (no Python); all ~50 test cases must pass. Problems repeat from a known list of ~30 on GitHub. Another format: 3 problems in 70 min. [GFG](https://www.geeksforgeeks.org/?p=489874), [LeetCode](https://leetcode.com/discuss/interview-experience/2249873/) (2022; format reported still current in Jan 2025, post 6315004)
2. **Qualcomm campus OA is all MCQ, no coding:** HirePro, 60 Qs / 90 min, three 30-min sections — aptitude, C/C++ (pointers, struct/union, static/extern, output prediction), CS core (OS, DSA). +1 / −0.25. Coding only in interviews. [GFG](https://www.geeksforgeeks.org/?p=1115092) (2023)
3. **D. E. Shaw:** OA is 3 coding Qs on HackerRank, mostly DP and maths. Interviews add graphs, divide and conquer, heaps, two pointers, binary lifting, knapsack variants, bit manipulation, plus SQL/OOP/OS. [jointaro Jul 2025](https://www.jointaro.com/interviews/companies/de-shaw/experiences/software-engineerinternship-hyderabad-july-1-2025-no-offer-positive-176d46d3/)
4. **Turing:** 45-min screen — a LeetCode-medium DSA problem, an LLM-response evaluation task, and a REST API question. Data Analyst roles: 6 SQL + 1 Python. [Glassdoor](https://fr.glassdoor.ca/Entretien/Turing-Entretien-E2462330-RVW95299538.htm) (~2025)
5. **HiLabs:** LeetCode-medium OA, then 2 virtual interviews (simple DSA: two pointers, binary search). DS track adds ML basics + ML case study. [code360](https://www.naukri.com/code360/interview-experiences/hilabs/interview-experience-on-campus-nov-2022-2-6952), [IITK SPO 2024](https://spo.iitk.ac.in/insights/2024-placement-abu-kashan-hilabs)
6. **Navi:** OA mixes aptitude, CS MCQs and coding; then 2 × 45-min interviews (DSA, DBMS/B-trees, light design) and HR. [Glassdoor](https://www.glassdoor.co.in/Interview/Navi-Interview-E3291445-RVW50979341.htm) (date unclear)
7. **D. E. Shaw interviews moving toward design-flavoured DSA** (streaming top-K leaderboard), with system design in round 3. [LeetCode May 2025](https://leetcode.com/discuss/post/6637806/)

---

## Questions by company

### D. E. Shaw
| # | Problem (paraphrased) | Closest LC/CF | Tags | Diff | Round | Source | Date |
|---|---|---|---|---|---|---|---|
| 1 | Stream of `{user: solvedCount}` updates; always show current top 10 | LC 1244 Design A Leaderboard (similar) | heap, ordered set, design | Med | Interview R1 | [post](https://leetcode.com/discuss/post/6637806/) | May 2025 |
| 2 | Can matrix A become B by transposing any k×k square submatrix (k ≥ 2)? Compare multisets on each anti-diagonal | CF 1136C Nastya Is Transposing Matrices | matrix, hashing | Med | Interview R2 | same | May 2025 |
| 3 | OA questions (linked, not read) | – | – | – | OA | [post](https://leetcode.com/discuss/post/6396883/) | ~Feb 2025 |
| 4 | Max occurrences of s as a subsequence of t after inserting exactly one char [U] | LC Maximum Number of Subsequences After One Inserting | strings, prefix counts | Med | pool | jointaro | [U] |
| 5 | Binary Tree Cameras [U] | LC 968 | trees, greedy DP | Hard | pool | jointaro | [U] |
| 6 | Min taps to water a garden [U] | LC 1326 | greedy, intervals, DP | Hard | pool | jointaro | [U] |
| 7 | 2D-array problem, priority-queue problem, college-system SQL query | – | matrix, heap, SQL | Med | Interview R1 | jointaro | Jul 2025 |
| 8 | "Interesting Sorting Problem" [T] | – | sorting | ? | OA | [post](https://leetcode.com/discuss/post/6966382/) | Jul 2025 |
| 9 | "DE Shaw OA question" [T] | – | – | – | OA | [post](https://leetcode.com/discuss/post/6679860/) | Apr 2025 |
| 10 | "DE SHAW OA Question" [T] | – | – | – | OA | [post](https://leetcode.com/discuss/post/6077737/) | Nov 2024 |
| 11 | "DE Shaw OA Sep 2024 (Q2?)" [T] | – | – | – | OA | [post](https://leetcode.com/discuss/post/5818917/) | Sep 2024 |
| 12 | "SMT Online Coding Assessment" [T] | – | – | – | OA | [post](https://leetcode.com/discuss/post/7647119/) | Mar 2026 |

### Samsung SRIB
| # | Problem | Closest | Tags | Diff | Round | Source | Date |
|---|---|---|---|---|---|---|---|
| 1 | n cards with number + suit; pick k to maximise (sum of numbers + Σ over suits of count²) [U] | – | greedy, sorting, DP | Med-Hard | OA | search result | ~2025 [U] |
| 2 | Check whether a graph is bipartite; all ~50 tests must pass | LC 785 | graph, BFS/DFS | Med | SWC OA | [GFG](https://www.geeksforgeeks.org/?p=489874) | older |
| 3 | Sort rows of a 2D array; trim a BST to a range | LC 669 | trees, sorting | Easy-Med | OA | GfG cluster | older [U] |
| 4 | Left view of binary tree; sum tree; count nodes whose left-subtree sum exceeds a threshold | GfG Left View, Sum Tree | trees | Easy-Med | OA | GfG SRIB posts | older [U] |
| 5 | Number of Islands | LC 200 | graph | Med | coding | [jointaro Nov 2025](https://www.jointaro.com/interviews/companies/samsung/work-experiences/software-developer-november-4-2025-2-717c8704/) | Nov 2025 |
| 6 | Burst Balloons | LC 312 | interval DP | Hard | coding | same | Nov 2025 |
| 7 | Longest Increasing Subsequence | LC 300 | DP, binary search | Med | coding | same | Nov 2025 |
| 8 | Coin Change (min coins) [U] | LC 322 | DP | Med | OA | [placementpapers](https://placementpapers.app/samsung/2025/) | 2025 |
| 9 | Merge Intervals, Top K Frequent, Longest Substring w/o Repeat, Valid Parentheses, Level Order, Linked List Cycle [U, generic] | LC 56/347/3/20/102/141 | mixed | Easy-Med | OA | same | 2025 |
| 10 | "SWC Professional Test, SRI-B, OA" [T] | – | – | Hard | OA | [post](https://leetcode.com/discuss/post/6315004/) | Jan 2025 |
| 11 | "Samsung OA Question" [T] | – | – | – | OA | [post](https://leetcode.com/discuss/post/6062481/) | Nov 2024 |
| 12 | "Samsung coding question" [T] | – | – | – | OA | [post](https://leetcode.com/discuss/post/7586852/) | Feb 2026 |

### Navi
Source: [Glassdoor](https://www.glassdoor.co.in/Interview/Navi-Interview-E3291445-RVW50979341.htm). Dates uncertain, possibly pre-2024.
| # | Problem | Closest | Tags | Diff | Round |
|---|---|---|---|---|---|
| 1 | Rod cutting | GfG Rod Cutting | DP | Med | OA |
| 2 | Merge intervals | LC 56 | sorting, intervals | Med | OA |
| 3 | Spiral traversal | LC 54 | matrix | Med | OA |
| 4 | Palindrome after deleting ≤1 char | LC 680 | two pointers | Easy | OA / interview |
| 5 | Number of islands | LC 200 | graph | Med | OA / interview |
| 6 | Longest valid parentheses | LC 32 | stack, DP | Hard | Interview |
| 7 | Course Schedule II | LC 210 | graph, topo sort | Med | Interview |

### Qualcomm
Source: [GFG](https://www.geeksforgeeks.org/?p=1115092) (2023).
| # | Problem | Closest | Tags | Diff | Round |
|---|---|---|---|---|---|
| 1 | Detect cycle in linked list | LC 141 | linked list | Easy | Interview |
| 2 | Find missing and repeating number | GfG Missing & Repeating | math, bits | Med | Interview |
| 3 | Bit-masking problems | – | bit manipulation | Easy-Med | Interview |

### Turing
| # | Problem | Tags | Diff | Round | Source | Date |
|---|---|---|---|---|---|---|
| 1 | LC-medium DSA + LLM-response evaluation + REST API task (45 min) | mixed | Med | OA | [Glassdoor](https://fr.glassdoor.ca/Entretien/Turing-Entretien-E2462330-RVW95299538.htm) | ~2025 |
| 2 | Basic Python list/string/loop problem | strings, arrays | Easy | OA | Glassdoor | ~2025 |
| 3 | DSA + recursion coding activity | recursion | Med | OA | [Glassdoor](https://www.glassdoor.com.ar/Entrevista/Online-coding-activity-question-based-on-programming-concepts-related-to-data-structures-and-recursion-e-t-c-QTN_8630249.htm) | [U] |
| 4 | "Turing.com OA Turing Question" [T] | – | – | OA | [post](https://leetcode.com/discuss/post/7199394/) | Sep 2025 |

### HiLabs
| # | Problem | Closest | Tags | Diff | Round | Source | Date |
|---|---|---|---|---|---|---|---|
| 1 | Can the graph be coloured with ≤ m colours? | GfG M-Coloring | graph, backtracking | Med | OA / interview | [code360](https://www.naukri.com/code360/interview-experiences/hilabs/interview-experience-on-campus-nov-2022-2-6952) | Nov 2022 |
| 2 | "HiLabs SDE: Online Assessment Problem" [T] | – | – | – | OA | [post](https://leetcode.com/discuss/post/5929340/) | Oct 2024 |
| 3 | DS track: two pointers, binary search, then ML basics + ML case study | – | – | Easy-Med | Interview | [IITK SPO](https://spo.iitk.ac.in/insights/2024-placement-abu-kashan-hilabs) | 2024 |

### Google [T]
- "Find Number of Quadruplets" (hashing) — [post](https://leetcode.com/discuss/post/6059263/) (Nov 2024)
- "System Goodness" — [post](https://leetcode.com/discuss/post/6298653/) (Jan 2025)
- STEP internship India 2025 — [post](https://leetcode.com/discuss/post/7478960/) (Jan 2026)
- Winter Intern 2025 interview questions — [post](https://leetcode.com/discuss/post/5972942/) (Oct 2024)

### IBM [T]
- Strings "similar" if every char frequency differs by ≤3 — closest LC 2068 (strings, hashing, Easy) — [post](https://leetcode.com/discuss/post/8499672/) (Sep 2026)
- "Extraordinary Substring" — [post](https://leetcode.com/discuss/post/5819392/) (Sep 2024)
- On-campus OA, 2 coding problems — [post](https://leetcode.com/discuss/post/8500776/) (Sep 2026)

### Adobe [T]
- "Drone Physics / OOP Problem" (simulation/OOP) — [post](https://leetcode.com/discuss/post/8454611/) (Aug 2026)

### No question-level data yet
Microsoft, Apple, Uber, LinkedIn, Atlassian, Salesforce, DevRev, Trilogy, Flipkart, Myntra, Meesho, PhonePe, Groww, Zepto, Dream11, Gameskraft, ThoughtSpot, Zscaler, Motorq, UiPath, Amazon, Expedia, Visa, Mastercard, PayPal, Goldman Sachs, Cadence, Texas Instruments, Oracle, SAP Labs, HP, Pace, Deutsche Bank, UBS, BNY Mellon. (Motorq and HP: no recent LeetCode posts at all. DevRev, Gameskraft, Trilogy, Pace, BNY: 1–4 posts each.)

---

## Topic frequency (small sample — weak evidence)
1. Graphs (BFS/DFS, bipartite, islands, topo sort, colouring)
2. DP (interval DP, LIS, coin change, rod cutting, knapsack variants)
3. Trees
4. Intervals and greedy
5. Heaps and ordered sets
6. Strings and two pointers
7. Matrix tricks / invariants
8. Bit manipulation and math
9. Stack
10. Linked lists
11. Binary search

---

## Unread LeetCode posts worth fetching next
URL: `https://leetcode.com/discuss/post/<ID>/` (use `fetch(ID)` in `leetcode_index/lc.py`)

| Company | Post IDs |
|---|---|
| Uber | 7606523, 7515097, 7251112, 7240446, 6849478, 6397193, 6149783 |
| LinkedIn | 7151239 |
| Salesforce | 6933121, 6803085, 6713417, 6641581 |
| Flipkart | 6957919, 6652871, 6384688 (GRiD 6.0) |
| Meesho | 7295631 (on-campus OA), 6691332, 6100369 |
| PhonePe | 8444588, 5968172 |
| Groww | 8392012 |
| ThoughtSpot | 6004629 |
| Microsoft | 7609045, 6455775, 6148845 |
| Apple | 5855235 |
| Amazon | 8545250, 6434202, 5966700 |
| Expedia | 7138563, 6511995 |
| Visa | 8148971, 7581694, 6819912 |
| Mastercard | 8498096 |
| PayPal | 6053000, 5912130 |
| Goldman Sachs | 6714007, 6618696 |
| SAP Labs | 5774469 |
| Pace | 5934003 |
| UBS (ML) | 7324832 |
| Samsung | 6315004 |
| HiLabs | 5929340 |
| D. E. Shaw | 6396883, 6966382, 5757058 |
