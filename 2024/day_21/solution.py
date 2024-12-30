import sys
from functools import cache
from itertools import pairwise

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

DIRECTIONS = [(">", (0, 1)), ("^", (-1, 0)), ("<", (0, -1)), ("v", (1, 0))]


def read_input(file_path: str) -> list[str]:
    with open(file_path) as f:
        return f.read().splitlines()


@cache
def shortest_paths(source_str: str, target_str: str) -> list[str]:
    if source_str in DIRPAD_POS and target_str in DIRPAD_POS:
        pad = DIRPAD
        source = DIRPAD_POS[source_str]
        target = DIRPAD_POS[target_str]
    elif source_str in NUMPAD_POS and target_str in NUMPAD_POS:
        pad = NUMPAD
        source = NUMPAD_POS[source_str]
        target = NUMPAD_POS[target_str]
    else:
        raise ValueError("`source` and `target` are not in the same pad.")

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
        for c, d in DIRECTIONS:
            stack.append(((pos[0] + d[0], pos[1] + d[1]), path + c))
    return res


@cache
def shortest_path_length(source: str, target: str, num_robot_dirpads: int) -> int:
    paths = shortest_paths(source, target)
    if num_robot_dirpads == 0:
        return 1 + min(map(len, paths))  # 1 is for the A that needs to be pressed
    return min(
        sum(
            shortest_path_length(a, b, num_robot_dirpads - 1)
            for a, b in pairwise("A" + path + "A")
        )
        for path in paths
    )


def code_complexity(code: str, num_robot_dirpads: int) -> int:
    path_len = sum(
        shortest_path_length(a, b, num_robot_dirpads) for a, b in pairwise("A" + code)
    )
    return path_len * int(code[:-1])


def main():
    file_path = sys.argv[1]
    codes = read_input(file_path)
    part_1 = sum(code_complexity(code, 2) for code in codes)
    part_2 = sum(code_complexity(code, 25) for code in codes)
    print(f"{part_1 = } {part_2 = }")


if __name__ == "__main__":
    main()
