# %%
def read_data(input_file):
    dirmap = {'L': (0, -1), 'R': (0, 1), 'U': (1, 0), 'D': (-1, 0)}
    with open(input_file) as f:
        for line in f:
            direction, n_steps = line.split()
            yield dirmap[direction], int(n_steps)


# %%
# Track relative position of the head. It can be any of:

# UL U UR
#  L *  R
# DL D DR

# (-1,  1) ( 0, 1) ( 1, 1)
# ( 0, -1) ( 0, 0) ( 0, 1)
# (-1, -1) (-1, 0) (-1, 1)

# If l1(pos) == 2 and move goes outside the grid, then move diagonally to the position the head was at
# If l1(pos) == 1 and move goes outside the grid, move to the same direction as the head


def l1(v):
    return abs(v[0]) + abs(v[1])


def add(u, v):
    return u[0] + v[0], u[1] + v[1]


def subtract(u, v):
    return u[0] - v[0], u[1] - v[1]


def arg_non_zero(v):
    return 0 if v[0] != 0 else 1


def part1(data):
    h_pos = t_pos = 0, 0
    visited = {t_pos}

    for direction, n_steps in data:
        for _ in range(n_steps):

            relative_h_pos = subtract(h_pos, t_pos)

            if l1(relative_h_pos) == 2:
                idx = arg_non_zero(direction)
                if relative_h_pos[idx] == direction[idx]:
                    t_pos = h_pos
            else:
                idx = arg_non_zero(direction)
                if relative_h_pos[idx] == direction[idx]:
                    t_pos = add(t_pos, direction)

            h_pos = add(h_pos, direction)

            visited.add(t_pos)

    return len(visited)


print(part1(read_data('input.txt')))

# %%
