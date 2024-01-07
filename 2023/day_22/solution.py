from dataclasses import dataclass
from functools import cache
from itertools import groupby, pairwise, product
from pprint import pprint
from typing import Self

type Graph[T] = dict[T, set[T]]


@dataclass(slots=True, frozen=True)
class Range:
    min: int
    max: int

    def intersects(self, other: Self) -> bool:
        return max(self.min, other.min) <= min(self.max, other.max)


@dataclass(slots=True, frozen=True)
class Brick:
    x: Range
    y: Range
    z: Range

    def supports(self, other: Self) -> bool:
        return (
            self.z.max < other.z.min
            and self.x.intersects(other.x)
            and self.y.intersects(other.y)
        )

    def __repr__(self) -> str:
        return f"{self.x.min},{self.y.min},{self.z.min}~{self.x.max},{self.y.max},{self.z.max}"

    @classmethod
    def from_string(cls, brick_str: str) -> Self:
        starts_str, ends_str = brick_str.strip().split("~")
        x_min, y_min, z_min = map(int, starts_str.split(","))
        x_max, y_max, z_max = map(int, ends_str.split(","))
        brick = cls(Range(x_min, x_max), Range(y_min, y_max), Range(z_min, z_max))
        return brick


def find_supporters_supportees(
    bricks: list[Brick],
) -> tuple[Graph[Brick], Graph[Brick]]:
    supporters: Graph[Brick] = {brick: set() for brick in bricks}
    supportees: Graph[Brick] = {brick: set() for brick in bricks}

    bricks = sorted(bricks, key=lambda brick: brick.z.min)

    grouped = [
        list(group) for _, group in groupby(bricks, key=lambda brick: brick.z.min)
    ]
    for g1, g2 in pairwise(grouped):
        for a, b in product(g1, g2):
            if a.supports(b):
                supporters[b].add(a)
                supportees[a].add(b)

    return supporters, supportees


def fall_bricks(bricks: list[Brick]) -> list[Brick]:
    supporters: Graph[Brick] = {brick: set() for brick in bricks}
    for a, b in product(bricks, repeat=2):
        if a.supports(b):
            supporters[b].add(a)

    @cache
    def fall_brick(brick: Brick) -> Brick:
        if not supporters[brick]:
            return Brick(brick.x, brick.y, Range(1, 1))

        z_min = 1 + max(
            supporter.z.max for supporter in map(fall_brick, supporters[brick])
        )
        z_max = z_min + (brick.z.max - brick.z.min)

        return Brick(brick.x, brick.y, Range(z_min, z_max))

    fallen = list(map(fall_brick, bricks))

    return fallen


def read_input(path: str) -> list[Brick]:
    with open(path) as f:
        return list(map(Brick.from_string, f))


def main():
    bricks = read_input("./2023/day_22/small.txt")
    # graph = BricksGraph(bricks)

    fallen = fall_bricks(bricks)

    supporters, supportees = find_supporters_supportees(fallen)

    pprint(supportees)


if __name__ == "__main__":
    main()
