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

    match grid[xx][yy]:
        case "#":
            return False
        case ".":
            return True
        case "O":
            return can_move(grid, (xx, yy), direction)
        case _:
            raise ValueError(f"Invalid symbol {grid[xx][yy]}")


def move(
    grid: list[list[str]], position: tuple[int, int], direction: tuple[int, int]
) -> None:
    x, y = position
    dx, dy = direction
    xx, yy = x + dx, y + dy

    match grid[xx][yy]:
        case "#":
            raise ValueError("Invalid Move")
        case ".":
            grid[x][y], grid[xx][yy] = grid[xx][yy], grid[x][y]
        case "O":
            move(grid, (xx, yy), direction)
            grid[x][y], grid[xx][yy] = grid[xx][yy], grid[x][y]
        case _:
            raise ValueError(f"Invalid symbol {grid[xx][yy]}")


def print_grid(grid: list[list[str]], position: tuple[int, int]) -> None:
    print(
        "\n".join(
            "".join(
                grid[i][j] if (i, j) != position else "@" for j in range(len(grid[0]))
            )
            for i in range(len(grid))
        )
    )


def main():
    file_path = sys.argv[1]
    grid, position, directions = read_input(file_path, expanded=False)
    for direction in directions:
        if can_move(grid, position, direction):
            move(grid, position, direction)
            position = position[0] + direction[0], position[1] + direction[1]
    print_grid(grid, position)
    print()
    part_1 = sum(
        100 * i + j
        for i in range(len(grid))
        for j in range(len(grid[0]))
        if grid[i][j] == "O"
    )
    print(part_1)


if __name__ == "__main__":
    main()
