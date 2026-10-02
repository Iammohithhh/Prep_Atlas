def srtf_average_wait(procs):
    """procs = [(arrival, burst), ...]; preemptive shortest-job-first (shortest remaining time first)."""
    n = len(procs)
    remaining = [b for _, b in procs]
    finish = [0] * n
    t = 0
    done = 0
    while done < n:
        ready = [i for i in range(n) if procs[i][0] <= t and remaining[i] > 0]
        if not ready:
            t += 1
            continue
        i = min(ready, key=lambda x: (remaining[x], procs[x][0], x))   # run for one time unit
        remaining[i] -= 1
        t += 1
        if remaining[i] == 0:
            finish[i] = t
            done += 1
    waits = [finish[i] - procs[i][0] - procs[i][1] for i in range(n)]
    return sum(waits) / n, waits

# ---- tests
avg, waits = srtf_average_wait([(0, 8), (1, 4), (2, 9), (3, 5)])
assert avg == 6.5 and waits == [9, 0, 15, 2], (avg, waits)
print('ok')
