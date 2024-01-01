from collections.abc import Iterator, Sequence
from dataclasses import dataclass, field
from heapq import heappop, heappush
from typing import Any, Self


def read_input(path: str) -> list[list[int]]:
    with open(path) as f:
        s = f.read()
    grid = [[int(x) for x in line] for line in s.splitlines()]
    return grid


@dataclass(slots=True, frozen=True)
class Pair:
    x: int
    y: int

    def __add__(self, other: Self) -> Self:
        return type(self)(self.x + other.x, self.y + other.y)

    def left(self) -> Self:
        return type(self)(-self.y, self.x)

    def right(self) -> Self:
        return type(self)(self.y, -self.x)

    def conforms(self, grid: Sequence[Sequence[Any]]) -> bool:
        m, n = len(grid), len(grid[0])
        return 0 <= self.x < m and 0 <= self.y < n

    def at[T](self, grid: Sequence[Sequence[T]]) -> T:
        return grid[self.x][self.y]


RIGHT = Pair(0, 1)
UP = Pair(-1, 0)
LEFT = Pair(0, -1)
DOWN = Pair(1, 0)


@dataclass(slots=True, frozen=True)
class Crucible:
    position: Pair
    direction: Pair
    num_straight: int

    def move_straight(self) -> Self:
        return type(self)(
            self.position + self.direction,
            self.direction,
            self.num_straight + 1,
        )

    def move_left(self) -> Self:
        return type(self)(
            self.position + self.direction.left(),
            self.direction.left(),
            1,
        )

    def move_right(self) -> Self:
        return type(self)(
            self.position + self.direction.right(),
            self.direction.right(),
            1,
        )

    def moves(self, min_num_straight: int, max_num_straight: int) -> Iterator[Self]:
        assert 0 <= min_num_straight < max_num_straight

        if self.num_straight < max_num_straight:
            yield self.move_straight()

        if self.num_straight >= min_num_straight:
            yield self.move_left()
            yield self.move_right()


@dataclass(order=True, slots=True, frozen=True)
class HeapElement:
    heat_loss: int
    crucible: Crucible = field(compare=False)


def min_heat_loss(
    grid: list[list[int]], min_num_straight: int, max_num_straight: int
) -> int:
    m = len(grid)
    n = len(grid[0])

    source = Pair(0, 0)
    target = Pair(m - 1, n - 1)

    heap: list[HeapElement] = []
    heappush(heap, HeapElement(0, Crucible(source, RIGHT, 0)))
    heappush(heap, HeapElement(0, Crucible(source, DOWN, 0)))

    done: set[Crucible] = set()

    while heap:
        element = heappop(heap)
        heat_loss = element.heat_loss
        crucible = element.crucible

        if crucible.position == target and crucible.num_straight >= min_num_straight:
            return heat_loss

        for next_crucible in crucible.moves(min_num_straight, max_num_straight):
            if not next_crucible.position.conforms(grid) or next_crucible in done:
                continue

            done.add(next_crucible)

            next_heat_loss = heat_loss + next_crucible.position.at(grid)

            heappush(
                heap,
                HeapElement(
                    next_heat_loss,
                    next_crucible,
                ),
            )

    return -1


def main() -> None:
    grid = read_input("input.txt")

    part_1 = min_heat_loss(grid, 0, 3)
    part_2 = min_heat_loss(grid, 4, 10)

    print(f"{part_1 = }, {part_2 = }")


if __name__ == "__main__":
    main()
