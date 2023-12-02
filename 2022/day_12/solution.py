from collections import deque


def read_data(input_file) -> tuple[list[list[str]], tuple[int, int], tuple[int, int]]:
    with open(input_file) as f:
        grid_rows = f.read().splitlines()

    flattened = ''.join(grid_rows)
    n_cols = len(grid_rows[0])

    source = divmod(flattened.index('S'), n_cols)
    target = divmod(flattened.index('E'), n_cols)

    grid = list(map(list, grid_rows))

    grid[source[0]][source[1]] = 'a'
    grid[target[0]][target[1]] = 'z'

    return grid, source, target


def bfs(grid: list[list[str]], source: tuple[int, int], target: str | tuple[int, int], reverse: bool) -> int:

    directions = (-1, 0), (0, -1), (1, 0), (0, 1)
    m, n = len(grid), len(grid[0])

    queue = deque([source])
    visited = set()
    level = -1

    while queue:

        level += 1

        for _ in range(len(queue)):

            cur = queue.popleft()

            if isinstance(target, tuple):
                if cur == target:
                    return level
            else:
                if grid[cur[0]][cur[1]] == target:
                    return level

            if cur in visited:
                continue
            visited.add(cur)

            for direction in directions:
                neighbor = cur[0] + direction[0], cur[1] + direction[1]
                if 0 <= neighbor[0] < m and 0 <= neighbor[1] < n:

                    diff = ord(grid[neighbor[0]][neighbor[1]]) - ord(grid[cur[0]][cur[1]])
                    if reverse:
                        diff *= -1

                    if diff <= 1:
                        queue.append(neighbor)

    return -1


def main():
    grid, source, target = read_data('input.txt')
    part1 = bfs(grid, source, target, False)
    part2 = bfs(grid, target, 'a', True)
    print(f'part1: {part1}\npart2: {part2}')


if __name__ == '__main__':
    main()
