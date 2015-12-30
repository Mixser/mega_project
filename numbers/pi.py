from __future__ import division
from decimal import Decimal as D
from decimal import getcontext
import time

N = 103
STEPS = 20

getcontext().prec = N


def f(y):
    if not isinstance(y, D):
        y = D(y)
    return (D(1) - y ** 4) ** (D(1) / D(4))


y = D(2).sqrt() - D(1)
a = D(6) - D(4) * D(2).sqrt()

start = time.time()

for i in xrange(STEPS):
    y = (D(1) - f(y)) / (1 + f(y))
    a = a * (D(1) + y) ** D(4) - D(2) ** (2 * D(i) + 3) * y * (1 + y + y ** 2)
end = time.time()

print end - start

pi = D(1.0) / a

print pi
