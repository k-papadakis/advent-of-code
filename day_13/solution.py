from itertools import chain, takewhile
from functools import cmp_to_key
from math import prod


def read_data(input_file):
    with open(input_file) as f:
        while pair := tuple(map(eval, takewhile(lambda line: line != '\n', f))):
            yield pair


def compare(a, b):
    if isinstance(a, int) and isinstance(b, int):
        if a < b:
            return -1
        elif a > b:
            return 1
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
        return -1
    elif len(a) > len(b):
        return 1
    else:
        return 0


def part1(data):
    return sum(i for i, (a, b) in enumerate(data, 1) if compare(a, b) != 1)


def part2(data):
    extras = ([[2]], [[6]])
    data_cat = chain(extras, chain.from_iterable(data))
    data_cat_increasing = sorted(data_cat, key=cmp_to_key(compare))
    return prod(map(lambda i: i + 1, map(data_cat_increasing.index, extras)))


def main():
    input_file = 'input.txt'
    print(f'part1: {part1(read_data(input_file))}\npart2: {part2(read_data(input_file))}')


if __name__ == '__main__':
    main()
