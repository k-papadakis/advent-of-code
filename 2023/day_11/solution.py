from itertools import pairwise


def read_input(path: str) -> list[str]:
    with open(path) as f:
        s = f.read()
    grid = s.splitlines()
    return grid


def get_coordinates(
    grid: list[str], expansion_coefficient: int
) -> tuple[list[int], list[int]]:
    m, n = len(grid), len(grid[0])
    i_map: list[int] = []
    shift = 0
    for i in range(m):
        if all(grid[i][j] == "." for j in range(n)):
            shift += expansion_coefficient - 1
        i_map.append(i + shift)

    j_map: list[int] = []
    shift = 0
    for j in range(n):
        if all(grid[i][j] == "." for i in range(m)):
            shift += expansion_coefficient - 1
        j_map.append(j + shift)

    i_coords: list[int] = []
    j_coords: list[int] = []
    for i in range(m):
        for j in range(n):
            if grid[i][j] == "#":
                i_coords.append(i_map[i])
                j_coords.append(j_map[j])

    return i_coords, j_coords


def pairwise_l1_sum_1d(coords: list[int]) -> int:
    n = len(coords)
    res = sum(
        (t2 - t1) * k * (n - k)
        for k, (t1, t2) in enumerate(pairwise(sorted(coords)), 1)
    )
    return res


def pairwise_l1_sum_2d(i_coords: list[int], j_coords: list[int]) -> int:
    return pairwise_l1_sum_1d(i_coords) + pairwise_l1_sum_1d(j_coords)


def main() -> None:
    grid = read_input("input.txt")

    part_1 = pairwise_l1_sum_2d(*get_coordinates(grid, expansion_coefficient=2))
    part_2 = pairwise_l1_sum_2d(*get_coordinates(grid, expansion_coefficient=1_000_000))

    print(f"{part_1 = }, {part_2 = }")


if __name__ == "__main__":
    main()
