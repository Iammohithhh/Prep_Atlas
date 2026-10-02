"""Second Oracle screenshot group, checked against original images."""


def extend(add, merge):
    merge('oracle-quiz-windows', 'Oracle', [f'IMG-20240803-WA00{i}.jpg' for i in range(36, 42)])
    merge('oracle-sports-ambiguity', 'Oracle', ['IMG-20240823-WA0056.jpg'])

    def cs(key, title, statement, answer, explanation, options, sources, topic):
        add('oracle-'+key, 'Oracle', title, statement, answer, explanation,
            section='cs', topic=topic, options=options, sources=sources)

    cs('segmentation', 'External fragmentation in memory management',
       'Which listed memory-management technique is classically associated with external fragmentation?', 'Segmentation',
       'Segments have variable sizes and need contiguous regions in the conventional model. Free memory can be split into holes too small for a requested segment even when their total is sufficient: external fragmentation. Fixed-size paging avoids this allocation problem, although a partly filled page can cause internal fragmentation. Swapping describes moving memory contents between RAM and storage rather than a specific allocation layout.',
       ['Paging', 'Swapping', 'Segmentation', 'Pure demand paging'],
       ['IMG-20240806-WA0152.jpg', 'IMG-20240823-WA0033.jpg'], 'os')
    add('oracle-matrix-edges', 'Oracle', 'Count edges from an adjacency matrix',
        'Given a graph with V vertices and E edges, what is the time complexity of counting its edges by scanning an adjacency matrix?', 'O(V²)',
        'An adjacency matrix has V² entries, all of which may need inspection to count present edges. For a simple undirected graph, scanning one triangle or dividing an off-diagonal count by two changes only the constant factor. An adjacency-list traversal has different complexity and is not the representation in this question.',
        section='dsa', topic='graphs', options=['O(V)', 'O(E²)', 'O(E)', 'O(V²)'],
        sources=['IMG-20240806-WA0153.jpg', 'IMG-20240823-WA0036.jpg'])
    add('oracle-monolith', 'Oracle', 'Challenges of monolithic architecture',
        'Which is a potential challenge of monolithic architecture? The supplied options are complex deployment process, improved scalability, tight coupling between components, and high maintenance overhead.', None,
        'Tight coupling is the most characteristic listed concern: changing one component can affect others, and the application often has to be released as a unit. Deployment complexity and maintenance overhead can also become challenges in a large monolith, so the wording does not establish a unique correct choice. A small, well-structured monolith can be simple to deploy and maintain; architecture alone does not determine those costs.',
        section='cs', topic='system-design', type='subjective',
        sources=['IMG-20240806-WA0154.jpg', 'IMG-20240823-WA0044.jpg'],
        notes='Several listed choices can be challenges. No single choice is automatically graded.')
    cs('rest-create', 'Collection URI for creating a blog post',
       'In a conventional REST-style blogging API, which listed URI should receive a POST request to create a new blog post?', '/blog/posts',
       'POST to the posts collection lets the server create a new member, typically returning its resource URI. The collection noun /blog/posts avoids adding an operation verb such as create or new to the resource path. The method is essential: a URI by itself does not specify creation semantics.',
       ['/blog/posts/new', '/blog/create/post', '/blog/posts', '/blog/posts/create'],
       ['IMG-20240806-WA0155.jpg', 'IMG-20240823-WA0046.jpg'], 'networks')
    add('oracle-subsequences', 'Oracle', 'Build all subsequences in dictionary order',
        'Given a string s containing distinct lowercase English letters, return every nonempty subsequence in lexicographically increasing order. A subsequence preserves the original order of its chosen characters.', None,
        'Enumerate each include/exclude decision, emitting every nonempty result, then sort the resulting strings. Distinct input characters ensure different position subsets produce different strings. There are 2ⁿ−1 outputs, so exponential work is unavoidable. Building strings costs O(n·2ⁿ); comparison sorting has a worst-case O(n²·2ⁿ) bound including comparisons of up to n characters. The output occupies O(n·2ⁿ) space.',
        section='dsa', topic='backtracking', type='coding', sources=['IMG-20240806-WA0156.jpg', 'IMG-20240806-WA0157.jpg'],
        function_signature='buildSubsequences(s)', constraints='1 < len(s) < 16; s contains distinct lowercase English letters.',
        examples=[{'input':'s = "ba"', 'output':'["a", "b", "ba"]'}, {'input':'s = "xyz"', 'output':'["x", "xy", "xyz", "xz", "y", "yz", "z"]'}])
    cs('subnet-broadcast', 'Broadcast address of a /27 subnet',
       'What is the broadcast address for subnet 172.16.10.128/27?', '172.16.10.159',
       'There are 32−27=5 host bits, giving 32 addresses per subnet. This block runs from 172.16.10.128 through 172.16.10.159. Setting every host bit to one yields .159, the broadcast address.',
       ['172.16.10.159', '172.16.10.191', '172.16.10.224', '172.16.10.255'],
       ['IMG-20240806-WA0159.jpg', 'IMG-20240823-WA0048.jpg'], 'networks')
    cs('pcb', 'Structure holding process information',
       'Which listed operating-system structure holds information about a process?', 'Process Control Block',
       'A process control block records information needed to manage and resume a process: its state, identifier, saved registers/program counter, scheduling information and memory/resource references. A heap and stack hold program data; a TLB caches address translations.',
       ['Heap', 'Process Control Block', 'Stack', 'TLB cache'], ['IMG-20240823-WA0032.jpg'], 'os')
    cs('bootloader', 'Program that loads the operating system',
       'Which listed program loads the operating system during boot?', 'Bootloader',
       'After firmware starts the boot sequence, a bootloader loads the operating-system kernel and transfers control to it. A compiler translates source code, while device drivers allow the running system to interact with hardware.',
       ['Compiler', 'Bootloader', 'Kernel', 'Device driver'], ['IMG-20240823-WA0034.jpg'], 'os')
    add('oracle-tree-reconstruction', 'Oracle', 'Traversal pair that determines a binary tree',
        'For a binary tree with distinct node values, which listed pair of traversals uniquely determines the tree?', 'Postorder and inorder',
        'The final postorder value is the root. Its unique position in inorder separates the left and right subtrees, which can then be reconstructed recursively. Distinct values are necessary for this simple uniqueness guarantee. Preorder plus postorder does not distinguish a lone left child from a lone right child; the other supplied pairs have similar ambiguities for general binary trees.',
        section='dsa', topic='trees', options=['Postorder and preorder', 'Postorder and inorder', 'Postorder and level order', 'Level order and preorder'],
        sources=['IMG-20240823-WA0035.jpg'], notes='The source does not state the distinct-values assumption; it is made explicit here.')
    add('oracle-avl-rotation', 'Oracle', 'Purpose of rotations in an AVL tree',
        'What is the primary purpose of rotations in an AVL tree?', 'Maintain balance and logarithmic height',
        'Rotations restore the AVL invariant that the two child-subtree heights differ by at most one while preserving BST inorder ordering. This keeps height O(log n), supporting logarithmic search, insertion and deletion. It does not require a complete tree or equal depth for every leaf.',
        section='dsa', topic='trees', options=['Make the tree complete', 'Put all leaves at the same depth', 'Maintain balance and logarithmic height', 'Make inorder traversal easier'], sources=['IMG-20240823-WA0037.jpg'])
    add('oracle-bst-insert', 'Oracle', 'Average insertion cost in a BST',
        'Under the usual random-insertion assumption, what is the average time complexity of inserting an element into an ordinary binary search tree?', 'O(log n)',
        'Insertion follows a root-to-null search path, taking O(h) for height h. Random insertion order gives logarithmic expected path length. An unbalanced tree built from sorted values can instead have height n and O(n) insertion; a balanced BST guarantees O(log n).',
        section='dsa', topic='trees', options=['O(1)', 'O(n)', 'O(log n)', 'O(n log n)'], sources=['IMG-20240823-WA0038.jpg', 'IMG-20240823-WA0049.jpg'], notes='The average-case input assumption is stated explicitly; it is absent from the source.')
    cs('atomicity', 'All-or-nothing transaction execution',
       'Which transaction property means either all operations of a transaction occur or none do, with no partial committed transaction?', 'Atomicity',
       'Atomicity is the all-or-nothing guarantee. Consistency preserves declared invariants, isolation governs interactions between concurrent transactions, and durability preserves committed results after failures.',
       ['Persistence', 'Isolation', 'Atomicity', 'Consistency'], ['IMG-20240823-WA0039.jpg'], 'dbms')
    cs('relation-cardinality', 'Number of tuples in a relation',
       'What is the term for the number of tuples (rows) in a relation?', 'Cardinality',
       'Relation cardinality is its number of tuples. Degree or arity is its number of attributes (columns). An entity is a represented object, not the row-count term.',
       ['Entity', 'Column', 'Cardinality', 'None of the above'], ['IMG-20240823-WA0040.jpg'], 'dbms')
    cs('dcl', 'Data Control Language commands',
       'Which listed commands belong to Data Control Language?', 'Both REVOKE and GRANT',
       'GRANT assigns privileges and REVOKE removes them. They control access permissions and are conventionally classified as DCL. Their exact privilege and role semantics depend on the database system.',
       ['REVOKE', 'GRANT', 'Both REVOKE and GRANT', 'None of the above'], ['IMG-20240823-WA0041.jpg'], 'dbms')
    cs('transfer-invariant', 'Transaction property preserving a bank-transfer invariant',
       'A transaction reads x, subtracts 50 and writes x, then reads y, adds 50 and writes y. Which ACID property describes preserving the constraint that x+y is unchanged?', 'Consistency',
       'The invariant x+y must be valid before and after a completed transaction: consistency. Isolation can be needed to prevent concurrent operations from violating the invariant, but it is a separate guarantee about interactions. Durability concerns persistence after commit, not the sum itself.',
       ['Durability', 'Consistency', 'Isolation', 'Both consistency and isolation'], ['IMG-20240823-WA0042.jpg'], 'dbms')
    cs('dbaas', 'Expansion of DBaaS', 'What does DBaaS stand for?', 'Database as a Service',
       'DBaaS means Database as a Service: a provider offers a managed database service rather than requiring the customer to operate the underlying database infrastructure. Management responsibilities still vary by service.',
       ['Data as a Service', 'Database as a Service', 'Database as a System', 'Data as a System'], ['IMG-20240823-WA0043.jpg'], 'dbms')
    cs('cache-tier', 'Typical effect of a database cache tier',
       'Which statement contradicts the usual goal of a separately scalable cache tier in front of a database?', 'A cache tier increases database workloads',
       'Cache hits answer repeated reads without reaching the database, usually reducing read workload and latency. A separately deployed cache can scale independently. Misses, invalidation and writes still require careful design; the answer describes the normal intended effect rather than a guarantee for every possible workload.',
       ['A cache tier improves system performance', 'A cache tier reduces database workloads', 'A cache tier can be scaled up independently', 'A cache tier increases database workloads'], ['IMG-20240823-WA0045.jpg'], 'system-design')
    cs('nat', 'Purpose of NAT', 'Which listed task describes a common use of Network Address Translation?', 'Map private IP addresses to public IP addresses for internet access',
       'NAT rewrites IP addresses, often together with transport ports, to allow hosts using private addresses to communicate through public addresses. DNS resolves names; DHCP assigns network configuration; encryption is a different task.',
       ['Translate domain names to IP addresses', 'Encrypt network traffic for secure communication', 'Assign IP addresses dynamically to devices', 'Map private IP addresses to public IP addresses for internet access'], ['IMG-20240823-WA0047.jpg'], 'networks')
    add('oracle-weekday', 'Oracle', 'Day of the week after 62 days',
        'If today is Monday, what day is it after 62 days?', 'Sunday',
        '62 leaves remainder 6 when divided by 7. Six days after Monday is Sunday; each complete seven-day block leaves the weekday unchanged.',
        options=['Sunday', 'Saturday', 'Monday', 'Wednesday'], sources=['IMG-20240823-WA0050.jpg'])
    add('oracle-remainder', 'Oracle', 'Remainder when 1,992 is divided by 92',
        'What is the remainder when 1,992 is divided by 92?', 'None of the above',
        '92×21=1,932 and 1,992−1,932=60. Since 0≤60<92, the remainder is 60, which is absent from the numeric choices.',
        options=['0', '1', '40', 'None of the above'], sources=['IMG-20240823-WA0053.jpg'])
    add('oracle-work-rates', 'Oracle', 'Find two workers with the same rate',
        'A and B together complete a job in 10 days. B and C together take 5 days. C and D together take 4 days. A alone takes 40 days. Which pair work at the same rate?', 'C and D',
        'In jobs per day, a=1/40. Then b=1/10−1/40=3/40, c=1/5−3/40=5/40, and d=1/4−5/40=5/40. Thus C and D each take 8 days alone.',
        options=['A and B', 'B and D', 'C and D', 'A and D'], sources=['IMG-20240823-WA0055.jpg'])
    add('oracle-semicircle-angles', 'Oracle', 'Two inscribed angles along a semicircle',
        'A, B, C, D and E are distinct points, in that order, on one semicircular arc. A and E are the endpoints of its diameter. What is ∠ABC + ∠CDE? The source options are 135°, 180°, 225°, 315° and 90°.', None,
        'Let the upper arcs AC and CE have measures u and v. Because AE is a diameter, u+v=180°. Angle ABC intercepts the other arc AC, so it equals (360°−u)/2. Similarly CDE=(360°−v)/2. Their sum is 360°−(u+v)/2=270°. None of the visible options matches the stated geometry. For example equal arc spacing makes both angles 135°, confirming the sum 270°.',
        topic='geometry', type='subjective', sources=['IMG-20240823-WA0057.jpg'], notes='The full diagram and point-order statement are visible, but the calculated answer is absent from the source options. No incorrect option is automatically graded.')
