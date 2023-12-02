def read_data(input_file):
    dirmap = {'L': (0, -1), 'R': (0, 1), 'U': (1, 0), 'D': (-1, 0)}
    with open(input_file) as f:
        for line in f:
            direction, n_steps = line.split()
            yield dirmap[direction], int(n_steps)


def add(u, v):
    return u[0] + v[0], u[1] + v[1]


def subtract(u, v):
    return u[0] - v[0], u[1] - v[1]


def l1(u, v):
    return abs(u[0] - v[0]) + abs(u[1] - v[1])


def find_follower_direction(leader, follower, leader_direction):

    directions = {(-1, 0), (0, -1), (1, 0), (0, 1), (1, 1), (1, -1), (-1, 1), (-1, -1), (0, 0)}

    leader_next = add(leader, leader_direction)

    if subtract(leader_next, follower) in directions:
        return 0, 0

    direction = min(directions, key=lambda direction: l1(leader_next, add(follower, direction)))
    return direction


def simulate(data, n_knots):
    knots = [(0, 0)] * n_knots
    visited = {knots[-1]}

    for direction, n_steps in data:
        for _ in range(n_steps):

            directions = [direction]

            for i in range(len(knots) - 1):
                directions.append(find_follower_direction(knots[i], knots[i + 1], directions[-1]))

            knots = list(map(add, knots, directions))

            visited.add(knots[-1])

    return len(visited)


def main():
    part1 = simulate(read_data('input.txt'), 2)
    part2 = simulate(read_data('input.txt'), 10)
    print(f'part1: {part1}\npart2: {part2}')


if __name__ == '__main__':
    main()
