import sys
from os import PathLike


def read_input(file: str | PathLike[str]) -> list[str]:
    with open(file) as f:
        return f.readlines()


def count_xmas(grid: list[str]) -> int:
    rm = range(len(grid))
    rn = range(len(grid[0]))
    directions = (0, 1), (1, 0), (-1, 0), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)

    res = 0
    x_positions = ((i, j) for i in rm for j in rn if grid[i][j] == "X")
    for i, j in x_positions:
        for dx, dy in directions:
            if all(
                (x := i + k * dx) in rm
                and (y := j + k * dy) in rn
                and grid[x][y] == "XMAS"[k]
                for k in range(1, 4)
            ):
                res += 1
    return res


def count_x_mas(grid: list[str]) -> int:
    rm = range(len(grid))
    rn = range(len(grid[0]))

    res = 0
    a_positions = ((i, j) for i in rm for j in rn if grid[i][j] == "A")
    for i, j in a_positions:
        if (
            (tli := i - 1) in rm
            and (tlj := j - 1) in rn
            and (bri := i + 1) in rm
            and (brj := j + 1) in rn
            and (tri := i - 1) in rm
            and (trj := j + 1) in rn
            and (bli := i + 1) in rm
            and (blj := j - 1) in rn
            and (
                ord(grid[tli][tlj]) ^ ord(grid[bri][brj]) ^ ord("M") ^ ord("S")
                | ord(grid[tri][trj]) ^ ord(grid[bli][blj]) ^ ord("M") ^ ord("S")
                == 0
            )
        ):
            res += 1
    return res


def main():
    file = sys.argv[1]
    grid = read_input(file)
    part_1 = count_xmas(grid)
    part_2 = count_x_mas(grid)
    print(f"{part_1 = } {part_2 = }")


if __name__ == "__main__":
    main()
