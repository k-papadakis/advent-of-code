import sys
from heapq import heappush, heappop

type Grid = list[str]
type Point = tuple[int, int]
type Node = tuple[Point, Point]


def read_input(
    file_path: str,
) -> tuple[Grid, Point, Point, Point]:
    with open(file_path) as f:
        grid = f.read().splitlines()
    source = next(
        (i, j)
        for i in range(len(grid))
        for j in range(len(grid[0]))
        if grid[i][j] == "S"
    )
    target = next(
        (i, j)
        for i in range(len(grid))
        for j in range(len(grid[0]))
        if grid[i][j] == "E"
    )
    direction = (0, 1)
    return grid, source, target, direction


def lowest_score(
    grid: Grid, source: Point, target: Point, direction: Point
) -> int | None:
    # A*
    def heurestic(source: Point, target: Point) -> int:
        x_dist = abs(target[0] - source[0])
        y_dist = abs(target[1] - source[1])
        must_turn = (x_dist == 0) ^ (y_dist == 0)
        return x_dist + y_dist + 1_000 * must_turn

    dist: dict[Point, int] = {source: 0}
    boundary: list[tuple[int, Node]] = [(0, (source, direction))]
    while boundary:
        f, (p, d) = heappop(boundary)
        if p == target:
            return f

        for dd in d, (-d[1], d[0]), (d[1], -d[0]):
            pp = (p[0] + dd[0], p[1] + dd[1])
            if grid[pp[0]][pp[1]] == "#":
                continue
            alt_dist = dist[p] + 1 + (1_000) * (d != dd)
            if pp not in dist or alt_dist < dist[pp]:
                dist[pp] = alt_dist
                ff = alt_dist + heurestic(pp, target)
                heappush(boundary, (ff, (pp, dd)))

    return None


def find_num_spots(grid: Grid, source: Point, target: Point, direction: Point) -> int:
    # Dijkstra
    prevs: dict[Node, set[Node]] = {}
    boundary: list[tuple[int, Node]] = [(0, (source, direction))]
    dist: dict[Node, int] = {(source, direction): 0}
    while boundary:
        _, (p, d) = heappop(boundary)

        for dd in d, (-d[1], d[0]), (d[1], -d[0]):
            pp = (p[0] + dd[0], p[1] + dd[1])
            if grid[pp[0]][pp[1]] == "#":
                continue
            alt_dist = dist[p, d] + 1 + (1_000) * (d != dd)
            if (pp, dd) not in dist or alt_dist < dist[pp, dd]:
                dist[pp, dd] = alt_dist
                prevs[pp, dd] = {(p, d)}
                heappush(boundary, (alt_dist, (pp, dd)))
            elif (pp, dd) in dist and alt_dist == dist[pp, dd]:
                prevs[pp, dd].add((p, d))

    def walk_back(node: Node) -> None:
        spots.add(node[0])
        if node not in prevs:
            return
        for prev in prevs[node]:
            walk_back(prev)

    spots: set[Point] = set()
    dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    min_dist = min(dist[target, d] for d in dirs if (target, d) in dist)
    for d in dirs:
        if (target, d) in dist and dist[target, d] == min_dist:
            walk_back((target, d))
    return len(spots)


def main():
    file_path = sys.argv[1]
    grid, source, target, direction = read_input(file_path)
    part_1 = lowest_score(grid, source, target, direction)
    part_2 = find_num_spots(grid, source, target, direction)
    print(f"{part_1 = } {part_2 = }")


if __name__ == "__main__":
    main()
