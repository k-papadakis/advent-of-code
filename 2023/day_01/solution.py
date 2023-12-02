import re
from typing import Callable

WORDS = (
    "zero",
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine",
)

SUBPATTERN_1 = r"\d"

WORDS_JOINED = "|".join(WORDS)
SUBPATTERN_2 = rf"\d|{WORDS_JOINED}"

PATTERN_TEMPLATE = r"(?:.*?({subpattern}).*({subpattern}).*?$)|(?:.*?({subpattern}))"

PATTERN_1 = re.compile(PATTERN_TEMPLATE.format(subpattern=SUBPATTERN_1))
PATTERN_2 = re.compile(PATTERN_TEMPLATE.format(subpattern=SUBPATTERN_2))

WORD_TO_DIGIT = {x: str(i) for i, x in enumerate(WORDS)}


def read_data():
    with open("input.txt") as f:
        for line in f:
            yield line.rstrip("\n")


def number_constructor(pattern: re.Pattern) -> Callable[[str], int]:
    def construct_number(s: str) -> int:
        x, y, z = pattern.match(s).groups()
        d1, d2 = (z, z) if z is not None else (x, y)

        num1, num2 = map(int, (WORD_TO_DIGIT.get(g, g) for g in (d1, d2)))

        num = 10 * num1 + num2
        return num

    return construct_number


def main() -> None:
    part_1 = sum(map(number_constructor(PATTERN_1), read_data()))
    part_2 = sum(map(number_constructor(PATTERN_2), read_data()))

    print(f"{part_1 = }, {part_2 = }")


if __name__ == "__main__":
    main()
