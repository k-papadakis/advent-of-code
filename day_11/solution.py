from collections import deque
from heapq import nlargest
from math import prod


class Monkey:

    def __init__(self, spec: str):

        spec_lst = spec.splitlines()

        self.name = spec_lst[0].rstrip(':')

        self.items = deque(map(int, spec_lst[1].lstrip('Starting items:').split(',')))

        self.operation = eval(f'lambda old: {spec_lst[2].rsplit("=")[1]}')

        self._divisor = int(spec_lst[3].lstrip('Test: divisible by '))
        self._monkey_true = int(spec_lst[4].lstrip('If true: throw to monkey '))
        self._monkey_false = int(spec_lst[5].lstrip('If false: throw to monkey '))

        self.n_inspects = 0

    def next_monkey(self, worry_level):
        return self._monkey_true if worry_level % self._divisor == 0 else self._monkey_false

    def throw_item(self):
        val = self.items.popleft()
        val = self.operation(val)
        val //= 3
        receiver = self.next_monkey(val)
        self.n_inspects += 1
        return receiver, val

    def catch_item(self, val):
        self.items.append(val)

    def __repr__(self):
        return repr(self.items)


def read_data(input_file) -> list[Monkey]:
    with open(input_file) as f:
        specs = f.read().split('\n\n')

    monkeys = list(map(Monkey, specs))
    return monkeys


def part1(monkeys: list[Monkey]) -> int:
    for _ in range(20):
        for monkey in monkeys:
            for _ in range(len(monkey.items)):
                receiver, val = monkey.throw_item()
                monkeys[receiver].catch_item(val)
    return prod(nlargest(2, (monkey.n_inspects for monkey in monkeys)))


print(part1(read_data('input.txt')))
