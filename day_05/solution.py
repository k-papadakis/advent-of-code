# %%
from itertools import takewhile, dropwhile
import re


def read_stacks():
    stacks = [[] for _ in range(9)]
    
    with open('input.txt') as f:
        for line in takewhile(lambda line: not line[1].isdigit(), f):
            for i, letter in enumerate(line[1::4]):
                if letter != ' ':
                    stacks[i].append(letter)

    for stack in stacks:
        stack.reverse()

    return stacks


def read_moves():
    pattern = re.compile(r'move (\d+) from (\d+) to (\d+)\n')
    
    with open('input.txt') as f:
        for line in dropwhile(lambda line: not line.startswith('m'), f):
            match = pattern.match(line)
            yield tuple(map(int, match.groups()))


def do_move_1(stacks, instruction):
    num, source, target = instruction
    for _ in range(num):
        stacks[target-1].append(stacks[source-1].pop())
    return stacks


# TODO: Implement a class

def do_moves(stacks, instructions, move_fn):
    for instruction in instructions:
        move_fn(stacks, instruction)
    return stacks

def part1():
    stacks = read_stacks()
    moves = read_moves()
    stacks = do_moves(stacks, moves, do_move_1)
    return ''.join(stack[-1] for stack in stacks)


# %%

stacks = read_stacks()
moves = read_moves()

def do_move_2(stacks, instruction):
    num, source, target = instruction
    t = []
    for _ in range(num):
        t.append(stacks[source-1].pop())
    for _ in range(num):
        stacks[target-1].append(t.pop())
    return stacks


do_moves(stacks, moves, do_move_2)
''.join(stack[-1] for stack in stacks)




# %%
