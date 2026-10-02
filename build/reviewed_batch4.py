"""First Oracle screenshot group: reviewed questions and explicit omissions."""


def extend(add, merge, skip):
    merge('reverse-array','Oracle',['IMG-20240730-WA0068.jpg'])
    add('oracle-postfix','Oracle','Convert an arithmetic expression to postfix',
        'What is the postfix form of a + b*c + d*e?', 'abc*+de*+',
        'Multiplications precede addition. The expression groups as (a+(b*c))+(d*e). Postorder traversal emits a b c * + d e * +. Postfix notation does not retain parentheses.',
        section='dsa',topic='stack-queue',options=['abc*+de*+','abc+*de*+','a+bc*de+*','abc*+(de)*+'],sources=['IMG-20240730-WA0066.jpg'])
    add('oracle-nosql-choice','Oracle','Evaluate criteria for choosing a nonrelational database',
        'Which of these criteria is unsuitable as a reason to choose a nonrelational database?\n\n- Very low application latency\n- Unstructured data without relationships\n- Only serialization/deserialization of JSON, XML or YAML\n- Storing a very small amount of data',None,
        'None of these alone uniquely determines the right database. Small data volume does not rule out a document/key-value store, and low latency is possible with relational systems too. Serialization formats alone are not a workload requirement. Evaluate access patterns, transactions, consistency, indexing, operational needs and cost. The MCQ appears to expect the small-data option, but that is not a universally valid technical rule.',
        section='cs',topic='dbms',type='subjective',sources=['IMG-20240730-WA0071.jpg'],notes='The source’s single-answer framing is technically ambiguous; no answer is automatically graded.')
    add('oracle-sparse-matrix','Oracle','Store a symmetric sparse matrix efficiently',
        'How can a symmetric sparse matrix be represented efficiently? The source lists heap, binary tree, hash table and adjacency list as options.',None,
        'Store only nonzero entries rather than a dense n×n matrix. An adjacency-list representation records each row’s nonzero columns and values; symmetry can let you keep one triangle and reconstruct the other. Compressed sparse-row or coordinate formats are also common. A hash table keyed by (row,column) is another sparse representation, so the most efficient choice depends on lookup/update and traversal needs. Among the listed options, adjacency list is the conventional graph-style answer.',
        section='dsa',topic='matrix',type='subjective',sources=['IMG-20240730-WA0077.jpg'],notes='The MCQ does not define the operations or storage layout needed to distinguish adjacency lists from hash-based sparse storage.')
    add('oracle-23tree','Oracle','Assess comparisons between a 2–3 tree and a BST',
        'The source asks which statement is false:\n\n1. A 2–3 tree requires less storage than a BST.\n2. Lookup in a 2–3 tree is more efficient than in a BST.\n3. A 2–3 tree is shallower than a BST.\n4. A 2–3 tree is balanced.',None,
        'A 2–3 tree keeps every leaf at the same depth and has logarithmic height. An unbalanced BST can become a linear chain, so a 2–3 tree has better worst-case lookup against that baseline. A balanced BST also gives O(log n) lookup. Total memory depends on node layout, pointer counts and occupancy, so the claim of always requiring less storage is unjustified. The likely intended false statement is 1, but statements 2 and 3 also need a stated BST baseline.',
        section='dsa',topic='trees',type='subjective',sources=['IMG-20240730-WA0078.jpg'],notes='The source does not specify whether its BST is balanced or how storage is measured.')
    add('oracle-five-ingredients','Oracle','Deduce all five selected ingredients',
        'A chef selects exactly five of apricots, bacon, cake, donuts, eggs, figs, grapes, hazelnuts and ice cream.\n\n1. If bacon is not used, grapes, hazelnuts and ice cream are not used.\n2. If apricots are used, bacon and cake are used.\n3. If donuts are not used, apricots are not used.\n4. Apricots and eggs are used.\n\nHow many of the five selected ingredients are known?', '5',
        'Apricots and eggs are given. Apricots imply bacon and cake. The contrapositive of statement 3 says apricots imply donuts. These are five distinct selected ingredients, exhausting the quota, so all five are known.',
        topic='logical',options=['2','3','4','5'],sources=['IMG-20240730-WA0079.jpg'])
    add('oracle-painted-cube','Oracle','Small cubes with three painted faces',
        'A cube is painted green on every surface and cut into 1,000 identical smaller cubes. How many small cubes have three painted faces?', '8',
        'There are 10 subdivisions along each dimension. Only the eight corner cubes touch three outer faces. Edge-interior cubes touch two painted faces, face-interior cubes one, and interior cubes none.',
        options=['8','10','100','64'],sources=['IMG-20240730-WA0081.jpg'])
    add('oracle-favorite-color','Oracle','Find whose favorite color is black',
        'Jack, Matthew, Albert, Peter and Sebastian each have one distinct country, sport and favorite color. Countries: South Korea, UK, India, China, Russia. Sports: football, cricket, volleyball, badminton, squash. Colors: brown, green, red, black, yellow.\n\n1. Jack likes red and is not from India or China.\n2. Albert plays football, does not like yellow and is not from the UK.\n3. Peter and Sebastian like yellow and green, in some order.\n4. Matthew plays badminton and is from Russia.\n5. Peter and Sebastian are from China and the UK, in some order.\n6. The person from India likes brown.\n7. The person from China likes green.\n8. The South Korean plays squash and the UK resident volleyball; one of these two likes yellow.\n\nWho likes black?', 'Matthew',
        'Peter and Sebastian occupy China/UK and green/yellow. Matthew is from Russia. Jack is therefore from South Korea, leaving Albert in India with brown. Jack has red, so the remaining color black belongs to Matthew.',
        topic='logical',options=['Matthew','Albert','Peter','Sebastian'],sources=['IMG-20240730-WA0082.jpg','IMG-20240730-WA0089.jpg'])
    add('oracle-standing-order','Oracle','Find the middle person in a five-person row',
        'Peter, Tyson, Richard, Steve and Quinn stand in a row.\n\n1. Peter is next to Quinn; Steve is next to Richard.\n2. Steve is not next to Tyson.\n3. Tyson stands leftmost.\n4. Richard is second from the right.\n5. Peter stands somewhere right of both Quinn and Tyson.\n6. Peter and Richard are next to each other.\n\nWho is in the middle?', 'Peter',
        'Number positions 1…5 from the left. Tyson=1 and Richard=4. Peter must be 3 or 5. Position 5 would require Quinn in 4 to be adjacent and left of Peter, but Richard already occupies 4. Hence Peter=3, Quinn=2 and Steve=5. The order is Tyson, Quinn, Peter, Richard, Steve.',
        topic='logical',options=['Peter','Richard','Steve','Quinn'],sources=['IMG-20240730-WA0083.jpg'])
    add('oracle-autonomy','Oracle','Closest word for self-government',
        'Choose the closest listed word for “a self-governing country or region.”', 'Autonomy',
        'Autonomy means self-government or the ability to govern independently. Autocracy is rule by one person, anarchy is absence of government, and ethnology studies peoples and cultures. Strictly, autonomy is the condition of self-government rather than the name of a country, but it is the closest option.',
        topic='verbal',options=['Autonomy','Autocracy','Anarchy','Ethnology'],sources=['IMG-20240730-WA0084.jpg'])
    add('oracle-hiring-idiom','Oracle','Evaluate idioms in a hiring sentence',
        'Complete: “I don’t think we should hire him. He seems like ____.” Options: a fish out of water; the black sheep of the family; a wolf in sheep’s clothing; the apple of my eye.',None,
        'A wolf in sheep’s clothing describes someone dangerous or deceptive who appears harmless, and fits a warning against hiring. A fish out of water describes someone uncomfortable in unfamiliar surroundings, which could also fit without further context. The black sheep is a disreputable member of a family/group; the apple of my eye is someone cherished. The short sentence does not uniquely identify the intended reason.',
        topic='verbal',type='subjective',sources=['IMG-20240730-WA0085.jpg'],notes='No answer key or additional context is visible; no unique answer is auto-graded.')
    add('oracle-exam-idiom','Oracle','Interpret idioms after preparing for an exam',
        'Complete: “I’ve been studying for this exam for months, so I’m hoping to ____.” The options are hit the ground running, have a field day, be a dark horse, and have a lot on my plate.',None,
        'Hit the ground running means to begin effectively and energetically. Have a field day means to enjoy an opportunity greatly; a dark horse is an unexpected contender; having a lot on one’s plate means having many responsibilities. The expected meaning is likely a strong start, but an exam-success idiom such as ace the exam is not among the options. The wording does not establish a unique answer without the setter’s intended context.',
        topic='verbal',type='subjective',sources=['IMG-20240730-WA0086.jpg'],notes='The source provides no answer key. This is a discussion of the supplied choices rather than a graded answer.')
    add('oracle-sports-ambiguity','Oracle','Interpret ambiguous sports-survey totals',
        'A source MCQ says that 100 selected employees include 50 who like football, 40 who like hockey, and “the rest like both.” It asks how many like at least one game. Options: 40, 90, 80, 20.',None,
        'If 50 and 40 are inclusive category totals, the overlap must be supplied: union=50+40−overlap. Treating “the rest” as 100−50−40=10 gives 80, but then 20 employees like neither, contradicting a literal claim that every remaining employee likes both. If 50 and 40 mean exclusive categories and the remaining 10 like both, everyone likes at least one, giving 100, which is absent. Thus 80 is a plausible intended answer under an extra assumption, not a logically unambiguous consequence.',
        topic='quant',type='subjective',sources=['IMG-20240730-WA0087.jpg'],notes='The source’s wording is inconsistent under common interpretations; no option is marked as confidently correct.')
    add('oracle-only-cricket','Oracle','Percentage who like only cricket',
        'In a group of students, 60% like football, 40% like cricket and 12% like neither. What percentage like only cricket?', '28',
        'The union is 88%. Intersection=60%+40%−88%=12%. Cricket-only=40%−12%=28%. Equivalently, union minus football is 88%−60%=28%.',
        options=['28','14','56','42'],sources=['IMG-20240730-WA0088.jpg'])
    add('oracle-spawned-antonym','Oracle','Word farthest in meaning from spawned',
        'In a passage describing inventions that “spawned technology use today,” which word is farthest in meaning from spawned?', 'squelched',
        'Spawned means generated or brought into being. Fostered, begat and generated all suggest creation or encouragement. Squelched means suppressed or put an end to, so it is the opposite choice. The candidate’s selected option in the screenshot is not an answer key.',
        topic='verbal',options=['fostered','begat','generated','squelched'],sources=['IMG-20240730-WA0090.jpg','IMG-20240730-WA0091.jpg','IMG-20240730-WA0092.jpg','IMG-20240730-WA0094.jpg'])
    add('oracle-friend-groups','Oracle','Maintain friend groups and answer size-total queries',
        'Students have IDs 1…n and begin in separate groups. For each aligned query (queryType, student1, student2), Friend joins the two students’ groups, including indirect friendships. Total reports the sum of the sizes of the groups containing the two students. Return results for Total queries.',None,
        'Use disjoint-set union with path compression and union by size. Friend merges distinct roots and updates the new root’s size. Total finds both roots and adds their component sizes. O(n+q α(n)) total time and O(n) space. Under the literal sum-of-two-group-sizes rule, querying two students in the same group counts its size twice; a union-size interpretation would count it once, so confirm that corner case when implementing a judge.',
        section='dsa',topic='graphs',type='coding',sources=['IMG-20240730-WA0062.jpg','IMG-20240730-WA0063.jpg','IMG-20240730-WA0064.jpg','IMG-20240731-WA0142.jpg'],function_signature='getTheGroups(n, queryType, students1, students2)',
        examples=[{'input':'n = 4\nqueryType = ["Friend", "Friend", "Total"]\nstudents1 = [1, 2, 1]\nstudents2 = [2, 3, 4]','output':'[4]'}],notes='The screenshots do not show full upper bounds or an example querying the same connected group twice.')
    add('oracle-quiz-windows','Oracle','Shortest complete talent window from each index',
        'Each student has a talent in 1…talentsCount. Teams must contain at least one student of every talent and must be consecutive in the talent array. For every starting index, return the shortest valid team length starting exactly there, or −1 if no such team can be formed.',None,
        'Use a sliding window with counts of represented talents. For each left boundary, extend the right boundary until all talents occur or the array ends. If complete, record right−left; otherwise record −1. Remove the leftmost talent before advancing left, updating the distinct count when its frequency reaches zero. The right pointer never moves backward. O(n+talentsCount) time and space O(n+talentsCount), including the result. This asks for an answer at every start, rather than one globally smallest window.',
        section='dsa',topic='sliding-window',type='coding',sources=['IMG-20240801-WA0049.jpg','IMG-20240801-WA0050.jpg','IMG-20240801-WA0051.jpg','IMG-20240801-WA0052.jpg','IMG-20240801-WA0053.jpg','IMG-20240803-WA0034.jpg','IMG-20240803-WA0035.jpg'],function_signature='teamSize(talent, talentsCount)',constraints='1 ≤ n,talentsCount ≤ 10⁵; 1 ≤ talent[i] ≤ talentsCount.',
        examples=[{'input':'talent = [1,2,3,2,1], talentsCount = 3','output':'[3,4,3,-1,-1]'},{'input':'talent = [1,1,2,2,3,1,3,2], talentsCount = 3','output':'[5,4,4,3,4,3,-1,-1]'}])
    skip('Oracle','IMG-20240730-WA0080.jpg','route condition unreadable')
    skip('Oracle','IMG-20240730-WA0095.jpg','diagram needs transcription')
    skip('Oracle','IMG-20240730-WA0096.jpg','chart question missing')
    skip('Oracle','IMG-20240730-WA0097.jpg','chart question missing')
    skip('Meesho','WhatsApp Image 2024-08-31 at 12.22.43_7fbc91b6.jpg','graph specification cropped')
