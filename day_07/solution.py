# %%
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
            cur.children[filename] = TreeNode(name=filename, size=int(size), parent=cur)

    return root



total = 0

def bottom_up_sum(node):
    global total
    
    # leaf file node
    if node.size is not None:
        return node.size
    
    s = sum(bottom_up_sum(child) for child in node.children.values())
    
    if s <= 100_000:
        total += s
    
    return s 


root = parse_tree(read_data('input.txt'))
bottom_up_sum(root)
total
