from collections import deque


def read_data(input_file) -> list[list[int]]:
    with open(input_file) as f:
        grid = f.read().splitlines()

    flattened = ''.join(grid)
    n_cols = len(grid[0])

    source = divmod(flattened.index('S'), n_cols)
    target = divmod(flattened.index('E'), n_cols)

    return grid, source, target


def bfs(grid, source, target):
    elevation = {c: i for i, c in enumerate('abcdefghijklmnopqrstuvwxyz')}
    elevation['S'] = elevation['a']
    elevation['E'] = elevation['z']

    directions = (-1, 0), (0, -1), (1, 0), (0, 1)
    m, n = len(grid), len(grid[0])

    queue = deque([source])
    visited = set()
    level = -1

    while queue:
        level += 1

        for _ in range(len(queue)):

            cur = queue.popleft()

            if cur == target:
                return level

            if cur in visited:
                continue
            visited.add(cur)

            for direction in directions:
                neighbor = cur[0] + direction[0], cur[1] + direction[1]
                if (
                    0 <= neighbor[0] < m and 0 <= neighbor[1] < n and
                    elevation[grid[neighbor[0]][neighbor[1]]] - elevation[grid[cur[0]][cur[1]]] <= 1
                ):
                    queue.append(neighbor)

    return -1


print(bfs(*read_data('input.txt')))
