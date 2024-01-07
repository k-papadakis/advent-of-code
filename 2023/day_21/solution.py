# Props to https://github.com/villuna/aoc23/wiki/A-Geometric-solution-to-advent-of-code-2023,-day-21

from collections import deque
from typing import Sequence

type Grid[T] = Sequence[Sequence[T]]
type Pair = tuple[int, int]


def read_input(path: str) -> tuple[Grid[str], Pair]:
    with open(path) as f:
        s = f.read()
    grid = [[x for x in line] for line in s.splitlines()]

    source = next(
        (i, j)
        for i in range(len(grid))
        for j in range(len(grid[0]))
        if grid[i][j] == "S"
    )

    return grid, source


def distances(grid: Grid[str], source: Pair) -> dict[Pair, int]:
    m, n = len(grid), len(grid[0])

    dists: dict[Pair, int] = {}
    q: deque[tuple[Pair, int]] = deque([(source, 0)])

    while q:
        (x, y), level = q.popleft()

        if (x, y) in dists:
            continue
        dists[x, y] = level

        for dx, dy in (0, 1), (-1, 0), (0, -1), (1, 0):
            xx, yy = x + dx, y + dy
            if 0 <= xx < m and 0 <= yy < n and grid[xx][yy] != "#":
                q.append(((xx, yy), level + 1))

    return dists


def main() -> None:
    grid, source = read_input("./2023/day_21/input.txt")

    dists = distances(grid, source)
    part_1 = sum(1 for d in dists.values() if d <= 64 and d % 2 == 64 % 2)

    source_steps, steps = divmod(26501365, 131)
    assert source_steps % 2 == 0 and steps == 65

    even_sources = source_steps**2
    odd_sources = (source_steps + 1) ** 2

    reachables_even = sum(1 for d in dists.values() if d % 2 == 0)
    reachables_odd = sum(1 for d in dists.values() if d % 2 == 1)

    even_corners = sum(1 for d in dists.values() if d > 65 and d % 2 == 0)
    odd_corners = sum(1 for d in dists.values() if d > 65 and d % 2 == 1)

    part_2 = (
        even_sources * reachables_even
        + odd_sources * reachables_odd
        - (source_steps + 1) * odd_corners
        + source_steps * even_corners
    )

    print(f"{part_1 = }, {part_2 = }")


if __name__ == "__main__":
    main()
