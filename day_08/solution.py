# %%
from itertools import accumulate
from math import inf


def read_data(input_file):
    with open(input_file) as f:
        return [list(map(int, line)) for line in f.read().splitlines()]


def iter_rows(m, n):
    for i in range(m):
        yield [(i, j) for j in range(n)]


def iter_cols(m, n):
    for j in range(n):
        yield [(i, j) for i in range(m)]


def iter_rows_reversed(m, n):
    for i in range(m):
        yield [(i, j) for j in reversed(range(n))]


def iter_cols_reversed(m, n):
    for j in range(n):
        yield [(i, j) for i in reversed(range(m))]


def visibility(gen, a, v):
    for indices in gen:
        max_so_far = accumulate((a[i][j] for i, j in indices), max, initial=-inf)
        for (i, j), M in zip(indices, max_so_far):
            if a[i][j] > M:
                v[i][j] = True


def part1(input_file):
    a = read_data(input_file)
    m, n = len(a), len(a[0])
    v = [[False for _ in range(n)] for _ in range(m)]

    for gen in iter_rows(m, n), iter_cols(m, n), iter_rows_reversed(m, n), iter_cols_reversed(m, n):
        visibility(gen, a, v)

    return sum(map(sum, v))


def part2(input_file):
    a = read_data(input_file)
    m, n = len(a), len(a[0])
    scores = [[1 for _ in range(n)] for _ in range(m)]

    for gen in iter_rows(m, n), iter_cols(m, n), iter_rows_reversed(m, n), iter_cols_reversed(m, n):
        for indices in gen:
            max_so_far = -inf
            steps_since_max = 0

            for t, (i, j) in enumerate(indices):
                steps_since_max += 1
                if a[i][j] > max_so_far:
                    max_so_far = a[i][j]
                    steps_since_max = 0
                    scores[i][j] *= t
                elif a[i][j] == max_so_far:
                    scores[i][j] *= steps_since_max
                    steps_since_max = 0
                else:
                    scores[i][j] *= steps_since_max

    return max(map(max, scores))


print(part2('mini.txt'))