import re
from collections.abc import Callable, Generator

WORDS = ("zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine")
word_to_digit = {x: str(i) for i, x in enumerate(WORDS)}

pattern_template = r"(?:.*?({subpattern}).*({subpattern}).*?$)|(?:.*?({subpattern}))"

pattern_1 = pattern_template.format(subpattern=r"\d")
pattern_2 = pattern_template.format(subpattern=rf"\d|{'|'.join(WORDS)}")


def _assert_match(match: re.Match[str] | None) -> re.Match[str]:
    if not match:
        raise ValueError("Could not match pattern.")
    return match


def read_data() -> Generator[str, None, None]:
    with open("input.txt") as f:
        for line in f:
            yield line.rstrip("\n")


def number_constructor(pattern: str | re.Pattern[str]) -> Callable[[str], int]:
    pattern = re.compile(pattern)

    def construct_number(s: str) -> int:
        match _assert_match(pattern.match(s)).groups():
            case None, None, str(z):
                d1 = d2 = z
            case str(x), str(y), None:
                d1, d2 = x, y
            case _:
                raise ValueError("Invalid regex match.")

        num1, num2 = map(int, (word_to_digit.get(g, g) for g in (d1, d2)))

        num = 10 * num1 + num2
        return num

    return construct_number


def main() -> None:
    part_1 = sum(map(number_constructor(pattern_1), read_data()))
    part_2 = sum(map(number_constructor(pattern_2), read_data()))

    print(f"{part_1 = }, {part_2 = }")


if __name__ == "__main__":
    main()
