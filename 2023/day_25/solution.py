# Assuming that the graph has a Unique minimum cut of Three edges.

from collections import defaultdict

type Graph = dict[str, set[str]]


def read_input(path: str) -> Graph:
    graph: Graph = defaultdict(set)

    with open(path) as f:
        for line in f:
            node, neighbors_str = line.split(":")
            neighbors = neighbors_str.split()

            for neighbor in neighbors:
                graph[node].add(neighbor)
                graph[neighbor].add(node)

    return graph


def leakage(nodeset: set[str], graph: Graph) -> dict[str, int]:
    res = {
        node: sum((neighbor not in nodeset) for neighbor in graph[node])
        for node in nodeset
    }
    return res


def split(graph: Graph) -> tuple[set[str], set[str]]:
    nodeset = set(graph)

    while True:
        lk = leakage(nodeset, graph)

        total_leakage = sum(lk.values())
        if total_leakage == 3:
            return nodeset, set(graph) - nodeset

        max_leaker = max(lk, key=lk.__getitem__)
        nodeset.remove(max_leaker)


def main() -> None:
    graph = read_input("input.txt")
    nodeset_1, nodeset_2 = split(graph)
    part_1 = len(nodeset_1) * len(nodeset_2)
    print(f"{part_1 = }")


if __name__ == "__main__":
    main()
