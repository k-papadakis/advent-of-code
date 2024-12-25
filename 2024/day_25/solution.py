import sys

type Grid = list[str]


def read_input(file_path: str) -> list[Grid]:
    with open(file_path) as f:
        return [grid_str.splitlines() for grid_str in f.read().split("\n\n")]


def locks_and_keys(grids: list[Grid]) -> tuple[list[list[int]], list[list[int]]]:
    locks: list[list[int]] = []
    keys: list[list[int]] = []
    for grid in grids:
        if all(x == "#" for x in grid[0]):
            keys.append(
                [
                    sum(grid[i][j] == "#" for i in range(len(grid))) - 1
                    for j in range(len(grid[0]))
                ]
            )
        else:
            locks.append(
                [
                    sum(grid[i][j] == "#" for i in reversed(range(len(grid)))) - 1
                    for j in range(len(grid[0]))
                ]
            )
    return locks, keys


def fits(key: list[int], lock: list[int]) -> bool:
    return all(a + b <= 5 for a, b in zip(key, lock))


def main():
    file_path = sys.argv[1]
    grids = read_input(file_path)
    locks, keys = locks_and_keys(grids)
    part_1 = sum(fits(lock, key) for lock in locks for key in keys)
    print(part_1)


if __name__ == "__main__":
    main()
