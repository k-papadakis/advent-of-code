from itertools import starmap

# Translating letters to numbers, so that we can use array indexing
MAP = {'A': 0, 'B': 1, 'C': 2, 'X': 0, 'Y': 1, 'Z': 2}
# MATCH[player][opponent] = points the player wins (excluding the value of his choice)
MATCH = (3, 0, 6), (6, 3, 0), (0, 6, 3)
# VAL[player] = the value of the player's choice
VAL = 1, 2, 3
# DECIDE[player][opponent] = The move the player must choose in part 2
DECIDE = (2, 0, 1), (0, 1, 2), (1, 2, 0)


def read_data():
    with open('input.txt') as f:
        for line in f:
            opponent, player = line.rstrip('\n').split(' ')
            yield MAP[player], MAP[opponent]


def match_score1(player, opponent):
    return MATCH[player][opponent] + VAL[player]


def match_score2(player, opponent):
    player = DECIDE[player][opponent]
    return match_score1(player, opponent)


def total_score(score_fn):
    return sum(starmap(score_fn, read_data()))


def main():
    part1 = total_score(match_score1)
    part2 = total_score(match_score2)
    print(f'part1: {part1}\npart2: {part2}')


if __name__ == '__main__':
    main()
