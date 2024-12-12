import sys
import itertools


def read_input(file_path: str) -> list[str]:
    with open(file_path) as f:
        return f.read().splitlines()


def is_opposite(u: tuple[int, int], v: tuple[int, int]) -> bool:
    return u == (-v[0], -v[1])


def fencing_prices(grid: list[str]) -> tuple[int, int]:
    directions = (1, 0), (0, 1), (-1, 0), (0, -1)
    rm, rn = range(len(grid)), range(len(grid[0]))
    visited = [[False for _ in rn] for _ in rm]
    part_1 = 0
    part_2 = 0
    for start_i, start_j in itertools.product(rm, rn):
        if visited[start_i][start_j]:
            continue
        stack = [(start_i, start_j)]
        visited[start_i][start_j] = True
        area = 0
        perimeter = 0
        corners = 0
        while stack:
            i, j = stack.pop()
            area += 1

            def is_foreign(x: int, y: int) -> bool:
                return x not in rm or y not in rm or grid[x][y] != grid[i][j]

            # Compute corners
            neighbors = [
                (di, dj) for di, dj in directions if not is_foreign(i + di, j + dj)
            ]
            if len(neighbors) == 0:
                corners += 4
            elif len(neighbors) == 1:
                corners += 2
            elif len(neighbors) == 2:
                a, b = neighbors
                if not is_opposite(a, b):
                    corners += is_foreign(i + a[0] + b[0], j + a[1] + b[1]) + (
                        is_foreign(i - a[0], j - a[1])
                        and is_foreign(i - b[0], j - b[1])
                    )
            else:
                for a, b in itertools.combinations(neighbors, 2):
                    corners += not is_opposite(a, b) and is_foreign(
                        i + a[0] + b[0], j + a[1] + b[1]
                    )

            for di, dj in directions:
                x, y = i + di, j + dj
                if not is_foreign(x, y):
                    if not visited[x][y]:
                        stack.append((x, y))
                        visited[x][y] = True
                else:
                    perimeter += 1

        part_1 += area * perimeter
        part_2 += area * corners

    return part_1, part_2


def main():
    file_path = sys.argv[1]
    grid = read_input(file_path)
    part_1, part_2 = fencing_prices(grid)
    print(f"{part_1 = } {part_2 = }")


if __name__ == "__main__":
    main()
