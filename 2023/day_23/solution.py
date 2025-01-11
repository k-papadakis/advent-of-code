from collections import defaultdict
from collections.abc import Hashable

type Pair = tuple[int, int]
type Graph[T: Hashable, W] = dict[T, dict[T, W]]

DIRECTIONS = {">": (0, 1), "^": (-1, 0), "<": (0, -1), "v": (1, 0)}


def read_input(file_path: str) -> list[str]:
    with open(file_path) as f:
        return f.read().splitlines()


def junction_graph(
    grid: list[str], source: Pair, target: Pair, slippery: bool
) -> Graph[Pair, int]:
    m, n = len(grid), len(grid[0])
    # dist from junction to junction
    dist: Graph[Pair, int] = defaultdict(dict)
    # pos, from_junction, steps
    stack: list[tuple[Pair, Pair, int]] = [(source, source, 0)]
    # pos, from_junction
    seen: set[tuple[Pair, Pair]] = {(source, source)}
    while stack:
        u, junction, steps = stack.pop()

        vs: list[tuple[Pair, Pair]] = [
            (d, (v0, v1))
            for d in DIRECTIONS.values()
            if 0 <= (v0 := u[0] + d[0]) < m
            and 0 <= (v1 := u[1] + d[1]) < n
            and grid[v0][v1] != "#"
        ]
        if len(vs) > 2 or u == target:
            assert u not in dist[junction]
            dist[junction][u] = steps

        if len(vs) > 2:
            junction = u
            steps = 0
            seen.add((junction, u))

        for d, v in vs:
            if (
                slippery
                and grid[u[0]][u[1]] in DIRECTIONS
                and d != DIRECTIONS[grid[u[0]][u[1]]]
            ):
                continue
            if (v, junction) in seen:
                continue
            seen.add((v, junction))
            stack.append((v, junction, steps + 1))

    return dist


def max_dist[T](graph: Graph[T, int], source: T, target: T) -> int:
    seen: set[T] = set()

    def dfs(u: T, d: int) -> int:
        if u == target:
            return d
        seen.add(u)
        max_length = max(
            (dfs(v, d + graph[u][v]) for v in graph[u] if v not in seen),
            default=0,
        )
        seen.remove(u)
        return max_length

    return dfs(source, 0)


def main():
    import sys

    file_path = sys.argv[1]
    grid = read_input(file_path)
    m, n = len(grid), len(grid[0])
    source: Pair = next((0, j) for j in range(n) if grid[0][j] == ".")
    target: Pair = next((m - 1, j) for j in range(n) if grid[m - 1][j] == ".")

    slippery_dist = junction_graph(grid, source, target, slippery=True)
    part_1 = max_dist(slippery_dist, source, target)

    non_slippery_dist = junction_graph(grid, source, target, slippery=False)
    part_2 = max_dist(non_slippery_dist, source, target)

    print(f"{part_1 = } {part_2 = }")


if __name__ == "__main__":
    main()
