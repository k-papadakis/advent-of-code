from typing import Iterable, Sequence

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


def find_reachable(
    grid: Grid[str], positions: set[Pair], max_steps: int, _steps: int = 0
) -> set[Pair]:
    if _steps == max_steps or not positions:
        return positions

    next_positions = {
        (x + dx, y + dy)
        for x, y in positions
        for dx, dy in ((0, 1), (-1, 0), (0, -1), (1, 0))
        if 0 <= x + dx < len(grid)
        and 0 <= y + dy < len(grid[0])
        and grid[x + dx][y + dy] != "#"
    }

    return find_reachable(grid, next_positions, max_steps, _steps + 1)


def reachable_str(grid: Grid[str], reachable: Iterable[Pair]) -> str:
    s = "\n".join(
        "".join("O" if (i, j) in reachable else grid[i][j] for j in range(len(grid[0])))
        for i in range(len(grid))
    )
    return s


def tile_grid[
    T
](grid: Grid[T], source: Pair, nrows: int, ncols: int) -> tuple[Grid[T], Pair]:
    lst = list(map(list, grid))
    tiled = [row * ncols for row in lst] * nrows
    tiled = list(map(list, tiled))
    central_source = (
        source[0] + len(grid) * (ncols - 1) // 2,
        source[1] + len(grid[0]) * (nrows - 1) // 2,
    )
    return tiled, central_source


def main() -> None:
    grid, source = read_input("./day_21/input.txt")

    part_1 = len(find_reachable(grid, {source}, 64))

    print(f"{part_1 = }")


# if __name__ == "__main__":
#     main()

grid, source = read_input("./day_21/input.txt")
# Replicate the grid once in each direction
tiled_grid, central_source = tile_grid(grid, source, 3, 3)

# Move exactly 65 steps to reach the end of the grid
# Move exactly 131 steps to reach a source again
for steps in 65, 131:
    with open(f"./day_21/reachable_{steps}.txt", "w") as f:
        f.write(
            reachable_str(
                tiled_grid, find_reachable(tiled_grid, {central_source}, steps)
            )
        )

source_jumps, steps = divmod(26501365, 135)
print(source_jumps, steps)
