from itertools import starmap
from typing import Literal
from collections import namedtuple

GameObject = namedtuple('GameObject', ['A', 'B', 'C', 'val'])
GAME = {'X': GameObject(3, 0, 6, 1), 'Y': GameObject(6, 3, 0, 2), 'Z': GameObject(0, 6, 3, 3)}


def read_data(filename, sep):
    with open(filename) as f:
        for line in f:
            opponent, player = line.rstrip('\n').split(sep)
            yield opponent, player


def match_score(opponent: Literal['A', 'B', 'C'], player: Literal['X', 'Y', 'Z']):
    g = GAME[player]
    return getattr(g, opponent) + g.val


def total_score(filename, sep=' '):
    return sum(starmap(match_score, read_data(filename, sep)))


if __name__ == '__main__':
    print(total_score('input.txt', sep=' '))
