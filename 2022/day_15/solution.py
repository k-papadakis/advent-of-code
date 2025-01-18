import re

type Pair = tuple[int, int]


def read_input(file_path: str) -> list[tuple[Pair, Pair]]:
    p = re.compile(
        r"^Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)$",
        re.MULTILINE,
    )
    with open(file_path) as f:
        return [
            ((int(m[2]), int(m[1])), (int(m[4]), int(m[3])))
            for m in p.finditer(f.read())
        ]


def find_interval(sensor: Pair, beacon: Pair, row: int) -> Pair | None:
    distance_to_beacon = abs(sensor[0] - beacon[0]) + abs(sensor[1] - beacon[1])
    distance_to_row = abs(sensor[0] - row)
    center = sensor[1]
    radius = distance_to_beacon - distance_to_row
    if radius >= 0:
        return (center - radius, center + radius)
    return None


def unite_intervals(intervals: list[Pair]) -> list[Pair]:
    union: list[Pair] = []
    for a, b in sorted(intervals):
        if union and union[-1][1] + 1 >= a:
            union[-1] = (union[-1][0], max(union[-1][1], b))
        else:
            union.append((a, b))
    return union


def non_beacon_positions(data: list[tuple[Pair, Pair]], row: int) -> int:
    intervals = [
        interval
        for sensor, beacon in data
        if (interval := find_interval(sensor, beacon, row)) is not None
    ]
    union = unite_intervals(intervals)
    coverage = sum(b - a + 1 for a, b in union)
    beacons = {beacon for _, beacon in data}
    num_beacon_positions = sum(
        any(beacon[0] == row and a <= beacon[1] <= b for a, b in intervals)
        for beacon in beacons
    )
    return coverage - num_beacon_positions


def main():
    import sys

    file_path = sys.argv[1]
    row = int(sys.argv[2])
    data = read_input(file_path)
    part_1 = non_beacon_positions(data, row)
    print(part_1)


if __name__ == "__main__":
    main()
