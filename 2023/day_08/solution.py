import re
from itertools import cycle


def read_input(path: str) -> tuple[str, dict[str, tuple[str, str]]]:
    pattern = re.compile(r"(?P<name>\w+) = \((?P<left>\w+), (?P<right>\w+)\)")

    with open(path) as f:
        directions = next(f).rstrip("\n")

        next(f)

        nodes = {}
        for line in f:
            m = pattern.match(line)
            if not m:
                raise ValueError("Could not match pattern.")
            nodes[m["name"]] = m["left"], m["right"]

    return directions, nodes


def num_steps_1(directions: str, nodes: dict[str, tuple[str, str]]) -> int:
    assert set(directions) == {"L", "R"}

    current = "AAA"

    for count, d in enumerate(cycle(directions)):
        if current == "ZZZ":
            return count

        current = nodes[current][0] if d == "L" else nodes[current][1]

    return -1  # Never happens


def num_steps_2(directions: str, nodes: dict[str, tuple[str, str]]) -> int:
    # Takes forever
    assert set(directions) == {"L", "R"}

    currents = [node_name for node_name in nodes if node_name.endswith("A")]

    for count, d in enumerate(cycle(directions)):
        print(currents)
        if all(current.endswith("Z") for current in currents):
            return count

        currents = [nodes[cur][0] if d == "L" else nodes[cur][1] for cur in currents]

    return -1  # Never happens


def main():
    directions, nodes = read_input("input.txt")
    num_steps_2(directions, nodes)

    part_1 = num_steps_1(directions, nodes)

    print(f"{part_1 = }")
