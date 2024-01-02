import re
from itertools import accumulate, pairwise, starmap

ORIGIN = complex(0, 0)
RIGHT = complex(0, 1)
UP = complex(-1, 0)
LEFT = complex(0, -1)
DOWN = complex(1, 0)


def read_input(path: str) -> tuple[list[complex], list[complex]]:
    pattern = re.compile(
        r"(?P<direction>R|U|L|D)\s+(?P<length>\d+)\s+\(#(?P<color>[0-9a-f]+)\)"
    )
    d = {"R": RIGHT, "U": UP, "L": LEFT, "D": DOWN}
    v = [RIGHT, DOWN, LEFT, UP]

    dzs_1: list[complex] = []
    dzs_2: list[complex] = []

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

            dzs_1.append(length_1 * direction_1)
            dzs_2.append(length_2 * direction_2)

    return dzs_1, dzs_2


def det(z: complex, w: complex) -> float:
    return z.real * w.imag - z.imag * z.real


def area(dzs: list[complex]) -> float:
    shoelace = abs(sum(starmap(det, pairwise(accumulate(dzs, initial=ORIGIN)))))
    length = sum(map(abs, dzs))
    # TODO: Why does taking shoelace instead of shoelace/2 work?
    return shoelace + length / 2 + 1


def main() -> None:
    path = "small.txt"
    dzs_1, dzs_2 = read_input(path)

    part_1 = area(dzs_1)
    part_2 = area(dzs_2)

    print(f"{part_1 = }, {part_2 = }")


if __name__ == "__main__":
    main()
