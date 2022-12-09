# %%

import math


def read_data(input_file):
    with open(input_file) as f:
        return [list(map(int, line)) for line in f.read().splitlines()]


def iter_rows(m, n):
    for i in range(m):
        yield ((i, j) for j in range(n))


def iter_cols(m, n):
    for j in range(n):
        yield ((i, j) for i in range(m))


def iter_rows_reversed(m, n):
    for i in range(m):
        yield ((i, j) for j in reversed(range(n)))


def iter_cols_reversed(m, n):
    for j in range(n):
        yield ((i, j) for i in reversed(range(m)))


def visibility(row_or_col_iter, array, visible):
    for indices in row_or_col_iter:
        max_so_far = -math.inf
        for i, j in indices:
            if array[i][j] > max_so_far:
                max_so_far = array[i][j]
                visible[i][j] = True


def part1(array):
    m, n = len(array), len(array[0])
    visible = [[False for _ in range(n)] for _ in range(m)]

    for gen in iter_rows(m, n), iter_cols(m, n), iter_rows_reversed(m, n), iter_cols_reversed(m, n):
        visibility(gen, array, visible)

    return sum(map(sum, visible))


# def find_visibility(array, i, j, direction):

#     m, n = len(array), len(array[0])
#     n_steps = 0
#     x, y = i, j

#     while (x := x + direction[0]) in range(m) and (y := y + direction[1]) in range(n):
#         n_steps += 1
#         if array[x][y] >= array[i][j]:
#             break

#     return n_steps


# def part2(array):
#     m, n = len(array), len(array[0])
#     directions = (0, 1), (1, 0), (-1, 0), (0, -1)

#     ret = max(
#         math.prod(find_visibility(array, i, j, direction)
#                   for direction in directions)
#         for i in range(m)
#         for j in range(n)
#     )

#     return ret


# def main():
#     a = read_data('input.txt')
#     print(f'part1: {part1(a)}\npart2: {part2(a)}')


# if __name__ == '__main__':
#     main()


# %%
a = read_data('mini.txt')
m, n = len(a), len(a[0])
dists = [[1 for _ in range(n)] for _ in range(m)]

for row in iter_rows(m, n):
    
    stack = []
    
    for i, j in row:
        
        while stack and stack[-1][0] < a[i][j]:
            stack.pop()
        
        dists[i][j] *= j - (stack[-1][1] if stack else -1)
        stack.append((a[i][j], j))

dists
