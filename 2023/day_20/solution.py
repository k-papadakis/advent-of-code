import math
from collections import defaultdict, deque
from copy import deepcopy
from dataclasses import dataclass
from typing import Iterator

type Digraph = dict[str, set[str]]


@dataclass(slots=True)
class Signal:
    source: str
    target: str
    pulse: bool


def read_input(path: str) -> tuple[Digraph, set[str], set[str], str]:
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

    return digraph, flipflops, conjunctions, "broadcaster"


# def save_digraph_image(
#     digraph: Digraph, flipflops: set[str], conjunctions: set[str], broadcaster_gate: str
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
#         elif node == broadcaster_gate:
#             colors.append("blue")
#         else:
#             colors.append("green")

#     plt.figure(figsize=(12, 12))
#     nx.draw_spring(g, with_labels=True, node_color=colors)
#     plt.savefig("graph.png")


def reversed_digraph(digraph: Digraph) -> Digraph:
    res: Digraph = defaultdict(set)

    for node, targets in digraph.items():
        for target in targets:
            res[target].add(node)

    return dict(res)


class Circuit:
    def __init__(
        self,
        digraph: Digraph,
        flipflops: set[str],
        conjunctions: set[str],
        broadcaster_gate: str,
    ) -> None:
        self.digraph = digraph
        self.reversed_digraph = reversed_digraph(digraph)
        self.flipflops = {flipflop: False for flipflop in flipflops}
        self.conjunctions = {
            conjunction: dict.fromkeys(self.reversed_digraph[conjunction], False)
            for conjunction in conjunctions
        }
        self.broadcaster_gate = broadcaster_gate

        self.low_pulses: int = 0
        self.high_pulses: int = 0

    def update_pulse_count(self, pulse: bool) -> None:
        if pulse:
            self.high_pulses += 1
        else:
            self.low_pulses += 1

    def propagate(self, signal: Signal) -> Iterator[Signal]:
        if signal.target == self.broadcaster_gate:
            yield from self.broadcaster_gate_propagate(signal)

        if signal.target in self.flipflops:
            yield from self.flipflop_propagate(signal)

        if signal.target in self.conjunctions:
            yield from self.conjunction_propagate(signal)

    def broadcaster_gate_propagate(self, signal: Signal) -> Iterator[Signal]:
        new_source = signal.target
        new_pulse = signal.pulse

        for new_target in self.digraph[signal.target]:
            yield Signal(new_source, new_target, new_pulse)

    def flipflop_propagate(self, signal: Signal) -> Iterator[Signal]:
        new_source = signal.target

        if not signal.pulse:
            self.flipflops[signal.target] = not self.flipflops[signal.target]
            new_pulse = self.flipflops[signal.target]

            for new_target in self.digraph[signal.target]:
                yield Signal(new_source, new_target, new_pulse)

    def conjunction_propagate(self, signal: Signal) -> Iterator[Signal]:
        new_source = signal.target

        self.conjunctions[signal.target][signal.source] = signal.pulse
        new_pulse = not all(self.conjunctions[signal.target].values())

        for new_target in self.digraph[signal.target]:
            yield Signal(new_source, new_target, new_pulse)

    def push_button(self) -> None:
        signal_queue: deque[Signal] = deque()
        signal_queue.append(Signal("button", self.broadcaster_gate, False))

        while signal_queue:
            signal = signal_queue.popleft()
            self.update_pulse_count(signal.pulse)
            signal_queue.extend(self.propagate(signal))

    def min_pushes_low_rx(self) -> int:
        """
        Assumes a very specific `System` structure:
          - The Circuit contains an output named rx.
          - rx has a single parent, which is a conjunction.
          - The sole common ancestor of the grandparents of rx is the broadcaster.
          - The grandparents of rx send a high (True) pulse at regular intervals of button pushes.
        """
        system = deepcopy(self)

        (rx_parent,) = system.reversed_digraph["rx"]
        rx_grandparents = set(system.reversed_digraph[rx_parent])

        button_push_periods: dict[str, int] = {}
        button_push_count = 0

        while rx_grandparents:
            button_push_count += 1

            signal_queue: deque[Signal] = deque()
            signal_queue.append(Signal("button", self.broadcaster_gate, False))

            while signal_queue:
                signal = signal_queue.popleft()

                if signal.source in rx_grandparents and signal.pulse:
                    rx_grandparents.remove(signal.source)
                    button_push_periods[signal.source] = button_push_count
                    break

                signal_queue.extend(self.propagate(signal))

        return math.lcm(*button_push_periods.values())


def main() -> None:
    digraph, flipflops, conjunctions, broadcaster_gate = read_input("input.txt")
    system = Circuit(digraph, flipflops, conjunctions, broadcaster_gate)

    for _ in range(1_000):
        system.push_button()
    part_1 = system.low_pulses * system.high_pulses

    system = Circuit(digraph, flipflops, conjunctions, broadcaster_gate)
    part_2 = system.min_pushes_low_rx()

    print(f"{part_1 = }, {part_2 = }")


if __name__ == "__main__":
    main()
