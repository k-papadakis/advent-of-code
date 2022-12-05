import re
from itertools import takewhile, dropwhile
from typing import Generator


def read_stacks(input_file: str) -> list[list[str]]:
    with open(input_file) as f:

        n_stacks = (len(f.readline()) + 1) // 4
        stacks = [[] for _ in range(n_stacks)]
        f.seek(0)

        for line in takewhile(lambda line: line.lstrip().startswith('['), f):
            for i, letter in enumerate(line[1::4]):
                if letter != ' ':
                    stacks[i].append(letter)

    for stack in stacks:
        stack.reverse()

    return stacks


def read_moves(input_file: str) -> Generator[tuple[int, int, int], None, None]:
    pattern = re.compile(r'move (\d+) from (\d+) to (\d+)')

    with open(input_file) as f:
        for line in dropwhile(lambda line: not line.startswith('move'), f):
            match = pattern.match(line)
            yield tuple(map(int, match.groups()))


class MultiStack:

    def __init__(self, stacks: list[list]) -> None:
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

    def peek(self) -> list:
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
