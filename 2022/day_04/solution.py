import re


def read_data():
    pattern = re.compile(r'(\d+)-(\d+),(\d+)-(\d+)\n')
    with open('input.txt') as f:
        for line in f:
            match = pattern.match(line)
            yield tuple(map(int, match.groups()))


def is_nested(t):
    return (t[0] <= t[2] and t[3] <= t[1]) or (t[2] <= t[0] and t[1] <= t[3])


def is_overlapped(t):
    return max(t[0], t[2]) <= min(t[1], t[3])


def main():
    part1 = sum(map(is_nested, read_data()))
    part2 = sum(map(is_overlapped, read_data()))
    print(f'part1: {part1}\npart2: {part2}')


if __name__ == '__main__':
    main()
