"""Oracle PDF repeats, qualified technical answers and unresolved source caveats."""


def extend(add, merge, skip, resolve):
    answer_pdf = 'ORACLE-MCQ-Final.pdf'
    photo_pdf = 'oracle mcqs.pdf'
    for key in (
        'oracle-pcb', 'oracle-virtual-address', 'oracle-postfix', 'oracle-c-macro',
        'oracle-acid-not', 'oracle-cap', 'oracle-nosql-choice', 'oracle-hosts',
        'oracle-having', 'oracle-idempotent', 'oracle-head', 'oracle-ring', 'oracle-arp',
        'oracle-sparse-matrix', 'oracle-23tree', 'oracle-five-ingredients',
        'oracle-painted-cube', 'oracle-favorite-color', 'oracle-standing-order',
        'oracle-autonomy', 'oracle-hiring-idiom', 'oracle-exam-idiom',
        'oracle-spawned-antonym', 'oracle-reading-louis', 'oracle-remainder',
        'oracle-phone-customers', 'oracle-only-cricket', 'oracle-pointer-output',
    ):
        merge(key, 'Oracle', [answer_pdf])
    for key in (
        'oracle-virtual-address', 'oracle-semaphore-race', 'oracle-kernel-mode',
        'oracle-priority-heap', 'oracle-memoization', 'oracle-marathon-vector',
        'oracle-pointer-output', 'oracle-acid-not', 'oracle-sql-default',
        'oracle-truncate-ddl', 'oracle-load-balancer', 'oracle-cap', 'oracle-zombie',
        'oracle-create-method', 'oracle-server-error', 'oracle-nested-uri',
        'oracle-bgp-layer', 'oracle-tcp-order', 'oracle-ongoing-tense',
        'oracle-past-perfect', 'oracle-three-ants', 'oracle-clock-overlap',
        'oracle-two-eggs', 'oracle-nine-coins', 'oracle-power-mod',
        'oracle-phone-customers', 'oracle-cyclical-sequence',
        'oracle-previous-year-day', 'oracle-weaned-off', 'oracle-pollution-ranks',
    ):
        merge(key, 'Oracle', [photo_pdf])
    merge('oracle-spawned-antonym', 'Oracle', ['IMG-20240810-WA0050.jpg'])

    solutions = ['DOC-20240809-WA0022.pdf', 'Final_oracle_coding.pdf']
    for key in ('oracle-any-tree-path', 'oracle-quiz-windows',
                'oracle-friend-groups', 'oracle-count-subsequence'):
        merge(key, 'Oracle', solutions)
    for key in ('oracle-intelligent-substring', 'oracle-minimax-clusters'):
        merge(key, 'Oracle', ['Final_oracle_coding.pdf'])
    for name in solutions:
        skip('Oracle', name, 'Solution-only collection: matched repeats are merged, but other named problems lack original statements, constraints or endpoint rules. See build/oracle_solution_review.md; do not treat supplied code as an official answer key.')

    add('oracle-syscall-interrupt', 'Oracle', 'Legacy i386 Linux system-call interrupt',
        'In the legacy 32-bit x86 (i386) Linux system-call interface, which software interrupt vector is used by the int instruction?', '0x80',
        'The i386 interface uses int $0x80, with the system-call number in eax. Native x86-64 uses the syscall instruction instead. The interrupt is architecture-specific, so the source’s unqualified wording “in Linux” is too broad. See the [Linux syscall manual](https://man7.org/linux/man-pages/man2/syscall.2.html).',
        section='cs', topic='os', options=['0x10', '0x60', '0x80', '0x40'], sources=[answer_pdf],
        notes='Architecture qualification is added to make the historical source answer valid; this is not a universal Linux calling convention.')

    add('oracle-range-partition', 'Oracle', 'Review incomplete range-partition DDL',
        'An orders table needs order_id (primary key), customer_id, order_date and total_amount. The source offers fragments beginning with CREATE TABLE orders, then a PARTITION BY RANGE clause, but omits all column declarations. One fragment uses RANGE COLUMNS; another appends PRIMARY KEY(order_id) after the partitions. Can any be accepted as a complete Oracle CREATE TABLE statement? Show a complete range-partitioned form.', None,
        'None of the displayed fragments is a complete Oracle table definition: the column declarations are missing. Oracle uses PARTITION BY RANGE (order_date), not the shown RANGE COLUMNS form. Define the primary key within the table definition and use explicit DATE literals for date bounds. A complete illustration is:\n\n```sql\nCREATE TABLE orders (\n  order_id NUMBER PRIMARY KEY,\n  customer_id NUMBER,\n  order_date DATE,\n  total_amount NUMBER(12,2)\n)\nPARTITION BY RANGE (order_date) (\n  PARTITION p1 VALUES LESS THAN (DATE \'2023-01-01\'),\n  PARTITION p2 VALUES LESS THAN (DATE \'2024-01-01\'),\n  PARTITION p_future VALUES LESS THAN (MAXVALUE)\n);\n```\n\nThe final partition accommodates later dates; the first two bounds are exclusive. Data types and the final partition are supplied for this illustration, not recovered from the options. The source’s tentative “C (maybe)” is not a verified answer. See [Oracle CREATE TABLE](https://docs.oracle.com/en/database/oracle/oracle-database/19/sqlrf/CREATE-TABLE.html).',
        section='cs', topic='sql', type='subjective', confidence='low',
        sources=['IMG-20240730-WA0069.jpg', 'IMG-20240823-WA0106.jpg', answer_pdf],
        notes='The source does not name a dialect; the discussion explicitly uses Oracle SQL. The original options are incomplete and are not automatically graded.')
    resolve('Oracle', 'IMG-20240823-WA0106.jpg')

    add('oracle-redis-store', 'Oracle', 'Recognise the conventional key-value store',
        'Which listed NoSQL database is conventionally classified as a key-value store?', 'Redis',
        'Redis organises data as keys associated with typed values, such as strings, hashes and lists. It is the conventional key-value answer in this list. NoSQL classifications describe common data models rather than forbidding other abstractions or access patterns. See [Redis keys and values](https://redis.io/docs/latest/develop/using-commands/keyspace/).',
        section='cs', topic='dbms', options=['HBase', 'MongoDB', 'Redis', 'Accumulo'],
        sources=[answer_pdf, 'IMG-20240823-WA0105.jpg', 'WhatsApp Image 2024-08-23 at 14.48.06_5038b95d.jpg'])
    for name in ['IMG-20240823-WA0105.jpg', 'WhatsApp Image 2024-08-23 at 14.48.06_5038b95d.jpg']:
        resolve('Oracle', name)

    add('oracle-animal-model', 'Oracle', 'Animal survival probabilities versus family composition',
        'There are 729 farmers, each owning six animals that are cows or hens. A flood occurs. A hen survives with probability 1/3 and a cow with probability 2/3. The source asks how many families have two hens and four cows. Does the supplied information determine that count?', None,
        'No. Species-specific survival probabilities do not give the initial animal composition, independence between outcomes or an observed number of survivors. The actual family count is therefore not determined. A different binomial model, in which each of six independent positions is a hen with probability 1/3 and a cow with probability 2/3, gives expected count 729×C(6,2)×(1/3)²×(2/3)⁴=240. That is a conditional expectation under an added composition model, not a consequence of the photographed survival statement and not a guaranteed realised count.',
        topic='probability', type='subjective', confidence='low',
        sources=['IMG-20240913-WA0048.jpg', 'IMG-20240915-WA0088.jpg', photo_pdf],
        notes='The source’s species/survival wording is retained as an ambiguity; its numerical options are not automatically graded.')
    resolve('Oracle', 'IMG-20240913-WA0048.jpg')
    resolve('Oracle', 'IMG-20240915-WA0088.jpg')

    add('oracle-downward-tree-path', 'Oracle', 'Maximum sum along a downward tree path',
        'Reconstructed from a solution-only collection: Given a nonempty rooted tree described by parent and values arrays, find the largest node-value sum along a nonempty downward path. It may begin at any node and end at a descendant, but every edge must move from parent to child. The unique root has parent −1.', None,
        'Visit parents before children. Let best_end[u] be the largest sum of a downward path ending at u. At the root it equals values[u]; elsewhere it is values[u]+max(0,best_end[parent[u]]). The answer is the largest best_end value. Initialise from a node value to handle all-negative trees. Build child lists and traverse iteratively rather than assuming parent indices precede their children or recursing down a deep chain. O(n) time and O(n) space. Unlike an unrestricted simple tree path, a downward path cannot join two child branches through their parent.',
        section='dsa', topic='trees', type='coding', sources=['Final_oracle_coding.pdf'],
        function_signature='bestSumDownwardTreePath(parent, values)',
        constraints='Arrays have equal positive length and describe a valid rooted tree. Original OA size/value bounds are not included in this solution-only source.',
        examples=[{'input':'parent = [-1,0,1,2,0]\nvalues = [-2,10,10,-3,10]', 'output':'20', 'explanation':'The downward path 1→2 gives 10+10; joining node 4 would require an upward edge.'}],
        notes='This problem definition is reconstructed from the titled implementation, not a verbatim OA statement. No official judge constraints or tests are available.')
