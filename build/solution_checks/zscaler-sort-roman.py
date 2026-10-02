def sort_roman(names):
    values = {'I': 1, 'V': 5, 'X': 10, 'L': 50}

    def roman_to_int(s):
        total = 0
        prev = 0
        for ch in reversed(s):
            v = values[ch]
            if v < prev:
                total -= v
            else:
                total += v
                prev = v
        return total

    def key(name):
        base, numeral = name.rsplit(' ', 1)
        return (base, roman_to_int(numeral))

    return sorted(names, key=key)

# ---- tests
assert sort_roman(["Louis IX", "Louis VIII", "Philip II", "Louis IV", "Philip I"]) == ["Louis IV", "Louis VIII", "Louis IX", "Philip I", "Philip II"]
assert sort_roman(["Mary XL", "Mary XXXIX", "Mary IX"]) == ["Mary IX", "Mary XXXIX", "Mary XL"]
print('ok')
