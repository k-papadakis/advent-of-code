from collections import deque


def read_data(input_file):
    with open(input_file) as f:
        while (c := f.read(1)) != '\n':
            yield c


def first_n_unique(iterable, n):
    queue = deque()
    counter = {}

    for i, right in enumerate(iterable, 1):

        queue.append(right)
        counter[right] = counter.get(right, 0) + 1

        if len(queue) < n:
            continue

        if len(counter) == n:
            return i

        left = queue.popleft()
        counter[left] -= 1
        if counter[left] == 0:
            counter.pop(left)


def main():
    part1 = first_n_unique(read_data('input.txt'), 4)
    part2 = first_n_unique(read_data('input.txt'), 14)
    print(f"part1: {part1}\npart2: {part2}")


if __name__ == '__main__':
    main()
