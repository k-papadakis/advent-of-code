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


def find_steps_and_area(grid: list[list[str]]) -> tuple[int, int]:
    source = next(
        (i, j)
        for i in range(len(grid))
        for j in range(len(grid[0]))
        if grid[i][j] == "S"
    )
    initial_direction = next(
        direction
        for direction in (RIGHT, UP, LEFT, DOWN)
        if direction in PIPES[grid[source[0] + direction[0]][source[1] + direction[1]]]
    )

    cursor: tuple[Pair, Pair] = source, initial_direction

    length = 0
    vertex = source
    area = 0

    while True:
        old_pos, old_direction = cursor
        pos = old_pos[0] + old_direction[0], old_pos[1] + old_direction[1]

        if pos == source:
            area += vertex[0] * pos[1] - vertex[1] * pos[0]
            break

        val = grid[pos[0]][pos[1]]

        direction = PIPES[val][old_direction]

        if old_direction != direction:
            area += vertex[0] * pos[1] - vertex[1] * pos[0]
            vertex = pos

        cursor = pos, direction
        length += 1

    steps = (length + 1) // 2
    area = (abs(area) - (length - 1)) // 2

    return steps, area


def main() -> None:
    grid = read_input("input.txt")
    part_1, part_2 = find_steps_and_area(grid)
    print(f"{part_1 = }, {part_2 = }")


if __name__ == "__main__":
    main()
