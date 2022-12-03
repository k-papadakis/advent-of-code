from functools import reduce
from itertools import islice

PRIORITIY = {c: i for i, c in enumerate('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ', 1)}


def read_data():
    with open('input.txt') as f:
        for line in f:
            yield line.rstrip('\n')


def batch_data():
    it = read_data()
    while batch := tuple(islice(it, 3)):
        yield batch


def common_item_1(item):
    mid = len(item) // 2
    return next(filter(set(item[:mid]).__contains__, item[mid:]))


def common_item_2(items):
    intersection = reduce(set.intersection, items[1:], set(items[0]))
    return intersection.pop()


def priority_sum(common_item_fn, data):
    return sum(map(PRIORITIY.__getitem__, map(common_item_fn, data)))


def main():
    part1 = priority_sum(common_item_1, read_data())
    part2 = priority_sum(common_item_2, batch_data())
    print(f'part1: {part1}\npart2: {part2}')


if __name__ == '__main__':
    main()
