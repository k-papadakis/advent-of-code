import sys
from collections import Counter
from collections.abc import Iterable
from os import PathLike


def read_input(file: str | PathLike[str]) -> tuple[list[int], list[int]]:
    left: list[int] = []
    right: list[int] = []
    with open(file) as f:
        for line in f:
            x, y = line.split(maxsplit=1)
            left.append(int(x))
            right.append(int(y))
    return left, right


def total_distance(left: Iterable[int], right: Iterable[int]) -> int:
    return sum(abs(x - y) for x, y in zip(sorted(left), sorted(right), strict=True))


def similarity_score(left: Iterable[int], right: Iterable[int]) -> int:
    right_counter = Counter(right)
    return sum(x * right_counter[x] for x in left)


def main() -> None:
    file = sys.argv[1]
    left, right = read_input(file)
    part_1 = total_distance(left, right)
    part_2 = similarity_score(left, right)
    print(f"{part_1 = } {part_2 = }")


if __name__ == "__main__":
    main()
