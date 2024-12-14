from dataclasses import dataclass, replace
import re
import sys
from typing import Self
import numpy as np
from PIL import Image


@dataclass(slots=True)
class Robot:
    position: tuple[int, int]
    velocity: tuple[int, int]

    def move(self, steps: int, bounds: tuple[int, int]) -> Self:
        x, y = self.position
        dx, dy = self.velocity
        m, n = bounds
        new_x = (x + (steps % m) * dx) % m
        new_y = (y + (steps % n) * dy) % n
        return replace(self, position=(new_x, new_y))

    def quadrant(self, bounds: tuple[int, int]) -> int | None:
        x, y = self.position
        m, n = bounds
        if m % 2 == 1 and x == m // 2 or n % 2 == 1 and y == n // 2:
            return None
        return 2 * (x > m // 2) + (y > n // 2)


def robots_density(robots: list[Robot]) -> float:
    n = len(robots)
    mean_x = sum(r.position[0] for r in robots) / n
    mean_y = sum(r.position[1] for r in robots) / n
    deviation = (
        sum(abs(r.position[0] - mean_x) + abs(r.position[1] - mean_y) for r in robots)
    ) / n
    return deviation


def plot_grid(robots: list[Robot], bounds: tuple[int, int], steps: int) -> None:
    grid = np.zeros(bounds, dtype=np.bool_)
    for robot in robots:
        i, j = robot.move(steps, bounds).position
        grid[i, j] = 1
    Image.fromarray(grid).save(f"{steps:05d}.png")


def safety_factor(robots: list[Robot], bounds: tuple[int, int], steps: int) -> int:
    quadrants = [0, 0, 0, 0]
    for robot in robots:
        q = robot.move(steps, bounds).quadrant((bounds))
        if q is not None:
            quadrants[q] += 1
    return quadrants[0] * quadrants[1] * quadrants[2] * quadrants[3]


def read_input(file_path: str) -> list[Robot]:
    p = re.compile(r"p=(\d+),(\d+) v=(-?\d+),(-?\d+)")
    robots: list[Robot] = []
    with open(file_path) as f:
        for line in f:
            m = p.match(line)
            assert m is not None
            y, x, dy, dx = map(int, m.groups())
            robots.append(Robot((x, y), (dx, dy)))
    return robots


def main():
    file_path = sys.argv[1]
    bounds = (103, 101)
    robots = read_input(file_path)

    part_1 = safety_factor(robots, bounds, 100)
    _, part_2 = min(
        (
            robots_density([robot.move(steps, bounds) for robot in robots]),
            steps,
        )
        for steps in range(bounds[0] * bounds[1])
    )

    plot_grid(robots, bounds, part_2)
    print(f"{part_1 = } {part_2 = }")


if __name__ == "__main__":
    main()
