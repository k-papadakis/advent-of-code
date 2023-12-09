from collections.abc import Generator


def read_input(path: str) -> Generator[list[int], None, None]:
    with open(path) as f:
        for line in f:
            yield list(map(int, line.split()))


def diff(seq: list[int]) -> list[int]:
    return [seq[i] - seq[i - 1] for i in range(1, len(seq))]


def full_diff(seq: list[int]) -> Generator[list[int], None, None]:
    d = seq
    yield d
    while set(d) != {0}:
        d = diff(d)
        yield d


def predict_future(seq: list[int]) -> int:
    return sum(d[-1] for d in full_diff(seq))


def predict_past(seq: list[int]) -> int:
    return sum(d[0] if i % 2 == 0 else -d[0] for i, d in enumerate(full_diff(seq)))


def main() -> None:
    path = "input.txt"

    part_1 = sum(map(predict_future, read_input(path)))
    part_2 = sum(map(predict_past, read_input(path)))

    print(f"{part_1 = } {part_2 = }")


if __name__ == "__main__":
    main()
