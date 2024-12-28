from functools import cache, reduce
from itertools import pairwise, starmap
import sys


def read_input(file_path: str) -> list[str]:
    with open(file_path) as f:
        return f.read().splitlines()


NUMPAD = [
    ["7", "8", "9"],
    ["4", "5", "6"],
    ["1", "2", "3"],
    ["X", "0", "A"],
]
NUMPAD_POS = {
    NUMPAD[i][j]: (i, j) for i in range(len(NUMPAD)) for j in range(len(NUMPAD[0]))
}

DIRPAD = [
    ["X", "^", "A"],
    ["<", "v", ">"],
]
DIRPAD_POS = {
    DIRPAD[i][j]: (i, j) for i in range(len(DIRPAD)) for j in range(len(DIRPAD[0]))
}

ATOD = {
    ">": (0, 1),
    "^": (-1, 0),
    "<": (0, -1),
    "v": (1, 0),
}
DTOA = {v: k for k, v in ATOD.items()}


@cache
def shortest_paths(source_str: str, target_str: str) -> list[str]:
    # TODO: make this function recursive to avoid recomputation
    if source_str in DIRPAD_POS and target_str in DIRPAD_POS:
        pad = DIRPAD
        source = DIRPAD_POS[source_str]
        target = DIRPAD_POS[target_str]
    elif source_str in NUMPAD_POS and target_str in NUMPAD_POS:
        pad = NUMPAD
        source = NUMPAD_POS[source_str]
        target = NUMPAD_POS[target_str]
    else:
        raise ValueError("source and target are not in the same pad")

    res: list[str] = []
    l1 = abs(target[0] - source[0]) + abs(target[1] - source[1])
    stack = [(source, "")]
    while stack:
        pos, path = stack.pop()
        if (
            len(path) > l1
            or not (0 <= pos[0] < len(pad))
            or not (0 <= pos[1] < len(pad[0]))
            or pad[pos[0]][pos[1]] == "X"
        ):
            continue
        if pos == target:
            res.append(path)
        for c, d in ATOD.items():
            stack.append(((pos[0] + d[0], pos[1] + d[1]), path + c))
    return res


def join_two(paths: list[str], other_paths: list[str]) -> list[str]:
    return [path + "A" + other_path for path in paths for other_path in other_paths]


def next_seq(seq: str) -> list[str]:
    return reduce(join_two, starmap(shortest_paths, pairwise("A" + seq + "A")))


def main():
    file_path = sys.argv[1]
    codes = read_input(file_path)

    part_1 = 0
    for code in codes:
        paths_1 = next_seq(code)
        paths_2 = [seq for path in paths_1 for seq in next_seq(path)]
        paths_3 = [seq for path in paths_2 for seq in next_seq(path)]
        min_len = min(map(len, paths_3))
        code_int = int(code[:-1])
        part_1 += min_len * code_int
    print(part_1)


if __name__ == "__main__":
    main()
