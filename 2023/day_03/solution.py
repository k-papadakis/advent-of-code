from collections import defaultdict
from collections.abc import Generator

type Coordinate = tuple[int, int]


def read_input() -> list[list[str]]:
    with open("input.txt") as f:
        return [list(line) for line in f.read().splitlines()]


def issymbol(s: str) -> bool:
    return len(s) == 1 and s != "." and not s.isdigit()


def neighbors(m: int, n: int, i: int, j: int) -> Generator[Coordinate, None, None]:
    for u, v in (
        (i - 1, j),
        (i + 1, j),
        (i, j - 1),
        (i, j + 1),
        (i + 1, j + 1),
        (i - 1, j - 1),
        (i - 1, j + 1),
        (i + 1, j - 1),
    ):
        if 0 <= u < m and 0 <= v < n:
            yield u, v


def list_to_int(lst: list[str]) -> int:
    return int("".join(lst))


def get_part_nums(arr: list[list[str]]) -> Generator[int, None, None]:
    m = len(arr)
    n = len(arr[0])

    start: Coordinate | None = None
    borders_symbol: bool = False

    for i in range(m):
        for j in range(n + 1):
            if j != n and arr[i][j].isdigit():
                if not start:
                    start = i, j
                if not borders_symbol:
                    borders_symbol = any(
                        issymbol(arr[u][v]) for u, v in neighbors(m, n, i, j)
                    )
            else:
                if start and borders_symbol:
                    yield list_to_int(arr[start[0]][start[1] : j])
                start = None
                borders_symbol = False


def get_gears(arr: list[list[str]]) -> dict[Coordinate, tuple[int, int]]:
    m = len(arr)
    n = len(arr[0])

    start: Coordinate | None = None
    bordering_stars: set[Coordinate] = set()
    stars: dict[Coordinate, list[int]] = defaultdict(list)

    for i in range(m):
        for j in range(n + 1):
            if j != n and arr[i][j].isdigit():
                if not start:
                    start = i, j
                bordering_stars.update(
                    (u, v) for u, v in neighbors(m, n, i, j) if arr[u][v] == "*"
                )
            else:
                if start and bordering_stars:
                    number = list_to_int(arr[start[0]][start[1] : j])
                    for star in bordering_stars:
                        stars[star].append(number)
                start = None
                bordering_stars.clear()

    gears = {k: (v[0], v[1]) for k, v in stars.items() if len(v) == 2}
    return gears


def main() -> None:
    part_1 = sum(get_part_nums(read_input()))
    part_2 = sum(x * y for (x, y) in get_gears(read_input()).values())
    print(f"{part_1 = }, {part_2 = }")


if __name__ == "__main__":
    main()
