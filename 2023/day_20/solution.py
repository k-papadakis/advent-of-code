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
    not_gates: set[str] = set()
    nand_gates: set[str] = set()

    for line in lines:
        type_name, targets_str = line.split(" -> ")
        targets = targets_str.split(", ")

        if type_name == "broadcaster":
            name = "broadcaster"

        elif type_name.startswith("%"):
            name = type_name[1:]
            not_gates.add(name)

        elif type_name.startswith("&"):
            name = type_name[1:]
            nand_gates.add(name)

        else:
            raise ValueError(type_name)

        digraph[name] = set(targets)

    return digraph, not_gates, nand_gates, "broadcaster"


# def save_digraph_image(
#     digraph: Digraph, not_gates: set[str], nand_gates: set[str], broadcaster_gate: str
# ) -> None:
#     import matplotlib.pyplot as plt
#     import networkx as nx

#     g = nx.DiGraph()
#     g.add_edges_from(
#         [(node, target) for node, targets in digraph.items() for target in targets]
#     )

#     colors = []
#     for node in g.nodes():
#         if node in not_gates:
#             colors.append("yellow")
#         elif node in nand_gates:
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
        not_gates: set[str],
        nand_gates: set[str],
        broadcaster_gate: str,
    ) -> None:
        self.digraph = digraph
        self.reversed_digraph = reversed_digraph(digraph)
        self.not_gates = {not_gate: False for not_gate in not_gates}
        self.nand_gates = {
            nand_gate: dict.fromkeys(self.reversed_digraph[nand_gate], False)
            for nand_gate in nand_gates
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
            yield from self.buffer_gate_propagate(signal)

        if signal.target in self.not_gates:
            yield from self.not_gate_propagate(signal)

        if signal.target in self.nand_gates:
            yield from self.nand_gate_propagate(signal)

    def buffer_gate_propagate(self, signal: Signal) -> Iterator[Signal]:
        new_source = signal.target
        new_pulse = signal.pulse

        for new_target in self.digraph[signal.target]:
            yield Signal(new_source, new_target, new_pulse)

    def not_gate_propagate(self, signal: Signal) -> Iterator[Signal]:
        new_source = signal.target

        if not signal.pulse:
            self.not_gates[signal.target] = not self.not_gates[signal.target]
            new_pulse = self.not_gates[signal.target]

            for new_target in self.digraph[signal.target]:
                yield Signal(new_source, new_target, new_pulse)

    def nand_gate_propagate(self, signal: Signal) -> Iterator[Signal]:
        new_source = signal.target

        self.nand_gates[signal.target][signal.source] = signal.pulse
        new_pulse = not all(self.nand_gates[signal.target].values())

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
          - rx has a single parent, which is a NAND gate.
          - The grandparents of rx are connected only via rx's parent and the broadcaster
          - The grandparents of rx receive a low (False) pulse at regular intervals of button pushes.
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

                if signal.target in rx_grandparents and not signal.pulse:
                    rx_grandparents.remove(signal.target)
                    button_push_periods[signal.target] = button_push_count
                    break

                signal_queue.extend(self.propagate(signal))

        return math.lcm(*button_push_periods.values())


def main() -> None:
    digraph, not_gates, nand_gates, broadcaster_gate = read_input("input.txt")
    system = Circuit(digraph, not_gates, nand_gates, broadcaster_gate)

    for _ in range(1_000):
        system.push_button()
    part_1 = system.low_pulses * system.high_pulses

    system = Circuit(digraph, not_gates, nand_gates, broadcaster_gate)
    part_2 = system.min_pushes_low_rx()

    print(f"{part_1 = }, {part_2 = }")


if __name__ == "__main__":
    main()
