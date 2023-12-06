type IntervalCollection = list[tuple[int, int]]
type Almanac = list[tuple[IntervalCollection, IntervalCollection]]


def intervals_map(p: IntervalCollection, q: IntervalCollection, x: int):
    for u, v in zip(p, q, strict=True):
        if u[0] <= x <= u[1]:
            return v[0] + (x - u[0])
    return x


def almanac_map(almanac: Almanac, x: int) -> int:
    res = x
    for p, q in almanac:
        res = intervals_map(p, q, res)
    return res


def read_input() -> (
    tuple[list[int], list[tuple[IntervalCollection, IntervalCollection]]]
):
    with open("input.txt") as f:
        seeds_str = f.readline()
        f.readline()
        almanac_str = f.read()

    seeds = list(map(int, seeds_str.lstrip("seeds:").split()))

    almanac: Almanac = []
    for chunk in almanac_str.split("\n\n"):
        c1: IntervalCollection = []
        c2: IntervalCollection = []
        for line in chunk.splitlines()[1:]:
            dest_start, source_start, length = map(int, line.split())
            c1.append((source_start, source_start + length))
            c2.append((dest_start, dest_start + length))

        almanac.append((c1, c2))

    return seeds, almanac


def main() -> None:
    seeds, almanac = read_input()
    part_1 = min(almanac_map(almanac, x) for x in seeds)

    print(f"{part_1 = }")


if __name__ == "__main__":
    main()
