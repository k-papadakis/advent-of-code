from itertools import combinations


def read_input(path: str) -> list[str]:
    with open(path) as f:
        s = f.read()
    grid = s.splitlines()
    return grid


def get_coordinates(
    grid: list[str], expansion_coefficient: int
) -> list[tuple[int, int]]:
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

    coordinates: list[tuple[int, int]] = []
    for i in range(m):
        for j in range(n):
            if grid[i][j] == "#":
                coordinates.append((i_map[i], j_map[j]))

    return coordinates


def get_pairwise_distances_sum(coords: list[tuple[int, int]]) -> int:
    res = sum(
        abs(i2 - i1) + abs(j2 - j1) for (i1, j1), (i2, j2) in combinations(coords, 2)
    )
    return res


def main() -> None:
    grid = read_input("input.txt")

    part_1 = get_pairwise_distances_sum(get_coordinates(grid, expansion_coefficient=2))
    part_2 = get_pairwise_distances_sum(
        get_coordinates(grid, expansion_coefficient=1_000_000)
    )

    print(f"{part_1 = }, {part_2 = }")


if __name__ == "__main__":
    main()
