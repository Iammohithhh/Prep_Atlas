"""Worker A, module 10: IBM multiple-choice questions."""

W = lambda *n: ['IMG-20240830-WA0%s.jpg' % x for x in n]


def sol(work, wrong, faster, traps):
    w = '\n'.join('- ' + x for x in wrong)
    t = '\n'.join('- ' + x for x in traps)
    return f'### Solution\n{work}\n\n### Why the other options are wrong\n{w}\n\n### Faster method\n{faster}\n\n### Common traps\n{t}\n'


def extend(add):
    def q(key, title, stmt, answer, expl, options, section, topic, sources, solution, conf='high', notes=None):
        kw = dict(options=options, section=section, topic=topic, type='mcq', sources=sources, solution=solution, confidence=conf)
        if notes:
            kw['notes'] = notes
        add(key, 'IBM', title, stmt, answer, expl, **kw)

    q('ibm-series-factorial', 'Complete the series A10 A12 B18 B42 __ C882',
      'Complete the following series: A10, A12, B18, B42, ___, C882.',
      'C162', 'The numbers differ by 2, 6, 24, 120, 720 (factorials 2!, 3!, 4!, 5!, 6!): 10, 12, 18, 42, 162, 882. The letters follow A, A, B, B, C, C.',
      ['B162', 'C162', 'B456', 'D456'], 'aptitude', 'quant', W('177'),
      sol('Differences between consecutive numbers: 12-10 = 2, 18-12 = 6, 42-18 = 24. These are 2!, 3!, 4!. The next difference is 5! = 120, so the missing number is 42 + 120 = 162; then 162 + 6! = 162 + 720 = 882, matching the last term. Letters come in pairs A, A, B, B, so the next pair starts with C: the fifth term is C162 and the sixth is C882.\n\n**Answer: C162**',
          ['B162: right number, but the letter pairs are A A B B C C.', 'B456 / D456: the number does not fit the factorial differences (456 - 42 = 414 is not a factorial).'],
          'Take differences first: 2, 6, 24 is an immediate factorial pattern; check the last term (882 - 162 = 720 = 6!).',
          ['Treating the letters as a separate cycle A, B, A, B.', 'Checking only one difference before committing.']))

    q('ibm-priority-inheritance', 'Real-time thread blocked on a mutex held by a non-preemptible thread',
      'Consider a complex multi-threaded Linux application that uses POSIX threads for parallel processing. The application has multiple threads accessing shared resources. One of the threads needs to perform a critical section of code protected by a mutex to ensure proper synchronization and prevent data corruption. Assume: (1) the thread that holds the mutex enters a non-preemptive state and cannot be forcibly preempted by the scheduler; (2) there is a real-time thread with higher priority that requires access to the same critical section protected by the mutex; (3) the real-time thread needs to be granted access to the critical section within a fixed time frame or it might cause a system failure. Which of the following statements is true?',
      'Implementing the priority inheritance protocol with the mutex will ensure the real-time thread\'s access to the critical section without compromising data integrity.',
      'Priority inheritance temporarily raises the priority of the mutex holder to that of the waiting real-time thread, so the holder finishes the critical section quickly and releases the mutex, bounding the real-time thread\'s wait without breaking mutual exclusion.',
      ['Since the thread holding the mutex cannot be preempted, the real-time thread will never be able to access the critical section.', 'The real-time thread will be granted access to the critical section and the mutex will be released from the non-preemptive thread, causing potential data corruption.', 'To avoid deadlock, the real-time thread will forcefully acquire the mutex, overriding the non-preemptive thread and prioritizing real-time execution.', 'Implementing the priority inheritance protocol with the mutex will ensure the real-time thread\'s access to the critical section without compromising data integrity.'],
      'cs', 'os', W('178', '182', '184', '227'),
      sol('This is the classic priority inversion problem: a high-priority thread waits for a mutex held by a lower-priority thread. With priority inheritance, the holder runs at the waiter\'s priority until it releases the mutex, so it cannot be starved by medium-priority threads and the real-time thread gets the lock in bounded time. Mutual exclusion is untouched, so data integrity is preserved.\n\n**Answer: implement the priority inheritance protocol.**',
          ['"Will never be able to access": the holder will eventually release the mutex; the issue is only the unbounded delay.', 'Forced release breaks mutual exclusion and can corrupt data.', 'Forcefully acquiring a held mutex is not possible with correct locking and would break data integrity.'],
          'Real-time + mutex + inversion = priority inheritance (or priority ceiling).',
          ['Confusing it with deadlock: nobody is waiting in a cycle.', 'Thinking preemption of the lock holder is allowed or safe.']))

    q('ibm-tcp-false-statement', 'Which statement about TCP packets is false?',
      'Which one of the following statements is FALSE?\nA) Three packets are sent to establish a TCP connection.\nB) The ACK packet from the receiver during TCP connection initiation has both the SYN and ACK bits set.\nC) Four packets are sent to terminate the TCP connection.',
      'None of these', 'A is true (SYN, SYN-ACK, ACK). B is true: the receiver\'s reply in the handshake is the SYN-ACK segment with both flags set. C is true: normal termination uses FIN, ACK, FIN, ACK. So no statement is false.',
      ['Only A', 'Only C', 'Both B and C', 'None of these'], 'cs', 'networks', W('179', '211', '212'),
      sol('Three-way handshake: the client sends SYN, the server answers SYN+ACK (both bits set), the client sends ACK: three packets (A true, B true). Connection teardown is a four-way exchange: FIN, ACK, FIN, ACK (C true; the middle two can be combined in some cases but the standard description has four packets).\n\n**Answer: None of these (no statement is false).**',
          ['Only A: the handshake does have three packets.', 'Only C: closing with four packets is the standard four-way termination.', 'Both B and C: both are true.'],
          'Recall the packets: SYN, SYN-ACK, ACK for opening; FIN, ACK, FIN, ACK for closing.',
          ['Reading B as "the final ACK"; the statement is about the receiver\'s reply, which is SYN+ACK.', 'Forgetting that TCP closing is four packets.'], ),
      conf='medium', notes='The wording of statement B is slightly garbled in the photos; it is read as the receiver\'s SYN-ACK reply, so no statement is false and the answer is "None of these".')

    q('ibm-employees-only-two', 'Employees who like exactly two of three departments',
      'In a company, 26 employees are in the HR department, 32 are in the technical department and 30 are in the management department. Of these, 5 employees are in all three departments and 37 are in only one of them. How many employees like only two of the three departments?',
      '18', 'Sum of department sizes = 26 + 32 + 30 = 88 = (only one) + 2·(only two) + 3·(all three) = 37 + 2x + 15, so 2x = 36 and x = 18.',
      ['13', '36', '18', '15'], 'aptitude', 'quant', W('185', '244'),
      sol('Count each employee once per department they are in: 26 + 32 + 30 = 88 memberships. Those in exactly one department contribute 37, those in all three contribute 3 × 5 = 15, and those in exactly two contribute 2x. So 88 = 37 + 2x + 15, giving 2x = 36 and **x = 18**.',
          ['13 and 15: arithmetic slips (not matching 2x = 36).', '36: this is 2x, the number of memberships of the two-department employees, not the number of employees.', '88 / 27 (in the other version): not consistent with the equation.'],
          'Total memberships = n1 + 2·n2 + 3·n3.',
          ['Forgetting to count the all-three group three times.', 'Answering 2x = 36.']))

    q('ibm-malloc-location', 'Where and when does malloc() allocate memory?',
      'The malloc() function in C/C++ allocates memory at which time/location?',
      'Execution time on heap', 'malloc is a runtime library call that reserves memory from the heap while the program runs.',
      ['Compilation time on stack', 'Linking time on stack', 'Load time on heap', 'Execution time on heap', 'Execution time on stack'], 'cs', 'c-cpp-output', W('189', '233'),
      sol('malloc is an ordinary function executed at run time. It asks the allocator (and ultimately the OS via brk/mmap) for a block from the heap and returns a pointer. Stack memory is used for local variables and is managed automatically; compile/link/load-time allocation applies to static and global data.\n\n**Answer: Execution time on heap.**',
          ['Compilation/link time: sizes passed to malloc are usually known only at run time.', 'Load time on heap: the loader sets up code/data segments, not malloc blocks.', 'Execution time on stack: that describes local variables or alloca().'],
          'malloc = dynamic = heap at run time.',
          ['Mixing up alloca (stack) with malloc (heap).']))

    q('ibm-history-last-commands', 'Which command lists the last three commands with their history IDs?',
      'Which of the following commands will list the last three commands you ran, excluding itself, with the history IDs of these commands?',
      'fc -l -3', 'fc -l -3 lists the last three commands from the history (the fc command itself is not included) along with their history numbers. fc -ln suppresses the numbers.',
      ['history -n 3', 'history -c 3', 'fc -l -3', 'fc -ln -3'], 'cs', 'os', W('194', '224'),
      sol('`fc -l N` lists commands from history. `fc -l -3` shows the last three commands before the fc invocation, with their event numbers. `fc -ln -3` also lists them but with the n flag omits the numbers. `history -n 3` is not a "list last 3" form (it reads new lines from the history file), and `history -c` clears the history.\n\n**Answer: fc -l -3**',
          ['history -n 3: -n means "read lines not yet read from the history file".', 'history -c 3: -c clears the history list.', 'fc -ln -3: no history IDs are printed because of the n flag.'],
          'Remember: fc -l lists, -n removes numbers.',
          ['Assuming history -n 3 shows the last 3 entries (that is history 3).', 'Forgetting that fc excludes itself while history includes itself.']),
      conf='medium', notes='The option text in the photographs is partly garbled (fc-1-3 is read as fc -l -3).')

    q('ibm-threads-global-variable', 'Two threads modifying a global variable',
      'A diagram shows a Linux process and its stack memory layout. The process has two threads, Thread1 and Thread2, each with its own stack, sharing the same address space. Thread1 is executing and making a function call, pushing data onto its stack. Simultaneously Thread2 is also executing and making its own function call, pushing data onto its stack. Both threads are using the same function with different arguments. What will happen if both threads modify a global variable within the function?',
      'The final value will be unpredictable since the order of their executions cannot be determined.',
      'Local variables and parameters live on each thread\'s own stack, but global variables are shared. Unsynchronised concurrent writes are a data race, so the final value depends on scheduling.',
      ['The global variable will be overwritten with the value from the thread that called the function last.', 'The global variable will be unaffected, as each thread has its own stack, isolating their modifications.', 'The final value will be unpredictable since the order of their executions cannot be determined.', 'The global variable will automatically be protected and only one thread can modify it at a time.'],
      'cs', 'os', W('197', '202', '254', '255'),
      sol('Threads share the code, data (including globals) and heap segments; only the stack (locals, return addresses) is private. If both threads write a global without a lock or atomic operation, the result is a race condition: the final value depends on the interleaving. Nothing in the hardware or the C runtime serialises accesses automatically.\n\n**Answer: unpredictable final value.**',
          ['"Last caller wins": not guaranteed; the interleaving of writes (and read-modify-write sequences) is arbitrary.', '"Unaffected because of own stacks": globals are not on the thread stack.', '"Automatically protected": there is no implicit mutual exclusion.'],
          'Shared memory + no synchronisation = race condition = unpredictable result.',
          ['Confusing thread-local stack data with global data.']))

    q('ibm-discount-percentage', 'Percentage discount for 12 items with a bonus discount',
      'A shopkeeper offered a discount of 15% on every item in the store. The discount is increased by 15% for customers who purchase more than 3 items at one time. What percentage discount will a customer receive if 12 items are purchased?',
      'None of these', 'An increase of 15% of the discount gives 15 × 1.15 = 17.25%, which is not among the options; an increase of 15 percentage points would give 30%. The statement is ambiguous.',
      ['30', '16.25', '225', 'None of these'], 'aptitude', 'quant', W('198'),
      sol('Reading 1 (relative increase): the discount rises by 15% of itself: 15% × 1.15 = 17.25%. This is not offered, so the answer would be "None of these".\nReading 2 (percentage points): 15% + 15% = 30%, which is offered.\nThe phrase "increased by 15%" most literally means a relative increase, giving 17.25%.\n\n**Answer: None of these (17.25%).**',
          ['30: only if the increase is read in percentage points.', '16.25: would need the 15% bonus to be 8.33% of the discount.', '225: 15 × 15, meaningless here.'],
          'Compute 15 × 1.15 and see whether it appears among the options.',
          ['Confusing "percent of a percent" with percentage points.', 'Multiplying by the number of items (12): the discount percentage does not depend on the count once it is above 3.']),
      conf='low', notes='The wording is ambiguous; the answer depends on whether "increased by 15%" is a relative or an absolute (percentage point) increase. The first option of the question is cropped in the photo.')

    q('ibm-fork-hello-count', 'How many times is "Hello" printed with a fork()?',
      'How many times does "Hello" get printed?\n\n```c\nint main() {\n    printf("Hello");\n    fork();\n    printf("Hello");\n}\n```',
      '4', 'printf without a newline only fills the stdout buffer. fork() copies the process including the buffered "Hello", so each of the two processes eventually prints "HelloHello": 4 Hello in total.',
      ['2', '3', '4', '6'], 'cs', 'c-cpp-output', W('201', '259'),
      sol('1. The first printf writes "Hello" into the stdout buffer. Because there is no newline (and stdout is line-buffered for a terminal, fully buffered otherwise) the text is not yet flushed.\n2. fork() duplicates the process, including the unflushed buffer: parent and child both hold "Hello".\n3. Each process executes the second printf, giving "HelloHello" in each buffer, flushed at exit.\nTotal = 2 × 2 = 4.\n\n**Answer: 4** (with a newline or fflush before fork the answer would be 3).',
          ['2: ignores the first print and the child.', '3: assumes the first Hello was already flushed before the fork.', '6: no mechanism produces six prints.'],
          'Buffered output is duplicated by fork: count prints per process after the fork plus the buffered prefix.',
          ['Assuming printf output is immediate.']),
      conf='medium', notes='The option values in the photographs are partly unclear (2, 3, 4, 6); the buffered-output interpretation gives 4.')

    q('ibm-kernel-panic', 'Most likely cause of a Linux kernel panic',
      'Which scenario is most likely to trigger a kernel panic error in the Linux operating system?',
      'Inserting a corrupt kernel module that conflicts with the existing kernel version',
      'Kernel code runs with full privilege, so a faulty or incompatible module can corrupt kernel memory and cause an unrecoverable error, i.e. a kernel panic. User-space problems are handled by the kernel without panicking.',
      ['Initiating a system call that attempts to access a non-existent hardware device', 'Inserting a corrupt kernel module that conflicts with the existing kernel version', 'Running a multi-threaded application that exceeds the system\'s maximum thread limit', 'Executing a memory-intensive scientific simulation with parallel processes'],
      'cs', 'os', W('204', '205', '253'),
      sol('A kernel panic is raised when the kernel itself detects a fatal internal error. Code loaded into the kernel (a module) runs in kernel mode; a corrupt or version-mismatched module can dereference bad pointers or break kernel data structures, leaving the kernel unable to continue.\n\n**Answer: inserting a corrupt kernel module that conflicts with the kernel version.**',
          ['System call to a missing device: the call fails with an error code (e.g. ENODEV).', 'Exceeding the thread limit: pthread_create returns EAGAIN.', 'Memory-intensive simulation: the OOM killer or swapping handles it; the kernel does not panic.'],
          'Kernel panic = fault in kernel-mode code; only the module option runs inside the kernel.',
          ['Confusing a user-space crash (segmentation fault) with a kernel panic.']))

    q('ibm-scp-root-file', 'Copy a root-only log file to a remote server',
      'A Linux system administrator needs to securely transfer a file named myapp.log from a local server to a remote server. The administrator has regular user privileges and the myapp.log file can only be accessed by the root user. Which command should the administrator use?',
      'sudo -u root scp /path/to/myapp.log ubuntu@10.0.1.34:/remote-dir/my-location/',
      'The file is readable only by root, so scp must run with root privileges: sudo -u root scp <file> <user@host:dir>. Changing the ownership of a root-owned file is unnecessary.',
      ['sudo scp -i /root/.ssh/id_rsa /path/to/myapp.log ubuntu@10.0.1.34:/remote-dir/my-location/', 'sudo -u root scp /path/to/myapp.log ubuntu@10.0.1.34:/remote-dir/my-location/', 'sudo -u root chown root /path/to/myapp.log && sudo -u root scp /path/to/myapp.log ubuntu@10.0.1.34:/remove-dir/my-location/'],
      'cs', 'os', W('207', '209', '225'),
      sol('scp reads the local file with the privileges of the invoking user. Since only root may read myapp.log, run scp under sudo: `sudo -u root scp /path/to/myapp.log ubuntu@10.0.1.34:/remote-dir/my-location/`. The file is already owned by root, so chown is a no-op, and the third command also has a misspelt destination directory (remove-dir).\n\n**Answer: sudo -u root scp ...**',
          ['sudo scp -i /root/.ssh/id_rsa ...: also runs as root but depends on root having a key at that path; the plain form is the simplest correct answer.', 'chown option: unnecessary (the file is already root-owned) and uses a different remote directory name.'],
          'Need root to read the file → prefix the scp with sudo.',
          ['Changing ownership instead of elevating privileges.', 'Mistyping paths in the options.']),
      conf='medium', notes='The three options were read from partly garbled photos; the second option is the simplest correct command.')

    q('ibm-fast-exponent-output', 'Output of a recursive fast exponentiation',
      'Guess the output of the following program:\n\n```java\npublic static int fun(int x, int n) {\n    if (n == 0) return 1;\n    else if (n % 2 == 0) return fun(x * x, n / 2);\n    else return x * fun(x * x, (n - 1) / 2);\n}\npublic static void main() {\n    int ans = fun(2, 10);\n    System.out.println(ans);\n}\n```',
      '1024', 'fun(x, n) computes x^n by repeated squaring: fun(2,10) = fun(4,5) = 4·fun(16,2) = 4·fun(256,1) = 4·256·fun(65536,0) = 1024.',
      ['1023', '2048', '1024', 'None of these'], 'cs', 'java-output', W('208', '221', '231'),
      sol('Trace: fun(2,10): n even → fun(4,5). n=5 odd → 4·fun(16,2). n=2 even → fun(256,1). n=1 odd → 256·fun(65536,0) = 256·1. Back up: 4 · 256 = 1024. (Also 2^10 = 1024.)\n\n**Answer: 1024**',
          ['1023 / 2048: off-by-one slips (2^10 - 1, 2^11).', 'None of these: 1024 is an option.'],
          'Recognise exponentiation by squaring: the result is x^n = 2^10.',
          ['Not squaring x in the recursive call.']))

    q('ibm-binary-to-base3', 'Convert (1101)2 to base 3',
      'Number represented by y in the equation (1101)_2 = (y)_3.',
      '111', '(1101)_2 = 8 + 4 + 1 = 13. In base 3: 13 = 1·9 + 1·3 + 1, so y = 111.',
      ['120', '101', '102', '111'], 'aptitude', 'quant', W('213', '260'),
      sol('Binary to decimal: 1·8 + 1·4 + 0·2 + 1·1 = 13. Decimal to base 3: 13 ÷ 3 = 4 remainder 1; 4 ÷ 3 = 1 remainder 1; 1 ÷ 3 = 0 remainder 1. Reading the remainders from the last to the first: 111.\n\n**Answer: 111**',
          ['120_3 = 15, 101_3 = 10, 102_3 = 11: none equals 13.'],
          'Convert to decimal (13) then check each option: 111_3 = 9 + 3 + 1 = 13.',
          ['Reading the remainders in the wrong order.']))

    q('ibm-dictionary-data-structure', 'Data structure for a key-value dictionary',
      'Select the data structure suitable for implementing a dictionary with key-value pairs.',
      'Hash Table', 'A hash table gives average O(1) insertion, lookup and deletion by key, the typical implementation of a dictionary.',
      ['Array', 'Stack', 'Hash Table', 'Queue'], 'dsa', 'hashing', W('214'),
      sol('A dictionary maps keys to values and must support fast lookup by key. A hash table computes an index from the key, giving expected constant-time operations. Stacks and queues only give access at their ends, and a plain array is indexed by position, not by arbitrary keys.\n\n**Answer: Hash Table**',
          ['Array: only integer indices; searching by key is O(n).', 'Stack: LIFO access only.', 'Queue: FIFO access only.'],
          'Key-value → hash table (or balanced BST for ordered maps).',
          ['Choosing an array because it is "fast"; it is only fast for index access.']))

    q('ibm-c-macro-statement', 'Which statement about C macros is correct?',
      'Which one of the following statements is correct?',
      'Once preprocessing is over and the program is sent for compilation, the macros are removed from the expanded source code.',
      'Macros are expanded by the preprocessor before compilation, so the compiler sees only the expanded text. They are textual, need not be upper case, have no scope rules like variables, and a macro call is replaced inline rather than transferring control.',
      ['A macro must be defined in capital letters.', 'Once preprocessing is over and the program is sent for compilation, the macros are removed from the expanded source code.', 'Macros have a local scope.', 'In a macro call, the control is passed to the macro.'],
      'cs', 'c-cpp-output', W('216', '217'),
      sol('The C preprocessor performs textual substitution before compilation. After preprocessing, no macro names remain: all uses have been replaced by their expansions, so the compiler never sees macros.\n\n**Answer: macros are removed from the expanded source once preprocessing is over.**',
          ['Capital letters are only a convention.', 'Macros are not scoped like local variables; they are visible from #define to #undef or end of file.', 'A macro call is not a function call: there is no control transfer, only inline text replacement.'],
          'Think of macros as find-and-replace done before the compiler runs.',
          ['Treating macros like functions.']))

    q('ibm-circular-list-use', 'What can a circular linked list implement?',
      'A circular linked list can be used to implement:',
      'Both', 'A circular linked list supports O(1) insertion and removal at both ends (with a tail pointer), so it can implement both a stack and a queue.',
      ['A stack', 'A queue', 'Both', 'Neither'], 'dsa', 'linked-list', W('219'),
      sol('Stack: push/pop at the head of a circular list. Queue: enqueue at the tail and dequeue at the head, which is natural for a circular list that keeps only a tail pointer (head = tail.next). Hence both can be implemented.\n\n**Answer: Both**',
          ['A stack / A queue alone: each is possible, but the question asks what it can be used for in general.', 'Neither: incorrect.'],
          'Any singly linked structure with head/tail access can serve both.',
          ['Thinking circularity restricts the operations.']))

    q('ibm-bash-default-env', 'File with default environment variables for bash',
      'Which file contains the default environment variables when using the bash shell?',
      '~/.profile', 'Of the options, ~/.profile is the per-user login startup file where environment variables are defined (bash reads ~/.bash_profile, ~/.bash_login or ~/.profile on login).',
      ['~/.profile', '~/.bash', '/etc/profile.d', '~/bash'], 'cs', 'os', W('220', '256'),
      sol('On login, bash reads /etc/profile and then the first existing of ~/.bash_profile, ~/.bash_login, ~/.profile. Environment variables (exported variables like PATH) are normally set there. ~/.bash and ~/bash are not standard files, and /etc/profile.d is a directory of scripts sourced by /etc/profile, not the single default file.\n\n**Answer: ~/.profile**',
          ['~/.bash and ~/bash: not standard bash startup files.', '/etc/profile.d: a directory of system-wide snippets, not "the" file.'],
          'Login shell environment lives in ~/.profile (or ~/.bash_profile).',
          ['~/.bashrc is for interactive non-login shells and is not listed.']),
      conf='low', notes='The question could also be answered with the system file /etc/profile, which is not among the options.')

    q('ibm-linear-search-complexity', 'Time complexity of linear search',
      'Determine the time complexity of linear search in an array of size n.',
      'O(n)', 'Linear search inspects elements one by one; in the worst case it examines all n.',
      ['O(1)', 'O(log n)', 'O(n)', 'O(n^2)'], 'dsa', 'arrays', W('226'),
      sol('In the worst case (key absent or at the last position) the loop compares n elements, so the time is Θ(n); the average case is about n/2, also O(n).\n\n**Answer: O(n)**',
          ['O(1): only best case (first element).', 'O(log n): binary search on sorted data.', 'O(n²): nested loops.'],
          'One loop over the data = O(n).',
          ['Quoting the best case instead of the worst case.']))

    q('ibm-harmonic-recurrence', 'Complexity of R(n) = R(n-1) + 1/n',
      'Consider the recurrence relation R(a) = R(a-1) + 1/a. Find the time complexity of R(n).',
      'O(log n)', 'Unrolling gives R(n) = 1 + 1/2 + ... + 1/n = H_n, the harmonic number, which is Θ(log n).',
      ['O(log n)', 'O(n)', 'O(n log n)', 'O(log log n)'], 'dsa', 'math', W('229'),
      sol('Expand: R(n) = R(n-1) + 1/n = R(n-2) + 1/(n-1) + 1/n = ... = R(0) + sum_{k=1..n} 1/k = H_n ≈ ln n + 0.577. The harmonic series grows like ln n, so R(n) = Θ(log n).\n\n**Answer: O(log n)**',
          ['O(n): the terms 1/k are not constants; summing n of them gives log n, not n.', 'O(n log n) / O(log log n): do not match the harmonic sum.'],
          'Recognise the harmonic series.',
          ['Treating each step as cost 1 (that would be O(n)).']))

    q('ibm-js-pass-by-value', 'Does JavaScript pass parameters by value or reference?',
      'Does JavaScript always pass parameters by value or by reference? Select the most accurate answer.',
      'value', 'JavaScript always passes arguments by value. For objects the value that is copied is the reference, so mutating the object is visible to the caller, but reassigning the parameter is not.',
      ['reference', 'depends on the parameter type', 'value', 'prefixing the parameter by \'&\' will pass it by reference'], 'cs', 'general-cs', W('230'),
      sol('Every argument is copied. For primitives the copy is the value; for objects the copy is the (pointer-like) reference, which is why mutations through it are visible but `param = {...}` has no effect on the caller. Technically this is call-by-sharing, still pass-by-value. JavaScript has no & operator for references.\n\n**Answer: value**',
          ['reference: references are copied, not aliased to the caller\'s variable.', 'depends on the parameter type: the mechanism is the same; only what is copied differs.', '&: not JavaScript syntax.'],
          'No pass-by-reference in JS; objects are passed by sharing.',
          ['Believing object mutations prove pass-by-reference.']),
      conf='medium')

    q('ibm-clean-conditional', 'Clean a long conditional expression',
      'What is a good way to clean the conditional expression?\n\n```js\nif (user.experience > 6 && user.earnings >= 5000 && user.contracts > 60 && user.warnings == 0) {\n    sendInvitation(user);\n    user.risingTalent = true;\n}\n```',
      'Move the complex conditional into its own separate function.', 'A well-named predicate function (e.g. isRisingTalent(user)) documents intent and keeps the if readable without changing behaviour.',
      ['Each component of the expression should be moved to a separate if statement.', 'Remove user.warnings == 0 from the expression.', 'Move the complex conditional into its own separate function.', 'Add an else statement at the end.'], 'cs', 'software-engineering', W('232'),
      sol('Clean-code practice: extract a complex boolean expression into a function with a descriptive name, so the call site reads like English and the conditions can be tested separately.\n\n**Answer: move it into its own function.**',
          ['Separate ifs change the logic (nesting) and make the code longer.', 'Removing a condition changes behaviour.', 'An else branch does not clean the expression.'],
          'Look for the refactoring that keeps behaviour: extract function.',
          ['Choosing options that alter the semantics.']))

    q('ibm-js-create-object', 'Correct ways to create a JavaScript object',
      'Which are correct ways to create a JavaScript object? (pick one or more)',
      'const data = {Name:"Tom", Roll:35}; and function data(){this.Name="Tom"; this.Roll=35;}', 'An object literal creates an object directly and a constructor function can be used with new. The class and struct snippets shown are not valid syntax.',
      ['const data = {Name:"Tom", Roll:35};', 'class data {this.Name="Tom"; this.Roll=35;}', 'struct data {this.Name="Tom"; this.Roll=35;}', 'function data(){this.Name="Tom"; this.Roll=35;}'], 'cs', 'general-cs', W('234'),
      sol('1. An object literal is valid: correct.\n2. A class body cannot contain bare statements like `this.Name = ...;`; assignments belong in the constructor: invalid as written.\n3. JavaScript has no `struct`: invalid.\n4. A function used as a constructor (`new data()`) sets properties on this: valid.\n\n**Answer: options 1 and 4.**',
          ['Option 2: statements are not allowed directly inside a class body.', 'Option 3: no struct keyword.'],
          'Literal and constructor function are the two classic forms (plus class with constructor() and Object.create).',
          ['Accepting the class option because classes exist; the syntax shown is wrong.']),
      conf='medium', notes='Multiple-select question; the official answer is not shown.')

    q('ibm-js-window-document', 'True statements about window and document',
      'Two of the most commonly used DOM elements are window and document. Which of the following are true about them? Choose one or more.',
      'The window element can be used to affect and react to events related to browser behavior; both window and document are singletons within a page.', 'window is the global browser object (resize, scroll, load events, location, history); document represents the loaded page. A page has exactly one of each.',
      ['Both window and document represent the same element. They are just named differently across different browsers.', 'The window element can be used to affect and react to events related to browser behavior.', 'A document element can be used to affect and react to events related to browser behavior.', 'Both window and document are singletons within a page. This means that there is always exactly one window and exactly one document instance for a page.'],
      'cs', 'general-cs', W('235'),
      sol('- They are different objects: window is the browser window/global object, document is the DOM of the loaded page: option 1 false.\n- window exposes browser-level events (resize, scroll, beforeunload, ...): option 2 true.\n- document deals with the page content/DOM events, not browser behaviour: option 3 false.\n- One window and one document per page (frames have their own): option 4 true.\n\n**Answer: options 2 and 4.**',
          ['Option 1: they are different objects.', 'Option 3: browser-behaviour events belong to window.'],
          'window = browser, document = page content.',
          ['Believing the two names are synonyms.']),
      conf='medium', notes='Multiple-select question; the official answer is not shown.')

    q('ibm-js-object-types', 'Which values are objects in JavaScript?',
      'Which of the following is considered an object in JavaScript? (pick one or more)',
      'function', 'Functions are objects. true, 10 and a string literal are primitive values (though they are wrapped temporarily in objects when methods are called).',
      ['function', 'true', '10', 'string'], 'cs', 'general-cs', W('236'),
      sol('JavaScript primitives are string, number, boolean, null, undefined, symbol and bigint. `true`, `10` and a string literal are primitives. A function is an object (it can have properties and is an instance of Function).\n\n**Answer: function**',
          ['true / 10 / string: primitives, not objects.'],
          'typeof gives "function" for functions, but they are still objects (functions inherit from Object).',
          ['Confusing wrapper objects (new String) with string primitives.']),
      conf='medium', notes='Multiple-select question; the official answer is not shown.')

    q('ibm-js-iife-counter', 'Output of a closure counter called three times',
      'What is the output of the following code?\n\n```js\nconst func = (function () {\n    let counter = 0;\n    return function () {\n        return counter++;\n    }\n})();\n\nlet result = func();\nresult = func();\nresult = func();\nconsole.log(result);\n```',
      '2', 'The IIFE creates a private counter. Post-increment returns the old value, so the three calls return 0, 1, 2; result holds the last one, 2.',
      ['Error', '0', '2', '3'], 'cs', 'general-cs', W('238'),
      sol('The immediately invoked function runs once, creating `counter = 0` and returning the inner function (a closure). Each call returns `counter++`: the current value, then increments. Calls: 0, then 1, then 2. After the third call `result` = 2.\n\n**Answer: 2**',
          ['Error: no error occurs.', '0: only the first call.', '3: that would be the counter after the call (++counter or the next value).'],
          'Post-increment returns the old value: three calls → 0, 1, 2.',
          ['Confusing counter++ with ++counter.']),
      conf='medium', notes='Only three options (Error, 0, 2) are clearly visible; a fourth option may be cropped.')

    q('ibm-js-function-length', 'function.length with default and rest parameters',
      'Predict the output:\n\n```js\nfunction test(a, b = 1, c, ...args) { }\nconsole.log(test.length)\n```',
      '1', 'Function.length counts the parameters before the first one with a default value and excludes the rest parameter: only a counts.',
      ['4', '3', '2', '1'], 'cs', 'general-cs', W('240'),
      sol('`length` is the number of parameters expected by the function, defined as the count of parameters up to (not including) the first parameter with a default value or the rest parameter. Here the first parameter with a default is b, so only `a` counts: length = 1.\n\n**Answer: 1**',
          ['4: counts all parameters including b, c and the rest parameter.', '3: counts a, b, c.', '2: counts a and b.'],
          'Stop counting at the first default value.',
          ['Counting c, which comes after a default parameter.']))

    q('ibm-js-hasownproperty', 'hasOwnProperty on a class instance and an Object.create object',
      'Predict the output:\n\n```js\nclass test {\n    name = "test"\n    printName() { }\n}\nconst ob1 = new test();\nconst ob2 = Object.create(test);\nconsole.log(ob1.hasOwnProperty(\'name\') == ob2.hasOwnProperty(\'name\'));\nconsole.log(ob1.hasOwnProperty(\'printName\') == ob2.hasOwnProperty(\'printName\'));\n```',
      'false true', 'ob1 has an own property name (class field), ob2 has none (own properties of the class constructor function are not its own), so the first comparison is true == false → false. printName is on the prototype, so both hasOwnProperty calls return false → false == false → true.',
      ['false true', 'true true', 'true false', 'false false'], 'cs', 'general-cs', W('243'),
      sol('- `ob1 = new test()`: the class field `name` is created as an own property of the instance → `ob1.hasOwnProperty("name")` = true.\n- `ob2 = Object.create(test)` creates a plain object whose prototype is the class constructor function; it has no own properties → false.\n- First line: true == false → **false**.\n- `printName` is a method defined on `test.prototype`, not an own property of ob1 → false; ob2 → false. false == false → **true**.\n\n**Answer: false true**',
          ['true true / true false / false false: do not match the two comparisons computed above.'],
          'Own vs inherited: fields are own, methods are on the prototype, and Object.create(F) does not copy anything.',
          ['Thinking methods defined in a class are own properties of each instance.']))

    q('ibm-virtual-memory-concept', 'What is virtual memory?',
      'Identify the concept of virtual memory in an operating system.',
      'Secondary storage (e.g. hard disk) used as an extension of RAM', 'Virtual memory lets processes use more address space than physical RAM by backing pages on secondary storage and swapping them in on demand.',
      ['Additional physical RAM', 'Secondary storage (e.g., hard disk) used as an extension of RAM', 'RAM allocated for system processes only', 'Memory reserved for graphics processing'], 'cs', 'os', W('237', '257'),
      sol('Virtual memory maps each process\'s virtual addresses onto physical frames; pages not currently in RAM live on disk (swap/page file). Demand paging brings them back when needed, so disk acts as an extension of RAM.\n\n**Answer: secondary storage used as an extension of RAM.**',
          ['Additional physical RAM: virtual memory does not add RAM.', 'RAM for system processes only: unrelated.', 'Graphics memory: unrelated.'],
          'Virtual memory = disk-backed address space.',
          ['Thinking it increases physical RAM.']))

    q('ibm-shared-ram-section', 'Which memory section is shared between a process and its thread?',
      'Which section of RAM is shared between a process and a thread?',
      'Heap', 'Threads of a process share the heap (and also the code and data segments); each thread has its own stack. Among the options the heap is the section commonly named as shared.',
      ['Heap', 'Stack', 'Data', 'Code'], 'cs', 'os', W('239'),
      sol('A process\'s threads share its code (text), data (globals) and heap; only the stack (and registers) is private to each thread. So the stack is definitely not shared. The question asks for a single section; the heap is the dynamically allocated memory that threads typically share.\n\n**Answer: Heap**',
          ['Stack: private to each thread.', 'Data and Code: also shared by threads, so the question is loosely phrased.'],
          'Eliminate Stack; of the rest pick the commonly cited shared dynamic area: heap.',
          ['Over-thinking: the data and code segments are shared too.']),
      conf='low', notes='The question allows more than one correct reading since code and data are also shared among threads; heap is chosen as the usual single answer.')

    q('ibm-os-responsibilities', 'Responsibilities of an operating system',
      'Which of the following are the responsibilities of an OS? (pick one or more)',
      'Process Management; Memory Management; Security; Performance', 'An OS schedules processes, manages memory, enforces protection and security, and tunes resource usage for performance.',
      ['Process Management', 'Memory Management', 'Security', 'Performance'], 'cs', 'os', W('241', '258'),
      sol('Core duties of an OS: process management (creation, scheduling, synchronisation), memory management (allocation, virtual memory), security/protection (access control, isolation), and performance (resource allocation, I/O scheduling, monitoring). All four options are standard responsibilities.\n\n**Answer: all four.**',
          ['None of the options is wrong.'],
          'When every option is a typical OS function, select all.',
          ['Selecting only the two textbook items (process and memory management).']),
      conf='medium', notes='Multiple-select question; the official answer is not shown.')

    q('ibm-static-variable-storage', 'Where are static, initialised static and local variables stored?',
      'Consider the following code snippet:\n\n```c\nstatic int a;\nstatic int b = 10;\nvoid func() {\n    int c;\n}\n```\nWhere are the variables a, b, c stored in RAM respectively?',
      'BSS, Data, Stack', 'Uninitialised static data goes to the BSS segment, initialised static data to the data segment, and locals to the stack.',
      ['Stack, Heap, BSS', 'Heap, Code, BSS', 'BSS, Data, Stack', 'Data, Heap, Stack'], 'cs', 'c-cpp-output', W('242'),
      sol('- `static int a;` is uninitialised static storage → BSS segment (zero-initialised at start).\n- `static int b = 10;` is initialised static storage → data segment.\n- `int c;` inside a function is an automatic variable → the stack frame of func.\n\n**Answer: BSS, Data, Stack**',
          ['Stack, Heap, BSS: a is not on the stack and b is not on the heap.', 'Heap, Code, BSS: statics are not on the heap and variables are not in the code segment.', 'Data, Heap, Stack: a is in BSS (uninitialised), and b is not on the heap.'],
          'Initialised static → Data, uninitialised static → BSS, local → Stack, malloc → Heap.',
          ['Putting uninitialised statics in the data segment.']),
      conf='medium', notes='The fourth option is cropped in the photograph.')

    q('ibm-c-preprocessing', 'What is part of the C preprocessing stage?',
      'Which of the following are used as part of the preprocessing stage in C? (pick one or more)',
      'Macros; Conditional Compilation; Include Guards', 'Macros (#define), conditional compilation (#if/#ifdef) and include guards (#ifndef/#define/#endif) are preprocessor features; function calls are compiled and executed later.',
      ['Macros', 'Function calls', 'Conditional Compilation', 'Include Guards'], 'cs', 'c-cpp-output', W('245'),
      sol('The preprocessor handles directives starting with #: macro definition/expansion, #include, conditional compilation (#if, #ifdef, #else) and include guards, which are just conditional compilation around a header. Function calls are part of the program logic, translated by the compiler and executed at run time.\n\n**Answer: Macros, Conditional Compilation, Include Guards.**',
          ['Function calls: not a preprocessing operation.'],
          'If it starts with # (or is built from # directives) it is preprocessing.',
          ['Counting function-like macros as function calls.']),
      conf='medium', notes='Multiple-select question; the official answer is not shown.')

    q('ibm-infinite-recursion', 'What happens if a function calls itself infinitely?',
      'What would happen if a function keeps calling itself infinitely? (pick one or more)',
      'Stack Overflow; Segmentation Fault', 'Every call pushes a stack frame; eventually the call stack is exhausted (stack overflow), which the OS typically reports as a segmentation fault.',
      ['Heap Overflow', 'Buffer Overflow', 'Stack Overflow', 'Segmentation Fault'], 'cs', 'c-cpp-output', W('246'),
      sol('Each recursive call allocates a new frame (return address, parameters, locals) on the call stack, which has limited size. Without a base case the stack is exhausted: a stack overflow. In C/C++ on Linux the process then receives SIGSEGV, shown as a segmentation fault. Heap overflow and buffer overflow concern heap allocations and array bounds, not unbounded recursion.\n\n**Answer: Stack Overflow and Segmentation Fault.**',
          ['Heap Overflow: the heap is not consumed by plain recursion.', 'Buffer Overflow: that is writing past the end of an array.'],
          'Infinite recursion → call stack runs out.',
          ['Selecting only one of the two (the second is the visible symptom).']),
      conf='medium', notes='Multiple-select question; the official answer is not shown.')

    q('ibm-memory-fit-fast', 'Fast memory allocation strategy',
      'Which memory management technique is considered fast for modern-day operating systems?',
      'First Fit', 'First Fit stops at the first hole that is large enough, so it needs less searching than Best Fit and Worst Fit, which scan all holes.',
      ['Best Fit', 'First Fit', 'Next Fit', 'Worst Fit'], 'cs', 'os', W('247'),
      sol('First Fit scans the free list and takes the first block that fits, so on average it examines far fewer holes than Best Fit or Worst Fit, which must scan all of them. It is also known to leave a decent fragmentation profile in practice.\n\n**Answer: First Fit**',
          ['Best Fit: scans the entire free list and leaves tiny unusable holes.', 'Worst Fit: scans the entire list and performs poorly in practice.', 'Next Fit: starts the search where the previous one ended; typically no better than first fit in fragmentation.'],
          'Fast = stops at the first match.',
          ['Next Fit is also quick; the commonly quoted answer is First Fit.']),
      conf='low', notes='Next Fit is a defensible alternative; the usual textbook answer is First Fit.')
