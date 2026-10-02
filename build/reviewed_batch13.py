"""Atlassian repeated photographs: exponent-product parity and minimum swap cost."""


def extend(add, merge):
    add('atlassian-product-parity','Atlassian','Parity of a sum of character-power products',
        'An array s contains lowercase strings. For each string, multiply ord(c)^m over all its characters, where ord(a)=97 through ord(z)=122. Add these string products and return EVEN or ODD according to the sum’s parity.',None,
        'For any positive integer m, ord(c)^m has the same parity as ord(c). A string product is odd exactly when every character has odd ordinal, namely a,c,e,…,y. XOR one parity bit for every such string; an odd number of odd products gives ODD. No large powers or products need to be constructed. O(total character count) time and O(1) extra space. If m=0 is allowed, every factor equals one, so each nonempty string contributes one and the answer depends only on the number of strings. The exponent’s allowed range is cropped: negative exponents would no longer define integer parity and require clarification.',
        section='dsa',topic='math',type='coding',
        sources=[f'63030732556317317{i}.jpg' for i in range(50,62)],
        function_signature='solve(m, s)',
        constraints='Lowercase a–z; 2 ≤ number of strings ≤ 20; 1 ≤ string length ≤ 10⁵; up to 50 test cases. The exponent bounds are cut off.',
        examples=[{'input':'m = 2, s = ["abc","abcd"]','output':'EVEN','explanation':'Both products contain the even factor ord(b).'}, {'input':'m = 47, s = ["azbde","abcher","acegk"]','output':'ODD','explanation':'Only acegk has all odd ordinals.'}],
        notes='The exact exponent bounds are missing; the positive-exponent solution and zero-exponent extension are distinguished explicitly.')
    add('atlassian-rearrange-students','Atlassian','Minimum cost to balance two lines of student heights',
        'Two arrays arrA and arrB each contain n positive student heights. Rearranging within a line is free. Swapping a student from A with one from B costs the smaller of their two heights. Find the minimum total swap cost that makes the two height multisets equal, or −1 if impossible.',None,
        'Count each height in the combined arrays. If any combined count is odd, equality is impossible. Let d[h]=countA[h]−countB[h]; A must export d[h]/2 copies when d[h]>0, and B must export −d[h]/2 copies when d[h]<0. All differences must be even, including negative ones. Build the two excess lists, sort one ascending and the other descending, and pair them. For each pair (a,b), pay min(a,b,2g), where g is the global minimum height across both arrays. The 2g route swaps through g twice and restores g to its original line while exchanging a and b. Pairing opposite orders gives the cheapest direct minima; the same 2g cap applies independently to every exchange. Sum costs using a wide integer. O(n log n) time and O(n) space. [LeetCode 2561](https://leetcode.com/problems/rearranging-fruits/) has the same cost model.',
        section='dsa',topic='greedy',type='coding',hard=True,
        sources=[f'63030732556317318{i}.jpg' for i in (16,17,18,19,20,22)],
        function_signature='rearrangeStudents(arrA, arrB)',constraints='1 ≤ n ≤ 2×10⁵; 1 ≤ heights ≤ 10⁹.',
        examples=[{'input':'arrA = [4,2,2,2]\narrB = [1,4,1,2]','output':'1','explanation':'Swap a 2 in A with a 1 in B.'}],
        leetcode={'name':'Rearranging Fruits','url':'https://leetcode.com/problems/rearranging-fruits/','similarity':'same'},
        notes='A matching title/implementation also occurs in Oracle’s solution collections; the complete prompt and constraints are recovered from Atlassian’s photographs. One solution collection wrongly labels this cost-1 sample as 6.')
    merge('atlassian-rearrange-students','Oracle',['DOC-20240809-WA0022.pdf','Final_oracle_coding.pdf'])
