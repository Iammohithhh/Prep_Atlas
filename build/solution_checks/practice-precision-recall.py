def precision_recall(truth, predicted):
    tp = sum(1 for t, p in zip(truth, predicted) if t == 1 and p == 1)
    fp = sum(1 for t, p in zip(truth, predicted) if t == 0 and p == 1)
    fn = sum(1 for t, p in zip(truth, predicted) if t == 1 and p == 0)
    prec = tp / (tp + fp) if tp + fp else 0.0
    rec = tp / (tp + fn) if tp + fn else 0.0
    return [prec, rec]

assert precision_recall([1, 0, 1, 1], [1, 1, 0, 1]) == [2 / 3, 2 / 3]
assert precision_recall([], []) == [0.0, 0.0]
assert precision_recall([0, 0], [0, 0]) == [0.0, 0.0]
print("ok")
