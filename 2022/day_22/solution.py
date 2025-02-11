# TODO: Solve part_2. It's not hard, but it is really cumbersome.

import re

type Point = tuple[int, int]


def read_input(file_path: str) -> tuple[list[str], list[str]]:
    with open(file_path) as f:
        s = f.read()
    grid_str, instructions_str = s.rstrip("\n").split("\n\n")
    grid = grid_str.split("\n")
    instructions = re.split(r"(L|R)", instructions_str)
    return grid, instructions


def wrap(grid: list[str], position: Point, direction: Point) -> Point:
    x, y = position
    dx, dy = direction
    while True:
        xx, yy = x - dx, y - dy
        if (
            xx not in range(len(grid))
            or yy not in range(len(grid[xx]))
            or grid[xx][yy] == " "
        ):
            return x, y
        x, y = xx, yy


def walk(
    grid: list[str],
    instructions: list[str],
    initial_position: Point,
    initial_direction: Point,
) -> tuple[Point, Point]:
    x, y = initial_position
    dx, dy = initial_direction
    for instruction in instructions:
        match instruction:
            case "L":
                dx, dy = (-dy, dx)
            case "R":
                dx, dy = (dy, -dx)
            case steps:
                for _ in range(int(steps)):
                    xx, yy = x + dx, y + dy
                    if (
                        xx not in range(len(grid))
                        or yy not in range(len(grid[xx]))
                        or grid[xx][yy] == " "
                    ):
                        xx, yy = wrap(grid, (x, y), (dx, dy))
                    if grid[xx][yy] == "#":
                        break
                    x, y = xx, yy
    return (x, y), (dx, dy)


def compute_password(position: Point, direction: Point) -> int:
    x = position[0] + 1
    y = position[1] + 1
    i = {(0, 1): 0, (1, 0): 1, (0, -1): 2, (-1, 0): 3}[direction]
    return 1000 * x + 4 * y + i


def main() -> None:
    import sys

    file_path = sys.argv[1]
    grid, instructions = read_input(file_path)
    initial_position = next((0, j) for j in range(len(grid[0])) if grid[0][j] == ".")
    initial_direction = (0, 1)
    final_position, final_direction = walk(
        grid, instructions, initial_position, initial_direction
    )
    part_1 = compute_password(final_position, final_direction)
    print(part_1)


if __name__ == "__main__":
    main()
