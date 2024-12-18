import sys


def read_input(
    file_path: str, expanded: bool
) -> tuple[list[list[str]], tuple[int, int], list[tuple[int, int]]]:
    with open(file_path) as f:
        grid_str, directions_str = f.read().split("\n\n")
    if expanded:
        trans = str.maketrans({"#": "##", ".": "..", "@": "@.", "O": "[]"})
        grid_str = grid_str.translate(trans)
    grid = [list(line) for line in grid_str.splitlines()]
    starting_position = next(
        (i, j)
        for i in range(len(grid))
        for j in range(len(grid[0]))
        if grid[i][j] == "@"
    )
    grid[starting_position[0]][starting_position[1]] = "."
    dmap = {">": (0, 1), "^": (-1, 0), "<": (0, -1), "v": (1, 0)}
    directions = [dmap[d] for d in directions_str.replace("\n", "")]
    return grid, starting_position, directions


def can_move(
    grid: list[list[str]], position: tuple[int, int], direction: tuple[int, int]
) -> bool:
    x, y = position
    dx, dy = direction
    xx, yy = x + dx, y + dy

    match dx, grid[xx][yy]:
        case _, "#":
            return False
        case _, ".":
            return True
        case _, "O":
            return can_move(grid, (xx, yy), direction)
        case 0, "[" | "]":
            return can_move(grid, (xx, yy), direction)
        case _, "[":
            return can_move(grid, (xx, yy), direction) and can_move(
                grid, (xx, yy + 1), direction
            )
        case _, "]":
            return can_move(grid, (xx, yy), direction) and can_move(
                grid, (xx, yy - 1), direction
            )
        case _:
            raise ValueError(f"Invalid symbol {grid[xx][yy]}")


def unsafe_single_step_move(
    grid: list[list[str]], position: tuple[int, int], direction: tuple[int, int]
) -> None:
    x, y = position
    dx, dy = direction
    xx, yy = x + dx, y + dy

    match dx, grid[xx][yy]:
        case _, "#":
            raise ValueError("Invalid Move")
        case _, ".":
            pass
        case _, "O":
            unsafe_single_step_move(grid, (xx, yy), direction)
        case 0, "[" | "]":
            unsafe_single_step_move(grid, (xx, yy), direction)
        case _, "[":
            unsafe_single_step_move(grid, (xx, yy + 1), direction)
            unsafe_single_step_move(grid, (xx, yy), direction)
        case _, "]":
            unsafe_single_step_move(grid, (xx, yy), direction)
            unsafe_single_step_move(grid, (xx, yy - 1), direction)
        case _:
            raise ValueError(f"Invalid symbol {grid[xx][yy]}")

    grid[x][y], grid[xx][yy] = grid[xx][yy], grid[x][y]


def safe_multi_step_move(
    grid: list[list[str]], position: tuple[int, int], directions: list[tuple[int, int]]
) -> None:
    p = position
    for direction in directions:
        if can_move(grid, p, direction):
            unsafe_single_step_move(grid, p, direction)
            p = (p[0] + direction[0], p[1] + direction[1])


def gps_sum(grid: list[list[str]]) -> int:
    return sum(
        100 * i + j
        for i in range(len(grid))
        for j in range(len(grid[0]))
        if grid[i][j] in {"O", "["}
    )


def main():
    file_path = sys.argv[1]

    grid, position, directions = read_input(file_path, expanded=False)
    safe_multi_step_move(grid, position, directions)
    part_1 = gps_sum(grid)

    grid, position, directions = read_input(file_path, expanded=True)
    safe_multi_step_move(grid, position, directions)
    part_2 = gps_sum(grid)

    print(f"{part_1 = } {part_2 = }")


if __name__ == "__main__":
    main()
