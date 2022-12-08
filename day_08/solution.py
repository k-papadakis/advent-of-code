from itertools import accumulate
from math import inf, prod


def read_data(input_file) -> list[list[int]]:
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


def visibility(gen, a, v) -> None:
    for indices in gen:
        max_so_far = accumulate((a[i][j] for i, j in indices), max, initial=-inf)
        for (i, j), M in zip(indices, max_so_far):
            if a[i][j] > M:
                v[i][j] = True


def part1(a: list[list[int]]) -> int:
    m, n = len(a), len(a[0])
    v = [[False for _ in range(n)] for _ in range(m)]

    for gen in iter_rows(m, n), iter_cols(m, n), iter_rows_reversed(m, n), iter_cols_reversed(m, n):
        visibility(gen, a, v)

    return sum(map(sum, v))


def find_visibility(a, i, j, direction):

    m, n = len(a), len(a[0])
    n_steps = 0
    x, y = i, j

    while (x := x + direction[0]) in range(m) and (y := y + direction[1]) in range(n):
        n_steps += 1
        if a[x][y] >= a[i][j]:
            break

    return n_steps


def part2(a):
    m, n = len(a), len(a[0])
    directions = (0, 1), (1, 0), (-1, 0), (0, -1)
    return max(
        prod(find_visibility(a, i, j, direction) for direction in directions) for i in range(m) for j in range(n)
    )


def main():
    a = read_data('input.txt')
    print(f'part: {part1(a)}\npart2: {part2(a)}')


if __name__ == '__main__':
    main()
