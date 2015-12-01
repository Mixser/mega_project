from math import sqrt

cached_prime = {1: False, 2: True}


def is_prime(num):
    if num in cached_prime:
        return cached_prime[num]
    for delimiter in xrange(2, int(sqrt(num)) + 1):
        if num % delimiter == 0:
            cached_prime[num] = False
            return False
    cached_prime[num] = False
    return True


def prime_factors(number):
    for i in xrange(1, int(sqrt(number)) + 1):
        if number % i == 0:
            if is_prime(i):
                yield i
            elif is_prime(number / i):
                yield number / i


for i in prime_factors(214124214124):
    print i
