from typing import Any, Sequence

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


def find_num_reachable(grid: Grid[Any], source: Pair, steps: int) -> int:
    # assert no obstacles between sources
    assert len(grid) == len(grid[0])
    assert len(grid) % 2 == 1
    assert source == (len(grid) // 2, len(grid) // 2)
    source_steps, local_steps = divmod(steps, len(grid))
    assert local_steps == len(grid) // 2

    if source_steps % 2 == 0:
        # 4*quadrant - 4*diagonal - 3*center
        # = 4sum(2i-1 for i in 1..m) - 4m - 3
        # = 4m^2 - 4m - 3, where m = source_steps//2
        # because the center has been counted 4 times by the quadrants
        # and each diagonal has been counted twice.
        m = source_steps // 2
        reachable_sources = 4 * m**2 - 4 * m - 3
    else:
        # 4*quadrant - 4 diagonal
        # = 4sum(2i for i in 1..m) - 4m
        # = 4m(m+1) - 4m
        # = 4m**2, where m = source_steps//2 + 1
        m = source_steps // 2 + 1
        reachable_sources = 4 * m**2

    local_reachable = len(
        find_reachable(grid, positions={source}, max_steps=local_steps)
    )

    global_reachable = reachable_sources * local_reachable

    return global_reachable


def main() -> None:
    grid, source = read_input("./2023/day_21/input.txt")

    part_1 = len(find_reachable(grid, {source}, 64))

    part_2 = find_num_reachable(grid, source, 26501365)

    print(f"{part_1 = }, {part_2 = }")


if __name__ == "__main__":
    main()
