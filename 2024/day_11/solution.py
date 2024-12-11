import functools
import sys


def read_input(file_path: str) -> list[int]:
    with open(file_path) as f:
        s = f.read()
    rocks = list(map(int, s.split()))
    return rocks


def count_digits(n: int, base: int = 10) -> int:
    res = 0
    t = n
    while t != 0:
        t //= base
        res += 1
    return res


def rsplit_int(n: int, position: int, base: int = 10) -> tuple[int, int]:
    divisor: int = pow(base, position)
    return divmod(n, divisor)


@functools.cache
def blink(rock: int, nblinks: int) -> int:
    if nblinks == 0:
        return 1
    elif rock == 0:
        return blink(1, nblinks - 1)
    elif (ndigits := count_digits(rock)) % 2 == 0:
        left, right = rsplit_int(rock, ndigits // 2)
        return blink(left, nblinks - 1) + blink(right, nblinks - 1)
    else:
        return blink(2024 * rock, nblinks - 1)


def main():
    file_path = sys.argv[1]
    rocks = read_input(file_path)
    part_1 = sum(blink(rock, 25) for rock in rocks)
    part_2 = sum(blink(rock, 75) for rock in rocks)
    print(f"{part_1} {part_2}")


if __name__ == "__main__":
    main()
