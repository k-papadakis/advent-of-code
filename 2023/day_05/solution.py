type Interval = tuple[int, int]
type IntervalCollection = list[Interval]
type Almanac = list[tuple[IntervalCollection, IntervalCollection]]


def union(p: IntervalCollection) -> IntervalCollection:
    p_sorted = sorted(p)

    res = [p_sorted[0]]

    for x, y in p_sorted[1:]:
        a, b = res[-1]

        if x <= b:
            res[-1] = (a, max(b, y))
        else:
            res.append((x, y))

    return res


def partition(
    p: IntervalCollection, partitioner: Interval
) -> tuple[IntervalCollection, IntervalCollection]:
    intersections: IntervalCollection = []
    complements: IntervalCollection = []

    a, b = partitioner

    for x, y in p:
        s, t = max(a, x), min(b, y)

        if s <= t:
            intersections.append((s, t))  # intersection
            if x < s:
                complements.append((x, s - 1))  # left complement
            if t < y:
                complements.append((t + 1, y))  # right complement
        else:
            complements.append((x, y))  # complement

    return intersections, complements


def shift(u: Interval, v: Interval, x: int) -> int:
    return v[0] + (x - u[0])


def map_int(p: IntervalCollection, q: IntervalCollection, x: int) -> int:
    for u, v in zip(p, q, strict=True):
        if u[0] <= x <= u[1]:
            return shift(u, v, x)
    return x


def almanac_map_int(almanac: Almanac, x: int) -> int:
    res = x
    for p, q in almanac:
        res = map_int(p, q, res)
    return res


def map_interval_collections(
    p: IntervalCollection, q: IntervalCollection, intervals: IntervalCollection
) -> IntervalCollection:
    res: IntervalCollection = []

    for u, v in zip(p, q):
        intersected, intervals = partition(intervals, u)
        res.extend((shift(u, v, x), shift(u, v, y)) for x, y in intersected)

    res.extend(intervals)

    return union(res)


def almanac_map_range(
    almanac: Almanac, intervals: IntervalCollection
) -> IntervalCollection:
    res = intervals
    for p, q in almanac:
        res = map_interval_collections(p, q, res)
    return res


def read_input() -> tuple[list[int], IntervalCollection, Almanac]:
    with open("input.txt") as f:
        seeds_str = f.readline()
        f.readline()
        almanac_str = f.read()

    seeds = list(map(int, seeds_str.lstrip("seeds:").split()))
    seed_ranges = [
        (start, start + length)
        for start, length in zip(seeds[:-1:2], seeds[1::2], strict=True)
    ]

    almanac: Almanac = []
    for chunk in almanac_str.split("\n\n"):
        c1: IntervalCollection = []
        c2: IntervalCollection = []

        for line in chunk.splitlines()[1:]:
            dest_start, source_start, length = map(int, line.split())
            c1.append((source_start, source_start + length))
            c2.append((dest_start, dest_start + length))

        almanac.append((c1, c2))

    return seeds, seed_ranges, almanac


def main() -> None:
    seeds, seed_ranges, almanac = read_input()

    part_1 = min(almanac_map_int(almanac, x) for x in seeds)
    part_2 = min(a for a, _ in almanac_map_range(almanac, seed_ranges))
    print(f"{part_1 = }, {part_2 = }")


if __name__ == "__main__":
    main()
