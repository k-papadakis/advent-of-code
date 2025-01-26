import itertools
import re

type Graph = dict[str, dict[str, int]]
type Rates = dict[str, int]
type Dists = dict[tuple[str, str], int | float]

INFINITY = float("infinity")


def read_input(file_path: str) -> tuple[Graph, Rates]:
    pattern = re.compile(
        r"Valve ([A-Z]{2}) has flow rate=(\d+); tunnels? leads? to valves? ((?:[A-Z]{2}, )*[A-Z]{2})"
    )
    with open(file_path) as f:
        s = f.read()
    graph: Graph = {}
    rates: Rates = {}
    for m in pattern.finditer(s):
        graph[m[1]] = {v: 1 for v in m[3].split(", ")}
        rates[m[1]] = int(m[2])
    return graph, rates


def floyd_warshall(graph: Graph) -> Dists:
    vertices = list(graph)

    dists: Dists = {(u, v): INFINITY for u, v in itertools.product(vertices, repeat=2)}
    for v in vertices:
        dists[v, v] = 0
    for u in graph:
        for v in graph[u]:
            dists[u, v] = graph[u][v]

    for v, u, w in itertools.product(vertices, repeat=3):
        dists[u, w] = min(dists[u, w], dists[u, v] + dists[v, w])

    return dists


def find_max_flow(
    graph: Graph, rates: Rates, source: str, remaining_time: int
) -> int | float:
    dists = floyd_warshall(graph)
    nonzeros = [v for v, r in rates.items() if r > 0]
    opened: set[str] = set()

    def dfs(u: str, remaining_time: int | float) -> int | float:
        max_flow = 0
        for v in nonzeros:
            t = remaining_time - dists[u, v] - 1
            if v not in opened and t >= 0:
                opened.add(v)
                max_flow = max(max_flow, t * rates[v] + dfs(v, t))
                opened.remove(v)
        return max_flow

    return dfs(source, remaining_time)


def find_max_flow_with_elephant(
    graph: Graph, rates: Rates, source: str, remaining_time: int
) -> int | float:
    dists = floyd_warshall(graph)
    nonzeros = [v for v, r in rates.items() if r > 0]
    opened: set[str] = set()
    max_flows: dict[frozenset[str], int | float] = {}  # opened_valves: max_flow

    def dfs(u: str, remaining_time: int | float, flow: int | float) -> None:
        fropened = frozenset(opened)
        max_flows[fropened] = max(max_flows.get(fropened, 0), flow)
        for v in nonzeros:
            t = remaining_time - dists[u, v] - 1
            if v not in opened and t >= 0:
                opened.add(v)
                dfs(v, t, t * rates[v] + flow)
                opened.remove(v)

    dfs(source, remaining_time, 0)
    max_flow = max(
        flow1 + flow2
        for (fropened1, flow1), (fropened2, flow2) in itertools.product(
            max_flows.items(), repeat=2
        )
        if not fropened1 & fropened2
    )
    return max_flow


def main() -> None:
    import sys

    file_path = sys.argv[1]
    graph, rates = read_input(file_path)
    part_1 = find_max_flow(graph, rates, "AA", 30)
    part_2 = find_max_flow_with_elephant(graph, rates, "AA", 26)
    print(f"{part_1 = } {part_2 = }")


if __name__ == "__main__":
    main()
