# TODO: Clean up this mess.

from collections import defaultdict

type Point = tuple[int, int]


def read_input(file_path: str) -> list[str]:
    with open(file_path) as f:
        return f.read().splitlines()


DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # NSWE


def step(elves: set[Point], round: int) -> bool:
    # new_elf_pos -> {old_elf_pos}
    proposals: defaultdict[Point, list[Point]] = defaultdict(list)
    for x, y in elves:
        if all(
            (x + dx, y + dy) not in elves
            for dx, dy in DIRECTIONS + [(1, 1), (-1, 1), (1, -1), (-1, -1)]
        ):
            continue
        for idx in range(4):
            dx, dy = DIRECTIONS[(round + idx) % 4]
            nbr = {
                (x + dx, y + dy),
                (x + dx - dy, y + dy + dx),
                (x + dx + dy, y + dy - dx),
            }
            if nbr.isdisjoint(elves):
                proposals[x + dx, y + dy].append((x, y))
                break

    changed = False
    for proposal, old in proposals.items():
        if len(old) == 1:
            elves.remove(old[0])
            elves.add(proposal)
            changed = True
    return changed


def find_bounding_rectangles(elves: set[Point]) -> tuple[Point, Point]:
    min_x = min(elves, key=lambda p: p[0])[0]
    max_x = max(elves, key=lambda p: p[0])[0]
    min_y = min(elves, key=lambda p: p[1])[1]
    max_y = max(elves, key=lambda p: p[1])[1]
    return (min_x, min_y), (max_x, max_y)


def print_grid(elves: set[Point]) -> None:
    (min_x, min_y), (max_x, max_y) = find_bounding_rectangles(elves)
    if min_x < 0:
        min_x = 0
        max_x -= min_x
    if min_y < 0:
        min_y = 0
        max_y -= min_y
    grid = [["."] * (max_y + 1) for _ in range(max_x + 1)]
    for elf in elves:
        x, y = elf
        grid[x - min_x][y - min_y] = "#"
    s = "\n".join("".join(row) for row in grid)
    print(s)


def simulate(grid: list[str], rounds: int) -> int:
    elves = {
        (i, j)
        for i in range(len(grid))
        for j in range(len(grid[0]))
        if grid[i][j] == "#"
    }
    # print("Initial state:")
    # print_grid(elves)
    # print()
    for round in range(rounds):
        changed = step(elves, round)
        if not changed:
            print(f"Stable after {round + 1} rounds")
            break
        # print(f"Round {round + 1}:")
        # print_grid(elves)
        # print()
    (min_x, min_y), (max_x, max_y) = find_bounding_rectangles(elves)
    area = (max_x - min_x + 1) * (max_y - min_y + 1)
    return area - len(elves)


def main() -> None:
    import sys

    file_path = sys.argv[1]
    grid = read_input(file_path)
    part_1 = simulate(grid, 100_000)
    print(part_1)


if __name__ == "__main__":
    main()
