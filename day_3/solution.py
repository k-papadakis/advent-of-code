PRIORITIY = {c: i for i, c in enumerate('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ', 1)}


def read_data():
    with open('input.txt') as f:
        for line in f:
            yield line.rstrip('\n')


def common_item(s):
    mid = len(s) // 2
    return next(filter(set(s[:mid]).__contains__, s[mid:]))


def priority_sum():
    return sum(map(PRIORITIY.__getitem__, map(common_item, read_data())))


print(priority_sum())
