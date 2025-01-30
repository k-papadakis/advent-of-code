from dataclasses import dataclass
from itertools import cycle, islice
from typing import Self

type Pair = tuple[int, int]

SHAPE_ARRAYS = [
    [
        "####",
    ],
    [
        ".#.",
        "###",
        ".#.",
    ],
    [
        "..#",
        "..#",
        "###",
    ],
    [
        "#",
        "#",
        "#",
        "#",
    ],
    [
        "##",
        "##",
    ],
]
WIDTH = 7


def read_input(file_path: str) -> str:
    with open(file_path) as f:
        return f.read().strip()


@dataclass
class Shape:
    points: set[Pair]

    def offset(self, di: int, dj: int) -> Self:
        return type(self)({(i + di, j + dj) for i, j in self.points})

    def up(self, n: int = 1) -> Self:
        return self.offset(n, 0)

    def down(self, n: int = 1) -> Self:
        return self.offset(-n, 0)

    def left(self, n: int = 1) -> Self:
        return self.offset(0, -n)

    def right(self, n: int = 1) -> Self:
        return self.offset(0, n)

    def in_bounds(self, width: int = WIDTH) -> bool:
        return all(0 <= j < width for _, j in self.points)

    def disjoint(self, other: Self) -> bool:
        return len(self.points & other.points) == 0

    def update(self, other: Self) -> None:
        return self.points.update(other.points)

    def max_height(self) -> int:
        return max(i for i, _ in self.points)

    @classmethod
    def from_array(cls, a: list[str]) -> Self:
        m = len(a)
        return cls(
            {
                (m - 1 - i, j)
                for i in range(len(a))
                for j in range(len(a[0]))
                if a[i][j] == "#"
            }
        )


def show(grid: Shape, shape: Shape, width: int = WIDTH) -> None:
    m = max(i for i, _ in grid.points | shape.points) + 1

    def symbol(i: int, j: int) -> str:
        if (i, j) in shape.points:
            return "@"
        elif (i, j) in grid.points:
            return "#"
        else:
            return "."

    s = "\n".join(
        "".join(symbol(i, j) for j in range(width)) for i in reversed(range(m))
    )
    print(s)


def simulate(nshapes: int, jet_patterns: str, width: int = WIDTH) -> int:
    SHAPES = [Shape.from_array(a) for a in SHAPE_ARRAYS]

    grid = Shape({(-1, i) for i in range(width)})
    grid_height: int = 0
    jet_patterns_iter = cycle(jet_patterns)
    for shape in islice(cycle(SHAPES), nshapes):
        shape = shape.offset(grid_height + 3, 2)

        while shape:
            blown = shape.left() if next(jet_patterns_iter) == "<" else shape.right()
            if blown.in_bounds() and blown.disjoint(grid):
                shape = blown

            descended = shape.down()
            if descended.disjoint(grid):
                shape = descended
            else:
                grid_height = max(grid_height, 1 + shape.max_height())
                grid.update(shape)
                break

    return grid_height


def main() -> None:
    import sys

    file_path = sys.argv[1]
    jet_patterns = read_input(file_path)
    part_1 = simulate(2022, jet_patterns)
    print(f"{part_1 = }")


if __name__ == "__main__":
    main()
