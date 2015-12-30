def buble_sort(data, cmp=cmp):
    data = list(data)
    for i in xrange(len(data) - 1):
        for j in xrange(0, len(data) - 1):
            diff = cmp(data[j], data[j + 1])
            if diff == 1:
                data[j], data[j + 1] = data[j + 1], data[j]

    return data


if __name__ == '__main__':
    from random import randint
    for i in xrange(10000):
        data = [randint(0, 2 ** 30) for i in xrange(1000)]
        print sorted(data) == buble_sort(data)
