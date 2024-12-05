import sys
from functools import cmp_to_key

type Rule = tuple[int, int]
type Manual = list[int]
type Graph = dict[int, set[int]]


def read_input(file_path: str) -> tuple[list[Rule], list[Manual]]:
    with open(file_path) as f:
        rules_str, manuals_str = f.read().split("\n\n", maxsplit=1)

    rules: list[Rule] = []
    for rule_str in rules_str.splitlines():
        x, y = rule_str.split("|", maxsplit=1)
        rules.append((int(x), int(y)))

    manuals: list[Manual] = []
    for manual_str in manuals_str.splitlines():
        manual = list(map(int, manual_str.split(",")))
        manuals.append(manual)

    return rules, manuals


def graph_from_rules(rules: list[Rule]) -> Graph:
    graph: Graph = {}
    for x, y in rules:
        if x not in graph:
            graph[x] = set()
        if y not in graph:
            graph[y] = set()
        graph[x].add(y)
    return graph


def cmp_key_from_graph(graph: Graph):
    def cmp(x: int, y: int):
        if y in graph[x]:
            return -1
        if x in graph[y]:
            return 1
        raise ValueError(f"Cannot compare {x} and {y}.")

    return cmp_to_key(cmp)


def main():
    file_path = sys.argv[1]
    rules, manuals = read_input(file_path)

    graph = graph_from_rules(rules)
    cmp_key = cmp_key_from_graph(graph)

    part_1 = 0
    part_2 = 0
    for manual in manuals:
        sorted_manual = sorted(manual, key=cmp_key)
        mid = sorted_manual[len(sorted_manual) // 2]
        if sorted_manual == manual:
            part_1 += mid
        else:
            part_2 += mid

    print(f"{part_1 = } {part_2 = }")


if __name__ == "__main__":
    main()
