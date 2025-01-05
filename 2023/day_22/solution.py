import sys
from dataclasses import dataclass
from collections import defaultdict, deque, Counter


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


def build_brick_graph(bricks: list[Brick]) -> defaultdict[int, set[int]]:
    x_max = max(brick.x_max for brick in bricks)
    y_max = max(brick.y_max for brick in bricks)
    heights = [[0 for _ in range(1 + y_max)] for _ in range(1 + x_max)]
    brick_ids = [[-1 for _ in range(1 + y_max)] for _ in range(1 + x_max)]
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
                        supportees[supporter_id].add(brick_id)
                heights[x][y] = height + brick.z_max - brick.z_min + 1
                brick_ids[x][y] = brick_id
    return supportees


def count_falls(brick_id: int, supportees: dict[int, set[int]]) -> int:
    num_fallen = 0
    in_degree = Counter(
        supportee for supporter in supportees for supportee in supportees[supporter]
    )
    q = deque([brick_id])
    while q:
        u = q.popleft()
        for v in supportees[u]:
            in_degree[v] -= 1
            if in_degree[v] == 0:
                num_fallen += 1
                q.append(v)
    return num_fallen


def main():
    file_path = sys.argv[1]
    bricks = read_input(file_path)
    supportees = build_brick_graph(bricks)
    part_1 = 0
    part_2 = 0
    for brick_id in range(len(bricks)):
        num_fallen = count_falls(brick_id, supportees)
        if num_fallen == 0:
            part_1 += 1
        else:
            part_2 += num_fallen
    print(f"{part_1 = } {part_2 = }")


if __name__ == "__main__":
    main()
