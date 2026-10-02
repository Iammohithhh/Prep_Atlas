class ListNode:
    def __init__(self, val=0):
        self.val = val
        self.next = None


def has_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            return True
    return False

# ---- tests
import random
def make(n, pos):
    nodes = [ListNode(i) for i in range(n)]
    for a, b in zip(nodes, nodes[1:]):
        a.next = b
    if n and pos >= 0:
        nodes[-1].next = nodes[pos]
    return nodes[0] if nodes else None
def brute(head):
    seen = set()
    while head:
        if id(head) in seen:
            return True
        seen.add(id(head))
        head = head.next
    return False
assert not has_cycle(None)
assert has_cycle(make(4, 1))
assert not has_cycle(make(4, -1))
for _ in range(300):
    n = random.randint(0, 12)
    pos = random.randint(-1, max(n - 1, -1))
    h = make(n, pos)
    assert has_cycle(h) == brute(h)
print('ok')
