"""Oracle September group, with explicit assumptions for defective MCQs."""


def extend(add, merge, skip):
    def question(key, title, statement, answer, explanation, options, suffix, section='cs', topic='networks'):
        add('oracle-'+key, 'Oracle', title, statement, answer, explanation, options=options,
            section=section, topic=topic, sources=['IMG-20240913-WA'+suffix+'.jpg'])

    question('previous-year-day', 'Weekday on the same date a year earlier',
        'December 8, 2007 was Saturday. What weekday was December 8, 2006?', 'Friday',
        'There are 365 days between these dates, so the later date is one weekday ahead. One day before Saturday is Friday.',
        ['Sunday','Thursday','Tuesday','Friday'], '0014', 'aptitude', 'quant')
    merge('oracle-past-perfect','Oracle',['IMG-20240913-WA0015.jpg'])
    merge('oracle-cap','Oracle',['IMG-20240913-WA0025.jpg'])
    merge('oracle-virtual-address','Oracle',['IMG-20240913-WA0036.jpg'])
    merge('oracle-acid-not','Oracle',['IMG-20240913-WA0043.jpg'])
    question('tcp-order', 'TCP delivery ordering and acknowledgement',
        'Which mechanism lets TCP track ordered delivery and identify data that has been received?', 'Sequence numbers and acknowledgements',
        'TCP numbers bytes in the stream and acknowledges received data. The receiver can reorder segments, detect gaps and reject duplicate data; retransmission can recover missing segments. Checksums help detect corruption. A connection handshake establishes the connection but does not by itself provide the ongoing delivery tracking.',
        ['Tunnelling','Handshaking','Sequence numbers and acknowledgements','Packet sniffing'], '0020')
    question('bgp-layer', 'BGP name and position above its transport',
        'What does BGP stand for, and which layer contains its messages when classifying the protocol by its use of TCP as transport?', 'Border Gateway Protocol, application layer',
        'BGP is Border Gateway Protocol. Its messages run over TCP, using port 179, so this encapsulation-based classification puts BGP above transport at the application layer. Its purpose is to exchange network-layer reachability information; that routing function should not be confused with how its own messages are transported. See [RFC 4271](https://www.rfc-editor.org/rfc/rfc4271.html).',
        ['Best Gateway Protocol, network layer','Border Gateway Protocol, application layer','Border Gateway Protocol, network layer','Backbone Gateway Protocol, data-link layer'], '0021')
    question('nested-uri', 'URI for a company employee subresource',
        'In a conventional REST-style resource hierarchy, which URI identifies employee {employeeId} under company {companyId}?', '/companies/{companyId}/employees/{employeeId}',
        'Nest the employee collection beneath the specific company resource, then identify its employee member. Plural collection names make the hierarchy clear. This is a conventional naming choice rather than a protocol requirement; an API can also expose employees as top-level resources.',
        ['/company/{companyId}/employees/{employeeId}','/companies/employees/{companyId}/{employeeId}','/companies/{companyId}/employee/{employeeId}','/companies/{companyId}/employees/{employeeId}'], '0022')
    add('oracle-create-method','Oracle','Methods that can create a REST resource',
        'Which HTTP method is suitable for resource creation? The source offers PUT, PATCH, POST and CREATE.', None,
        'POST commonly creates a new member of a collection when the server assigns its identifier. PUT can also create a resource at a client-selected URI if it does not exist, or replace it if it does. PATCH expresses partial modification and CREATE is not a standard HTTP method. Because both POST and PUT can create resources, the MCQ needs to specify the creation pattern to have one answer.',
        section='cs', topic='networks', type='subjective', sources=['IMG-20240913-WA0024.jpg'], notes='The generic source wording permits both PUT and POST; no unique option is graded.')
    question('load-balancer','Distribute traffic across web servers',
        'Which listed component distributes incoming requests across a set of web servers?', 'Load balancer',
        'A load balancer selects a backend according to its policy and health information, distributing traffic across available servers. Firewalls filter traffic, while ordinary routers and switches forward it; those roles alone do not provide application-backend load balancing.',
        ['Firewall','Router','Load balancer','Switch'], '0026', 'cs', 'system-design')
    question('marathon-vector','Store race finishers for rank-based access',
        'Finishers’ names arrive in finishing order. After the race, print the first ten finishers and ranks 100,200,300,… . Which listed data structure best fits appending in order and accessing these ranks?', 'Vector or resizable array',
        'A vector preserves arrival order with amortised O(1) append and O(1) indexed access. Rank r is stored at index r−1. A linked list needs traversal to reach each rank; a plain hash set does not preserve finishing order. A tree map is unnecessary for this append-and-index workload.',
        ['Vector or resizable array','Map implemented as a binary tree','Singly linked list','Hash set'], '0027', 'dsa', 'arrays')
    question('priority-heap','Standard data structure for a priority queue',
        'Which listed data structure is the conventional efficient implementation of a priority queue?', 'Heap',
        'A binary heap supports viewing the minimum or maximum in O(1), and insertion and removal of that extreme in O(log n). An unordered array or list can make insertion cheap but requires linear search to remove the extreme; maintaining sorted order makes insertion more costly.',
        ['Array','Stack','Heap','Linked list'], '0028', 'dsa', 'heap')
    question('memoization','Meaning of memoization',
        'In dynamic programming, what does memoization mean?', 'Store solved subproblems to avoid recomputation',
        'Memoization caches the result for each subproblem state. A later call with the same state reuses that result, often in a recursive top-down computation. Iterative bottom-up evaluation is normally called tabulation; both can avoid repeated work.',
        ['Write the algorithm in a memo','Recompute subproblems for accuracy','Store solved subproblems to avoid recomputation','Solve subproblems iteratively'], '0029', 'dsa', 'dp')
    question('kernel-mode','Privilege difference between user and kernel mode',
        'Which statement best describes the privilege difference between user mode and kernel mode?', 'Kernel mode can access protected memory regions that user mode cannot',
        'Kernel mode has privileges required to manage protected system resources, subject to the processor’s protection mechanisms. User programs request privileged services through controlled system calls or traps. Scheduling priority is a separate concept; kernel mode does not mean lower priority.',
        ['User mode allows direct hardware access but kernel mode does not','Kernel mode can access protected memory regions that user mode cannot','Kernel-mode applications have lower priority','User instructions can switch to kernel mode but not vice versa'], '0030', 'cs', 'os')
    add('oracle-intelligent-substring','Oracle','Longest substring with at most k normal characters',
        'The 26-character bit string charValue maps letters a…z to types: 0 means normal and 1 means special. Given lowercase string s and integer k, return the length of the longest contiguous substring containing at most k normal-character occurrences. Repeated occurrences each count.', None,
        'Maintain a sliding window and the count of normal occurrences within it. Add the new rightmost character; while the count exceeds k, remove characters from the left. Every resulting window is valid, so track its maximum length. Each pointer advances at most n times: O(n) time and O(1) extra space beyond the fixed 26-letter mapping. Count occurrences rather than distinct letters; two copies of a normal letter consume two places.',
        section='dsa', topic='sliding-window', type='coding', sources=[f'IMG-20240913-WA00{i}.jpg' for i in range(31,36)], function_signature='getSpecialSubstring(s, k, charValue)', constraints='1 ≤ len(s) ≤ 10⁵; len(charValue)=26; its characters are 0 or 1; s uses lowercase English letters.',
        examples=[{'input':'s = "giraffe", k = 2\ncharValue = "01111001111111111011111111"','output':'3','explanation':'Normal letters are a,f,g,r. Valid length-three windows include gir, ira and ffe.'},{'input':'s = "abcde", k = 2\ncharValue = "10101111111111111111111111"','output':'5'}], notes='The source writes “length of k” in its constraint list even though k is an integer. The visible narrative states an at-most-k count.')
    add('oracle-semaphore-race','Oracle','Binary versus two-permit semaphore around updates',
        'X starts at 10. Five threads each execute wait(S); X=X+1; signal(S), and three execute wait(S); X=X−1; signal(S). Compare the minimum final values with (1) a binary semaphore initially 1 and (2) a counting semaphore initially 2. The source options are (15,7), (7,7), (12,7), (12,8).', None,
        'Under the usual abstract model where each assignment has separately atomic read and write steps, the answer is (12,7). One permit gives mutual exclusion, preserving all updates: 10+5−3=12. Two permits allow lost updates. One decrement can read 10 and pause; all five increments run using the other permit; that pending decrement then writes 9, discarding their effects. The two remaining decrements reduce it to 7. Fewer than 7 is impossible with only three decrement operations. If this were implemented in C/C++ using an ordinary shared variable, allowing concurrent unsynchronised updates creates a data race instead of a well-defined numeric outcome; use a mutex or atomic operations.',
        section='cs', topic='os', type='subjective', sources=['IMG-20240913-WA0000.jpg','IMG-20240913-WA0037.jpg','IMG-20240913-WA0038.jpg'], notes='The read/write model is not specified in the source. The explanation makes the exam-style interleaving assumption explicit, without a portable-code guarantee.')
    add('oracle-pointer-output','Oracle','Pointer increment versus incrementing its character',
        'Ignoring separators, what characters does this C program print?\n\n```c\n#include <stdio.h>\nint main(void) {\n    char arr[] = "abcd";\n    char *p = arr;\n    printf("%c\\t", ++*p);\n    printf("%c\\t", *p++);\n    printf("%c\\t", (*p)++);\n    printf("%c\\n", *p);\n    return 0;\n}\n```','bbbc',
        '++*p changes arr[0] from a to b and prints b. *p++ prints that b, then advances p to arr[1]. (*p)++ prints the old arr[1], also b, then changes it to c. The last statement prints c. Each expression is in a separate full statement, so these operations are sequenced.',
        section='cs', topic='c-cpp-output', options=['bbbc','bccd','bbcc','bccc'], sources=['IMG-20240913-WA0039.jpg','IMG-20240913-WA0040.jpg'])
    question('sql-default','Column value when INSERT omits that column',
        'Which SQL column declaration supplies a value when an INSERT does not explicitly provide one for the column?', 'DEFAULT',
        'DEFAULT provides the column’s default expression/value when the insertion uses its default. NOT NULL disallows nulls, CHECK enforces a condition and UNIQUE restricts duplicate values. Explicitly inserting NULL is not generally the same as omitting the column.',
        ['NOT NULL','DEFAULT','CHECK','UNIQUE'], '0044', 'cs', 'dbms')
    question('truncate-ddl','Conventional classification of TRUNCATE TABLE',
        'In the conventional SQL command classification used in the source, TRUNCATE TABLE is classified as what?', 'Data Definition Language',
        'TRUNCATE TABLE is conventionally grouped under DDL, whereas DELETE is DML. Both can remove rows, but their locking, identity reset, trigger and transaction behaviours depend on the database system. The classification alone does not establish whether an operation can be rolled back.',
        ['Data Definition Language','Data Manipulation Language','Data Control Language','Transaction Control Language'], '0045', 'cs', 'dbms')
    question('zombie','Meaning of a Linux zombie process',
        'What is a zombie process in Linux?', 'A process that has finished but still has a process-table entry',
        'A zombie has exited, but its parent has not yet collected its exit status with a wait-family operation. It retains a small process-table record, not a running program. A background or long-running process is not a zombie merely for those reasons.',
        ['A process running in the background','A process running for a long time','A process that has finished but still has a process-table entry','A process that crashed due to memory corruption'], '0046', 'cs', 'os')
    question('server-error','HTTP server-error status-code class',
        'Which HTTP response status-code class represents server errors?', '5xx',
        'The 5xx class indicates server-error responses, such as 500 Internal Server Error or 503 Service Unavailable. The other classes are 1xx informational, 2xx successful, 3xx redirection and 4xx client error.',
        ['1xx','2xx','4xx','5xx'], '0047')
    add('oracle-weaned-off','Oracle','Meaning of weaned off in a passage',
        'In a passage, customers no longer wanted some services after being “weaned off” them during a long period at home. Which listed sentence does not express a similar idea?', 'Encourage people to eat fruits and vegetables',
        'Weaned off means gradually made less dependent on, or accustomed to doing without, something. Taking young animals off milk, discouraging alcohol consumption, and curtailing children’s interest in games all involve reducing a habit or dependence. Encouraging fruit and vegetable consumption instead promotes a behaviour.',
        topic='verbal', options=['Take seal pups off their mothers’ milk','Encourage people to eat fruits and vegetables','Dissuade patients from taking alcohol','Curtail children’s interest in TV and video games'], sources=['IMG-20240913-WA0019.jpg','IMG-20240913-WA0023.jpg'], notes='Only the relevant phrase context is paraphrased; unrelated historical/economic claims are omitted.')
    for suffix, reason in [('0016','sentence-error label actually contains a number-wheel diagram; needs transcription'),('0017','reading inference has two plausible brevity benefits'),('0018','sentence-improvement label actually contains the same number-wheel diagram'),('0041','named cloud services need current source verification'),('0042','historical software version needs dated verification'),('0048','animal-survival wording and assumptions need clarification')]:
        skip('Oracle','IMG-20240913-WA'+suffix+'.jpg',reason)
