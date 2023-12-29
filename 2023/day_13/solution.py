from collections.abc import Generator, Iterable, Sequence
from enum import StrEnum
from itertools import pairwise, takewhile


class Symbol(StrEnum):
    ASH = "."
    ROCK = "#"


type Grid = list[list[Symbol]]


def read_input(path: str) -> Generator[Grid, None, None]:
    with open(path) as f:
        while grid := list(takewhile(lambda line: line != "", map(str.strip, f))):
            yield [[Symbol(x) for x in line] for line in grid]


def as_int(symbols: Iterable[Symbol]) -> int:
    res = sum(1 << i if symbol == Symbol.ASH else 0 for i, symbol in enumerate(symbols))
    return res


def iter_rows(grid: Grid) -> Iterable[Iterable[Symbol]]:
    for i in range(len(grid)):
        yield [grid[i][j] for j in range(len(grid[0]))]


def iter_cols(grid: Grid) -> Iterable[Iterable[Symbol]]:
    for j in range(len(grid[0])):
        yield [grid[i][j] for i in range(len(grid))]


def is_mirrored(xs: Sequence[int], i: int, j: int) -> bool:
    n = len(xs)
    while i in range(n) and j in range(n):
        if xs[i] != xs[j]:
            return False
        i -= 1
        j += 1
    return True


def num_mirrored(xs: Sequence[int]) -> int:
    return sum(i + 1 for i, j in pairwise(range(len(xs))) if is_mirrored(xs, i, j))


def part_1(grid: Grid) -> int:
    rows = list(map(as_int, iter_rows(grid)))
    cols = list(map(as_int, iter_cols(grid)))
    return 100 * num_mirrored(rows) + num_mirrored(cols)


grids = read_input("input.txt")

print(sum(map(part_1, grids)))
