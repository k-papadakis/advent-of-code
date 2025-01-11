import sys

type Pair = tuple[int, int]

DIRECTIONS = {">": (0, 1), "^": (-1, 0), "<": (0, -1), "v": (1, 0)}


def read_input(file_path: str) -> list[str]:
    with open(file_path) as f:
        return f.read().splitlines()


def junction_distances(grid: list[str]) -> dict[tuple[Pair, Pair], int]:
    m, n = len(grid), len(grid[0])
    source: Pair = next((0, j) for j in range(n) if grid[0][j] == ".")
    target: Pair = next((m - 1, j) for j in range(n) if grid[m - 1][j] == ".")
    dist: dict[tuple[Pair, Pair], int] = {}  # dist from junction to junction
    # pos, from_junction, steps
    stack: list[tuple[Pair, Pair, int]] = [(source, source, 0)]
    # pos, from_junction
    seen: set[tuple[Pair, Pair]] = {(source, source)}
    while stack:
        u, junction, steps = stack.pop()

        if u == target:
            dist[junction, u] = steps

        vs: list[tuple[Pair, Pair]] = [
            (d, (v0, v1))
            for d in DIRECTIONS.values()
            if 0 <= (v0 := u[0] + d[0]) < m
            and 0 <= (v1 := u[1] + d[1]) < n
            and grid[v0][v1] != "#"
        ]
        if len(vs) > 2:
            assert (junction, u) not in dist
            dist[junction, u] = steps
            junction = u
            steps = 0
            seen.add((junction, u))

        for d, v in vs:
            if grid[u[0]][u[1]] in DIRECTIONS and d != DIRECTIONS[grid[u[0]][u[1]]]:
                continue
            if (v, junction) in seen:
                continue
            seen.add((v, junction))
            stack.append((v, junction, steps + 1))

    return dist


def main():
    file_path = sys.argv[1]
    grid = read_input(file_path)
    dist = junction_distances(grid)

    import networkx as nx

    g = nx.DiGraph()
    g.add_weighted_edges_from([(u, v, w) for (u, v), w in dist.items()])
    print(nx.dag_longest_path(g))
    print(nx.dag_longest_path_length(g))


if __name__ == "__main__":
    main()
