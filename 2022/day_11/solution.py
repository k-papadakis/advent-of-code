from collections import deque
from heapq import nlargest
from math import prod


class Monkey:

    def __init__(self, spec: str, calm: bool):

        self.calm = calm

        spec_lst = spec.splitlines()

        self.name = spec_lst[0].rstrip(':')

        self.items = deque(map(int, spec_lst[1].lstrip('Starting items:').split(',')))

        self.operation = eval(f'lambda old: {spec_lst[2].rsplit("=")[1]}')

        self.divisor = int(spec_lst[3].lstrip('Test: divisible by '))
        self._monkey_true = int(spec_lst[4].lstrip('If true: throw to monkey '))
        self._monkey_false = int(spec_lst[5].lstrip('If false: throw to monkey '))

        self.n_inspects = 0

    def next_monkey(self, worry_level):
        return self._monkey_true if worry_level % self.divisor == 0 else self._monkey_false

    def throw_item(self):
        val = self.items.popleft()
        val = self.operation(val)
        if self.calm:
            val //= 3
        receiver = self.next_monkey(val)
        self.n_inspects += 1
        return receiver, val

    def catch_item(self, val):
        self.items.append(val)

    def __repr__(self):
        return repr(self.items)


def read_data(input_file) -> list[str]:
    with open(input_file) as f:
        specs = f.read().split('\n\n')
    return specs


def part1(specs: list[str]) -> int:
    monkeys = [Monkey(spec, True) for spec in specs]

    for _ in range(20):
        for monkey in monkeys:
            for _ in range(len(monkey.items)):
                receiver, val = monkey.throw_item()
                monkeys[receiver].catch_item(val)

    return prod(nlargest(2, (monkey.n_inspects for monkey in monkeys)))


def part2(specs: list[str]) -> int:
    monkeys = [Monkey(spec, False) for spec in specs]

    mod = prod(monkey.divisor for monkey in monkeys)

    for _ in range(10_000):
        for monkey in monkeys:
            for _ in range(len(monkey.items)):
                receiver, val = monkey.throw_item()
                monkeys[receiver].catch_item(val % mod)

    return prod(nlargest(2, (monkey.n_inspects for monkey in monkeys)))


def main():
    specs = read_data('input.txt')
    print(f'part1: {part1(specs)}\npart2: {part2(specs)}')


if __name__ == '__main__':
    main()
