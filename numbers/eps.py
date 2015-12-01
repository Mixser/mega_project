from __future__ import division
from decimal import Decimal as D, getcontext

cache = {0: 1, 1: 1}


def cached_factorial(n):
    if n in cache:
        return cache[n]
    f = n * cached_factorial(n - 1)
    cache[n] = f
    return f


N = 1000  # int(raw_input())

getcontext().prec = N
prev_exp = D(0.0)
exp = D(1.0)
i = 1
while (exp - prev_exp) > D(10) ** D(-(N * 10)):
    prev_exp = exp
    exp += D(1.0) / D(cached_factorial(i))
    i += 1

print exp
