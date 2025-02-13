def read_input(file_path: str) -> list[str]:
    with open(file_path) as f:
        return f.read().splitlines()


def snafu_to_decimal(snafu: str) -> int:
    res = 0
    for c in snafu:
        if c == "=":
            x = -2
        elif c == "-":
            x = -1
        else:
            x = int(c)
        res *= 5
        res += x
    return res


def decimal_to_snafu(num: int) -> str:
    res: list[str] = []
    while num:
        num, r = divmod(num, 5)
        if r == 3:
            res.append("=")
            num += 1
        elif r == 4:
            res.append("-")
            num += 1
        else:
            res.append(str(r))
    return "".join(reversed(res))


def main() -> None:
    import sys

    file_path = sys.argv[1]
    snafus = read_input(file_path)
    total = sum(map(snafu_to_decimal, snafus))
    part_1 = decimal_to_snafu(total)
    print(part_1)


if __name__ == "__main__":
    main()
