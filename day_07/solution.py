from typing import Optional


class TreeNode:

    def __init__(
        self,
        name: str,
        size: Optional[int] = None,
        children: Optional[dict[str, 'TreeNode']] = None,
        parent: Optional['TreeNode'] = None
    ):
        self.name = name
        self.size = size
        self.children = children if children is not None else {}
        self.parent = parent

    def __repr__(self):
        return f'TreeNode(name={self.name}, size={self.size}, children={list(self.children.values())})'

    def __str__(self, level=0):
        ret = '\t' * level + self.name + (f' {self.size or ""}') + '\n'
        for child in self.children.values():
            ret += child.__str__(level + 1)
        return ret


def read_data(input_file):
    with open(input_file) as f:
        for line in f:
            yield line.rstrip('\n')


def parse_tree(lines):

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


def bottom_up_sum(node: TreeNode):
    sum_below_thresh = 0

    def _bottom_up_sum(node: TreeNode):
        nonlocal sum_below_thresh

        # leaf file node
        if node.size is not None:
            return node.size

        s = sum(_bottom_up_sum(child) for child in node.children.values())

        if s <= 100_000:
            sum_below_thresh += s

        return s

    return _bottom_up_sum(node), sum_below_thresh


def min_deletion(node: TreeNode, space_to_free):
    res = float('Infinity')

    def _bottom_up_sum(node: TreeNode):
        nonlocal res

        # leaf file node
        if node.size is not None:
            return node.size

        s = sum(_bottom_up_sum(child) for child in node.children.values())

        if space_to_free < s < res:
            res = s

        return s

    return _bottom_up_sum(node), res


def main():
    root = parse_tree(read_data('input.txt'))
    # print(root)
    # print(repr(root))
    total, part1 = bottom_up_sum(root)
    free_space = 70_000_000 - total
    space_to_free = max(0, 30_000_000 - free_space)
    _, part2 = min_deletion(root, space_to_free)

    print(f'part1: {part1}\npart2: {part2}')


if __name__ == '__main__':
    main()
