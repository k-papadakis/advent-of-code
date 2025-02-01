type Point = tuple[int, int, int]

DIRECTIONS = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]


def read_input(file_path: str) -> set[Point]:
    points: set[Point] = set()
    with open(file_path) as f:
        for line in f:
            x, y, z = map(int, line.split(","))
            points.add((x, y, z))
    return points


def approximate_surface_area(points: set[Point]) -> int:
    num_interior = 0
    for x, y, z in points:
        for dx, dy, dz in DIRECTIONS:
            if (x + dx, y + dy, z + dz) in points:
                num_interior += 1
    return len(points) * 6 - num_interior


def find_boundary(points: set[Point]) -> tuple[Point, Point]:
    min_point = (
        min(x for x, _, _ in points) - 1,
        min(y for _, y, _ in points) - 1,
        min(z for _, _, z in points) - 1,
    )
    max_point = (
        max(x for x, _, _ in points) + 1,
        max(y for _, y, _ in points) + 1,
        max(z for _, _, z in points) + 1,
    )
    return min_point, max_point


def calculate_surface_area(points: set[Point]) -> int:
    (x_min, y_min, z_min), (x_max, y_max, z_max) = find_boundary(points)
    stack: list[Point] = [(x_min, y_min, z_min)]
    filled: set[Point] = set()
    area = 0
    while stack:
        x, y, z = stack.pop()
        if not (x_min <= x <= x_max and y_min <= y <= y_max and z_min <= z <= z_max):
            continue
        if (x, y, z) in points:
            area += 1
            continue
        if (x, y, z) in filled:
            continue
        filled.add((x, y, z))
        stack.extend((x + dx, y + dy, z + dz) for dx, dy, dz in DIRECTIONS)
    return area


def main() -> None:
    import sys

    file_path = sys.argv[1]
    points = read_input(file_path)
    part_1 = approximate_surface_area(points)
    part_2 = calculate_surface_area(points)
    print(f"{part_1 = } {part_2 = }")


if __name__ == "__main__":
    main()
