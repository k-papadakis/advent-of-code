import sys


def read_input(file_path: str) -> list[tuple[int, list[int]]]:
    equations: list[tuple[int, list[int]]] = []
    with open(file_path) as f:
        for line in f:
            expected_str, numbers_str = line.split(":", maxsplit=1)
            expected = int(expected_str)
            numbers = list(map(int, numbers_str.split()))
            equations.append((expected, numbers))
    return equations


def concat(left: int, right: int) -> int:
    t = right
    while t != 0:
        t = t // 10
        left = left * 10
    return left + right


def is_valid(expected: int, nums: list[int], with_concat: bool) -> bool:
    stack = [(1, nums[0])]
    while stack:
        level, evaluation = stack.pop()
        if level == len(nums):
            if evaluation == expected:
                return True
        elif evaluation > expected:  # perf
            continue
        else:
            stack.append((level + 1, evaluation * nums[level]))
            stack.append((level + 1, evaluation + nums[level]))
            if with_concat:
                stack.append((level + 1, concat(evaluation, nums[level])))

    return False


def main():
    file_path = sys.argv[1]
    equations = read_input(file_path)
    part_1 = sum(
        expected
        for expected, nums in equations
        if is_valid(expected, nums, with_concat=False)
    )
    part_2 = sum(
        expected
        for expected, nums in equations
        if is_valid(expected, nums, with_concat=True)
    )
    print(f"{part_1 = } {part_2 = }")


if __name__ == "__main__":
    main()
