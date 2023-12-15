from functools import reduce


def read_input(path: str) -> list[str]:
    with open(path) as f:
        s = f.read()
    return s.rstrip("\n").split(",")


def ascii_hash(s: str) -> int:
    return reduce(lambda acc, x: ((acc + x) * 17) % 256, map(ord, s), 0)


part_1 = sum(map(ascii_hash, read_input("input.txt")))

print(part_1)
