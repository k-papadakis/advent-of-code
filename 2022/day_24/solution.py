from collections import deque
from math import lcm

type Point = tuple[int, int]


def read_input(file_path: str) -> list[str]:
    with open(file_path) as f:
        return f.read().splitlines()


def advance_grid(grid: list[list[str]]) -> list[list[str]]:
    m, n = len(grid), len(grid[0])
    new_grid: list[list[str]] = [["" for _ in range(n)] for _ in range(m)]
    for i in range(1, m - 1):
        for j in range(1, n - 1):
            for d in grid[i][j]:
                match d:
                    case "^":
                        new_i = i - 1 if i > 1 else m - 2
                        new_grid[new_i][j] += "^"
                    case "v":
                        new_i = i + 1 if i < m - 2 else 1
                        new_grid[new_i][j] += "v"
                    case "<":
                        new_j = j - 1 if j > 1 else n - 2
                        new_grid[i][new_j] += "<"
                    case ">":
                        new_j = j + 1 if j < n - 2 else 1
                        new_grid[i][new_j] += ">"
                    case _:
                        raise ValueError(f"Invalid direction: {d}")
    return new_grid


def find_blizzards_till_repeat(grid: list[str]) -> list[list[list[bool]]]:
    m, n = len(grid), len(grid[0])
    has_blizzard: list[list[list[bool]]] = []
    g = [["" if grid[i][j] == "." else grid[i][j] for j in range(n)] for i in range(m)]
    has_blizzard.append([[len(g[i][j]) > 0 for j in range(n)] for i in range(m)])
    for _ in range(lcm(m - 2, n - 2) - 1):
        g = advance_grid(g)
        has_blizzard.append([[len(g[i][j]) > 0 for j in range(n)] for i in range(m)])
    return has_blizzard


def quickest_path(
    grid: list[str],
    has_blizzard: list[list[list[bool]]],
    source: Point,
    target: Point,
    starting_time: int,
) -> int:
    m, n = len(grid), len(grid[0])
    mod = len(has_blizzard)
    visited: set[tuple[Point, int]] = set()
    q = deque([(starting_time, source)])
    while q:
        time, (i, j) = q.popleft()
        if (i, j) == target:
            return time
        if ((i, j), time % mod) in visited:
            continue
        visited.add(((i, j), time % mod))
        if (
            not (0 <= i < m)
            or not (0 <= j < n)
            or has_blizzard[time % mod][i][j]
            or grid[i][j] == "#"
        ):
            continue
        for new_i, new_j in [(i, j), (i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]:
            q.append((time + 1, (new_i, new_j)))
    return -1


def main() -> None:
    import sys

    file_path = sys.argv[1]
    grid = read_input(file_path)
    has_blizzards = find_blizzards_till_repeat(grid)
    m, n = len(grid), len(grid[0])
    source = next((0, j) for j in range(n) if grid[0][j] == ".")
    target = next((m - 1, j) for j in range(n) if grid[m - 1][j] == ".")
    part_1 = quickest_path(grid, has_blizzards, source, target, 0)
    t = quickest_path(grid, has_blizzards, target, source, part_1)
    part_2 = quickest_path(grid, has_blizzards, source, target, t)
    print(f"{part_1 = } {part_2 = }")


if __name__ == "__main__":
    main()
