from collections import deque
import sys


type Pair = tuple[int, int]


def read_input(file_path: str) -> list[Pair]:
    blockers: list[Pair] = []
    with open(file_path) as f:
        for line in f:
            x, y = map(int, line.split(",", maxsplit=1))
            blockers.append((x, y))
    return blockers


def min_steps(size: Pair, blockers: dict[Pair, int], n_fallen: int) -> int | None:
    q = deque([(0, 0)])
    level = 0
    visited = {(0, 0)}
    while q:
        for _ in range(len(q)):
            x, y = q.popleft()
            if (x, y) == size:
                return level

            for dx, dy in (1, 0), (0, 1), (-1, 0), (0, -1):
                if (
                    0 <= (xx := x + dx) <= size[0]
                    and 0 <= (yy := y + dy) <= size[1]
                    and (xx, yy) not in visited
                    and ((xx, yy) not in blockers or blockers[xx, yy] >= n_fallen)
                ):
                    q.append((xx, yy))
                    visited.add((xx, yy))
        level += 1
    return None


def full_block_pos(size: Pair, blockers: dict[Pair, int]) -> int:
    lo = 0
    hi = len(blockers)
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        steps = min_steps(size, blockers, mid)
        if steps is None:
            hi = mid - 1
        else:
            lo = mid + 1
    return hi


def main():
    size = (70, 70)
    file_path = sys.argv[1]
    blockers_list = list(read_input(file_path))
    blockers = {p: i for i, p in enumerate(blockers_list)}
    part_1 = min_steps(size, blockers, 1024)
    part_2 = blockers_list[full_block_pos(size, blockers)]
    print(f"part_1 = {part_1} part_2 = {part_2[0]},{part_2[1]}")


if __name__ == "__main__":
    main()
