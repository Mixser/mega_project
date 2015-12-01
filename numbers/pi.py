from __future__ import division
from decimal import Decimal, getcontext
import time

N = 103
STEPS = 20

getcontext().prec = N


def f(y):
    if not isinstance(y, Decimal):
        y = Decimal(y)
    return (Decimal(1) - y ** 4) ** (Decimal(1) / Decimal(4))


y = Decimal(2).sqrt() - Decimal(1)
a = Decimal(6) - Decimal(4) * Decimal(2).sqrt()

start = time.time()

for i in xrange(STEPS):
    y = (Decimal(1) - f(y)) / (1 + f(y))
    a = a * (Decimal(1) + y) ** Decimal(4) - Decimal(2) ** (2 * Decimal(i) + 3) * y * (1 + y + y ** 2)
end = time.time()

print end - start

pi = Decimal(1.0) / a

print pi
