from itertools import batched


class Grid:
    def __init__(self, grid: list[list[str]]):
        m, n = len(grid), len(grid[0])
        if m != n:
            raise NotImplementedError("This class does not handle non-square grids.")
        self.grid = grid
        self.shape = m, n

    def __getitem__(self, index: tuple[int, int]) -> str:
        i, j = index
        return self.grid[i][j]

    def __setitem__(self, index: tuple[int, int], value: str) -> None:
        i, j = index
        self.grid[i][j] = value

    def __iter__(self):
        return iter(self.grid)

    def __repr__(self) -> str:
        return "\n".join("".join(row) for row in self)

    def to_flat_str(self) -> str:
        return "".join("".join(row) for row in self)

    def parse_flat_str(self, string: str) -> "Grid":
        _, n = self.shape
        data = [list(batch) for batch in batched(string, n)]
        return type(self)(data)

    def north_load(self) -> int:
        m, n = self.shape
        return sum(m - i for i in range(m) for j in range(n) if self[i, j] == "O")

    def tilt_north(self) -> None:
        m, n = self.shape

        cur = [-1] * n

        for i in range(m):
            for j in range(n):
                match self[i, j]:
                    case "O":
                        cur[j] += 1
                        self[cur[j], j], self[i, j] = self[i, j], self[cur[j], j]
                    case "#":
                        cur[j] = i
                    case ".":
                        pass
                    case _:
                        raise ValueError(f"Unknown symbol {self[i, j]}")

    def reverse_rows(self) -> None:
        self.grid.reverse()

    def reverse_cols(self) -> None:
        for row in self:
            row.reverse()

    def transpose(self) -> None:
        m, n = self.shape

        for i in range(m):
            for j in range(i + 1, n):
                self[i, j], self[j, i] = self[j, i], self[i, j]

    def rotate_clockwise(self) -> None:
        self.reverse_rows()
        self.transpose()

    def rotate_anticlockwise(self) -> None:
        self.reverse_cols()
        self.transpose()

    def cycle(self) -> None:
        for _ in range(4):
            self.tilt_north()
            self.rotate_clockwise()

    def repeat_cycle(self, repetitions: int) -> None:
        start: int = 0
        period: int = repetitions
        cache: dict[str, int] = {self.to_flat_str(): 0}

        for i in range(1, repetitions + 1):
            self.cycle()
            s = self.to_flat_str()
            if s in cache:
                start = cache[s]
                period = i - cache[s]
                break
            cache[s] = i

        num_cycles = start + (repetitions - start) % period
        final_grid_str = next(
            grid_str
            for grid_str, repetition in cache.items()
            if repetition == num_cycles
        )
        final_grid = self.parse_flat_str(final_grid_str)
        self.grid = final_grid.grid


def read_input(path: str) -> Grid:
    with open(path) as f:
        s = f.read()
    return Grid(list(map(list, s.splitlines())))


def main() -> None:
    path = "input.txt"

    grid = read_input(path)
    grid.tilt_north()
    part_1 = grid.north_load()

    grid = read_input(path)
    grid.repeat_cycle(1_000_000_000)
    part_2 = grid.north_load()

    print(f"{part_1 = }, {part_2 = }")


if __name__ == "__main__":
    main()
