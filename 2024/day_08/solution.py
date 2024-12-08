import sys
from collections import defaultdict
from collections.abc import Generator


def read_input(file_path: str) -> list[str]:
    with open(file_path) as f:
        return f.read().splitlines()


type Pair = tuple[int, int]


def iter_harmonics(
    u: Pair, v: Pair, m: int, n: int, min_k: int = 0, max_k: int | None = None
) -> Generator[Pair]:
    uv = (v[0] - u[0], v[1] - u[1])
    k = min_k
    while max_k is None or k <= max_k:
        w = (v[0] + k * uv[0], v[1] + k * uv[1])
        if not (0 <= w[0] < m and 0 <= w[1] < n):
            return
        yield w
        k += 1


def find_unique_antinodes(
    grid: list[str], *, min_k: int = 0, max_k: int | None = None
) -> set[Pair]:
    m, n = len(grid), len(grid[0])

    prev_antennas: defaultdict[str, set[Pair]] = defaultdict(set)
    antinodes: set[Pair] = set()

    antennas_iter = (
        ((i, j), grid[i][j]) for i in range(m) for j in range(n) if grid[i][j] != "."
    )

    for v, antenna in antennas_iter:
        for u in prev_antennas[antenna]:
            antinodes.update(iter_harmonics(u, v, m, n, min_k, max_k))
            antinodes.update(iter_harmonics(v, u, m, n, min_k, max_k))
        prev_antennas[antenna].add(v)

    return antinodes


def main():
    file_path = sys.argv[1]
    grid = read_input(file_path)
    part_1 = len(find_unique_antinodes(grid, min_k=1, max_k=1))
    part_2 = len(find_unique_antinodes(grid, min_k=0, max_k=None))
    print(f"{part_1 = } {part_2 = }")


if __name__ == "__main__":
    main()
