from os import PathLike
import sys
import re


def read_input(file: str | PathLike[str]) -> str:
    with open(file) as f:
        return f.read()


def sum_mul(memory: str) -> int:
    pattern = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)")
    return sum(int(m[1]) * int(m[2]) for m in pattern.finditer(memory))


def sum_mul_enabled(memory: str) -> int:
    pattern = re.compile(
        r"""
        (?P<enable> do\(\))
        | (?P<disable> don't\(\))
        | mul\( (?P<x> \d{1,3}) , (?P<y> \d{1,3}) \)
        """,
        re.DOTALL | re.VERBOSE,
    )
    total = 0
    enable = True
    for m in pattern.finditer(memory):
        if m["enable"] is not None:
            enable = True
        elif m["disable"] is not None:
            enable = False
        else:
            if enable:
                total += int(m["x"]) * int(m["y"])
    return total


def main():
    file = sys.argv[1]
    memory = read_input(file)
    part_1 = sum_mul(memory)
    part_2 = sum_mul_enabled(memory)
    print(f"{part_1 = } {part_2 = }")


if __name__ == "__main__":
    main()
