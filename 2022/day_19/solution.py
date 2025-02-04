# https://youtu.be/5rb0vvJ7NCY
import math
import re
from collections.abc import Generator
from dataclasses import dataclass
from functools import cached_property
from typing import Self

# Robot and Material Types
ORE, CLAY, OBSIDIAN, GEODE = range(4)
# blueprint[i][j] is the requirement of material_j in making robot_i
type Blueprint = list[list[int]]


@dataclass
class State:
    blueprint: Blueprint
    remaining_time: int
    robots: list[int]
    materials: list[int]
    idled: list[bool]

    @classmethod
    def new(cls, blueprint: Blueprint, remaining_time: int) -> Self:
        n_robots = len(blueprint)
        n_materials = len(blueprint[0])
        robots = [0] * n_robots
        robots[ORE] = 1
        materials = [0] * n_materials
        idled = [False] * n_robots
        return cls(blueprint, remaining_time, robots, materials, idled)

    def children(self, max_geodes: int) -> Generator[Self]:
        if not self.best_case_can_beat(max_geodes):
            return
        if self.can_build(GEODE):
            yield self.build(GEODE)
            return
        for robot in ORE, CLAY, OBSIDIAN:
            if (
                self.can_build(robot)
                and not self.idled[robot]
                and not self.enough(robot)
            ):
                yield self.build(robot)
        if not all(self.idled):
            yield self.idle()

    def build(self, robot: int) -> Self:
        remaining_time = self.remaining_time - 1
        robots = self.robots[:]
        robots[robot] += 1
        materials = [
            cur - req + r
            for cur, req, r in zip(self.materials, self.blueprint[robot], self.robots)
        ]
        idled = [False] * len(self.idled)
        return type(self)(
            self.blueprint,
            remaining_time,
            robots,
            materials,
            idled,
        )

    def idle(self) -> Self:
        remaining_time = self.remaining_time - 1
        materials = [cur + r for cur, r in zip(self.materials, self.robots)]
        idled = [
            self.idled[robot] or self.can_build(robot)
            for robot in range(len(self.idled))
        ]
        return type(self)(
            self.blueprint,
            remaining_time,
            self.robots,
            materials,
            idled,
        )

    def can_build(self, robot: int) -> bool:
        return all(
            cur >= req for cur, req in zip(self.materials, self.blueprint[robot])
        )

    @cached_property
    def max_materials(self) -> list[int]:
        return [
            max(self.blueprint[i][j] for i in range(len(self.blueprint)))
            for j in range(len(self.blueprint[0]))
        ]

    def enough(self, robot: int) -> bool:
        return self.robots[robot] >= self.max_materials[robot]

    def best_case_can_beat(self, max_geodes: int) -> bool:
        t = self.remaining_time
        best_case = (
            self.materials[GEODE]
            + self.robots[GEODE] * t
            + (t - 1) * t // 2  # Creating a new geode every minute
        )
        return best_case >= max_geodes


def maximize_geodes(blueprint: Blueprint, remaining_time: int) -> int:
    initial_state = State.new(blueprint, remaining_time)
    stack = [initial_state]
    max_geodes = 0
    while stack:
        state = stack.pop()
        if state.remaining_time == 0:
            max_geodes = max(max_geodes, state.materials[GEODE])
            continue
        stack.extend(state.children(max_geodes))
    return max_geodes


def read_input(file_path: str) -> dict[int, Blueprint]:
    pattern = re.compile(
        " ".join(
            [
                r"(?m)^Blueprint (\d+):",
                r"Each ore robot costs (\d+) ore.",
                r"Each clay robot costs (\d+) ore.",
                r"Each obsidian robot costs (\d+) ore and (\d+) clay.",
                r"Each geode robot costs (\d+) ore and (\d+) obsidian.$",
            ]
        )
    )
    with open(file_path) as f:
        blueprints: dict[int, Blueprint] = {}
        for i, line in enumerate(f, 1):
            m = pattern.match(line)
            if m is None:
                raise ValueError(f"{f.name}:{i} invalid blueprint: {line!r}")
            g = list(map(int, m.groups()))
            blueprints[g[0]] = [
                [g[1], 0, 0, 0],
                [g[2], 0, 0, 0],
                [g[3], g[4], 0, 0],
                [g[5], 0, g[6], 0],
            ]
    return blueprints


def main() -> None:
    import sys

    file_path = sys.argv[1]
    blueprints = read_input(file_path)
    part_1 = sum(
        blueprint_id * maximize_geodes(blueprint, 24)
        for blueprint_id, blueprint in blueprints.items()
    )
    part_2 = math.prod(maximize_geodes(blueprints[i], 32) for i in range(1, 4))
    print(f"{part_1 = } {part_2 = }")


if __name__ == "__main__":
    main()
