from collections.abc import Iterable, Sequence
from enum import StrEnum
from itertools import chain, takewhile


class Symbol(StrEnum):
    ASH = "."
    ROCK = "#"


type Grid = list[list[Symbol]]


def read_input(path: str) -> Iterable[Grid]:
    with open(path) as f:
        while grid := list(takewhile(lambda line: line != "", map(str.strip, f))):
            yield [[Symbol(x) for x in line] for line in grid]


def as_int(symbols: Iterable[Symbol]) -> int:
    res = sum(1 << i if symbol == Symbol.ASH else 0 for i, symbol in enumerate(symbols))
    return res


def iter_rows(grid: Grid) -> Iterable[Iterable[Symbol]]:
    for i in range(len(grid)):
        yield (grid[i][j] for j in range(len(grid[0])))


def iter_cols(grid: Grid) -> Iterable[Iterable[Symbol]]:
    for j in range(len(grid[0])):
        yield (grid[i][j] for i in range(len(grid)))


def span(i: int, n: int) -> Iterable[tuple[int, int]]:
    assert i in range(n - 1)

    j = i + 1

    while 0 <= i and j < n:
        yield i, j
        i -= 1
        j += 1


def is_mirrored(xs: Sequence[int], i: int, smudges: int = 0) -> bool:
    diffs = 0
    for i, j in span(i, len(xs)):
        diffs += (xs[i] ^ xs[j]).bit_count()
        if diffs > smudges:
            return False
    return diffs == smudges


def grid_value(grid: Grid, smudges: int = 0) -> int:
    rows = list(map(as_int, iter_rows(grid)))
    cols = list(map(as_int, iter_cols(grid)))

    row_seeker = (
        100 * (i + 1)
        for i in range(len(rows) - 1)
        if is_mirrored(rows, i, smudges=smudges)
    )
    col_seeker = (
        i + 1 for i in range(len(cols) - 1) if is_mirrored(cols, i, smudges=smudges)
    )

    return next(chain(row_seeker, col_seeker), 0)


def main():
    path = "input.txt"

    part_1 = sum(grid_value(grid) for grid in read_input(path))
    part_2 = sum(grid_value(grid, smudges=1) for grid in read_input(path))

    print(f"{part_1 = }, {part_2 = }")


if __name__ == "__main__":
    main()
