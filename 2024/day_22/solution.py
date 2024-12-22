from collections.abc import Generator
from collections import deque
from itertools import islice, pairwise
import sys


def read_input(file_path: str) -> list[int]:
    with open(file_path) as f:
        return list(map(int, f))


def mix_and_prune(x: int, secret: int) -> int:
    return (x ^ secret) & ((1 << 24) - 1)


def create_rng(seed: int) -> Generator[int]:
    t = seed
    while True:
        yield t
        t = mix_and_prune(t << 6, t)
        t = mix_and_prune(t >> 5, t)
        t = mix_and_prune(t << 11, t)


def max_bananas(seeds: list[int]) -> int:
    cache: dict[tuple[int, int, int, int], dict[int, int]] = {}
    for i, seed in enumerate(seeds):
        rng = create_rng(seed)
        prices = (x % 10 for x in rng)
        deltas: deque[int] = deque(maxlen=4)
        for x, y in islice(pairwise(prices), 2000):
            deltas.append(y - x)
            if len(deltas) < 4:
                continue
            t = tuple(deltas)
            assert len(t) == 4
            if t not in cache:
                cache[t] = {}
            if i not in cache[t]:
                cache[t][i] = y
    return max(sum(v.values()) for v in cache.values())


def main():
    file_path = sys.argv[1]
    seeds = read_input(file_path)
    part_1 = sum(next(islice(rng, 2_000, None)) for rng in map(create_rng, seeds))
    part_2 = max_bananas(seeds)
    print(f"{part_1 = } {part_2 = }")


if __name__ == "__main__":
    main()
