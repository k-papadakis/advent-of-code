from itertools import takewhile


def read_data(input_file):
    with open(input_file) as f:
        while pair := tuple(map(eval, takewhile(lambda line: line != '\n', f))):
            yield pair


def compare(a, b):
    if isinstance(a, int) and isinstance(b, int):
        return a <= b

    if isinstance(a, int):
        return compare(a, b[0]) if b else True

    if isinstance(b, int):
        return not compare(b, a)

    # From this point, both a and b are lists.

    if not a:
        return True

    if not b:
        return not a

    return len(a) <= len(b) and all(compare(x, y) for x, y in zip(a, b))


def test_int_list():
    assert compare(1, [2, 3, 4])
    assert not compare([2, 3, 4], 1)


def test_int_int():
    assert compare(1, 2)
    assert not compare(2, 1)


def test_list_list():
    assert compare([1, 3], [2, 4, 5])
    assert not compare([1, 3, 5], [2, 4])
    assert not compare([1, 2, 3], [5, 0])


# for i, (a, b) in enumerate(read_data('mini.txt'), 1):
#     print(i, compare(a, b))

print(sum(i for i, (a, b) in enumerate(read_data('input.txt'), 1) if compare(a, b)))
