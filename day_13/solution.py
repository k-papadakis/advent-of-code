from itertools import takewhile


def read_data(input_file):
    with open(input_file) as f:
        while pair := tuple(map(eval, takewhile(lambda line: line != '\n', f))):
            yield pair


def compare(a, b):
    if isinstance(a, int) and isinstance(b, int):
        if a < b:
            return 1
        elif a > b:
            return -1
        else:
            return 0

    if isinstance(a, int):
        return compare([a], b)

    if isinstance(b, int):
        return compare(a, [b])

    for x, y in zip(a, b):
        if (t := compare(x, y)) != 0:
            return t

    if len(a) < len(b):
        return 1
    elif len(a) > len(b):
        return -1
    else:
        return 0


def main():
    part1 = sum(i for i, (a, b) in enumerate(read_data('input.txt'), 1) if compare(a, b) != -1)
    print(f'part1: {part1}')


if __name__ == '__main__':
    main()
