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


def predict(seq: list[int]) -> int:
    diffs = full_diff(seq)
    while len(diffs) > 1:
        x = diffs.pop()[-1]
        diffs[-1].append(diffs[-1][-1] + x)
    return diffs[-1][-1]


seqs = read_input("input.txt")
part_1 = sum(map(predict, seqs))
print(f"{part_1 = }")
