import sys


def read_input(file_path: str) -> list[str]:
    with open(file_path) as f:
        return f.read().splitlines()


def find_initial_position_and_direction(
    grid: list[str],
) -> tuple[tuple[int, int], tuple[int, int]]:
    directions = {">": (0, 1), "v": (1, 0), "<": (0, -1), "^": (-1, 0)}
    position = next(
        (i, j)
        for i in range(len(grid))
        for j in range(len(grid[0]))
        if grid[i][j] in directions
    )
    direction = directions[grid[position[0]][position[1]]]
    return position, direction


def visit(
    grid: list[str],
    initial_position: tuple[int, int],
    initial_direction: tuple[int, int],
) -> set[tuple[int, int]]:
    m = len(grid)
    n = len(grid[0])
    i, j = initial_position
    di, dj = initial_direction

    visited: set[tuple[int, int]] = {(i, j)}

    while 0 <= i < m and 0 <= j < n:
        if grid[i][j] == "#":
            i, j = i - di, j - dj
            di, dj = dj, -di
        else:
            visited.add((i, j))
        i, j = i + di, j + dj

    return visited


def has_loop(
    grid: list[str],
    initial_position: tuple[int, int],
    initial_direction: tuple[int, int],
    extra_obstacle: tuple[int, int],
) -> bool:
    m = len(grid)
    n = len(grid[0])
    i, j = initial_position
    di, dj = initial_direction

    visited: set[tuple[int, int, int, int]] = set()

    while 0 <= i < m and 0 <= j < n:
        if (i, j, di, dj) in visited:
            return True

        if grid[i][j] == "#" or (i, j) == extra_obstacle:
            i, j = i - di, j - dj
            di, dj = dj, -di
        else:
            visited.add((i, j, di, dj))
        i, j = i + di, j + dj

    return False


def main():
    file_path = sys.argv[1]
    grid = read_input(file_path)
    position, direction = find_initial_position_and_direction(grid)
    visited = visit(grid, position, direction)
    part_1 = len(visited)
    part_2 = sum(has_loop(grid, position, direction, obstacle) for obstacle in visited)

    print(f"{part_1 = }, {part_2 = }")


if __name__ == "__main__":
    main()
