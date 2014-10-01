from fractions import Fraction

print(1/2 + 1/4 + 1/8 + 1/16 + 1/32 + 1/64 + 1/128)
print(
    Fraction(1, 2) +
    Fraction(1, 4) +
    Fraction(1, 8) +
    Fraction(1, 16) +
    Fraction(1, 32) +
    Fraction(1, 64) +
    Fraction(1, 128))

from operator import add, sub, mul

print(100 - 7 * (8 + 4))
print(sub(100, mul(7, add(8, 4))))
# NOTE: add does NOT allow variadic arguments
#print(add(2, 3, 4))
