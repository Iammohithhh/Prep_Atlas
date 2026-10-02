def last_animal_name_length(animal_sequence, separator='-'):
    parts = animal_sequence.split(separator)
    for name in reversed(parts):               # skip trailing (and empty) pieces
        if name:
            return len(name)
    return 0

# ---- tests
assert last_animal_name_length("dog-cat-elephant") == 8
assert last_animal_name_length("-dog-cat--") == 3
assert last_animal_name_length("---") == 0
assert last_animal_name_length("lion") == 4
print('ok')
