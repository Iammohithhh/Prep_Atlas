def flippedBits(num1, num2):
    return bin((num1 ^ num2) & 0xFFFFFFFF).count('1')
assert flippedBits(7, 10) == 3
assert flippedBits(0, 0) == 0
assert flippedBits(-1, 0) == 32
print('ok')
