import sys


def main(width, height, cost):
    print width * height * cost
    return width * height * cost


if __name__ == "__main__":
    if len(sys.argv) < 4:
        sys.exit(1)
    try:
        width, height, cost = map(lambda x: int(x), sys.argv[1:])
    except ValueError as err:
        print err.message
        sys.exit(1)
    else:
        main(width, height, cost)
