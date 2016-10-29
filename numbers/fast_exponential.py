import sys

def power_recusive(a, b):
    if b == 0:
        return 1
    if b % 2 == 0:
        return power_recusive(a, b / 2) ** 2
    else:
        return power_recusive(a, b - 1) * a

if __name__ == '__main__':
    x, n = map(int, sys.argv[1:3])

    print power_recusive(x, n)
