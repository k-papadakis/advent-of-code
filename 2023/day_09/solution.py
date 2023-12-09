from itertools import cycle


def read_input(path: str) -> list[list[int]]:
    with open(path) as f:
        return [list(map(int, line.split())) for line in f]


def diff(seq: list[int]) -> list[int]:
    return [seq[i] - seq[i - 1] for i in range(1, len(seq))]


def full_diff(seq: list[int]) -> list[list[int]]:
    diffs = [seq]
    while set(diffs[-1]) != {0}:
        diffs.append(diff(diffs[-1]))
    return diffs


def predict_future(seq: list[int]) -> int:
    return sum(d[-1] for d in full_diff(seq))


def predict_past(seq: list[int]) -> int:
    return sum(sign * d[0] for sign, d in zip(cycle([1, -1]), full_diff(seq)))


def main() -> None:
    seqs = read_input("input.txt")

    part_1 = sum(map(predict_future, seqs))
    part_2 = sum(map(predict_past, seqs))

    print(f"{part_1 = } {part_2 = }")


if __name__ == "__main__":
    main()
