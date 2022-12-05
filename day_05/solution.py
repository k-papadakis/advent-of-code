import re
from itertools import takewhile, dropwhile
from typing import Generator, Any


def _read_n_stacks(input_file: str) -> int:
    pattern = re.compile(r'(\d+)\s+$')

    with open(input_file) as f:
        match = next(match for match in map(pattern.search, f) if match)
        return int(match.group(1))


def read_stacks(input_file: str) -> list[list[str]]:
    stacks = [[] for _ in range(_read_n_stacks(input_file))]

    with open(input_file) as f:
        for line in takewhile(lambda line: not line[1].isdigit(), f):
            for i, letter in enumerate(line[1::4]):
                if letter != ' ':
                    stacks[i].append(letter)

    for stack in stacks:
        stack.reverse()

    return stacks


def read_moves(input_file: str) -> Generator[tuple[int, int, int], None, None]:
    pattern = re.compile(r'move (\d+) from (\d+) to (\d+)')

    with open(input_file) as f:
        for line in dropwhile(lambda line: not line.startswith('m'), f):
            match = pattern.match(line)
            yield tuple(map(int, match.groups()))


class MultiStack:

    def __init__(self, stacks: list[list[Any]]) -> None:
        self.stacks = stacks

    def move_1(self, num: int, source: int, target: int) -> None:
        for _ in range(num):
            self.stacks[target].append(self.stacks[source].pop())

    def move_2(self, num: int, source: int, target: int) -> None:
        t = []
        for _ in range(num):
            t.append(self.stacks[source].pop())
        for _ in range(num):
            self.stacks[target].append(t.pop())

    def peek(self) -> list[Any]:
        return [stack[-1] for stack in self.stacks]


def move_all(input_file, move_fn_name):
    multistack = MultiStack(read_stacks(input_file))
    move = getattr(multistack, move_fn_name)

    for num, source, target in read_moves(input_file):
        move(num, source - 1, target - 1)

    return ''.join(multistack.peek())


def main():
    part1 = move_all('input.txt', 'move_1')
    part2 = move_all('input.txt', 'move_2')
    print(f"part1: {part1}\npart2: {part2}")


if __name__ == '__main__':
    main()
