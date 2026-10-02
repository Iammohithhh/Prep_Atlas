"""Reviewed additions from the archive. OCR is checked against source images.

Source references remain private in build/raw; public compilation strips them.
"""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
manifest=json.loads((ROOT/'build/manifest.json').read_text(encoding='utf-8'))
questions=[]
skipped=[]

def file(company, suffix):
    matches=[p for p in manifest[company] if p.endswith(suffix)]
    if len(matches)!=1:raise ValueError((company,suffix,len(matches)))
    return matches[0]

aliases=[]

def add(key,company,title,statement,answer,explanation,*,topic='quant',section='aptitude',options=None,sources=(),hard=False,notes=None,confidence='high',type=None,**extra):
    if any(q['id']=='curated-local-'+key for q in questions):raise ValueError('duplicate key '+key)
    q=dict(id='curated-local-'+key,company=company,also_asked_by=[],section=section,subsection=topic,topics=[topic],pattern=key,
           difficulty='hard' if hard else 'easy-medium',type=type or ('mcq' if options else 'numeric'),title=title,statement=statement,
           source_files=[file(company,s) for s in sources],explanation=explanation,**extra)
    if answer is not None:q.update(answer=answer,answer_source='solved',answer_confidence=confidence)
    if options:q['options']=options
    if notes:q['notes']=notes
    questions.append(q)


def merge(key, company, sources):
    q=next(q for q in questions if q['id']=='curated-local-'+key)
    if company!=q['company'] and company not in q['also_asked_by']:
        q['also_asked_by'].append(company)
    for suffix in sources:
        path=file(company,suffix)
        if path not in q['source_files']:q['source_files'].append(path)


def skip(company, suffix, reason):
    skipped.append(dict(file=file(company,suffix),reason=reason))


def alias(existing_id, company, sources):
    """Attach repeat screenshots to ANY existing public question id (raw batches, curated or web)."""
    aliases.append(dict(id=existing_id,company=company,source_files=[file(company,s) for s in sources]))


def resolve(company, suffix):
    """Remove a previous skip once that source's specific uncertainty is handled."""
    path=file(company,suffix)
    skipped[:]=[s for s in skipped if s['file']!=path]


add('prime-factors','Fractal','Distinct prime factors of 52,500',
    'How many prime numbers between 1 and 175 are factors of 52,500?', '4',
    '52,500 = 2² × 3 × 5⁴ × 7. Its distinct prime factors are 2, 3, 5 and 7, all between 1 and 175.',
    sources=['20240908_103807.jpg'])
add('garden-perimeter','Fractal','Length of a rectangular garden',
    'A rectangular garden is five times as long as it is wide. If 2,160 yards of fencing, including the gate, completely enclose the garden, what is its length in yards?', '900',
    'Let width be w and length 5w. Then 2(w+5w)=2,160, so w=180 and length=900 yards.',
    options=['850','900','750','800','1000'],sources=['IMG-20240908-WA0055.jpeg','IMG-20240908-WA0057.jpeg'])
add('labelled-die','Axtria','Two rolls with the same face label',
    'A cubical die is marked x on three faces, y on two faces and z on the remaining face. If the die is rolled twice, what is the probability that the first and second rolls show the same label?', '7/18',
    'Assuming a fair die and independent rolls, P(same)=(3/6)²+(2/6)²+(1/6)²=14/36=7/18.',
    options=['7/18','1/6','13/36','11/18'],sources=['IMG_20240914_162727188_HDR_AE.jpg'])
add('reverse-array','Axtria','Identify a two-pointer array operation',
    'What does this function do?\n\n```cpp\nvoid Test(int arr[], int start, int end) {\n    while (start < end) {\n        int temp = arr[start];\n        arr[start] = arr[end];\n        arr[end] = temp;\n        start++;\n        end--;\n    }\n}\n```', 'Reverse the array.',
    'The function swaps symmetric elements and moves the two indices towards the centre. It reverses the inclusive subarray arr[start…end]; it reverses the entire array when the caller passes its first and last indices. O(end−start+1) time and O(1) space.',
    section='dsa',topic='two-pointers',options=['Traverse each alternate elements of the array.','Swap all alternate elements of the array.','Traverse each and every elements of the array.','Reverse the array.'],
    sources=['IMG_20240914_162156765_HDR_AE.jpg','IMG_20240914_162234882_HDR_AE.jpg'])

arp='arpwood capital (1).pdf'
add('digit-sum-chain','Arpwood Capital','Minimum digits in a repeated digit-sum chain',
    'For a natural number n, define f(n) as the sum of its digits. A natural number k satisfies f(f(f(f(k))))=1 and\n\nk > f(k) > f(f(k)) > f(f(f(k))) > 1.\n\nWhat is the least number of digits that k can have?', '23',
    'The smallest value greater than 1 whose digit sum is 1 is 10. The smallest larger number with digit sum 10 is 19; the smallest larger number with digit sum 19 is 199. Thus f(k)≥199, requiring at least ceil(199/9)=23 digits. A 23-digit number with digit sum 199 exists, for example 22 nines followed by 1, so the lower bound is attainable.',
    options=['21','22','23','24'],sources=[arp],hard=True)
add('consecutive-hh','Arpwood Capital','Expected overlapping HH pairs',
    'A coin is tossed eight times and the outcomes are written as a string. What is the expected number of occurrences of HH? Overlaps count: HHH contains two occurrences of HH.', '7/4',
    'Assuming independent fair tosses, there are seven adjacent pairs. Each is HH with probability 1/4. By linearity of expectation, the expected count is 7/4; independence of overlapping pair indicators is not required.',
    options=['2','7/4','9/4','5/2'],sources=[arp])
add('conditional-reroll','Arpwood Capital','A die is rerolled only after 1, 2 or 3',
    'A fair six-sided die is rolled once. If the first result is 1, 2 or 3, the die is rolled a second time. What is the probability that the sum of all values rolled is at least 6?', '5/12',
    'A first roll of 6 succeeds directly: probability 1/6. First rolls 1, 2 and 3 need second rolls at least 5, 4 and 3, giving 2+3+4 favourable two-roll outcomes out of 36. Total = 1/6 + 9/36 = 5/12.',
    options=['10/21','2/3','5/12','1/8'],sources=[arp])
add('cube-divisor-count','Arpwood Capital','Which divisor counts can belong to a perfect cube?',
    'Numbers A, B, C and D have 22, 37, 53 and 66 positive factors respectively. Which of these could be a perfect cube?', 'A & B',
    'A perfect cube has prime exponents 3a, so its divisor count is a product of factors 3a+1, hence is 1 modulo 3. Counts 53 and 66 fail this necessary condition. Counts 22 and 37 are achievable by p²¹ and p³⁶, respectively.',
    options=['A & B','B & C','A, B & C','D'],sources=[arp],notes='A handwritten mark in the source selects a different answer. The solution here is derived independently.')
add('five-digit-multiple','Arpwood Capital','Five-digit multiples of 15 with distinct digits',
    'How many five-digit numbers with distinct digits, divisible by 15, can be formed from the digits 2, 3, 4, 5, 6 and 7?', '48',
    'Divisibility by 5 forces the last digit to be 5. The sum of all six available digits is 27. The omitted digit must be 3 or 6 so the five chosen digits sum to a multiple of 3. Each of these two choices has 4! arrangements for the first four positions: 2×24=48.',
    options=['36','48','60','96'],sources=[arp])
add('printed-digits','Arpwood Capital','Count printed 3s and 5s',
    'If every integer from 1,000 through 10,000 is printed once, how many occurrences of the digits 3 and 5 are printed in total?', '7400',
    'For either digit, the thousands place contributes 1,000 occurrences among 1,000…9,999. Each of the other three places contributes 900. Thus each digit appears 3,700 times and together they appear 7,400 times. The endpoint 10,000 adds neither digit.',
    options=['7960','7400','7680','7560'],sources=[arp])
add('coffee-tea-overlap','Arpwood Capital','Coffee and tea: inclusion–exclusion',
    'A survey finds that 63% of people like coffee and 76% like tea. Every person likes tea or coffee. What percentage likes both?', '39',
    'Using inclusion–exclusion, P(coffee ∩ tea)=63%+76%−100%=39%. The condition that everybody likes at least one drink is necessary for this exact value.',
    sources=[arp],notes='The source’s interval-style options are awkward; answer with the exact percentage.')
add('binomial-digit-product','Arpwood Capital','Repeated draws of digit pairs with product 18',
    'A number is selected uniformly from 00, 01, …, 99, with replacement. Event A occurs when its two digits have product 18. Four numbers are selected independently. What is the probability that A occurs at least twice?', '3553/390625',
    'The successful digit pairs are 29, 92, 36 and 63, so p=4/100=1/25. The count is Binomial(4,1/25). P(X≥2)=[6×24²+4×24+1]/25⁴=3553/390625.',
    options=['3553/390625','601/390625','3553/380625','601/380625'],sources=[arp])
add('ant-on-cube','Arpwood Capital','Expected random-walk steps across a cube',
    'An ant starts at one corner of a cube and moves only along its edges. At each corner it chooses one of the three outgoing edges uniformly at random. What is the expected number of edges traversed before first reaching the opposite corner?', '10',
    'Let E_d be the expected remaining steps at Hamming distance d from the target. E_0=0; E_3=1+E_2; E_2=1+(2/3)E_1+(1/3)E_3; E_1=1+(1/3)E_0+(2/3)E_2. Solving gives E_1=7, E_2=9 and E_3=10.',
    options=['7','8','9','10'],sources=[arp],hard=True,notes='The source has a handwritten tick at 9, but the Markov-chain equations give 10 from the opposite corner.')
add('uniform-ratio','Arpwood Capital','Ratio of two uniform random variables',
    'Let p and q be chosen independently and uniformly from (0,1). What is P(1 < p/q < 2)?', '1/4',
    'In the unit square, the region is q<p<min(2q,1). Its area is ∫₀¹⁄² q dq + ∫₁⁄₂¹ (1−q) dq = 1/8+1/8=1/4. Boundary events have probability zero.',
    options=['1/4','1/8','1/2','3/8'],sources=[arp])
add('lotus-doubling','Arpwood Capital','Lotus coverage doubles daily',
    'A pond initially has 25 lotuses, each covering one square foot. The pond has area 5,300 square feet, and each lotus doubles its covered area every day. After how many days is the pond completely covered?', '8 days',
    'After d days the total covered area is 25×2ᵈ. Seven days give 3,200 square feet, while eight give 6,400. The first day reaching at least 5,300 is day 8.',
    options=['6 days','7 days','8 days','9 days'],sources=[arp])

add('expedia-efficiency','Expedia','Maximum test-window efficiency',
    'Each test has an integer arrival time. Activate the testing environment once from time t₁ to t₂, inclusive; all tests arriving in this interval execute. Efficiency is the number of executed tests minus (t₂−t₁). At least two tests must execute. Return the maximum possible efficiency. Tests sharing an arrival time execute simultaneously, and efficiency may be negative.',None,
    'Sort arrival times a. For endpoints i<j, efficiency is j−i+1−a[j]+a[i] = (j+1−a[j])+(a[i]−i). Sweep j, maintaining the maximum a[i]−i over i<j. It suffices to activate at arrival endpoints. With repeated timestamps, starting earlier or ending later within a duplicate group only improves the count; the global optimum includes the whole group. O(n log n) time for sorting, O(n) space for a copy.',
    section='dsa',topic='sorting',type='coding',sources=['-1.jpg','expedia2.jpg'],
    function_signature='def getMaxEfficiency(arrivalTime)',constraints='2 ≤ n ≤ 2×10⁵; 1 ≤ arrivalTime[i] ≤ 10⁹.',
    examples=[{'input':'arrivalTime = [9, 1, 3, 5, 6]','output':'1','explanation':'Activate from 5 to 6: two tests minus one time unit gives efficiency 1.'}])
add('expedia-reorder','Expedia','Reorder layers by moving the last element',
    'Given lists current and desired representing the order of layers in a neural network, one operation takes the last element of current and inserts it at any position in the list. Determine the minimum number of operations needed to obtain desired. The source guarantees the transformation is possible.',None,
    'The elements never moved are a prefix of the original current list, and their relative order must survive in desired. Find the longest prefix of current that is a subsequence of desired; all remaining elements can be removed from the end and inserted in their required positions. The answer is n minus that prefix length. A greedy subsequence scan takes O(n) time and O(1) extra space.',
    section='dsa',topic='greedy',type='coding',sources=['expedia.jpg'],function_signature='def getMinSteps(current, desired)',
    examples=[{'input':'current = [2, 1, 3, 5, 4]\ndesired = [2, 4, 1, 5, 3]','output':'2','explanation':'Move 4 into position 2, then move the last element 5 before 3.'}],notes='The source image does not show the numeric constraints or an explicit uniqueness requirement.')
add('path-minimum','Adobe','Sum of minimum node weights over all tree paths',
    'Given an undirected tree on vertices 0…n−1, a weight for each vertex, and its edges, sum the minimum node weight on the simple path between every pair of distinct vertices. Count an unordered pair once: paths i→j and j→i are the same pair.',None,
    'Activate vertices in nonincreasing weight order. When activating a vertex of weight w, create its DSU component and union it with active neighbours. Unioning components of sizes a and b connects a×b previously disconnected unordered pairs whose path minimum is w, adding w×a×b. Equal weights can be processed in any order because their contribution has the same multiplier. O(n log n) for sorting and near-linear DSU work.',
    section='dsa',topic='graphs',type='coding',hard=True,sources=['IMG-20240719-WA0005.docx','IMG-20240719-WA0005.jpg','IMG-20240719-WA0006.jpg','IMG-20240719-WA0007.jpg','IMG-20240719-WA0008.jpg','IMG-20240719-WA0009.jpg'],
    examples=[{'input':'n = 4\nweight = [6, 3, 7, 5]\nedges = [[0, 1], [1, 3], [0, 2]]','output':'21'},{'input':'n = 5\nweight = [6, 1, 2, 5, 3]\nedges = [[0, 1], [1, 2], [0, 4], [2, 3]]','output':'13'}],notes='The exact upper bound on n is unclear in the image; it is not guessed here.')

add('cadence-memory','Cadence','Build a 2048×128 memory from 1024×64 blocks',
    'Design a 2,048-word on-chip memory with a 128-bit access width using predefined 1,024×64 memory modules. The top module has an 11-bit address, active-high enable, a write/read control (1 for write and 0 for read), 128-bit input/output data and a clock. Each block has a 10-bit address, active-low chip enable and an active-low write enable. Write Verilog or VHDL and explain the connections.',None,
    'Use four blocks: two banks for depth and two 64-bit blocks in parallel per bank for width. Addr[10] selects the bank; Addr[9:0] connects to every block. Split input data into upper/lower 64-bit halves. Gate active-low chip enables with MemEnable and bank selection, and invert the top write/read control for nWrEnable. Multiplex the selected bank’s two outputs into 128 bits. State the memory block’s synchronous-read latency before writing the output-selection logic.',
    section='cs',topic='computer-architecture',type='subjective',sources=['IMG-20241015-WA0016.jpeg'])
add('cadence-overlap-fsm','Cadence','FSM for two overlapping binary sequences',
    'Design a finite-state machine that detects both binary sequences 11011 and 11001. Overlapping occurrences must be detected. Explain the states and provide a state or transition diagram.',None,
    'Use states representing the longest suffix of the observed stream that is a prefix of either target pattern: empty, 1, 11, 110, 1101 and 1100. On each bit, append it, emit detection if a target completes, then retain the longest suffix that is still a valid prefix. This fallback preserves overlap. Specify whether your output is Mealy or Moore and show traces that include back-to-back and overlapping matches.',
    section='cs',topic='digital-electronics',type='subjective',sources=['IMG-20241015-WA0010.jpeg'],notes='The example input stream in the photo is unclear; the two target sequences are readable.')
add('cadence-div3','Cadence','Divide a clock by three with 50% duty cycle',
    'Design a sequential circuit that divides an input clock frequency by three. The output clock must have a 50% duty cycle. Support your design with a timing diagram.',None,
    'A 50% duty cycle at a period of three input cycles requires high and low intervals of 1.5 cycles each. A circuit using only input rising edges cannot place both transitions at those half-cycle boundaries. Use rising- and falling-edge state, or a suitable clock-generation primitive, and align the output transitions 1.5 input periods apart. Show the reset phase and explain generated-clock timing and glitch avoidance.',
    section='cs',topic='digital-electronics',type='subjective',sources=['IMG-20241015-WA0012.jpeg'])

add('ibm-subnet','IBM','Which addresses share a /28 subnet?',
    'Consider A = 201.119.1.30, B = 201.119.1.33 and C = 201.119.1.46. With subnet mask 255.255.255.240, which belong to the same subnet?', 'B and C',
    'The mask is /28, giving blocks of 16 addresses in the last octet. A belongs to 201.119.1.16/28 (16…31). B and C belong to 201.119.1.32/28 (32…47).',
    section='cs',topic='networks',options=['A and B','B and C','A, B and C','None'],sources=['IMG-20240830-WA0169.jpg'])
add('ibm-virtual-memory','IBM','Virtual memory and backing storage',
    'Which option best describes the concept of virtual memory in an operating system?', 'Secondary storage (e.g. hard disk) used as an extension of RAM',
    'The expected option describes a common use of virtual memory: pages may be backed by secondary storage when not resident in RAM. More precisely, virtual memory is an address-space abstraction with address translation, isolation and protection; it is not merely additional disk storage, and it can exist without swapping.',
    section='cs',topic='os',options=['Additional physical RAM','Secondary storage (e.g. hard disk) used as an extension of RAM','RAM allocated for system processes only','Memory reserved for graphics processing'],sources=['IMG-20240830-WA0172.jpg'])
add('ibm-btree','IBM','Maximum keys in a full B-tree',
    'What is the maximum number of keys in a B-tree of order 6 and height 4?', '7775',
    'Using order = maximum children and height = number of edges from root to leaf, there are five levels. Each node has at most five keys and six children. Maximum keys = 5(1+6+6²+6³+6⁴)=6⁵−1=7,775. If height means number of levels instead, the value would be 6⁴−1=1,295, so the height convention matters.',
    section='cs',topic='dbms',options=['7776','7775','16384','16383'],sources=['IMG-20240830-WA0180.jpg'],notes='The intended answer assumes height counts edges; the source does not explicitly define the height convention.')
add('oracle-virtual-address','Oracle','Why is a memory address called virtual?',
    'Why is a virtual memory address called virtual?', 'This memory address does not map to the actual memory cell that corresponds to the address number',
    'A virtual address is interpreted within a process address space and translated to a physical address by the memory-management unit. Its numeric value need not be the physical address of the backing cell. Applications use virtual addresses at runtime; some virtual addresses may be unmapped.',
    section='cs',topic='os',options=['This memory address does not map to the actual memory cell that corresponds to the address number','This memory is the same as physical memory','This memory cannot be accessed by applications at runtime'],sources=['IMG-20240730-WA0065.jpg'])
add('oracle-cap','Oracle','What does the CAP theorem describe?',
    'What does the CAP theorem describe with respect to distributed system design?', 'The trade-offs between consistency, availability, and partition tolerance',
    'During a network partition, a distributed system cannot guarantee both linearizable consistency and availability for every request. Partition tolerance describes functioning despite communication failures; the trade-off becomes relevant when a partition occurs. CAP consistency is not the same meaning as the C in ACID.',
    section='cs',topic='dbms',options=['The relationship between CPU and memory usage','The trade-offs between consistency, availability, and partition tolerance','The process of data encryption','The principles of object-oriented programming'],sources=['IMG-20240730-WA0070.jpg'])
add('oracle-hosts','Oracle','Purpose of /etc/hosts in Linux',
    'What is the use of the /etc/hosts file in Linux?', 'It contains the FQDN to IP address mappings',
    'The hosts file stores static mappings from IP addresses to hostnames, including fully qualified names and aliases. Whether it is consulted before DNS depends on the system’s name-service configuration, commonly /etc/nsswitch.conf. It is not the account database or a file inventory.',
    section='cs',topic='os',options=['It contains the list of all users','It contains a list of all files in the system','It contains the time and date information','It contains the FQDN to IP address mappings'],sources=['IMG-20240730-WA0072.jpg'])
add('oracle-having','Oracle','Filter groups in an SQL query',
    'Which SQL clause restricts returned groups to those for which a specified condition is true?', 'HAVING',
    'HAVING filters groups, typically after GROUP BY and aggregation. WHERE filters individual rows before aggregation. For example, GROUP BY department HAVING COUNT(*) > 5 retains departments with more than five rows.',
    section='cs',topic='sql',options=['WHERE','HAVING','DISTINCT','EXISTS'],sources=['IMG-20240730-WA0073.jpg'])
add('oracle-idempotent','Oracle','Idempotency in REST API design',
    'What does idempotency mean in REST API design?', 'The property that a method can be called multiple times without different outcomes',
    'An operation is idempotent when repeating an identical request has the same intended effect on server state as applying it once. Responses may differ: deleting an existing resource and then deleting it again may return different statuses while leaving the same final state. GET, PUT and DELETE have idempotent semantics; POST is not generally idempotent.',
    section='cs',topic='networks',options=['The ability of an API to handle multiple requests in parallel','The property that a method can be called multiple times without different outcomes','The capability of an API to update data','The feature of an API that allows it to delete resources'],sources=['IMG-20240730-WA0074.jpg'])
add('oracle-ring','Oracle','A failure in a basic ring topology',
    'In a ring-topology network, if one device fails, how does it affect the network?', 'All devices in the network are affected',
    'In the simple single-ring model assumed by this question, a device failure breaks the communication path and can affect the whole network. Real ring networks may use bypass mechanisms or a redundant second ring, so the answer is conditional on the basic topology.',
    section='cs',topic='networks',options=['Only the failed device is affected','All devices in the network are affected','Only the devices between which the failed device exists are affected','The network continues to function normally'],sources=['IMG-20240730-WA0075.jpg'])
add('oracle-arp','Oracle','Purpose of ARP',
    'What is the purpose of ARP (Address Resolution Protocol)?', 'Resolve an IPv4 address to a MAC address on the local link',
    'ARP discovers the link-layer address associated with an IPv4 address on the local broadcast domain. For a remote destination, the host normally resolves the next-hop router’s MAC address rather than the remote host’s. IPv6 uses neighbour discovery rather than ARP.',
    section='cs',topic='networks',type='subjective',sources=['IMG-20240730-WA0076.jpg'],notes='Only part of the option list is visible, so the cleaned prompt is presented as a short-answer question.')
add('oracle-c-macro','Oracle','Side effects in a MAX macro and printf',
    'Consider this C code. Can its output be determined reliably?\n\n```c\n#include <stdio.h>\n#define MAX(a,b) ((a) > (b) ? (a) : (b))\nint main(void) {\n    int x = 5, y = 10;\n    printf("%d %d %d\\n", MAX(x++, y++), x, y);\n    return 0;\n}\n```', 'Undefined behavior in C',
    'The macro repeats the chosen argument, but the more serious issue is the printf argument list: modifying x/y in one argument is unsequenced relative to reading them in other arguments. In C this is undefined behavior, so a numeric output option is not a portable answer. Evaluate side-effectful expressions in separate statements and use a function for max.',
    section='cs',topic='c-cpp-output',type='subjective',sources=['IMG-20240730-WA0067.jpg'],notes='Numeric source options do not provide a valid portable answer. The reconstructed C expression is analysed by language rules, not by one compiler run.')

add('hp-even-difference','HP','Longest subsequence with even adjacent-difference sum',
    'Choose a subsequence of an integer array and sort the chosen elements in increasing order. Sum the differences between each pair of adjacent sorted elements. Return the largest possible subsequence length for which this sum is even.',None,
    'The sum telescopes to maximum minus minimum. Thus the chosen minimum and maximum must have equal parity. Sort the array. For each parity, take the interval from its first occurrence to its last occurrence, including every element between them; its endpoints have equal parity and its size is optimal for that parity. Take the larger interval. O(n log n) time, O(n) space for a sorted copy.',
    section='dsa',topic='math',type='coding',sources=['07749c5e-3ca9-41df-b190-0c882478554b.jpg','3529ac02-69a1-48ca-bf39-c1df502d4221.jpg','b55d9af7-9fc5-4078-ba19-5dbb342ab6ec.jpg','e68bebac-c19c-44b4-92d8-9d58edf41390.jpg'],
    function_signature='def findLongestSubsequence(arr)',constraints='3 ≤ n ≤ 10⁵; 0 ≤ arr[i] ≤ 10⁹.',
    examples=[{'input':'arr = [2, 4, 1, 7]','output':'4','explanation':'Sorted values [1,2,4,7] have adjacent differences summing to 6.'},{'input':'arr = [7, 5, 6, 2, 3, 2, 4]','output':'6','explanation':'Choose [5,6,2,3,2,4], whose sorted minimum and maximum are 2 and 6.'}])
add('hp-lfu','HP','LFU cache with LRU tie-breaking',
    'Implement an LFU cache with a fixed capacity. GET key returns the stored value or −1 when absent. PUT key value inserts or updates an entry. When full, evict the least frequently used entry; among entries tied in frequency, evict the least recently used. Return the outputs of all GET queries.',None,
    'Keep key→(value,frequency), an ordered key bucket for each frequency, and the current minimum frequency. GET moves a key to the next frequency bucket and makes it most recent there. PUT of a new key evicts the oldest key in the minimum bucket when full. State whether a PUT update counts as an access before implementing it; the visible examples establish GET counting and eviction ties but do not fully specify update-frequency semantics. With ordered dictionaries or linked lists, operations are O(1) amortised.',
    section='dsa',topic='design',type='coding',hard=True,sources=['d61a51f5-2807-4ff6-a92a-460d5efc9d2d.jpg','c25a536f-bf91-4d54-9ae3-94a135ed0ad1.jpg','b0813337-0742-4713-b76d-8e02ce1cf765.jpg','5d5c61af-bc9c-4ba8-acc5-ebdcc78d36a9.jpg'],
    function_signature='def implementLFU(cacheSize, queries)',examples=[{'input':'cacheSize = 2\nqueries = ["PUT 1 1", "PUT 2 2", "GET 1", "PUT 3 3", "GET 2"]','output':'[1, -1]'}],notes='The source does not explicitly show the frequency rule for updating an existing key with PUT; clarify it before using external test cases.')

hilabs='hilabs ds.pdf'
add('hilabs-poisson','HiLabs','Distribution of independent calls in a day',
    'You need the probability of exactly k calls in one day. Calls occur independently, with a constant rate λ calls per day. Which probability distribution models the count?', 'Poisson distribution',
    'Under the homogeneous Poisson-process assumptions, the count in one day is Poisson(λ): P(N=k)=e^(−λ)λᵏ/k!. For an interval of t days the parameter is λt. Constant-rate independent arrivals are essential; a changing rate or clustered arrivals may require a different model.',
    section='ml',topic='stats-probability',type='subjective',sources=[hilabs])
add('hilabs-entropy','HiLabs','Entropy of a binary target array',
    'The target values in a training file are [0, 0, 0, 0, 1, 0, 1, 1]. Write the entropy of the target variable.', '−(5/8 log(5/8) + 3/8 log(3/8))',
    'There are five zeros and three ones. Shannon entropy is −Σp log p, so H=−[(5/8)log(5/8)+(3/8)log(3/8)]. Using base-2 logarithms gives about 0.9544 bits. The source gives a symbolic expression without specifying the log base.',
    section='ml',topic='stats-probability',type='subjective',sources=[hilabs])
add('hilabs-cbow','HiLabs','Which statements describe CBOW?',
    'For the continuous bag-of-words model, consider these statements:\n\n1. It predicts the word in the middle.\n2. It predicts the context.\n3. It estimates the probability of a word occurring in a context.\n4. Its architecture uses a neural network.\n\nWhich are correct?', '1, 3, and 4',
    'CBOW predicts a centre/target word from surrounding context words, typically using their aggregated embeddings. Skip-gram reverses the direction by predicting context from a target word. Thus statements 1, 3 and 4 describe CBOW.',
    section='ml',topic='deep-learning',options=['1, 2, and 3','2, 3, and 4','1, 3, and 4','All of these'],sources=[hilabs])
add('hilabs-pca-lda','HiLabs','PCA versus linear discriminant analysis',
    'Consider these statements about PCA and LDA (linear discriminant analysis):\n\n1. PCA is nonlinear and LDA is linear.\n2. PCA is supervised and LDA is unsupervised.\n\nWhich is correct?', 'None of these',
    'Standard PCA is a linear, unsupervised dimensionality-reduction method that preserves variance. Linear discriminant analysis uses labels to find linear projections that separate classes, so it is supervised. Both statements reverse or misstate the standard definitions. Kernel PCA is a different nonlinear extension.',
    section='ml',topic='ml-theory',options=['1','2','Both of these','None of these'],sources=[hilabs])
add('hilabs-relu','HiLabs','ReLU: piecewise linear versus globally linear',
    'Which of these statements about ReLU are correct?\n\n1. It is piecewise linear.\n2. For a positive input it outputs the input; otherwise it outputs zero.\n3. It can output an exact zero.\n4. It is a linear activation function.', 'Statements 1, 2 and 3',
    'ReLU(x)=max(0,x). It is linear separately on either side of zero, but it is not globally linear: for example ReLU(−1)+ReLU(1)=1 while ReLU(0)=0. It provides a nonlinear model when composed with affine layers; its derivative at zero needs a chosen subgradient convention.',
    section='ml',topic='deep-learning',type='subjective',sources=[hilabs],notes='Presented as a short-answer prompt because the scanned combination options are unclear.')
add('hilabs-auc','HiLabs','Interpret an ROC-AUC close to zero',
    'For a binary-classification model, what does an ROC-AUC score close to zero suggest?', 'The ranking is almost the reverse of the correct class ordering',
    'AUC is the probability that a randomly chosen positive example receives a higher score than a randomly chosen negative, with half credit for ties. Near-zero AUC indicates strongly reversed ranking under the chosen label/score convention. Check positive-class labels and score orientation; flipping score direction gives AUC close to one. This is not by itself proof of overfitting.',
    section='ml',topic='ml-theory',type='subjective',sources=[hilabs])
add('hilabs-outliers','HiLabs','Univariate outlier detection',
    'Consider statements about univariate outlier detection:\n\n1. It looks for unusual combinations across all variables.\n2. It looks for extreme values of a single variable.\n3. It can use box plots to detect outliers.\n4. It reduces the contribution of potential outliers during training.\n\nWhich describe the detection method itself?', 'Statements 2 and 3',
    'Univariate detection examines one variable at a time; box plots often flag observations beyond an IQR-based fence. Unusual combinations are multivariate anomalies. Reducing outlier influence is a modelling or treatment step, not an inherent consequence of detecting outliers.',
    section='ml',topic='data-analysis',type='subjective',sources=[hilabs])
add('hilabs-one-block','HiLabs','Partition a binary array into blocks with one 1 each',
    'A One block is a contiguous block containing exactly one element equal to 1. Given a binary array Arr, count the ways to partition the entire array into contiguous One blocks. Return 0 if no valid partition exists.',None,
    'List the positions of ones, p₁…pₖ. If k=0, return 0. Between consecutive ones, a boundary may be placed in pᵢ₊₁−pᵢ different positions. These choices are independent, so the answer is their product. Leading and trailing zeros must belong to the first and last blocks. A single one therefore gives one partition. O(n) time and O(1) extra space using a running previous-one position.',
    section='dsa',topic='math',type='coding',sources=[hilabs,'Hilabs1 DS.pdf'],constraints='1 ≤ N ≤ 100; Arr[i] ∈ {0,1}.',function_signature='def OneBlock(N, Arr)',
    examples=[{'input':'N = 3, Arr = [0, 1, 0]','output':'1','explanation':'The whole array is the only One block.'}],notes='The source uses a 64-bit return type but gives no modulus. Large valid arrays can produce a count exceeding 64 bits; Python integers avoid overflow.')

from reviewed_batch2 import extend
extend(add)
from reviewed_batch3 import extend
extend(add)
from reviewed_batch4 import extend
extend(add,merge,skip)
from reviewed_batch5 import extend
extend(add,merge)
from reviewed_batch6 import extend
extend(add,merge,skip)
from reviewed_batch7 import extend
extend(add,merge,skip)
from reviewed_batch8 import extend
extend(add,merge,skip)
from reviewed_batch9 import extend
extend(add,merge,skip)
from reviewed_batch10 import extend
extend(add,merge,skip)
from reviewed_batch11 import extend
extend(add,merge,skip,resolve)
from reviewed_batch12 import extend
extend(add,skip)
from reviewed_batch13 import extend
extend(add,merge)
from reviewed_batch14 import extend
extend(add,merge)
from reviewed_batch15 import extend
extend(add)

# Later batches: any build/reviewed_auto_*.py module exposing extend(...) with helper names as parameters.
import importlib, inspect
_helpers=dict(add=add,merge=merge,skip=skip,resolve=resolve,alias=alias)
for _path in sorted(Path(__file__).resolve().parent.glob('reviewed_auto_*.py')):
    _mod=importlib.import_module(_path.stem)
    _mod.extend(**{k:_helpers[k] for k in inspect.signature(_mod.extend).parameters})

if __name__=='__main__':
    out=ROOT/'build/raw/curated_local.json'
    processed={p for q in questions for p in q['source_files']}|{s['file'] for s in skipped}|{p for a in aliases for p in a['source_files']}
    out.write_text(json.dumps(dict(batch='curated_local',processed_files=sorted(processed),skipped_files=skipped,aliases=aliases,questions=questions),ensure_ascii=False,indent=2),encoding='utf-8')
    print(f'Saved {len(questions)} reviewed local additions.')
