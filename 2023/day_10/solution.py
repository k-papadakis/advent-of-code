from itertools import chain

type Pair = tuple[int, int]

RIGHT = (0, 1)
UP = (-1, 0)
LEFT = (0, -1)
DOWN = (1, 0)


PIPES: dict[str, dict[Pair, Pair]] = {
    "|": {UP: UP, DOWN: DOWN},
    "-": {LEFT: LEFT, RIGHT: RIGHT},
    "F": {UP: RIGHT, LEFT: DOWN},
    "J": {RIGHT: UP, DOWN: LEFT},
    "L": {DOWN: RIGHT, LEFT: UP},
    "7": {RIGHT: DOWN, UP: LEFT},
}


def read_input(path: str) -> list[list[str]]:
    with open(path) as f:
        s = f.read()
    grid = list(map(list, s.splitlines()))

    assert set(chain.from_iterable(grid)) <= {"S", "F", "|", "-", "J", ".", "L", "7"}

    return grid


def add(u: Pair, v: Pair) -> Pair:
    return (u[0] + v[0], u[1] + v[1])


def find_source(grid: list[list[str]]) -> Pair:
    m, n = len(grid), len(grid[0])
    source = next((i, j) for i in range(m) for j in range(n) if grid[i][j] == "S")
    return source


def initialize_cursor(grid: list[list[str]], source: Pair) -> tuple[Pair, Pair]:
    directions = RIGHT, UP, LEFT, DOWN
    candidates = (add(source, direction) for direction in directions)
    cursor = next(
        ((i, j), PIPES[grid[i][j]][direction])
        for direction, (i, j) in zip(directions, candidates)
        if direction in PIPES[grid[i][j]]
    )
    return cursor


grid = read_input("input.txt")
source = find_source(grid)
cursor = initialize_cursor(grid, source)
level = 0

while True:
    level += 1

    old_pos, old_direction = cursor
    pos = add(old_pos, old_direction)
    val = grid[pos[0]][pos[1]]
    if val == "S":
        break
    direction = PIPES[val][old_direction]

    cursor = pos, direction

print((level + 1) // 2)
