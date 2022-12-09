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


def part1(array):
    m, n = len(array), len(array[0])
    visible = [[False for _ in range(n)] for _ in range(m)]

    for gen in iter_rows(m, n), iter_cols(m, n), iter_rows_reversed(m, n), iter_cols_reversed(m, n):
        for indices in gen:
            max_so_far = float('-Infinity')
            for i, j in indices:
                if array[i][j] > max_so_far:
                    max_so_far = array[i][j]
                    visible[i][j] = True

    return sum(map(sum, visible))


def part2(array):
    m, n = len(array), len(array[0])
    dists = [[1 for _ in range(n)] for _ in range(m)]

    for row in iter_rows(m, n):

        stack = []

        for i, j in row:

            while stack and stack[-1][0] < array[i][j]:
                stack.pop()

            dists[i][j] *= (j - stack[-1][1]) if stack else j
            stack.append((array[i][j], j))

    for col in iter_cols(m, n):

        stack = []

        for i, j in col:

            while stack and stack[-1][0] < array[i][j]:
                stack.pop()

            dists[i][j] *= (i - stack[-1][1]) if stack else i
            stack.append((array[i][j], i))

    for reversed_row in iter_rows_reversed(m, n):

        stack = []

        for i, j in reversed_row:

            while stack and stack[-1][0] < array[i][j]:
                stack.pop()

            dists[i][j] *= (stack[-1][1] - j) if stack else n - 1 - j
            stack.append((array[i][j], j))

    for reversed_col in iter_cols_reversed(m, n):

        stack = []

        for i, j in reversed_col:

            while stack and stack[-1][0] < array[i][j]:
                stack.pop()

            dists[i][j] *= (stack[-1][1] - i) if stack else m - 1 - i
            stack.append((array[i][j], i))

    return max(map(max, dists))


def main():
    a = read_data('input.txt')
    print(f'part1: {part1(a)}\npart2: {part2(a)}')


if __name__ == '__main__':
    main()
