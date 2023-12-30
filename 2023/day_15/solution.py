from dataclasses import dataclass
from functools import reduce
from typing import Iterator


def read_input(path: str) -> list[str]:
    with open(path) as f:
        instructions_str = f.read()
    instructions = instructions_str.rstrip("\n").split(",")
    return instructions


def ascii_hash(s: str) -> int:
    return reduce(lambda acc, x: ((acc + x) * 17) % 256, map(ord, s), 0)


@dataclass(slots=True)
class Node:
    key: str
    value: int = 0
    next: "Node | None" = None
    prev: "Node | None" = None


class HashedLinkedList:
    """An simple alternative to `collections.OrderedDict`."""

    __slots__ = ["left_root", "right_root", "map"]

    def __init__(self) -> None:
        self.left_root = Node("^")
        self.right_root = Node("$")

        self.left_root.next = self.right_root
        self.right_root.prev = self.left_root

        self.map: dict[str, Node] = {}

    def __getitem__(self, key: str) -> int:
        return self.map[key].value

    def __setitem__(self, key: str, value: int) -> None:
        if key in self.map:
            self.map[key].value = value
            return

        node = Node(key=key, value=value)
        self.map[key] = node

        left = self.right_root.prev
        right = self.right_root

        assert left is not None
        left.next = node
        node.prev = left

        right.prev = node
        node.next = right

    def __delitem__(self, key: str) -> None:
        if key not in self.map:
            return

        node = self.map[key]
        left = node.prev
        right = node.next

        assert left is not None and right is not None
        left.next = right
        right.prev = left

        del self.map[key]

    def __iter__(self) -> Iterator[tuple[str, int]]:
        cur = self.left_root
        while cur.next and cur.next is not self.right_root:
            cur = cur.next
            yield cur.key, cur.value

    def __repr__(self) -> str:
        return " ".join(f"[{key} {val}]" for key, val in self)

    def __len__(self) -> int:
        return len(self.map)


class Boxes:
    __slots__ = ["data"]

    def __init__(self) -> None:
        self.data: list[HashedLinkedList] = [HashedLinkedList() for _ in range(256)]

    def __iter__(self) -> Iterator[HashedLinkedList]:
        return iter(self.data)

    def index(self, label: str) -> int:
        return ascii_hash(label)

    def __getitem__(self, label: str) -> int:
        return self.data[self.index(label)][label]

    def __delitem__(self, label: str) -> None:
        del self.data[self.index(label)][label]

    def __setitem__(self, label: str, focal_length: int) -> None:
        self.data[self.index(label)][label] = focal_length

    def instruct(self, instruction: str) -> None:
        if instruction.endswith("-"):
            label = instruction[:-1]
            del self[label]
        else:
            label, focal_length_str = instruction.split("=")
            focal_length = int(focal_length_str)
            self[label] = focal_length

    def focusing_power(self) -> int:
        res = sum(
            box_num * slot_num * focal_length
            for box_num, box in enumerate(self, 1)
            for slot_num, (_, focal_length) in enumerate(box, 1)
        )
        return res

    def __repr__(self) -> str:
        return "\n".join(f"Box {i}: {box}" for i, box in enumerate(self) if box)


def main() -> None:
    instructions = read_input("input.txt")

    part_1 = sum(map(ascii_hash, instructions))

    boxes = Boxes()
    for instruction in instructions:
        boxes.instruct(instruction)
    part_2 = boxes.focusing_power()

    print(f"{part_1 = }, {part_2 = }")


if __name__ == "__main__":
    main()
