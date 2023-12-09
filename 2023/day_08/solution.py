import re
from collections.abc import Callable
from itertools import cycle
from math import lcm


def read_input(path: str) -> tuple[str, dict[str, tuple[str, str]]]:
    pattern = re.compile(r"(?P<name>\w+) = \((?P<left>\w+), (?P<right>\w+)\)")

    with open(path) as f:
        directions = next(f).rstrip("\n")

        next(f)

        nodes: dict[str, tuple[str, str]] = {}
        for line in f:
            m = pattern.match(line)
            if not m:
                raise ValueError("Could not match pattern.")
            nodes[m["name"]] = m["left"], m["right"]

    return directions, nodes


def num_steps(
    directions: str,
    nodes: dict[str, tuple[str, str]],
    is_source_fn: Callable[[str], bool],
    is_target_fn: Callable[[str], bool],
) -> int:
    """source->target1 == target1->target2 holds for the input"""
    assert set(directions) == {"L", "R"}

    targets = set(filter(is_target_fn, nodes))
    steps: list[int] = []

    for current in filter(is_source_fn, nodes):
        for count, d in enumerate(cycle(directions)):
            if current in targets:
                steps.append(count)
                break
            current = nodes[current][0] if d == "L" else nodes[current][1]

    return lcm(*steps)


def main() -> None:
    directions, nodes = read_input("input.txt")

    part_1 = num_steps(
        directions,
        nodes,
        is_source_fn=lambda s: s == "AAA",
        is_target_fn=lambda s: s == "ZZZ",
    )

    part_2 = num_steps(
        directions,
        nodes,
        is_source_fn=lambda s: s.endswith("A"),
        is_target_fn=lambda s: s.endswith("Z"),
    )

    print(f"{part_1 = }, {part_2 = }")


if __name__ == "__main__":
    main()
