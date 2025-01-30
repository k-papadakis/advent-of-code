type Point = tuple[int, int, int]


def read_input(file_path: str) -> set[Point]:
    points: set[Point] = set()
    with open(file_path) as f:
        for line in f:
            x, y, z = map(int, line.split(","))
            points.add((x, y, z))
    return points


def approximate_surface_area(points: set[Point]) -> int:
    DIRECTIONS = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]
    num_interior = 0
    for x, y, z in points:
        for dx, dy, dz in DIRECTIONS:
            if (x + dx, y + dy, z + dz) in points:
                num_interior += 1
    return len(points) * 6 - num_interior


def main() -> None:
    import sys

    file_path = sys.argv[1]
    points = read_input(file_path)
    part_1 = approximate_surface_area(points)
    print(part_1)


if __name__ == "__main__":
    main()
