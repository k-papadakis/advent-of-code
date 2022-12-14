from itertools import chain, takewhile
from functools import cmp_to_key
from math import prod
from bisect import bisect_right


def read_data(input_file):
    with open(input_file) as f:
        while pair := tuple(map(eval, takewhile(lambda line: line != '\n', f))):
            yield pair


def compare(a, b):
    if isinstance(a, int) and isinstance(b, int):
        return a - b

    if isinstance(a, int):
        return compare([a], b)

    if isinstance(b, int):
        return compare(a, [b])

    for t in map(compare, a, b):
        if t != 0:
            return t

    return compare(len(a), len(b))


def part1(data):
    return sum(i for i, (a, b) in enumerate(data, 1) if compare(a, b) <= 0)


def part2(data):
    extras = ([[2]], [[6]])
    data_cat = chain(extras, chain.from_iterable(data))
    key_fn = cmp_to_key(compare)
    data_cat_increasing = sorted(data_cat, key=key_fn)
    return prod(bisect_right(data_cat_increasing, key_fn(extra), key=key_fn) for extra in extras)


def main():
    input_file = 'input.txt'
    print(f'part1: {part1(read_data(input_file))}\npart2: {part2(read_data(input_file))}')


if __name__ == '__main__':
    main()
