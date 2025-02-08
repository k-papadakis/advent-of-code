import re


def read_input(
    file_path: str,
) -> tuple[dict[str, tuple[str, str]], dict[str, int], dict[str, str]]:
    vals: dict[str, int] = {}
    ops: dict[str, str] = {}
    graph: dict[str, tuple[str, str]] = {}
    val_pattern = re.compile(r"(\w+): (\d+)")
    node_pattern = re.compile(r"(\w+): (\w+) ([-+*/]) (\w+)")
    with open(file_path) as f:
        for i, line in enumerate(f, 1):
            if m := val_pattern.match(line):
                vals[m[1]] = int(m[2])
            elif m := node_pattern.match(line):
                graph[m[1]] = (m[2], m[4])
                ops[m[1]] = m[3]
            else:
                raise ValueError(f"Invalid line {i}: {line}")
    return graph, vals, ops


def evaluate(
    tree: dict[str, tuple[str, str]], vals: dict[str, int], ops: dict[str, str]
) -> float:
    def dfs(node: str) -> float:
        if node in vals:
            return vals[node]
        left, right = tree[node]
        match ops[node]:
            case "-":
                return dfs(left) - dfs(right)
            case "+":
                return dfs(left) + dfs(right)
            case "*":
                return dfs(left) * dfs(right)
            case "/":
                return dfs(left) / dfs(right)
            case other:
                raise ValueError(f"Invalid op {other}")

    return dfs("root")


def main() -> None:
    import sys

    file_path = sys.argv[1]
    tree, vals, ops = read_input(file_path)
    print(evaluate(tree, vals, ops))


if __name__ == "__main__":
    main()
