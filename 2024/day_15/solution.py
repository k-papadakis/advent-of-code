import sys


def read_input(
    file_path: str,
) -> tuple[list[list[str]], tuple[int, int], list[tuple[int, int]]]:
    with open(file_path) as f:
        grid_str, directions_str = f.read().split("\n\n")
    grid = [list(line) for line in grid_str.splitlines()]
    starting_position = next(
        (i, j)
        for i in range(len(grid))
        for j in range(len(grid[0]))
        if grid[i][j] == "@"
    )
    grid[starting_position[0]][starting_position[1]] = "."
    dmap = {">": (0, 1), "^": (-1, 0), "<": (0, -1), "v": (1, 0)}
    directions = [dmap[d] for d in "".join(directions_str.splitlines())]
    return grid, starting_position, directions


def move(
    grid: list[list[str]], position: tuple[int, int], direction: tuple[int, int]
) -> tuple[int, int]:
    x, y = position
    dx, dy = direction
    xx, yy = x + dx, y + dy

    if grid[xx][yy] == ".":
        return xx, yy

    if grid[xx][yy] == "#":
        return x, y

    assert grid[xx][yy] == "O"

    while (xx := xx + dx) in range(len(grid)) and (yy := yy + dy) in range(
        len(grid[0])
    ):
        if grid[xx][yy] == "#":
            return x, y
        if grid[xx][yy] == ".":
            grid[x + dx][y + dy], grid[xx][yy] = grid[xx][yy], grid[x + dx][y + dy]
            return x + dx, y + dy

    raise ValueError("oh well")


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
    grid, position, directions = read_input(file_path)
    for direction in directions:
        position = move(grid, position, direction)
    part_1 = sum(
        100 * i + j
        for i in range(len(grid))
        for j in range(len(grid[0]))
        if grid[i][j] == "O"
    )
    print(part_1)


if __name__ == "__main__":
    main()
