from functools import cache
import sys


def read_input(file_path: str) -> tuple[frozenset[str], list[str]]:
    with open(file_path) as f:
        towels_str, patterns_str = f.read().split("\n\n")
    towels = frozenset(towels_str.split(", "))
    designs = patterns_str.splitlines()
    return towels, designs


def is_possible(design: str, towels: frozenset[str]) -> bool:
    if design in towels:
        return True
    return any(
        is_possible(design[len(towel) :], towels)
        for towel in towels
        if design.startswith(towel)
    )


@cache
def num_possible(design: str, towels: frozenset[str]) -> int:
    if not design:
        return 1
    return sum(
        num_possible(design[len(towel) :], towels)
        for towel in towels
        if design.startswith(towel)
    )


def main():
    file_path = sys.argv[1]
    towels, designs = read_input(file_path)
    part_1 = sum(is_possible(design, towels) for design in designs)
    part_2 = sum(num_possible(design, towels) for design in designs)
    print(f"{part_1 = } {part_2 = }")


if __name__ == "__main__":
    main()
