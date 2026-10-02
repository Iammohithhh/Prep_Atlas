import heapq


def process(balances, requests):
    bal = list(balances)
    pending = []                                   # min-heap of (time, account index, amount)
    for idx, req in enumerate(requests, 1):
        kind, ts, holder, amount = req.split()
        ts, holder, amount = int(ts), int(holder), int(amount)
        while pending and pending[0][0] <= ts:     # cashback at the same second happens first
            _, acc, cash = heapq.heappop(pending)
            bal[acc] += cash
        if not 1 <= holder <= len(bal):
            return [-idx]
        if kind == 'deposit':
            bal[holder - 1] += amount
        else:
            if amount > bal[holder - 1]:
                return [-idx]
            bal[holder - 1] -= amount
            heapq.heappush(pending, (ts + 86400, holder - 1, amount * 2 // 100))
    return bal

# ---- tests
assert process([1000, 1500], ["withdraw 1613327630 2 480", "withdraw 1613327644 2 800", "withdraw 1614105244 1 100",
                              "deposit 1614108844 2 200", "withdraw 1614108845 2 150"]) == [900, 295]
assert process([10], ["withdraw 5 1 20"]) == [-1]
assert process([10], ["deposit 5 1 1", "deposit 6 2 5"]) == [-2]
# cashback exactly 24h later is credited before a same-second withdrawal
assert process([100], ["withdraw 0 1 100", "withdraw 86400 1 2"]) == [0]
print('ok')
