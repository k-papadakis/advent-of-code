from collections.abc import Generator
import sys


def read_input(file_path: str) -> list[str]:
    with open(file_path) as f:
        return f.read().splitlines()


def parse_path(grid: list[str]) -> list[tuple[int, int]]:
    source = next(
        (x, y)
        for x in range(len(grid))
        for y in range(len(grid[0]))
        if grid[x][y] == "S"
    )
    cur = source
    path: list[tuple[int, int]] = [cur]
    while grid[cur[0]][cur[1]] != "E":
        cur = next(
            (cur[0] + d[0], cur[1] + d[1])
            for d in ((0, 1), (1, 0), (-1, 0), (0, -1))
            if (len(path) < 2 or (cur[0] + d[0], cur[1] + d[1]) != path[-2])
            and grid[cur[0] + d[0]][cur[1] + d[1]] != "#"
        )
        path.append(cur)
    return path


def find_cheats(
    path: list[tuple[int, int]],
) -> Generator[tuple[int, int]]:
    for i in range(len(path)):
        for j in range(i + 3, len(path)):
            if abs(path[j][0] - path[i][0]) + abs(path[j][1] - path[i][1]) == 2:
                yield (i, j)


def main():
    file_path = sys.argv[1]
    grid = read_input(file_path)
    path = parse_path(grid)

    part_1 = sum(j - i - 2 >= 100 for i, j in find_cheats(path))
    print(part_1)


if __name__ == "__main__":
    main()
