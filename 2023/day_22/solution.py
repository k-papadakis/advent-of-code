import sys
from dataclasses import dataclass
from collections import defaultdict


@dataclass(slots=True, frozen=True)
class Brick:
    x_min: int
    y_min: int
    z_min: int
    x_max: int
    y_max: int
    z_max: int


def read_input(file_path: str) -> list[Brick]:
    bricks: list[Brick] = []
    with open(file_path) as f:
        for brick_str in f:
            starts_str, ends_str = brick_str.strip().split("~")
            x_min, y_min, z_min = map(int, starts_str.split(","))
            x_max, y_max, z_max = map(int, ends_str.split(","))
            bricks.append(Brick(x_min, y_min, z_min, x_max, y_max, z_max))
    return bricks


def build_brick_graph(
    bricks: list[Brick],
) -> tuple[defaultdict[int, set[int]], defaultdict[int, set[int]]]:
    x_max = max(brick.x_max for brick in bricks)
    y_max = max(brick.y_max for brick in bricks)
    heights = [[0 for _ in range(1 + y_max)] for _ in range(1 + x_max)]
    brick_ids = [[-1 for _ in range(1 + y_max)] for _ in range(1 + x_max)]
    supporters: defaultdict[int, set[int]] = defaultdict(set)
    supportees: defaultdict[int, set[int]] = defaultdict(set)
    for brick_id, brick in sorted(enumerate(bricks), key=lambda t: t[1].z_min):
        rx = range(brick.x_min, brick.x_max + 1)
        ry = range(brick.y_min, brick.y_max + 1)
        height = max(heights[x][y] for x in rx for y in ry)
        for x in rx:
            for y in ry:
                if heights[x][y] == height:
                    supporter_id = brick_ids[x][y]
                    if supporter_id != -1:
                        supporters[brick_id].add(supporter_id)
                        supportees[supporter_id].add(brick_id)
                heights[x][y] = height + brick.z_max - brick.z_min + 1
                brick_ids[x][y] = brick_id
    return supporters, supportees


def main():
    file_path = sys.argv[1]
    bricks = read_input(file_path)
    supporters, supportees = build_brick_graph(bricks)

    part_1 = sum(
        all(len(supporters[supportee]) > 1 for supportee in supportees[brick_id])
        for brick_id in range(len(bricks))
    )
    print(part_1)


if __name__ == "__main__":
    main()
