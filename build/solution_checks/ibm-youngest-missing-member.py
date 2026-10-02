def find_youngest_member(ages, members):
    known = set(ages)
    best_name, best_age = None, None
    for m in members:
        name, last, age = m.split(',')
        age = int(age)
        if age in known:
            continue
        if best_age is None or age < best_age:            # strict < keeps the first occurrence on ties
            best_name, best_age = name, age
    return best_name                                      # None (null) if every age is present

# ---- tests
members = ["Ram,D,1", "Dev,B,2", "Adam,Jobs,3", "Adam,Jobs,4", "Ema,K,5", "Leena,Jack,7", "Patric,Queen,8", "Liam,Jones,9", "Riya,N,10", "Dilip,K,22"]
assert find_youngest_member([1, 2, 3, 4, 5], members) == "Leena"
assert find_youngest_member([1, 2, 3, 4, 5, 7, 8, 9, 10, 22], members) is None
assert find_youngest_member([], ["A,B,5", "C,D,3", "E,F,3"]) == "C"
print('ok')
