# %%
def read_data(input_file):
    with open(input_file) as f:
        for line in f:
            if line.startswith('noop'):
                yield None
            else:  # line.startswith('add')
                yield int(line.split()[1])


def part1(vals):
    cycle_start, cycle_end = None, 1
    x = 1
    res = 0

    for val in vals:
        if val is None:
            cycle_start, cycle_end = cycle_end, cycle_end + 1
        else:
            cycle_start, cycle_end = cycle_end, cycle_end + 2

        for cycle in range(20, 221, 40):
            if cycle_start <= cycle < cycle_end:
                res += cycle * x

        if val is not None:
            x += val

    return res


def part2(vals):
    monitor = ['.'] * 240
    sprite = 0
    cycle_start, cycle_end = None, 0

    for val in vals:

        if val is None:
            cycle_start, cycle_end = cycle_end, cycle_end + 1
        else:
            cycle_start, cycle_end = cycle_end, cycle_end + 2

        for k in range(cycle_start, cycle_end):
            if sprite <= k % 40 < sprite + 3:
                monitor[k] = '#'

        if val is not None:
            sprite += val

    return '\n'.join(''.join(monitor[i * 40 + j] for j in range(40)) for i in range(6))


def main():
    print(f'part1: {part1(read_data("mini.txt"))}\npart2:\n{part2(read_data("input.txt"))}')


if __name__ == '__main__':
    main()
