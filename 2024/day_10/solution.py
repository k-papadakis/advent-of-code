import sys
from collections.abc import Generator


def read_input(file_path: str) -> list[list[int]]:
    grid: list[list[int]] = []
    with open(file_path) as f:
        for line in f:
            grid.append(list(map(int, line.rstrip())))
    return grid


def valid_moves(
    p: tuple[int, int], grid: list[list[int]]
) -> Generator[tuple[int, int]]:
    for d in (1, 0), (0, 1), (-1, 0), (0, -1):
        if (
            0 <= (x := p[0] + d[0]) < len(grid)
            and 0 <= (y := p[1] + d[1]) < len(grid[0])
            and grid[x][y] - grid[p[0]][p[1]] == 1
        ):
            yield (x, y)


def score(trailhead: tuple[int, int], grid: list[list[int]]) -> int:
    res = 0
    stack = [trailhead]
    seen: set[tuple[int, int]] = set()
    while stack:
        p = stack.pop()
        if p in seen:
            continue
        seen.add(p)
        if grid[p[0]][p[1]] == 9:
            res += 1
        else:
            stack.extend(valid_moves(p, grid))
    return res


def rating(trailhead: tuple[int, int], grid: list[list[int]]) -> int:
    stack = [trailhead]
    res = 0
    while stack:
        p = stack.pop()
        if grid[p[0]][p[1]] == 9:
            res += 1
        else:
            stack.extend(valid_moves(p, grid))
    return res


def main():
    file_path = sys.argv[1]
    grid = read_input(file_path)
    trailheads = [
        (i, j) for i in range(len(grid)) for j in range(len(grid)) if grid[i][j] == 0
    ]
    part_1 = sum(score(trailhead, grid) for trailhead in trailheads)
    part_2 = sum(rating(trailhead, grid) for trailhead in trailheads)
    print(f"{part_1 = } {part_2 = }")


if __name__ == "__main__":
    main()
