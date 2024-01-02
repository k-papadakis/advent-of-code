import re
from dataclasses import dataclass
from itertools import accumulate, pairwise, starmap
from typing import Self


@dataclass(slots=True, frozen=True)
class Pair:
    x: int
    y: int

    def __add__(self, other: Self) -> Self:
        return type(self)(self.x + other.x, self.y + other.y)

    def __rmul__(self, k: int) -> Self:
        return type(self)(k * self.x, k * self.y)

    def __abs__(self) -> int:
        return abs(self.x) + abs(self.y)


ORIGIN = Pair(0, 0)
RIGHT = Pair(0, 1)
UP = Pair(-1, 0)
LEFT = Pair(0, -1)
DOWN = Pair(1, 0)


def read_input(path: str) -> tuple[list[Pair], list[Pair]]:
    pattern = re.compile(
        r"(?P<direction>R|U|L|D)\s+(?P<length>\d+)\s+\(#(?P<color>[0-9a-f]+)\)"
    )
    d = {"R": RIGHT, "U": UP, "L": LEFT, "D": DOWN}
    v = [RIGHT, DOWN, LEFT, UP]

    steps_1: list[Pair] = []
    steps_2: list[Pair] = []

    with open(path) as f:
        for line in f:
            m = pattern.match(line)
            if not m:
                raise ValueError(f"Could not match pattern on {line}")

            direction_1 = d[m["direction"]]
            length_1 = int(m["length"])

            color = int(m["color"], 16)
            length_2, index = divmod(color, 16)
            direction_2 = v[index]

            steps_1.append(length_1 * direction_1)
            steps_2.append(length_2 * direction_2)

    return steps_1, steps_2


def det(p: Pair, q: Pair) -> int:
    return p.x * q.y - p.y * q.x


def area(steps: list[Pair]) -> int:
    shoelace = abs(sum(starmap(det, pairwise(accumulate(steps, initial=ORIGIN)))))
    num_boundary = sum(map(abs, steps))
    num_interior = shoelace // 2 - num_boundary // 2 + 1
    return num_interior + num_boundary


def main() -> None:
    path = "input.txt"
    steps_1, steps_2 = read_input(path)

    part_1 = area(steps_1)
    part_2 = area(steps_2)

    print(f"{part_1 = }, {part_2 = }")


if __name__ == "__main__":
    main()
