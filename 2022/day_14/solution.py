from copy import deepcopy
from itertools import pairwise
from typing import Literal

type Grid = dict[tuple[int, int], Literal["#", "o"]]


def read_input(file_path: str) -> list[list[tuple[int, int]]]:
    paths: list[list[tuple[int, int]]] = []
    with open(file_path) as f:
        for line in f:
            path: list[tuple[int, int]] = []
            for t in line.split("->"):
                y, x = map(int, t.split(","))
                path.append((x, y))
            paths.append(path)
    return paths


def make_grid(paths: list[list[tuple[int, int]]]) -> Grid:
    grid: Grid = {}
    for path in paths:
        for s, t in pairwise(path):
            if s[0] == t[0]:
                for j in range(min(s[1], t[1]), max(s[1], t[1]) + 1):
                    grid[s[0], j] = "#"
            else:
                for i in range(min(s[0], t[0]), max(s[0], t[0]) + 1):
                    grid[i, s[1]] = "#"
    return grid


def grid_str(grid: Grid) -> str:
    m = 1 + max(x for x, _ in grid)
    n = 1 + max(y for _, y in grid)
    return "\n".join("".join(grid.get((i, j), ".") for j in range(n)) for i in range(m))


def num_fallen_till_abyss(grid: Grid, source: tuple[int, int] = (0, 500)) -> int:
    grid = deepcopy(grid)
    m = 1 + max(x for x, _ in grid)
    n = 1 + max(y for _, y in grid)
    i, j = source
    num_sands = 0
    while 0 <= i < m and 0 <= j < n:
        if i + 1 >= m or (i + 1, j) not in grid:
            i, j = i + 1, j
        elif i + 1 >= m or j - 1 < 0 or (i + 1, j - 1) not in grid:
            i, j = i + 1, j - 1
        elif i + 1 >= m or j + 1 >= n or (i + 1, j + 1) not in grid:
            i, j = i + 1, j + 1
        else:
            grid[i, j] = "o"
            i, j = source
            num_sands += 1
    return num_sands


def num_fallen_till_block(grid: Grid, source: tuple[int, int] = (0, 500)) -> int:
    grid = deepcopy(grid)
    m = 1 + max(x for x, _ in grid)
    i, j = source
    num_sands = 0
    while True:
        if i + 1 != m + 1 and (i + 1, j) not in grid:
            i, j = i + 1, j
        elif i + 1 != m + 1 and (i + 1, j - 1) not in grid:
            i, j = i + 1, j - 1
        elif i + 1 != m + 1 and (i + 1, j + 1) not in grid:
            i, j = i + 1, j + 1
        else:
            grid[i, j] = "o"
            num_sands += 1
            if (i, j) == source:
                break
            i, j = source
    return num_sands


def main():
    import sys

    file_path = sys.argv[1]
    paths = read_input(file_path)
    grid = make_grid(paths)
    with open("grid.txt", "w") as f:
        _ = f.write(grid_str(grid))
    part_1 = num_fallen_till_abyss(grid)
    print(part_1)
    part_2 = num_fallen_till_block(grid)
    print(part_2)


if __name__ == "__main__":
    main()
