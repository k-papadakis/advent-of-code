from collections import defaultdict


type Node = str
type Digraph = dict[Node, set[Node]]


def read_input(path: str) -> tuple[Digraph, Digraph, set[Node], set[Node]]:
    with open(path) as f:
        lines = f.read().splitlines()

    digraph: Digraph = defaultdict(set)
    reverse_digraph: Digraph = defaultdict(set)

    flipflops: set[Node] = set()
    conjunctions: set[Node] = set()

    for line in lines:
        type_name, targets_str = line.split(" -> ")
        targets = targets_str.split(", ")

        if type_name == "broadcaster":
            name = "broadcaster"

        elif type_name.startswith("%"):
            name = type_name[1:]
            flipflops.add(name)

        elif type_name.startswith("&"):
            name = type_name[1:]
            conjunctions.add(name)

        else:
            raise ValueError(type_name)

        for target in targets:
            digraph[name].add(target)
            reverse_digraph[target].add(name)

    digraph["output"]

    return dict(digraph), dict(reverse_digraph), flipflops, conjunctions

digraph, reverse_digraph, flipflops, conjunctions = read_input("small_2.txt")

