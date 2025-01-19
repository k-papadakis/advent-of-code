# See also this amazing solution
# https://github.com/Fitli/AoC2022/blob/62bef2e643343c4948a8e67d0ca9396ee756d321/15.py
import re

type Pair = tuple[int, int]
type Rectangle = tuple[Pair, Pair]


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


def l1(u: Pair, v: Pair) -> int:
    return abs(u[0] - v[0]) + abs(u[1] - v[1])


def find_interval(sensor: Pair, beacon: Pair, row: int) -> Pair | None:
    distance_to_beacon = l1(sensor, beacon)
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


def rectangle_is_valid(rectangle: Rectangle) -> bool:
    (min_x, min_y), (max_x, max_y) = rectangle
    return min_x <= max_x and min_y <= max_y


def rectangle_split(rectangle: Rectangle, point: Pair) -> list[Rectangle]:
    (min_x, min_y), (max_x, max_y) = rectangle
    x, y = point

    point_is_within_rectangle = (min_x <= x <= max_x) and (min_y <= y <= max_y)
    if not point_is_within_rectangle:
        return []

    sub_rectangles: list[Rectangle] = [
        ((min_x, min_y), (x, y)),  # top left
        ((x + 1, min_y), (max_x, y)),  # bottom left
        ((min_x, y + 1), (x, max_y)),  # top right
        ((x + 1, y + 1), (max_x, max_y)),  # bottom right
    ]

    return list(filter(rectangle_is_valid, sub_rectangles))


def rectangle_corners(rectangle: Rectangle) -> tuple[Pair, Pair, Pair, Pair]:
    (x_min, y_min), (x_max, y_max) = rectangle
    return (
        (x_min, y_min),
        (x_min, y_max),
        (x_max, y_min),
        (x_max, y_max),
    )


def rectangle_contains_undetected(rectangle: Rectangle, sensor: Pair, beacon: Pair):
    d = l1(sensor, beacon)
    return any(l1(sensor, corner) > d for corner in rectangle_corners(rectangle))


def find_undetected_beacon(
    data: list[tuple[Pair, Pair]], rectangle: Rectangle
) -> Pair | None:
    # Quarternary Search
    stack: list[Rectangle] = [rectangle]
    while stack:
        r = stack.pop()

        if r[0] == r[1]:
            if all(l1(sensor, r[0]) > l1(sensor, beacon) for sensor, beacon in data):
                return r[0]
            continue

        mid = (
            (r[0][0] + r[1][0]) // 2,
            (r[0][1] + r[1][1]) // 2,
        )
        for rr in rectangle_split(r, mid):
            if all(
                rectangle_contains_undetected(rr, beacon, sensor)
                for beacon, sensor in data
            ):
                stack.append(rr)
    return None


def main():
    import sys

    file_path = sys.argv[1]
    ROW = 2_000_000
    RECTANGLE = ((0, 0), (4_000_000, 4_000_000))
    data = read_input(file_path)

    part_1 = non_beacon_positions(data, ROW)

    undetected_beacon = find_undetected_beacon(data, RECTANGLE)
    assert undetected_beacon is not None
    part_2 = 4_000_000 * undetected_beacon[1] + undetected_beacon[0]

    print(f"{part_1 = } {part_2 = }")


if __name__ == "__main__":
    main()
