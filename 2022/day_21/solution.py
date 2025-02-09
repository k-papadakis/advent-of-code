import re
from typing import Literal

type Tree = dict[str, tuple[str, str]]
type Op = Literal["-", "+", "*", "/"]


def read_input(file_path: str) -> tuple[Tree, dict[str, int], dict[str, Op]]:
    vals: dict[str, int] = {}
    ops: dict[str, Op] = {}
    graph: Tree = {}
    val_pattern = re.compile(r"(\w+): (\d+)")
    node_pattern = re.compile(r"(\w+): (\w+) ([-+*/]) (\w+)")
    with open(file_path) as f:
        for i, line in enumerate(f, 1):
            if m := val_pattern.match(line):
                vals[m[1]] = int(m[2])
            elif m := node_pattern.match(line):
                graph[m[1]] = (m[2], m[4])
                ops[m[1]] = m[3]  # pyright: ignore[reportArgumentType]
            else:
                raise ValueError(f"Invalid line {i}: {line}")
    return graph, vals, ops


def evaluate(
    tree: Tree,
    ops: dict[str, Op],
    vals: dict[str, int],
    node: str,
    excluded: set[str] | None = None,
) -> dict[str, int]:
    if excluded is None:
        excluded = set()
    vals = {k: v for k, v in vals.items() if k not in excluded}

    def dfs(node: str) -> None:
        if node in vals or node in excluded:
            return
        left, right = tree[node]
        dfs(left)
        dfs(right)
        if not (left in vals and right in vals):
            return
        match ops[node]:
            case "-":
                vals[node] = vals[left] - vals[right]
            case "+":
                vals[node] = vals[left] + vals[right]
            case "*":
                vals[node] = vals[left] * vals[right]
            case "/":
                vals[node] = vals[left] // vals[right]

    dfs(node)
    return vals


def find_human_val(
    tree: Tree, ops: dict[str, Op], vals: dict[str, int], root: str, human: str
) -> int:
    vals = evaluate(tree, ops, vals, root, {human})
    node = next(node for node in tree[root] if node not in vals)
    vals[node] = next(vals[node] for node in tree[root] if node in vals)

    def fill(node: str) -> None:
        if node not in tree:
            return
        left, right = tree[node]
        if left in vals and right in vals:
            return
        elif left in vals:
            match ops[node]:
                case "+":
                    vals[right] = vals[node] - vals[left]
                case "-":
                    vals[right] = vals[left] - vals[node]
                case "*":
                    vals[right] = vals[node] // vals[left]
                case "/":
                    vals[right] = vals[left] // vals[node]
        elif right in vals:
            match ops[node]:
                case "+":
                    vals[left] = vals[node] - vals[right]
                case "-":
                    vals[left] = vals[right] + vals[node]
                case "*":
                    vals[left] = vals[node] // vals[right]
                case "/":
                    vals[left] = vals[right] * vals[node]
        else:
            raise ValueError(f"Both children of {node} are unevaluated.")
        fill(left)
        fill(right)

    fill(node)
    return vals[human]


def main() -> None:
    import sys

    file_path = sys.argv[1]
    tree, vals, ops = read_input(file_path)
    part_1 = evaluate(tree, ops, vals, "root")["root"]
    part_2 = find_human_val(tree, ops, vals, "root", "humn")
    print(f"{part_1 = } {part_2 = }")


if __name__ == "__main__":
    main()
