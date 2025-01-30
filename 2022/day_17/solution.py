from dataclasses import dataclass
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

    def move(self, di: int, dj: int) -> Self:
        return type(self)({(i + di, j + dj) for i, j in self.points})

    def move_up(self, n: int = 1) -> Self:
        return self.move(n, 0)

    def move_down(self, n: int = 1) -> Self:
        return self.move(-n, 0)

    def move_left(self, n: int = 1) -> Self:
        return self.move(0, -n)

    def move_right(self, n: int = 1) -> Self:
        return self.move(0, n)

    def in_bounds(self, width: int = WIDTH) -> bool:
        return all(0 <= j < width for _, j in self.points)

    def disjoint(self, other: Self) -> bool:
        return not self.points & other.points

    def update(self, other: Self) -> None:
        return self.points.update(other.points)

    def get_height(self) -> int:
        return max(i for i, _ in self.points)

    def get_boundary(self, height: int | None = None, width: int = WIDTH) -> Self:
        if height is None:
            height = self.get_height()
        stack: list[Pair] = [(height, 0)]
        seen: set[Pair] = set()
        boundary: set[Pair] = set()
        while stack:
            x, y = stack.pop()
            if (x, y) in seen:
                continue
            seen.add((x, y))
            if not (0 <= x <= height and 0 <= y < width):
                continue
            if (x, y) in self.points:
                boundary.add((x, y))
                continue
            for dx, dy in (1, 0), (0, 1), (-1, 0), (0, -1):
                stack.append((x + dx, y + dy))
        return type(self)(boundary)

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


def show_grid(grid: Shape, shape: Shape | None, width: int = WIDTH) -> None:
    if shape is None:
        shape = Shape(set())
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


def find_height(
    nshapes: int,
    jets: str,
    shape_arrays: list[list[str]] = SHAPE_ARRAYS,
    width: int = WIDTH,
) -> int:
    shapes = [Shape.from_array(a) for a in shape_arrays]

    grid = Shape({(-1, i) for i in range(width)})
    height: int = 0
    i_jet = -1
    # (boundary, i_shape_mod, i_jet_mod) -> i_shape
    states: dict[tuple[frozenset[Pair], int, int], int] = {}
    heights: list[int] = []

    for i_shape in range(nshapes):
        shape = shapes[i_shape % len(shapes)].move(height + 3, 2)

        while True:
            i_jet += 1
            jet = jets[i_jet % len(jets)]
            blown = shape.move_left() if jet == "<" else shape.move_right()
            if blown.in_bounds() and blown.disjoint(grid):
                shape = blown

            descended = shape.move_down()
            if descended.disjoint(grid):
                shape = descended
            else:
                height = max(height, 1 + shape.get_height())
                heights.append(height)
                grid.update(shape)
                boundary = frozenset(grid.get_boundary(height).move_down(height).points)

                # Cycle detection
                s = (boundary, i_shape % len(shapes), i_jet % len(jets))
                if s in states:
                    prev_i_shape = states[s]
                    ncycles, r = divmod(nshapes - prev_i_shape, i_shape - prev_i_shape)
                    return (
                        heights[prev_i_shape]
                        + (heights[i_shape] - heights[prev_i_shape]) * ncycles
                        + (heights[prev_i_shape + r] - heights[prev_i_shape])
                        - 1
                    )
                states[s] = i_shape

                break

    return height


def main() -> None:
    import sys

    file_path = sys.argv[1]
    jets = read_input(file_path)
    part_1 = find_height(2022, jets)
    part_2 = find_height(1_000_000_000_000, jets)
    print(f"{part_1 = } {part_2}")


if __name__ == "__main__":
    main()
