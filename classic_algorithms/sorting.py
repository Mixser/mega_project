from random import randint

from collections import deque

SIZE = 1000

def buble_sort(data, cmp=cmp):
    data = list(data)
    for i in xrange(len(data) - 1):
        for j in xrange(0, len(data) - 1):
            diff = cmp(data[j], data[j + 1])
            if diff == 1:
                data[j], data[j + 1] = data[j + 1], data[j]

    return data


def merge_list(first, second):
    result = []

    while first and second:
        if first[0] < second[0]:
            result.append(first.popleft())
        else:
            result.append(second.popleft())

    if first:
        result.extend(first)
    elif second:
        result.extend(second)

    return result


def merge_sort(data):
    n = len(data)
    if n < 2:
        return data
    mid = n / 2

    L = data[:mid]
    R = data[mid:]

    L = merge_sort(L)
    R = merge_sort(R)

    # I use deque, because the pop(0) method at list slower than the popleft() of deque
    L, R = deque(L), deque(R)

    data = merge_list(L, R)

    del L, R

    return data


def merge_test():
    data = [randint(0, 2 ** 30) for i in xrange(SIZE)]
    merge_sort(data)


def standart_test():
    data = [randint(0, 2 ** 30) for i in xrange(SIZE)]
    sorted(data)


def bubble_test():
    data = [randint(0, 2 ** 30) for i in xrange(SIZE)]
    buble_sort(data)

if __name__ == '__main__':
    merge_test()