from functools import reduce
from typing import Iterable, Optional


class TreeNode:

    def __init__(
        self,
        name: str,
        size: Optional[int] = None,
        children: Optional[dict[str, 'TreeNode']] = None,
        parent: Optional['TreeNode'] = None
    ) -> None:
        self.name = name
        self.size = size
        self.children = children if children is not None else {}
        self.parent = parent

    def __repr__(self) -> str:
        return f'TreeNode(name={self.name}, size={self.size}, children={list(self.children.values())})'

    def __str__(self, level: int = 0) -> str:
        ret = '\t' * level + self.name + (f' {self.size or ""}') + '\n'
        for child in self.children.values():
            ret += child.__str__(level + 1)
        return ret


def read_data(input_file):
    with open(input_file) as f:
        for line in f:
            yield line.rstrip('\n')


def parse_tree(lines: Iterable[str]) -> TreeNode:

    lines = iter(lines)
    next(lines)
    cur = root = TreeNode('/')

    for line in lines:
        if line == '$ cd ..':
            cur = cur.parent
        elif line.startswith('$ cd'):
            dirname = line.rsplit(' ', 1)[1]
            cur = cur.children.setdefault(dirname, TreeNode(name=dirname, parent=cur))
        elif line == '$ ls':
            continue
        elif line.startswith('dir'):
            dirname = line.rsplit(' ', 1)[1]
            cur.children.setdefault(dirname, TreeNode(name=dirname, parent=cur))
        else:
            size, filename = line.split(' ', 1)
            cur.children.setdefault(filename, TreeNode(name=filename, size=int(size), parent=cur))

    return root


def bottom_up_sum(node: TreeNode) -> tuple[int, int]:
    if node.size is not None:
        return node.size, 0

    s, t = reduce(lambda u, v: (u[0] + v[0], u[1] + v[1]), map(bottom_up_sum, node.children.values()))

    return s, t + (s if s <= 100_000 else 0)


def min_deletion(node: TreeNode, space_to_free: int) -> tuple[int, int]:
    if node.size is not None:
        return node.size, float('Infinity')

    s, t = reduce(
        lambda u, v: (u[0] + v[0], min(u[1], v[1])),
        (min_deletion(child, space_to_free) for child in node.children.values())
    )

    return s, s if space_to_free < s < t else t


def main() -> None:
    root = parse_tree(read_data('input.txt'))
    total, part1 = bottom_up_sum(root)
    _, part2 = min_deletion(root, total - 40_000_000)

    print(f'part1: {part1}\npart2: {part2}')


if __name__ == '__main__':
    main()
