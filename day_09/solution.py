# %%
def read_data(input_file):
    dirmap = {'L': (0, -1), 'R': (0, 1), 'U': (1, 0), 'D': (-1, 0)}
    with open(input_file) as f:
        for line in f:
            direction, n_steps = line.split()
            yield dirmap[direction], int(n_steps)


def l1(v):
    return abs(v[0]) + abs(v[1])


def add(u, v):
    return u[0] + v[0], u[1] + v[1]


def subtract(u, v):
    return u[0] - v[0], u[1] - v[1]


def arg_non_zero(v):
    return 0 if v[0] != 0 else 1


def move_follower(leader, follower, direction):
    relative_h_pos = subtract(leader, follower)

    if l1(relative_h_pos) == 2:
        idx = arg_non_zero(direction)
        if relative_h_pos[idx] == direction[idx]:
            follower = leader
    else:
        idx = arg_non_zero(direction)
        if relative_h_pos[idx] == direction[idx]:
            follower = add(follower, direction)

    return follower


def part1(data):
    head = tail = 0, 0
    visited = {tail}

    for direction, n_steps in data:
        for _ in range(n_steps):
            tail = move_follower(tail, head, direction)
            head = add(head, direction)
            visited.add(tail)

    return len(visited)


def part2(data):
    knots = [(0, 0)] * 10
    visited = {knots[-1]}

    for head_direction, n_steps in data:
        for _ in range(n_steps):
            direction = head_direction
            print(f'Moving head by {direction}')

            for i in range(len(knots) - 1):
                follower_old = knots[i + 1]
                knots[i + 1] = move_follower(knots[i], knots[i + 1], direction)
                knots[i] = add(knots[i], direction)
                direction = subtract(knots[i + 1], follower_old)
                print(direction)
                
            visited.add(knots[-1])


    print(visited)
    return len(visited)


part2(read_data('mini.txt'))

# %%
