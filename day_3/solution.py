from itertools import islice

PRIORITY = {c: i for i, c in enumerate('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ', 1)}


def read_data():
    with open('input.txt') as f:
        for line in f:
            yield line.rstrip('\n')


def batch_data():
    it = read_data()
    while batch := tuple(islice(it, 3)):
        yield batch


def common_item(x, y):
    return next(filter(set(x).__contains__, y))


def common_item_1(x):
    mid = len(x) // 2
    return common_item(x[:mid], x[mid:])


def common_item_2(xs):
    intersect_pair = set(xs[0]).intersection(xs[1])
    return common_item(intersect_pair, xs[2])


def priority_sum(common_item_fn, data):
    return sum(map(PRIORITY.__getitem__, map(common_item_fn, data)))


def main():
    part1 = priority_sum(common_item_1, read_data())
    part2 = priority_sum(common_item_2, batch_data())
    print(f'part1: {part1}\npart2: {part2}')


if __name__ == '__main__':
    main()
