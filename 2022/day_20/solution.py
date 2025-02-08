from collections import deque


def read_input(file_path: str) -> list[int]:
    with open(file_path) as f:
        return list(map(int, f))


def mix(
    numbers: list[int], *, decryption_key: int | None = None, niter: int = 1
) -> list[int]:
    n = len(numbers)
    if decryption_key is not None:
        numbers = [shift * decryption_key for shift in numbers]
    q = deque(enumerate(numbers))
    for _ in range(niter):
        for i in range(n):
            qpos = next(qpos for qpos, (npos, _) in enumerate(q) if npos == i)
            q.rotate(-qpos)
            ii, shift = q.popleft()
            assert i == ii
            q.rotate(-(shift % (n - 1)))
            q.append((i, shift))
    return [shift for _, shift in q]


def grove_coordinates(numbers: list[int]) -> tuple[int, int, int]:
    zero_pos = numbers.index(0)
    x, y, z = (
        numbers[(zero_pos + shift) % len(numbers)] for shift in (1000, 2000, 3000)
    )
    return x, y, z


def main() -> None:
    import sys

    file_path = sys.argv[1]
    numbers = read_input(file_path)
    part_1 = sum(grove_coordinates(mix(numbers)))
    part_2 = sum(grove_coordinates(mix(numbers, decryption_key=811589153, niter=10)))

    print(f"{part_1 = } {part_2 = }")


if __name__ == "__main__":
    main()
