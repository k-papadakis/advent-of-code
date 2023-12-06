import bisect
import math


def read_input():
    with open("input.txt") as f:
        s = f.read()

    times_str, distances_str = s.splitlines()

    times = list(map(int, times_str.lstrip("Time:").split()))
    distances = list(map(int, distances_str.lstrip("Distance:").split()))

    time = int(times_str.lstrip("Time:").replace(" ", ""))
    distance = int(distances_str.lstrip("Distance:").replace(" ", ""))

    return times, distances, time, distance


def num_winning_ways(available_time: int, record_distance: int) -> int:
    def distance_covered(hold_time: int) -> int:
        # Reaches maximum at available_time/2 and is symmetric around it.
        return hold_time * (available_time - hold_time)

    min_hold = bisect.bisect_right(
        range(0, available_time // 2 + 1), record_distance, key=distance_covered
    )
    return available_time - 2 * min_hold + 1


def main():
    times, distances, time, distance = read_input()

    part_1 = math.prod(map(num_winning_ways, times, distances))
    part_2 = num_winning_ways(time, distance)

    print(f"{part_1 = }, {part_2 = }")


if __name__ == "__main__":
    main()
