from collections import defaultdict
from collections.abc import Generator, Hashable
import sys


type Graph[T: Hashable] = dict[T, set[T]]


def read_input(file_path: str) -> Graph[str]:
    graph: defaultdict[str, set[str]] = defaultdict(set)
    with open(file_path) as f:
        for line in f:
            u, v = line.rstrip().split("-")
            graph[u].add(v)
            graph[v].add(u)
    return dict(graph)


def n_triangles[T: Hashable](graph: Graph[T], nodes: set[T]) -> int:
    triangles: set[frozenset[T]] = set()
    for node in nodes:
        for neighbor in graph[node]:
            triangles.update(
                frozenset((node, neighbor, common_neighbor))
                for common_neighbor in graph[node] & (graph[neighbor] - {node})
            )
    return len(triangles)


def complete_components[T: Hashable](graph: Graph[T]) -> Generator[set[T]]:
    seen: set[T] = set()
    for node in graph:
        if node in seen:
            continue
        component = {node}
        stack = [node]
        while stack:
            u = stack.pop()
            for v in graph[u]:
                if v not in component and all(v in graph[w] for w in component):
                    component.add(v)
                    stack.append(v)
        yield component
        seen.update(component)


def main():
    file_path = sys.argv[1]
    graph = read_input(file_path)
    part_1 = n_triangles(graph, {node for node in graph if node.startswith("t")})
    part_2 = ",".join(sorted(max(complete_components(graph), key=len)))
    print(f"part_1 = {part_1} part_2 = {part_2}")


if __name__ == "__main__":
    main()
