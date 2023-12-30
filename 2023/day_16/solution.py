from collections import defaultdict, deque
from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class Pair:
    x: int
    y: int

    def __add__(self, other: "Pair") -> "Pair":
        return type(self)(self.x + other.x, self.y + other.y)


right = Pair(0, 1)
up = Pair(-1, 0)
left = Pair(0, -1)
down = Pair(1, 0)

type Beam = tuple[Pair, Pair]


@dataclass(slots=True, frozen=True)
class Mirror:
    value: str
    reflect: dict[Pair, list[Pair]]

    def __repr__(self) -> str:
        return self.value


type MirrorGrid = list[list[Mirror]]

pipe = Mirror(
    "|",
    {
        right: [up, down],
        up: [up],
        left: [up, down],
        down: [down],
    },
)
dash = Mirror(
    "-",
    {
        right: [right],
        up: [left, right],
        left: [left],
        down: [left, right],
    },
)
slash = Mirror(
    "/",
    {
        right: [up],
        up: [right],
        left: [down],
        down: [left],
    },
)
bslash = Mirror(
    "\\",
    {
        right: [down],
        up: [left],
        left: [up],
        down: [right],
    },
)
dot = Mirror(
    ".",
    {
        right: [right],
        up: [up],
        left: [left],
        down: [down],
    },
)


def read_input(path: str) -> MirrorGrid:
    d = {"|": pipe, "-": dash, "/": slash, "\\": bslash, ".": dot}
    with open(path) as f:
        lines = f.read().splitlines()
    grid = [[d[c] for c in line] for line in lines]
    return grid


def energy(grid: MirrorGrid, beam: Beam) -> int:
    m, n = len(grid), len(grid[0])

    beams: deque[Beam] = deque([beam])
    visited: dict[Pair, set[Pair]] = defaultdict(set)

    while beams:
        p, d = beams.popleft()

        if d in visited[p]:
            continue
        visited[p].add(d)

        for dd in grid[p.x][p.y].reflect[d]:
            pp = p + dd
            if pp.x in range(m) and pp.y in range(n):
                beams.append((pp, dd))

    return len(visited)


def main() -> None:
    grid = read_input("small.txt")
    part_1 = energy(grid, (Pair(0, 0), right))

    print(f"{part_1 = }")
