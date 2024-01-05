from collections import defaultdict, deque

type Digraph = dict[str, set[str]]


def read_input(path: str) -> tuple[Digraph, set[str], set[str]]:
    with open(path) as f:
        lines = f.read().splitlines()

    digraph: Digraph = {}
    flipflops: set[str] = set()
    conjunctions: set[str] = set()

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

        digraph[name] = set(targets)

    return digraph, flipflops, conjunctions


# def save_digraph_image(
#     digraph: Digraph, flipflops: set[str], conjunctions: set[str]
# ) -> None:
#     import matplotlib.pyplot as plt
#     import networkx as nx

#     g = nx.DiGraph()
#     g.add_edges_from(
#         [(node, target) for node, targets in digraph.items() for target in targets]
#     )

#     colors = []
#     for node in g.nodes():
#         if node in flipflops:
#             colors.append("yellow")
#         elif node in conjunctions:
#             colors.append("red")
#         elif node == "broadcaster":
#             colors.append("blue")
#         else:
#             colors.append("green")

#     plt.figure(figsize=(12, 12))
#     nx.draw_spring(g, with_labels=True, node_color=colors)
#     plt.savefig("graph.png")


def reverse_digraph(digraph: Digraph) -> Digraph:
    res: Digraph = defaultdict(set)

    for node, targets in digraph.items():
        for target in targets:
            res[target].add(node)

    return res


class System:
    def __init__(
        self,
        digraph: Digraph,
        flipflops: set[str],
        conjunctions: set[str],
    ) -> None:
        reversed_digraph = reverse_digraph(digraph)

        self.digraph = digraph
        self.flipflops = {f: False for f in flipflops}
        self.conjunctions = {
            c: dict.fromkeys(reversed_digraph[c], False) for c in conjunctions
        }

        self.low_pulses: int = 0
        self.high_pulses: int = 0

    def push_button(self) -> None:
        q: deque[tuple[str, str, bool]] = deque()
        q.append(("button", "broadcaster", False))

        while q:
            parent, node, pulse = q.popleft()

            # print(f"{parent} -{'high' if pulse else 'low'}-> {node}")

            self.increment_pulses(pulse)

            if node == "broadcaster":
                new_pulse = pulse

                for target in self.digraph[node]:
                    q.append((node, target, new_pulse))

            elif node in self.flipflops:
                if pulse:
                    continue
                self.flipflops[node] = not self.flipflops[node]
                new_pulse = self.flipflops[node]

                for target in self.digraph[node]:
                    q.append((node, target, new_pulse))

            elif node in self.conjunctions:
                self.conjunctions[node][parent] = pulse
                new_pulse = not all(self.conjunctions[node].values())

                for target in self.digraph[node]:
                    q.append((node, target, new_pulse))

            else:
                continue

    def increment_pulses(self, pulse: bool) -> None:
        if pulse:
            self.high_pulses += 1
        else:
            self.low_pulses += 1


def main():
    digraph, flipflops, conjunctions = read_input("input.txt")

    system = System(digraph, flipflops, conjunctions)
    for _ in range(1_000):
        system.push_button()
    part_1 = system.low_pulses * system.high_pulses

    print(f"{part_1 = }")


if __name__ == "__main__":
    main()
